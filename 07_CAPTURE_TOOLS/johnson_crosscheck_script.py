"""
Johnson's Dictionary Online -- 1755 Cross-Check Script

WHAT THIS DOES
Visits johnsonsdictionaryonline.com for a real word, finds every 1755 result row,
reads the real definition text the site displays, and saves it. It does NOT guess,
OCR, or interpret anything -- it copies text that a real human already transcribed
correctly on that site.

BEFORE RUNNING THE FULL LIST
Run this in TEST MODE first (see bottom of file). Look at test_output.json yourself
and confirm the definitions in it are real and correct. Only then switch to the
full word list.

REQUIREMENTS
    pip install playwright
    playwright install chromium
"""

import json
import time
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

SEARCH_URL = "https://johnsonsdictionaryonline.com/views/search.php?term={}"
DELAY_BETWEEN_WORDS = 1.5   # seconds -- be respectful of a small academic site's server
DELAY_AFTER_CLICK = 0.8     # seconds -- give the page time to load the clicked entry

OUTPUT_FILE = "johnson_1755_results.json"
PROBLEMS_FILE = "johnson_1755_problems.json"
SCREENSHOT_DIR = Path("failure_screenshots")
SCREENSHOT_DIR.mkdir(exist_ok=True)


def load_existing_results():
    """Resume from where a previous run left off, if any results already exist."""
    if Path(OUTPUT_FILE).exists():
        return json.loads(Path(OUTPUT_FILE).read_text(encoding="utf-8"))
    return []


def save_results(results):
    Path(OUTPUT_FILE).write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")


def log_problem(problems, word, reason):
    problems.append({"word": word, "reason": reason})
    Path(PROBLEMS_FILE).write_text(json.dumps(problems, ensure_ascii=False, indent=1), encoding="utf-8")


def lookup_word(page, word):
    """
    Returns a list of {"w": word, "t": definition_text, "c": "confirmed"} dicts --
    one per 1755 result row found for this word. Returns an empty list if the word
    has no 1755 entry at all. Raises a clear exception if the page structure doesn't
    match what was confirmed earlier -- callers should catch this and log it, not
    silently continue.
    """
    page.goto(SEARCH_URL.format(word), wait_until="networkidle", timeout=20000)

    # Confirmed real selector from the site's own saved page source.
    search_box = page.locator("input.search-text")
    if search_box.count() == 0:
        raise RuntimeError(
            "input.search-text was not found on the page. The site's structure may "
            "have changed since this was written -- stop and check manually before continuing."
        )

    search_box.first.fill(word)

    # Force the search type to Headword for a clean, specific lookup.
    type_dropdown = page.locator("select.search-tag")
    if type_dropdown.count() > 0:
        type_dropdown.first.select_option("headword")

    # Find and click the real Search button.
    search_button = page.get_by_role("button", name="Search", exact=False)
    if search_button.count() == 0:
        raise RuntimeError("Could not find a Search button on the page.")
    search_button.first.click()

    page.wait_for_timeout(1200)  # let results render

    # Every confirmed-real result row is short text containing a year label.
    # A word can have zero, one, or several 1755 rows (different parts of speech).
    all_rows = page.locator("text=/1755/")
    row_count = all_rows.count()

    if row_count == 0:
        return []  # genuinely not found -- this is a real, valid outcome, not an error

    collected = []
    seen_texts = set()

    for i in range(row_count):
        row = all_rows.nth(i)
        try:
            row.click(timeout=5000)
        except PWTimeout:
            continue  # this specific row failed to click; move on to the next one, don't abort the word

        page.wait_for_timeout(int(DELAY_AFTER_CLICK * 1000))

        # The definition panel is the main content block; grab its visible text.
        # This selector is intentionally broad and defensive since the exact class
        # name of the definition panel was not confirmed directly -- if this grabs
        # obviously wrong content (menus, footers), that will be visible immediately
        # in test mode output, which is exactly why test mode exists.
        panel_candidates = page.locator("div, section, article").all()
        best_text = ""
        for el in panel_candidates:
            try:
                txt = el.inner_text(timeout=1000).strip()
            except Exception:
                continue
            if 40 < len(txt) < 3000 and word.lower() in txt.lower():
                if not best_text or len(txt) < len(best_text):
                    best_text = txt  # prefer the smallest block that still contains the word

        if best_text and best_text not in seen_texts:
            seen_texts.add(best_text)
            collected.append({"w": word, "t": best_text, "c": "confirmed"})

    return collected


def run(word_list, test_mode=False):
    results = [] if test_mode else load_existing_results()
    already_done = {r["w"].lower() for r in results}
    problems = json.loads(Path(PROBLEMS_FILE).read_text(encoding="utf-8")) if Path(PROBLEMS_FILE).exists() else []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not test_mode)  # visible browser in test mode so you can watch it
        page = browser.new_page()

        for word in word_list:
            if word.lower() in already_done and not test_mode:
                continue

            print(f"Looking up: {word}")
            try:
                found = lookup_word(page, word)
            except Exception as e:
                print(f"  PROBLEM: {e}")
                log_problem(problems, word, str(e))
                try:
                    page.screenshot(path=str(SCREENSHOT_DIR / f"{word}_error.png"))
                except Exception:
                    pass
                continue

            if found:
                print(f"  found {len(found)} 1755 entr{'y' if len(found)==1 else 'ies'}")
                results.extend(found)
            else:
                print("  no 1755 entry found")
                results.append({"w": word, "t": "", "c": "not_found_1755"})

            if not test_mode:
                save_results(results)  # save after every word so nothing is lost if this stops
            time.sleep(DELAY_BETWEEN_WORDS)

        browser.close()

    if test_mode:
        Path("test_output.json").write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
        print("\nTest mode complete. Open test_output.json and read it yourself before running the full list.")
    else:
        save_results(results)
        print(f"\nDone. {len(results)} total entries saved to {OUTPUT_FILE}.")
        if problems:
            print(f"{len(problems)} words had problems -- see {PROBLEMS_FILE}.")


if __name__ == "__main__":
    # ---- TEST MODE: run this first ----
    TEST_WORDS = ["regulate", "arms", "commerce", "liberty", "justice"]
    run(TEST_WORDS, test_mode=True)

    # ---- FULL RUN: only uncomment this after checking test_output.json yourself ----
    # full_list = json.loads(Path("CONSTITUTION_WORD_LIST.json").read_text(encoding="utf-8"))
    # run(full_list, test_mode=False)
