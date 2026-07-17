"""
Driver for the SECOND 1773 pass -- the words that came back NOT_FOUND first time.

For each word: look it up directly (lookup_word_1773). If nothing comes back,
try root_retry.candidate_roots() in order -- one real request each, respecting
the 1.5s courtesy delay -- and accept the first root that BOTH returns entries
AND passes headword_matches() (Safeguard 1 is not skipped for retried words).

Saves after every word so the run is resumable. Sequential only, never parallel.

Usage:
    python3 missed_words_driver.py <wordlist.json> <output.json>
"""
import json, time, sys
from pathlib import Path

sys.path.insert(0, "/home/noneya/Projects/VERITAS_MASTER_MERGE/07_CAPTURE_TOOLS")
from johnson_1773_scraper import lookup_word_1773, DELAY_BETWEEN_WORDS
from root_retry import candidate_roots
from headword_check import headword_matches
from playwright.sync_api import sync_playwright


def run(wordlist_path, output_path):
    words = json.loads(Path(wordlist_path).read_text(encoding="utf-8"))
    out = Path(output_path)

    results, done = [], set()
    if out.exists():
        try:
            results = json.loads(out.read_text(encoding="utf-8"))
            done = {r["word"].lower() for r in results}
        except Exception:
            results, done = [], set()

    todo = [w for w in words if w.lower() not in done]
    print(f"Total {len(words)} | done {len(done)} | to do {len(todo)}", flush=True)

    def save():
        out.write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        for idx, word in enumerate(todo, 1):
            try:
                entries = lookup_word_1773(page, word)
                if entries:
                    rec = {"word": word, "found_1773": True, "status": "found",
                           "entries": entries}
                else:
                    # SAFEGUARD 2 -- root-word retry, gated by SAFEGUARD 1.
                    rec = None
                    for root in candidate_roots(word):
                        time.sleep(DELAY_BETWEEN_WORDS)  # still a real request
                        root_entries = lookup_word_1773(page, root)
                        if root_entries and any(
                            headword_matches(root, r.get("headword_label", ""))
                            for r in root_entries
                        ):
                            rec = {"word": word, "found_1773": True, "status": "found",
                                   "entries": root_entries,
                                   "matched_via_root": True, "root_used": root}
                            break
                    if rec is None:
                        rec = {"word": word, "found_1773": False,
                               "status": "not_found", "entries": []}
            except Exception as e:
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
            tag = rec["status"]
            if rec.get("matched_via_root"):
                tag += f" via root '{rec['root_used']}'"
            elif rec["status"] == "found":
                tag += f" ({len(rec['entries'])})"
            print(f"[{idx}/{len(todo)}] {word}: {tag}", flush=True)
            time.sleep(DELAY_BETWEEN_WORDS)  # HARD RULE: courtesy delay between words
        browser.close()

    save()
    found = sum(1 for r in results if r["found_1773"])
    via_root = sum(1 for r in results if r.get("matched_via_root"))
    print(f"\nDONE. {len(results)} words | found {found} "
          f"(of which {via_root} via root-retry) | "
          f"not_found {sum(1 for r in results if r['status']=='not_found')}", flush=True)
    return results


if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2])
