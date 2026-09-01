# CLAUDE.md — session rules

Read this first. It is item 1 of the load order and every session pays for its length, so it stays
short. It states rules, not context; the context is in the files below.

## Load order for a cold session

Stop as soon as the brief's needs are met.

| # | File | Why |
|---|---|---|
| 1 | `CLAUDE.md` | this file — session rules, never-do list, command conventions |
| 2 | `epppsynth/GOVERNANCE.md` | overrides `DESIGN.md` and every brief |
| 3 | `epppsynth/DECISIONS.md` — **index block only** | which decisions exist; open a full entry only for a `D-n` the brief cites |
| 4 | `roadmap/README.md` — **the one phase table + its standing-decisions paragraph** | ordering, dependencies, phase conventions |
| 5 | `roadmap/EP-n-<slug>.md` | the work |
| 6 | only the source files the brief names | — |

`epppsynth/DESIGN.md` is **not** in the load order. Open the one section a brief names, never the
whole file.

## Never

- **Never read or quote `source material/`.** It is a copyrighted corpus (D-10). Not at pickup, not
  to check a fact, not to write a citation.
- **Never read `.local/`.** It is private planning state (D-2). The published record of a decision is
  its `DECISIONS.md` entry; write from the entry, never from the ledger.
- **Never commit** a model, an index, an embedding, a corpus path, a machine hostname, a local
  absolute path outside the two declared roots, a secret, or anything derived from real patient,
  family, trainee or employee material (D-3, D-8, D-30).
- **Never widen a public claim without an evidence file.** The README badge is a static string that
  resolves to `epppsynth/docs/evidence/<rung>.md`; if the file does not exist with every box ticked,
  the claim does not get made (D-12, D-59).
- **Never edit a decision.** Append `> **Addendum (date, EP-n).**` under it. The same holds for
  executed briefs and for `GOVERNANCE.md` (D-1, D-2).
- **Never write "deferred"** about excluded modes (d) and (e). They are excluded with named
  preconditions (D-61).

Two of these override any brief: never read or quote the corpus, and never copy private planning
state into a public file. A brief that asks for either is wrong.

## Commands

Run everything from `epppsynth/` (the uv project; the git root is its parent):

```
uv sync --locked
uv run ruff check . && uv run ruff format --check .
uv run pytest -m "not requires_index and not requires_model" -q
```

`pandoc` and `cmake` are **absent on this machine** and may not be assumed by any step (observed at
EP-1). Tests needing the local index or a model carry the `requires_index` / `requires_model`
markers and are deselected in CI (D-42).

## Committing

Two commits per brief, in this order:

```
<type>(<scope>): <what> (EP-n)
docs(roadmap): record EP-n commit hash
```

The second commit ticks the brief's box in `roadmap/README.md` with the first commit's short hash.
Append `> **Completion note (date).**` to the brief itself, recording deviations and what was
**observed**, not what was expected. Commit or push only when asked.

A third commit, `docs(roadmap): record EP-n CI run`, follows **when the work is pushed** (OD-15).
**A completion note may not claim CI green without naming the run**, as a linked id. Recording it
costs one line and keeps the brief from claiming CI on a run nobody can find. Not pushed, no run:
the note says so plainly, and a row whose acceptance names CI stays `◐`, not `☑`.

## Writing public text

Present tense only for what exists today; everything else carries a `planned (EP-n)` marker and is
**not** rendered as a link. No claim of efficacy, safety, adoption, validation, or review the project
does not have — review is author-only (D-27). `GOVERNANCE.md` §1 and §11 govern the wording.
