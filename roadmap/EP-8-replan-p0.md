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

---

> **Owner rulings of 2026-08-31 that land in this re-plan.** Registered in
> [`owner-decisions.md`](owner-decisions.md) from the completion notes of EP-1 … EP-4 and ruled by
> the project owner on **2026-08-31**. Each is an **input** to EP-8, not a decision EP-8 may
> re-open. Record each verdict and its date in the re-plan output.
>
> **OD-9 — no update automation for the pinned action SHAs.** Ruled option (a). Dependabot or
> renovate would mean a bot opening pull requests, which conflicts with **D-34**'s no-PR posture in
> v1; at this scale — **two** pinned third-party actions — the by-hand review `ADR-008` already
> promises is proportionate. No addendum under D-34 was written, because no carve-out was adopted;
> this note is the re-plan record under **D-42**. **The obligation is now EP-8's to discharge:**
> check both pins against their upstream releases, record the date and what was found, and hand the
> same obligation forward to the next phase re-plan. A review promised at every re-plan and
> performed at none is not a control, and the absence of a bot is what makes performing it
> load-bearing.
>
> **OD-11 — one hazard register, in `DESIGN.md` §14.** Confirmed as EP-2 executed it. EP-2's
> in-scope item 2 asked `GOVERNANCE.md` to tabulate R-1 … R-41; it was deliberately **not** moved,
> because `DESIGN.md` §14 already *is* that register and declares itself so, and GOVERNANCE §13
> already points at it and names the two highest-rated hazards. Restating 41 rows in a second file
> would create two registers that drift — the failure the single-register rule exists to prevent.
> What the item wanted was verified in place instead: all 41 rows present, contiguous, every row
> naming both a mitigating brief and a verifying gate. **The single-register rule is settled**: no
> later brief re-opens it, and `--hazards` reads `DESIGN.md` §14 alone. No decision entry was
> needed and none was written.
>
> **OD-1 — repository settings (D-76).** EP-4 observed `has_projects: true` against D-76's
> Projects **off**; the other three flags matched. Ruled option (a): **turn Projects off, matching
> D-76 as written** — nothing in the roadmap uses a project board — so no addendum under D-76 was
> written and none should be. The setting change is a platform action outside any brief. **EP-8
> re-observes all four flags** (`has_issues`, `has_discussions`, `has_wiki`, `has_projects`) plus
> `private-vulnerability-reporting`, records them with the date, and treats any remaining
> divergence as a finding — the badge scheme (D-59) exists to stop exactly this class of drift
> between a published decision and the platform it describes.
>
> **OD-8 — the issue form and the advisory intake.** Ruled: self-correcting, verify after the next
> push. At the time of the ruling the local branch was **six commits ahead of `origin`**, so
> `.github/ISSUE_TEMPLATE/discussion.yml` had not reached the platform and the issue-templates
> endpoint still returned 404 — which is why EP-4 had nothing to compare against. The platform
> reads issue forms *from* that directory, so pushing **is** configuring it. **EP-8 confirms, after
> the push:** that the form renders, and that its two required acknowledgement checkboxes behave as
> intended. Separately, `private-vulnerability-reporting` was verified `{"enabled": true}` through
> the API on 2026-08-31; its *form* has never been observed rendering, because an unauthenticated
> fetch returns the sign-in page. Record that split as it stands — the path is live, the form was
> not seen — rather than implying the form was checked.
>
> **OD-13 — the five owner-judgement acceptance criteria, ruled.** Offered by EP-1 … EP-4 and
> unruled until now. Verdicts, 2026-08-31:
>
> | Brief | # | Verdict | Basis |
> |---|---|---|---|
> | EP-1 | 10 | **pass** | `.github/workflows/ci.yml` is **36 lines** — one screen — and its first five lines state the no-model rule plainly, before `name:`, naming D-42 and pointing at ADR-008. |
> | EP-2 | 6 | **pass** | The four candidates the session offered are accepted as ruled: the two line-wrap artifacts where a `planned (EP-n)` marker fell to the next line, the not-a-risk-detector negative claim, and the badge parse contract. |
> | EP-2 | 10 | **fails as the files now stand — accepted as a known finding, not a pass** | `CLAUDE.md` ≈ 850 tokens; load-order items 1–4 ≈ **11.5k**, leaving ≈ 3.5k for a brief against the ~15k ceiling. **`--context-budget` will fail for at least EP-2 and EP-9.** EP-8 does not get to discover this: it is told. Build the check to fail honestly, record the per-brief table acceptance 5 already requires, and resolve the overflow by **shrinking item 3 or 4** — the `DECISIONS.md` index block and the phase table plus its standing-decisions paragraph — never by raising the ceiling and never by trimming a brief below the self-containment the whole load order exists to guarantee. |
> | EP-3 | 12 | **pass** | §3 (excluded uses), §6 (prohibitions and their enforcement), §11 (the stop criterion) and §16 (review status) are the four sections that answer it, and they answer it without leaving the file. |
> | EP-4 | 2 | **pass** | `PRIVACY.md` §11's 14 rows: 13 fill mechanism + brief + proof, and row 14's mechanism cell reads *"no mechanism — disclosed, not closed"*, which is the honest shape rather than a gap. A test already asserts that shape is the **only** permitted exception, which is what makes the verdict checkable rather than a reading. |
>
> **OD-2 — still open, and deliberately so.** `SAFETY.md` §4, *What it does not know*, was
> **authored** at EP-3 from D-8, D-14, D-18, D-25, D-63 and D-79, not copied from the approved
> draft: D-69 records four approved public blocks, three of which are byte-identical to EP-2's
> recorded baselines, while the fourth exists in no public artifact and its only remaining copy is
> private planning state a session may not open. It is the one block of approved public
> safety-facing wording whose shipped text has never been compared against what was approved. Only
> the owner can close it, by diffing §4 against the approved draft and then either confirming it or
> supplying the approved wording. **Until then EP-8 must not tick it**, and the ruling lands as a
> dated addendum under **D-69** recording that the block was authored at EP-3 and either matches or
> has been replaced.
>
> **Already landed, so EP-8 need not.** OD-3 (refined shared-passage invariant) → addendum under
> D-2, implemented by EP-6. OD-4 (per-mode panel invariance) → addendum under D-57; `GOVERNANCE.md`
> §4.5 was checked and needs **no** addendum, because it states the panel is *always visible* and
> makes no byte-identity claim. OD-5 (escalation copy settled as a decision) → addendum under D-18,
> which pins `SAFETY.md` §9 by commit, extraction rule and SHA-256 rather than restating the words;
> **the register expected this at EP-8 and it was ruled and landed early**, so EP-8 records it and
> moves on. OD-6 (the ingest spine, ruled **live**) → addendum under D-74, spine externalised to
> `tools/spine.local.json`, EP-6 and EP-22 updated. OD-7 (contact address) → ruled: keep the
> git-author address already public in this repository's commit metadata; no files changed. OD-10
> (modality-sweep exemptions) → confirmed as a **three**-entry table in EP-6, with one occurrence
> EP-2's exact-token grep could not match left for EP-6 to reword. OD-12 (banned-phrase carve-out)
> → confirmed in EP-39, where the entry count needing matcher support is **three**, not the two the
> register estimated.

---

> **Completion note (2026-09-01).** Executed. Ten checks, 45 unit tests over a fixture roadmap,
> seven deliberate red runs and seven reverts, and one green `--all`. Everything below records what
> was **observed**. Two acceptance criteria did not land as written and say so; one is an owner
> judgement this session cannot make, and one is CI, which cannot be green on a run that does not
> exist (OD-15).
>
> **The tool found real drift on its first run, in a place nobody had looked.** `--deps` reported
> **40 asymmetries** across every P3–P7 brief. They were not in the roadmap: they were in the
> checker. Reading the header block to the next `## ` heading swept a charter brief's
> `> **Charter.**` note — which names the re-plan EP that upgrades it — into that brief's `Blocks`
> field, inventing a dependency in all 31 charter briefs at once. Fixed by parsing the header as
> what it is: one contiguous block ending at the first blank line. The regression test
> (`test_a_charter_note_is_not_read_as_a_dependency`) names the bug, because a checker that is
> wrong in the same direction as the thing it checks is the failure mode worth a test.
>
> #### The size mix — old and new, side by side (acceptance 3)
>
> | | S | M | L | hours |
> |---|---|---|---|---|
> | Header before EP-8 | 2 | 17 | 36 | 90 |
> | Recomputed by `--table` from the eight phase tables | **2** | **17** | **36** | **90** |
>
> **They are identical.** The brief expected a correction and got a confirmation. It is recorded
> anyway, and the line in `roadmap/README.md` now says the figure is *derived, not maintained*:
> `--table` recomputes it from 55 table rows on every run and fails if the header disagrees, so
> nobody has to trust the last person who typed it.
>
> #### Seven deliberate red runs, seven reverts, one green (acceptance 2)
>
> Each was planted in the **real** roadmap, run, and reverted. Output is the finding line as printed.
>
> | # | Planted | Check | Finding, as printed |
> |---|---|---|---|
> | 1 | `roadmap/EP-99-probe.md`, ~96 KB of filler, plus a P0 table row | `--context-budget EP-99` | `over-budget  32,378 tokens against a 15,000 ceiling` |
> | 2 | EP-9 `Depends on` ← EP-16, EP-16 `Blocks` ← EP-9 | `--deps` | `cycle  EP-9 -> EP-16 -> EP-9` |
> | 3 | EP-2's box changed to `☑ 0dead00` | `--hashes` | `hash-unresolvable  \`0dead00\` is not a commit in this repository` |
> | 4 | EP-9's `## Safety preconditions` deleted | `--sections` | `missing-section  no \`## Safety preconditions\`` **and** `empty-safety-preconditions` |
> | 5 | EP-9's acceptance replaced with *"checked by hand and looks right"* | `--acceptance` | `no-command  acceptance names no fenced block and no command token`, and `--hazards` added `core-without-evidence` |
> | 6 | one `*(parked at EP-7)*` tag removed from `final-roadmap.md` | `--parked` | `parked-count-mismatch  5 parked item(s) in the brief, 4 entry(ies) tagged` |
> | 7 | a sentence spliced into EP-7's `## Context` | `--immutable` | `context-edited  \`## Context\` differs from the blob at 88faeef; annotate, never rewrite` |
>
> Then `--all`: ten checks, ten `passed`, `no findings.`
>
> **Deviation A — red run 6's revert deleted uncommitted work.** `git checkout -- roadmap/final-roadmap.md`
> reverted the file to `HEAD`, which threw away the whole extended parked section written minutes
> earlier, because it had not been committed. It was rebuilt and re-verified. Recorded because it is
> the obvious trap in "plant, run, revert" against a working tree that also holds the brief's own
> output, and the next re-plan will do the same seven red runs.
>
> #### The context budget, and the one thing this brief argued with itself about
>
> **Acceptance 5, the per-brief table.** All 55 briefs pass. P0 and P1, which acceptance 5 names:
>
> | brief | 1 | 2 | 3 | 4 | 5 | total | margin |
> |---|---|---|---|---|---|---|---|
> | EP-0 | 939 | 5,084 | 1,804 | 419 | 2,973 | 11,219 | 3,781 |
> | EP-1 | 939 | 5,084 | 1,804 | 419 | 3,544 | 11,790 | 3,210 |
> | EP-2 | 939 | 5,084 | 1,804 | 419 | 4,287 | 12,533 | 2,467 |
> | EP-3 | 939 | 5,084 | 1,804 | 419 | 4,365 | 12,611 | 2,389 |
> | EP-4 | 939 | 5,084 | 1,804 | 419 | 3,573 | 11,819 | 3,181 |
> | EP-5 | 939 | 5,084 | 1,804 | 419 | 4,013 | 12,259 | 2,741 |
> | EP-6 | 939 | 5,084 | 1,804 | 419 | 5,744 | 13,990 | 1,010 |
> | EP-7 | 939 | 5,084 | 1,804 | 419 | 4,440 | 12,686 | 2,314 |
> | EP-8 | 939 | 5,084 | 1,804 | 419 | 5,714 | 13,960 | 1,040 |
> | EP-9 | 939 | 5,084 | 1,804 | 503 | 6,016 | 14,346 | 654 |
> | EP-10 | 939 | 5,084 | 1,804 | 503 | 5,219 | 13,549 | 1,451 |
> | **EP-11** | 939 | 5,084 | 1,804 | 503 | 6,624 | **14,954** | **46** |
> | EP-12 | 939 | 5,084 | 1,804 | 503 | 4,665 | 12,995 | 2,005 |
> | EP-13 | 939 | 5,084 | 1,804 | 503 | 4,740 | 13,070 | 1,930 |
> | EP-14 | 939 | 5,084 | 1,804 | 503 | 5,057 | 13,387 | 1,613 |
> | EP-15 | 939 | 5,084 | 1,804 | 503 | 4,456 | 12,786 | 2,214 |
> | EP-16 | 939 | 5,084 | 1,804 | 503 | 4,530 | 12,860 | 2,140 |
>
> P2–P7 range from 9,112 (EP-54) to 12,163 (EP-22) and are not reproduced here; `--context-budget`
> prints all 55.
>
> **Deviation B — the overflow was real but smaller, and in a different brief, than OD-13 predicted.**
> The ruling estimated load-order items 1–4 at ≈ 11.5k tokens and said `--context-budget` would fail
> "for at least EP-2 and EP-9". Measured, items 1–4 came to **8.9k–9.0k**, and exactly one brief was
> ever over: **EP-11 at 15,577** against a 15,000 ceiling. EP-2 was at 13,156 and EP-9 at 14,963 —
> both under, EP-9 by 31 tokens. The ruling's *shape* was right and its arithmetic was not, and this
> note records both rather than quietly adopting the number that made the session look prescient.
>
> **The remedy was the one OD-13 directed: shrink load-order item 3.** The `DECISIONS.md` index
> block's `Decides` column went from an average of 84 characters to 55 — a signpost that tells a
> reader whether to open an entry, rather than a second summary competing with it. **No row was
> removed and no decision text was touched.** That recovered **623 tokens for every session**, and
> a dated note above the index block says what was done. The ceiling was not raised and no brief was
> trimmed.
>
> **What the session argued with itself about, recorded because the margin is thin.** After the
> compression EP-11 clears by **46 tokens** — a pass smaller than the error of the approximation
> that produced it. Compressing item 3 further was considered and rejected: below about 45 characters
> the gloss stops letting a session decide whether to open an entry, which spends *more* context in
> load-order item 6, not less — the check would improve while the session got worse. Compressing
> item 2 (`GOVERNANCE.md`, 5,084 tokens, 34 % of the ceiling on its own) was out of bounds by the
> same ruling. Splitting EP-11 renumbers the roadmap. So nothing further was done, and instead the
> tool now prints the tightest brief and its headroom on **every** run, and the whole question is
> registered as **OD-16** with the three candidate remedies and what each costs. The structural
> figure behind it: load-order items 1–3 cost **7,827 tokens, 52 % of the ceiling, before a brief is
> opened**, and item 3 grows with every new decision.
>
> **The tokenizer assumption is load-bearing and is printed, not buried.** No tokenizer is available
> offline, so the check divides characters by a stated **4.0**. Run it at `--chars-per-token 3.5` —
> plausible for markdown this dense — and **seven briefs go over**. That is why the constant is a
> command-line argument, why every run prints it, and why a real tokenizer is parked. Adding one line
> to `CLAUDE.md` would have cost about 30 tokens and put EP-11 over; **the session wanted to add one
> and did not.** That is what a 46-token margin means in practice.
>
> #### The re-plan's first decision — reviewer recruitment (the brief's own note)
>
> **Resolved as the reversal, formally, with a dated addendum under D-64.** P0 closed with no
> recruitment brief in it. The alternative — add a P0 brief and renumber 47 briefs — was rejected:
> D-64 already ruled that the pack drafts and outreach opens *together*, at P4, and renumbering the
> roadmap to satisfy a superseded sentence in D-64's own decision text would be bookkeeping wearing
> the costume of rigour. The pack is EP-37, upgraded by EP-31. **The cost is restated and not
> softened: the mode-(a) gate is schedule-exposed** — release-gate item 2 is unmeetable without
> recruited reviewers, EP-51 is the first brief that cannot proceed without them, and the role that
> `GOVERNANCE.md` §10 says cannot be silently dropped is the one most affected by starting late. The
> brief said *do not leave it implicit*; the addendum is the artifact that stops it being implicit.
>
> #### The owner rulings this brief was told to discharge
>
> All recorded in `roadmap/owner-decisions.md` under **P0 re-plan — EP-8, 2026-09-01**.
>
> - **OD-9 — the first by-hand pin review, performed.** `actions/checkout` is pinned to
>   `3d3c42e5…`, which is the `v7.0.1` tag object, and **v7.0.1 is current**. `astral-sh/setup-uv`
>   is pinned to `c771a70e…`, which is the `v9.0.0` tag object, and **v10.0.1 has been current since
>   2026-08-14** — one major version behind. Both pins were confirmed to be the commit the comment
>   names, so neither comment is decoration. **EP-8 did not bump it:** a major-version bump of a
>   pinned action is a CI posture change that `ADR-008` reserves for a by-hand review with a run
>   behind it, and doing it unasked inside a re-plan would be the automation OD-9 declined, wearing a
>   different hat. Registered as **OD-17**. The obligation is handed forward to EP-16 and to every
>   re-plan after it; landed as an addendum under **D-42**.
> - **OD-11 — one hazard register, confirmed.** `--hazards` reads `DESIGN.md` §14 alone and reports
>   **41 hazards, R-1 … R-41, contiguous**, each naming a mitigating brief that exists and a
>   verifying gate. It also checks the other direction: every `R-n` cited in any of the 55 briefs
>   resolves to a row. Zero unmitigated hazards, zero unresolved citations. No second register was
>   created.
> - **OD-1 — re-observed, and still divergent.** All four D-76 flags plus the private-reporting path
>   were read from the API on 2026-09-01: `has_issues true`, `has_discussions false`,
>   `has_wiki false`, `private-vulnerability-reporting {"enabled": true}` — and
>   **`has_projects` is still `true`**, against D-76's *off* and against the ruling of 2026-08-31.
>   The ruling is right and the click has not happened. The row stays `◐` and is handed forward,
>   because a divergence re-observed and re-recorded without being fixed is how a published decision
>   quietly becomes false.
> - **OD-8 — pushed, and still not observed. This is the honest split the brief asked for.** The
>   commits reached the remote: `origin/main` is at `638a0fe`, the default branch is `main`, and
>   `.github/ISSUE_TEMPLATE/discussion.yml` is in that tree — the form is published at the path the
>   platform reads issue forms from. It still could not be seen rendering. The REST route
>   `repos/{owner}/{repo}/issues/templates` returns 404 with a `documentation_url` pointing at
>   *get-an-issue*, i.e. a route that does not exist — which is very likely what EP-4 actually hit.
>   GraphQL's `repository.issueTemplates` returns an **empty list**, and that field is not known to
>   surface YAML issue *forms*, so the empty list is not evidence either way. An unauthenticated
>   fetch of `/issues/new/choose` returns the sign-in interstitial, exactly as the
>   private-vulnerability-reporting form does. **Recorded as: the file is published where the
>   platform reads it, and the rendered form has not been seen.** The two required acknowledgement
>   checkboxes have not been exercised. Closing it needs one signed-in human look.
> - **OD-13 — the five verdicts recorded**, and the one failure resolved as directed (above).
> - **OD-2 — deliberately not ticked.** `SAFETY.md` §4 was authored at EP-3 from the decisions, and
>   the approved draft's only remaining copy is private planning state a session may not open (D-2).
>   EP-8 was told not to tick it and did not.
>
> #### The template, ratified — amended, not confirmed unchanged (acceptance, in-scope 3)
>
> The six sections were confirmed unchanged; **five rules were added**, each one a convention that
> nine executions showed nobody had written down: the header is one contiguous block (the bug above);
> `Depends on`/`Blocks` are exact mirrors; the completion note goes at the very end of the file; a
> completion note records what was observed and may not claim CI without naming the run (OD-15); and
> an executed brief is never rewritten. The **charter variant** was added too — five sections, its
> note, and the acceptance exemption — because 31 of 55 briefs use a form the template did not
> describe. `--sections` was re-run across all 55: green.
>
> **Deviation C — `--sections` had to tolerate a shape the template forbids.** EP-3 and EP-4 both
> carry their `## Parked →` section **below** their completion note rather than above it. Executed
> briefs are append-only (`CLAUDE.md`), so neither can be tidied, and a checker that demanded
> otherwise would be demanding a rule violation. The check therefore compares the *canonical*
> headings' relative order, counting each at its first occurrence — which also handles EP-2, whose
> completion note restates a heading. The template now says where the note goes, so no later brief
> repeats it.
>
> **Deviation D — `--acceptance` exempts charter briefs, and the exemption is priced.** The brief
> asks that every brief's acceptance name a command. Twenty-five of the 31 charter briefs name none,
> their own notes say *"do not execute from the sketch alone"* and promise that each criterion
> becomes a named command or artifact at upgrade, and EP-8's out-of-scope forbids upgrading them. So
> a charter is exempt from naming a command and is instead **required to name the re-plan EP that
> will make it name one**; the exemptions are counted and listed on every run. A charter nobody ever
> upgrades is what the count is for. `--hazards` does not double-count them.
>
> #### P1 and P2, consistency-checked (in-scope 6 and 7)
>
> Mechanically: all 16 briefs pass `--sections`, `--acceptance`, `--deps`, `--table` and
> `--context-budget`. Beyond the tool: **every `D-n` cited in all 55 briefs resolves** to a row in
> the index (D-1 … D-79, zero unresolved), and every `R-n` resolves to the register.
>
> - **Definition of Ready, all eight P1 briefs: ready. None is marked blocked.** The one candidate
>   for blocking was the context budget, which EP-11 now passes. The other candidate was EP-5's
>   parked item — *"resolving SAMHSA and AHRQ reuse terms, carried as an explicit P1 blocker for
>   public intended-use language"* — and it is **not** an unowned blocker: **EP-10 already owns that
>   check** (its in-scope item 7), and explicitly allows the outcome *"still unverified"*, with the
>   conservative `reference-only-pending-rights-check` class and a matrix that forbids the wording
>   those sources would license. Confirmed, not changed.
> - **Sizes were not adjusted, and the retro says why** — `roadmap/P0-retro.md`. The only actuals
>   available are commit timestamps, which record when a session ended and never when it began; they
>   bound the four briefs that ran back-to-back in one sitting and say nothing about the other five.
>   Every bounded brief came in well under its size, and the retro **declines to read that as "the
>   sizes are too generous"**, because every one of those bounds is a warm start inside a run of
>   briefs — which is not the cold "one supervised session" D-22 describes.
> - **P2 confirmed, with one live divergence flagged.** EP-22's pandoc handling already matches what
>   P0 observed: pure-Python default, `--converter pandoc` opt-in behind a `shutil.which` probe,
>   never invoked implicitly — and its EP-7 dependency (the storage guards) now exists. The
>   divergence is between **EP-11 and EP-19**: EP-19 §5 describes `clause_weight` as *authored per
>   activation clause*, while EP-11 keys it by `(input field, predicate kind)` in the composer's
>   frozen table and forbids it on a concept, because EP-9's deny-list rejects any ordinal or score
>   field on a concept. EP-11 asks for this to be raised on EP-19; EP-11 has not run, so the re-plan
>   raised it, as an `> **EP-8 pickup note.**` appended to EP-19. **Nothing in EP-19 was changed** —
>   reconciling is EP-11's work, and EP-11 precedes EP-19 through EP-17 and EP-18, so the spec will
>   exist before EP-19 is picked up.
>
> #### The mandatory rewrite, and what the human packet item caught (in-scope 8, 10)
>
> **`README.md` was wrong, and no scanner could have caught it.** It said the repository holds *"an
> empty package skeleton"*. True when EP-2 wrote it; false for two briefs by the time EP-8 read it —
> EP-5, EP-6 and EP-7 landed the rights checks, nine leak scanners with a CI job, and the storage
> roots with their guards. Corrected: the paragraph now names what is there (a CLI and three
> packages, every one of which *checks* the project rather than being it) and says plainly that none
> of the tool runs. `epppsynth/README.md` carried the same claim and was corrected with it.
> `epppsynth/docs/evidence/design.md`'s *"No engine exists"* box carried the same stale evidence
> (`__init__.py` and `cli.py` only): **the box did not change state**, its evidence was rewritten,
> and the file records the re-check with its date. **The badge did not move and could not** — P0
> produced no engine — and `--status` now asserts the badge, the README status paragraph, the
> evidence file and `CITATION.cff` agree, which is the four-way check the safety-preconditions table
> asked for.
>
> This was found by **packet item 7, the human one**. The nine scanners were green throughout; the
> badge check confirmed the badge resolves to a fully ticked evidence file, and it did. What drifted
> was a sentence about the tree, and reading sentences about the tree is exactly what item 7 is for.
> The full packet is `epppsynth/docs/pre-publication/2026-09-01-P0-close.md`, signed against this
> brief's first commit, with two second opinions recorded: **`gitleaks` 8.30.1** (31 commits and the
> working tree, *no leaks found* both times) and **`reuse lint`** (*compliant with REUSE 3.3*,
> 137/137 files). Item 5 is recorded as **no input** — zero image files are tracked — never as
> "screenshots passed".
>
> #### Acceptance, as run
>
> | # | Criterion | Result |
> |---|---|---|
> | 1 | `--all` exits 0 against the real roadmap | ☑ ten checks, `no findings.` |
> | 2 | seven red runs, seven reverts, one green | ☑ table above; deviation A recorded |
> | 3 | `--table` recomputes the mix; header matches; old and new side by side | ☑ identical, `2 S · 17 M · 36 L ≈ 90 h` |
> | 4 | `--hazards` reports R-1 … R-41, each with a brief and a gate; zero unmitigated; zero core briefs without acceptance | ☑ 41 hazards; charter briefs held to naming their upgrader instead (deviation D) |
> | 5 | `--context-budget` passes for every P0 and P1 brief, recorded as a table | ☑ table above — and the margin is thin; deviation B and OD-16 |
> | 6 | `final-roadmap.md` keeps every prior entry, plus every parked item and every residual | ☑ **38** mirrored entries tagged one-for-one — 34 from EP-0 … EP-7 plus this brief's 4 — 7 residuals present, nothing removed |
> | 7 | all eight P1 briefs full, passing, and Ready — or marked blocked | ☑ all eight Ready; none blocked |
> | 8 | README status paragraph and badge true; `--status` confirms the agreement | ☑ after the correction above |
> | 9 | packet executed, dated, signed against the P0-closing commit; items 5 and 7 human | ☑ filed at `epppsynth/docs/pre-publication/2026-09-01-P0-close.md` |
> | 10 | retro records estimate against actual for all nine, and P1's sizes are adjusted **or the retro says no adjustment was warranted** | ☑ `roadmap/P0-retro.md`; **no adjustment**, with the reason |
> | 11 | CI green, including the new step | **◐ not yet.** Nothing is pushed, so no run exists. Every command CI runs is green locally: `ruff check`, `ruff format --check`, **236 passed**, `epppsynth scan --history` exit 0, `roadmap_check --all` exit 0. Per OD-15 this note does **not** claim CI, and the row stays `◐` until a run id exists |
> | 12 | *(judgement — the owner)* one P1 brief is executable by a cold session from the load order alone | **offered, unruled.** This session cannot judge it: it has read the whole tree, which is the one condition the criterion excludes |
>
> #### Deviations, collected
>
> **A** — a red-run revert deleted uncommitted work (above). **B** — the predicted overflow was
> smaller and in a different brief (above). **C** — `--sections` tolerates EP-3's and EP-4's parked
> section sitting below the completion note (above). **D** — `--acceptance` exempts charter briefs
> and prices the exemption (above). **E** — the packet lands in the *second* commit, not the first,
> because a packet cannot carry the hash of the commit that contains it; the second commit therefore
> touches two files rather than one. **F** — `../tools/roadmap_check.py` was added to the CI lint
> steps **by name** rather than widening ruff to `tools/`: `epub_to_md_pipeline.py` predates the
> toolchain, was imported as-is at EP-0, and has 12 pre-existing lint errors that are not this
> brief's to fix. **G** — three new owner decisions were opened (**OD-16** the load order's headroom,
> **OD-17** the `setup-uv` pin, **OD-18** the GiB/GB transcription); each records what EP-8 did *not*
> do, and why. **H** — this brief's row is set to `◐` in the **first** commit rather than left `☐`
> until the second. `--hashes` fails a brief that carries a completion note above an unticked box,
> and rightly so: it hides finished work. Setting the row to `◐` — *done, not landed*, the state
> EP-6 earned — makes the first commit true and green, and the second adds the hash. The row stays
> `◐` after that, because acceptance 11 names CI and no run exists yet (OD-15). Push both commits
> together. **I** — the pre-commit hook **blocked the first commit twice**. EP-6's `phi` scanner
> found an address-shaped string in the new test file, where the fixture repository configured a
> git identity in the obvious `name-at-example-dot-invalid` form; the fixture now configures an
> identity that is not address-shaped, which git accepts happily. It then blocked the commit a
> second time on **this very deviation**, because the first draft of it quoted the offending string.
> The scanner is right both times, and the rule it enforces is the one EP-0 set for prose: do not
> write the shape you are describing. Recorded because it is EP-6's defense in depth firing twice,
> unprompted, on EP-8's own new files — and because the second firing is the more interesting one.
>
> #### What P0 leaves for P1
>
> Six owner decisions unresolved and **no P1 brief blocked by any of them**: OD-1 (a click), OD-2
> (only the owner can compare), OD-8 (one signed-in look), OD-16, OD-17 and OD-18. The by-hand pin
> review is now EP-16's obligation. Nothing is pushed; the third commit, `docs(roadmap): record EP-8
> CI run`, follows the push (OD-15).
