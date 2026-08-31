# Pre-publication review packet

The seven items of `GOVERNANCE.md` §7, as a runnable checklist. It is re-run before any publication:
a push that changes a public artifact, a tag, a screenshot, a demo, or a narrative page.

> `.gitignore`, pre-commit hooks and CI scanners are **defense in depth. They are not proof that
> nothing leaked.** The proof is the pre-publication review packet, performed by a human, recorded
> with a date and a commit hash.

That sentence is the reason this document exists as prose with a signature block rather than as a
green tick on a CI run. A green run means nine scanners found nothing. It does not mean nothing is
there. **Items 5 and 7 are human steps and no script replaces them.**

This matters more here than it would elsewhere because the repository's history was erased and
re-created: a clean current tree is not a clean history claim.

## How to run it

From `epppsynth/` (the uv project; the git root is its parent):

```powershell
uv run epppsynth scan --history          # items 1, 2, 3, 4, 6 and the evidence half of 7
uv run epppsynth scan --fix-hints        # the same, with a one-line remedy under each finding
uv run pytest epppsynth/tests/test_publicsafety.py -q
```

`epppsynth scan` exits non-zero on any finding and prints one line per finding: check id, `path:line`,
rule name, and what the rule means. It never prints the matched text — a CI log that quoted a secret
would be the artifact the secrets check exists to prevent.

The pre-commit hook runs the same command without `--history`. Install it once:

```powershell
git config core.hooksPath .githooks
```

Hooks are advisory: they run on the operator's machine and can be bypassed. That is why CI runs the
same check.

If `gitleaks` or `trufflehog` happens to be installed, run one as a **second opinion** and record
which tool produced the result. Neither is a dependency of this project and neither is assumed
present.

## Nine scanners, seven items

`GOVERNANCE.md` §7 fixes the packet at seven items, so checks 8 and 9 add no eighth item. They map
onto the seven, and the mapping is written down here so a reader is not left counting nine scanners
against seven items and assuming one is missing.

| Scanner (check id) | Packet item |
|---|---|
| `secrets` | 1 — secrets scanned across the full history |
| `phi` | 2 — PHI-shaped patterns swept across tracked files and fixtures |
| `protected-text` | 3 — protected text checked |
| `ledger` | 3 — protected text checked (private planning state, D-2 / OD-3) |
| `identity` | 4 — local paths and machine identifiers swept |
| `roots` | 4 — local paths and machine identifiers swept (the index and model roots) |
| — *(no scanner)* | 5 — screenshots re-opened and read · **human** |
| `rights` | 6 — licence conformance checked |
| `badge` | 7 — every public claim compared against its evidence file |
| `modality` | 7 — every public claim compared against its evidence file (D-4, ruling OD-10) |

---

## Item 1 — Secrets, across the full history

**What is checked.** Token shapes (GitHub, fine-grained PAT, provider key, AWS access key id, Slack)
and credential assignments, over every tracked file **and** over `git log -p --all`. The history
sweep is what `--history` adds, and it is the reason the CI `scan` job is the only job in this
repository that sets `fetch-depth: 0`.

**Command.** `uv run epppsynth scan --history`

**What the script cannot check.** A secret that does not look like one — an unprefixed API key, a
password in prose, a credential inside a base64 blob or a binary file. It cannot tell a revoked
token from a live one, and **removing a secret from the tree does not remove it from the history**:
an unreachable object is not a deleted one. A finding here means rotate first, then rewrite.

---

## Item 2 — PHI-shaped patterns, across tracked files and fixtures

**What is checked.** Medical-record-number-shaped digit runs, dates of birth, labelled NPIs,
US social-security-number shapes, telephone shapes, email addresses other than the project's own
published contact, and street-address fragments — across every tracked file. Plus the D-36 rule:
every evaluation-scenario fixture carries a *no real person* attestation. **No scenarios exist yet**;
the check runs over an empty set and becomes live at EP-25.

Three matches are accounted for rather than reported, each mechanically and each printed in the scan
summary: an all-digit abbreviated git object id that `git rev-parse` resolves in this repository (a
run git cannot resolve stays a finding); a `size =` value in the machine-generated resolver lockfile;
and the one email address this repository already publishes in its own commit metadata (owner ruling
OD-7).

**Command.** `uv run epppsynth scan`

**What the script cannot check.** Whether a fictional scenario is *actually* fictional. A composite
built from remembered real encounters is PHI-shaped in no way a regex can see, and it is the failure
mode `GOVERNANCE.md` §5 and D-36 exist to prevent. The attestation is a human statement; the scanner
only checks that somebody made it.

---

## Item 3 — Protected text

**What is checked.** Three things.

1. **No corpus path in any commit.** `git log --all --diff-filter=A --name-only` must show no path
   under `source material/` other than its `README.md`. This is EP-0's one-time history assertion,
   now automated.
2. **The D-74 quotation budget** — 25 words per quote, 150 per source — counted over every tracked
   markdown file outside `epppsynth/tests/`. The test tree is outside the input set by **scope, not
   by exemption**: it holds EP-5's deliberately over-budget fixture, whose job is to make the counter
   fail, and a waiver inside the set would be indistinguishable from a real one.
3. **No tracked chapter-title sequence** — three or more title-shaped strings adjacent to a chapter
   ordinal, in reading order, within forty lines. That is how a source's outline reconstructs itself.
   It is the pattern EP-2 found in `tools/epub_to_md_pipeline.py`, that owner ruling OD-6 removed on
   2026-08-31 by moving the spine to untracked local configuration, and that this check exists to
   stop returning by another route.

The `ledger` scanner also reports under this item: every eight-word sequence shared between
`epppsynth/DECISIONS.md` and any file under `.local/` must fall inside a published decision entry,
an addendum, or the index block (D-2, owner ruling OD-3). It reads `.local/` and reports **only
positions and counts inside the already-public file** — never the matched text, never a line of
private content, never the name of a private file. It is local and pre-commit only: `.local/` does
not exist on a CI runner, so CI reports `skipped - no ledger present` and counts it as skipped,
**never as passed**.

**Command.** `uv run epppsynth scan --history`

**What the script cannot check.** Whether an authored paraphrase is close enough to its source to be
a derivative work. Word budgets catch quotation; they do not catch close paraphrase, and close
paraphrase is the rights failure mode that matters most. A human reads the authored prose against
the source. Nor can it tell a shared eight-word passage that *is* a settled decision from one that is
deliberation someone pasted in — it can only tell you where the passage sits.

---

## Item 4 — Local paths and machine identifiers

**What is checked.** Windows user-profile paths, UNC paths, absolute drive paths other than the two
declared roots, and the operating account's name and the machine's hostname, both read from the
environment **at run time** so that no tracked file has to carry them for the check to exist.

Separately, the two declared roots — `C:\epppindex` and `C:\epppmodels` — are **permitted in
documentation** and forbidden in code, tests, fixtures and configuration defaults. They are
deliberately public: D-30 and D-51 declare them, and `PRIVACY.md`, `DECISIONS.md` and the roadmap
name them on purpose. In a `.py` file, a fixture or a workflow they are a data path, and a data path
is how an index reaches a published artifact. The check is scoped by file type accordingly, and the
distinction is written down here so it survives.

**Command.** `uv run epppsynth scan`

**What the script cannot check.** An identifier nobody declared: a second machine's hostname, a
former account name, a colleague's name in a comment, or a path inside a screenshot. It reads the
environment of the machine it runs on and nothing else.

---

## Item 5 — Screenshots · **human, no script**

**What is checked.** Nothing automatically. Every image about to be published is **re-opened and
read**, and each of the following is confirmed by eye:

- [ ] EXIF and XMP metadata stripped (camera, software, timestamps, any path).
- [ ] No source pane visible, and no verbatim span from the local index anywhere in frame.
- [ ] No local path in a title bar, a breadcrumb, a terminal prompt, a tab, or a file dialog.
- [ ] No notification toast, no calendar, no email preview, no other window.
- [ ] No account name, hostname, or machine identifier in any chrome.
- [ ] Any scenario shown is manifestly fictional and carries its attestation.

**Why there is no script.** No screenshots exist yet. Automating this is parked until the P5 UI
briefs start producing them; automating it before then would be a check with no input, which is a
check nobody maintains. Note also that an image is not text: the scanners in items 1–4 read tracked
files, and a path rendered as pixels is invisible to every one of them.

---

## Item 6 — Licence conformance

**What is checked.** Every tracked file maps to exactly one licence under `REUSE.toml`; no file is
doubly matched; no annotation pattern matches nothing; every `.py` file's SPDX header agrees with the
table that covers it (`precedence = "aggregate"` means a drifted header silently wins); every
concept's `source_id` resolves to a row in the rights record; and no concept carries a verbatim field
sourced from a non-redistributable source (D-10, D-23, D-28, D-50, D-62).

**Command.** `uv run epppsynth scan` · second opinion, if installed: `reuse lint`

**What the script cannot check.** Whether a rights row is *true*. `reuse_class` and
`redistributable` are statements somebody made about a source's terms; two source families are still
held as `reference-only-pending-rights-check` for exactly that reason. The scanner checks that the
statement exists and is internally consistent, not that anyone verified it.

---

## Item 7 — Every public claim compared against its evidence · **human, no script**

**What is checked automatically.** Two narrow mechanical parts:

- the README badge parses against EP-2's contract, resolves to its mapped evidence file, and that
  file exists with **every** checkbox ticked (D-12, D-59);
- the retired modality stem appears in no tracked file outside the three-entry, owner-ratified
  exemption table (D-4, owner ruling OD-10).

**What is checked by a human, and is the substance of this item.** `README.md`, the badge, the
`prime` portfolio card and `CITATION.cff` all say the same thing, and **none says more than the
evidence supports**. Read them side by side and confirm:

- [ ] No claim of efficacy, safety, adoption, validation, approval, or external review.
- [ ] Review status stated as author-only, wherever review is mentioned.
- [ ] Present tense used only for what exists today; everything else carries a `planned (EP-n)`
      marker and is **not** rendered as a link.
- [ ] The status line and the not-a-risk-detector line are byte-identical to their approved text.
- [ ] Excluded modes described as excluded with named preconditions — never as "deferred" (D-61).
- [ ] Nothing implies communication preparation is inherently benign (`GOVERNANCE.md` §11).
- [ ] If a stop-criterion result is reported anywhere, it carries its confidence interval and the
      fixed power-limit sentence.

**Why there is no script for the substance.** A claim is a sentence in context. A linter can check a
badge string against a file; it cannot read "designed for clinicians" and know whether the evidence
file supports it. Banned-phrase and copy-deck linting arrives at EP-39 and will narrow this, never
close it.

---

## Signature block

The packet is not complete until this is filled in **by a person**, with a real date and the commit
hash the review was performed against. A green CI run is not a substitute, and this document says so
because a checklist that can be satisfied by a machine is a checklist that will be.

| Field | Value |
|---|---|
| Date | |
| Commit hash reviewed | |
| Reviewed by (name) | |
| Publication this packet covers | |
| Items 1, 2, 3, 4, 6, 7-mechanical — `epppsynth scan --history` exit code | |
| Item 5 — screenshots re-opened and read | |
| Item 7 — public claims compared against evidence | |
| Second-opinion secret scanner run, if any (tool and version) | |
| Findings accepted with a reason, if any | |

Completed packets are recorded in `release-evidence/<tag>/` at a tag (EP-50) and kept with the
change they cleared otherwise.
