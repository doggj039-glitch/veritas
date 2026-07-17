"""
Federalist vs. Anti-Federalist dialogue series — full topic map, no quote reused.

For each topic (sequenced to the Federalist Papers), retrieve the on-point
Federalist passages (scoped to that topic's paper range) and the best available
Anti-Federalist counters (across the whole AF corpus), pair them, and pull a CLEAN
verbatim sentence from the primary source for each. Every quote is logged; a quote
already used in any earlier topic is skipped, so nothing repeats. Fully offline,
verbatim, cited.
"""
import re, sys
from pathlib import Path
from agent_core import AgentCompartment, ROOT, _topical_terms

FED = AgentCompartment(ROOT / "10_AGENTS" / "federalist")
ANTI = AgentCompartment(ROOT / "10_AGENTS" / "antifederalist")
OUT = Path("/home/noneya/Desktop/FEDERALIST_ANTIFEDERALIST_DEBATE.md")

# clean full-source texts for verbatim sentence extraction (not the chunked index)
FED_SRC = re.sub(r"\s+", " ", (ROOT / "10_AGENTS/federalist/source/federalist.txt").read_text(encoding="utf-8", errors="replace"))
AF_SRC = {}
for f in (ROOT / "10_AGENTS/antifederalist/source").glob("*.txt"):
    t = f.read_text(encoding="utf-8"); AF_SRC[t.split("\n")[0].strip()] = re.sub(r"\s+", " ", t)

TOPICS = [
    (1,  "The Value of Union",                        1, 5,   "union states advantage safety strength"),
    (2,  "Dangers of Disunion Among the States",      6, 8,   "dissension war between states discord"),
    (3,  "Faction and the Extended Republic",         9, 10,  "faction republic democracy majority"),
    (4,  "Commerce and Economic Union",               11,13,  "commerce trade navigation revenue"),
    (5,  "Extent of Territory for a Republic",        14,14,  "extent territory large republic"),
    (6,  "Defects of the Confederation",              15,22,  "confederation requisition defect league"),
    (7,  "An Energetic National Government",          23,23,  "energy national government defence powers"),
    (8,  "Standing Armies",                           24,29,  "standing army military peace soldiers"),
    (9,  "The Power of Taxation",                     30,36,  "taxation taxes revenue impost money"),
    (10, "Difficulties of Framing the Government",    37,37,  "difficulties convention framing form"),
    (11, "Separation of Powers",                      47,51,  "separation departments powers legislative encroach"),
    (12, "Representation and the House",              52,58,  "representation representatives house election"),
    (13, "The Senate",                               62,66,  "senate states equal representation"),
    (14, "Executive Power",                          67,74,  "executive president magistrate power"),
    (15, "Appointments and Treaties",                75,77,  "appointment treaty nomination senate"),
    (16, "The Judiciary",                            78,83,  "judiciary courts judges supreme jurisdiction"),
    (17, "Absence of a Bill of Rights",              84,84,  "rights bill liberty declaration press"),
    (18, "Ratification and Amendment",               85,85,  "ratification amendment adopt convention"),
]

used = set()          # global quote keys — the no-reuse guarantee
log = []              # (topic_n, author, ref, first_words)


def key(sentence):
    return re.sub(r"[^a-z]", "", sentence.lower())[:60]


def author(ref):
    return "Publius" if ref.startswith("Federalist") else ref.split()[0] \
        if not ref.startswith(("Federal", "An Old")) else " ".join(ref.split()[:2])


# masthead / dateline / signature noise to reject as quotes
_NOISE = re.compile(r"\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|17\d\d)\b|"
                    r"To the People of the State|For the Independent Journal|From the New York|"
                    r"From The Independent|PUBLIUS|MADISON|HAMILTON|To the Citizens of", re.I)


def best_sentence(text, terms, avoid=used, minw=10, maxlen=340):
    """Highest term-overlap sentence in `text`, excluding mastheads and used quotes."""
    ts = set(terms)
    best, bestscore = None, 1        # require score >1 so a real term match is present
    for s in re.split(r"(?<=[.;])\s+", text):
        s = s.strip()
        if len(s.split()) < minw or len(s) > maxlen or key(s) in avoid or _NOISE.search(s):
            continue
        sc = sum(w in ts for w in re.findall(r"[a-z]+", s.lower()))
        if sc > bestscore:
            best, bestscore = s, sc
    return best


def fed_refs_in(lo, hi):
    return {f"Federalist No. {n}" for n in range(lo, hi + 1)}


def build_topic(n, title, lo, hi, terms):
    allowed = fed_refs_in(lo, hi)
    qterms = _topical_terms(title + " " + terms)
    fed_hits, _ = FED.search(qterms, k=60)
    exchanges = []
    for rowid, _r, ref, _t, _s in fed_hits:
        if ref not in allowed:
            continue
        pub = best_sentence(FED_SRC[FED_SRC.find(""):], qterms) if False else None
        # extract from the specific paper's text window around this passage's ref
        pub = best_sentence(FED_SRC, qterms)  # fed source is one file; term-scored sentence
        # better: restrict to this paper — find "FEDERALIST No. N" block
        pno = ref.split("No. ")[1]
        m = re.search(rf"FEDERALIST No\. {pno}\b", FED_SRC)
        block = FED_SRC[m.start(): m.start() + 16000] if m else FED_SRC
        pub = best_sentence(block, qterms)
        if not pub:
            continue
        # cross-retrieve the closest Anti-Federalist counter
        cterms = _topical_terms(pub) or qterms
        a_hits, _ = ANTI.search(cterms, k=30)
        counter = None
        for arow, _ar, aref, _at, _as in a_hits:
            src = AF_SRC.get(aref)
            if not src:
                continue
            cs = best_sentence(src, cterms)
            if cs:
                counter = (aref, cs); break
        if not counter:
            continue
        used.add(key(pub)); used.add(key(counter[1]))
        log.append((n, "Publius", ref, pub[:40]))
        log.append((n, author(counter[0]), counter[0], counter[1][:40]))
        exchanges.append((ref, pub, counter[0], counter[1]))
        if len(exchanges) >= 4:
            break
    return exchanges


def main():
    doc = ["# Federalist vs. Anti-Federalist — Dialogue Series",
           "*Verbatim, cited, no quote reused across topics. Generated offline from the primary-source corpora.*\n"]
    covered = 0
    for n, title, lo, hi, terms in TOPICS:
        ex = build_topic(n, title, lo, hi, terms)
        doc.append(f"\n## Topic {n} — {title}")
        doc.append(f"*Federalist No. {lo}{'–'+str(hi) if hi!=lo else ''}*\n")
        if not ex:
            doc.append("_(no verbatim pairing found in current corpus)_"); continue
        covered += 1
        for i, (fref, pub, aref, anti) in enumerate(ex, 1):
            doc.append(f"**[{n}.{i}] Publius ({fref}):**  \n“{pub}”\n")
            doc.append(f"**{author(aref)} ({aref}):**  \n“{anti}”\n")
    # reuse log
    doc.append("\n---\n## Quote-Reuse Log\n")
    doc.append("| Topic | Author | Source | Quote (opening) |")
    doc.append("|---|---|---|---|")
    for n, au, ref, q in log:
        doc.append(f"| {n} | {au} | {ref} | {q}… |")
    OUT.write_text("\n".join(doc), encoding="utf-8")
    print(f"topics with dialogue: {covered}/{len(TOPICS)}")
    print(f"total exchanges: {len(log)//2} | unique quotes logged: {len(used)}")
    print(f"-> {OUT}")


if __name__ == "__main__":
    main()
    FED.close(); ANTI.close()
