# Contributing to VERITAS

Thank you for looking. VERITAS is shared openly as information; corrections and disagreement are as
welcome as code. A few ground rules keep the instrument trustworthy.

## The three discipline rules (non-negotiable)
1. **Verbatim, never paraphrase, for founding-era meaning.** A founding-era definition or quote must
   be exact, with its source. If the record is silent, say "the record is silent" — never fill the gap.
2. **Cite every modern number.** Any present-day figure, case, or claim needs a public source a reader
   can open. No source line → cut it.
3. **Keep the three registers separate.** Founding (record) · Modern (web-cited) · Argument (your
   inference) must never blur. State settled doctrine accurately *before* raising any historical question.

## How to contribute
- **Issues** — report an error, a citation problem, a factual/legal critique, or a feature idea.
  Long, sourced critiques are ideal; they become part of the record.
- **Pull requests** — code, docs, citation fixes, additional **public-domain** sources, tests.
  Keep PRs focused; describe what changed and why.
- **Data** — see `DATA_AND_SOURCES.md`. Don't commit gigabytes or a bulk-harvested Johnson's; use
  public-domain sources, attribute CC-BY-SA material, and put large files in Git LFS or a Release.
- **Secrets** — never commit an API key or config. The `.gitignore` guards the known paths; don't add
  new secret paths.

## Style
- Python is stdlib-first by design (so VERITAS runs as a desktop/Windows/on-device app without a
  dependency stack). Match that unless there's a strong reason not to.
- Match the surrounding code's naming and comment density.

## Scope of authority
The maintainer welcomes more capable people helping steer the next phase — interpretive method, data
standards, engineering, or framing. Propose direction in an issue. The goal is a checkable instrument,
not any one person's ownership of it.
