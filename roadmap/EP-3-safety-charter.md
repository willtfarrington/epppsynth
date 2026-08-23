# EP-3 — SAFETY.md, the clinical-ethics charter

**Size:** L · **Mode:** n/a · **Core/Stretch:** core ·
**Depends on:** EP-2 (canonical docs + public front matter + badge scheme) · **Blocks:** EP-4 (privacy/security/conduct), EP-8 (roadmap tooling, re-plan P0), EP-39 (UI contract and copy deck)

## Context

`SAFETY.md` is the charter. It is the document that says what this tool refuses to do and why each
refusal exists, and it is the single source that four later briefs consume programmatically: the
banned-phrase lint (EP-39) reads its published list, the abstention chain (EP-20) implements its
taxonomy, the red-team set (EP-26) attacks its prohibitions, and the escalation panel (EP-44)
renders the copy it fixes. It is therefore not a statement of intent — it is a specification with
prose around it.

**What exists.** `README.md` with the approved status line, a short Intended-use summary, the
not-a-risk-detector line, and a link to `SAFETY.md` that currently resolves to nothing.
`GOVERNANCE.md` with the data boundary, the hazard table and the release gates.
`DECISIONS.md` with the D-1 … D-78 index. No `SAFETY.md`.

**What this brief creates.** `SAFETY.md` at the repository root, and one machine-readable artifact:
`epppsynth/copy/banned-phrases.toml`, which is the **same file** the EP-39 lint consumes.
`SAFETY.md` renders that list rather than restating it, because a published list and a linted list
that are two files are two lists, and they will diverge.

**The approved verbatim public text.** The four blocks — *Intended use*, *Excluded uses*, *What it
does not know*, *Status* — are approved (D-69) and are placed here **in full, character for
character**. EP-2 placed the Status line and a summary in the README; EP-3 is where the complete
text lives. Neither brief may paraphrase, and step 12 proves equality rather than similarity.

Implements: D-6 (sole accountable human), D-7 and D-37 (the stop criterion, with its numbers),
D-11 and D-26 (the output contract and the functions it preserves), D-14 (Western-secular scope,
labelled, with abstention as the mitigation), D-18 (deterministic hard stops; never a generative
classifier; the flat public claim that this is not a risk detector), D-19 (trainee
non-surveillance), D-20 (mode (c) scope and the moral-injury charter clause), D-23 (paraphrase plus
citation; never verbatim emission), D-38 (the five-part abstention taxonomy), D-53 (counter-reading
and insufficient-basis are structurally required), D-58 (uncertainty renders at the same weight as
hypotheses), D-63 (evidence honesty), D-65/D-66 (per-mode review labels), D-69 (approved wording),
D-74 (citation and quotation limits). Mitigates R-1 (coercion architecture), R-2 (automation bias),
R-5 (crisis mis-handling), R-11 (concept reification), R-12 (null-to-harm precedent), R-16 (mode (c)
inversion into individual pathology), R-17 (anchoring), R-31 (over-abstention).

## Safety preconditions

| Invariant at risk | Guard in this brief |
|---|---|
| The charter itself becomes an overclaim (R-9, R-12, D-63) | `SAFETY.md` states what is **built** and what is **planned**, per brief, and carries the D-63 evidence sentence: the closest analogue trials are null-to-adverse, the defensible analogue is a question-generation aid, and D-7's success criterion is a **feasibility and acceptability** measure, never an effectiveness claim. A charter that reads as reassurance is a failure of this brief. |
| A published prohibition that nothing enforces (R-14, "lens tokenism" applied to the charter itself) | Every prohibition in `SAFETY.md` carries an **enforcement column**: the brief that implements it and the eval suite that verifies it. A prohibition with no enforcement is written as *unenforced — planned EP-n*, explicitly, rather than left to look enforced. |
| Two copies of the banned-phrase list (drift) | The list lives once, in `epppsynth/copy/banned-phrases.toml`. `SAFETY.md` includes it by transclusion at authoring time and the acceptance check asserts the rendered block equals the file. |
| The escalation copy varying between documents (D-57, R-34) | The escalation heading — "If you are worried about someone's safety" — and the shipped US defaults (988; emergency services) are written **once** here, and EP-44 renders from this text. The charter states that the panel renders byte-identically on every response and that a varying panel would itself be a risk signal. |
| Crisis copy read as triage (R-5, D-18) | The not-a-risk-detector line is repeated verbatim inside the hard-stop section, adjacent to the escalation copy, not only in the README. The charter states that the tool **never checks what you type for danger**. |
| Mode (c) drifting into distress screening (R-16, D-20) | The charter clause is written verbatim: *moral injury arises from conditions, not individual deficiency*. The section states the composer rule (any output set containing a `personal-meaning` concept must also contain a `structural` one) and names EP-48 as its implementer. |
| Review status implied rather than stated (D-27, D-65, D-66) | A `## Review status` section states plainly: author review only; no external reviewer has read this; reviewer sign-off gates **mode (a) only**; mode (b) carries an "author review only" label and mode (c) ships `draft` with a "no evaluation exists for this mode" banner. |

Pre-publication checklist items exercised here: **3 (protected text — the charter quotes no source,
and the D-74 quotation budget is stated and self-applied)**, **7 (public claims — README, badge and
`SAFETY.md` must agree)**.

## In scope

1. **Place the four approved blocks verbatim.** *Intended use* · *Excluded uses* (the eight-bullet
   list, ending with the bolded not-a-risk-detector pair of sentences) · *What it does not know* ·
   *Status*. Copy from the approved text; do not retype from memory.
2. **Invariants section.** Seven named invariants, each one paragraph, each naming its enforcement
   brief and verifying suite: epistemic humility · no stereotyping · no coercion · do not
   pathologize disagreement · deterministic hard stops · mode separation · trainee
   non-surveillance.
3. **The output contract, and why each part exists** (D-11, D-26). Three parts: known facts and
   unknowns · multiple possible concerns, each with a counter-hypothesis and an insufficient-basis
   clause · disconfirming, permission-based questions. Record that a fourth part — neutral framing
   connecting stated values to clinician-verified options — was **deleted** from the contract rather
   than left undeliverable: it had no input field, no authored content source and no owning brief, so
   it would have shipped permanently empty. The no-ranking prohibition is unaffected and stays in
   full force; the tool simply says nothing about clinical options at all. State the four preserved
   functions of D-26 with one paragraph each,
   and name the three **retired** framings ("Hidden Dynamic (Diagnosis)", "Empathic Wedge",
   "Consensus Generation") as retired, with the reason — a charter that quietly drops them invites
   their return.
4. **The question-or-offer rule** (D-26b), stated as an absolute: every suggested utterance is a
   question or an offer, never an assertion about what the patient feels or should do. Name both
   enforcement points: the authoring linter (EP-21) and the runtime parse (EP-21, EP-43).
5. **The abstention taxonomy** (D-38) — all five triggers, **each with one worked example** written
   in this brief:
   1. the person's framework falls outside the declared Western-secular scope;
   2. insufficient basis in the supplied context;
   3. any hard-stop flag;
   4. the request asks for persuasion, prognosis, capacity, diagnosis, or ranking of options;
   5. disagreement or refusal is present — respond without pathologizing and offer no
      "overcoming objections" content.
   Add the counter-hazard explicitly (R-31): over-abstention trains the reader to dismiss
   abstentions, so the taxonomy carries a ceiling (10 %, D-75) and abstention is a *measured*
   behaviour, not a safe default.
6. **Hard stops** (D-18, as narrowed by EP-20). Deterministic only — explicit user-declared flags
   plus a fixed structural checklist over **declared structured fields only**. **Never a generative
   classifier, and never a scan of the free-text field.** State the reason in the charter, because
   the charter is where the public claim lives: a tool that scans prose for danger words *is* a risk
   detector, and an unreliable one, which is worse than none because it invites reliance
   (GOVERNANCE §4.5). The compensating controls are the always-visible escalation panel and a
   prominent declared-flag control. State the settled rendering rule:
   a hard stop renders a stop card in the **waypoints** region and zero waypoints; the
   escalation panel does not change, because a panel that varies is read as a risk signal (D-57,
   R-34). Write the escalation copy: the fixed heading, the shipped clearly-labelled US defaults,
   and the note that institution-specific numbers come from a local, gitignored config with a
   shipped `.example` (D-60), with no geolocation of any kind.
7. **The published banned-phrase list.** Create `epppsynth/copy/banned-phrases.toml` with, at
   minimum: recommend · should · you must · the patient needs to · the right choice · convince ·
   persuade · get them to · buy-in · overcome (objections) · denial · non-compliant ·
   difficult patient · goals-of-care conversation *(as a directive)* · clearly · obviously ·
   the evidence shows *(without a resolving citation)*. Each entry carries a `reason` field and a
   `d_ref` field naming the decision it enforces. `SAFETY.md` renders the list from the file.
8. **The stop criterion, with numbers** (D-7, D-37). Halt and re-scope if waypoints differ in
   clinical substance — not framing — in **> 10 %** of paired cases, or if any reviewer flags
   directive language in **> 5 %** of outputs. State both pivot families (D-72): Pivot A, the D-25
   patient-preference fields; Pivot B, a clinician leaning injected through the free-text field.
   State plainly, in `SAFETY.md` itself, that **Pivot B is vacuous on the deterministic baseline**:
   the free-text field is an inert echo (GOVERNANCE §4.2, §8) that enters no predicate, filter or
   score, so it cannot vary the output there. A zero result for Pivot B on that arm is an
   architectural property of the input contract, not an empirical finding, and it is informative only
   on the model path. Every published report of the criterion states this beside the rate; presenting
   a structurally guaranteed zero as evidence of safety would be the overclaim the criterion exists
   to prevent. The two pivots are always reported separately (EP-31).
   State the power limitation plainly (R-25): the criterion is underpowered at any feasible
   sample size, its report publishes a Wilson interval, and **a passing result is not evidence of
   safety**. State the consequence D-37 and R-9 require: if a trigger fires, the halt and its
   resolution appear in the public README — a halt that is not visible is itself an overclaim.
9. **Scope and cultural limits** (D-14). The model is Western and secular in origin and is labelled
   as such throughout; where a person's framework falls outside it, the correct behaviour is
   **explicit abstention and a note of the limit**, never improvisation; non-Western and
   non-secular frameworks are deliberately out of scope, and that is a limitation of the tool, not
   of the person. State that `cultural_scope.claims_universality` is hard-coded `false` (EP-9).
10. **Mode (c) section** (D-20, R-16) with the charter clause verbatim, the refusals (distress
    screening, scoring, diagnosis), and the composer pairing rule.
11. **Provenance and quotation discipline** (D-23, D-74). Generated output is always paraphrase plus
    citation and never reproduces source text. Public citations are **chapter-level locators only**
    — no page ranges. Quotation budget: **≤ 25 words per quote, ≤ 150 words per source**, enforced
    in CI (EP-6). The optional local source pane (D-23) may display short spans from the reader's
    own copy and is hard-excluded from export, screenshots, demo mode, CI and any published
    artifact.
12. **Uniform-emphasis rule** (D-58, R-33). Uncertainty, counter-hypotheses, insufficient-basis and
    abstention text render at the same size, weight and contrast as hypotheses. State it here
    because it is a safety property, not a style preference, and name EP-39/EP-43 as enforcement.
13. **`## Review status`** and **`## How to report a safety concern`** — the latter pointing at the
    private reporting path `SECURITY.md` will carry (**EP-4** owns that file; EP-3 links to it and
    the link must resolve by the end of P0, which the EP-8 link check confirms).
14. **Verbatim-equality check** against the approved text and against the strings EP-2 recorded.
15. **Commits:** `docs(epppsynth): add SAFETY.md clinical-ethics charter (EP-3)` then
    `docs(roadmap): record EP-3 commit hash`.

## Out of scope

- Implementing the abstention chain, the hard-stop precedence order, or the question-or-offer
  parser — **EP-20** and **EP-21**.
- The banned-phrase **lint** that consumes `banned-phrases.toml` — **EP-39**. EP-3 ships the data
  and the published list; EP-39 ships the check.
- Escalation panel rendering, `escalation.local.toml` and its `.example` — **EP-44**.
- The abstention, coercion and over-abstention **eval suites** — **EP-29**, **EP-30**.
- The paired-preference harness that computes the D-37 rate and its Wilson interval — **EP-31**.
- Numeric threshold derivation and the thresholds file — **EP-24** / D-75's P3 re-plan.
- `PRIVACY.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md` — **EP-4**.
- The clinical-reader narrative that restates the charter for a non-engineer — **EP-53**.
- Any content concept, given, function or principle — **EP-12**, **EP-13**, **EP-14**.

## Verification / acceptance

Runnable, from the repository root:

```powershell
# all five abstention triggers present, each with an example
Select-String -Path SAFETY.md -Pattern '^### Abstention trigger [1-5]'          # → 5 matches
Select-String -Path SAFETY.md -Pattern '^\*Example\.\*'                          # → at least 5

# all four D-26 functions have a paragraph, all three retired framings are named as retired
Select-String -Path SAFETY.md -SimpleMatch 'Hidden Dynamic','Empathic Wedge','Consensus Generation'

# the approved blocks are present verbatim
Select-String -Path SAFETY.md -SimpleMatch `
  'This tool is not a risk detector and must not be used as one.'
Select-String -Path SAFETY.md -SimpleMatch `
  'Design and planning artifact — v1 in progress; no release, no demo, no validation.'

# banned-phrase list is one file, and SAFETY renders it
uv run python -c "import tomllib,pathlib; d=tomllib.loads(pathlib.Path('epppsynth/copy/banned-phrases.toml').read_text(encoding='utf-8')); print(len(d['phrases']))"

# the stop-criterion numbers are stated
Select-String -Path SAFETY.md -Pattern '10 ?%','5 ?%','Wilson'

# the moral-injury charter clause, verbatim
Select-String -Path SAFETY.md -SimpleMatch 'moral injury arises from conditions, not individual deficiency'

# every link resolves
Select-String -Path SAFETY.md -Pattern '\]\(([^)#h][^)]*)\)' -AllMatches
```

Acceptance:

1. All five D-38 abstention triggers appear, each with exactly one worked example, and the
   over-abstention ceiling (10 %) is stated alongside them.
2. All four D-26 functions have their own paragraph; all three retired framings are named as
   retired with the reason.
3. The four approved blocks match the approved text **byte for byte**; the byte lengths equal those
   EP-2 recorded in its completion note.
4. `epppsynth/copy/banned-phrases.toml` parses as TOML, contains at least sixteen entries, and every
   entry has both a `reason` and a `d_ref`. The rendered list in `SAFETY.md` is generated from that
   file and matches it entry for entry (compare programmatically, not by eye).
5. Every prohibition in the charter carries an enforcement column naming a brief and a suite; any
   row whose enforcement does not yet exist reads *unenforced — planned EP-n*. Zero rows are blank.
6. The stop-criterion section contains both thresholds, both pivot families, the Wilson-interval
   requirement, the fixed power-limitation statement, and the public-halt rule.
7. The hard-stop section states "never a generative classifier", repeats the not-a-risk-detector
   line, and describes the settled hard-stop rendering rule (stop card in the waypoints region; escalation panel
   unchanged).
8. Mode (c)'s charter clause appears verbatim, and the `personal-meaning` ⇒ `structural` pairing
   rule is stated with EP-48 named.
9. The `## Review status` section states author-review-only, the mode-(a)-only reviewer gate, and
   both per-mode labels (D-65, D-66).
10. Every relative link in `SAFETY.md` resolves, except the `SECURITY.md` link, which is expected to
    resolve only after **EP-4**; the completion note records that dependency explicitly.
11. `uv run pytest -q` and CI stay green.
12. *(judgement — the project owner)* A clinician reading only `SAFETY.md` can state, without
    guessing, what the tool refuses to do, what would make the author stop building it, and what
    evidence does and does not exist today.

## Parked → final-roadmap.md

- A machine-readable charter (the invariants and prohibitions as data, with the prose generated
  from it). Attractive, but it would put the charter's authority in a schema this project has not
  designed; revisit at the P1 re-plan once the registry schema exists.
- An external ethics review of the charter itself, distinct from the D-27 reviewer sign-off on
  outputs. Named because reviewer recruitment (D-64) deliberately starts late and the charter is
  the artifact most improved by an outside read.
- Localised escalation resources beyond the shipped US defaults and the local config. Requires
  geolocation or a curated international list; D-18 rules out the first and v1 scope rules out the
  second.
- A published incident log for safety concerns received. Depends on `SECURITY.md`'s reporting path
  seeing any traffic; revisit if it does.
