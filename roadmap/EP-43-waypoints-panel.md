# EP-43 — Waypoints panel, abstention and hard-stop renders, focus management

**Size:** L · **Mode:** a · **Core/Stretch:** core ·
**Depends on:** EP-42 (input form), EP-21 (template composition, linters, CLI) ·
**Blocks:** EP-45 (provenance drawer), EP-46 (verification, accessibility packet, re-plan P5)

> **Charter.** Scope and acceptance below are sketches. **EP-37** (reviewer recruitment pack,
> re-plan P4) upgrades this to a full brief: `## Scope sketch` splits into `## In scope` /
> `## Out of scope`, and each criterion becomes a named command or artifact. Do not execute from the
> sketch alone.

## Context

The panel that renders D-11's three parts, and the highest-consequence UI brief in the phase. The
engine (EP-21) emits a validated three-part bundle; the form (EP-42) submits; nothing renders yet.

**Output order puts uncertainty first**: known facts and unknowns, then hypotheses, then
disconfirming questions. There is no values-to-options region: a fourth part connecting stated values
to clinician-verified options was **deleted** from the contract rather than left undeliverable (it
had no input field, no content source and no owning brief), so this panel has no region to render for
it and must not grow one. The unknowns list is never empty —
if the engine has no unknowns it abstains (D-38.2) rather than printing "none". Hypotheses are an
`<ol>` of at least two equal-weight siblings with the counter-hypothesis nested **inside** its own
`<li>` and an insufficient-basis clause per hypothesis, never a global footer disclaimer. Abstention
is a **first-class render**, template-enforced as mutually exclusive with hypotheses, styled as a
result and not as an error. A hard stop adds a card in **this** region and touches nothing else — the
escalation panel never varies (D-57).

Nothing here may be skimmed in three seconds: no TL;DR, no headline, no lead-bold sentence, no
ranking, no "most likely", no confidence numbers or bars (D-48 keeps `confidence` in the provenance
drawer), no copy-all, no animation, no streaming reveal, and no spinner that mimics deliberation.

## Safety preconditions

- **R-33 / D-58 — the single most load-bearing rule in the interface.** Counter-hypothesis,
  insufficient-basis and abstention text render at the same size, weight and contrast as hypotheses,
  and a CSS lint refuses muted colour tokens anywhere inside the waypoints region. This is
  simultaneously the 1.4.3 contrast requirement and the primary automation-bias control; it is not
  styling and may not be traded against layout.
- **R-37 / 4.1.3 Status Messages.** Results injected with no announcement and no focus move is one of
  the four default failures. Both are required: an `aria-live="polite"` status region announcing the
  result **and** a focus move to the results heading. `role="alert"` is reserved for hard stops and
  abstentions, at most one per response — alert flooding desensitises the hard-stop announcement.
- **1.3.1 Info and Relationships.** The hypothesis ↔ counter-hypothesis relationship is carried by
  nesting, never by adjacency; each part is a `<section aria-labelledby>`.
- **D-26b.** Every rendered utterance in the questions region parses as a question or an offer, with
  a render-time assertion that **fails closed** to an internal-error card rather than emitting text.
- **Y-3 / D-14.** The tradition label renders beside every given, on screen, not only in the docs.
- **Public artifact (D-3).** Checklist items 2 (PHI in fixtures), 3 (protected text — renders are
  paraphrase plus citation, never verbatim) and 5 (screenshots).

## Scope sketch (refine at re-plan)

1. The three parts in fixed order, each a labelled section; unknowns never empty.
2. Hypotheses as an `<ol>` of equal-weight siblings; counter-hypothesis nested inside its `<li>`;
   per-hypothesis insufficient-basis clause.
3. Abstention card naming its D-38 reason and emitting zero hypotheses, with the mutual exclusion
   enforced by the template structure rather than by a branch a future edit could add.
4. Hard-stop card rendered in this region only.
5. Focus and announcement wiring; the at-most-one-assertive-region rule.
6. The uniform-typography tokens plus the CSS lint that enforces them.
7. The render-time question-or-offer assertion and the internal-error card it fails to.
8. Identical behaviour on the no-JS full-page-POST path, including the focus move.

## Verification / acceptance (sketch)

- Focus lands on the results heading after every successful submit (browser test).
- Exactly one assertive region exists on hard-stop and abstention responses, and none otherwise.
- Golden-file test proving no template branch renders hypotheses and an abstention together.
- CSS lint green; contrast checks pass for every text run inside the waypoints region.
- A planted assertion-shaped utterance renders the internal-error card, not the string.
- Zero animation and no streaming behaviour in any state; committed accessibility-tree snapshots.

## Parked → final-roadmap.md

- Export, copy-all, print styling and any shareable rendering (excluded in v1 by D-6).
- Any ranking, scoring or ordering-by-confidence affordance (permanently excluded).
