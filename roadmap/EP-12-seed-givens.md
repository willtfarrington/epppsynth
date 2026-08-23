# EP-12 — Seed content A: existential givens + ordinary-concern counter-frame

**Size:** L · **Mode:** a (records also scoped to b) · **Core/Stretch:** core ·
**Depends on:** EP-10 (Provenance, rights, reuse class, citation rule, authoring guide), EP-11
(Composer specification) ·
**Blocks:** EP-15 (critique-lens protocol and run), EP-16 (registry validator, re-plan P1)

## Context

The first of three seed-content briefs. It authors the `given` concepts — the existential dimensions
drawn from **one** Western-secular tradition, **labelled as one tradition among several** (D-14) —
their manifestation children, their question templates, and the permanent **ordinary-concern
counter-frame** that guarantees no existential reading is ever the only reading available.

This is the highest-reification-risk content in the registry (**R-11**), authored from the most
tightly rights-constrained source (a copyrighted monograph), in a domain where the founding
hypothesis has **no supporting evidence at all**. Every guardrail in EP-9, EP-10 and EP-11 exists
largely because of this content set.

**ID allocation (fixed by EP-9, do not deviate):** `EPS.GIV.0001–0020`, `EPS.QT.0001–0029`. Target
≈ 16 `given` records — four root dimensions plus roughly eleven manifestation children plus the
counter-frame — against the ≈ 40-concept registry target (D-47). **A thin registry that abstains
honestly beats a padded one**: if a dimension does not yield defensible children, author fewer.

**What exists at pickup.** The schema, `families.yaml`, `input_fields.yaml`, the closed
`question_intent` enum and `schema_check` (EP-9). `sources.yaml`, the permission matrix, the
chapter-level-only citation rule, the authoring guide with its register rules and hedge-deletion
test, and the attestation file (EP-10). `docs/composer-spec.md` with invariants `CI-1 … CI-9` and the
worked traces (EP-11). **No content exists.** EP-13 and EP-14 are independent of this brief and may
run before or after it.

Everything authored here lands at `review_status: draft`. Promotion to `accepted` or `blocked` is
**EP-15's** decision, not this brief's.

Commands run from the workspace directory `epppsynth/` unless a step says "from the git root".

## Safety preconditions

- **R-11 / failure mode Y-1 (reification).** A labelled given is a hypothesis that reads as a
  finding. Guards, all structural: every `given` carries ≥ 1 `counter_hypothesis_of` edge and the
  set is symmetric-complete (EP-9 rule (h)); the composer pairs every emission with a counter-reading
  and an insufficient-basis clause (`CI-1`); and the prose itself must pass the authoring guide's
  **hedge-deletion test** — delete every hedge and if the remainder asserts something about a person,
  rewrite it.
- **Y-3 (universality smuggling).** Every record carries `tradition:` naming the framing,
  `cultural_scope.origin: western-secular`, `claims_universality: false`, and an **empty**
  `tested_in` list — the honest value. Every root given carries an
  `out_of_declared_scope_when` edge on the `outside-declared-scope` framework enum value, so the
  scope limit is **data**, not engine judgement (D-14, D-38.1).
- **Y-5 (category exhaustion).** Four dimensions imply the space is covered, so a fifth thing gets
  forced into one of four boxes. Guard: the **ordinary-concern counter-frame** (step 4) is a
  permanent, always-selectable record occupying its own family, injected by the composer as a
  mandatory floor member outside the cap.
- **Y-6 / R-17 (anchoring).** Every question template authored here is a **question or an offer**
  (`form`), never a conclusion to confirm, and is `disconfirming: true` wherever the intent allows
  it. The anchoring risk is untested; the concept prose must not claim otherwise.
- **Y-7 (authorial voice as authority).** The source's clinical-literary register carries persuasive
  force the registry would inherit. Guard: `derivation_mode: reading-informed-original`, plain hedged
  non-narrative prose, no aphorism, no vignette opening. Register is reviewed again by EP-15.
- **Y-8 / R-7 (rights leakage through structure).** Guards: chapter-level locators only, no page
  ranges, no quoted phrase, no chapter title reused as a label, and the locator-sequence lint. The
  four root dimensions must **not** be presented in the source's order, and the concept labels must
  be the author's own phrasings, not the source's coinages. Every record needs an attestation with an
  honest `residual_concern`.
- **R-41 (cultural flattening).** The declared scope is Western-secular and where a person's framework
  falls outside it the required behaviour is **explicit abstention naming the limit** — never
  adaptation, analogy or a generic humanistic substitute. This brief's contribution to that is the
  `out_of_declared_scope_when` edges and the honest `known_misfit` notes.
- **No ordinals (Y-4, R-16).** No record may carry a score, severity, count or ordinal field. The
  schema deny-list enforces it; do not attempt to encode "how strong" a given is.
- **Public-safety (D-3, R-6).** All prose is public and must be original. No phrase from any
  copyrighted source; no PHI pattern; no real person; no local path, machine name or account name;
  no clinical vignette that could read as a real case. Re-run the EP-6 pre-publication packet for
  *protected text*, *quotation budget*, *PHI patterns* and *local paths*.
- **Not clinical guidance.** These records describe *possible readings available to the clinician*,
  never properties of a person, and never what a person of a given background, diagnosis, functional
  status, age or belief system experiences.

## In scope

1. **Read the inputs, in this order:** `docs/authoring-guide.md` (register rules, abridgement
   anti-patterns, the `derivation_mode` decision tree, the attestation statement), then
   `docs/registry-schema.md` §Concept fields, then `docs/composer-spec.md` §Invariants and §Pipeline
   stage (e).

   **Do not open the source material, in this session or any other, for any purpose — including the
   chapter-title exclusion list.** `GOVERNANCE.md` §15 is a session rule that overrides every brief:
   *never read or quote the corpus*. This brief claims no exception to it, and an earlier draft that
   did was wrong. The chapter-title exclusion list is built **only from local generated metadata** —
   the `spine.toml` descriptor and `index-manifest.json` that EP-22's ingest writes to the index
   root, both of which live outside the repository tree and may hold titles — and **never by
   opening, reading, scanning or quoting the source text**. If that metadata does not carry a title,
   the title is simply absent from the list; the correct response is a narrower list, never a look at
   the book. The list itself is **local-only**: it lives beside the manifest outside the tree, is
   never committed, never enters CI, never appears in a published artifact or a completion note, and
   is consumed only by the local lint that compares an authored `label` against it. The corpus is out
   of the repository tree and never enters CI (D-10, D-16, D-51).

2. **Author four root `given` records** — one per existential dimension of the declared tradition,
   each in original prose:
   - `label` — the author's own phrasing of the dimension, never the source's coinage and never a
     chapter title;
   - `prose` — three to five plain sentences that (i) attribute the framing to the tradition, (ii)
     name what it might look like in an encounter, and (iii) state in the same paragraph that it may
     equally not be present and is one reading among several;
   - `tradition` — the tradition label rendered beside the given in the UI (Y-3);
   - `family` — each root given takes a **different** family (finitude-and-time,
     agency-and-control, connection-and-isolation, meaning-and-coherence, per EP-9's family set), so
     the composer's one-per-family rule produces genuinely different dimensions;
   - `locus: personal-meaning` on the root givens;
   - `mode_scope: [a, b]` — root givens are not mode-(c) content; the `condition` set (EP-14) is;
   - `activation_predicate` — keyed on `illness_stage` and `encounter_temporality` only. **Do not**
     key any predicate on `self_described_framework`, `language_interpreter_need` or
     `uncertainty_tolerance`: EP-9 declared the first two non-substance-bearing (framing-only /
     additive-only) and the third invariant, and a predicate on them would violate the declaration.
   - `evidence: {claim_type: interpretive, empirical_support: none}` — this is the honest value and
     it must not be softened;
   - `confidence: low` on every root given, with the definition from the schema (confidence that the
     framing is defensible, never that it applies to a person);
   - `contested_interpretations` — at least one per root given, written before any lens runs. The
     obvious one, and the one to write: that the category may be an artefact of a particular
     mid-twentieth-century Western psychotherapeutic idiom rather than a feature of human
     experience.

3. **Author the manifestation children** — roughly eleven `given` records reached by
   `may_manifest_as` from the roots. Each child is **more specific in its activation predicate** than
   its parent (that is what earns it a rank position under EP-11's integer specificity score) and
   names an observable pattern in the supplied input, not an inner state. Children inherit the
   parent's family. Each child needs its own `counter_hypothesis_of` partner, its own `invites`
   edges, and its own provenance and attestation. A child that cannot be written without asserting
   something about a person is not written.

4. **Author the permanent ordinary-concern counter-frame** — `EPS.GIV.0020`. (Steps 2 and 3 consume
   `EPS.GIV.0001` upward — four root givens then roughly eleven manifestation children — so the
   counter-frame cannot also be `EPS.GIV.0004`, which step 2 has already allocated. It takes the
   **last** ID in EP-9's `EPS.GIV.0001–0020` allocation, which is stable no matter how many children
   are authored and marks it as the permanent floor member rather than one given among many. Any
   reference to the counter-frame as `EPS.GIV.0004` is the collision, not the authority.) This record exists so that no existential reading is ever emitted alone:
   the plainest reading is often the right one, and a person may be attending to schedules, costs,
   childcare or work because those are the actual problems in front of them, with no existential
   dimension to find. Properties: `tradition: counter-frame`; `locus: structural`;
   `family: ordinary-and-structural` (its own family, occupied by nothing else);
   `derivation_mode: author-original`; `evidence: {claim_type: normative-design, empirical_support:
   not-applicable}`; `confidence: high`; `counter_hypothesis_of` edges to **every** root given, and
   every root given lists it back (symmetric-complete); `activation_predicate: {}` — **always
   selectable**. Mark it in the file with a comment naming Y-5 as its reason, so a future editor
   cannot delete it as redundant.

5. **Author the question templates** — `EPS.QT.0001–0029`, one or more per `given`, each with:
   `form` (`question` or `offer`, no third value); `question_intent` from the **closed** enum
   (`elicit-values`, `check-understanding`, `ask-permission`, `surface-concern`, `clarify-goal`,
   `invite-question`, `name-uncertainty`, `offer-referral`); `requires_permission`;
   `disconfirming`. Rules:
   - at least one template per root given has `question_intent: ask-permission` and
     `requires_permission: true`, so the encounter can be declined before it is opened;
   - at least one template per root given is `disconfirming: true` — a question whose honest answer
     could be "no, that is not it";
   - at least one `offer-referral` template exists across the set, satisfying the
     generalist-spiritual-care guardrail (Y-2) that every existential concept has a referral path;
   - **no template asserts.** No template names what the person feels, needs, or should do. Apply the
     hedge-deletion test to templates as well as to concept prose.

6. **Wire the relations.** For every record: exactly one `family`; ≥ 1 `counter_hypothesis_of` with
   the reverse edge present; ≥ 1 `invites`; `constrained_by` edges to the `principle` and `caution`
   records **by ID** — EP-14 owns those IDs, and EP-9's allocation table fixes them, so the edges can
   be written now and will resolve once EP-14 lands. If EP-14 has not yet run, `schema_check` will
   report dangling `constrained_by` targets: record them in the completion note as **expected**, and
   note that EP-16 is the brief where the whole graph must resolve. Every root `given` carries
   `out_of_declared_scope_when: {self_described_framework: [outside-declared-scope]}`.

7. **Provenance, rights and attestation for every record.** `source_id` resolving into
   `sources.yaml`; `derivation_mode` from EP-10's decision tree (`reading-informed-original` for the
   tradition-derived records, `author-original` for the counter-frame); a `short_citation` that is a
   **chapter-level locator only** — author surname, year, short title, at most one part or chapter
   number, no page range, no quoted phrase; `page_or_locator` left empty or local-only; an
   `attestation_id` with a truthfully filled `residual_concern`. Do not write "none" into
   `residual_concern` for a record authored from a copyrighted monograph unless it is genuinely true.

8. **Coverage self-check against the composer spec.** Before committing, hand-run three of the EP-11
   traces' input tuples against the authored set on paper and record in the completion note, per
   input: how many concepts survive selection and filtering, how many families they span, and whether
   three survive diversification. Any input where fewer than three survive is a **content** finding
   (A-W1), not an engine finding, and belongs in the completion note and in the EP-16 re-plan. This
   is a manual dry-run; the mechanised one needs the P3 scenarios (EP-25).

9. **Set every record to `review_status: draft`,** `version: 1`, `created` today, `lang: en`,
   `variant_of: null`, `lenses_applied: []`, and a computed `content_hash`. Promotion is EP-15's.

10. **Documentation.** No new doc file. Add a one-paragraph note to `DESIGN.md` §Content recording
    what was authored, the ID ranges consumed, and the manual dry-run result. Do **not** write a
    public narrative about the tradition — that is EP-53.

## Out of scope

- `function` concepts and the evidence appendix → **EP-13**.
- `principle`, `condition` and `caution` records → **EP-14** (this brief writes `constrained_by`
  edges pointing at their allocated IDs).
- Applying the critique lenses, and any promotion out of `draft` → **EP-15**.
- Cross-file validation that the whole relation graph resolves, the rendered markdown, and the CI job
  → **EP-16**.
- The charter clauses about anti-essentialism and scope declaration → **EP-3** (`SAFETY.md`).
- The user-facing scope-declaration string and the abstention copy → **EP-39** (copy deck).
- The on-screen rendering of the `tradition` label beside a given → **EP-43** (waypoints panel).
- Any non-Western or non-secular framework → **excluded by decision** (D-14); the enforcement here is
  labelling plus the `out_of_declared_scope_when` edges, and the tested abstention lives in
  **EP-30**.
- The mechanised coverage dry-run over the development scenarios → **EP-25** / **EP-24**.

## Verification / acceptance

- `uv run python -m epppsynth.registry.schema_check --rights` exits `0` except for `constrained_by`
  targets that EP-14 has not yet authored; those and only those may be outstanding, and the run with
  `--allow-forward-refs` exits `0`.
- `uv run python -m epppsynth.registry.schema_check --rights --json` reports: every `given` has ≥ 1
  `counter_hypothesis_of` and the set is symmetric-complete; every record has exactly one `family`;
  `claims_universality` is `false` on all of them; zero ordinal-field violations; zero citation
  violations; the quoted-word total for the monograph source is **0**.
- `uv run python -m epppsynth.registry.schema_check --path registry/concepts/givens.yaml --json`
  shows every root `given` carrying an `out_of_declared_scope_when` edge on
  `outside-declared-scope`.
- A grep-style assertion in `tests/ep/test_ep12.py`: no `question_template` in the allocated range
  has a `form` other than `question` or `offer`; every root given has ≥ 1 `ask-permission` and ≥ 1
  `disconfirming: true` template; ≥ 1 `offer-referral` template exists; the counter-frame record
  exists, has an empty `activation_predicate`, and is a `counter_hypothesis_of` partner of every root
  given.
- `uv run pytest tests/ep/test_ep12.py -q` green.
- From the git root: `python tools/roadmap_check.py --context-budget EP-12` passes.
- Pre-publication packet (EP-6) re-run for *protected text*, *quotation budget*, *PHI patterns* and
  *local paths*; output recorded in the completion note.
- *(judgement — author)* The hedge-deletion test is applied to every `prose` field and every
  `question_template.text`, and the completion note records how many records were rewritten because
  of it. Zero rewrites across ~16 records is a signal the test was not really applied.
- *(judgement — author)* The four root dimensions are not presented in the source's order, and no
  label is the source's coinage or a chapter title (Y-8).
- *(judgement — author)* Every `residual_concern` is truthful; at least one is non-null.
- Completion note records the step-8 manual dry-run: concepts surviving, families spanned, and any
  input falling below three.
- Commits: `feat(epppsynth): seed content A — existential givens and ordinary-concern counter-frame
  (EP-12)` then `docs(roadmap): record EP-12 commit hash`.

## Parked → final-roadmap.md

- Additional manifestation children beyond the ~11 authored here, if the P3 coverage dry-run (EP-25)
  shows scenarios falling below three survivors.
- A second tradition alongside the first — **excluded by decision** in v1 (D-14), recorded here only
  so the exclusion is visible from the content brief that would otherwise be its home.
- Non-English `variant_of` records for the given set.
- An automated register linter (aphorism, vignette-opening and second-person detection) to mechanise
  part of the Y-7 guard that is currently judgement.
- Whether the ordinary-concern counter-frame should also be selectable in mode (c), where `CI-8`
  already supplies a structural floor.
