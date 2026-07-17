# VERITAS — Governing Design (drift model)

*Authoritative architecture doc. If code or data conflicts with this, this wins. Written 2026-07-08.*

## Thesis

VERITAS measures **constitutional drift** — how the meaning of the Constitution moves
away from what it meant at the framing. The core insight: **the words themselves drift.**
So VERITAS does not store *a* definition per word; it stores a **timeline** of authoritative
definitions, and lets you watch the meaning move.

## 1. The baseline — "common use at the time" (the founding)

A word's founding-era meaning is fixed by **three sources, shown together by default**:

1. **Johnson's Dictionary, 1773** — the ordinary-meaning baseline, closest in time to the 1787 framing.
   - Data: `03_LIBRARIES/VERITAS_definitions_library.json` (5,125 verbatim entries, v3.1).
2. **Etymology** — the origin anchor (where the word came from).
   - Data (starter): the bracketed etymology inside each Johnson entry (e.g. `[obtenir, Fr. obtineo, Latin.]`).
   - Data (deepen): a published etymological authority — Skeat's *Etymological Dictionary* (public domain).
3. **Historical documents of the era** — actual founding-era usage.
   - Data: `03_LIBRARIES/constitutional_usage_database.json` — 11 sources (Federalist, Anti-Federalist,
     Madison's Notes, Elliot's Debates, Farrand's Records, Story, Rawle), keyed by word with quotes;
     1,395 words covered. Also `VERITAS_historical_context_library.json` for drafting/ratification intent.

These three = **what a literate person at the framing understood the word to mean.**

## 2. The drift series — every later authority, in publication order

Every **other** dictionary on file is a drift measurement point, ordered by **publication date**,
covering **common use** *and* **legal** meaning:

| ~Era (≥1 per 30 yrs) | Source | Register | Obtainability |
|---|---|---|---|
| origin | Skeat's Etymological Dict. (1910) / Century | etymology | ✅ public domain |
| 1755/1773 | **Johnson** *(baseline, not drift)* | common | ✅ have it |
| ~1806 / 1828 | Webster's American Dictionary | common | ✅ public domain |
| ~1864 | Webster / Worcester | common | ✅ public domain |
| 1891 / 1910 | Black's Law Dictionary, 1st / 2nd ed. | legal | ✅ public domain |
| 1913 | **Webster's** | common | ✅ have it (`sources_data/webster1913.json`) |
| ~1930s → present | OED, modern Black's, current common-use | both | ⚠️ copyright/subscription — licensed or cited-fair-use only |

**Cadence rule:** at least one authoritative dictionary every **30 years**, so drift is
measurable at constitutional resolution. The founding→1913 spine is fully buildable from
public-domain authorities; the 20th-century-to-present tail needs licensing (no scraping).

## 3. The admission bar — what may enter VERITAS

An entry is admissible **only** from a **fixed, citable, published authority**: a published book
or a scientifically/scholarly-backed manuscript.

- **Meets the bar:** Johnson, Webster (any edition), Black's, OED, Skeat, and the named
  historical-document corpus. Drift between editions is *acceptable and bounded* — you know
  exactly what the source is and when.
- **Fails the bar:** Wiktionary and any crowd-sourced / mutable / anonymous source. It doesn't
  add a definition, it adds **vagueness** — there is no fixed authority to cite.
- **Hard Rule 1 still governs:** every stored definition is **verbatim** — never invented or
  paraphrased — and **provenance-tagged** (source, year, edition, register).

The coverage checker (`07_CAPTURE_TOOLS/check_coverage.py`) may query non-admissible sources only
as **finders** (does this word exist / is it worth capturing) — a finder never becomes an entry.

## 4. Entry schema — a per-word timeline

Each word is an **ordered list of provenance-tagged snapshots**. The first three are the fixed
baseline triad; the rest are the drift series sorted by publication year.

```json
{
  "word": "commerce",
  "sources": [
    { "seq": 0, "tier": "baseline", "role": "johnson_1773",     "source": "Johnson", "year": 1773, "register": "common",    "verbatim_text": "...", "show_default": true },
    { "seq": 1, "tier": "baseline", "role": "etymology",         "source": "Skeat/Johnson-bracket",  "register": "etymology","verbatim_text": "...", "show_default": true },
    { "seq": 2, "tier": "baseline", "role": "historical_usage",  "source": "constitutional_usage_database", "register": "usage", "quotes": [ { "quote": "...", "source": "The Federalist Papers (1787-88)", "year": 1788 } ], "show_default": true },

    { "seq": 3, "tier": "drift", "source": "Webster",       "year": 1828, "register": "common", "verbatim_text": "...", "show_default": false },
    { "seq": 4, "tier": "drift", "source": "Webster",       "year": 1913, "register": "common", "verbatim_text": "...", "show_default": false },
    { "seq": 5, "tier": "drift", "source": "Black's Law",   "year": 1910, "register": "legal",  "verbatim_text": "...", "show_default": false }
  ]
}
```

**Storage rule:** add **one snapshot per word for every dictionary in the file** — the full
timeline is always stored, even when hidden.

## 5. Display rule — "Define the Drift"

- **Default view:** only the **first three** snapshots (the baseline triad) render — the
  founding-era common meaning, clean and uncluttered.
- **"Define the Drift"** — a user control. Clicking it reveals the rest: the full
  publication-ordered drift series, so the reader *opts in* to see how the meaning moved.
- Drift is never shown unbidden; the baseline is the default truth, drift is the investigation.

## 6. Current state → target (build roadmap)

| Component | Have | Needed |
|---|---|---|
| Johnson 1773 baseline | ✅ 5,125 verbatim entries (v3.1) | — |
| Etymology baseline | ⚠️ partial (Johnson brackets) | extract brackets; add Skeat for depth |
| Historical-usage baseline | ✅ `constitutional_usage_database.json` (1,395 words) | merge into timeline schema |
| Timeline schema migration | ✅ v3.2 — `sources[]` on all 5,125 entries (`migrate_to_timeline.py`) | — |
| Drift: Webster 1913 | ✅ v3.3 — snapshots on 3,784 entries (`add_webster_drift.py`) | — |
| Drift: Black's 1910 (legal) | ✅ v3.4 — 1,328 entries, LexPredict src (`add_blacks_drift.py`) | — |
| Drift: Webster 1828 (common) | ✅ v3.5 — 4,166 entries, DataWar src (`add_webster1828_drift.py`) | — |
| Drift: Webster 1844 (common) | ✅ v3.6 — 4,197 entries, DataWar src (`add_webster1844_drift.py`) | — |
| Drift: Webster 1864 | ❌ optional | fills 1844→1910 gap |
| Drift: Black's 1st (1891) | ❌ optional | earlier legal point |
| Drift: OED / modern | ❌ | licensed route only (not scraping) |
| "Define the Drift" UI | ✅ — clickable link + timeline window in `01_APP/main.py`; `veritas_definitions.get_timeline/has_drift` | — |

**Migration is additive and must preserve Hard Rule 1:** the existing Johnson `definition`
becomes `sources[0]` verbatim; nothing is reworded; every new snapshot is provenance-tagged.

## Constraint (unchanged)

Johnson's site prohibits systematic bulk download (non-commercial only) — bounded, respectful,
per-word batches with ≥1.5s delay; no full-dictionary harvest. Etymonline is off-limits (ToS).
Use bulk-legal published authorities (Webster, Black's early eds., Skeat) for the drift series.
