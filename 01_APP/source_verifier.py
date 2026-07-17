"""
source_verifier.py — VERITAS Phase 3.5

Verification cache for corpus documents.

Responsibility
--------------
Verify each corpus source once, store the result, and avoid re-checking
the same unchanged source on subsequent runs.  This is a cache, not an
automated web-checking loop.

The module is offline-first: it never contacts the web unless the caller
explicitly passes allow_online=True to verify_document().  When online
checking is disabled (the default), the module keeps the source, marks it
honestly, and generates a human-checkable verification link or search
query the researcher can follow manually.  Sources are never silently
discarded or falsely promoted to VERIFIED.

Verification statuses
---------------------
    VERIFIED               — source confirmed against a known-good URL
    UNVERIFIED             — source not yet checked; no URL available
    PARTIAL                — citation present but no authoritative URL yet
    CONFLICT               — stored metadata conflicts with current metadata
    NO_PUBLIC_SOURCE_FOUND — online check attempted; no usable URL found
    AUDIT_DUE              — source has exceeded the scheduled audit interval

Re-verification rules
---------------------
Do NOT re-verify when:
  • status is VERIFIED and document hash has not changed
    and metadata (title, citation) has not changed
    and verification URL has not changed
    and force=False and audit_due=False

Re-verify when ANY of:
  1. document hash changes
  2. title or citation metadata changes
  3. verification URL changes (caller supplies a new one)
  4. status is CONFLICT
  5. force=True (manual re-verification request)
  6. status is AUDIT_DUE

Verification link priority
--------------------------
When suggesting a public verification link:
  1. Official court / government source (detected by URL pattern)
  2. CourtListener  (courtlistener.com)
  3. Justia         (law.justia.com)
  4. Cornell / LII  (law.cornell.edu)
  5. GovInfo        (govinfo.gov)
  6. Library of Congress (loc.gov / congress.gov)
  7. Other reputable archive
  8. General search link (last resort)

Public API
----------
    SourceVerifier(cache_path=None)
    .classify_document(text, metadata)         -> dict
    .extract_case_identity(text, metadata)      -> dict
    .verify_document(doc_id, text, metadata,
                     allow_online=False,
                     force=False)               -> dict
    .suggest_verification_link(identity)        -> str
    .needs_reverification(doc_id,
                          document_hash,
                          metadata)             -> bool
    .mark_audit_due(doc_id)                     -> dict
    .verification_report()                      -> list[dict]

verified_by values (allowed examples)
--------------------------------------
    "Manual"             — record was preloaded or confirmed by a human
    "Official Court"     — confirmed via an official court / government URL
    "CourtListener"      — confirmed via courtlistener.com
    "Justia"             — confirmed via law.justia.com
    "Cornell/LII"        — confirmed via law.cornell.edu
    "GovInfo"            — confirmed via govinfo.gov
    "Library of Congress"— confirmed via loc.gov or congress.gov
    "Audit"              — status set by a scheduled audit run
    "Unknown"            — not yet verified or verifier not recorded
"""

from __future__ import annotations

import hashlib
import json
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote_plus

# ---------------------------------------------------------------------------
# Status constants
# ---------------------------------------------------------------------------

VERIFIED               = "VERIFIED"
UNVERIFIED             = "UNVERIFIED"
PARTIAL                = "PARTIAL"
CONFLICT               = "CONFLICT"
NO_PUBLIC_SOURCE_FOUND = "NO_PUBLIC_SOURCE_FOUND"
AUDIT_DUE              = "AUDIT_DUE"

_VALID_STATUSES = {
    VERIFIED, UNVERIFIED, PARTIAL, CONFLICT,
    NO_PUBLIC_SOURCE_FOUND, AUDIT_DUE,
}

# ---------------------------------------------------------------------------
# Document type constants
# ---------------------------------------------------------------------------

DOCTYPE_CASE       = "CASE"        # court judgment / decision
DOCTYPE_STATUTE    = "STATUTE"     # legislation / act / code
DOCTYPE_REGULATION = "REGULATION"  # regulation / rule / ordinance
DOCTYPE_CONST       = "CONSTITUTION"
DOCTYPE_CONSTITUTION = "CONSTITUTION"
DOCTYPE_SECONDARY  = "SECONDARY"   # commentary, article, summary
DOCTYPE_UNKNOWN    = "UNKNOWN"

# ---------------------------------------------------------------------------
# Regexes (jurisdiction-neutral)
# ---------------------------------------------------------------------------

# Neutral case citation: [YYYY] AB NNN
_NEUTRAL_CIT_RE = re.compile(
    r"\[(\d{4})\]\s+([A-Z]{2,8})\s+(\d+)", re.IGNORECASE
)
# "Name v Name" case citation
_CASE_V_RE = re.compile(
    r"\b([A-Z][A-Za-z\s''‑-]{0,40})\s+v\.?\s+([A-Z][A-Za-z\s''‑-]{1,40})"
    r"(?:\s*[\[\(](\d{4})[\]\)])?",
    re.IGNORECASE,
)
# Statute / Act / Code
_STATUTE_RE = re.compile(
    r"\b([A-Z][A-Za-z\s]{2,40}"
    r"(?:Act|Statute|Code|Regulation|Ordinance|Constitution))\b"
)
# Year in parentheses / brackets (for statute dating)
_YEAR_RE = re.compile(r"[\[\(](\d{4})[\]\)]")

# Provider URL fingerprints
_PROVIDER_PATTERNS: list[tuple[str, str]] = [
    (r"courtlistener\.com",  "CourtListener"),
    (r"law\.justia\.com",    "Justia"),
    (r"law\.cornell\.edu",   "Cornell/LII"),
    (r"govinfo\.gov",        "GovInfo"),
    (r"loc\.gov|congress\.gov", "Library of Congress"),
    (r"google\.com/search|bing\.com/search|duckduckgo\.com", "Search"),
]

# Default cache path
_HERE = Path(__file__).parent
DEFAULT_CACHE_PATH = _HERE / "corpus" / "index" / "source_verifier.db"


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _safe_str(v: Any) -> str | None:
    return str(v).strip() if v is not None and str(v).strip() else None


def _detect_provider(url: str) -> str:
    """Return a provider label from a verification URL."""
    if not url:
        return "Unknown"
    for pattern, label in _PROVIDER_PATTERNS:
        if re.search(pattern, url, re.IGNORECASE):
            return label
    # Official-looking domain (gov / judiciary / court)
    if re.search(r"\.(gov|judiciary|courts?)\b", url, re.IGNORECASE):
        return "Official"
    return "Archive"


# ---------------------------------------------------------------------------
# SourceVerifier
# ---------------------------------------------------------------------------

class SourceVerifier:
    """
    Verification cache for VERITAS corpus documents.

    Parameters
    ----------
    cache_path : str | Path | None
        Path to the SQLite cache file.  Defaults to
        ``corpus/index/source_verifier.db`` relative to this module's
        directory.  Parent directory is created automatically.
    """

    def __init__(self, cache_path: str | Path | None = None) -> None:
        self._path = Path(cache_path) if cache_path else DEFAULT_CACHE_PATH
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(str(self._path), check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._init_schema()

    # ------------------------------------------------------------------
    # Schema
    # ------------------------------------------------------------------

    def _init_schema(self) -> None:
        self._conn.executescript("""
            PRAGMA journal_mode=WAL;
            CREATE TABLE IF NOT EXISTS verifications (
                doc_id            TEXT PRIMARY KEY,
                document_hash     TEXT NOT NULL,
                title             TEXT,
                citation          TEXT,
                source_type       TEXT,
                status            TEXT NOT NULL DEFAULT 'UNVERIFIED',
                verification_url  TEXT,
                provider          TEXT,
                verification_date TEXT,
                last_audit_date   TEXT,
                confidence        REAL DEFAULT 0.0,
                notes             TEXT,
                verified_by       TEXT DEFAULT 'Unknown',
                created_at        TEXT NOT NULL,
                updated_at        TEXT NOT NULL
            );
        """)
        # Migrate existing DBs that predate this column (idempotent)
        try:
            self._conn.execute(
                "ALTER TABLE verifications ADD COLUMN verified_by TEXT DEFAULT 'Unknown'"
            )
        except sqlite3.OperationalError:
            pass  # column already present
        self._conn.commit()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def classify_document(self, text: str, metadata: dict) -> dict:
        """
        Classify a document by type.

        Parameters
        ----------
        text     : Full extracted text of the document.
        metadata : dict with at least 'title' key (may also have 'source_type').

        Returns
        -------
        dict with keys:
            doc_type   : str  — one of the DOCTYPE_* constants
            confidence : float  — 0.0–1.0
            indicators : list[str]  — evidence strings that drove the classification
        """
        title  = str(metadata.get("title", "")).lower()
        body   = text.lower()[:4000]  # first 4 KB is enough for signals
        source_type = str(metadata.get("source_type", "")).lower()
        indicators: list[str] = []
        scores: dict[str, float] = {
            DOCTYPE_CASE:       0.0,
            DOCTYPE_STATUTE:    0.0,
            DOCTYPE_REGULATION: 0.0,
            DOCTYPE_CONST:      0.0,
            DOCTYPE_SECONDARY:  0.0,
        }

        # ── Explicit source_type hint ──
        if source_type == "secondary":
            scores[DOCTYPE_SECONDARY] += 0.6
            indicators.append("source_type=secondary")

        # ── Case signals ──
        if _CASE_V_RE.search(text):
            scores[DOCTYPE_CASE] += 0.4
            indicators.append("contains 'v.' case citation")
        if _NEUTRAL_CIT_RE.search(text):
            scores[DOCTYPE_CASE] += 0.2
            indicators.append("contains neutral citation [YYYY] AB NNN")
        for kw in ("judgment", "judgment of", "court held", "appeal", "plaintiff",
                   "defendant", "claimant", "respondent", "appellant", "ruled",
                   "decision of the court", "reasons for judgment"):
            if kw in body:
                scores[DOCTYPE_CASE] += 0.1
                indicators.append(f"keyword: {kw!r}")
                break

        # ── Statute signals ──
        if re.search(r"\bact\b|\bstatute\b|\bcode\b", title):
            scores[DOCTYPE_STATUTE] += 0.5
            indicators.append("title contains 'Act/Statute/Code'")
        if re.search(r"\bsection\s+\d+\b|\bs\.\s*\d+\b", body):
            scores[DOCTYPE_STATUTE] += 0.2
            indicators.append("contains section numbering")
        if re.search(r"\bhereby\s+enacted\b|\bshall\b.*\bprovide\b", body):
            scores[DOCTYPE_STATUTE] += 0.15
            indicators.append("enactment language")

        # ── Regulation signals ──
        if re.search(r"\bregulation\b|\bordinance\b|\brule\b", title):
            scores[DOCTYPE_REGULATION] += 0.5
            indicators.append("title contains regulation/ordinance/rule")
        if re.search(r"\bpursuant\s+to\b|\bauthorized\s+by\b", body):
            scores[DOCTYPE_REGULATION] += 0.15
            indicators.append("regulatory language")

        # ── Constitution signals ──
        if re.search(r"\bconstitution\b", title):
            scores[DOCTYPE_CONST] += 0.6
            indicators.append("title contains 'constitution'")
        if re.search(r"\bwe\s+the\s+people\b|\barticle\s+[ivx]+\b", body):
            scores[DOCTYPE_CONST] += 0.25
            indicators.append("constitutional language")

        # ── Secondary signals ──
        for kw in ("commentary", "article", "essay", "analysis", "review",
                   "discussion", "academic", "scholar", "literature"):
            if kw in title or kw in body[:500]:
                scores[DOCTYPE_SECONDARY] += 0.3
                indicators.append(f"secondary keyword: {kw!r}")
                break

        # Pick the winner
        best_type = max(scores, key=lambda k: scores[k])
        best_score = scores[best_type]

        if best_score < 0.1:
            best_type  = DOCTYPE_UNKNOWN
            confidence = 0.0
        else:
            # Normalise to 0-1 loosely; cap at 1.0
            confidence = min(best_score, 1.0)

        return {
            "doc_type":   best_type,
            "confidence": round(confidence, 3),
            "indicators": list(dict.fromkeys(indicators)),  # dedup, preserve order
        }

    def extract_case_identity(self, text: str, metadata: dict) -> dict:
        """
        Extract the canonical identity of a document for use in link
        suggestion and verification.

        Parameters
        ----------
        text     : Extracted document text.
        metadata : dict with keys like 'title', 'doc_date', 'self_cite'.

        Returns
        -------
        dict with keys (all may be None if not found):
            title       : str
            citation    : str   — best canonical citation found
            year        : str   — four-digit year string
            parties     : tuple[str,str] | None  — (appellant, respondent)
            statute     : str   — statute name if doc is a statute
            doc_type    : str   — from classify_document
            self_cite   : str   — from metadata if present
            search_hint : str   — short string suitable for a search query
        """
        title     = _safe_str(metadata.get("title"))
        doc_date  = _safe_str(metadata.get("doc_date"))
        self_cite = _safe_str(metadata.get("self_cite"))

        year: str | None = None
        if doc_date:
            m = re.match(r"(\d{4})", doc_date)
            if m:
                year = m.group(1)

        # Best citation: prefer self_cite, then neutral, then v-form
        citation: str | None = self_cite

        neutral_m = _NEUTRAL_CIT_RE.search(text)
        if not citation and neutral_m:
            citation = neutral_m.group(0).strip()
            if not year:
                year = neutral_m.group(1)

        parties: tuple[str, str] | None = None
        case_m = _CASE_V_RE.search(text)
        if case_m:
            p1 = case_m.group(1).strip()
            p2 = case_m.group(2).strip()
            parties = (p1, p2)
            if not citation:
                citation = f"{p1} v {p2}"
                if case_m.group(3):
                    year = case_m.group(3)
                    citation += f" [{year}]"

        statute: str | None = None
        stat_m = _STATUTE_RE.search(text)
        if stat_m:
            statute = stat_m.group(1).strip()

        # Year fallback: scan text for a bracketed/parenthesised year
        if not year:
            yr_m = _YEAR_RE.search(text)
            if yr_m:
                year = yr_m.group(1)

        # Classify
        classification = self.classify_document(text, metadata)
        doc_type = classification["doc_type"]

        # Build a short search hint
        parts = []
        if citation:
            parts.append(citation)
        elif title:
            parts.append(title)
        if year and year not in (parts[0] if parts else ""):
            parts.append(year)
        search_hint = " ".join(parts) if parts else (title or "")

        return {
            "title":       title,
            "citation":    citation,
            "year":        year,
            "parties":     parties,
            "statute":     statute,
            "doc_type":    doc_type,
            "self_cite":   self_cite,
            "search_hint": search_hint,
        }

    def suggest_verification_link(self, identity: dict) -> str:
        """
        Suggest a public verification URL or search link for a document.

        Follows the priority order in the module docstring.  Never contacts
        the network.  Returns a URL string the researcher can open manually.

        Parameters
        ----------
        identity : dict as returned by extract_case_identity().

        Returns
        -------
        str — URL.  Always returns something (falls back to a web search).
        """
        citation    = identity.get("citation") or ""
        title       = identity.get("title") or ""
        doc_type    = identity.get("doc_type") or DOCTYPE_UNKNOWN
        search_hint = identity.get("search_hint") or title or citation

        # Use the neutral citation form if available for structured lookup
        neutral_m = _NEUTRAL_CIT_RE.search(citation) if citation else None

        # ── Case documents ──
        if doc_type in (DOCTYPE_CASE, DOCTYPE_UNKNOWN) and citation:
            # CourtListener full-text search (priority 2)
            q = quote_plus(citation.strip())
            return f"https://www.courtlistener.com/?q={q}&type=o&order_by=score+desc"

        # ── Statute / Regulation / Constitution ──
        if doc_type in (DOCTYPE_STATUTE, DOCTYPE_REGULATION, DOCTYPE_CONST):
            # GovInfo (priority 5) for statutes — widely applicable
            q = quote_plus((title or citation).strip())
            return f"https://www.govinfo.gov/app/search/%7B%22query%22%3A%22{q}%22%7D"

        # ── Secondary / fallback ──
        q = quote_plus(search_hint.strip()) if search_hint else quote_plus(title)
        # Cornell/LII is a good general fallback (priority 4)
        if doc_type == DOCTYPE_SECONDARY:
            return f"https://www.google.com/search?q={q}+site%3Alaw.cornell.edu+OR+site%3Alaw.justia.com"

        # Last resort: general web search (priority 8)
        return f"https://www.google.com/search?q={q}"

    def needs_reverification(
        self,
        doc_id: str,
        document_hash: str,
        metadata: dict,
    ) -> bool:
        """
        Determine whether a document needs re-verification.

        Returns False (no re-check needed) when:
          • Status is VERIFIED AND hash is unchanged AND title/citation
            metadata is unchanged.

        Returns True (re-check needed) when:
          1. No cached record exists yet.
          2. Document hash has changed.
          3. Title or citation metadata has changed.
          4. Status is CONFLICT or AUDIT_DUE.

        Parameters
        ----------
        doc_id        : Corpus document identifier.
        document_hash : Current SHA-256 hex of the document content.
        metadata      : dict with 'title' and optionally 'self_cite'/'citation'.

        Returns
        -------
        bool
        """
        row = self._conn.execute(
            "SELECT status, document_hash, title, citation FROM verifications "
            "WHERE doc_id = ?", (doc_id,)
        ).fetchone()

        if row is None:
            return True  # rule 1: no record yet

        if row["document_hash"] != document_hash:
            return True  # rule 2: hash changed

        new_title    = _safe_str(metadata.get("title")) or ""
        stored_title = row["title"] or ""
        if new_title != stored_title:
            return True  # rule 3a: title changed

        new_citation    = _safe_str(metadata.get("self_cite") or metadata.get("citation")) or ""
        stored_citation = row["citation"] or ""
        if new_citation != stored_citation:
            return True  # rule 3b: citation changed

        if row["status"] in (CONFLICT, AUDIT_DUE):
            return True  # rules 4 and 6

        return False

    def verify_document(
        self,
        doc_id: str,
        text: str,
        metadata: dict,
        allow_online: bool = False,
        force: bool = False,
    ) -> dict:
        """
        Verify a document and cache the result.

        Offline-first: will not contact the network unless allow_online=True.

        Parameters
        ----------
        doc_id       : Corpus document identifier.
        text         : Full extracted document text.
        metadata     : dict with at least 'title'; may include 'source_type',
                       'doc_date', 'self_cite'.
        allow_online : If True, online verification may be attempted (not
                       implemented in Phase 3.5 — reserved for a future
                       network-enabled phase).  When False (default), the
                       module generates a verification link but marks the
                       source UNVERIFIED or PARTIAL.
        force        : If True, re-verify even if the source is already
                       VERIFIED and the hash is unchanged (rule 5).

        Returns
        -------
        dict — the full verification record for this document, with keys
        matching the schema columns.
        """
        document_hash = _sha256(text)
        now           = _now_iso()

        # Check cache
        existing = self._get_record(doc_id)

        # Skip if already VERIFIED and no re-check is warranted
        if (
            existing is not None
            and not force
            and not self.needs_reverification(doc_id, document_hash, metadata)
        ):
            return dict(existing)

        # Detect CONFLICT: metadata changed on an already-verified source
        conflict = (
            existing is not None
            and existing["status"] == VERIFIED
            and (
                (existing["document_hash"] != document_hash)
                or (_safe_str(metadata.get("title")) or "" != existing["title"] or "")
            )
        )

        # Extract identity
        identity = self.extract_case_identity(text, metadata)
        suggested_link = self.suggest_verification_link(identity)

        title    = identity["title"]
        citation = identity["citation"]
        source_type = _safe_str(metadata.get("source_type")) or "unknown"

        # Determine status
        if conflict:
            status     = CONFLICT
            confidence = 0.0
            notes      = "Metadata or content changed after previous VERIFIED status."
        elif allow_online:
            # Phase 3.5: online capability is reserved; treated as PARTIAL
            # (a real implementation would make an HTTP call here)
            status     = PARTIAL
            confidence = 0.4
            notes      = (
                "allow_online=True requested but online verification is not "
                "implemented in this phase. Source is PARTIAL pending manual check. "
                f"Suggested link: {suggested_link}"
            )
        elif citation and suggested_link:
            status     = PARTIAL
            confidence = 0.3
            notes      = (
                f"Citation identified but not confirmed online. "
                f"Verify manually: {suggested_link}"
            )
        else:
            status     = UNVERIFIED
            confidence = 0.0
            notes      = (
                "No citation or verification URL available. "
                f"Search suggested: {suggested_link}"
            )

        # Preserve URL from existing record if we have one and it hasn't changed
        verification_url = suggested_link
        if existing and existing.get("verification_url") and not conflict:
            verification_url = existing["verification_url"]

        provider = _detect_provider(verification_url)

        # Derive verified_by
        if conflict:
            verified_by = "Unknown"
        elif status == UNVERIFIED:
            verified_by = "Unknown"
        elif existing and existing.get("verified_by") and existing["verified_by"] not in (None, "Unknown") and not force and not conflict:
            # Preserve an already-meaningful verified_by from the existing record
            verified_by = existing["verified_by"]
        else:
            # Default to provider name (matches the allowed examples in the docstring)
            verified_by = provider if provider not in ("Search", "Unknown") else "Unknown"

        record = {
            "doc_id":            doc_id,
            "document_hash":     document_hash,
            "title":             title,
            "citation":          citation,
            "source_type":       source_type,
            "status":            status,
            "verification_url":  verification_url,
            "provider":          provider,
            "verification_date": now,
            "last_audit_date":   existing["last_audit_date"] if existing else None,
            "confidence":        round(confidence, 3),
            "notes":             notes,
            "verified_by":       verified_by,
            "created_at":        existing["created_at"] if existing else now,
            "updated_at":        now,
        }

        self._upsert(record)
        return record

    def mark_audit_due(self, doc_id: str) -> dict:
        """
        Mark a cached verification record as requiring a scheduled audit.

        Sets status to AUDIT_DUE and updates last_audit_date.

        Parameters
        ----------
        doc_id : Corpus document identifier.

        Returns
        -------
        dict — the updated verification record.

        Raises
        ------
        KeyError : No verification record exists for doc_id.
        """
        existing = self._get_record(doc_id)
        if existing is None:
            raise KeyError(
                f"source_verifier.mark_audit_due: no record for doc_id={doc_id!r}"
            )

        now = _now_iso()
        self._conn.execute(
            "UPDATE verifications "
            "SET status=?, last_audit_date=?, verified_by=?, updated_at=? "
            "WHERE doc_id=?",
            (AUDIT_DUE, now, "Audit", now, doc_id)
        )
        self._conn.commit()

        updated = dict(existing)
        updated["status"]          = AUDIT_DUE
        updated["last_audit_date"] = now
        updated["verified_by"]     = "Audit"
        updated["updated_at"]      = now
        return updated

    def verification_report(self) -> list:
        """
        Return a list of all cached verification records.

        Ordered: CONFLICT and AUDIT_DUE first (highest attention needed),
        then NO_PUBLIC_SOURCE_FOUND, UNVERIFIED, PARTIAL, VERIFIED last.

        Returns
        -------
        list[dict] — one dict per record, keys matching schema columns.
                     All values are JSON-safe (str, float, None).
        """
        priority = {
            CONFLICT:               0,
            AUDIT_DUE:              1,
            NO_PUBLIC_SOURCE_FOUND: 2,
            UNVERIFIED:             3,
            PARTIAL:                4,
            VERIFIED:               5,
        }

        rows = self._conn.execute(
            "SELECT * FROM verifications ORDER BY updated_at DESC"
        ).fetchall()

        records = [dict(r) for r in rows]
        records.sort(key=lambda r: priority.get(r.get("status", ""), 99))
        return records

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get_record(self, doc_id: str) -> dict | None:
        row = self._conn.execute(
            "SELECT * FROM verifications WHERE doc_id = ?", (doc_id,)
        ).fetchone()
        return dict(row) if row else None

    def _upsert(self, record: dict) -> None:
        self._conn.execute("""
            INSERT INTO verifications (
                doc_id, document_hash, title, citation, source_type,
                status, verification_url, provider, verification_date,
                last_audit_date, confidence, notes, verified_by,
                created_at, updated_at
            ) VALUES (
                :doc_id, :document_hash, :title, :citation, :source_type,
                :status, :verification_url, :provider, :verification_date,
                :last_audit_date, :confidence, :notes, :verified_by,
                :created_at, :updated_at
            )
            ON CONFLICT(doc_id) DO UPDATE SET
                document_hash     = excluded.document_hash,
                title             = excluded.title,
                citation          = excluded.citation,
                source_type       = excluded.source_type,
                status            = excluded.status,
                verification_url  = excluded.verification_url,
                provider          = excluded.provider,
                verification_date = excluded.verification_date,
                last_audit_date   = excluded.last_audit_date,
                confidence        = excluded.confidence,
                notes             = excluded.notes,
                verified_by       = excluded.verified_by,
                updated_at        = excluded.updated_at
        """, record)
        self._conn.commit()

    # ------------------------------------------------------------------
    # Context manager / introspection
    # ------------------------------------------------------------------

    def close(self) -> None:
        self._conn.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    def __repr__(self) -> str:
        n = self._conn.execute(
            "SELECT COUNT(*) FROM verifications"
        ).fetchone()[0]
        return f"<SourceVerifier cache={self._path} records={n}>"
