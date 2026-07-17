"""
Johnson's Dictionary Online -- 1773 (4th folio ed.) Capture Script

Adapted from johnson_crosscheck_script.py (which targets the 1755 rows).
This version captures the 1773 edition result rows specifically.

WHAT IT DOES
For each word it opens
    https://johnsonsdictionaryonline.com/views/search.php?term=WORD
reads the list of result rows, and for EVERY row whose edition span reads
"1773" it clicks that row, waits for the definition panel (#result_word) to
load that specific entry, and copies the text VERBATIM as displayed. It never
guesses, OCRs, paraphrases, or cleans up anything. A word with no 1773 row is
recorded as NOT_FOUND -- an honest empty slot, never a guess.

DOM facts confirmed by direct inspection of the live site:
  * Result rows each contain  <span class="edition">1755|1773</span>
    inside a row whose text reads e.g. "commerce, n.s.1773".
  * Clicking a 1773 edition span loads that entry into  div#result_word
    and updates the page <title> to e.g. "commerce, n.s. (1773)".
  * A word can have zero, one, or several 1773 rows (different parts of speech).

REQUIREMENTS
    pip install playwright
    playwright install chromium
"""

import json
import re
import time
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

SEARCH_URL = "https://johnsonsdictionaryonline.com/views/search.php?term={}"
DELAY_BETWEEN_WORDS = 1.5   # seconds -- HARD RULE 3: be respectful of a small academic server
DELAY_AFTER_CLICK   = 0.9   # seconds -- give the clicked entry time to render into #result_word
PAGE_TIMEOUT_MS     = 30000


def _pos_from_title(title: str):
    """'commerce, n.s. (1773)' -> ('commerce', 'n.s.').  Best-effort; never invents."""
    t = re.sub(r"\s*\(1773\)\s*$", "", (title or "").strip())
    if "," in t:
        head, pos = t.rsplit(",", 1)
        return head.strip(), pos.strip()
    return t.strip(), ""


def lookup_word_1773(page, word):
    """
    Return a list of captured 1773 entries for `word`, each:
        {"headword_label", "part_of_speech", "year": 1773, "title", "definition_text"}
    Empty list == genuinely no 1773 entry (a real, valid NOT_FOUND outcome).
    Raises on unexpected page structure so the caller logs it instead of guessing.
    """
    page.goto(SEARCH_URL.format(word), wait_until="networkidle", timeout=PAGE_TIMEOUT_MS)
    page.wait_for_timeout(1800)  # let the JS-rendered result list settle

    # Sanity: the search UI must be present, otherwise the site changed.
    if page.locator("input.search-text").count() == 0 and page.locator("#result_word").count() == 0:
        raise RuntimeError(
            "Neither input.search-text nor #result_word found -- the site's structure "
            "may have changed. Stop and check manually before trusting any output."
        )

    # Every 1773 result row is a <span class="edition"> whose text is exactly 1773.
    year_spans = page.locator("xpath=//span[@class='edition'][normalize-space(text())='1773']")
    n = year_spans.count()
    if n == 0:
        return []  # no 1773 entry -- honest NOT_FOUND

    collected = []
    seen = set()
    for i in range(n):
        span = year_spans.nth(i)
        try:
            span.scroll_into_view_if_needed(timeout=4000)
            span.click(timeout=6000)
        except PWTimeout:
            continue  # this row wouldn't click; skip it rather than abort the whole word
        page.wait_for_timeout(int(DELAY_AFTER_CLICK * 1000))

        title = page.title()
        if "1773" not in title:
            # Panel did not switch to a 1773 entry; don't record a mismatched read.
            continue

        panel = page.locator("#result_word")
        if panel.count() == 0:
            continue
        text = panel.first.inner_text().strip()
        if not text:
            continue

        headword_label, pos = _pos_from_title(title)
        key = (title, text)
        if key in seen:
            continue
        seen.add(key)
        collected.append({
            "headword_label": headword_label,
            "part_of_speech": pos,
            "year": 1773,
            "title": title,
            "definition_text": text,   # VERBATIM as displayed
        })

    return collected


def run(word_list, out_path, test_mode=False):
    results = []
    problems = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        for word in word_list:
            print(f"Looking up (1773): {word}")
            try:
                entries = lookup_word_1773(page, word)
            except Exception as e:
                print(f"  PROBLEM: {e}")
                problems.append({"word": word, "reason": str(e)})
                results.append({"word": word, "found_1773": False,
                                "status": "error", "error": str(e), "entries": []})
                time.sleep(DELAY_BETWEEN_WORDS)
                continue

            if entries:
                print(f"  found {len(entries)} 1773 entr{'y' if len(entries)==1 else 'ies'}: "
                      + "; ".join(e['title'] for e in entries))
                results.append({"word": word, "found_1773": True,
                                "status": "found", "entries": entries})
            else:
                print("  NOT_FOUND (no 1773 entry)")
                results.append({"word": word, "found_1773": False,
                                "status": "not_found", "entries": []})

            # Save after every word so nothing is lost if the run is interrupted.
            Path(out_path).write_text(
                json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
            time.sleep(DELAY_BETWEEN_WORDS)  # HARD RULE 3

        browser.close()

    Path(out_path).write_text(
        json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
    found = sum(1 for r in results if r["found_1773"])
    print(f"\nDone. {found}/{len(results)} words had a 1773 entry. Saved to {out_path}")
    if problems:
        print(f"{len(problems)} words hit page problems.")
    return results


if __name__ == "__main__":
    LIB = Path("/home/noneya/Projects/VERITAS_MASTER_MERGE/03_LIBRARIES")
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        TEST_WORDS = ["commerce", "senate", "jury", "indictment", "habeas",
                      "bail", "freedom", "emolument", "militia", "arms"]
        run(TEST_WORDS, LIB / "johnson_1773_TEST_10.json", test_mode=True)
    else:
        print("Refusing to run the full list without an explicit driver. "
              "Use --test for the mandatory 10-word test.")
