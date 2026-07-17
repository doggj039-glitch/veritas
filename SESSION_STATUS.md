# VERITAS — Session Status (2026-07-08, library v3.6 — timeline + four drift points; "Define the Drift" UI live)

> UI (2026-07-08): "Define the Drift" shipped in `01_APP`. Research Map → "Key Terms & Definitions" now shows a clickable **⊕ Define the Drift** link per drifting term → opens a timeline window (baseline shown, drift in publication order, verbatim + provenance). Files: `veritas_definitions.py` (`get_timeline`/`has_drift`), `main.py` (`_display_research_result` link + `_open_drift_window`). No library change. Launch: `cd 01_APP && source .venv/bin/activate && python3 run.py` → Research Map tab.

> v3.6 (2026-07-08): drift pass #4 — Webster 1844 (common) → 4,197 entries; 1,236 now carry the full 1828→1844→1910→1913 arc. Source: DataWar `dictionary_webster1844.sql` (8-col schema) → `sources_data/webster1844.json` (73,217 headwords, junk-free). md5 `2221c527d493`, 4 copies identical. Backup `…BACKUP-BEFORE-W1844-DRIFT.json`; script `add_webster1844_drift.py`.
> v3.5: drift pass #3 — Webster 1828 (common) → 4,166 entries. 577 scrape-error pages filtered pre-ingest (25 hit library words), verified none reached the library. `sources_data/webster1828.json`; script `add_webster1828_drift.py`.
> v3.4: drift pass #2 — Black's Law 1910 (LEGAL) → 1,328 entries (1,259 both registers). LexPredict src (public-domain text; CC-BY-SA transcription, OCR) → `sources_data/blacks_1910.json`. Script `add_blacks_drift.py`.
> v3.3: drift pass #1 — Webster 1913 (common) → 3,784 entries (`add_webster_drift.py`).
> v3.2: timeline-schema migration — ordered `sources[]` on every entry (`migrate_to_timeline.py`).
> **Next:** Webster 1828/1864 (public domain, common) to fill pre-1913 cadence, then build the "Define the Drift" UI in `01_APP`. OED/modern = licensed only.

Snapshot of where the VERITAS definitions work stands, so it can be resumed from
any new session (or by a person). All work is on disk; nothing lives only in chat.

## Library state — v3.1
- **`03_LIBRARIES/VERITAS_definitions_library.json` = the one true dictionary, 5,125 verbatim Johnson entries.**
- Three identical copies live in `02_GATE_BLACKLETTER/{gate,engine,nova_johnson}/` (the gate needs a copy in each). **All four are byte-identical — md5 `b90d3058b95d`.**
- Metadata now carries `library_version: 3.1`, `last_updated: 2026-07-08`, `total_entries: 5125`, and a `build_history` list.
- Lineage: 209 (original) → +709 first 1773 pass → 62 adopted verbatim → +422 missed-words → 1,340 → +1,950 vocab-expansion → 3,290 → desktop-corrected swap + `obtain` + 9 stub fixes → **3,296 (v3.0)** → **+1,829 round-2 self-grounding-gap scrape → 5,125 (v3.1)**.
- Every entry is verbatim from johnsonsdictionaryonline.com (1755/1773). Nothing invented/paraphrased (Hard Rule 1). Adding version metadata left the entries content md5 unchanged (verified).

## Round-2 expansion — DONE (2026-07-08)
- Overnight scrape `03_LIBRARIES/vocab_round2_results.json` (1,905 words; 1,833 found) merged via `07_CAPTURE_TOOLS/process_vocab_round2.py` (loads the CURRENT library as base, not an old backup).
- Result: **1,829 added** (442 via root-retry), 1 re-verified (`obtain`), 3 blocked by the headword-mismatch safeguard (`began, eve, hidden` — manual lookup if wanted), 72 not-found (Roman numerals, comparatives/superlatives, proper nouns — legit non-headwords).
- Reports: `03_LIBRARIES/vocab_round2_report.{json,txt}`.
- Pre-merge backup: `VERITAS_definitions_library.BACKUP-BEFORE-VOCAB-ROUND2.json` (md5 `76629ee1096a`). Pre-finalize backup: `…BACKUP-BEFORE-V3.1-FINALIZE.json` (md5 `ac8d9af0fde5`).

## NEW — pre-flight coverage verifier (2026-07-08)
- `07_CAPTURE_TOOLS/check_coverage.py` — give it keywords; it reports which preloaded sources have each word BEFORE you capture, classifying each as **WORTH CAPTURING** or **DEAD END**. Writes a matrix + optional JSON report.
- Registry: `07_CAPTURE_TOOLS/sources.json`. Source types: `offline_library` / `offline_index` (instant, zero-network) and `ajax_probe` (bounded live existence-ping ≥1.5s, auto-skips words already in the library).
- **Enabled:** `veritas_library` (5,125-entry lib), `johnson_1773` (headless AJAX ping to `../ajax/search_mysql_new.php`), `webster1913`.
- **Webster's 1913** (public domain): full text `07_CAPTURE_TOOLS/sources_data/webster1913.json` (23 MB); headword index `sources_data/webster1913_headwords.txt` (102,217 lowercased headwords). Secondary source only — if pulling its definitions later, tag provenance and keep OUT of the verbatim-Johnson `definition` field.
- **Stubbed (one step from active):** `wiktionary`, `wordnet` — set `path` + `enabled: true` in `sources.json`.
- Usage: `python3 07_CAPTURE_TOOLS/check_coverage.py word1 word2 …` or `--file words.txt --json report.json`.

## Housekeeping — CLEARED (2026-07-08)
- Nightly Johnson cron (`0 1 * * *`) **removed**; crontab empty (backup `07_CAPTURE_TOOLS/crontab.backup.2026-07-08.txt`).
- Power setting **restored**: `inactivity-on-ac = 360` (read-back confirmed).
- No temporary sleep-inhibit locks needed anymore.

## Key scripts (`07_CAPTURE_TOOLS/`)
- `check_coverage.py` + `sources.json` — pre-flight coverage verifier (NEW).
- `johnson_1773_scraper.py` — core scraper (`lookup_word_1773`), captures 1773 rows.
- `missed_words_driver.py` — direct lookup + root-retry driver.
- `headword_check.py` (Safeguard 1) — flags wrong-entry captures; `root_retry.py` (Safeguard 2) — recovers inflected forms via their root.
- `process_1773.py` / `process_missed_words.py` / `process_vocab_expansion.py` / `process_vocab_round2.py` — merge results into the library (each loads the correct base snapshot).

## App wiring
- The GUI research pipeline (`01_APP/pipeline_runner.py` Step 4) draws plain-English definitions from this library first (via `01_APP/veritas_definitions.py`), falling back to `01_APP/literal_dictionary.py`.
- Step 3 term-finding (`document_processor.find_constitutional_terms`) now also treats every VERITAS headword as an eligible term.
- App launch: `cd 01_APP && source .venv/bin/activate && python3 run.py`.

## Constraint to respect
Johnson's site (johnsonsdictionaryonline.com) **explicitly prohibits systematic bulk download** and is non-commercial-only. Continue only bounded, respectful, per-word research batches (1.5s delay). Do NOT set up a full-dictionary (~42k) harvest. Full-Johnson would require a licensed dataset from LEME/UCF. Etymonline is off-limits for scraping (ToS); use bulk-legal sources (Wiktionary/Webster/WordNet dumps) instead.

## Optional next steps (nothing is blocking)
1. Wire `wiktionary` / `wordnet` into the coverage checker.
2. Pull Webster/Wiktionary definitions for WORTH-CAPTURING words into provenance-tagged secondary fields.
3. Manual lookup of the 3 headword-mismatch words (`began, eve, hidden`).
