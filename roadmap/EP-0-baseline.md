# EP-0 — Baseline & public-safety hygiene

**Size:** S · **Mode:** n/a · **Core/Stretch:** core ·
**Depends on:** — · **Blocks:** EP-1 (toolchain), EP-8 (roadmap tooling, re-plan P0)

## Context

This is the first executed brief in the plan, and it exists because of the order the repository was
created in. The repository is **already public** (D-3): history was erased and re-created, and
`.gitignore` was configured for the copyrighted corpus *before* any commit, so no path under
`source material/` has ever entered a commit. The usual "tidy it, then publish it" order is
unavailable — every commit from here on lands in a public tree. EP-0 therefore establishes a
*verified* baseline before any content brief writes a byte, so that every later brief inherits a
proven-clean starting point rather than an assumed one.

**What exists in the tree today.** Three commits. Six tracked files: `.gitignore`, `README.md`,
`epppsynth/README.md`, `roadmap/README.md`, `source material/README.md`, and
`tools/epub_to_md_pipeline.py`. `.gitignore` already excludes `source material/**` (with a negation
for that directory's own `README.md`), the common ebook and PDF extensions, Python build artefacts,
`.env*`, editor cruft, and `.local/`. The working tree also carries the uncommitted planning
bundle: the `.local/` addition to `.gitignore`, the rewritten `roadmap/README.md`,
`roadmap/_TEMPLATE.md`, and the P0–P7 briefs. **EP-0 commits that baseline.**

**What does not exist.** No `pyproject.toml`, no `src/` tree, no CI, no licence files, no canonical
docs, no `epppsynth/docs/` tree. Those are EP-1 … EP-8. `roadmap/final-roadmap.md` **does** exist,
seeded at planning time, and EP-0 only verifies it. EP-0 adds no project content of its own beyond
two repository-hygiene files.

Implements: D-3 (public by default), D-10 (corpus never redistributed), D-40 (repository layout),
and the GOVERNANCE public-safety posture (scanners are defense in depth, never proof). Mitigates
R-6 (public-history leakage) and R-7 (copyright / derivative distribution) at the point where they
are cheapest to prevent.

## Safety preconditions

| Invariant at risk | Guard in this brief |
|---|---|
| No copyrighted source text may ever enter the public tree (D-10, R-7) | Step 3's history assertion (`git log --all --diff-filter=A --name-only`) and step 2's `git check-ignore -v` probes both run **before** the baseline commit, and their raw output is pasted into the completion note. A non-empty result halts the brief. |
| No machine-identifying string may enter a public artifact (D-3; pre-publication checklist item 4) | Step 5 sweeps every tracked file for `C:` + `\Users\` (split per step 4's convention), the operator's Windows account name and the machine hostname — both read from the environment at run time and **never written into any tracked file** — plus UNC `\\` prefixes and any absolute drive path other than the two approved, deliberately public project roots. |
| `.local/` planning state must never be published (D-2) | Step 2 probes `.local/probe.md` through `git check-ignore -v`; step 7 asserts `git ls-files ".local"` is empty. |
| A clean tree is not a clean-history claim (D-3) | Step 4 scans the **full history**, not the tree. The completion note states in writing that these sweeps are defense in depth and that the authoritative artifact is the pre-publication packet built in EP-6. |
| An unverified fix could itself be the incident | If step 3 or step 4 finds anything, this brief **stops**. History rewriting on a public repository is an owner decision, not a step EP-0 may take. |

Pre-publication checklist items exercised here: **1 (secrets, full history)**, **3 (protected
text)**, **4 (local paths & hostname)**. EP-6 re-runs all seven once the packet exists.

## In scope

1. **Record the starting state.** Capture `git log --oneline`, `git ls-files` and
   `git status --porcelain` verbatim into the completion note. Expected: 3 commits, 6 tracked
   files, and the uncommitted planning bundle.
2. **Probe the ignore rules.** Run `git check-ignore -v` against each of
   `source material/probe.epub`, `source material/derived/probe.md`, `.local/probe.md`, `.env`,
   `epppsynth/.venv/probe`, and `probe.pdf`. Every one must report the `.gitignore` line that
   excludes it. Then assert the intended *negation*: `source material/README.md` returns no match.
   Record the matched line numbers.
3. **Assert clean history for the corpus.** Run
   `git log --all --diff-filter=A --name-only --pretty=format:` and filter the result for
   `source material/`. Only `source material/README.md` may appear. Anything else halts the brief.
4. **Full-history secret sweep.** Regex-sweep `git log -p --all` for token-shaped strings and
   credential assignments. **Pattern-writing convention, used throughout this brief:** every
   literal below is written **split across a `+`** so that this brief — itself a tracked file the
   sweep reads — does not match the rules it defines; reassemble each one before use. Token
   shapes: `ghp` + `_`, `github` + `_pat_`, `sk` + `-`, `AKI` + `A`, `xox[baprs]` + `-`, and
   `-----BEGIN [A-Z ]*PRIVATE` + ` KEY-----`. Credential assignments: `password` + `=` and
   `api[_-]?` + `key`. `gitleaks` is **not assumed present** on the target
   machine (standing posture: assume no tool that has not been verified present). If it happens to be
   available, run it as a second opinion and record which tool produced the result; the regex
   sweep is the guaranteed path.
5. **Local-path, username and hostname sweep over tracked files.** For every path in
   `git ls-files`, search for `C:` + `\Users\`, `C:` + `/Users/` (same splitting convention), the
   current account name, the current hostname, `\\`-prefixed UNC paths, and any absolute `X:\` <!-- leak-scan-allow: rule-definition -->
   path other than the two approved, deliberately public project roots. Zero hits required **after
   the step-6 allowlist is applied**.
6. **Build the rule-definition allowlist — a deliverable of this brief, not a footnote.** Both
   sweeps read every tracked file, and the briefs that define the rules necessarily contain the
   patterns they define. A line is exempt **only** if it carries the literal marker
   `leak-scan-allow: rule-definition` on that same line — as an HTML comment in markdown, as a
   trailing `#` comment in code, YAML or a workflow. The exemption is **line-scoped**: never a
   block, never a file, never a directory, and never a pattern. Steps 4 and 5 filter marked lines
   out **and** print the count and the paths of everything they skipped, so an exemption is always
   visible rather than silent. Record that inventory in the completion note; **EP-6** implements
   the identical marker in `epppsynth scan` and reconciles against this baseline.
7. **Tracked-file audit.** Assert `git ls-files "source material"` returns exactly
   `source material/README.md` and `git ls-files ".local"` returns nothing.
8. **Add `.gitattributes`** at the repository root: `* text=auto eol=lf` as the default;
   `-text` (binary) for `*.epub *.pdf *.gguf *.png *.jpg *.ico`; `*.py text eol=lf`. Without this,
   a CRLF round-trip can make a later leak-scanner diff unreadable and a "no change" claim false.
9. **Set repository-local long-path support:** `git config core.longpaths true`. Repository-local
   only — this brief makes no machine-wide, registry or elevated change.
10. **Verify `roadmap/final-roadmap.md`.** The file already exists with real content and
    `roadmap/README.md` links to it; publishing a tree with a broken relative link is a
    public-safety defect however small. **Do not create, replace, truncate or stub it.** Confirm it
    is present and non-empty, and that every relative link inside it resolves. If it is missing,
    stop and raise it with the owner rather than writing a replacement — EP-8 extends it, and a
    stub written here would destroy the seeded content.
11. **Commit the baseline** in two commits:
    `docs(repo): commit verified public-safe baseline (EP-0)` — covering `.gitignore`,
    `.gitattributes` and the roadmap bundle (`final-roadmap.md` included, unmodified) — then
    `docs(roadmap): record EP-0 commit hash`.

## Out of scope

- Python packaging, the `uv` project, any dependency — **EP-1**.
- Any CI workflow, pre-commit hook or automated scanner. EP-0 runs its sweeps by hand, once;
  turning them into enforced checks is **EP-6**.
- The README wording. The retired modality phrase is still in `README.md` when this brief ends —
  **EP-2** replaces it. EP-0 proves the tree is clean; it does not make it correct.
- Canonical docs (`DESIGN.md`, `GOVERNANCE.md`, `DECISIONS.md`) — **EP-2**.
- `LICENSE`, `NOTICE`, `CITATION.cff`, the rights table — **EP-5**.
- Extending `final-roadmap.md` — **EP-8**.
- Moving `tools/epub_to_md_pipeline.py` into the package (D-41) — **EP-22** (P2 corpus ingest).
  It stays exactly where it is, tracked and unmodified.
- Remote repository settings (Issues template, private vulnerability reporting). Done by the owner
  per D-76; the `SECURITY.md` that points at them is **EP-4**.

## Verification / acceptance

Runnable from the repository root:

```powershell
git ls-files "source material"
git ls-files ".local"
git check-ignore -v "source material/probe.epub" ".local/probe.md" ".env" "probe.pdf"
git log --all --diff-filter=A --name-only --pretty=format: |
  Select-String "source material/" | Where-Object { $_ -notmatch "README\.md$" }
$idpat = @(('C:' + '\\Users\\'), ('C:' + '/Users/'), '\\\\\\\\')   # leak-scan-allow: rule-definition
git ls-files | ForEach-Object { Select-String -Path $_ -Pattern $idpat }
git check-attr text -- README.md
git config --local core.longpaths
git status --porcelain
```

Acceptance:

1. Every probe in step 2 reports a matching `.gitignore` line; `source material/README.md` reports
   **no** match. Raw output pasted into the completion note.
2. The history assertion returns nothing except `source material/README.md`.
3. The secret sweep returns no hits outside lines carrying the step-6 marker, and the completion
   note names the tool that produced the result **and** lists every marked line it skipped.
4. The path/identity sweep returns no hits across all tracked files outside marked lines, and the
   marked-line inventory is pasted into the completion note. Every marked line is a rule
   definition; a marker on anything else is a defect that halts the brief.
5. `git ls-files "source material"` prints exactly one line; `git ls-files ".local"` prints none.
6. `git check-attr text -- README.md` reports `text: auto`; `git config --local core.longpaths`
   reports `true`.
7. `roadmap/final-roadmap.md` exists, is non-empty and is byte-identical to its pre-EP-0 state;
   every relative link in `roadmap/README.md` and in `final-roadmap.md` resolves —
   extract each `](...)` target and test it with `Test-Path`; zero failures.
8. `git status --porcelain` is empty after the two commits, and the EP-0 ☑ box in
   `roadmap/README.md` carries the short hash.
9. *(judgement — the project owner)* The completion note records what was **observed**, not what
   was assumed; any probe that could not be run says so, and says why.

## Parked → final-roadmap.md

- `gitleaks` / `trufflehog` as a pinned, installed dependency rather than an opportunistic second
  opinion. Deferred because EP-6 ships scanners that run with no third-party binary, and adding a
  scanner binary is a supply-chain decision (R-29) that P0 should not make in passing.
- A signed-commit policy for public commits. No `D-n` requires it; raise at the P0 re-plan (EP-8)
  if the owner wants provenance on the public history.
- Machine-wide `LongPathsEnabled` posture as documented prerequisite rather than a
  repository-local setting. Belongs with the third-party installability work, which D-33 puts
  beyond v1.

---

> **Completion note (2026-08-23).** Executed as written. Every acceptance check below records what
> was **observed**, not what was assumed. Where a check could not be run as specified it says so and
> says why, and four deviations are recorded — one of which leaves acceptance 8 partially unmet and
> is an owner decision, not something this brief may resolve.
>
> **Defense in depth, not proof.** The sweeps in steps 4 and 5 are defense in depth. They are *not*
> proof that nothing leaked. The authoritative artifact is the pre-publication review packet built
> in **EP-6** — performed by a human, recorded with a date and a commit hash. A green sweep here
> licenses no claim beyond "these patterns did not match on this date".

#### Step 1 — starting state (observed)

Three commits and six tracked files, exactly as the brief predicted:

```text
c2807d8 Add the EPUB to Markdown conversion pipeline
b435939 Add project scaffolding and exclude copyrighted source material
71947e1 Initial commit

.gitignore
README.md
epppsynth/README.md
roadmap/README.md
source material/README.md
tools/epub_to_md_pipeline.py
```

`git status --porcelain` showed ` M .gitignore`, ` M roadmap/README.md`, the 57-file untracked
roadmap bundle — **and three files the brief's "What does not exist" paragraph did not anticipate**
(deviation 1 below).

#### Step 2 — ignore-rule probes (raw output)

```text
.gitignore:9:*.epub                     source material/probe.epub
.gitignore:4:source material/**         source material/derived/probe.md
.gitignore:40:.local/                   .local/probe.md
.gitignore:26:.env                      .env
.gitignore:18:.venv/                    epppsynth/.venv/probe
.gitignore:13:*.pdf                     probe.pdf
```

All six report the excluding line. The intended **negation** was asserted three ways:
`git check-ignore` on `source material/README.md` exits **1 (not ignored)** both with and without
`--no-index`; run with `-v --no-index` it names `.gitignore:6:!source material/README.md` as the
last matching pattern — i.e. the file is carried by the negation on line 6, which is stronger
evidence than a bare absence of output.

#### Step 3 — corpus history assertion (raw output)

```text
$ git log --all --diff-filter=A --name-only --pretty=format: | grep "source material/"
source material/README.md
```

Filtered for entries that are **not** `README.md`: **empty**. The complete set of paths ever added
anywhere in history is the same six tracked files. Confirmed there is nothing else to scan:
`git show-ref` lists only `main` and `origin/main` (identical hashes), `git stash list` is empty,
`git rev-list --all --count` is 3. **PASS — the brief does not halt.**

#### Steps 4-6 — sweeps and the rule-definition allowlist

| Sweep | Scope | Result |
|---|---|---|
| Secret shapes | full history (`git log -p --all`, 555 lines) | **0 hits** |
| Secret shapes | 63 files (6 tracked + 57 to be published) | **0 hits** |
| Path / identity | 63 files (6 tracked + 57 to be published) | **0 hits**, after 3 allowlisted lines |

**Tool that produced the result.** A hand-written regex scanner, held **outside the repository** in
the session scratchpad so it is never tracked and never published. `gitleaks` and `trufflehog` were
both checked for and are **absent** on this machine, so no second opinion was available and the
regex sweep is the sole result — the guaranteed path the brief anticipated.

**Scope note (deviation 3).** The brief scopes step 5 to `git ls-files`. Scanning only the six
already-tracked files would have left the 57 roadmap files this brief *publishes* unscanned, which
inverts the brief's purpose, so the sweep was run over the union of tracked and about-to-be-tracked
files. The six tracked files alone are also clean.

**Rule-definition allowlist (step 6) — complete inventory, 3 lines.** Every one is a line that
defines a scan rule; there are no others, and no marker sits on anything that is not a rule
definition:

| File | Line | Rule matched | Form |
|---|---|---|---|
| `roadmap/EP-0-baseline.md` | 72 | absolute drive path | HTML comment |
| `roadmap/EP-0-baseline.md` | 127 | UNC prefix | trailing `#` (PowerShell) |
| `roadmap/EP-4-privacy-security-conduct.md` | 159 | UNC prefix + absolute drive path | trailing `#` (PowerShell) |

Line 127 already carried the marker. The other two were **added by this brief** — that is step 6's
deliverable, and those two markers are the only changes made to any brief's body text. **EP-6** must
reconcile `epppsynth scan` against exactly this inventory. A fourth line,
`roadmap/EP-0-baseline.md:78`, carries the marker *literal* because step 6 defines it there; it
matches no scan rule and therefore exempts nothing. A grep for the marker returns **4** lines
while the applied allowlist is **3** — `epppsynth scan` must count a marker only where it
actually suppresses a match.

**Two rule refinements, both recorded rather than silent:**

1. *Token shapes and identity strings are anchored to a word boundary.* Unanchored, the shortest
   token prefix in step 4 matches inside ordinary prose words, and the 5-character account name
   matches inside an unrelated English word — it did, at `tools/epub_to_md_pipeline.py:38`, a
   chapter title in already-public code. A real credential or a real path always begins at a token
   boundary. Without this anchoring the allowlist would have had to absorb dozens of prose false
   positives, which would have made the marker meaningless.
2. *The two approved roots are excluded by the rule, not by a marker.* Step 5 defines the rule as
   any absolute drive path **other than** the two deliberately public project roots
   (`C:\epppmodels`, `C:\epppindex` — the same exclusion EP-4 encodes in its own sweep). They are
   therefore not hits and correctly consume no allowlist entries; 19 of the 22 first-pass matches
   were these two roots quoted in EP-1, EP-4 and EP-7.

Neither the account name nor the hostname is written into any tracked file, including this note.
Both were read from the environment at run time, and the scanner redacts them from its own output.

#### Step 7 — tracked-file audit

```text
$ git ls-files "source material"     ->  source material/README.md      (exactly 1)
$ git ls-files ".local"              ->  (no output)                    (exactly 0)
```

`.local/` **does exist on disk with content** and is correctly untracked, so this is a live test of
the rule rather than a vacuous one.

#### Steps 8-9 — hygiene files

`.gitattributes` added with `* text=auto eol=lf`, `-text` for the six binary extensions, and
`*.py text eol=lf`. Verified: `git check-attr text -- README.md` reports `text: auto` (and
`eol: lf`); `probe.epub` / `probe.pdf` / `probe.png` report `text: unset`.
`git config --local core.longpaths` reports `true`. Repository-local only — no machine-wide,
registry or elevated change was made.

#### Step 10 — final-roadmap.md verified, not modified

Present, non-empty, **5531 bytes**, sha256
`7a5434b4a768a961adb657deb231c0710ad8e1cd252d00e1a370ddb62f0e6088`, byte-identical before and after
this brief. Not created, replaced, truncated or stubbed. Link resolution: **61/61** relative links
in `roadmap/README.md` and **1/1** in `final-roadmap.md` resolve, zero failures. Extended across all
61 markdown files in the bundle: **64/64** resolve.

#### Deviations

1. **Three untracked files the brief did not anticipate, deliberately left untracked.**
   `epppsynth/DECISIONS.md`, `epppsynth/DESIGN.md` and `epppsynth/GOVERNANCE.md` exist in the
   working tree with substantial content. The brief states these do not exist and places them in
   **EP-2**, whose own text says it *creates* them. They were **not committed**: publishing them
   here would perform EP-2's work while skipping EP-2's checks — in particular its tense sweep, its
   retired-modality grep and its `.local/` overlap diff — and EP-0's job is to prove the tree clean,
   not to widen it. **Consequence: acceptance 8 is not fully met.** `git status --porcelain` is not
   empty after the two commits; it lists exactly these three files and nothing else. Resolving this
   is EP-2's business, or the owner's.
2. **No second-opinion scanner.** `gitleaks` and `trufflehog` are absent; the regex sweep is the
   only result. Recorded per the brief's standing posture that no unverified tool is assumed present.
3. **Sweep scope widened to files about to be tracked** (see above).
4. **`.gitattributes` was added but the repository was not renormalised.** Three already-committed
   blobs still contain CRLF (`README.md`, `source material/README.md`,
   `tools/epub_to_md_pipeline.py`; `core.autocrlf` is unset). `git status` does not flag them —
   git's stat cache suppresses the comparison — so the tree looks clean while the condition step 8
   exists to prevent is still live: the next brief that touches `README.md` will produce a
   whole-file diff. Renormalising was **not** done because step 11 enumerates the commit contents
   exhaustively and those files belong to EP-2 and EP-22, and because rewriting a 427-line tool
   file's blob exceeds a brief whose doctrine is to verify rather than change.
   **Recommended for EP-1:** `git add --renormalize .` as its own commit.

#### Not done, deliberately

Nothing was pushed. Step 11 specifies two commits and says nothing about publishing them; `origin`
is configured, and leaving `main` ahead of the remote is the owner's call.
