# EP-51 — Human-factors protocol and run

**Size:** L · **Mode:** a · **Core/Stretch:** core ·
**Depends on:** EP-37 (reviewer recruitment pack, re-plan P4), EP-46 (verification and re-plan P5) ·
**Blocks:** EP-52 (mode (a) gate assembly)

> **Charter.** Scope and acceptance below are sketches. **EP-49** (per-mode eval sets, author-review
> labels, re-plan P6) upgrades this to a full brief: `## Scope sketch` splits into `## In scope` /
> `## Out of scope`, and each criterion becomes a named command or artifact. Do not execute from the
> sketch alone.

## Context

Formative, solo-feasible, **fictional material only**, sized to roughly three hours per reviewer
across two sessions. Reviewer roles are settled (D-64): a clinician in serious illness or palliative
care; a clinician-educator; and **a person with lived experience of serious illness or a patient
advocate** — the coercion and forced-meaning lens, which is the strongest available safeguard against
R-1 and the role most likely to be dropped for convenience. Treat it as required. An optional fourth
is an ethicist, chaplain or disability-community reviewer.

Two framings must be right from the start. D-7's success criterion is a **feasibility and
acceptability** measure, never an effectiveness claim (D-63) — the closest analogue trials are
null-to-adverse, and one found a small worsening of patient-reported depressive symptoms. And time
claims are reported as *"median time-to-3–5-waypoints of X seconds over N fictional cases with M
readers"*, never as a bare threshold.

**The human-subjects determination, restated correctly.** This activity is **product usability
testing of one specific artifact** — a formative, unblinded, small-N evaluation of *this build* on
*fictional material*, designed to find defects in this tool. It is not designed to develop or
contribute to **generalizable knowledge** about clinicians, patients, communication, or any
intervention class, and that is the ground of the determination. An earlier formulation rested it on
the study being "not intended for publication"; that reasoning is unsound, because **the plan does
publish**: the aggregate report goes into the public release-evidence bundle (EP-50) and EP-53 writes
a public narrative from it. The consent says so in plain words rather than eliding it — aggregate and
role-attributed only, individual scores never (see the safety preconditions).
Record a **dated, written self-determination** at `docs/evidence/human-subjects-self-determination.md`
— the activity, why it is non-generalizable, the public dissemination, and an explicit note that this
is a self-determination by a non-expert, not a determination by an IRB or QI committee. The trigger
naming is unchanged (D-77): if the design ever aims at generalizable knowledge — a study *of*
clinicians or patients rather than of this artifact, a comparative or hypothesis-testing design, real
patient material, or any framing as research about the intervention class — an IRB or QI
determination is required **first**, and `GOVERNANCE.md` names that trigger. Since §10's current
wording still rests on non-publication, record the corrected reasoning as a dated addendum under
§10 and under D-77.

## Safety preconditions

- **Reviewer distress and burden — the lived-experience reviewer is the most exposed participant.**
  This material is serious-illness content and the red-team set is crisis-adjacent; the reviewer with
  lived experience of serious illness carries the most exposure to it and had no provision until
  this clause. Binding on **session conduct**, not merely on the consent form (EP-37 states the same
  protocol at consent and onboarding):
  - **Pause, skip, stop.** The reviewer may pause at any point, skip any individual case, or end the
    session entirely, **at any time and without giving a reason**. The facilitator states this
    aloud at the start of each session and again before the red-team block, and the protocol
    forbids asking why. Doing any of it costs the reviewer nothing — not the role, not the sign-off,
    not the attribution.
  - **Advance warning and the right to decline the block.** Before consent and again before the block
    begins, the reviewer is told that the red-team set contains crisis-adjacent content (hard-stop
    cases touching self-harm, violence, abuse, severe distress), described at the level of what it
    covers rather than by example. They may **decline that entire block** and complete the rest of
    the review; this is recorded as a declined block, never as a partial, incomplete or failed
    session, and never counted against the planted-defect catch rate.
  - **A named support resource** is printed on the session sheet and read aloud — at minimum the same
    clearly-labelled resources the escalation constant ships (EP-20: 988 Suicide & Crisis Lifeline;
    emergency services) — together with a named study contact the reviewer may use to stop or
    reschedule without explanation.
  - **No justification for withdrawal.** Partial or total, no reason is requested or recorded;
    withdrawn material is discarded and already-recorded scores are removed on request.
  - **The debrief asks about burden as well as findings** — at least one question on how the material
    landed and whether anything should be handled differently for the next reviewer. Burden answers
    are findings: they can change the protocol, and they are summarised in the aggregate report
    alongside the usability findings.
  - Timing is subordinate to this: a session that runs short because a reviewer stopped is a complete
    session. Nothing here is waived for schedule.
- **R-24 — reviewer over-trust and social pressure.** The protocol is written so a reviewer can fail
  the tool cheaply: planted detectable defects in roughly one case in five, unannounced, plus a
  no-tool control subset.
- **R-28.** Attribution is role-only by default ("a palliative care physician"); named attribution
  appears in `NOTICE` / `CITATION.cff` only on explicit written opt-in with a standing right to
  withdraw. **Individual scores are never published** — aggregates and the sign-off statement only,
  which is the trainee non-surveillance principle applied to reviewers.
- **D-8.** The time-on-task timer is UI-instrumented and **non-retained**; no session recording, no
  transcript of typed text, no retained case content.
- **D-37.** Any reviewer answering "yes" to *does any output steer toward a particular decision?*
  counts toward the 5 % trigger and **blocks the gate** until dispositioned in writing.
- **Public artifact (D-3).** Checklist items 2 (PHI — fictional cases only, each with its "no real
  person" attestation) and 7 (public claims).
- **R-39 (pressure to use it on a real case).** The debrief asks the reader directly whether they
  wanted to use the tool on a real case, and the answer is published rather than filed away.

## Scope sketch (refine at re-plan)

1. The protocol document: comprehension (3-item check including "this is not a risk detector" and "no
   clinical recommendation was made"); cognitive load; trust calibration against planted defects;
   time-on-task reported as median and p90; **write-first added value** — the reader writes their own
   questions before seeing the tool, then marks which tool questions are new, and how often the tool
   *displaced* a question they already had; automation bias; warning recall and escalation locate;
   interruption and recovery; the accessibility walkthrough.
2. The one-page consent covering purpose, fictional material, no personal data beyond role, public
   paraphrase, right to withdraw, that participation is **not an endorsement of clinical use**, a
   plain statement of **what will be published** (an aggregate report in the public release-evidence
   bundle plus a public narrative written from it — aggregate and role-attributed only), a citation
   of the dated human-subjects self-determination, and the full distress and burden protocol from the
   safety preconditions (EP-37 authors the wording; this brief runs it).
3. The structured sign-off: role, what was reviewed (scenario-manifest hash plus build hash), S2/S4
   scores, and the three yes/no questions requiring **no / no / yes**.
4. Run the sessions and produce the aggregate report plus the per-reviewer signed statements. Record
   each sign-off **by role**, and either obtain the lived-experience reviewer's sign-off or produce
   the dated waiver named in the acceptance criteria.
5. Write the dated `docs/evidence/human-subjects-self-determination.md` before the first session, and
   record the corresponding dated addendum under `GOVERNANCE.md` §10 / D-77.

## Verification / acceptance (sketch)

- At least two signed, dated sign-offs exist, each citing this build hash and each answering
  no / no / yes; any other answer blocks the gate and is dispositioned in writing.
- **The roles are named, not just counted.** "Two sign-offs" is not sufficient on its own: the mode
  (a) gate requires the **lived-experience reviewer's sign-off specifically** (D-64,
  `GOVERNANCE.md` §10 — that role is the only one positioned to detect coercion and forced meaning
  from the side that bears its cost, and it is the role most likely to be dropped for convenience).
  Each sign-off records which role it is, and a check asserts the lived-experience role is among
  them. **The only alternative is an explicit, dated, published waiver** — in the gate evidence and
  in the public README status line — naming that the lived-experience review did not happen, why,
  and **what was lost by its absence** (specifically: the coercion and forced-meaning lens is
  unexercised, so the coercion findings rest on clinician judgement alone). Silent omission — two
  clinician sign-offs presented as a satisfied gate — is a gate failure, not a pass. EP-52 enforces
  this at assembly.
- The aggregate report publishes the planted-defect catch rate; a catch rate below roughly 50 % is
  recorded as a finding that blocks the D-7 claim, not the release.
- No individual score appears in any public artifact (scripted check over the bundle).
- Every claim sentence in the report names its instrument and its N.
- *(judgement, owner)* The report's limitations section is proportionate to a formative, unblinded,
  small-N study.

## Parked → final-roadmap.md

- Summative human-factors evaluation in a real environment with real users (an excluded-mode
  precondition, not a v1 item).
- Any evaluation designed to produce **generalizable knowledge** rather than to test this artifact —
  a study of clinicians or patients, a comparative or hypothesis-testing design, real patient
  material, or a framing as research about the intervention class. Any of these triggers the IRB/QI
  determination named in D-77 **before** the work starts.
