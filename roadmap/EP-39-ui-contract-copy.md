# EP-39 — UI contract, copy deck, banned-phrase lint

**Size:** L · **Mode:** a · **Core/Stretch:** core ·
**Depends on:** EP-3 (SAFETY.md — clinical-ethics charter), EP-21 (template composition, linters,
CLI) ·
**Blocks:** EP-40 (loopback app shell)

> **Charter.** Scope and acceptance below are sketches, not a final step list. **EP-37** (reviewer
> recruitment pack, re-plan P4) upgrades this brief to full form.

## Context

This brief writes the interface down before any HTML exists, because the two controls that matter
most in this UI are ordering rules and wording rules, and both are cheaper to fix in a document than
in six templates. It produces `epppsynth/docs/ui-contract.md`, a `copy/` deck in which every
user-visible string is data with an ID, and the banned-phrase lint.

Nothing UI-shaped exists at pickup. EP-3 has shipped `SAFETY.md` including the **published
banned-phrase list**; EP-21 has shipped the composer and its authoring-time linters. The list in
`SAFETY.md` is the **single source the lint consumes — never a copy**. Two files drift; one does not.

Two contract rules carry most of the safety weight. **Output order puts uncertainty first**:
known facts and unknowns, then hypotheses, then disconfirming questions. The contract is three parts,
not four: a values-to-options part was **deleted** rather than shipped permanently empty, so the copy
deck carries no strings for it and none may be added. Hypotheses are an ordered list of equal-weight
siblings with the
counter-hypothesis nested *inside* its own item and an insufficient-basis clause per hypothesis,
never a global footer. Abstention is a **first-class render**, template-enforced as mutually
exclusive with hypotheses. And nothing on this page can be skimmed in three seconds: no TL;DR, no
headline, no lead-bold sentence, no ranking, no confidence numbers, no copy-all, no animation, no
streaming reveal, and no spinner that mimics deliberation.

## Safety preconditions

- **R-33 / D-58.** The contract states, as a normative rule the CSS lint will enforce in EP-43, that
  uncertainty, counter-hypothesis, insufficient-basis and abstention text render at the same size,
  weight and contrast as hypotheses. This one rule is both the contrast requirement and the primary
  automation-bias control; it is written here so no later brief can treat it as styling.
- **R-34 / D-57.** The escalation heading is fixed at "If you are worried about someone's safety" —
  never "Risk", "Alerts", or "Flags". The copy deck carries it as an immutable string.
- **D-26b.** Every suggested utterance is a question or an offer; the contract states the render-time
  assertion and its **fail-closed** behaviour (internal-error card, never the offending text).
- **Public artifact (D-3).** Checklist items 3 (protected text — the copy deck quotes nothing from
  the corpus), 4 (local paths) and 7 (public claims) re-run before commit.

## Scope sketch (refine at re-plan)

1. `epppsynth/docs/ui-contract.md`: three always-present regions in DOM and visual order (input,
   waypoints, escalation), one route, no navigation; the three-part output order above; abstention and
   hard-stop render rules; the D-48 rule that confidence appears only in the provenance drawer.
2. `copy/` as data (one reviewable file per region), every string with an ID; the "nothing you type
   is saved" header line and the launch interstitial shown on **every** launch (D-60) — there is no
   persistence with which to remember a dismissal, and the friction is the safety feature.
3. The banned-phrase lint: reads `SAFETY.md`'s list, runs over `copy/`, over the templates, and over
   generated output **at render time**, failing closed in all three places.

   **Its scope is fixed by owner ruling OD-12 (confirmed 2026-08-31) and is not this brief's to
   re-open.** The ban governs **authored content and rendered output** — concept text, templates,
   the copy deck, composed waypoints. It does **not** govern documentation that names a phrasing in
   order to forbid it, or that reports what a user typed. Without that carve-out `SAFETY.md` §10 is
   unpublishable under its own rule: a list of banned phrases that could not contain the phrases
   could not be published. Two consequences the lint must implement rather than assume:

   - **The carve-out is scoped by target, not by exemption.** The lint runs over `copy/`, the
     templates and rendered output; documentation is **outside its input set**, not inside it with a
     waiver. Nothing about `SAFETY.md` §10 is allowlisted, because it is never scanned. A
     doc-shaped exemption inside the scanned set would be the hole this design avoids.
   - **Two of the 17 entries carry a `condition` field and need matcher support, not a plain
     grep.** `bp-010` (**overcome**) is banned only when the object is a person, their objection,
     their resistance or their refusal; `bp-014` (**goals-of-care conversation**) is permitted as a
     description of what happened and banned as an instruction to hold one; `bp-017` (**the evidence
     shows**) is banned unless the sentence resolves to a citation the renderer can bind to a source
     record — which is a **binding** check, not a text match, and is the reason it cannot be a grep
     at all. Ship a matcher per `condition` kind with its own unit tests, and fail closed on a
     `condition` value the matcher does not recognise: an unrecognised condition that silently
     passes turns a ban into a decoration.
4. Approved substitutes recorded beside the bans ("Something you might not have asked about yet" · "A
   reason this reading could be wrong" · "There is not enough here to say" · "This is outside what
   this tool covers"), so the ban is actionable rather than merely prohibitive.
5. A readability report on static chrome copy at a stated US grade 9–10 target that **reports and
   does not gate**; it is never applied to generated waypoints, which quote clinician-supplied words.

## Verification / acceptance (sketch)

- The lint fails on a planted "recommends" in `copy/`, in a template, and in a rendered string —
  three deliberate red runs recorded in the completion note.
- The carve-out is proven both ways: `SAFETY.md` itself passes (it is not in the input set) **and**
  a test asserts that adding a documentation path to the input set makes the lint fail, so the
  carve-out cannot be widened by accident.
- Each conditional entry has a red run **and** a green run: "overcome her objection" fails while
  "overcome by the news" passes; "schedule a goals-of-care conversation" fails while "after the
  goals-of-care conversation" passes; an unbound "the evidence shows" fails while a bound one
  passes. An unrecognised `condition` value fails closed, asserted by test.
- A scripted check proves the lint reads `SAFETY.md` and that no second copy of the list exists.
- Every ID in `copy/` is referenced by exactly one template slot; orphans and unused strings fail.
- *(judgement, owner)* The contract, read alone, is sufficient to build the panels without
  re-deriving any ordering decision.

## Parked → final-roadmap.md

- Mode (b) and mode (c) copy decks (EP-47, EP-48 extend this contract; they do not fork it).
- Localisation and any `lang` variant of the copy deck.
