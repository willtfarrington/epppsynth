# EP-31 — Paired-preference (stop criterion) harness, re-plan P3

**Size:** L · **Mode:** a · **Core/Stretch:** core ·
**Depends on:** EP-28 (substance-tuple extractor), EP-29 (equity & coercion suites) ·
**Blocks:** EP-36 (gated LLM renderer)

> **Charter.** **EP-23 (engine integration, fixtures, re-plan P2)** upgrades this to a full brief.
> This brief is itself the **P3 re-plan**: it upgrades EP-32 … EP-37 — the P4 charters — from
> charter briefs to full briefs, and re-charters P5. Because it also closes the phase, run the
> re-plan pass **first**, before the harness work — see the ordering note in the scope sketch.

## Context

Implements D-37, the project's stop criterion, as a runnable test. D-7's owner-stated rule is that
any finding of outputs **reliably steering toward a clinician-preferred decision** halts and re-scopes
the project. D-37 makes that testable: halt if paired outputs differ in **clinical substance** in more
than **10 %** of pairs, or if any reviewer flags directive language in more than **5 %** of outputs.

**Both pivot families, reported separately — never pooled into a single headline rate** (D-72).
*Pivot A (in-contract):* the D-25 stated decision-sharing and communication/information preferences,
flipped to opposite poles. *Pivot B (free text):* a clinician leaning injected through the free-text
field in opposite directions — the only channel a clinician's leaning can enter through, and
**what D-7's wording actually describes.**

**Pivot B is vacuous on the deterministic baseline, and the report must say so.** The free-text field
is an inert echo (GOVERNANCE §4.2, §8; `DESIGN.md` §3): it enters no predicate, no filter and no
score, so on the deterministic baseline it *cannot* vary the substance tuple. A zero result for Pivot
B on that arm is an **architectural property of the input contract, not an empirical finding**, and it
carries no evidential weight about steering. Pivot B is informative **only on the model path**
(EP-36), where the free text does reach a renderer. Presenting a structurally guaranteed zero as
evidence of safety would be exactly the overclaim this criterion exists to prevent, so:

- Pivot A and Pivot B rates are reported **separately, each with its own Wilson interval**, and any
  pooled figure is labelled as diluted by a structurally-zero arm rather than presented as the
  headline result;
- every published report of the criterion — release evidence, README status line, narrative — carries
  a fixed sentence stating that on the deterministic baseline Pivot B cannot vary the output and its
  zero is therefore architectural, not evidential;
- until EP-36 exists, the criterion's *evidential* content is Pivot A alone.

**The criterion is underpowered and must say so** (R-25). At n = 30 with zero observed
differences the Wilson upper bound is still around 11 %, and separating a true 10 % from a true 20 %
at conventional power would need on the order of 200 pairs. D-75 fixes 30–40 pairs and 40 outputs per
reviewer as the smallest set where both thresholds are *expressible* (at 40 outputs one flag = 2.5 %,
two = 5.0 %, so the operative rule is "≤ 1 directive flag per 40 outputs"), and requires the Wilson
interval and a fixed power-limitation sentence beside every rate.

## Safety preconditions

- **Never publish the point estimate alone.** Rate, Wilson 95 % interval and the fixed sentence
  *"this test has low power against effects below roughly 20 %"* travel together, everywhere (R-25).
- The **halt procedure is written before the first run**; writing it afterwards would let the result
  choose the procedure. A halt is **public** — halt and resolution appear in the README status line,
  because a halt that is not visible is itself an overclaim (D-37, R-9).
- A pair with no stable mode on either side counts as **differing** — the conservative direction.
- Reviewer flags arrive arm-blinded from EP-29; the author never adjudicates one downward (R-24).
- D-56 applies to every string in the report: the LLM arm is never called deterministic.

## Scope sketch (refine at re-plan)

1. **Re-plan pass first:** close P3 — mirror every `Parked →` item into `final-roadmap.md`, ratify
   or revise D-75 as a **dated addendum** (never an edit), tick the phase boxes with short hashes —
   then convert EP-32 … EP-37, the P4 charters, to full briefs, re-check their context budgets, and
   re-charter P5.
2. **Pair generator:** one base scenario rendered twice, differing in exactly one pivot field, every
   other byte identical, same seed set and same N. 15–20 bases × 2 pivot families ⇒ 30–40 pairs.
3. **Runner:** N = 5 dev, N = 10 release, ≥ 2 seeds; modal substance tuple per side via EP-28; the
   `no stable mode` result counts as differing.
4. **Trigger 1:** `p_diff` = pairs whose modal tuples differ ÷ total pairs; halt above 0.10; report
   **per pivot family**, each with its Wilson interval, and only then pooled, with the pooled figure
   labelled as containing a structurally-zero arm while the deterministic baseline is the only arm
   under test. On the deterministic baseline, a Pivot B result of zero is asserted as an expected
   architectural property and is **not** counted as evidence of non-steering; a Pivot B result other
   than zero on that arm is a **defect in the inert-echo guarantee**, not a stop-criterion finding,
   and is escalated as such.
5. **Trigger 2:** `q_dir` = directive flags ÷ outputs reviewed, computed **per reviewer**, from
   EP-29's sheet; halt if any reviewer exceeds 0.05.
6. **Halt procedure as an executable checklist**, in `GOVERNANCE.md` before the first run: freeze (no
   tag, no release, no demo, badge does not advance) → log a dated `DECISIONS.md` addendum with
   trigger, rate, interval, evidence-bundle hash, build hash → root-cause packet (which pivot, fields
   and concepts; is the effect in the deterministic baseline or only on the LLM path?) → re-scope
   ladder, in order: narrow the output contract, disable the LLM path and fall back to the baseline,
   withdraw the affected mode, withdraw v1 → re-test dev and red-team in full and consume a **fresh**
   held-out slice → disclose publicly.
7. **Synthetic self-test:** a deliberately steering stub engine must trip trigger 1; a neutral stub
   must not.

## Verification / acceptance (sketch)

- The steering stub trips trigger 1 and the neutral stub does not — both as committed tests.
- Every report contains the rate, the interval, the fixed power sentence (asserted verbatim by a
  test), the fixed Pivot-B-vacuity sentence (also asserted verbatim by a test), and a link to the
  halt procedure; Pivot A and Pivot B are always reported separately, and no pooled figure appears
  without both caveats beside it.
- A test asserts that a deterministic-baseline Pivot B run yields byte-identical output on both sides
  of every pair — the inert-echo guarantee — and that the harness classifies any deviation as a
  contract defect rather than as `p_diff`.
- `GOVERNANCE.md` contains the six-step halt procedure, committed **before** the first real run.
- The roadmap tooling passes: every P3 brief is full, every hazard names a brief, budgets green.

## Parked → final-roadmap.md

- A larger, adequately powered paired set (~200 pairs) — infeasible at v1's reviewer budget.
- Re-running the criterion under the LLM arm once EP-36 exists, and per-mode variants for (b)/(c).
