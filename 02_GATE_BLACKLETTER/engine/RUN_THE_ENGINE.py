"""
RUN THE ENGINE
==============

Watch the Blackletter engine decide five cases -- one for each kind of
disposition. Nothing here is wired into VERITAS. It is a safe, self-
contained demonstration of the rule-runner working on real rules and
your real sources.

You do not need to understand this file. Start it (the START HERE guide
tells you how) and read what it prints.
"""

from blackletter_engine import BlackletterEngine, render


# Five cases. Each is just DATA -- who acted, what they did, what they
# claimed, what it touched. This is exactly the shape you will write your
# own cases in.
CASES = [
    {
        "id": "case-pamphlet-permit",
        "ruleId": "speech-protection",
        "actor": "A town government, through its licensing office",
        "action": "Requires a paid permit before anyone may hand out political pamphlets on public streets",
        "claimedAuthority": "General police power to keep the streets orderly",
        "affectedObject": {"kind": "Right", "name": "Freedom of Speech"},
        "termsInvolved": ["speech"],
        "actionBurdens": True,
    },
    {
        "id": "case-repave-street",
        "ruleId": "speech-protection",
        "actor": "A town government",
        "action": "Repaves a public street",
        "claimedAuthority": "General power to maintain public roads",
        "affectedObject": {"kind": "None", "name": "(none)"},
        "termsInvolved": ["speech"],
    },
    {
        "id": "case-bulk-records",
        "ruleId": "speech-protection",
        "actor": "A federal agency",
        "action": "Collects citizens' personal records in bulk",
        "claimedAuthority": "An asserted interest in security",
        "affectedObject": {"kind": "Right", "name": "Right to Privacy"},
        "termsInvolved": ["privacy"],
    },
    {
        "id": "case-federal-local-matter",
        "ruleId": "enumerated-authority",
        "actor": "Congress",
        "action": "Directs how a town runs a purely local matter",
        "claimedAuthority": "A general federal power to promote the public good",
        "claimedAuthorityId": None,
        "affectedObject": {"kind": "Power", "name": "Reserved power"},
        "termsInvolved": ["power"],
    },
    {
        "id": "case-army-five-year",
        "ruleId": "enumerated-authority",
        "actor": "Congress",
        "action": "Appropriates money to raise and support armies for a five-year term",
        "claimedAuthority": "The power to raise and support armies",
        "claimedAuthorityId": "raise-and-support-armies",
        "armyAppropriationYears": 5,
        "affectedObject": {"kind": "Power", "name": "Army appropriation"},
        "termsInvolved": ["power"],
    },
]


def main():
    print("#" * 60)
    print("  THE BLACKLETTER ENGINE  --  five cases, five dispositions")
    print("#" * 60)
    print()

    engine = BlackletterEngine()
    print(f"  Rules loaded: {', '.join(engine.rules.keys())}")
    status = engine.gate.library_status()
    print(f"  Sources loaded through the gate: "
          f"{status['definitions_word_count']} definitions, "
          f"{status['etymology_word_count']} origins, "
          f"{status['historical_context_word_count']} notes.")
    print()

    for case in CASES:
        print(f"\n  CASE: {case['id']}")
        print(f"  {case['action']}")
        finding = engine.evaluate(case)
        print()
        print(render(finding))


if __name__ == "__main__":
    main()
