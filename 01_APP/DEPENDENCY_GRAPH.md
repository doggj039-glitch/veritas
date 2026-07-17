# VERITAS — Dependency Graph

## Runtime Module Dependencies

```
main.py
├── config.py
├── pipeline_runner.py
│   ├── corpus_index.py        (stdlib only: sqlite3, hashlib, re, json, pathlib)
│   ├── gap_log.py             (stdlib only: json, uuid, datetime, pathlib)
│   ├── citation_graph.py
│   │   ├── corpus_index.py
│   │   └── gap_log.py
│   ├── source_verifier.py     (stdlib only: sqlite3, hashlib, re, json, urllib)
│   ├── report_generator.py
│   │   └── privacy_scrubber.py
│   └── phone_contract.py      (stdlib only: hashlib, json, os, datetime, pathlib)
├── report_generator.py
│   └── privacy_scrubber.py
├── ai_integration.py          (requests)
├── document_processor.py      (pypdf, python-docx)
├── legal_dictionary.py        (stdlib only)
├── literal_dictionary.py      (stdlib only)
├── consistency_engine.py      (stdlib only; faster-whisper optional)
├── privacy_scrubber.py        (stdlib only)
└── metadata_stripper.py       (Pillow; mutagen optional)
```

## Third-Party Package Requirements

| Package | Required By | Required? |
|---------|------------|-----------|
| pypdf | document_processor | ✓ Required |
| python-docx | document_processor | ✓ Required |
| Pillow | metadata_stripper | ✓ Required |
| requests | ai_integration | ✓ Required |
| openpyxl | (future use) | Optional |
| lxml | (future use) | Optional |
| mutagen | metadata_stripper | Optional |
| faster-whisper | consistency_engine | Optional |
| google-generativeai | ai_integration | Optional |
