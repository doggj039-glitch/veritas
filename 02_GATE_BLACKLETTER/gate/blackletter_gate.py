"""
BLACKLETTER GATE — v0 resolver (scope: BLACKLETTER_GATE_SCOPE.md)

One job: decide whether a term is GROUNDED in the VERITAS founding-era baseline.
  ADMITTED            -> term resolves to a verbatim Johnson 1773 definition;
                         carry provenance (+ etymology / founding-era usage if present).
  VOID_FOR_VAGUENESS  -> no verbatim founding-era authority on file; blocked.

Controlling source = Johnson's Dictionary 1773 (4th folio), 100% of the library.
Etymology (92%) and founding-era usage (25%) CORROBORATE; they do not gate.
Drift (Webster/Black's) and modern dictionaries are NOT read by the gate.

This is a checkpoint, not an adjudicator. It says whether a word is *defined*,
not what the right answer is.
"""
import json
import re
import sys
import os
import sqlite3
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
# the gate reads its OWN copy of the library (02_GATE_BLACKLETTER/gate/)
GATE_LIB = ROOT / "02_GATE_BLACKLETTER" / "gate" / "VERITAS_definitions_library.json"
# reuse the library's own inflection recovery (govern <- governments) — spelling only
sys.path.insert(0, str(ROOT / "07_CAPTURE_TOOLS"))
try:
    from root_retry import candidate_roots
except Exception:
    def candidate_roots(w):  # graceful fallback
        return []

CONTROLLING_SOURCE = "Johnson's Dictionary (1773, 4th folio)"


def _baseline(entry, role):
    for s in entry.get("sources", []):
        if s.get("role") == role:
            return s
    return None


def _good_curated(q):
    """Reject curated usage that is really a TOC/index/heading fragment."""
    if not q or len(q) < 30:
        return False
    if ".." in q or q[:1].isdigit():
        return False
    if sum(c.isdigit() for c in q) / len(q) > 0.06:
        return False
    al = sum(c.isalpha() for c in q)
    if al and sum(c.isupper() for c in q if c.isalpha()) / al > 0.4:
        return False
    return True


class SqliteEntries:
    """Dict-like read-only view over the word-indexed library DB. Same API the gate and
    endpoints used on the old in-memory dict (get / [] / in / len / keys / iter), but
    queried on disk — low RAM + fast startup (the enabling change for the phone edition).
    Falls back is unnecessary: if the .db is absent the gate loads the JSON as before."""
    def __init__(self, db_path):
        self._db = sqlite3.connect("file:%s?mode=ro" % db_path, uri=True, check_same_thread=False)
        self._count = self._db.execute("SELECT COUNT(*) FROM entries").fetchone()[0]
        self._keys = None
    def meta(self, key, default=None):
        r = self._db.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
        return r[0] if r else default
    def __len__(self):
        return self._count
    def __contains__(self, word):
        return self._db.execute("SELECT 1 FROM entries WHERE word=? LIMIT 1", (word,)).fetchone() is not None
    def __getitem__(self, word):
        r = self._db.execute("SELECT json FROM entries WHERE word=?", (word,)).fetchone()
        if r is None:
            raise KeyError(word)
        return json.loads(r[0])
    def get(self, word, default=None):
        r = self._db.execute("SELECT json FROM entries WHERE word=?", (word,)).fetchone()
        return json.loads(r[0]) if r else default
    def keys(self):
        if self._keys is None:
            self._keys = [row[0] for row in self._db.execute("SELECT word FROM entries ORDER BY word")]
        return self._keys
    def __iter__(self):
        return iter(self.keys())
    def values(self):
        for row in self._db.execute("SELECT json FROM entries"):
            yield json.loads(row[0])
    def items(self):
        for row in self._db.execute("SELECT word, json FROM entries"):
            yield row[0], json.loads(row[1])


class BlackletterGate:
    def __init__(self, lib_path=GATE_LIB, flags_path=None):
        _p = str(lib_path)
        db_path = Path(_p[:-5] + ".db" if _p.endswith(".json") else _p + ".db")
        if db_path.exists():
            self.entries = SqliteEntries(db_path)          # queried on disk — low RAM, fast startup
            self.version = self.entries.meta("library_version")
        else:                                              # fallback: load the JSON into memory
            data = json.loads(Path(lib_path).read_text(encoding="utf-8"))
            self.entries = {e["word"].lower(): e for e in data["entries"]}
            self.version = data.get("library_version")
        self.count = len(self.entries)
        # optional flag sidecar (metadata layer; never touches verbatim text)
        fp = Path(flags_path) if flags_path else (Path(lib_path).parent / "blackletter_flags.json")
        self.flags = {}
        self.flags_version = None
        if fp.exists():
            fj = json.loads(fp.read_text(encoding="utf-8"))
            self.flags = fj.get("flags", {})
            self.flags_version = fj.get("flag_layer_version")
        # founding-era usage provider — fills historical_usage from the primary-source corpora
        try:
            from blackletter_usage import FoundingUsage
            self.usage = FoundingUsage()
        except Exception:
            self.usage = None
        # case-construction provider — the SCOTUS cases that later construed the term
        # (curated word->case map, enriched with the verified Oyez record). Corroborates
        # drift; does NOT gate.
        try:
            from blackletter_cases import CaseConstructions
            self.cases = CaseConstructions()
        except Exception:
            self.cases = None

    def _grounding(self, entry):
        j = _baseline(entry, "johnson_1773")
        ety = _baseline(entry, "etymology")
        hist = _baseline(entry, "historical_usage")
        has_ety = bool(ety and ety.get("verbatim_text"))
        has_use = bool(hist and hist.get("quotes"))
        if j and has_ety and has_use:
            return "full-triad"
        if j and has_ety:
            return "baseline+etymology"
        return "baseline-only"

    def _admit(self, term, entry, matched_via=None):
        ety = _baseline(entry, "etymology")
        hist = _baseline(entry, "historical_usage")
        verbatim = entry.get("definition") or (
            (_baseline(entry, "johnson_1773") or {}).get("verbatim_text"))
        # founding-era usage: PREFER the primary-source corpus (cleaner, on-point);
        # backfill only with the curated DB's non-noisy quotes.
        corpus_use = self.usage.lookup(entry["word"], k=3) if getattr(self, "usage", None) else []
        seen, founding_use = set(), []
        for u in corpus_use:
            key = re.sub(r"[^a-z]", "", (u.get("quote") or "").lower())[:40]
            if key and key not in seen:
                seen.add(key); founding_use.append(u)
        used_corpus = bool(founding_use)
        backfilled = False
        if len(founding_use) < 3:
            for u in (hist or {}).get("quotes") or []:
                q = u.get("quote") or ""
                key = re.sub(r"[^a-z]", "", q.lower())[:40]
                if key and key not in seen and _good_curated(q):
                    seen.add(key); founding_use.append(u); backfilled = True
                if len(founding_use) >= 3:
                    break
        founding_use = founding_use[:4]
        fu_src = (("founding_corpus" + ("+curated" if backfilled else "")) if used_corpus
                  else ("constitutional_usage_database" if founding_use else None))
        v = {
            "term": term,
            "status": "ADMITTED",
            "controlling": {
                "source": CONTROLLING_SOURCE,
                "part_of_speech": entry.get("part_of_speech"),
                "verbatim": verbatim,
            },
            "etymology": (ety or {}).get("verbatim_text") or None,
            "founding_use": founding_use,
            "founding_use_source": fu_src,
            "grounding": self._grounding(entry),
            "flags": self.flags.get(entry["word"].lower(), []),
        }
        # cases that later CONSTRUED this term (drift in doctrine). Corroborating, not gating.
        constructions = self.cases.lookup(entry["word"], k=4) if getattr(self, "cases", None) else []
        if constructions:
            v["constructions"] = constructions
        if matched_via:
            v["matched_via_root"] = matched_via
        return v

    def resolve(self, term):
        """Gate verdict for a single term."""
        w = (term or "").strip().lower()
        if not w:
            return {"term": term, "status": "VOID_FOR_VAGUENESS",
                    "reason": "empty term", "nearest": None}
        entry = self.entries.get(w)
        if entry:
            return self._admit(term, entry)
        # spelling-only inflection recovery (never guesses meaning)
        for root in candidate_roots(w):
            e = self.entries.get(root)
            if e:
                return self._admit(term, e, matched_via=root)
        return {
            "term": term,
            "status": "VOID_FOR_VAGUENESS",
            "reason": "no verbatim founding-era (Johnson 1773) authority on file",
            "nearest": candidate_roots(w)[:3] or None,
        }

    def gate(self, terms):
        """Resolve a list; return (admitted, voided)."""
        results = [self.resolve(t) for t in terms]
        admitted = [r for r in results if r["status"] == "ADMITTED"]
        voided = [r for r in results if r["status"] != "ADMITTED"]
        return admitted, voided, results

    def compile(self, text):
        """Stage 2->7 on raw text: LEX -> RESOLVE/TYPECHECK each term -> emit the
        canonical CompileReport. This is the gate's front-end output that the rest
        of VERITAS consumes. Ungrounded terms surface as VOID FOR VAGUENESS."""
        from blackletter_lexer import lex
        from blackletter_report import build_report
        verdicts = [self.resolve(t) for t in lex(text)]
        return build_report(text, self.version, verdicts)

    def gate_text(self, text):
        """Back-compat thin dict; prefer compile()."""
        r = self.compile(text)
        return {"input": text, "library_version": self.version,
                "compiles": r.compiles, "admitted": [d.term for d in r.diagnostics if d.status == "ADMITTED"],
                "void_for_vagueness": r.summary["void_terms"]}


if __name__ == "__main__":
    g = BlackletterGate()
    print(f"Blackletter gate loaded: library v{g.version}, {g.count} grounded terms\n")
    demo = sys.argv[1:] or ["commerce", "liberty", "floccinaucinihilipilification",
                            "infringe", "reprieve", "expressly", "regulating"]
    for t in demo:
        r = g.resolve(t)
        if r["status"] == "ADMITTED":
            via = f"  (via root '{r['matched_via_root']}')" if r.get("matched_via_root") else ""
            print(f"[ADMITTED]{via}  {t}  <{r['grounding']}>")
            print(f"    {CONTROLLING_SOURCE}: {r['controlling']['verbatim'][:90].strip()}...")
            for c in r.get("constructions", []):
                cite = c.get("citation") if c.get("in_corpus") else "pre-1956, name only"
                print(f"    ├─ construed by {c['name']} ({c['year']}) [{cite}] — {c.get('direction') or ''}")
        else:
            print(f"[VOID FOR VAGUENESS]  {t}  -- {r['reason']}")
