"""
Fetch the core Anti-Federalist essays (public domain, 1787-88) from
teachingamericanhistory.org, extracting the clean articleBody from each page's
JSON-LD. Saves one text file per essay for provenance. Respectful: ~1s/request.
"""
import json, re, html, time, urllib.request
from pathlib import Path

HERE = Path(__file__).parent / "antifederalist"
SRC = HERE / "source"
SRC.mkdir(parents=True, exist_ok=True)

ROMAN = ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x",
         "xi", "xii", "xiii", "xiv", "xv", "xvi"]

# curated candidate slugs -> citation label. Non-existent ones 404 and are skipped.
R18 = ROMAN + ["xvii", "xviii"]
CANDIDATES = []
for r in ROMAN:
    CANDIDATES.append((f"brutus-{r}", f"Brutus {r.upper()}"))
for r in ROMAN[:7]:
    CANDIDATES.append((f"cato-{r}", f"Cato {r.upper()}"))
for r in R18:
    CANDIDATES.append((f"centinel-{r}", f"Centinel {r.upper()}"))
for r in R18:
    CANDIDATES.append((f"federal-farmer-{r}", f"Federal Farmer {r.upper()}"))
    CANDIDATES.append((f"letters-from-the-federal-farmer-{r}", f"Federal Farmer {r.upper()}"))
for r in R18:
    CANDIDATES.append((f"agrippa-{r}", f"Agrippa {r.upper()}"))
for r in ROMAN[:8]:
    CANDIDATES.append((f"an-old-whig-{r}", f"An Old Whig {r.upper()}"))
    CANDIDATES.append((f"old-whig-{r}", f"An Old Whig {r.upper()}"))

URL = "https://teachingamericanhistory.org/document/{}/"


def _clean(t):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", t))).strip()


# TAH site boilerplate that leaks into the old plain-<p> template
_FOOTER = re.compile(r"community of practice|teaching career|We provide a vibrant|"
                     r"Teaching American History|sign up|newsletter|stage of your teaching", re.I)


def article_body(html_text):
    """Extract the essay text. New template: <p class="wp-block-paragraph"> blocks.
    Old template (Brutus XI–XV): plain <p> blocks — keep essay-length ones and drop
    site-footer boilerplate."""
    paras = re.findall(r'<p class="wp-block-paragraph"[^>]*>(.*?)</p>', html_text, re.S)
    if paras:
        cleaned = [_clean(p) for p in paras]
    else:
        raw = re.findall(r"<p\b[^>]*>(.*?)</p>", html_text, re.S)
        cleaned = [_clean(p) for p in raw if len(re.sub(r"<[^>]+>", "", p).split()) >= 25]
    out = [c for c in cleaned if c and not _FOOTER.search(c)]
    return "\n\n".join(out) if out else None


def fetch(slug):
    req = urllib.request.Request(URL.format(slug), headers={"User-Agent": "VERITAS-research/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def main():
    got, seen_labels = [], set()
    for slug, label in CANDIDATES:
        if label in seen_labels:      # e.g. two Federal Farmer slug forms — take first that works
            continue
        try:
            page = fetch(slug)
        except Exception:
            continue
        body = article_body(page)
        if not body:
            continue
        if len(body.split()) < 300:   # nav/stub, not a real essay
            continue
        (SRC / f"{slug}.txt").write_text(f"{label}\n\n{body}", encoding="utf-8")
        got.append((label, len(body.split())))
        seen_labels.add(label)
        print(f"  ✓ {label:20} {len(body.split()):5} words  ({slug})")
        time.sleep(1.0)
    print(f"\nfetched {len(got)} essays, {sum(w for _, w in got)} words total -> {SRC}")


if __name__ == "__main__":
    main()
