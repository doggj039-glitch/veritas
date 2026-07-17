# VERITAS
## Constitutional Research Engine

VERITAS is a desktop-first legal research tool that produces traceable,
sourced research maps from a local corpus of documents. It runs entirely
offline — no internet required for analysis.

---

## Quick Start (Linux)

```bash
# 1. Install system dependencies
sudo apt install python3 python3-pip python3-venv python3-tk

# 2. Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Run
python3 run.py
```

See [INSTALL_LINUX.md](INSTALL_LINUX.md) for full installation instructions.

---

## What It Does

1. Load a document or type a research question
2. Click **🔬 Run Research**
3. The 12-step pipeline runs automatically:
   - Restates your question in plain English
   - Identifies and defines key legal terms
   - Searches your local corpus
   - Follows citation chains recursively
   - Detects semantic drift across sources
   - Logs all unresolved gaps
4. Results appear in the **Research Map** tab
5. Save as HTML, text, or JSON — or open in browser

---

## Adding Documents to the Corpus

Drop files into:
- `corpus/primary/` — constitutional texts, statutes, judgments
- `corpus/secondary/` — commentary, summaries, articles

Supported formats: `.pdf`, `.docx`, `.txt`

**Important:** For reliable citation resolution, documents should include
their canonical citation in the header:

```
Evidence Act
Citation: [1991] EVA 1

Section 12 — Admissibility...
```

---

## Project Structure

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)

## Dependencies

See [DEPENDENCY_GRAPH.md](DEPENDENCY_GRAPH.md)

---

## Disclaimer

**RESEARCH AND STATISTICS TOOL ONLY — NOT LEGAL ADVICE — VERIFY ALL RESULTS.**

This tool is for research assistance only. All findings must be independently
verified by a qualified legal professional.
