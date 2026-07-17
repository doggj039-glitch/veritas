"""
Founding-era usage provider for the Blackletter gate.

Given a word, returns real verbatim passages that USE it, from the founding-era
primary-source corpora (Constitution, Bill of Rights, Declaration, Blackstone I–IV,
Elliot's Debates I–V, plus the Federalist / Anti-Federalist). Queried on-disk
(FTS5), never loaded — so it fills the gate's historical_usage layer for ANY word,
not just the ~25% the curated database covered. Verbatim + cited; no invention.
"""
import os, sqlite3, re
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
CORPORA = [
    # clean salvaged library FIRST (Federalist, Anti-Fed, Elliot, Farrand, Madison,
    # Story, Rawle, Blackstone, Montesquieu, Locke) — preferred over OCR
    ROOT / "03_LIBRARIES" / "historical_documents.db",
    ROOT / "03_LIBRARIES" / "founding_sources" / "founding_corpus.db",  # Constitution/Declaration/Bill of Rights
    ROOT / "10_AGENTS" / "federalist" / "corpus.db",
    ROOT / "10_AGENTS" / "antifederalist" / "corpus.db",
]

# Consolidated "Record" (Move 1): one corpus-tagged FTS5 `passages` table. Preferred
# when present; the per-file CORPORA above remain a drop-in fallback (delete the .db
# to revert). CONCORDANCE_CORPORA is the exact source set + order used before, so
# results are identical whether reading the Record or the legacy files.
RECORD = ROOT / "03_LIBRARIES" / "veritas_corpus.db"
CONCORDANCE_CORPORA = ["historical", "founding", "federalist", "antifederalist"]


# long-s and common ligatures are unambiguous — repair them (conſidered -> considered)
_LONGS = str.maketrans({"ſ": "s", "ﬅ": "st", "ﬀ": "ff", "ﬁ": "fi", "ﬂ": "fl", "ﬄ": "ffl"})
# table-of-contents / index headers: "Chap. II", "HAP. I", "Page x", "Vol. 2", "Sect. 3"
_HDR = re.compile(r"\b(?:c?hap|chapter|page|vol|book|sect|tit)\b\.?,?\s*(?:[ivxlcdm]+|\d+|[a-z])\b", re.I)


def _clean(s):
    s = s.translate(_LONGS)
    return re.sub(r"\s+", " ", s).strip(" .…-|")


def _ok(s):
    """Keep only clean, sentence-like founding-era snippets; reject OCR / table-of-contents noise."""
    if len(s) < 30:
        return False
    if "|" in s or "ſ" in s:                    # OCR column-break / stray long-s
        return False
    if any(ch in s for ch in "\\~^@`{}"):        # OCR junk characters (bo\ight, etc.)
        return False
    if re.search(r"\b[B-HJ-NP-Z]\b(?=\s+[a-z])", s):  # lone stray capital for I/l ("T think")
        return False
    letters = sum(c.isalpha() or c.isspace() for c in s)
    if letters / max(len(s), 1) < 0.86:
        return False
    toks = re.findall(r"[A-Za-z]+", s)
    if len(toks) < 6:
        return False
    if sum(1 for t in toks if len(t) <= 2) / len(toks) > 0.34:      # fragmented OCR
        return False
    if sum(1 for t in toks if len(t) == 1 and t.isupper()) >= 3:    # scattered index capitals
        return False
    if _HDR.search(s):                                             # chapter/page/vol header line
        return False
    return True


class FoundingUsage:
    def __init__(self, paths=CORPORA):
        # Prefer the consolidated Record (one FTS5 table, corpus-tagged); else fall
        # back to the per-file corpora. Identical results either way (verified).
        self.record = None
        self.cons = []
        if RECORD.exists():
            try:
                # check_same_thread=False mirrors the gate's SqliteEntries: the server is
                # single-threaded/serial, so one shared read-only connection is safe, and
                # this keeps it usable if the server ever runs on a background thread.
                self.record = sqlite3.connect(f"file:{RECORD}?mode=ro", uri=True,
                                              check_same_thread=False)
            except Exception:
                self.record = None
        if self.record is None:
            for p in paths:
                if Path(p).exists():
                    try:
                        self.cons.append(sqlite3.connect(f"file:{p}?mode=ro", uri=True))
                    except Exception:
                        pass

    def _ready(self):
        return self.record is not None or bool(self.cons)

    def _match(self, word, ntoken, limit):
        """Yield (ref, snippet) row-lists per source, in fixed source order — from the
        Record (one table filtered by `corpus`) or the legacy per-file corpora. Same
        query per source, same order, so lookup()/concordance() behave identically."""
        if self.record is not None:
            sql = ("SELECT ref, snippet(passages, 2, '', '', ' … ', %d) "
                   "FROM passages WHERE passages MATCH ? AND corpus = ? "
                   "ORDER BY rank LIMIT ?" % ntoken)
            for tag in CONCORDANCE_CORPORA:
                try:
                    yield self.record.execute(sql, (f'"{word}"', tag, limit)).fetchall()
                except sqlite3.OperationalError:
                    yield []
        else:
            sql = ("SELECT ref, snippet(passages, 2, '', '', ' … ', %d) "
                   "FROM passages WHERE passages MATCH ? ORDER BY rank LIMIT ?" % ntoken)
            for con in self.cons:
                try:
                    yield con.execute(sql, (f'"{word}"', limit)).fetchall()
                except sqlite3.OperationalError:
                    yield []

    def lookup(self, word, k=3):
        """Return up to k {quote, source} founding-era usages of `word`, one per source."""
        word = re.sub(r"[^a-zA-Z]", "", word)
        if not word or not self._ready():
            return []
        out, seen_src = [], set()
        for rows in self._match(word, 26, 4):
            for ref, snip in rows:
                q = _clean(snip)
                if _ok(q) and ref not in seen_src:
                    out.append({"quote": q[:240], "source": ref})
                    seen_src.add(ref)
                    break  # one per source for variety
        return out[:k]

    def concordance(self, word, cap=250):
        """EVERY clean founding-era occurrence of `word` across all corpora: [{quote, source}].
        Unlike lookup() (one per source), this returns the full, de-duplicated list — the drift
        evidence, verbatim + cited."""
        word = re.sub(r"[^a-zA-Z]", "", word)
        if not word or not self._ready():
            return []
        out, seen = [], set()
        for rows in self._match(word, 32, cap):
            for ref, snip in rows:
                q = _clean(snip)
                if _ok(q):
                    key = (ref, q[:90].lower())
                    if key not in seen:
                        seen.add(key)
                        out.append({"quote": q[:320], "source": ref})
        return out[:cap]

    def close(self):
        if self.record is not None:
            self.record.close()
        for c in self.cons:
            c.close()


if __name__ == "__main__":
    import sys
    fu = FoundingUsage()
    print(f"corpora loaded: {len(fu.cons)}")
    for w in sys.argv[1:] or ["militia", "commerce", "reprieve"]:
        print(f"\n=== {w} ===")
        for u in fu.lookup(w):
            print(f"  [{u['source']}] “…{u['quote'][:110]}…”")
