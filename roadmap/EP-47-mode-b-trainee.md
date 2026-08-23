# EP-47 — Mode (b) — trainee profile and non-surveillance guarantee

**Size:** M · **Mode:** b · **Core/Stretch:** core ·
**Depends on:** EP-46 (verification and re-plan P5) ·
**Blocks:** EP-48 (mode (c) self-reflection profile), EP-49 (per-mode eval sets, re-plan P6)

> **Charter.** Scope and acceptance below are sketches. **EP-46** (no-retention and no-egress
> harness, accessibility packet, re-plan P5) upgrades this to a full brief: `## Scope sketch` splits
> into `## In scope` / `## Out of scope`, and each criterion becomes a named command or artifact. Do
> not execute from the sketch alone.

## Context

Modes are built a → b → c (D-13), and mode (b) comes after mode (a)'s interface and verification
exist so it is a **profile over a proven engine**, not a parallel product. One engine, one input
contract, one output contract; what differs is `mode_scope` filtering, framing, guardrails,
escalation copy and eval set.

The defining constraint is not a feature but a promise. Mode (b) is **strictly local, with no
accounts, no scoring, no retention, no export, no employer visibility, and voluntary use only**
(D-19). The docs carry a **written non-surveillance guarantee** — and a guarantee is only real if its
enforcement is listed beside it, so each clause names the mechanism that makes it true: no account
system exists; no score is computed anywhere in the code path; D-52 forbids local logging in mode (b)
outright, not merely by default; D-6's no-export rule already removes the channel by which an
educator could obtain an artifact; and the absence of persistence is verified by EP-46's
filesystem-delta harness rather than asserted.

Reviewer sign-off gates mode (a) **only** (D-65), so mode (b) ships behind a public **"author review
only"** label. Without that label D-65 silently contradicts D-27.

## Safety preconditions

- **R-8 — trainee surveillance / compelled disclosure.** Educator-visible artifacts are *excluded*,
  not deferred. Nothing in this profile produces an output another party could obtain, and a test
  asserts the mode writes no file and emits no export affordance.
- **D-65 / R-9.** The "author review only" label appears in `README.md`, in `SAFETY.md` and in the
  interface itself — not only in the docs, where a user of the tool will not see it.
- **R-8 (assessment drift).** A trainee profile must not become an assessment instrument: no rubric, no grade, no
  ordinal field, no "your answer versus the model answer" framing.
- **Escalation invariance (D-57).** Mode (b) does not change the escalation panel. Its single-hash
  assertion must still hold across this profile's corpus.
- **Public artifact (D-3).** Checklist items 2 (PHI patterns in any education-context example, all of
  which are manifestly fictional), 4 (local paths) and 7 (public claims).

## Scope sketch (refine at re-plan)

1. `mode_scope` filtering rules and the trainee-facing framing of the same concepts — different
   register, identical clinical substance.
2. The non-surveillance guarantee written as a promise with each clause's enforcement listed, in
   `PRIVACY.md` and `SAFETY.md`, and summarised in the interface.
3. Education-context contraindications: not for assessment, not for observation, not a substitute for
   supervision, not to be run at an educator's request as a condition of anything.
4. The mode (b) copy deck as an extension of the EP-39 deck, subject to the same banned-phrase lint.
5. The public "author review only" label wired into the badge scheme (D-59) so CI can check it.

## Verification / acceptance (sketch)

- Filesystem-delta harness over a mode (b) session shows zero writes; no export affordance exists in
  any rendered response (scripted).
- A scripted check finds no score, grade, rubric or ordinal field anywhere in the mode (b) path.
- Every clause of the non-surveillance guarantee resolves to a named enforcement mechanism; a
  scripted check fails on a clause with none.
- The escalation panel's single-hash assertion holds across the mode (b) corpus.
- The "author review only" label is present in all three places and checked by CI.

## Parked → final-roadmap.md

- Trainee-controlled opt-in local retention (v1.x, D-19).
- Any educator-facing artifact, in any form (excluded, not deferred).
