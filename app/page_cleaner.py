"""
VERITAS -- page_cleaner.py
Strip a web page down to clean, readable text (title + body), removing
navigation menus, ads, scripts, and layout/styling clutter. Keeps only the
readable article/body text plus the page title.

Triggered ONLY by the Save button (this module never auto-runs on its own).
NO paid API is ever contacted. The only network call is an explicit
clean_url() fetch when you don't already have the page HTML.

Entry points
------------
clean_html(html, url)            -> {title, text, kept_chars}
clean_url(url)                   -> {title, text, kept_chars, url}   (fetches then cleans)
save_cleaned(result, url, base)  -> Path   (writes ONE provenance-stamped file)

Realistic expectation (flagged to Susan before build): auto-cleaning works
well on article/text-heavy pages (news, statutes, .gov) and less well on
tool-heavy / heavily-interactive pages. The viewer shows what was kept after
each save so the first several can be eyeballed.
"""
from __future__ import annotations

import datetime
import re
from pathlib import Path

try:
    from bs4 import BeautifulSoup
except ImportError:  # pragma: no cover
    BeautifulSoup = None

# Tags that are never body content.
_STRIP_TAGS = [
    "script", "style", "noscript", "nav", "header", "footer", "aside",
    "form", "button", "iframe", "svg", "canvas", "input", "select",
    "textarea", "template", "figure",
]

# id/class/role hints that mark boilerplate blocks (menus, ads, share bars...).
_BOILERPLATE_HINT = re.compile(
    r"(nav|menu|sidebar|footer|header|comment|advert|promo|cookie|banner|"
    r"share|social|related|newsletter|subscribe|breadcrumb|pagination|masthead|"
    r"sponsor|widget|popup|modal)",
    re.I,
)


def _text_density(tag) -> float:
    """Score a block by how much *non-link* text it holds (menus are link-heavy)."""
    text = tag.get_text(" ", strip=True)
    if not text:
        return 0.0
    link_chars = sum(len(a.get_text(" ", strip=True)) for a in tag.find_all("a"))
    link_ratio = link_chars / max(len(text), 1)
    return len(text) * (1.0 - min(link_ratio, 0.95))


def _extract_title(soup, fallback: str = "") -> str:
    for name, attrs in (("meta", {"property": "og:title"}),
                        ("meta", {"name": "twitter:title"})):
        m = soup.find(name, attrs=attrs)
        if m and m.get("content"):
            return m["content"].strip()
    if soup.title and soup.title.string:
        return soup.title.string.strip()
    h1 = soup.find("h1")
    if h1:
        return h1.get_text(" ", strip=True)
    return (fallback or "untitled").strip()


def clean_html(html: str, url: str = "") -> dict:
    """Clean already-fetched page HTML into {title, text, kept_chars}."""
    if BeautifulSoup is None:
        raise RuntimeError(
            "beautifulsoup4 is required. Install: pip install beautifulsoup4 lxml")
    soup = BeautifulSoup(html, "lxml")
    title = _extract_title(soup, fallback=url)

    # 1) drop never-content tags outright
    for t in soup(_STRIP_TAGS):
        t.decompose()

    # 2) choose the main content container FIRST, so later cleanup can't lose it
    root = (soup.find("article") or soup.find("main")
            or soup.find(attrs={"role": "main"})
            or soup.body or soup)

    # 3) within that root, remove boilerplate blocks by id/class/role hint --
    #    but NEVER a block that holds most of the text (a false positive, e.g. a
    #    wrapper whose class merely contains "banner"/"widget"). Collect first,
    #    then remove (decomposing mid-iteration orphans children -> .attrs None).
    root_len = max(len(root.get_text(" ", strip=True)), 1)
    to_remove = []
    for tag in root.find_all(True):
        if not tag.attrs:
            continue
        ident = " ".join(filter(None, [
            tag.get("id", ""),
            " ".join(tag.get("class", []) or []),
            tag.get("role", ""),
        ]))
        if (ident and _BOILERPLATE_HINT.search(ident)
                and len(tag.get_text(" ", strip=True)) < 0.5 * root_len):
            to_remove.append(tag)
    for tag in to_remove:
        try:
            tag.decompose()
        except Exception:
            pass

    # 4) if root wasn't a semantic container, narrow to the densest text block
    if root.name in (None, "body", "html", "[document]"):
        best, best_score = None, 0.0
        for tag in root.find_all(["div", "section", "article"]):
            score = _text_density(tag)
            if score > best_score:
                best, best_score = tag, score
        if best is not None:
            root = best

    # 5) pull readable blocks in document order
    blocks = []
    for el in root.find_all(
            ["h1", "h2", "h3", "h4", "p", "li", "blockquote", "pre", "td"]):
        txt = el.get_text(" ", strip=True)
        if txt and len(txt) > 1:
            blocks.append(txt)
    text = "\n\n".join(blocks).strip()

    # 6) last-resort fallback: all readable text in root (never return empty)
    if len(text) < 200:
        text = re.sub(r"\n{3,}", "\n\n", root.get_text("\n", strip=True)).strip()

    return {"title": title, "text": text, "kept_chars": len(text)}


# Look like a real browser -- many sites (congress.gov, etc.) 403 a plain
# fetch that doesn't. These mirror what Firefox sends.
_BROWSER_HEADERS = {
    "User-Agent": ("Mozilla/5.0 (X11; Linux x86_64; rv:128.0) "
                   "Gecko/20100101 Firefox/128.0"),
    "Accept": ("text/html,application/xhtml+xml,application/xml;q=0.9,"
               "image/avif,image/webp,*/*;q=0.8"),
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
}


def clean_url(url: str, timeout: int = 25) -> dict:
    """Fetch a URL (no JS) and clean it. Sends real-browser headers so sites
    that block non-browser agents still work. Used by the viewer + the CLI."""
    import requests  # local import so importing this module needs no network stack
    sess = requests.Session()
    sess.headers.update(_BROWSER_HEADERS)
    resp = sess.get(url, timeout=timeout, allow_redirects=True)
    resp.raise_for_status()
    result = clean_html(resp.text, url)
    result["url"] = url
    return result


def _slug(s: str, maxlen: int = 60) -> str:
    s = re.sub(r"[^\w\s-]", "", s or "").strip().lower()
    s = re.sub(r"[\s_-]+", "-", s)
    return (s[:maxlen] or "untitled").strip("-") or "untitled"


def save_cleaned(result: dict, url: str, base_dir, when: datetime.date | None = None) -> Path:
    """
    Write ONE provenance-stamped file:
        saved_sources/<year>/<YYYY-MM-DD>_<title-slug>.txt

    The header ALWAYS carries TITLE / SOURCE URL / DATE SAVED so provenance
    can never be separated from the saved text. Never overwrites an existing
    file (appends -2, -3 ... on a same-day, same-title collision).
    """
    when = when or datetime.date.today()
    base_dir = Path(base_dir)
    year_dir = base_dir / str(when.year)
    year_dir.mkdir(parents=True, exist_ok=True)

    title = result.get("title") or "untitled"
    slug = _slug(title)
    path = year_dir / f"{when.isoformat()}_{slug}.txt"
    n = 2
    while path.exists():
        path = year_dir / f"{when.isoformat()}_{slug}-{n}.txt"
        n += 1

    header = (
        f"TITLE: {title}\n"
        f"SOURCE URL: {url}\n"
        f"DATE SAVED: {when.isoformat()}\n"
        + "=" * 70 + "\n\n"
    )
    path.write_text(header + (result.get("text") or ""), encoding="utf-8")
    return path


if __name__ == "__main__":  # simple CLI: clean + save a URL
    import sys
    if len(sys.argv) < 2:
        print('Usage: python page_cleaner.py "https://a-link" [saved_sources_dir]')
        raise SystemExit(1)
    _url = sys.argv[1]
    _base = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).resolve().parent.parent / "saved_sources"
    _res = clean_url(_url)
    _p = save_cleaned(_res, _url, _base)
    print(f"Saved {_res['kept_chars']:,} chars -> {_p}")
