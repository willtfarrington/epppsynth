# EP-45 — Provenance drawer

**Size:** M · **Mode:** a · **Core/Stretch:** core ·
**Depends on:** EP-43 (waypoints panel), EP-16 (registry validator, rendered markdown) ·
**Blocks:** EP-46 (verification, accessibility packet, re-plan P5)

> **Charter.** Scope and acceptance below are sketches. **EP-37** (reviewer recruitment pack,
> re-plan P4) upgrades this to a full brief: `## Scope sketch` splits into `## In scope` /
> `## Out of scope`, and each criterion becomes a named command or artifact. Do not execute from the
> sketch alone.

## Context

Makes every waypoint traceable. The charter treats an untraceable output element as a defect, so
each waypoint carries an inline disclosure revealing the authored paraphrase, its short citation, its
cultural scope and its review status — read from the registry the EP-16 validator guarantees.

The pattern is the ARIA **disclosure** pattern (`<button aria-expanded aria-controls>`), not a
tooltip. That choice is deliberate and cheap: it removes 1.4.13 Content on Hover or Focus from the
conformance surface entirely. **No `title` attribute and no hover-revealed content appears anywhere
in this interface.**

Two content rules are absolute. **D-23:** generated output is paraphrase plus citation and never
reproduces source text; the drawer displays no verbatim span. **D-74:** public short citations are
chapter-level locators only — no page ranges — with no quoted phrase, no chapter title used as a
concept label, and no locator sequence that reconstructs a source's outline.

**D-48** puts `confidence` here and nowhere else: it may appear in the drawer, never beside a
waypoint, because a number beside a hypothesis is exactly the authority the tool is designed to
withhold.

## Safety preconditions

- **R-35 / D-23.** The optional local-only source pane is *not* enabled by this brief. Its hook may
  exist, disabled, behind the double gate (an environment flag **and** a present local index), its
  templates live under a `local_only/` directory excluded from any published build, and CI asserts
  the flag is unset and that no published template references that directory.
- **R-11 / Y-1.** The drawer shows provenance, not endorsement: it never renders a concept as a
  finding about the person, and the tradition label and cultural scope are shown with the citation.
- **R-33 / D-58.** The disclosure trigger and its revealed content obey the uniform-typography rule;
  the drawer is not a place to demote uncertainty into small grey text.
- **Public artifact (D-3).** Checklist item 3 (protected text — a length-threshold check over
  everything the drawer can display), item 5 (screenshots), item 6 (licence conformance).

## Scope sketch (refine at re-plan)

1. Per-waypoint disclosure button with `aria-expanded` and `aria-controls`; Enter and Space activate;
   Escape closes and returns focus to the trigger; no keyboard trap.
2. Drawer content from the registry: authored paraphrase, chapter-level short citation, source
   attribution, `cultural_scope`, `review_status`, contested interpretations where present, and
   `confidence`.
3. Target size at least 24 × 24 CSS px for the trigger (2.5.8), with label text part of the target.
4. Works on the no-JS path — a disclosure that only opens with htmx is a broken disclosure; the
   fallback renders the drawers expanded or as a full-page render.
5. The disabled, double-gated source-pane hook and its CI assertions.

## Verification / acceptance (sketch)

- Keyboard-only open, close and return-focus test for every drawer on the page.
- Scripted assertion that no `title` attribute and no hover-revealed content exists in any rendered
  response.
- Every displayed citation resolves to a live registry ID; an unresolvable citation fails the render
  rather than degrading silently.
- No displayed string exceeds the D-74 quotation budget; no chapter title appears as a label.
- With JavaScript disabled, every drawer's content is reachable.

## Parked → final-roadmap.md

- Enabling the local-only source pane (stretch; its four negative tests are specified in the P5
  standing decisions and its hazard is R-35).
- Cross-linking the rendered registry markdown from the drawer.
