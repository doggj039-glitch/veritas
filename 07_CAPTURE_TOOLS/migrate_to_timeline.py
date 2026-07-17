"""
Timeline-schema migration (VERITAS_DESIGN.md section 4).

Converts each single-`definition` entry into the drift timeline WITHOUT touching
the verbatim Johnson text: it ADDS an ordered `sources[]` list to every entry and
leaves all existing fields in place (additive + reversible).

Baseline triad written now (seq 0-2, show_default:true):
  seq 0  johnson_1773     <- entry["definition"] (verbatim, unchanged)
  seq 1  etymology        <- entry["etymology"] if present, else first [..] bracket
                             in the Johnson text; empty slot marked pending (Skeat).
  seq 2  historical_usage <- founding-era quotes from constitutional_usage_database.json
                             if the word is covered; empty slot marked pending otherwise.

Drift snapshots (seq 3+, Webster/Black's/OED) are appended by LATER passes; this
pass establishes the structure and the baseline only.

Reads/Writes: all FOUR active VERITAS_definitions_library.json copies (identically).
Bumps library_version -> 3.2 (timeline schema).
"""
import json, re, hashlib
from pathlib import Path

ROOT = Path("/home/noneya/Projects/VERITAS v.3")
LIBDIR = ROOT / "03_LIBRARIES"
GATE = ROOT / "02_GATE_BLACKLETTER"
BASE = LIBDIR / "VERITAS_definitions_library.json"
CUD = LIBDIR / "constitutional_usage_database.json"
COPIES = [
    BASE,
    GATE / "gate" / "VERITAS_definitions_library.json",
    GATE / "engine" / "VERITAS_definitions_library.json",
    GATE / "nova_johnson" / "VERITAS_definitions_library.json",
]
BRACKET = re.compile(r"\[[^\]]{1,120}\]")


def extract_etymology(entry):
    ety = (entry.get("etymology") or "").strip()
    if ety:
        return ety, "Johnson (etymology field)"
    d = entry.get("definition") or ""
    m = BRACKET.search(d[:200])
    if m:
        return m.group(0), "Johnson (bracketed etymology, derived)"
    return "", None


def main():
    lib = json.loads(BASE.read_text(encoding="utf-8"))
    entries = lib["entries"]
    cud = json.loads(CUD.read_text(encoding="utf-8")).get("entries", {})
    cud_lc = {w.lower(): v for w, v in cud.items()}

    # verbatim guard: definitions must be byte-identical after migration
    before_defs_md5 = hashlib.md5(
        json.dumps([e.get("definition", "") for e in entries], ensure_ascii=False).encode()).hexdigest()

    n_ety = n_ety_bracket = n_hist = 0
    for e in entries:
        w = e["word"]; wl = w.lower()

        seq0 = {
            "seq": 0, "tier": "baseline", "role": "johnson_1773",
            "source": "Johnson", "year": e.get("year", 1773), "register": "common",
            "verbatim_text": e["definition"], "show_default": True,
        }
        if e.get("part_of_speech"):
            seq0["part_of_speech"] = e["part_of_speech"]
        if e.get("senses_1773"):
            seq0["senses"] = e["senses_1773"]

        ety_text, ety_src = extract_etymology(e)
        seq1 = {
            "seq": 1, "tier": "baseline", "role": "etymology",
            "source": ety_src or "pending", "register": "etymology",
            "verbatim_text": ety_text, "show_default": True,
        }
        if ety_text:
            n_ety += 1
            if ety_src and ety_src.startswith("Johnson (bracketed"):
                n_ety_bracket += 1
        else:
            seq1["pending"] = "no etymology yet; add from Skeat's Etymological Dictionary"

        seq2 = {
            "seq": 2, "tier": "baseline", "role": "historical_usage",
            "source": "constitutional_usage_database", "register": "usage",
            "show_default": True, "quotes": [],
        }
        hit = cud_lc.get(wl)
        if hit and isinstance(hit, dict) and hit.get("usage"):
            quotes = []
            for u in hit["usage"]:
                if not isinstance(u, dict):
                    continue
                quotes.append({k: u[k] for k in ("quote", "source", "context") if k in u})
            seq2["quotes"] = quotes
            seq2["quote_count"] = hit.get("quote_count", len(quotes))
            if quotes:
                n_hist += 1
        else:
            seq2["pending"] = "no founding-era usage on file for this word"

        e["sources"] = [seq0, seq1, seq2]

    # metadata
    lib["library_version"] = "3.2"
    lib["last_updated"] = "2026-07-08"
    lib["schema"] = ("Per-word drift timeline (VERITAS_DESIGN.md s4): entry['sources'] is an ordered "
                     "list; seq 0-2 = baseline triad (johnson_1773, etymology, historical_usage; "
                     "show_default:true); seq 3+ = drift snapshots in publication order (show_default:false). "
                     "Legacy top-level fields (definition, etymology, ...) retained; sources[0].verbatim_text "
                     "mirrors 'definition' verbatim.")
    lib.setdefault("build_history", [])
    if isinstance(lib["build_history"], list):
        lib["build_history"].append(
            "v3.2 (2026-07-08): timeline-schema migration -- added ordered sources[] to all "
            f"{len(entries)} entries. Baseline triad populated: {n_ety} etymologies "
            f"({n_ety_bracket} derived from Johnson brackets), {n_hist} words with founding-era usage. "
            "Verbatim Johnson text unchanged (definitions md5 preserved). Drift snapshots deferred.")

    payload = json.dumps(lib, ensure_ascii=False, indent=1)
    for p in COPIES:
        p.write_text(payload, encoding="utf-8")

    # verification
    lib2 = json.loads(BASE.read_text(encoding="utf-8"))
    e2 = lib2["entries"]
    after_defs_md5 = hashlib.md5(
        json.dumps([e.get("definition", "") for e in e2], ensure_ascii=False).encode()).hexdigest()
    all_have_triad = all(len(e.get("sources", [])) >= 3 for e in e2)
    seq0_mirrors = all(e["sources"][0]["verbatim_text"] == e["definition"] for e in e2)
    md5s = {hashlib.md5(p.read_bytes()).hexdigest() for p in COPIES}

    print("entries:", len(e2))
    print("VERBATIM PRESERVED (definitions md5 unchanged):", before_defs_md5 == after_defs_md5)
    print("every entry has baseline triad (>=3 sources):", all_have_triad)
    print("seq0.verbatim_text mirrors 'definition' exactly:", seq0_mirrors)
    print(f"etymology populated: {n_ety}/{len(e2)}  ({n_ety_bracket} from Johnson brackets)")
    print(f"historical usage populated: {n_hist}/{len(e2)}")
    print("all 4 copies identical:", len(md5s) == 1, "| new md5:", md5s.pop()[:12])


if __name__ == "__main__":
    main()
