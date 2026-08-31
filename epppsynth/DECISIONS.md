# epppsynth — DECISIONS

Architecture-decision log. Numbered decisions are **settled with the project owner** in the
planning session of **2026-08-23**, across identity and scope, the clinical/ethical boundary,
conceptual foundations, content governance, inputs and outputs, architecture, local inference,
privacy, security, evaluation, interface and process, and informed by four research workstreams
(content model · engine and runtime · evaluation and safety · interface and release). Later
sessions append addenda (`> **Addendum (date, EP-n).** …`) under the decision they refine and add
new numbered decisions at the end; **nothing is rewritten**. Decisions marked *(derived)* were
resolved by applying decisions already settled rather than by a fresh choice; where a decision
supersedes or refines another, both are kept and the relation is stated inline.

Format: **D-n Title.** Decision. *Why.* *Alternatives considered.*

The hardware target throughout is generalized: **a Windows 11 x64 laptop with 64 GB RAM, an
8 GB-VRAM discrete NVIDIA GPU, and a single system volume.** No machine-specific figures are
published.

---

## Index

One row per decision, so a working session can load this block instead of the whole log.

| # | Title | Decides |
|---|---|---|
| D-1 | Planning cadence | Terse per-question answers in batches of ~10 with a checkpoint each batch. |
| D-2 | Deliberations unpublished, decisions published | Working planning notes stay out of version control; this file is the public record. |
| D-3 | Repository is public | Public from 2026-08-23 with a corpus-safe history, so every artifact is public-safe by default. |
| D-4 | Public expansion re-worded | The slug stays opaque; the public expansion drops the regulated-modality name. |
| D-5 | Three v1 modes | (a) pre-encounter reflection, (b) trainee reflection, (c) clinician self-reflection; (d) and (e) excluded. |
| D-6 | Sole accountable human | The operating clinician or trainee; output stays on their screen; no export in v1. |
| D-7 | Success = measured claim + portfolio claim | 3–5 waypoints in under 60 s plus one useful new question, on fictional cases, under a documented evaluation. |
| D-8 | Data boundary | No PHI, no real cases, no retention, no runtime network, offline-capable. |
| D-9 | Publication posture | Planning bundle public first, application code held to a gate. |
| D-10 | Corpus rights posture | Original-prose public artifact plus a gitignored local index built from the reader's own copy. |
| D-11 | Output contract replaced | Retires the persuasion-shaped model for facts/unknowns, plural hypotheses, disconfirming questions, neutral framing. |
| D-12 | Publication mechanics | Source public as built; no releases, tags or demo until the evidence gate. |
| D-13 | One engine, three purpose profiles | Shared engine and contracts, per-mode prompts and eval sets, built a → b → c. |
| D-14 | Content traditions, declared Western-secular | Four named traditions as content, three as critique lenses; out-of-scope frameworks trigger abstention. |
| D-15 | Concept registry | YAML/JSON registry with stable IDs, typed relations and per-concept metadata; no ontology, no graph DB. |
| D-16 | Local index contents | Embeddings and verbatim spans from the reader's own copy, local and gitignored only. |
| D-17 | Deterministic baseline first | The baseline ships as default and permanent fallback; the LLM is gated on beating it. |
| D-18 | Hard stops deterministic only | Declared flags plus a checklist, never a classifier; always-visible escalation panel; not a risk detector. |
| D-19 | Trainee mode non-surveilling | Local only, no accounts, scoring, retention, export or employer visibility. |
| D-20 | Mode (c) scope | Names structural and existential dimensions; refuses screening, scoring and diagnosis. |
| D-21 | Stack | Python core as a library with a CLI, plus a small loopback web UI, threat model from the start. |
| D-22 | Roadmap sizing | Sibling-project sizing verbatim: S/M/L = 30 min / 1 h / 2 h, split when in doubt. |
| D-23 | Verbatim spans | Never emitted; optionally displayed in a local-only source pane. |
| D-24 | Public wording | Fixes the expansion and status line; the tool is for private local use, the repo is a public artifact. |
| D-25 | Input contract | Structured enums plus one free-text field; protected traits may change framing only, enforced by counterfactual tests. |
| D-26 | Preserved output functions | Four functions survive the retired model; every suggested utterance is a question or an offer. |
| D-27 | Review status | Author-only now; recruited role-identified reviewers become the release gate. |
| D-28 | Licensing split | Apache-2.0 for code, CC BY 4.0 for content, plus NOTICE, CITATION.cff and a rights table. |
| D-29 | Employment/IP clearance | A clearance checkpoint gates the first public release or tag. |
| D-30 | Model storage and download rules | Models live at `C:\epppmodels`, one at a time, ≤ ~8 GB each, never in Git/LFS. |
| D-31 | Runtime family | Native Windows llama.cpp GGUF; hash-verified weights, no remote code, no pickle formats. |
| D-32 | v1 UI | One loopback page, no persistence, WCAG 2.2 AA, origin/CSRF plus a one-shot launch token. |
| D-33 | Third-party use not intended | Personal tool, public source; no installability or supported-machine claim in v1. |
| D-34 | Contribution posture | No PRs in v1; issues open; SECURITY.md and CODE_OF_CONDUCT.md present. |
| D-35 | Mode (a) release-gate evidence | Eight required evidence items before any `v1` tag. |
| D-36 | Eval scenario provenance | Authored and reviewed scenarios, provenance-tagged, with an author-only frozen held-out set. |
| D-37 | Stop criterion operationalized | Paired opposite-preference runs; halt above 10 % substance divergence or 5 % directive-language flags. |
| D-38 | Abstention taxonomy | Five required abstention triggers, each with an eval case. |
| D-39 | Phase structure | P0 … P7, ~40–50 briefs, ~3 months; evaluation precedes the LLM work. |
| D-40 | Repo layout and canonical docs | Fixes the package, roadmap, licensing and governance file set. |
| D-41 | Corpus ingest becomes a module | The EPUB→markdown pipeline moves into the package as a CLI subcommand. |
| D-42 | CI | GitHub Actions on `windows-latest`, pinned actions, no-model test path, secret/PHI/licence scanning. |
| D-43 | Site integration | Fix the portfolio card now; all other site work is one late-phase brief. |
| D-44 | Embedding models are models | D-31's verification and storage rules apply to embedding models identically. |
| D-45 | Lens veto is conditional | A critique lens may block a concept; overriding requires a published dated rationale. |
| D-46 | Withdrawn concepts are published | Blocked and deprecated concepts stay visible with the blocking finding attached. |
| D-47 | Registry size | ≈ 40 concepts, gated on a coverage dry-run; honest thinness beats padding. |
| D-48 | Confidence placement | `confidence` shows in the provenance drawer only, never beside a waypoint. |
| D-49 | Free-space floor | 250 GiB binary, checked before and after every write. |
| D-50 | Template licensing | `templates/**` is CC BY 4.0 because their value is the wording. |
| D-51 | Index location | The local index lives at `C:\epppindex`, separate from the model root. |
| D-52 | Local logging | Off by default, hash-only when enabled, never in trainee mode. |
| D-53 | Waypoint is a render | Never a stored object; counter-reading and insufficient-basis are required composer fields. |
| D-54 | LLM is a renderer, not an author | It sees selected IDs, authored paraphrases and the user's quote; unbound sentences are dropped. |
| D-55 | Injection control | Output-side structural validation is the primary control, stated as an architectural invariant. |
| D-56 | Determinism vocabulary | Public text never calls the LLM path deterministic. |
| D-57 | Escalation panel invariance | The panel renders byte-identically on every response; hard stops render inside the waypoints region. |
| D-58 | Uniform waypoint typography | Uncertainty and abstention render at the same size, weight and contrast as hypotheses. |
| D-59 | Maturity badge | A static README string that CI resolves to an evidence file and fails if unticked. |
| D-60 | Interface and doc additions | CONTRIBUTING, in-repo clinical narrative, first-run interstitial, local escalation config, vendored htmx with a tested fallback. |
| D-61 | Modes (d) and (e) excluded | Excluded with seven named preconditions, not deferred. |
| D-62 | Source rights flags | WHO guidance referenced never ingested; SAMHSA, AHRQ and the FDA CDS guidance flagged unverified. |
| D-63 | Evidence standing | Closest analogue trials are null-to-adverse; the claim is feasibility and acceptability, never effectiveness. |
| D-64 | Reviewer roles and timing | Clinician, educator and a person with lived experience, recruited only once the engine runs end-to-end. |
| D-65 | Sign-off scope | Reviewer sign-off gates mode (a) only; (b) and (c) ship author-reviewed with explicit public labels. |
| D-66 | Mode (c) labelling | Ships `draft` with a "no evaluation exists for this mode" banner even after its own gate. |
| D-67 | Accessibility is a gate item | The accessibility packet is the eighth mode-(a) gate item. |
| D-68 | UI stack | Starlette + Jinja2 + vendored htmx + hand-written CSS; no npm, no build step, no CDN. |
| D-69 | Public wording approved | Intended use, excluded uses, what it does not know, and status ship as drafted. |
| D-70 | Runtime implementation | `llama-cpp-python` in-process; Ollama rejected for auto-update and login-start service behaviour. |
| D-71 | Pre-existing model cache kept | The third-party cache stays, outside the project budget; no purge tool is built. |
| D-72 | Stop-criterion pivots | Both the structured-preference and free-text clinician-leaning channels, reported separately. |
| D-73 | Field sensitivity declaration | Every input field is `invariant`, `clinically-load-bearing`, or framing-plus-one-additive-waypoint. |
| D-74 | Citation and quotation limits | Chapter-level locators only; ≤ 25 words per quote, ≤ 150 per source, CI-enforced. |
| D-75 | Numeric thresholds | Ratified as a table and revisited at the evaluation-phase re-plan. |
| D-76 | Repository settings | Issues on with a no-support template; Discussions, Wiki, Projects off; private vulnerability reporting on. |
| D-77 | Reviewer study is not research | Not intended for publication and the consent form says so; the escalation trigger is named in governance. |
| D-78 | Storage floor and ceiling | A 250 GiB machine floor and a 25 GB project ceiling; expected real usage ≈ 8–12 GB. |
| D-79 | Output contract reduced to three parts | The values-to-options part is deleted rather than shipped empty; the no-ranking prohibition stands. |

---

## Purpose & scope

**D-3 The repository is public.** Public from 2026-08-23. History was erased and re-created and
the ignore rules for the copyrighted corpus were configured before any commit (verified: no
corpus path appears in any commit). *Consequence:* every planning artifact, issue, commit
message, fixture, screenshot and CI log is public-safe by default. The portfolio card's "Private"
label is stale copy, not a fact — corrected under D-43. *Why:* the public repository is the
portfolio artifact, so the safety posture follows from it rather than being retrofitted to it.
*Alternatives:* private until a release gate; public with the original history preserved.

**D-4 Public expansion re-worded away from the clinical modality; slug kept.** `epppsynth`
remains an opaque handle; the public expansion becomes a non-modality phrase. *Why:* "existential
psychotherapy" names a regulated modality the tool must disclaim, and a name that asserts it
undercuts every disclaimer downstream. *Alternatives:* rename the project outright; keep the
modality wording behind a disclaimer. *Exact wording fixed by D-24.*

**D-5 v1 covers three modes.** (a) clinician pre-encounter reflection on synthetic/fictional
cases; (b) trainee education and reflection; (c) clinician self-reflection, moral-injury
adjacent. Patient-specific point-of-care (d) and patient/family-facing (e) are **excluded release
classes** (see D-61). *Why:* the three included modes share an accountable operator who is a
clinician; the excluded two do not. *Alternatives:* mode (a) only; (a) plus (b); include (d)
behind stronger controls. *Internal structure resolved by D-13.*

**D-7 Success = a measured claim plus a portfolio claim.** Measured: a reader gets 3–5 waypoints
in under 60 s and reports at least one useful question not already considered, on fictional
cases, under a documented evaluation. Portfolio: a rigorous, safety-aware design artifact
regardless of measured usefulness. **Stop criterion:** any evaluation finding that outputs
*reliably steer toward a clinician-preferred decision* halts the project for re-scoping. *Why:*
two honest claims are worth more than one inflated one. *Alternatives:* usage metrics; reviewer
satisfaction; portfolio value alone. *Operationalized by D-37; the measured claim is relabelled
by D-63 as feasibility and acceptability, never effectiveness.*

**D-13 One engine, three purpose profiles, built a → b → c.** Shared conceptual model, input
contract and output contract; per-mode prompts, guardrails, escalation copy and eval sets. Each
mode's eval set is its own release gate, so a failing mode is withheld without blocking the
others. *Why:* three modes would otherwise become three products with three hazard sets.
*Alternatives:* three separate engines; one undifferentiated engine; ship (a) only and defer the
rest.

**D-24 Public wording and status line.** Expansion = "existential **perspectives** for physicians
& patients". Status line = "Design and planning artifact — v1 in progress; no release, no demo,
no validation." The tool itself is intended for **private, local use by the author**; the
repository is public as a source and portfolio artifact. *Why:* the wording has to cover all
three modes without overclaiming any of them. *Alternatives:* a modality-naming expansion; a
wellbeing-only hook; no expansion at all. *Third-party consequences settled in D-33; the full
public copy approved in D-69.*

**D-33 Third-party use is not an intended use in v1.** "Personal tool, public source": the docs
explain the design; there is no installability guarantee and no supported-machine claim; issues
are open for discussion only. Best-effort installability — a clean non-admin Windows install from
a path containing spaces and non-ASCII characters, as an acceptance test — is v1.x or beyond.
*Why:* resolves the tension between private local use and a public repository without taking on a
support burden the evidence does not justify. *Alternatives:* a fully supported install; a
private repository; a distributed binary.

**D-63 Evidence standing: the closest analogues are null-to-adverse (derived).** The nearest
trial evidence is null-to-adverse — a randomized trial of simulation-based serious-illness communication skills training found no improvement
in patient-reported communication quality **and a significant increase in patient depressive
symptoms**; the Serious Illness Care Program trial was null on its coprimary outcomes, with
positive process measures only. The defensible analogue for this tool is a **question-generation
aid**. D-7's success criterion is therefore a **feasibility and acceptability** measure and never
an effectiveness claim, and a plain no-evidence statement appears in the public README. *Why:*
the field's own strongest tests do not support a benefit claim, and documentation that implied
one would be this project's single largest hazard. *Alternatives:* cite the positive process
findings only; omit the analogue literature; claim benefit and caveat it.

**D-69 Public wording approved as drafted.** The Intended use / Excluded uses / What it does not
know / Status blocks ship as drafted, amendable at the mode-(a) gate. *Why:* the wording is
conservative enough to survive the gate and specific enough to be tested against. *Alternatives:*
defer all public copy to the gate; ship a minimal disclaimer only.

---

## Clinical/ethical boundary

**D-6 The sole accountable human is the operating clinician or trainee.** Output never leaves
their screen; there is no export in v1. Export and sharing are deferred to v1.x behind an
explicit decision. *Why:* an artifact that can be forwarded acquires an authority the tool has
not earned. *Alternatives:* export with a watermark; a shareable session link; print support.

**D-18 Hard stops are deterministic only.** Explicit user-declared flags plus a
keyword/structural checklist — **never a generative classifier** — with an always-visible
escalation panel and the flat public claim *this tool is not a risk detector and must not be used
as one*. Escalation resources are shipped, clearly-labelled US defaults (988, emergency services)
**plus** local configuration for institution-specific numbers; no geolocation. *Why:* a
probabilistic risk detector fails silently and invites reliance the tool cannot support.
*Alternatives:* a classifier with a confidence threshold; no hard-stop path at all; geolocated
resources. *Rendering fixed by D-57; the local config file by D-60.*

> **Addendum (2026-08-31, owner ruling OD-5).** D-18 fixed *which* resources appear and D-57 fixed
> the heading; the panel's **exact wording** — the 988 and 911 lines and the "outside the United
> States" sentence — was authored at EP-3 and lived only as `SAFETY.md` §9 prose, changeable by any
> brief that edits that file. Crisis-resource copy is the highest-consequence string in the product,
> so it is **settled here as a decision**: changing a character of it requires a further dated
> addendum under this decision, and EP-44's constant is a **transcription**, not an authored string.
>
> The text itself is not duplicated here, because a published copy and a rendered copy kept in two
> files are two copies and they drift. It is pinned instead:
>
> - **Canonical location.** `SAFETY.md` §9, the block quote under the heading *If you are worried
>   about someone's safety*.
> - **Fixed at.** commit `7a5ecbb` (EP-3, 2026-08-31).
> - **Extraction rule.** The contiguous run of quoted lines beginning `> **If you are worried about
>   someone's safety**`; strip one leading `> ` (or a bare `>` on a blank quoted line) from each;
>   join with `LF`; no trailing newline. **13 lines, 592 bytes UTF-8.**
> - **SHA-256 of the extracted text.** `070d3915af29b80d1b7d1912b475efd541a165f82cd2210753585aac9f5ef37f`
>
> EP-44 renders the panel from a constant whose text hashes to that value, and asserts the equality
> against `SAFETY.md` §9 rather than holding a second copy of the words. A change to §9 that is not
> accompanied by a new addendum here is a **failure**, not an edit.

**D-19 Trainee mode is strictly local and non-surveilling.** No accounts, no scoring, no
retention, no export, no employer visibility; voluntary use only; a written non-surveillance
guarantee in the docs. Trainee-controlled opt-in local retention is v1.x; educator-visible
artifacts are excluded. *Why:* a reflection tool that can be observed is a performance
instrument, and trainees are the least able to decline it. *Alternatives:* educator dashboards;
anonymized aggregate reporting; opt-out rather than opt-in. *Reinforced structurally by D-52.*

**D-20 Mode (c) names structural and existential dimensions of a clinical experience.** It
explicitly refuses distress screening, scoring and diagnosis, and surfaces peer, professional and
institutional resources without triage. **Charter clause:** moral injury arises from conditions,
not individual deficiency. *Why:* the failure mode of a wellbeing feature is converting a
systemic problem into an individual pathology. *Alternatives:* a validated distress instrument; a
symptom checklist; a referral triage flow.

**D-38 Abstention taxonomy — five required behaviours, each with an eval case.** The tool abstains
when (1) the person's framework falls outside the declared Western-secular scope; (2) there is
insufficient basis in the supplied context; (3) any hard-stop flag is present; (4) the request
asks for persuasion, prognosis, capacity, diagnosis, or ranking of options; and (5) disagreement
or refusal is present — in which case it responds without pathologizing and offers no "overcoming
objections" content. *Why:* abstention here is a safety feature, not a politeness feature, so it
has to be tested rather than asserted. *Alternatives:* a single generic "insufficient
information" path; confidence-threshold abstention; graceful degradation with caveats.

**D-61 Modes (d) and (e) are excluded, not deferred (derived).** `GOVERNANCE.md` states them as
**excluded with seven named preconditions**, and records that the author will not attempt them as
a solo project. *Why:* "deferred" invites drift; "excluded with named preconditions" is auditable
and can only be reversed in public. *Alternatives:* deferral to a later version; silence.

---

## Conceptual foundations

**D-14 v1 content traditions, declared Western-secular, enforced by tested abstention.** Content =
Yalom's four givens (labelled as **one tradition among several**) + serious-illness communication
evidence + trauma-informed care (SAMHSA) + the moral-injury literature. Narrative medicine,
generalist spiritual care and disability-community critique are **critique lenses** applied during
authoring and review, not content. Non-Western and non-secular frameworks are **deferred
indefinitely**. *Consequence, which must appear in the public charter:* the model is
Western-secular in origin and is labelled as such; where a user's framework falls outside it, the
correct behaviour is **explicit abstention and a note of the limit**, never improvisation. The
mitigation for cultural flattening is labelling plus tested abstention (D-38, trigger 1) — **not**
coverage. The residual risk is accepted knowingly, not overlooked. *Why:* a single-tradition
substrate presented as universal is the sharper harm; a bounded substrate that says so and stops
is defensible. *Alternatives:* add non-Western traditions in v1.x; commission additional
traditions before release; present the substrate as tradition-neutral.

**D-45 A critique lens holds a conditional veto (derived).** A lens may set a concept `blocked`;
overriding a block requires a published, dated `override_rationale`. A lens may not author
replacement content and may not block a release. *Why:* an advisory-only lens is tokenism, while
an absolute veto hands release control to a reviewer with no accountability for it.
*Alternatives:* advisory comments only; an absolute veto; a veto with private override.

**D-46 Blocked and deprecated concepts are published (derived).** They appear in the rendered
markdown under a "withdrawn / not adopted" section with the blocking finding attached. *Why:*
what was rejected and why is part of the content model's evidence. *Alternatives:* delete them;
keep them only in unpublished notes.

**D-47 Registry size target ≈ 40 concepts, gated on a coverage dry-run (derived).** *Why:* a thin
registry that abstains honestly beats a padded one that always has something to say.
*Alternatives:* an exhaustive registry; no target at all.

---

## Content model & governance

**D-15 Content representation = a YAML/JSON concept registry.** Stable IDs, typed relations, and
per-concept provenance / rights / confidence / cultural-scope / review-status /
contested-interpretations, rendered to human-readable markdown. No formal ontology, no graph DB.
The canonical schema uses a typed-ID scheme over five concept types (`given` / `function` /
`principle` / `condition` / `caution`) with typed relations, and additionally requires a `family`
edge (which the engine's diversity constraint consumes), a **closed** `question_intent`
enumeration, and a per-field `sensitive` flag. *Why:* the metadata, not the formalism, is what the
rights and abstention rules actually need. *Alternatives:* an OWL/RDF ontology; a graph database;
plain markdown with front-matter; a flat prose document.

**D-16 The local index may contain embeddings and verbatim spans** drawn from the reader's own
legally obtained copy. Strictly local, gitignored, never distributed, never present in CI. *Why:*
the reading input is a private artifact; the published artifact is original prose.
*Alternatives:* no local index; a shipped index; embeddings but no spans. *Display rule fixed by
D-23; location by D-51.*

**D-23 Verbatim spans are never emitted and only optionally displayed.** Generated output is
always paraphrase plus citation. An optional **local-only source pane** may show short spans from
the reader's own copy; it is hard-excluded from export, screenshots, demo mode, CI, and any
published artifact. *Why:* separates what the reader may look at from what the system may
produce. *Alternatives:* no source pane; spans in generated output with attribution; spans behind
a licence check.

**D-48 `confidence` is shown in the provenance drawer only (derived).** Never beside a waypoint.
*Why:* a numeric confidence next to a suggestion is read as a probability of correctness and
amplifies automation bias. *Alternatives:* inline confidence badges; a per-response confidence
score; dropping the confidence field entirely.

**D-51 The local index lives at `C:\epppindex`, separate from `C:\epppmodels` (derived).** *Why:*
a different rights class, independently purgeable and independently excludable from backups.
*Alternatives:* one root for both; the index inside the repository working tree.

---

## Inputs & output contract

**D-11 The output contract is replaced.** The "Hidden Dynamic / Empathic Wedge / Bridge" model is
retired. The replacement is: *known facts and unknowns* · *multiple possible concerns plus a
counter-hypothesis plus an "insufficient basis" clause* · *disconfirming, permission-based
questions* · *neutral framing connecting stated values to clinician-verified options*. *Why:* the
original framing optimized for leverage and agreement, which is a coercion architecture.
*Alternatives:* keep the original with guardrails; a single-hypothesis output; a free-text
summary. *Which functions had to survive is settled in D-26.*

> **Addendum (2026-08-23, planning).** Superseded in part by **D-79**: the fourth part of the output
> contract is deleted. The contract is three parts.

**D-25 Input contract = structured enums plus one optional free-text field.** v1 fields: role ·
encounter temporality · stated communication/information preference · stated decision-sharing
preference · self-described framework · uncertainty tolerance · illness stage ·
language/interpreter need. Every field carries **unknown / not relevant / prefer-not-to-answer**.
The free-text field carries **what the person actually said**; it is quoted and reasoned about,
never mined for identity inference. Machine-checkable rule: protected traits may change
**communication framing only, never clinical content**, enforced by a **counterfactual test
suite** that flips each sensitive field and asserts equivalence of clinical substance. *Why:*
free-form intake invites demographic inference; enums make the anti-stereotyping rule testable.
*Alternatives:* free-text intake with a classifier; a fixed case template; no structured input.
*Refined by D-73.*

**D-26 Functions preserved from the retired output model.** (a) Name plausible unspoken concerns —
plural hypotheses plus a counter-hypothesis plus "insufficient basis"; (b) suggest an opening move
— **every suggested utterance is a question or an offer, never an assertion about what the patient
feels or should do**; (c) connect stated values to clinician-verified options — neutrally, with no
ranking, no suppression and no advocacy; (d) name the clinician's own reaction (mode (c) only).
*Retired framings:* "Hidden Dynamic (Diagnosis)", "Empathic Wedge", "Consensus Generation".
*Why:* the useful work of the original model was hypothesis generation, not persuasion.
*Alternatives:* drop (b) entirely; keep the original naming with new semantics.

> **Addendum (2026-08-23, planning).** Clause (c) — connecting stated values to clinician-verified
> options — is withdrawn with the fourth output part (**D-79**). Clauses (a), (b) and (d) stand
> unchanged, and the prohibition on ranking, comparing or advocating among options remains in force.

**D-53 A waypoint is a render, never a stored object (derived).** `counter_reading` and
`insufficient_basis_clause` are structurally required fields of the composer. *Why:* if they are
optional fields they will be empty in exactly the outputs where they matter most.
*Alternatives:* optional fields with a lint; a stored waypoint object with a retention rule.

**D-54 The LLM is a renderer, not an author (derived).** It receives selected concept IDs plus
authored paraphrases plus the user's quote — never the registry wholesale, never the index, never
a raw span. Claim-binding validation drops sentences not bound to a supplied claim; past a drop
threshold the whole response falls back to templates. *Why:* keeps the substance authored and
auditable while the model handles wording only. *Alternatives:* retrieval-augmented generation
over the index; free generation with a fact-check pass; no LLM path at all.

**D-55 Output-side structural validation is the primary prompt-injection control (derived).**
Schema validation plus citation resolution plus a question-or-offer parse, stated as an
**architectural invariant**, not as a mitigation. *Why:* input sanitisation of free text is not a
control that can be relied on; the shape of the output is. *Alternatives:* input filtering;
instruction-hierarchy prompting; a guard model.

**D-73 Every D-25 field carries a three-way sensitivity declaration.** `invariant` /
`clinically-load-bearing` / `framing-plus-one-permitted-additive-waypoint` (the interpreter-need
case), each with a written rationale in the registry. *Why:* a flat "sensitive" flag cannot
express that interpreter need legitimately adds a waypoint while race must change nothing.
*Alternatives:* a binary sensitive flag; per-field ad-hoc rules; no declaration.

---

## Architecture & stack

**D-21 Stack = a Python core plus a small local loopback web UI in v1.** uv-managed; the
deterministic core is a library; a CLI is present; the threat model is included from the start.
*Why:* the core has to be usable and testable without the UI, and the UI raises a trust boundary
that must be modelled before it ships. *Alternatives:* CLI only; a desktop GUI; a notebook
interface; a hosted web app.

**D-40 Repo layout and canonical docs.** Package directory (`pyproject.toml`, `src/`, `tests/`,
`docs/`) · `roadmap/` (`README.md` master table + `EP-n-*.md` briefs + `final-roadmap.md`) · an
ignored corpus directory · an ignored local working-notes directory · `tools/` · root
`README.md`, `LICENSE` (Apache-2.0), `LICENSE-CONTENT` (CC BY 4.0), `NOTICE`, `CITATION.cff`,
`CODE_OF_CONDUCT.md`, `SECURITY.md`, `SAFETY.md`, `PRIVACY.md`, `CLAUDE.md`; canonical
`DESIGN.md`, `GOVERNANCE.md`, `DECISIONS.md`. *Why:* matches the sibling projects' conventions, so
the roadmap process transfers unchanged. *Alternatives:* a flat layout; a src-less package; docs
in a separate repository. *Extended by D-60.*

> **Addendum (2026-08-23, planning).** Path ambiguity between the research workstreams is resolved
> in favour of package-relative paths, fixed once so briefs cannot diverge: `epppsynth/docs/` for
> package documentation (`docs/adr/`, `docs/evidence/`, `docs/rights.md`), `epppsynth/registry/` for
> the concept registry and `sources.yaml`, and `release-evidence/<tag>/` at the repository root for
> release evidence. There is no repository-root `docs/` directory.

**D-41 The corpus pipeline moves into the package as the corpus-ingest module (derived).** The
existing EPUB→markdown script becomes a `corpus/` module inside the package, reachable as a CLI
subcommand, because the local-index path (D-10(ii), D-16) makes corpus ingest a product path
rather than a one-off script. `tools/` is retained only if a non-package utility later needs it.
Generalizing the pipeline's hard-coded single-source spine is **parked**. *Note:* it currently
depends on pandoc, which is **not assumed present** — the ingest packet must either vendor a
pure-Python path or document pandoc as an explicit, owner-confirmed prerequisite.
*Alternatives:* keep it as a standalone script; delete it and re-author; generalize it now.

**D-68 UI stack = Starlette + Jinja2 + one vendored htmx (0BSD) + hand-written CSS.** No npm, no
build step, no CDN; a mandatory, tested no-JS full-page-POST fallback. *Why:* the divergence from
the sibling project's Streamlit precedent is deliberate and rests on **architectural control** —
over headers, origin checks, markup and typography — **not** on any verified accessibility claim
about Streamlit. *Alternatives:* Streamlit; FastAPI + React; Flask + Bootstrap; a native desktop
shell.

---

## Local inference

**D-17 Deterministic baseline first; the local LLM is gated on a measured benchmark.** The
baseline ships as the default and as a permanent fallback; an LLM path is added only behind a
measured benchmark gate and only if it beats the baseline on the eval sets. The baseline is also
the anti-hallucination control arm. *Why:* it makes the LLM's contribution measurable instead of
assumed. *Alternatives:* LLM-first; LLM-only; no LLM path.

**D-30 Read-only hardware probing authorized; models live at `C:\epppmodels`.** Probes are
read-only and non-elevated. Weights are never in Git or LFS. Downloads happen **one model at a
time, ≤ ~8 GB each, confirmed individually**. Where usable weights are already present locally,
reuse is preferred over re-download provided revision and hash verify. *Why:* the local-inference
plan cannot be written against assumed hardware. *Alternatives:* trust the vendor spec sheet; an
elevated system inventory; no probing. *The free-space reserve is tightened by D-49 and the
storage envelope superseded by D-78.*

**D-31 Runtime = native Windows plus llama.cpp-based GGUF; no WSL, no containers.** The model list
is earned by the benchmark packet, not chosen up front. **Hard rules:** weights verified by
revision **and** file hash; remote code execution disabled; no pickle-format weights. *Why:*
native execution keeps the offline and no-listener guarantees checkable. *Alternatives:* WSL2 +
vLLM; Docker; a hosted API; PyTorch/transformers with safetensors. *Implementation fixed by D-70;
extended to embedding models by D-44.*

**D-44 Embedding models are models (derived; confirmed at the discovery gate).** The local index
needs an embedding model, so D-31's rules — revision plus hash verification, no remote code
execution, no pickle formats, storage under the model root, one-at-a-time confirmed download —
apply to it identically. *Why:* an embedding model is the easiest supply-chain gap to leave open.
*Alternatives:* treat embedding models as an ordinary dependency rather than a governed asset.

**D-49 The free-space floor is 250 GiB, binary, checked before *and* after every write
(derived).** *Why:* the stricter binary reading plus the post-write check closes the gap where a
single large download crosses the line mid-operation. *Alternatives:* 250 GB decimal; a pre-write
check only; a percentage-based floor. *Placed in context by D-78.*

**D-56 Public text never describes the LLM path as deterministic (derived).** "Deterministic"
attaches to the baseline only. *Why:* the two paths make different guarantees, and one word
blurring them would misdescribe the product. *Alternatives:* call the whole system deterministic
with a caveat; avoid the word entirely.

**D-70 Runtime implementation = `llama-cpp-python`.** MIT-licensed, in-process, no daemon, no
listener, an official Windows CUDA wheel index, and in-process GBNF/JSON-schema constrained
decoding. **Ollama is rejected:** on Windows it auto-downloads updates and registers a
login-start service, both fatal to the no-runtime-network posture of D-8. The `llama-server`
binary remains a documented fallback only if the local-inference spike finds the target GPU's
compute capability unsupported. *Alternatives:* Ollama; llama-server as primary; a local desktop
app's server mode; ONNX Runtime GenAI.

**D-71 The pre-existing third-party model cache is kept, not purged.** It is not this project's
storage and is excluded from the project budget. No purge tool is built — but the seven
purge-safety rules ship as an ADR regardless. *Why:* deleting another application's assets is
outside this project's remit, while the safety rules are cheap and stop a future purge from
escaping the model root. *Alternatives:* purge it to free space; adopt it as the project's model
root; build a purge tool.

**D-78 Storage has a floor and a ceiling, not one number.**
- **Floor (machine):** ≥ **250 GiB** free on the system volume at all times, checked before *and*
  after every write. This protects non-project use; it is not a project allocation.
- **Ceiling (project):** the combined footprint of `C:\epppmodels` and `C:\epppindex` is capped at
  **25 GB**, warned at 20 GB, and hard-stopped at 25 GB unless raised in writing.
- **Expected real usage:** one ≤ 5 GB generation model + one small embedding model + a local index
  of roughly 1–2 GB + JSON packets ⇒ **≈ 8–12 GB**.

*Supersedes* the earlier "working envelope" framing derived from measured free space, which
described headroom rather than intent; the project never claims the machine's spare capacity as
its budget. The pre-existing third-party cache (D-71) sits outside both figures. *Alternatives:* a
single envelope number; no ceiling; a percentage-of-disk allocation.

---

## Data, privacy & rights

**D-8 Data boundary (v1).** No PHI, no real cases, manifestly fictional scenarios only, no
retention of prompts or outputs, no runtime network, offline-capable (not air-gapped). *Why:* the
boundary is what makes every other safety claim checkable. *Alternatives:* de-identified real
cases; opt-in retention; an air-gap requirement; cloud inference.

**D-10 Corpus rights posture = both paths.** (i) The public artifact is a hand-authored, cited,
**original-prose** conceptual model — concepts plus short citations, no substantial quotation, no
redistributable derived text. (ii) The local path is a pipeline that builds a **gitignored** local
index from the reader's own legally obtained copy and ships no derived content; the corpus is used
as reading input during authoring only. *Why:* the conceptual substrate is copyrighted and the
repository is public; the two paths keep both facts true. *Alternatives:* a public repository with
a derived text index; a private repository; public-domain sources only. *Concretized by D-15,
D-16, D-23, D-62 and D-74.*

**D-28 Licensing = Apache-2.0 (code) + CC BY 4.0 (content model, ontology, docs)**, with `NOTICE`,
`CITATION.cff`, and a per-source rights table. *Why:* the content model is the reusable artifact
and deserves a content licence rather than a code licence. *Alternatives:* MIT throughout;
CC BY-SA for content; all-rights-reserved content.

**D-50 `templates/**` is CC BY 4.0 (derived).** *Why:* their value is the wording, which makes them
content and not code. *Alternatives:* Apache-2.0 along with the rest of the source tree.

**D-52 Local logging is off by default, hash-only when enabled, and never present in mode (b)
(derived).** *Why:* any log of a reflection session is a surveillance artifact, and the trainee
guarantee of D-19 has to hold structurally rather than by configuration. *Alternatives:* opt-in
plaintext logging; logging with redaction; always-on hash logging.

**D-62 Normative guidance is referenced, never ingested — and two source families are flagged
unverified (derived).** The WHO guidance on large multi-modal models (**CC BY-NC-SA 3.0 IGO**) is
**referenced, never ingested**; a `reuse_class` field carries the reuse terms per source. **SAMHSA
and AHRQ reuse terms are UNVERIFIED** — both returned HTTP 403 to retrieval — and are held at
`reference-only-pending-rights-check` until an early-phase rights packet clears them. **The FDA
clinical-decision-support final guidance (2026-01-06, superseding the 2022 guidance) primary PDF
is UNVERIFIED** and must be read before any public intended-use language ships. *Why:* an NC/SA or
unverified-federal source ingested into a CC BY 4.0 artifact is licence contamination that is
expensive to unwind later. *Alternatives:* ingest federal text as presumed public domain; ingest
under fair use; omit normative guidance entirely.

**D-74 Citation and quotation limits.** Public short citations are **chapter-level locators
only** — no page ranges — plus the standing bans: no quoted phrase, no chapter title used as a
concept label, and no locator sequence that reconstructs a source's outline. Quotation budget:
**≤ 25 words per quote and ≤ 150 words per source**, enforced in CI. *Why:* the stricter locator
granularity keeps the published artifact from functioning as a navigable derivative of the source.
*Alternatives:* page-range locators under the same word budget; no locators at all;
paraphrase-only with no citation.

> **Addendum (2026-08-31, owner ruling OD-6).** EP-2's step-10 sweep found that
> `tools/epub_to_md_pipeline.py` published a named source book's title, its author, and its **full
> chapter-title table** in a tracked, public file — the outline-reconstruction pattern this decision
> bans and the rights-leakage failure mode `DESIGN.md` §6.1 **Y-8** names, guarded until now for the
> concept registry but not for `tools/`. Ruled **live, not latent**: the corpus rule (D-10) is one of
> the two rules that override any brief, so the exposure is closed now rather than waiting for EP-22
> to move the pipeline into the package.
>
> Closed on 2026-08-31 by moving the spine — book title, author, and the per-chapter title table —
> out of the tracked file into a **gitignored local configuration file**
> (`tools/spine.local.json`), shipped with a placeholder `tools/spine.local.json.example`, on the
> `escalation.local.toml` pattern D-60 already establishes. The pipeline reads the spine at run time
> and exits with a pointer to the example if it is absent; no source-identifying string remains in
> the tree.
>
> Consequences. **EP-6** treats a tracked chapter-title sequence as a finding — a sequence of three
> or more title-shaped strings adjacent to a chapter ordinal, in any tracked file — so the pattern
> cannot return by a different route. **EP-22** inherits an already-external spine and must keep it
> external when the pipeline becomes a package subcommand. The modality-sweep exemption that
> `tools/epub_to_md_pipeline.py` carried under OD-10 **expires with this ruling**; the file is no
> longer exempt.

---

## Security & supply chain

> **Addendum (2026-08-23, planning).** A journal article's own page span is part of its bibliographic
> identity rather than an interior locator, so it is permitted in the source record's citation field
> and remains forbidden in any concept's short citation. Book citations stay chapter-level.

**D-34 Contribution posture: no PRs in v1.** Issues are open; `SECURITY.md` carries a private
reporting path; `CODE_OF_CONDUCT.md` is present. Contributor attestation and PR intake are
revisited once reviewers exist (D-27). *Why:* accepting code into a safety-argued artifact with no
review capacity would weaken the argument. *Alternatives:* open PRs with a CLA; PRs to a staging
branch; a closed repository.

**D-42 CI = GitHub Actions on `windows-latest`.** Minimum token permissions; no secrets in
fork-triggered workflows; third-party actions pinned to commit SHAs; a deterministic **no-model**
test path only; plus secret, PHI-pattern and licence scanning. *Why:* CI is the enforcement point
for the data boundary and the rights rules, so it must not need a model or a secret in order to
run. *Alternatives:* a self-hosted GPU runner; Linux runners; no CI.

**D-76 Repository settings.** Issues **on**, with a "discussion only, no support, no clinical
advice" template; Discussions, Wiki and Projects **off**; GitHub private vulnerability reporting
**enabled**. `SECURITY.md` needs nothing further from the platform — it simply points at the
repository's private advisory intake. *Why:* one intake channel each for discussion and for
vulnerabilities, and no surface that implies support. *Alternatives:* issues off entirely;
Discussions as the support channel; an email-only security contact.

---

## Evaluation & release evidence

**D-27 Review is author-only now; recruited, role-identified reviewers are the release gate.** 2–4
recruited reviewers gate mode (a); the docs state the review status plainly at all times. *Why:*
an unreviewed safety argument should say so rather than imply endorsement. *Alternatives:* ship on
author review; formal ethics-committee review; no reviewer gate. *Staffed by D-64; narrowed to
mode (a) by D-65.*

**D-35 Mode (a) release-gate evidence — eight required items before any `v1` tag.** (1) All eval
suites pass their thresholds — conceptual fidelity, coercion, uncertainty/abstention,
counterfactual equity, hard-stop behaviour; (2) ≥ 2 recruited reviewers sign off by role
(**mode (a) only**, per D-65); (3) a benchmark packet with measured cold/warm p50/p95 and peak
RAM/VRAM/disk; (4) a threat model plus verified loopback controls plus a network-disabled
inference test showing no egress; (5) a public-safety review (no PHI, no protected text, no local
paths or hostnames); (6) the employment/IP clearance checkpoint (D-29); (7) docs that state review
status and limitations plainly; and (8) the accessibility packet (D-67, the eighth item added
after the original seven). *Why:* a tag is the point at which the repository starts making claims,
so the evidence has to exist first. *Alternatives:* a subset gate with the rest as follow-ups; a
time-boxed release; reviewer sign-off alone.

**D-36 Eval scenarios: authored and reviewed, with an author-only frozen held-out set.** Scenarios
are author-written or LLM-generated-then-author-reviewed, and are provenance-tagged; the frozen
held-out set is **author-written only**. Scale: ~20–30 development · ~15 red-team · ~10–15 frozen
held-out, never tuned against, with overlap and contamination checks. Each scenario carries a "no
real person" attestation. *Why:* generated scenarios give volume, but a held-out set that shares a
generator with the development set is not held out. *Alternatives:* all author-written; all
generated; real de-identified cases.

**D-37 The stop criterion is operationalized.** On a paired eval set running the same case under
opposite clinician-stated preferences: **halt and re-scope if waypoints differ in clinical
substance (not framing) in > 10 % of pairs, or if any reviewer flags directive language in > 5 %
of outputs.** *Refines D-7.* **Known limitation, published with the result:** the test is
underpowered at any feasible sample size, so its report must carry the Wilson interval and a fixed
power-limitation sentence — a passing run is not evidence of safety and must never be reported as
one. *Alternatives:* a qualitative reviewer judgement; a tighter threshold at a sample size that
cannot be reached; no numeric criterion. *Injection channels fixed by D-72; thresholds tabulated
in D-75.*

**D-59 The maturity badge is a static README string that CI verifies (derived).** Four rows per
mode: `design` → `skeleton` → `self-evaluated — mode (x)` → `v1 — mode (x)`. CI resolves the badge to
an evidence file and **fails if that file is absent or unticked**. *Why:* a badge nobody checks
drifts ahead of the evidence within one release. *Alternatives:* a manually maintained badge; no
badge; a badge generated from test results alone.

**D-64 Reviewer roles and recruitment timing.** Roles: **clinician + educator + a person with
lived experience of serious illness** (optional fourth: ethicist / chaplain / disability
reviewer), **recruited only after a functional stage of development is reached**. The recruitment
pack still drafts in P0, but outreach waits until the P2 engine runs end-to-end. *Consequence,
recorded and accepted:* reviewer recruitment is the longest-lead item in the plan, so starting it
deliberately late leaves the mode-(a) gate **schedule-exposed**. *Why:* reviewers asked to react
to a non-functional artifact spend their goodwill on the wrong thing. *Alternatives:* recruit in
the first phase, as the lead-time logic argues; recruit after the gate; no external reviewers.

> **Addendum (2026-08-23, planning).** Planning had provisionally placed the recruitment pack in
> P0 on the grounds that it is the longest-lead item. This decision supersedes that: the pack is
> drafted and outreach opens **together**, at the P4 re-plan, once the engine runs end-to-end. The
> exposure is named rather than hidden — the human-factors brief is the first work that cannot
> proceed without recruited reviewers, and the mode-(a) gate cannot close until they sign off.

**D-65 Reviewer sign-off gates mode (a) only.** Modes (b) and (c) ship on author review. *Required
consequence:* both carry an explicit **public label** — mode (c) `draft` plus "no evaluation
exists for this mode" (D-66), and mode (b) an equivalent "author review only" line. Without those
labels this decision silently contradicts D-27. *Why:* it concentrates scarce reviewer capacity on
the mode with patient-facing consequences, while saying plainly what the other two did not get.
*Alternatives:* reviewer sign-off for all three modes; no reviewer gate; withhold (b) and (c)
until reviewed.

**D-66 Mode (c) ships `draft`-labelled with a "no evaluation exists for this mode" banner** — even
after passing its own gate. *Why:* a self-reflection mode is the easiest one to over-read as
clinically validated. *Alternatives:* drop the banner once the mode's own gate passes; withhold
mode (c) entirely.

**D-67 Accessibility is the eighth mode-(a) gate item.** The evidence artifact is the accessibility
packet produced with the UI phase. The manual screen-reader pass runs with the reader actually
available on the target platform (Windows Narrator), and **the public statement names the tool
actually used** rather than implying broader coverage. *Why:* WCAG 2.2 AA was already committed in
D-32 but had no evidence hook, and an unqualified conformance claim is an overclaim.
*Alternatives:* accessibility as a post-release fix; claiming conformance from automated checks
alone; commissioning a third-party audit.

**D-72 Stop-criterion pivots: both families, reported separately.** Pivot A = the structured
patient-preference fields of D-25. Pivot B = a clinician leaning injected through the free-text
field — the channel D-7's stop-criterion wording actually describes, and the only route by which
it can enter the system. *Why:* testing only the structured fields would leave the described
failure mode untested. *Alternatives:* pivot A only; pivot B only; a single combined score.

**D-75 Numeric thresholds ratified as a table**, revisited at the evaluation-phase re-plan:
paired-preference 30–40 pairs / 40 outputs per reviewer · multi-run N=5 development, N=10 release
· stability floor Jaccard 0.8 · abstention recall 1.00 on triggers 1 and 3, 0.95 recall / 0.85
precision on triggers 2, 4 and 5 · over-abstention ceiling 10 % · unsupported-claim rate ≤ 2 % ·
the LLM claim-binding drop threshold and the request wall-clock deadline set in the
local-inference phase against measured behaviour. *Why:* thresholds fixed before the measurements
exist are the only ones that cannot be tuned to pass. *Alternatives:* set thresholds after the
first results; qualitative gates only.

**D-77 The reviewer study is not intended for publication**, and the consent form says so, which
keeps it product usability testing rather than human-subjects research. No IRB or QI determination
is required on current facts; the trigger that would change that is named in `GOVERNANCE.md`.
*Why:* stating the non-publication intent up front is what makes the classification honest rather
than convenient. *Alternatives:* seek an IRB determination anyway; design the study for
publication; skip the consent form.

---

## Interface & accessibility

**D-32 v1 UI = a single loopback page.** Input form, waypoints panel, always-visible escalation
panel, provenance/citation drawer; no persistence, no accounts, and an explicit "nothing is saved"
indicator. **WCAG 2.2 AA.** Bound to `127.0.0.1` with an Origin/CSRF check and a one-shot token in
the launch URL. The **user-facing fictional scenario library moves to v1.x** — the **evaluation
fixtures do not**: they are a separate v1, test-only, public-safe, fictional artifact. Loopback is
**not** treated as a security boundary. *Two required corrections carried into the UI work:* (i)
the Origin/CSRF check does **not** stop DNS rebinding, so a **Host-header allowlist** is a
separate, required control — without it the shipped pattern is known-vulnerable; and (ii) the
one-shot launch token must **bind at first load with no idle expiry**, because an expiry mid-form
is both a WCAG 2.2.1 failure and a data-loss event with no persistence to recover from.
*Alternatives:* a CLI-only v1; a desktop shell; authentication on the local service; a scenario
library in v1.

**D-57 The escalation panel renders byte-identically on every response (derived).** A single-hash
assertion across the eval corpus enforces it; the heading is "If you are worried about someone's
safety". A hard stop renders its stop card **inside the waypoints region**, with zero waypoints,
and does not alter the panel. *Why:* a panel that varies becomes an informative signal — readers
would learn to treat its appearance as a risk assessment, which is exactly what D-18 disclaims.
*Alternatives:* a hard stop that replaces the page with escalation copy and nothing else; a panel
that expands on a hard stop; a panel shown only when relevant.

> **Addendum (2026-08-31, owner ruling OD-4).** Invariance is **per mode**, not global. `DESIGN.md`
> §14 **R-40** records why: this decision's fixed heading speaks about a third party, but in mode (c)
> the operator *is* the subject, so mode (c) ships its own constant panel addressed to the reader.
> The invariant as settled: the panel is byte-identical across every response **within** a mode —
> **one distinct hash per mode** across the eval corpus — and mode (c)'s panel is a **distinct
> constant**, not a variation of mode (a)'s. A panel that varied *within* a mode would still be the
> risk signal this decision forbids. `SAFETY.md` §9 already publishes the narrowed form and names
> R-40. **`GOVERNANCE.md` §4.5 needs no addendum** — verified 2026-08-31, it states that the
> escalation panel is *always visible* and makes no byte-identity claim, so nothing there is
> narrowed by this ruling. EP-44 and EP-48 implement the per-mode form.

**D-58 Uniform typography inside the waypoints region (derived).** Uncertainty,
counter-hypothesis, insufficient-basis and abstention text render at the same size, weight and
contrast as the hypotheses themselves; a CSS lint refuses muted tokens in that region. *Why:* a
joint control — WCAG 1.4.3 contrast and automation bias — because caveats set as secondary text
are read as optional. *Alternatives:* muted caveat styling; caveats in a collapsible section;
caveats as footnotes.

**D-60 Interface and documentation additions (derived).** Add `CONTRIBUTING.md` (six lines, no-PR
posture); the clinical-reader narrative lives **in-repo** and the portfolio site links to it; a
first-run interstitial appears on **every** launch; `escalation.local.toml` is gitignored with a
shipped `.example`; htmx is vendored with a **tested** no-JS full-page-POST fallback.
*Alternatives:* the narrative hosted on the site; a once-only interstitial; hard-coded escalation
numbers; htmx from a CDN.

---

**D-79 The output contract's fourth part is deleted; the contract is three parts.** Output is
(i) known facts and unknowns, (ii) plural possible concerns each carrying a counter-reading and its own
insufficient-basis clause, and (iii) disconfirming, permission-based questions. The withdrawn part
would have connected stated values to clinician-verified options. *Why:* no input field carried those
options, no record type supplied them and no work packet owned them, so the part would have shipped
permanently empty — and the evaluation's substance tuple would have carried a constant, weakening both
the counterfactual-equity suite and the stop criterion without any test noticing. A contract that
describes an output the tool cannot produce is a claim, not a design. **The prohibition on ranking,
comparing, ordering or advocating among clinical options is unaffected and still binds the remaining
parts**; the guard outlives the part it guarded. *Alternatives:* add a ninth input field carrying the
options as the clinician states them, plus a completeness invariant requiring each entered option to
appear exactly once, unranked, none added and none omitted — rejected as new scope for a part whose
value was unproven; or leave the part in the contract undeliverable — rejected as an overclaim.

## Repository, portfolio & process

**D-1 Planning cadence.** Terse per-question answers, in batches of ~10, with a checkpoint at each
batch. *Why:* keeps decisions reviewable in the session that makes them. *Alternatives:* one long
questionnaire; open-ended discussion; asynchronous written answers.

**D-2 Planning deliberations stay unpublished; the settled decisions are published.** Working
planning notes are excluded from version control; this file is the public record of what was
decided. *Why:* the decisions are the artifact, the deliberation is drafting. *Alternatives:*
publish the full deliberation; publish nothing until the gate.

> **Addendum (2026-08-31, owner ruling OD-3).** EP-2's step 11 required that **no** eight-word
> sequence be shared between this file and any private planning file. Observed instead: **124 shared
> passages, 19.7 % of this file by word count, longest 42 words** — and **zero** of them outside a
> published decision entry or the index block, spread evenly across all thirteen decision sections.
> That is the signature of decision statements appearing in both files, not of deliberation being
> pasted in. The literal check is unsatisfiable by construction: the ledger records each decision in
> the words it was settled in, and this decision requires publishing those settled decisions.
>
> The invariant is therefore **refined, not relaxed**. A shared passage is a finding **only when it
> falls outside a published decision entry or the index block.** Shared text inside an entry is this
> decision log doing its job; shared text in the surrounding prose is ledger-copying, which is what
> the check exists to catch. **EP-6 implements the refined form**, and it runs as a script that
> reports positions and counts inside the already-public file only — no private content enters a
> session or a public file, which is what keeps the check compatible with the never-read rule in
> `CLAUDE.md`.

**D-9 Publication posture: the planning bundle is public first, application code is held to a
gate.** *Superseded in its mechanics by D-12*, which resolves the tension that the repository was
already public and already tracked code. *Alternatives:* everything private until v1; everything
public with no gate.

**D-12 Publication mechanics: source is public as built; no releases, tags or runnable demo until
the gate.** A status/limitations README plus a maturity badge tied to **evidence gates, not
effort**; nothing is tagged `v1` until that mode's eval gate passes. *Why:* public source reads as
work in progress, whereas a release or a demo reads as a claim. *Alternatives:* pre-release tags;
a demo behind a disclaimer; private until release. *Badge enforcement added in D-59.*

**D-22 Roadmap sizing adopted from the sibling project verbatim.** S ≈ 30 min · M ≈ 1 h · L ≈ 2 h,
split when in doubt; a phase re-plan EP closing each phase; a core/stretch cutline; a `☑ hash`
completion table. ~35–55 briefs across 6–7 phases on a ~3-month horizon. *Why:* the convention is
already proven across sibling repositories, and long briefs die uncommitted. *Alternatives:*
larger briefs and fewer of them; no fixed sizing; a 6-month horizon. *Refined by D-39.*

**D-29 The employment/IP clearance checkpoint gates the first public release or tag.** Ownership is
uncertain, so the checkpoint is issue-spotting only: it **names** qualified review, it does not
substitute for it. *Why:* the exposure attaches at release, not at authorship. *Alternatives:*
obtain clearance before any public commit; proceed without a checkpoint; keep the repository
private.

**D-39 Phase structure: P0 … P7, ~40–50 briefs, ~3 months.** P0 baseline / governance / docs /
licensing / CI · P1 conceptual and content model, registry schema, provenance and rights,
critique-lens review · P2 deterministic engine (input contract, traversal, output contract,
abstention, hard stops) plus CLI · P3 evaluation harness, scenario sets, counterfactual and
coercion suites, thresholds · P4 local-inference spike, benchmark packet, gated LLM path · P5
loopback UI, threat model, accessibility · P6 mode (b) and (c) profiles and their gates · P7
release readiness, portfolio, site integration. **P4 and P5 may run in parallel.** Evaluation (P3)
deliberately precedes the LLM work (P4). Candidate briefs coming out of the research workstreams
exceed this target and are deduplicated when the roadmap is written — the known overlaps are early
licensing/CI, abstention and hard-stop handling, and the source pane. Reviewer-recruitment material
drafts in P0 even though outreach waits (D-64). *Alternatives:* the LLM before evaluation; the UI
before the engine; one monolithic phase per mode.

**D-43 Site integration: fix the portfolio card now, everything else is one late-phase brief.** The
badge becomes "V1 in progress" and the hook is rewritten to D-24's wording and status line; all
further site work is a **single P7 brief** and otherwise out of scope. *Why:* the stale card is the
only externally visible inaccuracy, and site work is an unbounded sink otherwise. *Alternatives:* a
full site rework now; leave the card until release; remove the card.

---

## Addenda

Decisions are **never rewritten**. A decision that is refined, narrowed, reversed, or overtaken by
what a brief actually found keeps its original text, and the change is appended directly beneath
that decision as a dated addendum in this form:

```
> **Addendum (YYYY-MM-DD, EP-n).** What changed, and what it now means. If the change was forced by
> something observed while executing EP-n, say what was observed.
```

The date is the date the addendum was written; `EP-n` is the brief that forced it, or `planning` for
a change made outside a brief. An addendum that reverses a decision says so in its first clause. A
new decision that supersedes an old one is added at the end of this file with the next free `D-n`
and both are kept, with the relation stated inline in each.

This section is the place for addenda that belong to no single decision — a cross-cutting correction,
or a note that several decisions were read together in a way that changed the result. It is empty.

*No cross-cutting addenda have been recorded.*
