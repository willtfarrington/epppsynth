# EP-53 — Clinical-reader narrative and site card correction

**Size:** M · **Mode:** n/a · **Core/Stretch:** core ·
**Depends on:** EP-52 (mode (a) gate assembly, IP clearance, badge upgrade) ·
**Blocks:** EP-54 (final retro and final-roadmap compilation)

> **Charter.** Scope and acceptance below are sketches. **EP-49** (per-mode eval sets, author-review
> labels, re-plan P6) upgrades this to a full brief: `## Scope sketch` splits into `## In scope` /
> `## Out of scope`, and each criterion becomes a named command or artifact. Do not execute from the
> sketch alone.

## Context

Follows the gate because the public narrative and the site card both quote the README status line,
and that line only becomes true at the gate (R-36).

Two deliverables. The **clinical-reader narrative** lives **in-repo** at
`epppsynth/docs/for-clinical-readers.md` — one canonical source, with the personal site linking to it
rather than restating it, because two copies drift. Roughly 1,200–1,800 words for a non-engineer
clinical reader, one diagram, seven parts: the problem in clinical language; what happens on the one
screen, walked through with a manifestly fictional case; what the tool refuses to do and why each
refusal exists; where the ideas come from and who says so; how we would know if it were harmful —
the eval gates and the stop criterion stated as thresholds a hospitalist can evaluate; what is not
built yet; and who is accountable.

The **site card** is wrong in three ways, not one. It currently badges the project **"Private"**,
which is false — the repository is public — it sits in the private grid, and its hook names the
regulated clinical modality the project retired (D-4). The fix is **one card replacement**, moved to
the public grid, with the hook quoting the README status line verbatim. **Every other change to that
site is parked** (D-43): no nav counts, no section copy, no other project entry.

## Safety preconditions

- **Anti-overclaim, the narrative's binding rule:** present tense **only** for what exists today;
  everything else is written "planned (EP-n)". No benchmark number without an evidence file, no
  comparison to any product or to a human, no efficacy or outcome language, and every claim traceable
  to a `D-n` or an evidence artifact.
- **R-12 / D-63.** The narrative states the null-to-adverse analogue evidence plainly; it may not
  imply that communication preparation is inherently benign.
- **R-38.** The narrative repeats that third-party use is not an intended use, that there is no
  installability guarantee, and that the repository is public as a source artifact, not a product.
- **R-9 / R-36.** One canonical source: the README status line, quoted verbatim by both the card and
  the narrative. Any divergence is a defect, re-checked at every re-plan.
- **Public artifact (D-3).** Checklist items 3 (protected text — the diagram and the worked case
  quote nothing from the corpus), 5 (any image re-opened and read, EXIF stripped, no local path in a
  title bar) and 7 (public claims must agree across README, badge, card and `CITATION.cff`).

## Scope sketch (refine at re-plan)

1. Write `epppsynth/docs/for-clinical-readers.md` to the seven-part structure with one diagram; state
   the anti-overclaim rules at the top of the document itself.
2. Link it from the README's clinical reading path.
3. Replace the personal site's project card: delete it from the private grid; insert the corrected
   card into the public grid after the sibling in-progress project; badge and hook rewritten.
4. Verify nothing else on that page contradicts the new copy — the private-grid trailing note and any
   counts must still read correctly after the move.
5. Confirm the card renders correctly in both light and dark themes.

## Verification / acceptance (sketch)

- Scripted grep over the card: no "Private" badge, and no retired-modality wording.
- The hook's status sentence matches the repository README's status line verbatim (scripted diff).
- The page validates and both themes render the badge correctly.
- Every capability sentence in the narrative is either present-tense-and-true and traceable to a
  shipped EP, or tagged "planned (EP-n)" — a reviewer pass recorded in the completion note.
- *(judgement, owner)* A non-engineer reader can state what the tool refuses to do after one read.

## Parked → final-roadmap.md

- Every other change to the personal site (D-43) — nav, section copy, other project entries.
- Any translated, printed or slide version of the narrative.
