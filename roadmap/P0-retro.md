# P0 retro — EP-0 … EP-8

Written at the P0 re-plan (**EP-8, 2026-09-01**) from the nine executed briefs and from `git log`.
D-22 says S, M and L are calibrated against actuals; this is the first phase that has any, and the
first thing the retro found is that they are worse actuals than the decision assumes.

## What "actual elapsed" can and cannot mean here

**The only timing instrument this project has is the commit timestamp, and it records when a session
ended.** Nothing records when one began. So the elapsed column below is a *bound*, not a
measurement, and it exists only where two briefs ran back-to-back in one sitting: the gap from the
previous brief's `docs(roadmap): record …` commit to this brief's `feat`/`docs` commit is an upper
bound on this brief's session, and it is an upper bound that also contains every pause the operator
took.

Four of the nine can be bounded that way. The other five are separated by gaps of hours or days —
EP-0 is the first commit of its day, EP-1 lands three days after the commit before it, EP-2 five days
after that — and for those the honest entry is **not measurable**, not an estimate dressed as one.

## Per brief

| # | Size | Elapsed (bound, and how) | Deviations | What was harder than expected |
|---|---|---|---|---|
| EP-0 | S | **not measurable** — first commit of 2026-08-23 | 4 | The history assertion. Scoping the sweep to `git ls-files` turned out to under-cover, and one deviation left acceptance 8 partially unmet as an owner decision rather than a defect. An S that had to reason about a re-created history. |
| EP-1 | M | **not measurable** — 3 days after the previous commit | 2 | Landing CI without leaking. `setup-uv`'s cache wrote uv cache paths into a public log, caught after the first commit and fixed in a second — which is why EP-1 is a two-hash row. |
| EP-2 | L | **not measurable** — 5 days after the previous commit | 6 | The brief's own `## Context` was stale on arrival, and the decision count was 79, not the 78 the brief carried. The largest single lesson of the phase: a brief describes the tree as it was when the brief was written. |
| EP-3 | L | **≤ 16 min** — `285d060` 14:52 → `7a5ecbb` 15:08 | 7 | Deviation 1. The approved four-block public text turned out to exist in **no public file**, so §4 was authored from the decisions instead of copied. That opened **OD-2**, which is still open and which only the owner can close. |
| EP-4 | M | **≤ 33 min** — `47e8cd0` 15:11 → `083137d` 15:44 | 7 | Seven deviations against an **M** — the worst deviation-to-size ratio in the phase. Three of them were platform observations a session simply cannot make: the issue form, the advisory intake, and Projects being on. |
| EP-5 | L | **≤ 90 min** — `7e32734` 15:44 → `b3424b2` 17:14, and the window also holds `41f755e`, the owner-rulings session | 11 | REUSE refuses a `path` that matches no file, so two boundary paths could not be declared before their directories exist. And `NOTICE` could not say "nothing is vendored", because `CODE_OF_CONDUCT.md` *is* the Contributor Covenant, reproduced under a licence whose one condition is attribution. |
| EP-6 | L | **≤ 37 min** first sitting — `76a472c` 17:14 → `c0edef5` 17:51; **plus ≈ 48 min** the next day, 12:37 → 13:25 | 12 | The most deviations in the phase, and the only brief that needed a second sitting. **The first pushed run caught a defect no local run could reach**: the history sweep's git-object-id exception cannot resolve in a shallow clone. The row was held at `◐` for a day rather than ticked on evidence that did not exist. |
| EP-7 | L | **≤ 27 min** — `bebf766` 13:25 → `88faeef` 13:52 | 6 | Every deviation was architectural rather than incidental. The read-only claim had to become **structural** — `inventory` returns a report and never holds a write path — because "this module does not write" is a property a test should be able to prove, not a discipline. |
| EP-8 | L | this brief | see its completion note | The context budget. The overflow OD-13 predicted was real but smaller and in a different place than the ruling estimated, and closing it consumed the phase's only genuinely contested judgement. |

## What the numbers say, and what they do not

- **Total deviations across eight executed briefs: 55.** Not one brief executed exactly as written.
  That is the phase's headline finding, and it is a finding about *briefs*, not about sessions: a
  brief written before the tree existed cannot describe the tree accurately.
- **Deviations rise with the size of the surface, not with the size of the brief.** EP-4 is an `M`
  with seven; EP-1 is an `M` with two. The difference is that EP-4 touches a platform nobody in the
  session can observe. Size predicts effort; *surface* predicts surprise.
- **Every bounded brief came in under its size.** EP-3, EP-6 and EP-7 are `L` (≈ 2 h) and none of
  their bounds exceeds 48 minutes; EP-4 is an `M` (≈ 1 h) at ≤ 33 minutes. It is tempting to read
  that as "the sizes are too generous". **The retro declines to.** Every one of those bounds is an
  upper bound on a session that was already warm, sitting inside a run of briefs, with the previous
  brief's context still loaded — which is precisely the condition D-22's "one supervised session"
  does *not* describe. The five unbounded briefs, each a cold start, are the ones that would tell us
  whether an `L` is two hours, and they are the five with no data.

## Calibration decision

**S, M and L are not redefined.** Recorded as a dated addendum under D-22 on 2026-09-01, with the
reason above. D-22 asks for calibration against actuals; four warm upper bounds are not actuals, and
changing a sizing convention on them would make the roadmap's estimates *less* trustworthy while
looking like rigour.

**P1's sizes are therefore unchanged from what the tables already carried**, and
`tools/roadmap_check.py --table` now asserts that the header's mix agrees with them: recomputed at
P0's close it reads **2 S · 17 M · 36 L ≈ 90 h**, identical to the figure the header already had.

Revisit at the P1 and P2 re-plans, when there are enough cold-start briefs to say something. Parked
in [`final-roadmap.md`](final-roadmap.md) so the revisit has an owner.

## What P0 changed about how a brief is written

Four things, all now enforced by `tools/roadmap_check.py` rather than remembered:

1. **A brief's `## Context` goes stale and must never be rewritten.** EP-2 found its own context
   stale; `--immutable` now compares every executed brief's `## Context` against the blob at the
   commit its done box records, and staleness is annotated below the brief instead.
2. **A done box is a claim about a commit.** `--hashes` resolves every one of them, and requires a
   completion note where there is a tick and no completion note where there is not.
3. **A completion note may not claim CI green without naming the run** (owner ruling OD-15, from
   EP-7). EP-6 earned the `◐` state — done, not landed — and it recurs.
4. **A parked item must reach `final-roadmap.md` or the check fails.** Thirty-four items from the
   eight executed briefs are mirrored, counted one for one by `--parked`.
