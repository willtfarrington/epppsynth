# EP-14 — Seed content C: trauma-informed principles + moral-injury conditions

**Size:** L · **Mode:** c (principles and cautions apply to a, b and c) · **Core/Stretch:** core ·
**Depends on:** EP-10 (Provenance, rights, reuse class, citation rule, authoring guide) ·
**Blocks:** EP-15 (critique-lens protocol and run), EP-16 (registry validator, re-plan P1)

## Context

The third seed-content brief, and the one that closes the relation graph: EP-12 and EP-13 both write
`constrained_by` edges into IDs this brief allocates. It authors three record sets:

1. the **six trauma-informed `principle` records** — constraints that filter or reshape any emission;
2. the **moral-injury `condition` records** — the mode-(c) substrate, describing *conditions of
   clinical work*, never a deficiency in the person doing it (**D-20**);
3. the **`caution` records** — anti-patterns, contraindications and abstention triggers, including
   the `escalates_to` edges that wire the deterministic hard stops.

**Two positions this brief must hold, both of which are easy to lose in the writing.**

- **Moral injury arises from conditions, not individual deficiency (D-20, charter clause).** A
  self-reflection tool can silently invert a structural claim into individual pathology — that is
  **R-16**, and it is the highest-severity content risk in this brief. The structural guard is the
  `locus` field plus the composer rule that any output set containing a `personal-meaning` concept
  must also contain a `structural` one (`CI-8`, D-20, R-16). This brief's job is to make that rule
  *satisfiable*: there must always be an eligible `structural` condition, or the composer falls to
  abstention.
- **The moral-injury literature is definitionally contested and its competing definitions were
  developed with a different population.** Every `condition` record carries the competing definitions
  as `contested_interpretations` rather than silently picking one, and states that applicability to
  clinical work is **asserted rather than established**.

**ID allocation (fixed by EP-9, do not deviate):** `EPS.PRN.0001–0008`, `EPS.CON.0001–0010`,
`EPS.CAU.0001–0012`, `EPS.QT.0050–0069`. Targets: 6 principles, ≈ 8 conditions, ≈ 10 cautions.

**What exists at pickup.** The schema, families, the closed `question_intent` enum, `schema_check`
(EP-9). `sources.yaml`, the permission matrix, the citation rule, the authoring guide and the
attestation file (EP-10). EP-12 and EP-13 may or may not have run; this brief does not depend on
them, but their `constrained_by` edges point here, so the IDs allocated above are **binding**. All
records land at `review_status: draft`.

Commands run from the workspace directory `epppsynth/` unless a step says "from the git root".

## Safety preconditions

- **R-16 (mode (c) inversion into individual pathology or de-facto distress screening) — the defining
  risk.** Guards: `locus` is **required** on every `condition`; at least three conditions must be
  `locus: structural` with an `activation_predicate` broad enough to be eligible in any mode-(c)
  request, so `CI-8`'s promotion step always has something to promote; **no** record may carry a
  score, severity, count or ordinal field; and no record may describe the operator as depleted,
  dysregulated, insufficiently resilient, or in need of self-care. Prose that would function as a
  screening item does not ship.
- **R-10 (mode (c) drifting into unlicensed mental-health self-help).** No `condition` record may
  offer a coping technique, an exercise, a reframe, or an intervention. Conditions **name**; they do
  not treat. The `invites` templates for conditions are questions and offers about the situation,
  never about the operator's inner state, and at least one is an `offer-referral` to a peer,
  professional or institutional resource **without triage** (D-20).
- **R-1 (coercion architecture).** The two trauma-informed principles most directly violated by a
  persuasion-shaped tool — *empowerment, voice and choice* and *collaboration and mutuality* — must
  be authored as **operative constraints with machine-checkable consequences**, not as values. Each
  gets at least one `caution` record naming a concrete anti-pattern the composer or the linter can
  catch.
- **R-5 (crisis mis-handling) / D-18, as narrowed by EP-20.** The `escalates_to` edges written here
  are **deterministic only** — they fire from explicit declared flags or a fixed structural checklist
  over **declared structured fields only**, never from a generative classifier and **never from a
  scan of the free-text field**, which is an inert echo (GOVERNANCE §4.2). A tool that scans prose
  for danger words is a risk detector, and an unreliable one, which is worse than none because it
  invites reliance. The tool is not a risk detector and must not be used as one; no `caution` prose
  may imply otherwise, and no `activation_predicate` or `escalates_to` condition authored here may
  name a free-text match. The escalation copy itself is a constant owned by EP-44, and the
  escalation panel renders byte-identically on every response (D-57) — nothing authored here may vary
  it.
- **R-15 / rights (D-62) — this brief's sharpest rights exposure.** The trauma-informed-care source
  family's reuse terms are **UNVERIFIED** (its page returned HTTP 403) and sit at
  `reference-only-pending-rights-check` unless EP-10's rights check cleared them. Under EP-10's
  permission matrix, an unverified or reference-only source's **wording may not inform prose**.
  Therefore: read `sources.yaml` for the current `reuse_class` before writing; author every principle
  as `reading-informed-original` in author-original wording, structure and sequence; and do **not**
  reproduce the source's list of principles in the source's order — that is abridgement, and
  abridgement is derivation (Y-8). Normative guidance under a non-commercial or share-alike licence
  is **referenced, never ingested**.
- **Y-4 (diagnostic drift) / no ordinals.** Neither `evidence_grade` nor any other graded field is
  permitted on a `principle`, `condition` or `caution` — `evidence_grade` is allow-listed for
  `function` records only.
- **`CI-1` / R-11.** `condition` is an **emittable** type, so every condition needs ≥ 1
  `counter_hypothesis_of` partner with a symmetric reverse edge. `principle` and `caution` are
  non-emittable and are exempt (EP-9 step 2).
- **D-74 citation limits.** Chapter-level locators only, no page ranges, no quoted phrase, no
  source's coinage or heading reused as a label. Quotation budget ≤ 25 words per quote, ≤ 150 per
  source — this brief quotes nothing.
- **Public-safety (D-3, R-6).** All prose public and original. No PHI pattern, no real person, no
  identifiable institution, no clinical vignette that could read as a real case, no local path,
  machine name or account name. Re-run the EP-6 pre-publication packet.
- **Not clinical guidance and not a mental-health service.** The mode-(c) records describe a
  *situation*; they hold no position on whether the operator's distress is proportionate.

## In scope

1. **Author the six `principle` records** (`EPS.PRN.0001–0006`, two IDs held in reserve). One per
   trauma-informed principle, in the author's own words and **not** in the source's order. Each
   record:
   - `prose` — states the constraint **operatively**: what an output may not do, and what the correct
     output is when the constraint bites. A principle written as a value ("we care about safety") is <!-- quote-budget-allow: a worked example of this project's own output constraint, authored here; not a quotation of any source -->
     rewritten as a constraint ("nothing in an output may assume a person wants a topic raised; where
     the person has declined, the correct output is the absence of a prompt plus a note that the tool
     has stopped");
   - `family` — safety-and-trust, permission-and-pacing, values-and-what-matters, connection-and-
     isolation, scope-and-referral, agency-and-control as fits; a principle's family is not used for
     diversification (principles are never emitted) but is required by schema;
   - `mode_scope: [a, b, c]` — principles constrain every mode;
   - `evidence: {claim_type: normative, empirical_support: not-applicable}`;
   - `derivation_mode: reading-informed-original`, `reuse_class` copied from the source's current
     value in `sources.yaml`;
   - `confidence: high` is defensible for a normative constraint the project is choosing to adopt;
     say so in the prose rather than implying empirical backing.
   - **Two of the six** — the voice-and-choice principle and the collaboration-and-mutuality
     principle — carry an explicit note that they are **named test criteria for the coercion
     evaluation** (EP-26 / EP-29), not generic values.

2. **Author ≈ 8 `condition` records** (`EPS.CON.0001–0010`). Each names a structural, relational or
   meaning-related condition of clinical work. Candidate axes, to be adjusted at authoring: a
   constraint between what a clinician judges right and what the setting permits; being required to
   deliver a decision made elsewhere; witnessing without a channel to act; a rupture in a
   relationship of trust with a team or an institution; carrying responsibility without
   corresponding authority; repeated exposure with no interval to reconstitute; a mismatch between
   the stated purpose of the work and its daily texture; loss of the sense that the work coheres.
   Each record:
   - `locus` — **required**; at least three records must be `locus: structural`, at least one
     `relational`, and the `personal-meaning` records must each have a structural counterpart that
     is eligible under the same or a broader `activation_predicate` (this is what keeps `CI-8`
     satisfiable);
   - `family` — spread across institutional-constraint, relational-rupture, witnessing-and-
     complicity, meaning-and-coherence, agency-and-control;
   - `mode_scope: [c]` for the operator-facing conditions; a condition that is also a *reading about
     the patient's situation* is a different record and belongs in `[a, b]` — do not dual-scope a
     record to make it do both jobs;
   - `prose` — describes the conditions, not the person; states in the record itself that no output
     may frame it as a coping deficit and that no output may score it;
   - `contested_interpretations` — **required and non-empty** on every condition. Write the competing
     definitions plainly: that the two dominant framings (betrayal of what is right by a legitimate
     authority in a high-stakes situation; and perpetrating, failing to prevent, or witnessing acts
     that transgress deeply held moral beliefs) are **not equivalent**, that both were developed with
     a population other than clinicians, and that applicability to clinical work is asserted rather
     than established;
   - `evidence: {claim_type: interpretive, empirical_support: contested-construct}`;
   - `confidence: low`;
   - ≥ 1 `counter_hypothesis_of` partner with the reverse edge present — for conditions, the natural
     counter is a different locus reading of the same situation, which is exactly the plurality
     `CI-8` is protecting.

3. **Author ≈ 10 `caution` records** (`EPS.CAU.0001–0012`). Three groups, each record naming a
   concrete, recognisable anti-pattern rather than a mood:
   - **Anti-patterns and contraindications** — the named v1 contraindications belong here as records
     the composer can attach: use during an active encounter; use with any real patient's
     information; use to prepare a conversation whose purpose is to obtain agreement; use as a
     substitute for chaplaincy, psychology, psychiatry, ethics consultation or interpreter services;
     use to assess or document any person's psychological state. Plus the coercion anti-patterns
     from the two named principles (objection handling; scripting a second attempt after a refusal;
     framing that makes one option feel safer or more courageous; treating a stated preference as an
     obstacle).
   - **Abstention triggers** — one `caution` per D-38 trigger, each carrying the trigger's
     `contraindicated_when` predicate so EP-20 can wire the precedence chain to data rather than to
     code constants. The scope trigger (D-38.1) is keyed on the literal
     `self_described_framework: outside-declared-scope` enum value, so scope is data, not engine
     judgement.
   - **Escalation** — the `caution` records carrying `escalates_to` edges to the escalation-copy ID.
     These fire deterministically from declared flags or the fixed checklist only. Their prose must
     repeat that the tool is not a risk detector.

4. **Author question templates** (`EPS.QT.0050–0069`) for the `condition` records — conditions are
   emittable and need `invites` edges. Rules: `form` ∈ {`question`, `offer`}; `question_intent` from
   the closed enum; **at least one `offer-referral`** template surfacing peer, professional and
   institutional resources **without triage** (D-20); no template asks the operator to rate, score or
   characterise their own state; no template offers a technique. Apply the hedge-deletion test.

5. **Close the relation graph.** After authoring, every `constrained_by` edge written by EP-12 and
   EP-13 must resolve to a record in this brief's allocated ranges. Run `schema_check` **without**
   `--allow-forward-refs` and fix any dangling target — either the edge was written against an ID
   this brief did not allocate (fix the edge, in the owning file, with a version bump and a changelog
   entry), or a needed record is missing (author it inside the allocated range). If EP-12 or EP-13
   has not yet run, record the unresolved direction in the completion note; EP-16 is where the graph
   must fully resolve.

6. **Satisfiability check for `CI-8`.** Enumerate every mode-(c) `activation_predicate` combination
   over the D-25 enum space that selects at least one `personal-meaning` condition, and confirm that
   each also selects at least one `structural` condition. Record the enumeration in the completion
   note. Any combination that fails is a **content** gap: either broaden a structural condition's
   predicate or narrow the personal-meaning one. Leaving it to the composer's abstention fallback is
   permitted but must be a recorded choice, not an oversight — an over-abstaining mode (c) trains the
   reader to dismiss abstentions (R-31).

7. **Provenance, rights and attestation** for every record per EP-10: resolving `source_id`,
   `derivation_mode` checked against the source's **current** `reuse_class` in `sources.yaml`, a
   chapter-level-only `short_citation` with no page range and no quoted phrase, `access_date`, and an
   `attestation_id` with a truthful `residual_concern`. For the trauma-informed principles
   specifically, the attestation's `residual_concern` should say honestly whether the record's
   *sequence* or *framing* tracks the source, since that is the abridgement exposure.

8. **Set every record to `review_status: draft`,** `version: 1`, `lang: en`, `variant_of: null`,
   `lenses_applied: []`, computed `content_hash`. Promotion is EP-15's.

9. **Documentation.** Add a note to `DESIGN.md` §Content recording the three record sets, the ID
   ranges consumed, the `CI-8` satisfiability result, and any `constrained_by` edge repaired in
   another brief's file. Add a dated addendum under **D-20** in `DECISIONS.md` recording that the
   conditions-not-deficiency claim is carried by the `locus` field plus `CI-8`, and that the
   competing definitions ship inside the records as `contested_interpretations`.

## Out of scope

- `given` concepts and the ordinary-concern counter-frame → **EP-12**.
- `function` concepts and the evidence appendix → **EP-13**.
- Applying the critique lenses and any promotion out of `draft` → **EP-15** (lens-derived `caution`
  records are added there, inside the reserve IDs of this brief's allocated range).
- Cross-file validation, the rendered markdown and the CI job → **EP-16**.
- The escalation copy constant and the escalation panel → **EP-44**; the abstention and hard-stop
  precedence chain implementation → **EP-20**.
- The charter clauses (moral injury arises from conditions; prohibited manipulation; contraindications
  and escalation) → **EP-3** (`SAFETY.md`); this brief supplies the records they govern.
- The user-facing wording of abstention text, the stop card and the referral copy → **EP-39**.
- The mode-(c) profile wiring, its guardrails, its `draft` label and its "no evaluation exists for
  this mode" banner → **EP-48** (D-66).
- Mode-(c) evaluation and inversion probes → **EP-49**.
- Any distress measure, screening instrument or score → **excluded by decision** (D-20); no EP owns
  it.

## Verification / acceptance

- `uv run python -m epppsynth.registry.schema_check --rights` exits `0` over the three authored files
  (add `--allow-forward-refs` only if EP-12 or EP-13 has not yet run, and say so in the completion
  note).
- `uv run python -m epppsynth.registry.schema_check --rights --json` reports: `locus` present on
  every `condition`; ≥ 3 conditions with `locus: structural`; every `condition` has a non-empty
  `contested_interpretations` and ≥ 1 symmetric `counter_hypothesis_of`; zero ordinal-field
  violations across all three sets; zero citation violations; zero quoted words for the
  trauma-informed source.
- `uv run pytest tests/ep/test_ep14.py -q` green, asserting: no `principle`, `condition` or `caution`
  record carries `evidence_grade`; every D-38 trigger has exactly one `caution` record with its
  `contraindicated_when` predicate; the scope trigger is keyed on the literal
  `outside-declared-scope` value; every `escalates_to` edge resolves to the single escalation-copy
  ID; at least one `offer-referral` template exists in the allocated `QT` range; no
  `question_template` in the range asks the operator to rate or score anything.
- A `CI-8` satisfiability test: for every mode-(c) predicate combination that selects a
  `personal-meaning` condition, at least one `structural` condition is also selected — or the
  combination is listed in an explicit, committed exceptions file with a reason.
- `uv run python -m epppsynth.registry.schema_check` run **without** `--allow-forward-refs` exits `0`
  once EP-12 and EP-13 have both landed; if this brief runs last, that is the acceptance run.
- From the git root: `python tools/roadmap_check.py --context-budget EP-14` passes.
- Pre-publication packet (EP-6) re-run for *protected text*, *quotation budget*, *PHI patterns* and
  *local paths*; output recorded in the completion note.
- *(judgement — author)* No `condition` record's prose could be read as a screening item. Test: could
  a reader answer it on a scale? If yes, rewrite.
- *(judgement — author)* No principle reproduces the source's list order, and each is written as a
  constraint with a stated consequence rather than as a value.
- *(judgement — author)* Every `residual_concern` on a principle record honestly addresses sequence
  and framing.
- Commits: `feat(epppsynth): seed content C — trauma-informed principles, moral-injury conditions,
  cautions (EP-14)` then `docs(roadmap): record EP-14 commit hash`.

## Parked → final-roadmap.md

- Re-authoring the principle records if EP-10's rights check later clears the trauma-informed source
  family to `cc-by-4.0-compatible` — the current records are conservative by necessity and could be
  sharper with verified terms.
- Additional `condition` records if the mode-(c) evaluation (EP-49) shows coverage gaps.
- A linter that detects screening-item phrasing (scalable predicates, frequency adverbs, intensity
  language) in `condition` prose, mechanising part of the R-16 guard that is currently judgement.
- Institution-specific resource entries beyond the shipped defaults — the local escalation config
  (EP-44) is the mechanism; the content is out of scope in v1.
- Whether the two reserved `PRN` IDs should hold a seventh and eighth principle drawn from the
  disability-community and narrative-medicine lenses, which are review lenses and not content in v1
  (D-14).
