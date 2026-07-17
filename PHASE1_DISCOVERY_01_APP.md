# VERITAS Desktop App — Phase 1 Discovery (Read-Only Analysis)

**Scope:** `/home/noneya/Projects/VERITAS v.3/01_APP` — the Python/Tkinter desktop application.
**Method:** static analysis (AST inventory + widget/callback extraction + existing project docs). **No files modified.**
**Excluded from detail:** `.venv/`, `archive/`, `*.BACKUP*`, `test_*.py` (noted separately), and the three large data-only modules.

---

## 1. PROJECT ARCHITECTURE

**Entry point:** `run.py` → `from main import main; main()` → `LegalAnalyzerApp(tk.Tk())`.

**Three clean layers (this is the key finding for conversion):**

| Layer | Files | Tkinter? |
|---|---|---|
| **UI** | `main.py` (1,745 LOC, one class `LegalAnalyzerApp`) | YES — the *only* module that imports `tkinter` |
| **Application logic (backend)** | `pipeline_runner`, `report_generator`, `corpus_index`, `gap_log`, `citation_graph`, `source_verifier`, `phone_contract`, `ai_integration`, `document_processor`, `consistency_engine`, `privacy_scrubber`, `metadata_stripper`, `veritas_definitions`, `config` | NO — all headless, import only stdlib + each other |
| **Data** | `literal_dictionary` (2,637 LOC), `legal_dictionary` (396), `historical_context_library` (1,007) — module-level dicts | NO |

**Consequence:** the backend is already a UI-agnostic library. A conversion replaces `main.py` and reuses everything else nearly as-is. The one caveat (see §6) is that a few *analysis functions live inside the UI class* and must be extracted.

**Runtime data (auto-created):** `corpus/{primary,secondary,index}`, `corpus/index/corpus.db` (SQLite FTS5), `corpus/index/source_verifier.db`, `reports/<timestamp>_<slug>/`.
**External data:** `config.VERITAS_DEFINITIONS_PATH` → `../03_LIBRARIES/VERITAS_definitions_library.json` — the same 1773 library the Blackletter gate uses. The app's "Define the Drift" feature reads its per-word timelines.

---

## 2. FUNCTION INVENTORY (application logic modules)

### `config.py` — constants only
Thresholds, `APP_TITLE/VERSION`, `WINDOW_WIDTH=1400/HEIGHT=900`, corpus/report paths, `VERITAS_DEFINITIONS_PATH`, `CITATION_MAX_HOPS=3`, `RESEARCH_SEARCH_LIMIT=20`, `SPECIFIC_FLAGS`.

### `pipeline_runner.py` — `PipelineRunner` (the 12-step research engine)
- `run(question, doc_text, doc_metadata)` — executes the full pipeline
- `save_report(result, reports_dir)`
- `_restate` (step 2), `_identify_terms` (3), `_define_terms` (4), `_search_corpus` (5–6), `_follow_citations` (7–8), `_detect_drift` (9), `_render_html`
- helpers: `_import_*` (lazy imports), `_now_iso`, `_sha256`, `_safe_get`

### `report_generator.py` — `ReportGenerator`
- `generate_html_report`, `generate_text_report` (document analysis)
- `generate_research_html`, `generate_research_text` (pipeline research map)

### `corpus_index.py` — `CorpusIndex` (SQLite FTS5)
- `ingest`, `search`, `resolve`, `list_all`, `rebuild`, `close`, context-manager; helpers `_extract_text/_extract_citations/_extract_self_cite`

### `gap_log.py` — `GapLog`
- `add`, `all`, `by_type`, `clear`, `to_json`/`from_json`, `save`/`load`, `__len__/__bool__`

### `citation_graph.py` — `CitationGraph`
- `add_citation`, `forward`, `reverse`, `has_citation`, `all_nodes`, `all_edges`, `follow(seed_ids, corpus_index, gap_log, max_hops)`; helper `_extract_citation_strings`

### `source_verifier.py` — `SourceVerifier` (SQLite cache)
- `classify_document`, `extract_case_identity`, `suggest_verification_link`, `needs_reverification`, `verify_document`, `mark_audit_due`, `verification_report`; helpers `_detect_provider` etc.

### `phone_contract.py` — `PhoneContract`
- `validate_package`, `write_manifest`, `read_manifest`, `package_summary`, `_count_from_files` — the report-package/manifest contract (built for a phone/Android viewer)

### `ai_integration.py` — `AIIntegration` (OpenAI + Gemini)
- provider plumbing: `_call_api/_call_openai/_call_gemini`, `_build_openai_payload`, reasoning-model handling
- features: `verify_findings`, `verify_legal_terms`, `detect_deflection`, `validate_cross_references`, `generate_summary`, `ask_custom_question`, `get_usage_stats`, `is_configured`

### `document_processor.py` — `DocumentProcessor`
- `load_document`, `_detect_format`, `_extract_pdf`, `extract_all_text` (built for Android load integration)
- analysis: `find_legal_citations`, `find_key_legal_terms`, `find_constitutional_terms` (reads the VERITAS library headwords), `get_statistics`
- module helpers: `_normalize_extracted_text`, `_split_sentences`, `_split_paragraphs`, `_extract_text/_extract_docx/_extract_rtf`

### `consistency_engine.py` — `ConsistencyEngine`
- `analyze_av_against_witness`, `_probe_media` (ffprobe), `_transcribe_media_file` (whisper/faster-whisper optional), `_compare_witness_to_transcript`, `_assess_perjury_risk`

### `veritas_definitions.py` — the bridge to the 1773 library
- `load_veritas_definitions`, `load_veritas_timelines`, `get_timeline(word)`, `has_drift(word)` — powers the "Define the Drift" UI

### `privacy_scrubber.py` — `scrub_party_identifiers(value)`
### `metadata_stripper.py` — `MetadataStripper`: `strip_image_metadata`, `strip_media_tags`, `strip_file`

---

## 3. UI INVENTORY (`main.py` → `LegalAnalyzerApp`, 63 methods)

**Window:** single `tk.Tk`, 1400×900, `ttk.Style` theming, a `Canvas` background image (brand asset), left control panel + right `PanedWindow` content.

**Menu bar (5 `Menu`, 4 cascades, 9 commands):**
- **File:** Open Document… · Paste Text… · Export HTML Report… · Export Text Report… · Exit
- **Tools:** Legal Dictionary Lookup… · AI Ask a Question…
- **Settings:** API Keys…
- **Help:** About

**Main `Notebook` — 6 tabs** (each built by a `_build_*_tab`):
1. **📄 Document** — load/paste, statistics, highlighted text view
2. **📖 Terminology** — `Treeview` of flagged terms + detail
3. **🚫 Deflection** — `Treeview` of deflection/ambiguity patterns
4. **🤖 AI Analysis** — AI verify/ask, status indicator
5. **📕 Dictionary** — searchable dictionary `Treeview` (literal + legal + VERITAS)
6. **🔬 VERITAS** — the research pipeline tab (question → research map → Define the Drift → save/export)

**Widget census (instantiations):** Button ×26, Label ×25, Frame ×22, LabelFrame ×11, Entry ×7, Menu ×5, Separator ×4, Treeview ×3, Toplevel ×3, Notebook ×2, Progressbar ×2, Combobox ×2, Radiobutton ×2, Canvas ×1, PanedWindow ×1, plus 12 `StringVar`.

**Dialogs (`Toplevel`/modal):**
- `_settings_dialog` (API Keys) · `_ai_question_dialog` · `_open_drift_window` ("Define the Drift" timeline) · `_dict_lookup_dialog` · `_paste_text` · `_about_dialog`
- `messagebox`: showwarning ×10, showinfo ×6, showerror ×6, askyesno ×1
- `filedialog`: askopenfilename ×1, asksaveasfilename ×3

**Event bindings (9):** `<<NotebookTabChanged>>`, `<<TreeviewSelect>>`, `<Configure>` (bg resize), `<Escape>`, `<Return>`.

**Callbacks:** 35 `command=` wirings (buttons/menus → methods).

**Concurrency:** 3 `threading.Thread` — long-running work (full analysis, research pipeline, AI calls) runs off the UI thread; results marshalled back to widgets.

**Workflows (data flow):**
1. **Load** → `_open_document`/`_paste_text` → `DocumentProcessor.load_document` → text + stats.
2. **Auto full analysis** → `_autorun_full_analysis` → `_run_full_analysis` (thread) → terminology + deflection analysis → populate trees + `_highlight_document`.
3. **AI** → `_ai_verify_specific`/`_ai_ask` (thread) → `AIIntegration.*` → `_display_ai_result`.
4. **Dictionary** → `_search_dictionary`/`_quick_dict_lookup` → literal/legal/`veritas_definitions`.
5. **Research** → `_run_research` (thread) → `PipelineRunner.run` → `_display_research_result` → `_open_drift_window` (timelines) → `_save_research_report`/`_open_research_html`/`_export_research_text` (`ReportGenerator`).

---

## 4. DEPENDENCY MAP

**Third-party (required):** `pypdf`, `python-docx` (document_processor); `Pillow` (metadata_stripper + UI background); `requests` (ai_integration).
**Optional:** `mutagen`, `faster-whisper`, `google-generativeai`; **declared/future:** `openpyxl`, `lxml`; **testing:** `pytest`.
**Stdlib in play:** `tkinter`, `sqlite3`, `threading`, `urllib`, `hashlib`, `json`, `re`, `pathlib`, `datetime`, `ctypes` (Windows DPI), `webbrowser`, `zipfile`, `subprocess`/`tempfile` (consistency_engine).

**Runtime module graph (from `DEPENDENCY_GRAPH.md`, confirmed against imports):**
```
main.py → config, pipeline_runner, report_generator, ai_integration,
          document_processor, legal_dictionary, literal_dictionary,
          privacy_scrubber, veritas_definitions
pipeline_runner → corpus_index, gap_log, citation_graph, source_verifier,
                  report_generator, phone_contract, consistency_engine,
                  document_processor, ai_integration, {literal,legal,historical} dicts,
                  veritas_definitions, config
citation_graph → corpus_index, gap_log
report_generator → privacy_scrubber
```
**Cross-project link:** `config.VERITAS_DEFINITIONS_PATH` → `../03_LIBRARIES/VERITAS_definitions_library.json` (shared with the Blackletter gate).

---

## 5. BACKEND MAP (UI-agnostic application logic)

Every module in §2 is importable and runnable **without Tkinter**. Grouped by role:

- **Ingestion/parsing:** `document_processor` (+ `metadata_stripper`, `privacy_scrubber`)
- **Corpus & retrieval:** `corpus_index` (FTS5), `citation_graph`, `gap_log`
- **Verification:** `source_verifier`, `phone_contract`
- **Reasoning:** `pipeline_runner` (orchestrator), `veritas_definitions`, dictionaries, `consistency_engine`
- **AI:** `ai_integration`
- **Output:** `report_generator` (HTML/text), `pipeline_runner.save_report`
- **Config:** `config`

**Primary backend API surface (what a new front end calls):**
`PipelineRunner.run(question, doc_text, doc_metadata) → research dict`; `DocumentProcessor.load_document(path) → {text, metadata}`; `AIIntegration.*`; `ReportGenerator.generate_*`; `veritas_definitions.get_timeline/has_drift`. These five are the whole app's logic.

**Tests (already exist, backend is covered):** `test_corpus_index` (21), `test_gap_log` (68), `test_citation_graph` (67), `test_source_verifier` (80), `test_pipeline_runner` (54), `test_report_generator` (56), `test_phone_contract` (55). **No UI tests** — consistent with UI/logic separation.

---

## 6. UI-ONLY vs APPLICATION-LOGIC CLASSIFICATION

**Pure UI (rebuild for any new front end) — `main.py` methods:**
`_load_brand_assets, _build_background, _refresh_background_image, _build_styles, _build_ui, _build_*_panel, _build_view_nav, _select_view, _sync_view_nav, _build_*_tab (×6), _populate_term_tree, _populate_defl_tree, _populate_dictionary_tree, _on_term_select, _on_dict_select, _highlight_document, _update_ai_status, _display_ai_result, _display_ai_error, _display_research_result, _display_research_error, _open_drift_window, _settings_dialog, _ai_question_dialog, _dict_lookup_dialog, _paste_text, _about_dialog, _on_close, all _export_/_save_/_open_* file-dialog wrappers.`

**Orchestration (thread + backend call + marshal to UI — reshape, don't delete):**
`_run_full_analysis, _run_terminology, _run_deflection, _run_research, _run_ai_verify, _ai_verify_specific, _ai_ask, _autorun_full_analysis, _open_document.`

**⚠ Application logic *trapped inside the UI class* (MUST be extracted before/at conversion):**
`_do_terminology_analysis, _do_deflection_analysis, _clean_flag_phrase, _is_context_only_phrase, _find_phrase_matches, _collect_issue_snippets, _add_issue, _results_for_display`, and module fn `_normalize_legal_term`. These operate on text/dictionaries, not widgets — they belong in a backend module (e.g. a new `analysis_engine.py`). This is the only place the clean layering leaks.

---

## 7. CONVERSION PLAN

**Target not yet fixed.** The codebase leans web/mobile (pipeline already emits HTML; `phone_contract` + `extract_all_text` "for Android load integration"; the VERITAS POC HTMLs). The plan below is target-agnostic through step 3, then branches.

**Step 0 — Decide the target.** Options: (a) **Web app** — FastAPI/Flask backend wrapping the existing modules + an HTML/JS front end (best fit; reuses HTML report generation and the POCs); (b) **Electron/Tauri** desktop; (c) **Mobile** (the phone_contract hints). Recommendation: **(a) web**, because the backend is already headless and the report layer is already HTML.

**Step 1 — Extract trapped logic (no behavior change).** Move the §6 ⚠ analysis functions out of `LegalAnalyzerApp` into a new headless `analysis_engine.py`; have `main.py` call it. This makes the UI 100% separable and is the only real refactor. Guard with the existing test pattern.

**Step 2 — Define the backend API/service boundary.** Wrap the five API surfaces (§5) behind a thin service layer: `load_document`, `run_full_analysis(text)`, `run_research(question, text)`, `ai_*`, `dictionary_lookup`, `get_drift(word)`, `export_report`. Everything already returns plain dicts/JSON — minimal work.

**Step 3 — Preserve the async contract.** The 3 threads become async endpoints / web-workers / status callbacks. The pipeline already exposes a status callback (`_on_pipeline_status(step, total, message)`) — reuse it for progress streaming.

**Step 4 (branch) — Rebuild the front end** for the chosen target, mapping 1:1 from §3:
- 6 tabs → 6 routes/views; menus → nav/actions; 3 Treeviews → tables/lists; the "Define the Drift" Toplevel → a modal/timeline component; file dialogs → uploads/downloads; `messagebox` → toasts/alerts.

**Step 5 — Port outputs & data.** `report_generator` HTML is reusable directly; keep `reports/<timestamp>_<slug>/` package + `phone_contract` manifest as the artifact contract; SQLite dbs port unchanged.

**Step 6 — Verify.** Backend tests already exist and stay green (logic unchanged). Add thin front-end/integration tests for the new UI only.

**Effort estimate:** backend reuse ~90%; real work is Step 1 (small refactor) + Step 4 (new UI). The clean separation means this is a **re-skin, not a rewrite.**

---
*End of Phase 1 discovery. Stopping here as instructed — no changes made, awaiting go-ahead for the next phase.*
