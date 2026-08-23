# epppsynth — GOVERNANCE

**This document overrides `DESIGN.md` and every roadmap brief.** Where a brief and this file
disagree, this file wins and the brief is wrong. Where this file is silent, `DECISIONS.md` governs.
Changes are appended as dated addenda; nothing here is rewritten.

Established in the planning session of **2026-08-23**.

---

## 1. What this project is, and what it is not

`epppsynth` — *existential perspectives for physicians & patients* — is a **local, offline-capable
reflection aid**. A human supplies encounter context explicitly, states a purpose, and receives a few
concise, revisable waypoints they can hold in working memory or discard.

It is **not** psychotherapy, not clinical decision support, not a risk detector, not a screening or
assessment instrument, and not a source of clinical recommendations. The name's historical expansion
named a regulated therapeutic modality; that expansion is retired and must not be reintroduced in any
public text.

**Status is stated honestly, always.** Public source availability is not evidence of efficacy,
safety, approval, or suitability. The repository is public as a design and source artifact; the tool
is built for its author's private local use.

## 2. Intended use

- **Mode (a) — clinician pre-encounter reflection on fictional scenarios only.** The v1 build target.
- **Mode (b) — trainee education and reflection.**
- **Mode (c) — clinician self-reflection on the structural and existential dimensions of a clinical
  experience.**

One engine, three purpose profiles, built a → b → c, each with its own eval set and its own release
gate. A failing mode is withheld without blocking the others.

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

## 4. Invariants

1. **Epistemic humility and human accountability.** Generated interpretations are revisable
   reflection aids — never psychotherapy, authoritative scripts, or diagnoses of motive, mental
   illness, capacity, suicidality, spirituality, prognosis, or treatment. Every emission carries
   alternatives, a counter-reading, and an insufficient-basis clause. The sole accountable human is
   the operating clinician or trainee.
2. **No stereotyping or inferred identity.** Nothing infers beliefs, culture, ethnicity, race,
   religion, disability, values, protected traits, or emotional state from names, diagnosis, prose
   proxies, or group membership. Every input field supports unknown / not relevant / prefer not to
   answer. Voluntarily stated preferences may affect **communication framing only**; protected traits
   never alter clinical content. The free-text field carries *what the person said* — it is an
   **inert echo**, quoted back to the reader and nothing more. It never changes what the engine emits,
   and it is never tokenised, keyword-scanned, classified, or mined for inference of any kind.
3. **No coercion.** Nothing may optimise explicit or covert persuasion, compliance, or a target
   clinical outcome. The operational line: *rapport* changes what a person is able to say;
   *persuasion* changes what a person decides. Prohibited outright: framing designed to make one
   option feel safer or more courageous; treating a stated preference as an obstacle; objection
   handling; scripting a second attempt after a refusal; and any output whose clinical substance
   varies with the clinician's own stated preference — which is machine-tested (§8).
4. **Disagreement is not pathologized.** Distrust, anger, grief, silence, requests for testing, and
   refusal may be rational responses to uncertainty, prior harm, inequity, communication failure, or
   institutional conduct. No output may explain a disagreement in terms of the person's psychological
   state.
5. **Hard stops are deterministic.** For possible impaired capacity or delirium, self-harm or
   violence risk, abuse, severe distress or psychosis, disputed surrogacy, coercion, or language-access
   failure: synthesis is suspended and only a minimal stop-and-escalate instruction is emitted.
   Detection is by explicit declared flags and a fixed checklist over **declared fields only** — never a
   generative classifier, and never a scan of the free-text field. A tool that scanned prose for danger
   words would be a risk detector, and an unreliable one, which is worse than none because it invites
   reliance. The compensating controls are the always-visible escalation panel and a prominent
   declared-flag control.
   Disability, communication style, limited English proficiency, cultural difference, and disagreement
   are not evidence of incapacity.
6. **Mode separation.** Patient-specific, PHI-processing, patient- or family-facing, point-of-care,
   and therapeutic uses are **excluded release classes** (§9). A disclaimer, the author's preference,
   or developer self-review cannot unlock them.
7. **Trainee non-surveillance.** Mode (b) is strictly local: no accounts, no scoring, no retention, no
   export, no employer visibility, voluntary use only. Structural moral injury is never individualised.
8. **Public-history safety.** No real patient, family, trainee, or employee material, no secrets, no
   institution-confidential information in repository history, issues, PRs, screenshots, demos,
   fixtures, prompts, telemetry, artifacts, or CI logs. Cases are manifestly fictional. "Local" is not
   automatically private, and de-identification does not mean zero risk.
9. **Rights and provenance.** No copyrighted books, articles, PDFs, proprietary instruments, scraped
   corpora, unlicensed derived indexes, or third-party weights are committed. Lawful access does not
   imply a right to redistribute, embed, train on, or publish derivatives.
10. **Generated text is inert.** It is never shell, code, database, tool, or clinical-order input;
    never rendered as raw HTML; never written into a chart, order, or note.
11. **Conservative claims.** Public materials use intended-use / excluded-use / status language and
    never overstate maturity, efficacy, safety, adoption, or regulatory status.

## 5. Data boundary

No PHI. No real cases. Manifestly fictional scenarios only. **No retention** of prompts or outputs.
**No runtime network.** Offline-capable, not air-gapped: the machine keeps its network, and the
*application* is proven silent.

"Proven" is literal. Retention is verified by a filesystem-delta harness, not asserted. The absence of
egress is verified in **two layers** — an in-process socket guard proves only the Python layer is
quiet; an outbound block-and-log rule scoped to the interpreter, asserted to have zero entries across
a full inference session, is what proves the native layer is. Residual channels that cannot be
eliminated — operating-system crash dumps, browser history and back-forward cache, the page file, GPU
memory not zeroed on free — are **disclosed in `PRIVACY.md`**, never denied.

Logging is off by default, records only hashes and timings when enabled, and is never enabled in
mode (b). The free-text input is a distinct type that redacts itself in any string representation, so
it cannot be logged by accident.

## 6. Rights, sources, and what may be committed

The conceptual substrate is read from sources the author lawfully holds; **none of it is
redistributed**. What ships is original prose that cites its sources.

- Every source carries a rights record: identifier, licence, `reuse_class`, verification status and
  date. Only `ingestible-*` sources may have their wording inform authored prose.
- **Normative guidance under a non-commercial or share-alike licence is referenced, never ingested.**
- Public citations are **chapter-level locators only** — no page ranges, no quoted phrase, no chapter
  title reused as a concept label, and no locator sequence that reconstructs a source's outline.
- Quotation budget, enforced in CI: **≤ 25 words per quote, ≤ 150 words per source.**
- The corpus lives in a gitignored directory inside the working tree (`source material/`); the derived
  index and any model weights live outside the tree entirely. None of it is tracked, enters CI, or
  appears in a published artifact, and a history assertion proves no corpus path was ever committed. Verbatim spans may exist in the local index and
  may be displayed in a local-only source pane; they may **never** be emitted, exported, screenshotted,
  or serialized. This is enforced by the type graph, not by discipline.
- Two normative-guidance source families' reuse terms are **UNVERIFIED** at planning time and are held
  as `reference-only-pending-rights-check` until cleared.

**Licensing:** Apache-2.0 for code, CC BY 4.0 for the content model and documentation, REUSE-conformant,
with `NOTICE`, `CITATION.cff`, and a generated per-source rights table.

## 7. Public-safety rule

Every artifact is public-safe by default, because the repository is public.

Before any publication: secrets scanned across the **full history**, PHI-shaped patterns swept across
tracked files and fixtures, protected text checked, local paths and machine identifiers swept,
screenshots re-opened and read, licence conformance checked, and every public claim compared against
its evidence file.

> `.gitignore`, pre-commit hooks and CI scanners are **defense in depth. They are not proof that
> nothing leaked.** The proof is the pre-publication review packet, performed by a human, recorded
> with a date and a commit hash. This matters especially because the repository's history was erased
> and re-created: a clean current tree is not a clean history claim.

## 8. Release gates

No `v1` tag exists until **all eight** items are satisfied for the mode being tagged, with artifacts
in `release-evidence/<tag>/` under a manifest whose recorded build hash equals the tagged commit:

1. All evaluation suites pass their thresholds — conceptual fidelity, clinical plausibility,
   uncertainty and hallucination, coercion and forced meaning, counterfactual equity, abstention and
   escalation, hard-stop behaviour.
2. **≥ 2 recruited reviewers sign off by role** (mode (a) only — see §10).
3. Benchmark packet complete: cold and warm, p50 and p95, peak memory and disk, including a CPU-only row.
4. Threat model verified: every loopback control has a passing adversarial test, and the no-egress test
   log is empty.
5. Public-safety review clean (§7).
6. Employment/IP clearance checkpoint recorded.
7. Documentation states review status and limitations plainly.
8. **Accessibility packet complete** — WCAG 2.2 AA, automated plus a scripted manual pass.

The maturity badge is a static string that CI resolves to an evidence file and **refuses to upgrade**
if the file is missing or its checklist is unticked. A badge tied to "evidence" is only real if the
tie is mechanical.

**Stop criterion.** The project halts and re-scopes if paired evaluation shows outputs differing in
clinical substance in more than 10 % of pairs, or if any reviewer flags directive language in more
than 5 % of outputs. On a trigger: freeze (no tag, no release, no badge advance) → log a dated
addendum → root-cause packet → re-scope ladder (narrow the output contract → disable the model path →
withdraw the affected mode → withdraw v1) → re-test on a fresh held-out slice → **disclose the halt
and its resolution in the public README**. A halt that is not visible is itself an overclaim.

The test pivots two ways: on the patient-preference fields, and on a clinician leaning expressed in
free text. Because free text is an inert echo (§4.2), **the second pivot cannot vary the deterministic
baseline at all** — non-variation there is an architectural property, not an empirical finding, and it
is informative only on the model path. Any report of the criterion states this; presenting a
structurally guaranteed zero as evidence of safety would be the overclaim the criterion exists to
prevent.

The test is also **underpowered** at any feasible sample size. Every report of it publishes the confidence
interval alongside the rate, plus a fixed sentence stating the power limit. Reporting the point
estimate alone would be the exact overclaim the criterion exists to prevent.

## 9. Excluded release classes

Patient-specific point-of-care use, patient- or family-facing use, PHI processing, EHR integration,
and autonomous action are **excluded** — not deferred. Each of the following preconditions requires an
external accountable party this project does not have, and **the author will not attempt these modes
as a solo project**:

1. A written intended-use and claims analysis reviewed by qualified regulatory counsel against the
   current clinical-decision-support guidance.
2. Institutional and employment-IP clearance completed in writing beforehand.
3. A privacy and security assessment by a qualified privacy officer or counsel.
4. Qualified legal and regulatory review plus an IRB or QI determination for any prospective
   evaluation involving real patients.
5. Independent multidisciplinary review — clinical, ethics, patient and family representation, and
   health equity — **with the authority to say no**.
6. A prospective summative human-factors evaluation in the real environment with the real user
   population.
7. Predefined go/no-go and stop criteria registered before the evaluation runs, with a rollback plan.

This is issue-spotting, not legal advice.

## 10. Review status, stated honestly

Reviewer sign-off gates **mode (a) only**. Modes (b) and (c) therefore ship carrying a public
"author review only" label, and mode (c) additionally ships `draft`-labelled with a **"no evaluation
exists for this mode"** banner. Reviewer recruitment opens once a functional stage exists, which
deliberately puts the longest-lead dependency late and leaves the mode (a) gate schedule-exposed.

Reviewer roles: a clinician in serious-illness care, a clinician-educator, and **a person with lived
experience of serious illness** — the last is required, not optional, because they are the only
reviewer positioned to detect coercion and forced meaning from the side that bears its cost.
Consent states that participation is **not an endorsement of clinical use**. Attribution is role-only
by default. Individual scores are never published.

**Human-subjects status, stated precisely.** The reviewer sessions are product usability testing of one
specific artifact, and the determination rests on **non-generalizable knowledge** — not on secrecy. It
is stated plainly that an aggregate report *is* published in the release evidence and that a public
narrative draws on it; resting the determination on "not intended for publication" while publishing an
aggregate would be unsound. A dated written self-determination is recorded in the repository and
labelled as the author's own, not an expert opinion. If the work is ever framed as producing
generalizable knowledge, an IRB or QI determination is required **first**.

**Reviewer welfare.** The reviewer with lived experience of serious illness is the participant most
exposed to this material. They may pause, skip any case, or stop without explanation and at no cost;
they receive advance warning of crisis-adjacent content and may decline that block entirely, recorded
as declined rather than failed; a support resource and a study contact are named; and the debrief asks
about burden as well as findings, treating the answer as a finding.

**The role cannot be silently dropped.** The mode (a) gate requires that reviewer's sign-off by name,
or an explicit dated waiver, published in both the gate evidence and the README status line, naming
what was lost. Omitting it quietly is a gate failure.

## 11. What the evidence actually supports

The closest evidence analogues to this project are **null-to-adverse**: a randomized trial of
simulation-based serious-illness communication training found no improvement in patient- or
family-reported communication quality **and a significant increase in patient depressive symptoms**;
the flagship structured-guide trial was null on both coprimary patient outcomes and positive only on
process measures. No study exists of this intervention class at all.

Consequences, binding on every public artifact:

- The defensible analogue is a **question-generation aid** — demonstrated to change *what gets asked*,
  not outcomes.
- The success criterion is a measure of **feasibility and acceptability**, never effectiveness.
- Documentation may not imply that communication preparation is inherently benign.
- Self-report is a weak surrogate; "the reader found a question useful" measures generativity, not value.

## 12. Scope of the conceptual model

The content model is **Western and secular in origin** and is labelled as such wherever it is used. It
is not a general model of how people face serious illness, and no coverage of non-Western or
religiously grounded frameworks is claimed or attempted. Where a person's framework falls outside the
declared scope, the required behaviour is **explicit abstention naming the limit** — not adaptation,
not analogy, not a generic humanistic substitute. Abstention is a tested safety behaviour with its own
evaluation cases, not a courtesy.

The tool generates no doctrine, no sacred-text quotation, no spiritual authority, and no claim that a
tradition requires a particular choice.

## 13. Hazards

The hazard register lives in `DESIGN.md` §14: **41 numbered entries**, each naming affected people,
likelihood and severity, the preventing mechanism, the brief that implements it, and the gate that
verifies it. It is the single register; nothing restates it. `tools/roadmap_check.py` fails if a hazard names no brief.

The two rated highest are: **an underpowered stop criterion read as evidence of safety**, and
**uncertainty rendered as de-emphasised secondary text** — the second being simultaneously a contrast
failure and the precise mechanism of automation bias.

## 14. Contribution and reporting

No pull requests are accepted in v1. Issues are open for discussion only — not support, and never
clinical advice. Security and safety concerns are reported privately through the repository's private
vulnerability reporting. Third-party deployment is not an intended use and is out of scope.

## 15. Session rules

Sessions executing roadmap briefs follow `CLAUDE.md` and the load order in `roadmap/README.md`. Two
rules override any brief: **never read or quote the corpus**, and **never copy private planning state
into a public file**.
