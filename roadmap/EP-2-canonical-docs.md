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
