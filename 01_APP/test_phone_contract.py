"""
test_phone_contract.py — Phase 6 Acceptance Test

Acceptance criteria:

  COMPILE / IMPORT
   1. phone_contract.py compiles without error.
   2. PhoneContract imports without error.
   3. Contract constants are present and correct.

  INSTANTIATION
   4. PhoneContract() instantiates without error.
   5. repr() works.

  validate_package()
   6. Returns a dict with keys: valid, errors, warnings, files.
   7. Missing folder → valid=False, error logged.
   8. Complete valid package → valid=True, no errors.
   9. Missing report.json → valid=False, error logged.
  10. Missing gap_log.json → valid=False, error logged.
  11. Missing source_list.json → valid=False, error logged.
  12. Missing report.html → valid=False, error logged.
  13. Missing report.txt → valid=False, error logged.
  14. Empty file → valid=False, error logged.
  15. report.json with bad JSON → valid=False, error logged.
  16. report.json missing required keys → valid=False, error logged.
  17. gap_log.json with invalid entry structure → error logged.
  18. gap_log.json with unknown gap_type → warning logged (not error).
  19. source_list.json with unknown source_type → warning logged.
  20. files dict contains all required filenames.

  write_manifest()
  21. Writes manifest.json into the package folder.
  22. manifest.json is valid JSON.
  23. manifest.json contains contract_version.
  24. manifest.json contains package_created timestamp.
  25. manifest.json contains the research question.
  26. manifest.json contains file inventory with sha256 checksums.
  27. manifest.json contains validation result.
  28. manifest.json contains phone_can and phone_cannot lists.
  29. write_manifest() raises FileNotFoundError for missing folder.
  30. write_manifest() raises ValueError for invalid package.

  read_manifest()
  31. read_manifest() returns the manifest dict.
  32. Returned dict matches what write_manifest() wrote.
  33. read_manifest() raises FileNotFoundError when manifest.json absent.
  34. read_manifest() raises ValueError for corrupt manifest.json.

  package_summary()
  35. Returns a dict with all required summary keys.
  36. question field matches report.json question.
  37. timestamp field is non-empty.
  38. corpus_hits count matches corpus_hits list length.
  39. citation_hops count matches citation_path list length.
  40. gap_count matches gap_log.json array length.
  41. source_count matches source_list.json array length.
  42. valid=True for a valid package.
  43. Falls back gracefully when manifest.json is absent.
  44. Returns safe defaults for a completely empty folder.

  PIPELINE INTEGRATION
  45. save_report() creates manifest.json automatically.
  46. manifest.json created by save_report() is valid.
  47. manifest.json contains the correct question.
  48. Checksums in manifest match actual file contents.

  REGRESSION
  49. corpus_index.py still compiles.
  50. gap_log.py still compiles.
  51. citation_graph.py still compiles.
  52. source_verifier.py still compiles.
  53. pipeline_runner.py still compiles.
  54. report_generator.py still compiles.
  55. main.py still compiles.

Run:  python3 test_phone_contract.py
"""

import hashlib
import json
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


def expect_exc(exc_type, fn, label: str) -> None:
    try:
        fn()
        check(label, False, f"expected {exc_type.__name__} — no exception raised")
    except exc_type as e:
        check(label, True, str(e)[:80])
    except Exception as e:
        check(label, False,
              f"expected {exc_type.__name__}, got {type(e).__name__}: {e}")


# ── Minimal valid package builder ────────────────────────────────────────────

SAMPLE_REPORT = {
    "question":         "What is the right to a fair trial?",
    "timestamp":        "2026-01-01T00:00:00+00:00",
    "pipeline_version": "4.0",
    "restatement":      "This question concerns the right to a fair trial.",
    "terms":            ["fair trial"],
    "definitions":      {"fair trial": {"plain_english": "Unbiased proceeding.",
                                        "doctrinal": ""}},
    "corpus_hits":      [{"doc_id": "a1", "title": "Rights Act",
                          "source_type": "primary", "doc_date": "2001-01-01",
                          "snippet": "", "rank": -0.9}],
    "citation_path":    [{"doc_id": "a1", "title": "Rights Act",
                          "source_type": "primary", "doc_date": "2001-01-01",
                          "self_cite": "[2001] RA 1", "citations": []}],
    "drift_flags":      [],
    "gaps":             [{"gap_id": "g1", "gap_type": "EMPTY_SEARCH",
                          "value": "habeas corpus", "source_doc_id": None,
                          "best_link": None,
                          "timestamp": "2026-01-01T00:00:00+00:00"}],
    "source_list":      [{"doc_id": "a1", "title": "Rights Act",
                          "source_type": "primary", "doc_date": "2001-01-01",
                          "self_cite": "[2001] RA 1", "path": ""}],
    "errors":           [],
}


def _write_valid_package(folder: Path) -> None:
    """Write a minimal valid report package into folder."""
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "report.json").write_text(
        json.dumps(SAMPLE_REPORT, indent=2), encoding="utf-8")
    (folder / "gap_log.json").write_text(
        json.dumps(SAMPLE_REPORT["gaps"], indent=2), encoding="utf-8")
    (folder / "source_list.json").write_text(
        json.dumps(SAMPLE_REPORT["source_list"], indent=2), encoding="utf-8")
    (folder / "report.html").write_text(
        "<!DOCTYPE html><html><body>VERITAS Research Map</body></html>",
        encoding="utf-8")
    (folder / "report.txt").write_text(
        "VERITAS RESEARCH MAP\nWhat is the right to a fair trial?\n",
        encoding="utf-8")


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

def run() -> bool:
    print("\n" + "=" * 60)
    print("  VERITAS Phase 6 — phone_contract.py Acceptance Test")
    print("=" * 60 + "\n")

    # ── 1–3. Compile / import ─────────────────────────────────────────
    print("── Compile & Import ────────────────────────────────────────")
    try:
        py_compile.compile(str(BUILD_DIR / "phone_contract.py"), doraise=True)
        check("phone_contract.py compiles without error", True)
    except py_compile.PyCompileError as e:
        check("phone_contract.py compiles without error", False, str(e))
        _summary(); sys.exit(1)

    try:
        from phone_contract import (
            PhoneContract, CONTRACT_VERSION,
            REQUIRED_FILES, REPORT_REQUIRED_KEYS,
            GAP_ENTRY_REQUIRED_KEYS, VALID_GAP_TYPES,
            SOURCE_ENTRY_REQUIRED_KEYS, VALID_SOURCE_TYPES,
            PHONE_CAN, PHONE_CANNOT,
        )
        check("PhoneContract imports without error", True)
        check("Contract constants are present and correct",
              CONTRACT_VERSION == "1.0"
              and len(REQUIRED_FILES) == 5
              and "report.json" in REQUIRED_FILES
              and "manifest.json" not in REQUIRED_FILES,
              f"version={CONTRACT_VERSION}, files={REQUIRED_FILES}")
    except Exception as e:
        check("PhoneContract imports without error", False, str(e))
        _summary(); sys.exit(1)

    from phone_contract import PhoneContract

    # ── 4–5. Instantiation ────────────────────────────────────────────
    print("\n── Instantiation ────────────────────────────────────────────")
    pc = PhoneContract()
    check("PhoneContract() instantiates without error", pc is not None)
    check("repr() works", "PhoneContract" in repr(pc))

    # ── 6–20. validate_package() ──────────────────────────────────────
    print("\n── validate_package() ───────────────────────────────────────")

    result_keys = {"valid", "errors", "warnings", "files"}
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)

        # Missing folder
        vr = pc.validate_package(str(tmp / "nonexistent"))
        check("Returns dict with required keys",
              result_keys <= set(vr.keys()))
        check("Missing folder → valid=False",
              not vr["valid"] and len(vr["errors"]) >= 1)

        # Valid package
        valid_folder = tmp / "valid"
        _write_valid_package(valid_folder)
        vr = pc.validate_package(str(valid_folder))
        check("Complete valid package → valid=True",
              vr["valid"],
              f"errors: {vr['errors']}")

        # Each missing required file
        for fname in ["report.json", "gap_log.json", "source_list.json",
                      "report.html", "report.txt"]:
            broken = tmp / f"missing_{fname}"
            _write_valid_package(broken)
            (broken / fname).unlink()
            vr = pc.validate_package(str(broken))
            check(f"Missing {fname} → valid=False",
                  not vr["valid"],
                  f"errors: {vr['errors'][:1]}")

        # Empty file
        empty = tmp / "empty_file"
        _write_valid_package(empty)
        (empty / "report.json").write_text("")
        vr = pc.validate_package(str(empty))
        check("Empty required file → valid=False", not vr["valid"])

        # Bad JSON in report.json
        bad_json = tmp / "bad_json"
        _write_valid_package(bad_json)
        (bad_json / "report.json").write_text("{not valid json{{")
        vr = pc.validate_package(str(bad_json))
        check("report.json with bad JSON → valid=False", not vr["valid"])

        # Missing required key in report.json
        missing_key = tmp / "missing_key"
        _write_valid_package(missing_key)
        data = dict(SAMPLE_REPORT)
        del data["question"]
        (missing_key / "report.json").write_text(json.dumps(data))
        vr = pc.validate_package(str(missing_key))
        check("report.json missing required key → valid=False", not vr["valid"])

        # gap_log.json invalid entry
        bad_gap = tmp / "bad_gap"
        _write_valid_package(bad_gap)
        (bad_gap / "gap_log.json").write_text(
            json.dumps([{"gap_id": "x"}]))  # missing gap_type, value, timestamp
        vr = pc.validate_package(str(bad_gap))
        check("gap_log.json with missing entry keys → error logged",
              len(vr["errors"]) >= 1,
              f"errors: {vr['errors']}")

        # gap_log.json unknown gap_type → warning not error
        warn_gap = tmp / "warn_gap"
        _write_valid_package(warn_gap)
        (warn_gap / "gap_log.json").write_text(json.dumps([{
            "gap_id": "g1", "gap_type": "UNKNOWN_TYPE",
            "value": "x", "timestamp": "2026-01-01T00:00:00+00:00"
        }]))
        vr = pc.validate_package(str(warn_gap))
        check("gap_log.json with unknown gap_type → warning, not error",
              vr["valid"] and len(vr["warnings"]) >= 1,
              f"valid={vr['valid']}, warnings={vr['warnings']}")

        # source_list.json unknown source_type → warning
        warn_src = tmp / "warn_src"
        _write_valid_package(warn_src)
        (warn_src / "source_list.json").write_text(json.dumps([{
            "doc_id": "x", "title": "X", "source_type": "tertiary"
        }]))
        vr = pc.validate_package(str(warn_src))
        check("source_list.json unknown source_type → warning",
              vr["valid"] and len(vr["warnings"]) >= 1)

        # files dict completeness
        vr_full = pc.validate_package(str(valid_folder))
        check("files dict contains all required filenames",
              all(f in vr_full["files"] for f in
                  ["report.json", "gap_log.json", "source_list.json",
                   "report.html", "report.txt"]))

    # ── 21–30. write_manifest() ───────────────────────────────────────
    print("\n── write_manifest() ─────────────────────────────────────────")

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        pkg = tmp / "pkg"
        _write_valid_package(pkg)

        mp = pc.write_manifest(str(pkg))
        check("write_manifest() writes manifest.json",
              Path(mp).is_file() and Path(mp).name == "manifest.json")

        try:
            m = json.loads(Path(mp).read_text(encoding="utf-8"))
            check("manifest.json is valid JSON", True)
            check("manifest.json contains contract_version",
                  "contract_version" in m and m["contract_version"] == "1.0")
            check("manifest.json contains package_created",
                  bool(m.get("package_created")))
            check("manifest.json contains the question",
                  m.get("question") == SAMPLE_REPORT["question"])
            check("manifest.json contains file inventory with sha256",
                  "files" in m and all(
                      "sha256" in v for v in m["files"].values()
                  ),
                  f"files keys: {list(m.get('files', {}).keys())}")
            check("manifest.json contains validation result",
                  "validation" in m and "valid" in m["validation"])
            check("manifest.json contains phone_can and phone_cannot",
                  isinstance(m.get("phone_can"), list)
                  and isinstance(m.get("phone_cannot"), list)
                  and len(m["phone_can"]) >= 1
                  and len(m["phone_cannot"]) >= 1)
        except Exception as e:
            for label in ["manifest.json is valid JSON",
                          "manifest.json contains contract_version",
                          "manifest.json contains package_created",
                          "manifest.json contains the question",
                          "manifest.json contains file inventory with sha256",
                          "manifest.json contains validation result",
                          "manifest.json contains phone_can and phone_cannot"]:
                check(label, False, str(e))

        # Error cases
        expect_exc(FileNotFoundError,
                   lambda: pc.write_manifest(str(tmp / "missing")),
                   "write_manifest() raises FileNotFoundError for missing folder")

        broken = tmp / "broken"
        broken.mkdir()
        expect_exc(ValueError,
                   lambda: pc.write_manifest(str(broken)),
                   "write_manifest() raises ValueError for invalid package")

    # ── 31–34. read_manifest() ────────────────────────────────────────
    print("\n── read_manifest() ──────────────────────────────────────────")

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        pkg = tmp / "pkg"
        _write_valid_package(pkg)
        pc.write_manifest(str(pkg))

        m = pc.read_manifest(str(pkg))
        check("read_manifest() returns the manifest dict",
              isinstance(m, dict) and "contract_version" in m)
        check("Returned dict matches what write_manifest() wrote",
              m.get("question") == SAMPLE_REPORT["question"])

        expect_exc(FileNotFoundError,
                   lambda: pc.read_manifest(str(tmp / "no_manifest")),
                   "read_manifest() raises FileNotFoundError when absent")

        corrupt = tmp / "corrupt"
        corrupt.mkdir()
        (corrupt / "manifest.json").write_text("{bad json{{")
        expect_exc(ValueError,
                   lambda: pc.read_manifest(str(corrupt)),
                   "read_manifest() raises ValueError for corrupt manifest")

    # ── 35–44. package_summary() ──────────────────────────────────────
    print("\n── package_summary() ────────────────────────────────────────")
    SUMMARY_KEYS = {"folder", "question", "timestamp", "valid",
                    "corpus_hits", "citation_hops", "gap_count", "source_count"}

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        pkg = tmp / "pkg"
        _write_valid_package(pkg)
        pc.write_manifest(str(pkg))

        s = pc.package_summary(str(pkg))
        check("package_summary() returns dict with all required keys",
              SUMMARY_KEYS <= set(s.keys()),
              f"missing: {SUMMARY_KEYS - set(s.keys())}")
        check("question matches report.json",
              s["question"] == SAMPLE_REPORT["question"])
        check("timestamp is non-empty", bool(s["timestamp"]))
        check("corpus_hits count is correct",
              s["corpus_hits"] == len(SAMPLE_REPORT["corpus_hits"]),
              f"got {s['corpus_hits']}, expected {len(SAMPLE_REPORT['corpus_hits'])}")
        check("citation_hops count is correct",
              s["citation_hops"] == len(SAMPLE_REPORT["citation_path"]),
              f"got {s['citation_hops']}, expected {len(SAMPLE_REPORT['citation_path'])}")
        check("gap_count is correct",
              s["gap_count"] == len(SAMPLE_REPORT["gaps"]),
              f"got {s['gap_count']}, expected {len(SAMPLE_REPORT['gaps'])}")
        check("source_count is correct",
              s["source_count"] == len(SAMPLE_REPORT["source_list"]),
              f"got {s['source_count']}, expected {len(SAMPLE_REPORT['source_list'])}")
        check("valid=True for valid package", s["valid"] is True)

        # No manifest fallback
        pkg2 = tmp / "pkg2"
        _write_valid_package(pkg2)
        s2 = pc.package_summary(str(pkg2))
        check("Falls back gracefully without manifest.json",
              SUMMARY_KEYS <= set(s2.keys()) and s2["question"] != "")

        # Empty folder
        empty = tmp / "empty"
        empty.mkdir()
        s3 = pc.package_summary(str(empty))
        check("Returns safe defaults for empty folder",
              SUMMARY_KEYS <= set(s3.keys()) and s3["valid"] is False)

    # ── 45–48. Pipeline integration ───────────────────────────────────
    print("\n── Pipeline Integration ─────────────────────────────────────")

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)

        from corpus_index import CorpusIndex
        doc = tmp / "rights.txt"
        doc.write_text("Rights of the Accused\nCitation: [2001] RTA 1\n"
                       "Every person has the right to a fair trial.\n")
        db = tmp / "corpus" / "index" / "corpus.db"
        idx = CorpusIndex(db_path=db)
        idx.ingest(str(doc), "primary", "2001-01-01", "Rights of the Accused")
        idx.close()

        class _Cfg:
            CORPUS_DB_PATH        = str(db)
            VERIFIER_DB_PATH      = None
            REPORTS_DIR           = str(tmp / "reports")
            CITATION_MAX_HOPS     = 2
            RESEARCH_SEARCH_LIMIT = 10

        from pipeline_runner import PipelineRunner
        pr = PipelineRunner(config=_Cfg())
        result = pr.run(question="fair trial rights")
        folder = Path(pr.save_report(result))

        check("save_report() creates manifest.json automatically",
              (folder / "manifest.json").is_file(),
              f"folder: {folder}")

        try:
            m = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
            check("manifest.json created by save_report() is valid JSON",
                  "contract_version" in m)
            check("manifest.json contains correct question",
                  m.get("question") == "fair trial rights")

            # Verify one checksum
            rj_actual = hashlib.sha256(
                (folder / "report.json").read_bytes()
            ).hexdigest()
            rj_manifest = m.get("files", {}).get("report.json", {}).get("sha256", "")
            check("Checksums in manifest match actual file contents",
                  rj_actual == rj_manifest,
                  f"actual={rj_actual[:16]}… manifest={rj_manifest[:16]}…")
        except Exception as e:
            for label in [
                "manifest.json created by save_report() is valid JSON",
                "manifest.json contains correct question",
                "Checksums in manifest match actual file contents",
            ]:
                check(label, False, str(e))

    # ── 49–55. Regression ─────────────────────────────────────────────
    print("\n── Regression ───────────────────────────────────────────────")
    for fname, label in [
        ("corpus_index.py",   "Phase 1: corpus_index.py"),
        ("gap_log.py",        "Phase 2: gap_log.py"),
        ("citation_graph.py", "Phase 3: citation_graph.py"),
        ("source_verifier.py","Phase 3.5: source_verifier.py"),
        ("pipeline_runner.py","Phase 4: pipeline_runner.py"),
        ("report_generator.py","Phase 5: report_generator.py"),
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
        print(f"  [{PASS_S}] Phase 6 acceptance test COMPLETE")
    else:
        failed = [label for label, ok in results if not ok]
        print(f"  [{FAIL_S}] {len(failed)} check(s) failed:")
        for f in failed:
            print(f"           • {f}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    ok = run()
    sys.exit(0 if ok else 1)
