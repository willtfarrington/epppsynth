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
