"""
Agent compartment core — the offline, grounded, no-API responder.

A compartment = one folder with persona.md + corpus.db (FTS5). Knowledge lives on
disk and is QUERIED, never fully loaded, so memory stays flat regardless of how
many books/agents exist. The responder can only surface what its sources verbatim
say (retrieval) + fixed founding-era definitions (the Blackletter gate). It cannot
hallucinate. When its corpus has nothing, it says so and points to the API tier.

Reusable for any agent; Federalist is the first instance.
"""
import sqlite3, re, sys, os
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
    raise RuntimeError(
        "VERITAS root not found: set VERITAS_ROOT, or run from inside the project "
        "(the folder that holds 00_APP and 02_GATE_BLACKLETTER)."
    )


ROOT = _veritas_root()
sys.path.insert(0, str(ROOT / "02_GATE_BLACKLETTER" / "gate"))
from blackletter_gate import BlackletterGate
from blackletter_lexer import lex

# one shared gate (library + flags) for all agents
_GATE = None
def gate():
    global _GATE
    if _GATE is None:
        _GATE = BlackletterGate()
    return _GATE


# ---- consolidated Record (Move 1): agents query ONE shared FTS5 table, scoped to
# their assigned sources via the `agent_scope` map. Reclaims the per-agent corpus.db
# duplicates. Falls back to a folder's own corpus.db when the Record isn't present. ----
RECORD = ROOT / "03_LIBRARIES" / "veritas_corpus.db"
_RECORD_CON = None
_SCOPES = None


def _record():
    global _RECORD_CON
    if _RECORD_CON is None and RECORD.exists():
        _RECORD_CON = sqlite3.connect(f"file:{RECORD}?mode=ro", uri=True, check_same_thread=False)
    return _RECORD_CON


def _scopes():
    """Per-agent WHERE fragment over the Record's passages, from agent_scope (cached).
    ref rows → `AND corpus=? AND ref IN(...)`; no ref rows → `AND corpus=?` (whole)."""
    global _SCOPES
    if _SCOPES is None:
        _SCOPES = {}
        con = _record()
        if con is not None:
            try:
                rows = con.execute("SELECT agent, corpus, ref FROM agent_scope").fetchall()
            except sqlite3.OperationalError:
                rows = []
            by = {}
            for agent, corpus, ref in rows:
                c, refs = by.get(agent, (corpus, []))
                if ref is not None:
                    refs.append(ref)
                by[agent] = (corpus, refs)
            for agent, (corpus, refs) in by.items():
                if refs:
                    where = " AND corpus = ? AND ref IN (%s)" % ",".join("?" * len(refs))
                    _SCOPES[agent] = (where, [corpus, *refs])
                else:
                    _SCOPES[agent] = (" AND corpus = ?", [corpus])
    return _SCOPES


def record_scoped_agents():
    return set(_scopes().keys())


def agent_available(agent_dir):
    """Usable if it has a persona AND either its own corpus.db or a Record scope."""
    d = Path(agent_dir)
    return (d / "persona.md").exists() and \
        ((d / "corpus.db").exists() or d.name in record_scoped_agents())


class AgentCompartment:
    def __init__(self, agent_dir):
        self.dir = Path(agent_dir)
        self.name = self.dir.name
        self.persona = (self.dir / "persona.md").read_text(encoding="utf-8") \
            if (self.dir / "persona.md").exists() else ""
        m = re.search(r"\*\*Name:\*\*\s*(.+)", self.persona)
        self.voice = m.group(1).split("(")[0].strip() if m else self.name
        self._con = None  # lazy corpus.db conn
        self._df_cache = {}  # term -> doc-frequency; corpus is read-only so cache for the run
        # Prefer the agent's OWN corpus.db when present (byte-exact, corpus-local bm25).
        # Only fall through to the shared Record when the private db has been retired —
        # so reclaiming the redundant dbs is the only thing that moves an agent onto it.
        scope = _scopes().get(self.name)
        if not (self.dir / "corpus.db").exists() and scope is not None and _record() is not None:
            self._scope_where, self._scope_params = scope
            self._on_record = True
        else:
            self._scope_where, self._scope_params = "", []
            self._on_record = False

    def _db(self):
        if self._on_record:
            return _record()
        if self._con is None:
            self._con = sqlite3.connect(self.dir / "corpus.db")
        return self._con

    def doc_freq(self, term):
        """How many passages contain this term (0 = absent from the corpus).
        Cached per instance: the corpus is read-only, so a term's frequency never
        changes within a run. This collapses the repeated calls (search's term
        filter + _compose's absent-check + the definitions pass) to ONE query
        per distinct term instead of 2–3."""
        cached = self._df_cache.get(term)
        if cached is not None:
            return cached
        try:
            n = self._db().execute(
                "SELECT count(*) FROM passages WHERE passages MATCH ?" + self._scope_where,
                [f'"{term}"', *self._scope_params]).fetchone()[0]
        except sqlite3.OperationalError:
            n = 0
        self._df_cache[term] = n
        return n

    def search(self, terms, k=4, exclude_ids=()):
        """Top-K passages (FTS5 OR-match, bm25). Returns (rows, best_bm25).
        rows = (rowid, bm25, paper_no, title, snippet). exclude_ids skips passages
        already shown this thread (so 'tell me more' returns fresh material)."""
        terms = [t for t in terms if t.isalpha() and len(t) > 2 and self.doc_freq(t) > 0]
        if not terms:
            return [], None
        match = " OR ".join(f'"{t}"' for t in terms)
        sql = ("SELECT rowid, bm25(passages) AS r, ref, title, "
               "snippet(passages, 2, '', '', ' … ', 28) "
               "FROM passages WHERE passages MATCH ?" + self._scope_where + " ")
        params = [match, *self._scope_params]
        if exclude_ids:
            sql += "AND rowid NOT IN (%s) " % ",".join("?" * len(exclude_ids))
            params += list(exclude_ids)
        sql += "ORDER BY r LIMIT ?"
        params.append(k)
        try:
            rows = self._db().execute(sql, params).fetchall()
        except sqlite3.OperationalError:
            return [], None
        return rows, (rows[0][1] if rows else None)

    def close(self):
        if self._con:                 # only a legacy conn we opened; never the shared Record
            self._con.close(); self._con = None


# framing/meta words: about the ACT of asking, not the topic. Dropped from
# retrieval so the query locks onto topical terms (faction), not filler (founders).
RETRIEVAL_STOPWORDS = {
    "mean", "meant", "means", "meaning", "think", "thought", "thinks", "founder",
    "founders", "tell", "explain", "say", "said", "says", "know", "knew", "want",
    "wanted", "understand", "consider", "view", "views", "opinion", "believe",
    "believed", "paper", "papers", "federalist", "publius", "time", "times", "define",
    "definition", "discuss", "describe", "regarding", "concerning", "question", "ask",
    "asked", "wrote", "write", "writes", "feel", "felt", "thing", "things", "really",
    "actually", "author", "authors", "intend", "intended",
}

_SENSE_SPLIT = re.compile(r"(?m)(?=^\s*\d+\.\s)")


def bind_sense(verbatim, context):
    """Cheap sense-binding: if the definition has numbered senses, return the one
    whose words best overlap the surrounding context (question + retrieved passages).
    Else return the head gloss. Fixes multi-sense words showing the wrong sense."""
    body = verbatim
    # drop the headword/POS/etymology line so senses score cleanly
    m = re.search(r"\]\s*", verbatim)
    if m:
        body = verbatim[m.end():]
    senses = [s.strip() for s in _SENSE_SPLIT.split(body) if re.match(r"^\d+\.", s.strip())]
    ctx = set(re.findall(r"[a-z]{4,}", context.lower()))
    if len(senses) >= 2 and ctx:
        senses.sort(key=lambda s: -sum(1 for w in set(re.findall(r"[a-z]{4,}", s.lower())) if w in ctx))
        chosen = re.sub(r"^\d+\.\s*", "", senses[0])
    else:
        chosen = re.sub(r"^\s*\d+\.\s*", "", body.strip()) if body.strip() else verbatim
    return re.sub(r"\s+", " ", chosen).strip()[:160]


def _topical_terms(question):
    """Content terms with framing words removed — used for BOTH retrieval and definitions."""
    return [t for t in lex(question)
            if t.isalpha() and len(t) > 2 and t not in RETRIEVAL_STOPWORDS]


def _compose(agent, question, topical, hits, more=False):
    """Shared response composer — used by both single-shot respond() and Conversation."""
    g = gate()
    absent = [t for t in topical if agent.doc_freq(t) == 0]
    topical_absent = [t for t in absent if len(t) >= 6]
    passage_ctx = question + " " + " ".join(h[4] for h in hits)

    out = [f'[{agent.name.upper()} AGENT]  (offline · keyword retrieval · grounded · no API)',
           f'On: "{question}"', ""]

    # definitions: topical terms that admit, sense-bound to the passages (skip on "more")
    defs = [(t, g.resolve(t)) for t in dict.fromkeys(topical)]
    defs = [(t, r) for t, r in defs if r["status"] == "ADMITTED"]
    defs.sort(key=lambda tr: -len(tr[0]))
    if defs and not more:
        out.append("Founding-era terms (Johnson 1773, verbatim):")
        for t, r in defs[:3]:
            out.append(f"  • {t} — {bind_sense(r['controlling']['verbatim'], passage_ctx)}")
        out.append("")

    if not hits:
        if more:
            out.append("That's all I have in my assigned sources on that thread. Ask about "
                       "something else, or connect an API to reason further.")
        else:
            out += ["I have nothing in my assigned sources matching that.",
                    "For anything beyond my assigned text, connect an API."]
        return "\n".join(out)

    confident = not topical_absent
    v = agent.voice
    out.append(f"More from {v} on that:" if more else
               (f"What {v} wrote (closest passages by keyword match):" if not confident
                else f"What {v} actually wrote:"))
    for _rowid, _r, ref, title, snip in hits:
        snip = re.sub(r"\s+", " ", snip).strip()
        cite = ref + (f' ("{title[:52]}")' if title else "")
        out += [f'  “…{snip}…”', f'      — {cite}', ""]

    if confident:
        out.append("I can show you only what my assigned sources say, verbatim. For "
                   "interpretation beyond them, connect an API.")
    else:
        out.append(f"⚠ Low confidence: your term(s) {topical_absent} do not appear anywhere "
                   "in my assigned sources — these passages only share generic words. This is "
                   "exactly where a reasoning API is needed.")
    return "\n".join(out)


def respond(agent: AgentCompartment, question: str) -> str:
    """Single-shot (stateless) response."""
    topical = _topical_terms(question)
    hits, _ = agent.search(topical, k=4)
    return _compose(agent, question, topical, hits)


def team_ask(agents, question):
    """One question → EVERY voice at once (the triangulation thesis). Lexes the
    question ONCE and shares the topical terms across all agents, instead of each
    agent re-lexing the same question separately. Each agent still retrieves within
    its own scope, so per-voice output is identical to calling respond() per agent.
    Returns {agent_name: composed_text}."""
    topical = _topical_terms(question)
    return {ag.name: _compose(ag, question, topical, ag.search(topical, k=4)[0])
            for ag in agents}


# follow-up cues (raw question words — lexer strips most, so match on the surface)
_CONTINUE = {"more", "another", "else", "other", "further", "elaborate", "continue",
             "expand", "again", "also", "additional", "go on", "keep going"}
_ANAPHORA = {"that", "this", "it", "they", "them", "those", "these", "he", "him", "his", "there"}


class Conversation:
    """Multi-turn wrapper. Carries the current thread's topical terms so follow-ups
    resolve against it, and excludes already-shown passages on 'tell me more' so the
    reader can work through a topic to the end of the book. Fully offline; the buffer
    is a few short turns — no memory growth."""

    def __init__(self, agent, window=4):
        self.agent = agent
        self.window = window
        self.focus = []          # current thread's topical terms
        self.shown = set()       # passage rowids already shown this thread
        self.turns = []          # short history of {question, focus}

    def ask(self, question):
        own = _topical_terms(question)
        wl = set(re.findall(r"[a-z']+", question.lower()))
        is_more = bool(wl & _CONTINUE)
        is_followup = (not own) or bool(wl & _ANAPHORA) or (is_more and len(own) <= 1)

        if own and not is_followup:                 # a new topic starts a new thread
            self.focus, self.shown, more = own, set(), False
        else:                                       # follow-up: keep thread focus (+ any new words)
            self.focus = list(dict.fromkeys(own + self.focus))[:5]
            more = is_more

        hits, _ = self.agent.search(self.focus, k=4, exclude_ids=(self.shown if more else set()))
        for h in hits:
            self.shown.add(h[0])
        self.turns.append({"q": question, "focus": self.focus})
        self.turns = self.turns[-self.window:]
        return _compose(self.agent, question, self.focus, hits, more=more)


if __name__ == "__main__":
    fed = AgentCompartment(ROOT / "10_AGENTS" / "federalist")
    convo = Conversation(fed)
    thread = sys.argv[1:] or [
        "What is the danger of faction in a republic?",   # new topic
        "Tell me more.",                                  # 'more' → fresh passages, same thread
        "Does a large republic help control it?",         # follow-up (anaphora 'it'), adds 'large'
        "What about the power of taxation?",              # new topic → new thread
    ]
    for q in thread:
        print("\n>>> " + q)
        print(convo.ask(q))
        print("-" * 70)
    fed.close()
