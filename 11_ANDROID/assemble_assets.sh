#!/usr/bin/env bash
# Build  app/src/main/assets/veritas-data.zip  — the data tree the APK ships and
# unpacks to the phone's files dir on first run. The zip's top folder is "veritas/",
# so it extracts to  filesDir/veritas/00_APP/...  which VERITAS_ROOT then points at.
#
# LEAN (default) = phone-first set (Define/Drift, dictionary browse, founding-doc
# reader, notes) ≈ 100 MB — just the SQLite library + engine + web + books.
# --full also bundles the 170 MB FTS5 corpora (enables concordance / live founding-
# usage search) ≈ 280 MB.
#
# Run this on a machine WITH disk space (this desktop's local disk is usually full —
# use the USB or the Android-Studio build box). Needs `zip`.
set -e
SRC="${VERITAS_SRC:-/home/noneya/Projects/VERITAS v.3}"
HERE="$(cd "$(dirname "$0")" && pwd)"
OUT="$HERE/app/src/main/assets"
TMP="$(mktemp -d)"; STAGE="$TMP/veritas"
mkdir -p "$STAGE/00_APP" "$STAGE/02_GATE_BLACKLETTER/gate" "$STAGE/10_AGENTS" "$STAGE/07_CAPTURE_TOOLS"

# ---- web + engine (small) ----
cp "$SRC/00_APP"/*.py "$STAGE/00_APP/" 2>/dev/null || true
cp "$SRC/00_APP/m.html" "$SRC/00_APP/VERITAS.html" "$SRC/00_APP/guide.html" "$STAGE/00_APP/" 2>/dev/null || true
cp -r "$SRC/00_APP/books" "$STAGE/00_APP/" 2>/dev/null || true

# ---- the gate: SQLite library (NOT the 89 MB json) + gate python + flags ----
cp "$SRC/02_GATE_BLACKLETTER/gate"/*.py  "$STAGE/02_GATE_BLACKLETTER/gate/" 2>/dev/null || true
cp "$SRC/02_GATE_BLACKLETTER/gate/VERITAS_definitions_library.db" "$STAGE/02_GATE_BLACKLETTER/gate/"
cp "$SRC/02_GATE_BLACKLETTER/gate/blackletter_flags.json" "$STAGE/02_GATE_BLACKLETTER/gate/" 2>/dev/null || true

# ---- agent + capture-tool python (imports the engine needs; corpora only with --full) ----
cp "$SRC/10_AGENTS"/*.py       "$STAGE/10_AGENTS/" 2>/dev/null || true
cp "$SRC/07_CAPTURE_TOOLS"/*.py "$STAGE/07_CAPTURE_TOOLS/" 2>/dev/null || true

if [ "$1" = "--full" ]; then
  echo "…including FTS5 corpora (concordance)"
  mkdir -p "$STAGE/03_LIBRARIES/founding_sources"
  cp "$SRC/03_LIBRARIES/historical_documents.db" "$STAGE/03_LIBRARIES/" 2>/dev/null || true
  cp "$SRC/03_LIBRARIES/founding_sources/founding_corpus.db" "$STAGE/03_LIBRARIES/founding_sources/" 2>/dev/null || true
  for a in federalist antifederalist ratification convention blackstone story montesquieu; do
    mkdir -p "$STAGE/10_AGENTS/$a"; cp "$SRC/10_AGENTS/$a/corpus.db" "$STAGE/10_AGENTS/$a/" 2>/dev/null || true
  done
fi

mkdir -p "$OUT"
rm -f "$OUT/veritas-data.zip"
( cd "$TMP" && zip -0 -r -q "$OUT/veritas-data.zip" veritas )
rm -rf "$TMP"
echo "built $OUT/veritas-data.zip  ($(du -sh "$OUT/veritas-data.zip" | cut -f1))"
echo "NOTE: bump assetVersion in MainActivity.kt so the phone re-extracts the new data."
