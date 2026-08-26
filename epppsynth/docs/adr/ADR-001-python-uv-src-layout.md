# ADR-001 — Python core, uv-managed, `src/` layout

**Status:** accepted ·
**Date:** 2026-08-26 ·
**Related:** D-21, D-40, D-42

## Context

EP-1 turns a verified-clean public tree (EP-0) into a project. Every later
brief with executable acceptance criteria needs a package to install, a test
runner to invoke, and a CI job to run them in. D-21 fixes the stack — a Python
core as a library with a CLI — and D-40 fixes the layout. The target machine
has Python 3.14, `uv` and `git`, and does **not** have `pandoc` or `cmake`;
nothing in the skeleton may assume either.

## Decision

The package lives at `epppsynth/` as a uv-managed project: `pyproject.toml`
with `hatchling` (pinned) as the build backend, a `src/` layout
(`src/epppsynth/`), a `tests/` root, a committed `uv.lock`, and a
`[project.scripts]` entry so `epppsynth` runs end to end from day one. The
runtime dependency list starts deliberately empty; `pytest` and `ruff` are the
only dev dependencies. Version is `0.0.0` and tracks the maturity badge
(EP-2 owns the badge). Two pytest markers, `requires_index` and
`requires_model`, are registered with `--strict-markers` so tests that need
local-only state are structurally excludable from CI.

## Consequences

- `uv sync --locked` is the single reproducible setup step on any clone; a
  resolution drift fails loudly instead of succeeding silently.
- The `src/` layout means tests import the installed package, not the working
  directory, so a packaging mistake fails in CI rather than at first use.
- The CLI entry point is the cheapest permanent end-to-end smoke test.
- An empty runtime dependency list makes the first real dependency a visible,
  reviewable event (R-29) rather than background noise.
- No type checker yet: that is a P2 decision at EP-17, where there are
  contract types worth checking.

## Alternatives considered

- **Flat (src-less) layout** — rejected: imports resolve against the checkout
  even when packaging is broken, hiding exactly the class of error a skeleton
  exists to surface.
- **pip + venv + requirements.txt** — rejected: no lockfile discipline by
  default, and D-21 already settles on uv.
- **setuptools as build backend** — rejected: hatchling is smaller, and its
  src-layout support needs no legacy configuration.
- **Poetry** — rejected: a second resolver and lockfile format alongside uv
  for no added capability.
