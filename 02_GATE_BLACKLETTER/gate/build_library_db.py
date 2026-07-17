#!/usr/bin/env python3
"""Convert the Johnson definitions library JSON -> on-disk SQLite (word-indexed).

Lets the gate query one word at a time instead of loading the whole 89 MB library
into RAM — the enabling change for the Android/phone edition, and a faster desktop
startup as a bonus. Non-destructive: writes a sibling .db; the .json stays as-is.
Re-run this whenever the library JSON changes.
"""
import json, sqlite3, os
from pathlib import Path

SRC = Path(__file__).with_name("VERITAS_definitions_library.json")
DST = SRC.with_suffix(".db")

def main():
    data = json.loads(SRC.read_text(encoding="utf-8"))
    entries = data["entries"]
    tmp = str(DST) + ".tmp"
    if os.path.exists(tmp):
        os.remove(tmp)
    con = sqlite3.connect(tmp)
    con.execute("PRAGMA journal_mode=OFF")
    con.execute("PRAGMA synchronous=OFF")
    con.execute("CREATE TABLE entries(word TEXT PRIMARY KEY, json TEXT)")
    con.execute("CREATE TABLE meta(key TEXT PRIMARY KEY, value TEXT)")
    rows = []
    for e in entries:
        w = (e.get("word") or "").strip().lower()
        if not w:
            continue
        rows.append((w, json.dumps(e, ensure_ascii=False)))
    con.executemany("INSERT OR REPLACE INTO entries(word, json) VALUES(?, ?)", rows)
    con.execute("INSERT OR REPLACE INTO meta VALUES('library_version', ?)", (str(data.get("library_version") or ""),))
    con.execute("INSERT OR REPLACE INTO meta VALUES('total_entries', ?)", (str(len(rows)),))
    con.commit()
    n = con.execute("SELECT COUNT(*) FROM entries").fetchone()[0]
    con.close()
    os.replace(tmp, DST)
    print("built", DST.name, "| entries:", n, "| version:", data.get("library_version"))

if __name__ == "__main__":
    main()
