"""
VERITAS -- local_search.py
Answer VERITAS questions ONLY from pages already saved in saved_sources/.

HARD RULES (per Susan's decision):
  * NO network call. NO paid API. Under NO circumstance. This module contains
    no API/HTTP code at all -- that is the guarantee.
  * If nothing saved matches well enough, say so plainly ("nothing saved on
    this yet") -- never a silent guess, never a fallback call.

Entry point
-----------
search(query, saved_dir) -> {
    answered: bool,
    query: str,
    matches: [ {title, url, date, score, snippet, path}, ... ],   # only if answered
    message: str | None,                                          # set if NOT answered
}
"""
from __future__ import annotations

import re
from pathlib import Path

# Light synonym / variant map -- same spirit as the Education Helper dictionary:
# a few common word relations so a question still matches near-wordings.
_SYNONYMS = {
    "law": ["statute", "act", "code", "legislation"],
    "court": ["tribunal", "judiciary", "judge", "judicial"],
    "right": ["rights", "liberty", "freedom"],
    "money": ["currency", "coin", "coinage", "dollar", "tender"],
    "search": ["seizure", "warrant"],
    "speech": ["expression", "press", "assembly"],
    "power": ["authority", "powers"],
    "state": ["states", "federalism"],
    "tax": ["taxation", "duty", "impost", "excise"],
}

_WORD = re.compile(r"[a-z0-9']+")
_HEADER_SEP = "=" * 70


def _variants(word: str) -> set[str]:
    """Cheap variants: plurals/tenses + a small synonym map (no heavy NLP)."""
    w = word.lower()
    out = {w}
    for suf in ("s", "es", "ed", "ing", "'s"):
        if w.endswith(suf) and len(w) > len(suf) + 2:
            out.add(w[: -len(suf)])
    out.update({w + "s", w + "es"})
    out.update(_SYNONYMS.get(w, []))
    return out


def _query_terms(query: str) -> set[str]:
    terms: set[str] = set()
    for w in _WORD.findall(query.lower()):
        if len(w) > 2:  # skip tiny function words (of, to, is...)
            terms |= _variants(w)
    return terms


def _parse_file(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8", errors="replace")
    meta = {"title": path.stem, "url": "", "date": ""}
    body = raw
    if raw.startswith("TITLE:"):
        head, _sep, body = raw.partition(_HEADER_SEP)
        for line in head.splitlines():
            if line.startswith("TITLE:"):
                meta["title"] = line[len("TITLE:"):].strip()
            elif line.startswith("SOURCE URL:"):
                meta["url"] = line[len("SOURCE URL:"):].strip()
            elif line.startswith("DATE SAVED:"):
                meta["date"] = line[len("DATE SAVED:"):].strip()
    return {
        "path": str(path), "title": meta["title"], "url": meta["url"],
        "date": meta["date"], "text": body.strip(),
    }


def _snippet(text: str, low: str, needles: list[str], width: int = 240) -> str:
    for needle in needles:
        if not needle:
            continue
        i = low.find(needle)
        if i >= 0:
            start = max(0, i - 80)
            return ("..." if start else "") + text[start:start + width].strip() + "..."
    return text[:width].strip() + "..."


def search(query: str, saved_dir, top: int = 5, min_hits: int = 2) -> dict:
    """
    Best-matching saved files for a question. NEVER contacts anything.
    If the best match is weaker than `min_hits`, returns answered=False with a
    plain message -- the caller MUST NOT fall back to any paid service.
    """
    saved_dir = Path(saved_dir)
    terms = _query_terms(query)
    phrase = query.strip().lower()
    results = []

    if saved_dir.exists():
        for path in sorted(saved_dir.rglob("*.txt")):
            if path.name == "README.txt":
                continue
            doc = _parse_file(path)
            low = doc["text"].lower()
            words = set(_WORD.findall(low))
            hits = terms & words
            score = len(hits)
            if len(phrase) > 4 and phrase in low:
                score += 5  # an exact phrase match is a strong signal
            if score:
                doc["score"] = score
                doc["hits"] = sorted(hits)
                doc["snippet"] = _snippet(doc["text"], low, [phrase] + list(hits))
                results.append(doc)

    results.sort(key=lambda r: r["score"], reverse=True)
    best = results[0]["score"] if results else 0
    answered = best >= min_hits

    return {
        "answered": answered,
        "query": query,
        "matches": [
            {k: r[k] for k in ("title", "url", "date", "score", "snippet", "path")}
            for r in results[:top]
        ] if answered else [],
        "message": None if answered else (
            "Nothing saved answers this yet. VERITAS only answers from pages "
            "you have Saved -- nothing on this topic has been saved. "
            "(No outside or paid service was contacted.)"
        ),
    }


if __name__ == "__main__":  # simple CLI
    import sys
    _base = Path(__file__).resolve().parent.parent / "saved_sources"
    _q = " ".join(sys.argv[1:]) or input("Ask VERITAS (local only): ")
    _out = search(_q, _base)
    if not _out["answered"]:
        print(_out["message"])
    else:
        for m in _out["matches"]:
            print(f"\n[{m['score']}] {m['title']}  ({m['date']})\n  {m['url']}\n  {m['snippet']}")
