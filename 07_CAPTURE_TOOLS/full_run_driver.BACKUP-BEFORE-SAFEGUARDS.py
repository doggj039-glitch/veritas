"""
Full-run driver for the 1773 capture.

Scrapes every word in johnson_1773_wordlist.json using the confirmed
lookup_word_1773() from johnson_1773_scraper.py, saving to
johnson_1773_results.json after EVERY word so an interruption never loses work.

Resumable: rerun and it skips words already captured. Sequential only, 1.5s
between words (HARD RULE 3) -- never parallel, to stay kind to the server.
"""
import json, time, sys
from pathlib import Path

sys.path.insert(0, "/home/noneya/Projects/VERITAS_MASTER_MERGE/07_CAPTURE_TOOLS")
from johnson_1773_scraper import lookup_word_1773, DELAY_BETWEEN_WORDS
from playwright.sync_api import sync_playwright

ROOT = Path("/home/noneya/Projects/VERITAS_MASTER_MERGE/03_LIBRARIES")
WORDLIST = ROOT / "johnson_1773_wordlist.json"
OUT = ROOT / "johnson_1773_results.json"
PROGRESS = ROOT / "johnson_1773_progress.txt"

words = json.loads(WORDLIST.read_text(encoding="utf-8"))

# ---- resume ----
results = []
done = set()
if OUT.exists():
    try:
        results = json.loads(OUT.read_text(encoding="utf-8"))
        done = {r["word"].lower() for r in results}
    except Exception:
        results, done = [], set()

todo = [w for w in words if w.lower() not in done]
print(f"Total {len(words)} words | already done {len(done)} | to do {len(todo)}", flush=True)


def save():
    OUT.write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    for idx, word in enumerate(todo, 1):
        try:
            entries = lookup_word_1773(page, word)
            if entries:
                rec = {"word": word, "found_1773": True, "status": "found", "entries": entries}
            else:
                rec = {"word": word, "found_1773": False, "status": "not_found", "entries": []}
        except Exception as e:
            # Never abort the whole run for one bad word; try to recover the page.
            print(f"  [{idx}/{len(todo)}] PROBLEM {word}: {e}", flush=True)
            rec = {"word": word, "found_1773": False, "status": "error",
                   "error": str(e), "entries": []}
            try:
                page.close()
            except Exception:
                pass
            try:
                page = browser.new_page()
            except Exception:
                pass

        results.append(rec)
        save()
        n_ent = len(rec["entries"])
        tag = rec["status"] + (f" ({n_ent})" if n_ent else "")
        if idx % 10 == 0 or idx == len(todo):
            msg = f"[{idx}/{len(todo)}] {word}: {tag} | total records {len(results)}"
            print(msg, flush=True)
            PROGRESS.write_text(msg + "\n", encoding="utf-8")
        time.sleep(DELAY_BETWEEN_WORDS)  # HARD RULE 3
    browser.close()

found = sum(1 for r in results if r["found_1773"])
nf = sum(1 for r in results if r["status"] == "not_found")
err = sum(1 for r in results if r["status"] == "error")
print(f"\nSCRAPE COMPLETE. {len(results)} words | found {found} | not_found {nf} | error {err}", flush=True)
PROGRESS.write_text(f"COMPLETE: {len(results)} words | found {found} | not_found {nf} | error {err}\n",
                    encoding="utf-8")
