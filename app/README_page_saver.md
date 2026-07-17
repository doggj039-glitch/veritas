# VERITAS — Page-Saver + Local-Only Answer System

A popup window for links, a manual **Save** button that strips a web page to
clean readable text and stores it locally, and a search that answers VERITAS
questions **only from what you've saved — no paid API, ever.**

## The pieces
| File | Job |
|---|---|
| `saved_sources/<year>/` | the one fixed home for every saved page |
| `app/link_viewer.py` | **native window — no browser engine.** Paste a link → it fetches + cleans → shows the exact text that will be saved → **Save This Page** / **Close** |
| `app/page_cleaner.py` | strips menus/ads/scripts/styling, keeps title + body text (fetch via `requests`, no browser) |
| `app/local_search.py` | answers a question from the saved files only — never calls out |

## Use it
**Fetch + save a page (the window):**
```
cd "~/Projects/VERITAS v.3/app"
python link_viewer.py                      # opens empty; paste a link + Fetch
python link_viewer.py "https://www.congress.gov/…"   # opens and fetches it
```
The window **shows you the cleaned text before you save** — that's your once-over.
Review it, then click **Save This Page**. It stores `saved_sources/2026/2026-07-17_title.txt`
with the source URL + date saved inside the file. (No browser, no Chromium — plain native Qt.)

**Ask a question (local only):**
```
python local_search.py  what does the coinage clause say
```
If nothing saved matches, it says so plainly — it does **not** call any API.

## Rules baked in
- **No paid API call** anywhere in this feature — `local_search.py` has no
  network code at all.
- **No auto-save** — cleaning only happens when you click Save.
- **Provenance is inseparable** — every saved file starts with `TITLE / SOURCE
  URL / DATE SAVED`, and the filename starts with the date.

## Honest limitation
Auto-cleaning nails article/text pages (news, statutes, .gov). On tool-heavy or
heavily-interactive pages it may keep too much or too little — so the window
shows you what it kept after each save. Eyeball the first several; if one comes
out wrong, just delete that `.txt` and re-save, or trim it by hand (it's plain
text).
