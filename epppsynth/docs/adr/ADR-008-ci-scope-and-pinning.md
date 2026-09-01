# ADR-008 — CI scope and action pinning

**Status:** accepted ·
**Date:** 2026-08-26 ·
**Related:** D-3, D-16, D-42, D-51

## Context

CI logs are public artifacts (D-3), and CI is the enforcement point for the
data boundary: no job may ever touch a model, an index, or the corpus (D-16,
D-42, D-51). Third-party actions are the first supply-chain exposure the
repository takes on (R-29). D-42 settles the posture; this ADR records it
where a reviewer of the workflow file will find it.

## Decision

One workflow, `.github/workflows/ci.yml`, is the **no-model path** and the
only CI in the repository:

- Triggers: `push` and `pull_request` only — never `pull_request_target`.
- `permissions: contents: read` at workflow top level; no job elevates it. No
  secrets are referenced anywhere; the no-model path needs none.
- One job on `windows-latest` (the target platform, D-42), running
  `uv sync --locked`, `ruff check`, `ruff format --check`, and
  `pytest -m "not requires_index and not requires_model"`.
- `actions/checkout` sets `persist-credentials: false`.
- No `run:` block interpolates `github.event.*` (script-injection surface),
  and no step prints paths outside the checkout, environment dumps, or cache
  paths.
- Every third-party action is pinned to a full 40-character commit SHA with
  the version as a trailing comment, so a pin is distinguishable from a guess.

## Recorded pins

| Action | Commit SHA | Version |
|---|---|---|
| `actions/checkout` | `3d3c42e5aac5ba805825da76410c181273ba90b1` | v7.0.1 |
| `astral-sh/setup-uv` | `c771a70e6277c0a99b617c7a806ffedaca235ff9` | v9.0.0 |

SHAs were resolved from the projects' own tag refs (`git ls-remote`) on
2026-08-26; both tags are lightweight, so the tag SHA is the commit SHA.
**The pins are reviewed at each phase re-plan** (EP-8, EP-16, EP-23, EP-31,
EP-37, EP-46, EP-49). Automated pin-bumping (Dependabot/Renovate) is parked:
anything that opens a PR conflicts with the no-PR posture (D-34).

## Consequences

- A drifted lockfile or a moved tag fails loudly; nothing resolves silently.
- EP-6 adds the leak scanners into this frame; EP-1's workflow is the frame,
  not the checks.
- The workflow needs no secret, so a fork or a public log can never leak one
  from it.

## Alternatives considered

- **Tag-pinned actions (`@v7`)** — rejected: a tag is mutable and R-29 is
  about exactly that mutation.
- **Linux runners** — rejected: the target machine is Windows and D-42 wants
  CI to prove the path that ships.
- **A model-in-CI eval job** — rejected outright by D-16/D-51: models,
  indexes and the corpus never enter CI.

---

## Amendment (2026-08-31, EP-6) — the leak-prevention job and its three allowlists

**Status:** accepted · **Related:** D-2, D-4, D-10, D-42, D-59, D-74, owner rulings OD-3, OD-6, OD-10

EP-6 adds a second job, `scan`, to the same workflow and under the same posture: `windows-latest`,
top-level `permissions: contents: read`, no secret referenced, both actions pinned to the SHAs
recorded above, `persist-credentials: false`. It runs `uv run epppsynth scan --history`, the same CLI
entry point `.githooks/pre-commit` invokes, so the hook and CI cannot drift; a unit test compares the
two command lines.

`fetch-depth: 0` appears in **exactly one job** — this one — and carries a comment saying why. The
secret sweep reads `git log -p --all`, because an unreachable object is not a deleted one and this
repository's history was erased and re-created once. A deep fetch anywhere else in this repository is
a smell.

Check 9 (private-ledger passages) has no `.local/` to read on a runner. It prints
`skipped - no ledger present` and is counted as **skipped, never as passed**. A skip counted as a
pass is how that check would quietly stop working.

### The three allowlists, counted separately

None of the three may be used to reach another's scope.

| # | Allowlist | Size | Grows by |
|---|---|---|---|
| 1 | The canary directory — `epppsynth/tests/canaries`, by **exact path**, never by pattern | exactly 1 entry | an amendment to this ADR |
| 2 | The retired-modality exemption table (check 8), three files each carrying its reason | exactly 3 entries | a further **owner ruling** — not an ADR amendment, not a session's judgement |
| 3 | The rule-definition **line marker**, in a comment on the line it exempts | unbounded, but line-scoped and fully inventoried on every run | a line that matches a rule it defines |

Allowlist 1 is one hard-coded directory with a test guarding its length, and that length test is the
property that makes it safe; a configurable `allowlist.toml` is parked in `final-roadmap.md` for
exactly that reason. Allowlist 2 is an owner ruling recorded in code, and a second unit test fails if
a fourth row appears. Allowlist 3 is never a block, a file, a directory or a pattern, is never
inherited by the next line, and a marker that suppresses nothing is itself reported as a defect — an
exemption for a line that does not need one is a hole waiting for a future edit.

### Accounted-for matches, which are not allowlists

Three narrow, mechanical exceptions sit inside individual rules rather than in any allowlist, and
every one of them is printed in the scan summary: an all-digit abbreviated git object id that
`git rev-parse` resolves in this repository; a `size =` value in the machine-generated resolver
lockfile; and the one email address this repository already publishes in its own commit metadata
(owner ruling OD-7). Each is derived from data or from git rather than from a path list, and each
fails closed — a digit run git cannot resolve is still a finding.

A fourth, `bibliographic-identity`, is a rule refinement raised by EP-6 and **registered for
ratification as OD-14** in `roadmap/owner-decisions.md`: an occurrence of the retired modality stem
inside a `source_id` or a citation `title` declared in `epppsynth/registry/sources.yaml` is
bibliographic identity, which D-74 requires this project to be able to cite, and not this project
describing itself. It is derived from the rights record rather than from a path list, and it is why
check 8 runs green without a fourth exemption row.

### Consequences

- Two jobs now run per push. Neither references a secret, a model root, an index root or the corpus.
- The `scan` job's log prints paths, line numbers and rule names, and **never a matched string**.
- Dependency vulnerability scanning is still parked (EP-41), and `gitleaks` / `trufflehog` remain
  uninstalled; the checklist records a second opinion when one happens to be available.

### Ratification (2026-09-01, owner ruling OD-14)

`bibliographic-identity` is **ratified as implemented**. It is an accounted-for match, not a fourth
allowlist, and its scope is exactly as recorded above: a skip applies only where the retired modality
stem falls inside a string `epppsynth/registry/sources.yaml` declares as a `source_id` or a citation
`title` — never a file, a directory, a pattern or a line. The OD-10 exemption table is untouched and
still has three entries. `roadmap/owner-decisions.md`, *Resolutions — 2026-09-01*, carries the
ruling and the reasoning; a change to the scope needs a further owner ruling, not an ADR amendment.

### Amendment (2026-09-01, EP-6) — shallow clones and the `git-object-id` exception

The `test` job checks out at the default depth and **keeps doing so**: it needs no history, and a deep
fetch it has no use for is the smell this ADR warns about. One consequence has to be named rather
than discovered. The `git-object-id` exception asks git whether an all-digit run is a real object
here; in a shallow clone git cannot answer for anything older than the fetched depth, so the run is
reported as a finding. The rule fails closed, which is right, and the `phi` check's note now says
`SHALLOW CLONE` and why, so an unexplained PHI finding is never left unexplained.

The two unit tests that scan the whole repository and assert it is green are skipped on a shallow
clone, with that reason. The property is not lost: the `scan` job runs the identical scan with
`fetch-depth: 0` and fails the build. `fetch-depth: 0` still appears in exactly one job.

### Amendment (2026-09-01, EP-7) — a fourth allowlist: the two root constants, by symbol

**Status:** accepted · **Related:** D-30, D-49, D-51, D-71, D-78, ADR-009

EP-7 gives the project a storage package, and a storage package has to know where its roots are. The
`roots` check exists so that the two root paths appear in documentation and nowhere else; that rule
is right, and it needs exactly one hole, cut deliberately and shaped as narrowly as the rule allows.

| # | Allowlist | Size | Grows by |
|---|---|---|---|
| 4 | The **root constants** — `MODEL_ROOT` and `INDEX_ROOT`, by **symbol**, on their assignment lines, in `epppsynth/src/epppsynth/storage/limits.py` by **exact path** | exactly 2 symbols in 1 module | an amendment to this ADR |

**By symbol, not by file.** The exemption applies to a line that begins an assignment to one of the
two named symbols. A root path anywhere else in that same module — a default argument, a docstring
example, a comment, a second assignment — is still a finding, and a unit test asserts exactly that
by planting one. A file-scoped exemption would have been one line shorter and would have turned the
one module that must name the roots into the one module where naming them is free.

It is an **allowlist** and is counted as the fourth, not an accounted-for match: it derives from a
path list, and the three exceptions this ADR records as accounted-for matches derive from data or
from git. Calling it an accounted-for match would have understated it.

The construction the exemption exists to prevent is the alternative that was rejected: building the
root path at run time from `%SystemDrive%` plus a name fragment. That passes the scanner without an
exemption, which is exactly what is wrong with it — the scanner would then be blind to any future
module that did the same thing, and the visible hole would have been traded for an invisible one.

The self-check grows with it. `scan_allowlist` now also asserts that the allowlisted module is
tracked and that each of the two symbols is assigned **exactly once**; an allowlist that has drifted
from the file it exempts is an off switch. In a tree that does not contain the storage package at
all — a throwaway fixture repository — the allowlist is out of scope and nothing is reported.

`MODALITY_EXEMPTION_COUNT` is untouched and the OD-10 table still has three entries. None of the four
allowlists may be used to reach another's scope, and a unit test asserts the four do not overlap.
