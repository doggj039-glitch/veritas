#!/usr/bin/env python3
"""
VERITAS local bridge — connects the Library Workstation front-end to the real engine.

Runs entirely on your machine (127.0.0.1), fully offline, no external calls. Serves the
app's files AND exposes the gate + agents as a tiny JSON API, so the Ask box actually
resolves founding-era meaning and the agents actually answer from their sources.

  GET /api/resolve?term=<text>   -> Blackletter gate: verbatim 1773 def, verdict,
                                    etymology, founding usage, the cases that construed it
  GET /api/ask?agent=<n>&q=<q>   -> a grounded agent's answer (verbatim, cited)
  GET /api/agents                -> the agent roster
  GET /<file>                    -> the app (VERITAS.html, books/, assets)

Usage:  python3 veritas_server.py [port]   (default 8737)
"""
import json, sys, re, os, subprocess, signal, shlex, bisect, sqlite3, urllib.request, urllib.error
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs, unquote
from pathlib import Path

def _veritas_root():
    """Honor VERITAS_ROOT if set (Android/Chaquopy), else self-locate the app folder
    by walking up from this file (desktop / Windows .exe / USB — runs from any path)."""
    env = os.environ.get("VERITAS_ROOT")
    if env:
        return Path(env)
    _p = Path(__file__).resolve()
    for _q in (_p, *_p.parents):
        if (_q / "00_APP").is_dir() and (_q / "02_GATE_BLACKLETTER").is_dir():
            return _q
    return Path("/home/noneya/Projects/VERITAS v.3")


ROOT = _veritas_root()
APP = ROOT / "00_APP"
sys.path.insert(0, str(ROOT / "02_GATE_BLACKLETTER" / "gate"))
sys.path.insert(0, str(ROOT / "10_AGENTS"))

from blackletter_gate import BlackletterGate      # noqa: E402
from blackletter_lexer import lex                 # noqa: E402
from agent_core import AgentCompartment, respond, agent_available  # noqa: E402
import veritas_reason                              # grounded reasoning tier (Path B); stdlib-only

# ---- concordance: every founding-era occurrence of a word across the corpus ----
try:
    from blackletter_usage import FoundingUsage       # noqa: E402
    _USAGE = FoundingUsage()
except Exception:
    _USAGE = None
# approximate publication year per source (for the drift/time dimension of the concordance)
_SRC_YEAR = [
    ("declaration", 1776), ("bill of rights", 1791), ("constitution", 1787),
    ("federalist", 1788), ("anti-federalist", 1788), ("antifederalist", 1788),
    ("elliot", 1788), ("farrand", 1787), ("madison", 1787),
    ("story", 1833), ("rawle", 1829), ("blackstone", 1769),
    ("montesquieu", 1748), ("locke", 1689),
]
def _src_year(src):
    s = (src or "").lower()
    for key, yr in _SRC_YEAR:
        if key in s:
            return yr
    return None
def _concordance(word):
    if not _USAGE:
        return {"word": word, "count": 0, "rows": [], "error": "usage corpus unavailable"}
    rows = _USAGE.concordance(word, cap=250)
    for r in rows:
        r["year"] = _src_year(r.get("source"))
    rows.sort(key=lambda r: (r.get("year") or 9999, r.get("source") or ""))
    return {"word": word, "count": len(rows), "rows": rows}

# ---- readable dictionaries: browse Johnson 1773 baseline in order, drift on demand ----
_DICT_KEYS = None
def _dict_keys():
    global _DICT_KEYS
    if _DICT_KEYS is None:
        _DICT_KEYS = sorted(GATE.entries.keys())
    return _DICT_KEYS
def _entry_view(e):
    john = ""; ety = ""; drift = []
    for s in e.get("sources", []):
        role = s.get("role"); txt = (s.get("verbatim_text") or "").strip()
        if role == "johnson_1773":
            john = txt
        elif role == "etymology":
            ety = txt
        elif s.get("tier") == "drift":
            drift.append({"role": role, "source": s.get("source"), "year": s.get("year"),
                          "register": s.get("register"), "text": txt[:800]})
    if not john:
        john = (e.get("definition") or "").strip()
    drift.sort(key=lambda x: (x.get("year") or 9999))
    return {"word": e.get("word"), "johnson": john, "etymology": ety, "drift": drift}
def _entry_full(e):
    v = _entry_view(e)                     # word, johnson, etymology, drift[]
    usage = []
    for s in e.get("sources", []):
        if s.get("role") == "historical_usage":
            for q in (s.get("quotes") or []):
                usage.append({"quote": q.get("quote"), "source": q.get("source"), "year": q.get("year")})
    v["usage"] = usage[:8]
    v["found"] = True
    return v
def _dictbrowse(frm, limit):
    keys = _dict_keys()
    limit = max(1, min(limit, 120))
    i = bisect.bisect_left(keys, frm) if frm else 0
    sl = keys[i:i + limit]
    nxt = keys[i + limit] if (i + limit) < len(keys) else None
    return {"total": len(keys), "start": i, "next": nxt,
            "entries": [_entry_view(GATE.entries[k]) for k in sl]}

# ---- local natural-voice TTS (Piper) — read-aloud that works reliably on Linux ----
_PIPER = APP / "tts" / "piper" / "piper"
_VOICE = APP / "tts" / "voices" / "en_US-lessac-medium.onnx"
_TTS = {"proc": None}
def _tts_available():
    return _PIPER.exists() and _VOICE.exists()
def _tts_stop():
    p = _TTS.get("proc")
    if p and p.poll() is None:
        try:
            os.killpg(os.getpgid(p.pid), signal.SIGKILL)
        except Exception:
            pass
    _TTS["proc"] = None
def _tts_speak(text):
    _tts_stop()
    text = (text or "").strip()[:4000]
    if not text or not _tts_available():
        return False
    cmd = "%s --model %s --output-raw 2>/dev/null | aplay -q -r 22050 -f S16_LE -t raw - 2>/dev/null" % (
        shlex.quote(str(_PIPER)), shlex.quote(str(_VOICE)))
    p = subprocess.Popen(["bash", "-c", cmd], stdin=subprocess.PIPE, preexec_fn=os.setsid)
    try:
        p.stdin.write(text.encode("utf-8"))
        p.stdin.close()
    except Exception:
        pass
    _TTS["proc"] = p
    return True

# ---- local offline speech-to-text (Vosk) — dictation with NO cloud, NO API key ----
# The browser Web Speech API only transcribes via Google's cloud (and distro Chromium
# ships without the key), so dictation is done here instead: the mic buffer is POSTed
# to /api/dictate as raw 16-bit mono PCM and recognized on-device. vosk is imported
# lazily so the server still starts if it (or the model) is absent.
_STT_MODEL_DIR = APP / "stt" / "model"
_STT = {"model": None}
def _stt_available():
    return _STT_MODEL_DIR.is_dir()
def _stt_model():
    if _STT["model"] is None:
        from vosk import Model, SetLogLevel
        SetLogLevel(-1)
        _STT["model"] = Model(str(_STT_MODEL_DIR))
    return _STT["model"]
def _stt_transcribe(pcm_bytes, rate=16000):
    """pcm_bytes: mono 16-bit little-endian PCM at `rate` Hz. Returns recognized text."""
    from vosk import KaldiRecognizer
    rec = KaldiRecognizer(_stt_model(), float(rate))
    rec.AcceptWaveform(pcm_bytes)
    return json.loads(rec.FinalResult()).get("text", "")

print("Loading VERITAS engine (gate + library)…")
GATE = BlackletterGate()
AGENT_DIR = ROOT / "10_AGENTS"
_AGENTS = {}


def get_agent(name):
    name = (name or "").lower().strip()
    d = AGENT_DIR / name
    if not agent_available(d):
        return None
    if name not in _AGENTS:
        _AGENTS[name] = AgentCompartment(d)
    return _AGENTS[name]


def agent_list():
    out = []
    for d in sorted(AGENT_DIR.iterdir()):
        if d.is_dir() and agent_available(d):
            a = get_agent(d.name)
            out.append({"name": d.name, "voice": a.voice})
    return out


sys.path.insert(0, str(ROOT / "03_LIBRARIES" / "analysis_layer"))
try:
    import manifest as _analysis        # analysis-library manifest + Socratic walkthroughs
except Exception:
    _analysis = None


def definitions_only(defn):
    """Return Johnson's sense(s) VERBATIM, minus his illustrative literary quotations
    (Shakespeare, Pope, Milton…). The gloss is the numbered/first line; the quotation
    follows it. We select the gloss substring — we never paraphrase. Full verbatim is
    preserved in the library and still returned as `verbatim`."""
    if not defn:
        return defn
    lines = [ln.strip() for ln in defn.split("\n") if ln.strip()]
    if not lines:
        return defn.strip()
    glosses, cur = [], None
    for ln in lines:
        if re.match(r"^\d+\.\s", ln):            # a numbered sense begins
            if cur:
                glosses.append(cur)
            cur = ln
        elif cur is not None and not re.search(r"[.;:]\s*$", cur):
            cur += " " + ln                       # rare: a gloss that wrapped a line
        # else: an illustrative-quotation line -> skip
    if cur:
        glosses.append(cur)
    if glosses:
        return " ".join(glosses)
    # single-sense entry: drop a short "HEADWORD POS [etym]" preamble, keep the first sentence
    text = " ".join(lines)
    m = re.match(r"^.{0,70}?\]\s*", text)
    if m:
        text = text[m.end():]
    gm = re.match(r".*?\.(?=\s|$)", text)
    return (gm.group(0) if gm else text).strip()


# ---- reasoning-tier tool receivers (Path B) --------------------------------------
# These are what the reasoning agent's tool calls actually hit. Each one RECEIVES a
# structured request from Claude and returns VERITAS's OWN verbatim record — never the
# model's memory. This is the anti-fabrication seam: founding-era facts enter the
# reasoning transcript only through these functions, quoted from the gate/corpus/agents.
def _tool_founding_meaning(inp):
    word = (inp.get("word") or "").strip()
    r = GATE.resolve(word)
    if r.get("status") == "VOID_FOR_VAGUENESS":
        return ('VOID FOR VAGUENESS: no verbatim Johnson 1773 authority for "%s" — it was '
                "undefined at the founding. Do not supply a meaning for it." % word)
    if r.get("status") != "ADMITTED":
        return 'The record is silent on "%s" — no founding-era entry. Do not invent one.' % word
    e = GATE.entries.get(word.lower())
    view = _entry_full(e) if e else {}
    ctrl = (r.get("controlling") or {}).get("verbatim") or view.get("johnson") or ""
    out = ['FOUNDING_MEANING of "%s" (VERITAS record, verbatim — quote, do not paraphrase):' % word,
           "Johnson 1773 (controlling): " + definitions_only(ctrl)]
    if view.get("etymology"):
        out.append("Etymology: " + view["etymology"])
    for u in (r.get("founding_use") or [])[:3]:
        out.append('Founding usage: "%s" [%s]' % (u.get("quote", ""), u.get("source", "")))
    for d in (view.get("drift") or [])[:4]:
        out.append("DRIFT (later dictionary) %s %s: %s"
                   % (d.get("source"), d.get("year"), (d.get("text") or "")[:220]))
    for c in (r.get("constructions") or [])[:4]:
        out.append("Case that construed it: %s (%s) — %s"
                   % (c.get("name"), c.get("year"), c.get("direction", "")))
    return "\n".join(out)


def _tool_concordance(inp):
    word = (inp.get("word") or "").strip()
    d = _concordance(word)
    rows = d.get("rows", [])[:20]
    if not rows:
        return 'No founding-era occurrences of "%s" in the corpus.' % word
    out = ['CONCORDANCE of "%s" (%d occurrences; showing %d, verbatim):'
           % (word, d.get("count", 0), len(rows))]
    for r in rows:
        txt = (r.get("quote") or r.get("text") or "")[:240]
        out.append('"%s" — %s (%s)' % (txt, r.get("source", ""), r.get("year", "") or ""))
    return "\n".join(out)


def _tool_ask_voice(inp):
    voice = (inp.get("voice") or "").strip().lower()
    q = (inp.get("question") or "").strip()
    a = get_agent(voice)
    if not a:
        return ('No founding voice named "%s". Available: %s'
                % (voice, ", ".join(x["name"] for x in agent_list())))
    return respond(a, q)


_RESEARCH_TOOLS = {"founding_meaning": _tool_founding_meaning,
                   "founding_concordance": _tool_concordance,
                   "ask_founding_voice": _tool_ask_voice}


# ---- API-key config (for the future grounded "Ask Claude" tier) --------------------
# The key lives ONLY on the server side: an env var, or a locked-down local file.
# It is never placed in the served page and never returned to the browser.
CONFIG_DIR = Path.home() / ".config" / "veritas"
CONFIG_FILE = CONFIG_DIR / "config.json"


def current_key():
    k = os.environ.get("ANTHROPIC_API_KEY")
    if k:
        return k.strip(), "environment"
    try:
        c = json.loads(CONFIG_FILE.read_text())
        if c.get("anthropic_api_key"):
            return c["anthropic_api_key"].strip(), "config file"
    except Exception:
        pass
    return None, None


def save_key(key):
    key = (key or "").strip()
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if key:
        CONFIG_FILE.write_text(json.dumps({"anthropic_api_key": key}))
        try:
            CONFIG_FILE.chmod(0o600)
        except Exception:
            pass
    else:
        try:
            CONFIG_FILE.unlink()
        except FileNotFoundError:
            pass


# ---- full SCOTUS corpus browse/search (all 7,696 cases) ----------------------------
_SCOTUS = None


def scotus_cases():
    global _SCOTUS
    if _SCOTUS is None:
        try:
            rec = ROOT / "03_LIBRARIES" / "veritas_corpus.db"      # consolidated Record (Move 1)
            if rec.exists():
                con = sqlite3.connect(f"file:{rec}?mode=ro", uri=True)
                _SCOTUS = [json.loads(js) for (js,) in con.execute("SELECT js FROM cases")]
                con.close()
            else:
                p = ROOT / "03_LIBRARIES" / "scotus_oral_arguments" / "scotus_index.json"
                _SCOTUS = json.loads(p.read_text(encoding="utf-8")).get("cases", [])
        except Exception:
            _SCOTUS = []
    return _SCOTUS


def search_cases(query, limit=60):
    cases = scotus_cases()
    q = (query or "").strip().lower()
    if not q:
        rows = sorted(cases, key=lambda c: c.get("year", ""), reverse=True)[:limit]  # newest first
    else:
        toks = q.split()
        rows = [c for c in cases
                if all(t in (c.get("name", "") + " " + c.get("citation", "")).lower() for t in toks)][:limit]
    return rows


def key_status():
    k, src = current_key()
    return {"key_set": bool(k), "source": src,
            "hint": ("…" + k[-4:]) if (k and len(k) >= 4) else None,
            "env_locked": bool(os.environ.get("ANTHROPIC_API_KEY"))}


# ---- Ask-Claude tier: retrieval-augmented, gate-fenced -------------------------------
# Everything the model sees is retrieved LOCALLY first (gate definitions + founding usage +
# cases). The model only composes from that grounded context — it never supplies meanings.
DEFAULT_MODEL = "claude-sonnet-5"

SYSTEM_PROMPT = (
    "You are VERITAS, a constitutional-analysis instrument grounded in founding-era meaning. "
    "Answer the user's question USING ONLY the grounded sources provided below — verbatim "
    "definitions from Johnson's Dictionary (1773, controlling), founding-era usage, and the "
    "Supreme Court cases that construed the terms. Rules:\n"
    "- Quote and cite the sources. Do not introduce facts, definitions, or cases not present below.\n"
    "- Never invent or paraphrase a founding-era meaning; the Johnson 1773 definitions control.\n"
    "- If a term is marked VOID FOR VAGUENESS, treat it as undefined at the founding — do not supply a meaning.\n"
    "- If the grounded sources do not answer the question, say so plainly rather than guess.\n"
    "- Be concise. Distinguish the founding meaning from later drift.\n\n"
    "GROUNDED SOURCES:\n")


def current_model():
    return os.environ.get("VERITAS_MODEL") or DEFAULT_MODEL


def build_context(question):
    """Retrieve a tight, grounded context locally: definitions + usage + cases for the terms."""
    terms, seen, blocks = [], set(), []
    for t in lex(question):
        if len(t) < 3 or t in seen:
            continue
        seen.add(t)
        r = GATE.resolve(t)
        if r.get("status") == "ADMITTED":
            terms.append(t)
            blocks.append(f'DEFINITION — "{t}" (Johnson 1773, controlling): {definitions_only(r["controlling"]["verbatim"])}')
            for u in (r.get("founding_use") or [])[:2]:
                blocks.append(f'  FOUNDING USAGE of "{t}": "{u.get("quote", "")}" [{u.get("source", "")}]')
            for c in (r.get("constructions") or [])[:3]:
                d = c.get("dissent")
                dtx = f' Dissent: {d.get("defender")}.' if (d and not d.get("none_filed")) else ""
                blocks.append(f'  CASE construing "{t}": {c.get("name")} ({c.get("year")}) — {c.get("direction", "")}.{dtx}')
        elif r.get("status") == "VOID_FOR_VAGUENESS":
            blocks.append(f'NOTE — "{t}" is VOID FOR VAGUENESS: no verbatim Johnson 1773 authority; undefined at the founding.')
    return terms, "\n".join(blocks) if blocks else "(no founding-era terms resolved from the question)"


def call_claude(key, model, system, question, max_tokens=1024):
    body = json.dumps({"model": model, "max_tokens": max_tokens, "system": system,
                       "messages": [{"role": "user", "content": question}]}).encode()
    req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=body, headers={
        "x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=90) as resp:
        data = json.loads(resp.read())
    text = "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")
    return text, data.get("usage", {})


MIME = {".html": "text/html;charset=utf-8", ".js": "text/javascript", ".css": "text/css",
        ".json": "application/json", ".png": "image/png", ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg", ".svg": "image/svg+xml", ".woff2": "font/woff2", ".ico": "image/x-icon"}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, code, body, ctype="application/json"):
        b = body if isinstance(body, bytes) else body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        try:
            self.wfile.write(b)
        except BrokenPipeError:
            pass

    def _json(self, obj, code=200):
        self._send(code, json.dumps(obj, ensure_ascii=False), "application/json")

    def do_GET(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        try:
            if u.path == "/api/resolve":
                return self._resolve(q)
            if u.path == "/api/ask":
                return self._ask(q)
            if u.path == "/api/agents":
                return self._json({"count": GATE.count, "library_version": GATE.version,
                                   "agents": agent_list()})
            if u.path == "/api/analysis":
                return self._json({"provenance": _analysis.PROVENANCE, "note": _analysis.NOTE,
                                   "datasets": _analysis.manifest()} if _analysis else {"datasets": []})
            if u.path == "/api/socratic":
                did = q.get("dataset", [""])[0]
                w = _analysis.walkthrough(did) if _analysis else None
                return self._json(w if w else {"error": "no walkthrough for " + did}, 200 if w else 404)
            if u.path == "/api/config":
                return self._json(key_status())
            if u.path == "/api/cases":
                return self._json({"total": len(scotus_cases()),
                                   "results": search_cases(q.get("q", [""])[0],
                                                           int(q.get("limit", ["60"])[0] or 60))})
            if u.path == "/api/claude":
                key, _src = current_key()
                if not key:
                    return self._json({"error": "No API key set. Add one in Settings (⚙) to use the grounded Ask-Claude tier."}, 400)
                question = unquote(q.get("q", [""])[0]).strip()
                if not question:
                    return self._json({"error": "empty question"}, 400)
                terms, ctx = build_context(question)
                model = current_model()
                try:
                    text, usage = call_claude(key, model, SYSTEM_PROMPT + ctx, question)
                    return self._json({"answer": text, "grounded_terms": terms, "usage": usage, "model": model})
                except urllib.error.HTTPError as e:
                    detail = e.read().decode("utf-8", "ignore")[:300]
                    return self._json({"error": f"API error {e.code}: {detail}"}, 502)
                except Exception as e:
                    return self._json({"error": "Could not reach the API: " + str(e)}, 502)
            if u.path == "/api/research":
                # The grounded REASONING tier (Path B). OFF until a key is present ($0).
                # The loop runs in-process; the reasoning agent reaches founding facts ONLY
                # through _RESEARCH_TOOLS (the record), then we receive its FOUNDING/MODERN/
                # ARGUMENT synthesis + provenance trace + cost back as one dict.
                key, _src = current_key()
                if not key:
                    return self._json({"error": "The reasoning tier is OFF. Add an API key in "
                                       "Settings (⚙) to enable it — it stays $0 until you run a "
                                       "question, then costs cents. Founding lookups remain free/offline."}, 400)
                question = unquote(q.get("q", [""])[0]).strip()
                if not question:
                    return self._json({"error": "empty question"}, 400)
                depth = (q.get("depth", ["normal"])[0] or "normal").lower()
                res = veritas_reason.research(question, key, _RESEARCH_TOOLS,
                                              current_model(), depth)
                return self._json(res, 200 if not res.get("error") else 502)
            if u.path == "/api/pulled":
                try:
                    m = json.loads((APP / "books" / "pulled_manifest.json").read_text())
                except Exception:
                    m = {"items": []}
                return self._json(m)
            if u.path == "/api/entry":
                w = (q.get("word", [""])[0] or "").strip().lower()
                e = GATE.entries.get(w) if w else None
                return self._json(_entry_full(e) if e else {"word": w, "found": False})
            if u.path == "/api/dictbrowse":
                return self._json(_dictbrowse((q.get("from", [""])[0] or "").lower().strip(),
                                              int(q.get("limit", ["60"])[0] or 60)))
            if u.path == "/api/concordance":
                return self._json(_concordance(re.sub(r"[^A-Za-z-]", "", q.get("q", [""])[0])[:40]))
            if u.path == "/api/speak":
                ok = _tts_speak(unquote(q.get("text", [""])[0]))
                return self._json({"speaking": ok, "voice": "piper·en_US-lessac"} if ok
                                  else {"error": "tts unavailable"}, 200 if ok else 503)
            if u.path == "/api/speak_stop":
                _tts_stop()
                return self._json({"stopped": True})
            if u.path == "/api/open":
                url = unquote(q.get("url", [""])[0])
                # only ever hand an http(s) URL to the system browser — never a shell/file/other scheme
                if not re.match(r"^https?://[^\s]+$", url):
                    return self._json({"error": "only http(s) URLs are allowed"}, 400)
                try:
                    subprocess.Popen(["xdg-open", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    return self._json({"opened": True})
                except Exception as e:
                    return self._json({"error": str(e)}, 500)
            return self._static(u.path)
        except Exception as e:  # never crash the server on one bad request
            return self._json({"error": str(e)}, 500)

    def do_POST(self):
        u = urlparse(self.path)
        n = int(self.headers.get("Content-Length", 0) or 0)
        if u.path == "/api/dictate":
            # body = raw mono 16-bit little-endian PCM; ?rate=<Hz> (browser capture rate)
            try:
                if not _stt_available():
                    return self._json({"error": "offline speech model not installed"}, 503)
                raw = self.rfile.read(n) if n else b""
                q = parse_qs(u.query)
                rate = int((q.get("rate", ["16000"])[0]) or 16000)
                return self._json({"text": _stt_transcribe(raw, rate)})
            except Exception as e:
                return self._json({"error": str(e)}, 500)
        try:
            data = json.loads(self.rfile.read(n) or b"{}") if n else {}
        except Exception:
            data = {}
        try:
            if u.path == "/api/config":
                if os.environ.get("ANTHROPIC_API_KEY"):
                    return self._json({"error": "A key is set via the ANTHROPIC_API_KEY environment "
                                       "variable; unset it to manage the key here.", **key_status()}, 409)
                save_key(data.get("anthropic_api_key", ""))
                return self._json({"saved": True, **key_status()})
            return self._json({"error": "not found"}, 404)
        except Exception as e:
            return self._json({"error": str(e)}, 500)

    def _resolve(self, q):
        text = unquote(q.get("term", [""])[0]).strip()
        terms = lex(text)
        if not terms and text:
            terms = [text.lower().strip()]
        seen, results = [], []
        for t in terms:
            if t in seen:
                continue
            seen.append(t)
            r = GATE.resolve(t)
            c = r.get("controlling") or {}
            if r.get("status") == "ADMITTED" and c.get("verbatim"):
                c["definition"] = definitions_only(c["verbatim"])   # sense only, no literary quotes
            results.append(r)
        return self._json({"input": text, "results": results})

    def _ask(self, q):
        name = q.get("agent", [""])[0]
        question = unquote(q.get("q", [""])[0]).strip()
        a = get_agent(name)
        if not a:
            return self._json({"error": f"no such agent: {name}"}, 404)
        return self._json({"agent": name, "voice": a.voice, "answer": respond(a, question)})

    def _static(self, path):
        if path in ("/", ""):
            path = "/VERITAS.html"
        p = (APP / path.lstrip("/")).resolve()
        if not str(p).startswith(str(APP.resolve())) or not p.is_file():
            return self._send(404, "not found", "text/plain")
        self._send(200, p.read_bytes(), MIME.get(p.suffix, "application/octet-stream"))


def run(port=8737):
    """Start the engine (blocking). Called by the desktop CLI AND the Android/Chaquopy
    shell (from a background thread, after it has set VERITAS_ROOT to the app data dir)."""
    srv = HTTPServer(("127.0.0.1", int(port)), Handler)  # serial: gate/agent DBs are single-thread
    agents = agent_list()
    print(f"VERITAS bridge ready → http://127.0.0.1:{port}/VERITAS.html")
    print(f"  gate: library v{GATE.version}, {GATE.count} grounded terms")
    print(f"  agents: {len(agents)} ({', '.join(a['name'] for a in agents)})")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nshutting down.")


def main():
    run(int(sys.argv[1]) if len(sys.argv) > 1 else 8737)


if __name__ == "__main__":
    main()
