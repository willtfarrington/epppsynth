# ADR-007 — Cache purge safety rules

**Status:** accepted — no implementation exists ·
**Date:** 2026-09-01 ·
**Related:** D-30, D-49, D-71, D-78, R-21

## Context

A pre-existing third-party model cache of roughly 92 GB sits on this machine.
D-71 keeps it: deleting another application's assets is outside this project's
remit, and the cache is excluded from the project's budget entirely.

So this ADR answers a question nobody is asking yet, on purpose. If the owner
ever does need that space back, the work will be wanted quickly, and a deletion
tool written quickly is the most dangerous thing this repository could contain.
R-21 is that risk: a cache purge escaping the model root. The seven rules below
cost nothing to write now and remove the improvisation that would otherwise
happen later.

**This ADR is a specification for work that does not exist.** EP-7 built no
purge tool, no deletion path and no Recycle-Bin helper. The
`epppsynth.storage` package is asserted to contain none: `test_storage.py`
parses every module in it and fails on a call to `os.remove`, `os.unlink`,
`Path.unlink`, `Path.rmdir`, `shutil.rmtree`, `shutil.move` or a Recycle-Bin
helper. That test is the evidence for this Status line.

## Decision

If a cache-purge tool is ever built, it satisfies **all seven** rules before it
deletes anything. It is a `final-roadmap.md` item, it is not started as part of
another brief, and satisfying these rules is its first acceptance criterion —
not a review comment on it afterwards.

1. **One configured cache root.** Absolute, and read from configuration. Not
   from `argv`, and not from an environment variable read at the point of use —
   an environment variable is a value another process can change between the
   check and the deletion.

2. **Prove descendancy.** Fully resolve both the root and the target, following
   symlinks and junctions, and then require **all three**:
   `target.is_relative_to(root)`, `target != root`, and
   `len(target.parts) >= 4`. The last is a blast-radius floor: a path three
   components deep is far more likely to be a mistake than a cache entry.

3. **Reject the dangerous locations, as root *or* as target.** Drive roots, the
   user profile root, the Windows directory, `Program Files`, and any repository
   working tree — the last detected by walking up for a `.git` directory. A tool
   that can be pointed at a working tree will eventually be pointed at one.

4. **Reject unresolved variables and globs.** Any residual `%…%`, `$env:`, `~`,
   or `* ? [ ]` in a path is a hard error rather than something to expand.
   **No globbing at all**: deletion consumes an explicit file list produced by
   the inventory step. A glob is a promise about what matched at the moment it
   was written, and deletion happens later.

5. **Refuse reparse-point traversal.** If any directory in the walk carries
   `FILE_ATTRIBUTE_REPARSE_POINT`, stop and demand explicit per-path approval.
   Following a junction is how a purge confined to a cache reaches a data drive.
   EP-7's read-only inventory already walks this way — it records the flag and
   does not descend — so the walk a purge tool needs already exists and is
   already tested.

6. **Inventory → dry-run → confirm.** Emit a plan file naming, per entry, the
   path, the byte count, the reason it is in the plan, and its hash; print the
   totals; and require the operator to confirm **that plan's hash**, not merely
   to answer yes. Plans expire after **15 minutes**, because a confirmation
   given against a filesystem that has since changed is not a confirmation.

7. **Preserve the reserve, and prefer recoverable deletion.** Log free space
   before and after. Refuse to run at all if pre-purge free space is already
   below the D-49 floor **and** the plan does not remedy it — a purge that
   leaves the machine still below the floor has taken the risk without buying
   the benefit. Send to the Recycle Bin rather than unlinking, and **never**
   recursively force-remove a directory.

## Consequences

- The rules are cheap now and expensive to reconstruct later, which is the whole
  argument for writing them before they are needed.
- Rules 2, 5 and 7 are already partly satisfied by code EP-7 wrote for other
  reasons: the reparse-point-aware walk and the before-and-after free-space
  guards. A future purge tool inherits them rather than reimplementing them.
- Rule 6 makes a purge a two-step operation with a durable artifact between the
  steps. That is deliberate friction, and any future brief that proposes
  removing it is proposing to remove the control, not the friction.
- The Status line is load-bearing. It stays `accepted — no implementation
  exists` until a `final-roadmap.md` item is executed and this ADR is amended
  with a dated addendum naming that brief. A future session that finds deletion
  code in this repository while this line still reads as it does has found a
  defect.
- **Nothing here licenses touching the pre-existing cache.** D-71 keeps it, and
  these rules govern a hypothetical tool, not an intention.

## Alternatives considered

- **Write nothing until a purge tool is actually wanted** — rejected: the moment
  it is wanted is the moment there is pressure to skip the safety work, and the
  rules cost an hour now.
- **Build the purge tool now, since the rules are written** — rejected by D-71
  and by EP-7's scope. Deleting another application's assets is not this
  project's remit, and a deletion path in the repository is a standing hazard
  whether or not anybody runs it.
- **Rely on the Recycle Bin alone as the safety net** — rejected: it does not
  catch a file too large for the bin, it does not exist on every volume, and it
  is a recovery mechanism rather than a control.
- **A confirmation prompt rather than a plan hash** — rejected: a prompt
  confirms intent, and rule 6 needs to confirm *the specific set of files*.
