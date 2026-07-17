"""
BLACKLETTER GATE — flag layer.  Spec: BLACKLETTER_GATE_SPEC.md (stage 4a / 6)

Flags are METADATA ABOUT a definition — they never touch the verbatim text. They
live in a SIDECAR (blackletter_flags.json), so the fixed library stays byte-for-
byte unchanged. A flagged term still ADMITS through the gate; the flag rides along
as a WARNING (compiler warning, not error). Void for Vagueness stays the only
error. Flags are freely adjustable after the fact — edit the sidecar, the library
never moves.

Detectors (read-only, no network, operate on existing entry data):
  abbreviated-capture   WARNING  early truncated capture (empty senses_1773) -- quotes dropped
  not-verified-1773     WARNING  verification_status is not 'verified_1773'
  multi-sense           INFO     2+ numbered senses -> sense-binding is an interpretive act
  etymology-pending     INFO     etymology slot empty (awaiting Skeat)
  founding-use-pending  INFO     no founding-era usage quotes on file
  multi-POS             INFO     combined part-of-speech entry (e.g. n.s.; v.a.)
"""
import json, re
from pathlib import Path

ROOT = Path("/home/noneya/Projects/VERITAS v.3")
LIB = ROOT / "02_GATE_BLACKLETTER" / "gate" / "VERITAS_definitions_library.json"
SIDECAR = ROOT / "02_GATE_BLACKLETTER" / "gate" / "blackletter_flags.json"
FLAG_LAYER_VERSION = "1"

_SENSE = re.compile(r'(?m)(?:^|\s)(\d+)\.\s')


def _src(e, role):
    return next((s for s in e.get("sources", []) if s.get("role") == role), None)


def detect(entry):
    """Return the list of flags for one entry. Pure function of existing data."""
    flags = []
    w = entry.get("word")

    # abbreviated = no structured senses AND short text. The length guard avoids
    # false positives: some full entries simply lack the senses_1773 array.
    if not entry.get("senses_1773") and len((entry.get("definition") or "").strip()) < 300:
        flags.append({"type": "abbreviated-capture", "severity": "warning",
                      "note": "early truncated capture — illustrative quotations may be missing; "
                              "re-capture from the 1773 folio for full verbatim text"})
    if entry.get("verification_status") != "verified_1773":
        flags.append({"type": "not-verified-1773", "severity": "warning",
                      "note": f"verification_status = {entry.get('verification_status')!r}"})
    if len(set(_SENSE.findall(entry.get("definition", "") or ""))) >= 2:
        flags.append({"type": "multi-sense", "severity": "info",
                      "note": "multiple numbered senses — which sense governs is an interpretive act "
                              "(sense-binding), not fixed by the gate"})
    s1 = _src(entry, "etymology")
    if not (s1 and s1.get("verbatim_text")):
        flags.append({"type": "etymology-pending", "severity": "info",
                      "note": "etymology slot empty (awaiting Skeat)"})
    s2 = _src(entry, "historical_usage")
    if not (s2 and s2.get("quotes")):
        flags.append({"type": "founding-use-pending", "severity": "info",
                      "note": "no founding-era usage quotes on file"})
    if ";" in (entry.get("part_of_speech") or ""):
        flags.append({"type": "multi-POS", "severity": "info",
                      "note": f"combined part-of-speech entry ({entry.get('part_of_speech')})"})
    return flags


def build_index(entries, library_version):
    index = {}
    counts = {}
    for e in entries:
        fl = detect(e)
        if fl:
            index[e["word"].lower()] = fl
            for f in fl:
                counts[f["type"]] = counts.get(f["type"], 0) + 1
    return {
        "flag_layer_version": FLAG_LAYER_VERSION,
        "library_version": library_version,
        "note": "Flag metadata layer. Does NOT modify the verbatim library. "
                "A flagged term still ADMITS; the flag rides along as a warning. "
                "Freely adjustable — edit here, the library never moves.",
        "counts": counts,
        "flagged_entries": len(index),
        "flags": index,
    }


def main():
    data = json.loads(LIB.read_text(encoding="utf-8"))
    entries = data["entries"]
    idx = build_index(entries, data.get("library_version"))
    SIDECAR.write_text(json.dumps(idx, ensure_ascii=False, indent=1), encoding="utf-8")
    n = len(entries)
    print(f"flag audit — library v{idx['library_version']}, {n} entries")
    print(f"library UNCHANGED (sidecar only): {SIDECAR.name}\n")
    for t, c in sorted(idx["counts"].items(), key=lambda x: -x[1]):
        sev = "WARNING" if t in ("abbreviated-capture", "not-verified-1773") else "info"
        print(f"  [{sev:7}] {t:22} {c:5}  ({100*c//n}%)")
    print(f"\n  entries with >=1 flag: {idx['flagged_entries']}  ({100*idx['flagged_entries']//n}%)"
          f"   clean: {n - idx['flagged_entries']}")


if __name__ == "__main__":
    main()
