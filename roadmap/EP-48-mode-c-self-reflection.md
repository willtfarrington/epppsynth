# EP-48 — Mode (c) — clinician self-reflection profile

**Size:** L · **Mode:** c · **Core/Stretch:** core ·
**Depends on:** EP-47 (mode (b) trainee profile) ·
**Blocks:** EP-49 (per-mode eval sets, re-plan P6)

> **Charter.** Scope and acceptance below are sketches. **EP-46** (no-retention and no-egress
> harness, accessibility packet, re-plan P5) upgrades this to a full brief: `## Scope sketch` splits
> into `## In scope` / `## Out of scope`, and each criterion becomes a named command or artifact. Do
> not execute from the sketch alone.

## Context

The last mode and the one with the highest inversion risk. Mode (c) is **scoped to naming structural
and existential dimensions of a clinical experience** (D-20). It **refuses distress screening,
scoring and diagnosis**, and it surfaces peer, professional and institutional resources without
triage. It holds no position on whether the operator's distress is proportionate, and it never
describes the operator as depleted, dysregulated, insufficiently resilient, or in need of self-care.

The charter clause is the design, not the tone: **moral injury arises from conditions, not individual
deficiency** — the charter wording fixed in `SAFETY.md`. The mechanism that makes that true is a composer rule, not careful wording —
**any output set containing a personal-meaning concept must also contain a structural one, enforced
by the composer.** A profile that only *sounds* structural will drift into individual pathology under
the first ambiguous case; a composer that refuses to emit the set will not.

Mode (c) ships **`draft`-labelled with a "no evaluation exists for this mode" banner** (D-66), even
after its own gate, and carries the public "author review only" label because reviewer sign-off gates
mode (a) alone (D-65). Both labels are conditions of shipping, not decorations.

## Safety preconditions

- **R-16 — mode (c) inverting into individual pathology or distress screening.** The primary control
  is the composer rule above, machine-tested. Secondary controls: no ordinal, severity, score or
  count field may exist in this profile (the registry validator already rejects them); no screening
  question; no "how are you coping" instrument; no longitudinal anything.
- **R-10.** The profile must not become unlicensed mental-health self-help. Resources are surfaced
  without triage, without ranking, and without any statement about what the operator should do.
- **D-18 / D-57.** Still not a risk detector, and the escalation panel still renders byte-identically
  — including here, where the operator is the subject. Its single-hash assertion covers this corpus.
- **D-66 / D-65 / R-9.** The `draft` label and the "no evaluation exists for this mode" banner appear
  in the interface, in `README.md` and in `SAFETY.md`; the badge scheme (D-59) can resolve them.
- **Public artifact (D-3).** Checklist items 2 (PHI — all examples manifestly fictional), 4 (local
  paths) and 7 (public claims — nothing here may imply a wellbeing benefit; D-63's null-to-adverse
  evidence posture applies with full force).
- **R-40 (the panel addresses the wrong person).** This mode owns the operator-addressed escalation
  constant defined in EP-44, and its single-hash assertion runs against the mode (c) corpus.

## Scope sketch (refine at re-plan)

1. The mode (c) profile: clinician-reaction concepts, `mode_scope` filtering, and the resource-
   surfacing copy written without triage language.
2. The composer guardrail — a `personal-meaning` concept never emits without a `structural`
   companion — implemented in the composer and property-tested, not asserted in review.
3. The refusals wired as abstentions with named reasons: distress screening, scoring, diagnosis, and
   any request for an assessment of the operator.
4. The mode (c) copy deck extending EP-39's, subject to the same banned-phrase lint, plus this mode's
   own additions (no "resilience", no "burnout score", no "self-care plan").
5. The `draft` banner and the "author review only" label wired for CI checking.

## Verification / acceptance (sketch)

- Property test: across the profile's whole corpus, **no** output set contains a personal-meaning
  concept without a structural one — zero exceptions, no override path.
- A scripted check finds no ordinal, severity, score or count field anywhere in the mode (c) path.
- Each refusal produces its abstention record and zero concept content.
- The escalation panel's single-hash assertion holds across the mode (c) corpus.
- The `draft` label and the no-evaluation banner are present in all three places and CI-checked.
- *(judgement, owner)* No output reads as a statement about the operator rather than about conditions.

## Parked → final-roadmap.md

- Any distress measure, instrument or score, in any form (permanently excluded).
- Longitudinal tracking, journaling or any retained self-reflection artifact (D-8 forbids it in v1).
