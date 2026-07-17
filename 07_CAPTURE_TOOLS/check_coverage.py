#!/usr/bin/env python3
"""
check_coverage.py -- pre-flight VERIFIER for VERITAS.

Give it keywords; it reports which of your preloaded sources actually have each
word, BEFORE you spend time capturing. Sources live in sources.json (a registry
you preload/edit). Two kinds:
  - offline_library / offline_index : instant local lookup, zero network.
  - ajax_probe                      : bounded, respectful live existence-ping
                                      (>=1.5s delay). Never a bulk harvest --
                                      see [[veritas-scraping-boundary]].

Usage:
  python3 check_coverage.py apportion habeas emolument
  python3 check_coverage.py --file words.txt
  python3 check_coverage.py apportion --json out.json
"""
import sys, json, time, argparse, urllib.request, urllib.parse
from pathlib import Path

HERE = Path(__file__).parent
REGISTRY = HERE / "sources.json"


def load_registry():
    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    return [s for s in reg["sources"] if s.get("enabled")]


def load_offline_words(src):
    """Return a lowercased set of headwords for an offline source, or None if unreadable."""
    p = (HERE / src["path"]).resolve() if src.get("path") else None
    if not p or not p.exists():
        return None
    try:
        raw = p.read_text(encoding="utf-8")
    except Exception:
        return None
    if src["type"] == "offline_library":
        data = json.loads(raw)
        return {e["word"].lower() for e in data.get("entries", [])}
    # offline_index: JSON list, or newline-delimited word list
    txt = raw.strip()
    if txt.startswith("["):
        return {str(w).lower() for w in json.loads(txt)}
    return {ln.strip().lower() for ln in txt.splitlines() if ln.strip() and not ln.startswith("#")}


def ajax_probe(src, word):
    """Bounded existence-ping. Returns (found:bool, detail:str)."""
    data = urllib.parse.urlencode({
        "searchterm": word, "query": "headword",
        "searchYear": src.get("search_year", "1773"),
    }).encode()
    req = urllib.request.Request(
        src["endpoint"], data=data,
        headers={"User-Agent": "Mozilla/5.0", "X-Requested-With": "XMLHttpRequest"})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            body = json.loads(r.read().decode("utf-8", "replace"))
    except Exception as e:
        return None, f"err:{type(e).__name__}"
    files = body.get("filenames") or []
    if not files:
        return False, ""
    labels = body.get("labels") or []
    return True, "; ".join(labels[:3])


def check(words, sources):
    # preload offline sets once
    offline = {}
    for s in sources:
        if s["type"] in ("offline_library", "offline_index"):
            offline[s["key"]] = load_offline_words(s)

    rows = []
    for w in words:
        wl = w.lower()
        cells = {}
        in_lib = False
        # offline first (free, instant)
        for s in sources:
            if s["key"] in offline:
                wordset = offline[s["key"]]
                if wordset is None:
                    cells[s["key"]] = ("na", "not installed")
                else:
                    hit = wl in wordset
                    cells[s["key"]] = ("yes", "") if hit else ("no", "")
                    if s["type"] == "offline_library" and hit:
                        in_lib = True
        # ajax probes (bounded, respectful)
        for s in sources:
            if s["type"] != "ajax_probe":
                continue
            if s.get("skip_if_in_library") and in_lib:
                cells[s["key"]] = ("skip", "already in library")
                continue
            found, detail = ajax_probe(s, w)
            if found is None:
                cells[s["key"]] = ("err", detail)
            else:
                cells[s["key"]] = ("yes", detail) if found else ("no", "")
            time.sleep(float(s.get("delay_seconds", 1.5)))
        rows.append({"word": w, "cells": cells, "in_library": in_lib})
    return rows


GLYPH = {"yes": "✓", "no": "✗", "na": "·", "skip": "=", "err": "!"}


def print_matrix(rows, sources):
    keys = [s["key"] for s in sources]
    labels = {s["key"]: s["label"] for s in sources}
    wcol = max([4] + [len(r["word"]) for r in rows])
    header = "word".ljust(wcol) + "  " + "  ".join(k[:12].center(12) for k in keys)
    print(header)
    print("-" * len(header))
    for r in rows:
        line = r["word"].ljust(wcol) + "  "
        line += "  ".join(GLYPH[r["cells"][k][0]].center(12) for k in keys)
        print(line)
    print("-" * len(header))
    print("legend: ✓ has it   ✗ absent   = already in library (probe skipped)   · source not installed   ! error")
    print("sources:")
    for s in sources:
        print(f"  {s['key']:16} {labels[s['key']]}")
    # worth-capturing hint
    worth = [r["word"] for r in rows if not r["in_library"]
             and any(r["cells"][k][0] == "yes" for k in keys)]
    dead = [r["word"] for r in rows if not r["in_library"]
            and all(r["cells"][k][0] in ("no", "na", "err") for k in keys)]
    print()
    print(f"WORTH CAPTURING (not in library, found somewhere): {len(worth)}  {worth[:20]}")
    print(f"DEAD ENDS (not in library, found nowhere -- skip): {len(dead)}  {dead[:20]}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("words", nargs="*")
    ap.add_argument("--file", help="newline-delimited word list")
    ap.add_argument("--json", help="write full report to this path")
    args = ap.parse_args()

    words = list(args.words)
    if args.file:
        words += [ln.strip() for ln in Path(args.file).read_text().splitlines() if ln.strip()]
    words = list(dict.fromkeys(words))  # dedupe, keep order
    if not words:
        ap.error("give words on the command line or via --file")

    sources = load_registry()
    rows = check(words, sources)
    print_matrix(rows, sources)

    if args.json:
        Path(args.json).write_text(json.dumps(
            {"words": len(words),
             "sources": [s["key"] for s in sources],
             "results": rows}, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"\nreport -> {args.json}")


if __name__ == "__main__":
    main()
