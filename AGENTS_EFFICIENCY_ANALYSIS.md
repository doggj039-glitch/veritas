# VERITAS — Agents & Teams: Efficiency Analysis
*Analysis of `~/Projects/VERITAS v.3/10_AGENTS/` — how the agents/teams do their tasks, and where they can do them more efficiently. Written 2026-07-17. Read `VERITAS_DESIGN.md` for the drift model this serves.*

---

## 1. What the agent system actually is

Two layers, cleanly separated:

- **The Record (data):** `03_LIBRARIES/veritas_corpus.db` — ONE SQLite FTS5 database, **66,645 passages**, tagged by `corpus` (historical, founding, federalist, antifederalist, sedgwick, lieber…), plus a `cases` table and an `agent_scope` map that says which passages each agent may see.
- **The agents (personas):** 10 founding-era voices — `blackstone, convention, montesquieu, ratification, rawle, story, sedgwick, lieber, federalist, antifederalist`. Each = a `persona.md` + a **scope** into the Record. `agent_core.py` retrieves top-K passages by BM25 keyword match, binds Johnson-1773 definitions through the Blackletter gate, and composes a **verbatim, cited, no-hallucination** answer. Knowledge is *queried, never loaded* → memory stays flat no matter how many books/agents exist.

**This is a genuinely good design.** Grounded, offline, no API, un-bluffable. The inefficiencies below are about *housekeeping and mechanics*, not the concept.

---

## 2. Every agent — current state

| Agent | persona | Runs on | Note |
|---|---|---|---|
| federalist | ✅ | **private `corpus.db` (2.2 M)** ⚠️ | also present in the Record → **duplicated** |
| antifederalist | ✅ | **private `corpus.db` (936 K)** ⚠️ | also in the Record → **duplicated** |
| sedgwick | ✅ | **private `corpus.db` (2.9 M)** ⚠️ | also in the Record → **duplicated** |
| lieber | ✅ | **private `corpus.db` (664 K)** ⚠️ | also in the Record → **duplicated** |
| blackstone | ✅ | Record scope (4) | ✅ already consolidated |
| convention | ✅ | Record scope (4) | ✅ already consolidated |
| montesquieu | ✅ | Record scope (4) | ✅ already consolidated |
| ratification | ✅ | Record scope (5) | ✅ already consolidated |
| rawle | ✅ | Record scope (1) | ✅ already consolidated |
| story | ✅ | Record scope (3) | ✅ already consolidated |

---

## 3. Efficiency findings (ranked: safe quick wins → deeper)

### ✅ A — DONE & VERIFIED (2026-07-17): agents unified onto the Record; ~61 MB reclaimed
### ✅ B — DONE & VERIFIED (2026-07-17): 3 gate dictionaries → symlinks to one canonical file; ~267 MB reclaimed; drift hazard removed. Gate re-verified resolving commerce/government/faction.
*All 10 agents verified `on_record=True` with identical grounded citations; `triangulate` team process verified. Total ~328 MB reclaimed, zero content change. Original A findings below.*

### 🟢 A. The corpus consolidation was designed but never finished — **~62 MB duplicated, split-brain retrieval**
`agent_core.py` *prefers* a private `corpus.db` when it exists and only uses the shared Record when it's gone (lines 104–113). The Record already contains federalist/antifederalist/sedgwick/lieber **and** their `agent_scope` rows — so those four corpora are stored **twice**, and those four agents are querying the *private* copies while the Record copies sit unused. On top of that, `10_AGENTS/_retired_corpora/` is **55 MB of already-superseded copies** still on disk.
- **Waste:** ~6.7 MB private dbs (duplicated) + 55 MB retired = **~62 MB dead weight**, and the system runs "split-brain" (6 agents on the Record, 4 on private dbs).
- **Fix (safe, ~5 min):** delete the 4 private `corpus.db` files → those agents fall through to the Record *automatically* (the code path already exists and is tested by design). Delete `_retired_corpora/`. Result: **one source of truth, all 10 agents on one index, ~62 MB reclaimed.** *(Verify each agent still answers after, since retrieval moves from corpus-local bm25 to Record-scoped bm25 — scores shift slightly but content is identical.)*

### 🟢 B. The founding dictionary is stored **4× byte-identical**
`VERITAS_definitions_library.json` (the 5,125-entry Johnson library) lives once in `03_LIBRARIES/` and **three more identical copies** in `02_GATE_BLACKLETTER/{gate,engine,nova_johnson}/` (md5 `b90d3058b95d`). "The gate needs a copy in each" is a workaround, not a requirement.
- **Cost:** 4× a multi-MB file + a **consistency hazard** (update one, forget three → silent drift, which is exactly what VERITAS exists to prevent).
- **Fix:** point all three gate consumers at the single `03_LIBRARIES/` path (or a symlink). One dictionary, one truth.

### 🟡 C. Retrieval fires many small queries per question (N+1 pattern)
In `agent_core.py`, a single `respond()`:
1. `search()` calls `doc_freq()` **once per term** to filter (lines 135) → N COUNT queries,
2. then the MATCH query,
3. then `_compose()` calls `doc_freq()` **again** per term for the "absent" check (line 203),
4. then resolves a Johnson definition per term (line 210).
So a 4-word question ≈ **10+ SQLite round-trips**, several of them repeats of the same `doc_freq`.
- **Fix:** compute `doc_freq` **once per term and cache it** for the request (dict on the agent, cleared per question); reuse in filter + absent-check. Optionally get all term frequencies in one grouped query. Cuts round-trips roughly in half. *(Offline it's already fast — this matters most when a "team" runs many agents × many topics, e.g. `debates_service.build_all` = 9 topics × 3 voices = 27 full retrievals.)*

### 🟡 D. The "team" is parallel *independent* retrieval, not shared retrieval
`triangulate.py`, `debate.py`, `debates_service.py` each **re-open their own agent instances** and run **separate** `search()` calls per voice for the *same* question. Since every agent now lives in the **same Record**, one question could be answered with **one retrieval pass** filtered per `corpus`, instead of 2–3 independent passes.
- **Fix:** a small shared `team_query(question)` that hits the Record once and splits results by corpus/scope → feeds all voices. Fewer connections, fewer queries, and it makes cross-agent pairing (below) natural.

### 🟡 E. `debate.py` pairing is bag-of-words overlap — the code admits it
The point/counterpoint match is "vocabulary overlap, not semantic judgment" (its own docstring). It mis-pairs whenever the two sides argue the same clause in *different* words — which is common. It's efficient but **functionally weak**.
- **Fix (mechanical):** weight overlap by term rarity (idf) instead of raw count, and pair on the Federalist passage's *topical* terms only (already computed) — cheap, meaningfully better pairings. **(Deeper, functional fix in §4.)**

### 🟢 F. Small cleanups
- `RETRIEVAL_STOPWORDS` lists `"meant"` **three times** and `"founders"`/`"federalist"` etc. — harmless but sloppy; dedupe to a clean frozenset.
- Agent instances are opened at *module import* in `triangulate.py`/`debate.py` (not lazily), so importing either opens the 114 MB Record even if unused. `debates_service.py` already does this right (lazy `_agents`). Make them all lazy + shared.
- `agent_core._veritas_root()` hard-codes `/home/noneya/Projects/VERITAS v.3` as a last-resort fallback (line 25) — fine on this machine, will silently mislocate on any other. Make it raise instead, so a bad deploy fails loudly.

---

## 4. The bigger truth: two kinds of "efficiency"

There are **two ceilings** here, and they're different:

- **Mechanical efficiency** (§3): storage, queries, orchestration. All fixable, mostly safe, real wins — do these.
- **Functional efficiency** — *are the agents doing their task the best way?* Here the honest answer is: **they can only quote, not reason.** They retrieve verbatim passages and pair them by keyword. That's their strength (un-bluffable, offline, free) **and** their ceiling. A question whose answer isn't sitting as a keyword-matchable passage gets "I have nothing in my assigned sources" — the code says so and points to "connect an API."

So "make the agents more efficient at their task" splits:
- **If the task is *evidence retrieval*** (surface what the founders verbatim said, side by side) → they're near-optimal; do §3 and they're excellent.
- **If the task is *reasoning*** (weigh the sides, synthesize, answer a novel question) → no amount of mechanical tuning gets there; that needs a reasoning layer (Claude API, or a small on-device model), which is the tradeoff already on the table. The current design is *built for* this: it cleanly hands off to an API tier when its corpus runs dry.

**Recommendation:** do §3 A–F (they're cheap, safe, and make the retrieval team genuinely tight — one Record, one index, fewer queries, better pairings). Keep the "no-API, verbatim" agents as the **evidence layer**. Add reasoning as an *optional* layer on top (bring-your-own-Claude, or a bundled small model) rather than trying to squeeze reasoning out of keyword retrieval — that's where the "lost potential" actually is.

---

## ✅ C, D, E, F — DONE & VERIFIED (2026-07-17)
- **C** doc_freq now cached per instance — verified **50% of DB queries eliminated** (12 calls → 6 queries in one response), agent output byte-identical.
- **D** added `team_ask(agents, question)` (lex once, share terms); `triangulate.py` uses it — verified **team_ask == respond()** for all agents; team orchestration intact.
- **E** `debate.py` pairing now **rarity-weighted (idf-ish)** — verified still verbatim + cited (Federalist 24/26 ↔ Brutus VIII/II on standing armies).
- **F** stopwords de-duped; `triangulate.py`/`debate.py` now **lazy-load** (import no longer opens the 114 MB Record); `_veritas_root()` **fails loud** instead of hard-coding a path.
*All changes preserve the verbatim/grounded/no-hallucination contract; only speed + selection quality changed.*

## 5. Suggested order of work
1. **A + B** (delete duplicated corpora, unify the dictionary) — biggest cleanup, ~62 MB, safest, removes the split-brain. Verify all 10 agents still answer.
2. **F** (lazy+shared loading, stopword dedupe, fail-loud root) — tiny, tidies the foundation.
3. **C + D** (cache doc_freq, one shared team retrieval) — the real runtime speedup for team runs.
4. **E** (idf-weighted pairing) — better debates for near-zero cost.
5. **Then** decide the reasoning layer separately (§4) — that's a direction, not a cleanup.
