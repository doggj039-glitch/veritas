"""
VERITAS Libraries Module  —  now with the Grammarian (the resolver / gate)
==========================================================================

This file gives VERITAS access to three reference layers and, on top of
them, ONE gate that the rest of the system asks before it is allowed to
use a word.

  1. THE DEFINITIONS LIBRARY  (the controlling layer)
     Plain, ordinary-meaning definitions from Samuel Johnson's 1755
     dictionary and Nathan Bailey's 1721 dictionary. This answers:
     "What did this word plainly mean at the time?"  This is the layer
     that CONTROLS. If a word is not here, it is not sourced.

  2. THE ETYMOLOGY DICTIONARY  (corroboration only)
     Root meanings from ODEE (Onions 1966), the OED, Bosworth-Toller,
     and Lewis & Short. This answers: "Where did the word come from?"
     It supports a definition. It never overrides one.

  3. THE HISTORICAL CONTEXT LIBRARY  (corroboration only)
     Drafting records, ratification debates, and early legal commentary
     (Farrand, Madison, the Federalist and Anti-Federalist Papers,
     Elliot's Debates, Story, Blackstone, and the Annals of Congress).
     This answers: "What did people mean by the word when they used it?"
     It supports a definition. It never overrides one.

--------------------------------------------------------------------
THE GATE  (this is the new part)
--------------------------------------------------------------------

The one method that matters for the governance layer is:

    from veritas_libraries import VeritasLibraries
    libraries = VeritasLibraries()

    result = libraries.resolve("senate")

'resolve' does not just look a word up. It decides, in a fixed order
that never changes, whether the word has a CONTROLLING definition:

    1. Founding-era dictionary meaning (Johnson 1755 / Bailey 1721) -- CONTROLS
    2. Etymological root -------------------------------------------- corroborates
    3. Historical context / intent --------------------------------- corroborates
    4. Modern meaning ---------------------------------------------- reference only, never controls

If a controlling definition is found, the word is 'resolved' and the
other layers are attached as labeled corroboration -- never blended in.

If NO controlling definition is found, the word is returned as
'void-for-vagueness'. It does not guess. A rule that depends on that
word must halt on it until the word is sourced. That halt is the whole
point: it is how the system refuses to give an answer it cannot back up.

Keep this file in the same folder as its three data files:

    VERITAS_definitions_library.json
    VERITAS_historical_context_library.json
    etymology_dictionary.py
"""

import json
import os
import importlib.util


class VeritasLibraries:
    """
    Loads the three VERITAS reference layers and exposes the resolver
    (the Grammarian / gate) on top of them.
    """

    # The fixed resolution order. This is written down on purpose so that
    # anyone can see it and so it can never quietly change.
    RESOLUTION_ORDER = [
        "1. Founding-era dictionary (Johnson 1755 / Bailey 1721) -- CONTROLS",
        "2. Etymological root (ODEE, OED, Bosworth-Toller, Lewis & Short) -- corroborates",
        "3. Historical context & intent (Federalist, Farrand, Blackstone, ...) -- corroborates",
        "4. Modern meaning -- reference only, never controls",
    ]

    def __init__(self, folder_path=None):
        if folder_path is None:
            folder_path = os.path.dirname(os.path.abspath(__file__))
        self.folder_path = folder_path

        definitions_file = os.path.join(folder_path, "VERITAS_definitions_library.json")
        context_file = os.path.join(folder_path, "VERITAS_historical_context_library.json")

        self.definitions_data = self._load_json_file(definitions_file)
        self.context_data = self._load_json_file(context_file)
        self._etymology = self._load_etymology(folder_path)

        self._definitions_index = self._build_definitions_index()
        self._context_index = self._build_context_index()

    # ------------------------------------------------------------
    # LOADING
    # ------------------------------------------------------------

    def _load_json_file(self, path):
        """Reads a .json data file. Returns a flagged empty structure
        instead of crashing if the file cannot be found or read."""
        if not os.path.exists(path):
            return {"_load_error": f"Could not find file: {path}", "entries": []}
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as error:
            return {"_load_error": f"Could not read file {path}: {error}", "entries": []}

    def _load_etymology(self, folder_path):
        """Loads the etymology dictionary (a Python file). Returns an
        empty table (not a crash) if it is missing or unreadable, so the
        gate still works on the two JSON layers alone."""
        path = os.path.join(folder_path, "etymology_dictionary.py")
        if not os.path.exists(path):
            self._etymology_error = f"Could not find file: {path}"
            return {}
        try:
            spec = importlib.util.spec_from_file_location("etymology_dictionary", path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            data = getattr(module, "ETYMOLOGY_DICTIONARY", {})
            self._etymology_error = None
            return {str(k).strip().lower(): v for k, v in data.items()}
        except Exception as error:
            self._etymology_error = f"Could not read etymology file: {error}"
            return {}

    def _build_definitions_index(self):
        """Builds a word -> entry lookup for the Definitions Library."""
        index = {}
        for entry in self.definitions_data.get("entries", []):
            word = entry.get("word", "").strip().lower()
            if word:
                index.setdefault(word, []).append(entry)
        return index

    def _build_context_index(self):
        """Builds a word -> note lookup for the Historical Context Library."""
        index = {}
        notes_section = self.context_data.get("word_in_use_notes", {})
        if isinstance(notes_section, dict):
            for entry in notes_section.get("entries", []):
                word = entry.get("word", "").strip().lower()
                if word:
                    index.setdefault(word, []).append(entry)
        return index

    # ------------------------------------------------------------
    # THE GATE  --  the Grammarian
    # ------------------------------------------------------------

    def resolve(self, word):
        """
        The gate. Given a word, decide whether it has a CONTROLLING
        founding-era definition, and attach every other layer as labeled
        corroboration. If nothing controls, return Void for Vagueness so
        the calling rule halts on this word instead of guessing.
        """
        word_key = word.strip().lower()
        trace = []

        # --- LAYER 1 (controlling): founding-era dictionary meaning ---
        dict_matches = self._definitions_index.get(word_key, [])
        controlling = None
        if dict_matches:
            entry = dict_matches[0]
            controlling = {
                "definition": entry.get("definition", ""),
                "etymology_note_from_dictionary": entry.get("etymology", ""),
                "tier": entry.get("tier"),
                "source": "Definitions Library (Johnson's 1755 / Bailey's 1721)",
                # Honest flag: the per-entry data does not yet say WHICH of the
                # two dictionaries this came from. Not invented here.
                "which_dictionary_recorded": False,
            }
            trace.append(
                f"LAYER 1 (controls): '{word_key}' found in the founding-era Definitions Library."
            )
        else:
            trace.append(
                f"LAYER 1 (controls): '{word_key}' has NO founding-era dictionary definition."
            )

        # --- LAYER 2 (corroboration): etymological root ---
        etymology = self._etymology.get(word_key)
        if etymology:
            trace.append("LAYER 2 (corroborates): etymological root available.")

        # --- LAYER 3 (corroboration): historical context / intent ---
        context = self._context_index.get(word_key, [])
        if context:
            trace.append("LAYER 3 (corroborates): historical-context note available.")

        # --- disposition ---
        if controlling:
            status = "resolved"
            trace.append("DISPOSITION: resolved -- a controlling definition governs this word.")
        else:
            status = "void-for-vagueness"
            trace.append(
                "DISPOSITION: Void for Vagueness -- no controlling source. "
                "Any rule that depends on this word must HALT until it is sourced."
            )

        return {
            "word": word,
            "status": status,                     # "resolved" or "void-for-vagueness"
            "controlling": controlling,           # None when void for vagueness
            "corroboration": {
                "etymology": etymology,           # None when absent -- never controls
                "historical_context": context,    # [] when absent -- never controls
            },
            "resolution_order": self.RESOLUTION_ORDER,
            "trace": trace,
        }

    def is_sourced(self, word):
        """The one-line gate check a rule calls before it is allowed to
        use a word. True only if a controlling definition exists."""
        return self.resolve(word)["status"] == "resolved"

    # ------------------------------------------------------------
    # PLAIN LOOKUP METHODS (kept, unchanged behavior)
    # ------------------------------------------------------------

    def get_definition(self, word):
        word_key = word.strip().lower()
        matches = self._definitions_index.get(word_key, [])
        return {
            "word": word,
            "found": len(matches) > 0,
            "definitions": matches,
            "source_library": "Definitions Library (Johnson's 1755 / Bailey's 1721)",
        }

    def get_etymology(self, word):
        word_key = word.strip().lower()
        entry = self._etymology.get(word_key)
        return {
            "word": word,
            "found": entry is not None,
            "etymology": entry,
            "source_library": "Etymology Dictionary (ODEE / OED / Bosworth-Toller / Lewis & Short)",
        }

    def get_historical_context(self, word):
        word_key = word.strip().lower()
        matches = self._context_index.get(word_key, [])
        return {
            "word": word,
            "found": len(matches) > 0,
            "context_notes": matches,
            "source_library": "Historical Context & Intent Library",
        }

    def get_everything(self, word):
        return {
            "word": word,
            "definitions": self.get_definition(word),
            "etymology": self.get_etymology(word),
            "historical_context": self.get_historical_context(word),
        }

    def list_available_sources(self):
        return self.context_data.get("sources", [])

    def library_status(self):
        definitions_error = self.definitions_data.get("_load_error")
        context_error = self.context_data.get("_load_error")
        return {
            "definitions_library_loaded": definitions_error is None,
            "definitions_library_error": definitions_error,
            "definitions_word_count": len(self._definitions_index),
            "etymology_loaded": getattr(self, "_etymology_error", None) is None,
            "etymology_error": getattr(self, "_etymology_error", None),
            "etymology_word_count": len(self._etymology),
            "historical_context_library_loaded": context_error is None,
            "historical_context_library_error": context_error,
            "historical_context_word_count": len(self._context_index),
        }


# ------------------------------------------------------------
# QUICK SELF-TEST
# ------------------------------------------------------------
# Running this file directly prints a status report and shows the gate
# deciding a word it CAN source and a word it CANNOT.

if __name__ == "__main__":
    libraries = VeritasLibraries()
    status = libraries.library_status()

    print("VERITAS Libraries status check")
    print("-------------------------------")
    print(f"Definitions loaded: {status['definitions_library_loaded']} "
          f"({status['definitions_word_count']} words)")
    print(f"Etymology loaded:   {status['etymology_loaded']} "
          f"({status['etymology_word_count']} words)")
    print(f"Context loaded:     {status['historical_context_library_loaded']} "
          f"({status['historical_context_word_count']} words)")
    print()

    print("GATE TEST 1 -- a word that IS sourced:")
    r1 = libraries.resolve("senate")
    print(f"  status: {r1['status']}")
    for line in r1["trace"]:
        print("   -", line)
    print()

    print("GATE TEST 2 -- a word that is NOT sourced:")
    r2 = libraries.resolve("indictment")
    print(f"  status: {r2['status']}")
    for line in r2["trace"]:
        print("   -", line)
