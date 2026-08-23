# EP-10 — Provenance, rights, reuse class, citation rule, authoring guide

**Size:** L · **Mode:** n/a · **Core/Stretch:** core ·
**Depends on:** EP-5 (Licensing pack + per-source rights table), EP-9 (Registry schema v0) ·
**Blocks:** EP-12 (seed content A), EP-13 (seed content B), EP-14 (seed content C), EP-16 (registry
validator, re-plan P1)

## Context

EP-9 declared that a concept carries a `provenance` block and a `reuse_class`. This brief gives those
fields their **semantics, their permitted values, the per-source rights table they point at, the
citation rule they must satisfy, and the authoring guide a human follows when writing concept prose
from a copyrighted reading**. Nothing may be authored until this brief lands: EP-12, EP-13 and EP-14
all depend on it.

It implements **D-10** (both rights paths: a hand-authored, cited, original-prose public artifact;
a gitignored local index built from the reader's own legally obtained copy), **D-28** (Apache-2.0 code
+ CC BY 4.0 content, `NOTICE`, `CITATION.cff`, per-source rights table), **D-62** (normative guidance
under a non-commercial or share-alike licence is **referenced, never ingested**), **D-74** (citation
and quotation limits), and **D-23** (verbatim spans are never emitted, only optionally displayed in a
local-only pane).

**Two hard positions this brief must encode, not merely describe.**

1. **Public citations are chapter-level locators only.** No page ranges. No quoted phrase. No chapter
   title reused as a concept label. No sequence of locators that reconstructs a work's outline.
   Quotation budget ≤ 25 words per quote and ≤ 150 words per source, enforced in CI (D-74).
2. **Two source families' reuse terms are UNVERIFIED** — the trauma-informed-care source family and
   the shared-decision-making source family, whose pages returned HTTP 403 to direct fetch. Until a
   rights check clears them they carry `reuse_class: reference-only-pending-rights-check`, and
   **this brief owns that check**. The check may end in "still unverified"; that is an acceptable
   outcome and it keeps the conservative posture, but it must be *recorded* with what was attempted.

**What exists at pickup, and who owns what.** EP-5 shipped the licensing pack (`NOTICE`, `LICENSE`,
`LICENSE-CONTENT`, `CITATION.cff`), **the `registry/sources.yaml` schema and its closed
`reuse_class` enumeration**, the `epppsynth/src/epppsynth/rights/` loader and the
`epppsynth/docs/rights.md` generator, the quotation-budget counter function, and the first source
rows — with the two unverified families already recorded as
`reference-only-pending-rights-check` with their HTTP 403 observation and date. EP-6 shipped the
leak-prevention CI and the pre-publication packet. EP-9 shipped the registry schema, `schema_check`
and the empty `provenance` / `reuse_class` field declarations.

**EP-5 is authoritative on the source-side schema; this brief does not redefine it.** What this brief
adds is the *concept side*: the provenance block's semantics, the `derivation_mode` enumeration and
its permission matrix against EP-5's `reuse_class`, the concept-facing citation lints, the authoring
guide, the per-concept attestation, and the rights check EP-5 explicitly handed forward. No concept
content exists.

Commands run from the workspace directory `epppsynth/` unless a step says "from the git root".

## Safety preconditions

- **R-15 (licence contamination) — the highest-severity risk in this brief.** Guard: `reuse_class` is
  a **required, closed** enum on every source; a hard rule maps `reuse_class` to permitted
  `derivation_mode` values; the checker fails on any concept whose `derivation_mode` is not permitted
  by its source's `reuse_class`. A non-commercial or share-alike source may **only** be `reference-only`
  — it can never license authored prose, because the CC BY 4.0 content licence cannot absorb it.
- **R-7 (copyright / derivative distribution) and Y-8 (rights leakage through structure).** Original
  prose can still infringe by reproducing a work's organisation. Guards: the abridgement rule
  (step 3), the outline-reconstruction lint (step 5), and the per-concept authoring attestation
  (step 6).
- **D-74 enforcement.** The citation lint is a *validator rule with a regex*, not a style note:
  reject any `short_citation` containing a quotation mark of any kind (straight, curly, guillemet),
  any page-range pattern, any `p.`/`pp.` locator, or a string matching a chapter title in the local
  manifest. Reject any concept whose `label` string-matches a chapter title. The quotation budget
  counter runs across the whole registry and fails at > 25 words in one quoted span or > 150 words
  attributable to one `source_id`.
- **D-16 / D-23 / R-19, R-35 (local index leakage).** The local reading corpus and the local index
  live **outside the repository tree**, are gitignored, and never enter CI. The `page_or_locator`
  field is **local-only**: it exists in the schema, is populated during authoring, and is **stripped
  from every public render and every exportable type**. Guard: a render-time strip plus a CI check
  that no committed artifact contains a `page_or_locator` value.
- **D-29 / R-9 (IP overclaim).** This brief is **issue-spotting, not legal advice**, and every
  artifact it writes says so in its own front matter. EP-5's `verification_note` field records
  *who looked and how*, never "cleared".
- **Public-safety (D-3, R-6).** Everything here is public. The authoring guide's worked example must
  be **original prose** with no phrase from any copyrighted source. No local filesystem path, machine
  name or account name appears in any committed file; the local corpus manifest is referenced by
  *relative role* ("the local reading manifest"), never by absolute path. Re-run the EP-6
  pre-publication packet for *protected text*, *local paths* and *quotation budget*.
- **Not a clinical artifact.** No clinical guidance, no concept content, no user-facing copy.

## In scope

1. **The provenance block, fixed.** Write into `docs/registry-schema.md` (§Provenance) and
   `schema/concept.schema.json`:

   | Field | Required | Notes |
   |---|---|---|
   | `source_id` | yes | FK into `sources.yaml`; must resolve |
   | `derivation_mode` | yes | closed enum, step 2 |
   | `short_citation` | yes | the public string; rule in step 4 |
   | `page_or_locator` | no | **local-only**, stripped from every public render |
   | `access_date` | yes | ISO date the author consulted the source |
   | `attestation_id` | yes | FK into `authoring-attestations.yaml`, step 6 |

   `reuse_class` sits on the **source**, is denormalised onto the concept for lint speed, and the
   checker fails if the two disagree — so a source's reclassification cannot silently leave a stale
   concept behind.

2. **`derivation_mode`, and the matrix that binds it to EP-5's `reuse_class`.** This brief defines
   one new closed enum:

   `derivation_mode` ∈ `reading-informed-original` · `public-domain-derived` · `government-work` ·
   `reference-only` · `author-original`

   `reuse_class` is **EP-5's closed enum, used as-is**: `cc-by-4.0-compatible` · `reference-only` ·
   `reference-only-pending-rights-check` · `owner-copy-read-as-input`. Do not add a value; if the
   rights check in step 7 produces a source that fits none of the four, raise it as an EP-5 schema
   amendment with a dated addendum rather than widening the enum here.

   The permission matrix — **write it as a table in the spec and as a lookup in the checker**:

   | `reuse_class` (EP-5) | Permitted `derivation_mode` | May its wording inform prose? |
   |---|---|---|
   | `cc-by-4.0-compatible` | any | yes, with attribution |
   | `reference-only` | `reference-only`, `reading-informed-original` | **no** — cite and read only |
   | `reference-only-pending-rights-check` | `reference-only`, `reading-informed-original` | **no** — the conservative default |
   | `owner-copy-read-as-input` | `reference-only`, `reading-informed-original` | **no** — the copy is a reading input, not a licence |

   `government-work` and `public-domain-derived` are reachable only from `cc-by-4.0-compatible`, and
   only once EP-5's `verified_at` is non-null on that source. A source whose `verified_at` is `null`
   can never license authored wording, whatever its `reuse_class` says — the checker enforces
   `verified_at` as a precondition, not the class alone.

   `reading-informed-original` means: the author read the source, then wrote prose that is their own
   in wording, sentence structure and sequence. It is permitted against a copyrighted source and is
   the normal mode for this project. It is **not** a licence to abridge — see step 3.

3. **The abridgement rule, stated as a rule.** *Abridgement is derivation.* Prose written from any
   source that is not `cc-by-4.0-compatible` must not (a) follow the source's sequence of headings,
   (b) preserve the source's sentence structure with substituted words, (c) reproduce the source's
   list of items in the source's order, or (d) reuse the source's distinctive coinages as labels. The
   authoring guide gives each of the four a worked "this is derivation / this is original" pair
   written in original prose.

4. **The short-citation rule (D-74), and the one conflict this brief resolves.** A public short
   citation is a **bibliographic pointer only**: author surname(s), year, short title, and **at most
   one structural locator no finer than a part or chapter number**. It may not contain any quoted
   phrase; any chapter *title* reused as the concept's own label; any page or page-range locator; or
   any sequence of locators across concepts that reconstructs a work's outline.

   **Conflict and resolution.** The source design recommended permitting page ranges in public
   citations as bibliographic rather than expressive. D-74 chose the stricter option. **D-74
   governs**, and this brief encodes chapter-level-only. One consequence needs a named carve-out:
   a **journal article's own page span is the article's bibliographic identity**, not an interior
   locator into a work. The resolution — write it into the spec and flag it for owner ratification at
   the EP-16 re-plan:
   - a `short_citation` on a **concept** carries no page span, ever, for any source type;
   - EP-5's `sources.yaml` `citation` field may carry a journal article's full page span, because
     that is the article's bibliographic record and is never rendered as a concept's locator; EP-5
     already pins `locator_granularity: chapter`, which this rule is the concept-side counterpart of;
   - the lint enforces the first rule on `short_citation` and exempts the `sources.yaml` `citation`
     field by literal path.

5. **Populate `sources.yaml`, and add the concept-facing lints.** EP-5 owns the schema, the loader,
   the generator and `docs/rights.md`; this brief **fills the rows** for every source the seed briefs
   will cite — the four content sources and the three critique-lens literatures — using EP-5's field
   set (`source_id` · `citation` · `rights_holder` · `access_basis` · `licence` · `reuse_class` ·
   `permitted_use` · `quote_budget_words` · `source_budget_words` · `locator_granularity` ·
   `in_local_index` · `redistributable` · `verified_at` · `verification_note`). Every source not
   affirmatively verified stays at `reference-only-pending-rights-check` with `verified_at: null`
   and an honest `verification_note`, which EP-5's generator already surfaces under its "rights not
   yet verified" heading. Do not add fields to EP-5's schema; record the verification detail from
   step 7 in `verification_note` and in `docs/rights-check-2026-P1.md`.

   **Lints added to `schema_check` here** (rule group `rights-*`) — these are concept-side and are
   new work; EP-5's own validator checks the source rows, and EP-6 runs the quotation-budget counter
   over `docs/**`, which this brief extends to the registry YAML fields:

   **Lints added to `schema_check` here** (rule group `rights-*`):
   - every concept `provenance.source_id` resolves to a `sources.yaml` record;
   - the `reuse_class` → `derivation_mode` matrix holds for every concept;
   - `short_citation` contains no quotation mark, no `p.`/`pp.`, no `\d+\s*[-–—]\s*\d+` page-range
     pattern;
   - no concept `label` string-matches an entry in the local reading manifest's chapter-title list
     (the manifest is read from **outside the repository tree** at lint time and is never committed;
     when it is absent the rule reports `skipped-no-manifest`, and the pre-publication packet treats
     a skipped run as a **finding**, not a pass);
   - the locator-sequence check: no two concepts from the same `source_id` may carry consecutive
     chapter locators in registry order more than twice in a row;
   - the quotation budget: ≤ 25 words in any single quoted span, ≤ 150 words per `source_id` across
     the whole registry, counted over every field that can hold a quote;
   - no committed file contains a `page_or_locator` value.

6. **The authoring guide** — `docs/authoring-guide.md`, the document EP-12/13/14 are executed
   against. Contents:
   - **The original-prose rule** and the four abridgement anti-patterns from step 3, each with an
     original-prose worked pair.
   - **Register rules (failure mode Y-7, authorial voice as authority).** Concept prose is plain,
     hedged and non-narrative. It states a *possible reading available to the clinician*, never a
     property of a person. Banned constructions, with rewrites: second-person address to the patient;
     "the patient is/feels/needs"; narrative vignette openings; aphorism; any sentence that would
     read as a finding if the hedge were deleted. The guide gives a **hedge-deletion test**: delete
     every hedging clause; if the remainder asserts something about a person, the prose fails.
   - **The `derivation_mode` decision tree** as a flowchart in text: what is the source's
     `reuse_class` → did you read the source → is the wording yours → is the *sequence* yours → which
     mode applies.
   - **A worked concept, end to end**, in original prose: an ordinary-concern counter-frame entry
     showing every provenance field populated, `derivation_mode: author-original`, an empty
     `tested_in`, a populated `contested_interpretations`, and its attestation record. Adapting the
     planning worked entries is permitted; copying anything from a copyrighted source is not.
   - **The per-concept attestation.** `registry/authoring-attestations.yaml`, one record per concept:
     `attestation_id` · `concept_id` · `author` · `date` · `sources_consulted[]` ·
     `derivation_mode` · `statement` (a fixed sentence the author affirms: prose is their own in
     wording, structure and sequence; no quoted phrase; no chapter title as a label; the local-only
     locator, if any, is not published) · `residual_concern` (nullable free text — the honest place
     for "this one is close to the source's framing"). A non-null `residual_concern` is surfaced in
     the rendered markdown and is a mandatory read for the D-29 clearance checkpoint (EP-52).
   - **Front matter:** issue-spotting, not legal advice.

7. **The rights check this brief owns (D-62).** For the two UNVERIFIED source families:
   - attempt verification through at least two independent routes (the publishing body's own terms
     page; a government-wide or institution-wide reuse policy; the document's own front matter in a
     copy the author already holds; an archived copy of the terms page);
   - record each attempt in EP-5's `verification_note` with the date and the outcome, including
     failures and their HTTP status, and the fuller narrative in `docs/rights-check-2026-P1.md`;
   - set `reuse_class` to `cc-by-4.0-compatible` and `verified_at` to the date **only** where the
     terms were actually read; otherwise leave `reference-only-pending-rights-check` with
     `verified_at: null` and say why;
   - write a short `docs/rights-check-2026-P1.md` recording the whole exercise, and a dated addendum
     under **D-62** in `DECISIONS.md` with the outcome per source family.

   **Either outcome is acceptable.** What is not acceptable is authoring prose *from* those sources'
   wording while they remain unverified — the matrix in step 2 already forbids it, and EP-14 is
   written to author its principle concepts as `reading-informed-original` against the conservative
   posture so it is not blocked either way.

8. **The reference-never-ingest rule for normative guidance (D-62).** Add a `normative_guidance: true`
   flag on sources that are governance or policy guidance rather than evidence. Any source with that
   flag **and** a non-commercial or share-alike licence is pinned to `reuse_class: reference-only`
   and may never take a `derivation_mode` other than `reference-only`. The checker enforces the pin.

9. **Wiring.** Extend `schema_check` with the `rights-*` rule group behind `--rights` (default on),
   add the group to the EP-6 pre-publication packet's checklist, and add a `docs/` cross-reference
   from `GOVERNANCE.md` §Public-safety to the citation rule.

10. **Tests** (`tests/ep/test_ep10.py`): fixture concepts exercising each matrix cell; a
    `reference-only` source with `derivation_mode: us-federal-work` fails; a `short_citation` with a
    page range fails; one with a curly quotation mark fails; a label matching a manifest chapter
    title fails; a 26-word quoted span fails; a 151-word per-source total fails; a committed
    `page_or_locator` fails; a missing attestation fails; a source/concept `reuse_class` mismatch
    fails; the manifest-absent path reports `skipped-no-manifest` rather than passing silently.

## Out of scope

- The `NOTICE` / `LICENSE` / `LICENSE-CONTENT` / `CITATION.cff` files themselves and REUSE conformance
  → **EP-5**.
- The leak-prevention CI workflow and the pre-publication packet's structure → **EP-6** (this brief
  adds checklist items to it, it does not rebuild it).
- Any concept content → **EP-12**, **EP-13**, **EP-14**.
- Cross-file lens-coverage validation and the rendered markdown → **EP-16**.
- The local corpus ingest pipeline and the local index → **EP-22**.
- The provenance drawer UI that surfaces these fields → **EP-45**.
- Legal review of the rights posture and the employment/IP clearance → **EP-52** (D-29); this brief
  produces the packet that checkpoint reads.
- Public README wording about rights → **EP-53**.

## Verification / acceptance

- `uv run python -m epppsynth.registry.schema_check --rights --include-examples` exits `0`.
- `uv run python -m epppsynth.registry.schema_check --rights --path tests/fixtures/ep10/page-range`
  exits `1` with the `rights-citation-locator` rule as the only violation.
- `uv run python -m epppsynth.registry.schema_check --rights --json` reports, per `source_id`, the
  quoted-word total and the concept count, and `"unverified_sources"` listing every source still at
  `reference-only-pending-rights-check` — this list is what EP-16's re-plan and EP-52's checkpoint
  read.
- `uv run pytest tests/ep/test_ep10.py -q` green, with a failing-fixture test per lint in step 5.
- `uv run ruff check .` and the project type check green.
- From the git root: `python tools/roadmap_check.py --context-budget EP-10` passes.
- `docs/rights-check-2026-P1.md` exists and records, per unverified source family, at least two
  attempted verification routes with dates and outcomes. A recorded failure is a pass for this
  criterion; an unrecorded one is not.
- Pre-publication packet (EP-6) re-run for *protected text*, *local paths* and *quotation budget*;
  output recorded in the completion note.
- *(judgement — author)* The authoring guide's hedge-deletion test is applied to its own worked
  example and the result is shown in the guide.
- *(judgement — author)* No sentence in any committed file quotes a copyrighted source, including in
  the rights-check write-up, where licence terms are **described**, never quoted.
- Commits: `feat(epppsynth): provenance, rights, citation rule, authoring guide (EP-10)` then
  `docs(roadmap): record EP-10 commit hash`.

## Parked → final-roadmap.md

- Re-running the rights check for any source family that stays `reference-only-pending-rights-check`
  through P1; if it is still unverified at the mode-(a) gate, EP-52 decides whether the dependent
  concepts ship.
- Automated licence-text fingerprinting (detecting a source's phrasing surviving into authored prose
  by n-gram overlap against the local reading corpus) — a stronger Y-8 guard than the structural lint.
- A machine-readable REUSE/SPDX expression per registry file, once the content licence set is stable.
- Ratification of the journal-page-span carve-out in step 4.
- Translation-time rights handling for `variant_of` records.
