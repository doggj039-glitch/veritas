"""
test_corpus_index.py — Phase 1 Acceptance Test

Acceptance criteria (from VERITAS Implementation Spec, Section 9, Phase 1):
  1. Ingest 3 test documents (1 primary, 1 primary, 1 secondary).
  2. Search for a term.
  3. Confirm primary sources rank before secondary sources.
  4. Confirm resolve() can match a citation.
  5. Confirm all code compiles (py_compile run before this test).

Run:  python3 test_corpus_index.py
"""

import json
import os
import sys
import tempfile
import textwrap
from pathlib import Path

# Add veritas/ to path so we can import corpus_index directly
sys.path.insert(0, str(Path(__file__).parent))

from corpus_index import CorpusIndex

PASS = "\033[32mPASS\033[0m"
FAIL = "\033[31mFAIL\033[0m"

results = []

def check(label, condition, detail=""):
    status = PASS if condition else FAIL
    print(f"  [{status}] {label}")
    if detail:
        print(f"         {detail}")
    results.append((label, condition))
    return condition


# ── Document content ─────────────────────────────────────────────────────────

DOC1 = textwrap.dedent("""\
    Title: Rights of the Accused — Primary Constitution Text
    Citation: [2001] RTA 1

    Every person has the right to be presumed innocent until proven guilty.
    The state must disclose all material evidence to the defence before trial.
    Fundamental justice requires a fair hearing before an impartial tribunal.
    This document constitutes primary constitutional authority on disclosure.
""")

DOC2 = textwrap.dedent("""\
    Title: Evidence Act — Primary Statute
    This is the Evidence Act.

    Section 12 — Admissibility of Evidence
    No evidence obtained in violation of fundamental rights shall be admitted
    unless the court is satisfied its admission would not bring the administration
    of justice into disrepute.
    Disclosure of exculpatory evidence is mandatory.
    Reference: Rights of the Accused [2001] RTA 1.
""")

DOC3 = textwrap.dedent("""\
    Title: Commentary on Disclosure Law — Secondary Source

    Scholars have long debated the scope of the disclosure obligation.
    This article surveys the academic literature on disclosure and
    fundamental justice, drawing on primary sources from various jurisdictions.
    The consensus view is that disclosure obligations are grounded in the
    presumption of innocence.
    See: Evidence Act; Rights of the Accused [2001] RTA 1.
""")


# ── Run test ─────────────────────────────────────────────────────────────────

def run():
    print("\n" + "="*60)
    print("  VERITAS Phase 1 — corpus_index.py Acceptance Test")
    print("="*60 + "\n")

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Write test documents to disk
        f1 = tmpdir / "constitution_rights.txt"
        f2 = tmpdir / "evidence_act.txt"
        f3 = tmpdir / "disclosure_commentary.txt"
        f1.write_text(DOC1)
        f2.write_text(DOC2)
        f3.write_text(DOC3)

        db_path = tmpdir / "corpus" / "index" / "corpus.db"

        print("── Phase 1 · Setup ─────────────────────────────────────────")
        with CorpusIndex(db_path=db_path) as idx:

            # ── TEST 1: Compile check (import succeeded to get here) ──────
            check("corpus_index.py compiles and imports without error", True)

            # ── TEST 2: CorpusIndex instantiates, DB created ──────────────
            db_exists = db_path.exists()
            check("SQLite DB created at corpus/index/corpus.db", db_exists,
                  f"path: {db_path}")

            print("\n── Phase 1 · Ingest ────────────────────────────────────────")

            # ── TEST 3: Ingest 3 documents ────────────────────────────────
            id1 = idx.ingest(str(f1), source_type="primary",
                             date="2001-01-01",
                             title="Rights of the Accused")
            check("Ingest doc1 (primary) returns a doc_id", bool(id1),
                  f"doc_id: {id1[:16]}…")

            id2 = idx.ingest(str(f2), source_type="primary",
                             date="1985-07-17",
                             title="Evidence Act")
            check("Ingest doc2 (primary) returns a doc_id", bool(id2),
                  f"doc_id: {id2[:16]}…")

            id3 = idx.ingest(str(f3), source_type="secondary",
                             date="2018-03-01",
                             title="Commentary on Disclosure Law")
            check("Ingest doc3 (secondary) returns a doc_id", bool(id3),
                  f"doc_id: {id3[:16]}…")

            all_docs = idx.list_all()
            check("list_all() returns 3 documents", len(all_docs) == 3,
                  f"returned {len(all_docs)} documents")

            # ── TEST 4: Stable ID (SHA-256) ───────────────────────────────
            id1_again = idx.ingest(str(f1), source_type="primary",
                                   date="2001-01-01",
                                   title="Rights of the Accused (re-ingest)")
            check("Stable doc_id: same file content → same SHA-256",
                  id1 == id1_again,
                  f"first={id1[:16]}… re-ingest={id1_again[:16]}…")
            all_docs_after = idx.list_all()
            check("Re-ingesting same content does not add a duplicate row",
                  len(all_docs_after) == 3,
                  f"count after re-ingest: {len(all_docs_after)}")

            print("\n── Phase 1 · Search & Ranking ──────────────────────────────")

            # ── TEST 5: Search returns results ────────────────────────────
            hits = idx.search("disclosure", prefer_primary=True)
            check("search('disclosure') returns at least one result",
                  len(hits) >= 1,
                  f"returned {len(hits)} hit(s)")

            # ── TEST 6: Primary sources rank before secondary ─────────────
            # All three docs contain 'disclosure'; with prefer_primary=True,
            # the two primary docs must appear before the secondary doc.
            primary_positions = [
                i for i, h in enumerate(hits)
                if h["source_type"] == "primary"
            ]
            secondary_positions = [
                i for i, h in enumerate(hits)
                if h["source_type"] == "secondary"
            ]
            primaries_before_secondary = (
                bool(primary_positions)
                and bool(secondary_positions)
                and max(primary_positions) < min(secondary_positions)
            )
            ranking_detail = (
                f"primary positions={primary_positions}, "
                f"secondary positions={secondary_positions}"
            )
            check(
                "Primary sources rank before secondary (prefer_primary=True)",
                primaries_before_secondary,
                ranking_detail
            )

            print("         Result order:")
            for i, h in enumerate(hits):
                print(f"           [{i}] [{h['source_type']:9s}] "
                      f"{h['title'][:50]}  rank={h['rank']:.4f}")

            # ── TEST 7: prefer_primary=False doesn't crash ────────────────
            hits_no_pref = idx.search("disclosure", prefer_primary=False)
            check("search() works with prefer_primary=False",
                  len(hits_no_pref) >= 1)

            # ── TEST 8: Bad query returns empty list, not exception ───────
            bad_hits = idx.search('AND OR')   # invalid FTS5 syntax
            check("Malformed FTS5 query returns [] not an exception",
                  isinstance(bad_hits, list))

            # ── TEST 9: Empty query returns [] ────────────────────────────
            empty_hits = idx.search("")
            check("Empty query returns []", empty_hits == [])

            print("\n── Phase 1 · Resolve ───────────────────────────────────────")
            # ── TEST 10: resolve() via self_cite (neutral citation) ─────────
            resolved = idx.resolve("[2001] RTA 1")
            check(
                "resolve('[2001] RTA 1') resolves to doc1 via self_cite",
                resolved == id1,
                f"expected {id1[:16]}…, got {(resolved or 'None')[:16]}…"
            )

            # ── TEST 11: resolve() partial self_cite match ───────────────
            partial = idx.resolve("RTA 1")
            check(
                "resolve() partial self_cite match ('RTA 1') finds doc1",
                partial == id1,
                f"expected {id1[:16]}…, got {(partial or 'None')[:16]}…"
            )

            # ── TEST 12: resolve() returns None for unknown citation ───────
            none_result = idx.resolve("Completely Unknown v Nobody [9999]")
            check(
                "resolve() returns None for an unknown citation",
                none_result is None
            )

            # ── TEST 13: resolve() by title substring ─────────────────────
            by_title = idx.resolve("Evidence Act")
            check(
                "resolve('Evidence Act') resolves via title match",
                by_title == id2,
                f"expected {id2[:16]}…, got {(by_title or 'None')[:16]}…"
            )

            print("\n── Phase 1 · list_all() ordering ───────────────────────────")

            # ── TEST 14: list_all() returns primary before secondary ───────
            all_docs = idx.list_all()
            types = [d["source_type"] for d in all_docs]
            primary_before = (
                types.index("primary") < types.index("secondary")
                if "secondary" in types else True
            )
            check(
                "list_all() returns primary sources before secondary",
                primary_before,
                f"order: {types}"
            )

            print("\n── Phase 1 · rebuild() ─────────────────────────────────────")

            # ── TEST 15: rebuild() runs without error ──────────────────────
            try:
                idx.rebuild()
                rebuild_ok = True
            except Exception as e:
                rebuild_ok = False
                print(f"         Exception: {e}")
            check("rebuild() completes without exception", rebuild_ok)

            # ── TEST 16: Search still works after rebuild ──────────────────
            hits_post = idx.search("fundamental justice", prefer_primary=True)
            check(
                "search() still works after rebuild()",
                len(hits_post) >= 1,
                f"returned {len(hits_post)} hit(s)"
            )

            # ── TEST 17: Ranking still correct after rebuild ───────────────
            post_types = [h["source_type"] for h in hits_post]
            primaries_post = [i for i, t in enumerate(post_types) if t == "primary"]
            secondaries_post = [i for i, t in enumerate(post_types) if t == "secondary"]
            ranking_ok_post = (
                (not primaries_post or not secondaries_post)
                or max(primaries_post) < min(secondaries_post)
            )
            check(
                "Primary-before-secondary ranking intact after rebuild()",
                ranking_ok_post,
                f"order: {post_types}"
            )

    # ── Summary ──────────────────────────────────────────────────────────────
    print("\n" + "="*60)
    passed = sum(1 for _, ok in results if ok)
    total  = len(results)
    print(f"  Result: {passed}/{total} checks passed")
    if passed == total:
        print(f"  [{PASS}] Phase 1 acceptance test COMPLETE")
    else:
        failed = [label for label, ok in results if not ok]
        print(f"  [{FAIL}] {len(failed)} check(s) failed:")
        for f in failed:
            print(f"           • {f}")
    print("="*60 + "\n")
    return passed == total


if __name__ == "__main__":
    ok = run()
    sys.exit(0 if ok else 1)
