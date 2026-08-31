# EP-22 — Corpus ingest module and local index

**Size:** L · **Mode:** n/a · **Core/Stretch:** core ·
**Depends on:** EP-7 (storage inventory), EP-17 (contracts package), EP-21 (template composition,
linters, CLI) ·
**Blocks:** EP-23 (engine integration, re-plan P2)

## Context

`tools/epub_to_md_pipeline.py` is the repository's oldest code and, until EP-1, its only code. D-41
moves it into the package as the corpus-ingest module, reachable as a CLI subcommand, because
D-10(ii) and D-16 make local corpus ingest a **product path** — the authoring aid that turns the
reader's own legally obtained copy into a local, gitignored derived index — rather than a one-off
script. Its *content* is independent of the engine, but it is **not** parallelisable with EP-21:
step 8 registers `epppsynth corpus ingest` with the CLI that EP-21 builds, so EP-21 must land
first.

Implements **D-41** (the move and the subcommand), **D-16** (the local index may hold derived text
from the reader's own copy, strictly local, gitignored, never distributed, never in CI), **D-51**
(the index root is separate from the model root: different rights class, independently purgeable and
backup-excludable), **D-78/D-49** (the storage floor and the project ceiling, checked before *and*
after every write), and the standing toolchain fact that **pandoc is absent on the target
machine** and may not be assumed.

**Three constraints shape every decision below.**

1. **Pandoc may not be assumed.** The default path is pure Python. Pandoc remains available as an
   explicitly selected, probed, documented prerequisite, and CI never exercises it.
2. **Nothing derived from the corpus enters the repository.** The corpus and the derived index live
   outside the repository tree at the configured index root (D-51), are gitignored, never enter CI,
   and index-dependent tests are skip-marked so CI stays green with no index present. This brief
   refers to that root by its configuration name, `EPPP_INDEX_ROOT`, and never writes the literal
   path into a tracked file — EP-6's leak scanners search tracked files for index-root strings, and
   the roadmap is a tracked file.
3. **The existing script's hard-coded spine is itself a rights exposure.** Its document table
   reproduces a copyrighted book's chapter titles and its complete outline sequence in a tracked,
   public file. D-74 bans exactly that (no chapter title reused as a label, no locator sequence that
   reconstructs the outline), and R-7/R-19 name the hazard. Moving the file into the package without
   fixing this would carry the exposure forward and make it look deliberate. Externalising the spine
   is therefore in scope and is the first substantive step.

> **Owner ruling note (2026-08-31, OD-6).** Constraint 3 was ruled a **live** exposure rather than a
> latent one and was **closed ahead of this brief**, under the dated addendum to D-74. The book
> title, the author and the chapter-title table now live in `tools/spine.local.json`, gitignored,
> with `tools/spine.local.json.example` shipped carrying placeholder rows; the script loads the
> spine at run time and exits with a pointer to the example when it is absent. So EP-22 **inherits
> an already-external spine**: its job is no longer to externalise it but to **keep** it external
> across the move into the package — same file, or a documented successor under the configured
> index root — and to carry the loader and its missing-config exit path into the module. The
> paragraph above is left as written; it is the record of why the spine is where it is.

**Already in the tree:** `tools/epub_to_md_pipeline.py` (EPUB XHTML in, per-chapter Markdown plus a
routing index and a manifest out; endnote and footnote inlining; a BeautifulSoup pre-processing
pass; a pandoc subprocess for the HTML-to-Markdown conversion; a hard-coded document table). EP-7's
storage roots, `preflight_space()` and the ceiling check. EP-17's contracts, including the
`SpanBearing` marker that any span type produced here must derive from.

**Not in the tree:** any embedding model, any vector index, any retrieval. This brief builds the
**derived-text index and its manifest** only.

## Safety preconditions

- **R-7 / R-19 (rights leakage into a public artifact), D-10, D-16, D-74.** Guards, layered:
  the spine descriptor moves out of the tree (step 2); the module contains no book title, author,
  chapter title or locator; every output path is asserted to be under the configured index root and
  **refused if it resolves inside any git working tree** (walk up for `.git`); the manifest is
  written to the index root only; EP-6's scanners cover corpus filenames and index-root strings in
  tracked files; index-dependent tests are skip-marked and CI runs with no index.
- **R-15 (licence contamination).** Guard: the pure-Python converter is written against the existing
  permissively licensed dependencies (`beautifulsoup4`, `lxml`). A copyleft HTML-to-Markdown library
  is explicitly rejected and named as rejected in the ADR addendum, so a later session does not
  "helpfully" add one. Any new dependency must clear the P0 permissive-only allow-list.
- **D-78 / D-49 (storage).** Guard: `preflight_space()` runs before and after every write with the
  250 GiB binary floor; the combined model-plus-index footprint is checked against the 20 GB warning
  and the 25 GB hard stop; a run that would breach either refuses before writing a byte and exits
  with a distinct code.
- **ADR-007 path safety.** Guard: the ingest reuses the descendancy rules — fully resolve root and
  target following junctions, require the target to be a strict descendant with at least four path
  parts, reject drive roots, the user profile, system directories and any repository working tree,
  and reject unresolved environment variables, `~`, and glob characters. The ingest **never
  deletes**; it writes into a fresh output directory and refuses a non-empty one without
  `--overwrite`.
- **Engine isolation.** Guard: an import-graph test asserts no module under `contracts`, `registry`,
  `select`, `guard` or `compose` imports `epppsynth.corpus`, and that `corpus` imports nothing from
  `select`, `guard` or `compose`. Corpus ingest is authoring tooling that ships in the package and
  is never invoked by the synthesis path.
- **Public artifact.** The module, its tests and its example descriptor are tracked and public.
  Re-run the EP-6 pre-publication items, and additionally grep the diff for the source book's title,
  author and any chapter title before commit.

## In scope

1. **Move.** `git mv tools/epub_to_md_pipeline.py` into `src/epppsynth/corpus/`, then split it in a
   second commit so history survives the move: `epub.py` (container and OPF reading, document
   enumeration), `html_to_md.py` (the converter), `notes.py` (endnote and footnote collection and
   inlining), `spine.py` (descriptor loading and validation), `manifest.py`, `ingest.py` (the
   orchestrator). Remove `tools/` if nothing non-package remains in it (D-41).
2. **Externalise the spine.** The hard-coded document table becomes a `spine.toml` descriptor read
   from the index root: per entry, the source document name, an output slug, a kind
   (`front` / `part` / `chapter` / `back`), an optional ordinal, and a title string. The package
   ships `spine.example.toml` describing a **manifestly fictional** work — *The Lantern-Keeper's
   Almanac* by A. Fictitious — and nothing else. `spine.py` validates the descriptor: unique slugs,
   monotonic ordinals, every named source document present in the container. A CI check asserts no
   tracked file contains a spine table with more than the example's entries.
3. **Pure-Python converter, default.** Extend the existing inline-element walker to block level:
   headings, paragraphs, lists, block quotes, tables, pre-formatted text, horizontal rules, images
   mapped through the existing decorative-glyph table, and the existing page-marker comments. Output
   is GitHub-flavoured Markdown with no wrapping. Deterministic: the same input yields
   byte-identical output, asserted by test. No new dependency.
4. **Pandoc as an opt-in, probed prerequisite.** `--converter {python,pandoc}` defaults to `python`.
   Selecting `pandoc` runs a `shutil.which("pandoc")` probe first and, on absence, exits with a
   distinct code and an actionable message naming the prerequisite and the fact that the Python path
   needs no install. Pandoc is never invoked implicitly, never probed unless selected, and never
   exercised in CI. Document it in `docs/` as a confirmed optional prerequisite, not an assumption.
5. **Paths and storage.** All output goes under `EPPP_INDEX_ROOT` (D-51), resolved through EP-7's
   configuration, with the ADR-007 descendancy checks and the floor and ceiling checks from the
   safety preconditions. Refuse an output path inside any git working tree. Log pre- and post-write
   free space.
6. **Manifest.** `index-manifest.json` at the index root: schema version, spine descriptor hash,
   converter used and its version, per-file records (slug, source document, kind, ordinal, word
   count, SHA-256 of the derived file), a `sources.yaml` row reference, and the constants
   `in_local_index: true` and `redistributable: false`. The manifest lives outside the tree, so it
   may hold titles; nothing tracked ever does.
7. **Run banner and rights notice.** Every ingest run prints, before doing anything: the index root
   (resolved at runtime, never baked in), the rights-table row id, and the statement that the
   derived text is non-redistributable, is excluded from Git and CI, and exists only for the
   reader's own local use.
8. **CLI.** Register `epppsynth corpus ingest --spine PATH --source PATH [--out PATH]
   [--converter {python,pandoc}] [--overwrite] [--dry-run]` with EP-21's CLI. `--dry-run` prints the
   plan — files, byte estimates, target paths, space before and after — and writes nothing.
9. **Skip-marking.** Register a `requires_index` pytest marker in `pyproject.toml`; CI runs
   `-m "not requires_index"`. Two meta-tests keep the arrangement honest: one asserts at least one
   test carries the marker (so it cannot be silently deleted), and one asserts no marked test is
   collected under the CI selection.
10. **Fixture.** A small hand-authored EPUB under `tests/fixtures/corpus/` containing the fictional
    work from step 2 — original text written for this test, four short documents, one endnote, one
    footnote, one decorative glyph, one table — so the converter has a public-safe end-to-end case
    that runs in CI with no index and no corpus.
11. **ADR addendum** to ADR-007: corpus ingest is authoring tooling, never on the synthesis path;
    the spine lives outside the tree; the copyleft converter library is rejected by name; pandoc is
    optional and probed.

## Out of scope

- Embeddings, a vector index, or any retrieval over the corpus — the embedding-model rubric is
  **EP-34** and the local source pane that reads spans is **EP-45**, with its isolation and the
  span-leak canary verified in **EP-46**. Nothing on the synthesis path ever reads the index
  (**EP-19**).
- Any cache-purge or deletion tool. ADR-007's seven rules are written in **EP-7**; no purge tool is
  built in v1.
- Authoring concepts from the ingested text — **EP-12 / EP-13 / EP-14**; the rights table itself is
  **EP-10**.
- Generalising the ingest beyond its current single-book spine. Parked by D-41 and repeated below.
- The storage roots, `preflight_space()` and the ceiling implementation — **EP-7**; this brief calls
  them.

## Verification / acceptance

1. `uv run epppsynth corpus ingest --help` — exits 0 and shows the subcommand registered.
2. `uv run pytest tests/corpus -q -m "not requires_index"` — green on a machine with **no index and
   no corpus present**, which is also exactly what CI runs.
3. End-to-end on the fictional fixture: `uv run epppsynth corpus ingest --spine
   tests/fixtures/corpus/spine.toml --source tests/fixtures/corpus/lantern-keeper/ --out <temp dir>`
   produces four Markdown files, the routing index and the manifest; a second run into a second temp
   directory is **byte-identical** apart from the resolved root recorded in the manifest, which is
   excluded from the comparison.
4. Path refusal: a test asserts the ingest exits non-zero, before writing, when `--out` resolves
   inside a git working tree, when it is a drive root, when it contains an unresolved environment
   variable or a glob character, and when it is a non-empty directory without `--overwrite`.
5. Storage refusal: with `preflight_space()` stubbed to report the floor breached, the run exits
   with the distinct storage code and creates no file; the same for the 25 GB project ceiling, and a
   warning-only path at 20 GB.
6. Pandoc absence: with `shutil.which` patched to return `None`, `--converter pandoc` exits with the
   documented code and message; `--converter python` on the same input succeeds. No test invokes
   pandoc.
7. Isolation: `uv run python -m epppsynth.tools.import_graph --forbid-edge
   epppsynth.select,epppsynth.compose,epppsynth.guard,epppsynth.registry,epppsynth.contracts
   --to epppsynth.corpus` exits 0.
8. Marker meta-tests green; `uv run pytest --collect-only -m requires_index -q` lists a non-empty
   set locally and collects nothing under the CI selection.
9. Leak checks: `uv run epppsynth scan` (the scanner CLI built in EP-6) green on the tree, and a
   manual grep of the diff for the source book's title, author and chapter titles returns nothing.
10. *(judgement — owner)* The pure-Python converter's output is good enough to author from. If it is
    not, the honest outcome is to keep pandoc as a documented prerequisite for the owner's own runs
    and record that as a dated addendum, not to silently depend on it.

## Parked → final-roadmap.md

- **Generalising the ingest beyond the single-book spine** (D-41, explicitly parked): auto-detecting
  the spine from the container's own manifest, supporting other container formats, multi-work
  ingest.
- The embedding index and any similarity search over the derived text.
- A resumable or incremental ingest; v1 re-runs the whole spine.
- Bundling a pure-Python converter as a standalone package for reuse.
