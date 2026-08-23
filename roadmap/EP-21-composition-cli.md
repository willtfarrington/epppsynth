# EP-21 — Template composition, linters, CLI

**Size:** L · **Mode:** a · **Core/Stretch:** core ·
**Depends on:** EP-20 (Abstention and hard-stop precedence chain) ·
**Blocks:** EP-22 (corpus ingest and local index), EP-23 (engine integration, re-plan P2), EP-24
(eval harness), EP-36 (gated LLM renderer), EP-39 (UI contract and copy deck), EP-43 (waypoints
panel)

## Context

Selection produces concept IDs and integers. This brief turns them into the three-part output
contract, and it is where the project's central linguistic rule becomes machine-enforced: **every
suggested utterance must parse as a question or an offer, never an assertion about what the patient
feels or should do** (D-26b), checked at authoring *and* at runtime, failing closed.

Implements **D-11** (the three-part output contract), **D-26** (all four preserved functions),
**D-53** (`counter_reading` and `insufficient_basis_clause` structurally required), **D-50**
(`templates/**` is CC BY 4.0 — their value is the wording), **D-58**'s data-side precondition
(uncertainty and abstention are ordinary content, not decorated exceptions), and the composition
half of **D-73** (the one permitted additive waypoint). It also lands the CLI that D-21 requires.

Templates are **data with a restricted slot grammar**, not code and not a general template engine.
Slots fill only from registry fields, from guard constants, or from the verbatim echo of the
reader's own words. There is no free-form concatenation, no expression syntax, and no dependency on
Jinja or on the UI stack — the engine composes plain text structures that EP-43 later renders.

**Already in the tree:** EP-17's contracts, EP-18's loader and `question_intent` enumeration,
EP-19's `SelectionResult`, EP-20's guard chain, outcomes and escalation constants.

**Not in the tree:** any HTML, any web framework, any copy deck for chrome (EP-39), any LLM path
(EP-36). This brief's output is a fully populated `OutputBundle`, `Abstention` or `HardStopBundle`.

## Safety preconditions

- **R-1 (coercion architecture), D-26(b).** Guard: the question-or-offer linter, run twice. At
  authoring, `epppsynth templates lint` walks every template and every registry `question_template`
  and fails on anything that is neither interrogative nor an offer. At runtime, the same predicate
  runs over each composed utterance before it enters the bundle. Failing closed means the utterance
  is dropped; if that leaves a waypoint without its required question the waypoint is dropped; if
  that drops the bundle below cardinality three, the bundle becomes an insufficient-basis
  abstention. The offending string is never rendered and never logged.
- **R-1 / D-26(c) (no ranking, no advocacy).** Guard: a ranking-language deny-list applied to
  **every composed part** — no "recommends", "best", "preferred", "most appropriate", no ordering
  language. Zero hits required. The prohibition is unconditional and does not depend on any part of
  the contract naming options: the tool never ranks, compares, orders or advocates among clinical
  options, and it now says nothing about options at all.
  **Note for a later session: the deny-list's former companion, an option-completeness check, is
  gone with the part it guarded and must not be reinstated.** An earlier draft of the contract
  carried a fourth part — neutral framing connecting stated values to clinician-verified options —
  whose completeness half ("no omission of an option the clinician entered") presupposed a ninth,
  optional input that the input contract never had, and whose content source, the registry's
  `framing` records, no brief ever authored. The owner **deleted part (iv)** rather than add the
  ninth input and leave the part shipping empty. Only the deny-list survives, and it survives because
  it is load bearing for parts (ii) and (iii), not because part (iv) once existed.
- **R-2 (automation bias), D-58.** Guard: the composer emits no headline, no summary, no lead
  sentence, no "top waypoint" and no confidence expression of any kind. Uncertainty,
  counter-hypotheses, insufficient-basis clauses and abstentions are ordinary fields of the same
  shape as everything else; a test asserts the abstention partial and the hypotheses partial are
  mutually exclusive, so no branch can render a hedged hypothesis alongside an abstention.
- **R-16 (mode (c) inversion into individual pathology), D-20.** Guard: the composer rule that any
  bundle containing a `personal-meaning` locus concept must also contain a `structural` one is
  implemented here and active in mode (c); the mode profile that switches it on is EP-48's.
- **D-25 / the free-text rule.** The echo slot is the **only** consumer of
  `UserUtterance.for_quotation()`. Guard: an AST scan asserts exactly one call site in the whole
  package, and a test asserts the echoed text is byte-identical to the input, never trimmed,
  normalised, case-folded or truncated in the bundle.
- **R-27 (prompt injection).** Guard: the settled control is output-side and structural. Every
  bundle validates against the contract types, every citation resolves to a live registry ID, and
  every suggested utterance parses as a question or an offer. Text arriving through the free-text
  field can only ever reach the echo slot, where it is data.
- **Public artifact.** `templates/**` is tracked, public and CC BY 4.0 (D-50) with REUSE annotations
  in `REUSE.toml`. Re-run the EP-6 pre-publication items; quotation budgets under D-74 apply to any
  template that carries a citation.

## In scope

1. Create `src/epppsynth/compose/` with `slots.py`, `loader.py`, `assemble.py`, `linters.py`,
   `hashing.py`, and `templates/` at the workspace root holding the authored YAML.
2. **Template format and slot grammar.** Each template is a YAML record with an ID, a
   `question_intent` or part designation, and a body containing slots of the single form
   `{{namespace.field}}`. The closed slot registry in `slots.py` enumerates every legal slot and its
   source: `concept.*` (label, prose, counter_reading, insufficient_basis_clause, citations),
   `echo.utterance`, `guard.*` (the scope-limit and non-pathologizing constants), `input.*` (the
   declared enum labels only). The loader rejects an unknown slot, a nested slot, whitespace inside
   a slot, any filter or expression syntax, and any slot appearing in a part that may not use it.
   Rendering is literal substitution; there is no evaluation step and therefore no injection
   surface.
3. **`template_version`.** SHA-256 over the canonicalised template set, computed by the same
   canonicalisation rules EP-18 wrote for the registry, and stamped into every bundle as the third
   member of the version triple.
4. **Three-part assembly, in the fixed order that puts uncertainty first:** (i) known facts and
   unknowns — two headed lists, and the unknowns list is never empty; if the engine has no unknowns
   the correct behaviour is to abstain, not to print "none"; (ii) plural concerns — two or more
   hypotheses as siblings of equal weight, each carrying its nested counter-reading and its own
   insufficient-basis clause, never a global footer disclaimer, never ordered by confidence;
   (iii) disconfirming, permission-based questions, ordered by the registry's `question_intent`
   enumeration so the order is authored rather than incidental.
5. **Required-field enforcement at composition.** EP-17 makes `counter_reading` and
   `insufficient_basis_clause` structurally required; this brief additionally refuses to emit if
   either resolves to an empty or whitespace-only string, raising `CompositionRefused`.
6. **The linters** in `linters.py`, one predicate each, all pure and all reused by CI, by the
   runtime path and later by EP-24's harness:
   - `is_question_or_offer(text)` — true if the utterance ends with `?` after stripping trailing
     whitespace and closing punctuation, or begins with a stem from the closed list in
     `compose/offer_stems.yaml`. Nothing else passes.
   - `has_ranking_language(text)` — the ranking and advocacy deny-list, applied to every composed
     part.
   - `has_banned_phrase(text)` — the generated-output half of the banlist (assertions about what the
     patient is, feels or wants; "risk", "flagged", "screening", "non-compliant", "in denial",
     "overcoming objections", "buy-in", and the rest). The chrome and copy-deck half is EP-39's.
   - `is_generic_abstention(text)` — refuses copy that says only that the tool cannot help (R-31).
7. **Guard integration.** `compose()` consumes EP-20's `GuardOutcome`: `Continue`'s
   `suppress_tags` removes every concept carrying the tag before assembly, and its `require_frames`
   forces the non-pathologizing frame into part (ii). `Stop`, `Refuse` and `ScopeAbstain` skip
   assembly entirely and produce the corresponding bundle. `assert_hard_stop_consistency` runs last.
8. **The interpreter-need additive note.** When the language/interpreter field is declared, the
   bundle prepends the fixed note that the concept prose was authored in English within a
   Western-secular frame and that phrasing may not survive interpretation. This is the single
   permitted additive output under D-73's `framing-plus-one-permitted-additive-waypoint` class, and
   a test asserts it is the only difference the field can produce.
9. **CLI** in `src/epppsynth/cli.py`, argparse-based, no third-party CLI dependency: `epppsynth run
   --fixture PATH [--mode a] [--emit-bundle]` · `epppsynth registry validate` (registered by EP-18)
   · `epppsynth templates lint` · `epppsynth corpus ingest` (registered by EP-22). `run` prints a
   human-readable render to stdout. `--emit-bundle` prints the canonical JSON through EP-17's
   chokepoint and is documented as a developer and evaluation affordance consumed by EP-24, **not**
   a reader-facing export; D-6's no-export rule is unaffected and `PRIVACY.md` says so.
10. **Stack isolation.** An import-graph test asserts that nothing under `src/epppsynth/compose/`
    imports `jinja2`, `starlette` or any web dependency. The engine must remain usable, and
    testable, with the UI absent.
11. REUSE annotations for `templates/**` as CC BY 4.0 (D-50), and an addendum to ADR-003 recording
    the slot grammar and the twice-run linter.

## Out of scope

- HTML, CSS, ARIA, focus management and the waypoints panel — **EP-43**; the copy deck and the
  banned-phrase lint over static chrome — **EP-39**.
- The LLM renderer, claim binding and the drop-threshold fallback — **EP-36**, which reuses this
  brief's validators unchanged.
- Evaluation scoring, the substance-tuple extractor and thresholds — **EP-24**, **EP-28**,
  **EP-31**.
- Mode (b) and mode (c) profiles — **EP-47**, **EP-48**; the mode (c) composer rule is implemented
  here but wired to a profile there.
- The provenance drawer's presentation of citations and contested interpretations — **EP-45**.

## Verification / acceptance

1. `uv run epppsynth templates lint` — exits 0 on the tracked template set and on every registry
   `question_template`.
2. **A planted assertion-shaped utterance fails the linter.** With
   `"The patient is frightened of dying."` inserted into a copy of the template set,
   `uv run epppsynth templates lint --path tests/fixtures/templates-bad/` exits non-zero naming the
   template ID. The runtime half is tested separately: a fixture registry whose question resolves to
   the same string produces an insufficient-basis abstention, and a grep assertion in the test
   confirms the offending string appears nowhere in stdout, stderr or the bundle.
3. `uv run epppsynth run --fixture tests/fixtures/envelopes/EN-001.yaml` — produces a complete
   three-part bundle; repeated for three fictional fixtures covering 3, 4 and 5 waypoints.
4. `uv run pytest tests/compose -q` — green, including: mutual exclusion of the abstention and
   hypotheses partials · unknowns list never empty · zero ranking deny-list hits anywhere in the
   composed bundle · every
   composed utterance passes `is_question_or_offer` · exactly one call site for `for_quotation` ·
   verbatim echo byte-identical to input · the interpreter-need note is the sole diff that field
   produces · a `personal-meaning` concept in mode (c) forces a `structural` companion.
5. Slot-grammar tests: unknown slot, nested slot, expression syntax and a part-illegal slot each
   fail at template load with a message naming the template and the slot.
6. `template_version` stability: reordering template files and keys leaves the hash unchanged;
   changing one character of body text changes it.
7. Determinism carried forward: `uv run python -m epppsynth.tools.repeat_hash --runs 100 --fixture
   tests/fixtures/envelopes/EN-001.yaml` prints `100/100 identical` over the *composed* bundle.
8. Import-graph test for the web-dependency ban exits 0; `uv run reuse lint` exits 0 with the new
   `templates/**` annotations.
9. *(judgement — owner)* The rendered bundle reads as the D-11 contract and not as advice; the offer
   stem list is neither so narrow that natural phrasing fails nor so broad that assertions slip
   through.

## Parked → final-roadmap.md

- A richer template language (conditionals, pluralisation, locale rules). Deliberately excluded: the
  restricted grammar is the injection control.
- Author-facing template preview tooling.
- A copy-to-clipboard or print affordance. Excluded in v1 by D-6 and by the deliberate absence of a
  skimmable surface; if revisited it needs a human-factors finding, not a feature request.
