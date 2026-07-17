"""
gap_log.py — VERITAS Phase 2

Owns recording of every item the research pipeline could not resolve:
unresolved citations, undefined terms, and empty searches. Each entry
carries the best available source link so the researcher can close the
gap manually.

Kept as its own module (not folded into corpus_index.py or
citation_graph.py) because gaps can originate from either module, as
well as from the definition and search stages.

Public API
----------
    GapLog()
    .add(gap_type, value, source_doc_id=None, best_link=None) -> str
    .all() -> list[dict]
    .by_type(gap_type) -> list[dict]
    .clear() -> None
    .to_json() -> str
    .from_json(json_str) -> None   [classmethod: GapLog.from_json(s)]
    .save(path) -> None
    .load(path) -> None            [classmethod: GapLog.load(path)]

Gap types (use the module-level constants)
------------------------------------------
    UNRESOLVED_CITATION  — a citation string that could not be resolved
                           to any corpus document.
    UNDEFINED_TERM       — a term used in a source but not defined
                           anywhere in the citation chain or dictionaries.
    EMPTY_SEARCH         — a corpus search that returned zero results.

Entry schema (each dict returned by all() / by_type())
-------------------------------------------------------
    gap_id       : str   — unique ID for this entry (UUID4)
    gap_type     : str   — one of the three constants above
    value        : str   — the citation / term / query that failed
    source_doc_id: str | None  — corpus doc_id where the gap was found
    best_link    : str | None  — URL or file path for manual follow-up
    timestamp    : str   — ISO-8601 UTC timestamp of when gap was logged
"""

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Gap type constants
# ---------------------------------------------------------------------------

UNRESOLVED_CITATION = "UNRESOLVED_CITATION"
UNDEFINED_TERM      = "UNDEFINED_TERM"
EMPTY_SEARCH        = "EMPTY_SEARCH"

_VALID_TYPES = {UNRESOLVED_CITATION, UNDEFINED_TERM, EMPTY_SEARCH}

# ---------------------------------------------------------------------------
# GapLog
# ---------------------------------------------------------------------------

class GapLog:
    """
    In-memory log of research gaps, with JSON serialisation.

    Thread-safety: not thread-safe. All pipeline stages run sequentially
    on desktop, so a single shared instance is sufficient.
    """

    def __init__(self):
        self._entries: list[dict] = []

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def add(
        self,
        gap_type: str,
        value: str,
        source_doc_id: str = None,
        best_link: str = None,
    ) -> str:
        """
        Record a new gap.

        Parameters
        ----------
        gap_type      : One of UNRESOLVED_CITATION, UNDEFINED_TERM,
                        EMPTY_SEARCH.
        value         : The citation string, term, or query that failed.
        source_doc_id : corpus_index doc_id of the document where this
                        gap was encountered, if known.
        best_link     : Best available URL or file path the researcher
                        can use to close the gap manually.

        Returns
        -------
        gap_id : str — the UUID4 assigned to this entry.

        Raises
        ------
        ValueError : gap_type is not one of the three valid constants.
        ValueError : value is empty or None.
        """
        if gap_type not in _VALID_TYPES:
            raise ValueError(
                f"gap_log.add: gap_type must be one of "
                f"{sorted(_VALID_TYPES)}, got {gap_type!r}"
            )
        if not value or not str(value).strip():
            raise ValueError(
                "gap_log.add: value must be a non-empty string"
            )

        entry = {
            "gap_id":        str(uuid.uuid4()),
            "gap_type":      gap_type,
            "value":         str(value).strip(),
            "source_doc_id": source_doc_id if source_doc_id else None,
            "best_link":     best_link if best_link else None,
            "timestamp":     datetime.now(timezone.utc).isoformat(),
        }
        self._entries.append(entry)
        return entry["gap_id"]

    def all(self) -> list:
        """
        Return all gap entries in insertion order.

        Returns
        -------
        list of dict — shallow copies; mutating the dicts does not affect
        the internal log.
        """
        return [dict(e) for e in self._entries]

    def by_type(self, gap_type: str) -> list:
        """
        Return all entries of a specific gap type.

        Parameters
        ----------
        gap_type : One of UNRESOLVED_CITATION, UNDEFINED_TERM, EMPTY_SEARCH.

        Returns
        -------
        list of dict — shallow copies, in insertion order.

        Raises
        ------
        ValueError : gap_type is not one of the three valid constants.
        """
        if gap_type not in _VALID_TYPES:
            raise ValueError(
                f"gap_log.by_type: gap_type must be one of "
                f"{sorted(_VALID_TYPES)}, got {gap_type!r}"
            )
        return [dict(e) for e in self._entries if e["gap_type"] == gap_type]

    def clear(self) -> None:
        """
        Remove all entries from the log.

        Does not affect any persisted JSON file; call save() afterwards
        if the cleared state should be written to disk.
        """
        self._entries.clear()

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def to_json(self, indent: int = 2) -> str:
        """
        Serialise the log to a JSON string.

        Returns
        -------
        str — UTF-8 JSON, pretty-printed at the given indent level.
        """
        return json.dumps(self._entries, indent=indent, ensure_ascii=False)

    @classmethod
    def from_json(cls, json_str: str) -> "GapLog":
        """
        Deserialise a GapLog from a JSON string produced by to_json().

        Parameters
        ----------
        json_str : str — JSON string (list of entry dicts).

        Returns
        -------
        GapLog instance populated with the deserialised entries.

        Raises
        ------
        ValueError : json_str is not valid JSON or not a JSON array.
        """
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"gap_log.from_json: invalid JSON — {e}") from e

        if not isinstance(data, list):
            raise ValueError(
                f"gap_log.from_json: expected a JSON array, "
                f"got {type(data).__name__}"
            )

        instance = cls()
        required = {"gap_id", "gap_type", "value", "timestamp"}
        for i, entry in enumerate(data):
            if not isinstance(entry, dict):
                raise ValueError(
                    f"gap_log.from_json: entry {i} is not a dict"
                )
            missing = required - entry.keys()
            if missing:
                raise ValueError(
                    f"gap_log.from_json: entry {i} missing keys: {missing}"
                )
            if entry["gap_type"] not in _VALID_TYPES:
                raise ValueError(
                    f"gap_log.from_json: entry {i} has invalid "
                    f"gap_type {entry['gap_type']!r}"
                )
            # Normalise optional fields
            normalised = {
                "gap_id":        str(entry["gap_id"]),
                "gap_type":      entry["gap_type"],
                "value":         str(entry["value"]),
                "source_doc_id": entry.get("source_doc_id") or None,
                "best_link":     entry.get("best_link") or None,
                "timestamp":     str(entry["timestamp"]),
            }
            instance._entries.append(normalised)

        return instance

    def save(self, path: str) -> None:
        """
        Write the log to a JSON file at path.

        Creates parent directories automatically. Overwrites any existing
        file at path.

        Parameters
        ----------
        path : str or Path — destination file path.
        """
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(self.to_json(), encoding="utf-8")

    @classmethod
    def load(cls, path: str) -> "GapLog":
        """
        Load a GapLog from a JSON file previously written by save().

        Parameters
        ----------
        path : str or Path — source file path.

        Returns
        -------
        GapLog instance.

        Raises
        ------
        FileNotFoundError : path does not exist.
        ValueError        : file content is not valid GapLog JSON.
        """
        p = Path(path)
        if not p.is_file():
            raise FileNotFoundError(
                f"gap_log.load: file not found: {p!r}"
            )
        return cls.from_json(p.read_text(encoding="utf-8"))

    # ------------------------------------------------------------------
    # Convenience / introspection
    # ------------------------------------------------------------------

    def __len__(self) -> int:
        return len(self._entries)

    def __bool__(self) -> bool:
        return bool(self._entries)

    def __repr__(self) -> str:
        counts = {t: 0 for t in _VALID_TYPES}
        for e in self._entries:
            counts[e["gap_type"]] += 1
        return (
            f"<GapLog entries={len(self._entries)} "
            f"citations={counts[UNRESOLVED_CITATION]} "
            f"terms={counts[UNDEFINED_TERM]} "
            f"searches={counts[EMPTY_SEARCH]}>"
        )
