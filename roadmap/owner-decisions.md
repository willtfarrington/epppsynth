# epppsynth — pending owner decisions

Rulings that executed briefs raised and **could not make for themselves**. Each one is either a
judgement a brief deliberately left to the project owner, or a drift between a published decision and
what was observed on the ground.

This file is a **register, not a decision log**. Nothing here is settled until it lands where the
"Ruling lands in" line says — a dated `> **Addendum (date, EP-n).**` under the decision it refines in
[`../epppsynth/DECISIONS.md`](../epppsynth/DECISIONS.md), a platform action, or a confirmation
recorded at the next phase re-plan. Rows are ticked ☑ with the date and the place the ruling landed;
nothing is deleted.

Opened **2026-08-31** from the completion notes of EP-1 … EP-4. EP-0 is not surveyed here.

---

## P0 — from EP-1 … EP-4

### Summary

| # | Ruling needed | Raised by | Class | Ruling lands in | Done |
|---|---|---|---|---|---|
| OD-1 | Projects is **on**; D-76 says off | EP-4 dev. 3 | drift | platform setting, or addendum under D-76 | ◐ ruled (a) 2026-08-31 — **platform action outstanding** |
| OD-2 | Does the authored *"What it does not know"* block match the approved draft? | EP-3 dev. 1 | confirmation | addendum under D-69 | ☐ **open — owner only** |
| OD-3 | Is a settled decision statement shared with the private ledger a leak? | EP-2 dev. 5 | ruling | addendum under D-2; EP-6 implements | ☑ 2026-08-31 — addendum under D-2; EP-6 §1.9 |
| OD-4 | Escalation-panel invariance is **per mode**, not global | EP-3 dev. 4 | refinement | addendum under D-57 | ☑ 2026-08-31 — addendum under D-57; EP-44 |
| OD-5 | Should the escalation-panel copy be settled as a decision? | EP-3 handoff | ruling | addendum under D-18 / D-57 at EP-8 | ☑ 2026-08-31 — addendum under D-18 (landed early); EP-44 |
| OD-6 | Is the tracked chapter-title table a **live** rights exposure? | EP-2 parked | ruling | addendum under D-10 / D-74; EP-5, EP-6, EP-22 | ☑ 2026-08-31 — **live**; addendum under D-74; spine externalised; EP-6 §1.3 + §1.8, EP-22 |
| OD-7 | Dedicated contact alias, or keep the git author address? | EP-4 dev. 4 | ruling | `CODE_OF_CONDUCT.md`, `SECURITY.md`, the test constant | ☑ 2026-08-31 — keep; no file changed |
| OD-8 | Confirm the issue form renders and its two checkboxes behave | EP-4 dev. 2 | verification | observation recorded at EP-8 | ☐ ruled self-correcting 2026-08-31 — **verification outstanding, needs the push** |
| OD-9 | Dependabot / renovate for pinned action SHAs vs D-34's no-PR posture | EP-1 parked | ruling | addendum under D-34, or a re-plan note under D-42 | ☑ 2026-08-31 — (a) no automation; EP-8 re-plan note under D-42 |
| OD-10 | Confirm the four-entry modality-sweep exemption list | EP-2 dev. 4 | confirmation | EP-6's scanner definition | ☑ 2026-08-31 — confirmed as **three** entries; EP-6 §1.8 |
| OD-11 | Confirm the hazard register stays in `DESIGN.md` §14 alone | EP-2 dev. 3 | confirmation | EP-8 re-plan note | ☑ 2026-08-31 — confirmed; EP-8 re-plan note |
| OD-12 | Confirm the banned-phrase ban's documentation carve-out | EP-3 dev. 7 | confirmation | EP-39's lint specification | ☑ 2026-08-31 — confirmed; EP-39 scope sketch item 3 |
| OD-13 | Owner-judgement acceptance criteria, offered and unruled (× 5) | EP-1 … EP-4 | confirmation | EP-8 re-plan note | ☑ 2026-08-31 — four pass, EP-2 #10 **fails**; EP-8 re-plan note |

**Status at 2026-08-31.** Ten of thirteen ruled and landed. Three are not: **OD-1** is ruled but the
platform setting has not been changed, **OD-2** can be closed only by the owner, and **OD-8** cannot
be observed until the six unpushed commits reach the remote. `◐` means *ruled, not yet landed*; the
row is not ☑ until the action exists, because a ruling recorded as done and never performed is the
drift this register exists to catch.

**Class.** *drift* — a published decision and the observed world disagree. *ruling* — a choice only
the owner can make. *refinement* — a decision is right but narrower or broader than written.
*confirmation* — a brief made the call and needs it ratified. *verification* — an observation the
session could not make.

---

### OD-1 — Projects is enabled, contrary to D-76

**Observed 2026-08-31 (EP-4).** The platform reports `has_issues: true`, `has_discussions: false`,
`has_wiki: false`, **`has_projects: true`**, `private: false`. D-76 settles Discussions, Wiki **and**
Projects as off. Three of four match; the fourth does not. EP-4 explicitly changes no repository
setting, so nothing was touched.

**At stake.** A permanent divergence between a published decision and the platform it describes — the
class of drift the badge scheme (D-59) exists to prevent. Nothing leaks and no claim is overstated
either way.

**Options.** (a) Turn Projects off, matching D-76 as written. (b) Keep it on and append a dated
addendum under D-76 stating why.

**Recommended.** (a) — nothing in the roadmap uses a project board, and D-76 is otherwise satisfied.

**Ruling lands in:** the platform setting, or an addendum under D-76. Either way, EP-8 re-observes
the four flags and records them.

### OD-2 — the *"What it does not know"* block was authored, not copied

**Observed 2026-08-31 (EP-3).** D-69 records that four public blocks — intended use, excluded uses,
*what it does not know*, and the status line — ship as drafted. Three were reproducible from public
files and are byte-identical to EP-2's recorded baselines (status line **84 bytes**, the
not-a-risk-detector pair **103 bytes**). The fourth exists in no public artifact: a sweep of every
tracked file found the phrase only in pointers, never the block itself. EP-3 authored it from D-8,
D-14, D-18, D-25, D-63 and D-79 rather than read the approved draft, whose only remaining location is
private planning state a session may not open.

**At stake.** This is the one block of approved public wording whose shipped text has never been
compared against what was approved, and it is public-facing safety copy.

**Action.** Diff `SAFETY.md`'s *what it does not know* section against the approved draft, then either
confirm it or supply the approved wording. Only the owner can do this.

**Ruling lands in:** an addendum under D-69 recording that the block was authored at EP-3 and either
matches or has been replaced.

### OD-3 — shared text between `DECISIONS.md` and the private ledger

**Observed 2026-08-31 (EP-2).** EP-2's step 11 required that **no** eight-word sequence be shared
between `epppsynth/DECISIONS.md` and any private planning file. Observed instead: **124 shared
passages, 19.7 % of `DECISIONS.md` by word count, longest 42 words** — and **zero** of them outside a
published decision entry or the index block, distributed evenly across all thirteen decision sections
(3–20 passages each), which is the signature of decision statements appearing in both files rather
than of deliberation being pasted in.

The check as written is unsatisfiable by construction: the ledger records each decision in the words
it was settled in, and D-2 requires publishing those settled decisions. The measurement ran as a
script reporting only positions and counts inside the already-public file; no private content entered
the session or any public file.

**At stake.** EP-6 must implement one of these two checks, and they cannot both hold.

**Options.** (a) Ratify the refined invariant — *every shared passage falls inside a published
decision entry or the index block, never in the surrounding prose* — and have EP-6 implement that.
(b) Keep the literal check and accept that it fails permanently.

**Recommended.** (a). The refined form detects ledger-copying; the literal form detects the decision
log doing its job.

**Ruling lands in:** an addendum under D-2, cited by EP-6's scanner.

### OD-4 — escalation-panel invariance is per mode

**Observed 2026-08-31 (EP-3).** D-57 and `GOVERNANCE.md` §4.5 state the escalation panel renders
byte-identically **on every response**. `DESIGN.md` §14 **R-40** narrows this: mode (c)'s fixed
heading speaks about a third party while its operator *is* the subject, so mode (c) ships its own
constant panel addressed to the reader. `SAFETY.md` §9 publishes the narrowed form and names R-40,
rather than a global claim EP-44 would have to contradict.

**At stake.** A published invariant that EP-44 will implement, stated one way in governance and
another in the charter. The narrow form is almost certainly right; it is not yet recorded as a
decision.

**Recommended.** Append a dated addendum under D-57: invariance is **per mode** — byte-identical
across every response *within* a mode, with mode (c)'s panel a distinct constant.

**Ruling lands in:** an addendum under D-57. `GOVERNANCE.md` §4.5 then wants its own dated addendum,
since that file is append-only too.

### OD-5 — should the escalation-panel copy be a decision, or charter text?

**Observed 2026-08-31 (EP-3).** D-18 fixes only *which* resources appear and D-57 only the heading.
The exact panel wording — including the `988` and `911` lines and the "outside the United States"
sentence — was **authored at EP-3** and now lives as `SAFETY.md` §9 prose. EP-44 will render it from
a constant.

**At stake.** Crisis-resource copy is the highest-consequence string in the product. As charter text
it can be changed by any brief that edits `SAFETY.md`; as a decision, changing it requires a dated
addendum.

**Options.** (a) Settle the copy as a dated addendum under D-18, making EP-44's constant a
transcription. (b) Leave it as charter text and let EP-44 own the constant.

**Recommended.** (a), at the EP-8 re-plan.

**Ruling lands in:** an addendum under D-18 (resources) or D-57 (rendering), at EP-8.

### OD-6 — the tracked chapter-title table in the ingest pipeline

**Observed 2026-08-31 (EP-2).** `tools/epub_to_md_pipeline.py` publishes a source book's title and
its **full chapter-title table** in a tracked, public file. That is the outline-reconstruction
pattern D-74 forbids for public citations and that `DESIGN.md` §6.1 Y-8 names as a rights-leakage
failure mode — currently guarded for the registry, not for `tools/`. Found by EP-2's step-10 sweep
and **not fixable inside EP-2**: the table is the pipeline's operative source spine, D-41 already
parks generalising it, and the pipeline moves into the package at EP-22. It is also why that file
carries a standing exemption from the modality sweep (OD-10).

**At stake.** Whether this is a **live** rights exposure requiring removal now, or a **latent** one
that EP-22 closes when it moves the spine into untracked local config.

**Options.** (a) Live — strip the spine to untracked config before EP-5, and have EP-6 treat a
tracked chapter-title sequence as a finding. (b) Latent — record the reasoning, scan for it at EP-6,
and let EP-22 close it.

**Recommended.** The EP-6 scanner rule either way, plus a ruling on whether the existing table comes
out now. The corpus rule (D-10) is one of the two that override any brief, which argues for not
waiting.

**Ruling lands in:** an addendum under D-10 or D-74, cited by EP-5, EP-6 and EP-22.

### OD-7 — the project contact address

**Observed 2026-08-31 (EP-4).** No project contact address existed anywhere in the repository, and
the Code of Conduct and `SECURITY.md` both require one. EP-4 used the address already public in this
repository's own commit metadata, so filling the placeholder disclosed nothing that publishing the
repository had not already disclosed. It appears twice: as the Covenant's enforcement contact, and as
the `SECURITY.md` fallback, where it is labelled as not a monitored security inbox and as strictly
worse than the private advisory path.

**At stake.** A personal address is now the published enforcement contact for a public repository.
EP-4's completion note names this as the one item in that brief the owner should overrule.

**Action.** Substitute a dedicated alias if one is wanted: a two-line change plus the `CONTACT`
constant in `epppsynth/tests/test_public_docs.py`.

**Ruling lands in:** the two documents and the test constant. No decision entry is needed unless the
address is to be fixed by decision.

### OD-8 — confirm the issue form renders

**Observed 2026-08-31 (EP-4).** Nothing was configured on the platform — `.github` contained
`workflows` only, and the issue-templates endpoint returned 404 — so there was nothing to compare the
committed file against. This is self-correcting: the platform reads issue forms **from**
`.github/ISSUE_TEMPLATE/`, so committing `discussion.yml` *is* configuring it, and it takes effect on
push.

Separately, the private advisory intake could not be observed rendering its form (an unauthenticated
fetch returns the sign-in page). The **setting** was verified through the platform API instead:
`private-vulnerability-reporting` → `{"enabled": true}`, observed 2026-08-31. The path is live; the
form was not seen, and the completion note says so rather than implying it was.

**Action.** After the next push, confirm the issue form renders and that its two required
acknowledgement checkboxes behave as intended.

**Ruling lands in:** an observation recorded at EP-8; no decision entry needed if it renders.

### OD-9 — Dependabot / renovate versus the no-PR posture

**Raised by EP-1 (parked).** CI pins two third-party actions to 40-character commit SHAs (D-42), and
`ADR-008` states pins are reviewed at each phase re-plan. Automating that review means a bot that
opens pull requests, which conflicts with **D-34** — no pull requests are accepted in v1.

**At stake.** Either the pins are reviewed by hand at each re-plan, or the no-PR posture acquires a
machine-shaped exception.

**Options.** (a) No automation; keep the manual re-plan review `ADR-008` already promises.
(b) Enable update automation and append an addendum under D-34 carving out bot pull requests.

**Recommended.** (a) at this scale — two pinned actions, reviewed at each of the remaining phase
re-plans.

**Ruling lands in:** an addendum under D-34 if automation is adopted; otherwise a re-plan note under
D-42.

### OD-10 — the modality-sweep exemption list

**Observed 2026-08-31 (EP-2).** The sweep for the retired modality term found six files. Four were
**reworded to broader terms**, so the disclaimer is strengthened rather than weakened:
`GOVERNANCE.md` §1 and §4.1 and `src/epppsynth/__init__.py` now read "not **therapy**", and
`DESIGN.md` §6.1 reads "a **therapeutic** framework". Two could not be cleared inside EP-2's scope.
The proposed standing exemption list, each entry with its reason:

| File | Reason |
|---|---|
| `epppsynth/DECISIONS.md` | D-4 records the retired expansion; the record must keep the word |
| `source material/README.md` | precautionary — swept and found to contain **no** occurrence |
| `roadmap/EP-2-canonical-docs.md` | self-referential: the brief quotes the token to specify the sweep |
| `tools/epub_to_md_pipeline.py` | exempt *for now*, with a reason — see OD-6 |

**Action.** Confirm the list, so EP-6 implements the sweep with a four-entry exemption table carrying
reasons rather than as a bare grep. The fourth entry expires when OD-6 is ruled.

**Ruling lands in:** EP-6's scanner definition, citing this row.

### OD-11 — one hazard register, in `DESIGN.md` §14

**Observed 2026-08-31 (EP-2).** In-scope item 2 asked `GOVERNANCE.md` to tabulate R-1 … R-41. It was
**not** moved. `DESIGN.md` §14 already is that table and declares itself the register; GOVERNANCE §13
already points at it and names the two highest-rated hazards. Restating 41 rows in a second file
creates two registers that drift — the failure the single-register rule exists to prevent. What the
brief wanted was verified in place instead: all 41 rows present, contiguous, every row naming both a
mitigating brief and a verifying gate.

**Action.** Confirm the single-register rule so no later brief re-opens it. GOVERNANCE §13 and
`tools/roadmap_check.py` (EP-8) already assume it.

**Ruling lands in:** an EP-8 re-plan note; no decision entry needed if confirmed as written.

### OD-12 — the banned-phrase ban's documentation carve-out

**Observed 2026-08-31 (EP-3).** `SAFETY.md` §10 publishes a list of phrases that must not appear in
output, in a document that necessarily contains all of them — unpublishable under its own rule. §10
therefore fixes the scope EP-39's lint must implement: the ban governs **authored content and
rendered output** — concept text, templates, copy deck, composed waypoints — and **not**
documentation that names a phrasing in order to forbid it, or that reports what a user typed. One
example in §8 was reworded where a banned token was incidental rather than necessary.

**At stake.** The difference between a lint EP-39 can ship and one that fails on its own
specification.

**Action.** Confirm the carve-out. Note that two of the file's 17 entries carry a `condition` field
and need matcher support rather than a plain grep.

**Ruling lands in:** EP-39's lint specification, citing this row.

### OD-13 — owner-judgement acceptance criteria, offered and unruled

Five acceptance criteria across the four briefs are marked *(judgement — the project owner)*. Each was
completed and offered for confirmation, and none has been ruled. They are collected here so they are
not silently inherited as passed.

| Brief | # | Criterion | What was offered |
|---|---|---|---|
| EP-1 | 10 | The workflow file reads end to end in one screen and its header states the no-model rule plainly | The header comment was observed present; readability is unruled |
| EP-2 | 6 | Every behaviour sentence in `README.md` and `DESIGN.md` is present-tense-and-true or carries a `planned (EP-n)` marker | **4 candidates, all ruled acceptable by the session**: two line-wrap artifacts where the marker fell on the next line, the not-a-risk-detector negative claim, and the badge parse contract |
| EP-2 | 10 | `CLAUDE.md` → `GOVERNANCE.md` → the index → the P0 table → one brief suffices to execute that brief | `CLAUDE.md` ≈ **850 tokens**; load-order items 1–4 ≈ **11.5k**, leaving ≈ 3.5k for a brief. **EP-8's `--context-budget` check will fail for at least EP-2 and EP-9 as the files now stand** |
| EP-3 | 12 | A clinician reading only `SAFETY.md` can state what the tool refuses, what would stop the build, and what evidence exists | §3, §6, §11 and §16 are the four sections that answer it |
| EP-4 | 2 | Every privacy promise names its mechanism and the brief that enforces it | `PRIVACY.md` §11: **14 rows**, 13 filling mechanism + brief + proof, and **one — row 14 — whose mechanism cell reads "no mechanism — disclosed, not closed"**. A test asserts that shape is the only permitted exception |

**Action.** Walk the five and tick them, or name what fails. EP-2 #10 carries a design consequence for
EP-8 whichever way it is ruled.

**Ruling lands in:** an EP-8 re-plan note recording the five verdicts and their date.

---

## Resolutions — 2026-08-31

Where each ruling landed, and what executing it turned up. Rows above are the index; this is the
record. Nothing above was deleted.

**OD-1 — ruled (a): Projects off.** Nothing in the roadmap uses a project board and D-76 is
otherwise satisfied, so the platform is brought to the decision rather than the decision to the
platform; no addendum under D-76 is written, because none is warranted when the decision stands as
written. **The platform action did not execute in this session** — the `PATCH` to the repository
settings was refused by the environment's permission layer, not by the platform. It is a
single call, and it is the whole of what remains:

```bash
gh api -X PATCH repos/willtfarrington/epppsynth -f has_projects=false
```

EP-8 re-observes all four flags plus `private-vulnerability-reporting` and records them with the
date, whether or not the call has been made by then.

**OD-2 — open.** Left deliberately unticked. `SAFETY.md` §4 is authored text standing where
approved text was recorded, and the comparison needs the approved draft, which lives only in private
planning state. The EP-8 brief carries the note; the ruling lands as a dated addendum under D-69.

**OD-3 — ruled (a): the refined invariant.** Landed as a dated addendum under **D-2**. The
invariant is now: a shared eight-word passage is a finding **only when it falls outside a published
decision entry or the index block**. EP-6 gains it as scanner **9**, specified to run as a script
that reports positions and counts inside the already-public file only, and to report *skipped — no
ledger present* in CI rather than a pass, because `.local/` does not exist on a runner. Its canary
is a synthetic pair of fixture files, so proving the check works never requires touching the real
ledger.

**OD-4 — ruled: invariance is per mode.** Landed as a dated addendum under **D-57**; EP-44's
context paragraph restated to match. **One correction to the register's own text:** it said
`GOVERNANCE.md` §4.5 would want its own addendum. Checked on 2026-08-31 — §4.5 states that the
compensating control is an *always-visible* escalation panel and makes **no** byte-identity claim,
so nothing there is narrowed by this ruling and no addendum was written. The global claim lived in
D-57 alone.

**OD-5 — ruled (a), and landed now rather than at EP-8.** Crisis-resource copy is the
highest-consequence string in the product, so the earlier protection was taken. The addendum under
**D-18** does **not** restate the words — a published copy and a rendered copy in two files are two
copies and they drift. It pins them: canonical location `SAFETY.md` §9, fixed at commit `7a5ecbb`,
with the extraction rule (strip one leading `> ` per line, join with LF, no trailing newline — 13
lines, 592 bytes UTF-8) and the SHA-256
`070d3915af29b80d1b7d1912b475efd541a165f82cd2210753585aac9f5ef37f`. EP-44 transcribes and asserts
equality against §9 live; a change to §9 without a further addendum is a failure, not an edit.

**OD-6 — ruled live, and closed.** The corpus rule (D-10) overrides any brief, which argued against
waiting for EP-22. Landed as a dated addendum under **D-74** and as the code change itself:
`tools/epub_to_md_pipeline.py` no longer contains the book title, the author, the source EPUB
filename or the chapter-title table. They load at run time from `tools/spine.local.json`
(gitignored), with `tools/spine.local.json.example` shipped carrying placeholder rows, on the
`escalation.local.toml` pattern of D-60; a missing config exits with a pointer to the example.
EP-6's protected-text scanner gains the general rule — a tracked chapter-title sequence is a finding
— so the pattern cannot return by another route, and EP-22 carries a note that it inherits an
already-external spine.

**OD-7 — ruled: keep the git-author address.** It is already public in this repository's own commit
metadata, so publishing it disclosed nothing that publishing the repository had not. No document and
no test constant changed. Recorded here rather than as a decision entry, so that a later session
reads it as a ruling rather than as an oversight.

**OD-8 — ruled self-correcting; verification outstanding.** Confirmed on 2026-08-31 that local
`main` is **six commits ahead of `origin`**: EP-2, EP-3 and EP-4 are unpushed, which is why
`.github/ISSUE_TEMPLATE/discussion.yml` is absent from the platform and the issue-templates endpoint
still returns 404. Pushing *is* configuring it. EP-8 confirms the form renders and that its two
required acknowledgement checkboxes behave.

**OD-9 — ruled (a): no automation.** Two pinned actions do not justify a bot that opens pull
requests against D-34's no-PR posture. No addendum under D-34 was written, because no carve-out was
adopted; the re-plan note under **D-42** lives in the EP-8 brief and makes the by-hand review
`ADR-008` promises an explicit EP-8 deliverable rather than a standing intention.

**OD-10 — confirmed, as a three-entry table, and the sweep widened.** Landed in EP-6's scanner
definition as check **8**, with reasons attached. Two of the four proposed rows are deliberately
absent: `source material/README.md` was precautionary and contains no occurrence — an exemption for
a file that does not need one is a hole waiting for a future edit — and
`tools/epub_to_md_pipeline.py`'s exemption **expired** when OD-6 was ruled live. **One new
observation.** EP-2 swept for the exact token `psychotherapy`; the sweep is specified in EP-6 as a
stem sweep for `psychotherap`, which surfaces one file the exact-token grep could not match:
`roadmap/EP-12-seed-givens.md` line 122, *"mid-twentieth-century Western **psychotherapeutic**
idiom"*. It is left for EP-6 to resolve **by rewording to the broader term**, on EP-2's own
precedent — not by a fourth exemption, which would need a further ruling.

**OD-11 — confirmed.** The single-register rule stands: `DESIGN.md` §14 is the hazard register,
GOVERNANCE §13 points at it, and nothing restates it. Recorded as an EP-8 re-plan note; no decision
entry needed and none written.

**OD-12 — confirmed, with a count correction.** Landed in EP-39's scope sketch. The carve-out is
specified to work by **scope, not by exemption**: documentation is outside the lint's input set
rather than inside it with a waiver, so nothing about `SAFETY.md` §10 is allowlisted because it is
never scanned. **The register said two of the 17 entries carry a `condition` field; there are
three** — `bp-010` (**overcome**), `bp-014` (**goals-of-care conversation**) and `bp-017` (**the
evidence shows**), the last of which is a citation-binding check rather than a text match and so
could never have been a grep. EP-39 now names all three, requires a matcher per `condition` kind,
and requires the lint to **fail closed** on a `condition` value its matcher does not recognise.

**OD-13 — walked and ruled: four pass, one fails.** Verdicts and their bases are recorded in the
EP-8 re-plan note. The one that does not pass is **EP-2 #10**, the context budget: items 1–4 of the
load order come to ≈ 11.5k tokens against a ~15k ceiling, leaving ≈ 3.5k for a brief, and
`--context-budget` will fail for at least EP-2 and EP-9. It is ruled a **known finding accepted
into EP-8**, not a pass — EP-8 is told rather than left to discover it, and is directed to resolve
the overflow by shrinking load-order item 3 or 4, never by raising the ceiling and never by
trimming a brief below the self-containment the load order exists to guarantee.

---

## Not owner decisions — recorded so they are not lost

Raised by the same completion notes but directed at a later brief rather than at the owner. Listed
once here; they are the re-plan's business, not this register's.

- **EP-8** — decide whether `PRIVACY.md` §11's status column becomes tool-checked by
  `roadmap_check.py` rather than hand-maintained. Hand-maintained is the failure mode the badge
  scheme was designed to avoid.
- **EP-8** — decide whether to pin the `uv` *binary* version in CI. The action installs the latest
  uv; `uv.lock` guards the resolution either way, so this is a reproducibility nicety, not a hole.
- **EP-8** — note that `SAFETY.md` is **not** in the load order; the briefs that need it (EP-20,
  EP-26, EP-39, EP-44) name it as a step-6 source file.
- **EP-8** — EP-2's acceptance 3 expects 78 decisions; there are **79** (D-79 postdates that brief).
  The check was executed as the invariant it encodes — index rows == full entries == actual count —
  and passed. The stale figure is historical and is not edited.
- **EP-6** — inherits three testable assertions from `SECURITY.md`: no runtime credentials in the
  tree **or the full history**, no secret-shaped strings, and the identity sweep, already implemented
  over five files and wanting widening to all tracked files. Its pattern block carries a
  `leak-scan-allow: rule-definition` marker the scanner must honour.
- **EP-17 / EP-40 / EP-41 / EP-42 / EP-46 / EP-47** — each owns named rows of the `PRIVACY.md` §11
  enforcement register and must move its status column off *not built*.
