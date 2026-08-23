# EP-15 — Critique-lens protocol + full lens run

**Size:** L · **Mode:** n/a (reviews content for a, b and c) · **Core/Stretch:** core ·
**Depends on:** EP-12 (Seed content A), EP-13 (Seed content B), EP-14 (Seed content C) ·
**Blocks:** EP-16 (registry validator, re-plan P1)

## Context

Every seed record is at `review_status: draft`. This brief writes the **critique-lens protocol** and
then **runs it across the whole registry**, promoting each record to `accepted` or `blocked`. It is
the only brief in P1 whose output is a judgement about the content rather than the content itself,
and the only one whose acceptance criterion is a **finding**, not a clean run.

It implements **D-14** (narrative medicine, generalist spiritual care and disability-community
critique are **review lenses, not content**), **D-45** (lens veto is **conditional** — a lens may set
a concept `blocked`; only a published, dated `override_rationale` clears it; a lens may not author
replacement content and may not block a release), **D-46** (blocked and deprecated concepts **are
published** under "withdrawn / not adopted" with the blocking finding attached), and **D-27** (review
is **author-applied** in v1 and must be described as *self-review against published criteria*, never
as "reviewed by").

**The acceptance criterion that defines this brief: ≥ 1 blocking finding must be recorded.** Zero
blocking findings across roughly forty records does not mean the content is clean — it means the
protocol is not biting, and the protocol is revisited and re-run. This is the direct guard against
**R-14 (lens tokenism)**: a review recorded but toothless, used as legitimation. Write that rule into
the protocol document itself so a future run cannot quietly treat a clean sweep as success.

**What exists at pickup.** The schema including the `lens_finding` record type and
`lens_findings.yaml` (EP-9). The authoring guide with its register rules and hedge-deletion test
(EP-10). `docs/composer-spec.md` with invariants `CI-1 … CI-9` and the output templates as traces
(EP-11). All three seed sets at `draft` (EP-12, EP-13, EP-14). `schema_check` runs clean over the
registry with no forward references outstanding.

Commands run from the workspace directory `epppsynth/` unless a step says "from the git root".

## Safety preconditions

- **R-14 (lens tokenism) — the risk this brief exists to prevent.** Guards: the conditional veto with
  a **published, dated** override rationale; the coverage gate (every `accepted` record carries a
  finding **or an explicit `no-finding` record** from each of the three lenses — silence is not
  clearance); the ≥ 1 blocking finding acceptance criterion; and the honesty rule in step 2.
- **Honesty about who reviewed (D-27, R-28).** This is **author self-review against published
  criteria**. Every artifact this brief writes says so in its own front matter, and no artifact may
  use "reviewed by", "vetted", "endorsed", or a reviewer's role as an implied credential.
  Reviewer attribution read as clinical endorsement is R-28; recruiting the actual reviewers is
  EP-37, and their sign-off gates mode (a) only (D-65).
- **D-46 (publication of blocked records).** Blocked records are **not deleted and not hidden**. They
  keep their IDs, take `review_status: blocked`, keep the blocking finding attached permanently, and
  are published in the rendered markdown under "withdrawn / not adopted". This is the most credible
  evidence the protocol is real; it also exposes half-formed thinking in a public portfolio artifact,
  which is an accepted cost.
- **D-45 (a lens may not author).** A lens issues findings and `requested_change` text. It does
  **not** write replacement prose — mixing review and authoring destroys the independence that makes
  the review meaningful. Where a finding requires new content, the disposition is `deferred` with a
  named owning EP, or the record is blocked; the rewriting happens in a separate authoring pass with
  its own version bump and changelog entry, recorded as such.
- **A lens may not block a release**, only an item (D-45). No finding in this brief may set a
  project-level or phase-level gate.
- **No new content risk.** Any `caution` record added as a result of a lens finding is authored
  inside EP-14's reserved `EPS.CAU` range, follows EP-10's authoring guide, and gets its own
  attestation — a lens finding is not a licence to bypass the authoring rules.
- **Public-safety (D-3, R-6).** Findings are public. They must be original prose, must not quote any
  copyrighted source, must name no real person (including no reviewer's name — roles only), and must
  contain no local path, machine name or account name. Re-run the EP-6 pre-publication packet for
  *protected text*, *quotation budget* and *local paths*.
- **Not clinical guidance.** Findings are editorial judgements about a content model, not clinical
  opinions.

## In scope

1. **Write the protocol** — `docs/lens-protocol.md`. It is a published artifact and the criteria in
   it are what "self-review against published criteria" refers to. Contents:
   - **Standing and limits.** Three lenses (D-14). Author-applied in v1. Conditional veto. A lens may
     block an item, never a release, and may never author replacement content. Front matter states
     the self-review posture in the same words the public docs will use.
   - **Two object classes.** A **candidate concept** (any of the five types, plus question
     templates) and an **output template** (the waypoint composition shapes, abstention copy
     placeholders, and the stop-card shape — reviewed as EP-11's traces, since the copy itself is
     EP-39's).
   - **The three question sets**, written out in full — these are the criteria, and vagueness here is
     what produces tokenism:

     | Lens | Of a **concept** | Of an **output template** | Blocks when |
     |---|---|---|---|
     | **Narrative medicine** | Does this substitute a category for this person's own account? Would applying it before an encounter make the clinician listen less? Is the concept stated as a candidate reading or as a description of a person? Does the register carry authorial force (Y-7)? | Does the template leave room for the account to contradict it? Is the question open, or does it presuppose the concept? | The concept is stated as a description of a person rather than a candidate reading; or the template's question is closed, leading, or presupposes the concept |
     | **Generalist spiritual care** | Is this within what a non-chaplain generalist should *notice*, or does it invite the clinician to *work* the concern (Y-2)? Is there a referral path? Does it require interpretive or pastoral skill the operator does not have? | Does the template imply the clinician should provide spiritual care rather than notice and offer referral? | The concept requires skill the operator does not have; or no referral or abstention path exists |
     | **Disability community** | Does this attribute existential distress to a functional state? Does it assume a quality-of-life judgement the person has not made? Whose inference is the activation predicate encoding — the person's or the observer's? | Does the template let a "good outcome" be defined by the clinician? Does its framing presume decline equals suffering? | The concept encodes an outside quality-of-life inference; or the template's framing presumes decline equals suffering |

   - **Severity levels.** `blocking` (withholds the item from v1) · `substantive` (requires a change
     or a recorded rejection with reasons) · `note` (recorded, no action required). Define each with
     a test a reviewer can apply, not a feeling.
   - **Dispositions.** `accepted` · `rejected` (requires reasons) · `deferred` (requires a named
     owning EP).
   - **The override rule (D-45).** `blocked → accepted` requires a dated, authored, **published**
     `override_rationale` on the finding. The blocking finding stays attached to the concept
     permanently, override or not. There is no silent clear.
   - **The coverage gate.** Every `accepted` record carries ≥ 1 record from each of the three lenses —
     a finding **or** an explicit `no-finding` record. An explicit `no-finding` must name the
     question from the set that was applied; "reviewed, nothing found" without a named question does
     not satisfy the gate.
   - **The zero-findings rule.** If a full run produces no `blocking` finding, the protocol is
     revisited — the question sets sharpened or the severity tests tightened — and the run repeated.
     Record the revision. A clean sweep is a protocol result, never a content result.
   - **What the protocol is not.** Not external review. Not a substitute for the recruited reviewers
     (EP-37, D-64). Not a clinical or legal opinion.

2. **Confirm the `lens_finding` record shape** against EP-9's schema and extend it if the protocol
   needs a field the schema lacks (a schema change here is a `schema_version` patch bump with an
   ADR). The record: `id` (`LENS.<LENS3>.<NNNN>` with `NARR`, `SPIR`, `DIS`) · `lens` ·
   `applied_to` (concept, template or trace ID) · `object_class` · `applied_by`
   (`author-self-review`) · `date` · `severity` · `finding` (prose) · `requested_change` (prose) ·
   `disposition` · `override_rationale` (nullable) · `resulting_version` · `no_finding` (bool) ·
   `question_applied` (which question from the set — required when `no_finding` is true).

3. **Run all three lenses over the whole registry.** Every concept from EP-12, EP-13 and EP-14; every
   question template; and the output templates as EP-11's traces. Work lens by lens,
   not record by record, so each lens is applied with its own question set held in mind rather than
   diluted across three perspectives per record.

   Practical guidance, to be followed and recorded:
   - Apply the **narrative-medicine** lens to the `given` set first — it is where category
     substitution and authorial register are most likely, and where the hedge-deletion test may have
     passed while the prose still reads as description.
   - Apply the **generalist-spiritual-care** lens hardest to any concept that invites the clinician
     to *work* a concern, and check that every existential concept has a reachable `offer-referral`
     template. A concept with no referral path is a blocking finding by the protocol's own rule.
   - Apply the **disability-community** lens hardest to every `activation_predicate` keyed on
     `illness_stage`, and to any concept whose activation depends on a functional state. The lens's
     bite is that distress attributed to a functional state is very often the observer's projection —
     a majority of people with moderate-to-serious disability rate their quality of life as good or
     excellent, against outside assumption. An activation predicate that fires on a functional state
     rather than on something the person has themselves raised is the paradigm blocking case.

4. **Disposition every finding, and act on it.**
   - `blocking` + `accepted` → set the record `review_status: blocked`, leave it in the file, attach
     the finding.
   - `blocking` + overridden → set `review_status: accepted`, write the dated
     `override_rationale` on the finding, bump the record's `version` and append to its `changelog`.
     Overrides are expected to be rare; each one is a paragraph of public reasoning.
   - `substantive` + `accepted` → the record is revised in a separate authoring pass (a lens may not
     author, D-45), version-bumped, changelog-entried with the `lens_finding_id`, then re-checked
     against the same question.
   - `substantive` + `rejected` → reasons recorded on the finding; the finding stays attached.
   - `note` → recorded; no action.
   - Add `alternative_reading` edges from records to the findings that ship inside them as
     `contested_interpretations`, so unresolved dissent is carried in the record rather than filed
     away.

5. **Promote every record** out of `draft` to `lens-review` and then to `accepted` or `blocked`, with
   the transitions legal under EP-9's state machine and each recorded in the record's `changelog`.
   Populate `lenses_applied` on every record. **No record may remain `draft` at the end of this
   brief** — a record nobody could review is a record that does not ship, and the honest disposition
   for it is `blocked` with a finding saying why.

6. **Write the run report** — `docs/lens-run-2026-P1.md`: counts per lens and per severity; the list
   of blocked records with their findings; the list of overrides with their rationales; the coverage
   table (records × lenses); the records revised and their version bumps; and, if the run produced no
   blocking finding, the protocol revision made and the re-run result. Front matter: author
   self-review against published criteria.

7. **Feed EP-37.** Add a short section to the protocol naming the reviewer roles the three lenses
   imply — a narrative-medicine or medical-humanities educator, a board-certified chaplain, a
   disability-community reviewer with lived experience of serious-illness care, plus a palliative-care
   clinician for the `function` records' evidence claims (D-64 settles the roles; this brief records
   which question set each role would own). Outreach itself waits for a functional stage (D-64) and
   belongs to EP-37.

8. **Documentation.** Add `docs/lens-protocol.md` and `docs/lens-run-2026-P1.md` to `DESIGN.md`
   §Traceability. Add a dated addendum under **D-45** in `DECISIONS.md` recording the run: the number
   of blocking findings, the number of overrides, and — if applicable — the protocol revision the
   zero-findings rule forced. Record the blocked-record count in `GOVERNANCE.md`'s review-status
   statement so the public number is not only in a docs page.

## Out of scope

- Authoring any concept content, including replacement prose for a substantive finding, as part of
  the review pass → the authoring rules in **EP-10** and the owning seed brief (**EP-12**, **EP-13**,
  **EP-14**); a revision is a separate, recorded authoring pass in the owning file.
- The `no-lens-record` cross-file validation rule, the rendered markdown's "withdrawn / not adopted"
  section, and the CI job → **EP-16**.
- Recruiting the external reviewers and the recruitment pack → **EP-37** (D-64).
- Reviewer sign-off as a release gate → **EP-52** (mode (a) only, D-65).
- The narrative-medicine, spiritual-care and disability literatures as **content** → excluded by
  decision (D-14): they are review lenses in v1 and no EP adds them as concepts.
- The human-factors study, the anchoring probe and any empirical test of whether the lens findings
  were right → **EP-51**.
- The public wording of the review-status statement → **EP-53**.

## Verification / acceptance

- `uv run python -m epppsynth.registry.schema_check --rights` exits `0` over the full registry
  including `lens_findings.yaml`, with **no forward references** outstanding.
- `uv run python -m epppsynth.registry.schema_check --lens-coverage --json` reports, for every
  non-`draft` record, one row per lens with the finding ID or the `no-finding` record ID; the run
  fails if any `accepted` record is missing a row for any of the three lenses.
- `uv run pytest tests/ep/test_ep15.py -q` green, asserting: **≥ 1 finding with
  `severity: blocking`**; no record left at `review_status: draft`; every `blocked` record has ≥ 1
  attached blocking finding; every record whose status moved `blocked → accepted` has a non-null,
  dated `override_rationale`; every `no_finding: true` record names a `question_applied`; every
  `disposition: deferred` names an owning EP; no finding record contains prose in a
  `replacement_prose`-shaped field (a lens may not author).
- `uv run python -m epppsynth.registry.schema_check --json` reports the count of `blocked` records —
  **reported, never hidden** — and that count matches `docs/lens-run-2026-P1.md` and the
  `GOVERNANCE.md` statement.
- From the git root: `python tools/roadmap_check.py --context-budget EP-15` passes.
- Pre-publication packet (EP-6) re-run for *protected text*, *quotation budget* and *local paths*;
  output recorded in the completion note.
- **The defining criterion** *(judgement — author, and mechanised by the test above)*: at least one
  blocking finding is recorded. **If the run produced none**, the completion note must show the
  protocol revision made, and the re-run must be executed and reported in the same brief. Shipping a
  zero-blocking-finding run without a documented protocol revision fails this brief.
- *(judgement — author)* Every `no-finding` record names the specific question applied. A
  `no-finding` that names no question is rewritten.
- *(judgement — author)* No artifact written here says "reviewed by" or implies external review.
- Commits: `feat(epppsynth): critique-lens protocol and full lens run (EP-15)` then
  `docs(roadmap): record EP-15 commit hash`.

## Parked → final-roadmap.md

- Re-running the three lenses with the **recruited** reviewers once EP-37's outreach completes; the
  v1 run is author self-review and the external run is a separate, later artifact.
- A fourth lens (clinical ethics, or interpreter/language access) if the run shows the three miss a
  recurring class of finding.
- Tracking whether blocking findings cluster by source, family or concept type — a signal about which
  content set is weakest, worth measuring once the registry is larger.
- A re-review trigger: which changes to a record require its lens records to be invalidated and
  re-run. v1 handles this by hand through `resulting_version`.
- Publishing the question sets as a standalone reusable artifact, if the protocol proves useful
  outside this project.
