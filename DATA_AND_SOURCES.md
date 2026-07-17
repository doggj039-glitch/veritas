# VERITAS — Data & Sources

VERITAS's value is its **record**: verbatim, provenance-tagged sources. The record is not stored in
this code repository (it's gigabytes, and git is for code). This document lists every source, its
terms in plain English, and how to assemble it locally. **VERITAS is shared as information, not sold.**

Sources fall into two buckets: **public-domain** (bundle freely if you want) and **fetch-your-own**
(one source asks that the full set not be bulk re-posted — so we point you to it instead).

---

## The founding baseline

| Source | Role | Terms (plain English) | How to get it |
|---|---|---|---|
| **Johnson's Dictionary (1755 / 1773)** | Controlling founding-era definitions (verbatim) | The online source is free for **non-commercial** use but asks that the **full dictionary not be bulk-downloaded / re-posted**. So VERITAS builds it by **bounded, respectful, per-word requests (≥1.5 s apart)** — it does not ship or mirror a harvested copy. | Use `07_CAPTURE_TOOLS/johnson_1773_scraper.py` for the words you need, or license a dataset (e.g. LEME/UCF). Do **not** run a full ~42k harvest. |
| **Etymology** | Origin anchor | Bracketed etymology inside each Johnson entry; deepen with **Skeat's Etymological Dictionary (1910)** — public domain. | From the Johnson entries + a public-domain Skeat text. |
| **Founding-era usage** | Actual usage quotes | Federalist, Anti-Federalist, Madison's Notes, Elliot's Debates, Farrand's Records, Story, Rawle — all **public domain**. | Freely bundleable; texts widely available (e.g. Project Gutenberg, the Avalon Project). |

## The drift series (all public domain — bundle freely)

| Source | Register | Notes |
|---|---|---|
| Webster's 1828 / 1844 / 1913 | common | Public domain. VERITAS used DataWar / public transcriptions. |
| Black's Law Dictionary, 1st (1891) / 2nd (1910) | legal | Public domain text; VERITAS used the **LexPredict** transcription, which is **CC-BY-SA** — **attribute it** if you redistribute that copy. |
| Skeat's Etymological Dictionary (1910) | etymology | Public domain. |

## The founding-voice agent corpora (public domain — bundle freely)
`10_AGENTS/` personas + query code are in this repo. Their **corpora** (`corpus.db`) are excluded
(size), but the underlying texts — Federalist, Anti-Federalist, Blackstone, Story, Montesquieu,
Rawle, Sedgwick, Lieber, Convention & Ratification debates — are **public domain**. Rebuild with the
`10_AGENTS/build_*.py` scripts from the public-domain source texts.

## Case law
The Supreme Court index / constructions are drawn from public court records
(e.g. `law.cornell.edu`, public opinions). Public domain / public record.

---

## Rebuilding the record locally
1. Assemble the public-domain corpora and later dictionaries (freely available).
2. For the Johnson baseline, capture **only the words you need**, respectfully, with `07_CAPTURE_TOOLS/`.
3. Run the processors in `07_CAPTURE_TOOLS/` to build the library and the drift timeline; the design
   doc (`VERITAS_DESIGN.md`) specifies the schema.

## If you choose to bundle data in a fork
- **Fine to bundle:** everything marked public domain above (attribute LexPredict / CC-BY-SA where used).
- **Please don't bulk-repost:** a full harvested Johnson's Dictionary — link to the source or a
  licensed dataset instead. Being non-commercial covers use; the courtesy is about not mirroring the
  whole thing.
- Big files belong in **Git LFS** or a **GitHub Release asset**, not the main git tree.

---

*Every source above is chosen so that a reader can verify a claim against a fixed, citable authority.
That verifiability is the point — keep it intact.*
