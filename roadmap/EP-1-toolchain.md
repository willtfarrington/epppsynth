# EP-1 — Toolchain, package skeleton, ADR framework, CI

**Size:** M · **Mode:** n/a · **Core/Stretch:** core ·
**Depends on:** EP-0 (baseline & public-safety hygiene) · **Blocks:** EP-2 (canonical docs), EP-6 (leak-prevention CI), EP-7 (storage inventory), EP-8 (roadmap tooling, re-plan P0), EP-17 (contracts package), EP-38 (threat model)

## Context

EP-0 proved the tree is clean. EP-1 makes it a project: the first brief in the plan that runs a
command rather than reading one, and therefore the prerequisite for every brief whose acceptance
criteria are executable. Nothing downstream can name a test, a linter or a CI job until this
skeleton exists.

**What exists.** A public repository with a verified baseline, `.gitignore`, `.gitattributes`, a
placeholder `epppsynth/README.md`, and `tools/epub_to_md_pipeline.py`. No packaging metadata, no
virtual environment, no lockfile, no tests, no CI.

**What this brief creates.** The `uv`-managed Python project at `epppsynth/` (D-21, D-40) with a
`src/` layout, a committed lockfile, pytest wired to a passing empty suite, the ADR directory and
template, and one GitHub Actions workflow on `windows-latest` that runs the deterministic, no-model
test path only (D-42).

**Toolchain facts for the target machine.** Python 3.14, `uv` and `git` are present and verified.
**`pandoc` and `cmake` are absent** and must not be assumed by anything this brief creates;
in particular, no step here may depend on `tools/epub_to_md_pipeline.py` running, because that
script requires pandoc. Nothing in this brief compiles native code, so the absence of `cmake` is
recorded rather than worked around; it becomes load-bearing only at the P4 inference spike, where a
source build of the runtime would be the fallback that the absent native toolchain rules out.

Implements: D-21 (Python core, uv-managed, deterministic core as a library, CLI present), D-40
(repository layout and canonical doc locations), D-42 (CI on `windows-latest`, minimum token
permissions, third-party actions pinned to commit SHAs, no-model path only). Mitigates R-29
(supply-chain compromise) at the moment the first dependency enters the tree.

## Safety preconditions

| Invariant at risk | Guard in this brief |
|---|---|
| CI logs are public artifacts (D-3) | The workflow prints no path outside the checkout, no environment dump, and no `uv` cache path. The `run:` blocks contain **no** `${{ github.event.* }}` interpolation (script injection), and the job sets `persist-credentials: false` on checkout. |
| Supply chain (R-29) | Every third-party action is pinned to a full 40-character commit SHA with the version as a trailing comment. `uv.lock` is committed and CI installs with `uv sync --locked` so a resolution drift fails rather than silently succeeds. No pre-release and no VCS dependency is permitted in `pyproject.toml`. |
| A CI job must never touch a model, an index, or the corpus (D-16, D-42, D-51) | The workflow declares `epppsynth/tests/` as the only test root and the job body names no path under `C:\epppmodels`, `C:\epppindex` or `source material/`. A test that needs any of them is `skip`-marked by a marker registered here (`requires_index`, `requires_model`) and CI runs with `-m "not requires_index and not requires_model"`. |
| Minimum privilege on the workflow token | `permissions: contents: read` at workflow top level; no job elevates it. No secrets are referenced at all, because the no-model path needs none (WS-3 §3.5). |
| Excluding secrets and local state from the venv path | `.gitignore` already excludes `.venv/`; step 2 re-probes it with `git check-ignore -v` before the first `uv sync`. |

Pre-publication checklist items exercised here: **1 (secrets)**, **4 (local paths — the workflow
file is a tracked file and is swept like any other)**.

## In scope

1. **Confirm the toolchain, do not install one.** Record `python --version`, `uv --version`,
   `git --version`. Record explicitly that `pandoc` and `cmake` are **absent** (`Get-Command pandoc`
   and `Get-Command cmake` both fail) and that nothing in this brief depends on either. Paste the
   version strings — not the install paths — into the completion note.
2. **Re-probe the venv exclusion:** `git check-ignore -v epppsynth/.venv/probe` must match.
3. **Create the uv project at `epppsynth/`.** `pyproject.toml` with `[project]` name `epppsynth`,
   `version = "0.0.0"` (it tracks the maturity badge, which is `status: design` — EP-2 owns the
   badge itself), `requires-python = ">=3.14"`, a deliberately empty runtime dependency list, and a
   `[project.scripts]` entry `epppsynth = "epppsynth.cli:main"`. Build backend: `hatchling`, pinned.
4. **`src/` layout** per D-40: `epppsynth/src/epppsynth/__init__.py` exporting `__version__`, and
   `epppsynth/src/epppsynth/cli.py` with a `main()` that prints the version and the
   `(contract, registry, template)` version triple placeholders and exits 0. The CLI exists from
   day one because D-21 requires it and because a CLI entry point is the cheapest end-to-end smoke
   test the project will ever have.
5. **Test root.** `epppsynth/tests/test_smoke.py` asserting the package imports, `__version__` is a
   string, and `main()` exits 0. Register the two skip markers (`requires_index`, `requires_model`)
   in `[tool.pytest.ini_options]` with `--strict-markers`.
6. **Dev dependency group** (`[dependency-groups] dev`): `pytest`, `ruff`. No formatter beyond
   `ruff format`, no type checker in P0 — a type checker is a P2 decision once the contracts package
   exists. Configure `ruff` in `pyproject.toml` (line length 100, `E,F,I,UP,B` rule set).
7. **Lock and sync:** `uv lock` then `uv sync --locked`. Commit `uv.lock`.
8. **ADR framework.** `epppsynth/docs/adr/` with `_TEMPLATE.md` (Status · Context · Decision ·
   Consequences · Alternatives considered · Date · Related `D-n`), and stubs for the four ADRs the
   plan already knows it needs:
   - `ADR-001-python-uv-src-layout.md` — written now, in full, since this brief is its subject.
   - `ADR-007-cache-purge-safety-rules.md` — stub; **EP-7** writes the seven rules.
   - `ADR-008-ci-scope-and-pinning.md` — written now, recording the D-42 posture.
   - `ADR-009-storage-roots-and-limits.md` — stub; **EP-7** writes the floor and ceiling.
   A stub is a title, `Status: proposed`, and one line naming the EP that will fill it. An empty
   file is not acceptable — a cold session must be able to tell a stub from an omission.
9. **CI workflow** at `.github/workflows/ci.yml`:
   - triggers `push` and `pull_request` (never `pull_request_target`);
   - `permissions: contents: read` at top level;
   - one job, `runs-on: windows-latest`;
   - `actions/checkout` and `astral-sh/setup-uv` pinned to full commit SHAs with `# vX.Y.Z`
     trailing comments, `persist-credentials: false` on checkout;
   - steps: `uv sync --locked`, `uv run ruff check .`, `uv run ruff format --check .`,
     `uv run pytest -m "not requires_index and not requires_model" -q`;
   - `concurrency` group keyed on the ref, cancelling in-progress runs;
   - a comment block at the top of the file stating that this workflow is the **no-model path** and
     that no job in this repository may reference a secret, a model root, or the corpus.
10. **Record the action SHAs and their versions** in `ADR-008` so a later reviewer can tell a pin
    from a guess, and add a note that the pins are reviewed at each phase re-plan.
11. **Commits:** `feat(epppsynth): add uv project skeleton, ADR framework and CI (EP-1)` then
    `docs(roadmap): record EP-1 commit hash`.

## Out of scope

- Any engine, registry, contract or schema code — **EP-17** (contracts), **EP-18** (registry
  loader), **EP-9** (registry schema).
- Licence headers, `REUSE.toml`, `LICENSES/` — **EP-5**. `pyproject.toml` gets no `license` field
  beyond the SPDX identifier `Apache-2.0`, and EP-5 reconciles it with the REUSE layout.
- Leak scanners, PHI patterns, badge-to-evidence checks and the pre-publication packet — **EP-6**.
  EP-1's workflow is the frame those checks are added to, not the checks themselves.
- The storage preflight, cache inventory and `models.lock.json` verifier — **EP-7**.
- `tools/roadmap_check.py` and `--context-budget` — **EP-8**.
- Any dependency on `pandoc`; the corpus-ingest module and its pandoc-or-pure-Python decision —
  **EP-22** (pandoc is absent and may not be assumed).
- `llama-cpp-python`, CUDA wheels, or anything that would make CI need a GPU — **EP-33** onward.
- Type checking and coverage thresholds — parked, see below.

## Verification / acceptance

Runnable, from `epppsynth/`:

```powershell
uv sync --locked
uv run ruff check .
uv run ruff format --check .
uv run pytest -m "not requires_index and not requires_model" -q
uv run epppsynth --version
```

And from the repository root:

```powershell
git ls-files "epppsynth/uv.lock"
Select-String -Path ".github/workflows/ci.yml" -Pattern 'uses:\s+\S+@[0-9a-f]{40}'
Select-String -Path ".github/workflows/ci.yml" -Pattern 'github\.event\.'   # → no output
Select-String -Path ".github/workflows/ci.yml" -Pattern 'secrets\.'          # → no output
Get-ChildItem epppsynth/docs/adr -Filter "ADR-*.md" | Measure-Object          # → 4
```

Acceptance:

1. `uv sync --locked` succeeds on a cold `.venv` and does **not** modify `uv.lock`
   (`git status --porcelain` empty afterwards). This is the reproducibility claim; if the lock
   moves, the claim is false.
2. `uv run pytest` is green and reports at least the three smoke assertions; `--strict-markers` is
   active, proven by a deliberately misspelled marker failing collection (run once, then revert —
   record it in the completion note).
3. `uv run epppsynth --version` prints the version and exits 0.
4. Every `uses:` line in `ci.yml` matches a 40-hex-character SHA. Zero occurrences of
   `github.event.` and of `secrets.` anywhere in the workflow.
5. The workflow declares `permissions: contents: read` at the top level and no job overrides it.
6. Four ADR files exist; `ADR-001` and `ADR-008` are complete; `ADR-007` and `ADR-009` are stubs
   that name **EP-7** as their author.
7. One green CI run on `windows-latest`; its run URL is recorded in the completion note.
8. The completion note records that `pandoc` and `cmake` were confirmed **absent** and that nothing
   in this brief depends on either.
9. *(judgement — the project owner)* The workflow file is readable end to end in one screen and its
   header comment states the no-model rule plainly.

## Parked → final-roadmap.md

- A type checker (`mypy` / `pyright`) and a coverage floor. Both are cheap to add and expensive to
  add badly; they belong with the contracts package (EP-17), where there are types worth checking.
- Scheduled `pip-audit` / OSV scanning of the lockfile (WS-3 §3.5). It belongs to the supply-chain
  hardening pass at EP-41 rather than to a P0 skeleton, but it must not be lost.
- A CycloneDX SBOM job. Per-release, not per-push — **EP-50** owns it; recorded here so the CI
  frame is known to be incomplete by design.
- Dependabot / renovate configuration for the pinned action SHAs. Any automation that opens a PR
  conflicts with D-34's no-PR posture in v1 and needs an owner decision first.
