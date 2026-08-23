# EP-44 — Escalation panel and local escalation config

**Size:** S · **Mode:** a · **Core/Stretch:** core ·
**Depends on:** EP-40 (loopback application shell) ·
**Blocks:** EP-46 (verification, accessibility packet, re-plan P5)

> **Charter.** Scope and acceptance below are sketches. **EP-37** (reviewer recruitment pack,
> re-plan P4) upgrades this to a full brief: `## Scope sketch` splits into `## In scope` /
> `## Out of scope`, and each criterion becomes a named command or artifact. Do not execute from the
> sketch alone.

## Context

Small, safety-critical, and kept as its own brief precisely so it is never folded into a larger
change where its invariant could be relaxed for a layout reason. This is the highest-consequence copy
in the product.

**The panel renders byte-identically on every response** — one distinct hash across the whole eval
corpus (D-57, R-34). That invariance is the mechanism: if the panel ever varied with input, clinicians
would learn to read it as a signal, and the flat public claim *this tool is not a risk detector*
(D-18) would become false in practice. A hard stop therefore adds a card in the **waypoints** region
(EP-43) and touches nothing here. The panel renders from a constant with no dependency on registry,
template or model load, so it is the one thing that still works when everything else has failed.

Heading, fixed: **"If you are worried about someone's safety"** — never "Risk", "Alerts", or "Flags".
The body states that the tool does not detect risk, never screens, scores or flags anyone, and that
nothing typed is checked for danger.

## Safety preconditions

- **A-8 — unverified at pickup.** The shipped US defaults were *not* re-verified during research.
  Each number is verified against its issuing authority and the verification date recorded before the
  panel ships; `GOVERNANCE.md` carries the annual re-check. A wrong number here is the worst
  available failure in the product.
- **R-34.** No geolocation, no conditional logic of any kind, no per-mode variation, no ordering that
  depends on input. The panel is a constant.
- **2.4.11 Focus Not Obscured (AA).** The panel is normal in-flow and **not** `position: sticky` or
  `fixed`; a sticky always-visible panel covering a focused control is one of the four criteria this
  interface most plausibly fails. At narrow widths it sits above waypoints, and tab order still
  matches reading order at every breakpoint.
- **D-3 / privacy.** Institution-specific numbers are identifying, so `escalation.local.toml` is
  **gitignored** with a shipped `.example`; checklist items 1 (secrets), 4 (local paths) and 7 (public
  claims) re-run before commit.
- **R-40 (the panel addresses the wrong person in mode (c)).** Invariance is **per mode**: mode (c)
  ships its own constant panel addressed to the operator, still byte-identical within the mode and
  still hash-asserted. A single global panel would speak about a third party to a distressed reader
  who is themselves the subject.

## Scope sketch (refine at re-plan)

1. The invariant panel: fixed heading, fixed body copy from the EP-39 deck, rendered from a constant.
2. Shipped US defaults, each with its issuing authority and verification date recorded in a committed
   provenance note beside the constant.
3. `escalation.local.toml` loading for institution-specific numbers, with `escalation.local.toml.example`
   shipped and the real file gitignored.
4. Layout placement rules: in-flow, above waypoints in the single-column breakpoint, reachable by a
   skip link, present identically on the no-JS path.
5. Confirm the panel satisfies 3.2.6 Consistent Help for free — worth naming, because the safety
   design is paying for a conformance requirement.

## Verification / acceptance (sketch)

- **One distinct hash** of the rendered panel across the entire eval corpus, including every hard-stop
  and abstention case — the phase's headline assertion.
- The word "risk" appears in the panel only inside the sentence that denies it (scripted).
- `git check-ignore -v` confirms the local config is ignored; the `.example` is tracked.
- With the local config absent, the shipped defaults render unchanged.
- Each number's issuing authority and verification date present in the completion note.

## Parked → final-roadmap.md

- Non-US escalation resource sets and any locale-aware selection.
- Any per-mode escalation variation (mode (c) resource copy is EP-48 and lives outside this panel).
