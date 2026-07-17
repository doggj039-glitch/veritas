"""
Mismatch detector: compares the word actually searched for against the
headword label the site returned, so a wrong-entry capture (like coin ->
Coigne, or as -> Ask) gets flagged for a human instead of silently entering
the library.
"""
import re

def _normalize_headword(label: str) -> str:
    """Strip Johnson's 'To VERB' verb-entry convention and punctuation."""
    s = (label or "").lower().strip()
    s = re.sub(r"^to\s+", "", s)
    s = re.sub(r"[^a-z]", "", s)
    return s

def headword_matches(searched_word: str, headword_label: str) -> bool:
    """
    True if the returned entry is plausibly the same word as what was
    searched for. Compares normalized first-4-letters, which is forgiving
    of Johnson's long-s/spelling variants but catches genuinely different
    words (coin vs coigne passes; coin vs ask fails; let vs -let fails).
    """
    w = re.sub(r"[^a-z]", "", (searched_word or "").lower())
    h = _normalize_headword(headword_label)
    if not w or not h:
        return False
    return w[:4] == h[:4]
