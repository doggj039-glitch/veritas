"""
Drift pass #2: Black's Law Dictionary, 2nd ed. (1910) -- LEGAL register.
(VERITAS_DESIGN.md sections 2 & 4.)

Appends a Black's-1910 drift snapshot (register: legal) to every library entry
whose headword is a Black's term, then RE-SORTS each entry's drift snapshots into
publication order (Black's 1910 sits before Webster 1913). Baseline triad (seq 0-2)
stays fixed. Verbatim; provenance-tagged. Idempotent.

Source term text: public-domain Black's Law Dictionary, 2nd ed. (1910),
Henry Campbell Black. Transcription: LexPredict lexpredict-legal-dictionary
(CC-BY-SA-4.0), verbatim OCR (may contain scan artifacts).
File: 07_CAPTURE_TOOLS/sources_data/blacks_1910.json (columnar: term/definition/...).

Reads/Writes all FOUR library copies. Bumps library_version -> 3.4.
"""
import json, hashlib
from pathlib import Path

ROOT = Path("/home/noneya/Projects/VERITAS v.3")
LIBDIR = ROOT / "03_LIBRARIES"
GATE = ROOT / "02_GATE_BLACKLETTER"
BASE = LIBDIR / "VERITAS_definitions_library.json"
BLACKS = ROOT / "07_CAPTURE_TOOLS" / "sources_data" / "blacks_1910.json"
COPIES = [
    BASE,
    GATE / "gate" / "VERITAS_definitions_library.json",
    GATE / "engine" / "VERITAS_definitions_library.json",
    GATE / "nova_johnson" / "VERITAS_definitions_library.json",
]
PROVENANCE = ("Black's Law Dictionary, 2nd ed. (1910), Henry Campbell Black -- public-domain text; "
              "transcription via LexPredict (CC-BY-SA-4.0). Verbatim OCR; may contain scan artifacts.")


def load_blacks():
    d = json.loads(BLACKS.read_text(encoding="utf-8"))
    terms, defs = d["term"], d["definition"]
    blk = {}
    for i in terms:
        t = (terms[i] or "").strip().lower()
        df = (defs.get(i) or "").strip()
        if t and df:
            blk.setdefault(t, df)
    return blk


def resort_sources(sources):
    """Keep baseline (seq 0-2) fixed in role order; sort drift by year then source; renumber."""
    baseline = [s for s in sources if s.get("tier") == "baseline"]
    drift = [s for s in sources if s.get("tier") == "drift"]
    baseline.sort(key=lambda s: s.get("seq", 0))          # preserve johnson/etymology/historical order
    drift.sort(key=lambda s: (s.get("year", 9999), s.get("source", "")))
    out = baseline + drift
    for i, s in enumerate(out):
        s["seq"] = i
    return out


def main():
    lib = json.loads(BASE.read_text(encoding="utf-8"))
    entries = lib["entries"]
    blk = load_blacks()

    before_defs_md5 = hashlib.md5(
        json.dumps([e.get("definition", "") for e in entries], ensure_ascii=False).encode()).hexdigest()

    added = skipped_existing = no_blacks = 0
    for e in entries:
        srcs = e.setdefault("sources", [])
        if not any(s.get("role") == "blacks_1910" for s in srcs):
            text = blk.get(e["word"].lower())
            if text:
                srcs.append({
                    "seq": None, "tier": "drift", "role": "blacks_1910",
                    "source": "Black's Law Dictionary", "year": 1910, "register": "legal",
                    "verbatim_text": text, "show_default": False, "provenance": PROVENANCE,
                })
                added += 1
            else:
                no_blacks += 1
        else:
            skipped_existing += 1
        e["sources"] = resort_sources(srcs)   # always re-sort (also fixes any prior ordering)

    lib["library_version"] = "3.4"
    lib["last_updated"] = "2026-07-08"
    lib.setdefault("build_history", [])
    if isinstance(lib["build_history"], list):
        lib["build_history"].append(
            f"v3.4 (2026-07-08): drift pass #2 -- appended Black's Law Dictionary 1910 (LEGAL register) "
            f"drift snapshots to {added} entries ({no_blacks} not Black's terms; {skipped_existing} already had one). "
            "Drift re-sorted into publication order (Black's 1910 before Webster 1913). Baseline verbatim unchanged.")

    payload = json.dumps(lib, ensure_ascii=False, indent=1)
    for p in COPIES:
        p.write_text(payload, encoding="utf-8")

    # verification
    e2 = json.loads(BASE.read_text(encoding="utf-8"))["entries"]
    after_defs_md5 = hashlib.md5(
        json.dumps([e.get("definition", "") for e in e2], ensure_ascii=False).encode()).hexdigest()
    seq0_intact = all(e["sources"][0]["role"] == "johnson_1773"
                      and e["sources"][0]["verbatim_text"] == e["definition"] for e in e2)
    baseline_fixed = all([s["role"] for s in e["sources"][:3]] == ["johnson_1773", "etymology", "historical_usage"]
                         for e in e2)
    def drift_sorted(e):
        yrs = [s["year"] for s in e["sources"] if s.get("tier") == "drift"]
        return yrs == sorted(yrs)
    all_drift_sorted = all(drift_sorted(e) for e in e2)
    seqs_ok = all([s["seq"] for s in e["sources"]] == list(range(len(e["sources"]))) for e in e2)
    with_blacks = sum(1 for e in e2 if any(s.get("role") == "blacks_1910" for s in e["sources"]))
    with_both = sum(1 for e in e2 if any(s.get("role") == "blacks_1910" for s in e["sources"])
                    and any(s.get("role") == "webster_1913" for s in e["sources"]))
    md5s = {hashlib.md5(p.read_bytes()).hexdigest() for p in COPIES}

    print("entries:", len(e2))
    print("Black's 1910 legal snapshots added:", added)
    print("entries now carrying Black's 1910:", with_blacks, "| with BOTH Black's+Webster:", with_both)
    print("words not in Black's:", no_blacks)
    print("JOHNSON BASELINE INTACT (seq0 verbatim==definition):", seq0_intact)
    print("baseline triad still seq0-2 in order:", baseline_fixed)
    print("VERBATIM PRESERVED (definitions md5 unchanged):", before_defs_md5 == after_defs_md5)
    print("drift in publication order in every entry:", all_drift_sorted)
    print("seq numbering contiguous:", seqs_ok)
    print("all 4 copies identical:", len(md5s) == 1, "| new md5:", md5s.pop()[:12])


if __name__ == "__main__":
    main()
