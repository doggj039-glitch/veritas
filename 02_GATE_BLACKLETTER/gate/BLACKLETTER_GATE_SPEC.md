# BLACKLETTER GATE — LOCKED SPECIFICATION (v1)

**Status: LOCKED (2026-07-09).** Blackletter is officially THE GATE of VERITAS.
This document fixes what the gate is. Supersedes BLACKLETTER_GATE_SCOPE.md (the
earlier scoping draft); that remains valid as background.

Blackletter models **how a computer runs** — but a gate is the *front end* of that
process only. It answers one question: **"is this term grounded in fixed
founding-era meaning?"** — ADMITTED, or VOID FOR VAGUENESS. It never executes a
verdict on the law. Execution (the kernel) is explicitly out of this spec.

---

## THE PIPELINE (compiler front end)

The gate runs a term, clause, or query through these stages, in order. Each stage
is a real computing process with a fixed constitutional meaning:

| # | Stage | Computing process | What it does here | State |
|---|-------|-------------------|-------------------|-------|
| 1 | INPUT | source text | the clause / statute / query under review | — |
| 2 | LEX | tokenizer | split into candidate legal terms; drop stopwords | DONE |
| 3 | RESOLVE | symbol resolution | bind each term → Johnson 1773 baseline entry | DONE |
| 4 | TYPECHECK | type checking | term must resolve to fixed meaning, else fault | DONE |
| 4a| SENSE-BIND | overload resolution | record which sense applies; flag if ambiguous (multi-sense) | PARTIAL |
| 5 | FAULT | trap / exception | throw VOID FOR VAGUENESS with a trace | DONE |
| 6 | AUDIT | journal / stack trace | attach provenance (source/year/edition) to every admission | DONE |
| 7 | REPORT | compiler output | emit one machine-readable compile report | DONE |
| 8 | TEST | CI / regression | run validation cases through the gate; verdicts must not drift | DONE |

**FRONT END COMPLETE (2026-07-09):** all 8 stages built and locked; `blackletter_gate_tests.py`
green (9/9). The gate is a complete, self-guarding compiler front end for constitutional
meaning. Kernel (back end) remains deferred per the line below.

**Determinism guarantee:** the same input against the same `library_version`
yields the same verdict, always. `library_version` is the toolchain version;
every report records it.

---

## THE ONE FAULT + THE WARNING TIER

The gate throws exactly one *error*: **VOID FOR VAGUENESS** — "no verbatim
founding-era (Johnson 1773) authority on file." It carries a trace: the term, the
reason, and nearest root(s). One gate, one error. (Additional doctrines — ultra
vires, due-process — belong to the KERNEL, out of this spec.)

Between clean-admit and error sits the **WARNING** tier — the flag layer
(`blackletter_flags.py` → `blackletter_flags.json` sidecar). A flag is metadata
ABOUT a definition; it NEVER touches the verbatim text and NEVER blocks admission.
A flagged term ADMITS with warnings (the report `compiles` with warnings, like a
compiler). Flag types: abbreviated-capture, not-verified-1773 (warning);
multi-sense, etymology-pending, founding-use-pending, multi-POS (info). Flags live
in the sidecar so the library stays byte-for-byte fixed and flags stay freely
adjustable — annotate here, the library never moves. The gate loads the sidecar if
present; absent, it runs unflagged.

---

## RESOLUTION ORDER (fixed, never reordered)

1. Johnson's Dictionary **1773** (4th folio) — CONTROLLING. Verbatim only.
2. Etymology — corroborating.
3. Founding-era usage — corroborating.
4. Drift (Webster 1828/1844/1913, Black's 1910) — reference only; the gate does
   NOT read drift to admit.
5. Modern / copyrighted — reference only; never authority.

Admission requires only stage 1 (Johnson 1773). Etymology/usage enrich a verdict;
they do not gate it. (Coverage: Johnson 100%, etymology 92%, founding-use 25% —
demanding the full triad would void 77% of the founding vocabulary.)

---

## VERDICT CONTRACT

```
resolve(term) ->
  { term, status:"ADMITTED",
    controlling:{ source:"Johnson's Dictionary (1773, 4th folio)", part_of_speech, verbatim },
    etymology, founding_use[], grounding:"full-triad"|"baseline+etymology"|"baseline-only",
    matched_via_root? }
| { term, status:"VOID_FOR_VAGUENESS", reason, nearest[] }
```

Implemented: `blackletter_gate.py` (`BlackletterGate.resolve`, `.gate`, `.compile`).
Lexer: `blackletter_lexer.py` (`lex`). Report: `blackletter_report.py` (`CompileReport`,
`build_report`). Case bridge: `blackletter_gate_case.py` (fills validation-case placeholders).

`gate.compile(text)` runs LEX->RESOLVE->TYPECHECK->REPORT and returns a
`CompileReport`: {report_version, library_version, input, input_id (sha256 of
library_version+input — deterministic, no wall-clock), compiles, summary
(counts + grounding_counts + void_terms), diagnostics[] (one per term, lex order)}.
`.render()` = human compiler output; `.to_json()` = machine object VERITAS consumes.

---

## THE LINE — WHAT IS *NOT* THE GATE (kernel; deferred, not cancelled)

The back end of "how a computer runs" is the constitutional KERNEL. It is real
and buildable LATER, gated behind the front end proving out. NOT in scope now:

| Computing process | Kernel meaning (future) |
|-------------------|-------------------------|
| execution / call stack | the 12-step validation chain run as a program |
| memory protection / access control | rights as protected memory; actors as processes |
| instruction set (ISA) | enumerated powers; ultra vires = illegal instruction |
| privilege rings | agent authorities |
| scheduler | agent orchestration |

Rule: **nothing from the kernel column is built until front-end stages 1–8 are
complete and covered by tests.** This is the guardrail that keeps the gate from
sprawling into an OS project.

---

## META LAYER (already VERITAS's philosophical core)

- **Versioning / releases** = Article V, the sanctioned upgrade path. Meaning
  changes only through the defined protocol, never by runtime reinterpretation.
- **Deprecation** = superseded law.

These are documented here because they are the *reason* the gate exists: the gate
enforces that meaning is fixed and sourced, changeable only by the protocol — not
hot-patched at the moment of enforcement.

---

## LOCKED DEFINITION (one line)

> The Blackletter gate is the compiler front end for constitutional meaning: it
> lexes text into terms, resolves each to a fixed, verbatim, founding-era
> authority, type-checks that the meaning exists, and either ADMITS it with
> provenance or throws VOID FOR VAGUENESS. It validates; it does not execute.
