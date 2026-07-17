# VERITAS — Linux Installation Guide
# Tested on Linux Mint / Ubuntu 22.04+

## 1. System Requirements

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv python3-tk
```

## 2. Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install Dependencies

```bash
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Run the App

```bash
python3 run.py
```

Or directly:

```bash
python3 main.py
```

## 5. Run Tests

```bash
python3 -m pytest
```

Or individually:

```bash
python3 test_corpus_index.py
python3 test_gap_log.py
python3 test_citation_graph.py
python3 test_source_verifier.py
python3 test_pipeline_runner.py
python3 test_report_generator.py
python3 test_phone_contract.py
```

## 6. Verify Installation

```bash
python3 -c "import main; print('OK')"
```

## Optional Packages

| Package | Purpose | Install |
|---------|---------|---------|
| mutagen | Audio/video metadata stripping | `pip install mutagen` |
| faster-whisper | Audio transcription | `pip install faster-whisper` |
| google-generativeai | Google Gemini AI | `pip install google-generativeai` |

The app runs without these — configure via Settings menu.
