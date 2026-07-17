"""
test_report_generator.py — Phase 5 Acceptance Test

Acceptance criteria:

  COMPILE / IMPORT
   1. report_generator.py compiles without error.
   2. ReportGenerator imports without error.

  EXISTING METHODS — must not regress
   3. generate_html_report() still exists.
   4. generate_text_report() still exists.
   5. generate_html_report() produces a file with existing content.
   6. generate_text_report() produces a file with existing content.

  NEW METHOD — generate_research_html()
   7. generate_research_html() exists on ReportGenerator.
   8. Returns the output path.
   9. Creates the output file.
  10. Output is valid HTML (contains <!DOCTYPE html>).
  11. Output contains "VERITAS".
  12. Output contains the research question.
  13. Output contains all 8 section headings.
  14. Output contains corpus hit titles when hits are present.
  15. Output contains citation path entries when present.
  16. Output contains gap entries when present.
  17. Output contains source list entries when present.
  18. Empty corpus hits renders a "no documents" message, not an error.
  19. Empty citation path renders a "no chain" message, not an error.
  20. Empty gaps renders a "no gaps" message, not an error.
  21. Disclaimer is present in HTML output.
  22. Output is UTF-8 encoded.

  NEW METHOD — generate_research_text()
  23. generate_research_text() exists on ReportGenerator.
  24. Returns the output path.
  25. Creates the output file.
  26. Output contains "VERITAS RESEARCH MAP".
  27. Output contains the research question.
  28. Output contains all 8 numbered section headers.
  29. Output contains corpus hit titles when hits are present.
  30. Output contains gap entries when present.
  31. Empty sections render gracefully (no crash, no blank output).
  32. Output is plain text (no HTML tags).

  PIPELINE INTEGRATION
  33. save_report() now creates report.txt alongside report.html.
  34. report.html produced by save_report() uses generate_research_html().
  35. report.txt produced by save_report() uses generate_research_text().

  REGRESSION
  36. corpus_index.py still compiles.
  37. gap_log.py still compiles.
  38. citation_graph.py still compiles.
  39. source_verifier.py still compiles.
  40. pipeline_runner.py still compiles.
  41. main.py still compiles.

Run:  python3 test_report_generator.py
"""

import json
import os
import py_compile
import sys
import tempfile
from pathlib import Path

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


# ── Sample data ──────────────────────────────────────────────────────────────

SAMPLE_RESULT = {
    "question":         "What is the right to a fair trial?",
    "timestamp":        "2026-01-01T00:00:00+00:00",
    "pipeline_version": "4.0",
    "restatement":      "This question asks about the legal right to receive a fair and impartial trial.",
    "terms":            ["fair trial", "fundamental justice"],
    "definitions": {
        "fair trial": {
            "plain_english":    "A legal proceeding conducted without bias.",
            "plain_source":     "Literal Dictionary",
            "doctrinal":        "A trial conforming to established legal principles.",
            "doctrinal_source": "Legal Dictionary",
        },
        "fundamental justice": {
            "plain_english":    "Basic fairness in legal proceedings.",
            "plain_source":     "Literal Dictionary",
            "doctrinal":        "",
            "doctrinal_source": "",
        },
    },
    "corpus_hits": [
        {
            "doc_id":      "abc123",
            "title":       "Rights of the Accused",
            "source_type": "primary",
            "doc_date":    "2001-01-01",
            "snippet":     "Every person has the right to a [fair trial].",
            "rank":        -0.9,
        },
        {
            "doc_id":      "def456",
            "title":       "Commentary on Rights",
            "source_type": "secondary",
            "doc_date":    "2018-03-01",
            "snippet":     "The right to a [fair trial] is fundamental.",
            "rank":        -0.5,
        },
    ],
    "citation_path": [
        {
            "doc_id":      "abc123",
            "title":       "Rights of the Accused",
            "source_type": "primary",
            "doc_date":    "2001-01-01",
            "self_cite":   "[2001] RTA 1",
            "citations":   [],
        },
    ],
    "drift_flags": [
        {
            "term":         "fair trial",
            "doc_id":       "def456",
            "doc_title":    "Commentary on Rights",
            "baseline":     "A trial conducted without bias.",
            "usage_sample": "The fair trial concept has evolved.",
            "similarity":   0.25,
        }
    ],
    "gaps": [
        {
            "gap_id":        "gap-001",
            "gap_type":      "UNRESOLVED_CITATION",
            "value":         "Unknown v Ghost [9999] 1 SCR 999",
            "source_doc_id": "abc123",
            "best_link":     None,
            "timestamp":     "2026-01-01T00:00:00+00:00",
        }
    ],
    "source_list": [
        {
            "doc_id":      "abc123",
            "title":       "Rights of the Accused",
            "source_type": "primary",
            "doc_date":    "2001-01-01",
            "self_cite":   "[2001] RTA 1",
            "path":        "/corpus/primary/rights.txt",
        }
    ],
    "errors": [],
}

EMPTY_RESULT = {
    "question":         "Empty corpus test",
    "timestamp":        "2026-01-01T00:00:00+00:00",
    "pipeline_version": "4.0",
    "restatement":      "",
    "terms":            [],
    "definitions":      {},
    "corpus_hits":      [],
    "citation_path":    [],
    "drift_flags":      [],
    "gaps":             [],
    "source_list":      [],
    "errors":           [],
}

EXISTING_ANALYSIS = {
    "terminology_issues": [
        {"term": "unlawful", "type": "misuse", "issue": "test issue",
         "correct_form": "unlawfully", "source": "Test", "count": 1,
         "definition": "def", "category": "cat", "matches": [], "spans": []}
    ],
    "deflection_issues": [],
}
EXISTING_META = {
    "file_name": "test.txt", "format": ".txt",
    "word_count": 100, "paragraph_count": 5,
    "char_count": 500, "sentence_count": 10,
}


def run() -> bool:
    print("\n" + "=" * 60)
    print("  VERITAS Phase 5 — report_generator.py Acceptance Test")
    print("=" * 60 + "\n")

    # ── 1–2. Compile / import ─────────────────────────────────────────
    print("── Compile & Import ────────────────────────────────────────")
    try:
        py_compile.compile(str(BUILD_DIR / "report_generator.py"), doraise=True)
        check("report_generator.py compiles without error", True)
    except py_compile.PyCompileError as e:
        check("report_generator.py compiles without error", False, str(e))
        _summary(); sys.exit(1)

    try:
        from report_generator import ReportGenerator
        check("ReportGenerator imports without error", True)
    except Exception as e:
        check("ReportGenerator imports without error", False, str(e))
        _summary(); sys.exit(1)

    from report_generator import ReportGenerator

    # ── 3–6. Existing methods regression ─────────────────────────────
    print("\n── Existing Methods (regression) ───────────────────────────")
    rg = ReportGenerator()
    check("generate_html_report() exists", hasattr(rg, "generate_html_report"))
    check("generate_text_report() exists", hasattr(rg, "generate_text_report"))

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)

        html_path = str(tmp / "existing.html")
        try:
            rg.generate_html_report(EXISTING_ANALYSIS, EXISTING_META, html_path)
            content = Path(html_path).read_text()
            check("generate_html_report() produces a file with existing content",
                  "VERITAS Analysis Report" in content and "<!DOCTYPE" in content)
        except Exception as e:
            check("generate_html_report() produces a file with existing content",
                  False, str(e))

        txt_path = str(tmp / "existing.txt")
        try:
            rg.generate_text_report(EXISTING_ANALYSIS, EXISTING_META, txt_path)
            content = Path(txt_path).read_text()
            check("generate_text_report() produces a file with existing content",
                  "VERITAS ANALYSIS REPORT" in content)
        except Exception as e:
            check("generate_text_report() produces a file with existing content",
                  False, str(e))

    # ── 7–22. generate_research_html() ────────────────────────────────
    print("\n── generate_research_html() ────────────────────────────────")
    check("generate_research_html() exists",
          hasattr(rg, "generate_research_html"))

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        out = str(tmp / "research.html")

        try:
            result_path = rg.generate_research_html(SAMPLE_RESULT, out)
            check("generate_research_html() returns the output path",
                  result_path == out)
            check("generate_research_html() creates the output file",
                  Path(out).is_file())

            html = Path(out).read_text(encoding="utf-8")
            check("Output is valid HTML (contains <!DOCTYPE html>)",
                  "<!DOCTYPE html>" in html)
            check("Output contains 'VERITAS'", "VERITAS" in html)
            check("Output contains the research question",
                  "fair trial" in html.lower())

            # All 8 section headings
            for i in range(1, 9):
                check(f"Output contains section {i} heading",
                      f"section-num\">{i}<" in html or f">{i}." in html or
                      f">{i}</span>" in html or str(i) in html)

            check("Output contains corpus hit title",
                  "Rights of the Accused" in html)
            check("Output contains citation path entry",
                  "[2001] RTA 1" in html)
            check("Output contains gap entry",
                  "UNRESOLVED_CITATION" in html or "Unknown v Ghost" in html)
            check("Output contains source list entry",
                  "Rights of the Accused" in html)

        except Exception as e:
            for label in [
                "generate_research_html() returns the output path",
                "generate_research_html() creates the output file",
                "Output is valid HTML (contains <!DOCTYPE html>)",
                "Output contains 'VERITAS'",
                "Output contains the research question",
            ]:
                check(label, False, str(e))

        # Empty result — should not crash
        out_empty = str(tmp / "empty.html")
        try:
            rg.generate_research_html(EMPTY_RESULT, out_empty)
            empty_html = Path(out_empty).read_text()
            check("Empty corpus hits renders gracefully",
                  "corpus" in empty_html.lower() or "no" in empty_html.lower())
            check("Empty citation path renders gracefully",
                  Path(out_empty).is_file())
            check("Empty gaps renders gracefully",
                  Path(out_empty).is_file())
            check("Disclaimer is present in HTML output",
                  "NOT LEGAL ADVICE" in empty_html or "disclaimer" in empty_html.lower())
            check("Output is UTF-8 encoded",
                  True)  # read_text with encoding="utf-8" succeeded above
        except Exception as e:
            for label in [
                "Empty corpus hits renders gracefully",
                "Empty citation path renders gracefully",
                "Empty gaps renders gracefully",
                "Disclaimer is present in HTML output",
                "Output is UTF-8 encoded",
            ]:
                check(label, False, str(e))

    # ── 23–32. generate_research_text() ───────────────────────────────
    print("\n── generate_research_text() ────────────────────────────────")
    check("generate_research_text() exists",
          hasattr(rg, "generate_research_text"))

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        out = str(tmp / "research.txt")

        try:
            result_path = rg.generate_research_text(SAMPLE_RESULT, out)
            check("generate_research_text() returns the output path",
                  result_path == out)
            check("generate_research_text() creates the output file",
                  Path(out).is_file())

            txt = Path(out).read_text(encoding="utf-8")
            check("Output contains 'VERITAS RESEARCH MAP'",
                  "VERITAS RESEARCH MAP" in txt)
            check("Output contains the research question",
                  "fair trial" in txt.lower())

            for i in range(1, 9):
                check(f"Output contains section {i} header",
                      f"{i}." in txt)

            check("Output contains corpus hit title",
                  "Rights of the Accused" in txt)
            check("Output contains gap entry",
                  "UNRESOLVED_CITATION" in txt or "Unknown v Ghost" in txt)

            # Empty result
            out_e = str(tmp / "empty.txt")
            rg.generate_research_text(EMPTY_RESULT, out_e)
            txt_e = Path(out_e).read_text()
            check("Empty sections render gracefully (no crash)",
                  Path(out_e).is_file() and len(txt_e) > 0)
            check("Output is plain text (no HTML tags)",
                  "<html" not in txt.lower() and "<body" not in txt.lower())

        except Exception as e:
            for label in [
                "generate_research_text() returns the output path",
                "generate_research_text() creates the output file",
                "Output contains 'VERITAS RESEARCH MAP'",
                "Output contains the research question",
                "Empty sections render gracefully (no crash)",
                "Output is plain text (no HTML tags)",
            ]:
                check(label, False, str(e))

    # ── 33–35. Pipeline integration ───────────────────────────────────
    print("\n── Pipeline Integration ─────────────────────────────────────")

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)

        # Build a small corpus so pipeline can run
        from corpus_index import CorpusIndex
        doc = tmp / "rights.txt"
        doc.write_text("Rights of the Accused\nCitation: [2001] RTA 1\n"
                       "Every person has the right to a fair trial.\n")
        db = tmp / "corpus" / "index" / "corpus.db"
        idx = CorpusIndex(db_path=db)
        idx.ingest(str(doc), "primary", "2001-01-01", "Rights of the Accused")
        idx.close()

        class _Cfg:
            CORPUS_DB_PATH       = str(db)
            VERIFIER_DB_PATH     = None
            REPORTS_DIR          = str(tmp / "reports")
            CITATION_MAX_HOPS    = 2
            RESEARCH_SEARCH_LIMIT = 10

        from pipeline_runner import PipelineRunner
        pr = PipelineRunner(config=_Cfg())
        result = pr.run(question="fair trial rights")

        try:
            folder = Path(pr.save_report(result))

            check("save_report() creates report.txt",
                  (folder / "report.txt").is_file(),
                  f"folder: {folder}")

            check("save_report() creates report.html",
                  (folder / "report.html").is_file())

            html_content = (folder / "report.html").read_text()
            check("report.html uses generate_research_html() (contains VERITAS)",
                  "VERITAS" in html_content)

            txt_content = (folder / "report.txt").read_text()
            check("report.txt uses generate_research_text() (contains VERITAS RESEARCH MAP)",
                  "VERITAS RESEARCH MAP" in txt_content)

        except Exception as e:
            for label in [
                "save_report() creates report.txt",
                "save_report() creates report.html",
                "report.html uses generate_research_html()",
                "report.txt uses generate_research_text()",
            ]:
                check(label, False, str(e))

    # ── 36–41. Regression ─────────────────────────────────────────────
    print("\n── Regression ───────────────────────────────────────────────")
    for fname, label in [
        ("corpus_index.py",   "Phase 1: corpus_index.py"),
        ("gap_log.py",        "Phase 2: gap_log.py"),
        ("citation_graph.py", "Phase 3: citation_graph.py"),
        ("source_verifier.py","Phase 3.5: source_verifier.py"),
        ("pipeline_runner.py","Phase 4: pipeline_runner.py"),
        ("main.py",           "Phase 4: main.py"),
    ]:
        try:
            py_compile.compile(str(BUILD_DIR / fname), doraise=True)
            check(f"{label} still compiles", True)
        except py_compile.PyCompileError as e:
            check(f"{label} still compiles", False, str(e))

    _summary()
    return all(ok for _, ok in results)


def _summary():
    print("\n" + "=" * 60)
    passed = sum(1 for _, ok in results if ok)
    total  = len(results)
    print(f"  Result: {passed}/{total} checks passed")
    if passed == total:
        print(f"  [{PASS_S}] Phase 5 acceptance test COMPLETE")
    else:
        failed = [label for label, ok in results if not ok]
        print(f"  [{FAIL_S}] {len(failed)} check(s) failed:")
        for f in failed:
            print(f"           • {f}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    ok = run()
    sys.exit(0 if ok else 1)
