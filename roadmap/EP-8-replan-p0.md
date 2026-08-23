# EP-8 — Roadmap tooling, EP template, re-plan P0

**Size:** L · **Mode:** n/a · **Core/Stretch:** core ·
**Depends on:** EP-0 (baseline), EP-1 (toolchain), EP-2 (canonical docs), EP-3 (SAFETY charter), EP-4 (privacy/security/conduct), EP-5 (licensing pack), EP-6 (leak-prevention CI), EP-7 (storage inventory) · **Blocks:** — (nothing in the master table lists this brief as a dependency; the phase gate is stated in the README, not here)

## Context

EP-8 closes P0. It does three things that only make sense once the other eight briefs are done:
it builds the tooling that keeps the roadmap honest, it ratifies the brief template against nine
briefs that were actually executed, and it runs the phase re-plan — the point at which P1 and P2
are checked for consistency against what P0 actually built, and everything each brief parked is
mirrored into `final-roadmap.md`.

**What exists.** A public repository with: a verified baseline and `.gitattributes`; a uv project
with a CLI, ADRs and CI; canonical docs and the badge scheme; `SAFETY.md` with the banned-phrase
data file; the four policy documents; the licensing pack and the generated rights table; seven
scanners with seven recorded red runs and a pre-publication packet; and the storage roots, guards
and inventory. `roadmap/_TEMPLATE.md` and `roadmap/README.md` were committed by EP-0 as part of the
planning baseline. `roadmap/final-roadmap.md` already exists with seeded content, verified
unmodified by EP-0 — **EP-8 extends it.**

**What this brief creates.** `tools/roadmap_check.py`, the extended `final-roadmap.md`, the P0
retro with real timings, consistency-checked P1 and P2 briefs, and the corrected roadmap header
figures.

**The size mix is recomputed, never restated.** EP-8 derives it from the eight phase tables and
writes the result into the header; `roadmap_check.py --table` asserts the header agrees with the
tables from that point on. Do not carry a remembered figure into this brief — a hand-maintained
summary of a machine-readable table is exactly the drift the tool exists to prevent.

Implements: D-22 (sizing, phase re-plan EP closing each phase, core/stretch cutline, `☑ hash`
table), D-39 (phase structure), D-40 (roadmap bundle layout), and the compaction rule that the
README status paragraph and maturity badge are the one place rewriting at a re-plan is
**mandatory**. Mitigates R-9 (overclaim — a stale status paragraph is the cheapest overclaim
there is) and R-36 (narrative drift ahead of the badge).

## Safety preconditions

| Invariant at risk | Guard in this brief |
|---|---|
| A stale public status paragraph (R-9, R-36) | The compaction rule is applied and then **checked**: `roadmap_check.py --status` asserts the README badge, the README status paragraph, the `status: design` evidence file, and `CITATION.cff`'s `version` and abstract all agree. This is the one rewrite the re-plan makes mandatory. |
| Rewriting history rather than annotating it | Executed briefs' `## Context` sections are **never** rewritten — they are the historical record. Staleness is annotated with `> **EP-n pickup note.**`. `DECISIONS.md` gains dated addenda only, never edits. `roadmap_check.py --immutable` compares each executed brief's `## Context` against the blob at its recorded commit and fails on any change. |
| A context-budget gate that never fires | `--context-budget` is proven by a **deliberate red run** on a planted bloated probe brief, then the probe is deleted. A budget check that has never failed is a decoration. |
| Parked items quietly lost | `--parked` cross-checks that every `## Parked → final-roadmap.md` entry across all executed briefs appears in `final-roadmap.md`, and that the discovery-state residual list is represented one-for-one. A parked item that exists in only one of the two places fails the check. |
| The re-plan making public claims the evidence does not support | Every upgraded P1 brief is checked against the Definition of Ready before it is marked ready, and the badge stays `status: design` — P0 produced no engine, so nothing may move it. |
| `.local/` content entering the public roadmap while writing `final-roadmap.md` | The parked list is assembled from the briefs' own `## Parked →` sections and from the *public* residual statements, never by copying private ledger prose. EP-6's scanners run before the commit. |

Pre-publication checklist items exercised here: **all seven**, run as the packet, dated and signed
against the P0-closing commit. This is the first time the packet runs as a packet rather than as
individual checks.

## In scope

1. **`tools/roadmap_check.py`** with these modes, each independently runnable and each with unit
   tests over fixture roadmaps:
   - `--hashes` — every ☑ box carries a short hash that resolves in `git log`, and every brief whose
     box is ticked has a `> **Completion note (date).**`; conversely, no unticked brief has one.
     Support the two-hash form for briefs that span two commits.
   - `--deps` — parse `Depends on` / `Blocks` from every brief header, build the graph, fail on a
     cycle, fail on a dependency naming a brief that does not exist, and fail on an asymmetry (A
     depends on B but B does not list A under `Blocks`).
   - `--table` — the phase tables and the brief files agree: every table row has a file, every file
     has a row, sizes match, and the header's size mix and hour estimate are recomputed from the
     tables (this is the correction described above).
   - `--sections` — every brief has all six template sections in order, and `## Safety
     preconditions` is non-empty (an explicit `n/a` counts; an omitted section does not).
   - `--acceptance` — every brief's acceptance section names at least one command, detected as a
     fenced code block or an inline command token.
   - `--hazards` — every hazard R-1 … R-41 in `epppsynth/DESIGN.md` §14 names a mitigating
     brief and a verifying gate, and every **core** brief names at least one acceptance artifact.
   - `--context-budget EP-n` — sum the token cost of load-order items 1–5 for that brief
     (`CLAUDE.md`, `GOVERNANCE.md`, the `DECISIONS.md` **index block only**, the brief's phase table
     plus its standing-decisions paragraph, and the brief) and fail above ~15k tokens. Document the
     tokenizer used; if no tokenizer is available offline, use a documented character-based
     approximation and say so in the output, because a silent approximation is worse than a stated
     one.
   - `--parked` — the cross-check described in the safety preconditions.
   - `--immutable` — executed briefs' `## Context` sections unchanged since their recorded commit.
   - `--status` — the four-way agreement check described in the safety preconditions.
   - `--all` — run everything; this is what CI calls.
2. **Wire `roadmap_check.py --all` into CI** as a step in the existing scan job, with the same
   posture (no secrets, pinned actions, minimum permissions).
3. **Ratify `roadmap/_TEMPLATE.md`.** It was committed at EP-0 as part of the planning baseline.
   Now that nine briefs have been executed against it, either confirm it unchanged or amend it —
   and if amended, record what nine executions taught, and re-run `--sections` across all 55 briefs.
4. **Extend `roadmap/final-roadmap.md`** — it already carries the planning-session seed, so add to
   it and never replace it; an existing entry is amended in place, never dropped. Three sources of
   new entries:
   every executed brief's `## Parked →` section; the D-40/D-41 parked items (generalizing the
   hard-coded corpus spine; retaining `tools/` only if a non-package utility later needs it); and
   the public residual list — scenario-library UI, export and sharing, trainee opt-in retention,
   third-party installability, generalized corpus ingest, fine-tuning, any patient-facing mode.
   Group by theme, and give every entry a one-line reason and, where one exists, the condition that
   would reopen it.
5. **P0 retro.** Record, per brief: estimated size, actual elapsed time, what was harder than
   expected, and any deviation from the brief. Use the actuals to calibrate P1's sizes — D-22 says
   sizing is calibrated against actuals, and this is the first opportunity.
6. **Consistency-check P1.** EP-9 … EP-16 are **already full briefs on disk** — this is not an
   upgrade. Check them against the ratified template and against what P0 actually built: every
   `Depends on` / `Blocks` pair mirrors, every acceptance criterion names a command or an artifact,
   every cited `D-n` and `R-n` resolves, sizes reflect the retro's calibration, and each satisfies
   the Definition of Ready. Amend what has gone stale; do not rewrite a brief that is already
   correct.
7. **Consistency-check P2.** EP-17 … EP-23 are likewise **full briefs, not charters** — they need
   no re-chartering. Confirm or revise their scope in light of what P0 built — in particular EP-22
   (corpus ingest), which depends on EP-7's storage guards, on EP-21's CLI, and on the unresolved
   `pandoc` question (pandoc is absent on the target machine). The charter-to-full upgrade job
   begins at P3, whose briefs EP-23 upgrades.
8. **Apply the mandatory rewrite.** Update the README status paragraph and the maturity badge to be
   true as of the P0-closing commit. The badge remains `status: design` — P0 produced no engine.
   Update `epppsynth/docs/evidence/design.md` if any of its boxes changed meaning.
9. **Record dated addenda** in `DECISIONS.md` for anything P0 changed or discovered, including the
   size-mix correction and the deliberate GiB/GB transcription EP-7 flagged.
10. **Run the pre-publication packet** end to end (EP-6's seven items), sign it with the date and
    the P0-closing commit hash, and file it.
11. **Correct the roadmap header** with the recomputed size mix and hour estimate.
12. **Commits:** `feat(tools): add roadmap_check and close P0 re-plan (EP-8)` then
    `docs(roadmap): record EP-8 commit hash`.

## Out of scope

- Any P1 content: the registry schema, provenance fields, or any concept — **EP-9** … **EP-15**.
- Any change to the badge beyond confirming `status: design`. Moving it requires an engine, which
  is **EP-21**, and an evidence file, which is **EP-23**.
- Re-running EP-6's canary red runs. They are recorded once in EP-6's completion note; EP-8 runs the
  scanners green as part of the packet, not the canaries.
- Rewriting any executed brief's `## Context` — forbidden by the compaction rule, enforced by
  `--immutable`.
- The `prime` site card correction — **EP-53** (D-43).
- Reviewer recruitment materials. Currently scheduled at **EP-37** in P4; see the note below, which
  EP-8 must resolve as its first re-plan decision.
- Upgrading P3 … P7 charter briefs. The preceding phase's re-plan EP owns each upgrade (EP-23,
  EP-31, EP-37, EP-46, EP-49).

## Verification / acceptance

Runnable, from the repository root:

```powershell
uv run python tools/roadmap_check.py --all
uv run python tools/roadmap_check.py --context-budget EP-9
uv run python tools/roadmap_check.py --parked
uv run python tools/roadmap_check.py --immutable
uv run epppsynth scan --history
uv run pytest -q
```

Acceptance:

1. `roadmap_check.py --all` exits 0 against the real roadmap.
2. **Deliberate red runs**, each recorded with its output and then reverted:
   - a planted bloated probe brief fails `--context-budget`;
   - a planted dependency cycle fails `--deps`;
   - a ☑ box carrying a non-existent hash fails `--hashes`;
   - a brief with `## Safety preconditions` deleted fails `--sections`;
   - a brief whose acceptance section names no command fails `--acceptance`;
   - a parked item removed from `final-roadmap.md` fails `--parked`;
   - an edited `## Context` in an executed brief fails `--immutable`.
   Seven red runs, seven reverts, one green `--all` afterwards.
3. `--table` recomputes the size mix from the phase tables and the roadmap header now matches it.
   The completion note states the old figures and the new ones side by side.
4. `--hazards` reports every one of R-1 … R-41 with a mitigating brief and a verifying gate; zero
   unmitigated hazards and zero core briefs without acceptance evidence.
5. `--context-budget` passes for **every** brief in P0 and P1, not just a sample. Output recorded as
   a table.
6. `final-roadmap.md` still contains every entry it carried before this brief, plus every
   `## Parked →` entry from all nine P0 briefs and every item on the public residual list, each with
   a reason and, where applicable, a reopening condition. `--parked` green.
7. All eight P1 briefs exist as full briefs, pass `--sections` and `--acceptance`, and satisfy the
   Definition of Ready. Any that does not is marked **blocked** with the decision it is waiting on
   named — blocked is an acceptable outcome; a brief that looks ready and is not, is not.
8. The README status paragraph and badge are true as of the P0-closing commit, and `--status`
   confirms README, evidence file and `CITATION.cff` agree.
9. The pre-publication packet is executed, dated, and signed against the P0-closing commit hash,
   with items 5 and 7 recorded as human passes.
10. The P0 retro records estimate versus actual for all nine briefs, and P1's sizes are visibly
    adjusted by it (or the retro states explicitly that no adjustment was warranted).
11. CI green, including the new `roadmap_check.py --all` step.
12. *(judgement — the project owner)* Handing any one P1 brief to a cold session, with only the load
    order files, is sufficient to execute it.

## Parked → final-roadmap.md

- A rendered roadmap view (burndown, dependency graph image). `roadmap_check.py` builds the graph in
  memory already; rendering it needs a diagramming dependency and `pandoc` is absent.
- Automatic completion-note stubs generated from `git log`. Attractive, but a completion note whose
  deviations section is machine-written would be worthless; the value is in the human sentence.
- A real tokenizer for `--context-budget` if the P0 implementation ends up using a character-based
  approximation. Named so the approximation cannot quietly become permanent.
- Calibrating S/M/L against actuals across more than one phase. One phase of timings is a sample of
  nine; revisit at the P1 and P2 re-plans before changing D-22's definitions.

---

> **Note for the re-plan — a dependency conflict EP-8 must resolve.** The post-gate reconciliation
> moved reviewer recruitment to **P0**, because it is the longest-lead item in the plan
> and release-gate item 2 is unmeetable without it. D-64 then amended the *timing* — outreach waits
> until the P2 engine runs end-to-end — while stating that the recruitment **pack** still drafts in
> P0. The P0 table above contains no such brief; the recruitment pack is currently scheduled as
> **EP-37**, in P4, depending on EP-23. Either the pack is drafted in P0 (add a brief and renumber,
> or fold it into this re-plan) or that move is formally reversed with a dated addendum
> recording that the mode-(a) gate is schedule-exposed as a consequence. **Do not leave it
> implicit.** D-64 already records that the owner accepted the schedule exposure; what is missing is
> the artifact that says so in the roadmap.
