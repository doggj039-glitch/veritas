"""
Case-construction provider for the Blackletter gate.

For a term the gate ADMITS, this answers a different question than the definition:
*which Supreme Court cases later CONSTRUED that word, and in which direction did they
move it?* The linkage is the curated word->case map (VERITAS-authored: necessary ->
McCulloch, commerce -> Lopez/Raich, ...), enriched with the VERIFIED Oyez record
(citation + official link) wherever the 7,696-case corpus has it (1956+; older
landmarks like McCulloch stay name/year only).

This CORROBORATES drift — it shows how doctrine moved a founding term over time. It does
NOT gate: a word is admitted on its Johnson 1773 baseline, with or without cases. Map
data is passed through verbatim; nothing is invented.
"""
import json, re, unicodedata
from pathlib import Path

ROOT = Path("/home/noneya/Projects/VERITAS v.3")
WORD_TO_CASES = ROOT / "03_LIBRARIES" / "from_sdcard" / "tables" / "word_to_cases.json"
SCOTUS_INDEX = ROOT / "03_LIBRARIES" / "scotus_oral_arguments" / "scotus_index.json"


def _norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9 ]", "", s).strip()


def _fmt_cite(s):
    if not s:
        return s
    s = re.sub(r"\bUS\b", "U.S.", s)
    s = re.sub(r"\s_+\s", " ___ ", s)
    return re.sub(r"\s+", " ", s).strip()


# generic legal tokens carry no identity — a match on these alone means nothing
_GENERIC = {"united", "states", "v", "vs", "inc", "co", "company", "corp", "corporation",
            "commission", "commr", "commrs", "department", "dept", "board", "city", "county",
            "of", "the", "et", "al", "usa", "no", "and", "llc", "lp"}


def _dist(name):
    """Distinctive (identity-bearing) tokens of a case name."""
    return {t for t in _norm(name).split() if t not in _GENERIC and len(t) > 2}


# analysis layer: recorded dissents / counterevidence per case (interpretive, not a source)
try:
    import sys
    sys.path.insert(0, str(ROOT / "03_LIBRARIES" / "analysis_layer"))
    from analysis_layer import dissent_for as _dissent_for
except Exception:
    def _dissent_for(name):
        return None


class CaseConstructions:
    def __init__(self, w2c=WORD_TO_CASES, index=SCOTUS_INDEX):
        self.by_word = {}
        try:
            d = json.loads(Path(w2c).read_text(encoding="utf-8"))
            self.by_word = {k.lower(): v for k, v in d.items()}
        except Exception:
            pass
        # norm_name -> [Oyez records] (a caption can recur across years); + year -> [records]
        self.oyez = {}
        self.by_year = {}
        try:
            for r in json.loads(Path(index).read_text(encoding="utf-8")).get("cases", []):
                self.oyez.setdefault(_norm(r["name"]), []).append(r)
                try:
                    y = int(r.get("year") or 0)
                except (TypeError, ValueError):
                    y = 0
                if y:
                    self.by_year.setdefault(y, []).append(r)
        except Exception:
            pass

    def _hit(self, r):
        return {"citation": _fmt_cite(r.get("citation")), "court": r.get("court"),
                "oyez": r.get("oyez"), "in_corpus": True}

    def _enrich(self, name, year):
        """Enrich ONLY on (year match) AND (exact name OR full token-subset). Never guess:
        anything short of that stays name-only, so a citation is right or absent — never wrong."""
        try:
            yr = int(year)
        except (TypeError, ValueError):
            return {"in_corpus": False}
        years = [y for y in (yr - 1, yr, yr + 1)]
        # 1) exact normalized-name match within the year window
        recs = self.oyez.get(_norm(name)) or []
        for r in recs:
            try:
                if int(r.get("year") or 0) in years:
                    return self._hit(r)
            except ValueError:
                continue
        # 2) year-gated token-subset match (every distinctive map token is in the caption)
        want = _dist(name)
        if want:
            for y in years:
                for r in self.by_year.get(y, []):
                    if want <= _dist(r["name"]):
                        return self._hit(r)
        return {"in_corpus": False}

    def lookup(self, word, k=4):
        """Up to k cases that construed `word`, each enriched with its Oyez record."""
        rows = self.by_word.get((word or "").lower())
        if not rows:
            return []
        out = []
        for c in rows[:k]:
            rec = {"name": c.get("name"), "year": c.get("year"),
                   "construction": c.get("what"), "direction": c.get("direction"),
                   "chain": c.get("chain")}
            rec.update(self._enrich(c.get("name") or "", c.get("year")))
            d = _dissent_for(c.get("name") or "")
            if d:
                rec["dissent"] = d
            out.append(rec)
        return out

    def words(self):
        return sorted(self.by_word)


if __name__ == "__main__":
    import sys
    cc = CaseConstructions()
    print(f"word->case map: {len(cc.by_word)} words | Oyez captions indexed: {len(cc.oyez)}")
    for w in sys.argv[1:] or ["commerce", "necessary", "speech"]:
        print(f"\n=== {w} ===")
        for c in cc.lookup(w):
            tag = f" [{c['citation']}]" if c.get("in_corpus") else " [pre-1956, name only]"
            print(f"  {c['name']} ({c['year']}){tag}  {c.get('direction') or ''}")
            print(f"    {(c.get('construction') or '')[:120]}")
