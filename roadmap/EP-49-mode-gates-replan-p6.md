# EP-49 — Per-mode eval sets, author-review labels, re-plan P6

**Size:** L · **Mode:** b + c · **Core/Stretch:** core ·
**Depends on:** EP-47 (mode (b) trainee profile), EP-48 (mode (c) self-reflection profile) ·
**Blocks:** — (the mode (b) and (c) gates are separate from the mode (a) tag, D-13)

> **Charter.** Scope and acceptance below are sketches; **EP-46** (no-retention and no-egress
> harness, accessibility packet, re-plan P5) upgrades this brief to full form. This brief is also the
> P6 re-plan, and per `roadmap/README.md` it is the brief that upgrades the P7 charters to full form.
> Do not execute from the sketch alone.

## Context

D-13 makes each mode's eval set its own release gate, and a failing mode is withheld without blocking
the others. This brief builds those two gates and closes the phase.

It also settles the labelling that D-65 makes mandatory. **Reviewer sign-off gates mode (a) only**,
so modes (b) and (c) ship on author review and must both carry public **"author review only"**
labels; mode (c) additionally ships `draft`-labelled with a **"no evaluation exists for this mode"**
banner (D-66). Those labels are what keep D-65 from silently contradicting D-27 — an unlabelled mode
shipped without reviewer sign-off is an overclaim by omission (R-9).

The harness, taxonomy and thresholds already exist from P3, so this brief authors sets and wires
gates rather than building machinery. The numeric thresholds ratified in D-75 apply per mode unless
this re-plan changes them in writing.

## Safety preconditions

- **R-9 / R-32.** No mode may present as more validated than it is. The labels are checked by CI
  against the badge scheme (D-59), not by memory.
- **R-16.** Mode (c)'s composer rule is gated here as a **hard** criterion — no threshold, no
  tolerance, no exception path.
- **R-8.** Mode (b)'s non-surveillance clauses are re-tested as part of its gate, not accepted from
  EP-47's completion note.
- **D-57.** The escalation panel's single-hash assertion is re-run across all three profiles at once,
  because a per-mode variation would be exactly the failure R-34 names.
- **Public artifact (D-3).** Checklist items 2, 4 and 7 across the per-mode scenario sets and the
  public labels.

## Scope sketch (refine at re-plan)

1. Mode (b) eval set: trainee-framing fidelity, the non-surveillance enforcement tests, abstention
   behaviour under the education-context contraindications, and the no-write / no-export assertions.
2. Mode (c) eval set: the personal-meaning ↔ structural composer property test over the whole corpus,
   the refusal cases (screening, scoring, diagnosis, assessment-of-the-operator), and the
   resource-surfacing-without-triage cases.
3. Abstention property tests re-run in **all three** mode profiles (D-38's five triggers), because
   abstention is a tested safety behaviour, not a courtesy.
4. Banned-phrase lint over both per-mode copy decks, still reading the single list in `SAFETY.md`.
5. Wire the per-mode gates and their labels into the badge scheme and its CI resolver.
6. **Re-plan P6:** retro and timings; mirror every P6 brief's `## Parked →` section into
   `final-roadmap.md`; upgrade EP-50 … EP-54, the P7 charters, to full briefs; rewrite the README
   status paragraph and the per-mode badge rows so a cold session reads something true.

## Verification / acceptance (sketch)

- Both per-mode suites run in CI on the deterministic no-model path (D-42) and emit their reports.
- Mode (c): zero violations of the composer rule across the corpus — a single violation fails the
  gate outright.
- Mode (b): zero writes, zero export affordances, zero score-shaped fields.
- One distinct escalation-panel hash across all three profiles' corpora combined.
- "Author review only" present for both modes, and `draft` plus the no-evaluation banner present for
  mode (c), in the interface, `README.md` and `SAFETY.md`; CI fails if any is missing.
- *(judgement, owner)* Each mode's public status sentence is defensible against its evidence file.

## Parked → final-roadmap.md

- Reviewer sign-off for modes (b) and (c) (would require recruitment beyond D-64's mode (a) roles).
- Any cross-mode comparison claim; the modes are gated separately and are not benchmarked against
  each other.
