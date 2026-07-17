# Copyright (c) contributors. Licensed under the Apache License, Version 2.0.
"""
VERITAS Definitions Loader
==========================

Exposes the shared VERITAS definitions library
(03_LIBRARIES/VERITAS_definitions_library.json) to the app in the SAME shape the
pipeline already expects from literal_dictionary.LITERAL_DICTIONARY, i.e.:

    {word_lower: {"definition": str, "source": str, "etymology": str}}

This is the curated, verified/adopted founding-era store (Johnson 1755/1773 with
Nathan Bailey 1721 as fallback) that the Blackletter gate uses. Wiring the GUI to
it lets the research pipeline draw plain-English meanings from the same sourced
library rather than only the app's local literal_dictionary.

Read-only: this loader never writes to or alters the library. The definition
text is used verbatim as stored (nothing reworded here).
"""

import json
import os

try:
    from config import VERITAS_DEFINITIONS_PATH as _CFG_PATH
except Exception:
    _CFG_PATH = None


def _default_path():
    if _CFG_PATH:
        return _CFG_PATH
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "03_LIBRARIES", "VERITAS_definitions_library.json",
    )


def load_veritas_definitions(path=None):
    """Load the library and return a word -> {definition, source, etymology}
    mapping. Returns an empty dict (never raises) if the file is missing or
    unreadable, so the pipeline simply falls back to its other sources."""
    path = path or _default_path()
    out = {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return out

    for entry in data.get("entries", []):
        word = str(entry.get("word", "")).strip().lower()
        if not word or word in out:
            continue
        # Prefer the entry's definition; fall back to normalized_text for newly
        # added 1773 entries. Both are verbatim site/source transcription.
        definition = entry.get("definition") or entry.get("normalized_text") or ""
        if not definition:
            continue

        year = entry.get("year")
        src_name = entry.get("source") or "Johnson's Dictionary"
        provenance = f"{src_name} {year}" if year else src_name
        out[word] = {
            "definition": definition,
            "source": f"VERITAS Definitions Library ({provenance})",
            "etymology": entry.get("etymology", "") or "",
            "verification_status": entry.get("verification_status", ""),
        }
    return out


def load_veritas_timelines(path=None):
    """Load the per-word drift timeline: word -> ordered list of source snapshots
    (the entry['sources'] array; baseline triad seq 0-2 + drift seq 3+ in
    publication order). Returns {} if the file is missing or pre-timeline. See
    VERITAS_DESIGN.md. Read-only; verbatim text passed through untouched."""
    path = path or _default_path()
    out = {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return out
    for entry in data.get("entries", []):
        word = str(entry.get("word", "")).strip().lower()
        srcs = entry.get("sources")
        if word and srcs and word not in out:
            out[word] = srcs
    return out


# Loaded once at import, mirroring how LITERAL_DICTIONARY is a module-level dict.
VERITAS_DEFINITIONS = load_veritas_definitions()
VERITAS_TIMELINES = load_veritas_timelines()


def get_timeline(word):
    """Return the ordered source timeline for a word, or [] if none."""
    return VERITAS_TIMELINES.get(str(word).strip().lower(), [])


def has_drift(word):
    """True if the word has at least one drift snapshot (a later authority beyond
    the founding-era baseline) -- i.e. there is drift worth defining."""
    return any(s.get("tier") == "drift" for s in get_timeline(word))


if __name__ == "__main__":
    d = VERITAS_DEFINITIONS
    print(f"Loaded {len(d)} VERITAS definitions from {_default_path()}")
    for w in ("senate", "jury", "freedom", "commerce", "treason"):
        e = d.get(w)
        if e:
            print(f"  {w}: [{e['verification_status']}] {e['definition'][:70]!r}")
        else:
            print(f"  {w}: (not in library)")
