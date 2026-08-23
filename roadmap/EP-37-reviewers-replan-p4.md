# EP-37 — Reviewer recruitment pack, re-plan P4

**Size:** M · **Mode:** a · **Core/Stretch:** core ·
**Depends on:** EP-23 (engine integration, re-plan P2), EP-35 (first measured run), EP-36 (gated LLM
renderer) ·
**Blocks:** EP-51 (human-factors protocol and run)

> **Charter.** **EP-31 (paired-preference harness, re-plan P3)** upgrades this to a full brief. This
> brief is itself the **P4 re-plan**: it upgrades EP-38 … EP-46 — the P5 charters — from charter
> briefs to full briefs, and re-charters P6. It also closes the phase, and it runs after EP-33's
> go/no-go, which is what the P4 re-plan mostly exists to absorb.

## Context

Implements D-27, D-64 and D-77, and unblocks D-35(2) — the release gate that requires **≥ 2 recruited
reviewers to sign off by role**. This is the longest-lead item in the plan and it sits here
deliberately: D-64 amended the timing so that outreach opens only once a functional stage exists, not
in P0. The pack may have been drafted earlier; **opening outreach is this brief's job**, and the
schedule exposure it creates is accepted and recorded.

**Roles.** (1) a clinician practising in serious illness / palliative / oncology care — the clinical
plausibility scorer; (2) a clinician-educator or trainee-facing faculty member — mode (b) relevance
and the non-surveillance guarantee; (3) **a person with lived experience of serious illness, or a
patient advocate — required, not optional.** That third role is the only reviewer positioned to
detect coercion and forced meaning from the side that bears its cost, and it is the role most likely
to be dropped for convenience. An optional fourth — ethicist, chaplain, or disability-community
reviewer — serves as the D-14 critique lens.

**Ask:** two sessions of 60–90 minutes, asynchronous permitted, ≈ 3 hours total. Session 1: read the
charter and limitations, then score fictional cases on the clinical-plausibility and coercion rubrics
(arm-blinded, per EP-29). Session 2: the human-factors protocol plus a structured debrief (EP-51).

## Safety preconditions

- **Consent states plainly that participation is not an endorsement of clinical use** (R-28), and
  that the tool is unvalidated with no evidence of benefit (D-63, R-38).
- **The human-subjects determination rests on non-generalizable knowledge, not on non-publication.**
  The activity is **product usability testing of one specific artifact**: a formative, unblinded,
  small-N evaluation of *this build* on *fictional material*, designed to find defects in this tool
  and not to develop or contribute to generalizable knowledge about clinicians, patients,
  communication, or any intervention class. That — not secrecy — is what places it outside
  human-subjects research.
  **State the public dissemination plainly rather than eliding it.** Findings *are* disseminated:
  an aggregate report is published in the public release-evidence bundle (EP-50), and EP-53 writes a
  public narrative from it. The pack must say so, in those words, so no reviewer consents on the
  belief that nothing will be public. What is published is aggregate and role-attributed; individual
  scores never are. An earlier formulation of this precondition rested the determination on the
  study being "not intended for publication" — that reasoning is **unsound as written**, because the
  plan does publish, and it is replaced here.
  **Record a dated, written self-determination in the repository** —
  `docs/evidence/human-subjects-self-determination.md`, dated and signed by the author, stating the
  activity, why it
  is non-generalizable product usability testing, that findings are publicly disseminated in
  aggregate, and that this is a self-determination by a non-expert and not a determination by an IRB
  or a QI committee. The pack cites it.
  The pack still **names the IRB / QI determination trigger** unchanged (D-77): if the activity is
  ever designed to produce generalizable knowledge — a study of clinicians or patients rather than of
  this artifact, a comparative or hypothesis-testing design, real patient material, or any framing as
  research about the intervention class — an IRB or QI determination is required **first**. It states
  the requirement; it does not make the determination. Record the corrected reasoning as a dated
  addendum under `GOVERNANCE.md` §10 and under **D-77**, since §10's current wording still rests on
  non-publication.
- Data minimisation: no personal data beyond role, plus a name only on explicit written opt-in.
- **Attribution is role-only by default** ("a palliative care physician"); named attribution appears
  in the citation and notice files only on written opt-in, with a standing right to withdraw.
- Individual scores are **never** published — aggregates and the sign-off statement only (D-19's
  non-surveillance principle applied to reviewers).
- Reviewer sign-off gates **mode (a) only** (D-65); the pack says so, so no reviewer believes they
  cleared (b) or (c). Reviewers score **before** any discussion with the author, and no flag is
  adjudicated downward (R-24).

## Scope sketch (refine at re-plan)

1. Re-plan pass: close P4 — record EP-35's measured wall-clock deadline and drop threshold as dated
   `DECISIONS.md` addenda, mirror `Parked →` items into `final-roadmap.md`, tick the phase boxes —
   then convert EP-38 … EP-46, the P5 charters, to full briefs, re-check their context budgets, and
   re-charter P6.
2. A one-page role description per role, including what the reviewer will and will not be asked to do.
3. The one-page consent: purpose; no PHI and no real cases; role-only data; paraphrase permission;
   right to withdraw at any time; the non-endorsement sentence; a plain statement of **what will be
   published** (an aggregate report in the public release-evidence bundle, and a public narrative
   written from it — aggregate and role-attributed, never individual scores); and a citation of the
   dated human-subjects self-determination.
4. **The distress and burden protocol, stated in the consent and repeated at onboarding.** The
   material is serious-illness content, and the reviewer with **lived experience of serious illness**
   is simultaneously the most exposed participant and, until now, the one with no provision. The pack
   states, in the reviewer's own copy and not only in the author's protocol:
   - the right to **pause at any point, skip any individual case, or stop the session entirely**,
     at any time, **without giving a reason** — and that doing so does not cost them the role,
     the sign-off, the attribution, or anything else;
   - **advance warning, before consent is given and again before the block begins, that the red-team
     set contains crisis-adjacent content** (hard-stop cases touching self-harm, violence, abuse,
     severe distress), described at the level of what it covers rather than by example — with the
     standing option to **decline that entire block** and complete the rest of the review, recorded
     as a declined block and never as a partial or failed session;
   - a **named support resource** printed on the consent and on the session sheet — at minimum the
     same clearly-labelled resources the escalation constant ships (EP-20: 988 Suicide & Crisis
     Lifeline; emergency services) — plus a named study contact the reviewer may reach to stop or
     reschedule without explanation;
   - **no requirement to justify a withdrawal**, partial or total; no follow-up asking why; withdrawn
     material is discarded and any already-recorded scores are removed on request;
   - a **debrief that asks about burden as well as findings** — at least one question about how the
     material landed and whether any part should be handled differently for the next reviewer —
     with its answers treated as findings that can change the protocol, not as pleasantries.
   None of this is optional or at the author's discretion, and none of it is traded away for
   schedule. EP-51 implements the same protocol in session conduct.
5. The attribution and withdrawal policy.
6. The **sign-off template**: role; what was reviewed (scenario-manifest hash + build hash); the
   plausibility and coercion scores; and three yes/no questions — *does any output steer toward a
   particular decision?* · *would any output mislead a clinician?* · *is the stated limitation
   language adequate?* Sign-off requires **no / no / yes**. Any "yes" on the first counts toward
   D-37's 5 % trigger and blocks the gate until dispositioned in writing.
7. A scheduling plan and a private outreach log; open outreach.

## Verification / acceptance (sketch)

- A reviewer could read the pack cold and decide whether to participate — no other document needed;
  the non-endorsement sentence, the withdrawal right, the statement of what will be published, the
  citation of the dated human-subjects self-determination and the IRB/QI trigger are all present,
  each asserted by a string check.
- The distress and burden protocol is present in the reviewer-facing consent, not only in the
  author's protocol: the pause/skip/stop right, the no-reason-required clause, the crisis-adjacent
  content warning with the block-decline option, the named support resource and the burden debrief
  question — each asserted by a string check.
- `docs/evidence/human-subjects-self-determination.md` exists, is dated, names the activity as
  non-generalizable product usability testing, states the public dissemination, and names the
  IRB/QI trigger.
- The sign-off template renders the three questions and the no/no/yes rule.
- The pack contains no PHI, no real case, and no identifying content about the author's workplace.
- The outreach log exists with dates and is excluded from the public tree.
- *(judgement — author)* the lived-experience role is described in a way a non-clinician would find
  respectful and legible.

## Parked → final-roadmap.md

- Per-mode sign-off for modes (b) and (c) — currently author review only (D-65, D-66); revisit at
  EP-49 whether the same three-question sign-off should extend to them.
- Compensation or honoraria for reviewers — not resolved for v1.
