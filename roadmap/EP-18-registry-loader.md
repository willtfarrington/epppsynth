# EP-18 — Registry loader, schema versioning, migrations

**Size:** L · **Mode:** n/a · **Core/Stretch:** core ·
**Depends on:** EP-9 (Registry schema v0 — types, relations, IDs, versioning), EP-17 (Contracts
package) ·
**Blocks:** EP-19 (selection and ranking), EP-23 (engine integration, re-plan P2)

## Context

EP-9 decided what a concept *is*. This brief makes the decision executable: a strict loader that
turns `registry/*.yaml` into frozen in-memory records, refuses to start on anything it does not
fully understand, and produces the `registry_version` content hash that stamps every output.

Implements **D-15** (YAML/JSON registry, no ontology, no graph database), **D-45/D-46**
(`review_status` lifecycle — only `accepted` concepts are selectable, `blocked` and `deprecated`
are retained and published), **D-73** (the sensitivity declaration lives in the registry and is
cross-checked against contracts), and the registry leg of the version triple. Lands **ADR-002**
(registry schema and ID scheme) and **ADR-010** (schema migration policy).

The taxonomy is settled and this brief does not redesign it. IDs are `EPS.<TYPE3>.<NNNN>`, namespace
prefixed, type-tagged, zero-padded, never reused and never renumbered. Five concept types —
`given` (`GIV`), `function` (`FUN`), `principle` (`PRN`), `condition` (`CON`), `caution` (`CAU`) —
plus one supporting record kind, `question_template` (`QT`); there is no `framing` (`FRM`) kind —
it existed only for the deleted output part (iv), and its ID band is retired, never reused. Nine relation
kinds: `may_manifest_as`, `counter_hypothesis_of`, `invites`, `constrained_by`,
`contraindicated_when`, `out_of_declared_scope_when`, `alternative_reading`,
`evidence_for` / `evidence_absent_for` (one kind, two polarities), and `escalates_to`. To those,
P2 adds **`family`** (the diversity key consumed by EP-19), the closed **`question_intent`**
enumeration on `question_template` records, and the per-input-field **`sensitivity`** declaration.

**Already in the tree:** EP-17's contracts package, including `contracts.facets`. EP-9's authored
JSON Schema and the registry directory layout. EP-12/13/14's seed concepts and EP-16's validator
work exist by the time this brief runs, but this loader is the *runtime* path — EP-16's validator is
an authoring tool and the two share the schema files, not the code path.

**Not in the tree:** any selection, scoring or composition. The loader hands back a frozen registry
object and an index; it makes no judgement about which concepts an input should reach.

## Safety preconditions

- **A half-loaded registry is worse than no tool.** Guard: validation is all-or-nothing. On any
  error the loader raises `RegistryInvalid` carrying the complete structured error list and the CLI
  exits 2. There is no partial load, no "skip the bad file", and no warning-only mode.
- **A registry failure must not take the escalation panel with it.** Guard: `epppsynth.registry`
  imports nothing from `epppsynth.guard`, and EP-20's `emergency_escalation_only()` path is tested
  with this loader raising. That cross-check is an acceptance item in both briefs.
- **R-13 (registry accretion without provenance).** Guard: `provenance.source_id`,
  `derivation_mode`, `short_citation`, `review_status`, `confidence`, `cultural_scope` and
  `content_hash` are all required by schema; `additionalProperties: false` at every level so an
  unrecognised field is an error rather than a silent carry.
- **R-41 / D-14 (cultural flattening).** Guard: `cultural_scope.claims_universality` must be present
  and must be `false`; `true` is a load error, not a lint warning.
- **R-7 / D-74 (rights).** Guard: no registry field may hold a verbatim span. The loader rejects a
  `short_citation` containing a quotation mark, rejects any concept whose source is marked
  `redistributable: false` in `sources.yaml` and which carries a quotation-shaped field, and
  re-runs EP-10's chapter-level-locator rule. Referential integrity to `sources.yaml` is checked
  here as well as in CI, because the runtime must not load what CI would have rejected.
- **R-27 (prompt injection via registry content).** Guard: a lint pass rejects instruction-shaped
  strings in any prose field (imperative second person addressed to a model, "ignore previous",
  fenced-code or role-marker syntax). Registry text is data that gets rendered, never instruction.
- **Public artifact.** Schema files, migrations and error messages are all tracked. Re-run the EP-6
  pre-publication items; in particular, no error message may echo an absolute local path — paths in
  diagnostics are rendered relative to the workspace root.

## In scope

1. Create `src/epppsynth/registry/` with `model.py` (frozen record types), `loader.py`,
   `hashing.py`, `index.py`, `schema/` (the JSON Schema files, one per record kind) and
   `migrations/`.
2. **Strict schema validation.** Validate every file against its schema before constructing any
   record. `additionalProperties: false` everywhere; enums closed; required fields enforced by the
   schema rather than by constructor checks, so the schema stays the single source of truth.
3. **ID rules.** Parse and enforce the `EPS.<TYPE3>.<NNNN>` grammar; assert that the `TYPE3` segment
   agrees with the record's `type` field (a mis-typed relation target is then detectable without a
   lookup); assert global uniqueness; and assert that no ID appears in the committed
   `registry/retired-ids.txt` tombstone list. Retirement is `status: deprecated` plus a required
   `deprecation_reason` and an optional `superseded_by` — never deletion, never reuse.
4. **Relation validation.** For each of the nine relation kinds plus `family`: the target must
   exist, must be of a permitted type for that relation, and the edge must carry its required
   `basis` field. `counter_hypothesis_of` is checked **symmetric-complete** over `given` records —
   a `given` with no counter-hypothesis partner is a load error, which is what makes D-53's
   "counter-reading always available" reachable at runtime.
5. **Derived indexes.** Build, once, at load: the activation index keyed by `(facet, value)` so
   EP-19's gather step is a dict lookup and not a search; the `family` grouping; the
   `counter_hypothesis_of` adjacency; and the `question_template` index keyed by `question_intent`.
   All indexes are sorted mappings of sorted tuples, so iteration order never depends on insertion
   order or on `PYTHONHASHSEED`.
6. **`question_intent`.** Load the closed enumeration **from the schema file**, never hard-coded in
   engine code, and validate every `question_template` record against it. EP-21 consumes it for
   ordering; if a member is added in P1 no P2 code changes.
7. **Sensitivity cross-check.** Load `registry/facets.yaml` (the D-73 declaration with its written
   rationales) and assert it agrees exactly with `contracts.facets` on field set and class. Drift in
   either direction is a load error naming both sides.
8. **`schema_version` and migrations.** Every registry file carries `schema_version`. The loader
   holds an ordered upgrader chain of pure functions `v(n) -> v(n+1)`; an unknown *future* version
   is refused outright rather than guessed at; an old version is upgraded in memory and, with
   `--write`, on disk. Each migration ships with a fixture pair and a round-trip test. Migrations
   never touch prose.
9. **`registry_version`.** SHA-256 over the canonicalised registry, computed in `hashing.py` against
   a written canonicalisation spec: UTF-8, NFC normalisation, LF endings, keys sorted, lists sorted
   where order is not semantic (and explicitly *not* sorted where it is, with the semantic lists
   named), floats forbidden, comments and file boundaries ignored. Consequence: splitting one file
   into three, or reordering keys, does not change the hash; changing one character of prose does.
10. **Selectability.** The loaded object exposes `selectable()` (only `review_status: accepted`) and
    `all_records()` (everything, including `draft`, `blocked` and `deprecated`, which EP-16 renders
    under "withdrawn / not adopted"). Nothing downstream is allowed to filter by review status
    itself; EP-19 consumes `selectable()` only, asserted by a test.
11. **CLI subcommand** `epppsynth registry validate [--write] [--json]`, exit 0 clean, 2 invalid,
    emitting a stable sorted error list suitable for CI diffing.
12. Write `docs/adr/ADR-002-registry-schema-and-ids.md` and
    `docs/adr/ADR-010-schema-migration-policy.md`.

## Out of scope

- Authoring or editing any concept — **EP-12 / EP-13 / EP-14**; the lens protocol is **EP-15**.
- The rendered human-readable markdown of the registry — **EP-16**.
- The `sources.yaml` rights table itself and its generated `docs/rights.md` — **EP-10**; this brief
  only consumes it for referential checks.
- Scoring, gathering, diversity — **EP-19**.
- Templates and `template_version` — **EP-21**.
- The corpus index and anything derived from the reader's own copy — **EP-22**. The runtime registry
  path never touches it.

## Verification / acceptance

1. `uv run epppsynth registry validate` — exits 0 on the tracked registry.
2. `uv run pytest tests/registry -q` — green, including one planted-defect test per row: duplicate
   ID · dangling relation target · `TYPE3` segment disagreeing with the `type` field · a `given`
   with no `counter_hypothesis_of` partner · an unknown *future* `schema_version` ·
   `cultural_scope.claims_universality: true` · an unknown key under `additionalProperties: false` ·
   a `short_citation` containing a quotation mark · an ID present in `retired-ids.txt` ·
   a `facets.yaml` entry whose sensitivity class disagrees with `contracts.facets`. Each must exit 2
   with exactly one error naming the offending ID.
3. **Hash stability:** `uv run pytest tests/registry/test_hashing.py -q` asserts that shuffling key
   order, reordering records within a file, and splitting one file into three all yield the
   identical `registry_version`, while changing a single character of prose changes it.
4. **Order independence:** loading the registry in five subprocesses with different `PYTHONHASHSEED`
   values yields byte-identical serialized indexes.
5. Migration round-trip: `uv run pytest tests/registry/test_migrations.py -q` upgrades each shipped
   fixture from its authored version to current and asserts the result validates and hashes stably.
6. Cross-brief check with EP-20: with the loader forced to raise `RegistryInvalid`,
   `emergency_escalation_only()` still returns the panel. The test lives in `tests/guard/` and is
   listed in both briefs.
7. *(judgement — owner)* The canonicalisation spec's list of "order is semantic" fields is correct;
   getting it wrong makes the hash either unstable or insensitive.

## Parked → final-roadmap.md

- A registry diff tool that explains *why* `registry_version` changed between two commits
  (valuable for reviewer sign-off, not needed for v1).
- Cross-registry federation or importing a second registry namespace; v1 is one registry.
- A downgrade path in the migration chain. v1 is upgrade-only; a downgrade would need a policy on
  lossy fields that no v1 use case requires.
