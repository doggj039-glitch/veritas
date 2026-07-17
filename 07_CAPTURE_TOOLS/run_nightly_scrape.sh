#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# VERITAS -- nightly self-grounding round-2 scrape (SCRAPE ONLY).
#
# Pulls Johnson 1773 definitions for the 1,905-word filtered gap list, saving
# after every word (resumable). It does NOT touch the library -- processing is
# done manually, supervised, in the morning.
#
# Self-terminating: once all 1,905 words are captured it exits immediately and
# makes no further requests to the site, so leaving this in cron is harmless.
# Sequential only, 1.5s between requests (courtesy to a small academic server).
# ---------------------------------------------------------------------------
set -u
ROOT="/home/noneya/Projects/VERITAS v.3"
WORDLIST="$ROOT/03_LIBRARIES/vocab_round2_wordlist.json"
RESULTS="$ROOT/03_LIBRARIES/vocab_round2_results.json"
LOG="$ROOT/03_LIBRARIES/vocab_round2_nightly.log"
TOTAL=1905

echo "=== nightly scrape start: $(date '+%F %T %Z') ===" >> "$LOG"

# Skip entirely if the batch is already complete (no needless browser launch / requests).
DONE=$(python3 -c "import json,os; f='$RESULTS'; print(len(json.load(open(f))) if os.path.exists(f) else 0)" 2>/dev/null || echo 0)
if [ "${DONE:-0}" -ge "$TOTAL" ]; then
    echo "already complete ($DONE/$TOTAL) -- nothing to do." >> "$LOG"
    echo "=== nightly scrape end: $(date '+%F %T %Z') ===" >> "$LOG"
    exit 0
fi

cd "$ROOT/07_CAPTURE_TOOLS" || { echo "ERROR: cd failed" >> "$LOG"; exit 1; }
# shellcheck disable=SC1091
source "$ROOT/01_APP/.venv/bin/activate" || { echo "ERROR: venv activate failed" >> "$LOG"; exit 1; }

python3 missed_words_driver.py "$WORDLIST" "$RESULTS" >> "$LOG" 2>&1
rc=$?

echo "driver exit code: $rc" >> "$LOG"
echo "=== nightly scrape end: $(date '+%F %T %Z') ===" >> "$LOG"
exit $rc
