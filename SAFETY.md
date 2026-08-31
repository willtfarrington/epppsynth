# SAFETY — the clinical-ethics charter

This is the charter for `epppsynth`. It states what the tool refuses to do and why each refusal
exists.

It is a **specification**, not a statement of intent. Four later work packets consume it directly:
the banned-phrase lint reads the list published below from the same file it is generated from
(planned EP-39), the abstention chain implements the taxonomy in §8 (planned EP-20), the red-team
set attacks the prohibitions in §6 (planned EP-26), and the escalation panel renders the copy fixed
in §9 (planned EP-44).

**Nothing in this repository runs.** There is no engine, no registry, no evaluation, and no
release. Every prohibition below is a binding constraint on what may be built, and the enforcement
table in §6 states, per prohibition, that nothing enforces it yet and which work packet will. A
charter that reads as reassurance would be a failure of this document; this one is meant to read as
a list of debts.

Where this document and [`epppsynth/GOVERNANCE.md`](epppsynth/GOVERNANCE.md) disagree, governance
wins and this document is wrong. Decisions cited as `D-n` are recorded in full in
[`epppsynth/DECISIONS.md`](epppsynth/DECISIONS.md); hazards cited as `R-n` are recorded in
[`epppsynth/DESIGN.md`](epppsynth/DESIGN.md) §14; work packets cited as `EP-n` are in
[`roadmap/README.md`](roadmap/README.md).

---

## 1. Status

```
Design and planning artifact — v1 in progress; no release, no demo, no validation.
```

No version has been tagged. No demo exists. No evaluation has been run, by this project or by
anyone else. The repository is public as a design and source artifact; **public source availability
is not evidence of efficacy, safety, approval, or suitability.** The tool is built for its author's
private local use.

## 2. Intended use

`epppsynth` — *existential perspectives for physicians & patients* — is a **local, offline-capable
reflection aid**. A human supplies encounter context explicitly, states a purpose, and receives a
few concise, revisable waypoints they can hold in working memory or discard.

It is **not** therapy, not clinical decision support, not a risk detector, not a screening or
assessment instrument, and not a source of clinical recommendations.

Three purpose profiles are in scope for v1, built in this order, each with its own evaluation set
and its own release gate, so that a failing mode is withheld without blocking the others:

- **Mode (a) — clinician pre-encounter reflection on fictional scenarios only.** The v1 build target.
- **Mode (b) — trainee education and reflection.**
- **Mode (c) — clinician self-reflection on the structural and existential dimensions of a clinical
  experience.**

Patient-specific point-of-care use and patient- or family-facing use are **excluded release
classes** (D-61). They are excluded with seven named preconditions — each requiring an external
accountable party this project does not have — rather than placed on a schedule. No work packet in
the roadmap advances them, no version number reaches them, and reversing the exclusion would be a
public act with a dated rationale. The preconditions are listed in
[`epppsynth/GOVERNANCE.md`](epppsynth/GOVERNANCE.md) §9.

## 3. Excluded uses

This tool must not be used:

- with real patient information of any kind;
- to make, support, justify, or document a clinical decision;
- as a screening, triage, risk-detection, monitoring, or safety instrument;
- to assess capacity, prognosis, diagnosis, or mental health;
- to generate anything shown or read to a patient or family;
- to persuade, or to prepare arguments for persuading, a patient or family toward any decision;
- to evaluate, score, grade, observe, or monitor a trainee;
- during an active encounter;
- in place of consulting palliative care, psychiatry, ethics, chaplaincy, social work, interpreter
  services, or a crisis service.

**This tool is not a risk detector and must not be used as one.** It never checks what is typed for
danger.

## 4. What it does not know

The tool has no access to anything it is not explicitly handed, and it infers nothing from what it
is handed. Stated as a list, because the gap between what a reader assumes a program knows and what
this one knows is itself a hazard (R-2, automation bias). These are binding statements about the
design, not descriptions of a program that runs today; nothing here runs.

- **It does not know the person.** No chart, note, result, medication list, or history reaches it.
  It sees a small set of structured fields a human typed, plus one optional quotation of what the
  person actually said. There is no patient record anywhere in the system.
- **It does not know what anyone believes, values, or feels.** Nothing is inferred from a name, a
  diagnosis, a group membership, or the wording of the free-text field. A preference affects the
  output only when a human has stated it in a declared field, and then it changes **communication
  framing only, never clinical content** (D-25).
- **It does not know whether anyone is in danger.** It never examines free text for risk. See §9.
- **It does not know the clinical situation.** It has no prognosis, no capacity assessment, no
  diagnosis, no list of the options actually available to this person, and no view on which of them
  is appropriate. It says nothing about clinical options at all (D-79).
- **It does not know traditions outside its declared scope.** The content model is Western and
  secular in origin. Where a person's framework falls outside it, the required behaviour is
  explicit abstention naming the limit — never adaptation, analogy, or a generic humanistic
  substitute. See §12.
- **It does not know whether it helps.** No evidence of benefit exists for this tool or for its
  class. See §11.
- **It does not know what happened.** There is no retention, no follow-up, no outcome, and no
  record that a session occurred. Nothing is remembered between sessions.

---

## 5. The invariants

Seven invariants. Each is stated once here and enforced elsewhere; the work packet that implements
it and the suite that verifies it are named at the end of each paragraph. None of them is enforced
today, because nothing is built today.

**Epistemic humility and human accountability.** Generated interpretations are revisable reflection
aids — never therapy, authoritative scripts, or diagnoses of motive, mental illness, capacity,
suicidality, spirituality, prognosis, or treatment. Every emission carries alternatives, a
counter-reading, and an insufficient-basis clause; these are structurally required composer fields,
not optional ones, because optional fields are empty in exactly the outputs where they matter most
(D-53). Confidence is never shown beside a waypoint (D-48). The sole accountable human is the
operating clinician or trainee: the output stays on their screen, and there is no export in v1
(D-6). *Implemented by EP-11 (composer specification) and EP-21 (composition CLI); verified by
EP-24 (evaluation harness) and EP-30 (abstention suites).*

**No stereotyping or inferred identity.** Nothing infers beliefs, culture, ethnicity, race,
religion, disability, values, protected traits, or emotional state from names, diagnosis, prose
proxies, or group membership. Every input field supports *unknown*, *not relevant*, and *prefer not
to answer*. Voluntarily stated preferences may affect communication framing only; protected traits
never alter clinical content. The free-text field carries what the person said and is an **inert
echo** — quoted back to the reader and nothing more. It never changes what the engine emits, and it
is never tokenised, keyword-scanned, classified, or mined for inference of any kind. *Implemented
by EP-17 (contracts) and EP-21; verified by EP-29 (counterfactual equity suite), which flips each
sensitive field and asserts equivalence of clinical substance.*

**No coercion.** Nothing may optimise explicit or covert persuasion, compliance, or a target
clinical outcome. The operational line: *rapport* changes what a person is able to say;
*persuasion* changes what a person decides. Prohibited outright: framing designed to make one
option feel safer or more courageous; treating a stated preference as an obstacle; objection
handling; scripting a second attempt after a refusal; and any output whose clinical substance
varies with the clinician's own stated preference. The last of these is machine-tested rather than
asserted (§11). *Implemented by EP-11 and EP-21; verified by EP-29 (coercion suite) and EP-31
(paired-preference harness).*

**Disagreement is not pathologized.** Distrust, anger, grief, silence, requests for testing, and
refusal may be rational responses to uncertainty, prior harm, inequity, communication failure, or
institutional conduct. No output may explain a disagreement in terms of the person's psychological
state. Declared disagreement suppresses persuasion-tagged content and emits a non-pathologizing
frame instead. *Implemented by EP-20 (abstention and hard-stop chain); verified by EP-30
(abstention suites).*

**Hard stops are deterministic.** Detection is by explicit declared flags and a fixed structural
checklist over declared fields only — **never a generative classifier, and never a scan of the
free-text field.** Disability, communication style, limited English proficiency, cultural
difference, and disagreement are not evidence of incapacity. See §9 for the full statement, the
reason, and the compensating controls. *Implemented by EP-20 and EP-44 (escalation panel); verified
by EP-30 (hard-stop suite).*

**Mode separation.** Patient-specific, PHI-processing, patient- or family-facing, point-of-care,
and therapeutic uses are excluded release classes. A disclaimer, the author's preference, or
developer self-review cannot unlock them. Each mode has its own prompts, copy, evaluation set and
release gate; a failing mode is withheld without blocking the others (D-13). *Implemented by EP-47,
EP-48 and EP-52 (per-mode gates); verified by EP-49 (mode-gate re-plan) and EP-50 (release
evidence).*

**Trainee non-surveillance.** Mode (b) is strictly local: no accounts, no scoring, no retention, no
export, no employer visibility, voluntary use only. Structural moral injury is never
individualised. A trainee who can be observed is being assessed, and trainees are the people least
able to decline (D-19). *Implemented by EP-47 (mode (b)); verified by EP-46 (retention and egress
harnesses) and EP-38 (threat model).*

## 6. Prohibitions and their enforcement

A prohibition that nothing enforces is a sentence, not a control. Every prohibition this charter
makes therefore carries the work packet that implements it and the suite that verifies it.

**Today every row of the status column reads *unenforced — planned EP-n*, because no engine
exists.** That is what the column is for: this is a list of promises with owners, not a list of
guarantees. A row may stop saying *unenforced* only when the named packet has shipped and the named
suite passes.

| # | Prohibition | Implemented by | Verified by | Status today |
|---|---|---|---|---|
| P-1 | No assertion about what a patient feels, wants, or should do — every suggested utterance is a question or an offer | EP-21 | EP-29 | unenforced — planned EP-21 |
| P-2 | No persuasion, objection handling, or scripted second attempt after a refusal | EP-20, EP-21 | EP-29 | unenforced — planned EP-20 |
| P-3 | No output whose clinical substance varies with the clinician's stated preference | EP-11, EP-21 | EP-31 | unenforced — planned EP-31 |
| P-4 | No ranking, comparing, ordering, or advocating among clinical options | EP-11 | EP-24, EP-29 | unenforced — planned EP-11 |
| P-5 | No inference of belief, culture, race, religion, disability, values, or emotional state | EP-17 | EP-29 | unenforced — planned EP-17 |
| P-6 | The free-text field is an inert echo — never tokenised, keyword-scanned, classified, or mined | EP-17, EP-21 | EP-26, EP-29 | unenforced — planned EP-17 |
| P-7 | No explanation of a disagreement in terms of the person's psychological state | EP-20 | EP-30 | unenforced — planned EP-20 |
| P-8 | No generative classifier, and no scan of free text for danger | EP-20 | EP-30 | unenforced — planned EP-20 |
| P-9 | The escalation panel never varies with input, within a mode | EP-44 | EP-30 | unenforced — planned EP-44 |
| P-10 | No emission of source text; paraphrase plus a chapter-level citation only | EP-10, EP-21 | EP-6 | unenforced — planned EP-6 |
| P-11 | Uncertainty, counter-reading, insufficient-basis and abstention never render de-emphasised | EP-39, EP-43 | EP-46 | unenforced — planned EP-39 |
| P-12 | No trainee scoring, retention, export, or employer visibility | EP-47 | EP-38, EP-46 | unenforced — planned EP-47 |
| P-13 | No distress screening, scoring or diagnosis in mode (c); no personal-meaning concept without a structural one | EP-48 | EP-30 | unenforced — planned EP-48 |
| P-14 | No banned phrase from the list in §10, in authored or rendered copy | EP-39 | EP-24 | unenforced — planned EP-39 |
| P-15 | No patient-facing, PHI-processing, point-of-care or autonomous use | EP-52 | EP-50 | unenforced — planned EP-52 |
| P-16 | No claim of efficacy, safety, validation, adoption or external review | EP-2, EP-50 | EP-6 | unenforced — planned EP-6 |
| P-17 | No retention of prompts or outputs, and no runtime network traffic | EP-41 | EP-46 | unenforced — planned EP-41 |

P-16 is the only row with a shipped artifact behind it — the README's status line, badge and
no-evidence statement, placed at EP-2 — and it is still marked unenforced, because the check that
resolves the badge to its evidence file and fails on an unticked box is EP-6 and does not exist.
Prose that says the right thing is not enforcement.

## 7. The output contract

The original design sketch for this tool named a hidden dynamic, drove an empathic wedge into it,
and generated consensus. That is a persuasion pipeline, and it was retired outright (D-11). What
replaced it is a three-part contract.

**Part one — known facts and unknowns.** The output begins by separating what the clinician
actually supplied from what nobody has said. This exists because the failure it prevents is silent:
a reader who cannot see the boundary of the input will read the tool's inferences as information
about the person. Naming the unknowns first makes the thinness of the basis visible before any
hypothesis is read.

**Part two — plural possible concerns, each carrying a counter-reading and its own
insufficient-basis clause.** Concerns are always plural, because a single named concern is an
anchor: once a clinician has been handed one interpretation before an encounter, they will hear the
encounter through it (R-17). The counter-reading and the insufficient-basis clause are structurally
required composer fields, not stylistic additions (D-53), and they render at the same weight as the
concern itself (§15). A labelled existential given that arrives without them stops being a
hypothesis and becomes a finding about the person, which is the reification hazard R-11.

**Part three — disconfirming, permission-based questions.** The suggested moves are questions whose
answers could show the hypotheses to be wrong, and they ask permission before they open a subject.
Confirming questions would make the tool a machine for finding evidence of what it already
proposed.

### The fourth part was deleted, not deferred

The contract as first replaced had a fourth part: neutral framing connecting stated values to
clinician-verified options. It is **deleted** (D-79). No input field carried those options, no
record type supplied them and no work packet owned them, so the part would have shipped
permanently empty — and the evaluation's substance tuple would have carried a constant, weakening
both the counterfactual-equity suite and the stop criterion without any test noticing. A contract
that describes an output the tool cannot produce is a claim, not a design.

**The no-ranking prohibition is unaffected and stays in full force.** It now binds the three
remaining parts: nothing ranks, compares, orders, or advocates among clinical options. The tool
simply says nothing about clinical options at all. The guard outlives the part it guarded.

### The four functions preserved from the retired model

D-26 named four functions worth keeping from the retired output model. Three stand; the third was
withdrawn with the fourth output part, and is stated here rather than quietly dropped.

**(a) Name plausible unspoken concerns.** Plural hypotheses, plus a counter-hypothesis, plus an
explicit insufficient-basis clause. This is the function that survives review, because hypothesis
generation is a legitimate use of a content model and does not require the tool to be right.

**(b) Suggest an opening move.** Every suggested utterance is a question or an offer — never an
assertion about what the patient feels or should do. See the rule below.

**(c) Connect stated values to clinician-verified options — withdrawn.** This clause is withdrawn
with D-79, for the reason given above. It is recorded here as withdrawn rather than removed,
because a function that disappears without a note is a function that comes back. The prohibition on
ranking, comparing and advocating that governed it remains in force over everything else.

**(d) Name the clinician's own reaction.** Mode (c) only, and bounded by §13: naming a reaction is
not screening for one, and the reaction is never scored, tracked, or interpreted as a symptom.

### The three retired framings

Named here as retired, with the reason, because a charter that quietly drops them invites their
return under new names:

- **"Hidden Dynamic (Diagnosis)"** — retired. It framed the tool's output as a diagnosis of a
  psychological state the patient had not disclosed. That is a diagnosis of motive, which invariant
  one forbids outright, and it is the seed of the reification hazard.
- **"Empathic Wedge"** — retired. It framed rapport as an instrument for opening a decision, which
  is precisely the line between rapport and persuasion that the no-coercion invariant draws.
- **"Consensus Generation"** — retired. It named agreement as the deliverable of the encounter. A
  tool optimising for agreement is a coercion architecture regardless of how gently it is worded
  (R-1).

### The question-or-offer rule

**Every suggested utterance is a question or an offer. Never an assertion about what the patient
feels, wants, needs, or should do.** This is absolute; there is no output type, mode, or
configuration under which an assertion about another person's interior state is emitted.

It is enforced at two points, and both are needed because they fail differently. The **authoring
linter** (planned EP-21) rejects a template whose suggested utterance is not interrogative or
offer-shaped, catching the failure at the time content is written. The **runtime parse** (planned
EP-21, rendered under EP-43) validates the composed output structurally and discards any suggested
utterance that does not parse as a question or an offer, catching the failure on the model path,
where the text was not written by a human at all. Output-side structural validation is the primary
injection control (D-55): an unbound or unparseable sentence is dropped, never repaired.

## 8. Abstention

Abstention is a safety behaviour with its own evaluation cases, not a courtesy and not a fallback
for when generation fails. Five triggers are required (D-38). Each abstention names the limit it
ran into; a bare "insufficient information" would teach the reader nothing about which limit was
reached.

All five are *unenforced — planned EP-20*, verified by *EP-30 (abstention suites)*.

### Abstention trigger 1 — the person's framework falls outside the declared Western-secular scope

The content model is Western and secular in origin (§12). Where a person's stated framework falls
outside it, the tool abstains and says so. It does not adapt, analogise, or substitute a generic
humanistic reading, because a substitute presented as understanding is the cultural-flattening
harm itself (R-41). Required recall on this trigger is 1.00 (D-75).

*Example.* A clinician enters, in the self-described-framework field, that a fictional patient
understands their illness through a religious tradition the content model does not carry. The tool
returns no waypoints about meaning. It states that its concept set is Western and secular in
origin, that this tradition is outside it, and that the limit is the tool's and not the person's —
and it names chaplaincy and the patient's own community as the people who can help, without
claiming to know whether either would.

### Abstention trigger 2 — insufficient basis in the supplied context

Where the declared fields do not support a hypothesis, the tool declines to generate one rather
than filling the gap from the shape of the case. Required recall 0.95 at precision 0.85 (D-75).

*Example.* A fictional case is entered with illness stage *unknown*, communication preference
*prefer not to answer*, decision-sharing preference *unknown*, and an empty free-text field. The
tool returns the known-and-unknown part, then abstains from the concerns and questions parts, and
states which fields would change that. It does not infer a framework from the diagnosis.

### Abstention trigger 3 — any hard-stop flag is present

A declared hard-stop flag suspends synthesis entirely. This is not partial abstention: no
waypoints are emitted alongside a stop card. See §9. Required recall on this trigger is 1.00
(D-75), because a missed hard stop is the one abstention failure with an immediate route to harm.

*Example.* A clinician ticks the declared flag for disputed surrogacy. The tool emits the stop card
and zero waypoints, and points to the ethics service and the institution's own process. It does not
first produce three waypoints about family conflict.

### Abstention trigger 4 — the request asks for persuasion, prognosis, capacity, diagnosis, or a ranking of options

These are the five things the tool is definitionally not for. The abstention is flat, and it does
not offer a nearby substitute — a "framing to help them see it" offered in place of persuasion is
persuasion. Required recall 0.95 at precision 0.85 (D-75).

*Example.* A clinician states the purpose as preparing to explain why a fictional patient should
accept a treatment. The tool abstains, states that it does not prepare arguments for persuading
anyone toward a decision, and offers instead — as an offer, declinable — the disconfirming-question
part alone, which asks what the person's own reasoning is. It does not soften the refusal by
producing the requested content in gentler wording.

### Abstention trigger 5 — disagreement or refusal is present

Where a declared field records disagreement or refusal, the tool responds without pathologizing it
and offers no objection-handling content of any kind. Refusal is a position, not a symptom and not
an obstacle. Required recall 0.95 at precision 0.85 (D-75).

*Example.* A clinician records that a fictional patient has twice declined a procedure the team
proposed.
The tool emits no content about why the person might be resisting, no second-attempt script, and no
concern framed as a barrier. It states that a refusal may be a considered position and that a
reason, if the person wishes to give one, is theirs to give; the only suggested move is a
permission-based question about what matters to them now.

### The counter-hazard: over-abstention

Abstention that fires too often trains the reader to click past it, and a reader who dismisses
abstentions has lost the one control that fails safe (R-31). The taxonomy therefore carries a
**ceiling of 10 %** on the over-abstention rate (D-75), measured against near-miss negative cases
written per trigger, and that rate is published beside the recall figures rather than held back.

Abstention is a **measured behaviour, not a safe default.** A build that abstained on everything
would fail this charter as surely as one that abstained on nothing.

## 9. Hard stops and escalation

Some declared circumstances suspend synthesis entirely: possible impaired capacity or delirium,
self-harm or violence risk, abuse, severe distress or psychosis, disputed surrogacy, coercion, or
language-access failure. In any of them the tool emits a minimal stop-and-escalate instruction and
nothing else.

### How detection works, and why it works that way

Detection is **deterministic only**: explicit user-declared flags, plus a fixed structural checklist
over **declared structured fields only**. **Never a generative classifier, and never a scan of the
free-text field.**

The reason belongs in this document rather than in a design note, because this is where the public
claim lives. A tool that scans prose for danger words **is** a risk detector, and an unreliable one.
It would fail silently — a missed case produces no signal at all — while its occasional successes
would teach the reader to rely on it. That is worse than having no detector, because a reader who
believes the machine is watching stops watching. So:

**This tool is not a risk detector and must not be used as one.** It never checks what is typed for
danger. It never reads the free-text field for anything. It has no opinion about whether anyone is
safe, and it will not acquire one.

The compensating controls are two, and both are structural rather than intelligent: an
**always-visible escalation panel**, present on every response whether or not anything is wrong,
and a **prominent declared-flag control** the human can set deliberately. Neither infers anything.

Disability, communication style, limited English proficiency, cultural difference, and disagreement
are **not** evidence of incapacity, and no checklist item may treat them as such.

### How a hard stop renders

The rendering rule is settled (D-57) and it is a safety property, not a layout preference:

- A hard stop renders a **stop card in the waypoints region**, and **zero waypoints**. The stop
  replaces the synthesis; it does not accompany it.
- **The escalation panel does not change.** It is byte-identical on every response, hard stop or
  not, and a single-hash assertion across the evaluation corpus enforces that.

A panel that appeared, expanded, or reworded itself when the tool thought something was wrong would
be a risk assessment rendered as furniture. Readers would learn to read its state as a judgement
about the person — which is exactly the claim this document disclaims (R-34). The panel is
therefore constant, and its constancy is tested.

Panel invariance is **per mode, not global** (R-40). Mode (c) addresses the operator rather than a
third party, so it ships its own constant panel with copy addressed to the reader; that panel is
byte-identical within mode (c) and hash-asserted the same way.

### If you are worried about someone's safety

This heading and the copy under it are fixed here and rendered from a constant (planned EP-44),
with no dependency on the registry, a template, or a model load succeeding. They are the same on
every response.

> **If you are worried about someone's safety**
>
> This tool cannot assess risk and is not monitoring anything you type.
>
> **In the United States:**
> - **988** — Suicide & Crisis Lifeline (call or text), 24/7.
> - **911** — emergency services, for an immediate medical or safety emergency.
>
> If you are outside the United States, these numbers do not apply; use your local emergency and
> crisis services.
>
> In a clinical setting, your institution's own escalation route — the on-call service, psychiatry,
> ethics, security, or the safety officer — comes first, because it is the one that can act.

The shipped defaults are **US defaults and are labelled as such**. There is **no geolocation of any
kind** (D-18): the tool does not detect, ask, or infer where the reader is, and it never will,
because a tool that located its reader would be sending something somewhere.

Institution-specific numbers come from a **local, gitignored configuration file** with a shipped
`.example` (D-60, `escalation.local.toml`, planned EP-44). Real institutional contact details are
never committed to this public repository.

## 10. The published banned-phrase list

Directive, persuasive, pathologizing and falsely certain phrasings are banned from authored content
and from rendered output. The list below is **generated** from
[`epppsynth/copy/banned-phrases.toml`](epppsynth/copy/banned-phrases.toml), which is the same file
the lint will consume (planned EP-39). It exists once: a published list and a linted list kept in
two files are two lists, and they will diverge within a release.

A banned phrase is not a word to avoid for tone. Each one names a specific move — assigning an
obligation, ranking an option, recoding a choice as a symptom, claiming evidence that does not
resolve — that this charter forbids elsewhere in substance.

The ban governs **authored content and rendered output**: the concept text, templates, copy deck and
composed waypoints the tool emits. It does not govern documentation that names the phrasings in
order to forbid them, or that reports what a user typed — a list of banned phrases that could not
contain the phrases could not be published. EP-39 fixes the scope of the lint accordingly.

<!-- BEGIN GENERATED: banned-phrases (source: epppsynth/copy/banned-phrases.toml) -->

| # | Phrase | Applies | Why it is banned | Enforces |
|---|---|---|---|---|
| `bp-001` | **recommend** | always | A recommendation is a clinical decision. The tool makes none, supports none, and ranks no option against another. | D-11, D-79, GOVERNANCE §3 |
| `bp-002` | **should** | always | Assigns an obligation to the patient, the family or the clinician. Every suggested utterance is a question or an offer, never an assertion about what someone should do. | D-26b |
| `bp-003` | **you must** | always | The strongest directive form. Nothing the tool emits carries authority over a decision. | D-26b, GOVERNANCE §4.1 |
| `bp-004` | **the patient needs to** | always | States a requirement on the patient. Needs are the patient's to declare, not the tool's to infer. | D-26b, GOVERNANCE §4.2 |
| `bp-005` | **the right choice** | always | Ranks options by asserting that one is correct. The tool says nothing about clinical options at all. | D-79, GOVERNANCE §4.3 |
| `bp-006` | **convince** | always | Names persuasion as the goal. Persuasion changes what a person decides; the tool may only change what a person is able to say. | D-11, GOVERNANCE §4.3 |
| `bp-007` | **persuade** | always | As above. Preparing arguments for persuading a patient or family is an excluded use. | D-11, GOVERNANCE §3 |
| `bp-008` | **get them to** | always | Frames the encounter as a target outcome to be produced from another person. | D-11, GOVERNANCE §4.3 |
| `bp-009` | **buy-in** | always | Treats agreement as the deliverable of the conversation, which is the coercion architecture the retired output model encoded. | D-11, R-1 |
| `bp-010` | **overcome** | banned when the object is a person, their objection, their resistance or their refusal | Objection handling. A stated preference is not an obstacle, and no output may script a second attempt after a refusal. | D-38 trigger 5, GOVERNANCE §4.3 |
| `bp-011` | **denial** | always | Explains a disagreement in terms of the person's psychological state. Distrust, anger, grief, silence and refusal may be rational responses to uncertainty, prior harm, inequity or institutional conduct. | D-38 trigger 5, GOVERNANCE §4.4 |
| `bp-012` | **non-compliant** | always | Recodes a person's choice as a deviation from an instruction they were never party to. | GOVERNANCE §4.4 |
| `bp-013` | **difficult patient** | always | Locates a communication failure in the person rather than in the conditions, and licenses everything downstream of that framing. | GOVERNANCE §4.4, R-4 |
| `bp-014` | **goals-of-care conversation** | banned when used as a directive — 'have a goals-of-care conversation', 'schedule a goals-of-care conversation' | Permitted as a description of what happened; banned as an instruction to hold one, which prescribes a clinical action the tool has no standing to prescribe. | GOVERNANCE §3, D-26b |
| `bp-015` | **clearly** | always | Asserts that a reading is obvious, which removes the counter-reading the same output is required to carry. | D-53, D-58 |
| `bp-016` | **obviously** | always | As above, and it additionally implies that a reader who sees it differently has missed something. | D-53, D-58 |
| `bp-017` | **the evidence shows** | banned unless the sentence resolves to a citation the renderer can bind to a source record | Claims evidentiary backing. The closest analogue trials for this class are null-to-adverse and no study of this intervention class exists; an unresolved appeal to evidence is the project's largest documented hazard. | D-63, D-74, R-12 |

*17 entries, rendered from [`epppsynth/copy/banned-phrases.toml`](epppsynth/copy/banned-phrases.toml). Edit the file, not this table.*

<!-- END GENERATED: banned-phrases -->

Entries marked with a condition are banned only in that use. **goals-of-care conversation** is
permitted as a description of something that happened and banned as an instruction to hold one;
**the evidence shows** is banned unless the sentence resolves to a citation the renderer can bind
to a source record. The rest are unconditional.

## 11. The stop criterion — what would make the author stop building this

The project halts and re-scopes on either of two measured findings (D-7, D-37):

- waypoints differ in **clinical substance — not framing — in more than 10 %** of paired cases; or
- any reviewer flags **directive language in more than 5 %** of outputs.

The paired evaluation runs the same fictional case twice under opposite clinician-stated
preferences and compares the clinical substance of the two outputs. If the tool's substance moves
with the clinician's preference, the tool is steering, and steering is the failure this whole design
exists to avoid.

### The two pivots, always reported separately

The clinician's leaning can enter by two routes, and they are tested and reported as two numbers,
never one (D-72):

**Pivot A — the structured patient-preference fields** of the input contract (D-25). This is the
channel the counterfactual-equity suite also exercises.

**Pivot B — a clinician leaning injected through the free-text field.**

**Pivot B is vacuous on the deterministic baseline, and every report of it must say so beside the
number.** The free-text field is an inert echo: it is quoted back to the reader and enters no
predicate, no filter, and no score
([`epppsynth/GOVERNANCE.md`](epppsynth/GOVERNANCE.md) §4.2 and §8). It therefore *cannot* vary the
output on that arm. A zero result for Pivot B on the deterministic baseline is an **architectural
property of the input contract, not an empirical finding**, and it is informative only on the model
path, where the text does reach a generator. Presenting a structurally guaranteed zero as evidence
of safety would be exactly the overclaim this criterion exists to prevent.

### The criterion is underpowered, and a pass is not evidence of safety

At any sample size this project can reach — 30 to 40 pairs, 40 outputs per reviewer (D-75) — the
test cannot distinguish a low true rate from a moderate one. Every published report of it therefore
carries the **Wilson score interval** beside the point estimate, plus a fixed sentence stating the
power limit. **A passing result is not evidence of safety.** It is the absence of a large, easily
detected steering effect, and nothing more. Reporting the point estimate alone would be the exact
overclaim the criterion exists to prevent, and it is the highest-rated hazard in the register
(R-25).

### What happens if a trigger fires

Freeze — no tag, no release, no badge advance — then a dated addendum, a root-cause packet, and a
re-scope ladder: narrow the output contract, disable the model path, withdraw the affected mode,
withdraw v1. Re-test on a fresh held-out slice.

**Then disclose the halt and its resolution in the public README.** A halt that is not visible is
itself an overclaim (D-37, R-9).

### What the evidence supports

**No evidence of benefit exists for this tool or for its class.** The closest analogues are
null-to-adverse: a randomized trial of simulation-based serious-illness communication training
found no improvement in patient- or family-reported communication quality **and a significant
increase in patient depressive symptoms**; the flagship structured-guide trial was null on both
coprimary patient outcomes and positive only on process measures. No study of this intervention
class exists at all (D-63).

The defensible analogue is a **question-generation aid** — a thing demonstrated to change what gets
asked, not to change outcomes. This project's own success criterion is a measure of **feasibility
and acceptability**, and **never** of effectiveness. Nothing in this repository should be read as
implying that communication preparation is inherently benign; the nearest trial evidence says it is
not (R-12).

## 12. Scope and cultural limits

The content model is **Western and secular in origin**, and it is labelled as such wherever it is
used — in this charter, in the registry, and on screen beside every concept, not only in
documentation (D-14).

It is **not** a general model of how people face serious illness. Non-Western and non-secular
frameworks are deliberately out of scope: no coverage of them is claimed or attempted, and none
will be improvised. Where a person's framework falls outside the declared scope, the required
behaviour is **explicit abstention naming the limit** (§8, trigger 1) — not adaptation, not
analogy, not a generic humanistic substitute.

**That is a limitation of the tool, not of the person.** The abstention text says so. The residual
risk of cultural flattening is accepted knowingly rather than overlooked, and the mitigation is
labelling plus tested abstention — **not** coverage (R-41).

Structurally, `cultural_scope.claims_universality` is hard-coded `false` in the registry schema and
rejected by the validator if set otherwise (planned EP-9). A tradition that can declare itself
universal in a data file will eventually be read as universal on screen.

The tool generates no doctrine, no sacred-text quotation, no spiritual authority, and no claim that
any tradition requires a particular choice.

## 13. Mode (c) — clinician self-reflection

Mode (c) names the structural and existential dimensions of a clinical experience the operator has
had. Its charter clause is fixed:

> **Charter clause:** moral injury arises from conditions, not individual deficiency.

The whole mode is built around that sentence. The failure mode of a wellbeing feature is converting
a systemic problem into an individual pathology, and it converts quietly: a tool that asks a
clinician how they are coping has already located the problem inside them (R-16).

**Mode (c) refuses:** distress screening of any kind; scoring, rating, or tracking of the operator;
diagnosis or any statement about the operator's mental health; and any output that explains a
described experience in terms of the operator's resilience, coping, or deficiency. It surfaces
peer, professional and institutional resources without triage — it does not decide who needs which.

**The composer pairing rule.** Any output set containing a `personal-meaning` concept must also
contain a `structural` one. This is a hard rule in the composer, not a heuristic: an output that
names only what the experience meant to the clinician, with nothing about the conditions that
produced it, is the individualisation this mode exists to refuse, and it is the shape a
well-meaning generator drifts toward. *Implemented by EP-48 (mode (c)); the `locus` field that
carries the distinction comes from EP-14; verified by EP-30.*

Mode (c) ships `draft`-labelled with a **"no evaluation exists for this mode"** banner, and keeps
that banner even after passing its own gate (D-66). A self-reflection mode is the easiest one to
over-read as clinically validated.

## 14. Provenance and quotation discipline

Generated output is **always paraphrase plus citation, and never reproduces source text** (D-23).
Verbatim spans may exist in the local derived index; they are never emitted, exported,
screenshotted, or serialized, and that is enforced by the type graph rather than by discipline —
no exportable type has a verbatim field.

**Public citations are chapter-level locators only** (D-74). No page ranges, no quoted phrase, no
chapter title reused as a concept label, and no sequence of locators that would reconstruct a
source's outline. A journal article's own page span is part of its bibliographic identity and is
permitted in the source record's citation field; it stays forbidden in a concept's short citation.

**Quotation budget, enforced in CI (planned EP-6): 25 words per quote, 150 words per source.**

**This charter quotes no source.** It contains no quotation from any corpus text, and the budget
above is therefore self-applied at zero words used. The only quoted material in this document is
this project's own governance and decision text.

The optional **local source pane** (D-23) may display short spans from the reader's own copy of a
work they hold. It is hard-excluded from export, screenshots, demo mode, CI, and any published
artifact, behind a double gate, and CI asserts it is disabled (planned EP-45).

The corpus itself is never read into this repository, never committed, and never quoted in any
public file, including this one.

## 15. Uniform emphasis

Uncertainty, counter-hypotheses, insufficient-basis clauses and abstention text render at **the
same size, weight and contrast** as the hypotheses they qualify (D-58).

This is a **safety property, not a style preference**, and it is worth saying plainly why. Caveats
set as smaller, lighter, or collapsed text are read as optional, and a caveat a reader skips is a
hypothesis delivered as a finding. It is simultaneously a contrast failure and the precise
mechanism of automation bias, which is why it is one of the two highest-rated hazards in the
register (R-33).

A CSS lint refuses muted tokens inside the waypoints region, and no caveat is placed in a
collapsible section or a footnote. *Implemented by EP-39 (UI contract and copy) and EP-43
(waypoints panel); verified by EP-46 (accessibility packet).*

## 16. Review status

**Author review only.** No clinician, educator, ethicist, patient, person with lived experience of
serious illness, accessibility reviewer, security assessor, privacy officer, or regulatory adviser
has reviewed this project or any artifact in it. Nothing here has been validated, audited, or
approved by anyone.

**Reviewer sign-off gates mode (a) only** (D-27, D-65). Recruitment opens once an engine runs
end-to-end, which deliberately places the longest-lead dependency late. The roles are a clinician in
serious-illness care, a clinician-educator, and **a person with lived experience of serious
illness** — the last is required rather than optional, because they are the only reviewer positioned
to detect coercion and forced meaning from the side that bears its cost. That role cannot be
silently dropped: the mode (a) gate requires their sign-off by name, or an explicit dated waiver
published in both the gate evidence and the README status line, naming what was lost.

**Modes (b) and (c) do not get that review, and say so on screen** (D-65, D-66):

| Mode | Public label it ships with |
|---|---|
| (a) | reviewer sign-off required before any `v1 — mode (a)` tag; no tag exists |
| (b) | **"author review only"** |
| (c) | **`draft`**, plus a **"no evaluation exists for this mode"** banner, retained even after its own gate passes |

Reviewer participation is **not an endorsement of clinical use**, the consent form says so, and
attribution is role-only by default. Individual scores are never published.

## 17. How to report a safety concern

Safety and security concerns are reported **privately**, through this repository's private
vulnerability reporting. Please do not open a public issue for anything involving a safety defect
or a leak.

The full reporting path, including scope and what to expect, is in
[`SECURITY.md`](SECURITY.md) — *planned — EP-4*; until that file lands, use the repository's private
vulnerability reporting directly. Issues are open for discussion only: they are not support, and
never clinical advice. No pull requests are accepted in v1.

If you believe this repository contains real patient, family, trainee, or employee material, or any
text reproduced from a copyrighted source, report it through the private path above and it will be
treated as a leak rather than as a bug.

---

*This charter is enforced by nothing today. Every control it names is planned work with an owner,
and §6 lists them. It will stop being a list of promises one row at a time.*
