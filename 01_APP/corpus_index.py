"""
corpus_index.py — VERITAS Phase 1 (revised in Phase 3)

Owns corpus storage, per-document metadata, FTS5 indexing, search with
primary/secondary ranking, citation resolution, and full-corpus listing.

All reads and writes to corpus/index/corpus.db go through this module only.
No other VERITAS module touches the index files directly.

Public API
----------
    CorpusIndex(db_path=None)
    .ingest(path, source_type, date, title) -> doc_id (str)
    .search(query, limit, prefer_primary) -> list[dict]
    .resolve(citation_string) -> str | None
    .list_all() -> list[dict]
    .rebuild() -> None

Phase 3 change — resolve() semantics fix
-----------------------------------------
resolve() previously scanned each document's *outgoing* citations array to
find a target, which is the wrong direction: a document's citations[] lists
what it cites, not what it is.  The correct model:

  A corpus document is identified by its title and by its self_cite field
  (the canonical citation form of the document itself, if one can be
  extracted from its body at ingest time).

  resolve(citation_string) now checks:
    1. self_cite exact/substring match (primary means of identification)
    2. title substring match (fallback)

  The outgoing-citations scan has been removed.

A self_cite column has been added to the documents table and populated at
ingest time by extracting the first neutral-citation pattern ([YYYY] AB NNN)
or the first case-citation (Name v Name) that appears in the document body.
"""

import hashlib
import json
import os
import re
import sqlite3
from datetime import datetime
from pathlib import Path

_HERE = Path(__file__).parent
DEFAULT_DB_PATH = _HERE / "corpus" / "index" / "corpus.db"


# ---------------------------------------------------------------------------
# Text extraction
# ---------------------------------------------------------------------------

def _extract_text(path: str) -> str:
    p = Path(path)
    if p.suffix.lower() in (".txt", ".md", ".rst", ".html", ".htm", ".csv"):
        try:
            return p.read_text(encoding="utf-8", errors="replace")
        except OSError as e:
            return f"[read error: {e}]"
    try:
        raw = p.read_bytes()
        return raw.replace(b"\x00", b" ").decode("utf-8", errors="replace")
    except OSError as e:
        return f"[read error: {e}]"


# ---------------------------------------------------------------------------
# Citation extraction
# ---------------------------------------------------------------------------

_CASE_CITATION_RE = re.compile(
    r"\b[A-Z][A-Za-z\s''‑-]{0,40}\s+v\.?\s+[A-Z][A-Za-z\s''‑-]{1,40}"
    r"(?:\s*[\[\(]\d{4}[\]\)])?(?:\s+\d+\s+[A-Z]{2,6}\s+\d+)?",
    re.IGNORECASE,
)
_NEUTRAL_CITATION_RE = re.compile(r"\[\d{4}\]\s+[A-Z]{2,6}\s+\d+")
_STATUTE_RE = re.compile(
    r"\b[A-Z][A-Za-z\s]{2,40}"
    r"(?:Act|Statute|Code|Regulation|Ordinance|Constitution)\b"
)


def _extract_citations(text: str) -> list:
    """Return deduplicated outgoing citation strings found in text."""
    found: set[str] = set()
    for m in _CASE_CITATION_RE.finditer(text):
        s = m.group(0).strip()
        if len(s) > 5:
            found.add(s)
    for m in _NEUTRAL_CITATION_RE.finditer(text):
        found.add(m.group(0).strip())
    for m in _STATUTE_RE.finditer(text):
        s = m.group(0).strip()
        if len(s) > 6:
            found.add(s)
    return sorted(found)


def _extract_self_cite(text: str, title: str) -> str | None:
    """
    Extract the canonical self-identifying citation of a document.

    Strategy (in order of preference):
      1. First neutral citation pattern [YYYY] AB NNN in the body.
      2. First case-citation Name v Name [...] in the body.
      3. First statute pattern "Name Act/Statute/Code..." in the body
         that is also a substring of the title.
      4. None — no self-cite could be determined.

    This is intentionally conservative: it is better to leave self_cite
    as None (falling back to title matching in resolve()) than to
    misidentify the wrong citation as the document's own.
    """
    # 1. Neutral citation ([YYYY] AB NNN) — these are document-identifying
    m = _NEUTRAL_CITATION_RE.search(text)
    if m:
        return m.group(0).strip()

    # 2. Case citation
    m = _CASE_CITATION_RE.search(text)
    if m:
        cit = m.group(0).strip()
        if len(cit) > 5:
            return cit

    # 3. Statute name that appears in title (confirms it's self-identifying)
    title_lower = title.lower()
    for m in _STATUTE_RE.finditer(text):
        s = m.group(0).strip()
        if len(s) > 6 and s.lower() in title_lower:
            return s

    return None


# ---------------------------------------------------------------------------
# CorpusIndex
# ---------------------------------------------------------------------------

class CorpusIndex:
    """
    Manages the VERITAS local corpus index.

    Parameters
    ----------
    db_path : str | Path | None
        Path to the SQLite database file. Defaults to
        ``corpus/index/corpus.db`` relative to this module's directory.
        Parent directory is created automatically if absent.
    """

    def __init__(self, db_path=None):
        self._db_path = Path(db_path) if db_path else DEFAULT_DB_PATH
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(
            str(self._db_path), check_same_thread=False
        )
        self._conn.row_factory = sqlite3.Row
        self._init_schema()

    # ------------------------------------------------------------------
    # Schema
    # ------------------------------------------------------------------

    def _init_schema(self):
        c = self._conn
        c.execute("PRAGMA journal_mode=WAL")
        c.execute("PRAGMA foreign_keys=ON")

        c.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                doc_id      TEXT PRIMARY KEY,
                path        TEXT NOT NULL,
                title       TEXT NOT NULL,
                source_type TEXT NOT NULL
                            CHECK(source_type IN ('primary','secondary')),
                doc_date    TEXT,
                word_count  INTEGER,
                ingested_at TEXT NOT NULL,
                citations   TEXT,
                self_cite   TEXT
            )
        """)

        # Add self_cite column to existing DBs (idempotent)
        try:
            c.execute("ALTER TABLE documents ADD COLUMN self_cite TEXT")
        except sqlite3.OperationalError:
            pass  # column already exists

        try:
            c.execute("""
                CREATE VIRTUAL TABLE docs_fts USING fts5(
                    doc_id UNINDEXED,
                    title,
                    body,
                    tokenize='unicode61'
                )
            """)
        except sqlite3.OperationalError as e:
            if "already exists" not in str(e):
                raise

        c.commit()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def ingest(self, path: str, source_type: str, date: str = None,
               title: str = None) -> str:
        """
        Add a document to the corpus index.

        Parameters
        ----------
        path        : Path to the document file (must exist).
        source_type : ``'primary'`` or ``'secondary'``.
        date        : ISO-8601 date string (e.g. ``'2001-03-14'``), or None.
        title       : Display title. Defaults to the file stem if omitted.

        Returns
        -------
        doc_id : str  — SHA-256 hex digest of the file's raw bytes.

        Raises
        ------
        ValueError        : source_type not 'primary' or 'secondary'.
        FileNotFoundError : path does not exist.
        """
        path = str(path)
        if not os.path.isfile(path):
            raise FileNotFoundError(
                f"corpus_index.ingest: file not found: {path!r}"
            )
        if source_type not in ("primary", "secondary"):
            raise ValueError(
                f"corpus_index.ingest: source_type must be 'primary' or "
                f"'secondary', got {source_type!r}"
            )

        raw = Path(path).read_bytes()
        doc_id = hashlib.sha256(raw).hexdigest()

        if title is None:
            title = Path(path).stem

        text = _extract_text(path)
        word_count = len(text.split())
        citations = _extract_citations(text)
        self_cite = _extract_self_cite(text, title)
        ingested_at = datetime.utcnow().isoformat()

        c = self._conn
        c.execute("""
            INSERT INTO documents
                (doc_id, path, title, source_type, doc_date,
                 word_count, ingested_at, citations, self_cite)
            VALUES (?,?,?,?,?,?,?,?,?)
            ON CONFLICT(doc_id) DO UPDATE SET
                path        = excluded.path,
                title       = excluded.title,
                source_type = excluded.source_type,
                doc_date    = excluded.doc_date,
                word_count  = excluded.word_count,
                ingested_at = excluded.ingested_at,
                citations   = excluded.citations,
                self_cite   = excluded.self_cite
        """, (doc_id, path, title, source_type, date,
              word_count, ingested_at, json.dumps(citations), self_cite))

        c.execute("DELETE FROM docs_fts WHERE doc_id = ?", (doc_id,))
        c.execute(
            "INSERT INTO docs_fts(doc_id, title, body) VALUES (?,?,?)",
            (doc_id, title, text)
        )
        c.commit()
        return doc_id

    def search(self, query: str, limit: int = 20,
               prefer_primary: bool = True) -> list:
        """
        Full-text search the corpus.

        Parameters
        ----------
        query          : FTS5 query string.
        limit          : Maximum results (default 20).
        prefer_primary : If True (default), primary sources rank before
                         secondary within the same BM25 score band.

        Returns
        -------
        list of dict: doc_id, title, source_type, doc_date, path,
                      word_count, citations (list), snippet, rank.
        """
        if not query or not query.strip():
            return []

        order_clause = (
            "CASE d.source_type WHEN 'primary' THEN 0 ELSE 1 END, fts.rank"
            if prefer_primary
            else "fts.rank"
        )

        try:
            rows = self._conn.execute(f"""
                SELECT
                    d.doc_id,
                    d.title,
                    d.source_type,
                    d.doc_date,
                    d.path,
                    d.word_count,
                    d.citations,
                    snippet(fts.docs_fts, 2, '[', ']', '...', 24) AS snippet,
                    fts.rank AS rank
                FROM docs_fts fts
                JOIN documents d ON fts.doc_id = d.doc_id
                WHERE fts.docs_fts MATCH ?
                ORDER BY {order_clause}
                LIMIT ?
            """, (query, limit)).fetchall()
        except sqlite3.OperationalError:
            return []

        return [
            {
                "doc_id":      r["doc_id"],
                "title":       r["title"],
                "source_type": r["source_type"],
                "doc_date":    r["doc_date"],
                "path":        r["path"],
                "word_count":  r["word_count"],
                "citations":   json.loads(r["citations"] or "[]"),
                "snippet":     r["snippet"] or "",
                "rank":        r["rank"],
            }
            for r in rows
        ]

    def resolve(self, citation_string: str) -> "str | None":
        """
        Identify which corpus document IS the cited work.

        Checks (in order):
          1. self_cite exact match (case-insensitive).
          2. self_cite substring match — needle in self_cite or self_cite in needle.
          3. Title substring match.

        The outgoing-citations array is intentionally NOT scanned: a document's
        citations[] lists what it cites, not what it is.  Scanning citations[]
        for resolution was semantically wrong and has been removed.

        Parameters
        ----------
        citation_string : The citation text to resolve.

        Returns
        -------
        doc_id (str) of the first matching document, or None.
        """
        if not citation_string:
            return None

        needle = citation_string.strip().lower()
        c = self._conn

        # 1 & 2. self_cite match
        rows = c.execute(
            "SELECT doc_id, self_cite FROM documents WHERE self_cite IS NOT NULL"
        ).fetchall()
        for row in rows:
            sc = row["self_cite"].lower()
            if needle == sc:
                return row["doc_id"]
            if needle in sc or sc in needle:
                return row["doc_id"]

        # 3. Title substring match
        row = c.execute(
            "SELECT doc_id FROM documents WHERE LOWER(title) LIKE ?",
            (f"%{needle}%",)
        ).fetchone()
        if row:
            return row["doc_id"]

        return None

    def list_all(self) -> list:
        """
        Return metadata for every document in the corpus.

        Ordered: primary sources first, then secondary; within each group
        sorted by doc_date ascending (nulls last), then title.

        Returns
        -------
        list of dict: doc_id, title, source_type, doc_date, path,
                      word_count, ingested_at, citations (list), self_cite.
        """
        rows = self._conn.execute("""
            SELECT doc_id, title, source_type, doc_date, path,
                   word_count, ingested_at, citations, self_cite
            FROM documents
            ORDER BY
                CASE source_type WHEN 'primary' THEN 0 ELSE 1 END,
                COALESCE(doc_date, '9999') ASC,
                title ASC
        """).fetchall()

        return [
            {
                "doc_id":      r["doc_id"],
                "title":       r["title"],
                "source_type": r["source_type"],
                "doc_date":    r["doc_date"],
                "path":        r["path"],
                "word_count":  r["word_count"],
                "ingested_at": r["ingested_at"],
                "citations":   json.loads(r["citations"] or "[]"),
                "self_cite":   r["self_cite"],
            }
            for r in rows
        ]

    def rebuild(self) -> None:
        """
        Re-index all documents tracked in the documents table.

        Clears and repopulates the FTS5 index from stored file paths.
        Documents whose files no longer exist are removed and logged.
        """
        c = self._conn
        rows = c.execute(
            "SELECT doc_id, path, title FROM documents"
        ).fetchall()

        c.execute("DELETE FROM docs_fts")
        c.commit()

        stale = []
        reindexed = 0
        for r in rows:
            path = r["path"]
            if not os.path.isfile(path):
                stale.append(path)
                c.execute("DELETE FROM documents WHERE doc_id = ?", (r["doc_id"],))
                continue

            text = _extract_text(path)
            citations = _extract_citations(text)
            self_cite = _extract_self_cite(text, r["title"])

            c.execute(
                "UPDATE documents SET citations = ?, self_cite = ? WHERE doc_id = ?",
                (json.dumps(citations), self_cite, r["doc_id"])
            )
            c.execute(
                "INSERT INTO docs_fts(doc_id, title, body) VALUES (?,?,?)",
                (r["doc_id"], r["title"], text)
            )
            reindexed += 1

        c.commit()
        for p in stale:
            print(f"[corpus_index] rebuild: file not found, removed: {p}")
        print(
            f"[corpus_index] rebuild complete. "
            f"{reindexed} documents re-indexed, "
            f"{len(stale)} stale records removed."
        )

    # ------------------------------------------------------------------
    # Context manager / introspection
    # ------------------------------------------------------------------

    def close(self):
        self._conn.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    def __repr__(self):
        n = self._conn.execute(
            "SELECT COUNT(*) FROM documents"
        ).fetchone()[0]
        return f"<CorpusIndex db={self._db_path} documents={n}>"
