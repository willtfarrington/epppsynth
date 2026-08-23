# EP-13 — Seed content B: communication functions + evidence appendix

**Size:** L · **Mode:** a (records also scoped to b) · **Core/Stretch:** core ·
**Depends on:** EP-10 (Provenance, rights, reuse class, citation rule, authoring guide) ·
**Blocks:** EP-15 (critique-lens protocol and run), EP-16 (registry validator, re-plan P1)

## Context

The second seed-content brief. It authors the `function` concepts — conversational **functions**
(elicit, check understanding, offer permission) drawn from the serious-illness communication evidence
— and the **evidence appendix**, which is the document that keeps this whole project honest.

**The honest evidence position this brief must carry (D-63), stated up front because everything else
follows from it:**

- The closest analogue trials are **null to adverse**. One high-quality randomized trial of an
  adjacent intervention found **no** improvement in patient- or family-reported communication quality
  or quality of end-of-life care, **and a small but statistically significant increase in patients'
  depressive symptoms**. The flagship structured-guide trial was **null on its coprimary patient
  outcomes** and positive only on process outcomes.
- The **defensible analogue is a question-generation aid** — an intervention class whose demonstrated
  effect is on *what gets asked*, not on outcomes.
- The founding hypothesis of this project — that a handful of pre-encounter waypoints derived from a
  concept registry change what a clinician notices or asks — has **zero supporting evidence**. No
  study of this intervention class was located. This is a permanent evidence limitation, not a
  pending search.
- Therefore each `function` concept records **both what its source supports and what it does not**,
  in two required fields, and the success criterion of this project is a **feasibility and
  acceptability** measure, never an effectiveness claim.

This is the content set most exposed to **R-12 (null-to-harm precedent)** and **R-9 (portfolio
overclaim)**. It is also the set with the sharpest scope line: the shared-decision-making literature
that grounds these functions includes *option comparison* steps, and D-26(c) forbids ranking or
comparing clinical options. These concepts are **elicitation functions only**.

**ID allocation (fixed by EP-9, do not deviate):** `EPS.FUN.0001–0012`, `EPS.QT.0030–0049`. Target
≈ 10 `function` records.

**What exists at pickup.** The schema, families, the closed `question_intent` enum, `schema_check`
(EP-9). `sources.yaml`, the permission matrix, the chapter-level-only citation rule, the authoring
guide and the attestation file (EP-10). This brief does **not** depend on EP-11 or on EP-12; it may
run before either. All records land at `review_status: draft`.

Commands run from the workspace directory `epppsynth/` unless a step says "from the git root".

## Safety preconditions

- **R-12 (null-to-harm precedent) — the defining risk of this brief.** Guards: the two required
  fields `evidence.supported_claim` and `evidence.not_supported` on **every** `function` record;
  the mandatory `evidence_absent_for` edge wherever no inspected source supports the function; and
  the evidence appendix itself, published with the tool. The appendix must state the adverse finding
  plainly rather than as a caveat, and must not be softened at any later phase without a dated
  addendum.
- **R-9 (portfolio overclaim under hiring pressure).** The appendix's no-evidence statement for the
  founding hypothesis must be written here in the exact form the public README will carry (EP-53
  quotes it verbatim; it does not re-word it). Nothing in this brief may describe the project as
  improving communication, outcomes, or care.
- **R-2 (automation bias) / `CI-1`.** `function` concepts are emittable, so each needs ≥ 1
  `counter_hypothesis_of` partner and a symmetric reverse edge (EP-9 rule (h)); the composer pairs
  every emission with a counter-reading and an insufficient-basis clause.
- **Scope line: elicitation only (D-26c).** No `function` concept may compare, rank, weigh, recommend
  or sequence clinical options; none may generate content whose function is to increase the
  likelihood that a person accepts a particular course. Guard: a review of every record against the
  question `does this help the clinician ask, or does it help the clinician get an answer they
  prefer?` plus the coercion criteria in step 6.
- **R-1 (coercion architecture).** The trauma-informed principles most directly violated by a
  persuasion-shaped tool — voice and choice, and collaboration and mutuality — are named as test
  criteria in step 6, not as generic values. Every template is a **question or an offer** (D-26b).
- **Y-4 (diagnostic drift) / no ordinals.** `evidence.evidence_grade` is the one graded field
  permitted on a `function`, and it grades a **source's evidentiary standing**, never a person or a
  concern (EP-9's allow-list). No other graded, scored or counted field may appear.
- **R-15 / rights (D-62).** The shared-decision-making source family's reuse terms are **UNVERIFIED**
  and sit at `reference-only-pending-rights-check` unless EP-10's rights check cleared them. Under
  EP-10's permission matrix that means their wording may **not** inform prose: author every affected
  record as `reading-informed-original` with author-original wording, structure and sequence, and
  check the current `reuse_class` in `sources.yaml` before writing rather than assuming.
- **D-74 citation limits.** Chapter-level locators only; a journal article's own page span belongs in
  `sources.yaml`'s bibliographic record, never in a concept's `short_citation`. No quoted phrase.
  Quotation budget ≤ 25 words per quote, ≤ 150 words per source — the appendix is the file most
  likely to breach it, so it quotes **nothing** and reports every finding in original prose,
  including numeric results, which are facts and not expression.
- **Public-safety (D-3, R-6).** All prose public and original. No PHI pattern, no real person, no
  local path, machine name or account name. Re-run the EP-6 pre-publication packet for *protected
  text*, *quotation budget*, *PHI patterns* and *local paths*.
- **Not clinical guidance.** These records describe *functions available to the clinician*, never
  what a person feels or should do.

## In scope

1. **Write the evidence appendix first** — `docs/evidence-appendix.md`. Authoring the functions
   before the appendix inverts the dependency and invites the overclaim. Structure:
   - **§1 What this tool is analogised to.** The question-generation aid class, and why: its
     demonstrated effect is on what gets asked, not on outcomes.
   - **§2 The closest trials, and what they found.** In original prose, with DOIs, no quotation: the
     null-to-adverse trial (no improvement in patient- or family-reported communication quality or
     quality of end-of-life care; a small statistically significant increase in patient depressive
     symptoms), and the structured-guide trial (null coprimary patient outcomes; positive process
     outcomes — more, earlier, better-documented, more accessible conversations; secondary anxiety
     and depression reductions with limited durability). State the authors' own stated limitations.
   - **§3 Why self-report is a weak surrogate.** Trainee self-assessment tracks patient report in one
     narrow domain and diverges for general end-of-life communication; so a reader reporting a useful
     question measures the tool's **generativity**, not its value.
   - **§4 The founding-hypothesis gap.** A plain, permanent statement that no located source
     evaluates a pre-encounter, offline, clinician-only reflection aid of this kind; that whether
     naming a plausible unspoken concern beforehand improves or contaminates an encounter is
     untested and the anchoring risk runs the other way; and that no evidence exists for modes (b)
     or (c). Write the **exact sentence** the public README will carry, in a fenced block labelled
     `README status sentence — quoted verbatim by EP-53`.
   - **§5 The claim register.** A table of every claim the project makes, each marked *empirical* or
     *interpretive*, with the source and the claim's limits. Every `function` concept's
     `supported_claim` appears here.
   - **§6 What this appendix is not.** Not a systematic review; a record of what the author read and
     what it did and did not support.
   - Front matter: this appendix is published with the tool and is a release-gate artifact.

2. **Author ≈ 10 `function` concepts.** Each is a conversational *function*, not a script. Candidate
   functions, to be adjusted at authoring — ask permission before opening a difficult topic; check
   what the person already understands; invite the person's questions; elicit what matters to the
   person in their own words; name uncertainty without resolving it; check how much detail the person
   wants now; offer to include someone the person chooses; note what the person has said they do not
   want discussed; offer a referral to a specialist role; check back whether the conversation
   should continue. Each record carries:
   - `label` and `prose` — plain, hedged, non-narrative, author-original; the prose says what the
     function *does* and states that the output is an offer, never a statement about what the person
     feels;
   - `family` — spread across the communication families (information-and-disclosure,
     understanding-and-uncertainty, permission-and-pacing, values-and-what-matters,
     scope-and-referral). **Two functions in the same family will never co-occur in one output**
     under EP-11's one-per-family rule, so a family holding four near-identical functions is a
     content error: check the family spread before committing;
   - `locus` — omit unless the record is mode-(c) scoped;
   - `mode_scope: [a, b]`;
   - `activation_predicate` — keyed on `stated_information_preference`,
     `stated_decision_sharing_preference`, `encounter_temporality` and `illness_stage`. **Never** on
     `self_described_framework`, `uncertainty_tolerance` or `language_interpreter_need` (EP-9
     declared those non-substance-bearing);
   - `confidence` per the schema definition;
   - `contested_interpretations` where a function's grounding is disputed.

3. **The two required evidence fields, on every `function` record (D-63).** This is the core of the
   brief:

   ```yaml
   evidence:
     claim_type: empirical-process | interpretive | normative-design
     empirical_support: process-outcomes-only | none | not-applicable | contested-construct
     evidence_grade: A | B | C | absent
     supported_claim: >
       What the inspected source actually supports — in the source's own outcome terms, stated
       narrowly, with the population and setting named.
     not_supported: >
       What the same source does NOT support. Required and non-empty. Where the source's coprimary
       outcomes were null, say so here in those words.
   ```

   Rules: `not_supported` is **never** empty and never "unknown"; where no inspected source supports
   the function, `evidence_grade: absent`, `empirical_support: none`, and a mandatory
   `evidence_absent_for` edge to the relevant `source_id`; and `supported_claim` then says plainly
   that the function is included on design grounds rather than evidential ones. Expect **several**
   functions in that position — that is the honest state of this literature, and a set where every
   function is evidence-backed should be treated as a signal that the fields were written
   aspirationally.

4. **Author question templates** — `EPS.QT.0030–0049`, at least one per function, each with `form`
   ∈ {`question`, `offer`}, a `question_intent` from the closed enum, `requires_permission` and
   `disconfirming`. At least one `offer-referral` template. Apply the authoring guide's
   hedge-deletion test to every template.

5. **Wire the relations.** Exactly one `family` per record. ≥ 1 `counter_hypothesis_of` with the
   reverse edge present — for functions, the natural counter is a function that would be the right
   move if the first reading of the situation is wrong (for example, checking understanding against
   asking permission to stop). ≥ 1 `invites`. `constrained_by` edges into EP-14's allocated
   `principle` and `caution` IDs; if EP-14 has not yet run these are expected forward references,
   recorded in the completion note and resolved at EP-16. `evidence_for` / `evidence_absent_for`
   edges to `source_id`s that resolve in `sources.yaml`.

6. **The elicitation-only review, run as a checklist over every record before commit.** For each
   function, answer in the completion note:
   - Does it compare, rank, weigh, sequence or recommend clinical options? If yes, it does not ship
     (D-26c).
   - Could its output plausibly function as objection handling, as a second attempt after a refusal,
     or as an emotional appeal attached to a course of action? If yes, it does not ship (R-1).
   - Does it respect **voice and choice** — does it leave declining as a complete outcome requiring
     no follow-up prompt?
   - Does it respect **collaboration and mutuality** — is the clinician asking, or extracting?
   - Would its clinical substance change if the clinician's own preference changed? It must not
     (D-37, D-72 pivot B).

7. **Provenance, rights and attestation** for every record and for the appendix's source list, per
   EP-10: resolving `source_id`, `derivation_mode` from the decision tree against the source's
   **current** `reuse_class`, a chapter-level-only `short_citation` with no page range and no quoted
   phrase, `access_date`, and an `attestation_id` with a truthful `residual_concern`.

8. **Set every record to `review_status: draft`,** `version: 1`, `lang: en`, `variant_of: null`,
   `lenses_applied: []`, computed `content_hash`. Promotion is EP-15's.

9. **Documentation.** Add `docs/evidence-appendix.md` to `DESIGN.md` §Traceability and to the
   release-gate artifact list referenced by **D-35**/**D-67** (EP-50 assembles the bundle; this brief
   only registers the artifact). Add a dated addendum under **D-63** in `DECISIONS.md` recording that
   the appendix exists, where the README sentence lives, and that EP-53 quotes it verbatim.

## Out of scope

- `given` concepts and the ordinary-concern counter-frame → **EP-12**.
- `principle`, `condition` and `caution` records → **EP-14** (this brief writes `constrained_by`
  edges pointing at their allocated IDs).
- Applying the critique lenses and any promotion out of `draft` → **EP-15**.
- Cross-file validation, the rendered markdown and the CI job → **EP-16**.
- Charter clauses about prohibited manipulation and about the tool not being inherently benign →
  **EP-3** (`SAFETY.md`); this brief supplies the evidence they rest on.
- The public README status wording and the clinical-reader narrative → **EP-53** (which quotes §4's
  sentence verbatim rather than re-writing it).
- Option-comparison and decision-support functionality → **excluded by decision** (D-26c); it belongs
  to the clinician, not the tool, and no later EP owns it. This is now simply true of the whole
  contract rather than a gap in it: the output part that would have connected stated values to
  clinician-verified options was **deleted** rather than left undeliverable — it had no input field,
  no authored content source and no owning brief, so it would have shipped permanently empty and
  would have made `option_ref_set` a constant in EP-11's substance tuple. The `framing` record kind
  and its `EPS.FRM.*` band went with it (EP-9, EP-18); this brief authors no `framing` content, and
  no later brief should reintroduce the kind to restore the part. The no-ranking prohibition in this
  brief's step 6 criteria survives untouched and is still load bearing.
- The coercion red-team suite that tests step 6's criteria mechanically → **EP-26** / **EP-29**.
- Assembling the release-evidence bundle → **EP-50**.

## Verification / acceptance

- `uv run python -m epppsynth.registry.schema_check --rights --path registry/concepts/functions.yaml`
  exits `0` (with `--allow-forward-refs` if EP-14 has not yet run).
- `uv run python -m epppsynth.registry.schema_check --rights --json` reports for the `function` set:
  every record has non-empty `supported_claim` **and** non-empty `not_supported`; every record with
  `evidence_grade: absent` has an `evidence_absent_for` edge; `counter_hypothesis_of` is
  symmetric-complete; exactly one `family` per record; zero citation violations; zero quoted words
  attributable to any source.
- `uv run pytest tests/ep/test_ep13.py -q` green, asserting: no `function` record has an empty or
  placeholder `not_supported`; no `question_template` in the allocated range has a `form` outside
  {`question`, `offer`}; ≥ 1 `offer-referral` template exists; no more than three functions share a
  single `family`; and `docs/evidence-appendix.md` contains the fenced `README status sentence`
  block.
- `uv run python -m epppsynth.registry.schema_check --rights --json` reports the appendix's quoted
  word count as **0**.
- From the git root: `python tools/roadmap_check.py --context-budget EP-13` passes.
- Pre-publication packet (EP-6) re-run for *protected text*, *quotation budget*, *PHI patterns* and
  *local paths*; output recorded in the completion note.
- *(judgement — author)* The appendix states the adverse depressive-symptom finding in its own
  section, not inside a caveat clause, and states the founding-hypothesis gap as permanent rather
  than pending.
- *(judgement — author)* The step-6 checklist is answered in writing for **every** function record in
  the completion note, not summarised.
- *(judgement — author)* At least one function carries `evidence_grade: absent`. If none does, the
  evidence fields were written aspirationally and the set is re-reviewed before commit.
- Commits: `feat(epppsynth): seed content B — communication functions and evidence appendix (EP-13)`
  then `docs(roadmap): record EP-13 commit hash`.

## Parked → final-roadmap.md

- Re-verifying the two summary-only sources whose full texts were not inspected during planning (the
  advance-care-planning viewpoint and the decision-aid systematic review), and updating the appendix
  if the inspected text changes any claim.
- A periodic evidence refresh — the appendix is a point-in-time record and will go stale; the cadence
  and its trigger belong to a post-v1 release.
- Function concepts for modes beyond (a) and (b), if the mode-(c) gate (EP-49) shows a need.
- Mechanising the step-6 elicitation-only checklist as a linter over concept prose.
- Whether `evidence_grade` should be dropped entirely in favour of the two prose fields, since a
  letter grade is exactly the kind of compression the no-ordinal rule exists to prevent — decide at
  the EP-16 re-plan.
