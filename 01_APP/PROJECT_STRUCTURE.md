# VERITAS — Project Structure

```
veritas/
│
├── main.py                    # Desktop app entry point (Tkinter UI)
├── run.py                     # Launcher script
├── config.py                  # All configuration settings
│
├── VERITAS MODULES
├── corpus_index.py            # Phase 1 — SQLite FTS5 corpus index
├── gap_log.py                 # Phase 2 — Research gap logging
├── citation_graph.py          # Phase 3 — Citation graph & follow
├── source_verifier.py         # Phase 3.5 — Source verification cache
├── pipeline_runner.py         # Phase 4 — 12-step research pipeline
├── report_generator.py        # Phase 5 — HTML + text report generation
├── phone_contract.py          # Phase 6 — Phone viewer data contract
│
├── PHOENIX BASE MODULES
├── ai_integration.py          # AI provider integration
├── document_processor.py      # PDF/DOCX/TXT loading and parsing
├── legal_dictionary.py        # Legal term definitions
├── literal_dictionary.py      # Plain-English definitions
├── consistency_engine.py      # Statement consistency checking
├── privacy_scrubber.py        # PII removal from exports
├── metadata_stripper.py       # Media metadata removal
│
├── TESTS (one per module)
├── test_corpus_index.py       # 21 checks
├── test_gap_log.py            # 68 checks
├── test_citation_graph.py     # 67 checks
├── test_source_verifier.py    # 80 checks
├── test_pipeline_runner.py    # 54 checks
├── test_report_generator.py   # 56 checks
├── test_phone_contract.py     # 55 checks
│
├── DATA FOLDERS (created at runtime)
├── corpus/
│   ├── primary/               # Drop primary sources here (PDFs, TXT, DOCX)
│   ├── secondary/             # Drop secondary sources here
│   └── index/
│       ├── corpus.db          # SQLite FTS5 index (auto-created)
│       └── source_verifier.db # Verification cache (auto-created)
├── reports/                   # Saved research reports (auto-created)
│   └── <timestamp>_<slug>/
│       ├── report.json
│       ├── gap_log.json
│       ├── source_list.json
│       ├── report.html
│       ├── report.txt
│       └── manifest.json
│
├── DOCUMENTATION
├── README.md
├── INSTALL_LINUX.md
├── requirements.txt
├── PROJECT_STRUCTURE.md
├── DEPENDENCY_GRAPH.md
├── IMPORT_GRAPH.md
├── CHANGELOG.md
│
└── archive/                   # Superseded duplicate files (not runtime)
    ├── corpus_index-1.py
    ├── source_verifier-1.py
    ├── pipeline_runner-v1.py
    ├── pipeline_runner-v2.py
    ├── main-v1.py
    ├── test_corpus_index-1.py
    └── test_source_verifier-1.py
```
