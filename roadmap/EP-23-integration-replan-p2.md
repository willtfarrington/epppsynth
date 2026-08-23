# EP-23 — Engine integration, fixtures, re-plan P2

**Size:** L · **Mode:** a · **Core/Stretch:** core ·
**Depends on:** EP-17 (Contracts package), EP-18 (Registry loader), EP-19 (Selection and ranking),
EP-20 (Abstention and hard-stop precedence chain), EP-21 (Template composition, linters, CLI), EP-22
(Corpus ingest module and local index) ·
**Blocks:** EP-37 (reviewer recruitment pack, re-plan P4)

## Context

Six briefs each proved their own piece. This one wires them into a single entry point, proves the
whole path is deterministic end to end, freezes the fixture library that P3 will build its suites
on, and closes the phase.

It also trips a schedule-critical switch. **D-64 defers reviewer outreach until the P2 engine runs
end to end.** The moment this brief's acceptance passes, the longest-lead item in the plan (EP-37,
and through it the D-35(2) sign-off gate) becomes startable. Recording that explicitly is part of
the re-plan, because a deferral nobody notices expiring is just a delay.

Implements the integration halves of **D-17** (the baseline is the shipped default and the permanent
fallback — here it is the *only* path, and it must be complete on its own), **D-36** (every fixture
carries a "no real person" attestation), **D-8** (the whole suite runs with no model, no index and
no network), and the phase-closing conventions in `roadmap/README.md`.

**Already in the tree:** the full P2 stack. **Not in the tree:** any evaluation scoring, any UI, any
model. Everything this brief runs is the deterministic baseline.

## Safety preconditions

- **R-30 (evidence drift).** Guard: every golden file records the version triple it was generated
  against, and CI fails if a golden is stale relative to the current triple. Evidence that does not
  name the build it came from is not evidence.
- **R-6 (public-history leakage), D-36.** Guard: every fixture envelope is manifestly fictional and
  carries a `no_real_person: true` attestation field validated by schema; a test asserts the field
  is present on all of them; the EP-6 scanners run over the fixture directory specifically.
- **R-2 / R-33 (uncertainty de-emphasised).** Guard: the integration suite asserts that every
  emitted bundle carries a non-empty unknowns list, a counter-reading on every waypoint and an
  insufficient-basis clause on every waypoint. A bundle that omits any of them is a failure, not a
  variation.
- **R-5 / R-34.** Guard: the degraded-path tests from EP-20 are re-run at integration level with
  the real loader and the real composer, not with stubs, so the escalation panel's independence is
  proven against the shipped wiring rather than against a mock.
- **D-8 (no runtime network).** Guard: the full suite runs offline. A socket guard fixture makes
  `socket.socket`, `socket.create_connection` and `ssl.SSLContext.wrap_socket` raise for the whole
  session, and the suite must stay green. The native-layer firewall audit belongs to EP-46; this is
  the Python-layer half and it is cheap to have now.
- **Public artifact — the whole phase.** Re-run the complete EP-6 pre-publication packet over
  everything P2 added: no local absolute paths, no host or user name, no corpus filenames, no
  index-root or model-root literals, no PHI-shaped strings, quotation budgets within D-74. This is
  the phase's last chance to catch a leak before P3 builds on top of it.

## In scope

1. **`src/epppsynth/engine.py`** — one public entry point,
   `run(envelope: InputEnvelope, *, mode: Mode) -> OutputBundle | Abstention | HardStopBundle`,
   wiring in the settled order: `run_guard` → registry load → select → compose →
   contract validation → `assert_hard_stop_consistency` → return. Registry and template loads happen
   **after** the guard, so a hard stop never depends on them. The version triple is assembled here,
   with `UNAVAILABLE` filled for any component whose load did not run.
2. **Fixture library** at `tests/fixtures/envelopes/`, twelve manifestly fictional envelopes with a
   short README describing the coverage: three ordinary cases yielding 3, 4 and 5 waypoints · one
   per abstention trigger (hard-stop flag, prohibited request class, out-of-declared-scope
   framework, declared disagreement or refusal, insufficient basis via the evidence floor) · one
   interpreter-need case exercising the single permitted additive note · one case where the
   family-diversity rule binds · one mode (c) case exercising the `personal-meaning` and
   `structural` pairing. Each carries the D-36 attestation.
3. **Golden bundles** at `tests/golden/`, one per fixture, generated through EP-17's export
   chokepoint, each filename and header carrying the version triple.
   `uv run pytest tests/integration --regenerate-golden` regenerates them and refuses to run on a
   dirty working tree.
4. **Determinism gates,** run as one suite:
   - 100 in-process repeats per fixture, byte-identical;
   - five subprocess runs per fixture under five different `PYTHONHASHSEED` values, one distinct
     hash each;
   - a purity scan over `contracts`, `registry`, `select`, `guard` and `compose` — no import of
     `random`, `time`, `datetime`, `uuid`, `secrets` or `os.urandom`, no float literal, no unsorted
     iteration over a `dict` or `set`;
   - a runtime assertion that every score encountered is an `int`.
5. **Counterfactual smoke** over the D-73 sensitivity classes — the full harness is EP-29's, this
   is the tripwire: flipping any `invariant` field leaves the bundle byte-identical; flipping the
   `framing-plus-one-permitted-additive-waypoint` field produces exactly the one permitted additive
   note and no other diff; flipping a `clinically-load-bearing` field is *allowed* to change
   clinical substance and the test records the diff rather than asserting on it, so a later surprise
   is visible.
6. **Failure-ladder integration tests,** with real components: invalid registry → exit 2, structured
   error list, escalation panel still renders · missing or invalid templates → same · both missing →
   same · guard raising → `emergency_escalation_only()` and nothing else. **The escalation panel
   renders with registry, templates and model all unavailable**, proven here against the shipped
   wiring.
7. **Type-graph gate at integration level:** the walk runs over `OutputBundle`, `Abstention`,
   `HardStopBundle` and `SelectionResult` together, so no field added anywhere in P2 can hold a
   span.
8. **Re-plan P2.** Tick the P2 boxes in `roadmap/README.md` with short hashes; append `>
   **Completion note (date).**` to each executed brief including deviations; record every decision
   change as a dated addendum in `DECISIONS.md` (never an edit) — including EP-20's D-18 narrowing
   if it has not already landed; mirror every `## Parked → final-roadmap.md` item from EP-17 … EP-22
   into `final-roadmap.md`; re-check sizes against actual elapsed time and adjust the P3 estimates;
   run `uv run python tools/roadmap_check.py` including the context-budget check for the P3 briefs;
   **upgrade the P3 charter briefs EP-24 … EP-30 — and EP-31, the P3 re-plan charter, with them —
   to full briefs, and re-charter P4**; confirm the Definition of Ready for EP-24; and **record that
   D-64's precondition is now met, so EP-37's reviewer outreach may open**.
9. Update the `docs/` engine overview with the wiring diagram and the degradation table, and confirm
   ADR-002 … ADR-005 and ADR-010 are all landed and consistent with what shipped.

## Out of scope

- Any evaluation harness, scenario set, taxonomy or threshold — **EP-24** … **EP-31**. This brief
  produces fixtures, not scenarios; the distinction matters because scenarios carry expected
  behaviour and fixtures do not.
- Any UI — **EP-38** … **EP-46**.
- Any model, benchmark or LLM path — **EP-32** … **EP-37**.
- The native-layer no-egress audit and the filesystem-delta harness — **EP-46**.
- Upgrading the P4 charter briefs to full briefs — **EP-31** owns that; this brief upgrades the P3
  charters only.
- Reviewer outreach itself — **EP-37**; this brief records that it may begin.

## Verification / acceptance

1. `uv run pytest -q` — the **whole** suite green with no model, no index and no network, on
   `windows-latest` in CI and locally.
2. `uv run python -m epppsynth.tools.repeat_hash --runs 100 --all-fixtures` — prints
   `100/100 identical` for each of the twelve fixtures; **100 repeated runs on the same input are
   byte-identical**.
3. `uv run epppsynth run --fixture tests/fixtures/envelopes/EN-001.yaml` — succeeds for each of the
   twelve fixtures, producing the expected bundle kind for each.
4. `uv run python -m epppsynth.tools.purity_scan src/epppsynth` — exits 0 (no clock, no RNG, no
   float, no unsorted iteration in the engine packages).
5. `uv run python -m epppsynth.contracts.typegraph OutputBundle Abstention HardStopBundle
   SelectionResult` — exits 0; **the type-graph walk finds no field capable of holding a span**.
6. `uv run pytest tests/integration/test_degraded.py -q` — the escalation panel renders with
   registry, templates and model all unavailable, against the real wiring.
7. Golden staleness check: CI fails when a golden's recorded version triple differs from the current
   one; demonstrated by bumping `CONTRACT_VERSION` in a scratch branch and observing the failure.
8. `uv run python tools/roadmap_check.py --context-budget EP-24` — passes under the ~15k token
   budget, and the hazard-to-brief coverage check is green.
9. `uv run epppsynth scan` (the scanner CLI built in EP-6) and the EP-6 pre-publication packet —
   green over everything P2 added, with the packet's checklist filled in and committed.
10. *(judgement — owner)* Reading three fixture outputs end to end, the bundles are useful, honest
    and non-directive; the phase's residual risks are listed in the re-plan; and the owner confirms
    D-64's precondition is met before EP-37 opens.

## Parked → final-roadmap.md

- A stable public fixture pack that third parties could run. Excluded by D-33 (third-party use is
  not an intended use in v1); the fixtures exist for this project's tests.
- Performance work on the baseline. It is fast enough that D-7's under-sixty-seconds criterion is
  not in question, and optimising before P3 measures anything would be premature.
- A single-command "engine report" bundling determinism, purity, type-graph and leak evidence into
  one artifact. Attractive, but the release-evidence bundle is EP-50's job and this would duplicate
  its structure.
