# VERITAS — Changelog

## Recovery Build — June 2026

### Fixed
- `document_processor.py`: Updated `PyPDF2` import to `pypdf` (PyPDF2 is
  deprecated; pypdf is the maintained successor).
- `metadata_stripper.py`: Made `mutagen` import optional with graceful
  fallback so app starts without it installed.
- `consistency_engine.py`: `faster-whisper` and `whisper` imports are already
  inside try/except blocks — confirmed optional, no change needed.

### Organised
- Renamed canonical files from numbered duplicates:
  - `citation_graph-1.py`  → `citation_graph.py`
  - `corpus_index-2.py`    → `corpus_index.py`
  - `gap_log-1.py`         → `gap_log.py`
  - `source_verifier-2.py` → `source_verifier.py`
  - `pipeline_runner (2).py` → `pipeline_runner.py`
  - `main (1).py`           → `main.py`
- Archived superseded duplicates to `archive/`
- Recovered Phoenix base modules from `phoenix_neutral_source.zip`

### Added
- `requirements.txt` — clean, no deprecated packages
- `README.md`
- `INSTALL_LINUX.md`
- `PROJECT_STRUCTURE.md`
- `DEPENDENCY_GRAPH.md`
- `IMPORT_GRAPH.md`
- `CHANGELOG.md`

## Phase History

| Phase | Module | Tests |
|-------|--------|-------|
| 1 | corpus_index.py | 21/21 |
| 2 | gap_log.py | 68/68 |
| 3 | citation_graph.py | 67/67 |
| 3.5 | source_verifier.py | 80/80 |
| 4 | pipeline_runner.py + main.py + config.py | 54/54 |
| 5 | report_generator.py | 56/56 |
| 6 | phone_contract.py | 55/55 |

**Total: 401/401 checks passing**
