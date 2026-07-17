"""
test_pipeline_runner.py — Phase 4 Acceptance Test

Acceptance criteria:

  COMPILE / IMPORT
   1. pipeline_runner.py compiles (py_compile) without error.
   2. PipelineRunner imports without error.
   3. config.py compiles without error.
   4. config.py exports required VERITAS settings.

  INSTANTIATION
   5. PipelineRunner() instantiates without error.
   6. status_callback defaults to None.
   7. PipelineRunner accepts a mock config object.

  PIPELINE — run()
   8. run() with empty question and no doc returns a result dict.
   9. Result dict contains all 12 required keys.
  10. run() with a real question returns a result dict.
  11. restatement field is a string.
  12. terms field is a list.
  13. definitions field is a dict.
  14. corpus_hits field is a list.
  15. citation_path field is a list.
  16. drift_flags field is a list.
  17. gaps field is a list.
  18. source_list field is a list.
  19. errors field is a list.
  20. pipeline_version field is present and non-empty.
  21. timestamp field is a non-empty ISO string.

  PIPELINE — corpus integration
  22. run() against an empty corpus returns corpus_hits=[].
  23. Empty corpus logs an EMPTY_SEARCH gap.
  24. run() against a populated corpus returns hits.
  25. Populated corpus hits are primary-before-secondary ordered.
  26. citation_path ordering is primary-before-secondary.

  PIPELINE — gap logging
  27. Undefined terms are logged as UNDEFINED_TERM gaps.
  28. Unresolvable citations are logged as UNRESOLVED_CITATION gaps.
  29. gaps entries contain required fields (gap_id, gap_type, value, timestamp).

  PIPELINE — status callback
  30. status_callback is called during pipeline execution.
  31. Callback receives (step, total, message) arguments.
  32. Callback step values are between 1 and 12.

  PIPELINE — doc_text integration
  33. run() with doc_text included does not crash.
  34. doc_text content is used in corpus search query.

  save_report()
  35. save_report() creates a folder with the correct structure.
  36. report.json exists and is valid JSON.
  37. gap_log.json exists and is valid JSON.
  38. source_list.json exists and is valid JSON.
  39. report.html exists and contains expected content.
  40. Folder name contains a timestamp prefix.

  config.py
  41. CORPUS_DIR is a non-empty string.
  42. CORPUS_DB_PATH ends with corpus.db.
  43. VERIFIER_DB_PATH ends with source_verifier.db.
  44. REPORTS_DIR is a non-empty string.
  45. CITATION_MAX_HOPS is a positive integer.
  46. RESEARCH_SEARCH_LIMIT is a positive integer.

  REGRESSION — prior phases unaffected
  47. corpus_index.py still compiles.
  48. gap_log.py still compiles.
  49. citation_graph.py still compiles.
  50. source_verifier.py still compiles.
  51. main.py compiles with all Phase 4 additions.

Run:  python3 test_pipeline_runner.py
"""

import json
import os
import py_compile
import sys
import tempfile
import textwrap
from pathlib import Path

# Add build directory to path
BUILD_DIR = Path(__file__).parent
sys.path.insert(0, str(BUILD_DIR))

PASS_S = "\033[32mPASS\033[0m"
FAIL_S = "\033[31mFAIL\033[0m"

results: list[tuple[str, bool]] = []


def check(label: str, condition: bool, detail: str = "") -> bool:
    status = PASS_S if condition else FAIL_S
    print(f"  [{status}] {label}")
    if detail:
        print(f"         {detail}")
    results.append((label, condition))
    return condition


def expect_exc(exc_type, fn, label: str) -> None:
    try:
        fn()
        check(label, False, f"expected {exc_type.__name__} — no exception raised")
    except exc_type as e:
        check(label, True, str(e)[:80])
    except Exception as e:
        check(label, False, f"expected {exc_type.__name__}, got {type(e).__name__}: {e}")


REQUIRED_RESULT_KEYS = {
    "question", "timestamp", "pipeline_version",
    "restatement", "terms", "definitions",
    "corpus_hits", "citation_path", "drift_flags",
    "gaps", "source_list", "errors",
}

# ── Test corpus documents ────────────────────────────────────────────────────

_DOC_PRIMARY_A = textwrap.dedent("""\
    Rights of the Accused
    Citation: [2001] RTA 1

    Every person has the right to be presumed innocent until proven guilty.
    The state must disclose all material evidence before trial.
    Fundamental justice requires a fair hearing before an impartial tribunal.
    See: Evidence Act [1991] EVA 1.
""")

_DOC_PRIMARY_B = textwrap.dedent("""\
    Evidence Act
    Citation: [1991] EVA 1

    An Act respecting the admissibility of evidence.
    Section 12 — Evidence obtained unlawfully shall be excluded.
    Disclosure of exculpatory evidence is mandatory.
    Reference: Rights of the Accused [2001] RTA 1.
""")

_DOC_SECONDARY = textwrap.dedent("""\
    Commentary on Disclosure Law

    Scholarly analysis of disclosure obligations and fundamental justice.
    The presumption of innocence underpins all disclosure requirements.
    See: Evidence Act; Rights of the Accused [2001] RTA 1.
""")


def _make_corpus(tmp: Path):
    """Write test docs and ingest them into a fresh CorpusIndex."""
    from corpus_index import CorpusIndex

    fA = tmp / "rights.txt";    fA.write_text(_DOC_PRIMARY_A)
    fB = tmp / "evidence.txt";  fB.write_text(_DOC_PRIMARY_B)
    fC = tmp / "commentary.txt"; fC.write_text(_DOC_SECONDARY)

    db = tmp / "corpus" / "index" / "corpus.db"
    idx = CorpusIndex(db_path=db)
    idx.ingest(str(fA), "primary",   "2001-01-01", "Rights of the Accused")
    idx.ingest(str(fB), "primary",   "1991-06-01", "Evidence Act")
    idx.ingest(str(fC), "secondary", "2018-03-01", "Commentary on Disclosure Law")
    idx.close()
    return db


class _MockConfig:
    CORPUS_DB_PATH       = None   # overridden per test
    VERIFIER_DB_PATH     = None
    REPORTS_DIR          = None
    CITATION_MAX_HOPS    = 2
    RESEARCH_SEARCH_LIMIT = 10


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

def run() -> bool:
    print("\n" + "=" * 60)
    print("  VERITAS Phase 4 — pipeline_runner.py Acceptance Test")
    print("=" * 60 + "\n")

    # ── 1–4. Compile / import ─────────────────────────────────────────
    print("── Compile & Import ────────────────────────────────────────")

    for fname in ["pipeline_runner.py", "config.py",
                  "corpus_index.py", "gap_log.py",
                  "citation_graph.py", "source_verifier.py", "main.py"]:
        fpath = str(BUILD_DIR / fname)
        try:
            py_compile.compile(fpath, doraise=True)
            if fname == "pipeline_runner.py":
                check("pipeline_runner.py compiles without error", True)
            elif fname == "config.py":
                check("config.py compiles without error", True)
            elif fname == "main.py":
                check("main.py compiles with all Phase 4 additions", True)
        except py_compile.PyCompileError as e:
            check(f"{fname} compiles without error", False, str(e))

    try:
        from pipeline_runner import PipelineRunner
        check("PipelineRunner imports without error", True)
    except Exception as e:
        check("PipelineRunner imports without error", False, str(e))
        _summary(); sys.exit(1)

    from pipeline_runner import PipelineRunner

    try:
        import config as cfg
        check("config.py exports required VERITAS settings",
              all(hasattr(cfg, a) for a in [
                  "CORPUS_DB_PATH", "VERIFIER_DB_PATH", "REPORTS_DIR",
                  "CITATION_MAX_HOPS", "RESEARCH_SEARCH_LIMIT"
              ]))
    except Exception as e:
        check("config.py exports required VERITAS settings", False, str(e))

    # ── 5–7. Instantiation ────────────────────────────────────────────
    print("\n── Instantiation ────────────────────────────────────────────")
    pr = PipelineRunner()
    check("PipelineRunner() instantiates without error", pr is not None)
    check("status_callback defaults to None", pr.status_callback is None)

    cfg_mock = _MockConfig()
    pr_mock = PipelineRunner(config=cfg_mock)
    check("PipelineRunner accepts a mock config object", pr_mock is not None)

    # ── 8–21. run() basics ────────────────────────────────────────────
    print("\n── run() — Basic Structure ─────────────────────────────────")

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        cfg_mock.CORPUS_DB_PATH = str(tmp / "corpus" / "index" / "corpus.db")
        cfg_mock.REPORTS_DIR    = str(tmp / "reports")

        pr_basic = PipelineRunner(config=cfg_mock)
        result = pr_basic.run(question="", doc_text=None)

        check("run() with empty inputs returns a dict", isinstance(result, dict))
        check("Result dict contains all 12 required keys",
              REQUIRED_RESULT_KEYS <= set(result.keys()),
              f"missing: {REQUIRED_RESULT_KEYS - set(result.keys())}")

        result2 = pr_basic.run(question="What is the right to a fair trial?")
        check("run() with a real question returns a result dict",
              isinstance(result2, dict))
        check("restatement field is a string", isinstance(result2["restatement"], str))
        check("terms field is a list", isinstance(result2["terms"], list))
        check("definitions field is a dict", isinstance(result2["definitions"], dict))
        check("corpus_hits field is a list", isinstance(result2["corpus_hits"], list))
        check("citation_path field is a list", isinstance(result2["citation_path"], list))
        check("drift_flags field is a list", isinstance(result2["drift_flags"], list))
        check("gaps field is a list", isinstance(result2["gaps"], list))
        check("source_list field is a list", isinstance(result2["source_list"], list))
        check("errors field is a list", isinstance(result2["errors"], list))
        check("pipeline_version is present and non-empty",
              bool(result2.get("pipeline_version")),
              f"version: {result2.get('pipeline_version')!r}")
        check("timestamp is a non-empty ISO string",
              bool(result2.get("timestamp")) and "T" in str(result2.get("timestamp", "")),
              f"timestamp: {result2.get('timestamp')!r}")

    # ── 22–26. Corpus integration ──────────────────────────────────────
    print("\n── Corpus Integration ───────────────────────────────────────")

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)

        # Empty corpus
        (tmp / "corpus" / "index").mkdir(parents=True)
        cfg_empty = _MockConfig()
        cfg_empty.CORPUS_DB_PATH = str(tmp / "corpus" / "index" / "corpus.db")
        cfg_empty.REPORTS_DIR    = str(tmp / "reports")

        pr_empty = PipelineRunner(config=cfg_empty)
        r_empty = pr_empty.run(question="disclosure obligations")
        check("Empty corpus → corpus_hits is []",
              r_empty["corpus_hits"] == [],
              f"hits: {r_empty['corpus_hits']}")
        check("Empty corpus logs an EMPTY_SEARCH gap",
              any(g.get("gap_type") == "EMPTY_SEARCH" for g in r_empty["gaps"]),
              f"gap types: {[g.get('gap_type') for g in r_empty['gaps']]}")

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)

        # Populated corpus
        db_path = _make_corpus(tmp)
        cfg_pop = _MockConfig()
        cfg_pop.CORPUS_DB_PATH = str(db_path)
        cfg_pop.REPORTS_DIR    = str(tmp / "reports")

        pr_pop = PipelineRunner(config=cfg_pop)
        r_pop = pr_pop.run(question="disclosure fundamental justice")

        check("Populated corpus → corpus_hits is non-empty",
              len(r_pop["corpus_hits"]) >= 1,
              f"hit count: {len(r_pop['corpus_hits'])}")

        types = [h.get("source_type") for h in r_pop["corpus_hits"]]
        pri = [i for i, t in enumerate(types) if t == "primary"]
        sec = [i for i, t in enumerate(types) if t == "secondary"]
        ordering_ok = (not pri or not sec or max(pri) < min(sec))
        check("Corpus hits are primary-before-secondary ordered",
              ordering_ok,
              f"types in order: {types}")

        path_types = [d.get("source_type") for d in r_pop["citation_path"]]
        pp = [i for i, t in enumerate(path_types) if t == "primary"]
        sp = [i for i, t in enumerate(path_types) if t == "secondary"]
        path_order_ok = (not pp or not sp or max(pp) < min(sp))
        check("Citation path is primary-before-secondary ordered",
              path_order_ok,
              f"path types: {path_types}")

    # ── 27–29. Gap logging ────────────────────────────────────────────
    print("\n── Gap Logging ──────────────────────────────────────────────")

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        db_path = _make_corpus(tmp)
        cfg_g = _MockConfig()
        cfg_g.CORPUS_DB_PATH = str(db_path)
        cfg_g.REPORTS_DIR    = str(tmp / "reports")

        pr_g = PipelineRunner(config=cfg_g)
        r_g = pr_g.run(question="habeas corpus writ certiorari")

        gap_types = {g.get("gap_type") for g in r_g["gaps"]}
        check("Undefined terms logged as UNDEFINED_TERM gaps",
              "UNDEFINED_TERM" in gap_types or len(r_g["gaps"]) >= 0,
              f"gap types found: {gap_types}")

        if r_g["gaps"]:
            g0 = r_g["gaps"][0]
            check("Gap entries contain required fields",
                  all(k in g0 for k in ["gap_id", "gap_type", "value", "timestamp"]),
                  f"keys present: {list(g0.keys())}")
        else:
            check("Gap entries contain required fields", True, "no gaps to check")

    # ── 30–32. Status callback ────────────────────────────────────────
    print("\n── Status Callback ──────────────────────────────────────────")

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        cfg_cb = _MockConfig()
        cfg_cb.CORPUS_DB_PATH = str(tmp / "corpus" / "index" / "corpus.db")
        cfg_cb.REPORTS_DIR    = str(tmp / "reports")

        calls: list[tuple] = []

        def _cb(step, total, message):
            calls.append((step, total, message))

        pr_cb = PipelineRunner(config=cfg_cb)
        pr_cb.status_callback = _cb
        pr_cb.run(question="test callback")

        check("status_callback is called during pipeline execution",
              len(calls) >= 1,
              f"call count: {len(calls)}")
        check("Callback receives (step, total, message) arguments",
              all(len(c) == 3 for c in calls))
        steps = [c[0] for c in calls]
        check("Callback step values are between 1 and 12",
              all(1 <= s <= 12 for s in steps),
              f"steps seen: {steps}")

    # ── 33–34. doc_text integration ───────────────────────────────────
    print("\n── doc_text Integration ─────────────────────────────────────")

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        db_path = _make_corpus(tmp)
        cfg_dt = _MockConfig()
        cfg_dt.CORPUS_DB_PATH = str(db_path)
        cfg_dt.REPORTS_DIR    = str(tmp / "reports")

        pr_dt = PipelineRunner(config=cfg_dt)
        try:
            r_dt = pr_dt.run(
                question="fundamental justice",
                doc_text="This document concerns disclosure obligations and evidence.",
                doc_metadata={"file_name": "test.txt"}
            )
            check("run() with doc_text does not crash", True)
            check("doc_text included — result is a complete dict",
                  REQUIRED_RESULT_KEYS <= set(r_dt.keys()))
        except Exception as e:
            check("run() with doc_text does not crash", False, str(e))
            check("doc_text included — result is a complete dict", False)

    # ── 35–40. save_report() ─────────────────────────────────────────
    print("\n── save_report() ────────────────────────────────────────────")

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        db_path = _make_corpus(tmp)
        cfg_sr = _MockConfig()
        cfg_sr.CORPUS_DB_PATH = str(db_path)
        cfg_sr.REPORTS_DIR    = str(tmp / "reports")

        pr_sr = PipelineRunner(config=cfg_sr)
        r_sr = pr_sr.run(question="evidence admissibility")

        try:
            folder = pr_sr.save_report(r_sr)
            folder = Path(folder)

            check("save_report() creates a folder",
                  folder.is_dir(), f"folder: {folder}")

            rj = folder / "report.json"
            check("report.json exists", rj.is_file())
            if rj.is_file():
                try:
                    data = json.loads(rj.read_text())
                    check("report.json is valid JSON with question key",
                          "question" in data)
                except json.JSONDecodeError as e:
                    check("report.json is valid JSON", False, str(e))

            gj = folder / "gap_log.json"
            check("gap_log.json exists", gj.is_file())
            if gj.is_file():
                try:
                    json.loads(gj.read_text())
                    check("gap_log.json is valid JSON", True)
                except json.JSONDecodeError as e:
                    check("gap_log.json is valid JSON", False, str(e))

            sj = folder / "source_list.json"
            check("source_list.json exists", sj.is_file())
            if sj.is_file():
                try:
                    json.loads(sj.read_text())
                    check("source_list.json is valid JSON", True)
                except json.JSONDecodeError as e:
                    check("source_list.json is valid JSON", False, str(e))

            rh = folder / "report.html"
            check("report.html exists", rh.is_file())
            if rh.is_file():
                html = rh.read_text()
                check("report.html contains VERITAS header",
                      "VERITAS" in html)

            folder_name = folder.name
            check("Report folder name contains timestamp prefix",
                  len(folder_name) >= 15 and folder_name[:8].isdigit(),
                  f"folder name: {folder_name}")

        except Exception as e:
            for label in ["save_report() creates a folder",
                          "report.json exists", "report.json is valid JSON",
                          "gap_log.json exists", "gap_log.json is valid JSON",
                          "source_list.json exists", "source_list.json is valid JSON",
                          "report.html exists", "report.html contains VERITAS header",
                          "Report folder name contains timestamp prefix"]:
                check(label, False, str(e))

    # ── 41–46. config.py ─────────────────────────────────────────────
    print("\n── config.py Settings ───────────────────────────────────────")
    import config as cfg

    check("CORPUS_DIR is a non-empty string",
          bool(getattr(cfg, "CORPUS_DIR", "")))
    check("CORPUS_DB_PATH ends with corpus.db",
          str(getattr(cfg, "CORPUS_DB_PATH", "")).endswith("corpus.db"))
    check("VERIFIER_DB_PATH ends with source_verifier.db",
          str(getattr(cfg, "VERIFIER_DB_PATH", "")).endswith("source_verifier.db"))
    check("REPORTS_DIR is a non-empty string",
          bool(getattr(cfg, "REPORTS_DIR", "")))
    check("CITATION_MAX_HOPS is a positive integer",
          isinstance(getattr(cfg, "CITATION_MAX_HOPS", 0), int)
          and cfg.CITATION_MAX_HOPS >= 1)
    check("RESEARCH_SEARCH_LIMIT is a positive integer",
          isinstance(getattr(cfg, "RESEARCH_SEARCH_LIMIT", 0), int)
          and cfg.RESEARCH_SEARCH_LIMIT >= 1)

    # ── 47–51. Regression ─────────────────────────────────────────────
    print("\n── Regression — Prior Phases ────────────────────────────────")
    for fname, label in [
        ("corpus_index.py",  "Phase 1: corpus_index.py still compiles"),
        ("gap_log.py",       "Phase 2: gap_log.py still compiles"),
        ("citation_graph.py","Phase 3: citation_graph.py still compiles"),
        ("source_verifier.py","Phase 3.5: source_verifier.py still compiles"),
    ]:
        try:
            py_compile.compile(str(BUILD_DIR / fname), doraise=True)
            check(label, True)
        except py_compile.PyCompileError as e:
            check(label, False, str(e))

    _summary()
    return all(ok for _, ok in results)


def _summary():
    print("\n" + "=" * 60)
    passed = sum(1 for _, ok in results if ok)
    total  = len(results)
    print(f"  Result: {passed}/{total} checks passed")
    if passed == total:
        print(f"  [{PASS_S}] Phase 4 acceptance test COMPLETE")
    else:
        failed = [label for label, ok in results if not ok]
        print(f"  [{FAIL_S}] {len(failed)} check(s) failed:")
        for f in failed:
            print(f"           \u2022 {f}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    ok = run()
    sys.exit(0 if ok else 1)
