# epppsynth — Roadmap

Master roadmap for building the local reflection aid described in
[`../epppsynth/DESIGN.md`](../epppsynth/DESIGN.md), under the rules of
[`../epppsynth/GOVERNANCE.md`](../epppsynth/GOVERNANCE.md), implementing the decisions in
[`../epppsynth/DECISIONS.md`](../epppsynth/DECISIONS.md) (D-1 … D-78, settled with the project owner
in the planning session of **2026-08-23**).

**Planned 2026-08-23.** v1 is **55 self-contained session briefs across 8 phases** (EP-0 … EP-54).
P0–P2 have full briefs now; P3–P7 have **charter briefs** that each phase's re-plan EP upgrades to
full briefs. Every named idea that is not built in v1 is parked in
[`final-roadmap.md`](final-roadmap.md).

**What "done" means for v1.** Not feature completion — **evidence**. The `v1 — mode (a)` tag is cut
only when the eight release-gate items of D-35/D-67 are satisfied and their artifacts exist in
`release-evidence/<tag>/`. Modes (b) and (c) are separate gates (D-13), and both carry public
"author review only" labels because reviewer sign-off gates mode (a) alone (D-65, D-66).

## How to use this roadmap

Each `EP-n-*.md` brief is **self-contained**: a session that has read only that brief plus the
load-order files below can execute it. Hand one brief to one session. Execute in order, verify the
acceptance criteria, commit, then check the box here.

**Minimum context load order for a cold session** (stop when the brief's needs are met):

| # | File | Why |
|---|---|---|
| 1 | `CLAUDE.md` | session rules, never-do list, command conventions |
| 2 | `epppsynth/GOVERNANCE.md` | overrides DESIGN and every brief |
| 3 | `epppsynth/DECISIONS.md` — **index block only** | which decisions exist; open a full entry only for a `D-n` the brief cites |
| 4 | `roadmap/README.md` — **the one phase table + its standing-decisions paragraph** | ordering, dependencies, phase conventions |
| 5 | `roadmap/EP-n-<slug>.md` | the work |
| 6 | only the source files the brief names | — |

**Never read at pickup:** `.local/` (private planning state), `source material/` (copyrighted,
D-10), other briefs, `final-roadmap.md`, or `DESIGN.md` in full. `tools/roadmap_check.py
--context-budget EP-n` sums items 1–5 and fails above 15k tokens. It is close: items 1–3 alone cost
about **52 %** of the ceiling before a brief is opened, and the tightest brief clears it by fewer
tokens than the approximation's own error. The tool prints both figures on every run (OD-16).

Workspace: `epppsynth/` (the uv project, directly under the repository root). Git root: the
repository root (`README.md`, `epppsynth/`, `roadmap/`, `source material/`, `tools/`).

**Canonical paths** (fixed here so briefs do not diverge): package docs and ADRs live under
`epppsynth/docs/` (`epppsynth/docs/adr/`, `epppsynth/docs/evidence/`, `epppsynth/docs/rights.md`);
the concept registry lives under `epppsynth/registry/` (`epppsynth/registry/sources.yaml`); release
evidence under `release-evidence/<tag>/`; the model and index roots are outside the repository.

**Sizes** (D-22): S ≈ 30 min · M ≈ 1 h · L ≈ 2 h of one supervised session; anything larger is split
at pickup. Current mix: **2 S · 17 M · 36 L ≈ 90 h** — roughly three months at 7 h/week (D-39). This
line is **derived, not maintained**: `roadmap_check --table` recomputes it from the eight phase
tables and fails if the two disagree. Recomputed at EP-8 it was unchanged. Sizes were **not**
recalibrated against P0's actuals, and [`P0-retro.md`](P0-retro.md) says why.

**Core / Stretch.** The `Core` column is the cutline: if time runs short, stretch briefs drop first
(numbering gaps are fine — hupsim precedent). Re-plan EPs may move briefs across the line.

**Charter briefs** (P3–P7) use `## Scope sketch (refine at re-plan)` and
`## Verification / acceptance (sketch)` and carry a `> **Charter.**` note naming the re-plan EP that
upgrades them.

**Conventions carried over from `hupsim` and `mimicwarehouse`** (use verbatim):
`> **Completion note (date).**` appended to executed briefs · `> **Addendum (date, EP-n).**` under
decisions · `> **EP-n pickup note.**` when a later session picks up a stale brief ·
`~~risk~~ **Resolved by EP-n (date)**` strike-throughs · two-hash ☑ boxes when an EP spans two
commits · `EP-n-completion-handoff.md` / `-completion-report.md` pairs for context-limit rescues ·
commit pairs `feat(epppsynth): … (EP-n)` then `docs(roadmap): record EP-n commit hash`, plus a third
`docs(roadmap): record EP-n CI run` when the work is pushed (OD-15) ·
`docs(roadmap): add EP-n — …` when a brief is added mid-phase · every brief carries a
`## Parked → final-roadmap.md` section mirrored at the phase re-plan.

**`Depends on` / `Blocks` convention.** Both header fields name **immediate neighbours only** — never
transitive ones — and the two must be **exact mirrors** of each other: `EP-a` lists `EP-b` under
`Depends on` **if and only if** `EP-b` lists `EP-a` under `Blocks`. The `Depends on` column of the
phase tables above is the authority; every brief's `Blocks` line is derived from it. A brief that
nothing depends on carries `Blocks: —` (phase-gate ordering that is not a dependency is stated in
this README, not in the header line). `roadmap_check --deps` fails on any asymmetry. The header block
is one contiguous block ending at the first blank line; a `> **Charter.**` note goes below it, never
inside it.

**Definition of Ready.** Every `Depends on` is ☑ · the safety-preconditions section is written ·
every acceptance criterion names a command or an artifact · no step requires a decision the owner
has not made (if one does, the brief is **blocked**, not started) · the context budget passes.

**Definition of Done.** Acceptance commands green · `> **Completion note (date).**` appended
including deviations · any decision change recorded as a dated addendum in `DECISIONS.md` (never an
edit) · `## Parked →` items mirrored at the next re-plan · two commits · ☑ ticked with the short
hash · for any brief touching a public artifact, the relevant pre-publication checklist items re-run
· **a completion note that claims CI green names the run as a linked id** (OD-15), and a brief whose
acceptance names CI stays `◐` until that run exists.

---

## Phase P0 — Foundation, governance, public-safety (full briefs)

| # | Brief | Size | Depends on | Core | Done |
|---|-------|------|-----------|------|------|
| EP-0 | [Baseline & public-safety hygiene](EP-0-baseline.md) | S | — | core | ☑ 3706992 |
| EP-1 | [Toolchain, package skeleton, ADR framework, CI](EP-1-toolchain.md) | M | EP-0 | core | ☑ c29c95a + a4403e6 |
| EP-2 | [Canonical docs + public front matter + badge scheme](EP-2-canonical-docs.md) | L | EP-1 | core | ☑ 8dd937a |
| EP-3 | [SAFETY.md — clinical-ethics charter](EP-3-safety-charter.md) | L | EP-2 | core | ☑ 7a5ecbb |
| EP-4 | [PRIVACY, SECURITY, CODE_OF_CONDUCT, CONTRIBUTING](EP-4-privacy-security-conduct.md) | M | EP-2, EP-3 | core | ☑ 083137d |
| EP-5 | [Licensing pack + per-source rights table](EP-5-licensing-rights.md) | L | EP-2 | core | ☑ b3424b2 |
| EP-6 | [Leak-prevention CI + pre-publication packet](EP-6-leak-prevention-ci.md) | L | EP-1, EP-2, EP-5 | core | ☑ c0edef5 + 4efc7a2 |
| EP-7 | [Storage roots, cache inventory, reserve floor & project ceiling](EP-7-storage-inventory.md) | L | EP-1 | core | ☑ 88faeef |
| EP-8 | [Roadmap tooling, EP template, re-plan P0](EP-8-replan-p0.md) | L | EP-0 … EP-7 | core | ☑ 0733b2c |

> **EP-6 was `◐` for a day, and the distinction earned its keep.** The row was held at *done but not landed* until the two CI rows existed, because a brief recorded as complete on evidence that does not yet exist is the drift the roadmap exists to catch. Closing them took three further commits: the first pushed run caught a shallow-clone defect that no local run could reach. Both runs are recorded in the brief's completion note. `roadmap_check --table` (EP-8) should still read `◐`, because the state recurs.

**P0 closed 2026-09-01 at EP-8.** The retro — estimate against actual, deviations, and what each
brief found harder than it expected — is [`P0-retro.md`](P0-retro.md). Its headline: **55 deviations
across eight executed briefs, and not one executed exactly as written.** Nine briefs' parked items
are mirrored into [`final-roadmap.md`](final-roadmap.md), and `tools/roadmap_check.py --parked`
counts them one for one from here on.

**Ordering rationale.** EP-0 first so every later commit is guarded by a verified `.gitignore` and a
clean-history assertion before any content exists — the repository is already public (D-3), so the
usual "tidy it before publishing" order is unavailable. EP-1 precedes everything that runs a command.
EP-2 lands the canonical docs before EP-3/4/5 write into them. EP-5 precedes EP-6 because the leak
scanners enforce the rights table's rules. EP-7 is independent of the docs and may run in parallel
with EP-2 … EP-6.

**Standing decisions for P0.** Repository is public; every artifact is public-safe by default (D-3).
Apache-2.0 code + CC BY 4.0 content, REUSE-conformant (D-28, D-50). CI on `windows-latest`, minimum
token permissions, third-party actions pinned to commit SHAs, deterministic no-model path only
(D-42). Storage: **floor** ≥ 250 GiB free on the system volume at all times, **ceiling** 25 GB total
for the project's model and index roots, warned at 20 GB (D-78). Scanners are defense in depth, never
proof (GOVERNANCE §Public-safety).

**Pending owner decisions.** Rulings that an executed brief raised and could not make for itself are
registered in [`owner-decisions.md`](owner-decisions.md). **Eighteen are open or ruled at P0's
close**: thirteen were opened on 2026-08-31 from EP-1 … EP-4, two more came from EP-6 and EP-7, and
EP-8 opened three. Each names where its ruling lands (a dated `DECISIONS.md` addendum, a platform
action, or a re-plan note); the register records them, it does not settle them, and the ☑ goes on
only once the ruling exists where that line says.

**The owner ruled at the re-plan on 2026-09-01, and two remain.** Closed that day: **OD-1** —
Projects was disabled through the platform and all four D-76 flags re-observed matching; **OD-16** —
the context ceiling is accepted as it stands and the remedy for the next breach is **named in
advance**, split the offending brief (D-22), never a shared load-order file and never the ceiling;
**OD-18** — the GiB/GB transcription is kept, because each unit matches what its number is compared
against; and **OD-17** — `setup-uv` bumped to v10.0.1 in a commit of its own, *after* EP-8's CI run
was recorded, so a red run could not be ambiguous between the two, with the first by-hand pin review
written up as an `ADR-008` amendment and the obligation handed to EP-16.

**Two remain open, and no P1 brief is blocked on either.** **OD-2** asks whether `SAFETY.md` §4
matches the approved draft, which only the owner can compare because the draft is private planning
state. **OD-8** needs one signed-in human look at the issue form: it is published where the platform
reads issue forms from, and no path available to a session shows it rendering. Both are open for the
same reason — each needs a human to look at something no session can reach.

## Phase P1 — Conceptual & content model (full briefs)

| # | Brief | Size | Depends on | Core | Done |
|---|-------|------|-----------|------|------|
| EP-9 | [Registry schema v0 — types, relations, IDs, versioning](EP-9-registry-schema.md) | L | EP-2 | core | ☐ |
| EP-10 | [Provenance, rights, reuse class, citation rule, authoring guide](EP-10-provenance-authoring.md) | L | EP-5, EP-9 | core | ☐ |
| EP-11 | [Composer specification](EP-11-composer-spec.md) | L | EP-9 | core | ☐ |
| EP-12 | [Seed content A — existential givens + ordinary-concern counter-frame](EP-12-seed-givens.md) | L | EP-10, EP-11 | core | ☐ |
| EP-13 | [Seed content B — communication functions + evidence appendix](EP-13-seed-functions.md) | L | EP-10 | core | ☐ |
| EP-14 | [Seed content C — trauma-informed principles + moral-injury conditions](EP-14-seed-principles-conditions.md) | L | EP-10 | core | ☐ |
| EP-15 | [Critique-lens protocol + full lens run](EP-15-lens-review.md) | L | EP-12, EP-13, EP-14 | core | ☐ |
| EP-16 | [Registry validator, rendered markdown, re-plan P1](EP-16-validator-replan-p1.md) | M | EP-9 … EP-15 | core | ☐ |

**EP-9 opens with a pickup gate.** Three items closed P0 unresolved and none can be settled by a
session: **OD-2**, **OD-8**, and EP-8's twelfth acceptance criterion. They are carried in
[`pickup-gate.md`](pickup-gate.md), which EP-9's header names, and the third **blocks** EP-9 because
its answer can change the brief. Put all three to the owner before starting P1.

**Ordering rationale.** The schema (EP-9) precedes the provenance spec (EP-10) because rights fields
are schema fields; both precede any authored concept. The composer spec (EP-11) is written before
content so the content is authored against a known emission contract — in particular the requirement
that every emitted concept carries a counter-hypothesis and an insufficient-basis clause (D-53).
EP-12/13/14 are independent of each other and may run in any order. EP-15 needs all three seed sets
because the lens coverage gate is measured across the whole registry.

**Standing decisions for P1.** Content = existential givens (labelled as one tradition among several)
+ serious-illness communication evidence + trauma-informed care + moral-injury literature (D-14).
Narrative medicine, generalist spiritual care and disability-community critique are **review lenses**,
not content. Non-Western and non-secular frameworks are out of scope by decision; the enforcement is
labelling plus **tested abstention** (D-14, D-38.1). YAML/JSON registry, no formal ontology (D-15).
Registry target ≈ 40 concepts, gated on a coverage dry-run (D-47). `cultural_scope.claims_universality`
is hard-coded `false`. Lens veto is conditional, overridable only by a published rationale (D-45);
blocked concepts are published under "withdrawn / not adopted" (D-46). Public citations are
**chapter-level only**; quotation budget ≤ 25 words per quote, ≤ 150 per source (D-74). Normative
guidance is referenced, never ingested (D-62).

## Phase P2 — Deterministic engine (full briefs)

| # | Brief | Size | Depends on | Core | Done |
|---|-------|------|-----------|------|------|
| EP-17 | [Contracts package](EP-17-contracts.md) | M | EP-1, EP-11 | core | ☐ |
| EP-18 | [Registry loader, schema versioning, migrations](EP-18-registry-loader.md) | L | EP-9, EP-17 | core | ☐ |
| EP-19 | [Selection and ranking](EP-19-selection-ranking.md) | L | EP-18 | core | ☐ |
| EP-20 | [Abstention and hard-stop precedence chain](EP-20-abstention-hardstop.md) | M | EP-19 | core | ☐ |
| EP-21 | [Template composition, linters, CLI](EP-21-composition-cli.md) | L | EP-20 | core | ☐ |
| EP-22 | [Corpus ingest module and local index](EP-22-corpus-ingest.md) | L | EP-7, EP-17, EP-21 | core | ☐ |
| EP-23 | [Engine integration, fixtures, re-plan P2](EP-23-integration-replan-p2.md) | L | EP-17 … EP-22 | core | ☐ |

**Ordering rationale.** Contracts (EP-17) first, because the type graph is what makes D-23's
"no verbatim span in any exportable type" a structural property rather than a discipline. The
abstention and hard-stop chain (EP-20) runs **before** composition (EP-21) in both the code and the
roadmap: the chain executes first at runtime and is the one path that must work when everything else
fails. EP-22 (corpus ingest) is independent of the engine in *content*, but it registers its
subcommand with EP-21's CLI, so it follows EP-21 rather than running in parallel with it.

**Standing decisions for P2.** Deterministic baseline is the shipped default and the permanent
fallback (D-17); integer scoring, lexicographic tie-break, one concept per `family` in the top-k, no
floats, no clock, no RNG. "Deterministic" describes the baseline only, never the LLM path (D-56).
Every suggested utterance is a question or an offer, enforced by a linter at authoring **and** at
runtime (D-26b). The escalation panel renders from a constant with no dependency on registry,
template or model load (D-57). Corpus and index live outside the repository tree, gitignored, and
never enter CI (D-16, D-51). `pandoc` is **not** assumed present — it is absent on the target machine.

## Phase P3 — Evaluation (charter briefs; upgraded by EP-23, the P2 re-plan)

| # | Brief | Size | Depends on | Core | Done |
|---|-------|------|-----------|------|------|
| EP-24 | [Eval harness, result schema, scenario schema, taxonomy, coverage](EP-24-eval-harness.md) | L | EP-21 | core | ☐ |
| EP-25 | [Development scenario set (~20–30)](EP-25-dev-scenarios.md) | L | EP-24 | core | ☐ |
| EP-26 | [Red-team scenario set (~15)](EP-26-redteam-scenarios.md) | L | EP-24 | core | ☐ |
| EP-27 | [Frozen held-out set, freeze ritual, contamination checks](EP-27-heldout-freeze.md) | L | EP-24 | core | ☐ |
| EP-28 | [Substance-tuple extractor and comparator](EP-28-substance-tuple.md) | M | EP-9, EP-17, EP-24 | core | ☐ |
| EP-29 | [Counterfactual equity and coercion suites](EP-29-equity-coercion-suites.md) | L | EP-25, EP-27, EP-28 | core | ☐ |
| EP-30 | [Abstention, hard-stop and over-abstention suites](EP-30-abstention-suites.md) | L | EP-25, EP-26, EP-27 | core | ☐ |
| EP-31 | [Paired-preference (stop criterion) harness, re-plan P3](EP-31-paired-preference-replan-p3.md) | L | EP-28, EP-29 | core | ☐ |

**Ordering rationale.** The substance-tuple extractor (EP-28) is the single most load-bearing piece
of the evaluation: it powers both the counterfactual suite and the stop criterion, so it precedes
both. The held-out set (EP-27) is authored **before** any tuning run and frozen under a signed tag.
Evaluation precedes local inference (P4) deliberately — the baseline must be measurable before a
model is allowed to compete with it (D-17).

**Standing decisions for P3.** Held-out is author-written only, executed at most once per release
candidate, and a failure may be repaired only by changing the dev set and re-authoring — never by
editing the held-out case (D-36). Numeric thresholds are ratified in D-75 and revisited at this
re-plan. Multi-run variance is mandatory because seeds do not give GPU bitwise determinism; an
unstable case is a **failure**, not a curiosity. The stop criterion is underpowered at feasible
sample sizes and its report must publish the Wilson interval and a fixed power-limitation sentence
(D-37, R-25). LLM-as-judge scoring is rejected (it would collapse the control arm).

## Phase P4 — Local inference (charter briefs; upgraded by EP-31, the P3 re-plan)

| # | Brief | Size | Depends on | Core | Done |
|---|-------|------|-----------|------|------|
| EP-32 | [Benchmark packet schema and null packet](EP-32-benchmark-schema.md) | M | EP-7 | core | ☐ |
| EP-33 | [Runtime spike — GPU architecture go/no-go](EP-33-runtime-spike.md) | L | EP-32 | core | ☐ |
| EP-34 | [Model and embedding selection rubric (no weights chosen)](EP-34-model-rubric.md) | M | EP-33 | core | ☐ |
| EP-35 | [First measured run, degradation and cancellation ladders](EP-35-measured-run.md) | L | EP-34 | core | ☐ |
| EP-36 | [Gated LLM renderer, claim binding, baseline comparison](EP-36-gated-renderer.md) | L | EP-21, EP-35, EP-31 | core | ☐ |
| EP-37 | [Reviewer recruitment pack, re-plan P4](EP-37-reviewers-replan-p4.md) | M | EP-23, EP-35, EP-36 | core | ☐ |

**Ordering rationale.** The packet schema (EP-32) exists before the spike so the spike's output is a
comparable artifact rather than a note. EP-33 is the **highest-uncertainty brief in the plan** — the
prebuilt CUDA wheel's coverage of this GPU's compute capability is undocumented and unverified; its
first step is a go/no-go. EP-36 depends on P3 because "beats the baseline" is only meaningful against
the suites. EP-37 sits here because reviewer outreach opens once a functional stage exists (D-64). Planning
initially placed the recruitment pack in P0 as the longest-lead item; **D-64 supersedes that** — the
pack is drafted and outreach opens together, here. The cost is accepted and named: the mode (a) gate
is schedule-exposed, and EP-51 (human factors) is the first brief that cannot proceed without it.

**Standing decisions for P4.** Runtime is `llama-cpp-python`, in-process, no daemon, no listener;
`llama-server` is a documented fallback only if the spike fails (D-70). Weights are verified by
revision + file hash, remote code execution disabled, no pickle formats, GGUF only, and the same
rules apply to embedding models (D-31, D-44). One model at a time, ≤ ~8 GB each, individually
confirmed before download (D-30). Models live in the project model root, never Git/LFS. The LLM is a
**renderer, not an author** — it receives selected concept IDs and authored paraphrases, never the
registry wholesale, never the index, never a raw span (D-54). Ships only if it beats the baseline.

## Phase P5 — Interface, threat model, verification (charter briefs; upgraded by EP-37, the P4 re-plan)

| # | Brief | Size | Depends on | Core | Done |
|---|-------|------|-----------|------|------|
| EP-38 | [Threat model](EP-38-threat-model.md) | L | EP-1 | core | ☐ |
| EP-39 | [UI contract, copy deck, banned-phrase lint](EP-39-ui-contract-copy.md) | L | EP-3, EP-21 | core | ☐ |
| EP-40 | [Loopback application shell](EP-40-app-shell.md) | M | EP-38, EP-39 | core | ☐ |
| EP-41 | [Loopback security controls and adversarial suite](EP-41-loopback-controls.md) | M | EP-40 | core | ☐ |
| EP-42 | [Input form](EP-42-input-form.md) | M | EP-40, EP-41 | core | ☐ |
| EP-43 | [Waypoints panel, abstention and hard-stop renders, focus management](EP-43-waypoints-panel.md) | L | EP-42, EP-21 | core | ☐ |
| EP-44 | [Escalation panel and local escalation config](EP-44-escalation-panel.md) | S | EP-40 | core | ☐ |
| EP-45 | [Provenance drawer](EP-45-provenance-drawer.md) | M | EP-43, EP-16 | core | ☐ |
| EP-46 | [No-retention and no-egress harness, accessibility packet, re-plan P5](EP-46-verification-replan-p5.md) | L | EP-40 … EP-45 | core | ☐ |

**Ordering rationale.** The threat model (EP-38) precedes the first line of UI code, because the
content security policy determines that templates must be CSP-clean from the first commit — a
loopback UI raises a browser trust boundary while v1 has no authentication.
EP-41 is separated from EP-40 so the eight controls are tested as controls, not as incidental
behaviour. EP-44 is small and safety-critical and is kept its own brief so it is never folded into a
larger change.

**Standing decisions for P5.** Starlette + Jinja2 + one vendored htmx + hand-written CSS, no npm, no
build step, no CDN, with a **tested** no-JS full-page-POST fallback (D-68). Bound to loopback with an
Origin/`Sec-Fetch-Site` check, a **Host-header allowlist** (the DNS-rebinding control, which
Origin/CSRF does not provide), a one-shot launch token bound at first load with **no idle
expiry**, a session CSRF token, and a strict CSP. Loopback is not treated as a security
boundary. The escalation panel renders byte-identically on every response — one distinct hash across
the eval corpus (D-57, R-34). Uncertainty, counter-hypotheses, insufficient-basis and abstention text
render at the same size, weight and contrast as hypotheses (D-58, R-33). WCAG 2.2 AA, tested with
axe-core plus a scripted manual pass using Windows Narrator; the public statement says "built to …
tested by … not independently audited", never "compliant" (D-67, R-32). No animation, no streaming
reveal, no copy-all, no confidence numbers.

## Phase P6 — Modes (b) and (c) (charter briefs; upgraded by EP-46, the P5 re-plan)

| # | Brief | Size | Depends on | Core | Done |
|---|-------|------|-----------|------|------|
| EP-47 | [Mode (b) — trainee profile and non-surveillance guarantee](EP-47-mode-b-trainee.md) | M | EP-46 | core | ☐ |
| EP-48 | [Mode (c) — clinician self-reflection profile](EP-48-mode-c-self-reflection.md) | L | EP-47 | core | ☐ |
| EP-49 | [Per-mode eval sets, author-review labels, re-plan P6](EP-49-mode-gates-replan-p6.md) | L | EP-47, EP-48 | core | ☐ |

**Ordering rationale.** Modes are built a → b → c (D-13); (b) and (c) come after mode (a)'s interface
and verification exist, so each is a profile over a proven engine rather than a parallel product.

**Standing decisions for P6.** Mode (b): strictly local, no accounts, no scoring, no retention, no
export, no employer visibility, voluntary use only, with a written non-surveillance guarantee
(D-19). Mode (c): scoped to naming structural and existential dimensions of a clinical experience;
refuses distress screening, scoring and diagnosis; any output set containing a `personal-meaning`
concept must also contain a `structural` one, enforced by the composer (D-20, R-16); ships
`draft`-labelled with a "no evaluation exists for this mode" banner (D-66). Reviewer sign-off gates
mode (a) only, so (b) and (c) carry public "author review only" labels (D-65).

## Phase P7 — Release readiness and portfolio (charter briefs; upgraded by EP-49, the P6 re-plan)

| # | Brief | Size | Depends on | Core | Done |
|---|-------|------|-----------|------|------|
| EP-50 | [Release-gate evidence bundle and CI enforcement](EP-50-release-evidence.md) | L | EP-46 | core | ☐ |
| EP-51 | [Human-factors protocol and run](EP-51-human-factors.md) | L | EP-37, EP-46 | core | ☐ |
| EP-52 | [Mode (a) gate assembly, IP clearance checkpoint, badge upgrade](EP-52-mode-a-gate.md) | M | EP-50, EP-51 | core | ☐ |
| EP-53 | [Clinical-reader narrative and site card correction](EP-53-narrative-site.md) | M | EP-52 | core | ☐ |
| EP-54 | [Final retro and final-roadmap compilation](EP-54-final-retro.md) | M | EP-53 | core | ☐ |

**Ordering rationale.** The evidence machinery (EP-50) exists before the gate is assembled (EP-52),
so the gate is a check rather than a construction. EP-53 follows EP-52 because the public narrative
and the site card quote the README status line, which only becomes true at the gate (R-36).

**Standing decisions for P7.** The `v1 — mode (a)` tag requires all eight gate items with artifacts
in `release-evidence/<tag>/` and a manifest whose recorded build hash equals the tagged commit
(D-35, D-67, R-30). The maturity badge is a static README string that CI resolves to an evidence file
and refuses to upgrade without it (D-59). The employment/IP clearance checkpoint (D-29) gates the
first public tag. Everything on the personal site beyond the one project card is out of scope (D-43).
If a stop-criterion trigger fires, the halt and its resolution appear in the public README — a halt
that is not visible is itself an overclaim (D-37, R-9).

---

## Traceability

Concept/need → requirement → architecture/content → brief → evidence is maintained in
[`../epppsynth/DESIGN.md`](../epppsynth/DESIGN.md) §Traceability. Every hazard `R-1 … R-41` in
[`../epppsynth/DESIGN.md`](../epppsynth/DESIGN.md) §14 names the brief that mitigates it and the gate
that verifies it; `tools/roadmap_check.py --hazards` fails if a hazard names no brief, if a cited
`R-n` does not exist there, or if a core brief names no acceptance evidence. `--all` runs all ten
checks and is what CI calls.
