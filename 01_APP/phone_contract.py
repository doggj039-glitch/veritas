"""
phone_contract.py — VERITAS Phase 6

Defines, validates, and documents the phone viewer data contract.

The phone app's only job is reading and displaying research records that
the desktop already produced. It never runs the pipeline, never searches
the corpus, never follows citations, and never generates reports.

This module is the single source of truth for:
  - The exact structure of every file in a report package
  - What the phone is and is not allowed to do
  - Validation so the desktop can confirm a package is phone-readable
    before saving it

Report package layout (one folder per research session)
-------------------------------------------------------
    reports/<timestamp>_<slug>/
        report.json        — full research map (8 sections)
        gap_log.json       — missing information entries
        source_list.json   — flat bibliography
        report.html        — rendered HTML for offline reading
        report.txt         — plain text version
        manifest.json      — package metadata + integrity checksums

Public API
----------
    PhoneContract()
    .validate_package(folder_path)  -> dict  {valid, errors, warnings}
    .write_manifest(folder_path)    -> str   (manifest.json path)
    .read_manifest(folder_path)     -> dict
    .package_summary(folder_path)   -> dict  (phone-safe display metadata)
"""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Contract version
# ---------------------------------------------------------------------------

CONTRACT_VERSION = "1.0"

# ---------------------------------------------------------------------------
# Required files in every report package
# ---------------------------------------------------------------------------

REQUIRED_FILES = [
    "report.json",
    "gap_log.json",
    "source_list.json",
    "report.html",
    "report.txt",
]

# ---------------------------------------------------------------------------
# report.json — required top-level keys
# ---------------------------------------------------------------------------

REPORT_REQUIRED_KEYS = {
    "question",
    "timestamp",
    "pipeline_version",
    "restatement",
    "terms",
    "definitions",
    "corpus_hits",
    "citation_path",
    "drift_flags",
    "gaps",
    "source_list",
    "errors",
}

# ---------------------------------------------------------------------------
# gap_log.json — required keys per entry
# ---------------------------------------------------------------------------

GAP_ENTRY_REQUIRED_KEYS = {
    "gap_id",
    "gap_type",
    "value",
    "timestamp",
}

VALID_GAP_TYPES = {
    "UNRESOLVED_CITATION",
    "UNDEFINED_TERM",
    "EMPTY_SEARCH",
}

# ---------------------------------------------------------------------------
# source_list.json — required keys per entry
# ---------------------------------------------------------------------------

SOURCE_ENTRY_REQUIRED_KEYS = {
    "doc_id",
    "title",
    "source_type",
}

VALID_SOURCE_TYPES = {"primary", "secondary"}

# ---------------------------------------------------------------------------
# Phone navigation features (documentation — enforced by the phone app)
# ---------------------------------------------------------------------------

PHONE_CAN = [
    "Open a saved report package from the reports/ folder.",
    "Display all 8 report sections for reading.",
    "Jump to a section by number (1–8).",
    "Follow an internal link from the gap log to its source document entry.",
    "Display the source list with title, type, date, and citation.",
    "Show the manifest (package metadata and checksums).",
]

PHONE_CANNOT = [
    "Run the research pipeline.",
    "Search the corpus.",
    "Follow citations.",
    "Generate new reports.",
    "Modify any file in the package.",
    "Access the internet.",
    "Accept typed research questions (read-only viewer only).",
]


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def _sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _file_size(path: str) -> int:
    try:
        return os.path.getsize(path)
    except OSError:
        return 0


# ---------------------------------------------------------------------------
# PhoneContract
# ---------------------------------------------------------------------------

class PhoneContract:
    """
    Validates report packages against the VERITAS phone viewer contract
    and writes the manifest.json file that the phone app reads first.
    """

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def validate_package(self, folder_path: str) -> dict:
        """
        Validate a report package folder against the phone contract.

        Checks:
          - All required files are present.
          - report.json is valid JSON with all required keys.
          - gap_log.json is a valid JSON array; entries have required keys.
          - source_list.json is a valid JSON array; entries have required keys.
          - report.html and report.txt are non-empty.

        Parameters
        ----------
        folder_path : Path to the report package folder.

        Returns
        -------
        dict with keys:
            valid    : bool   — True if all required checks pass
            errors   : list   — blocking problems (package unusable by phone)
            warnings : list   — non-blocking issues (package usable but imperfect)
            files    : dict   — per-file presence and size
        """
        folder = Path(folder_path)
        errors:   list[str] = []
        warnings: list[str] = []
        files:    dict      = {}

        if not folder.is_dir():
            return {
                "valid":    False,
                "errors":   [f"Folder does not exist: {folder_path}"],
                "warnings": [],
                "files":    {},
            }

        # ── File presence ─────────────────────────────────────────────
        for fname in REQUIRED_FILES:
            fpath = folder / fname
            exists = fpath.is_file()
            size   = _file_size(str(fpath)) if exists else 0
            files[fname] = {"present": exists, "size_bytes": size}
            if not exists:
                errors.append(f"Missing required file: {fname}")
            elif size == 0:
                errors.append(f"Required file is empty: {fname}")

        # ── report.json ───────────────────────────────────────────────
        rj = folder / "report.json"
        if rj.is_file() and _file_size(str(rj)) > 0:
            try:
                data = json.loads(rj.read_text(encoding="utf-8"))
                if not isinstance(data, dict):
                    errors.append("report.json must be a JSON object, not an array.")
                else:
                    missing = REPORT_REQUIRED_KEYS - set(data.keys())
                    if missing:
                        errors.append(
                            f"report.json missing required keys: {sorted(missing)}"
                        )
                    # Soft checks
                    if not data.get("question", "").strip():
                        warnings.append("report.json: 'question' is empty.")
                    if not data.get("timestamp", "").strip():
                        warnings.append("report.json: 'timestamp' is empty.")
                    if not isinstance(data.get("corpus_hits"), list):
                        errors.append("report.json: 'corpus_hits' must be a list.")
                    if not isinstance(data.get("citation_path"), list):
                        errors.append("report.json: 'citation_path' must be a list.")
                    if not isinstance(data.get("gaps"), list):
                        errors.append("report.json: 'gaps' must be a list.")
                    if not isinstance(data.get("source_list"), list):
                        errors.append("report.json: 'source_list' must be a list.")
            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                errors.append(f"report.json is not valid JSON: {e}")

        # ── gap_log.json ──────────────────────────────────────────────
        gj = folder / "gap_log.json"
        if gj.is_file() and _file_size(str(gj)) > 0:
            try:
                gaps = json.loads(gj.read_text(encoding="utf-8"))
                if not isinstance(gaps, list):
                    errors.append("gap_log.json must be a JSON array.")
                else:
                    for i, entry in enumerate(gaps):
                        missing = GAP_ENTRY_REQUIRED_KEYS - set(entry.keys())
                        if missing:
                            errors.append(
                                f"gap_log.json entry {i} missing keys: {sorted(missing)}"
                            )
                        gt = entry.get("gap_type", "")
                        if gt not in VALID_GAP_TYPES:
                            warnings.append(
                                f"gap_log.json entry {i} has unknown gap_type: {gt!r}"
                            )
            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                errors.append(f"gap_log.json is not valid JSON: {e}")

        # ── source_list.json ──────────────────────────────────────────
        sj = folder / "source_list.json"
        if sj.is_file() and _file_size(str(sj)) > 0:
            try:
                sources = json.loads(sj.read_text(encoding="utf-8"))
                if not isinstance(sources, list):
                    errors.append("source_list.json must be a JSON array.")
                else:
                    for i, entry in enumerate(sources):
                        missing = SOURCE_ENTRY_REQUIRED_KEYS - set(entry.keys())
                        if missing:
                            warnings.append(
                                f"source_list.json entry {i} missing keys: {sorted(missing)}"
                            )
                        st = entry.get("source_type", "")
                        if st not in VALID_SOURCE_TYPES:
                            warnings.append(
                                f"source_list.json entry {i} has unknown source_type: {st!r}"
                            )
            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                errors.append(f"source_list.json is not valid JSON: {e}")

        return {
            "valid":    len(errors) == 0,
            "errors":   errors,
            "warnings": warnings,
            "files":    files,
        }

    def write_manifest(self, folder_path: str) -> str:
        """
        Write manifest.json into a report package folder.

        The manifest is what the phone app reads first. It contains:
          - contract_version
          - package_created timestamp
          - question (from report.json)
          - pipeline_version (from report.json)
          - file inventory with SHA-256 checksums and sizes
          - validation result

        Parameters
        ----------
        folder_path : Path to the report package folder.

        Returns
        -------
        str — path to the written manifest.json file.

        Raises
        ------
        FileNotFoundError : folder_path does not exist.
        ValueError        : Package fails validation (errors present).
        """
        folder = Path(folder_path)
        if not folder.is_dir():
            raise FileNotFoundError(
                f"phone_contract.write_manifest: folder not found: {folder_path}"
            )

        validation = self.validate_package(folder_path)
        if not validation["valid"]:
            raise ValueError(
                f"phone_contract.write_manifest: package has errors — "
                f"{validation['errors']}"
            )

        # Read question and pipeline_version from report.json
        question = ""
        pipeline_version = ""
        timestamp = ""
        rj = folder / "report.json"
        if rj.is_file():
            try:
                data = json.loads(rj.read_text(encoding="utf-8"))
                question         = data.get("question", "")
                pipeline_version = data.get("pipeline_version", "")
                timestamp        = data.get("timestamp", "")
            except Exception:
                pass

        # File inventory with checksums
        inventory = {}
        for fname in REQUIRED_FILES:
            fpath = folder / fname
            if fpath.is_file():
                inventory[fname] = {
                    "sha256":     _sha256_file(str(fpath)),
                    "size_bytes": _file_size(str(fpath)),
                }

        manifest = {
            "contract_version":  CONTRACT_VERSION,
            "package_created":   _now_iso(),
            "question":          question,
            "pipeline_version":  pipeline_version,
            "report_timestamp":  timestamp,
            "files":             inventory,
            "validation": {
                "valid":    validation["valid"],
                "warnings": validation["warnings"],
            },
            "phone_can":    PHONE_CAN,
            "phone_cannot": PHONE_CANNOT,
        }

        manifest_path = folder / "manifest.json"
        manifest_path.write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
        return str(manifest_path)

    def read_manifest(self, folder_path: str) -> dict:
        """
        Read and return the manifest.json from a report package.

        Parameters
        ----------
        folder_path : Path to the report package folder.

        Returns
        -------
        dict — the manifest contents.

        Raises
        ------
        FileNotFoundError : manifest.json does not exist in folder.
        ValueError        : manifest.json is not valid JSON.
        """
        mp = Path(folder_path) / "manifest.json"
        if not mp.is_file():
            raise FileNotFoundError(
                f"phone_contract.read_manifest: manifest.json not found in {folder_path!r}"
            )
        try:
            return json.loads(mp.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            raise ValueError(
                f"phone_contract.read_manifest: manifest.json is not valid JSON: {e}"
            ) from e

    def package_summary(self, folder_path: str) -> dict:
        """
        Return a minimal display-ready summary of a report package.

        This is what a phone app list view would show for each saved report —
        just enough to identify and select a report without loading the full
        report.json.

        Reads from manifest.json if present; falls back to report.json.

        Returns
        -------
        dict with keys:
            folder        : str   — absolute folder path
            question      : str   — research question
            timestamp     : str   — when the report was generated
            corpus_hits   : int   — number of corpus results
            citation_hops : int   — length of the citation path
            gap_count     : int   — number of gaps logged
            source_count  : int   — number of sources used
            valid         : bool  — whether the package passed validation
        """
        folder = Path(folder_path)

        # Try manifest first (fast)
        mp = folder / "manifest.json"
        if mp.is_file():
            try:
                m = json.loads(mp.read_text(encoding="utf-8"))
                # Still need counts from the data files
                counts = self._count_from_files(folder)
                return {
                    "folder":        str(folder.resolve()),
                    "question":      m.get("question", ""),
                    "timestamp":     m.get("report_timestamp", ""),
                    "valid":         m.get("validation", {}).get("valid", False),
                    **counts,
                }
            except Exception:
                pass

        # Fallback: read report.json directly
        rj = folder / "report.json"
        if rj.is_file():
            try:
                data = json.loads(rj.read_text(encoding="utf-8"))
                counts = self._count_from_files(folder)
                return {
                    "folder":    str(folder.resolve()),
                    "question":  data.get("question", ""),
                    "timestamp": data.get("timestamp", ""),
                    "valid":     self.validate_package(folder_path)["valid"],
                    **counts,
                }
            except Exception:
                pass

        return {
            "folder":        str(folder.resolve()),
            "question":      "",
            "timestamp":     "",
            "valid":         False,
            "corpus_hits":   0,
            "citation_hops": 0,
            "gap_count":     0,
            "source_count":  0,
        }

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _count_from_files(self, folder: Path) -> dict:
        """Read counts from the JSON data files."""
        corpus_hits = citation_hops = gap_count = source_count = 0

        rj = folder / "report.json"
        if rj.is_file():
            try:
                data = json.loads(rj.read_text(encoding="utf-8"))
                corpus_hits   = len(data.get("corpus_hits",   []))
                citation_hops = len(data.get("citation_path", []))
            except Exception:
                pass

        gj = folder / "gap_log.json"
        if gj.is_file():
            try:
                gap_count = len(json.loads(gj.read_text(encoding="utf-8")))
            except Exception:
                pass

        sj = folder / "source_list.json"
        if sj.is_file():
            try:
                source_count = len(json.loads(sj.read_text(encoding="utf-8")))
            except Exception:
                pass

        return {
            "corpus_hits":   corpus_hits,
            "citation_hops": citation_hops,
            "gap_count":     gap_count,
            "source_count":  source_count,
        }

    def __repr__(self) -> str:
        return f"<PhoneContract contract_version={CONTRACT_VERSION!r}>"
