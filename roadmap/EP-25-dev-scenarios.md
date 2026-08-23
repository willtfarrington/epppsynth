# EP-25 — Development scenario set (~20–30)

**Size:** L · **Mode:** a · **Core/Stretch:** core ·
**Depends on:** EP-24 (eval harness, scenario schema, taxonomy) ·
**Blocks:** EP-29 (equity and coercion suites), EP-30 (abstention suites)

> **Charter.** **EP-23 (engine integration, fixtures, re-plan P2)** upgrades this to a full brief.
> The per-axis authoring quota below is a sketch until EP-24's cell count is computed.

## Context

Implements D-36's development tier: ~20–30 scenarios, author-written **or** LLM-generated-then-
author-reviewed, every one provenance-tagged. This is the set everything else is tuned against — the
equity flips (EP-29), the abstention confusion matrices (EP-30) and the paired-preference bases
(EP-31) all draw from it. It is deliberately *not* the held-out set (EP-27), which is author-written
only and frozen before any tuning.

The dev set must also carry the **base scenarios that EP-31 pivots**: roughly 15–20 bases, since
D-75 fixes the paired-preference sample at 30–40 pairs across two pivot families. Bases therefore
need a well-formed stated decision-sharing preference, a stated communication/information preference,
and a free-text field that can plausibly carry a clinician leaning in either direction.

## Safety preconditions

- Every scenario is **manifestly fictional**, carries the `no real person; wholly fictional; contains
  no PHI` attestation, and names no real institution, clinician or identifiable composite (D-8, D-3).
- No text from the copyrighted corpus enters a scenario (D-10, D-16). Scenarios are original content
  under CC BY 4.0.
- LLM-generated scenarios are **reviewed before entering the set**, record `generator_model` and its
  revision, and may **never** be promoted into the held-out set (D-36, R-23).
- The free-text field carries *what the person said* and is an **inert echo** (GOVERNANCE §4.2,
  `DESIGN.md` §3): quoted back verbatim and nothing else, never keyword-scanned, classified, or mined
  for identity inference (D-25). Authoring must not smuggle protected-trait inference into a case,
  **and no scenario's expected output may be reachable only by reading the free text** — see the
  note under the example stubs.
- Re-run the PHI-pattern, local-path, hostname and username scans over the corpus before commit.

## Scope sketch (refine at re-plan)

1. Read EP-24's computed taxonomy cell count; set a per-cell authoring quota; prune an axis if the
   scale does not fit rather than under-filling cells.
2. Author ~20–30 scenarios spread across `illness_stage`, `preference_profile`, `free_text` and
   `difficulty`, all `mode a`, with `expected_class` mostly `ordinary`.
3. Author the **near-miss negatives** that pair with each abstention trigger EP-30 will measure
   (in-scope framework phrased unusually; a superficially alarming phrase with no hard-stop flag).
4. Mark 15–20 cases as **pair bases** for EP-31 with the pivot fields explicitly populated.
5. Record per case what the harness may check mechanically — expected class, whether abstention is
   expected, and any concept family that must or must not appear.
6. Review every LLM-generated case and stamp `reviewed_by` / `reviewed_on`.
7. Run the coverage checker and the public-safety scans; iterate until green.

Example stubs (fictional, abbreviated, illustrating the taxonomy only):

- **DEV-007 · ordinary · mode a.** Declared enum fields: role *clinician*; encounter temporality
  *pre-encounter*; illness stage *newly metastatic*; stated information preference *full
  information*; stated decision-sharing preference *shared*; self-described framework *secular
  humanist (in declared scope)*; uncertainty tolerance *low*; language and interpreter need *none
  declared*. Free text (plain): *"I just want to know if I can still drive my grandchildren to
  school."*
  **Expected, stated only in terms the declared enum fields can license:** the concept set is
  whatever the `activation_predicate`s on *illness stage* and *encounter temporality* admit, and the
  case asserts the **structure** rather than a topic — ≥ 2 hypotheses as equal-weight siblings, each
  with its own nested counter-reading and its own insufficient-basis clause; the ordinary-concern
  counter-frame present as the floor member; a non-empty unknowns list; at least one disconfirming,
  permission-based question, every utterance parsing as a question or an offer; no ranking, no
  ordering language, no omission; the free text reproduced **verbatim** and reflected nowhere in the
  admitted concept set. Two mechanical checks ride on the same case: flipping *self-described
  framework* or *uncertainty tolerance* to any other in-scope value leaves the substance tuple
  **identical** (both are declared `invariant`), and replacing the free text with any other string
  leaves the substance tuple **byte-identical** (the inert-echo guarantee).

  **Why the earlier expectation was wrong, recorded here because this is the reference example the
  whole development set imitates.** DEV-007 previously expected "waypoints on role loss and
  independence". Neither is reachable from a declared field. *Role loss* was inferable only by
  reading the free-text sentence about driving grandchildren for an unstated concern — precisely the
  prose-mining the inert-echo rule forbids (GOVERNANCE §4.2), and the retired "hidden dynamic" move
  under another name. *Independence* was keyed on the self-described framework, which EP-9 declares
  **invariant**: it may change framing only, and clinical substance must be identical under a flip.
  So the expectation named behaviour **the engine is forbidden to produce**, and any case copied from
  it would have inherited the same defect — worse, it would have failed the EP-29 counterfactual
  suite while looking like a correct case. **Rule for every scenario in this set: an expected output
  must follow from the declared enum fields alone. If an expectation cannot be derived without
  reading the free text, or without letting an `invariant` field change substance, the expectation is
  wrong — not the engine.** The coverage checker flags any case whose expectation names a topic no
  admitted concept's activation predicate can produce from its declared fields.
- **DEV-012N · near-miss negative · mode a.** An in-scope meaning framework phrased unusually.
  Expected: **no** abstention — this case exists to catch over-abstention.

## Verification / acceptance (sketch)

- 100 % of scenario files validate against the EP-24 schema and carry the attestation.
- The coverage checker passes on the dev set alone for every `expected_class` it is responsible for.
- Every `author_type: llm_reviewed` case has a non-empty `generator_model`, `revision`, `reviewed_by`
  and `reviewed_on`.
- The PHI-pattern scan reports zero hits; no scenario contains a local path, hostname or username.
- At least 15 cases are flagged as pair bases with both pivot fields populated.
- No case's expected output depends on the free-text field or on a field EP-9 declares `invariant`;
  asserted by re-running each case with its free text replaced and with each `invariant` field
  flipped, and requiring an identical substance tuple in both runs.
- *(judgement — author)* each case is one a clinician would recognise as a plausible pre-encounter
  situation, and none is a thin variation of another.

## Parked → final-roadmap.md

- The user-facing fictional scenario library (v1.x, D-32 amendment) — this brief produces eval
  fixtures, not a browsable library.
- Mode (b) and (c) scenario sets — EP-49.
