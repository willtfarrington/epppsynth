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
| OD-1 | Projects is **on**; D-76 says off | EP-4 dev. 3 | drift | platform setting, or addendum under D-76 | ☑ 2026-09-01 — **performed by the owner**; all four flags re-observed and matching |
| OD-2 | Does the authored *"What it does not know"* block match the approved draft? | EP-3 dev. 1 | confirmation | addendum under D-69 | ☐ **open — owner only** |
| OD-3 | Is a settled decision statement shared with the private ledger a leak? | EP-2 dev. 5 | ruling | addendum under D-2; EP-6 implements | ☑ 2026-08-31 — addendum under D-2; EP-6 §1.9 |
| OD-4 | Escalation-panel invariance is **per mode**, not global | EP-3 dev. 4 | refinement | addendum under D-57 | ☑ 2026-08-31 — addendum under D-57; EP-44 |
| OD-5 | Should the escalation-panel copy be settled as a decision? | EP-3 handoff | ruling | addendum under D-18 / D-57 at EP-8 | ☑ 2026-08-31 — addendum under D-18 (landed early); EP-44 |
| OD-6 | Is the tracked chapter-title table a **live** rights exposure? | EP-2 parked | ruling | addendum under D-10 / D-74; EP-5, EP-6, EP-22 | ☑ 2026-08-31 — **live**; addendum under D-74; spine externalised; EP-6 §1.3 + §1.8, EP-22 |
| OD-7 | Dedicated contact alias, or keep the git author address? | EP-4 dev. 4 | ruling | `CODE_OF_CONDUCT.md`, `SECURITY.md`, the test constant | ☑ 2026-08-31 — keep; no file changed |
| OD-8 | Confirm the issue form renders and its two checkboxes behave | EP-4 dev. 2 | verification | observation recorded at EP-8 | ☐ pushed 2026-09-01; **form still not observed** — see the EP-8 note |
| OD-9 | Dependabot / renovate for pinned action SHAs vs D-34's no-PR posture | EP-1 parked | ruling | addendum under D-34, or a re-plan note under D-42 | ☑ 2026-08-31 — (a) no automation; **first by-hand pin review performed 2026-09-01 at EP-8, one finding — OD-17** |
| OD-10 | Confirm the four-entry modality-sweep exemption list | EP-2 dev. 4 | confirmation | EP-6's scanner definition | ☑ 2026-08-31 — confirmed as **three** entries; EP-6 §1.8 |
| OD-11 | Confirm the hazard register stays in `DESIGN.md` §14 alone | EP-2 dev. 3 | confirmation | EP-8 re-plan note | ☑ 2026-08-31 — confirmed; EP-8 re-plan note |
| OD-12 | Confirm the banned-phrase ban's documentation carve-out | EP-3 dev. 7 | confirmation | EP-39's lint specification | ☑ 2026-08-31 — confirmed; EP-39 scope sketch item 3 |
| OD-13 | Owner-judgement acceptance criteria, offered and unruled (× 5) | EP-1 … EP-4 | confirmation | EP-8 re-plan note | ☑ 2026-08-31 — four pass, EP-2 #10 **fails**; the overflow was resolved at EP-8 by shrinking load-order item 3 |
| OD-14 | Ratify the `bibliographic-identity` refinement to the OD-10 modality sweep | EP-6 dev. 1 | confirmation | EP-6's scanner definition; a further ruling if overturned | ☑ 2026-09-01 — ratified as implemented; EP-6 §1.8, `ADR-008` |
| OD-15 | Must a completion note name the CI run it claims to be green on? | EP-7 dev. | ruling | `CLAUDE.md` §Committing; `roadmap/README.md` Definition of Done | ☑ 2026-09-01 — yes, as a linked id; both files updated |
| OD-16 | The load order's fixed overhead leaves the tightest brief 46 tokens of headroom | EP-8 | ruling | the remedy, named in advance, in `roadmap_check.py` and the roadmap README | ☑ 2026-09-01 — accept and **name the trigger**: the remedy is to split the brief |
| OD-17 | `astral-sh/setup-uv` is pinned to v9.0.0; v10.0.1 is current | EP-8 | ruling | `ci.yml` and `ADR-008`, in a commit of its own | ☑ 2026-09-01 — ruled **bump** and **performed**, after EP-8's run; `ADR-008` amendment |
| OD-18 | Normalise the deliberate GiB/GB transcription, or keep it | EP-8 | ruling | an addendum under D-78 | ☑ 2026-09-01 — **keep**; each unit matches what it measures |

**Status at 2026-08-31.** Ten of thirteen ruled and landed. Three are not: **OD-1** is ruled but the
platform setting has not been changed, **OD-2** can be closed only by the owner, and **OD-8** cannot
be observed until the six unpushed commits reach the remote. `◐` means *ruled, not yet landed*; the
row is not ☑ until the action exists, because a ruling recorded as done and never performed is the
drift this register exists to catch.

> **Added 2026-08-31 (EP-6).** **OD-14** was opened while executing EP-6 and is not counted in the paragraph above, which records the position before it. It is a confirmation, not a blocker: the refinement is implemented and the scanner runs green with it, so a ruling either ratifies what is already there or directs a change.

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
observation.** EP-2 swept for the exact token `psychotherapy`; the sweep is specified in EP-6 as a  <!-- leak-scan-allow: rule-definition -->
stem sweep for `psychotherap`, which surfaces one file the exact-token grep could not match:  <!-- leak-scan-allow: rule-definition -->
`roadmap/EP-12-seed-givens.md` line 122, *"mid-twentieth-century Western **psychotherapeutic**  <!-- leak-scan-allow: rule-definition -->
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

### OD-14 — bibliographic identity in the retired-modality sweep

**Class:** confirmation · **Raised by:** EP-6 · **Opened:** 2026-08-31

**Observed while executing EP-6.** OD-10 fixed the modality-sweep exemption table at three entries
and named exactly one occurrence left to resolve: `roadmap/EP-12-seed-givens.md` line 122, resolved
here by rewording to the broader term, as ruled. The stem sweep run against the tree as it stands
surfaces **seventeen more**, in twelve files, none of which OD-10 could have seen: they arrived with
**EP-5**, which landed the source rights record on the same day the ruling was written. Every one of
them is the source identifier `yalom-existential-` ‹stem› `-1980` or the citation title it is built
from — in `CITATION.cff`, `epppsynth/registry/sources.yaml`, the generated
`epppsynth/docs/rights.md`, one docstring, four test fixtures and one test module.

**Why this is not a fourth exemption row.** D-4 retires an expansion of *this project's own name*.
D-74 requires that every source carry a citable record. A book's title is bibliographic identity and
cannot be reworded; a rights record with an unnameable source is not a rights record. The two rules
only appear to collide.

**What EP-6 implemented, for ratification.** A rule refinement, not a path exemption: an occurrence
of the stem is skipped **only** when it falls inside a `source_id` or a citation `title` that
`epppsynth/registry/sources.yaml` declares. It is derived from an owner-ratified data file rather
than from a session's judgement, it is inventoried in every scan summary under the reason
`bibliographic-identity`, and it fails closed — an occurrence anywhere else, in any file, is still a
finding. The three-entry table is untouched and still has three entries, guarded by a unit test.

**The ruling needed.** Ratify the refinement, or direct a different resolution — the alternatives
considered and rejected were: a fourth exemption row (needs a ruling anyway, and exempts whole files
rather than the citation); renaming the `source_id` to drop the stem (leaves the citation title,
which cannot be renamed); and leaving check 8 red (the brief's acceptance requires a green clean
run). Recorded in `ADR-008`'s EP-6 amendment as an accounted-for match rather than as an allowlist.

---

### OD-15 — a completion note that claims CI must name the run

**Class:** ruling · **Raised by:** EP-7 · **Opened:** 2026-09-01

**Observed while executing EP-7.** The brief's acceptance criterion 13 reads *"CI green"*. The two
commits landed, every command CI runs was green locally, and `ci.yml` was confirmed to reference
neither storage root — but nothing had been pushed, so no CI run existed. The completion note as
first written claimed the suite was green **locally**, and the session said plainly that CI had not
run. On the push, the run went green and its id existed in exactly one place: a terminal that was
about to close.

**Why this is not new.** EP-6 already recorded run ids as linked URLs, because EP-6's own acceptance
table happened to carry a `CI run URL` column. One brief's wording produced the right behaviour by
accident, and the next brief would have had to think of it again.

**The ruling needed.** Whether a completion note must name the CI run it claims to be green on, and
what a brief's row shows when the work is committed but not pushed. The alternatives are: leave it to
each brief's acceptance wording (the status quo, which is how EP-7 nearly lost its run id); require
the push as part of Done (which would override *commit or push only when asked*); or require only
that the **claim** carry its evidence.

---

## Resolutions — 2026-09-01

**OD-14 — ratified as implemented.** The refinement stands, and it lands where OD-10 landed: in
EP-6's scanner definition, recorded in the `ADR-008` amendment. No `DECISIONS.md` addendum is
written, because none is warranted — D-4 is unchanged and D-74 is unchanged; what was wrong was the
sweep's reading of them, and the sweep is not a decision.

**What is ratified, stated so a later session cannot widen it.** An occurrence of the retired
modality stem is skipped **only** when it falls inside a string that
`epppsynth/registry/sources.yaml` declares as a `source_id` or as a citation `title`. Not a file, not
a directory, not a pattern, not a line. Move the citation and the skip moves with it; delete the row
from the rights record and every occurrence that depended on it becomes a finding on the next run.
The exemption is derived from an owner-ratified data file, and that derivation is the whole of its
authority.

**Why this and not a fourth exemption row.** D-4 retires an expansion of *this project's own name*.
D-74 requires that every source carry a citable record, and a book's title is bibliographic identity
that cannot be reworded. The two rules never actually collided; the sweep did. A fourth row would
have exempted twelve whole files — including `CITATION.cff`, the generated rights table and four
fixtures — for the sake of one string in each, which is a far wider hole than the one it closed, and
it would have needed this ruling anyway.

**What stays fixed.** The OD-10 exemption table still has **exactly three** entries and still grows
only by a further owner ruling; a unit test fails on a fourth. This ratification adds nothing to it.
The three allowlists remain separately counted and none may reach another's scope.

**What would reopen this.** A source whose `source_id` or title carries the stem *and* which is not
a real bibliographic record — a placeholder, a fixture row, or an invented identifier added to
`sources.yaml` to buy a skip. That is a rights-record defect first and a sweep defect second, and it
is caught by the `rights` check before the modality check ever sees it.

**OD-15 — yes, as a linked id.** A completion note may not claim CI green without naming the run.
Where the work is pushed, the run is recorded in a third commit,
`docs(roadmap): record EP-n CI run`. Where it is not pushed, the note says so and the row stays `◐` —
*done but not landed* — until the run exists. Recording the id costs one line and keeps the brief
from claiming CI on a run nobody can find.

**Where it lands.** `CLAUDE.md` §Committing and `roadmap/README.md` — the conventions paragraph and
the Definition of Done. No `DECISIONS.md` addendum is written: D-42 settles what CI *is*, and this
settles how a brief cites it, which is a session convention rather than an architecture decision. It
is the same principle as D-59 (a badge that resolves to an evidence file) and as the `◐` note under
the P0 table — *a brief recorded as complete on evidence that does not yet exist is the drift the
roadmap exists to catch* — applied to the one artifact that is generated **after** the commits rather
than before.

**Scope, stated so a later session cannot widen it.** This governs what a completion note may
**claim**. It does **not** make pushing part of Done and it does not override *commit or push only
when asked*: an unpushed brief is finishable, it simply does not get to assert a green CI run, and
its row shows `◐`. Nothing is retrospective — EP-0 … EP-5 are closed and are not reopened, and
**EP-7's own note names its run as a bare id rather than a link**, which stays as written, because an
executed brief is appended to and never edited. The linked form applies from EP-8.

**For EP-8.** `tools/roadmap_check.py` can make the tie mechanical rather than remembered: a
completion note containing a CI claim must carry a run link, and a `☑` row whose brief names CI in
its acceptance must have one. A tie to evidence is only real if the tie is mechanical.

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

---

## P0 re-plan — EP-8, 2026-09-01

The re-plan discharges the obligations the 2026-08-31 rulings handed it, re-observes the two that
could not be observed then, and opens three new entries. Every observation below is what was
**seen** on 2026-09-01, not what was expected.

### Obligations discharged

**OD-9 — the by-hand pin review, performed.** OD-9 ruled out update automation and made the
by-hand review `ADR-008` promises the compensating control. A review promised at every re-plan and
performed at none is not a control, so here is the first one, in full.

| Action | Pin in `ci.yml` | Resolves to | Latest upstream release | Finding |
|---|---|---|---|---|
| `actions/checkout` | `3d3c42e5aac5ba805825da76410c181273ba90b1` | tag `v7.0.1` | **v7.0.1** (2026-07-20) | none — current |
| `astral-sh/setup-uv` | `c771a70e6277c0a99b617c7a806ffedaca235ff9` | tag `v9.0.0` | **v10.0.1** (2026-08-14) | **one major version behind** — OD-17 |

Both pins were confirmed to be the commit the named tag points at, so neither comment is decoration.
The obligation is **handed forward to EP-16**, the P1 re-plan, and to every phase re-plan after it.

**OD-11 — one hazard register, recorded as ruled.** `tools/roadmap_check.py --hazards` reads
`epppsynth/DESIGN.md` §14 and nothing else. It reports 41 hazards, R-1 … R-41, contiguous, each
naming a mitigating brief that exists and a verifying gate. No second register was created and none
should be.

**OD-13 — the five verdicts, recorded, and the one failure resolved.** The four passes stand as
ruled on 2026-08-31. **EP-2 #10**, the context budget, was ruled a known finding accepted into
EP-8 with a directed remedy: shrink load-order item 3 or 4, never the ceiling and never a brief's
self-containment. It was resolved by compressing item 3 — the `DECISIONS.md` index block's
`Decides` column, from an average of 84 characters to an average of 55 — which recovered **623
tokens for every session**, not just for the briefs that were over. Every brief in the roadmap now
fits. The observed figures differ from the ruling's estimate and the difference is recorded rather
than smoothed: the ruling put items 1–4 at ≈ 11.5k tokens; the tool measures them at 8.9k–9.0k
under a stated 4-characters-per-token approximation. Only **EP-11** was ever over, at 15,577
against a 15,000 ceiling — not EP-2 and EP-9, which the ruling predicted would fail. What the
ruling got right is the shape: the load order was over its own ceiling, and the fix belonged in
item 3.

**OD-5 — recorded and closed.** Landed early, on 2026-08-31, as an addendum under D-18. The
register expected it here; EP-8 records it and moves on.

### Re-observations

**OD-1 — Projects is still on.** All four D-76 flags and the private-reporting path were
re-observed through the API on 2026-09-01:

| Setting | D-76 says | Observed | Verdict |
|---|---|---|---|
| `has_issues` | on | `true` | matches |
| `has_discussions` | off | `false` | matches |
| `has_wiki` | off | `false` | matches |
| `has_projects` | **off** | **`true`** | **diverges — the ruled platform action has not been performed** |
| private vulnerability reporting | on | `{"enabled": true}` | matches |

The ruling is unchanged and correct; what is missing is the click. The row stays `◐` and is handed
to the next re-plan, because a divergence that is re-observed and re-recorded without being fixed is
how a published decision quietly becomes false (D-59's whole reason for existing).

**OD-8 — pushed, and still not observed.** The commits reached the remote: `origin/main` is at
`638a0fe`, the default branch is `main`, and `.github/ISSUE_TEMPLATE/discussion.yml` is present in
that tree. The form is therefore where the platform reads issue forms from. It still could not be
seen rendering, by any path available to a session:

- the REST route `repos/{owner}/{repo}/issues/templates` returns 404 with a `documentation_url`
  pointing at *get-an-issue* — it is a route that does not exist, which is the likeliest explanation
  of EP-4's original 404 as well;
- the GraphQL `repository.issueTemplates` field returns an **empty list**, and that field is not
  known to surface YAML issue *forms* as distinct from markdown templates, so the empty list is not
  evidence either way;
- an unauthenticated fetch of `/issues/new/choose` returns the sign-in interstitial, exactly as the
  private-vulnerability-reporting form does.

**Recorded as it stands: the file is published at the path the platform reads, and the rendered form
has not been seen.** The two required acknowledgement checkboxes have not been exercised. Closing
this needs one signed-in human look at the new-issue chooser, which is not a thing a session can do.

**OD-2 — still open, deliberately, and not ticked.** `SAFETY.md` §4 was authored at EP-3 from the
decisions rather than copied from the approved draft, and the only remaining copy of that draft is
private planning state a session may not open (D-2). EP-8 was told not to tick it and has not. It is
the one block of approved public safety-facing wording whose shipped text has never been compared
against what was approved.

---

### OD-16 — the load order's fixed overhead

**Class:** ruling · **Raised by:** EP-8 · **Opened:** 2026-09-01

**Observed while executing EP-8.** After item 3 was compressed as OD-13 directed, every brief in the
roadmap fits the ceiling — the tightest, **EP-11**, by **46 tokens**. That is a pass, and it is a
pass smaller than the error of the approximation that produced it, which the tool prints on every
run. The structural figure behind it is the one worth ruling on: load-order items 1–3 cost **7,827
tokens before any brief is opened** — 52 % of the ceiling — and item 2, `GOVERNANCE.md`, is 5,084 of
them on its own. Item 3 grows with every new decision, and D-80 will cost about 25 tokens of every
future session.

**Why this is a ruling and not a fix.** The three candidate remedies each cost something the owner
has already priced once, and OD-13's directive placed two of them out of bounds:

1. **Compress item 3 further.** The `Decides` column is now a 55-character signpost. Below about 45
   it stops letting a session decide whether to open an entry, which means *more* context spent in
   item 6, not less — the check would improve while the session got worse.
2. **Compress item 2.** `GOVERNANCE.md` overrides every brief, which is exactly why OD-13 put it
   out of bounds; it is also the largest single item and the only one with real slack.
3. **Split the two largest briefs.** D-22 already says anything larger than L is split at pickup,
   and EP-11 at 6,624 tokens is the largest un-executed brief in the plan. Splitting renumbers the
   roadmap, which is why EP-8 did not do it unasked.

**What EP-8 did instead.** Recorded the margin in the tool's own output, so that every CI run prints
the tightest brief and its headroom, and parked a real tokenizer so the approximation cannot become
permanent. Nothing was raised and no brief was trimmed.

---

### OD-17 — `astral-sh/setup-uv` is a major version behind

**Class:** ruling · **Raised by:** EP-8 · **Opened:** 2026-09-01

**Observed while executing EP-8.** The OD-9 pin review found `astral-sh/setup-uv` pinned at the
`v9.0.0` commit while **v10.0.1** has been current since 2026-08-14. `actions/checkout` is current.
The pin is not a vulnerability and CI is green on it; a major version is a behaviour change, and
`enable-cache: false` — the input that keeps uv cache paths out of the public log (D-3) — is the one
this repository depends on.

**The ruling needed.** Bump to the v10.0.1 commit and verify on a pushed run, or record a dated
decision to hold at v9.0.0 with the reason. **EP-8 did neither**, because bumping a pinned action is
a CI posture change that `ADR-008` reserves for a by-hand review with a run behind it, and inventing
one inside a re-plan would be the automation OD-9 declined, wearing a different hat.

---

### OD-18 — normalise the GiB/GB transcription, or keep it

**Class:** ruling · **Raised by:** EP-7, flagged for this re-plan · **Opened:** 2026-09-01

**Observed while executing EP-7, confirmed here.** D-49 states the free-space floor in **binary**
units — 250 GiB — and D-78 states the project ceiling in **decimal** units — 25 GB, warned at 20 GB.
`epppsynth/src/epppsynth/storage/limits.py` transcribes both exactly as decided, `ADR-009` records
that the mismatch is deliberate, and a unit test asserts the two constants keep their different
bases. Nothing is wrong; the units simply differ because the decisions differ.

**The ruling needed.** Normalise the two decisions onto one base, as a dated addendum under D-49 and
D-78 — or confirm the transcription stands and close this. It is an owner decision and not a code
change: the code already does what was decided, and changing the base changes the floor by 7 % and
the ceiling by 7 % in opposite directions.

---

## Resolutions — 2026-09-01, ruled by the project owner at the P0 re-plan

Four of the six entries open at EP-8's close are ruled here; the verdicts and their bases follow.
**OD-2 and OD-8 remain open**, and both are open for the same reason: each needs a human to look at
something a session cannot reach.

**OD-1 — closed. The platform setting was performed.** The owner disabled Projects through the web
interface on 2026-09-01, and all four D-76 flags plus the reporting path were re-observed through
the API immediately afterwards: `has_issues true`, `has_discussions false`, `has_wiki false`,
`has_projects false`, `private-vulnerability-reporting {"enabled": true}`. The ruling of 2026-08-31
was option (a) — match D-76 as written — and no addendum under D-76 was warranted then or now,
because no carve-out was adopted. **The published decision and the platform now agree**, which is
the whole point of the row: it was ruled on 2026-08-31, re-observed still divergent on 2026-09-01
at EP-8, and only then acted on. A ruling recorded as done and never performed is the drift this
register exists to catch, and this row is the register catching it.

**OD-16 — ruled: accept the margin, and name the trigger.** Nothing is changed now. Every brief in
the roadmap fits, the tool prints the tightest brief's headroom on every run, and the ceiling
remains 15,000. What is decided in advance is **the remedy for the next breach**, so that the
session which trips the gate is not left improvising between four documents it should not touch:

> **When a brief breaches the context ceiling, split that brief.** D-22 already says a unit larger
> than L is split at pickup; this is that rule reaching the load order. Never trim `CLAUDE.md`,
> `GOVERNANCE.md`, the `DECISIONS.md` index block or a phase table to make a brief fit — those are
> paid by every session, and shrinking them to accommodate one oversized brief spends everyone's
> budget on one brief's excess. Never trim a brief below the self-containment the load order exists
> to guarantee. Never raise the ceiling.

The ruling is **operational, not documentary**: `roadmap_check.py` carries it as
`OVER_BUDGET_REMEDY`, every `over-budget` finding prints it, and a unit test asserts that the
finding still names it. The alternatives were considered and rejected — splitting EP-11 pre-emptively
(real work against a brief that currently passes, and P1 content EP-8 put out of scope), and
trimming `GOVERNANCE.md` (the largest single lever at 34 % of the ceiling, and the highest-risk edit
in the repository, because it is the document that overrides `DESIGN.md` and every brief and a cold
session needs it whole).

**The figure that will trigger it, recorded so nobody is surprised.** Items 1–3 cost 7,827 tokens —
52 % of the ceiling — before a brief is opened. Each new decision adds roughly 25 tokens to item 3,
and the tightest brief, EP-11, clears by 46. **D-81 is approximately where the gate fires.** When it
does, EP-11 is split, and the paragraph above is why.

**OD-17 — ruled: bump, in a commit of its own, after EP-8's CI run is recorded.** The review found
`actions/checkout` current at v7.0.1 and `astral-sh/setup-uv` a major version behind. Reading v10's
release notes changed the risk assessment: **v10.0.0's only breaking change is that
`enable-cache: auto` now disables the cache for `pull_request_target`, `workflow_run` and `release`
events — and this repository sets `enable-cache: false` explicitly**, so the breaking change cannot
reach it. v10.0.0 also adds `version: latest-known`, which installs the newest uv whose checksum the
action knows, and that is precisely the supply-chain nicety EP-1 parked as *pinning the uv binary
version in CI*. v10.0.1 is a one-line resilience fix.

**The sequencing is the substance of the ruling.** The bump does **not** ride along with EP-8's
push, because that push produces the CI run that is EP-8's acceptance 11 evidence; a red run would
then be ambiguous between the brief and the bump. EP-8 lands and records its run first, then the
bump lands with a run of its own and an `ADR-008` amendment. The row stays `◐` until that commit
exists — **ruled, not yet performed**, the same state OD-1 sat in for a day and for the same reason.

> **Performed 2026-09-01, and the row is now ☑.** EP-8 landed and recorded run 33549349557 first;
> the bump then landed alone, replacing `c771a70e…` with `20cfd1bf945f4377ade1205e4dbc17946fc9a30d`
> (v10.0.1) in both jobs, with the full review — both pins, what each resolves to, what is current,
> and why a major version was safe here — recorded as an `ADR-008` amendment. `version:
> latest-known` was **not** adopted and stays parked, better specified than before. The next by-hand
> review is EP-16's.

**OD-18 — ruled: keep the transcription; closed as confirmed.** The floor stays binary (250 GiB) and
the ceiling stays decimal (25 GB, warned at 20 GB), exactly as D-49 and D-78 state them. The reason
recorded is stronger than "it is already written down": **each unit matches what its number is
actually compared against.** The floor is checked against free space as the operating system reports
it, and Windows reports free space in binary units; the ceiling is a budget against model sizes as
they are published, and those are quoted in decimal — a "5 GB model" is 5 × 10⁹ bytes. Normalising
would force one of the two numbers to disagree with the thing it measures, and would move the real
floor and the real ceiling by about 7 % in opposite directions. The mismatch is not untidiness; it
is each number speaking the units of its own domain. Landed as a dated addendum under **D-78**,
alongside the EP-8 addendum that registered the question.

### Still open — and now gated at EP-9 pickup

**Both, plus EP-8's twelfth acceptance criterion, are carried as a pickup gate**
([`pickup-gate.md`](pickup-gate.md)), named by `roadmap/EP-9-registry-schema.md`'s header so that the
session picking up EP-9 meets them before doing any EP-9 work. This register is **not** in the
minimum context load order; a cold session would never have read it. Each gate carries three lettered
choices and states what the session does with each answer, so the owner's reply can be one letter.
Gate 3 blocks EP-9, because its answer can change the brief.

### Why neither can be closed by a session

**OD-2 — `SAFETY.md` §4 against the approved draft.** Unchanged. §4 was authored at EP-3 from D-8,
D-14, D-18, D-25, D-63 and D-79 rather than copied, because the approved draft's only surviving copy
is private planning state (D-2). It is the one block of approved public safety-facing wording whose
shipped text has never been compared against what was approved. **Only the owner can compare it**,
and until that comparison happens the row is not ticked. It lands as a dated addendum under D-69
recording that the block was authored at EP-3 and either matches or has been replaced.

**OD-8 — the issue form.** Unchanged, and now demonstrably not a push problem. The form is published
where the platform reads issue forms from — `origin/main`, default branch, `.github/ISSUE_TEMPLATE/`
— and no path available to a session shows it rendering: the REST route does not exist, GraphQL's
`repository.issueTemplates` returns an empty list and is not known to cover YAML issue *forms*, and
an unauthenticated fetch of the chooser returns the sign-in interstitial. **Closing it needs one
signed-in human look** at `/issues/new/choose`, confirming the card renders, the preamble renders,
and that the two acknowledgement checkboxes are present and block submission until both are ticked.
That last is the part nobody has ever exercised.

**Acceptance criterion 12 of EP-8 — held open by the owner.** *"Handing any one P1 brief to a cold
session, with only the load order files, is sufficient to execute it."* The owner declined to rule it
on the strength of the mechanical checks and will read EP-9 first. Recorded here so that it is not
quietly counted as passed: the executing session could not judge it, having read the whole tree, and
the owner has not yet judged it either.
