# EP-9 — Registry schema v0: types, relations, IDs, versioning

**Size:** L · **Mode:** n/a · **Core/Stretch:** core ·
**Depends on:** EP-2 (Canonical docs + public front matter + badge scheme) ·
**Blocks:** EP-10 (provenance and authoring guide), EP-11 (composer specification), EP-16 (registry
validator, re-plan P1), EP-18 (registry loader), EP-28 (substance-tuple extractor)

> **PICKUP GATE — owner input required before this brief starts (EP-8, 2026-09-01).** Three items
> closed P0 unresolved and none can be settled by a session: **OD-2** (does `SAFETY.md` §4 match the
> approved wording?), **OD-8** (does the issue form render, and do its two checkboxes block
> submission?), and **EP-8 acceptance 12** (is this brief executable cold? — **blocking**, because
> the answer can change it). Each carries three lettered choices and what to do with each answer in
> [`pickup-gate.md`](pickup-gate.md). **Open that file and put all three to the owner before doing
> any EP-9 work.** Delete this block when all three are resolved.

## Context

This brief writes the data model every later phase reads. It implements **D-15** (YAML/JSON concept
registry with stable IDs, typed relations, and per-concept provenance / rights / confidence /
cultural-scope / review-status / contested-interpretations; no formal ontology, no graph DB) and the
schema half of **D-53** (a waypoint is a *render*, never a stored object).

Two planning workstreams proposed incompatible schemas. The settled merge, which this brief
implements and which is not reopened here:

- The **concept taxonomy and ID scheme are canonical** — five concept types (`given`, `function`,
  `principle`, `condition`, `caution`), nine typed relation kinds, `EPS.<TYPE3>.<NNNN>` IDs,
  tombstoning rather than deletion, `lang` / `variant_of`.
- **Three fields are added** that later phases cannot work without:
  1. a **`family` grouping edge** — the engine emits at most one concept per family in the top-k,
     which is the mechanism that produces plural hypotheses across *genuinely different* dimensions
     rather than four restatements of one dimension;
  2. a **closed `question_intent` enumeration** on every question template — without a closed set the
     P3 substance comparator (EP-28) has nothing to compare;
  3. a **three-way `sensitivity` declaration** per input field — `invariant` /
     `clinically-load-bearing` / `framing-plus-one-permitted-additive-waypoint` — each with a written
     rationale (**D-73**).
- Ranking is **integer-scored with a lexicographic tie-break on concept ID**. No floats anywhere, so
  ties are exact and output is bit-reproducible. Scores are **computed at request time and never
  stored on a concept** — see the deny-list in step 6.

**What exists in the tree at pickup.** `epppsynth/` is the uv workspace (EP-1) with `src/`, `tests/`,
`docs/` and an ADR directory. `epppsynth/DESIGN.md`, `GOVERNANCE.md` and `DECISIONS.md` exist (EP-2).
The licensing pack and the per-source rights table skeleton exist (EP-5) but **`sources.yaml` is not
populated** — that is EP-10. No registry directory, no concept, no validator, no engine code exists.
`tools/roadmap_check.py` exists (EP-8).

**What this brief does not do.** It authors *no* clinical or existential content beyond
schema-illustrative fixtures in a reserved ID band, and it writes no selection code.

Commands below run from the workspace directory `epppsynth/` unless a step says "from the git root".

## Safety preconditions

- **R-11 (concept reification) / failure mode Y-1.** The schema is the first place reification can be
  designed out. Guard: `counter_hypothesis_of` is a **required, non-empty** relation on every
  *emittable* type (`given`, `function`, `condition`) and every edge must resolve to an existing
  non-deprecated concept of the same type. `principle` and `caution` are non-emittable (they filter
  and trigger), so the requirement does not apply to them — a deliberate narrowing recorded in step 2.
- **Y-3 (universality smuggling).** `cultural_scope.claims_universality` is a **constant `false`**:
  the JSON Schema pins it with `const: false` and the checker rejects `true` with no exception path
  and no override flag. `cultural_scope.tested_in` may be an empty list — an empty list is the honest
  statement, not a defect.
- **Y-4 (diagnostic drift) / R-16.** No concept may carry an ordinal, severity, score or count field.
  Guard: a schema **deny-list plus a field-name regex** (step 6), with exactly two allow-listed
  graded fields, each named by literal path and each carrying a written rationale in the spec.
- **R-13 (registry accretion without provenance).** Every provenance, cultural-scope and review field
  is `required` in the JSON Schema from the first commit, so a concept cannot be added now and
  "filled in later".
- **Public-safety (D-3, R-6, GOVERNANCE §Public-safety).** Everything written here is public. The
  worked examples must be **original prose** containing no phrase from any copyrighted source, no
  chapter title, no page range, no real person, no local filesystem path, no machine name, no account
  name. Re-run the EP-6 pre-publication packet items for *protected text*, *local paths* and *PHI
  patterns* before committing.
- **Rights (D-62, R-15).** This brief adds the `reuse_class` **field**; it makes no claim about any
  actual source's terms. Every example uses `reuse_class: reference-only-pending-rights-check`, the
  conservative value. Clearing it is EP-10's job.
- **Not a clinical artifact.** Nothing here is or contains clinical guidance; the examples are schema
  fixtures. No hard-stop or escalation behaviour is defined here (EP-11 specifies it, EP-20
  implements it).

## In scope

1. **Directory layout.** Create and document:

   ```
   epppsynth/registry/
     schema/          concept.schema.json · question_template.schema.json
                      family.schema.json · lens_finding.schema.json · source.schema.json
                      input_field.schema.json · registry.meta.json
     concepts/        givens.yaml · functions.yaml · principles.yaml · conditions.yaml · cautions.yaml
     question_templates.yaml
     families.yaml
     input_fields.yaml
     lens_findings.yaml
     sources.yaml            (skeleton only here; populated by EP-10)
     examples/               schema fixtures in the reserved 9000 ID band
   epppsynth/docs/registry-schema.md      the human-readable spec (canonical prose)
   ```

   All registry files are UTF-8, LF, two-space YAML indent, keys in the order the spec lists them.
   `registry.meta.json` carries `schema_version: "0.1.0"`, `registry_version` (integer, monotonic)
   and `id_high_water` per type — the last two are what EP-18's migrations read.

2. **Five concept types and their emittability.** Write this table into `docs/registry-schema.md`:

   | Type | `TYPE3` | Emittable | What it is |
   |---|---|---|---|
   | `given` | `GIV` | yes | A named existential dimension, always labelled as one tradition's framing |
   | `function` | `FUN` | yes | A conversational *function* (elicit, check understanding, offer permission) |
   | `principle` | `PRN` | no | A constraint that filters or reshapes any emission |
   | `condition` | `CON` | yes | A structural / relational condition of clinical work (mode-(c) substrate) |
   | `caution` | `CAU` | no | An anti-pattern, contraindication or abstention trigger |

   **Emittable** means the type may appear in a composed output and therefore must satisfy D-53's
   pairing rule. Record the narrowing explicitly: the source design required a counter-hypothesis
   partner on `given` only; D-53 says *no concept is ever emitted alone*, so the requirement is
   extended to every emittable type and dropped for the two that are never emitted.

3. **Relations.** Nine relation *kinds*, eleven edge names (`evidence_for` / `evidence_absent_for`
   are the two poles of one kind), plus the added `family` grouping edge. Each edge carries a
   required `basis` naming the concept IDs or the `source_id` that licenses it.

   | Edge | Domain → range | Cardinality | Notes |
   |---|---|---|---|
   | `may_manifest_as` | `given` → child `given` | 0..n | Always defeasible; the child is a manifestation, not a subtype |
   | `counter_hypothesis_of` | emittable ↔ same-type emittable | **≥ 1, symmetric-complete** | If A lists B, B must list A; the checker fails otherwise |
   | `invites` | any concept → `question_template` | **≥ 1 on emittable** | The emitted utterance always comes from here |
   | `constrained_by` | any concept → `principle` \| `caution` | 0..n | — |
   | `contraindicated_when` | concept → input-enum predicate | 0..n | e.g. a hard-stop flag present |
   | `out_of_declared_scope_when` | concept → framework-enum value | **≥ 1 on `given`** | Fires abstention (D-38.1) |
   | `alternative_reading` | concept → `LENS.*` finding ID | 0..n | Renders as a contested interpretation |
   | `evidence_for` / `evidence_absent_for` | `function` → `source_id` | `evidence_absent_for` **required** where no inspected source supports the function | D-63 |
   | `escalates_to` | `caution` → escalation-copy ID | 0..n | Deterministic only (D-18) |
   | `family` *(added)* | any concept → `EPS.FAM.<NNNN>` | **exactly 1, required** | The diversity key |

   `family` is modelled as an **ID-bearing record**, not a free string, so each family can carry the
   dimension it names and the rationale for treating it as distinct — which is what makes the
   one-per-family rule auditable rather than a naming accident.

4. **`families.yaml`** — author ~14–16 families covering the four content sources, each with `id`
   (`EPS.FAM.<NNNN>`), `label`, `dimension` (one sentence naming the axis), `rationale` (why it is
   *not* the same axis as its nearest neighbour) and `expected_types`. Suggested axes, adjustable at
   authoring: finitude-and-time · agency-and-control · connection-and-isolation ·
   meaning-and-coherence · ordinary-and-structural · information-and-disclosure ·
   understanding-and-uncertainty · permission-and-pacing · values-and-what-matters ·
   safety-and-trust · institutional-constraint · relational-rupture · witnessing-and-complicity ·
   scope-and-referral. Families are **not** concepts: they carry no prose the user ever sees.

5. **Required concept fields.** Fix the field list, ordering and types in `concept.schema.json` and
   mirror them in the spec prose:

   `id` · `type` · `label` · `lang` (`en` in v1) · `variant_of` (nullable, reserved) · `prose` ·
   `family` · `locus` (`structural` \| `relational` \| `personal-meaning`; **required on `condition`
   and on any concept whose `mode_scope` includes `c`**) · `mode_scope` (subset of `a`,`b`,`c`) ·
   `activation_predicate` (map of input-field name → list of enum values, or `any`) · `relations` ·
   `provenance` (block; field list owned by EP-10) · `reuse_class` (owned by EP-10) ·
   `cultural_scope` (`origin`, `claims_universality: false`, `tested_in[]`, `known_misfit?`) ·
   `evidence` (`claim_type`, `empirical_support`; on `function` also `evidence_grade`,
   `supported_claim`, `not_supported`) · `contested_interpretations[]` (`{text, ref}`) ·
   `review_status` · `lenses_applied[]` · `confidence` (`low`\|`moderate`\|`high`) ·
   `version` (integer, monotonic) · `content_hash` · `created` · `last_reviewed` · `changelog[]`.

   `confidence` is defined in the spec as **confidence that the concept is a defensible framing** —
   never confidence that it applies to a person — and is shown in the provenance drawer only (D-48).

6. **The no-ordinal rule, made precise.** Write the deny-list into the schema *and* the spec:
   `additionalProperties: false` on every record type, plus a checker rule failing on any field name
   matching `(?i)(score|rank|severity|grade|level|count|tally|index|percent|weight|priority|ordinal)`
   anywhere in a concept record. **Exactly two allow-listed exceptions**, each named by literal path
   and each with a written rationale in the spec:
   - `evidence.evidence_grade` — grades a *source's* evidentiary standing, never a person or a
     concern;
   - `confidence` — grades a *framing's* defensibility, never a person or a concern.

   Everything else is denied. Record the reasoning explicitly: the source design's ranking sketch
   included a stored `specificity_score`, which this rule forbids. Ranking inputs are **derived at
   request time from `activation_predicate` and `evidence_grade`** (EP-11); nothing computed is ever
   written back to a concept. This is the schema-level enforcement of "no concept may carry an
   ordinal, severity, score or count field".

7. **ID scheme, versioning and lifecycle.**
   - `EPS.<TYPE3>.<NNNN>` — namespace-prefixed, type-tagged, zero-padded to four digits, monotonic,
     **never reused, never renumbered**. Type is in the ID so a mis-typed relation is detectable
     without a lookup. Fixed width means byte-wise lexicographic order equals numeric order within a
     type, which is what makes EP-11's tie-break exact.
   - Non-concept namespaces: `EPS.QT.<NNNN>` (question templates), `EPS.FAM.<NNNN>` (families),
     `SRC.<SHORTNAME>` (sources), `LENS.<LENS3>.<NNNN>` (findings).
   - **Retired band: `EPS.FRM.<NNNN>` (framings).** The `framing` record kind existed only to supply
     output part (iv), the values-to-options frame; that part was **deleted** from the output
     contract rather than left undeliverable, so the record kind, its schema, its file and its ID
     band are all removed. Consistent with the never-reused, never-renumbered rule above, **`FRM`
     identifiers are never reused** and the band is never reallocated to another record kind. Do not
     reintroduce the kind to "restore" part (iv).
   - **Reserved band:** `EPS.<TYPE3>.9000`–`9999` is for schema fixtures under `examples/` only.
     Content authoring never allocates there; the validator excludes the band from the shipped
     registry while still schema-checking it.
   - **Allocation ranges for the seed briefs**, recorded here so three parallel briefs cannot
     collide: EP-12 → `GIV.0001–0020`, `QT.0001–0029`; EP-13 → `FUN.0001–0012`, `QT.0030–0049`;
     EP-14 → `PRN.0001–0008`, `CON.0001–0010`, `CAU.0001–0012`, `QT.0050–0069`.
   - `version` is an integer bumped on any change to `prose` or `relations`; `content_hash` is
     `sha256` over the normalised (NFC, LF, trailing space stripped, keys sorted) prose + relations.
     Changing prose without bumping `version` is a checker failure. Every bump appends
     `{version, date, change, reason, lens_finding_id?}` to `changelog`.
   - `review_status` state machine: `draft` → `lens-review` → `accepted` \| `blocked`;
     `accepted` → `deprecated`; `blocked` → `accepted` **only** with a dated, published
     `override_rationale` (D-45); `blocked` → `deprecated`. Only `accepted` may be emitted. Encode
     the machine as an explicit transition table in the spec and as a checker rule.
   - **Tombstoning, never deletion.** A withdrawn concept keeps its ID, takes
     `review_status: deprecated`, gains a **required** `deprecation_reason` and an optional
     `superseded_by`, is excluded from selection, and stays in the file and in the rendered markdown
     under "withdrawn / not adopted" (D-46).
   - **Language.** `lang: en` on every record; v1 is English-only and says so as a scope statement.
     `variant_of` is reserved so a future translation is a **sibling record with the same concept
     identity and a different `lang`**, never an edit of the English record.

8. **`question_template` records and the closed `question_intent` enum.** Fields: `id` · `lang` ·
   `text` · `form` (`question` \| `offer`; no third value exists) · `question_intent` ·
   `requires_permission` (bool) · `disconfirming` (bool) · `mode_scope` · `provenance` ·
   `review_status` · `version` · `content_hash`.

   The **closed** `question_intent` enumeration for schema v0.1.0 is exactly:
   `elicit-values` · `check-understanding` · `ask-permission` · `surface-concern` · `clarify-goal` ·
   `invite-question` · `name-uncertainty` · `offer-referral`.

   Seven come from the evaluation design's substance-tuple definition, which gave them as an
   illustrative list and required only that the set be closed. `offer-referral` is added here because
   the generalist-spiritual-care guardrail (Y-2) requires every existential concept to have a
   referral path, and a referral has no other intent to be classified under. Record the addition and
   its reason in the spec. **Closed means closed:** adding a value is a `schema_version` minor bump
   plus a re-run of the P3 substance comparator (EP-28), and the spec says so.

9. **`input_fields.yaml` and the three-way sensitivity declaration (D-73).** One record per D-25
   field: `name` · `enum_values[]` (every field also carries `unknown`, `not-relevant`,
   `prefer-not-to-answer`) · `sensitivity` ∈ {`invariant`, `clinically-load-bearing`,
   `framing-plus-one-permitted-additive-waypoint`} · `rationale` (required prose) ·
   `permitted_effect` (required prose: exactly what this field may change) ·
   `counterfactual_suite_ref` (the P3 suite that pins it — EP-29).

   Author the eight records with these dispositions, each rationale written out in full. `free_text`
   is **not** among them — see the note below the table:

   | Field | `sensitivity` | Permitted effect |
   |---|---|---|
   | `role` | clinically-load-bearing | selects the `mode_scope` filter, nothing else |
   | `encounter_temporality` | clinically-load-bearing | gates `activation_predicate` matching |
   | `stated_information_preference` | clinically-load-bearing | the person's own stated preference about disclosure *must* change what is emitted |
   | `stated_decision_sharing_preference` | clinically-load-bearing | same |
   | `illness_stage` | clinically-load-bearing | gates `activation_predicate` matching |
   | `self_described_framework` | **invariant** | framing only — with the single literal value `outside-declared-scope` firing the abstention path by schema, so scope is data, not engine judgement (D-14, D-38.1) |
   | `uncertainty_tolerance` | invariant | wording of the uncertainty text only; uncertainty content itself is mandatory regardless (D-58) |
   | `language_interpreter_need` | **framing-plus-one-permitted-additive-waypoint** | the one additive waypoint is the fixed interpreter note; it adds, never substitutes, and never removes a concept |
   | `free_text` | *(not applicable — see note)* | none: quoted back verbatim and nothing else |

   **`free_text` carries no sensitivity classification, and the schema must not accept one for it.**
   The three-way declaration classifies *how a field may change what is emitted*; `free_text` is an
   **inert echo** (GOVERNANCE §4.2, `DESIGN.md` §3) that cannot affect substance, framing, or
   selection at all, so there is nothing for a sensitivity class to describe. It is recorded in
   `input_fields.yaml` as an `echo_only: true` record carrying `rationale` and
   `counterfactual_suite_ref` but **no** `sensitivity` and **no** `permitted_effect`; `schema_check`
   fails a `free_text` record that declares either. This is settled, not pending: there is no
   fourth sensitivity value, no carve-out, and no owner ratification outstanding.

10. **Worked examples in the reserved band.** Under `examples/`, one record per concept type plus one
    `question_template`, one `family` and one `lens_finding` — **original prose**,
    schema-illustrative, IDs in the 9000 band. Each example must exercise at least one required-field
    edge case (an empty `tested_in`, a non-empty `contested_interpretations`, a `deprecated`
    tombstone).

11. **`schema_check` — the runnable conformance checker.** Ship
    `src/epppsynth/registry/schema_check.py`, runnable as `python -m epppsynth.registry.schema_check`,
    with `--path`, `--json` and `--include-examples`. Rule groups implemented **here**:
    (a) every record validates against its JSON Schema; (b) `claims_universality` is `false`;
    (c) the ordinal deny-list regex with its two allow-listed paths; (d) ID format, uniqueness, band
    and allocation-range conformance; (e) `content_hash` / `version` consistency; (f) `review_status`
    transitions legal against `changelog`; (g) every `family` and every relation target resolves;
    (h) `counter_hypothesis_of` symmetric-complete over emittable types; (i) `question_intent` in the
    closed enum and `form` ∈ {`question`, `offer`}. Exit `0` clean, `1` on any violation, `2` on a
    usage error; one line per violation as `<file>:<id>: <rule-id>: <message>`. Cross-file rights,
    citation and lens-coverage rules are **not** here — they are EP-10's and EP-16's.

12. **Tests** (`tests/ep/test_ep09.py`): each rule group gets a passing fixture and a failing fixture
    built in `tmp_path`. `claims_universality: true` fails; a stored `specificity_score` fails; a
    reused ID fails; an asymmetric counter-hypothesis pair fails; a prose edit without a version bump
    fails; `blocked → accepted` with no `override_rationale` fails; an out-of-band ID under
    `concepts/` fails; a ninth `question_intent` value fails.

13. **Documentation.** Write `docs/registry-schema.md` as the canonical prose spec — it is what later
    briefs read, not the JSON. Add an ADR recording the three merged-in fields and the two
    allow-listed graded fields with their rationales. Add a dated addendum under **D-15** in
    `DECISIONS.md` recording that `family`, `question_intent` and the three-way `sensitivity`
    declaration are schema requirements, and under **D-73** recording that `free_text` is excluded
    from the declaration entirely as an inert echo. Add
    the registry paths to `DESIGN.md` §Traceability.

## Out of scope

- Populating `sources.yaml`, the `provenance` block's field semantics, `reuse_class` values, the
  citation rule and the authoring guide → **EP-10**.
- Selection, filtering, ranking, capping, composition, the abstention precedence chain and the
  substance-tuple serialization → **EP-11** (spec); **EP-19 / EP-20 / EP-21** (implementation).
- Any real `given`, `function`, `principle`, `condition` or `caution` content → **EP-12**, **EP-13**,
  **EP-14**.
- The lens question sets, severity semantics and coverage gate → **EP-15**.
- Cross-file validation, the rendered markdown and the CI job → **EP-16**.
- Typed Python dataclasses / models over these records → **EP-17** (contracts package).
- Loader, `schema_version` migrations and the `(contract, registry, template)` version triple →
  **EP-18**.
- Any change to the D-25 input field list itself → owner decision; D-25 fixes the list and this brief
  only annotates it.

## Verification / acceptance

- `uv run python -m epppsynth.registry.schema_check --include-examples` exits `0` and reports the
  rule-group count and the record count per type.
- `uv run python -m epppsynth.registry.schema_check --path registry/examples --json` emits valid JSON
  with `"violations": []`.
- `uv run python -m epppsynth.registry.schema_check --path tests/fixtures/ep09/universality-true`
  exits `1` with the `claims_universality` rule as the only violation — proving the guard fires
  rather than merely existing.
- `uv run pytest tests/ep/test_ep09.py -q` green, with at least one failing-fixture test per rule
  group in step 11.
- `uv run ruff check .` and the project type check green.
- From the git root: `python tools/roadmap_check.py --context-budget EP-9` passes.
- Pre-publication packet (EP-6) re-run for *protected text*, *local paths* and *PHI patterns*; scan
  output recorded in the completion note. Scanners are defense in depth, never proof.
- *(judgement — author)* Every family's `rationale` names the nearest family it is **not**. A family
  whose rationale cannot distinguish it from its neighbour is merged before commit.
- *(judgement — author)* The `input_fields.yaml` rationales are written prose, not restatements
  of the enum value.
- Commits: `feat(epppsynth): registry schema v0 — types, relations, IDs, versioning (EP-9)` then
  `docs(roadmap): record EP-9 commit hash`.

## Parked → final-roadmap.md

- Non-English concept variants via `variant_of` — the field is reserved and unused in v1.
- A schema-diff tool reporting breaking vs additive changes between `schema_version` values; EP-18
  needs it only if a v0.2.0 lands.
- Machine-readable family-overlap detection (clustering families by shared activation predicates) to
  catch two families that are the same axis under different names.
- Generalising `escalates_to` beyond the shipped US default escalation copy.
