# epppsynth — Extension roadmap (parked)

Everything deliberately **not** built in v1. Seeded 2026-08-23 from the planning session; each phase's
re-plan EP mirrors its briefs' `## Parked → final-roadmap.md` sections into this file.

Nothing here is a commitment. Items marked **excluded** are not "later" — they are governed by
[`../epppsynth/GOVERNANCE.md`](../epppsynth/GOVERNANCE.md) §9 and require external accountable parties
this project does not have.

**How an entry gets here, and how that is checked.** An entry mirrored from a brief's
`## Parked → final-roadmap.md` section carries the tag *(parked at EP-n)*. The tag is not decoration:
`tools/roadmap_check.py --parked` counts the bullets in each executed brief's parked section and the
entries tagged with that brief here, and fails when the two disagree. An item that exists in only one
of the two places is an item quietly lost, which is the failure this file exists to prevent. Entries
seeded from the planning session and entries that come from a decision rather than a brief carry no
tag, because no brief owns them.

## v1.x — plausible next increments

| Item | Why it is not in v1 | Prerequisite |
|---|---|---|
| Scenario library in the interface | v1 needs fictional scenarios for *evaluation*, not for the reader to browse; the two are different artifacts | EP-25 … EP-27 complete |
| Trainee-controlled opt-in local retention (mode b) | v1's non-surveillance guarantee is easier to keep absolute; opt-in retention needs a control surface the trainee fully owns | mode (b) gate |
| Export or sharing of output | v1 keeps output on screen and unexportable, which removes a whole class of leakage and chart-contamination hazards | an explicit decision plus a rights review of exported citations |
| Best-effort third-party installability | v1 is a personal tool with public source; installability is a support burden and an implied claim | a clean non-admin install from a path with spaces and non-ASCII characters, as an acceptance test |
| Local-only source pane | span display is safe only behind a double gate; the double gate is the work | EP-45, plus the index from EP-22 |
| A second escalation-resource locale | the shipped defaults are US and are labelled as such | verification of each number against its issuing authority |

## v2 and beyond

| Item | Why it is not in v1 |
|---|---|
| Generalised corpus ingest beyond the current single-source spine | the ingest module is authoring tooling, not the product; generalising it buys nothing until a second source is lawfully available and rights-cleared |
| Additional conceptual traditions inside the declared scope | breadth without review capacity is how a content model accretes unprovenanced concepts (R-13) |
| Fine-tuning of any model | gated behind measured baseline failure, lawful training data, governance, and an evaluation the project does not yet have |
| Retrieval over the local index on the emission path | would make output non-reproducible and reopen the rights boundary at exactly the wrong place; the index serves authoring and the source pane only |
| A packaged installer | implies a supported product |
| Any multi-user, hosted, or LAN-exposed deployment | a separate threat model and a separate release class |

## Parked during P0 — foundation, governance and public safety

Mirrored at the P0 re-plan (EP-8) from the `## Parked → final-roadmap.md` section of every executed
P0 brief, grouped by theme rather than by brief, because the themes are where the decisions will be
made. Every entry names why it is not in v1 and, where one exists, the condition that would reopen
it. Nothing here is scheduled.

### Supply chain and CI

- **`gitleaks` or `trufflehog` as a pinned, installed dependency** rather than an opportunistic
  second opinion. EP-6 ships scanners that need no third-party binary, and adding one is a
  supply-chain decision (R-29) that a foundation phase should not make in passing. *Reopens if* a
  scanner gap is found that no first-party rule can close. *(parked at EP-0)*
- **A signed-commit policy for the public history.** No `D-n` requires it, and the history was
  erased and re-created once already, so signatures would start from a re-created baseline rather
  than cover it. *Reopens if* the owner wants provenance on the public history; the signed
  pre-publication attestation below depends on this one. *(parked at EP-0)*
- **A type checker (`mypy` or `pyright`) and a coverage floor.** Both are cheap to add and expensive
  to add badly. *Reopens at* EP-17, the contracts package, where there are types worth checking.
  *(parked at EP-1)*
- **Scheduled `pip-audit` or OSV scanning of the lockfile.** Belongs with the supply-chain hardening
  pass rather than with a skeleton. *Reopens at* EP-41. *(parked at EP-1)*
- **A CycloneDX SBOM job.** Per-release, not per-push, so the CI frame is incomplete by design until
  there is a release to describe. *Reopens at* EP-50, which owns the release evidence bundle.
  *(parked at EP-1)*
- **Dependabot or renovate for the pinned action SHAs.** Ruled out, not deferred: owner ruling OD-9
  chose no automation, because a bot that opens pull requests conflicts with D-34's no-PR posture
  and two pinned actions do not justify it. The obligation it replaces is a by-hand pin review at
  every phase re-plan, discharged at EP-8 and handed forward. *Reopens if* D-34's no-PR posture
  changes. *(parked at EP-1)*
- **Pinning the `uv` binary version in CI** (`setup-uv`'s `version:` input). `uv.lock` guards the
  resolution either way, so this is a reproducibility nicety rather than a hole. *Reopens if* a run
  ever differs because of the uv version rather than the lockfile. *(parked at EP-1)*
- **An `allowlist.toml` for scanner exceptions.** Deliberately not built. Today the allowlist is one
  hard-coded directory with a test guarding its length, and that is the property that makes it safe;
  a configurable allowlist is how scanners quietly stop working. *Reopens only* with a named reason
  and a test that still bounds it. *(parked at EP-6)*

### Public history, review packet and provenance

- **Scanning rendered CI logs for identity strings.** The workflow is written not to print them, and
  "written not to" is weaker than "checked". *Reopens at* EP-46, the P5 verification re-plan.
  *(parked at EP-6)*
- **Screenshot EXIF stripping as an automated step.** Checklist item 5 is human for now because no
  screenshots exist. *Reopens when* the P5 interface briefs start producing them. *(parked at EP-6)*
- **A signed pre-publication attestation** — the packet's signature block as a signed commit or a
  detached signature. Depends on the parked signed-commit policy above. *(parked at EP-6)*
- **A published incident log for safety concerns received.** Depends on `SECURITY.md`'s reporting
  path seeing any traffic. *Reopens if* it does. *(parked at EP-3)*
- **A published security advisory log.** Nothing to log while nothing is released. *Reopens at*
  EP-52, when the first tag is cut. *(parked at EP-4)*

### Public text and documentation

- **A rendered documentation site.** `pandoc` is absent on the target machine and no static-site
  generator is in the dependency set; markdown on GitHub is the delivery mechanism for v1.
  *(parked at EP-2)*
- **Translations of the public front matter.** Raised because D-25 carries a language and
  interpreter-need field, which invites the question. Out of scope for a personal, local,
  single-operator tool (D-33). *(parked at EP-2)*
- **An automated tense and claim linter over the README.** EP-2 does the sweep by hand and EP-6 adds
  a banned-phrase check; a general-purpose overclaim linter is a larger idea. *Reopens at* EP-39,
  with the copy deck. *(parked at EP-2)*
- **Per-mode README fragments.** One README with per-mode badge rows is adequate at three modes.
  *Reopens if* modes (b) and (c) grow their own front matter at P6. *(parked at EP-2)*
- **A machine-readable charter** — the invariants and prohibitions as data, with the prose generated
  from it. Attractive, but it would put the charter's authority in a schema this project has not
  designed. *Reopens at* the P1 re-plan, once the registry schema exists. *(parked at EP-3)*
- **An external ethics review of the charter itself**, distinct from the D-27 reviewer sign-off on
  outputs. Named because reviewer recruitment deliberately starts late (D-64) and the charter is the
  artifact most improved by an outside read. *(parked at EP-3)*
- **A contributor attestation (DCO or equivalent) and a PR intake process.** D-34 defers both until
  reviewers exist (D-27), and `CONTRIBUTING.md` names that trigger, so the item has a condition
  rather than a date. *(parked at EP-4)*
- **A `SECURITY.md` PGP key or encrypted reporting channel.** GitHub private vulnerability reporting
  covers it. *Reopens only if* a reporter asks. *(parked at EP-4)*
- **A documented data-protection or records-retention posture beyond "nothing is retained".** Would
  become relevant only if the excluded modes (d) and (e) were ever reopened, which
  `GOVERNANCE.md` §9 forecloses. *(parked at EP-4)*

### Escalation resources

- **Localised escalation resources beyond the shipped US defaults and the local config.** Requires
  either geolocation, which D-18 rules out, or a curated international list, which v1 scope rules
  out. Every number would need verification against its issuing authority. *(parked at EP-3)*

### Rights, licensing and citation

- **Resolving the SAMHSA and AHRQ reuse terms** (both returned HTTP 403 at research time) **and
  reading the FDA CDS final guidance of 2026-01-06.** Carried as an explicit P1 blocker for public
  intended-use language, not as a nice-to-have. *(parked at EP-5)*
- **A licence-compatibility policy engine for dependencies** — permissive-only allow-list, with
  copyleft or ambiguous halting the release. *Reopens at* EP-50, with the release evidence bundle.
  *(parked at EP-5)*
- **Per-file SPDX headers in markdown.** `REUSE.toml` path patterns cover them. *Reopens only if* a
  downstream consumer needs per-file granularity, which D-33 makes unlikely in v1. *(parked at EP-5)*
- **Registering a DOI for the software** (Zenodo or equivalent) so `CITATION.cff` can carry one.
  Premature while nothing is released. *Reopens at* EP-52. *(parked at EP-5)*
- **Generalizing the rights table into a reusable schema** for the sibling projects. Noted because
  the shape is not project-specific; out of scope for v1. *(parked at EP-5)*
- **Generalizing the hard-coded corpus spine** in the ingest tooling into configuration, and
  **retaining `tools/` as a directory only if a non-package utility later needs it** (D-40, D-41).
  The spine is already externalised to an untracked local file under owner ruling OD-6; generalizing
  it further buys nothing until a second source is lawfully available and rights-cleared, and
  `tools/` currently holds three such utilities.

### Storage, models and the machine

- **A cache-purge tool implementing ADR-007.** Explicitly parked, not forgotten: the seven safety
  rules exist so that if the owner ever needs the space back, the work starts from a specification
  rather than from an improvisation. *(parked at EP-7)*
- **Deduplicating or reorganising the pre-existing third-party model cache.** Out of scope by D-71
  and likely to stay so. *(parked at EP-7)*
- **A backup-exclusion configuration for the index root.** The separate root exists precisely to
  make this easy; performing it is an owner machine action, not project code. *(parked at EP-7)*
- **Automated re-inventory on a schedule, and drift detection against `models.lock.json`.** Useful
  once weights actually exist. *Reopens at* the P4 re-plan. *(parked at EP-7)*
- **Hard-linking or reusing a verified weight from the third-party cache** into the project model
  root rather than re-downloading. Attractive for the ceiling, but it makes the project's footprint
  depend on a directory the project does not own. *Reopens with* an owner decision. *(parked at EP-7)*
- **Machine-wide `LongPathsEnabled` as a documented prerequisite** rather than a repository-local
  setting. Belongs with the third-party installability work, which D-33 puts beyond v1.
  *(parked at EP-0)*

### Roadmap tooling

- **A rendered roadmap view** — a burndown, or a dependency graph as an image.
  `tools/roadmap_check.py` already builds the graph in memory, but rendering it needs a diagramming
  dependency and `pandoc` is absent. *(parked at EP-8)*
- **Automatic completion-note stubs generated from `git log`.** Attractive, and rejected on purpose:
  a completion note whose deviations section is machine-written would be worthless, because the
  value of the note is the human sentence about what was harder than expected. *(parked at EP-8)*
- **A real tokenizer for `--context-budget`.** The P0 implementation divides characters by a stated
  constant, and prints the constant on every run. Named here so the approximation cannot quietly
  become permanent — the more so because the tightest brief clears the ceiling by a margin smaller
  than the approximation's own error. *Reopens when* a tokenizer can be used without a network fetch
  or a new runtime dependency. *(parked at EP-8)*
- **Calibrating S, M and L against actuals across more than one phase.** One phase of timings is a
  sample of nine, and the P0 retro found the sample too skewed to act on. *Reopens at* the P1 and P2
  re-plans, before D-22's definitions change. *(parked at EP-8)*

## Excluded — not deferred

Governed by `GOVERNANCE.md` §9. Patient-specific point-of-care use · patient- or family-facing use ·
PHI processing · EHR integration · autonomous action · therapeutic use of any kind. The author will
not attempt these as a solo project. The seven preconditions each name an external accountable party.

**Non-Western and non-secular conceptual frameworks** are out of scope by decision, not by backlog.
The mitigation is an explicit scope label plus tested abstention. Adding them would require
compensated co-design with the communities concerned and qualified review — doing it badly is worse
than not doing it, and pretending the backlog will fix it is worse still.

## De-scoped during planning

- **"Hidden Dynamic / Empathic Wedge / Bridge"** as an output model. Retired. Three of the functions
  worth keeping — naming plausible unspoken concerns, suggesting an opening move, and naming the
  clinician's own reaction — survive in the three-part contract, reframed so that concerns are plural
  hypotheses with counter-readings and every suggested utterance is a question or an offer rather than
  a lever. The fourth, connecting values to options, was withdrawn with the contract's fourth part
  (see below).
- **The output contract's fourth part** — "neutral framing connecting stated values to
  clinician-verified options". Deleted, not deferred. It had no input field, no record type and no
  owning brief, so it would have shipped permanently empty while making the evaluation's substance
  tuple carry a constant. Restoring it would require all three of: an input field carrying the options
  as the clinician states them, a completeness invariant (each entered option appears exactly once,
  unranked, none added, none omitted, checked mechanically), and evidence that the part is worth the
  coercion surface it opens. Absent all three, the tool says nothing about clinical options at all.
- **A formal ontology (OWL/RDF) with a reasoner.** Buys inference the product does not need and
  imports an authority claim it must avoid.
- **Ollama as the local runtime.** Auto-downloads updates on Windows and registers a background
  service; both are incompatible with a verifiable no-runtime-network claim.
- **LLM-as-judge evaluation scoring.** Would collapse the independence of the deterministic control
  arm and add an unauditable dependency inside an offline boundary.
- **A widget-framework interface.** Rejected on architectural control: the output contract's semantics
  and the accessibility gate both require owning the markup. Recorded with the caveat that no
  accessibility claim was verified about the alternative.
- **A cache-purge tool.** The seven safety rules are written; the tool is not built, because nothing
  currently needs it.
