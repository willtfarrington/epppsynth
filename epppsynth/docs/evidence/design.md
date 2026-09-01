# Evidence — `status: design`

The evidence file the current README badge resolves to. It exists so the badge is a claim about
**artifacts that exist**, not about effort spent (D-12, D-59). Every box below names the artifact
that makes it true, so the claim can be checked without trusting the person who ticked it.

**Badge string:** `status: design`
**Claim:** design and planning artifact — roadmap and canonical docs exist; no engine exists.
**Ticked:** 2026-08-31, by the author, at EP-2.
**Re-checked:** 2026-09-01, by the author, at EP-8 — the P0 re-plan. Every box below was re-read
against the tree as P0 closes. **No box changed state.** One box's *evidence* changed and was
rewritten, because the package is no longer empty: see "No engine exists". The claim it supports —
that no engine exists — is unchanged and is what keeps the badge at `status: design`.
**Review:** author only. No external reviewer has read any artifact named here.

## Checklist

- [x] **A roadmap exists.** `roadmap/README.md` — eight phase tables, P0 … P7, with per-brief
      dependencies and a core/stretch cutline — plus 55 briefs `roadmap/EP-0-*.md` …
      `roadmap/EP-54-*.md` and `roadmap/final-roadmap.md`.
- [x] **Canonical documents exist.** `CLAUDE.md` (session rules and load order),
      `epppsynth/GOVERNANCE.md` (invariants, data boundary, release gates, excluded release
      classes), `epppsynth/DESIGN.md` (technical design, hazard register R-1 … R-41, traceability),
      `epppsynth/DECISIONS.md` (index block plus D-1 … D-79 with rationale and alternatives).
- [x] **Public front matter exists and states its own limits.** `README.md` carries the D-24
      expansion and status line, the not-a-risk-detector line, the badge scheme and its parse
      contract, the no-evidence statement, and an explicit "author review only" section.
- [x] **No engine exists.** `epppsynth/src/epppsynth/` holds `cli.py` and three packages, and
      every one of them checks the project rather than being it: `publicsafety/` (the nine
      leak-prevention scanners, EP-6), `rights/` (the per-source rights and licence checks, EP-5),
      and `storage/` (the two roots, the reserve floor and the project ceiling, EP-7). There is no
      concept registry, no composer, no traversal, no abstention chain, no renderer, and no UI —
      not one module on the engine side of `epppsynth/DESIGN.md` §17's module map exists as a file.
      The test suite tests **that tooling**, never engine behaviour, because there is no engine
      behaviour to test.
- [x] **No evaluation exists.** There is no `epppsynth/eval/` directory, no scenario set, no
      threshold table populated with observed numbers, and no evaluation report. The evaluation
      architecture is described in `epppsynth/DESIGN.md` §12 as planned work (EP-24 … EP-31).
- [x] **No release exists.** No Git tag of any kind; no `release-evidence/` directory; no published
      package, binary, demo, or hosted instance. `epppsynth/pyproject.toml` declares version
      `0.0.0`.
- [x] **No external review, validation, or audit exists.** No recruited reviewer, no IRB or QI
      determination, no accessibility audit, no security assessment, no regulatory review. The
      reviewer gate is described in `epppsynth/GOVERNANCE.md` §10 as future work (EP-37, EP-52).

## What would revoke this badge

Any of the above ceasing to be true without the badge moving. In particular: if an engine begins to
run end-to-end on fixtures, this file stops describing the project and
`epppsynth/docs/evidence/skeleton.md` must be written before the badge advances — never after.

## What would advance it

`status: skeleton`, and only that, once the deterministic engine and CLI run end-to-end on fixtures
(EP-17 … EP-21). Advancing straight to an evaluated rung is not available: the rungs are ordered and
each has its own evidence file.
