"""Build the Ratification Debates agent corpus from Elliot's Debates (already
captured in 03_LIBRARIES/founding_sources/source). Same FTS5 compartment pattern."""
import re, sqlite3
from pathlib import Path

ROOT = Path("/home/noneya/Projects/VERITAS v.3")
SRC = ROOT / "03_LIBRARIES" / "founding_sources" / "source"
DB = ROOT / "10_AGENTS" / "ratification" / "corpus.db"
VOLS = {f"elliot_vol{n}.txt": f"Elliot's Debates, Vol. {n}" for n in range(1, 6)}


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
    n = 0
    for fn, ref in VOLS.items():
        p = SRC / fn
        if not p.exists():
            continue
        for passage in chunk(p.read_text(encoding="utf-8", errors="replace")):
            if len(passage) < 40:
                continue
            con.execute("INSERT INTO passages(ref, title, body) VALUES (?,?,?)", (ref, "", passage))
            n += 1
    con.commit()
    kb = DB.stat().st_size // 1024
    con.close()
    print(f"ratification corpus: {n} passages, {kb} KB")


if __name__ == "__main__":
    main()
