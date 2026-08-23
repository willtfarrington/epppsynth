# EP-54 — Final retro and final-roadmap compilation

**Size:** M · **Mode:** n/a · **Core/Stretch:** core ·
**Depends on:** EP-53 (clinical-reader narrative and site card correction) · **Blocks:** —

> **Charter.** Scope and acceptance below are sketches; **EP-49** (per-mode eval sets, author-review
> labels, re-plan P6) upgrades this brief to full form. This brief closes P7 and the roadmap; there
> is no phase after it, so it upgrades nothing. Do not execute from the sketch alone.

## Context

The last brief. It closes the roadmap the way every other phase was closed, and it is the one place
where the project's own record of what it got wrong is written down.

Three jobs. **Compile `final-roadmap.md`** from every executed brief's `## Parked →` section, so the
parking lot is a union of what was actually discovered rather than what was anticipated at planning
time. **Close the traceability loop**: every hazard `R-1 … R-41` names the brief that mitigates it
and the gate that verifies it, and `tools/roadmap_check.py` fails if a hazard names no brief or a core
brief names no acceptance evidence. **Rewrite the README status paragraph and the maturity badge** —
the one place where rewriting is mandatory at a re-plan (compaction rule 5), because a cold session
reads them first and the sibling project's late README-drift brief exists precisely because that was
allowed to rot.

Executed briefs' `## Context` sections are **never** rewritten; they are the historical record, and
staleness is annotated with a pickup note. Decision changes are dated addenda in `DECISIONS.md`,
never edits.

## Safety preconditions

- **R-9 / R-32.** The retro is where overclaim is most tempting, because it is written after the tag.
  Every summary sentence resolves to an evidence file or is written as a limitation.
- **D-37.** If a stop-criterion trigger fired at any point in the project, the retro states it and
  states its resolution, and the public README says so too.
- **D-63.** The retro records the founding hypothesis' no-evidence status as it stood at the end,
  unchanged by the project having been completed.
- **Public artifact (D-3).** Checklist items 4 (local paths, hostname, username across the whole
  roadmap directory, timings included) and 7 (public claims, across README, badge, `CITATION.cff`,
  the narrative and the site card simultaneously).

## Scope sketch (refine at re-plan)

1. Mirror every executed brief's `## Parked →` section into `final-roadmap.md`, deduplicated, each
   item naming the brief that discovered it.
2. Record timings against the S/M/L estimates for all eight phases, so the sizing model has actuals.
3. Traceability sweep: hazard → brief → gate, and requirement → architecture → brief → evidence;
   `roadmap_check.py` green with no unmatched hazard.
4. Rewrite the README status paragraph and badge to the true end state.
5. Write the retro: what the plan got wrong, which briefs were mis-sized, which decisions were
   reversed by addendum, and which hazards turned out to be inert.

## Verification / acceptance (sketch)

- `tools/roadmap_check.py` green: every ☑ hash resolves in `git log`, no dependency cycle, every
  hazard names a brief, every core brief names acceptance evidence.
- `final-roadmap.md` contains at least one entry from every executed brief that parked something, and
  no entry that no brief parked.
- The README status paragraph and badge agree with the evidence files (CI badge check).
- No local user-profile path, hostname or username anywhere under `roadmap/` (leak scanner).
- *(judgement, owner)* The retro names at least one thing the plan got materially wrong; a retro with
  none has not been written honestly.

## Parked → final-roadmap.md

- Everything in `final-roadmap.md` by construction; this brief adds no new parked items of its own.
