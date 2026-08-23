# EP-24 — Eval harness, result schema, scenario schema, taxonomy, coverage

**Size:** L · **Mode:** n/a (harness) · **Core/Stretch:** core ·
**Depends on:** EP-21 (composition, linters, CLI) ·
**Blocks:** EP-25 (dev scenario set), EP-26 (red-team scenario set), EP-27 (held-out freeze), EP-28
(substance-tuple extractor)

> **Charter.** **EP-23 (engine integration, fixtures, re-plan P2)** upgrades this to a full brief:
> `## Scope sketch` splits into `## In scope` / `## Out of scope`, and each sketched criterion below
> becomes a named command or artifact. Do not execute from the sketch alone.

## Context

Implements D-35(1) and D-36. P3 precedes P4 deliberately: D-17 makes the deterministic baseline both
the shipped default and the anti-hallucination control arm, so it must be measurable before a model
may compete with it. Nothing evaluative exists in the tree; what exists after P2 is `epppsynth run`
emitting a validated three-part `OutputBundle` (EP-21), the abstention and hard-stop chain (EP-20),
the registry loader and its version hash (EP-18), and the contracts package (EP-17).

This brief is the floor every other P3 brief stands on. Two tiers: **Tier D** (deterministic) runs
in CI on every commit on the no-model path (D-42) at 100 % pass; **Tier S** (stochastic) runs locally
only, gates on an interval lower bound, never enters CI. D-75's thresholds are inputs here, not
decisions, and live in one file so the P3 re-plan can revise them in one place: paired preference
**30–40 pairs / 40 outputs per reviewer** · multi-run **N = 5 dev, N = 10 release** over ≥ 2 seeds ·
stability floor **Jaccard 0.8** · abstention recall **1.00** on the out-of-scope and hard-stop
triggers, **0.95 recall / 0.85 precision** on the rest · over-abstention ceiling **10 %** ·
unsupported-claim rate **≤ 2 %**.

## Safety preconditions

- **The scenario corpus is a public artifact** (D-3, D-42). A `no real person; wholly fictional;
  contains no PHI` attestation is a required schema field; a PHI-shaped pattern scan (DOB-, MRN-,
  SSN-, phone-, NPI-shaped) runs over it; re-run the pre-publication checks for local paths,
  hostname and username.
- **No retention** (D-8): logs and CI artifacts carry metrics, IDs and version identity only — never
  a prompt, an output body, or case free text.
- **LLM-as-judge is rejected**: no scorer, comparator or checker may call a model — it would collapse
  the independence of the control arm (D-17). Enforced structurally: the eval package does not import
  the inference path.
- **D-56:** no report string calls the LLM path deterministic; bit-identical tests are baseline-only.
  An unstable case is a **failure**, not a curiosity — seeds do not give GPU bitwise determinism, and
  the clinician cannot know which run they got.

## Scope sketch (refine at re-plan)

1. `epppsynth.eval` package and an `epppsynth eval` subcommand; no-model path by default.
2. **Result schema** — per case: id, set, suite, expected class, run records, pass/fail, the version
   triple (registry / schema / contract), thresholds-file hash, build hash.
3. **Scenario schema** with provenance front matter: `id · set (dev|redteam|heldout) · author_type
   (human|llm_reviewed) · generator_model + revision · created · reviewed_by/on · expected_class ·
   axes · attestation · licence (CC BY 4.0) · content_hash`.
4. **Taxonomy — six required axes:** `mode` · `expected_class` (ordinary | abstain-1…5 | hard-stop) ·
   `illness_stage` · `preference_profile` · `free_text` (absent | plain | adversarial) · `difficulty`.
5. **Coverage checker** (CI): every `expected_class` has ≥ 3 positives and ≥ 3 near-miss negatives;
   every D-25 field appears with `unknown`, `not relevant` and `prefer-not-to-answer`. Compute the
   cell count **before** EP-25 authoring and prune an axis if the D-36 scale cannot fill it.
6. **Tier D wiring:** schema validation, unit, property and consistency tests, golden files with an
   update ritual (a golden change requires a justification line in the commit message).
7. **Multi-run runner:** N and seeds from `thresholds.yaml`; per case, exact-match rate, modal
   substance agreement (delegated to EP-28), mean pairwise concept-set Jaccard; < 0.8 ⇒ unstable ⇒
   failed. **Wilson 95 % helper**; gates read the lower bound, never the point estimate.
8. `thresholds.yaml` (D-75) plus an `eval-report.json` / `eval-report.md` renderer.

## Verification / acceptance (sketch)

- A dev-set dry run exits 0 with no model present and emits a schema-valid result file; the coverage
  checker fails on an injected under-covered `expected_class` and on a missing attestation.
- The Wilson helper matches hand-computed bounds at n = 30, k = 0 and n = 40, k = 2.
- Every report carries the version triple, the thresholds hash and the build hash.
- A check asserts `epppsynth.eval` imports nothing from the inference package.
- *(judgement — author)* the taxonomy cell count is affordable at the D-36 scenario scale.

> **Note (2026-08-23).** The taxonomy keeps a `free_text` axis (absent | plain | adversarial). It is a
> useful scenario-authoring dimension, but because free text is an inert echo it **cannot change
> deterministic output**: its cells must never be read as coverage of engine behaviour, only of
> rendering and of the model path. State this where the coverage report is generated.

## Parked → final-roadmap.md

- Standalone LLM-arm vs baseline comparison report (stretch); the comparison run itself is EP-36.
- Per-mode thresholds and mode (b)/(c) eval sets — EP-49.
