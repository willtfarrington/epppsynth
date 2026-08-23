# EP-20 — Abstention and hard-stop precedence chain

**Size:** M · **Mode:** a · **Core/Stretch:** core ·
**Depends on:** EP-19 (Selection and ranking) ·
**Blocks:** EP-21 (template composition, linters, CLI), EP-23 (engine integration, re-plan P2)

## Context

This is the one path that must work when everything else has failed. It runs **first** at runtime,
before the registry is read, and it runs **last**, as a consistency re-check before anything is
emitted. It is placed before composition in the roadmap for the same reason it is placed before
composition in the code.

Implements **D-38** (the five-trigger abstention taxonomy), **D-18** (hard stops are deterministic
only, never a generative classifier, with an always-visible escalation panel and the flat public
claim *this tool is not a risk detector and must not be used as one*), **D-57** (the escalation
panel renders from a constant with no dependency on registry, template or model load), and
**D-14/D-38.1** (a framework outside the declared Western-secular scope produces explicit
abstention, never improvisation). Lands **ADR-005** (abstention precedence chain).

**The rendering rule this brief encodes, which overrides WS-2's "escalation only" formulation.** A
hard stop renders its **stop card in the waypoints region and emits zero waypoints**. The escalation
panel is *not* the carrier of the stop; it is invariant and must never vary with input. A panel that
varied would become a risk signal a clinician could learn to read, which would falsify the project's
"not a risk detector" claim exactly as R-34 describes. So the engine exposes the invariance as a
property the interface can rely on rather than as a convention the interface must remember.

**Already in the tree:** EP-17's `HardStopBundle`, `Abstention`, `EscalationPanel` and
`AbstentionTrigger`; EP-18's loader; EP-19's pipeline and its typed drop reasons, including the
`out_of_declared_scope_when` signal this brief consumes.

**Not in the tree:** any prose assembly (EP-21), any UI (EP-43/EP-44), any eval thresholds (EP-30).

## Safety preconditions

- **R-5 (crisis mis-handling), D-18.** Guard: no gate in this chain is a classifier, a score, a
  probability or a heuristic. Every gate reads **declared structured fields only**. There is no
  model, no threshold and no learned component anywhere in `src/epppsynth/guard/`, asserted by the
  purity scan and by an import-graph test.
- **D-25 / the free-text rule.** The free-text field is quoted verbatim back to the reader and is
  **never tokenised, mined, or used to infer anything** — and that includes inferring danger. No
  gate in this chain reads it. Guard: a test asserts that no module under `src/epppsynth/guard/`
  references `for_quotation` or the utterance field, and `run_guard()`'s signature takes the
  structured envelope fields, not the utterance. **This narrows D-18's "keyword/structural
  checklist" to the declared fields, and the narrowing must be recorded as a dated addendum under
  D-18 in `DECISIONS.md` before this brief is closed** (step 4 below). The rationale is that a tool
  which scans free text for danger words *is* a risk detector — a bad one — and D-18's own public
  claim forbids being one.
- **R-34 (escalation panel read as a risk signal).** Guard: `render_escalation_panel()` takes no
  envelope, no bundle, no registry and no selection result; its only optional argument is the loaded
  local configuration. A signature test asserts no parameter is annotated with any input, registry
  or output type, and the panel's rendered bytes are hashed across the whole fixture corpus with the
  assertion of exactly one distinct hash.
- **R-37 (`role="alert"` flooding).** Guard: this brief emits *data*, never ARIA. The stop card
  carries a typed `announce: bool` that EP-43 maps to a single live-region announcement; nothing
  else in the bundle may set it, enforced by a type-level constraint and a test.
- **R-31 (over-abstention trains the reader to dismiss abstentions).** Guard: each trigger produces
  a distinct, specific `reason_text` naming *what* is missing or *why* the tool stopped. Generic
  "cannot help" copy is forbidden by a linter check on the constants module. Measurement of the
  over-abstention ceiling belongs to EP-30.
- **Failure of this path is a refusal, not a degradation.** Guard: if `run_guard()` raises for any
  reason, the caller renders `emergency_escalation_only()` and nothing else. Tested.
- **Public artifact.** Escalation and stop copy are public, tracked, and safety-critical. Re-run the
  EP-6 pre-publication items, and treat every wording change here as requiring the P0 safety-charter
  review named in `SAFETY.md`.

## In scope

1. Create `src/epppsynth/guard/` with `escalation.py`, `chain.py`, `triggers.py`, `outcomes.py`,
   `config.py`. `escalation.py` **imports nothing from the project** — no registry, no compose, no
   select, no llm, no contracts beyond the `EscalationPanel` dataclass — and holds its copy as
   module-level string constants.
2. **The escalation constant.** Heading: *If you are worried about someone's safety.* Body: the
   fixed D-18/D-57 statement that the tool does not detect risk, never screens, scores or flags
   anyone, that nothing typed here is checked for danger, and that these numbers are the thing to
   use. Plus the shipped, clearly-labelled US defaults (988; emergency services) and the slot for
   institution-specific numbers from `escalation.local.toml` (gitignored, with a tracked
   `.example`). Local configuration may add institution numbers; it may not alter the heading or the
   fixed statement, enforced by the config schema.
3. **`render_escalation_panel(config: EscalationConfig | None = None) -> EscalationPanel`.** The
   engine-level property, stated in the module docstring and enforced by tests: *the panel is a pure
   function of the shipped constant and the local configuration, and of nothing else — not the
   input, not the registry, not the templates, not the model, not the outcome of any gate.* Also
   `emergency_escalation_only() -> EscalationPanel`, the degraded entry point used when the registry
   or template load has failed.
4. **The chain.** `run_guard(envelope) -> GuardOutcome`, executed before any registry access. One
   module-level tuple `PRECEDENCE` fixes the order and is the only place the order exists:
   1. **Hard-stop flag** — the operator's explicit declaration in `DeclaredFlags`. Short-circuits to
      `Stop`.
   2. **Prohibited request class** — persuasion, prognosis, capacity, diagnosis, or ranking of
      options, read from the declared `RequestClass` enum and from a literal deny-list over the
      declared request fields. Short-circuits to `Refuse(reason)`.
   3. **Out-of-declared-scope framework** — the self-described framework falls outside the declared
      Western-secular scope enum. Short-circuits to `ScopeAbstain`, whose copy names the limit and
      does not improvise (D-14).
   4. **Declared disagreement or refusal** — a *modifier*, not a short circuit. Returns
      `Continue(suppress_tags=("persuasive",), require_frames=("non-pathologizing",))`, and the
      composer must honour both. No "overcoming objections" content may survive it.

   Record the D-18 narrowing addendum described in the safety preconditions as part of this step.
5. **The fifth trigger's seam.** D-38(2), insufficient basis, is not a pre-chain gate: it is
   EP-19's evidence floor, and it renders through this brief's `Abstention` construction so all five
   triggers share one type, one copy module and one set of eval hooks. Document the seam in
   `chain.py` so a later reader does not go looking for a gate that is deliberately elsewhere.
6. **Hard stop last.** `assert_hard_stop_consistency(outcome, bundle)` runs immediately before
   emission: if the hard-stop flag was set and the bundle carries any waypoint, raise and emit the
   stop bundle instead. Belt and braces on the one gate whose failure mode is unacceptable.
7. **The stop bundle.** `HardStopBundle(stop_card=…, waypoints=())` — the stop card is rendered in
   the **waypoints region** by EP-43, the waypoints tuple is typed empty so no branch can populate
   it, and the escalation panel accompanying it is byte-identical to every other response's.
8. **Degradation contract.** A documented, tested table: registry invalid → refuse to start, exit
   2, escalation still renders · templates missing or invalid → same · model unavailable →
   deterministic baseline (P4's ladder, referenced not implemented) · guard itself raising →
   `emergency_escalation_only()`.
9. Write `docs/adr/ADR-005-abstention-precedence-chain.md`, including the hard-stop rendering resolution
   and the reason the panel's invariance is an engine property rather than a UI convention.

## Out of scope

- Rendering, ARIA, focus management and the visual treatment of the stop card — **EP-43**; the
  escalation panel's markup and its single-hash assertion in the browser — **EP-44**.
- The banned-phrase lint over static UI copy — **EP-39**; this brief lints only its own constants.
- Abstention recall and precision thresholds, the over-abstention ceiling, and the red-team suite —
  **EP-30**, with thresholds ratified in D-75 and revisited at the P3 re-plan (**EP-31**).
- The LLM path's use of the same chain — **EP-36**; the chain is written here so that path can reuse
  it unchanged.
- Local escalation configuration UX and the shipped `.example` file's institution guidance —
  **EP-44**.

## Verification / acceptance

1. `uv run pytest tests/guard -q` — green, with **one named test per trigger** (hard-stop flag ·
   prohibited request class · out-of-declared-scope framework · declared disagreement/refusal ·
   insufficient basis via the EP-19 seam).
2. **Precedence test.** A single planted envelope that trips all four pre-chain gates at once yields
   exactly the hard-stop bundle; six further tests cover each ordered pair.
3. **The escalation panel renders with registry, templates and model all unavailable.**
   `uv run pytest tests/guard/test_degraded.py -q` installs an import hook that makes
   `epppsynth.registry` and `epppsynth.compose` raise `ImportError`, points the model root at an
   empty directory, and asserts `emergency_escalation_only()` returns the full panel with the
   correct heading. A second case forces `RegistryInvalid` from EP-18's loader and asserts the same.
4. **Invariance.** `uv run pytest tests/guard/test_panel_invariance.py -q` renders the panel once
   per fixture envelope across the whole fixture corpus, hashes each, and asserts **exactly one
   distinct hash**. A companion signature test asserts no parameter of `render_escalation_panel` is
   annotated with an input, registry, selection or output type.
5. **Isolation.** `uv run python -m epppsynth.tools.import_graph --module epppsynth.guard.escalation
   --forbid epppsynth.registry,epppsynth.compose,epppsynth.select,epppsynth.llm` exits 0.
6. **No free-text path.** An AST scan over `src/epppsynth/guard/` finds no reference to
   `for_quotation` or to the utterance field; a runtime test passes an envelope whose free text
   contains alarming fictional wording and asserts the guard outcome is `Continue` and the text is
   echoed verbatim, unaltered, and never matched against anything.
7. **Zero waypoints on stop.** A hard-stop fixture produces `HardStopBundle` with an empty waypoints
   tuple, and `assert_hard_stop_consistency` raises when a waypoint is injected.
8. Purity scan over `src/epppsynth/guard/` — no clock, no RNG, no float, no unsorted iteration.
9. *(judgement — owner, and re-checked by the P0 safety charter)* The escalation and stop copy read
   as help rather than as a verdict, and no trigger's `reason_text` is generic.

## Parked → final-roadmap.md

- Geolocated or region-aware escalation resources. Explicitly excluded in v1 (D-18: no geolocation);
  the local configuration file is the whole mechanism.
- An operator-editable trigger list. Hard-stop triggers are code and copy, reviewed under the safety
  charter, not configuration.
- Any statistical or model-assisted abstention. Excluded by D-18 for v1 and by the "not a risk
  detector" claim thereafter; if it is ever revisited it needs its own charter clause, not a brief.
