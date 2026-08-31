# EP-2 — Canonical docs + public front matter + badge scheme

**Size:** L · **Mode:** n/a · **Core/Stretch:** core ·
**Depends on:** EP-1 (toolchain, package skeleton, ADR framework, CI) · **Blocks:** EP-3 (SAFETY charter), EP-4 (privacy/security/conduct), EP-5 (licensing pack), EP-6 (leak-prevention CI), EP-8 (roadmap tooling, re-plan P0), EP-9 (registry schema v0)

## Context

Every brief in this plan begins by reading `CLAUDE.md`, then `epppsynth/GOVERNANCE.md`, then the
`DECISIONS.md` index block. **None of those files exists yet.** EP-2 creates them, and in doing so
converts the roadmap's declared load order from an intention into something a cold session can
actually follow. It is the largest brief in P0 for that reason: it is not writing prose, it is
building the substrate that the other seven briefs read.

It also fixes the single most visible defect in the public tree. The root `README.md` currently
reads, in full:

> `# epppsynth` / `existential psychotherapy for physicians & patients`

That names a regulated clinical modality the tool must disclaim (D-4). **EP-2 replaces it** with
the approved expansion "**existential perspectives for physicians & patients**" and the approved
status line "**Design and planning artifact — v1 in progress; no release, no demo, no
validation.**" (D-24). Until this brief lands, the public front door of the project makes a claim
that GOVERNANCE forbids.

**What exists.** The uv project, `src/` layout, `epppsynth/docs/adr/` with four ADRs, one green CI
workflow, the roadmap bundle, and a two-line `README.md` carrying the retired wording.
`epppsynth/README.md` is an empty placeholder.

**What this brief creates.** `CLAUDE.md`, `epppsynth/DESIGN.md`, `epppsynth/GOVERNANCE.md`,
`epppsynth/DECISIONS.md` (index block first, then full entries), the rewritten root `README.md`
with the four-row maturity-badge scheme, and `epppsynth/docs/evidence/design.md` — the evidence
file the current badge resolves to.

**The approved verbatim public text** (Intended use / Excluded uses / What it does not know /
Status) is drafted and approved (D-69). EP-2 places **Status** and a short Intended-use summary in
`README.md`; **EP-3** places the full four-block text in `SAFETY.md` and the README links to it.
Neither brief may paraphrase the approved wording — it is copied character for character, and
step 9's diff proves it.

Implements: D-3, D-4, D-12 (maturity badge tied to evidence, not effort), D-24 (public wording),
D-40 (canonical docs), D-59 (badge is a static string CI resolves to an evidence file), D-61
(excluded modes are *excluded with named preconditions*, not "deferred"), D-63 (the no-evidence
statement appears in the public README), D-69 (approved wording). Mitigates R-9 (portfolio
overclaim) and R-36 (site/narrative drift ahead of the badge).

## Safety preconditions

| Invariant at risk | Guard in this brief |
|---|---|
| Overclaim under hiring pressure (R-9, D-63) | Every sentence in `README.md` describing behaviour is in the present tense **only if it exists today**; everything else is written as "planned (EP-n)". The evidence-honesty statement of D-63 — that the closest analogue trials are null-to-adverse and that the defensible analogue is a question-generation aid — appears in the README, not only in SAFETY. Step 10's tense sweep is a mechanical check for the failure mode. |
| Badge tied to effort rather than evidence (D-59, R-9) | The badge is a plain-text string in `README.md`, and `epppsynth/docs/evidence/design.md` is created **in the same commit** with its checklist ticked. The CI check that enforces the mapping is EP-6; this brief must therefore leave the badge and the evidence file in a state EP-6 can parse, and the format is fixed here and recorded in the README. |
| Retired modality wording remains public (D-4) | Step 10 greps every tracked file for `psychotherapy` and requires zero hits outside `DECISIONS.md` (where D-4 records what was retired and why) and `source material/README.md` (the corpus directory name, which is a factual reference to a book title and is not a claim about the tool). |
| `.local/` content leaking into public docs (D-2) | `DECISIONS.md` is written from the decision *statements*, never by copying the discovery ledger. Step 11 diffs the two: no sentence of more than eight consecutive words may appear in both `epppsynth/DECISIONS.md` and any file under `.local/`. Hazard IDs, decision IDs and constraint IDs are exempt. |
| Excluded modes read as "coming soon" (D-61) | `GOVERNANCE.md` states modes (d) and (e) as **excluded**, lists the seven named preconditions, and records that the author will not attempt them as a solo project. The word "deferred" is banned in that section, checked by step 10. |
| Docs claim a review status the project does not have (D-27, D-65) | `README.md` states "author review only" plainly and names D-27's reviewer gate as future work, with the brief number. |

Pre-publication checklist items exercised here: **4 (local paths & hostname)**, **7 (public claims
— README, badge and `CITATION.cff` must all say the same thing; `CITATION.cff` does not exist yet,
so this brief records the exact strings EP-5 must match)**.

## In scope

1. **`CLAUDE.md`** at the repository root — the session-rules file that is item 1 of the load
   order. Contents: the never-do list (never read `.local/` or `source material/` at pickup; never
   commit a model, an index, or a corpus path; never widen a public claim without an evidence
   file; never edit a decision — append a dated addendum), the command conventions (`uv run …`
   from `epppsynth/`; `pandoc` and `cmake` are absent and may not be assumed), the commit-pair
   convention, and the load order itself as a table. Keep it under ~1.5k tokens: it is read by
   every session and its size is a tax on all of them.
2. **`epppsynth/GOVERNANCE.md`** — the file that overrides DESIGN and every brief. Sections:
   *Data boundary* (D-8, verbatim); *Rights and what may be committed* (D-10, D-28); *Public-safety
   posture* (D-3) carrying the defense-in-depth statement **verbatim**: `.gitignore`, pre-commit
   hooks and CI scanners are defense in depth; they are not proof that nothing leaked; the proof is
   the pre-publication review packet, performed by a human, recorded with a date and a commit hash;
   *Trainee non-surveillance guarantee* (D-19); *Excluded release classes* — modes (d) and (e),
   excluded with their seven named preconditions and the solo-project statement (D-61); *Release
   gates* (the eight D-35/D-67 items, listed, each naming the brief that produces its artifact);
   *Hazard register* R-1 … R-41 as a table, each row naming the mitigating brief and the verifying
   gate; *Human-subjects posture* (D-77 — the reviewer study is not intended for publication, the
   consent form says so, and the trigger that would change that is named); *Session rules* pointing
   at `CLAUDE.md`.
3. **`epppsynth/DECISIONS.md`** — **the index block comes first**: one row per decision,
   `D-n · title · one clause`, D-1 … D-78. Then the full entries in the fixed form
   `**D-n Title.** Decision. *Why.* *Alternatives considered.*`. Then an empty
   `## Addenda` section with the `> **Addendum (date, EP-n).**` convention documented. The index
   exists so that a cold session loads ~80 lines instead of ~700; EP-8's `--context-budget` check
   depends on it.
4. **`epppsynth/DESIGN.md`** — purpose and non-goals · the three modes and one engine (D-13) ·
   input contract (D-25) · output contract (D-11/D-26) · abstention taxonomy (D-38) · deterministic
   engine and the LLM gate (D-17, D-54, D-56) · concept registry (D-15) · corpus ingest and the
   local index (D-10, D-16, D-23, D-51) · UI architecture and the accessibility contract (D-32,
   D-58, D-68) · threat-model pointer · a `## Traceability` section, seeded with the header row and
   the rule, populated by later phases · a **module map with each module tagged by the EP that
   builds it**. Sections whose content is a later phase's work carry an explicit
   `> Planned — EP-n.` line rather than speculative prose.
5. **Rewrite the root `README.md`.** Structure, in order: name + the D-24 expansion "existential
   perspectives for physicians & patients" · the maturity badge line · the D-24 status line
   verbatim · what it is, in three sentences · a short Intended-use summary with a link to
   `SAFETY.md` for the full approved text (**EP-3** places it) · the not-a-risk-detector line
   verbatim · the three modes with per-mode status and per-mode badge rows · the D-63 evidence
   statement (analogue trials are null-to-adverse; this is a question-generation aid; no
   effectiveness claim is made) · reading paths (clinical reader →
   `epppsynth/docs/for-clinical-readers.md`, *planned — EP-53*; engineer →
   `epppsynth/DESIGN.md`) · roadmap link · licence split (*placed by EP-5*) · citation (*placed by
   EP-5*) · "no PRs in v1; issues for discussion only" (D-34, expanded by **EP-4**).
6. **Badge scheme.** Four rows **per mode**, plain text, no shield image (a shield is a network
   fetch on a page the owner does not control):

   | Badge string | README meaning | Earned when | Evidence file |
   |---|---|---|---|
   | `status: design` | design & planning artifact | roadmap + canonical docs exist; no engine | `epppsynth/docs/evidence/design.md` |
   | `status: skeleton` | runs; not evaluated | deterministic engine + CLI run end-to-end on fixtures | `epppsynth/docs/evidence/skeleton.md` |
   | `status: self-evaluated — mode (x)` | mode (x) evaluated **by the project's own suites**, not by an external body | all eight D-35/D-67 items satisfied for mode (x) | `epppsynth/docs/evidence/mode-x-gate.md` |
   | `status: v1 — mode (x)` | v1 tagged for mode (x) | above + tag cut + D-29 clearance recorded | `epppsynth/docs/evidence/mode-x-release.md` |

   The third rung reads **`self-evaluated`**, not `evaluated`. A bare "evaluated" reads as external
   validation, and every suite behind that rung is written and run by the project itself; the prefix
   keeps the badge honest about who did the evaluating (GOVERNANCE §1, §11 — status is stated
   honestly, and public materials never overstate maturity or review status). The README row's
   meaning column says the same in words, so the honesty does not rest on a reader parsing a hyphen.

   Document the **exact** parse contract EP-6's checker will implement: the badge is a line in
   `README.md` matching `^status: (design|skeleton|self-evaluated — mode \([abc]\)|v1 — mode \([abc]\))$`
   inside a fenced block, and the checker maps it to the evidence path by the table above.
7. **Create `epppsynth/docs/evidence/design.md`** — the evidence file for today's badge. It is a
   checklist with ticked boxes: roadmap exists · canonical docs exist · no engine exists · no
   evaluation exists · no release exists. Each box names the artifact that makes it true. This file
   is what stops the badge from being a claim about effort.
8. **Set the current badge to `status: design`** and set every per-mode row to "not started".
9. **Verbatim-text discipline.** Copy the D-69 wording used in this brief (the Status line, the
   not-a-risk-detector line) character for character from the approved text. Record in the
   completion note the exact byte length of each copied string so EP-3 and EP-5 can assert equality
   rather than similarity.
10. **Run the tense, banned-word and claim sweeps** described in the acceptance section, and fix
    what they find before committing.
11. **Run the `.local/` overlap check** (safety precondition 4) and fix anything it flags.
12. **Commits:** `docs(epppsynth): add canonical docs, public front matter and badge scheme (EP-2)`
    then `docs(roadmap): record EP-2 commit hash`.

## Out of scope

- The full approved four-block public text (Intended use / Excluded uses / What it does not know /
  Status) as a charter — **EP-3** places it in `SAFETY.md`. EP-2 places only the Status line, a
  short Intended-use summary, and the not-a-risk-detector line, and links onward.
- `PRIVACY.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md` — **EP-4**.
- `LICENSE`, `LICENSE-CONTENT`, `LICENSES/`, `REUSE.toml`, `NOTICE`, `CITATION.cff`, the rights
  table — **EP-5**. EP-2 leaves two named placeholders in the README and records the exact strings
  EP-5 must match.
- The CI check that enforces badge → evidence — **EP-6**. EP-2 defines the parse contract; EP-6
  implements it and proves it with a deliberate red run.
- `epppsynth/docs/for-clinical-readers.md` — **EP-53**. The README links to it with a
  `planned — EP-53` marker, not a live link.
- The `prime` site card correction — **EP-53** (D-43).
- DESIGN's completed module map and the populated traceability matrix — **EP-23** (P2 integration)
  and each phase's re-plan.
- The registry schema itself — **EP-9**.

## Verification / acceptance

Runnable, from the repository root:

```powershell
# the retired modality wording is gone from every public claim
git ls-files | ForEach-Object { Select-String -Path $_ -Pattern 'psychotherapy' } |
  Where-Object { $_.Path -notmatch 'DECISIONS\.md|source material' }        # → no output

# the approved status line is present, character for character
Select-String -Path README.md -SimpleMatch `
  'Design and planning artifact — v1 in progress; no release, no demo, no validation.'

# badge parses and its evidence file exists
Select-String -Path README.md -Pattern '^status: design$'
Test-Path epppsynth/docs/evidence/design.md

# DECISIONS index has exactly one row per decision
(Select-String -Path epppsynth/DECISIONS.md -Pattern '^\| D-\d+ ').Count      # → 78

# every D-n cited anywhere in tracked files resolves to an entry
git ls-files | ForEach-Object { Select-String -Path $_ -Pattern 'D-\d+' -AllMatches } |
  ForEach-Object { $_.Matches.Value } | Sort-Object -Unique                    # cross-check vs index

# banned word in the excluded-modes section
Select-String -Path epppsynth/GOVERNANCE.md -Pattern 'deferred' -Context 0,0   # → none in that section

# every relative link in the new docs resolves
git ls-files "*.md" | ForEach-Object { Select-String -Path $_ -Pattern '\]\(([^)#h][^)]*)\)' -AllMatches }
```

Acceptance:

1. `README.md` contains the D-24 expansion and the D-24 status line **exactly**, byte lengths
   matching those recorded in step 9. No occurrence of "psychotherapy" survives outside
   `DECISIONS.md` and `source material/README.md`.
2. The badge line matches the documented regex and `epppsynth/docs/evidence/design.md` exists with
   every box ticked and every box naming its artifact.
3. `epppsynth/DECISIONS.md` opens with an index block whose row count equals the number of full
   entries, and equals 78. Every `D-n` referenced anywhere in a tracked file resolves to an index
   row; there are no dangling references and no orphan entries.
4. `epppsynth/GOVERNANCE.md` contains the defense-in-depth sentence verbatim, lists all eight
   release-gate items with the brief that produces each artifact, and tabulates R-1 … R-41 with a
   mitigating brief and a verifying gate for every row.
5. Modes (d) and (e) appear in `GOVERNANCE.md` as **excluded** with seven named preconditions and
   the solo-project statement; the word "deferred" does not appear in that section.
6. Tense sweep: every sentence in `README.md` and `DESIGN.md` describing tool behaviour is either
   present-tense-and-true-today or carries a `planned (EP-n)` marker. *(judgement — the project
   owner; the sweep produces the candidate list, the owner rules on each.)*
7. `.local/` overlap check: no eight-word sequence shared between `epppsynth/DECISIONS.md` and any
   `.local/` file, excluding ID tokens.
8. Every relative link in every tracked `.md` resolves with `Test-Path`, except links explicitly
   marked `planned — EP-n`, which must **not** be rendered as links at all.
9. `uv run pytest -q` from `epppsynth/` is still green and CI is still green — this brief adds no
   code, and a red run means it touched something it should not have.
10. *(judgement — the project owner)* Reading `CLAUDE.md` → `GOVERNANCE.md` → the `DECISIONS.md`
    index → the P0 table → any one brief is sufficient to execute that brief, and the four files
    together stay inside the ~15k-token budget EP-8 will enforce.

## Parked → final-roadmap.md

- A rendered documentation site. `pandoc` is absent and no static-site generator is in the
  dependency set; markdown-on-GitHub is the delivery mechanism for v1.
- Translations of the public front matter. Raised because D-25 has a language/interpreter-need
  field, which invites the question; out of scope for a personal, local, single-operator tool
  (D-33).
- An automated tense/claim linter over the README. EP-2 does the sweep by hand and EP-6 adds a
  banned-phrase check; a general-purpose overclaim linter is a larger idea and belongs with the
  copy deck at EP-39.
- Per-mode README fragments. The single README with per-mode badge rows is adequate at three modes;
  revisit if modes (b) and (c) grow their own front matter at P6.

---

> **Completion note (2026-08-31).** Executed as `8dd937a`, with six deviations recorded below.
> Every result stated here is what was **observed**, not what was expected. The sweeps of steps 10
> and 11 were run as a single script; all 30 checks pass.
>
> #### Deviation 1 — the brief's "What exists" was stale
>
> The brief states that `CLAUDE.md`, `epppsynth/DESIGN.md`, `epppsynth/GOVERNANCE.md` and
> `epppsynth/DECISIONS.md` do not exist. **Three of the four already existed**, committed by EP-0
> (`8cb31ec`) and substantially complete: `DECISIONS.md` (58 KB) already carried the index block
> *and* the full entries, `GOVERNANCE.md` (19 KB) already carried §1–§15 including the D-8 data
> boundary and the verbatim defense-in-depth statement, and `DESIGN.md` (32 KB) already carried the
> complete R-1 … R-41 hazard register and a seeded traceability matrix. Only `CLAUDE.md` was
> genuinely absent. EP-2 therefore **closed the gaps** rather than creating the file set. The gaps
> closed were: `CLAUDE.md` (created); the root `README.md` (rewritten from two lines); the badge
> scheme and its parse contract; `epppsynth/docs/evidence/design.md` (created); brief attribution on
> the eight release gates; the D-61 wording in GOVERNANCE §9; the `## Addenda` section in
> `DECISIONS.md`; the DESIGN module map; and per-section planned markers.
> `epppsynth/README.md` was a **0-byte tracked file** and was filled with a short pointer stub — not
> in the brief, but a blank tracked file is a defect and the fix is three sentences.
>
> #### Deviation 2 — there are 79 decisions, not 78
>
> Acceptance 3 expects 78. **D-79** (the output contract reduced to three parts) was added after this
> brief was written. The check was executed as the invariant it encodes — *index rows == full
> entries == the actual count* — and observed **79 index rows, 79 full entries, contiguous
> D-1 … D-79, no duplicates**. The cross-check of every `D-n` cited in any tracked file found **no
> dangling reference and no orphan entry**.
>
> #### Deviation 3 — the hazard register stays in `DESIGN.md` §14
>
> In-scope item 2 asks `GOVERNANCE.md` to tabulate R-1 … R-41. It was **not** moved. `DESIGN.md` §14
> already is that table and states "**This table is the register**; every other document points at it
> rather than restating it"; GOVERNANCE §13 already points at it and names the two highest-rated
> hazards. Restating 41 rows in a second file creates two registers that drift, which is the failure
> the single-register rule exists to prevent. What the brief actually wanted was verified in place
> instead: **all 41 rows present, contiguous, and every row names both a mitigating brief and a
> verifying gate** (checks 4d–4f).
>
> #### Deviation 4 — the modality sweep needed two more exemptions, and four rewordings
>
> Step 10 exempts `DECISIONS.md` and `source material/README.md`. The sweep found six files. Four
> were **reworded**, each to a *broader* term, so the disclaimer is strengthened rather than
> weakened: GOVERNANCE §1 and §4.1 and `src/epppsynth/__init__.py` now read "not **therapy**" (which
> excludes strictly more than the retired term did), and DESIGN §6.1 now reads "a **therapeutic**
> framework". Two files could not be cleared inside this brief's scope:
>
> - `roadmap/EP-2-canonical-docs.md` — this brief, which necessarily quotes the banned token in order
>   to specify the sweep. Self-referential; exempt permanently.
> - `tools/epub_to_md_pipeline.py` — see the parked item below. Exempt for now, with a reason.
>
> `source material/README.md` was checked and contains **no** occurrence; its exemption is
> precautionary. EP-6 should implement the sweep with this four-entry exemption list, each entry
> carrying its reason, rather than as a bare grep.
>
> #### Deviation 5 — the `.local/` overlap check is unsatisfiable as written
>
> Step 11 requires that **no** eight-word sequence be shared between `epppsynth/DECISIONS.md` and any
> `.local/` file. Observed: **124 shared passages, 19.7 % of `DECISIONS.md` by word count, longest 42
> words.** This is not a leak and the check cannot be made to pass, because the two requirements
> conflict: the private ledger records each decision *in the words it was settled in*, and D-2
> **requires publishing those settled decisions**, so the decision statement itself is necessarily
> shared text. The two longest shared passages are D-37's stop criterion and D-26's preserved output
> functions — both settled decision statements, both required to be public.
>
> The invariant that actually guards against ledger-copying was tested instead: **every shared
> passage must fall inside a published decision entry or the index block, never in the surrounding
> prose.** Observed: **zero passages outside a published decision entry.** The shared text is
> distributed evenly across all thirteen decision sections (3–20 passages each), which is the
> signature of decision statements appearing in both files rather than of deliberation being pasted
> in.
>
> No `.local/` file was read by the session. The check runs as a script that reports only positions
> and counts within the already-public `DECISIONS.md`; no private content entered the session or any
> public file. **EP-6 should implement the refined form**, not the literal one, and the owner should
> confirm the ruling that a shared settled-decision statement is not a leak.
>
> #### Deviation 6 — planned markers were added, and the tense sweep re-scoped
>
> In-scope item 4 requires DESIGN sections whose content is later-phase work to carry an explicit
> `> **Planned — EP-n.**` line. None did — the file relied on a single preamble sentence and on
> `EP-n` tags in the section headings. Markers were added to **§1–§13 and §15** (14 in total). §14
> (the hazard register) and §17 (the module map, which marks state per row) describe artifacts that
> exist today and carry none.
>
> With those in place the tense sweep over `README.md` and `DESIGN.md` produced **4 candidates, all
> ruled acceptable**: two are line-wrap artifacts where the `planned — EP-n` marker fell on the next
> line; one is the not-a-risk-detector line, a negative claim true today; one describes the badge
> parse contract, which exists today. *(Acceptance 6 is owner judgement — the sweep produced the
> candidate list and the ruling above is offered for confirmation.)*
>
> #### Step 9 — verbatim byte lengths, for EP-3 and EP-5 to assert equality against
>
> | String | Chars | UTF-8 bytes | Placed in |
> |---|---|---|---|
> | `existential perspectives for physicians & patients` | 50 | **50** | `README.md` line 3 |
> | `Design and planning artifact — v1 in progress; no release, no demo, no validation.` | 82 | **84** | `README.md`, below the badge |
> | `This tool is not a risk detector and must not be used as one. It never checks what is typed for danger.` | 103 | **103** | `README.md` intended-use section; GOVERNANCE §3 |
>
> The em dash in the status line is U+2014 (3 bytes), which is why 82 characters is 84 bytes — assert
> on bytes, not on length. The not-a-risk-detector line was verified **byte-identical** between
> `README.md` and `GOVERNANCE.md` §3 after stripping bold markers (check 1e). **EP-5's
> `CITATION.cff` must reproduce rows 1 and 2 exactly**; EP-3's `SAFETY.md` must reproduce rows 2 and
> 3 exactly, and must not paraphrase.
>
> #### Badge and evidence (steps 6–8)
>
> Badge set to `status: design` inside a fenced block; **exactly one** line in `README.md` matches
> the parse contract. All three per-mode rows read "not started".
> `epppsynth/docs/evidence/design.md` created with **7 boxes, all ticked**, each naming its artifact.
> Every claim in it was verified against the tree: 55 briefs present; `git tag` returns **0 tags**;
> no `release-evidence/`; no `epppsynth/eval/`; `pyproject.toml` version `0.0.0`; `src/epppsynth/`
> contains only `__init__.py` and a placeholder `cli.py`. The parse contract EP-6 must implement is
> recorded verbatim in the README, and matched exactly one line when run against it.
>
> #### Link discipline (acceptance 8)
>
> Every relative link in every tracked `.md` resolves. **Nothing marked `planned — EP-n` is rendered
> as a link** — `SAFETY.md` (EP-3), `epppsynth/docs/for-clinical-readers.md` (EP-53), and the licence
> and citation placeholders (EP-5) are plain text with an explicit marker, per acceptance 8 rather
> than per in-scope item 5, which asks for a link to a file that does not exist yet.
>
> #### Acceptance 9 — the tree is still green
>
> From `epppsynth/`: `uv run ruff check .` returned "All checks passed!"; `uv run ruff format
> --check .` returned "13 files already formatted"; the deselected-marker pytest run returned
> **3 passed**. A carriage-return search over `HEAD` produced no output and exit 1: no committed blob
> contains a carriage return, so EP-1's line-ending invariant still holds. (Python's default newline
> translation left CRLF in the working copy of four edited files; the committed blobs were normalised
> to LF by `.gitattributes`, and the working copy was normalised to match before the second commit.)
>
> #### Acceptance 10 — load-order budget
>
> `CLAUDE.md` is **3,379 characters ≈ 850 tokens**, inside the ~1.5k the brief allows. Items 1–4 of
> the load order (`CLAUDE.md` + `GOVERNANCE.md` + the `DECISIONS.md` index block + one P0 phase
> table) total ≈ 11.5k tokens, leaving ≈ 3.5k for a brief inside EP-8's ~15k budget. The two largest
> briefs in P0 exceed that on their own, so **EP-8's `--context-budget` check will fail for at least
> EP-2 and EP-9 as the files now stand** — recorded here so EP-8 designs for it rather than
> discovers it. *(The rest of acceptance 10 is owner judgement.)*

## Parked → final-roadmap.md

- **`tools/epub_to_md_pipeline.py` publishes the source book's title and its full chapter-title table
  in a tracked, public file** (lines 4, 24, 35–44, 359). That is the outline-reconstruction pattern
  D-74 forbids for public citations and that DESIGN §6.1 Y-8 names as a rights-leakage failure
  mode — currently guarded only for the registry, not for `tools/`. Found by this brief's step-10
  sweep and **not fixable inside EP-2**: the table is the pipeline's operative source spine, D-41
  already parks generalising it, and the pipeline moves into the package at **EP-22**. Flagged for
  **EP-5** (the per-source rights table), **EP-6** (the leak scanners, which should treat a tracked
  chapter-title sequence as a finding) and **EP-22** (which should move the spine into an untracked
  local config as it moves the code). Worth a decision addendum if the owner rules it a live rights
  exposure rather than a latent one.
- The four items the brief already parks (a rendered documentation site; translations of the public
  front matter; an automated tense/claim linter; per-mode README fragments) carry over unchanged.
