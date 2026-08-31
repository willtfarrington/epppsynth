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

> **Completion note (2026-08-31).** Executed as `7a5ecbb`. Every result below is what was
> **observed**, not what was expected. The acceptance block was run verbatim in PowerShell and its
> counts are recorded; the parts of it that need a machine comparison were additionally written as
> tests (`epppsynth/tests/test_safety_charter.py`, 16 passing) so they re-run in CI rather than once.
>
> #### Deviation 1 — the approved four-block text is not in this brief, and is not in any public file
>
> The Context section states that the four approved blocks "are placed here **in full, character for
> character**". **They are not in this brief.** A sweep of every tracked file found the phrase "What
> it does not know" only in pointers — `DECISIONS.md` D-69's index row, `README.md`, EP-2 and this
> brief — never the block itself. EP-2 says the same thing in the opposite direction: it "places the
> Status line and a short Intended-use summary" and leaves the full text to EP-3. The only remaining
> location is `.local/`, which `CLAUDE.md` forbids reading and which overrides any brief.
>
> Resolved by copying what is public and authoring only what is not, marked here so the owner can
> diff it against the approved draft:
>
> | Block | Source used | Verbatim? |
> |---|---|---|
> | Status | `README.md`, below the badge | yes — **84 bytes**, equal to EP-2's step-9 row 2 |
> | Intended use | `GOVERNANCE.md` §1 and §2 | yes, plus the D-61 excluded-classes paragraph |
> | Excluded uses | `GOVERNANCE.md` §3 | yes, all bullets plus the bolded pair |
> | *not a risk detector* pair | `README.md` / `GOVERNANCE.md` §3 | yes — **103 bytes**, equal to EP-2's row 3 |
> | What it does not know | **authored at EP-3** from D-8, D-14, D-18, D-25, D-63, D-79 | **no — needs owner confirmation** |
>
> Governance §2 and §3 are the binding public statement of intended and excluded uses, so copying
> from them is the closest available thing to copying the approved text. *What it does not know* is
> the only one of the four blocks that no public artifact already fixed.
>
> #### Deviation 2 — the excluded-uses list has nine bullets, not eight
>
> In-scope item 1 says "the eight-bullet list". `GOVERNANCE.md` §3 has **nine**. Governance overrides
> the brief, so all nine were copied. The bullet the brief's count omits is unknowable from here;
> nothing was dropped to make the number fit.
>
> #### Deviation 3 — D-26's third function is withdrawn, so "four preserved functions" cannot be written
>
> In-scope item 3 asks for "the four preserved functions of D-26 with one paragraph each", and
> acceptance 2 asks that all four have their own paragraph. But D-26 carries an addendum: clause (c)
> — connect stated values to clinician-verified options — **is withdrawn with D-79**, the same
> deletion the brief itself asks the charter to record for the output contract's fourth part. Writing
> four *preserved* functions would republish a withdrawn one.
>
> Written as **four paragraphs, three preserved and one recorded as withdrawn**, for the reason the
> brief gives for the retired framings: a function that disappears without a note is a function that
> comes back. Acceptance 2 is met in the form "four paragraphs", not in the form "four preserved".
>
> #### Deviation 4 — panel invariance is per mode, not global
>
> Safety-precondition row 4 and in-scope item 6 say the escalation panel "renders byte-identically on
> every response". `DESIGN.md` §14 **R-40** narrows that: mode (c)'s fixed heading speaks about a
> third party while its operator *is* the subject, so panel invariance is **per mode**, and mode (c)
> ships its own constant panel addressed to the reader. §9 states the rule in the narrowed form and
> names R-40, rather than publishing a global claim EP-44 would have to contradict.
>
> #### Deviation 5 — `SECURITY.md` is rendered as a link, against EP-2's link discipline
>
> EP-2's acceptance 8 established that nothing marked `planned — EP-n` is rendered as a link. In-scope
> item 13 of this brief says the opposite for one file: "EP-3 links to it and the link must resolve by
> the end of P0". Acceptance 10 confirms the exception. The link is therefore rendered, labelled
> *planned — EP-4*, with the working private-reporting route stated in the same sentence so the
> section is usable before EP-4 lands.
>
> **Observed:** across all 70 tracked markdown files plus `SAFETY.md`, `SECURITY.md` is the **only**
> unresolved relative link in the repository. `test_every_relative_link_resolves_except_the_ep4_file`
> asserts exactly that, so it fails if a second one appears and needs updating — deliberately — when
> EP-4 lands.
>
> #### Deviation 6 — two files the brief does not name were needed to make acceptance 4 and 5 checkable
>
> Acceptance 4 requires the rendered list to match the file "programmatically, not by eye", which
> needs a renderer: `tools/render_banned_phrases.py` (`--check` exits 1 on drift). Acceptances 1, 2,
> 3, 5, 6, 7, 8 and 10 are structural properties of a file four later briefs consume, so they were
> written as `epppsynth/tests/test_safety_charter.py` rather than as a one-time manual pass. Both are
> inside the brief's intent and outside its file list.
>
> #### Deviation 7 — the banned-phrase ban needed an explicit scope note
>
> §10 publishes a list of phrases that must not appear in output, in a document that necessarily
> contains all of them; the list would be unpublishable under its own rule. §10 therefore states the
> scope EP-39's lint must implement: the ban governs **authored content and rendered output** —
> concept text, templates, copy deck, composed waypoints — and not documentation that names a phrasing
> in order to forbid it, or that reports what a user typed. One example in §8 was reworded to avoid a
> banned token where the token was incidental rather than necessary.
>
> #### What was created
>
> `SAFETY.md` — 692 lines, seventeen sections. `epppsynth/copy/banned-phrases.toml` — **17 entries**,
> one more than the sixteen the brief lists at minimum, each with `id`, `phrase`, `reason` and
> `d_ref`, and a `condition` on the two conditional bans. `tools/render_banned_phrases.py`.
> `epppsynth/tests/test_safety_charter.py`. `README.md` updated: the `SAFETY.md` pointer is now a
> resolving link with its `planned — EP-3` marker dropped, and a reading path for it was added.
>
> #### Acceptance, as observed
>
> | # | Criterion | Observed |
> |---|---|---|
> | 1 | five triggers, one example each, 10 % ceiling stated | `^### Abstention trigger [1-5]` → **5**; `^\*Example\.\*` → **5**; the ceiling is stated in §8 |
> | 2 | four D-26 paragraphs; three retired framings named | four paragraphs (deviation 3); framings sweep → **4 matches** (three headings plus the narrative sentence opening §7) |
> | 3 | approved blocks byte-for-byte | status line **84 bytes**, risk-detector pair **103 bytes** — equal to EP-2's step-9 rows 2 and 3, asserted in a test. *The "what it does not know" block has no recorded baseline — deviation 1.* |
> | 4 | TOML parses, ≥ 16 entries, `reason` + `d_ref` each, rendered block matches | **17 entries**, all fields present, `--check` exits 0, compared per entry |
> | 5 | every prohibition names a brief and a suite; zero blanks | **17 rows**, all five cells non-empty, every status cell names an `EP-n`. **Every row reads *unenforced — planned EP-n*, because nothing is built** — including P-16, whose README wording exists but whose CI check (EP-6) does not |
> | 6 | stop criterion: both thresholds, both pivots, Wilson, power limit, public halt | all present in §11; `10 ?%`/`5 ?%`/`Wilson` → **4 matches** |
> | 7 | "never a generative classifier", risk-detector line repeated, rendering rule | all present in §9; the risk-detector pair appears **twice** in the file, in §3 and §9 |
> | 8 | mode (c) clause verbatim, pairing rule, EP-48 named | rendered in D-20's exact form — `> **Charter clause:** moral injury arises from conditions, not individual deficiency.` → **1 match** |
> | 9 | review status: author-only, mode (a) gate, both labels | §16, with a per-mode label table |
> | 10 | every link resolves except `SECURITY.md` | **confirmed** — deviation 5 |
> | 11 | `pytest` and CI green | `ruff check` "All checks passed!"; `ruff format --check` "14 files already formatted"; `pytest -m "not requires_index and not requires_model" -q` → **16 passed**. No committed blob contains a carriage return |
> | 12 | *(owner judgement)* a clinician can state the refusals, the stop condition, and the evidence | offered for confirmation; §3, §6, §11 and §16 are the four sections that answer it |
>
> Pre-publication items re-run: **3 (protected text)** — the charter quotes no corpus text at all, the
> D-74 budget is stated in §14 and self-applied at **zero words used**, and the only quoted material
> is this project's own governance. A sweep of the new files found no occurrence of the retired
> modality term, no absolute path, no machine identifier and no corpus path. **7 (public claims)** —
> README, badge and `SAFETY.md` agree: `status: design`, no release, author review only, no evidence
> of benefit.
>
> #### For later briefs
>
> - **EP-4** must make the `SECURITY.md` link resolve, and should update the link test's expected list
>   rather than deleting the test.
> - **EP-39** consumes `epppsynth/copy/banned-phrases.toml` directly. The scope of the lint is fixed in
>   §10 (deviation 7), and the two `condition` entries need matcher support rather than a plain grep.
> - **EP-44** renders §9's escalation block from a constant. The exact panel copy — including the
>   `988` and `911` lines and the "outside the United States" sentence — was **authored here**, since
>   D-18 fixes only the resources and D-57 only the heading. If the owner wants that copy settled as a
>   decision rather than as charter text, it wants a dated addendum at the EP-8 re-plan.
> - **EP-8**'s context-budget check should note that `SAFETY.md` is not in the load order; the briefs
>   that need it (EP-20, EP-26, EP-39, EP-44) name it as a step-6 source file.

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
