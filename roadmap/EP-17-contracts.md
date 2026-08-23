# EP-17 — Contracts package

**Size:** M · **Mode:** n/a · **Core/Stretch:** core ·
**Depends on:** EP-1 (Toolchain, package skeleton, ADR framework, CI), EP-11 (Composer
specification) ·
**Blocks:** EP-18 (registry loader), EP-22 (corpus ingest and local index), EP-23 (engine
integration, re-plan P2), EP-28 (substance-tuple extractor)

## Context

This brief lands the type graph that every other P2 brief imports, and it is first in the phase for
one reason: **D-23 ("verbatim spans are never emitted") becomes a structural property here or it
never becomes one at all.** If the output bundle is a plain dict, or holds an `Any`, no later
discipline can prove a span cannot ride out with it. If it is a closed graph of frozen dataclasses
over an allowlisted set of leaf types, a short test proves it for every future change.

Implements: **D-23** (span isolation by type), **D-25** (input contract — eight enum fields plus one
free-text field), **D-73** (three-way per-field sensitivity declaration), **D-53**
(`counter_reading` and `insufficient_basis_clause` are structurally required composer fields),
**D-8** (no retention — the `UserUtterance` redaction), and the
`(contract_version, registry_version, template_version)` triple that makes every later golden test
and every reviewer citation meaningful. Lands **ADR-003** (output contract types and the
no-verbatim-field invariant).

**Already in the tree:** EP-1's `epppsynth/` uv workspace, the `src/epppsynth/` package skeleton,
pytest wired, `docs/adr/` with the ADR template, CI on `windows-latest` with a no-model test path.
EP-11's composer specification fixes the *wording* of the three-part emission contract and the names
of the required per-waypoint fields.

**Not in the tree:** any registry, loader, scoring or template. This brief writes **types and one
serializer, and no logic**. Nothing here reads a file, takes a clock reading, or branches on a
registry value.

## Safety preconditions

- **R-7 / R-19 (rights leakage), D-23.** The whole point of the brief. Guard: `SpanBearing` is a
  marker base class; `VerbatimSpan` and `SourcePanePayload` derive from it and live in their own
  module; the type-graph walk over `OutputBundle` asserts that no reachable type is a `SpanBearing`
  subclass, that no reachable field is typed `Any`, `object`, a bare `dict`/`list`/`tuple`, or a
  union containing any of those, and that every leaf type is on an explicit allowlist. A new field
  of an unlisted type fails the test — the invariant fails closed.
- **D-8 (no retention), R-18.** A free-text utterance that reaches a log defeats the retention claim
  in one line of careless debugging. Guard: `UserUtterance` is not a `str` subclass, exposes no
  string methods, and redacts through `__repr__`, `__str__` and `__format__`; extraction requires
  the explicit `for_quotation()` accessor. Tested against `repr`, `str`, f-strings, `%`-formatting,
  `logging`, `pprint`, and `json.dumps` (which must raise rather than serialize).
- **R-3 (stereotyping / inferred identity), D-25.** Guard: the sensitivity declaration is a frozen
  mapping in code, not a comment; every D-25 field carries exactly one of the three D-73 classes;
  a coverage test means a new field cannot be added unclassified.
- **R-2 (automation bias), D-48.** Guard: no numeric confidence field exists anywhere in the output
  types. `basis` is an ordinal enum (`declared` / `follows-from-declared` / `not-supported`) and
  integer scores are deliberately absent from every exportable type.
- **Public artifact.** Everything here is tracked and public. Re-run the EP-6 pre-publication items
  before commit: no local absolute paths, no host or user name, no corpus filenames, no index-root
  or model-root literals, no PHI-shaped strings, and every docstring example manifestly fictional.

## In scope

1. Create `src/epppsynth/contracts/` with `types.py`, `facets.py`, `versions.py`, `export.py`,
   `source_pane.py`, `typegraph.py`. Every record is `@dataclass(frozen=True, slots=True,
   kw_only=True)`. No module in the package performs I/O, imports `random`, `time`, `datetime`,
   `uuid` or `secrets`, or defines a method with a side effect.
2. **Input types.** `InputEnvelope` carrying the eight D-25 fields as closed enums — role ·
   encounter temporality · stated communication/information preference · stated decision-sharing
   preference · self-described framework · uncertainty tolerance · illness stage ·
   language/interpreter need — each enum containing the three mandatory escapes `UNKNOWN`,
   `NOT_RELEVANT`, `PREFER_NOT_TO_ANSWER` and **no default member**. Plus `Mode` (`A`/`B`/`C`),
   `RequestClass` (the declared shape of the ask, including the D-38(4) prohibited classes),
   `DeclaredFlags` (the operator's explicit hard-stop declarations), and `utterance: UserUtterance`.
3. **`UserUtterance`.** A frozen wrapper over one `str`, constructed with a length cap, whose
   `__repr__`, `__str__` and `__format__` all return `<redacted>`, which defines no `__iter__`,
   `__contains__`, `__len__`, `lower()`, `split()` or comparison operators, and whose only accessor
   is `for_quotation() -> str`. Its docstring states the rule in full: *this text is quoted verbatim
   back to the reader and is never tokenised, mined, or used to infer anything.*
4. **`facets.py`.** The D-73 declaration as a frozen mapping from each D-25 field to one of
   `INVARIANT`, `CLINICALLY_LOAD_BEARING`, `FRAMING_PLUS_ONE_PERMITTED_ADDITIVE_WAYPOINT`, each with
   a one-sentence `rationale` string. This mirrors `registry/facets.yaml` authored in P1; EP-18's
   loader cross-checks the two and fails closed on drift, so the declaration cannot rot in either
   direction.
5. **Output types.** `Citation` (concept id + source id + short citation, never a span) · `Waypoint`
   (`observation_frame`, `candidate_reading`, `counter_reading` **required**,
   `insufficient_basis_clause` **required**, `question`, `unknowns: tuple[str, ...]`, `basis`,
   `citations`) · `KnownsAndUnknowns` · `OutputBundle` (the three D-11 parts,
   `waypoints: tuple[Waypoint, ...]`, `versions: VersionTriple`, `mode`) · `Abstention`
   (`trigger: AbstentionTrigger`, `reason_text`, `versions`) · `HardStopBundle` (`stop_card`, and
   `waypoints` typed as an empty tuple — see EP-20) · `EscalationPanel`.
6. **Span isolation.** `source_pane.py` defines `SpanBearing`, `VerbatimSpan` and
   `SourcePanePayload`. Nothing in `types.py` imports it; an import-graph test asserts the edge runs
   one way only, so a span type can never become reachable from the bundle by an innocent import.
7. **`versions.py`.** `CONTRACT_VERSION` (a hand-bumped literal), the `UNAVAILABLE` sentinel string,
   and `VersionTriple(contract: str, registry: str, template: str)` where `registry` and `template`
   hold `UNAVAILABLE` when their loads did not succeed. The triple is a field of the *envelope*; it
   is never interpolated into escalation copy, which is what lets EP-20's panel stay byte-invariant
   while every emitted envelope still carries the triple.
8. **`export.py`.** The single `serialize_for_export(obj) -> str` chokepoint: canonical JSON, sorted
   keys, `ensure_ascii=False`, LF endings, floats forbidden anywhere in the tree, and an explicit
   `ExportRefused` for any object that is, or transitively reaches, a `SpanBearing`. Every golden
   file, every `--emit-bundle` output and any future export path goes through it, so it is exercised
   code and not a stub.
9. **`typegraph.py`.** `reachable_types(root)` walking dataclass field annotations transitively
   (resolving string annotations, unions and generic parameters), plus a
   `python -m epppsynth.contracts.typegraph OutputBundle` entry point that prints the reachable set
   and exits non-zero on any violation, so CI can call it without going through pytest.
10. Write `docs/adr/ADR-003-output-contract-types.md`: the allowlist rule, the `SpanBearing` marker,
    the chokepoint, and the named extension point for EP-36 (`model_identity` is an additive
    optional field on `OutputBundle`, never a new leaf type outside the allowlist).

## Out of scope

- Registry records, schema and loading — **EP-18**.
- Any scoring, filtering or selection type — **EP-19**, which registers its `SelectionResult` with
  the type-graph walk's root set.
- The guard chain and the escalation constants — **EP-20**.
- Template data format and `template_version` computation — **EP-21**.
- Rendering a source pane, and the span-leak canary — **EP-45** (provenance drawer) and **EP-46**
  (no-retention and no-egress harness).
- The logging filter that raises on a raw envelope — **EP-46**.
- Any export *affordance* for the reader; D-6 forbids it in v1. The chokepoint exists; the button
  does not. A v1.x export format is parked below.

## Verification / acceptance

1. `uv run pytest tests/contracts -q` — green.
2. `uv run python -m epppsynth.contracts.typegraph OutputBundle` — exits 0 and prints the reachable
   type set; **the type-graph walk finds no field capable of holding a span**. A companion test
   plants a `VerbatimSpan` field on a copy of `Waypoint` and asserts the walker exits non-zero.
3. Redaction suite: `repr(u)`, `str(u)`, `f"{u}"`, `"%s" % u`, `logging` at every level and `pprint`
   all yield `<redacted>` and never the text; `json.dumps(u)` raises `TypeError`;
   `u.for_quotation()` returns the text exactly.
4. `serialize_for_export(SourcePanePayload(...))` raises `ExportRefused`, and so does an
   `OutputBundle` with a span smuggled in through a subclass.
5. Coverage test: every D-25 field appears exactly once in the sensitivity mapping; adding a ninth
   field without a class fails the test.
6. No-float test: `serialize_for_export` raises on any float in the tree, and an AST scan finds no
   float literal under `src/epppsynth/contracts/`.
7. `uv run reuse lint` exits 0 after the new files (SPDX headers on every `.py`).
8. *(judgement — owner)* The three-part `OutputBundle` field names match EP-11's composer
   specification word for word; a mismatch is a bug in this brief, not in EP-11. `OutputBundle`
   carries **no** values-to-options field: that fourth part was deleted from the contract rather than
   left undeliverable, and re-adding a field for it here would re-open it by the back door.

## Parked → final-roadmap.md

- An actual export or share format for v1.x (D-6 defers it); the chokepoint is where it will attach.
- `lang` / `variant_of` on output records for a future non-English variant (zero-cost structuring
  now, no behaviour in v1, which is English-only and says so).
- A runtime "explain this bundle" introspection type that would surface the internal integer scores;
  deliberately excluded from v1 because D-48 keeps scores out of the reader's view.
