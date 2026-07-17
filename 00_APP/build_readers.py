"""
Build offline READER pages — one per founding-era work — from the clean library text
(historical_documents.db). Each book card in the app links here so people can actually
READ the full text, offline. Verbatim; passages in document order.

Writes:  00_APP/books/<slug>.html   (one per work)
Prints:  the READ map (normalized leaf label -> slug) to wire into the app.
"""
import sqlite3, re, html, json
from pathlib import Path

ROOT = Path("/home/noneya/Projects/VERITAS v.3")
HIST = ROOT / "03_LIBRARIES" / "historical_documents.db"
OUT = ROOT / "00_APP" / "books"
OUT.mkdir(parents=True, exist_ok=True)

WORKS = [
    {"slug": "federalist-papers", "title": "The Federalist Papers", "cite": "Publius · 1787–88", "leaf": "The Federalist Papers", "prefix": ["The Federalist Papers"]},
    {"slug": "anti-federalist-papers", "title": "The Anti-Federalist Papers", "cite": "Brutus, Federal Farmer, et al. · 1787–88", "leaf": "The Anti-Federalist Papers", "prefix": ["The Anti-Federalist Papers"]},
    {"slug": "elliots-debates", "title": "Elliot’s Debates", "cite": "Jonathan Elliot · Vols. I–V", "leaf": "Elliot’s Debates", "prefix": ["Elliot's Debates"]},
    {"slug": "farrands-records", "title": "Farrand’s Records of the Federal Convention", "cite": "Max Farrand · Vols. I–III", "leaf": "Farrand’s Records", "prefix": ["Farrand's Records"]},
    {"slug": "madisons-notes", "title": "Madison’s Notes of the Federal Convention", "cite": "James Madison · 1787", "leaf": "Madison’s Notes of the Convention", "prefix": ["Madison's Notes"]},
    {"slug": "story-commentaries", "title": "Story, Commentaries on the Constitution", "cite": "Joseph Story · 1833 · Vols. I–III", "leaf": "Story, Commentaries on the Constitution", "prefix": ["Story, Commentaries"]},
    {"slug": "rawle-view", "title": "Rawle, A View of the Constitution", "cite": "William Rawle · 1825", "leaf": "Rawle, A View of the Constitution", "prefix": ["Rawle, A View"]},
    {"slug": "blackstone-commentaries", "title": "Blackstone’s Commentaries on the Laws of England", "cite": "William Blackstone · 1765–69 · Bks. I–IV", "leaf": "Blackstone’s Commentaries", "prefix": ["Blackstone, Commentaries"]},
    {"slug": "montesquieu-spirit", "title": "Montesquieu, The Spirit of the Laws", "cite": "1748 · Vols. I–IV", "leaf": "Montesquieu, The Spirit of the Laws", "prefix": ["Montesquieu, The Spirit"]},
    {"slug": "locke-essay", "title": "Locke, An Essay Concerning Human Understanding", "cite": "John Locke · 1689 · Vols. I–II", "leaf": "Locke, Essay Concerning Human Understanding", "prefix": ["Locke, An Essay"]},
]

STYLE = """
:root{--bg:#0c0e13;--surface:#12151d;--line:#282e3c;--ink:#e9e7dd;--ink-dim:#c3c7d2;--ink-mute:#79808f;--gold:#c9a24b;--gold-bright:#e6c877;--gold-soft:rgba(201,162,75,.13);
--serif:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif;--sans:ui-sans-serif,-apple-system,"Segoe UI",system-ui,sans-serif;--mono:ui-monospace,Menlo,Consolas,monospace}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--ink-dim);font-family:var(--serif);font-size:18px;line-height:1.75}
.bar{position:sticky;top:0;z-index:5;display:flex;align-items:center;gap:16px;padding:12px 22px;background:rgba(18,21,29,.94);border-bottom:1px solid var(--line);backdrop-filter:blur(6px)}
.bar a.back{font-family:var(--mono);font-size:12.5px;color:var(--gold-bright);text-decoration:none;border:1px solid var(--line);border-radius:7px;padding:6px 12px}
.bar a.back:hover{background:var(--gold-soft)}
.bar .wm{font-family:var(--serif);letter-spacing:.34em;text-indent:.34em;color:var(--gold);font-weight:600;font-size:15px;margin-left:auto}
header.doc{max-width:760px;margin:44px auto 8px;padding:0 26px}
header.doc h1{font-family:var(--serif);font-size:31px;color:var(--ink);margin:0 0 8px;line-height:1.2;text-wrap:balance}
header.doc .cite{font-family:var(--mono);font-size:13px;color:var(--gold)}
header.doc .note{margin-top:14px;font-family:var(--sans);font-size:12.5px;color:var(--ink-mute);border-top:1px solid var(--line);padding-top:14px}
main{max-width:760px;margin:0 auto 90px;padding:0 26px}
h2.vol{font-family:var(--sans);font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:var(--gold);margin:46px 0 6px;padding-top:20px;border-top:1px solid var(--line)}
p{margin:0 0 18px;max-width:66ch}
::selection{background:var(--gold-soft)}
::-webkit-scrollbar{width:11px}::-webkit-scrollbar-thumb{background:#2c3342;border-radius:20px}
.toc{font-family:var(--sans);font-size:13px;margin:10px 0 0;padding:0;list-style:none;display:flex;flex-wrap:wrap;gap:8px}
.toc a{color:var(--ink-dim);text-decoration:none;border:1px solid var(--line);border-radius:20px;padding:4px 11px}
.toc a:hover{color:var(--gold-bright);border-color:var(--gold-soft)}
"""


def natvol(ref):
    m = re.search(r"(?:Vol\.|Bk\.)\s*([IVX0-9]+)", ref)
    if not m:
        return 0
    r = m.group(1)
    if r.isdigit():
        return int(r)
    val = {"I": 1, "V": 5, "X": 10}
    tot, prev = 0, 0
    for ch in reversed(r):
        v = val.get(ch, 0)
        tot += -v if v < prev else v
        prev = max(prev, v)
    return tot


def build():
    con = sqlite3.connect(f"file:{HIST}?mode=ro", uri=True)
    rows = con.execute("SELECT rowid, ref, body FROM passages ORDER BY rowid").fetchall()
    con.close()
    read_map, report = {}, []
    for w in WORKS:
        sel = [r for r in rows if any(r[1].startswith(p) for p in w["prefix"])]
        if not sel:
            continue
        # group by ref (volume), order volumes naturally, passages by rowid
        by_ref = {}
        for rid, ref, body in sel:
            by_ref.setdefault(ref, []).append((rid, body))
        refs = sorted(by_ref, key=lambda r: (natvol(r), r))
        multi = len(refs) > 1
        toc = ""
        if multi:
            toc = '<ul class="toc">' + "".join(
                f'<li><a href="#v{i}">{html.escape(r)}</a></li>' for i, r in enumerate(refs)) + "</ul>"
        parts = [
            f'<div class="bar"><a class="back" href="../VERITAS.html">← Back to VERITAS</a><span class="wm">VERITAS</span></div>',
            f'<header class="doc"><h1>{html.escape(w["title"])}</h1><div class="cite">{html.escape(w["cite"])}</div>',
            '<div class="note">Verbatim public-domain text from the VERITAS library. Passages appear in document order; the source is archive.org OCR, so older texts may show scanning artifacts.</div>',
            toc, "</header>", "<main>"]
        npass = 0
        for i, ref in enumerate(refs):
            if multi:
                parts.append(f'<h2 class="vol" id="v{i}">{html.escape(ref)}</h2>')
            for rid, body in sorted(by_ref[ref]):
                parts.append("<p>" + html.escape(body) + "</p>")
                npass += 1
        parts.append("</main>")
        doc = (f"<!doctype html><html lang=en><head><meta charset=utf-8>"
               f"<meta name=viewport content='width=device-width,initial-scale=1'>"
               f"<title>{html.escape(w['title'])} — VERITAS</title><style>{STYLE}</style></head><body>"
               + "".join(parts) + "</body></html>")
        (OUT / f"{w['slug']}.html").write_text(doc, encoding="utf-8")
        read_map[re.sub(r"[^a-z0-9]+", "", w["leaf"].lower())] = w["slug"]
        report.append((w["title"], npass, len(doc) // 1024))
    (OUT / "_read_map.json").write_text(json.dumps(read_map, ensure_ascii=False))
    print(f"{'WORK':46}{'PASSAGES':>9}{'KB':>8}")
    for t, n, kb in report:
        print(f"{t[:46]:46}{n:>9}{kb:>8}")
    total = sum(kb for _, _, kb in report)
    print(f"\n{len(report)} reader pages · {total} KB total → 00_APP/books/")
    print("READ map:", json.dumps(read_map, ensure_ascii=False))


if __name__ == "__main__":
    build()
