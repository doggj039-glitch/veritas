# VERITAS — User Manual

*Constitutional-analysis instrument grounded in founding-era meaning.*
Version of this manual: 1.0 · Library: v3.13 (Johnson 1773, 5,130 entries)

Status tags used throughout:
**✅ Built** — exists and runs today (offline).
**🔷 Proposed** — designed but NOT built; described so you know the shape, not because it works yet.
**💡 Idea** — a suggestion, not a commitment.

> **Ground rule (why VERITAS exists): no bad info.** Every definition and quote is *verbatim* from a fixed, citable, published source. VERITAS never paraphrases a founding-era meaning and never invents one. If it doesn't have a grounded answer, it says so ("Void for Vagueness") instead of guessing. Keep this in mind reading the two modes below — the whole point of the offline design is that it *cannot* make things up.

---

## 1. What VERITAS is

VERITAS resolves the words of the Constitution to their **founding-era meaning** (Samuel Johnson's *Dictionary*, 1773 folio — the edition in use at ratification), then shows how each word **drifted** afterward (Webster 1828/1844/1913, Black's Law 1910) and how the **Supreme Court construed** it over time. The thesis it is built to defend: *the Constitution is not a "living document" whose words quietly change meaning — it is more like code, whose terms have fixed definitions, and whose only legitimate amendment path is Article V, not redefinition.*

Three layers do the work:

1. **The Dictionary** — the founding-era baseline + a per-word drift timeline.
2. **The Gate (Blackletter)** — a checkpoint that admits a word only if it resolves to a verbatim 1773 definition, or throws it out as *Void for Vagueness*.
3. **The Corpora & Agents** — founding-era primary sources and case law you can search and question.

---

## 2. The two modes at a glance

| | **Offline mode ✅** | **Online / API mode 🔷 (proposed)** |
|---|---|---|
| **Status** | Built, working today | Design only — not built |
| **What answers you** | Deterministic lookups + keyword retrieval | A Claude model composing over the same grounded sources |
| **Internet needed** | No | Yes (API calls) |
| **Cost** | Free | Per-token API cost |
| **Privacy** | Fully local; nothing leaves the machine | Prompts + retrieved text sent to the API |
| **Can it invent?** | **No** — verbatim only, by construction | Possible — so the Gate must fence every claim |
| **Reproducible** | Byte-identical every run | Varies run to run |
| **Best for** | Ground truth, citations, verification | Drafting, synthesis, natural conversation |

The intended relationship: **offline is the source of truth; online is a writer that may only speak in offline's citations.** Online mode never overrides a founding meaning — it retrieves verbatim text from the local corpora and the Gate, and is only allowed to *arrange* it.

---

## 3. Offline mode — the system you have ✅

Everything here runs locally with Python 3, no network, no API key.

### 3.1 The Dictionary
- **`03_LIBRARIES/VERITAS_definitions_library.json`** — 5,130 entries, every one a verbatim Johnson 1773 baseline with a per-word `sources[]` timeline (baseline → etymology → founding-era usage → drift points).
- **Reference dictionaries** (finder/comparison only, *never* the drift baseline):
  - `reference_dictionaries/johnson_1755_reference.{json,db}` — 3,231 clean 1755 entries (an *earlier* edition; use to compare 1755 vs 1773 drift, as with `liberty`).
  - `from_zip_datasets/reference_copyrighted/` — Black's Law 8th/9th. **Copyrighted → lookup only, never ingested verbatim.**

### 3.2 The Gate (Blackletter) — the heart of the instrument
`02_GATE_BLACKLETTER/gate/`. A compiler-style **front end** for constitutional text:

`INPUT → LEX → RESOLVE → TYPECHECK → SENSE-BIND → FAULT → AUDIT → REPORT → TEST`

- **`blackletter_gate.py`** — `resolve(term)` → **ADMITTED** (verbatim 1773 + provenance + etymology + founding-era usage + flags + the cases that construed it) or **VOID_FOR_VAGUENESS** (no founding authority on file). `compile(text)` runs a whole clause.
- **`blackletter_usage.py`** — fills a term's founding-era usage from the primary-source corpora (verbatim, cited).
- **`blackletter_cases.py`** — the SCOTUS cases that later construed a term, with direction of drift, each enriched with a *year-verified* Oyez citation + link (or honestly name-only).
- **`blackletter_flags.py`** — an adjustable metadata sidecar (warnings, never rewrites the verbatim text).
- **`blackletter_gate_tests.py`** — 11 golden regression tests.

**It is a checkpoint, not a judge.** It tells you whether a word is *defined at the founding*, not what the right ruling is. A "Void" means "not a Johnson 1773 headword" — a tripwire for undefined operative vocabulary — **not** "unconstitutional."

### 3.3 Founding-era corpora (searchable, verbatim)
FTS5 databases, *queried on disk, never loaded into memory*:
- **`historical_documents.db`** — 25 works, 36,569 passages: Federalist, Anti-Federalist, Elliot's Debates I–V, Farrand's Records, Madison's Notes, Story, Rawle, Blackstone I–IV, Montesquieu, Locke.
- **`founding_sources/founding_corpus.db`** — Constitution, Declaration, Bill of Rights + OCR of Blackstone/Elliot.

### 3.4 Case law
- **`scotus_oral_arguments/`** — the Oyez corpus, **7,696 cases (1956–2018)**: verified caption, citation, court, dates, parties, docket, Oyez + Justia links.
- **`scotus_index.json`** + **`scotus_oral_arguments.db`** — a compact index + FTS5 case finder.
- **`from_sdcard/tables/word_to_cases.json`** — the curated word→case construction map (which cases moved which word, and how).

### 3.5 The Agents (keyword-grounded, no LLM)
`10_AGENTS/` — three "personalities" that answer *only* from their assigned primary sources:
- **Federalist** (85 papers · Publius) · **Anti-Federalist** (32 essays · Brutus et al.) · **Ratification** (Elliot's Debates, 12,065 passages).
- Each = a persona + an FTS5 corpus. They retrieve verbatim passages by keyword and speak in-voice. **No model, no API, no invention** — a "keyword-based AI layer."

### 3.6 The interface
- **`veritas_mockup.html`** — the "Library Workstation" (dark, gold-on-near-black). Six windows: **Primary** (Library + Ask), **Drift Tracker**, **Timeline**, **Case Detail** (backed by the Oyez corpus), **Graph View**, **Debates** (the three agents in dialogue). *Currently a front-end mockup wired to real project data.*

---

## 4. Online / API mode — proposed 🔷

**None of this is built. It is the intended shape if you add a Claude API.**

The design principle stays fixed: **the API may only speak in VERITAS's citations.** Concretely:

1. **Retrieve, then compose (RAG).** A question first pulls verbatim passages from the local corpora + the Gate's resolved definitions. The model receives *only* that grounded text and is instructed to quote it and cite it — not to answer from its own training.
2. **The Gate fences every operative term.** Before the model's answer is shown, its key terms are run back through the Gate; anything that doesn't resolve to Johnson 1773 is surfaced (drift flag / Void), so drift can't sneak in as fact.
3. **The admission bar still holds.** Copyrighted sources (Black's, OED) remain finder-only — the model may say "Black's 1910 defines X" and *point*, but the verbatim ingest rule is unchanged.

What it would add over offline: natural multi-turn conversation with the agents, synthesis across sources, first-draft briefs/books, and plain-language Q&A — all **grounded and cited**, never free-floating.

**💡 Ideas for online mode:** a "citations-only" strict setting (model output rejected if any sentence lacks a retrieved source); a side-by-side "offline says / online says" panel so you can always check the model against ground truth; a cost meter; a local-model option (Ollama) to keep everything offline while still getting composition.

---

## 5. Feature list (by mode)

| Feature | Offline | Online/API |
|---|---|---|
| Verbatim 1773 definition lookup | ✅ | ✅ (via retrieval) |
| Void-for-Vagueness gate | ✅ | ✅ (as a guardrail) |
| Drift timeline (1773 → 1913) | ✅ | ✅ |
| Founding-era usage search | ✅ | ✅ |
| SCOTUS case finder + construction chain | ✅ | ✅ |
| 1755-vs-1773 comparison | ✅ | ✅ |
| Agent Q&A (keyword) | ✅ | — |
| Agent *conversation* (fluent, multi-turn) | — | 🔷 |
| Synthesis / draft briefs & books | limited (templates) | 🔷 |
| Natural-language questions | — | 🔷 |
| Works with no internet | ✅ | — |

---

## 6. Differences that matter (choose deliberately)

- **Trust.** Offline *cannot* fabricate — that is its value for anything you'd put in front of a court or reader. Online *can*, so it is only as trustworthy as its grounding + the Gate fence.
- **Privacy.** Offline keeps every source and query on your machine. Online sends prompts and retrieved text to the API provider.
- **Cost & reproducibility.** Offline is free and byte-identical every run (good for citations). Online costs per token and varies run to run.
- **Speed of *answers* vs speed of *drafting*.** Offline gives instant exact lookups. Online is slower per call but turns lookups into prose.
- **Rule of thumb:** *verify and cite offline; draft and explain online — then re-verify the draft offline.*

---

## 7. Controls — command reference (offline) ✅

Run from the project root (`/home/noneya/Projects/VERITAS v.3`).

```bash
# Resolve terms through the Gate (ADMITTED / VOID) with drift + construction chain
python3 02_GATE_BLACKLETTER/gate/blackletter_gate.py commerce liberty necessary

# Run the golden regression tests (should print 11/11)
python3 02_GATE_BLACKLETTER/gate/blackletter_gate_tests.py

# See the SCOTUS cases that construed a term
python3 02_GATE_BLACKLETTER/gate/blackletter_cases.py commerce speech search

# Founding-era usage of a word (verbatim, cited)
python3 02_GATE_BLACKLETTER/gate/blackletter_usage.py militia reprieve

# Johnson 1755 reference lookup / comparison (finder only)
python3 03_LIBRARIES/reference_dictionaries/johnson_1755_lookup.py liberty commerce

# (Re)build the SCOTUS index + FTS5 finder
python3 03_LIBRARIES/build_scotus_index.py

# (Re)build the Case Detail data for the UI
python3 03_LIBRARIES/scotus_oral_arguments/build_case_detail.py
```

In Python, to compile a whole clause:
```python
from blackletter_gate import BlackletterGate      # run from 02_GATE_BLACKLETTER/gate/
g = BlackletterGate()
report = g.compile("Congress shall have power to regulate commerce among the several States")
print(report.render())        # ✓/✗ per term, compiler-style
```

**Controls that protect the data (do these, always):**
- The verbatim library changes **only** toward the source, and only through a logged, versioned edit (Article V discipline). Never let a tool paraphrase it.
- Flags are the adjustable layer — edit `blackletter_flags.json`, never the definitions.
- Copyrighted references are finder-only. Never bulk-ingest them or the Johnson site.

**🔷 Proposed controls (online mode):** `VERITAS_API_KEY` env var; a mode switch (`--offline` default / `--online`); a `--citations-only` strict flag; a per-session cost cap.

---

## 8. Ideas & suggestions (roadmap) 💡

*Forward-looking — not built, not promised.*

- **Finish the UI spokes with live data** — Graph View and Timeline already read real data; wire the Primary "Ask" box to the Gate so typing a clause shows ADMITTED/VOID inline.
- **Re-capture the 102 remaining abbreviated dictionary entries** in batches (marquee constitutional words first) so every entry carries its illustrative quotations.
- **Expand the word→case map** beyond the current 20 words, and index full opinion text (not just Oyez metadata) so the construction chain covers more terms.
- **A "drift score" view** — you already have `DRIFT_RANKED_WORD_LIST` (738 words scored); surface the most-drifted words as a leaderboard tied to the Timeline.
- **Article V module** — model the amendment process as the *only* legitimate way a term's meaning changes (the philosophical core of the whole project).
- **The Kernel (deferred)** — the "constitutional computer" back end (enumerated powers as an instruction set, rights as memory protection, ultra vires as an illegal instruction). Real, but intentionally **not** built until the Gate front end is fully finished — it's the scope trap the project agreed to avoid.
- **Local-model online mode** — get composition without leaving the machine (Ollama), preserving the offline privacy guarantee.

---

## 9. The doctrine (the rules everything obeys)

1. **Verbatim only.** Never invent or paraphrase a founding-era meaning.
2. **Fixed, citable authority.** Only published, datable sources are admitted verbatim; copyrighted works are finder-only.
3. **1773 is controlling.** Etymology and founding-era usage corroborate; drift (Webster/Black's) and modern dictionaries are reference — they show the drift, they never override the meaning.
4. **When ungrounded, say so.** Void for Vagueness beats a confident guess.
5. **Change only through a logged protocol.** Text moves only toward its source, and only with a version bump — the Article V habit applied to the library itself.

*This manual describes the project honestly: offline is real; online/API is a design; ideas are ideas. If a future version blurs that line, fix the manual first.*
