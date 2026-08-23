# EP-28 — Substance-tuple extractor and comparator

**Size:** M · **Mode:** a · **Core/Stretch:** core ·
**Depends on:** EP-9 (registry schema v0), EP-17 (contracts package), EP-24 (eval harness) ·
**Blocks:** EP-29 (equity and coercion suites), EP-31 (paired preference, re-plan P3)

> **Charter.** **EP-23 (engine integration, fixtures, re-plan P2)** upgrades this to a full brief.
> Sized M but flagged **highest-value in P3** — the re-plan should confirm M is still right after
> the P1 registry fields are known.

## Context

This is the single most load-bearing piece of the evaluation. D-37's stop criterion turns on whether
paired outputs differ in **clinical substance** rather than framing, and D-25's counterfactual rule
turns on the same distinction; without a mechanical definition both collapse into unaided human
judgement and neither is auditable. One definition powers both suites.

**Operational definition.** *Substance* is the normalized tuple
`(concept_id_set, question_intent_multiset, abstention_flags)`, where `question_intent` is a **closed
enumeration** carried on every question template (e.g. `elicit-values`, `check-understanding`,
`ask-permission`, `surface-concern`, `clarify-goal`, `invite-question`, `name-uncertainty`).
Ordering is normalized away: D-26(c) forbids ranking, so order carries no meaning by construction.
*Framing* is wording, register, sentence order, hedging, length, and which of several equivalent
phrasings realises a given intent. Two outputs **differ in substance** iff their normalized tuples
differ; everything else is framing.

**The tuple is three members, not four.** An earlier draft carried a fourth member, `option_ref_set`
— the clinician-verified options named in output part (iv). Part (iv) was **deleted** from the
output contract rather than left undeliverable (it had no input field, no authored content source and
no owning brief), so `option_ref_set` would have been a constant across every pair, silently
weakening both the counterfactual-equity suite and the D-37 stop criterion that rest on this tuple.
Do not restore it; a member that never varies is worse than no member.

**Prerequisites from P1/P2** (A-WS3-2): every question template carries `question_intent`, and every
D-25 field carries the three-way sensitivity declaration of D-73 (`invariant` /
`clinically-load-bearing` / `framing-plus-one-permitted-additive-waypoint`). If either is missing at
pickup, this brief is **blocked**, not started — raise it as a P1 defect.

## Safety preconditions

- The comparator must never fall back to prose similarity, embedding distance, or a model judgement:
  LLM-as-judge is rejected because it would collapse the control arm (D-17).
- The human-readable diff emits concept IDs, intents and abstention flags — never prose bodies and
  never a verbatim span (D-23). The diff is an artifact that may be published.
- Disputed cases are **logged, never silently resolved**. A silent resolution here would quietly move
  the stop criterion's threshold.
- Extraction is a pure function of a validated `OutputBundle`; it reads no clock, no RNG, no network.

## Scope sketch (refine at re-plan)

1. Add the tuple to the result schema and give it a stable serialization for hashing.
2. Implement the extractor over validated output bundles; fail loudly on an output the schema
   accepted but the extractor cannot read — that is a contract bug, not a skip.
3. Normalization: set semantics for concepts, multiset semantics for intents, canonical ordering of
   abstention flags.
4. Comparator returning `equal` or `differs` plus a structured diff; a `disputed` outcome for the
   D-73 additive-waypoint category, routed to the log rather than to a pass.
5. **Modal-tuple selection across N runs**, used by EP-29 and EP-31: the modal tuple per side, and an
   explicit `no stable mode` result that callers must handle (EP-31 counts it as differing).
6. Unit tests including one hand-built pair differing **only in framing** and one differing **only in
   substance**, plus a pair where the only difference is ordering.

## Verification / acceptance (sketch)

- The three hand-built pairs classify correctly: framing-only ⇒ equal, substance-only ⇒ differs,
  order-only ⇒ equal.
- Extraction succeeds on 100 % of dev-set outputs; zero silent skips.
- Same bundle in ⇒ byte-identical tuple out, over 100 repeats.
- The disputed-case log is non-empty only for D-73's additive-waypoint category, and every entry has
  a written adjudication.
- *(judgement — author)* the intent enumeration is fine enough that two outputs a clinician would
  call substantively different cannot produce an equal tuple.

## Parked → final-roadmap.md

- Semantic similarity of prose, and any similarity measure requiring a model — permanently out.
- Widening `question_intent` after real reviewer feedback; the enumeration is closed for v1.
