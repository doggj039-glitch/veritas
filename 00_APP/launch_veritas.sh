#!/usr/bin/env bash
# VERITAS launcher — starts the local bridge (gate + agents engine) if needed, then
# opens the Library Workstation as a standalone app window pointed at it.
# Fully offline: the bridge binds 127.0.0.1 only; no internet is used.

PORT=8737
ROOT="/home/noneya/Projects/VERITAS v.3"
URL="http://127.0.0.1:$PORT/VERITAS.html"
LOG="$HOME/.local/share/veritas-server.log"

# start the engine bridge unless it's already listening
if ! curl -s -o /dev/null --max-time 2 "http://127.0.0.1:$PORT/api/agents"; then
  nohup setsid python3 -u "$ROOT/00_APP/veritas_server.py" "$PORT" >"$LOG" 2>&1 < /dev/null &
  # wait up to ~20s for the engine to finish loading the library + agents
  for i in $(seq 1 40); do
    curl -s -o /dev/null --max-time 1 "http://127.0.0.1:$PORT/api/agents" && break
    sleep 0.5
  done
fi

# open the app in a chromeless window (Chromium family preferred). External links
# (Oyez, Justia, web) are handed to the system browser by the bridge's /api/open,
# so the app stays clean AND links still work — the "hybrid".
for b in google-chrome-stable google-chrome chromium chromium-browser brave-browser microsoft-edge; do
  if command -v "$b" >/dev/null 2>&1; then
    exec "$b" --app="$URL" --class=VERITAS --name=VERITAS \
      --password-store=basic \
      --user-data-dir="$HOME/.local/share/veritas-app" \
      --no-first-run --no-default-browser-check
  fi
done
if command -v firefox >/dev/null 2>&1; then
  exec firefox --new-window "$URL"
fi
exec xdg-open "$URL"
