# EP-42 — Input form

**Size:** M · **Mode:** a · **Core/Stretch:** core ·
**Depends on:** EP-40 (loopback app shell), EP-41 (loopback security controls) ·
**Blocks:** EP-43 (waypoints panel), EP-46 (verification, accessibility packet, re-plan P5)

> **Charter.** Scope and acceptance below are sketches. **EP-37** (reviewer recruitment pack,
> re-plan P4) upgrades this to a full brief: `## Scope sketch` splits into `## In scope` /
> `## Out of scope`, and each criterion becomes a named command or artifact. Do not execute from the
> sketch alone.

## Context

Renders D-25's input contract: eight structured enum fields plus one optional free-text field. The
shell exists; the form does not. Every field is a `<fieldset><legend>` radio group and **not** a
`<select>`, because a select hides the option set and makes "prefer not to answer" invisible until
opened — the escapes have to be visible to be usable. Every group carries the three D-25 escapes
(unknown / not relevant / prefer not to answer) as real options with **no pre-selected default**, and
the form refuses submission with an unanswered group while offering "unknown" as the one-click
resolution named in the error text.

The free-text field is labelled **"What the person actually said"**, with helper text stating that
their words are quoted back and reasoned about and are never used to infer anything about who they
are. `autocomplete="off"` and `spellcheck="false"` are a **privacy control** here — they stop browser
form-history capture of D-8-adjacent text — and must be documented as such so a later reviewer does
not mistake them for an accessibility defect. WCAG 1.3.5 Identify Input Purpose is genuinely **N/A**:
no field collects information *about the user*, so no `autocomplete` token applies. Write the N/A
rationale down rather than leaving it silently unaddressed.

## Safety preconditions

- **R-3 / D-25.** The form collects declared structure, never inferred identity. Protected and
  identity-adjacent fields may change communication framing only, never clinical substance; the
  enforcement is EP-29's counterfactual suite, and this brief must not add any field that would
  make that suite unable to flip a value cleanly.
- **3.3.3 Error Suggestion (AA).** Validation that only colours a border is one of the four criteria
  this interface most plausibly fails by default. Errors carry `aria-invalid`, `aria-describedby`
  pointing at the error text, an error-summary heading at the top of the form linking to each failing
  group, and a focus move to that summary. The suggestion names the "unknown" escape explicitly.
- **D-8.** Nothing typed is persisted anywhere: no draft save, no local storage, no server-side
  session copy of the text beyond the request.
- **Public artifact (D-3).** Checklist items 2 (PHI patterns — every shipped example value is
  manifestly fictional), 4 (local paths) and 5 (screenshots).

## Scope sketch (refine at re-plan)

1. Eight `<fieldset><legend>` radio groups for D-25's fields — role · encounter temporality · stated
   communication/information preference · stated decision-sharing preference · self-described
   framework · uncertainty tolerance · illness stage · language/interpreter need — each with the
   three escapes and no default selection.
2. The free-text `<textarea>` with its label, helper copy, `autocomplete="off"`,
   `spellcheck="false"`, and **the length cap EP-41 fixed** — read from EP-41's bound, never
   re-declared here, which is why EP-41 is a dependency of this brief.
3. Error summary, per-field error text, focus management, and the documented 1.3.5 N/A rationale.
4. Target sizes of at least 24 × 24 CSS px (2.5.8), with the label text part of the target.
5. Instructions placed before the field, never as placeholder text — a placeholder is not a label.
6. Works identically on the no-JS full-page-POST path.

## Verification / acceptance (sketch)

- axe-core clean on the empty, filled and error states, using the dev-group tooling EP-40
  provisions (this brief installs nothing).
- Empty-submit test: the summary exists, receives focus, and each link resolves to a `<fieldset>`.
- A scripted assertion that no `<select>` and no pre-selected radio exists in the rendered form.
- A committed accessibility-tree snapshot, so structural regressions surface as a diff.
- The form submits and re-renders correctly with JavaScript disabled.

## Parked → final-roadmap.md

- Any field that infers rather than records (none is permitted in v1 by D-25).
- Saved drafts, input history, or a scenario picker (v1.x scenario library, D-32).
