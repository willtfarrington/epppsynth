# EP-11 — Composer specification

**Size:** L · **Mode:** a (specified for b and c) · **Core/Stretch:** core ·
**Depends on:** EP-9 (Registry schema v0) ·
**Blocks:** EP-12 (seed content A), EP-16 (registry validator, re-plan P1), EP-17 (contracts
package)

## Context

This brief writes the **emission contract** — the specification the deterministic engine implements
in P2 and the contract the seed content is authored against. It is written *before* any content
(EP-12 depends on it) so the content is authored knowing exactly what the composer will do to it,
in particular that **every emitted concept arrives with a counter-reading and an insufficient-basis
clause** (**D-53**).

It implements **D-53** (a waypoint is a *render*, never a stored object), **D-11** and **D-26** (the
output contract and the four preserved functions), **D-38** (the five-trigger abstention taxonomy),
**D-18** (deterministic hard stops only), **D-20 / R-16** (mode (c): a `personal-meaning` concept
never appears without a `structural` one), **D-57** (the escalation panel renders byte-identically on
every response), and **D-58** (uniform typography inside the waypoints region).

**The settled merge this brief encodes.** Ranking is **integer-scored with a lexicographic tie-break
on concept ID** — no floats, so ties are exact and output is bit-reproducible; **at most one concept
per `family`** appears in the top-k, which is the mechanism that makes the hypotheses plural across
genuinely different dimensions instead of four restatements of one; and every emitted question
carries a value from the **closed `question_intent` enumeration**, without which the P3 substance
comparator has nothing to compare.

**One conflict this brief resolves.** The source design's charter draft said that on a hard stop the
tool emits "escalation copy and nothing else". That is incompatible with D-57 / R-34: a panel that
appears only sometimes *is* a risk signal, which is exactly the failure R-34 names. **D-57 governs.**
A hard stop renders a stop card **in the waypoints region** and zero waypoints; the escalation panel
is byte-identical on every response, hard stop or not. Both intents survive. Record the resolution as
a dated addendum under D-18 in `DECISIONS.md`, and note that the charter clause wording in `SAFETY.md`
(EP-3) needs the same correction — raise it as a `> **EP-11 pickup note.**` on EP-3 if EP-3 has
already landed.

**What exists at pickup.** The registry schema, `families.yaml`, `input_fields.yaml`, the closed
`question_intent` enum, and `schema_check` (EP-9). The provenance and rights spec and the authoring
guide (EP-10). **No engine code, no templates, no concept content, no eval harness.**

This brief writes a **specification plus machine-checkable traces**. It writes no selection code.

Commands run from the workspace directory `epppsynth/` unless a step says "from the git root".

## Safety preconditions

- **R-11 / R-2 (reification, automation bias) — the reason this brief exists before content.**
  `counter_reading` and `insufficient_basis_clause` are **structurally required fields of every
  composed waypoint** (D-53). The spec states them as required, the trace schema marks them
  `required`, and the trace checker fails a trace missing either. No concept is ever emitted alone.
  A composer that could emit a bare concept would make D-11, D-26(a) and R-2 matters of prompt
  discipline; here they are matters of type.
- **R-34 / D-57 (escalation panel read as a risk signal).** The spec states as an invariant that the
  escalation panel is rendered from a constant with no dependency on registry, template or model
  load, and is byte-identical on every response including abstentions and hard stops. The spec must
  not contain any rule that varies it. EP-44 and EP-46 verify the single-hash assertion.
- **R-16 / D-20 (mode (c) inversion into individual pathology).** The `locus` rule is specified as a
  deterministic, testable composer step (step 6), not as tone guidance: an output set containing a
  `personal-meaning` concept and no `structural` one is **not a permitted output**.
- **R-17 / Y-6 (anchoring).** Every emitted utterance is a **question or an offer**, never an
  assertion about what a person feels or should do (D-26b). The spec requires the `form` field on the
  chosen template and states the runtime grammar check; the anchoring risk itself is untested and the
  spec says so, pointing at the human-factors probe (EP-51).
- **Determinism (D-17, D-56).** The specified algorithm has **no clock, no RNG, no float, no set
  iteration order, no dictionary insertion-order dependence**. Every ordering is explicit. "Deterministic"
  attaches to this baseline only; the spec must never describe the LLM path as deterministic.
- **No scores stored, no scores shown.** Ranking integers are computed at request time from schema
  fields and are never written back to a concept (EP-9 deny-list) and never rendered to the user. No
  confidence number reaches the waypoints region (D-48, D-58).
- **Public-safety (D-3, R-6).** The worked traces are public. Their inputs must be **manifestly
  fictional**, carry the "no real person" attestation, and contain no PHI pattern, no real-sounding
  identifier, no local path, no machine name, no account name. Their concept prose is placeholder
  text in the reserved 9000 ID band, not real content. Re-run the EP-6 pre-publication packet.
- **Not a clinical artifact and not a risk detector.** The spec's front matter says so, and the
  hard-stop section repeats the flat public claim from D-18.

## In scope

1. **Document.** Write `docs/composer-spec.md`, the canonical prose specification. It is what EP-17,
   EP-19, EP-20, EP-21 and EP-28 read. Structure: invariants → input → pipeline → output type →
   abstention chain → mode profiles → substance tuple → worked traces → open questions.

2. **Invariants, stated first and numbered** so implementation briefs can cite them:
   `CI-1` in every non-abstaining output, **each hypothesis carries its own counter-reading and its
   own insufficient-basis clause** — exactly one of each *per hypothesis*, never one per output set
   and never a global footer disclaimer (`DESIGN.md` §4; EP-21, EP-39, EP-43) ·
   `CI-2` every emitted utterance is a question or an offer ·
   `CI-3` at most one concept per `family` among the hypothesis-bearing waypoints ·
   `CI-4` output is byte-identical across repeated runs on identical input ·
   `CI-5` the escalation panel is byte-identical on every response ·
   `CI-6` no ordinal, score, count or confidence value reaches the waypoints region ·
   `CI-7` exactly one abstention record is emitted when the chain fires, and no concept content
   accompanies it · `CI-8` an output set containing a `locus: personal-meaning` concept also contains
   a `locus: structural` one · `CI-9` every rendered element resolves to a concept ID and a source; an
   untraceable element is a defect (explainability, D-32/D-45).

   **Why the contract has three parts and not four.** An earlier draft carried a fourth part —
   neutral framing connecting stated values to clinician-verified options — together with a
   provisional `CI-10` option-completeness invariant conditional on a ninth, optional input. No input
   field carried those options, no brief authored the `framing` records the part would have drawn on,
   and no brief owned it, so it would have shipped permanently empty and would have made
   `option_ref_set` a constant, silently weakening both the counterfactual-equity suite and the P3
   stop criterion. The owner **deleted part (iv) and `CI-10`** rather than leave them undeliverable or
   add a ninth input plus a completeness invariant to prop them up. Do not restore either. The
   no-ranking prohibition is unaffected: the tool never ranks, compares, orders or advocates among
   clinical options — it now says nothing about options at all, and D-26(c) remains load bearing for
   parts (ii) and (iii).

3. **Input.** The composer's input is the D-25 tuple: the eight structured enum fields plus the one
   optional free-text field, each with `unknown` / `not-relevant` / `prefer-not-to-answer` available,
   plus the declared hard-stop flags and the mode. Specify the **normalisation** applied before
   selection (case, whitespace, canonical enum spelling) so `CI-4` holds. Specify that the free-text
   field is an **inert echo** (GOVERNANCE §4.2, `DESIGN.md` §3): it is quoted back to the reader
   verbatim and nothing else. It is not normalised, not tokenised, not keyword-scanned, not
   classified, and never mined for identity inference; it enters no predicate, no filter and no
   score, so it cannot change which concepts are emitted (D-25, charter anti-essentialism). The
   spec states this as a structural property, and step 9's checker treats any trace in which the
   free text influences a stage as a defect.

4. **Pipeline.** Specify five stages, each with its own subsection, pseudocode, and a statement of
   what makes it deterministic.

   **(a) select** — a concept is selected if every key in its `activation_predicate` is satisfied by
   the input tuple. A predicate value of `any` matches any value **except** `prefer-not-to-answer`,
   which never satisfies a predicate (it is a declined answer, not a wildcard). Only
   `review_status: accepted` concepts are selectable; `draft`, `lens-review`, `blocked` and
   `deprecated` are never selectable. `mode_scope` must contain the active mode.

   **(b) filter** — drop, in this order, any concept where: a `contraindicated_when` predicate
   matches; a `constrained_by` `caution` is active; the concept type is non-emittable (`principle`,
   `caution`). If an `out_of_declared_scope_when` predicate matches, do **not** drop-and-continue —
   raise the scope abstention (step 5, trigger .1) for the whole request.

   **(c) rank — one integer, total order, reproducible.** Compute a **single non-negative integer**
   per surviving concept and sort on `(-score, concept_id)`. One integer with a lexicographic
   tie-break, rather than a tuple of ordered keys, is the settled shape: the merge says
   *integer-scored with a lexicographic tie-break on concept ID*, so evidence grade and confidence
   survive **inside** the integer rather than as extra sort keys.

   ```
   facet_certainty(f) = 2 if the input declared a value for f
                        0 for unknown / not-relevant / prefer-not-to-answer
   clause_weight(f, kind) = 1..3, from the composer's frozen SCORING table, keyed by
                            (input field, predicate kind) — NEVER stored on a concept
   confidence_ordinal = {low: 1, moderate: 2, high: 3}[concept.confidence]
   evidence_bonus     = {A: 3, B: 2, C: 1, absent/not-applicable: 0}[concept.evidence.evidence_grade]

   score(c) = ( Σ over matched clauses of clause_weight × facet_certainty ) × confidence_ordinal
              + evidence_bonus
   sort key = (-score, concept_id)          # concept_id ascending, byte-wise
   ```

   Every term is a small non-negative `int`; the spec requires the implementation to assert the
   result is an `int`. **No floats appear anywhere in the pipeline.** Because EP-9 fixes IDs at
   `EPS.<TYPE3>.<NNNN>` with zero padding, byte-wise ascending order equals numeric order within a
   type, so the tie-break is exact and stable.

   **Where the constants live, and why it matters.** `clause_weight`, `confidence_ordinal`,
   `evidence_bonus` and the evidence floor are entries in a **single frozen module-level table**
   owned by the composer, each with a written rationale. **None of them is a concept field.** The
   non-negotiable is that no concept may carry an ordinal, severity, score or count field, and EP-9's
   deny-list regex enforces it — a per-clause weight authored *onto a concept* would violate that
   rule, so the weight is keyed by `(input field, predicate kind)` in the table instead. Note for the
   P2 pickup: **EP-19 currently describes `clause_weight` as authored per activation clause; that is
   the one place EP-19 diverges from this spec, and this spec governs.** Raise it as an
   `> **EP-11 pickup note.**` on EP-19 and reconcile there, not by relaxing EP-9's deny-list.

   **(d) diversify and cap** — walk the ranked list in order, admitting a concept only if its
   `family` is not already represented, until the cap. Within a family the winner is the best sort
   key; families are then ordered by their winner's sort key. **Cap = 5** hypothesis-bearing
   waypoints (D-7's 3–5). Specify the family rule as an invariant with a rationale: without it, four
   concepts from one family look like four hypotheses and are one.

   **Three independent conditions convert the whole result to insufficient basis** (trigger .2), each
   with its constant and rationale in the `SCORING` table, and none of them ever produces a partial
   bundle or padding: fewer than **3** concepts survive; the sum of the admitted scores is below
   `SCORING.floor`; or the count of input facets answered `unknown` / `not-relevant` /
   `prefer-not-to-answer` exceeds the count of declared facets. Changing any constant requires
   regenerating the worked traces in the same commit.

   **(e) compose** — for each admitted concept build a waypoint **render** with exactly these fields:

   ```
   observation_frame        what in the supplied input this attaches to
   candidate_reading        the concept, hedged
   counter_reading          REQUIRED — from counter_hypothesis_of, resolved deterministically
   insufficient_basis_clause  REQUIRED, exactly one per hypothesis (never set-level)
   question                 from `invites`; carries `form` and `question_intent`
   citations[]              concept_id + source_id, surfaced in the provenance drawer only
   ```

   Specify `counter_reading` resolution deterministically: from the concept's
   `counter_hypothesis_of` list, take the partner with the best `(-score, concept_id)` sort key among
   those passing the same filters and **not already admitted to the output set**; if every partner is
   already admitted, use the best-sort-key partner and mark the render
   `counter_reading_shared: true` so EP-43 can render it once without losing the pairing. **If no
   partner passes the filters at all, fill `counter_reading` from a module constant stating that no
   counter-reading in the registry clears the floor for this input** — the field is never empty and
   never omitted, which is what makes `CI-1` a type-level guarantee rather than a content-coverage
   bet. The insufficient-basis clause is emitted **once per hypothesis**, nested inside the
   hypothesis it qualifies — never once per output set and never as a global footer disclaimer
   (`DESIGN.md` §4; EP-21, EP-39, EP-43). A hypothesis carrying no clause of its own is the defect;
   the clause recurring across hypotheses is correct, because a disclaimer the reader passes once at
   the foot of the page qualifies nothing.

   **The ordinary-concern counter-frame** (EP-12's permanent entry) is appended as a **mandatory floor
   member** after diversification, occupies its own family, and does not consume a cap slot. Its
   purpose is failure mode Y-5 (category exhaustion): the space is never presented as covered by the
   existential categories.

   **The interpreter note** — when `language_interpreter_need` is declared, prepend the fixed
   interpreter note as **one additive waypoint** (D-73's
   `framing-plus-one-permitted-additive-waypoint` case). It adds; it never substitutes and never
   removes a concept, and it does not consume a cap slot. Specify it as the *only* additive waypoint
   any input field may cause.

5. **Abstention and hard-stop precedence chain (D-38, D-18).** Specify a **first-match-wins ordered
   chain**, evaluated before selection. **The order below is EP-20's `PRECEDENCE` tuple and
   `DESIGN.md` §5; where this spec and EP-20 disagree, EP-20 governs and this spec is wrong.**
   Triggers 0–2 are short circuits, each emitting exactly one record (`CI-7`); trigger 3 is a
   **modifier** that does not short-circuit:

   | Order | Trigger | D-38 ref | Behaviour |
   |---|---|---|---|
   | 0 | any declared hard-stop flag or a declared-field checklist match | D-38.3, D-18 | short circuit: stop card in the **waypoints region**, zero waypoints, escalation panel unchanged (D-57; the settled hard-stop rendering resolution) |
   | 1 | the request asks for persuasion, prognosis, capacity, diagnosis, or ranking of options | D-38.4 | short circuit: prohibited-request abstention |
   | 2 | `self_described_framework == outside-declared-scope` | D-38.1 | short circuit: scope abstention naming the limit; no concept content, no analogy, no generic humanistic substitute |
   | 3 | declared disagreement or refusal | D-38.5 | **modifier, not abstention**: composition continues under `suppress_tags=("persuasive",)` and `require_frames=("non-pathologizing",)`, both honoured by the composer (EP-20 step 4.4). Persuasive-tagged content is suppressed and a non-pathologizing frame is emitted; no content aimed at reopening the topic survives |
   | 4 | insufficient basis in the supplied context, **including** fewer than 3 concepts surviving stage (d) | D-38.2 | whole-bundle insufficient-basis abstention (EP-19's evidence floor, rendered through the same `Abstention` type) |

   State the ordering rationale: 0 is safety and pre-empts everything; 1 and 2 are categorical
   properties of the request; 3 is a property of the recorded context and only *modifies* what is
   composed; 4 is the residual.

   **Why trigger 3 is a modifier and not an abstention.** An earlier draft of this brief treated
   declared disagreement as an abstention emitting no concept content. That reading is wrong and is
   corrected here: it would mean the tool **withdraws entirely from a person who pushes back**,
   which is the opposite of the intent. GOVERNANCE §4.4 requires that disagreement is not
   pathologized, not that it is met with silence, and the required behaviour is a non-pathologizing
   frame with persuasive content suppressed (`DESIGN.md` §5, EP-20). `CI-7`'s "exactly one
   abstention record, with no concept content accompanying it" therefore governs triggers 0–2 and 4,
   and never trigger 3.

   Specify that the hard-stop checklist is **deterministic — explicit declared flags plus a fixed
   checklist over declared structured fields only — never a generative classifier** (D-18 as
   narrowed by EP-20), and that the tool is not a risk detector and must not be used as one. **No
   gate in the chain reads the free-text field**: a tool that scans prose for danger words is a risk
   detector, and an unreliable one, which is worse than none because it invites reliance
   (GOVERNANCE §4.5, EP-20).

   Specify that trigger 1 fires from a **literal enum value on the framework field**, so scope is
   data the input contract carries, not a judgement the engine makes (D-14, D-38.1). This is what
   makes the abstention testable rather than aspirational.

6. **Mode profiles.** One subsection per mode, specifying only the *composer* differences:
   - **(a)** the default; `mode_scope` must contain `a`.
   - **(b)** identical selection; the trainee framing is a template concern (EP-47), not a composer
     one. Specify that **no logging path exists in mode (b)** (D-19, D-52) as a composer-level
     statement so EP-21 cannot add one.
   - **(c)** the `locus` rule (`CI-8`), specified as a deterministic post-step: if the admitted set
     contains a `locus: personal-meaning` concept and no `locus: structural` one, promote the
     highest-ranked eligible `structural` concept into the set, displacing the **lowest-ranked**
     `personal-meaning` concept if the set is at cap; if no eligible `structural` concept exists, the
     whole emission is replaced by the insufficient-basis abstention. Specify explicitly that mode
     (c) performs **no screening, no scoring and no diagnosis**, and that the composer has no field
     through which a distress measure could be expressed.

7. **The substance tuple, specified here so EP-28 can implement it.** Define the normalised
   comparison tuple `(concept_id_set, question_intent_multiset, abstention_flags)`:
   - `concept_id_set` — a sorted set of admitted concept IDs; the floor member and the interpreter
     note are included and flagged, because their presence or absence is substance;
   - `question_intent_multiset` — the multiset of `question_intent` values across emitted questions,
     **order normalised away** (D-26(c) forbids ranking, so order carries no meaning by construction);
   - `abstention_flags` — the abstention trigger, or empty.

   Specify the canonical serialization (sorted, LF, UTF-8, JSON with sorted keys) and its hash, so a
   pair comparison is a string equality and the P3 stop criterion is not re-litigating what "same"
   means at run time.

8. **Worked traces.** Ship `docs/composer-traces/` with **at least six** machine-checkable traces
   using placeholder concepts in the reserved 9000 band and manifestly fictional inputs:
   (i) a normal mode-(a) emission at cap 5; (ii) a two-survivor case falling to insufficient basis;
   (iii) a scope abstention; (iv) a hard stop showing the stop card in the waypoints region and the
   unchanged escalation panel; (v) a mode-(c) case where the `locus` promotion fires; (vi) an
   interpreter-need case showing the additive waypoint. Each trace is a YAML file recording input,
   the stage-by-stage intermediate lists with each concept's integer score and its `(-score,
   concept_id)` sort key, and the final output, plus its substance tuple and hash.

9. **`spec_check` — the runnable trace checker.** Ship `src/epppsynth/registry/spec_check.py`,
   runnable as `python -m epppsynth.registry.spec_check`, validating every trace against
   `schema/composer_trace.schema.json` and asserting the invariants of step 2 that a trace can
   express: `CI-1`, `CI-2`, `CI-3`, `CI-6`, `CI-7`, `CI-8`, plus that every stage's ranking is
   consistent with the integer scores recorded in the trace, and that recomputing the substance
   tuple from the trace's output reproduces the recorded hash. This is a **specification** checker —
   it verifies the traces are internally consistent with the spec, not that any engine exists.

10. **Tests** (`tests/ep/test_ep11.py`): every trace passes; hand-broken copies fail one invariant
    each (a waypoint with no counter-reading; a hypothesis with no insufficient-basis clause of its
    own, and a set carrying one shared set-level clause instead of one per hypothesis; two concepts from one
    family; an assertion-form utterance; a mode-(c) set with personal-meaning and no structural; a
    trace whose recorded sort order contradicts its own integer scores; a trace whose substance hash
    does not recompute).

11. **Documentation.** Add the dated addendum under **D-18** recording the hard-stop rendering
    resolution. Add `docs/composer-spec.md` to `DESIGN.md` §Traceability with its invariant IDs, so
    EP-19/20/21 and the P3 suites can cite `CI-n`. Add an ADR for the integer ranking scheme and the
    family diversity rule.

## Out of scope

- Any implementation of selection, ranking, abstention, hard stops or template rendering →
  **EP-19**, **EP-20**, **EP-21**.
- Typed contracts / dataclasses for the input tuple and the waypoint render → **EP-17**.
- The user-facing wording of abstention text, stop-card copy, the interpreter note and the escalation
  panel → **EP-39** (copy deck) with **EP-3** (charter) governing; this brief specifies *where* each
  string is emitted and its invariants, never the string.
- Real concept content and question templates → **EP-12**, **EP-13**, **EP-14**.
- The substance-tuple extractor and comparator implementation → **EP-28**.
- The paired-preference stop-criterion harness and its thresholds → **EP-31** (D-37, D-75).
- Anything about the LLM renderer path → **EP-36** (D-54); the LLM never runs the pipeline specified
  here, it renders its output.
- The waypoints panel layout, focus management and typography enforcement → **EP-43** (D-58).

## Verification / acceptance

- `uv run python -m epppsynth.registry.spec_check` exits `0` over all traces and prints the invariant
  IDs asserted per trace.
- `uv run python -m epppsynth.registry.spec_check --path tests/fixtures/ep11/no-counter-reading`
  exits `1` with `CI-1` as the only violation.
- `uv run python -m epppsynth.registry.spec_check --json` reports, per trace, the substance tuple and
  its recomputed hash; the recomputed hash equals the recorded one for every trace.
- `uv run pytest tests/ep/test_ep11.py -q` green, with one broken-trace test per invariant in
  step 10.
- `uv run python -m epppsynth.registry.schema_check --include-examples` still exits `0` (the trace
  fixtures must not pollute the registry).
- `uv run ruff check .` and the project type check green.
- From the git root: `python tools/roadmap_check.py --context-budget EP-11` passes.
- Pre-publication packet (EP-6) re-run for *PHI patterns*, *local paths* and *protected text* over
  the trace files; every trace input carries the "no real person" attestation.
- *(judgement — author)* The spec contains no rule that could vary the escalation panel, verified by
  reading the spec end to end against `CI-5`.
- *(judgement — author)* Every one of `CI-1` … `CI-9` is cited by at least one pipeline step and at
  least one trace, so no invariant is decorative. There is no `CI-10`; the invariant numbering stops
  at nine.
- Commits: `feat(epppsynth): composer specification and worked traces (EP-11)` then
  `docs(roadmap): record EP-11 commit hash`.

## Parked → final-roadmap.md

- A property-based generator over the input enum space that enumerates every reachable output shape
  and asserts the invariants exhaustively — valuable, but it needs the P2 engine and belongs with
  **EP-23**.
- Making the cap (5) and the floor (3) configurable; v1 pins them to D-7's numbers.
- A second diversity axis beyond `family` (for example `locus`) if the coverage dry-run shows the
  family rule alone produces monotonous sets.
- Composer support for `variant_of` records once a non-English variant exists.
- Whether the ordinary-concern floor member should also appear in mode (c), which has its own
  structural floor via `CI-8` — decide at the EP-49 mode gates.
