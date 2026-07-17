"""
citation_graph.py — VERITAS Phase 3

Owns citation relationship recording, directed graph construction, forward
and reverse citation lookup, recursive citation following, and ordered
doctrine/timeline path assembly (pipeline steps 7 and 8).

All citation resolution is performed against a CorpusIndex instance.
Unresolved citations are logged to a GapLog instance.  No legal analysis
is performed here; no internet access occurs; no UI is modified.

Public API
----------
    CitationGraph()
    .add_citation(citing_doc_id, cited_doc_id) -> None
    .forward(doc_id) -> list[str]
    .reverse(doc_id) -> list[str]
    .follow(seed_doc_ids, corpus_index, gap_log,
            max_hops=3) -> OrderedDict[str, dict]
    .has_citation(citing_doc_id, cited_doc_id) -> bool
    .all_nodes() -> list[str]
    .all_edges() -> list[tuple[str, str]]
    .node_count() -> int
    .edge_count() -> int
    .clear() -> None

Design notes
------------
The graph is stored as two adjacency dicts:
  _forward : {citing_doc_id: set of cited_doc_ids}
  _reverse : {cited_doc_id:  set of citing_doc_ids}

follow() performs a breadth-first walk from the seed documents, resolving
citation strings in each visited document via corpus_index.resolve(), logging
anything that does not resolve to gap_log, and returning an OrderedDict keyed
by doc_id in chronological/insertion order (primary-source-first within the
same BM25 tier, matching corpus_index.list_all() ordering for the resolved
subset).

follow() also populates the internal graph as a side-effect, so callers can
query forward()/reverse() after a follow() call without a separate build step.
"""

from __future__ import annotations

import json
import re
from collections import OrderedDict, deque
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from corpus_index import CorpusIndex
    from gap_log import GapLog

# ---------------------------------------------------------------------------
# Citation string extraction (same generic patterns as corpus_index.py;
# duplicated here intentionally so citation_graph has no import dependency
# on corpus_index internals — it calls the public API only)
# ---------------------------------------------------------------------------

_CASE_RE = re.compile(
    r"\b[A-Z][A-Za-z\s''‑-]{0,40}\s+v\.?\s+[A-Z][A-Za-z\s''‑-]{1,40}"
    r"(?:\s*[\[\(]\d{4}[\]\)])?(?:\s+\d+\s+[A-Z]{2,6}\s+\d+)?",
    re.IGNORECASE,
)
_NEUTRAL_RE = re.compile(r"\[\d{4}\]\s+[A-Z]{2,6}\s+\d+")
_STATUTE_RE = re.compile(
    r"\b[A-Z][A-Za-z\s]{2,40}"
    r"(?:Act|Statute|Code|Regulation|Ordinance|Constitution)\b"
)


def _extract_citation_strings(text: str) -> list[str]:
    """Return deduplicated citation strings found in raw text."""
    found: set[str] = set()
    for m in _CASE_RE.finditer(text):
        s = m.group(0).strip()
        if len(s) > 5:
            found.add(s)
    for m in _NEUTRAL_RE.finditer(text):
        found.add(m.group(0).strip())
    for m in _STATUTE_RE.finditer(text):
        s = m.group(0).strip()
        if len(s) > 6:
            found.add(s)
    return sorted(found)


# ---------------------------------------------------------------------------
# CitationGraph
# ---------------------------------------------------------------------------

class CitationGraph:
    """
    Directed graph of document-to-document citation relationships.

    Documents are identified by their corpus doc_id (SHA-256 hex string
    from CorpusIndex).  The graph holds only the relationship structure;
    document metadata lives in CorpusIndex.

    Thread-safety: not thread-safe (pipeline runs sequentially on desktop).
    """

    def __init__(self) -> None:
        # {citing_doc_id: set[cited_doc_id]}
        self._forward: dict[str, set[str]] = {}
        # {cited_doc_id: set[citing_doc_id]}
        self._reverse: dict[str, set[str]] = {}

    # ------------------------------------------------------------------
    # Graph mutation
    # ------------------------------------------------------------------

    def add_citation(self, citing_doc_id: str, cited_doc_id: str) -> None:
        """
        Record that citing_doc_id cites cited_doc_id.

        Silently deduplicates: adding the same edge twice is a no-op.

        Parameters
        ----------
        citing_doc_id : doc_id of the document that contains the citation.
        cited_doc_id  : doc_id of the document being cited.

        Raises
        ------
        ValueError : Either ID is empty or None.
        ValueError : citing_doc_id == cited_doc_id (self-citation).
        """
        if not citing_doc_id or not str(citing_doc_id).strip():
            raise ValueError(
                "citation_graph.add_citation: citing_doc_id must be non-empty"
            )
        if not cited_doc_id or not str(cited_doc_id).strip():
            raise ValueError(
                "citation_graph.add_citation: cited_doc_id must be non-empty"
            )
        citing_doc_id = str(citing_doc_id).strip()
        cited_doc_id  = str(cited_doc_id).strip()
        if citing_doc_id == cited_doc_id:
            raise ValueError(
                "citation_graph.add_citation: self-citation not permitted "
                f"(doc_id={citing_doc_id!r})"
            )

        self._forward.setdefault(citing_doc_id, set()).add(cited_doc_id)
        self._reverse.setdefault(cited_doc_id,  set()).add(citing_doc_id)

        # Ensure both nodes appear even when they have no edges in the
        # other direction yet
        self._forward.setdefault(cited_doc_id,  set())
        self._reverse.setdefault(citing_doc_id, set())

    def clear(self) -> None:
        """Remove all nodes and edges from the graph."""
        self._forward.clear()
        self._reverse.clear()

    # ------------------------------------------------------------------
    # Graph queries
    # ------------------------------------------------------------------

    def forward(self, doc_id: str) -> list[str]:
        """
        Return the doc_ids of all documents cited BY doc_id.

        Parameters
        ----------
        doc_id : The citing document's doc_id.

        Returns
        -------
        Sorted list of doc_ids.  Empty list if doc_id has no outgoing edges
        or is not in the graph.
        """
        return sorted(self._forward.get(str(doc_id).strip(), set()))

    def reverse(self, doc_id: str) -> list[str]:
        """
        Return the doc_ids of all documents that CITE doc_id.

        Parameters
        ----------
        doc_id : The cited document's doc_id.

        Returns
        -------
        Sorted list of doc_ids.  Empty list if doc_id has no incoming edges
        or is not in the graph.
        """
        return sorted(self._reverse.get(str(doc_id).strip(), set()))

    def has_citation(self, citing_doc_id: str, cited_doc_id: str) -> bool:
        """
        Return True if a direct citation edge from citing → cited exists.
        """
        return cited_doc_id in self._forward.get(
            str(citing_doc_id).strip(), set()
        )

    def all_nodes(self) -> list[str]:
        """
        Return a sorted list of all doc_ids that appear in the graph
        (as either a citing or cited document).
        """
        nodes: set[str] = set(self._forward.keys()) | set(self._reverse.keys())
        return sorted(nodes)

    def all_edges(self) -> list[tuple[str, str]]:
        """
        Return a sorted list of all (citing_doc_id, cited_doc_id) edge tuples.
        """
        edges: list[tuple[str, str]] = []
        for citing, cited_set in self._forward.items():
            for cited in cited_set:
                edges.append((citing, cited))
        return sorted(edges)

    def node_count(self) -> int:
        """Return the number of distinct documents in the graph."""
        return len(self.all_nodes())

    def edge_count(self) -> int:
        """Return the number of directed citation edges in the graph."""
        return sum(len(v) for v in self._forward.values())

    # ------------------------------------------------------------------
    # Citation following (pipeline steps 7 + 8)
    # ------------------------------------------------------------------

    def follow(
        self,
        seed_doc_ids: list[str],
        corpus_index: "CorpusIndex",
        gap_log: "GapLog",
        max_hops: int = 3,
    ) -> "OrderedDict[str, dict]":
        """
        Recursively follow citations starting from seed_doc_ids.

        Algorithm (breadth-first, hop-limited):
          1. Enqueue each seed doc_id at hop 0.
          2. For each doc at the current hop:
             a. Retrieve its stored citation strings from corpus_index.
             b. Attempt to resolve each citation string via
                corpus_index.resolve().
             c. If resolved and not yet visited: add edge to graph, enqueue
                target at hop+1.
             d. If not resolved: log to gap_log as UNRESOLVED_CITATION with
                the citing doc_id as source.
          3. Stop when the queue is empty or max_hops is reached.
          4. Return an OrderedDict of {doc_id: metadata} for every document
             visited, ordered chronologically (by doc_date) with primary
             sources before secondary sources within the same date.

        This method also updates the internal citation graph as a side-effect,
        so forward()/reverse()/has_citation() reflect the walk after the call.

        Parameters
        ----------
        seed_doc_ids  : Starting document doc_ids (pipeline step 7 entry
                        point — typically the top-ranked primary sources from
                        corpus_index.search()).
        corpus_index  : A CorpusIndex instance (must already have documents
                        ingested).
        gap_log       : A GapLog instance to receive UNRESOLVED_CITATION
                        entries for any citation string that could not be
                        resolved.
        max_hops      : Maximum recursive depth (default 3, configurable via
                        config.py in the full pipeline).  Prevents runaway
                        walks on densely cited corpora.

        Returns
        -------
        OrderedDict[str, dict]
            Keys   : doc_id strings, in chronological / primary-first order.
            Values : metadata dicts from corpus_index.list_all() for each
                     visited document.  Seeds that are not found in the corpus
                     are silently omitted from the result (they cannot be
                     walked).

        Raises
        ------
        ValueError : max_hops < 1.
        TypeError  : corpus_index or gap_log is None.
        """
        if corpus_index is None:
            raise TypeError(
                "citation_graph.follow: corpus_index must not be None"
            )
        if gap_log is None:
            raise TypeError(
                "citation_graph.follow: gap_log must not be None"
            )
        if max_hops < 1:
            raise ValueError(
                f"citation_graph.follow: max_hops must be >= 1, got {max_hops}"
            )

        # Build a metadata lookup from corpus for quick access
        all_meta: dict[str, dict] = {
            doc["doc_id"]: doc for doc in corpus_index.list_all()
        }

        from gap_log import UNRESOLVED_CITATION  # avoid circular at module level

        visited: dict[str, int] = {}   # doc_id -> hop at which it was visited
        queue: deque[tuple[str, int]] = deque()

        # Seed the queue — only with doc_ids that actually exist in corpus
        for doc_id in seed_doc_ids:
            doc_id = str(doc_id).strip()
            if doc_id in all_meta and doc_id not in visited:
                visited[doc_id] = 0
                queue.append((doc_id, 0))

        while queue:
            current_id, hop = queue.popleft()

            if hop >= max_hops:
                # Reached the hop limit: record the node as visited but
                # do not follow its citations further.
                continue

            # Retrieve citation strings stored for this document
            meta = all_meta.get(current_id, {})
            raw_citations: list[str] = meta.get("citations", [])

            # Also re-extract from the stored JSON in case citations field
            # is a JSON string rather than a list (defensive)
            if isinstance(raw_citations, str):
                try:
                    raw_citations = json.loads(raw_citations)
                except (json.JSONDecodeError, TypeError):
                    raw_citations = []

            for cit_str in raw_citations:
                resolved_id = corpus_index.resolve(cit_str)

                if resolved_id is None:
                    # Log as unresolved gap
                    gap_log.add(
                        UNRESOLVED_CITATION,
                        cit_str,
                        source_doc_id=current_id,
                        best_link=None,
                    )
                    continue

                # Avoid self-loops (resolve might return the document itself)
                if resolved_id == current_id:
                    continue

                # Record the edge
                self.add_citation(current_id, resolved_id)

                # Enqueue if not yet visited
                if resolved_id not in visited:
                    visited[resolved_id] = hop + 1
                    queue.append((resolved_id, hop + 1))

        # Assemble result: chronological order, primary before secondary
        # within the same date, matching list_all() ordering semantics.
        def _sort_key(doc_id: str) -> tuple:
            m = all_meta.get(doc_id, {})
            source_rank = 0 if m.get("source_type") == "primary" else 1
            date = m.get("doc_date") or "9999-99-99"
            title = m.get("title") or ""
            return (source_rank, date, title)

        ordered_ids = sorted(visited.keys(), key=_sort_key)

        result: OrderedDict[str, dict] = OrderedDict()
        for doc_id in ordered_ids:
            if doc_id in all_meta:
                result[doc_id] = dict(all_meta[doc_id])

        return result

    # ------------------------------------------------------------------
    # Convenience / introspection
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"<CitationGraph nodes={self.node_count()} "
            f"edges={self.edge_count()}>"
        )
