"""
Drift pass #1: Webster's 1913 (VERITAS_DESIGN.md sections 2 & 4).

Appends a Webster's-1913 DRIFT snapshot (register: common) to every library entry
whose headword appears in Webster's, at the next seq slot (typically seq 3), with
show_default:false. Verbatim public-domain text; provenance-tagged. Idempotent:
skips any entry that already has a webster_1913 snapshot.

The Johnson baseline (seq 0) is NEVER touched -- verbatim guard checks the
definitions md5 is unchanged. This is additive.

Source: 07_CAPTURE_TOOLS/sources_data/webster1913.json (public domain,
matthewreagan/WebstersEnglishDictionary, 102,217 headwords).
Reads/Writes all FOUR active library copies. Bumps library_version -> 3.3.
"""
import json, hashlib
from pathlib import Path

ROOT = Path("/home/noneya/Projects/VERITAS v.3")
LIBDIR = ROOT / "03_LIBRARIES"
GATE = ROOT / "02_GATE_BLACKLETTER"
BASE = LIBDIR / "VERITAS_definitions_library.json"
WEBSTER = ROOT / "07_CAPTURE_TOOLS" / "sources_data" / "webster1913.json"
COPIES = [
    BASE,
    GATE / "gate" / "VERITAS_definitions_library.json",
    GATE / "engine" / "VERITAS_definitions_library.json",
    GATE / "nova_johnson" / "VERITAS_definitions_library.json",
]
PROVENANCE = "Webster's 1913 (public domain; matthewreagan/WebstersEnglishDictionary). Verbatim; not reworded."


def main():
    lib = json.loads(BASE.read_text(encoding="utf-8"))
    entries = lib["entries"]
    webster = json.loads(WEBSTER.read_text(encoding="utf-8"))
    webster_lc = {k.lower(): v for k, v in webster.items()}

    before_defs_md5 = hashlib.md5(
        json.dumps([e.get("definition", "") for e in entries], ensure_ascii=False).encode()).hexdigest()

    added = skipped_existing = no_webster = 0
    for e in entries:
        srcs = e.setdefault("sources", [])
        if any(s.get("role") == "webster_1913" for s in srcs):
            skipped_existing += 1
            continue
        text = webster_lc.get(e["word"].lower())
        if not text or not text.strip():
            no_webster += 1
            continue
        srcs.append({
            "seq": len(srcs), "tier": "drift", "role": "webster_1913",
            "source": "Webster", "year": 1913, "register": "common",
            "verbatim_text": text, "show_default": False, "provenance": PROVENANCE,
        })
        added += 1

    lib["library_version"] = "3.3"
    lib["last_updated"] = "2026-07-08"
    lib.setdefault("build_history", [])
    if isinstance(lib["build_history"], list):
        lib["build_history"].append(
            f"v3.3 (2026-07-08): drift pass #1 -- appended Webster's 1913 drift snapshots "
            f"(seq 3, register:common, show_default:false) to {added} entries "
            f"({no_webster} words absent from Webster; {skipped_existing} already had one). "
            "First visible drift point on the timeline. Johnson baseline verbatim unchanged.")

    payload = json.dumps(lib, ensure_ascii=False, indent=1)
    for p in COPIES:
        p.write_text(payload, encoding="utf-8")

    # verification
    lib2 = json.loads(BASE.read_text(encoding="utf-8"))
    e2 = lib2["entries"]
    after_defs_md5 = hashlib.md5(
        json.dumps([e.get("definition", "") for e in e2], ensure_ascii=False).encode()).hexdigest()
    seq0_intact = all(e["sources"][0]["role"] == "johnson_1773"
                      and e["sources"][0]["verbatim_text"] == e["definition"] for e in e2)
    with_drift = sum(1 for e in e2 if any(s.get("role") == "webster_1913" for s in e["sources"]))
    seqs_ok = all([s["seq"] for s in e["sources"]] == list(range(len(e["sources"]))) for e in e2)
    md5s = {hashlib.md5(p.read_bytes()).hexdigest() for p in COPIES}

    print("entries:", len(e2))
    print("Webster drift snapshots added this run:", added)
    print("entries now carrying a Webster 1913 drift point:", with_drift)
    print("words absent from Webster (no drift added):", no_webster)
    print("JOHNSON BASELINE INTACT (seq0 verbatim==definition):", seq0_intact)
    print("VERBATIM PRESERVED (definitions md5 unchanged):", before_defs_md5 == after_defs_md5)
    print("seq numbering contiguous in every entry:", seqs_ok)
    print("all 4 copies identical:", len(md5s) == 1, "| new md5:", md5s.pop()[:12])


if __name__ == "__main__":
    main()
