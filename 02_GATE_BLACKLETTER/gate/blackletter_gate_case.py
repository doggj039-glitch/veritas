"""
BLACKLETTER GATE — validation-case bridge (v0).

Runs a Blackletter validation case (e.g. hypothetical-pamphlet-permit.json)
through the gate: every term in `originalTermsInvolved` is resolved against the
live 1773 library, and the case's "PLACEHOLDER pending verified Johnson's-
dictionary text" findings are filled with the real verbatim definition +
provenance — or flagged Void for Vagueness if the term isn't grounded.

This is the concrete wiring the case's check-original-definition step was
waiting on. It does NOT re-adjudicate the case; it only supplies the grounded
founding-era meaning that the legal reasoning depends on.

Usage:
  python3 blackletter_gate_case.py <case.json> [--write <out.json>]
"""
import json, sys
from pathlib import Path
from blackletter_gate import BlackletterGate, CONTROLLING_SOURCE

PLACEHOLDER_MARK = "PLACEHOLDER"


def resolve_case(case, gate):
    terms = list(dict.fromkeys(case.get("originalTermsInvolved", [])))
    resolutions = {t: gate.resolve(t) for t in terms}

    # 1) attach a machine-readable gate block
    case["gateResolution"] = {
        t: ({"status": r["status"],
             "source": CONTROLLING_SOURCE,
             "verbatim": r["controlling"]["verbatim"],
             "grounding": r["grounding"]}
            if r["status"] == "ADMITTED"
            else {"status": r["status"], "reason": r["reason"]})
        for t, r in resolutions.items()
    }

    # 2) fill the check-original-definition placeholder in the chain
    for step in case.get("chain", []):
        if step.get("step") == "check-original-definition" and PLACEHOLDER_MARK in str(step.get("finding", "")):
            step["finding"] = _finding_text(terms, resolutions, step.get("finding", ""))
            step["gated"] = True

    # 3) fill driftFinding.originalPublicMeaning
    df = case.get("driftFinding")
    if isinstance(df, dict) and PLACEHOLDER_MARK in str(df.get("originalPublicMeaning", "")):
        primary = terms[0] if terms else None
        r = resolutions.get(primary)
        if r and r["status"] == "ADMITTED":
            df["originalPublicMeaning"] = (
                f"'{primary}' — {CONTROLLING_SOURCE}, verbatim: "
                f"{_first_sense(r['controlling']['verbatim'])}")
        elif r:
            df["originalPublicMeaning"] = f"Void for Vagueness — '{primary}' has no verbatim 1773 authority on file."

    return case, resolutions


def _first_sense(verbatim):
    """The headword line + sense 1, for a compact drift note."""
    return " ".join(verbatim.split("\n")[:3]).strip()


def _finding_text(terms, resolutions, original):
    parts = []
    for t in terms:
        r = resolutions[t]
        if r["status"] == "ADMITTED":
            parts.append(f"'{t}' GROUNDED — {CONTROLLING_SOURCE} defines it verbatim: "
                         f"\"{r['controlling']['verbatim'].strip()}\" "
                         f"[Blackletter gate: ADMITTED, grounding={r['grounding']}].")
        else:
            parts.append(f"'{t}' VOID FOR VAGUENESS — {r['reason']} "
                         f"[Blackletter gate blocks reasoning on an ungrounded term].")
    # keep the author's provisional legal reading, minus the PLACEHOLDER hedge
    tail = original.split("—", 1)[-1].strip() if "—" in original else ""
    tail = tail.replace("needs confirmation once source text is loaded.", "").strip()
    if tail.lower().startswith("provisionally"):
        parts.append("Grounded reading: " + tail)
    return " ".join(parts)


def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    case_path = Path(sys.argv[1])
    case = json.loads(case_path.read_text(encoding="utf-8"))
    gate = BlackletterGate()

    resolved, resolutions = resolve_case(case, gate)

    print(f"CASE: {case.get('id')}")
    print(f"gate: library v{gate.version}, {gate.count} grounded terms\n")
    print("ORIGINAL TERMS THROUGH THE GATE:")
    for t, r in resolutions.items():
        if r["status"] == "ADMITTED":
            print(f"  [ADMITTED] {t}  <{r['grounding']}>")
            print(f"      {CONTROLLING_SOURCE}:")
            for line in r["controlling"]["verbatim"].split("\n")[:4]:
                if line.strip():
                    print(f"        {line.strip()}")
        else:
            print(f"  [VOID FOR VAGUENESS] {t} — {r['reason']}")
    print()
    admitted = sum(1 for r in resolutions.values() if r["status"] == "ADMITTED")
    print(f"RESULT: {admitted}/{len(resolutions)} original terms grounded in Johnson 1773.")
    print(f"        check-original-definition placeholder: "
          f"{'FILLED' if all(r['status']=='ADMITTED' for r in resolutions.values()) else 'PARTIALLY / VOIDED'}.")
    print(f"        case disposition ({case.get('finalResult')}) unchanged — the gate supplies grounding, not the verdict.")

    if "--write" in sys.argv:
        out = Path(sys.argv[sys.argv.index("--write") + 1])
        out.write_text(json.dumps(resolved, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\nresolved case -> {out}")


if __name__ == "__main__":
    main()
