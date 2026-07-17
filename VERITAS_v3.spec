# -*- mode: python ; coding: utf-8 -*-
# VERITAS_v3.spec — PyInstaller spec for the *v.3 web-app* VERITAS (server + browser),
# NOT the old tkinter app. Entry point is 00_APP/veritas_desktop.py, which sets
# VERITAS_ROOT to the bundle dir and runs veritas_server.run() + opens the browser.
#
#   Build (ON the target OS — PyInstaller does NOT cross-compile):
#       pip install pyinstaller
#       pyinstaller VERITAS_v3.spec
#   Output:  dist/VERITAS/VERITAS.exe   (Windows)   or   dist/VERITAS/VERITAS (Linux)
#
# Set INCLUDE_TTS=0 in the environment before building to drop the 112 MB Piper voice
# (read-aloud then falls back to the browser's speech synthesis / native TTS).

import os
from PyInstaller.utils.hooks import collect_dynamic_libs, collect_data_files

PROJ = SPECPATH                                   # dir containing this spec = repo root
INCLUDE_TTS = os.environ.get("INCLUDE_TTS", "1") != "0"
# Offline dictation (Vosk). Set INCLUDE_STT=0 to drop it + the ~68 MB model.
INCLUDE_STT = os.environ.get("INCLUDE_STT", "1") != "0"


def add_file(datas, rel, dest):
    src = os.path.join(PROJ, rel)
    if os.path.isfile(src):
        datas.append((src, dest))
    else:
        print("VERITAS.spec: SKIP missing file", rel)


def add_dir(datas, rel, dest):
    src = os.path.join(PROJ, rel)
    if os.path.isdir(src):
        datas.append((src, dest))
    else:
        print("VERITAS.spec: SKIP missing dir", rel)


def add_glob(datas, reldir, pattern, dest):
    import glob
    for src in glob.glob(os.path.join(PROJ, reldir, pattern)):
        datas.append((src, dest))


datas = []

# ---- 00_APP: the UI + the engine module (imported from disk at runtime) ----
for f in ("VERITAS.html", "m.html", "guide.html", "_pdfrt.html",
          "veritas_server.py", "build_readers.py"):
    add_file(datas, os.path.join("00_APP", f), "00_APP")
add_dir(datas, "00_APP/books", "00_APP/books")
if INCLUDE_TTS:
    add_dir(datas, "00_APP/tts", "00_APP/tts")
if INCLUDE_STT:
    add_dir(datas, "00_APP/stt/model", "00_APP/stt/model")   # Vosk model (~68 MB)

# ---- 02_GATE_BLACKLETTER/gate: all engine code + ONLY the SQLite library ----
# (skip VERITAS_definitions_library.json + the *.BACKUP-*.json — ~230 MB of stale copies;
#  the gate prefers the .db and only falls back to JSON if the .db is absent.)
add_glob(datas, "02_GATE_BLACKLETTER/gate", "*.py", "02_GATE_BLACKLETTER/gate")
for f in ("VERITAS_definitions_library.db", "blackletter_flags.json",
          "VERITAS_historical_context_library.json"):
    add_file(datas, os.path.join("02_GATE_BLACKLETTER/gate", f), "02_GATE_BLACKLETTER/gate")

# ---- 10_AGENTS: agent code + every compartment (persona.md + corpus.db) ----
add_glob(datas, "10_AGENTS", "*.py", "10_AGENTS")
_agents_root = os.path.join(PROJ, "10_AGENTS")
if os.path.isdir(_agents_root):
    for name in sorted(os.listdir(_agents_root)):
        d = os.path.join(_agents_root, name)
        if os.path.isdir(d) and os.path.isfile(os.path.join(d, "corpus.db")):
            datas.append((d, os.path.join("10_AGENTS", name)))

# ---- 03_LIBRARIES: ONLY the files the engine actually reads (~103 MB of 3.2 GB) ----
# concordance / founding-usage (the Drift dimension) + "cases that construed it".
add_file(datas, "03_LIBRARIES/historical_documents.db", "03_LIBRARIES")
add_file(datas, "03_LIBRARIES/founding_sources/founding_corpus.db", "03_LIBRARIES/founding_sources")
add_file(datas, "03_LIBRARIES/scotus_oral_arguments/scotus_index.json", "03_LIBRARIES/scotus_oral_arguments")
add_file(datas, "03_LIBRARIES/from_sdcard/tables/word_to_cases.json", "03_LIBRARIES/from_sdcard/tables")
add_dir(datas, "03_LIBRARIES/analysis_layer", "03_LIBRARIES/analysis_layer")

# The engine modules are imported from disk (sys.path.insert at runtime), so they are
# shipped as data above. These hidden imports cover the stdlib the engine relies on,
# which PyInstaller can't see through the runtime path insertion.
hiddenimports = [
    "sqlite3", "json", "re", "hashlib", "bisect", "shlex", "signal",
    "subprocess", "difflib", "unicodedata", "html", "html.parser",
    "http.server", "socketserver", "urllib", "urllib.request",
    "urllib.parse", "urllib.error", "webbrowser", "threading",
]

# Vosk offline speech-to-text: bundle its native lib (libvosk) + package data, and
# pull in its runtime deps (cffi) so /api/dictate works in the frozen app.
binaries = []
if INCLUDE_STT:
    binaries += collect_dynamic_libs("vosk")
    datas += collect_data_files("vosk")
    hiddenimports += ["vosk", "cffi", "_cffi_backend"]

block_cipher = None

a = Analysis(
    [os.path.join(PROJ, "00_APP", "veritas_desktop.py")],
    pathex=[PROJ, os.path.join(PROJ, "00_APP")],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["numpy", "pandas", "matplotlib", "scipy", "PIL",
              "pytest", "PyQt5", "PySide2", "tkinter"],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# One-DIR build (a folder with VERITAS.exe + data). Faster startup than one-file and
# no giant temp-extract on every launch — better for the ~300 MB of bundled data.
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="VERITAS",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,            # keep the little status window; close it to quit VERITAS
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join(PROJ, "00_ASSETS", "veritas.ico")
        if os.path.isfile(os.path.join(PROJ, "00_ASSETS", "veritas.ico")) else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="VERITAS",
)
