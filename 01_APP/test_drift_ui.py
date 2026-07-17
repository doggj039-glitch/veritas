# Copyright (c) contributors. Licensed under the Apache License, Version 2.0.
"""
Manual test harness for the "Define the Drift" UI.

Launches the REAL app (LegalAnalyzerApp) and injects a sample research result so
the Research Map's "Key Terms & Definitions" section is populated immediately --
no AI pipeline / API key / corpus needed. Terms with a dictionary drift timeline
show a clickable "⊕ Define the Drift" link; click one to open the timeline window.

Run:  cd 01_APP && source .venv/bin/activate && python3 test_drift_ui.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from main import LegalAnalyzerApp

SAMPLE = {
    "question": "[DEMO] How has the meaning of 'commerce' drifted since the founding?",
    "timestamp": "2026-07-08 (demo)",
    "restatement": "Demo research result injected to test the 'Define the Drift' timeline UI.",
    "definitions": {
        "commerce": {"plain_english": "Trade and exchange between people or states.",
                     "doctrinal": "Basis of the Commerce Clause (Art. I, §8).",
                     "historical_context": "Founding-era usage was broad ('intercourse')."},
        "senate": {"plain_english": "The upper legislative chamber.",
                   "doctrinal": "Art. I, §3.", "historical_context": "Council of elders."},
        "liberty": {"plain_english": "Freedom from restraint.",
                    "doctrinal": "Due Process / 5th & 14th Amend.", "historical_context": ""},
        "tyranny": {"plain_english": "Arbitrary or despotic exercise of power.",
                    "doctrinal": "The harm the separation of powers guards against.",
                    "historical_context": ""},
    },
    "corpus_hits": [], "citation_path": [], "drift_flags": [],
    "gaps": [], "source_list": [], "errors": ["DEMO MODE — sample data, not a real pipeline run."],
}


def main():
    root = tk.Tk()
    app = LegalAnalyzerApp(root)

    def inject():
        try:
            app.research_result = SAMPLE
            if hasattr(app, "notebook") and hasattr(app, "research_tab"):
                app.notebook.select(app.research_tab)
            app._display_research_result(SAMPLE)
            print("Injected demo research result. Click a '⊕ Define the Drift' link in the Research Map.")
        except Exception as e:
            import traceback; traceback.print_exc()
            print("Injection failed:", e)

    root.after(600, inject)
    root.mainloop()


if __name__ == "__main__":
    main()
