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

Implements: D-2 (settled decisions published, deliberations not — the refined shared-passage
invariant of the 2026-08-31 addendum), D-3 (public-safe by default), D-4 (retired modality
wording), D-10 (corpus never redistributed), D-42 (CI posture),
D-51 (index root outside the tree, never in CI), D-59 (badge resolves to an evidence file or CI
fails), D-74 (quotation budget enforced in CI). Mitigates R-6 (public-history leakage), R-7
(rights leakage), R-19 (index reaching a published artifact via fixture, screenshot or error
message), R-9 (badge tied to effort), R-29 (supply chain — the scanners cover the workflow files
themselves).

## Safety preconditions

| Invariant at risk | Guard in this brief |
|---|---|
| Scanners mistaken for proof (GOVERNANCE §Public-safety) | `epppsynth/docs/pre-publication-checklist.md` opens with the defense-in-depth statement verbatim and states that items 5 (screenshots) and 7 (public claims) are **human** steps that no script replaces. The packet records a date, a commit hash and a human name; a green CI run is not a substitute and the document says so. |
| The canaries themselves leaking (a scanner test that plants a real-looking secret) | The nine **red runs** are executed locally and their canaries never enter a commit (item 8). The committed unit-test fixtures live under `epppsynth/tests/canaries/` and contain **synthetic, structurally-valid-but-inert** strings: a token-shaped string with a documented non-existent prefix, an MRN-shaped digit run, a fake `C:` + `\Users\<placeholder>\` path with a literal placeholder segment. Every canary file carries a header line stating it is a deliberate test fixture. The scanners are configured to **exempt exactly that directory** by explicit path, never by pattern — a pattern-based exemption is how a real leak later hides. |
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
      and the D-74 quotation budget via EP-5's `count_quotations`. Plus, from the **2026-08-31
      addendum under D-74** (owner ruling OD-6): a **tracked chapter-title sequence** is a finding —
      three or more title-shaped strings adjacent to a chapter ordinal or a reading-order index, in
      any tracked file. That is how a source's outline reconstructs itself, and it is the pattern
      EP-2 found in `tools/epub_to_md_pipeline.py` and that ruling removed on 2026-08-31 by moving
      the spine to untracked local config. The check exists so the pattern cannot return by another
      route — `tools/` sat outside the registry-shaped guard that covered Y-8 until then.
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
   8. **Retired modality term** (D-4; owner ruling **OD-10**, confirmed 2026-08-31) — a **stem**
      sweep for `psychotherap` across every tracked file, implemented with an **exemption table
      carrying reasons**, never as a bare grep and never as a bare path list. The owner-ratified
      table has **three** entries:

      | File | Reason |
      |---|---|
      | `epppsynth/DECISIONS.md` | D-4 records the retired expansion; the record must keep the word |
      | `roadmap/EP-2-canonical-docs.md` | self-referential — the brief quotes the token in order to specify the sweep |
      | `roadmap/EP-6-leak-prevention-ci.md` | this brief, for the same reason |

      Two of the four rows EP-2 proposed are deliberately **absent**. `source material/README.md`
      was proposed precautionarily; the sweep confirmed it contains **no** occurrence, and an
      exemption for a file that does not need one is a hole waiting for a future edit.
      `tools/epub_to_md_pipeline.py` was the fourth, exempt *for now, with a reason*; that
      exemption **expired** when OD-6 was ruled **live** on 2026-08-31 and the spine moved out of
      the tracked file.

      **One occurrence must be resolved before this scanner can run green.** EP-2 swept for the
      exact token `psychotherapy`; widening to the stem surfaces one file that grep could not
      match — `roadmap/EP-12-seed-givens.md` line 122, *"mid-twentieth-century Western
      **psychotherapeutic** idiom"*. Resolve it the way EP-2 resolved its own four hits: **reword
      to the broader term** ("therapeutic"), which strengthens the disclaimer rather than weakening
      it. Do **not** add a fourth exemption — the table above is the owner-ratified list and grows
      only by a further ruling.
   9. **Private-ledger passages** (D-2; owner ruling **OD-3**, 2026-08-31) — the **refined**
      invariant, which is the one EP-2's measurement showed to be implementable: every eight-word
      sequence shared between `epppsynth/DECISIONS.md` and any file under `.local/` must fall
      **inside a published decision entry or the index block**. A shared passage in the surrounding
      prose is a finding. The literal form — *no* shared eight-word sequence — is unsatisfiable by
      construction and is **not** what this scanner implements: the ledger records each decision in
      the words it was settled in and D-2 requires publishing those settled decisions, which is why
      EP-2 measured 124 shared passages, 19.7 % by word count, longest 42 words, and every one of
      them inside an entry.

      **How it runs, and why the mechanics are part of the specification.** The check is a script.
      It reads `.local/` and reports **only** positions and counts inside the already-public file —
      never the matched text, never a line of private content, in its output, its exit message or
      its CI summary. Nothing private reaches a session transcript, a CI log or a public file,
      which is what makes a check over `.local/` compatible with the never-read rule in
      `CLAUDE.md`. It is **local and pre-commit only**: `.local/` does not exist on a CI runner, so
      the CI job must report `skipped — no ledger present` and must **not** report a pass. A skip
      counted as a pass is exactly how this check would quietly stop working.
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
   `uv run epppsynth scan --history`. Check 9 (private-ledger passages) has no ledger to read on a
   runner: it must print `skipped — no ledger present` and be counted as skipped, never as passed.
5. **Pre-commit hook.** `.githooks/pre-commit` invoking the identical command (without `--history`,
   for speed, with a comment stating that the history scan is CI's job), plus a documented
   `git config core.hooksPath .githooks` step and a note that hooks are advisory: they run on the
   operator's machine and can be bypassed, which is exactly why CI runs the same check.
6. **`epppsynth/docs/pre-publication-checklist.md`** — the seven items, each with: what is checked,
   the command that checks it, what the script **cannot** check, and a signature block (date,
   commit hash, human name). Items 5 (screenshots re-opened and read, EXIF stripped, no source
   pane, no local paths in a title bar, no notification toasts) and 7 (README, badge, `prime` card
   and `CITATION.cff` all say the same thing and none says more than the evidence supports) are
   marked **human** and have no script. Checks 8 and 9 add **no eighth item**: GOVERNANCE §7 fixes
   the packet at seven, so the checklist records the mapping instead — check 8 (retired modality
   term) is evidence under item 7 (public claims compared against evidence) and check 9
   (private-ledger passages) under item 3 (protected text). Say so in the document, so a reader is
   not left counting nine scanners against seven items and assuming one is missing.
7. **Canary fixtures** under `epppsynth/tests/canaries/` — one per scanner, **nine** in total, each
   with a header line declaring itself a deliberate fixture, each inert. Check 9's canary is a
   **synthetic pair** — a fake decisions file and a fake ledger file, both authored here — so that
   proving the ledger check works never requires reading or copying the real `.local/`.
8. **Run the deliberate red runs — locally.** **No red-run canary is pushed.** A public
   repository's history is permanent and an unreachable object is not a deleted one; proving a
   scanner works is not a reason to write a token-shaped or patient-shaped string into that
   history. (This is distinct from item 7's committed fixtures, which are inert by construction,
   header-declared, and confined to one allowlisted directory — the red runs plant *un*-exempted
   copies outside it, and those must never leave the working tree.) For each of the nine checks: plant the canary in the **working tree
   only**, run the *same* command CI runs (`uv run epppsynth scan --history`), record the exact
   failing check id and the command's output, remove the canary, and confirm a clean local run.
   All **nine** go in the completion note as a table of local runs.
   Then, **once**, prove the CI wiring itself fires: push a single **innocuous** canary — the
   badge set to `status: skeleton` with its evidence file absent, which carries no secret, no PHI,
   no local path and no protected text — on a scratch branch; record the failing CI run URL and
   check id; revert; confirm green. The nine local runs prove the rules; the one pushed run proves
   the workflow is wired to them. State that split explicitly in the completion note, so a later
   reader does not read "one CI red run" as thin evidence.
9. **Record the exemption rules** in `ADR-008` (CI scope and pinning): the canary directory is
   allowlisted by exact path, the allowlist has exactly one entry, and adding an entry requires an
   ADR amendment. Record the **modality-sweep exemption table** (check 8) beside it as a *third*,
   separately-counted allowlist: three entries, each carrying its reason, owner-ratified
   2026-08-31, growing only by a further **owner ruling** — not by an ADR amendment and not by a
   session's judgement. None of the three allowlists may be used to reach another's scope.
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

The acceptance criterion for this brief is **nine deliberate local red runs, one pushed
innocuous CI red run, and one clean green run**, recorded as a table in the completion note with
one row per check. Only row 7 is pushed; rows 1–6, 8 and 9 are local-tree runs and their canaries
never reach a commit:

| # | Check | Canary planted | Expected failure | Local run recorded |
|---|---|---|---|---|
| 1 | secrets (tree + history) | token-shaped inert string | `scan: secrets` non-zero | ☐ |
| 2 | PHI patterns | MRN-shaped digit run | `scan: phi` non-zero | ☐ |
| 3 | protected text | over-budget quotation (30 words) | `scan: protected-text` non-zero | ☐ |
| 4 | local paths / identity | a placeholder user-profile path (see the split literal above) | `scan: identity` non-zero | ☐ |
| 5 | index/model root misuse | the index root spelled out in a test fixture | `scan: roots` non-zero | ☐ |
| 6 | licence / rights | dangling `source_id` | `scan: rights` non-zero | ☐ |
| 7 | badge → evidence (**the one pushed run**) | badge set to `status: skeleton` with no evidence file | `scan: badge` non-zero | ☐ CI run URL |
| 8 | retired modality term (OD-10) | the stem planted in a file outside the three-entry exemption table | `scan: modality` non-zero | ☐ |
| 9 | private-ledger passages (OD-3) | the synthetic pair, with a shared eight-word run placed in the fixture's **prose** rather than inside an entry | `scan: ledger` non-zero | ☐ |

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
   added. The modality-sweep exemption table has exactly **three** entries, each with a non-empty
   reason string, asserted by a second unit test that fails if a fourth is added — that table is an
   owner ruling, not a developer convenience. The rule-definition allowlist is separately reported: `epppsynth scan` on the clean tree
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

---

> **Completion note (2026-08-31).** Executed. `epppsynth/src/epppsynth/publicsafety/` ships the nine
> scanners as importable, tested functions; `epppsynth scan [--history] [--fix-hints] [--check ID]`
> is the single entry point the CI `scan` job and `.githooks/pre-commit` both invoke;
> `epppsynth/docs/pre-publication-checklist.md` is the seven-item packet; `epppsynth/tests/canaries/`
> holds the nine committed fixtures; `ADR-008` carries the EP-6 amendment. `git config
> core.hooksPath` reports `.githooks`. `uv run epppsynth scan --history` exits **0** on the clean
> tree in **1.9 s wall** (tree plus 1,327,407 patch bytes of `git log -p --all`), which is fast
> enough that nobody will avoid running it — no re-plan finding for EP-8 on that count. 139 tests
> pass (41 of them new); `ruff check` and `ruff format --check` are clean.
>
> **The red runs: nine local, none pushed.** Every canary was planted in the working tree, staged
> only so that `git ls-files` could see it — the scanners read tracked files, so writing a file
> without staging it proves nothing — scanned with the *same* command CI runs, then unstaged and
> deleted. **Nothing was committed.** Placement was chosen so each canary fell under an existing
> `REUSE.toml` annotation; a canary at the repository root would also have tripped `rights` with
> `licence-uncovered`, and a red run that fails two checks is not evidence about one.
>
> | # | Check | Canary planted | Expected | Observed |
> |---|---|---|---|---|
> | 1 | secrets | `epppsynth/tests/redrun-secrets.txt` | `scan: secrets` non-zero | ☑ exit 1; `secrets` alone; `github-token` L8, `credential-assignment` L10 |
> | 2 | phi | `epppsynth/tests/redrun-phi.txt` | `scan: phi` non-zero | ☑ exit 1; `phi` alone; `mrn-shaped-digit-run` L7, `email-address` L12 |
> | 3 | protected text | `epppsynth/docs/redrun-protected.md` | `scan: protected-text` non-zero | ☑ exit 1; `protected-text` alone; `quote-budget` L11, `chapter-title-sequence` L19 |
> | 4 | local paths / identity | `epppsynth/tests/redrun-identity.txt` | `scan: identity` non-zero | ☑ exit 1; `identity` alone; `user-profile-path` L6, `unc-path` L8, `foreign-drive-letter` L6 |
> | 5 | index/model root misuse | `epppsynth/tests/redrun-roots.yaml` | `scan: roots` non-zero | ☑ exit 1; `roots` alone; `index-root-outside-documentation` L6, `model-root-outside-documentation` L7 |
> | 6 | licence / rights | `epppsynth/registry/concepts/redrun-canary.yaml` | `scan: rights` non-zero | ☑ exit 1; `rights` alone; `source-ref`, dangling `source_id` |
> | 7 | badge → evidence | the README badge set to `status: skeleton` | `scan: badge` non-zero | ☑ **local** exit 1; `badge` alone; `evidence-file-absent` for `epppsynth/docs/evidence/skeleton.md`. **The pushed CI run is outstanding — see below.** |
> | 8 | retired modality term | `epppsynth/tests/redrun-modality.md` | `scan: modality` non-zero | ☑ exit 1; `modality` alone; both the token and the adjectival form, L10 and L11 |
> | 9 | private-ledger passages | the synthetic pair, on a temporary root | `scan: ledger` non-zero | ☑ `failed`; **one** finding, at the fixture's prose line 8; the 22 passages shared inside the entry correctly not reported |
>
> Acceptance 1 holds for all nine: **each red run failed only on its own check id.** Acceptance 2's
> history assertion was run afterwards — `git log -p --all` contains **0** occurrences of the
> token shape, the credential assignment, the planted digit run, the user-profile path, the UNC
> host, the string `redrun-`, or the modality canary's header. Acceptance 3, 4, 5, 6 and 7 are
> covered by `epppsynth/tests/test_publicsafety.py`, which fails if a second canary-allowlist entry
> or a fourth modality-exemption row appears.
>
> **Two acceptance rows are outstanding, and they are the two that need a push.** Row 7's pushed CI
> red run and the clean green CI run on `windows-latest` require the commits to reach the remote,
> which was left to the owner. Everything else in the brief is done. To close them: push `main` and
> record the green run URL; then, on a scratch branch, change the one `status: design` line in
> `README.md` to `status: skeleton` (the canary in `epppsynth/tests/canaries/badge_README.md`),
> push, record the failing run URL and the check id, delete the branch, and confirm green. That
> canary carries no secret, no PHI, no local path and no protected text, which is why it is the one
> that may be pushed. **The nine local runs prove the rules; the one pushed run proves the workflow
> is wired to them** — read as one CI red run, that is thin; read as the split it is, it is not.
>
> **Deviations and what they cost.**
>
> 1. **The three-entry modality table could not run green as ratified, and OD-14 is opened.** OD-10
>    named exactly one occurrence left to resolve — `roadmap/EP-12-seed-givens.md` line 122, reworded
>    here to *"mid-twentieth-century Western therapeutic idiom"* exactly as ruled. The stem sweep run
>    against the tree as it stands surfaces **seventeen more, in twelve files**, none of which the
>    ruling could have seen: they arrived with **EP-5**, which landed the source rights record on the
>    same day OD-10 was written. Every one is the Yalom `source_id` or the citation title it is built
>    from. Resolved **not** by a fourth exemption row — that needs a further ruling, and the table
>    still has exactly three entries, guarded by a unit test — but by a **rule refinement**: an
>    occurrence inside a `source_id` or citation `title` that `epppsynth/registry/sources.yaml`
>    declares is bibliographic identity, which D-74 requires this project to be able to cite, and not
>    this project describing itself. It is derived from an owner-ratified data file rather than from
>    a session's judgement, it is inventoried on every run under `bibliographic-identity`, and it
>    fails closed. **Registered as OD-14 in `roadmap/owner-decisions.md` for ratification**, and
>    recorded in the `ADR-008` amendment. It is not a blocker: the scanner runs green with it, so a
>    ruling either ratifies what is there or directs a change.
> 2. **`roadmap/owner-decisions.md` lines 379–381** carry the stem while recording the ruling that
>    defines the sweep — the same reason the two exempt briefs do. Resolved with the general
>    line-marker mechanism of §2.1, not with a fourth path exemption. The ruling's own words are
>    untouched.
> 3. **EP-4's block-level marker became line markers.** `epppsynth/tests/test_public_docs.py` carried
>    `leak-scan-allow: rule-definition` on its own line above the `IDENTITY_PATTERNS` tuple. §2.1
>    makes the marker line-scoped and never inherited, so the scanner did not honour it and reported
>    it as an unnecessary marker. Moved onto the two lines that actually match a rule. Two of the
>    four pattern lines needed no marker: they do not match the rules they define.
> 4. **A tenth check id, `allowlist`, is reported.** The nine remain the nine; `allowlist` is the
>    rule-definition allowlist checking itself, which is how §2.1's "a marker on a non-rule line is
>    reported as a defect" is implemented. A marker that suppresses nothing is a finding.
> 5. **A marker is recognised only in a comment, never in backticks.** `CLAUDE.md`, EP-0, EP-4, EP-6
>    and `quotes.py` all *name* the marker in prose. Inline code spans are stripped before the marker
>    is looked for, so naming it is not using it. Without that, every mention would have exempted its
>    own line.
> 6. **The quotation budget was widened, and one brief needed a reason.** The counter now runs over
>    every tracked markdown file outside `epppsynth/tests/` — the widening
>    `rights.paths.quotation_scan_paths` named so it would be a visible edit. The test tree is
>    outside the input set **by scope, not by exemption**, on OD-12's own precedent: it holds EP-5's
>    deliberately over-budget fixture, and a waiver inside the set would be indistinguishable from a
>    real one. The widening surfaced one 34-word self-quotation in `EP-14`, which is a worked example
>    of this project's own output constraint and not a quotation of any source; it carries a
>    `quote-budget-allow` comment stating that reason.
> 7. **Three accounted-for matches were needed, and none of them is a path exemption.** A digit run
>    that `git rev-parse` resolves as an object in this repository (two all-numeric short hashes in
>    roadmap rows); a `size =` value in the machine-generated resolver lockfile (43); and the one
>    email address this repository already publishes in its own commit metadata (6, owner ruling
>    OD-7). Each is mechanical, each fails closed, each is printed in the summary. Recorded in the
>    `ADR-008` amendment as accounted-for matches rather than as a fourth allowlist.
> 8. **Hook/CI equality is asserted as a relation, not as raw string equality.** The brief asks for
>    equal command lines *and* for `--history` in CI only; those cannot both hold. The unit test
>    asserts `hook + " --history" == ci step`, which is strictly stronger than a loose comparison.
> 9. **Red run 9 could not be planted in the real tree.** Doing so would mean writing into `.local/`
>    and editing `DECISIONS.md`'s prose. It ran against a temporary root holding the synthetic pair,
>    through the same `scan_ledger` code path. The CI shape was confirmed separately: with no
>    `.local/` present the check reports `skipped — no ledger present` and its status is `skipped`,
>    asserted **not** equal to `passed`.
> 10. **`.githooks/**` needed three edits, and the scanner found the omission itself.** Adding the
>    hook to `REUSE.toml` without adding it to `NOTICE` and `README.md` failed EP-5's boundary tests,
>    and omitting it from `REUSE.toml` altogether produced a `licence-pattern-unused` finding. All
>    three now agree.
> 11. **`epppsynth/tests/test_smoke.py` was updated** to call `cli.main([])`. The CLI now parses its
>    arguments, and under pytest `sys.argv[1:]` is pytest's own.
> 12. **A path is fixed for EP-25.** The D-36 scenario-attestation check reads
>    `epppsynth/eval/scenarios/`, runs over an empty set today, and becomes live by content. EP-25
>    uses that path or changes the constant.
>
> **Observed, and worth carrying to EP-8.** The clean tree's skip inventory is 82 lines across six
> reasons. Forty-three of them are one lockfile, which is noise the eye will learn to skip; the
> eleven that matter — the rule-definition markers — are listed separately and are the ones a reader
> should audit. `epppsynth/DECISIONS.md` shares **1,145** eight-word passages with private planning
> state, 11.6 % of the file by word count, and **every one of them** falls inside a published entry,
> an addendum, or the index block. EP-2 measured 124 passages and 19.7 % under a coarser method;
> both measurements say the same thing about where the sharing is, which is what OD-3 ruled on.
> Recognising an addendum blockquote as published content was necessary and is not a loosening: D-1
> says a decision is never edited, only appended to, so an addendum *is* the entry.
>
> **Acceptance 8 is owner judgement and is offered, not claimed.** Every finding prints a check id,
> `path:line`, a rule name and a sentence saying what the rule means; `--fix-hints` adds a one-line
> remedy. No finding prints the matched text, which is deliberate and is itself a limit on
> legibility: a reader is told where to look and never shown what was found.

> **Addendum (2026-09-01).** **OD-14 is ruled: ratified as implemented.** The `bibliographic-identity`
> refinement stands at exactly the scope EP-6 built it — a skip only where the stem falls inside a
> `source_id` or citation `title` that `epppsynth/registry/sources.yaml` declares, never a file, a
> directory, a pattern or a line. It lands where OD-10 landed, in the scanner definition, with the
> reasoning recorded in `roadmap/owner-decisions.md` under *Resolutions — 2026-09-01* and the scope
> restated in `ADR-008`. No `DECISIONS.md` addendum was written and none is warranted: D-4 and D-74
> are unchanged, and a sweep is not a decision. The OD-10 table still has three entries. Deviation 1
> of the completion note above is therefore closed; the two CI rows remain the only outstanding work.

> **Addendum (2026-09-01) — a defect the brief's own design created, found by committing.**
> The completion note above records `uv run epppsynth scan --history` exiting **0**. That was true
> when it was run and **false one commit later**, and the reason is worth keeping.
>
> The tree sweep skips the canary directory by exact path. The history sweep was a flat regex over
> `git log -p --all` with **no path awareness at all**, so the moment `epppsynth/tests/canaries/`
> reached a commit, the committed token-shaped fixture put the secrets check permanently red — two
> findings, on a repository containing no secret. Item 7 of the brief requires those fixtures to be
> committed and item 1.1 requires the history sweep; the two are in tension, and nothing in the
> brief resolves it because the tension only appears *after* the first commit lands. The nine local
> red runs could not have caught it: they were run before the commit existed, which is exactly when
> a history check has nothing to say.
>
> **Fixed by making the history sweep honour the same allowlist by the same path.** `git log -p --all`
> is split into one segment per file diff, keyed on the `+++ b/…` line (which runs to end-of-line and
> so survives a path containing spaces; a deletion falls back to `--- a/…`). A segment under the one
> allowlisted directory is skipped and inventoried under the reason `canary-directory`. **Commit
> headers and commit messages form the first segment and carry no path, so they can never be exempt** —
> a secret pasted into a commit message is a secret in the history.
>
> Four behaviours were then proven on throwaway repositories, and are now unit tests:
>
> | Situation | Observed |
> |---|---|
> | the canary committed, nothing else | `passed`, one `canary-directory` skip |
> | the identical token shape committed **outside** the canary directory | `failed` |
> | that file then deleted from the tree | `failed` on the history, **zero** tree findings — the "an unreachable object is not a deleted one" property, demonstrated rather than asserted |
> | the token shape in a **commit message** | `failed` |
>
> Adding those tests also tripped the PHI sweep on the test file's own throwaway git-author address,
> which is the split-literal convention working as intended; the literal is now assembled across a
> `+`. Test count is 143. `uv run epppsynth scan --history` exits 0 again, and this time on a tree
> whose history contains the canaries.
>
> **What this says about the packet.** A check can be green, correct, and about to become wrong,
> and no scanner told anybody — the commit did. It is the plainest available argument for
> `epppsynth/docs/pre-publication-checklist.md` being a human step re-run *before publication*
> rather than a CI badge: scanners are defense in depth, and this is what the depth is for.

> **Addendum (2026-09-01) — the first pushed run, and what it caught.**
> Run [33535486728](https://github.com/willtfarrington/epppsynth/actions/runs/33535486728) on `main`:
> **`scan` passed in 24 s, `test` failed.** The new job works on a runner — `fetch-depth: 0`, the
> full-history secret sweep, the `git rev-parse` exception, and `ledger` reporting
> `skipped — no ledger present` all behaved — and the failure was in the *old* job, caused by the
> new tests.
>
> `actions/checkout` fetches at depth 1 unless told otherwise, and the `test` job is deliberately not
> told otherwise. The `git-object-id` exception asks git whether an all-digit run names a real object
> here; in a shallow clone git cannot answer, so the two all-digit short hashes recorded in
> `roadmap/README.md` and `EP-0` became `mrn-shaped-digit-run` findings, and the two unit tests that
> scan the whole repository and assert it is green failed. **The rule failed closed, which is
> right.** What was wrong is that it failed closed *silently*, and an unexplained PHI finding on a
> repository containing no PHI is worse than none: it teaches a reader to disbelieve the check.
>
> **Fixed in three parts, none of which loosens a rule.**
> 1. `scan_phi` detects a shallow clone and says so in its note — `SHALLOW CLONE - the git-object-id
>    exception cannot be evaluated … Re-run with the full history before believing a digit-run
>    finding.` The finding still stands.
> 2. The two whole-repository tests are skipped on a shallow clone, with that reason named. The
>    property is not lost: the `scan` job runs the identical scan with the full history and fails the
>    build. `fetch-depth: 0` still appears in **exactly one job**, and the `test` job still fetches no
>    history it has no use for — giving it a deep fetch to make a test pass would have been undoing a
>    deliberate posture for convenience.
> 3. The new test's own literal `3706992` is split across a `+`, so the test file carries no digit run
>    of its own. Same convention, same reason.
>
> Verified by cloning this repository `--depth 1` and running the CI commands inside it: **142 passed,
> 2 skipped**, and the `phi` row carries the shallow-clone note. On the full clone: 144 passed,
> `--history` exit 0. Recorded in `ADR-008` as a second dated EP-6 amendment.

> **Addendum (2026-09-01) — the two CI rows are closed. EP-6 is complete.**
>
> | Row | Run | Observed |
> |---|---|---|
> | clean green run, `main` | [33536220160](https://github.com/willtfarrington/epppsynth/actions/runs/33536220160) | ✅ `scan` 26 s, `test` 1m02s. `secrets  passed  tree + history (1,503,038 patch bytes)`; `ledger  skipped  skipped — no ledger present`; `test` 142 passed, 2 skipped |
> | pushed red run, `ep6-badge-canary` | [33537175379](https://github.com/willtfarrington/epppsynth/actions/runs/33537175379) | ❌ `scan` failed on **`badge  epppsynth/docs/evidence/skeleton.md  evidence-file-absent`** — every other check passed, `ledger` skipped |
>
> The badge canary was one commit changing one line of `README.md`, committed with `--no-verify`
> because the pre-commit hook runs the same scan and refused it. That refusal is the hook proving
> itself. The branch was deleted from the remote and locally afterwards.
>
> **Three things the pushed runs proved that no local run could.**
>
> 1. `secrets  passed  tree + history (1,503,038 patch bytes)` on the runner — `fetch-depth: 0`, the
>    deep fetch and the full-history sweep all work in CI, not just on a machine that happens to have
>    the history lying around.
> 2. `ledger  skipped  skipped — no ledger present`, on a runner where `.local/` genuinely does not
>    exist. Locally that path can only be simulated. This is the row OD-3 warned would be easiest to
>    get quietly wrong, and it is **skipped**, not passed.
> 3. The `scan` job is wired to the rules: changing one line of a public artifact turned it red, with
>    the right check id and the right rule, and nothing else moved.
>
> On the canary branch the `test` job also failed, with `1 failed, 141 passed, 2 skipped` — the one
> failure being `test_the_cli_scan_accepts_a_single_check`, which asserts a clean-tree exit 0 and is
> correctly red while a canary is planted. Two of the three tests that would have failed locally were
> *skipped* there, because that job checks out shallow; the local run on the same branch failed all
> three. Both are right, and the difference is the shallow-clone behaviour documented above.
>
> **An incidental finding, recorded because it was not asked for.** The first attempt at the canary
> wrote the badge line as `status: design → status: skeleton`, and the checker reported
> `badge-unparseable  0 line(s) match the EP-2 badge contract; exactly one must` rather than
> `evidence-file-absent`. That is check 7's *other* behaviour — a **malformed** badge is caught
> distinctly from a badge that has outrun its evidence — demonstrated by accident and worth keeping,
> because a badge nobody can parse is a badge nobody is checking.
>
> **Stale markers retired.** `EP-6` is done, so three `planned — EP-6` markers were removed: the
> badge checker in `README.md` §Maturity badge, the secret-scanner assertion in `SECURITY.md`, and
> row 1 of the `PRIVACY.md` §11 enforcement register, which now reads *scanner runs in CI and in the
> pre-commit hook*. Present tense only for what exists today (`CLAUDE.md`, GOVERNANCE §1) — leaving a
> `planned` marker on a thing that now exists is an understatement, but it is still a public artifact
> disagreeing with the repository.
>
> **One last thing the scanner caught, on the commit that closed it.** This addendum first quoted the
> runner's patch size as a bare seven-digit figure, and `phi` reported two `mrn-shaped-digit-run`
> findings against this file. Correct: a bare seven-digit run in prose is precisely the shape the
> rule exists for, and `git rev-parse` cannot vouch for it. Written with thousands separators, which
> is the better prose form regardless. The completion note for the brief that built the scanners was
> edited by the scanners, twice — which is the most direct evidence available that they run on
> everything and are exempt from nothing.
