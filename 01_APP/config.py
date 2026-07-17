# Copyright (c) contributors. Licensed under the Apache License, Version 2.0.
"""
Configuration for the Document Analyzer / VERITAS Research Engine
"""

import os

# Analysis thresholds
MIN_KEYWORD_MATCH = 1
CONFIDENCE_THRESHOLDS = {
    "high": 0.75,
    "medium": 0.50,
    "low": 0.25
}

# Application Settings
APP_TITLE = "VERITAS"
APP_VERSION = "1.0.0"
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900

# User-specific focus sections (Set to empty list to analyze the entire document)
FOCUS_SECTIONS = []

# Specific User Flags
SPECIFIC_FLAGS = {
    "lack_of_photos": {
        "patterns": [r'\black\s+of\s+(?:photos?|photographs?|images?|pictures?)\b', r'\bno\s+(?:photos?|photographs?|images?|pictures?)\s+(?:taken|available|provided)\b'],
        "label": "Lack of Photos",
        "description": "The document indicates a lack of photographic evidence, which may affect the reliability of observations or searches."
    }
}

# ── VERITAS Research Engine Settings ──────────────────────────────────────────

# Base directory (resolved at runtime)
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Corpus paths
CORPUS_DIR         = os.path.join(_BASE_DIR, "corpus")
CORPUS_PRIMARY_DIR = os.path.join(CORPUS_DIR, "primary")
CORPUS_SECONDARY_DIR = os.path.join(CORPUS_DIR, "secondary")
CORPUS_INDEX_DIR   = os.path.join(CORPUS_DIR, "index")
CORPUS_DB_PATH     = os.path.join(CORPUS_INDEX_DIR, "corpus.db")
VERIFIER_DB_PATH   = os.path.join(CORPUS_INDEX_DIR, "source_verifier.db")

# Reports output path
REPORTS_DIR = os.path.join(_BASE_DIR, "reports")

# VERITAS definitions library (founding-era plain meaning: Johnson 1755/1773 +
# Bailey 1721). Curated/verified store shared with the Blackletter gate; lives
# one level up in 03_LIBRARIES. The pipeline prefers this over the app's local
# literal_dictionary for plain-English definitions.
VERITAS_DEFINITIONS_PATH = os.path.join(
    _BASE_DIR, "..", "03_LIBRARIES", "VERITAS_definitions_library.json"
)

# Citation graph settings
CITATION_MAX_HOPS = 3   # Maximum recursive citation-following depth

# Research pipeline settings
RESEARCH_SEARCH_LIMIT = 20   # Max corpus search results per query
