# epppsynth — DESIGN

The technical design. `GOVERNANCE.md` overrides this document; `DECISIONS.md` records why each choice
was made. Planned 2026-08-23; nothing here is built yet. Every component names the roadmap brief
(`EP-n`) that builds it.

---

## 1. Purpose and non-goals

**Purpose.** Given (a) a small set of explicitly supplied, structured facts about an encounter,
(b) optionally the person's own words, and (c) a stated purpose, produce **3–5 concise waypoints** a
clinician or trainee can hold in working memory or discard: what is known and unknown, plural possible
concerns each with a counter-reading and an insufficient-basis clause, and disconfirming
permission-based questions.

**Non-goals.** Ranking, adjudicating, or suppressing clinical options · inferring anyone's inner state,
identity, or beliefs · detecting risk · persuading anyone of anything · replacing a conversation, a
clinician, an interpreter, a chaplain, an ethicist, or a crisis service · running on anyone else's
machine as a product.

## 2. Three modes, one engine

One engine with three **purpose profiles** — mode (a) clinician pre-encounter reflection on fictional
cases, (b) trainee education, (c) clinician self-reflection. They share the conceptual model, the input
contract, the output contract, the abstention chain and the hard-stop path; they differ in
`mode_scope` filtering, copy, escalation wording, and their own evaluation sets and release gates.

## 3. Input contract — EP-17, EP-42

Eight structured enum fields, every one carrying **unknown / not relevant / prefer not to answer** as
real options with no pre-selected default: role · encounter temporality · stated communication and
information preference · stated decision-sharing preference · self-described framework · uncertainty
tolerance · illness stage · language and interpreter need.

Plus **one free-text field: "what the person actually said."** It is an **inert echo**: quoted back to
the reader verbatim, and nothing else. It never contributes to selection, never changes which concepts
are emitted, is never tokenised, classified, keyword-scanned, or used to infer anything about anyone.
It is a distinct type whose string representation is `<redacted>`, so it cannot reach a log by
accident. A structural test asserts no code path reads it except the echo.

*Why this is stated so absolutely:* the moment free text can change what the engine emits, the engine
is reading prose for unstated content — which is the retired "hidden dynamic" move under another name.
Two consequences follow and are recorded rather than hidden: the hard-stop checklist matches
**declared fields only** (§5), and the stop criterion's free-text pivot is vacuous on the deterministic
baseline and informative only on the model path (§12).

Every field carries a three-way **sensitivity declaration** with a written rationale:

| Class | Meaning | Example |
|---|---|---|
| `invariant` | may change framing only; clinical substance must be identical under a flip | self-described framework |
| `clinically-load-bearing` | legitimately changes content | illness stage, encounter temporality |
| `framing-plus-one-permitted-additive-waypoint` | framing, plus exactly one additive waypoint | language and interpreter need |

The counterfactual suite (EP-29) enforces this mechanically rather than trusting it.

## 4. Output contract — EP-17, EP-21, EP-43

Three parts, rendered in this order, uncertainty **first**:

1. **Known facts and unknowns.** The unknowns list is never empty; if the engine has no unknowns it
   abstains rather than printing "none".
2. **Possible concerns.** ≥ 2 hypotheses as equal-weight siblings; each carries a nested
   counter-reading and its own insufficient-basis clause. No ordering by confidence, no numbers, no
   percentages, no "most likely".
3. **Disconfirming, permission-based questions.** Every suggested utterance parses as a **question or
   an offer** — never an assertion about what anyone feels, needs, or should do.

**A fourth part was specified and then deleted.** It would have connected stated values to
*clinician-verified options*, but no input field carried those options, no record type was authored to
supply them, and no brief owned it — so it would have shipped permanently empty and made
`option_ref_set` a constant that silently weakened both the equity suite and the stop criterion. The
alternative was a ninth input field plus a completeness invariant; deletion was chosen instead. **The
tool now says nothing about clinical options at all.** The prohibition on ranking, comparing, ordering
or advocating among options is unchanged and still binds parts (ii) and (iii) — the guard outlives the
part it guarded, and a later session must not "restore" the fourth part on the grounds that its
guardrails look unused.

`counter_reading` and `insufficient_basis_clause` are **structurally required fields of the composer**,
so the epistemic guarantees are enforced by the type system and the validator rather than by prompt
discipline or good intentions.

**Never emitted:** numeric confidence, risk language, screening or assessment language, first-person
voice, "recommends", "the patient feels", objection-handling scaffolding. The banned-phrase list lives
in `SAFETY.md` and is the single source a lint consumes at authoring time and at render time, failing
closed (EP-39).

## 5. Abstention and hard stops — EP-20, EP-30, EP-44

The chain runs **first**, in fixed precedence, before any selection:

1. **Hard-stop flag** → stop card in the waypoints region, zero waypoints.
2. **Prohibited request class** — persuasion, prognosis, capacity, diagnosis, ranking → refusal with a
   named reason.
3. **Framework outside the declared Western-secular scope** → abstention naming the limit. This is a
   literal enum value on the framework field, so scope is *data*, not engine judgement.
4. **Declared disagreement or refusal** → non-pathologizing frame; no content aimed at reopening it.
5. **Insufficient basis** — fewer than three concepts survive filtering, or unknowns outweigh knowns →
   whole-bundle abstention. The bar never lowers to hit a count.

Detection is deterministic — declared flags plus a fixed checklist, **never a generative classifier**.
The escalation copy renders from a **constant**, with no dependency on registry, template, or model
load succeeding, and the escalation panel is byte-identical on every response **within a mode**, so its
state carries no information. Invariance is per mode, not global: mode (c)'s operator is also its
subject, so that mode ships its own constant panel addressed to the operator rather than about a third
party (R-40). A panel that varies with input is a risk signal, which would falsify the project's
central safety claim.

## 6. Conceptual model — EP-9 … EP-16

A YAML concept registry — not a formal ontology, which would buy inference the product does not need
and import an authority claim it must avoid.

**Concept types:** `given` (an existential dimension, labelled as one tradition's framing) ·
`function` (a conversational function, each with an evidence grade) · `principle` (a
trauma-informed constraint that filters or reshapes emissions) · `condition` (a structural or
relational condition of clinical work; the mode (c) substrate) · `caution` (an anti-pattern,
contraindication, or abstention trigger). One supporting record kind: `question_template`.

**Typed relations,** each carrying the concept IDs or citation that licenses it: `may_manifest_as` ·
`counter_hypothesis_of` (symmetric-complete — every `given` needs one or the registry fails
validation) · `invites` · `constrained_by` · `contraindicated_when` · `out_of_declared_scope_when` ·
`alternative_reading` · `evidence_for` / `evidence_absent_for` (the second is **mandatory** where no
inspected source supports a function) · `escalates_to` · `family` (the diversity grouping the engine
uses to guarantee plural hypotheses across genuinely different dimensions).

**Every concept carries:** stable ID `EPS.<TYPE3>.<NNNN>` (never reused, never renumbered) · version
and content hash · provenance (source, derivation mode, chapter-level citation) · rights and
`reuse_class` · cultural scope with `claims_universality` hard-coded `false` · evidence claim type ·
review status (`draft` → `lens-review` → `accepted` → `blocked` → `deprecated`; only `accepted` is
emitted) · contested interpretations · `locus` (`structural` / `relational` / `personal-meaning`) ·
`mode_scope` · `lang`. The validator rejects any ordinal, severity, score, or count field anywhere in
the registry.

**Critique lenses** — narrative medicine, generalist spiritual care, disability-community critique —
review every concept and every output template. A lens may set an item `blocked`; only a published,
dated override rationale clears it. A lens may not author replacement content and may not block a
release. Coverage is a gate: every `accepted` concept carries a finding or an explicit `no-finding`
from all three. Blocked concepts are published under "withdrawn / not adopted" with the finding
attached — the most credible available evidence that the protocol is real.

### 6.1 Repurposing failure modes — Y-1 … Y-8

Taking a psychotherapy framework and using it as a non-therapy reflection aid fails in specific,
nameable ways. Each has a mechanism against it, not a caution:

| # | Failure mode | Guardrail |
|---|---|---|
| Y-1 | **Reification** — a labelled given reads as a finding about the person | no concept emitted without a counter-reading and an insufficient-basis clause; composer-enforced |
| Y-2 | **Depth transfer without the container** — existential inquiry in therapy is held by a relationship, a contract and a trained therapist; a clinic visit has none of those | `function` concepts are elicitation-only; the spiritual-care lens blocks any concept requiring interpretive work; every existential concept carries a referral path |
| Y-3 | **Universality smuggling** — a mid-twentieth-century Western frame presented as the structure of human existence | `claims_universality` hard-coded false; the tradition label renders beside every given; the scope declaration is on screen, not only in docs |
| Y-4 | **Diagnostic drift** — existential vocabulary hardens into quasi-clinical categorisation | no scores, severities or counts anywhere; the validator rejects ordinal fields |
| Y-5 | **Category exhaustion** — four givens imply the space is covered, so a fifth thing is forced into one of four boxes | a permanent ordinary-concern counter-frame that is always selectable, and "insufficient basis" as a first-class output rather than a fallback |
| Y-6 | **Anchoring the encounter** — naming a plausible concern beforehand makes the clinician hear confirmation | every waypoint is a question to ask, never a conclusion to confirm; an anchoring probe in the human-factors evaluation; flagged as untested |
| Y-7 | **Authorial voice as authority** — a source's clinical-literary register carries persuasive force the registry would inherit | concept prose is plain, hedged and non-narrative; the lenses review register, not only content |
| Y-8 | **Rights leakage through structure** — original prose that nonetheless reproduces a source's organisation | chapter-level citations only; validator lint against chapter-title labels and outline-reconstructing locator sequences |

## 7. Composition — EP-11, EP-19, EP-21

```
abstention/hard-stop chain (fixed precedence, first and last)
  → normalise input to a canonical facet vector (free text contributes only as a verbatim echo)
  → gather   concepts with an activation edge matching a declared facet   [dict lookup, not search]
  → filter   out-of-scope · contraindicated · wrong mode · not accepted
  → rank     integer score; no floats ⇒ exact ties ⇒ lexicographic tie-break on concept ID
  → diversify at most one concept per family in the top-k
  → pair     each survivor with its counter-hypothesis, else the literal insufficient-basis item
  → cap      3–5 waypoints; fewer than 3 survivors ⇒ partial or whole abstention
  → compose  templates as data with a restricted slot grammar; slots fill only from registry fields
             or the reader's own quoted words
  → validate contract schema · citation resolution · question-or-offer parse · banned-phrase lint
```

Pure functions, no clock, no RNG, sorted everywhere. Bit-reproducible and golden-testable on the
`(contract_version, registry_version, template_version)` triple, which is stamped into every output.
That exactness is what makes the counterfactual suite mechanical rather than a matter of judgement.

**Uncertainty is ordinal, never numeric:** each waypoint carries `basis ∈ {declared,
follows-from-declared, not-supported}` and an explicit unknowns list. Internal scores are test-visible
only. A confidence number beside a reading would manufacture exactly the authority the tool exists to
withhold.

## 8. The gated model path — EP-32 … EP-36

The deterministic baseline is the **shipped default and the permanent fallback**. A local model is
added only behind a measured benchmark gate, and only if it beats the baseline on the evaluation sets.

When enabled, the model is a **renderer, not an author**. It receives selected concept IDs, their
authored paraphrases, and the reader's quoted words — never the registry wholesale, never the corpus
index, never a raw span. Output is constrained by a JSON schema in which every prose leaf sits beside
a required concept ID; post-validation drops any sentence that does not bind to a candidate ID, and
past a drop threshold the whole response is discarded in favour of templates. Under that design the
model can only lose information, never invent it.

Runtime: an in-process GGUF runtime — no daemon, no listener, no auto-update. Weights are pinned by
revision and verified by file hash; remote code execution is disabled; pickle-format weights are
refused. The same rules apply to embedding models. **"Deterministic" never describes this path** —
GPU kernels are not bit-deterministic even with a fixed seed. Its claim is narrower and testable:
schema-valid, claim-bound, and subject to the same abstention chain.

**Degradation ladder, always logged, never silent:** full offload → reduced offload → CPU-only →
deterministic baseline. Missing or corrupt weights → baseline with a visible banner. Registry fails
validation → refuse to start, because a half-loaded registry is worse than no tool. Hard-stop path
fails → render nothing but the escalation panel.

## 9. Corpus and local index — EP-22

Authoring-time only, and strictly separate from the runtime path. The ingest module converts a copy of
a source the author lawfully holds into local markdown and an optional local index. The corpus lives
in a gitignored directory **inside** the working tree (`source material/`, excluded by `.gitignore`
and verified absent from history); the derived index and the model weights live **outside** the tree
entirely. None of it enters CI or a published artifact. Verbatim spans may
exist there and may be displayed in a **local-only source pane**; they may never be emitted, exported,
or screenshotted. This is enforced by the type graph: spans live in a separate payload produced by a
separate call, never nested in the output bundle, and refused by a single export chokepoint. Runtime
reads exactly two artifacts: the validated registry and the templates.

## 10. Interface — EP-38 … EP-46

Server-rendered HTML on loopback: one route, three always-present regions (input form · waypoints ·
escalation), no navigation, no accounts, no persistence, an explicit "nothing is saved" indicator, and
a launch interstitial that cannot be permanently dismissed because there is nothing to remember it.

**Loopback is not a security boundary.** Eight independently tested controls: loopback bind on an
ephemeral port · **Host-header allowlist** (the DNS-rebinding control, which an Origin check does not
provide) · Origin and fetch-metadata checks · a one-shot launch token bound at first load with no idle
expiry, exchanged for a host-only session cookie · a session-bound CSRF token · a strict content
security policy and header set · **no CORS headers at all** · a single session that ends when the tab
closes.

**Accessibility is a release gate, not a polish pass.** WCAG 2.2 AA, tested by automation plus a
scripted manual pass; the public statement says "built to … tested by … not independently audited",
never "compliant". Two rules do most of the work: results are announced **and** focused, and
**uncertainty is never de-emphasised** — counter-readings, insufficient-basis text and abstentions
render at the same size, weight and contrast as hypotheses, enforced by a lint that refuses muted
tokens in the waypoints region. That one rule is simultaneously the contrast requirement and the
primary automation-bias control.

No animation, no streaming reveal, no spinner that mimics deliberation, no TL;DR, no copy-all.

## 11. Storage

Two roots outside the repository: a model root and an index root, kept separate because they are
different rights classes and must be independently purgeable. A **floor** of ≥ 250 GiB free on the
system volume is asserted before and after every write; a **ceiling** of 25 GB caps the project's own
footprint, warned at 20 GB. Expected real usage is roughly 8–12 GB. Downloads are one at a time,
individually confirmed, hash-verified, and recorded in a lockfile that is the register of every weight
the project may load. The seven cache-purge safety rules are written as an ADR; **no purge tool is
built**.

## 12. Evaluation architecture — EP-24 … EP-31

Two tiers. **Deterministic** suites run in CI on the no-model path at 100 % pass: schema, unit,
property, consistency and golden tests. **Stochastic** suites run only when the model path is enabled,
N=5 development and N=10 release runs per case, gating on a confidence-interval lower bound, with an
unstable case counted as a **failure** — a clinician cannot know which run they got.

Eight suites: conceptual fidelity · clinical plausibility · uncertainty and hallucination · coercion
and forced meaning · counterfactual equity · abstention and escalation (with an over-abstention
ceiling, because a tool that abstains constantly teaches its reader to dismiss abstentions) ·
hard-stop behaviour (100 %, no exceptions) · human factors.

Scenarios: ~20–30 development, ~15 red-team, ~10–15 **frozen held-out** authored before any tuning,
frozen under a signed tag, executed at most once per release candidate, with blocking contamination
checks. A held-out failure is repaired by changing the development set and re-authoring — never by
editing the held-out case.

"Clinical substance versus framing" is machine-decidable as the normalized tuple `(concept_id_set,
question_intent_multiset, abstention_flags)`. One definition powers both the equity
suite and the stop criterion.

## 13. Trust boundaries

1. Corpus and index ↔ everything else — one-way, authoring only.
2. Browser origin ↔ loopback server — eight controls, §10.
3. Weight file ↔ process — hash-verified before load, no remote code, no pickle.
4. **The export boundary** — a single serialization chokepoint that refuses any payload capable of
   carrying a verbatim span.
5. Acquisition network ↔ runtime network — acquisition is confirmed and hash-pinned; runtime is zero
   and verified in two layers.

Prompt injection is handled at the **output** side, as an architectural invariant rather than a
mitigation: if every output must satisfy the schema, resolve every citation to a live registry ID, and
parse every utterance as a question or an offer, an injected instruction has no channel through which
to express harm.

## 14. Hazard register

41 hazards, each with affected people, prevention, the brief that implements the control, and the gate
that verifies it. Highest-rated: **R-25**, an underpowered stop criterion read as
evidence of safety; **R-33**, uncertainty rendered as de-emphasised secondary text; **R-1**, the
coercion architecture the original design sketch would have produced; **R-34**, an escalation panel
that varies with input and so becomes a risk signal.

| ID | Hazard | Affected | L/S | Prevention (mechanism, not intention) | Brief | Gate |
|---|---|---|---|---|---|---|
| R-1 | Coercion architecture — output functions as leverage toward a decision | patients, families | M/H | every utterance a question or offer; no objection-handling content; substance invariant to clinician preference | EP-3, EP-21, EP-31 | mode (a) |
| R-2 | Automation bias / authority laundering | clinicians → patients | H/H | mandatory counter-reading and insufficient-basis clause; no numeric confidence; ordinal basis labels only | EP-11, EP-43 | human factors |
| R-3 | Stereotyping or inferred identity | patients | M/H | structured enums only; free text inert; counterfactual flip suite | EP-17, EP-29 | equity suite |
| R-4 | Pathologizing disagreement | patients | M/H | declared disagreement suppresses persuasive-tagged content and emits a non-pathologizing frame | EP-20, EP-30 | abstention suite |
| R-5 | Crisis mishandled | patients, clinicians | L/H | deterministic hard stops from declared flags; zero-dependency escalation constant | EP-20, EP-44 | hard-stop suite, 100 % |
| R-6 | Public-history leakage | patients, author | M/H | fictional-only fixtures; history assertion; scanners as defense in depth | EP-0, EP-6 | every publication |
| R-7 | Rights leakage / unlawful redistribution | rights holders | M/H | per-source rights table; no verbatim field in any exportable type; quotation budget in CI | EP-5, EP-17, EP-22 | every publication |
| R-8 | Trainee surveillance or compelled disclosure | trainees | L/H | no accounts, no scoring, no retention, no export, no employer visibility | EP-47 | mode (b) |
| R-9 | Portfolio overclaim under hiring pressure | readers, patients | M/H | badge resolves to an evidence file; conservative claim language; halts disclosed publicly | EP-2, EP-50, EP-53 | every publication |
| R-10 | Mode (c) drifts into unlicensed self-help | clinicians | M/M | no screening, scoring or diagnosis; structural concept required alongside personal-meaning | EP-48 | mode (c) |
| R-11 | Concept reification — a labelled given read as a finding | patients | M/H | no concept emitted without a counter-reading and an insufficient-basis clause | EP-11, EP-12 | conceptual fidelity |
| R-12 | Null-to-harm precedent — documentation implies a benefit the evidence contradicts | patients, readers | M/H | evidence appendix published with the tool; charter clause forbidding "preparation is benign" | EP-3, EP-13 | mode (a) |
| R-13 | Registry accretion without provenance | all | H/M | required-field validator; CI fails on any concept missing provenance or cultural scope | EP-10, EP-16 | P1 exit |
| R-14 | Lens tokenism — review recorded but toothless | disabled people, people outside the declared frame | M/H | conditional veto with published override; ≥ 1 blocking finding or the protocol is revisited | EP-15 | P1 exit |
| R-15 | Licence contamination into the content model | project | M/H | `reuse_class` per source; normative guidance referenced, never ingested | EP-5, EP-10 | every publication |
| R-16 | Mode (c) inversion into individual pathology | clinicians, trainees | M/H | `locus` field; personal-meaning implies structural, enforced by the composer; no ordinals | EP-14, EP-48 | mode (c) |
| R-17 | Anchoring — pre-encounter naming biases what the clinician then hears | patients | M/M | waypoints phrased as questions to ask, never conclusions; anchoring probe in human factors | EP-11, EP-51 | mode (a) |
| R-18 | Crash dumps capture prompts, defeating "no retention" | patients via the machine | M/H | redacting excepthook; dump posture documented rather than denied | EP-46 | privacy harness |
| R-19 | Local index leaks via a fixture, screenshot or error message | rights holders | M/H | index outside the tree; index-dependent tests skip-marked; span-leak canary | EP-22, EP-46 | every publication |
| R-20 | Runtime version drift invalidates the benchmark packet | clinician relying on measured behaviour | M/M | no daemon runtime; wheel pinned by version and hash; runtime version in every packet | EP-32, EP-35 | benchmark |
| R-21 | A future cache purge escapes the model root | the operator's machine | L/H | seven purge-safety rules recorded as an ADR; no purge tool is built | EP-7 | pre-merge review |
| R-22 | Launch token persists in browser history or sync | clinician | M/M | token consumed then redirected; no-referrer; no-store | EP-41 | loopback suite |
| R-23 | Held-out contamination | patients downstream | M/H | author-only held-out authored before tuning; frozen manifest; blocking overlap checks | EP-27 | eval suites |
| R-24 | Reviewer over-trust and social pressure | patients, reviewers | M/M | blinded scoring before discussion; structured yes/no sign-off; individual scores unpublished | EP-37, EP-51 | mode (a) |
| R-25 | **Underpowered stop criterion read as evidence of safety** | patients, readers | H/H | interval published beside every rate; fixed power-limitation sentence; the baseline pivot's vacuity disclosed | EP-31 | mode (a) |
| R-26 | DNS rebinding into the loopback interface | the reader | M/M | Host-header allowlist, as a control distinct from Origin and CSRF checks | EP-41 | loopback suite |
| R-27 | Prompt injection via free text or generated scenarios | the reader; the evaluation's integrity | M/M | output-side schema, citation resolution and question-or-offer parse; failing output discarded | EP-21, EP-26 | eval suites |
| R-28 | Reviewer attribution read as clinical endorsement | reviewers, patients | M/M | consent disclaims endorsement; role-only attribution; narrow sign-off wording | EP-37 | mode (a) |
| R-29 | Supply-chain compromise | the machine, the public repository | L/H | SHA-pinned actions; hash-locked dependencies; least-privilege tokens; no fork secrets | EP-1, EP-6 | every release |
| R-30 | Evidence drift — the gate passes against a build that is not the tagged one | patients, readers | M/H | every artifact records the build hash; the release job asserts equality with the tag | EP-50 | every release |
| R-31 | Over-abstention trains the reader to dismiss abstentions | readers, patients | M/M | near-miss negatives per trigger; over-abstention rate reported publicly beside recall | EP-30 | abstention suite |
| R-32 | Conformance or validation overclaim | disabled users, readers | M/M | fixed "built to … tested by … not independently audited" phrasing | EP-2, EP-46 | every publication |
| R-33 | **Uncertainty rendered as de-emphasised secondary text** | clinicians → patients | H/H | uniform size, weight and contrast inside the waypoints region; lint refuses muted tokens there | EP-39, EP-43 | accessibility packet |
| R-34 | Escalation panel read as a risk signal because it varies with input | patients, clinicians | M/H | byte-identical render within a mode; single-hash assertion across the eval corpus | EP-44 | hard-stop suite |
| R-35 | Source pane leaks spans into a screenshot, CI log or published template | rights holders | M/H | double gate; local-only templates excluded from the published tree; CI asserts disabled | EP-45 | every publication |
| R-36 | Site or narrative copy drifts ahead of the badge | hiring readers | M/M | one canonical status line, quoted verbatim by the card and the narrative | EP-53 | P7 |
| R-37 | Assertive-region flooding desensitises the hard-stop announcement | screen-reader users | M/M | assertive role reserved for hard stops and abstentions; at-most-one assertion per response | EP-43 | accessibility packet |
| R-38 | A third party runs the tool and treats it as validated | unknown clinicians and patients | M/H | intended and excluded uses at the top of the README; no release, tag or demo before the gate | EP-2, EP-53 | every publication |
| R-39 | **The intended user's own pressure to use it on a real case.** v1 is fictional-only, so the tool has no legitimate place in the workflow it was designed around — which is precisely the pressure that produces a real-case use | patients | M/H | launch interstitial repeating the exclusion; no PHI-shaped input affordance; the human-factors debrief asks directly whether the reader wanted to use it on a real case, and the answer is published | EP-40, EP-51 | mode (a) |
| R-40 | **Mode (c)'s escalation panel addresses the wrong person.** Its fixed heading speaks about a third party, but in mode (c) the operator is the subject | clinicians, trainees | M/H | panel invariance is **per mode**, not global: mode (c) ships its own constant panel addressed to the operator, still byte-identical within the mode and still hash-asserted | EP-44, EP-48 | mode (c) |
| R-41 | **Cultural flattening** — a single Western-secular tradition read as a general account of how people face serious illness | patients outside the declared frame | M/H | `claims_universality` hard-coded false and validator-rejected; the tradition label renders beside every concept; out-of-scope frameworks abstain rather than adapt; the disability and spiritual-care lenses can block a concept | EP-9, EP-12, EP-15, EP-20 | P1 exit, abstention suite |

Each hazard names the brief that implements its control and the gate that verifies it.
`tools/roadmap_check.py --hazards` fails if a hazard names no brief, if a cited `R-n` does not exist
here, or if a core brief names no acceptance evidence. **This table is the register**; every other
document points at it rather than restating it.

## 15. Traceability

| Need | Requirement | Component / content | Brief | Evidence |
|---|---|---|---|---|
| Reflection without authority | plural hypotheses + counter-reading + insufficient basis, structurally required | composer | EP-11, EP-19 | conceptual-fidelity suite |
| No coercion | every utterance a question or offer; substance invariant to clinician preference | linter; paired-preference harness | EP-21, EP-31 | coercion suite; stop criterion |
| No stereotyping | three-way field sensitivity; free text never mined | input contract | EP-17, EP-29 | counterfactual equity suite |
| Honest scope limits | out-of-scope framework as a literal enum → abstention | registry + chain | EP-9, EP-20 | abstention suite |
| Crisis safety | deterministic detection; invariant escalation panel | hard-stop path | EP-20, EP-44 | hard-stop suite, 100 % |
| No retention, no egress | typed redaction; two-layer verification | privacy harness | EP-46 | filesystem delta; empty egress log |
| Rights integrity | no verbatim span in any exportable type | export chokepoint | EP-17, EP-22 | type-graph test; leak scanners |
| Usable by a real reader | announced and focused results; undiminished uncertainty | interface | EP-43, EP-46 | accessibility packet |
| Honest public claims | badge resolves to an evidence file | CI badge check | EP-2, EP-50 | deliberate red run |

## 16. ADR queue

001 runtime selection · 002 registry schema and ID scheme · 003 output contract types and the
no-verbatim-field invariant · 004 integer scoring and tie-breaking · 005 abstention precedence ·
006 renderer-only model path and claim binding · 007 storage roots, reserve floor, project ceiling and
the seven purge-safety rules · 008 licensing boundary and REUSE layout · 009 network posture and its
verification · 010 schema migration policy · 011 benchmark packet schema · 012 source-pane isolation.
ADR-001, 007, 008 and 009 land in P0; the rest land with their phase.

## 17. Module map

Filled in as briefs land; every module is tagged with the `EP-n` that built it, per the sibling
repositories' convention.
