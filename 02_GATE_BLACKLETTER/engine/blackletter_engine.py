"""
THE BLACKLETTER ENGINE  --  the rule-runner
===========================================

This is the heart of Blackletter. You hand it a CASE -- who acted, what
they did, what authority they claimed, and what right or power it touched
-- and it runs that case through a fixed chain against a RULE, then hands
back one plain disposition with a full trace of how it got there.

It never guesses and it never grades. Every word the case relies on is
resolved through the gate first; if a word is not sourced, the engine
stops on that word (Void for Vagueness) and goes no further. The
disposition it returns is a mechanical classification, not an opinion:
it reports what the structure shows and leaves the judgment to you.

THE ERROR DOCTRINE  (every disposition IS a constitutional idea)
  VOID FOR VAGUENESS   -- a word the case leans on has no controlling
                          definition. The engine will not run on it.
  RESERVED             -- the authority claimed is not among the
                          enumerated powers. Tenth Amendment: it is
                          reserved to the States or the people.
  ULTRA VIRES          -- the authority claimed IS enumerated, but the
                          action crosses that power's own textual limit.
  ABRIDGMENT           -- the action burdens a protected right, and no
                          authority is delegated over that subject.
  DUE PROCESS VIOLATION-- a required procedure was not followed.
  VALID                -- none of the above fired.

The rules are loaded as DATA (the files in the 'rules' folder), never
baked into this code. The Constitution is simply the first ruleset. Add
a rule file, and the engine can run it. That is the whole design.
"""

import json
import os
from veritas_libraries import VeritasLibraries


def load_rules(folder):
    """Read every .json rule file in a folder into a dict keyed by id."""
    rules = {}
    if not os.path.isdir(folder):
        return rules
    for name in sorted(os.listdir(folder)):
        if name.endswith(".json"):
            with open(os.path.join(folder, name), "r", encoding="utf-8") as f:
                rule = json.load(f)
                rules[rule["id"]] = rule
    return rules


class BlackletterEngine:
    def __init__(self, rules_folder=None, gate=None):
        base = os.path.dirname(os.path.abspath(__file__))
        self.gate = gate or VeritasLibraries(base)
        self.rules = load_rules(rules_folder or os.path.join(base, "rules"))

    def evaluate(self, case):
        """Run one case against its named rule. Returns a finding dict."""
        trace = []
        rule = self.rules.get(case.get("ruleId"))
        if rule is None:
            return self._finding("NO RULE", None, case,
                                 f"No rule named '{case.get('ruleId')}' is loaded.", trace)

        # STEP 1 -- identify (put the facts of the case on the record)
        trace.append(f"Actor: {case.get('actor','(unstated)')}")
        trace.append(f"Action: {case.get('action','(unstated)')}")
        trace.append(f"Authority claimed: {case.get('claimedAuthority','(none stated)')}")
        obj = case.get("affectedObject", {})
        trace.append(f"Right/power touched: {obj.get('name','(none stated)')}")
        trace.append(f"Rule applied: {rule['ruleName']}  [{', '.join(rule.get('citation',[]))}]")

        # STEP 2 -- THE WALL: resolve every relied-on word through the gate
        terms = sorted(set(case.get("termsInvolved", [])) | set(rule.get("termsRelied", [])))
        trace.append(f"Resolving relied-on words: {', '.join(terms) if terms else '(none)'}")
        for term in terms:
            result = self.gate.resolve(term)
            if result["status"] == "resolved":
                trace.append(f"   '{term}': sourced -- OK")
            else:
                trace.append(f"   '{term}': NOT sourced -- STOP")
                return self._finding(
                    "VOID FOR VAGUENESS", rule, case,
                    f"The word '{term}' has no controlling definition in the sources. "
                    f"The engine will not run on an unsourced word. Source it first.",
                    trace)

        # STEP 3 -- authority analysis, by the kind of rule
        if rule["kind"] == "prohibition":
            return self._evaluate_prohibition(rule, case, trace)
        elif rule["kind"] == "authority-grant":
            return self._evaluate_authority(rule, case, trace)
        else:
            return self._finding("NO RULE", rule, case,
                                 f"Rule kind '{rule['kind']}' is not understood.", trace)

    # ---- prohibition rules (protect a right) ----
    def _evaluate_prohibition(self, rule, case, trace):
        protected = rule["protects"]["name"].strip().lower()
        touched = case.get("affectedObject", {}).get("name", "").strip().lower()
        burdens = case.get("actionBurdens", touched == protected)

        if not (touched == protected and burdens):
            return self._finding(
                "VALID", rule, case,
                f"The action does not burden {rule['protects']['name']}. "
                f"This rule is not triggered.", trace)

        trace.append(f"The action burdens a protected right: {rule['protects']['name']}.")
        if rule.get("authorityOverSubject") == "none-delegated":
            trace.append("No authority is delegated over this subject. The authority "
                         "claimed cannot supply what was never granted.")
            return self._finding(rule.get("failureResult", "ABRIDGMENT"), rule, case,
                                 f"The action burdens {rule['protects']['name']}, and no "
                                 f"authority is delegated over it.", trace)
        return self._finding("VALID", rule, case, "No prohibition triggered.", trace)

    # ---- authority-grant rules (does the power exist, and within limits?) ----
    def _evaluate_authority(self, rule, case, trace):
        enumerated_ids = {p["id"] for p in rule.get("enumeratedPowers", [])}
        claimed_id = case.get("claimedAuthorityId")

        if claimed_id not in enumerated_ids:
            trace.append(f"Authority claimed ('{case.get('claimedAuthority','')}') is NOT "
                         f"among the enumerated powers.")
            return self._finding(
                "RESERVED", rule, case,
                "The authority claimed is not among the enumerated powers. By the Tenth "
                "Amendment's own words it is reserved to the States or to the people.",
                trace)

        trace.append(f"Authority claimed is enumerated: '{claimed_id}'.")
        limit = rule.get("textualLimits", {}).get(claimed_id)
        if limit:
            value = case.get(limit["field"])
            if value is not None and value > limit["max"]:
                trace.append(f"The action crosses the textual limit: {limit['description']} "
                             f"(claimed value: {value}, limit: {limit['max']}).")
                return self._finding(
                    "ULTRA VIRES", rule, case,
                    f"The authority is enumerated, but the action crosses its textual limit: "
                    f"{limit['description']}.", trace)
            trace.append(f"Textual limit met ({limit['field']} = {value}, limit {limit['max']}).")

        if rule.get("requiredProcedure") and not case.get("procedureFollowed", True):
            return self._finding("DUE PROCESS VIOLATION", rule, case,
                                 "A required procedure was not followed.", trace)

        return self._finding("VALID", rule, case,
                             "The authority is enumerated and its textual limits are met.", trace)

    # ---- build a finding ----
    def _finding(self, disposition, rule, case, reason, trace):
        remedy = rule.get("remedy") if rule else None
        return {
            "disposition": disposition,
            "reason": reason,
            "remedy": remedy,
            "case_id": case.get("id", "(unnamed case)"),
            "trace": list(trace),
        }


def render(finding):
    """Print a finding in plain English."""
    line = "=" * 60
    out = [line, f"  DISPOSITION:  {finding['disposition']}", line, "",
           "  Trace (every step, in order):"]
    for step in finding["trace"]:
        out.append(f"    {step}")
    out.append("")
    out.append(f"  Finding: {finding['reason']}")
    remedy = finding.get("remedy")
    merits_dispositions = ("ABRIDGMENT", "ULTRA VIRES", "RESERVED", "DUE PROCESS VIOLATION")
    if finding["disposition"] in merits_dispositions and remedy and remedy.get("exists"):
        out.append("")
        out.append(f"  Remedy: {remedy.get('whatRestoresRight','(unspecified)')}")
        out.append(f"     Who may claim it: {remedy.get('whoCanClaim','(unspecified)')}")
        out.append(f"     Where: {remedy.get('whereClaimed','(unspecified)')}")
    out.append("")
    return "\n".join(out)
