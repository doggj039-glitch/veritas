"""
BLACKLETTER GATE — stage 8: TEST.  Spec: BLACKLETTER_GATE_SPEC.md

The regression suite that locks the front end. It compiles a set of GOLDEN cases
through the gate and asserts the verdicts do not drift. If you change the library
or the gate code and a verdict moves, this catches it immediately.

Goldens are pinned to the library version they were established against
(EXPECTED_LIBRARY_VERSION). A version change is a prompt to re-review, not a
silent pass — the assertions still run, so a moved verdict fails loudly.

Run:  python3 blackletter_gate_tests.py           (exit 0 = all pass, 1 = failure)
"""
import sys
from pathlib import Path
from blackletter_gate import BlackletterGate
from blackletter_gate_case import resolve_case
import json

EXPECTED_LIBRARY_VERSION = "3.13"
CASE_FILE = Path("/home/noneya/Desktop/Blackletter/hypothetical-pamphlet-permit.json")

# Golden clause/term expectations. Each may specify:
#   expect_compiles : bool
#   must_admit      : terms that must be ADMITTED
#   must_void       : terms that must be VOID FOR VAGUENESS
#   must_contain    : {term: substring that must appear in that term's verbatim}
GOLDENS = [
    {"name": "1st-Amendment compiles",
     "input": "Congress shall make no law abridging the freedom of speech, or of the press",
     "expect_compiles": True,
     "must_admit": ["congress", "law", "abridging", "freedom", "speech", "press"]},

    {"name": "2nd-Amendment compiles",
     "input": "A well-regulated Militia, being necessary to the security of a free State, "
              "the right of the people to keep and bear Arms, shall not be infringed",
     "expect_compiles": True,
     "must_admit": ["militia", "necessary", "security", "state", "right", "people", "arms", "infringed"]},

    {"name": "reconcile gaps now admit",
     "input": "liberty infringe reprieve expressly",
     "expect_compiles": True,
     "must_admit": ["liberty", "infringe", "reprieve", "expressly"]},

    {"name": "liberty carries the 1773 political sense",
     "input": "liberty",
     "must_contain": {"liberty": "inordinate government"}},

    {"name": "modern Commerce-Clause vocabulary voids",
     "input": "Congress may regulate interstate commerce affecting the aggregate national economy",
     "expect_compiles": False,
     "must_admit": ["commerce", "regulate"],
     "must_void": ["interstate", "aggregate", "national", "economy"]},

    {"name": "modern administrative vocabulary voids",
     "input": "The administrative agency shall promulgate regulations governing greenhouse gas emissions",
     "expect_compiles": False,
     "must_void": ["administrative", "promulgate", "greenhouse", "emissions"]},

    {"name": "nonsense voids",
     "input": "floccinaucinihilipilification",
     "expect_compiles": False,
     "must_void": ["floccinaucinihilipilification"]},

    {"name": "root-retry admits inflections",
     "input": "regulating abridged governing",
     "expect_compiles": True,
     "must_admit": ["regulating", "abridged", "governing"]},

    {"name": "flag layer surfaces warnings (admit, not block)",
     "input": "ability liberty",
     "expect_compiles": True,                       # flags never block admission
     "must_admit": ["ability", "liberty"],
     "must_flag": {"ability": "abbreviated-capture", "liberty": "multi-sense"}},

    {"name": "core batch now full verbatim (speech restored)",
     "input": "speech",
     "must_contain": {"speech": "articulate utterance"}},
]


def check_golden(gate, g):
    rep = gate.compile(g["input"])
    admitted = {d.term for d in rep.diagnostics if d.status == "ADMITTED"}
    voided = set(rep.summary["void_terms"])
    verbatim = {d.term: (d.verbatim or "") for d in rep.diagnostics}
    flagtypes = {d.term: {f["type"] for f in (d.flags or [])} for d in rep.diagnostics}
    fails = []
    if "expect_compiles" in g and rep.compiles != g["expect_compiles"]:
        fails.append(f"compiles={rep.compiles}, expected {g['expect_compiles']} "
                     f"(void: {sorted(voided) or 'none'})")
    for t in g.get("must_admit", []):
        if t not in admitted:
            fails.append(f"'{t}' expected ADMITTED, was {'VOID' if t in voided else 'absent'}")
    for t in g.get("must_void", []):
        if t not in voided:
            fails.append(f"'{t}' expected VOID, was {'ADMITTED' if t in admitted else 'absent'}")
    for t, sub in g.get("must_contain", {}).items():
        if sub.lower() not in verbatim.get(t, "").lower():
            fails.append(f"'{t}' verbatim missing expected text '{sub}'")
    for t, ftype in g.get("must_flag", {}).items():
        if ftype not in flagtypes.get(t, set()):
            fails.append(f"'{t}' expected flag '{ftype}', had {sorted(flagtypes.get(t, set())) or 'none'}")
    return fails


def check_case_file(gate):
    """The pamphlet validation case: speech must ground and the Johnson placeholder
    must be filled."""
    fails = []
    if not CASE_FILE.exists():
        return ["SKIP", f"case file not found: {CASE_FILE}"]
    case = json.loads(CASE_FILE.read_text(encoding="utf-8"))
    resolved, resolutions = resolve_case(case, gate)
    if resolutions.get("speech", {}).get("status") != "ADMITTED":
        fails.append("'speech' expected ADMITTED in pamphlet case")
    step = next((s for s in resolved.get("chain", []) if s.get("step") == "check-original-definition"), {})
    if "PLACEHOLDER" in str(step.get("finding", "")):
        fails.append("check-original-definition still contains a PLACEHOLDER after gating")
    if "vocal words" not in str(step.get("finding", "")).lower():
        fails.append("filled finding missing the verbatim 1773 'speech' text")
    return fails


def main():
    gate = BlackletterGate()
    print(f"Blackletter gate regression suite")
    print(f"library v{gate.version} ({gate.count} terms) | goldens pinned to v{EXPECTED_LIBRARY_VERSION}")
    if gate.version != EXPECTED_LIBRARY_VERSION:
        print(f"  NOTE: library version changed ({EXPECTED_LIBRARY_VERSION} -> {gate.version}); "
              f"verdict changes below are expected to be reviewed.")
    print()

    total = passed = 0
    for g in GOLDENS + [{"name": "pamphlet validation case", "case": True}]:
        total += 1
        fails = check_case_file(gate) if g.get("case") else check_golden(gate, g)
        if fails and fails[0] == "SKIP":
            print(f"  ~ SKIP  {g['name']} — {fails[1]}")
            total -= 1
            continue
        if fails:
            print(f"  ✗ FAIL  {g['name']}")
            for f in fails:
                print(f"          - {f}")
        else:
            passed += 1
            print(f"  ✓ PASS  {g['name']}")

    print()
    print(f"RESULT: {passed}/{total} passed.")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
