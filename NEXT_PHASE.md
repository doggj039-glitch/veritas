# VERITAS — Next Phase: A Call for Collaborators

VERITAS is a working research instrument built by one person, largely solo. It has reached the
point where the next phase would benefit from people who know more than its author about specific
things — and it is being shared openly for exactly that reason. **This is information, freely
shared; nothing here is for sale.** If any part below is your field, your input is wanted.

---

## What VERITAS is (in one paragraph)

An offline-first engine that measures **constitutional drift**: it stores a word's *verbatim*
founding-era meaning (Johnson's Dictionary + founding usage), tracks how that meaning moved through
later dictionaries and Supreme Court constructions, lets you query ten grounded founding-era
"voices" that can only quote their own sources, and — optionally — runs a reasoning tier that
synthesizes a founding-vs-modern analysis under a strict, cite-everything contract. The research
method it supports is written up in `VERITAS_RESEARCH_MANUAL.md`; the architecture in
`VERITAS_DESIGN.md`.

## What is solid today
- A verbatim, provenance-tagged founding-era dictionary engine with a working "Define the Drift"
  timeline (baseline → later editions in date order).
- Ten grounded, no-hallucination agents; a "triangulate" mode that puts one question to opposing
  founding voices and shows the sourced disagreement.
- A reasoning tier with a **FOUNDING (record) / MODERN (web-cited) / ARGUMENT (labeled inference)**
  contract that is structurally unable to state a founding meaning from model memory.
- Runs offline and free for the core; the reasoning tier is off/$0 until a key is added.

---

## Where expert input is most wanted

### 1. Constitutional-law & legal-history review  *(the most important ask)*
The engine encodes a specific interpretive method — **original public meaning** and the seven
canons of construction (expressio unius, ejusdem generis, noscitur a sociis, surplusage, etc.).
That is one respected school among several. We want scholars to:
- Pressure-test the canon logic and the worked analyses (esp. the 14th-Amendment / corporate-
  personhood chain) for accuracy and fairness.
- Flag where the instrument overstates, or where a competing interpretive tradition would read the
  same text differently — and help it *represent that disagreement* rather than pick a side.
- Verify that "settled doctrine" is always stated accurately before any historical question is raised.

### 2. The source record & its provenance
- Audit the admission bar (what may enter as evidence) and the verbatim/provenance discipline.
- Improve OCR/citation quality in the corpora; expand the drift series with more public-domain
  authorities; advise on the cleanest lawful way to assemble each source (see `DATA_AND_SOURCES.md`).

### 3. The reasoning tier's soundness
- Adversarially test the FOUNDING/MODERN/ARGUMENT separation — can it be made to smuggle an
  ungrounded claim into the FOUNDING section? Harden the contract if so.
- Improve grounding, citation fidelity, and cost efficiency.

### 4. Engineering / packaging
- Mobile (Android/Chaquopy) and desktop packaging; performance; test coverage.
- General code review — it is stdlib-heavy and single-author; a second set of eyes is welcome.

### 5. Security & safety review
- The reasoning tier calls an external API and the web; review key handling, input handling, and
  the "off by default" guarantees.

---

## How to get involved
- **Open an issue** describing what you'd review, fix, or extend — or just what you think is wrong.
  Disagreement is useful; this project would rather be corrected than flattered.
- **Open a pull request** for code, docs, corpus/citation fixes, or additional public-domain sources.
- For substantive legal/historical critique, a written issue (even a long one) is the ideal format —
  it becomes part of the record.
- See `CONTRIBUTING.md` for the ground rules (the big one: **verbatim sources, never paraphrase
  founding-era meaning; cite every modern number; keep inference labeled as inference**).

## Taking over the next phase
The author is explicitly open to more capable people leading the project's direction. If you want to
help steer — the interpretive method, the data standards, the engineering, or the mission framing —
say so in an issue. The goal is a trustworthy, checkable instrument, not any one person's ownership
of it.

---

*VERITAS gathers the record; the public sources make it checkable; the reader asks the question.
Help make each of those three things better.*
