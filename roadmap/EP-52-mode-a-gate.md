# EP-52 — Mode (a) gate assembly, IP clearance checkpoint, badge upgrade

**Size:** M · **Mode:** a · **Core/Stretch:** core ·
**Depends on:** EP-50 (release-gate evidence bundle and CI enforcement), EP-51 (human-factors
protocol and run) ·
**Blocks:** EP-53 (clinical-reader narrative and site card)

> **Charter.** Scope and acceptance below are sketches. **EP-49** (per-mode eval sets, author-review
> labels, re-plan P6) upgrades this to a full brief: `## Scope sketch` splits into `## In scope` /
> `## Out of scope`, and each criterion becomes a named command or artifact. Do not execute from the
> sketch alone.

## Context

The gate itself. EP-50 built the machinery and EP-51 produced the human-factors evidence, so this
brief **checks** rather than constructs: assemble the eight items into `docs/evidence/mode-a-gate.md`,
run the full pre-publication checklist, record the clearance outcome, and only then let the badge
move.

Two things gate the first public tag independently of the evidence. The **employment/IP clearance
checkpoint** (D-29) is issue-spotting only — the checkpoint names qualified review, it does not
substitute for it — and it must be completed and dated **before** the tag, not concurrently. And the
badge is a static README string that CI resolves to an evidence file and refuses to upgrade without
it (D-59); the flip is therefore a consequence of the evidence existing, never a decision taken
alongside it.

**Which sign-offs, not how many.** Gate item 2 is satisfied only if the recruited sign-offs include
the **lived-experience reviewer's** (D-64, `GOVERNANCE.md` §10); a count of two clinician sign-offs
does not satisfy it. If that role could not be recruited or withdrew, the gate may proceed **only**
on an explicit, dated **waiver published** in `docs/evidence/mode-a-gate.md` *and* in the public
README status line, naming what was lost — the coercion and forced-meaning lens went unexercised, so
the coercion findings rest on clinician judgement alone. **Silent omission is a gate failure.** The
waiver is a disclosure, never a substitute: it does not upgrade the badge's claim and it is quoted
verbatim by EP-53 rather than paraphrased.

Reviewer sign-off gates mode (a) **only** (D-65). Passing this gate changes nothing about modes (b)
and (c), whose "author review only" labels — and mode (c)'s `draft` banner and "no evaluation exists
for this mode" line (D-66) — are re-checked here precisely because a mode (a) tag is the moment a
reader is most likely to over-generalise.

## Safety preconditions

- **R-9 / R-36.** The README status line becomes the single canonical claim; nothing else in the
  repository or on the personal site may say more than it does. EP-53 quotes it verbatim.
- **R-30.** The tag is cut only against the build whose hash the manifest records.
- **D-37 / R-9.** If a stop-criterion trigger has fired at any point, the halt and its resolution are
  in the public README before the tag, not after.
- **D-61.** Excluded modes (d) and (e) remain stated as **excluded with seven named preconditions**,
  not "deferred" — re-checked here because a v1 tag is when "deferred" starts to read as "coming".
- **Public artifact (D-3).** The **entire** pre-publication checklist, all seven items, executed
  against a specific commit, signed and dated. Not a subset.

## Scope sketch (refine at re-plan)

1. Assemble `docs/evidence/mode-a-gate.md`: each of the eight items ticked with a link to its
   artifact in `release-evidence/<tag>/`. For item 2, record each sign-off **by role** and assert
   that the lived-experience role is present, or attach the dated published waiver described above.
2. Record the D-29 employment/IP clearance outcome as a dated `ip-clearance.md`, naming the external
   input relied on.
3. Run the full pre-publication checklist; sign and date it against the commit.
4. Re-check the mode (b) and (c) labels and mode (c)'s `draft` banner.
5. Flip the maturity badge, then and only then consider cutting the tag.
6. Record any item that failed and what was done about it — a gate with no recorded failures over a
   project this size deserves suspicion.

## Verification / acceptance (sketch)

- CI's badge check passes only *after* the evidence file exists and every checklist box in it is
  ticked; the deliberate red run from EP-50 is re-confirmed here.
- The manifest's recorded build hash equals the tagged commit.
- `ip-clearance.md` exists, is dated, and is not expired.
- Modes (b) and (c) labels present and CI-checked.
- Gate item 2 lists sign-offs **by role**, and either the lived-experience role appears among them or
  a dated waiver naming what was lost is present in both the gate evidence and the public README
  status line; a scripted check fails the gate if neither holds.
- *(judgement, owner)* The pre-publication packet is signed against a named commit; no item was
  waived, and any that could not be completed is recorded as blocking rather than skipped.

## Parked → final-roadmap.md

- Tags for modes (b) and (c) (their gates are EP-49's and are separate, D-13).
- Any release beyond the first public tag: rollback notes, deprecation and archive procedure.
