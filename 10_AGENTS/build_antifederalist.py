"""
Build the Anti-Federalist agent's compartment from the fetched essays
(10_AGENTS/antifederalist/source/*.txt — first line = citation label, rest = body).
Chunk into passages, index into an on-disk FTS5 corpus. One-time offline ingest.
"""
import re, sqlite3
from pathlib import Path

HERE = Path(__file__).parent / "antifederalist"
SRC = HERE / "source"
DB = HERE / "corpus.db"


def chunk(body, target=900):
    paras = [p.strip().replace("\n", " ") for p in re.split(r"\n\s*\n", body) if p.strip()]
    out, buf = [], ""
    for p in paras:
        if len(buf) + len(p) + 1 > target and buf:
            out.append(buf.strip()); buf = p
        else:
            buf = (buf + " " + p).strip()
    if buf:
        out.append(buf.strip())
    return out


def main():
    if DB.exists():
        DB.unlink()
    con = sqlite3.connect(DB)
    con.execute("CREATE VIRTUAL TABLE passages USING fts5("
                "ref UNINDEXED, title, body, tokenize='porter unicode61')")
    essays = sorted(SRC.glob("*.txt"))
    npass = 0
    labels = []
    for f in essays:
        text = f.read_text(encoding="utf-8")
        label, _, body = text.partition("\n")
        label = label.strip()
        labels.append(label)
        for passage in chunk(body.strip()):
            con.execute("INSERT INTO passages(ref, title, body) VALUES (?,?,?)",
                        (label, "", passage))
            npass += 1
    con.commit()
    size_kb = DB.stat().st_size // 1024
    con.close()
    print(f"essays ingested: {len(essays)} ({', '.join(labels)})")
    print(f"passages indexed: {npass}")
    print(f"corpus.db: {size_kb} KB on disk")


if __name__ == "__main__":
    main()
