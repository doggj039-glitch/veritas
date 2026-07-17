"""
BLACKLETTER GATE — stage 7: REPORT.  Spec: BLACKLETTER_GATE_SPEC.md

The canonical compiler output. One object, produced by compiling text through the
gate, that the rest of VERITAS consumes. Modeled on a real compiler's output:

  result           -> COMPILES / DOES NOT COMPILE
  diagnostics[]    -> one per term (like compiler errors/warnings), in lex order
  toolchain        -> library_version (the source of truth) + report spec version
  input_id         -> deterministic hash of (library_version, input): same input
                      against the same library ALWAYS yields the same id + verdict

No wall-clock time is baked into identity, so reports are reproducible and diffable.
"""
from dataclasses import dataclass, field, asdict
import hashlib
import json

REPORT_VERSION = "1"


@dataclass
class Diagnostic:
    term: str
    status: str                       # ADMITTED | VOID_FOR_VAGUENESS
    severity: str                     # ok | warning | error
    # admitted:
    source: str = None
    grounding: str = None
    part_of_speech: str = None
    verbatim: str = None
    matched_via_root: str = None
    flags: list = None                # metadata warnings riding along (never block admission)
    # voided:
    reason: str = None
    nearest: list = None

    @classmethod
    def from_verdict(cls, v):
        if v["status"] == "ADMITTED":
            c = v["controlling"]
            flags = v.get("flags") or []
            return cls(term=v["term"], status="ADMITTED",
                       severity="warning" if flags else "ok",
                       source=c["source"], grounding=v.get("grounding"),
                       part_of_speech=c.get("part_of_speech"), verbatim=c.get("verbatim"),
                       matched_via_root=v.get("matched_via_root"), flags=flags)
        return cls(term=v["term"], status="VOID_FOR_VAGUENESS", severity="error",
                   reason=v.get("reason"), nearest=v.get("nearest"))


@dataclass
class CompileReport:
    report_version: str
    library_version: str
    input: str
    input_id: str
    compiles: bool
    summary: dict
    diagnostics: list                 # list[Diagnostic]

    def to_dict(self):
        d = asdict(self)
        return d

    def to_json(self, indent=2):
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)

    def render(self, verbatim_chars=70):
        """Human-readable, compiler-style."""
        s = self.summary
        head = "COMPILES" if self.compiles else "DOES NOT COMPILE"
        lines = [
            "Blackletter gate — compile report",
            f'input: "{self.input}"',
            f"toolchain: Johnson 1773 library v{self.library_version} | report spec v{self.report_version}",
            f"id: {self.input_id[:16]}",
            f"result: {head}  ({s['terms_total']} terms, {s['admitted']} grounded, "
            f"{s.get('flagged', 0)} flagged, {s['void']} void for vagueness)",
            "",
        ]
        for d in self.diagnostics:
            if d.status == "ADMITTED":
                via = f" (via root '{d.matched_via_root}')" if d.matched_via_root else ""
                mark = "⚠" if d.severity == "warning" else "✓"
                lines.append(f"  {mark} {d.term:<14} [{d.grounding}]{via}  {d.source}")
                for f in (d.flags or []):
                    lines.append(f"        ⚠ {f['type']} ({f['severity']}): {f['note']}")
            else:
                near = f"  (nearest: {', '.join(d.nearest)})" if d.nearest else ""
                lines.append(f"  ✗ {d.term:<14} VOID FOR VAGUENESS — {d.reason}{near}")
        return "\n".join(lines)


def build_report(input_text, library_version, verdicts, report_version=REPORT_VERSION):
    """verdicts: ordered list of resolve() outputs (lex order)."""
    diagnostics = [Diagnostic.from_verdict(v) for v in verdicts]
    admitted = [d for d in diagnostics if d.status == "ADMITTED"]
    void = [d for d in diagnostics if d.status != "ADMITTED"]
    grounding_counts = {}
    for d in admitted:
        grounding_counts[d.grounding] = grounding_counts.get(d.grounding, 0) + 1
    input_id = hashlib.sha256(f"{library_version}\x00{input_text}".encode("utf-8")).hexdigest()
    flagged = [d for d in admitted if d.severity == "warning"]
    summary = {
        "terms_total": len(diagnostics),
        "admitted": len(admitted),
        "flagged": len(flagged),
        "void": len(void),
        "grounding_counts": grounding_counts,
        "void_terms": [d.term for d in void],
        "flagged_terms": [d.term for d in flagged],
    }
    return CompileReport(
        report_version=report_version,
        library_version=library_version,
        input=input_text,
        input_id=input_id,
        compiles=(len(void) == 0),
        summary=summary,
        diagnostics=diagnostics,
    )
