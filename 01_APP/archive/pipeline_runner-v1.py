"""
pipeline_runner.py — VERITAS Phase 4

Owns the 12-step research pipeline. Called by main.py when the user
triggers "Run Research". Returns a structured research map dict that
main.py displays in the Research Map tab and optionally saves to disk.

No UI code lives here. No web access. No jurisdiction-specific logic.

Public API
----------
    PipelineRunner(config=None)
    .run(question, doc_text=None, doc_metadata=None) -> dict
    .save_report(result, reports_dir)               -> str  (folder path)
    .status_callback                                 # callable, set by caller

Pipeline steps (strict order)
------------------------------
    1.  Capture       — accept question + optional document text
    2.  Restate       — plain-English restatement via ai_integration
    3.  Identify terms — extract key legal terms via document_processor
    4.  Define        — plain-English + doctrinal definitions
    5.  Search corpus — FTS5 search via corpus_index
    6.  Rank          — primary before secondary (enforced by corpus_index)
    7.  Follow citations — recursive walk via citation_graph
    8.  Assemble doctrine/timeline — ordered output from citation_graph
    9.  Detect drift  — term usage vs baseline via consistency_engine
    10. Log gaps      — all unresolved items via gap_log
    11. Build research map — assemble all stage outputs into result dict
    12. Return        — caller saves to disk if desired
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable


# ---------------------------------------------------------------------------
# Lazy imports — these are in the same directory as this file
# ---------------------------------------------------------------------------

def _import_corpus_index():
    from corpus_index import CorpusIndex
    return CorpusIndex

def _import_gap_log():
    from gap_log import GapLog, UNRESOLVED_CITATION, UNDEFINED_TERM, EMPTY_SEARCH
    return GapLog, UNRESOLVED_CITATION, UNDEFINED_TERM, EMPTY_SEARCH

def _import_citation_graph():
    from citation_graph import CitationGraph
    return CitationGraph

def _import_source_verifier():
    from source_verifier import SourceVerifier
    return SourceVerifier


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def _safe_get(d: dict, *keys, default=None):
    for k in keys:
        if isinstance(d, dict):
            d = d.get(k, default)
        else:
            return default
    return d


# ---------------------------------------------------------------------------
# PipelineRunner
# ---------------------------------------------------------------------------

class PipelineRunner:
    """
    Executes the 12-step VERITAS research pipeline.

    Parameters
    ----------
    config : module or dict-like, optional
        Configuration object. If None, imports config.py from the same
        directory. Expected attributes:
            CORPUS_DB_PATH, VERIFIER_DB_PATH, REPORTS_DIR,
            CITATION_MAX_HOPS, RESEARCH_SEARCH_LIMIT
    """

    def __init__(self, config=None):
        if config is None:
            import config as _cfg
            config = _cfg
        self._config = config
        self._corpus_db    = getattr(config, "CORPUS_DB_PATH",    None)
        self._verifier_db  = getattr(config, "VERIFIER_DB_PATH",  None)
        self._reports_dir  = getattr(config, "REPORTS_DIR",       None)
        self._max_hops     = getattr(config, "CITATION_MAX_HOPS", 3)
        self._search_limit = getattr(config, "RESEARCH_SEARCH_LIMIT", 20)

        # Caller may set this to receive live status updates
        # Signature: status_callback(step: int, total: int, message: str)
        self.status_callback: Callable | None = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(
        self,
        question: str,
        doc_text: str = None,
        doc_metadata: dict = None,
    ) -> dict:
        """
        Execute the full 12-step research pipeline.

        Parameters
        ----------
        question      : The research question (typed by the user or derived
                        from a loaded document's title).
        doc_text      : Optional pre-loaded document text (from the Document
                        tab). If supplied, it is combined with the question
                        for term extraction and corpus search.
        doc_metadata  : Optional metadata dict from document_processor.

        Returns
        -------
        dict — the complete research map with keys:
            question, timestamp, pipeline_version,
            restatement, terms, definitions,
            corpus_hits, citation_path, drift_flags,
            gaps, source_list, errors
        """
        TOTAL_STEPS = 12
        errors: list[str] = []

        def _status(step: int, msg: str):
            if self.status_callback:
                try:
                    self.status_callback(step, TOTAL_STEPS, msg)
                except Exception:
                    pass

        # ── Step 1: Capture ───────────────────────────────────────────
        _status(1, "Step 1/12 — Capturing input…")
        question = (question or "").strip()
        doc_text = (doc_text or "").strip()
        combined_text = f"{question}\n\n{doc_text}".strip() if doc_text else question
        timestamp = _now_iso()

        # ── Step 2: Restate ───────────────────────────────────────────
        _status(2, "Step 2/12 — Restating question…")
        restatement = self._restate(question, doc_text, errors)

        # ── Step 3: Identify terms ────────────────────────────────────
        _status(3, "Step 3/12 — Identifying key terms…")
        terms = self._identify_terms(combined_text, errors)

        # ── Step 4: Define ────────────────────────────────────────────
        _status(4, "Step 4/12 — Looking up definitions…")
        definitions = self._define_terms(terms, errors)

        # ── Steps 5 & 6: Search corpus + rank ────────────────────────
        _status(5, "Step 5/12 — Searching corpus…")
        corpus_hits, gap_log = self._search_corpus(
            question, terms, definitions, errors
        )

        # ── Steps 7 & 8: Follow citations + assemble doctrine path ────
        _status(7, "Step 7/12 — Following citations…")
        citation_path, graph = self._follow_citations(
            corpus_hits, gap_log, errors
        )

        # ── Step 9: Detect drift ──────────────────────────────────────
        _status(9, "Step 9/12 — Detecting semantic drift…")
        drift_flags = self._detect_drift(
            definitions, citation_path, errors
        )

        # ── Step 10: Log gaps ─────────────────────────────────────────
        _status(10, "Step 10/12 — Logging gaps…")
        gaps = gap_log.all()

        # ── Step 11: Build research map ───────────────────────────────
        _status(11, "Step 11/12 — Assembling research map…")
        source_list = list(citation_path.values())

        result = {
            # Section 1 — Header
            "question":          question,
            "timestamp":         timestamp,
            "pipeline_version":  "4.0",

            # Section 2 — Plain-English Restatement
            "restatement":       restatement,

            # Section 3 — Key Terms & Definitions
            "terms":             terms,
            "definitions":       definitions,

            # Section 4 — Corpus Findings
            "corpus_hits":       corpus_hits,

            # Section 5 — Citation & Doctrine Path
            "citation_path":     [
                {
                    "doc_id":      doc_id,
                    "title":       meta.get("title", ""),
                    "source_type": meta.get("source_type", ""),
                    "doc_date":    meta.get("doc_date", ""),
                    "citations":   meta.get("citations", []),
                    "self_cite":   meta.get("self_cite", ""),
                }
                for doc_id, meta in citation_path.items()
            ],

            # Section 6 — Semantic Drift Flags
            "drift_flags":       drift_flags,

            # Section 7 — Missing Information Log
            "gaps":              gaps,

            # Section 8 — Source List
            "source_list":       [
                {
                    "doc_id":      s.get("doc_id", ""),
                    "title":       s.get("title", ""),
                    "source_type": s.get("source_type", ""),
                    "doc_date":    s.get("doc_date", ""),
                    "self_cite":   s.get("self_cite", ""),
                    "path":        s.get("path", ""),
                }
                for s in source_list
            ],

            # Internal
            "errors":            errors,
        }

        # ── Step 12: Return ───────────────────────────────────────────
        _status(12, "Step 12/12 — Research map complete.")
        return result

    def save_report(self, result: dict, reports_dir: str = None) -> str:
        """
        Save a research map result to a folder on disk.

        Creates:
            reports/<timestamp>/report.json
            reports/<timestamp>/gap_log.json
            reports/<timestamp>/source_list.json
            reports/<timestamp>/report.html

        Parameters
        ----------
        result      : dict as returned by run().
        reports_dir : Destination parent folder. Defaults to config.REPORTS_DIR.

        Returns
        -------
        str — absolute path to the created report folder.
        """
        reports_dir = reports_dir or self._reports_dir
        if not reports_dir:
            raise ValueError("pipeline_runner.save_report: no reports_dir configured")

        # Folder name: timestamp + first 30 chars of question
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        q_slug = re.sub(r"[^\w\s-]", "", result.get("question", "research"))[:30].strip()
        q_slug = re.sub(r"\s+", "_", q_slug) or "research"
        folder_name = f"{ts}_{q_slug}"
        folder = Path(reports_dir) / folder_name
        folder.mkdir(parents=True, exist_ok=True)

        # report.json — full result
        (folder / "report.json").write_text(
            json.dumps(result, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

        # gap_log.json — just the gaps section
        (folder / "gap_log.json").write_text(
            json.dumps(result.get("gaps", []), indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

        # source_list.json — just the source list
        (folder / "source_list.json").write_text(
            json.dumps(result.get("source_list", []), indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

        # report.html — human-readable summary
        (folder / "report.html").write_text(
            self._render_html(result),
            encoding="utf-8"
        )

        return str(folder)

    # ------------------------------------------------------------------
    # Pipeline step implementations
    # ------------------------------------------------------------------

    def _restate(self, question: str, doc_text: str, errors: list) -> str:
        """Step 2 — Plain-English restatement."""
        if not question and not doc_text:
            return ""
        try:
            from ai_integration import AIIntegration
            ai = AIIntegration()
            if ai.is_configured():
                context = doc_text[:1500] if doc_text else ""
                prompt_text = question if not context else f"{question}\n\nDocument context:\n{context}"
                result = ai.ask_custom_question(
                    "Restate the following research question in plain English in one clear paragraph. "
                    "Do not answer it — only restate what is being asked:\n\n" + prompt_text,
                    ""
                )
                content = result.get("content", "").strip()
                if content and not result.get("error"):
                    return content
        except Exception as e:
            errors.append(f"Step 2 restate: {e}")

        # Fallback: return the question itself
        return question

    def _identify_terms(self, text: str, errors: list) -> list:
        """Step 3 — Extract key legal terms from the combined text."""
        if not text:
            return []
        try:
            from document_processor import DocumentProcessor
            dp = DocumentProcessor()
            if hasattr(dp, "find_key_legal_terms"):
                terms = dp.find_key_legal_terms(text)
                if isinstance(terms, list):
                    return [str(t) for t in terms]
        except Exception as e:
            errors.append(f"Step 3 identify_terms: {e}")

        # Fallback: extract capitalised multi-word phrases (simple heuristic)
        found = set()
        for m in re.finditer(
            r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b", text
        ):
            phrase = m.group(0).strip()
            if 3 < len(phrase) < 60:
                found.add(phrase)
        return sorted(found)[:30]

    def _define_terms(self, terms: list, errors: list) -> dict:
        """Step 4 — Look up plain-English and doctrinal definitions."""
        definitions: dict[str, dict] = {}
        if not terms:
            return definitions

        try:
            from literal_dictionary import LITERAL_DICTIONARY
        except Exception:
            LITERAL_DICTIONARY = {}

        try:
            from legal_dictionary import LEGAL_DICTIONARY
        except Exception:
            LEGAL_DICTIONARY = {}

        for term in terms:
            term_lower = term.lower().replace(" ", "_")
            plain_def = ""
            doctrinal_def = ""
            plain_source = ""
            doctrinal_source = ""

            # Plain-English: literal dictionary
            for key, val in LITERAL_DICTIONARY.items():
                if key.lower() == term_lower or term.lower() in key.lower():
                    plain_def = val.get("definition", "") if isinstance(val, dict) else str(val)
                    plain_source = "Literal Dictionary"
                    break

            # Doctrinal: legal dictionary
            for key, val in LEGAL_DICTIONARY.items():
                if key.lower() == term_lower or term.lower() in key.lower():
                    if isinstance(val, dict):
                        doctrinal_def = (
                            val.get("definition")
                            or val.get("legal_definition", "")
                        )
                        doctrinal_source = val.get("source") or val.get("legal_source", "Legal Dictionary")
                    else:
                        doctrinal_def = str(val)
                        doctrinal_source = "Legal Dictionary"
                    break

            definitions[term] = {
                "plain_english":       plain_def,
                "plain_source":        plain_source,
                "doctrinal":           doctrinal_def,
                "doctrinal_source":    doctrinal_source,
            }

        return definitions

    def _search_corpus(
        self,
        question: str,
        terms: list,
        definitions: dict,
        errors: list,
    ):
        """Steps 5 & 6 — Search corpus and return ranked hits + a fresh GapLog."""
        GapLog, UNRESOLVED_CITATION, UNDEFINED_TERM, EMPTY_SEARCH = _import_gap_log()
        gap_log = GapLog()

        if not self._corpus_db:
            errors.append("Step 5: no CORPUS_DB_PATH configured")
            return [], gap_log

        try:
            CorpusIndex = _import_corpus_index()
            idx = CorpusIndex(db_path=self._corpus_db)
        except Exception as e:
            errors.append(f"Step 5 corpus open: {e}")
            return [], gap_log

        # Build search query: question + top terms
        query_parts = [question] + terms[:5]
        query = " ".join(query_parts).strip()

        hits = []
        try:
            hits = idx.search(
                query,
                limit=self._search_limit,
                prefer_primary=True   # Step 6: primary before secondary enforced
            )
        except Exception as e:
            errors.append(f"Step 5 search: {e}")

        # Log empty search as a gap
        if not hits and query.strip():
            gap_log.add(
                EMPTY_SEARCH,
                query[:200],
                source_doc_id=None,
                best_link=None,
            )

        # Log undefined terms (terms with no definition found)
        for term, defn in definitions.items():
            if not defn.get("plain_english") and not defn.get("doctrinal"):
                gap_log.add(
                    UNDEFINED_TERM,
                    term,
                    source_doc_id=None,
                    best_link=None,
                )

        return hits, gap_log

    def _follow_citations(
        self,
        corpus_hits: list,
        gap_log,
        errors: list,
    ):
        """Steps 7 & 8 — Follow citations recursively and return ordered doctrine path."""
        if not self._corpus_db:
            errors.append("Step 7: no CORPUS_DB_PATH configured")
            return OrderedDict(), None

        try:
            CorpusIndex = _import_corpus_index()
            CitationGraph = _import_citation_graph()
            idx   = CorpusIndex(db_path=self._corpus_db)
            graph = CitationGraph()
        except Exception as e:
            errors.append(f"Step 7 init: {e}")
            return OrderedDict(), None

        # Seed from top primary hits (up to 5)
        seed_ids = [
            h["doc_id"] for h in corpus_hits
            if h.get("source_type") == "primary"
        ][:5]

        # If no primary hits, use whatever we have
        if not seed_ids:
            seed_ids = [h["doc_id"] for h in corpus_hits][:5]

        if not seed_ids:
            return OrderedDict(), graph

        try:
            citation_path = graph.follow(
                seed_ids,
                idx,
                gap_log,
                max_hops=self._max_hops,
            )
        except Exception as e:
            errors.append(f"Step 7 follow: {e}")
            citation_path = OrderedDict()

        return citation_path, graph

    def _detect_drift(
        self,
        definitions: dict,
        citation_path: OrderedDict,
        errors: list,
    ) -> list:
        """Step 9 — Detect semantic drift in term usage across sources."""
        drift_flags: list[dict] = []
        if not definitions or not citation_path:
            return drift_flags

        try:
            from consistency_engine import ConsistencyEngine
            engine = ConsistencyEngine()
        except Exception as e:
            errors.append(f"Step 9 consistency_engine import: {e}")
            return drift_flags

        for term, defn in definitions.items():
            baseline = defn.get("doctrinal") or defn.get("plain_english")
            if not baseline:
                continue

            for doc_id, meta in citation_path.items():
                doc_path = meta.get("path", "")
                if not doc_path or not os.path.isfile(doc_path):
                    continue
                try:
                    with open(doc_path, "r", encoding="utf-8", errors="replace") as f:
                        doc_text = f.read()
                except OSError:
                    continue

                # Extract sentences containing the term
                sentences = [
                    s.strip() for s in re.split(r"[.!?]", doc_text)
                    if term.lower() in s.lower() and len(s.strip()) > 20
                ]
                if not sentences:
                    continue

                usage_sample = " ".join(sentences[:3])

                # Use consistency_engine to compare baseline vs usage
                try:
                    if hasattr(engine, "compare_statements"):
                        result = engine.compare_statements(baseline, usage_sample)
                        score = result.get("similarity", 1.0) if isinstance(result, dict) else 1.0
                    else:
                        # Simple word-overlap fallback
                        b_words = set(baseline.lower().split())
                        u_words = set(usage_sample.lower().split())
                        overlap = len(b_words & u_words)
                        score = overlap / max(len(b_words), 1)

                    if score < 0.3:
                        drift_flags.append({
                            "term":           term,
                            "doc_id":         doc_id,
                            "doc_title":      meta.get("title", ""),
                            "baseline":       baseline[:200],
                            "usage_sample":   usage_sample[:200],
                            "similarity":     round(score, 3),
                        })
                except Exception as e:
                    errors.append(f"Step 9 drift check ({term}): {e}")

        return drift_flags

    # ------------------------------------------------------------------
    # HTML rendering
    # ------------------------------------------------------------------

    def _render_html(self, result: dict) -> str:
        """Render the research map as a simple readable HTML file."""
        q = result.get("question", "")
        ts = result.get("timestamp", "")
        restatement = result.get("restatement", "")
        terms = result.get("terms", [])
        definitions = result.get("definitions", {})
        corpus_hits = result.get("corpus_hits", [])
        citation_path = result.get("citation_path", [])
        drift_flags = result.get("drift_flags", [])
        gaps = result.get("gaps", [])
        source_list = result.get("source_list", [])
        errors = result.get("errors", [])

        def esc(s):
            return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        sections = []

        # 1 — Header
        sections.append(f"""
<div class="section">
  <h2>1. Research Query</h2>
  <p><strong>Question:</strong> {esc(q)}</p>
  <p><strong>Timestamp:</strong> {esc(ts)}</p>
  <p><strong>Pipeline:</strong> VERITAS v{esc(result.get('pipeline_version','4.0'))}</p>
</div>""")

        # 2 — Restatement
        if restatement:
            sections.append(f"""
<div class="section">
  <h2>2. Plain-English Restatement</h2>
  <p>{esc(restatement)}</p>
</div>""")

        # 3 — Terms & Definitions
        if definitions:
            rows = ""
            for term, defn in definitions.items():
                plain = esc(defn.get("plain_english") or "—")
                doc   = esc(defn.get("doctrinal")    or "—")
                rows += f"<tr><td><strong>{esc(term)}</strong></td><td>{plain}</td><td>{doc}</td></tr>\n"
            sections.append(f"""
<div class="section">
  <h2>3. Key Terms &amp; Definitions</h2>
  <table>
    <thead><tr><th>Term</th><th>Plain English</th><th>Doctrinal</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
</div>""")

        # 4 — Corpus Findings
        if corpus_hits:
            rows = ""
            for h in corpus_hits:
                rows += (
                    f"<tr><td>{esc(h.get('title',''))}</td>"
                    f"<td>{esc(h.get('source_type',''))}</td>"
                    f"<td>{esc(h.get('doc_date',''))}</td>"
                    f"<td>{esc(h.get('snippet',''))}</td></tr>\n"
                )
            sections.append(f"""
<div class="section">
  <h2>4. Corpus Findings</h2>
  <table>
    <thead><tr><th>Title</th><th>Type</th><th>Date</th><th>Excerpt</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
</div>""")
        else:
            sections.append('<div class="section"><h2>4. Corpus Findings</h2><p class="empty">No corpus documents matched this query. Add documents to corpus/primary/ or corpus/secondary/ and re-run.</p></div>')

        # 5 — Citation & Doctrine Path
        if citation_path:
            items = ""
            for i, doc in enumerate(citation_path, 1):
                items += (
                    f"<li>[{i}] <strong>{esc(doc.get('title',''))}</strong> "
                    f"({esc(doc.get('source_type',''))}, {esc(doc.get('doc_date',''))}) "
                    f"— {esc(doc.get('self_cite',''))}</li>\n"
                )
            sections.append(f"""
<div class="section">
  <h2>5. Citation &amp; Doctrine Path</h2>
  <ol>{items}</ol>
</div>""")
        else:
            sections.append('<div class="section"><h2>5. Citation &amp; Doctrine Path</h2><p class="empty">No citation chain resolved.</p></div>')

        # 6 — Drift Flags
        if drift_flags:
            rows = ""
            for d in drift_flags:
                rows += (
                    f"<tr><td>{esc(d.get('term',''))}</td>"
                    f"<td>{esc(d.get('doc_title',''))}</td>"
                    f"<td>{esc(d.get('similarity',''))}</td>"
                    f"<td>{esc(d.get('usage_sample','')[:120])}</td></tr>\n"
                )
            sections.append(f"""
<div class="section">
  <h2>6. Semantic Drift Flags</h2>
  <table>
    <thead><tr><th>Term</th><th>Document</th><th>Similarity</th><th>Usage Sample</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
</div>""")
        else:
            sections.append('<div class="section"><h2>6. Semantic Drift Flags</h2><p class="empty">No drift detected.</p></div>')

        # 7 — Gaps
        if gaps:
            rows = ""
            for g in gaps:
                rows += (
                    f"<tr><td>{esc(g.get('gap_type',''))}</td>"
                    f"<td>{esc(g.get('value',''))}</td>"
                    f"<td>{esc(g.get('source_doc_id','') or '—')}</td>"
                    f"<td>{esc(g.get('best_link','') or '—')}</td></tr>\n"
                )
            sections.append(f"""
<div class="section">
  <h2>7. Missing Information Log</h2>
  <table>
    <thead><tr><th>Type</th><th>Value</th><th>Source Doc</th><th>Reference</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
</div>""")
        else:
            sections.append('<div class="section"><h2>7. Missing Information Log</h2><p class="empty">No gaps logged.</p></div>')

        # 8 — Source List
        if source_list:
            rows = ""
            for s in source_list:
                rows += (
                    f"<tr><td>{esc(s.get('title',''))}</td>"
                    f"<td>{esc(s.get('source_type',''))}</td>"
                    f"<td>{esc(s.get('doc_date',''))}</td>"
                    f"<td><code>{esc(s.get('self_cite','') or '—')}</code></td></tr>\n"
                )
            sections.append(f"""
<div class="section">
  <h2>8. Source List</h2>
  <table>
    <thead><tr><th>Title</th><th>Type</th><th>Date</th><th>Citation</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
</div>""")

        # Errors (collapsible footer)
        if errors:
            err_items = "".join(f"<li>{esc(e)}</li>" for e in errors)
            sections.append(f'<div class="section errors"><h2>Pipeline Errors</h2><ul>{err_items}</ul></div>')

        body = "\n".join(sections)

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>VERITAS Research Map — {esc(q[:60])}</title>
<style>
  body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #111; color: #eee;
         max-width: 1200px; margin: 0 auto; padding: 20px; }}
  h1   {{ color: #9ab; border-bottom: 2px solid #334; padding-bottom: 8px; }}
  h2   {{ color: #8ab; margin-top: 0; }}
  .section {{ background: #1a1a1a; border: 1px solid #333; border-radius: 6px;
              padding: 16px 20px; margin-bottom: 16px; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
  th    {{ background: #2a3a4a; color: #cde; text-align: left; padding: 8px; }}
  td    {{ border-bottom: 1px solid #222; padding: 7px 8px; vertical-align: top; }}
  tr:hover td {{ background: #1e2a30; }}
  code  {{ background: #222; padding: 1px 4px; border-radius: 3px; font-size: 12px; }}
  .empty {{ color: #666; font-style: italic; }}
  .errors {{ border-color: #633; }}
  .errors h2 {{ color: #c88; }}
</style>
</head>
<body>
<h1>VERITAS Research Map</h1>
<p style="color:#666">Generated: {esc(ts)} &nbsp;|&nbsp; VERITAS Pipeline v{esc(result.get('pipeline_version','4.0'))}</p>
{body}
</body>
</html>"""
