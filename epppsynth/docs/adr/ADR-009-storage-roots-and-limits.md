# ADR-009 — Storage roots and limits

**Status:** accepted ·
**Date:** 2026-09-01 ·
**Related:** D-3, D-16, D-30, D-31, D-44, D-49, D-51, D-71, D-78

## Context

Nothing in this project may download a model, build an index or write a
benchmark packet until something refuses to do so when the machine cannot
afford it. Three questions had to be answered before any of that work starts,
and answering them late would mean answering them under pressure from a
download already in progress:

1. **Where does project data live?** Weights and a derived index are large, are
   never committed (D-30), and are of two different rights classes.
2. **How much of the machine may the project take?** The machine is the
   operator's, and it is used for things that are not this project.
3. **How much may the project take of itself?** A budget that exists only as an
   intention is not a budget.

A pre-existing third-party model cache of roughly 92 GB already sits on this
machine. It belongs to other applications, it is kept (D-71), and it is part of
neither answer.

## Decision

### Two roots, deliberately separate

| Root | Holds | Why it is its own root |
|---|---|---|
| `C:\epppmodels` | `models.lock.json`, weights under `models/<publisher>/<repo>/<revision>/`, embedding models under `embeddings/` in the identical shape (D-44), `benchmarks/`, `inventory/` | D-30. Freely licensed third-party weights, individually confirmed one at a time, never in Git or LFS |
| `C:\epppindex` | the D-16 local index | D-51. A **different rights class** — derived from a copyrighted corpus the author lawfully holds — independently purgeable and independently excludable from backup |

Merging them would put copyright-derived content and freely licensed weights
under one retention policy, and the first time either had to be handled
separately the merge would have to be undone under whatever pressure prompted
it. Both roots sit **outside the repository working tree**, so neither can reach
a published artifact by being committed (R-19).

`<revision>` is a 40-hex commit SHA and never a branch name, so the path itself
records what was verified.

The two paths are deliberately public: they appear in this ADR, in
`DECISIONS.md`, in `PRIVACY.md` and in the roadmap. In **code** they appear
exactly once, as `MODEL_ROOT` and `INDEX_ROOT` in
`epppsynth/src/epppsynth/storage/limits.py`, which the EP-6 `roots` scanner
allowlists **by symbol** — see the ADR-008 amendment of the same date. Any other
occurrence in any tracked non-documentation file is a scan finding.

### The floor is the machine's

**At least 250 GiB free on the system volume at all times** (D-49), checked
immediately **before and after every write**.

- The check runs on both sides because a single large download can cross the
  line mid-operation, and a pre-write check alone would never see it.
- The post-write check cannot un-write the bytes. It is an error condition that
  **latches**: it halts the *next* write, which is the only thing still within
  reach. Nothing clears the latch automatically.
- The floor is **not a project allocation**. The project never claims the
  headroom above it — free space above 250 GiB belongs to the operator's other
  work, not to this project's budget.

### The ceiling is the project's

The combined footprint of the two roots is **warned at 20 GB and hard-stopped at
25 GB** (D-78). The warning fires on every call above the level, not once.
Expected real usage is one generation model of 5 GB or less, one small embedding
model, an index of roughly 1–2 GB and JSON packets: **about 8–12 GB**. A
footprint far outside that range is a surprise, and the recorded expectation is
what makes it legible as one.

Raising either the floor or the ceiling requires a **written owner decision
recorded as a dated addendum in `DECISIONS.md`**. The constants carry that
sentence in their own comments, because the failure mode being guarded against
is a session editing a number to make a download fit.

### The units differ on purpose

The floor is **binary** — 250 GiB, `250 × 1024³`. The ceiling is **decimal** —
25 GB, `25 × 1000³`. That is exactly how D-49 and D-78 state them, and neither
is normalised to the other. Transcribing a decision faithfully matters more than
internal tidiness, and a reader who finds the mismatch should be able to
establish in one place that it is deliberate rather than a bug. A unit test
asserts both forms, including that the floor is *not* the decimal reading.
**Flagged for the P0 re-plan (EP-8)** as a candidate for a single explicit
decision on units, which would be an owner decision and not a code change.

### The pre-existing third-party cache is outside both figures

D-71. It is inventoried read-only, its file count and total size are recorded,
and it is never counted against the floor or the ceiling and never touched. The
seven rules a purge tool would have to satisfy are written in `ADR-007`; no
purge tool exists.

## Observations recorded at EP-7 (2026-09-01)

**Cloud-sync scope (WS2-A5).** Checked before anything was written into either
root. Two sync scopes exist on this machine: one provider mounts a **separate
drive letter**, and one provider's folder sits **under the user profile**. No
known-folder redirection is configured, and no mirrored-folder entry covers the
system volume's root. **Neither root falls under any sync scope**, and both sit
directly under the system volume's root rather than under the user profile. A
copyright-derived index syncing off-machine would be a rights incident rather
than an inconvenience, so this is re-checked at any re-plan that moves a root.
Configuring a backup exclusion for the index root is an owner machine action and
is parked in `final-roadmap.md`; the separate root exists to make it a one-line
action when it is wanted.

**Third-party cache, before and after the first inventory run.** Unchanged: the
same file count, the same total size, and every file's modification time
identical. Counts and totals only are recorded, here and in EP-7's completion
note — no paths, no filenames, no hardware identifiers (D-3).

## Consequences

- Every write in `epppsynth.storage` goes through one guarded write path, so
  "checked before and after every write" is a property of the code rather than a
  claim about it. New write paths are the thing to look for in review.
- The inventory writes its output **only** to `C:\epppmodels\inventory\<UTC>.json`,
  outside the repository. That file is the single most likely source of a local
  path or a machine identifier in this project (pre-publication checklist item
  4), and it is never committed.
- CI never touches either root and never runs `epppsynth storage` (D-42). The
  test suite exercises the limits on a temporary tree with the free-space and
  directory-size calls injected, so proving a 25 GB ceiling needs no 25 GB.
- The ceiling is measured, not estimated: it walks both roots on every check,
  which costs a directory walk per call and is the price of a limit that cannot
  drift from the disk.
- EP-22 (index), EP-32 (packet schema), EP-34 (model choice) and EP-35 (first
  measured run) all inherit these roots and both guards, and none of them
  restates the numbers.

## Alternatives considered

- **One root for both weights and the index** — rejected by D-51: one retention
  policy over two rights classes, and the backup-exclusion case would force the
  split later anyway.
- **The index inside the repository working tree**, gitignored — rejected: an
  ignore rule is defense in depth, not proof, and R-19 is exactly the case where
  it fails.
- **A single storage number** instead of a floor and a ceiling — rejected by
  D-78: it conflates protecting the machine with budgeting the project, and
  whichever meaning was written down, the other would be silently lost.
- **A percentage-of-disk floor** — rejected: it moves when the disk does, and
  the guarantee the operator wants is an absolute amount of room.
- **A pre-write check only** — rejected by D-49: it cannot see a write that
  crosses the line while it is running.
- **Normalising GiB and GB to one unit** — rejected: it would silently restate
  two owner decisions, and both were stated in the units their reasoning used.
- **Adopting the pre-existing 92 GB cache as the model root** — rejected by
  D-71: it would make the project's footprint depend on a directory the project
  does not own and cannot govern.
