#!/usr/bin/env python3
"""
VERITAS desktop launcher — the PyInstaller entry point for the standalone app
(Windows .exe / Linux binary). It is the frozen equivalent of launch_veritas.sh.

What it does:
  1. Points VERITAS_ROOT at the bundled tree (sys._MEIPASS when frozen, the dev
     project when run from source) BEFORE any engine module is imported, so the
     gate, agents, usage and cases all resolve their data from the bundle.
  2. Starts the local bridge (veritas_server.run) on a background thread, bound to
     127.0.0.1 only — fully offline, no external calls.
  3. Waits for the engine to answer, then opens the Library Workstation in the
     user's default browser.
  4. Keeps running until this window is closed (Ctrl-C / close the console).

Build:  pyinstaller VERITAS_v3.spec      (run ON the target OS — no cross-compile)
"""
import os
import sys
import time
import threading
import webbrowser
import urllib.request
from pathlib import Path

PORT = int(os.environ.get("VERITAS_PORT", "8737"))
URL = f"http://127.0.0.1:{PORT}/VERITAS.html"
PING = f"http://127.0.0.1:{PORT}/api/agents"


def _app_root() -> Path:
    """The tree that holds 00_APP, 02_GATE_BLACKLETTER, 10_AGENTS, 03_LIBRARIES."""
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)                       # PyInstaller bundle dir
    return Path(__file__).resolve().parent.parent       # dev: <repo>/VERITAS v.3


def _wait_and_open():
    """Poll the engine; open the browser once it answers (or give up after ~30s)."""
    for _ in range(120):
        try:
            urllib.request.urlopen(PING, timeout=1).read()
            break
        except Exception:
            time.sleep(0.25)
    else:
        print("VERITAS: engine did not come up in time; open", URL, "manually.")
        return
    print("VERITAS: opening", URL)
    import shutil
    import subprocess
    # When frozen, PyInstaller sets LD_LIBRARY_PATH (and possibly LD_PRELOAD) to the
    # bundle's _internal dir. Any child we spawn — a system browser above all —
    # inherits it and loads the bundle's libraries instead of its own, and crashes
    # on startup. Restore the pre-bundle values (PyInstaller saves them as *_ORIG;
    # if there was none, the var was unset originally) so everything we launch from
    # here on starts in the host environment.
    for var in ("LD_LIBRARY_PATH", "LD_PRELOAD"):
        orig = os.environ.pop(var + "_ORIG", None)
        if orig is not None:
            os.environ[var] = orig
        else:
            os.environ.pop(var, None)
    # Prefer a Chromium-family browser in app mode. VERITAS's 🎤 dictation uses the
    # browser Web Speech API, which Firefox does NOT implement (Chromium/Chrome do).
    # Opening in Chromium keeps speech-to-text working regardless of the system default.
    # Fall back to the default browser if no Chromium-family browser is installed.
    for exe in ("chromium", "chromium-browser", "google-chrome", "google-chrome-stable",
                "brave-browser", "microsoft-edge"):
        path = shutil.which(exe)
        if path:
            try:
                subprocess.Popen([path, "--app=" + URL], start_new_session=True,
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return
            except Exception:
                pass
    try:
        webbrowser.open(URL)
    except Exception:
        print("VERITAS: could not open a browser automatically; go to", URL)


def main():
    root = _app_root()
    # MUST be set before importing the engine — gate/agents/usage read it at import.
    os.environ["VERITAS_ROOT"] = str(root)
    sys.path.insert(0, str(root / "00_APP"))

    import veritas_server  # noqa: E402  (import after VERITAS_ROOT is set)

    print("VERITAS desktop")
    print("  root:", root)
    print("  keep this window open while you use VERITAS; close it to quit.")

    threading.Thread(target=_wait_and_open, daemon=True).start()
    try:
        veritas_server.run(PORT)          # blocks, serves forever
    except KeyboardInterrupt:
        print("\nVERITAS: shutting down.")


if __name__ == "__main__":
    main()
