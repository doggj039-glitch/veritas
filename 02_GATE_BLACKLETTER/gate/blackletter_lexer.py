"""
BLACKLETTER GATE — stage 2: LEX (tokenizer).  Spec: BLACKLETTER_GATE_SPEC.md

Turns raw text (a clause, sentence, statute) into the ordered list of CONTENT
terms the gate must resolve. Unlike the app's find_constitutional_terms (a
dictionary *matcher* that only surfaces already-known words), the lexer emits
EVERY carrying word — including ones absent from the library — so the gate can
throw VOID FOR VAGUENESS on the ungrounded ones. Stopwords are dropped using the
SAME constitutional stopword set the app uses (mirrored here, kept in sync).

lex("Congress shall make no law abridging the freedom of speech")
  -> ['congress','make','law','abridging','freedom','speech']
     (shall/no/the/of dropped as stopwords)
"""
import re

# Mirror of document_processor.find_constitutional_terms._STOPWORD_HEADWORDS.
# The gate and the app MUST agree on what is non-substantive; keep these identical.
STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being", "do", "does", "did",
    "have", "has", "had", "having", "will", "would", "shall", "should", "can", "could", "may",
    "might", "must", "of", "to", "in", "on", "at", "by", "for", "with", "and", "or", "but", "not",
    "no", "this", "that", "these", "those", "it", "its", "as", "if", "then", "than", "so", "such",
    "what", "which", "who", "whom", "how", "why", "when", "where", "there", "here", "from", "into",
    "up", "down", "out", "off", "over", "under", "again", "once", "about", "against", "between",
    "through", "during", "before", "after", "above", "below", "both", "each", "few", "more",
    "most", "other", "some", "own", "same",
}

# A token is a run of letters, allowing internal apostrophes/hyphens (don't split
# "well-regulated" mid-word here; the gate's root-retry handles inflections).
_TOKEN = re.compile(r"[A-Za-z][A-Za-z'\-]*[A-Za-z]|[A-Za-z]")


def lex(text, keep_duplicates=False):
    """Return ordered content terms (lowercased). Drops stopwords, punctuation,
    numbers, and single letters. Splits hyphenated compounds into parts so each
    is gated (well-regulated -> well, regulated)."""
    terms = []
    seen = set()
    for m in _TOKEN.finditer(text or ""):
        raw = m.group(0)
        # split hyphenated compounds; strip stray apostrophes at the ends
        for part in raw.split("-"):
            w = part.strip("'").lower()
            if len(w) < 2 or w in STOPWORDS:
                continue
            if not keep_duplicates and w in seen:
                continue
            seen.add(w)
            terms.append(w)
    return terms


if __name__ == "__main__":
    import sys
    demo = " ".join(sys.argv[1:]) or \
        "Congress shall make no law abridging the freedom of speech, or of the press"
    print("INPUT:", demo)
    print("TERMS:", lex(demo))
