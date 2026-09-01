# EP-19 — Selection and ranking

**Size:** L · **Mode:** a · **Core/Stretch:** core ·
**Depends on:** EP-18 (Registry loader, schema versioning, migrations) ·
**Blocks:** EP-20 (abstention and hard-stop chain), EP-23 (engine integration, re-plan P2)

## Context

This is the engine's arithmetic: given a validated registry and an input envelope, decide which
concepts become waypoints. It is the brief that has to earn the word **deterministic**, because D-17
makes the baseline both the shipped default and the permanent fallback, and D-56 says the word
attaches to this path and to nothing else.

The mechanics are settled: **gather → filter → integer score → one-per-`family` diversity →
counter-hypothesis → cardinality 3–5 → evidence floor.** No floats, no clock, no RNG, `sorted()`
everywhere; ties break lexicographically on concept ID. Integer arithmetic is not a stylistic
preference — it is what makes exact ties possible, which is what makes a total order possible, which
is what makes 100 repeated runs byte-identical and a golden-file suite meaningful.

Implements **D-17** (deterministic baseline), **D-26(a)** (plural hypotheses across genuinely
different dimensions, which is what the `family` constraint mechanically produces), **D-53**
(counter-reading and insufficient-basis are structural, not optional), **D-7** (3–5 waypoints), and
the selection half of **D-25**'s anti-stereotyping rule. Lands **ADR-004** (integer scoring and
tie-breaking).

**Already in the tree:** EP-17's contracts, EP-18's loader with its activation index, `family`
grouping and `counter_hypothesis_of` adjacency.

**Not in the tree:** the abstention chain (EP-20 runs *before* this at runtime but is written after
it, because the chain's abstention outcomes are typed against the results this brief defines), and
any template or prose (EP-21). This brief emits concept IDs and integers, not sentences.

## Safety preconditions

- **R-3 (stereotyping / inferred identity), D-25.** Two guards. First, `normalise()` accepts an
  `InputEnvelope` and its signature explicitly excludes `UserUtterance` — the free-text field has no
  path into scoring, and a test asserts that no module under `src/epppsynth/select/` references
  `for_quotation` or the utterance field at all. Second, a facet set to `PREFER_NOT_TO_ANSWER` must
  score identically to `UNKNOWN`: declining to answer can never raise or lower any concept's score,
  and that is a property test, not a convention.
- **R-2 (automation bias / authority laundering).** Guard: integer scores are internal and
  test-visible only. Nothing in this brief writes a score into any type that EP-17's export
  chokepoint can serialize; the type-graph walk over `SelectionResult` enforces it.
- **R-17 (anchoring).** Guard: the `family` diversity rule and the mandatory counter-hypothesis
  pairing exist precisely so a reader is never handed five paraphrases of one reading. A property
  test asserts that any bundle of two or more waypoints spans two or more families.
- **Padding to hit a count is a safety failure, not a UX nicety.** Guard: the cardinality floor of
  three is enforced by *abstaining*, never by lowering the bar. A test plants a registry state where
  exactly two concepts survive and asserts the result is an insufficient-basis outcome with zero
  waypoints, not two waypoints and an apology.
- **Public artifact.** Golden files and fixtures are tracked and public. Every fixture envelope is
  manifestly fictional and carries the D-36 "no real person" attestation field. Re-run the EP-6
  pre-publication items before commit.

## In scope

1. Create `src/epppsynth/select/` with `normalise.py`, `gather.py`, `score.py`, `diversify.py`,
   `pair.py`, `floor.py`, `pipeline.py`, `types.py`. Every function is pure: same arguments, same
   result, no I/O, no module-level mutable state.
2. **Normalise.** `normalise(envelope) -> FacetVector` — a sorted tuple of `(facet, value,
   certainty)`. `certainty` is an integer: a declared value scores 2; `UNKNOWN`, `NOT_RELEVANT` and
   `PREFER_NOT_TO_ANSWER` all score 0. The free-text field contributes nothing.
3. **Gather.** Union of records whose `activation_predicate` clauses match any facet in the vector,
   read from EP-18's activation index. A dict lookup, not a search. Returns a sorted tuple of IDs.
4. **Filter,** in fixed order, each producing a typed reason record so EP-20 and the provenance
   drawer can say *why* something was dropped: `contraindicated_when` matches · `mode_scope`
   excludes the requested mode · `out_of_declared_scope_when` matches (recorded, and handed to EP-20
   as the D-38(1) scope-limit signal) · not in `registry.selectable()`.
5. **Integer score.** One module-level frozen table, `score.SCORING`, holding every constant, so
   nothing is buried in an expression:
   - `clause_weight` — authored per activation clause, integer 1–3, default 1;
   - `facet_certainty` — 2 declared, 0 otherwise (from step 2);
   - `confidence_ordinal` — `low` 1, `moderate` 2, `high` 3;
   - `evidence_bonus` — from `evidence_grade`: A 3, B 2, C 1, absent or not-applicable 0.

   `score(c) = (Σ over matched clauses of clause_weight × facet_certainty) × confidence_ordinal +
   evidence_bonus`. Every term is a small non-negative `int`; the function asserts
   `isinstance(result, int)`. This is the reconciliation of WS-1's ordered sort keys with WS-2's
   integer sum: evidence grade and confidence survive *inside* the integer, so the final sort key
   stays `(-score, concept_id)` and the tie-break stays purely lexicographic, as settled.
6. **Diversify.** At most one concept per `family` in the surviving set; within a family the winner
   is the highest score, ties broken lexicographically on ID. Families are sorted by their winner's
   sort key.
7. **Counter-hypothesis pairing.** For each survivor, take its `counter_hypothesis_of` partner with
   the best sort key among those that pass the same filters. If no partner clears the evidence
   floor, fill `counter_reading` from a module constant stating that no counter-reading in the
   registry clears the floor for this input. The field is never empty and never omitted — EP-17
   makes it structurally required and this brief guarantees a value exists.
8. **Cardinality.** Cap at 5. Fewer than 3 survivors is an insufficient-basis outcome for the whole
   bundle. No partial bundles, no padding.
9. **Evidence floor.** Two independent conditions, either of which converts the whole result to
   insufficient-basis: the sum of the top-k scores is below `SCORING.floor`, or the count of
   `unknowns` exceeds the count of `knowns`. Both thresholds live in `SCORING` with a written
   rationale; changing either requires regenerating golden files in the same commit, which CI
   checks.
10. **`SelectionResult`** in `select/types.py`: frozen, span-free, holding sorted tuples of selected
    IDs, their pairings, their per-concept `basis` ordinal, the `unknowns` list, and the typed drop
    reasons. Registered with EP-17's type-graph walk as an additional root.
11. **`epppsynth.tools.repeat_hash`** — a small module invoked as
    `python -m epppsynth.tools.repeat_hash --runs N --fixture F` that runs the pipeline N times,
    hashes each serialized result through EP-17's chokepoint, and prints one line
    (`N/N identical sha256=…`) exiting non-zero on any divergence. Used by this brief and by EP-23.
12. **`epppsynth.tools.purity_scan`** — invoked as
    `python -m epppsynth.tools.purity_scan <package-path>`. An AST walk that exits non-zero on any
    import of `random`, `time`, `datetime`, `uuid`, `secrets` or `os.urandom`, on any float
    literal, and on any unsorted iteration over a `dict` or `set`. It is used by this brief's
    acceptance and by **EP-23**, so it is built here rather than assumed.
13. **`epppsynth.tools.import_graph`** — invoked as
    `python -m epppsynth.tools.import_graph --module M` (print a module's transitive import
    closure) and `--forbid-edge A->B` (exit non-zero if that edge exists in the closure). It is the
    mechanism behind EP-20's zero-dependency escalation constant and EP-22's
    "ingest never on the synthesis path" assertion, both of which call it, so it is built here.
    Deliberately dependency-free: `ast` and `importlib` only.
14. Golden-file suite under `tests/select/golden/`, each file named by the version triple and
    regenerated by `uv run pytest tests/select --regenerate-golden`, which is refused when the
    working tree is dirty.
15. Write `docs/adr/ADR-004-integer-scoring-and-tie-breaking.md`, including the reconciliation
    recorded in scope item 5 and the reason lexicographic tie-breaking beats any "more informative"
    secondary key: an informative tie-break is an implicit ranking, and D-26(c) forbids ranking.

## Out of scope

- The abstention and hard-stop chain, and the escalation panel — **EP-20**.
- Any prose, template, or the question-or-offer linter — **EP-21**.
- Evaluation thresholds, stability floors and the counterfactual *harness* — **EP-24** and
  **EP-29**; this brief ships a smoke-level counterfactual check only.
- Mode (b) and mode (c) profile behaviour — **EP-47** and **EP-48**; `mode_scope` filtering is
  implemented here but only mode (a) is exercised.
- Any similarity search, embedding or retrieval on the emission path. Rejected for v1 by design and
  owned by no brief; the index serves authoring and the source pane only (**EP-22**, **EP-45**).

## Verification / acceptance

1. `uv run pytest tests/select -q` — green.
2. `uv run python -m epppsynth.tools.repeat_hash --runs 100 --fixture
   tests/fixtures/envelopes/EN-004.yaml` — prints `100/100 identical` and exits 0. **100 repeated
   runs on the same input are byte-identical.**
3. Cross-process determinism: the same fixture run in five subprocesses under five different
   `PYTHONHASHSEED` values produces one distinct hash.
4. **Purity scan:** `uv run python -m epppsynth.tools.purity_scan src/epppsynth/select` — the
   tool built in scope item 12 — exits 0 here, and its own unit tests show it exiting non-zero on
   a fixture containing each banned construct.
5. **Import graph:** `uv run python -m epppsynth.tools.import_graph --module epppsynth.select` —
   the tool built in scope item 13 — prints the closure, and `--forbid-edge` exits non-zero on a
   fixture edge that does exist and zero on one that does not.
6. Property tests: adding an `unknown` never adds a waypoint · removing a declared facet never
   increases any concept's score · `PREFER_NOT_TO_ANSWER` and `UNKNOWN` produce identical results ·
   any result with two or more waypoints spans two or more families · results are invariant under
   registry file reordering.
7. Cardinality tests: a registry state with two survivors yields an insufficient-basis outcome with
   zero waypoints; a state with nine survivors yields exactly five, from five distinct families.
8. Counter-hypothesis test: with the partner concept forced below the floor, `counter_reading` is
   the module constant and is non-empty.
9. Golden files committed and CI-checked for staleness against the recorded version triple.
10. *(judgement — owner)* The `SCORING` constants produce sensible selections on three fictional
   fixtures. Numbers chosen here are provisional and are revisited at the P3 re-plan (EP-31).

## Parked → final-roadmap.md

- Learned or tuned scoring weights. Out of scope for v1 by construction: any fitted weight makes the
  baseline non-auditable and would need its own evaluation.
- A "why not" explainer surfacing the typed drop reasons to the reader. The data is produced here;
  the affordance is a v1.x question because it risks reading as a ranking.
- Multi-registry or per-institution weight overlays.

---

> **EP-8 pickup note (2026-09-01).** The P0 re-plan's P2 consistency check found the one place this
> brief and **EP-11 (composer specification)** disagree, and EP-11 governs. §5 above describes
> `clause_weight` as *"authored per activation clause"*. EP-11's in-scope item 4(c) says the weight
> is keyed by `(input field, predicate kind)` in the composer's frozen `SCORING` table and is
> **never stored on a concept** — because EP-9's deny-list regex forbids a concept from carrying any
> ordinal, severity, score or count field, and a per-clause weight authored onto a concept would
> violate it. EP-11 asks for this to be raised on EP-19 and reconciled there; EP-11 has not run yet,
> so the note is raised here by the re-plan instead.
>
> **Nothing in this brief is changed.** Reconciling the two is EP-11's work, and EP-11 is a
> dependency of EP-17, which is a dependency of EP-18, which is a dependency of this brief — so the
> spec will exist before this brief is picked up. **Do not resolve it by relaxing EP-9's deny-list.**
