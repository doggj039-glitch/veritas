"""
test_gap_log.py — Phase 2 Acceptance Test

Acceptance criteria (from VERITAS Implementation Spec, Section 9, Phase 2):

  1. gap_log.py compiles and imports without error.
  2. GapLog() instantiates cleanly with an empty log.
  3. add() accepts all three valid gap types and returns a unique gap_id.
  4. add() rejects an invalid gap_type with ValueError.
  5. add() rejects an empty value with ValueError.
  6. all() returns all entries in insertion order.
  7. all() returns shallow copies (mutating the returned dicts does not
     affect the internal log).
  8. by_type() returns only entries of the requested type.
  9. by_type() rejects an invalid gap_type with ValueError.
 10. clear() removes all entries.
 11. to_json() produces valid JSON that round-trips through from_json().
 12. from_json() restores all fields correctly.
 13. from_json() rejects non-JSON input with ValueError.
 14. from_json() rejects a JSON object (not array) with ValueError.
 15. from_json() rejects entries with missing required keys.
 16. from_json() rejects entries with invalid gap_type.
 17. save() writes a readable file; load() restores it exactly.
 18. load() raises FileNotFoundError for a missing file.
 19. Optional fields (source_doc_id, best_link) round-trip as None when
     not supplied.
 20. Optional fields round-trip correctly when supplied.
 21. Multiple adds produce unique gap_ids.
 22. len() and bool() reflect log state correctly.
 23. repr() includes entry count and per-type counts.
 24. clear() after save() does not modify the saved file.

Run:  python3 test_gap_log.py
"""

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

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


def expect_exception(exc_type, fn, label, detail=""):
    try:
        fn()
        check(label, False, f"expected {exc_type.__name__} but no exception raised")
    except exc_type as e:
        check(label, True, detail or str(e)[:80])
    except Exception as e:
        check(label, False, f"expected {exc_type.__name__}, got {type(e).__name__}: {e}")


# ── Run ──────────────────────────────────────────────────────────────────────

def run():
    print("\n" + "=" * 60)
    print("  VERITAS Phase 2 — gap_log.py Acceptance Test")
    print("=" * 60 + "\n")

    # ── 1. Compile / import ───────────────────────────────────────────
    print("── Compile & Import ────────────────────────────────────────")
    try:
        import py_compile, os, tempfile as _t
        src = str(Path(__file__).parent / "gap_log.py")
        py_compile.compile(src, doraise=True)
        from gap_log import (
            GapLog,
            UNRESOLVED_CITATION,
            UNDEFINED_TERM,
            EMPTY_SEARCH,
        )
        check("gap_log.py compiles (py_compile) without error", True)
        check("gap_log module imports without error", True)
        check(
            "Module constants present (UNRESOLVED_CITATION, UNDEFINED_TERM, EMPTY_SEARCH)",
            all([UNRESOLVED_CITATION, UNDEFINED_TERM, EMPTY_SEARCH]),
            f"values: {UNRESOLVED_CITATION!r}, {UNDEFINED_TERM!r}, {EMPTY_SEARCH!r}",
        )
    except Exception as e:
        check("gap_log.py compiles and imports", False, str(e))
        print(f"\n  [ABORT] Cannot import gap_log — remaining tests skipped.\n")
        _print_summary()
        sys.exit(1)

    from gap_log import GapLog, UNRESOLVED_CITATION, UNDEFINED_TERM, EMPTY_SEARCH

    # ── 2. Instantiation ──────────────────────────────────────────────
    print("\n── Instantiation ───────────────────────────────────────────")
    gl = GapLog()
    check("GapLog() instantiates without error", gl is not None)
    check("New GapLog is empty: all() returns []", gl.all() == [])
    check("New GapLog: len() == 0", len(gl) == 0)
    check("New GapLog: bool() is False", bool(gl) is False)

    # ── 3. add() — valid gap types ────────────────────────────────────
    print("\n── add() — valid gap types ─────────────────────────────────")

    id_cit = gl.add(
        UNRESOLVED_CITATION,
        "Smith v Jones [2001] 2 SCR 45",
        source_doc_id="abc123",
        best_link="https://example.com/smith-v-jones",
    )
    check("add(UNRESOLVED_CITATION) returns a non-empty gap_id", bool(id_cit),
          f"gap_id: {id_cit}")

    id_term = gl.add(
        UNDEFINED_TERM,
        "fundamental justice",
        source_doc_id="def456",
    )
    check("add(UNDEFINED_TERM) returns a non-empty gap_id", bool(id_term),
          f"gap_id: {id_term}")

    id_search = gl.add(
        EMPTY_SEARCH,
        "habeas corpus writ",
    )
    check("add(EMPTY_SEARCH) returns a non-empty gap_id", bool(id_search),
          f"gap_id: {id_search}")

    check("After 3 adds: len() == 3", len(gl) == 3)
    check("After 3 adds: bool() is True", bool(gl) is True)

    # ── 4 & 5. add() — invalid inputs ─────────────────────────────────
    print("\n── add() — invalid inputs ──────────────────────────────────")
    expect_exception(
        ValueError,
        lambda: gl.add("BAD_TYPE", "some value"),
        "add() raises ValueError for invalid gap_type",
    )
    expect_exception(
        ValueError,
        lambda: gl.add(UNRESOLVED_CITATION, ""),
        "add() raises ValueError for empty value",
    )
    expect_exception(
        ValueError,
        lambda: gl.add(UNRESOLVED_CITATION, "   "),
        "add() raises ValueError for whitespace-only value",
    )
    expect_exception(
        ValueError,
        lambda: gl.add(UNRESOLVED_CITATION, None),
        "add() raises ValueError for None value",
    )
    check(
        "Invalid adds did not change the log (still 3 entries)",
        len(gl) == 3,
    )

    # ── 6. all() — ordering and completeness ─────────────────────────
    print("\n── all() ───────────────────────────────────────────────────")
    entries = gl.all()
    check("all() returns 3 entries", len(entries) == 3)
    check(
        "all() returns entries in insertion order",
        [e["gap_type"] for e in entries]
        == [UNRESOLVED_CITATION, UNDEFINED_TERM, EMPTY_SEARCH],
    )
    check(
        "all() entry contains required fields",
        all(
            {"gap_id", "gap_type", "value", "source_doc_id",
             "best_link", "timestamp"} <= set(e.keys())
            for e in entries
        ),
    )

    # ── 7. all() — shallow copy isolation ────────────────────────────
    print("\n── all() — copy isolation ───────────────────────────────────")
    entries2 = gl.all()
    entries2[0]["value"] = "MUTATED"
    entries3 = gl.all()
    check(
        "Mutating returned dict does not affect internal log",
        entries3[0]["value"] == "Smith v Jones [2001] 2 SCR 45",
    )

    # ── 8. by_type() ─────────────────────────────────────────────────
    print("\n── by_type() ───────────────────────────────────────────────")
    cits = gl.by_type(UNRESOLVED_CITATION)
    check("by_type(UNRESOLVED_CITATION) returns 1 entry", len(cits) == 1)
    check(
        "by_type result has correct gap_type",
        cits[0]["gap_type"] == UNRESOLVED_CITATION,
    )
    check(
        "by_type(UNRESOLVED_CITATION) entry has source_doc_id",
        cits[0]["source_doc_id"] == "abc123",
    )
    check(
        "by_type(UNRESOLVED_CITATION) entry has best_link",
        cits[0]["best_link"] == "https://example.com/smith-v-jones",
    )

    terms = gl.by_type(UNDEFINED_TERM)
    check("by_type(UNDEFINED_TERM) returns 1 entry", len(terms) == 1)

    searches = gl.by_type(EMPTY_SEARCH)
    check("by_type(EMPTY_SEARCH) returns 1 entry", len(searches) == 1)

    # ── 9. by_type() invalid ─────────────────────────────────────────
    expect_exception(
        ValueError,
        lambda: gl.by_type("NOT_A_TYPE"),
        "by_type() raises ValueError for invalid gap_type",
    )

    # ── 10. clear() ──────────────────────────────────────────────────
    print("\n── clear() ─────────────────────────────────────────────────")
    gl_copy = GapLog.from_json(gl.to_json())  # preserve for later tests
    gl.clear()
    check("clear() empties the log: all() == []", gl.all() == [])
    check("clear() empties the log: len() == 0", len(gl) == 0)
    check("clear() empties the log: bool() is False", bool(gl) is False)

    # Restore for remaining tests
    gl = gl_copy

    # ── 11 & 12. to_json() / from_json() round-trip ──────────────────
    print("\n── to_json() / from_json() ─────────────────────────────────")
    j = gl.to_json()
    check("to_json() returns a non-empty string", bool(j))

    parsed = json.loads(j)
    check("to_json() output is a valid JSON array", isinstance(parsed, list))
    check("to_json() array has 3 elements", len(parsed) == 3)

    gl2 = GapLog.from_json(j)
    check("from_json() produces a GapLog with 3 entries", len(gl2) == 3)

    e0 = gl2.all()[0]
    check(
        "from_json() restores gap_type correctly",
        e0["gap_type"] == UNRESOLVED_CITATION,
    )
    check(
        "from_json() restores value correctly",
        e0["value"] == "Smith v Jones [2001] 2 SCR 45",
    )
    check(
        "from_json() restores source_doc_id correctly",
        e0["source_doc_id"] == "abc123",
    )
    check(
        "from_json() restores best_link correctly",
        e0["best_link"] == "https://example.com/smith-v-jones",
    )
    check(
        "from_json() restores timestamp correctly",
        bool(e0["timestamp"]),
    )
    check(
        "from_json() restores gap_id correctly",
        e0["gap_id"] == gl.all()[0]["gap_id"],
    )

    # ── 13–16. from_json() — invalid inputs ───────────────────────────
    print("\n── from_json() — invalid inputs ────────────────────────────")
    expect_exception(
        ValueError,
        lambda: GapLog.from_json("not json at all {{{"),
        "from_json() raises ValueError for non-JSON string",
    )
    expect_exception(
        ValueError,
        lambda: GapLog.from_json('{"key": "value"}'),
        "from_json() raises ValueError for JSON object (not array)",
    )
    expect_exception(
        ValueError,
        lambda: GapLog.from_json('[{"gap_type": "UNRESOLVED_CITATION"}]'),
        "from_json() raises ValueError for entry missing required keys",
    )
    expect_exception(
        ValueError,
        lambda: GapLog.from_json(json.dumps([{
            "gap_id": "x", "gap_type": "BAD",
            "value": "v", "timestamp": "t"
        }])),
        "from_json() raises ValueError for invalid gap_type in entry",
    )

    # ── 17. save() / load() ───────────────────────────────────────────
    print("\n── save() / load() ─────────────────────────────────────────")
    with tempfile.TemporaryDirectory() as tmpdir:
        p = Path(tmpdir) / "reports" / "gap_log.json"
        gl.save(str(p))
        check("save() creates the file (including parent dirs)", p.is_file(),
              f"path: {p}")

        content = p.read_text(encoding="utf-8")
        check("save() file contains valid JSON", bool(json.loads(content)))

        gl3 = GapLog.load(str(p))
        check("load() restores all 3 entries", len(gl3) == 3)
        check(
            "load() entries match original gap_ids",
            [e["gap_id"] for e in gl3.all()]
            == [e["gap_id"] for e in gl.all()],
        )
        check(
            "load() entries match original values",
            [e["value"] for e in gl3.all()]
            == [e["value"] for e in gl.all()],
        )
        check(
            "load() entries match original types",
            [e["gap_type"] for e in gl3.all()]
            == [e["gap_type"] for e in gl.all()],
        )

        # ── 18. load() missing file ───────────────────────────────────
        expect_exception(
            FileNotFoundError,
            lambda: GapLog.load(str(Path(tmpdir) / "nonexistent.json")),
            "load() raises FileNotFoundError for missing file",
        )

        # ── 24. clear() does not modify the saved file ────────────────
        gl3.clear()
        check(
            "clear() after load() does not modify saved file",
            len(json.loads(p.read_text())) == 3,
        )

    # ── 19 & 20. Optional fields ──────────────────────────────────────
    print("\n── Optional fields ─────────────────────────────────────────")
    gl_opt = GapLog()
    id_no_opt = gl_opt.add(EMPTY_SEARCH, "no options query")
    e_no_opt = gl_opt.all()[0]
    check(
        "source_doc_id defaults to None when not supplied",
        e_no_opt["source_doc_id"] is None,
    )
    check(
        "best_link defaults to None when not supplied",
        e_no_opt["best_link"] is None,
    )

    id_with_opt = gl_opt.add(
        UNRESOLVED_CITATION,
        "R v Example [2000]",
        source_doc_id="doc-xyz",
        best_link="https://example.com/ref",
    )
    e_with_opt = gl_opt.all()[1]
    check(
        "source_doc_id round-trips correctly when supplied",
        e_with_opt["source_doc_id"] == "doc-xyz",
    )
    check(
        "best_link round-trips correctly when supplied",
        e_with_opt["best_link"] == "https://example.com/ref",
    )

    # Optional fields survive JSON round-trip
    gl_opt2 = GapLog.from_json(gl_opt.to_json())
    e_rt = gl_opt2.all()[0]
    check(
        "None source_doc_id survives JSON round-trip",
        e_rt["source_doc_id"] is None,
    )
    e_rt2 = gl_opt2.all()[1]
    check(
        "Supplied best_link survives JSON round-trip",
        e_rt2["best_link"] == "https://example.com/ref",
    )

    # ── 21. Unique gap_ids ────────────────────────────────────────────
    print("\n── Unique gap_ids ───────────────────────────────────────────")
    gl_ids = GapLog()
    ids = [
        gl_ids.add(UNRESOLVED_CITATION, f"citation {i}")
        for i in range(20)
    ]
    check(
        "20 adds produce 20 unique gap_ids",
        len(set(ids)) == 20,
        f"unique count: {len(set(ids))}",
    )

    # ── 22. len() and bool() ─────────────────────────────────────────
    print("\n── len() and bool() ────────────────────────────────────────")
    gl_lb = GapLog()
    check("Empty GapLog: len() == 0", len(gl_lb) == 0)
    check("Empty GapLog: bool() is False", not bool(gl_lb))
    gl_lb.add(UNDEFINED_TERM, "habeas corpus")
    check("After 1 add: len() == 1", len(gl_lb) == 1)
    check("After 1 add: bool() is True", bool(gl_lb))

    # ── 23. repr() ───────────────────────────────────────────────────
    print("\n── repr() ──────────────────────────────────────────────────")
    gl_r = GapLog()
    gl_r.add(UNRESOLVED_CITATION, "cit1")
    gl_r.add(UNRESOLVED_CITATION, "cit2")
    gl_r.add(UNDEFINED_TERM, "term1")
    gl_r.add(EMPTY_SEARCH, "query1")
    r = repr(gl_r)
    check("repr() contains entry count", "entries=4" in r, f"repr: {r}")
    check("repr() contains citation count", "citations=2" in r, f"repr: {r}")
    check("repr() contains term count", "terms=1" in r, f"repr: {r}")
    check("repr() contains search count", "searches=1" in r, f"repr: {r}")

    # ── Summary ───────────────────────────────────────────────────────
    _print_summary()
    return all(ok for _, ok in results)


def _print_summary():
    print("\n" + "=" * 60)
    passed = sum(1 for _, ok in results if ok)
    total = len(results)
    print(f"  Result: {passed}/{total} checks passed")
    if passed == total:
        print(f"  [{PASS}] Phase 2 acceptance test COMPLETE")
    else:
        failed = [label for label, ok in results if not ok]
        print(f"  [{FAIL}] {len(failed)} check(s) failed:")
        for f in failed:
            print(f"           • {f}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    ok = run()
    sys.exit(0 if ok else 1)
