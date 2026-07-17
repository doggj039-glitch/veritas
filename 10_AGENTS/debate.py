"""
Debate generator — duplicate the point/counterpoint pattern from a topic.

For a topic, it pulls Publius's strongest passages, then for EACH one cross-
retrieves the Anti-Federalist passage that shares the most vocabulary (the closest
rebuttal). Every line is verbatim from the corpus, with its citation. Optionally
scope either side to specific sections (refs) for tighter, hand-picked pairings.

Fully offline, keyword-based. The pairing is vocabulary-overlap, not semantic
judgment — but the overlap is now weighted by term RARITY (idf-ish), so a shared
distinctive word ("faction", "standing") counts far more than a common one
("government", "power"). Good when both sides argue the same clause.
"""
import sys, re, math
from agent_core import AgentCompartment, ROOT, _topical_terms

# Lazy: importing must not open the Record — only running a debate does.
_AGENTS = None
def _agents():
    global _AGENTS
    if _AGENTS is None:
        _AGENTS = {n: AgentCompartment(ROOT / "10_AGENTS" / n)
                   for n in ("federalist", "antifederalist")}
    return _AGENTS


def _weights(agent, terms):
    """Rarer term → higher weight. A word in few passages is distinctive; a word
    everywhere ('government') barely narrows anything. Uses the (now cached)
    doc_freq, so this is nearly free."""
    return {t: 1.0 / math.log(agent.doc_freq(t) + 2) for t in terms}


def _full(agent, rowid):
    return agent._db().execute("SELECT ref, body FROM passages WHERE rowid=?", (rowid,)).fetchone()


def _lead(body, terms, weights=None, maxlen=300):
    """A clean lead quote: the sentence best covering the topic terms, each term
    weighted by rarity so the lead locks onto the distinctive language."""
    body = re.sub(r"\s+", " ", body).strip()
    sents = re.split(r"(?<=[.;])\s+", body)
    w = weights or {}
    def score(s):
        present = set(re.findall(r"[a-z]+", s.lower()))
        return sum(w.get(t, 1.0) for t in terms if t in present)
    best = max(sents, key=score)
    return best[:maxlen].strip()


def debate(topic, rounds=4, fed_only_refs=None, anti_only_refs=None):
    FED, ANTI = _agents()["federalist"], _agents()["antifederalist"]
    terms = _topical_terms(topic)
    fed_w = _weights(FED, terms)
    fed_hits, _ = FED.search(terms, k=rounds * 2)
    print("═" * 76 + f"\nTOPIC:  {topic}\n" + "═" * 76)
    used_anti, shown = set(), 0
    for rowid, _r, ref, _t, _snip in fed_hits:
        if fed_only_refs and ref not in fed_only_refs:
            continue
        fref, fbody = _full(FED, rowid)
        pub = _lead(fbody, terms, fed_w)
        # cross-retrieve the closest Anti-Federalist counter using this passage's vocabulary
        pterms = _topical_terms(pub) or terms
        anti_w = _weights(ANTI, pterms)
        a_hits, _ = ANTI.search(pterms, k=6, exclude_ids=used_anti)
        counter = None
        for arow, _ar, aref, _at, _as in a_hits:
            if anti_only_refs and aref not in anti_only_refs:
                continue
            used_anti.add(arow)
            abody = _full(ANTI, arow)[1]
            counter = (aref, _lead(abody, pterms, anti_w))
            break
        if not counter:
            continue
        shown += 1
        print(f"\n[{shown}] PUBLIUS  ({fref}):")
        print(f'      "{pub}"')
        print(f"     COUNTER  ({counter[0]}):")
        print(f'      "{counter[1]}"')
        if shown >= rounds:
            break
    print("\n" + "═" * 76)
    print("Every line verbatim from the corpus. Pairing = rarity-weighted vocabulary overlap.")


if __name__ == "__main__":
    topic = " ".join(sys.argv[1:]) or "a standing army in time of peace"
    debate(topic)
    for a in _agents().values():
        a.close()
