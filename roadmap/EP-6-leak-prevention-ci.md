# EP-6 — Leak-prevention CI + pre-publication packet

**Size:** L · **Mode:** n/a · **Core/Stretch:** core ·
**Depends on:** EP-1 (toolchain), EP-2 (canonical docs), EP-5 (licensing pack) ·
**Blocks:** EP-8 (roadmap tooling, re-plan P0)

## Context

Every brief before this one has run its safety checks by hand, once, and pasted the output into a
completion note. That does not scale past P0 and it does not survive a tired session. EP-6 converts
those checks into enforcement: scanners that run in CI on `windows-latest` and in an identical
pre-commit hook, plus the seven-item pre-publication review packet as a runnable script.

It depends on **EP-5** and not merely on EP-1, for the reason the P0 ordering rationale gives: the
leak scanners enforce the rights table's rules. `check_no_verbatim_from_nonredistributable`,
`check_source_refs` and `count_quotations` are already written and unit-tested in EP-5; EP-6 wires
them into the workflow. Writing them here would mean inventing rights logic inside a CI brief.

It also depends on **EP-2** transitively (through EP-5) for the badge parse contract: EP-2 fixed the
regex and the badge → evidence-file mapping, and EP-6 implements the checker that resolves it.

**What exists.** One CI workflow that lints and tests. Tested rights-check functions. A defined
badge parse contract with `epppsynth/docs/evidence/design.md` as the current target. `.gitignore`
covering `source material/**` and `.local/`. A verified-clean history from EP-0 — verified **once**,
by hand.

**What this brief creates.** `epppsynth/src/epppsynth/publicsafety/` with the scanners as importable,
tested functions; a `scan` CLI subcommand; a second CI job wiring all of them; an identical
pre-commit hook; `epppsynth/docs/pre-publication-checklist.md` as a runnable checklist; and
`epppsynth/tests/canaries/` — the planted-canary fixtures the acceptance criteria require.

**Acceptance shape.** Because the deliverable *is* a set of CI checks, acceptance is a **deliberate
red run on a planted canary plus a green run on a clean tree** — for every check. A scanner that has
never failed has never been shown to work.

Implements: D-3 (public-safe by default), D-10 (corpus never redistributed), D-42 (CI posture),
D-51 (index root outside the tree, never in CI), D-59 (badge resolves to an evidence file or CI
fails), D-74 (quotation budget enforced in CI). Mitigates R-6 (public-history leakage), R-7
(rights leakage), R-19 (index reaching a published artifact via fixture, screenshot or error
message), R-9 (badge tied to effort), R-29 (supply chain — the scanners cover the workflow files
themselves).

## Safety preconditions

| Invariant at risk | Guard in this brief |
|---|---|
| Scanners mistaken for proof (GOVERNANCE §Public-safety) | `epppsynth/docs/pre-publication-checklist.md` opens with the defense-in-depth statement verbatim and states that items 5 (screenshots) and 7 (public claims) are **human** steps that no script replaces. The packet records a date, a commit hash and a human name; a green CI run is not a substitute and the document says so. |
| The canaries themselves leaking (a scanner test that plants a real-looking secret) | The seven **red runs** are executed locally and their canaries never enter a commit (item 8). The committed unit-test fixtures live under `epppsynth/tests/canaries/` and contain **synthetic, structurally-valid-but-inert** strings: a token-shaped string with a documented non-existent prefix, an MRN-shaped digit run, a fake `C:` + `\Users\<placeholder>\` path with a literal placeholder segment. Every canary file carries a header line stating it is a deliberate test fixture. The scanners are configured to **exempt exactly that directory** by explicit path, never by pattern — a pattern-based exemption is how a real leak later hides. |
| An exemption becoming a hole | The canary exemption is a single allowlisted directory constant with a unit test asserting the allowlist has exactly one entry. Any addition fails that test and forces a deliberate decision. |
| The index or model roots appearing in CI (D-16, D-51) | The workflow references neither root. A scanner asserts that no tracked file contains `C:` + `\epppindex` **as a data path in code or fixtures** — the two roots may appear in *documentation* (they are deliberately public) but never in a fixture, a test, or a default configuration value. The check is scoped by file type accordingly, and the rule is written down in the checklist so the distinction survives. |
| A badge upgraded without evidence (D-59, R-9) | The badge checker parses the README string against EP-2's regex, resolves it to the mapped evidence file, and fails if that file is absent **or** if it contains an unticked checkbox. Proven by a deliberate red run: temporarily set the badge to `status: skeleton`, watch CI fail, revert. |
| A pre-commit hook that drifts from CI | The hook and the CI job invoke the **same** CLI entry point with the same arguments. A unit test asserts the hook script's command line and the workflow step's command line are equal strings. |

Pre-publication checklist items exercised here: **all seven** — this brief is where they become the
packet.

## In scope

1. **`epppsynth/src/epppsynth/publicsafety/scan.py`** — the scanners, each an importable function
   returning findings, each with unit tests:
   1. **Secrets** — token-shaped strings and credential assignments, over the **full history**
      (`git log -p --all`) as well as the tree.
   2. **PHI patterns** — MRN-shaped digit runs, date-of-birth patterns, NPI, SSN, phone, email,
      street-address fragments — across tracked files **and** fixtures. Plus the D-36 rule: every
      scenario fixture must carry a "no real person" attestation. (No scenarios exist yet; the
      check runs over an empty set and becomes live at EP-25.)
   3. **Protected text** — no path under `source material/` tracked in any commit (the EP-0 history
      assertion, now automated); a length-threshold check for quoted spans in docs and fixtures;
      and the D-74 quotation budget via EP-5's `count_quotations`.
   4. **Local paths, username, hostname** — `C:` + `\Users\`, `C:` + `/Users/`, the operator's account name
      and machine hostname read from the environment at run time, UNC `\\` prefixes, and drive
      letters other than the two approved public roots — across code, docs, briefs, fixtures and
      workflow files.
   5. **Index/model roots in the wrong place** — `C:` + `\epppindex` and `C:` + `\epppmodels` permitted in
      documentation, forbidden in code, tests, fixtures and default configuration values.
   6. **Licence conformance** — EP-5's coverage check, `check_source_refs`, and
      `check_no_verbatim_from_nonredistributable`.
   7. **Badge → evidence** — parse the README badge, resolve the mapped evidence file, fail if
      absent or if any checkbox in it is unticked.
2. **Rule-definition allowlist — a named deliverable of this brief, not a footnote.** The
   scanners read briefs, docs, code, fixtures and workflow files, so every file that *defines* a
   rule contains that rule's own pattern; with no allowlist, `epppsynth scan` fails on
   `EP-0-baseline.md`, on this brief, on `scan.py` and on the checklist during its first clean run,
   and the "zero hits" acceptance below is unmeetable. Two mechanisms, both required:
   1. **The line marker.** A line is skipped **only** if it carries the literal
      `leak-scan-allow: rule-definition` on that same line — an HTML comment in markdown, a
      trailing `#` comment in code, YAML and workflow files. The exemption is line-scoped: never a
      block, never a file, never a directory, never a pattern, and never inherited by the next
      line.
   2. **Split literals in prose.** A rule literal written in a brief or in documentation is split
      across a `+` (`C:` + `\Users\`) so the prose does not match the rule it describes and
      needs no marker at all. EP-0 sets this convention; this brief keeps it and the checklist
      states it.
   `epppsynth scan` prints the count and the path/line of every line it skipped in its summary, so
   an exemption is never silent, and unit tests assert that the marker exempts only the line it
   appears on and that a marker on a non-rule line is reported as a defect. This allowlist is
   **separate from** the canary-directory allowlist and is counted separately; neither may be used
   to reach the other's scope.
3. **CLI subcommand** `epppsynth scan [--history] [--fix-hints]` returning a non-zero exit code and
   a machine-readable summary (one finding per line: check id, path, line, matched rule). No
   finding text is printed with enough context to reproduce a secret.
4. **CI job.** Add a second job to `.github/workflows/ci.yml` (or a sibling workflow, same posture):
   `runs-on: windows-latest`, `permissions: contents: read`, actions pinned to full commit SHAs,
   `persist-credentials: false`, `fetch-depth: 0` **only** for the job that needs full history — and
   a comment saying why, because a deep fetch is otherwise a smell. Steps: `uv sync --locked`, then
   `uv run epppsynth scan --history`.
5. **Pre-commit hook.** `.githooks/pre-commit` invoking the identical command (without `--history`,
   for speed, with a comment stating that the history scan is CI's job), plus a documented
   `git config core.hooksPath .githooks` step and a note that hooks are advisory: they run on the
   operator's machine and can be bypassed, which is exactly why CI runs the same check.
6. **`epppsynth/docs/pre-publication-checklist.md`** — the seven items, each with: what is checked,
   the command that checks it, what the script **cannot** check, and a signature block (date,
   commit hash, human name). Items 5 (screenshots re-opened and read, EXIF stripped, no source
   pane, no local paths in a title bar, no notification toasts) and 7 (README, badge, `prime` card
   and `CITATION.cff` all say the same thing and none says more than the evidence supports) are
   marked **human** and have no script.
7. **Canary fixtures** under `epppsynth/tests/canaries/` — one per scanner, seven in total, each
   with a header line declaring itself a deliberate fixture, each inert.
8. **Run the deliberate red runs — locally.** **No red-run canary is pushed.** A public
   repository's history is permanent and an unreachable object is not a deleted one; proving a
   scanner works is not a reason to write a token-shaped or patient-shaped string into that
   history. (This is distinct from item 7's committed fixtures, which are inert by construction,
   header-declared, and confined to one allowlisted directory — the red runs plant *un*-exempted
   copies outside it, and those must never leave the working tree.) For each of the seven checks: plant the canary in the **working tree
   only**, run the *same* command CI runs (`uv run epppsynth scan --history`), record the exact
   failing check id and the command's output, remove the canary, and confirm a clean local run.
   All seven go in the completion note as a table of local runs.
   Then, **once**, prove the CI wiring itself fires: push a single **innocuous** canary — the
   badge set to `status: skeleton` with its evidence file absent, which carries no secret, no PHI,
   no local path and no protected text — on a scratch branch; record the failing CI run URL and
   check id; revert; confirm green. The seven local runs prove the rules; the one pushed run proves
   the workflow is wired to them. State that split explicitly in the completion note, so a later
   reader does not read "one CI red run" as thin evidence.
9. **Record the exemption rule** in `ADR-008` (CI scope and pinning): the canary directory is
   allowlisted by exact path, the allowlist has exactly one entry, and adding an entry requires an
   ADR amendment.
10. **Commits:** `feat(epppsynth): add leak-prevention scanners, CI job and pre-publication packet (EP-6)`
   then `docs(roadmap): record EP-6 commit hash`.

## Out of scope

- Writing the rights rules themselves — **EP-5**. EP-6 imports and wires them.
- Defining the badge vocabulary and the parse contract — **EP-2**. EP-6 implements the checker.
- `gitleaks` / `trufflehog` as an installed dependency — parked at EP-0 and still parked; the
  scanners here run with no third-party binary. If one is present on the operator's machine, the
  checklist says to run it as a second opinion and record which tool produced the result.
- The runtime source-pane exclusion (spans must never reach a screenshot, CI or a template) —
  **EP-45** (provenance drawer) and **EP-46**. EP-6 scans the tree; it does not constrain the
  running app.
- Scenario attestation content — **EP-25**, **EP-26**, **EP-27**. EP-6 ships the check; the
  scenarios that satisfy it come later.
- The release-evidence manifest and the tag-time CI enforcement — **EP-50**.
- Dependency vulnerability scanning (`pip-audit` / OSV) — **EP-41** hardening pass.
- Accessibility, banned-phrase and copy-deck linting — **EP-39**.

## Verification / acceptance

Runnable, from the repository root:

```powershell
uv run epppsynth scan                    # → exit 0 on a clean tree
uv run epppsynth scan --history          # → exit 0, includes the full-history secret sweep
uv run pytest epppsynth/tests/test_publicsafety.py -q
git config core.hooksPath                # → .githooks
```

The acceptance criterion for this brief is **seven deliberate local red runs, one pushed
innocuous CI red run, and one clean green run**, recorded as a table in the completion note with
one row per check. Only row 7 is pushed; rows 1–6 are local-tree runs and their canaries never
reach a commit:

| # | Check | Canary planted | Expected failure | Local run recorded |
|---|---|---|---|---|
| 1 | secrets (tree + history) | token-shaped inert string | `scan: secrets` non-zero | ☐ |
| 2 | PHI patterns | MRN-shaped digit run | `scan: phi` non-zero | ☐ |
| 3 | protected text | over-budget quotation (30 words) | `scan: protected-text` non-zero | ☐ |
| 4 | local paths / identity | a placeholder user-profile path (see the split literal above) | `scan: identity` non-zero | ☐ |
| 5 | index/model root misuse | the index root spelled out in a test fixture | `scan: roots` non-zero | ☐ |
| 6 | licence / rights | dangling `source_id` | `scan: rights` non-zero | ☐ |
| 7 | badge → evidence (**the one pushed run**) | badge set to `status: skeleton` with no evidence file | `scan: badge` non-zero | ☐ CI run URL |

Additional acceptance:

1. Each red run fails **only** on its own check id — a canary that trips two scanners means one
   scanner is over-matching, and that is a defect to fix, not a pass.
2. After every canary is removed, one clean green CI run on `windows-latest`, URL recorded. `git
   log -p --all` after the pushed run contains no token-shaped, PHI-shaped, path-shaped or
   protected-text canary — asserted, not assumed.
3. `uv run epppsynth scan --history` finds nothing on the clean tree and its runtime is recorded
   (if the history scan is slow enough to discourage running it, that is a finding for EP-8's
   re-plan).
4. The canary allowlist has exactly one entry, asserted by a unit test that fails if a second is
   added. The rule-definition allowlist is separately reported: `epppsynth scan` on the clean tree
   exits 0 **and** prints the full inventory of lines it skipped, every one of which is a rule
   definition. A unit test asserts a marker does not exempt the following line, the enclosing
   block, or any other file.
5. The pre-commit hook and the CI step invoke the same command, asserted by a unit test comparing
   the two strings.
6. `epppsynth/docs/pre-publication-checklist.md` contains all seven items, opens with the
   defense-in-depth statement verbatim, marks items 5 and 7 as human, and carries an empty
   signature block.
7. The workflow still declares `permissions: contents: read` at top level, references no secret,
   and pins every action to a 40-hex SHA. `fetch-depth: 0` appears in exactly one job and carries
   its explanatory comment.
8. *(judgement — the project owner)* Someone who has never seen this repository can run
   `uv run epppsynth scan` and understand each finding without opening the source.

## Parked → final-roadmap.md

- An `allowlist.toml` for legitimate scanner exceptions. Deliberately **not** built: today the
  allowlist is one hard-coded directory with a test guarding its length, which is the property that
  makes it safe. A configurable allowlist is how scanners quietly stop working; revisit only with a
  named reason.
- Scanning rendered CI logs themselves for identity strings. The workflow is written not to print
  them, but "written not to" is weaker than "checked". Raise at the P5 verification re-plan.
- Screenshot EXIF stripping as an automated step. Item 5 is human for now because no screenshots
  exist; automate when the P5 UI briefs start producing them.
- A signed pre-publication attestation (the packet's signature block as a signed commit or a
  detached signature). Depends on the parked signed-commit policy from EP-0.
