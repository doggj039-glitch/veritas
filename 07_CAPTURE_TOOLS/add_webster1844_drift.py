"""
Drift pass #4: Webster's Dictionary (1844) -- COMMON register.
Tightens the 1828 -> 1910 cadence gap. (VERITAS_DESIGN.md sections 2 & 4.)

Appends a Webster-1844 drift snapshot to every library entry whose headword is a
(cleaned) 1844 term, then re-sorts each entry's drift into publication order:
Webster 1828 -> Webster 1844 -> Black's 1910 -> Webster 1913. Baseline (seq 0-2)
stays fixed. Verbatim; provenance-tagged. Idempotent.

Source text: public-domain Webster's 1844, transcription DataWar/1828-dictionary
(1828.mshaffer.com / Gutenberg). Parsed from webster1844.sql (8-col schema),
HTML stripped, junk-filtered. Cleaned map:
07_CAPTURE_TOOLS/sources_data/webster1844.json (73,217 headwords).

Reads/Writes all FOUR library copies. Bumps library_version -> 3.6.
"""
import json, hashlib
from pathlib import Path

ROOT = Path("/home/noneya/Projects/VERITAS v.3")
LIBDIR = ROOT / "03_LIBRARIES"
GATE = ROOT / "02_GATE_BLACKLETTER"
BASE = LIBDIR / "VERITAS_definitions_library.json"
W1844 = ROOT / "07_CAPTURE_TOOLS" / "sources_data" / "webster1844.json"
COPIES = [
    BASE,
    GATE / "gate" / "VERITAS_definitions_library.json",
    GATE / "engine" / "VERITAS_definitions_library.json",
    GATE / "nova_johnson" / "VERITAS_definitions_library.json",
]
PROVENANCE = ("Webster's Dictionary (1844), Noah Webster -- public-domain text; transcription "
              "DataWar/1828-dictionary (1828.mshaffer.com / Project Gutenberg). HTML stripped; "
              "junk-filtered. Verbatim.")


def resort_sources(sources):
    baseline = sorted([s for s in sources if s.get("tier") == "baseline"], key=lambda s: s.get("seq", 0))
    drift = sorted([s for s in sources if s.get("tier") == "drift"],
                   key=lambda s: (s.get("year", 9999), s.get("source", "")))
    out = baseline + drift
    for i, s in enumerate(out):
        s["seq"] = i
    return out


def main():
    lib = json.loads(BASE.read_text(encoding="utf-8"))
    entries = lib["entries"]
    w1844 = json.loads(W1844.read_text(encoding="utf-8"))

    before_defs_md5 = hashlib.md5(
        json.dumps([e.get("definition", "") for e in entries], ensure_ascii=False).encode()).hexdigest()

    added = skipped_existing = absent = 0
    for e in entries:
        srcs = e.setdefault("sources", [])
        if not any(s.get("role") == "webster_1844" for s in srcs):
            text = w1844.get(e["word"].lower())
            if text and text.strip():
                srcs.append({
                    "seq": None, "tier": "drift", "role": "webster_1844",
                    "source": "Webster", "year": 1844, "register": "common",
                    "verbatim_text": text, "show_default": False, "provenance": PROVENANCE,
                })
                added += 1
            else:
                absent += 1
        else:
            skipped_existing += 1
        e["sources"] = resort_sources(srcs)

    lib["library_version"] = "3.6"
    lib["last_updated"] = "2026-07-08"
    lib.setdefault("build_history", [])
    if isinstance(lib["build_history"], list):
        lib["build_history"].append(
            f"v3.6 (2026-07-08): drift pass #4 -- appended Webster's 1844 (common) drift snapshots to "
            f"{added} entries ({absent} absent; {skipped_existing} already had one). Tightens 1828->1910 "
            "cadence. Drift re-sorted (1828->1844->1910->1913). Baseline verbatim unchanged.")

    payload = json.dumps(lib, ensure_ascii=False, indent=1)
    for p in COPIES:
        p.write_text(payload, encoding="utf-8")

    e2 = json.loads(BASE.read_text(encoding="utf-8"))["entries"]
    after_defs_md5 = hashlib.md5(
        json.dumps([e.get("definition", "") for e in e2], ensure_ascii=False).encode()).hexdigest()
    seq0_intact = all(e["sources"][0]["role"] == "johnson_1773"
                      and e["sources"][0]["verbatim_text"] == e["definition"] for e in e2)
    baseline_fixed = all([s["role"] for s in e["sources"][:3]] == ["johnson_1773", "etymology", "historical_usage"]
                         for e in e2)
    all_drift_sorted = all([s["year"] for s in e["sources"] if s.get("tier") == "drift"] ==
                           sorted(s["year"] for s in e["sources"] if s.get("tier") == "drift") for e in e2)
    seqs_ok = all([s["seq"] for s in e["sources"]] == list(range(len(e["sources"]))) for e in e2)
    with_1844 = sum(1 for e in e2 if any(s.get("role") == "webster_1844" for s in e["sources"]))
    n4 = sum(1 for e in e2 if len([s for s in e["sources"] if s.get("tier") == "drift"]) >= 4)
    no_junk = not any("please check your spelling" in (s.get("verbatim_text", "").lower())
                      for e in e2 for s in e["sources"])
    md5s = {hashlib.md5(p.read_bytes()).hexdigest() for p in COPIES}

    print("entries:", len(e2))
    print("Webster 1844 snapshots added:", added, "| absent:", absent)
    print("entries now carrying Webster 1844:", with_1844)
    print("entries with 4+ drift points (1828/1844/1910/1913):", n4)
    print("JOHNSON BASELINE INTACT:", seq0_intact, "| baseline triad seq0-2:", baseline_fixed)
    print("VERBATIM PRESERVED (definitions md5 unchanged):", before_defs_md5 == after_defs_md5)
    print("drift in publication order:", all_drift_sorted, "| seq contiguous:", seqs_ok)
    print("no scrape-error text anywhere:", no_junk)
    print("all 4 copies identical:", len(md5s) == 1, "| new md5:", md5s.pop()[:12])


if __name__ == "__main__":
    main()
