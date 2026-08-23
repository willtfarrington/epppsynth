# EP-16 — Registry validator, rendered markdown, re-plan P1

**Size:** M · **Mode:** n/a · **Core/Stretch:** core ·
**Depends on:** EP-9 (Registry schema v0), EP-10 (Provenance, rights, reuse class, citation rule,
authoring guide), EP-11 (Composer specification), EP-12 (Seed content A), EP-13 (Seed content B),
EP-14 (Seed content C), EP-15 (Critique-lens protocol + full lens run) ·
**Blocks:** EP-45 (provenance drawer)

## Context

The phase-closing brief for P1. Three jobs:

1. **Consolidate every checker into one registry validator** with a stable rule-ID vocabulary, wire
   it into CI, and make it the single command that answers "is the registry sound?". P1 accumulated
   checks across three modules — EP-9's `schema_check`, EP-10's `rights-*` rule group, EP-11's
   `spec_check` — and a fourth set of **cross-file** rules that no earlier brief could run because
   the content did not exist yet.
2. **Render the registry to human-readable markdown** (D-15), including the "withdrawn / not adopted"
   section that publishes blocked and deprecated concepts with their blocking findings (D-46), and
   surfacing gaps visibly rather than only failing (R-13).
3. **Re-plan P1** — tick the phase table, mirror every `## Parked →` item into `final-roadmap.md`,
   record deviations as dated addenda, and hand P2 a registry it can load.

**What exists at pickup.** The full registry: schema, families, input fields, three seed content
sets, question templates, sources, lens findings, attestations. `docs/registry-schema.md`,
`docs/composer-spec.md` with `CI-1 … CI-9`, `docs/authoring-guide.md`, `docs/evidence-appendix.md`,
`docs/lens-protocol.md`, `docs/lens-run-2026-P1.md`, `docs/rights-check-2026-P1.md`. The EP-6 CI
workflow and pre-publication packet. No engine, no loader, no eval harness.

This is an **M** brief because the rules were specified in EP-9 … EP-15; this brief implements the
cross-file ones, consolidates, renders and re-plans. If the consolidation turns out to be a rewrite
rather than a merge, split it at pickup (D-22).

Commands run from the workspace directory `epppsynth/` unless a step says "from the git root".

## Safety preconditions

- **R-13 (registry accretion without provenance) — the risk this brief closes out.** The validator is
  the mechanism. Guard: CI fails on any concept lacking provenance, cultural scope, a family, a
  counter-hypothesis or a lens record, and the rendered markdown **surfaces gaps visibly** rather
  than silently omitting them.
- **The non-negotiables, verified here as validator rules rather than as prose** — this brief is
  where each becomes mechanically true over real content:
  - `cultural_scope.claims_universality` is `false` on every record; `true` is rejected with no
    exception path (rule `REG-UNIV-01`).
  - No concept carries an ordinal, severity, score or count field, outside the two allow-listed
    graded paths (`REG-ORD-01`).
  - Public citations are **chapter-level locators only** — no page ranges, no quoted phrase, no
    chapter title reused as a concept label, no outline-reconstructing locator sequence; quotation
    budget ≤ 25 words per quote and ≤ 150 words per source (`REG-CITE-01…05`, D-74).
  - A source at a non-commercial, share-alike, reference-only or pending-rights-check class may not
    license authored wording — the `reuse_class` → `derivation_mode` matrix holds (`REG-RIGHTS-01`,
    D-62).
  - Every `given` carries an `out_of_declared_scope_when` edge on the literal
    `outside-declared-scope` framework value, so scope is data, not engine judgement
    (`REG-SCOPE-01`, D-14, D-38.1).
  - `counter_reading` and `insufficient_basis_clause` are structurally required outputs, asserted
    over EP-11's traces (`SPEC-CI-1`, D-53) and made *satisfiable* over real content by
    `REG-COUNTER-01` (symmetric-complete counter-hypotheses across the emittable types).
  - Mode (c): every mode-(c) predicate combination selecting a `personal-meaning` concept also
    selects a `structural` one, or is in the committed exceptions file (`REG-LOCUS-01`, D-20, R-16).
  - Every `accepted` record carries a finding or an explicit `no-finding` from each of the three
    lenses; the `blocked` count is **reported, not hidden** (`REG-LENS-01…02`, D-45, D-46).
- **R-19 / R-35 (local index or local path leakage).** The validator reads the local reading manifest
  for the chapter-title lint **from outside the repository tree** and must never write any of its
  content into a report, a rendered page, a CI log or a JSON output — only pass/fail per rule. In CI
  the manifest is absent, so the rule reports `skipped-no-manifest`; the pre-publication packet
  treats a skipped run as a **finding**, not a pass. No committed artifact may contain a
  `page_or_locator` value (`REG-LOCAL-01`).
- **R-9 / R-36 (overclaim and badge drift).** The rendered markdown and the re-plan must not describe
  P1 as validated, reviewed or evaluated. P1 produces a content model reviewed by **author
  self-review against published criteria** (D-27) with **no evaluation of any kind** — the eval phase
  is P3. The maturity badge does not advance here (D-59).
- **D-42 CI constraints.** The CI job runs on `windows-latest`, minimum token permissions, third-party
  actions pinned to commit SHAs, deterministic **no-model** path only. The validator must run with no
  network, no model, no corpus and no index.
- **Public-safety (D-3, R-6).** The rendered markdown is a public artifact and is the largest single
  publication event in P1. Re-run the **full** EP-6 pre-publication packet against it, not a subset.
- **Not clinical guidance.** The rendered registry carries the same front matter as the source
  records: possible readings available to a clinician, never properties of a person; not a risk
  detector; author review only.

## In scope

1. **Consolidate into `src/epppsynth/registry/validate.py`**, runnable as
   `python -m epppsynth.registry.validate`, with `--path`, `--json`, `--rule <ID>`, `--only-group`,
   `--allow-forward-refs` (default **off**) and `--strict` (treat `skipped` as failure). Keep
   `schema_check` and `spec_check` as importable rule groups rather than deleting them, so EP-9's and
   EP-11's acceptance commands continue to work; `validate` is the umbrella. Assign every rule a
   stable ID in a documented namespace (`SCHEMA-*`, `RIGHTS-*`, `SPEC-*`, `REG-*`) and print
   `<file>:<id>: <RULE-ID>: <message>`. Exit `0` clean, `1` on violations, `2` on usage error, `3`
   when a rule was skipped under `--strict`.

2. **Implement the cross-file rules no earlier brief could run.** These are new work:
   - `REG-COUNTER-01` — `counter_hypothesis_of` symmetric-complete across the whole registry, every
     partner `accepted` and non-deprecated. An `accepted` concept whose only partner is `blocked` is
     a violation: it can no longer satisfy `CI-1` at run time.
   - `REG-FAMILY-01` — every concept resolves to exactly one family; report the concept count per
     family; **warn** where one family holds more than four emittable concepts of one type (a signal
     the family is really two axes) and where a family holds none (dead weight).
   - `REG-LOCUS-01` — the mode-(c) satisfiability enumeration from EP-14, re-run over the final
     content, with the committed exceptions file honoured and echoed.
   - `REG-LENS-01/02` — lens coverage over `accepted` records; blocked count reported.
   - `REG-GRAPH-01` — no dangling relation target anywhere, no cycle in `may_manifest_as`, every
     `escalates_to` resolving to the single escalation-copy ID, every `invites` target `accepted`.
   - `REG-REACH-01` — **every `accepted` emittable concept is reachable**: at least one point in the
     D-25 enum space selects it. An unreachable concept is not a failure but a reported finding — it
     is content that can never be seen, and the re-plan decides whether to broaden it or deprecate
     it.
   - `REG-ORPHAN-01` — every `question_template` and every `family` is referenced by at least
     one concept; unreferenced records are reported. (`framing` records are not checked: the kind was
     removed with output part (iv), which was deleted from the contract rather than left
     undeliverable.)
   - `REG-ATTEST-01` — every concept has an attestation; every non-null `residual_concern` is listed
     for the D-29 clearance checkpoint (EP-52).
   - `REG-CITE-05` — the outline-reconstruction check across the *final* registry order, which only
     becomes meaningful once all three seed sets are present.
   - `REG-COUNT-01` — report the registry size against the ≈ 40 target (D-47) **as a number, not a
     gate**: a thin registry that abstains honestly beats a padded one, and the gate is the P3
     coverage dry-run, not this count.

3. **Wire CI.** Add a `registry` job to the EP-6 workflow: `windows-latest`, minimum permissions,
   pinned actions, no network, `python -m epppsynth.registry.validate --strict` plus
   `python -m epppsynth.registry.spec_check`. The chapter-title lint will report
   `skipped-no-manifest` in CI; under `--strict` that is exit `3`, so the CI invocation runs
   **without** `--strict` for that one rule and the pre-publication packet carries the local
   `--strict` run instead. Document the split explicitly in the workflow comment so nobody "fixes"
   it later by weakening the local run.

4. **Render the registry** — `src/epppsynth/registry/render.py` → `docs/registry.md`, deterministic
   and byte-stable (sorted, no timestamp in the body; the generation stamp goes in a single trailing
   line so a re-render diff is one line). Sections:
   - **Front matter** — what this is; Western-secular in origin and labelled as such; not clinical
     guidance; not a risk detector; author self-review against published criteria; no evaluation
     exists yet.
   - **How to read a concept** — the field glossary, including that `confidence` means confidence
     that the framing is defensible and never that it applies to a person, and that citations are
     chapter-level bibliographic pointers.
   - **Accepted concepts**, grouped by **family** (not by type), each with its label, prose,
     `tradition` where present, `locus`, counter-hypothesis partners, invited question intents,
     cultural scope with its empty-or-populated `tested_in`, evidence block including
     `not_supported`, contested interpretations, lens records, provenance and short citation.
     `page_or_locator` is **stripped**.
   - **Withdrawn / not adopted (D-46)** — every `blocked` and `deprecated` record with its blocking
     finding or `deprecation_reason` attached, and any `override_rationale`. This section is not
     collapsible and not an appendix.
   - **Coverage and gaps** — the lens coverage table; unreferenced records; unreachable concepts;
     families with no concepts; sources still at `reference-only-pending-rights-check`; concepts with
     a non-null `residual_concern`. Gaps are **surfaced**, which is the R-13 mitigation.
   - **Sources** — EP-5's generated rights table, embedded or linked, with `reuse_class`,
     `verified_at` and `verification_note` per source.

5. **Re-plan P1.** Following the sibling repos' conventions verbatim:
   - Tick EP-9 … EP-16 in `roadmap/README.md` with short hashes.
   - Mirror every `## Parked → final-roadmap.md` item from EP-9 … EP-16 into `final-roadmap.md`,
     grouped by theme, each naming the brief it came from.
   - Record deviations as **dated addenda** in `DECISIONS.md`, never edits. At minimum, decide and
     record:
     - the **journal-page-span carve-out** to D-74's chapter-level-only rule (EP-10 step 4) — ratify,
       amend, or tighten;
     - **settled, record only:** `free_text` is **excluded** from D-73's three-way sensitivity
       declaration entirely, because as an inert echo it cannot affect substance and there is nothing
       for a class to describe (GOVERNANCE §4.2, `DESIGN.md` §3, EP-9 step 9). There is no carve-out
       and no fourth value to ratify; the addendum records the exclusion, not a decision;
     - the **hard-stop rendering** resolution under D-18 (EP-11) if EP-11 did not already record it;
     - whether `evidence_grade` survives, given that a letter grade is the kind of compression the
       no-ordinal rule exists to prevent (EP-13's parked item);
     - the disposition of any source still at `reference-only-pending-rights-check`, and whether the
       concepts depending on it ship (this feeds EP-52's clearance checkpoint).
   - Append `> **Completion note (date).**` blocks to EP-9 … EP-15 where a session left one
     outstanding, and strike through any P1 hazard now resolved as
     `~~risk~~ **Resolved by EP-n (date)**`.
   - Confirm the P2 entry conditions: the registry validates clean with `--allow-forward-refs` off,
     `docs/composer-spec.md` invariants are numbered and cited, and EP-17/EP-18 have a stable schema
     and a rule vocabulary to build against.
   - Record the registry size, the blocked-record count, the lens finding counts by severity, and the
     unverified-source list — these are the P1 numbers EP-50's evidence bundle will cite.

6. **Update `roadmap/README.md`'s P1 standing-decisions paragraph** if the re-plan changed anything
   in it, as an addition rather than a rewrite, dated.

7. **Tests** (`tests/ep/test_ep16.py`): a fixture registry exercising each new `REG-*` rule with a
   passing and a failing case; the renderer is byte-stable across two runs except the trailing
   generation line; the renderer emits the withdrawn section when a blocked record exists and emits
   an explicit "none" when it does not; no rendered output contains a `page_or_locator` value or any
   string from the chapter-title manifest; `--strict` turns a skipped rule into exit `3`.

## Out of scope

- Any change to the schema, the rights spec, the composer spec or any concept content — this brief
  **validates and renders**; a rule that fails is fixed in the owning brief's file with a version
  bump and a changelog entry, recorded as a deviation in that brief's completion note (**EP-9**,
  **EP-10**, **EP-11**, **EP-12**, **EP-13**, **EP-14**, **EP-15**).
- The registry **loader**, `schema_version` migrations and the `(contract, registry, template)`
  version triple → **EP-18**.
- Typed contracts over the records → **EP-17**.
- Any engine behaviour → **EP-19**, **EP-20**, **EP-21**.
- The mechanised coverage dry-run against development scenarios that gates D-47's ≈ 40 target →
  **EP-24** / **EP-25**; this brief reports the count only.
- The provenance drawer that renders these fields in the UI → **EP-45**.
- The release-evidence bundle and the badge upgrade → **EP-50**, **EP-52** (D-59: the badge does not
  advance here).
- The public README and the clinical-reader narrative → **EP-53**.

## Verification / acceptance

- `uv run python -m epppsynth.registry.validate --strict` exits `0` locally (with the local reading
  manifest present, so the chapter-title lint actually runs rather than skipping).
- `uv run python -m epppsynth.registry.validate --json` emits, and the completion note records: the
  registry size; the count per type and per family; the `blocked` count; lens findings by severity;
  unreachable concepts; unreferenced templates and families; sources still at
  `reference-only-pending-rights-check`; concepts with a non-null `residual_concern`; and the
  quoted-word total per source (expected: `0`).
- `uv run python -m epppsynth.registry.spec_check` exits `0`.
- `uv run python -m epppsynth.registry.render --check` exits `0` — the committed `docs/registry.md`
  is byte-identical to a fresh render except the trailing generation line.
- `uv run pytest tests/ep/test_ep16.py -q` green, with a failing-fixture test per `REG-*` rule in
  step 2.
- `uv run pytest -q` green across the whole suite (EP-9 … EP-16 test modules all still pass).
- `uv run ruff check .` and the project type check green.
- The CI `registry` job is green on a pushed branch, on `windows-latest`, with pinned action SHAs and
  minimum token permissions, and its log contains no registry prose, no chapter title and no local
  path.
- From the git root: `python tools/roadmap_check.py` passes with no hazard naming no brief and no
  core brief naming no acceptance evidence; `python tools/roadmap_check.py --context-budget EP-16`
  passes.
- **Full** EP-6 pre-publication packet re-run against `docs/registry.md` and every P1 doc; output
  recorded in the completion note.
- *(judgement — author)* `docs/registry.md`'s withdrawn section is present, uncollapsed, and reads as
  a first-class part of the document rather than an appendix (D-46).
- *(judgement — author)* Nothing in the rendered markdown or the re-plan describes P1 as validated,
  reviewed or evaluated.
- *(judgement — owner)* The five re-plan decisions in step 5 are each recorded as a dated addendum
  with a rationale, including any that ratify the interim position unchanged.
- Commits: `feat(epppsynth): registry validator, rendered markdown, CI job (EP-16)` then
  `docs(roadmap): re-plan P1 — tick table, mirror parked items, record EP-16 commit hash`.

## Parked → final-roadmap.md

- A registry diff tool that reports, between two commits, which concepts changed, which lens records
  were invalidated by a version bump, and which composer traces would change — the maintenance
  workflow P1 does not need yet but P3's contamination checks will want.
- Rendering the registry to a second format (a printable one-pager per family) for reviewer use in
  EP-37 / EP-51.
- A `--fix` mode for the mechanical rules (recomputing `content_hash`, sorting relation lists); v1
  keeps the validator read-only on purpose so no rule can silently repair a real problem.
- Measuring whether the family partition actually produces plural hypotheses in practice, once the
  P3 scenarios exist — the family rule is a mechanism, and this brief can only confirm it is wired,
  not that it works.
- Re-running the rights check for any source still unverified at the end of P1, before EP-52.
