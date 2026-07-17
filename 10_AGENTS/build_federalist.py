"""
Build the Federalist agent's compartment corpus: parse the Gutenberg text into
papers, chunk into passages, and index them into an on-disk FTS5 database.

This is the ONE-TIME offline ingest. At runtime the agent never re-reads the book
— it queries this index and pulls only the top-K matching passages (memory-flat).
"""
import re, sqlite3
from pathlib import Path

HERE = Path(__file__).parent / "federalist"
SRC = HERE / "source" / "federalist.txt"
DB = HERE / "corpus.db"

HEADER = re.compile(r"^FEDERALIST\s+No\.\s+(\d+)\s*$", re.MULTILINE)


def strip_gutenberg(text):
    a = text.find("*** START OF THE PROJECT GUTENBERG")
    if a != -1:
        text = text[text.find("\n", a) + 1:]
    b = text.find("*** END OF THE PROJECT GUTENBERG")
    if b != -1:
        text = text[:b]
    return text


def split_papers(text):
    """Return [(paper_no, title, body)] — real papers only (TOC entries filtered by length)."""
    parts = list(HEADER.finditer(text))
    papers = []
    for i, m in enumerate(parts):
        no = int(m.group(1))
        start = m.end()
        end = parts[i + 1].start() if i + 1 < len(parts) else len(text)
        body = text[start:end].strip()
        if len(body) < 1500:          # TOC line / stray header, not a real paper
            continue
        # first non-empty line after the header is the paper's title
        lines = [ln.strip() for ln in body.splitlines()]
        title = next((ln for ln in lines if ln), "")
        papers.append((no, title, body))
    # dedupe: keep the longest body per paper number (guards against any TOC leakage)
    best = {}
    for no, title, body in papers:
        if no not in best or len(body) > len(best[no][1]):
            best[no] = (title, body)
    return [(no, best[no][0], best[no][1]) for no in sorted(best)]


def chunk(body, target=900):
    """Merge paragraphs into ~target-char passages so retrieval is passage-level."""
    paras = [p.strip().replace("\n", " ") for p in re.split(r"\n\s*\n", body) if p.strip()]
    passages, buf = [], ""
    for p in paras:
        if len(buf) + len(p) + 1 > target and buf:
            passages.append(buf.strip()); buf = p
        else:
            buf = (buf + " " + p).strip()
    if buf:
        passages.append(buf.strip())
    return passages


def main():
    text = strip_gutenberg(SRC.read_text(encoding="utf-8", errors="replace"))
    papers = split_papers(text)

    if DB.exists():
        DB.unlink()
    con = sqlite3.connect(DB)
    con.execute("CREATE VIRTUAL TABLE passages USING fts5("
                "ref UNINDEXED, title, body, tokenize='porter unicode61')")
    npass = 0
    for no, title, body in papers:
        for passage in chunk(body):
            con.execute("INSERT INTO passages(ref, title, body) VALUES (?,?,?)",
                        (f"Federalist No. {no}", title, passage))
            npass += 1
    con.commit()
    size_kb = DB.stat().st_size // 1024
    con.close()
    print(f"papers parsed: {len(papers)} (No. {papers[0][0]}..{papers[-1][0]})")
    print(f"passages indexed: {npass}")
    print(f"corpus.db: {size_kb} KB on disk  (queried, never fully loaded)")
    print(f"sample titles: " + " | ".join(f'No.{n} \"{t[:30]}\"' for n, t, _ in papers[:3]))


if __name__ == "__main__":
    main()
