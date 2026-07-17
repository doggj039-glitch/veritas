# VERITAS

**A research instrument for measuring constitutional drift — how the meaning of the words in
the Constitution has moved away from what they meant at the framing.**

VERITAS is not a verdict machine. It does not answer *"is this constitutional?"* It answers a
checkable question: **read by the rules used when the words were written, what did a word / law /
ruling mean — and how far, measurably and with sources, has practice drifted from that?** It
gathers the documented record, keeps founding-era meaning and modern meaning strictly separate,
and hands you a sourced, plain-English basis for asking the real question yourself.

It stands on **two founding-era pillars**: **Johnson's Dictionary (1755/1773)** for what the *words*
meant, and **the period's rules of legal construction** (expressio unius, ejusdem generis, noscitur a
sociis, the rule against surplusage, original public meaning…) for how the *text* was to be read.

> **👉 New here? Start with [INTRODUCTION.md](INTRODUCTION.md)** — the plain-English "what this is and
> why," the two pillars, and an open invitation.

> **This project is looking for people far more capable to take it further and make it genuinely good** —
> constitutional-law scholars, legal historians, linguists of period English, and engineers. It was built
> largely solo and has reached the limit of one builder. **If that's you, please take it over.** Read
> **[NEXT_PHASE.md](NEXT_PHASE.md)**; substantive review of the legal reasoning is especially wanted.

---

## What it actually does

Two layers, deliberately separated so the second can never fabricate the first:

### 1. The offline record (free · no internet · cannot invent)
Everything here is **verbatim** from a fixed, citable source; when the record is silent it says
so rather than filling the gap.
- **The founding baseline** — a word's meaning *verbatim* from Johnson's Dictionary (1755/1773,
  the controlling source), the etymology, and founding-era usage quotations.
- **"Define the Drift"** — the same word in every later dictionary on file, in publication order
  (Webster 1828/1844/1913, Black's Law 1910…), so you watch the meaning move.
- **The founding voices** — ten grounded agents (*Federalist, Anti-Federalist, Blackstone, Story,
  Montesquieu, Rawle, Sedgwick, Lieber, the Convention, the Ratification debates*). Each answers
  **only** with verbatim, cited passages from its own corpus; put a question to two opposing voices
  and the disagreement between their sourced words is the evidence.
- **The cases** — the Supreme Court decisions that later construed a term.

### 2. The reasoning tier (optional · needs an API key · web-sourced)
Lets the instrument reason and synthesize under a strict contract. Every answer is split into
three labeled sections and the tiers cannot cross:
- **FOUNDING** — founding-era meaning, drawn **only** from the offline record above.
- **MODERN** — present-day meaning/law, drawn **only** from a cited web search, **marked as modern**.
- **ARGUMENT** — the reasoning connecting them, **labeled as inference** (analysis, not a sourced fact).

It is **off and $0 by default** until a key is added; then a question costs cents, with a depth dial
and the running cost always shown.

### The method
The research method it supports — establish the baseline, apply the founders' seven rules of
construction, measure the divergence with sourced data, trace the cascade, document it verifiably —
is written up for a first-time user in **[VERITAS_RESEARCH_MANUAL.md](VERITAS_RESEARCH_MANUAL.md)**.
The governing architecture (the drift model, the admission bar, the schema) is in
**[VERITAS_DESIGN.md](VERITAS_DESIGN.md)**.

---

## Architecture (map of the repo)

VERITAS is a Python engine that serves a local web UI (no framework, stdlib only, so it runs as a
desktop app, a Windows folder-payload, or on-device). Numbered folders are a build pipeline:

| Path | What it is |
|---|---|
| `02_GATE_BLACKLETTER/` | **The gate** — resolves a word to its verbatim founding meaning + drift + cases; the "admit vs. void-for-vagueness" logic |
| `10_AGENTS/` | The ten grounded founding-voice agents (`agent_core.py`, `triangulate.py`, `debate.py`) + their personas |
| `00_APP/` | The server (`veritas_server.py`), the reasoning tier (`veritas_reason.py`), the web UI |
| `01_APP/` | The desktop research-map GUI + the "Define the Drift" timeline |
| `07_CAPTURE_TOOLS/` | The scrapers/processors that **build** the record (respectful, bounded — see the data doc) |
| `11_ANDROID/` | Android packaging notes |
| `03_LIBRARIES/`, `08_RAW_QUARANTINE/` | **The data — excluded from this repo** (see below) |

An efficiency analysis of the agent layer is in `AGENTS_EFFICIENCY_ANALYSIS.md`.

---

## Data is not in this repo — and why

The corpora and dictionaries (several GB) are **excluded on purpose**:
1. **Redistribution terms.** The Johnson's Dictionary source **prohibits systematic bulk download
   and redistribution** (non-commercial only). VERITAS builds its baseline through bounded,
   respectful, per-word requests — it does **not** ship a harvested copy, and neither does this repo.
2. **Size.** Gigabytes of data don't belong in git.

The public-domain corpora (Federalist, Anti-Federalist, Blackstone, Story, the debates) and the
public-domain later dictionaries (early Webster, Black's) are freely rebuildable. See
**[DATA_AND_SOURCES.md](DATA_AND_SOURCES.md)** for exactly what each source is, its license, and how
to assemble the record locally within each source's terms. `07_CAPTURE_TOOLS/` holds the code to do it.

---

## Running it (offline half — free, no key)

```bash
# From the project root, with the data assembled per DATA_AND_SOURCES.md:
cd 00_APP && python3 veritas_server.py        # serves the local UI
```
The reasoning tier stays off until an API key is set; the offline record works with no key and no
internet.

---

## Honest limits (read before relying on any output)

- **VERITAS is a research tool, not legal advice, and not a court.** Its "FOUNDING" layer is a
  disciplined presentation of sources; its "ARGUMENT" layer is explicitly *inference*. Outputs are a
  documented basis for a question, not a legal conclusion.
- **The construction method encodes a point of view** (original-public-meaning, the seven canons)
  that is one respected school among several. The instrument is honest about being that school; it
  does not claim to be the only valid reading. **Expert review of this reasoning is actively wanted
  — see [NEXT_PHASE.md](NEXT_PHASE.md).**
- **"Settled doctrine" and "open question" are kept distinct.** Where current law is settled, VERITAS
  says so plainly, *then* documents the historical question — it never dresses an opinion as a holding.
- The reasoning tier depends on a third-party model and live web sources for its MODERN/ARGUMENT
  halves; those are cited so you can verify them, and you should.

---

## License

Code and data carry **different terms.** See [LICENSE](LICENSE) for the code and
[DATA_AND_SOURCES.md](DATA_AND_SOURCES.md) for the per-source data terms. *(License choice pending —
see NEXT_PHASE.md.)*
