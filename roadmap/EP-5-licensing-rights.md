# EP-5 — Licensing pack + per-source rights table

**Size:** L · **Mode:** n/a · **Core/Stretch:** core ·
**Depends on:** EP-2 (canonical docs + public front matter + badge scheme) · **Blocks:** EP-6 (leak-prevention CI), EP-8 (roadmap tooling, re-plan P0), EP-10 (provenance and authoring guide)

## Context

This project's central rights problem is a public repository whose conceptual substrate cannot be
redistributed. D-10 resolves it with two paths: the **public** artifact is a hand-authored,
cited, original-prose conceptual model; the **local** path builds a gitignored index from the
reader's own legally obtained copy and ships no derived content. EP-5 makes that resolution
machine-checkable. It is the brief that turns "we do not redistribute" from a posture into a
constraint the build enforces.

EP-5 precedes EP-6 for a specific reason recorded in the P0 ordering rationale: **the leak scanners
enforce the rights table's rules.** A scanner cannot assert "no concept sourced from a
non-redistributable entry carries a verbatim field" until the rights table exists and defines
`redistributable`.

**What exists.** Canonical docs, `SAFETY.md` with the D-74 quotation limits stated, the four
policy documents, the uv project, and a `README.md` carrying two named placeholders EP-2 left for
the licence split and the citation. `pyproject.toml` declares the SPDX identifier `Apache-2.0` and
nothing else about licensing.

**What this brief creates.** The REUSE-conformant licensing layout, `NOTICE`, `CITATION.cff`, the
`registry/sources.yaml` schema with its generator, and the generated `epppsynth/docs/rights.md`.

**The licence boundary** (D-28, D-50), stated once here and enforced by `REUSE.toml`:

| Licence | Paths |
|---|---|
| Apache-2.0 | `epppsynth/src/**`, `epppsynth/tests/**`, `tools/**`, `epppsynth/schemas/**`, `pyproject.toml`, `.github/**` |
| CC BY 4.0 | `epppsynth/docs/**`, `epppsynth/registry/**`, `epppsynth/templates/**`, `roadmap/**`, `epppsynth/DESIGN.md`, `epppsynth/GOVERNANCE.md`, `epppsynth/DECISIONS.md`, `SAFETY.md`, `PRIVACY.md`, `README.md` |

`templates/**` is CC BY 4.0 by D-50: they are authored prose loaded by code, and their value is the
wording.

Implements: D-10 (both rights paths), D-28 (Apache-2.0 code + CC BY 4.0 content, `NOTICE`,
`CITATION.cff`, per-source rights table), D-50 (templates are content), D-62 (`reuse_class` per
source; WHO LMM is CC BY-NC-SA 3.0 IGO and is **referenced, never ingested**; SAMHSA and AHRQ reuse
terms are **UNVERIFIED** and are `reference-only-pending-rights-check`; the FDA CDS final guidance
of 2026-01-06 is **UNVERIFIED** and must be read before any public intended-use language ships),
D-74 (chapter-level locators only; ≤ 25 words per quote, ≤ 150 per source). Mitigates R-7
(copyright / derivative distribution) and R-15 (licence contamination — NC/SA or unverified federal
text entering a CC BY 4.0 tree).

## Safety preconditions

| Invariant at risk | Guard in this brief |
|---|---|
| Licence contamination (R-15, D-62) | `sources.yaml` carries a required `reuse_class` per source with a **closed** enumeration: `cc-by-4.0-compatible`, `reference-only`, `reference-only-pending-rights-check`, `owner-copy-read-as-input`. The generator refuses to emit `docs/rights.md` if any source used by any concept has `reuse_class: reference-only*` and a non-empty verbatim field. WHO LMM is recorded as `reference-only` with its CC BY-NC-SA 3.0 IGO licence named; SAMHSA and AHRQ are recorded as `reference-only-pending-rights-check` with the HTTP 403 observation and the date. |
| An unverified source silently becoming a verified one | Every `reuse_class: *-pending-rights-check` row carries a `verified_at: null` field and a `verification_note`. The generator emits them into `docs/rights.md` under a visibly separated **"rights not yet verified"** heading. The rights table is allowed to say "we do not know"; it is not allowed to imply that we do. |
| The corpus becoming redistributable by accident (D-10, R-7) | The owner's purchased copy is a row with `access_basis: owner-purchased-copy`, `redistributable: false`, `in_local_index: true`, `permitted_use: read-as-input, short-citation-in-docs`, and `redistribution: none`. The CI rule EP-6 enforces is written and tested here as a library function so EP-6 wires an already-proven check. |
| Quotation budget unenforced (D-74) | The budget — ≤ 25 words per quote, ≤ 150 words per source — is expressed as data in `sources.yaml` (`quote_budget_words`, `source_budget_words`) with the D-74 defaults, and a counter function is written and unit-tested here. EP-6 runs it in CI over `epppsynth/docs/**`. |
| Chapter-level locators only (D-74) | The schema's `locator` field is constrained to a chapter-level pattern; page ranges fail validation. The standing bans are recorded in the schema documentation: no quoted phrase as a concept label, no chapter title as a concept label, no locator sequence that reconstructs a source's outline. |
| A public README claiming a licence the tree does not implement | Step 11 asserts that every tracked file maps to exactly one licence by the `REUSE.toml` rules, and that the README's licence-split paragraph names exactly the boundary in the table above. |

Pre-publication checklist items exercised here: **3 (protected text — the length-threshold check for
quoted spans is built here)**, **6 (licence conformance)**, **7 (public claims — `CITATION.cff` must
agree with the README and the badge)**.

## In scope

1. **`LICENSES/`** with the full texts: `LICENSES/Apache-2.0.txt` and `LICENSES/CC-BY-4.0.txt`
   (REUSE layout).
2. **`LICENSE`** at the repository root = the Apache-2.0 text, so GitHub's licence detection sees
   the code licence. **`LICENSE-CONTENT`** retained per D-40 as a short pointer file naming CC BY
   4.0 and `LICENSES/CC-BY-4.0.txt`, not a duplicate of the text.
3. **`REUSE.toml`** implementing the boundary table above as path-pattern annotations, so YAML and
   markdown trees need no per-file headers. Add SPDX headers only to `.py` files
   (`# SPDX-License-Identifier: Apache-2.0` and a copyright line).
4. **`NOTICE`** (Apache-2.0 §4(d)): project name and copyright; the dual-licence split stated with
   the **exact path boundaries**; third-party attributions for anything vendored (nothing is
   vendored yet — state that explicitly rather than leaving the section empty); a pointer to the
   rights table; and the rights-posture sentence, which must appear verbatim: *this repository
   contains no third-party copyrighted source text; the concept registry is original prose that
   cites its sources* (D-10(i)).
5. **`CITATION.cff`**, CFF 1.2.0: `cff-version`, `message`, `title`, `authors`, `type: software`,
   `repository-code`, `version` tracking the badge (`0.0.0` while `status: design`),
   `date-released`, `license: Apache-2.0`, and an `abstract` that (a) uses the D-24 wording,
   (b) states the **content** licence because CFF has only one licence field, and (c) ends with
   "Work in progress; not validated; not for clinical use." Populate `references:` with the D-14
   traditions so anyone citing the software is pointed at the primary sources.
6. **`epppsynth/registry/sources.yaml`** — the schema and the first rows. Required fields per
   source: `source_id` · `citation` (author, title, year, publisher, edition, DOI/ISBN) ·
   `rights_holder` · `access_basis` (owner-purchased-copy | open-access | public-domain |
   government-work) · `licence` (SPDX id or `all-rights-reserved`) · `reuse_class` (closed
   enumeration, above) · `permitted_use` (read-as-input | short-citation-in-docs |
   redistribution-none, multi-valued) · `quote_budget_words` (default 25) ·
   `source_budget_words` (default 150) · `locator_granularity` (fixed: `chapter`) ·
   `in_local_index` (bool) · `redistributable` (bool) · `verified_at` · `verification_note`.
   Seed the rows the plan already knows: the owner's purchased primary text; the SAMHSA
   trauma-informed guidance; the AHRQ material; the WHO LMM guidance; the serious-illness
   communication literature; the moral-injury literature; and the FDA CDS final guidance
   (2026-01-06) as a `reference-only` regulatory reference marked **UNVERIFIED — must be read
   before any public intended-use language ships** (D-62).
7. **Generator + validator** at `epppsynth/src/epppsynth/rights/`:
   - `load_sources()` with schema validation (closed enumerations, required fields, the
     chapter-only locator pattern);
   - `render_rights_md()` → `epppsynth/docs/rights.md`, with the unverified rows under their own
     heading;
   - `check_source_refs(registry_paths)` — every `concept.provenance.source_id` resolves. The
     registry does not exist yet (**EP-9**), so this function is written against the schema
     contract and unit-tested on fixtures; it becomes live at EP-10.
   - `check_no_verbatim_from_nonredistributable(...)` — the D-10 rule, as a function.
   - `count_quotations(paths)` — the D-74 budget counter.
   Every one of these is a library function with unit tests, so EP-6 wires proven code into CI
   rather than inventing checks under time pressure.
8. **Generate `epppsynth/docs/rights.md`** and commit it. It is generated, and the generator is the
   source of truth; add a header line saying so and naming the command that regenerates it.
9. **Fill the two README placeholders** EP-2 left: the licence-split paragraph (matching the table
   above exactly) and the citation paragraph pointing at `CITATION.cff`.
10. **Validate `CITATION.cff`.** Use a CFF validator available through `uv run` — do not assume a
    system binary. Record which validator was used and its version.
11. **Licence-coverage assertion.** Write and run a check that every tracked file maps to exactly
    one licence under `REUSE.toml`, with zero unmatched files and zero doubly-matched files. Run
    `reuse lint` if the tool installs cleanly under `uv run`; if it does not, the coverage
    assertion above is the acceptance path and the completion note says so.
12. **Commits:** `feat(epppsynth): add licensing pack and per-source rights table (EP-5)` then
    `docs(roadmap): record EP-5 commit hash`.

## Out of scope

- Wiring any of these checks into CI or a pre-commit hook — **EP-6**. EP-5 ships tested functions;
  EP-6 ships enforcement with a deliberate red run.
- Populating the rights table with the concepts that cite each source — **EP-10** (provenance and
  authoring guide), because a `source_id` reference needs a registry to reference it from.
- The registry schema itself, and the `cultural_scope` / `review_status` / `contested_interpretations`
  fields — **EP-9**.
- CycloneDX SBOM generation and `epppsynth/docs/third-party-licenses.md` — **EP-50** (per release,
  not per commit). Named in `NOTICE` as planned.
- Resolving the SAMHSA and AHRQ rights questions, and reading the FDA CDS final guidance. Both are
  **owner-gated research tasks**, not code; they are recorded as unverified here and are carried as
  P1 blockers for any public intended-use language (**EP-10**).
- The vendored htmx attribution (0BSD, with path, version and SHA-256) — **EP-40**, when htmx is
  actually vendored. `NOTICE` states today that nothing is vendored yet.
- Model licences and their acceptable-use clauses — **EP-7** records the metadata shape;
  **EP-34** screens them by hand, because no scanner reads them.

## Verification / acceptance

Runnable, from the repository root unless noted:

```powershell
# REUSE layout present
Test-Path LICENSE, LICENSE-CONTENT, NOTICE, CITATION.cff, REUSE.toml,
          LICENSES/Apache-2.0.txt, LICENSES/CC-BY-4.0.txt

# every tracked file maps to exactly one licence
uv run python -m epppsynth.rights.coverage --check      # → exit 0, prints 0 unmatched, 0 doubly-matched

# rights table regenerates byte-identically (it is generated, so drift is a bug)
uv run python -m epppsynth.rights.render --out epppsynth/docs/rights.md
git diff --exit-code epppsynth/docs/rights.md            # → no diff

# schema validation and the two rights rules
uv run pytest epppsynth/tests/test_rights.py -q

# a deliberately injected dangling source_id fails
uv run python -m epppsynth.rights.check --fixture epppsynth/tests/fixtures/dangling_source.yaml  # → non-zero

# CFF validates
uv run python -c "import yaml,pathlib; yaml.safe_load(pathlib.Path('CITATION.cff').read_text(encoding='utf-8'))"
# plus the chosen CFF validator, recorded by name and version in the completion note

# NOTICE carries the rights-posture sentence verbatim
Select-String -Path NOTICE -SimpleMatch `
  'this repository contains no third-party copyrighted source text'

# no page-range locator anywhere
Select-String -Path epppsynth/registry/sources.yaml -Pattern 'pp?\.\s*\d+\s*[-–]\s*\d+'   # → no output
```

Acceptance:

1. All seven licensing files exist and `reuse lint` exits 0 — **or**, if `reuse` does not install
   cleanly, the coverage check reports zero unmatched and zero doubly-matched tracked files and the
   completion note records why the substitute path was used.
2. `CITATION.cff` validates, its `version` is `0.0.0`, its `license` is `Apache-2.0`, and its
   abstract names the content licence and ends with the required sentence.
3. `NOTICE` states the dual-licence split with exact path boundaries, contains the rights-posture
   sentence verbatim, and explicitly states that nothing is vendored yet.
4. `epppsynth/registry/sources.yaml` validates against the schema; every row has a `reuse_class`
   from the closed enumeration; the WHO LMM row is `reference-only` with CC BY-NC-SA 3.0 IGO named;
   the SAMHSA, AHRQ and FDA rows are `reference-only-pending-rights-check` / `reference-only` with
   `verified_at: null` and a dated `verification_note` recording the HTTP 403 observations.
5. `epppsynth/docs/rights.md` regenerates with no diff, and its unverified rows appear under a
   separate, clearly titled heading.
6. `check_no_verbatim_from_nonredistributable` **fails** on a planted fixture in which a concept
   sourced from a `redistributable: false` row carries a verbatim field, and passes on the clean
   fixture. Both runs recorded.
7. `check_source_refs` **fails** on the planted dangling-`source_id` fixture.
8. `count_quotations` reports zero over-budget quotes across `epppsynth/docs/**` and `SAFETY.md`,
   and **fails** on a planted 30-word quotation. Recorded.
9. No page-range locator exists anywhere in `sources.yaml` or in `epppsynth/docs/**`.
10. The README's licence-split paragraph matches the boundary table exactly, and the citation
    paragraph resolves to `CITATION.cff`.
11. `uv run pytest -q` and CI green.
12. *(judgement — the project owner)* Reading `epppsynth/docs/rights.md` alone makes clear, for each
    source, what the project may do with it, what it may never do, and whether anyone has actually
    checked.

## Parked → final-roadmap.md

- Resolving SAMHSA and AHRQ reuse terms (both returned HTTP 403 at research time) and reading the
  FDA CDS final guidance of 2026-01-06. Carried as an explicit P1 blocker for public intended-use
  language, not as a nice-to-have.
- A licence-compatibility policy engine for dependencies (permissive-only allow-list; copyleft or
  ambiguous halts the release). Belongs with the release evidence bundle at EP-50.
- Per-file SPDX headers in markdown. `REUSE.toml` path patterns cover them; revisit only if a
  downstream consumer needs per-file granularity, which D-33 makes unlikely in v1.
- Registering a DOI for the software (Zenodo or equivalent) so `CITATION.cff` can carry one.
  Premature while nothing is released; revisit at EP-52.
- Generalizing the rights table into a reusable schema for the sibling projects. Noted because the
  shape is not project-specific; out of scope for v1.
