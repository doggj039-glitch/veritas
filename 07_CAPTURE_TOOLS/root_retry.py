"""
When a word comes back NOT_FOUND, try a small number of plausible root
forms before giving up -- Johnson often only gives a headword to the root
(govern), not every inflected form (governments, governed, governing).
Never guesses at MEANING -- only tries alternate SPELLINGS to search for,
and always records which form actually matched.
"""
import re

def candidate_roots(word: str) -> list:
    """Return plausible root forms to retry, most likely first. Pure spelling
    transforms only -- no semantic guessing."""
    w = word.lower()
    cands = []

    if w.endswith("ies") and len(w) > 4:
        cands.append(w[:-3] + "y")
    if w.endswith("es") and len(w) > 3:
        cands.append(w[:-2])
    if w.endswith("s") and not w.endswith("ss") and len(w) > 3:
        cands.append(w[:-1])

    if w.endswith("ied") and len(w) > 4:
        cands.append(w[:-3] + "y")
    if w.endswith("ed") and len(w) > 3:
        cands.append(w[:-2])
        cands.append(w[:-1])
        if len(w) > 4 and w[-3] == w[-4]:
            cands.append(w[:-3])

    if w.endswith("ing") and len(w) > 4:
        cands.append(w[:-3])
        cands.append(w[:-3] + "e")
        if len(w) > 5 and w[-4] == w[-5]:
            cands.append(w[:-4])

    if w.endswith("ment") and len(w) > 5:
        cands.append(w[:-4])

    extra = []
    for c in list(cands):
        if c.endswith("ment") and len(c) > 5:
            extra.append(c[:-4])
    cands.extend(extra)

    seen, out = set(), []
    for c in cands:
        if c and c != w and c not in seen:
            seen.add(c)
            out.append(c)
    return out
