# SPDX-FileCopyrightText: 2026 W. Taylor Farrington
# SPDX-License-Identifier: Apache-2.0
"""Load and validate `epppsynth/registry/sources.yaml`.

Validation collects every problem and raises once, because a rights file with
four faults should report four faults. The rules are the closed enumerations of
`model.py` plus the cross-field consistency the file's own header states: a row
may not say it is non-redistributable in one field and redistributable in
another, and it may not claim a local index entry for a source nobody owns a
copy of.

The budgets are checked as an upper bound, never as an equality: a row may set a
stricter quotation budget than D-74's, and may never set a looser one.
"""

from __future__ import annotations

import pathlib
from typing import Any

import yaml

from .model import (
    ACCESS_BASES,
    DEFAULT_QUOTE_BUDGET_WORDS,
    DEFAULT_SOURCE_BUDGET_WORDS,
    ISO_DATE_RE,
    LICENCE_RE,
    LOCATOR_GRANULARITIES,
    PAGE_RANGE_RE,
    PERMITTED_USES,
    REDISTRIBUTION_MODES,
    REUSE_CLASSES,
    SOURCE_ID_RE,
    SOURCE_KINDS,
    Citation,
    RightsError,
    Source,
    SourceRegistry,
)
from .paths import sources_yaml

SCHEMA_VERSION = 1

_SOURCE_FIELDS = (
    "source_id",
    "source_kind",
    "citation",
    "rights_holder",
    "access_basis",
    "licence",
    "reuse_class",
    "permitted_use",
    "redistribution",
    "quote_budget_words",
    "source_budget_words",
    "locator_granularity",
    "in_local_index",
    "redistributable",
    "verified_at",
    "verification_note",
)

_CITATION_FIELDS = ("author", "title", "year", "publisher", "edition", "doi_or_isbn")

#: A `source-family` is a body of literature, so these have no value for one and
#: must be null. Recording a family's "publisher" would be a false precision.
_FAMILY_NULL_FIELDS = ("author", "year", "publisher", "edition", "doi_or_isbn")


def load_sources(path: pathlib.Path | str | None = None) -> SourceRegistry:
    """Parse, validate and return the source rights record.

    Raises `RightsError` listing every problem found.
    """
    target = pathlib.Path(path) if path is not None else sources_yaml()
    if not target.is_file():
        raise RightsError(f"source rights record not found: {target}")

    raw_text = target.read_text(encoding="utf-8")
    problems: list[str] = []

    # D-74's locator rule, checked as text: a page range is a leak wherever it
    # appears in this file, including inside a note.
    for match in PAGE_RANGE_RE.finditer(raw_text):
        line = raw_text.count("\n", 0, match.start()) + 1
        problems.append(f"line {line}: page-range locator {match.group(0)!r} (D-74 bans these)")

    try:
        document = yaml.safe_load(raw_text)
    except yaml.YAMLError as exc:  # pragma: no cover - exercised only on malformed YAML
        raise RightsError(f"{target}: not valid YAML: {exc}") from exc

    if not isinstance(document, dict):
        raise RightsError(f"{target}: top level must be a mapping")

    problems.extend(_check_header(document))
    sources: list[Source] = []
    rows = document.get("sources")
    if not isinstance(rows, list) or not rows:
        problems.append("`sources` must be a non-empty list")
        rows = []

    seen: set[str] = set()
    for index, row in enumerate(rows):
        where = f"sources[{index}]"
        if not isinstance(row, dict):
            problems.append(f"{where}: must be a mapping")
            continue
        source_id = row.get("source_id")
        if isinstance(source_id, str):
            where = f"source {source_id!r}"
            if source_id in seen:
                problems.append(f"{where}: duplicate source_id")
            seen.add(source_id)
        row_problems = _check_row(row, where)
        problems.extend(row_problems)
        if not row_problems:
            sources.append(_build(row))

    if problems:
        listing = "\n".join(f"  - {problem}" for problem in problems)
        raise RightsError(f"{target}: {len(problems)} problem(s):\n{listing}")

    return SourceRegistry(schema_version=document["schema_version"], sources=tuple(sources))


def _check_header(document: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if document.get("schema_version") != SCHEMA_VERSION:
        problems.append(f"`schema_version` must be {SCHEMA_VERSION}")

    defaults = document.get("defaults")
    if not isinstance(defaults, dict):
        problems.append("`defaults` must be a mapping carrying the D-74 budget")
        return problems

    expected = {
        "quote_budget_words": DEFAULT_QUOTE_BUDGET_WORDS,
        "source_budget_words": DEFAULT_SOURCE_BUDGET_WORDS,
        "locator_granularity": "chapter",
    }
    # The defaults restate D-74 in the data. They are checked for equality, not
    # merely for presence, so that loosening the published budget requires
    # changing a decision rather than editing a number.
    for key, value in expected.items():
        if defaults.get(key) != value:
            problems.append(f"`defaults.{key}` must be {value!r} (D-74), got {defaults.get(key)!r}")
    for key in defaults:
        if key not in expected:
            problems.append(f"`defaults.{key}` is not a known default")
    return problems


def _check_row(row: dict[str, Any], where: str) -> list[str]:
    problems: list[str] = []

    for field in _SOURCE_FIELDS:
        if field not in row:
            problems.append(f"{where}: missing required field `{field}`")
    for field in row:
        if field not in _SOURCE_FIELDS:
            problems.append(f"{where}: unknown field `{field}` (the schema is closed)")
    if problems:
        return problems

    source_id = row["source_id"]
    if not isinstance(source_id, str) or not SOURCE_ID_RE.match(source_id):
        problems.append(f"{where}: `source_id` must be a lower-case hyphenated slug")

    problems.extend(_check_enum(row, where, "source_kind", SOURCE_KINDS))
    problems.extend(_check_enum(row, where, "access_basis", ACCESS_BASES))
    problems.extend(_check_enum(row, where, "reuse_class", REUSE_CLASSES))
    problems.extend(_check_enum(row, where, "redistribution", REDISTRIBUTION_MODES))
    problems.extend(_check_enum(row, where, "locator_granularity", LOCATOR_GRANULARITIES))

    licence = row["licence"]
    if not isinstance(licence, str) or not LICENCE_RE.match(licence):
        problems.append(
            f"{where}: `licence` must be an SPDX identifier, `all-rights-reserved` or `unknown`"
        )

    uses = row["permitted_use"]
    if not isinstance(uses, list) or not uses:
        problems.append(f"{where}: `permitted_use` must be a non-empty list")
    else:
        unknown = [use for use in uses if use not in PERMITTED_USES]
        if unknown:
            problems.append(f"{where}: `permitted_use` has unknown value(s) {unknown!r}")
        if len(set(uses)) != len(uses):
            problems.append(f"{where}: `permitted_use` repeats a value")

    for field, ceiling in (
        ("quote_budget_words", DEFAULT_QUOTE_BUDGET_WORDS),
        ("source_budget_words", DEFAULT_SOURCE_BUDGET_WORDS),
    ):
        value = row[field]
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            problems.append(f"{where}: `{field}` must be a positive integer")
        elif value > ceiling:
            problems.append(f"{where}: `{field}` is {value}, above the D-74 ceiling of {ceiling}")

    for field in ("in_local_index", "redistributable"):
        if not isinstance(row[field], bool):
            problems.append(f"{where}: `{field}` must be a boolean")

    verified_at = row["verified_at"]
    if verified_at is not None and not (
        isinstance(verified_at, str) and ISO_DATE_RE.match(verified_at)
    ):
        problems.append(f"{where}: `verified_at` must be null or an ISO date (YYYY-MM-DD)")

    note = row["verification_note"]
    if not isinstance(note, str) or not note.strip():
        problems.append(
            f"{where}: `verification_note` is required on every row — a row with nothing "
            "recorded about what was checked is a row that implies it was"
        )

    for field in ("rights_holder",):
        if not isinstance(row[field], str) or not row[field].strip():
            problems.append(f"{where}: `{field}` must be a non-empty string")

    problems.extend(_check_citation(row, where))
    if not problems:
        problems.extend(_check_cross_field(row, where))
    return problems


def _check_enum(row: dict[str, Any], where: str, field: str, allowed: frozenset[str]) -> list[str]:
    value = row[field]
    if value not in allowed:
        options = ", ".join(sorted(allowed))
        return [f"{where}: `{field}` must be one of {{{options}}}, got {value!r}"]
    return []


def _check_citation(row: dict[str, Any], where: str) -> list[str]:
    problems: list[str] = []
    citation = row["citation"]
    if not isinstance(citation, dict):
        return [f"{where}: `citation` must be a mapping"]

    kind = row["source_kind"]
    allowed = set(_CITATION_FIELDS) | ({"scope_note"} if kind == "source-family" else set())
    for field in _CITATION_FIELDS:
        if field not in citation:
            problems.append(f"{where}: `citation.{field}` is required (null is an allowed value)")
    for field in citation:
        if field not in allowed:
            problems.append(f"{where}: `citation.{field}` is not permitted for a {kind}")

    title = citation.get("title")
    if not isinstance(title, str) or not title.strip():
        problems.append(f"{where}: `citation.title` must be a non-empty string")

    year = citation.get("year")
    if year is not None and not (isinstance(year, int) and not isinstance(year, bool)):
        problems.append(f"{where}: `citation.year` must be null or an integer")

    if kind == "work":
        for field in ("author", "publisher", "edition"):
            value = citation.get(field)
            if not isinstance(value, str) or not value.strip():
                problems.append(f"{where}: a `work` requires `citation.{field}`")
        if citation.get("year") is None:
            problems.append(f"{where}: a `work` requires `citation.year`")
    elif kind == "source-family":
        scope_note = citation.get("scope_note")
        if not isinstance(scope_note, str) or not scope_note.strip():
            problems.append(
                f"{where}: a `source-family` requires `citation.scope_note` saying what the "
                "family is, because its title alone does not bound it"
            )
        for field in _FAMILY_NULL_FIELDS:
            if citation.get(field) is not None:
                problems.append(
                    f"{where}: `citation.{field}` must be null for a `source-family` — a "
                    "literature has no single one, and recording one implies a precision "
                    "the row does not have"
                )
    return problems


def _check_cross_field(row: dict[str, Any], where: str) -> list[str]:
    """The rules that make the redundant fields a guard rather than a hazard."""
    problems: list[str] = []
    no_redistribution = row["redistribution"] == "none"
    declared_none = "redistribution-none" in row["permitted_use"]
    redistributable = row["redistributable"]

    if no_redistribution != declared_none:
        problems.append(
            f"{where}: `redistribution: none` and `redistribution-none` in `permitted_use` "
            "must agree"
        )
    if no_redistribution == redistributable:
        problems.append(
            f"{where}: `redistribution: {row['redistribution']}` contradicts "
            f"`redistributable: {redistributable}`"
        )

    if row["in_local_index"] and row["access_basis"] != "owner-purchased-copy":
        problems.append(
            f"{where}: `in_local_index: true` requires `access_basis: owner-purchased-copy` — "
            "the local index is built from the reader's own copy and from nothing else (D-16)"
        )
    if str(row["reuse_class"]).startswith("reference-only") and row["in_local_index"]:
        problems.append(
            f"{where}: a `{row['reuse_class']}` source is referenced and never ingested, so it "
            "cannot be `in_local_index: true` (D-62)"
        )
    if (
        str(row["reuse_class"]).startswith("reference-only")
        and "read-as-input" in (row["permitted_use"])
    ):
        problems.append(
            f"{where}: a `{row['reuse_class']}` source grants no `read-as-input` permission (D-62)"
        )
    if row["reuse_class"] == "cc-by-4.0-compatible" and not redistributable:
        problems.append(
            f"{where}: `cc-by-4.0-compatible` means the wording may ship, so `redistributable` "
            "must be true"
        )
    return problems


def _build(row: dict[str, Any]) -> Source:
    citation = row["citation"]
    return Source(
        source_id=row["source_id"],
        source_kind=row["source_kind"],
        citation=Citation(
            author=citation.get("author"),
            title=citation["title"],
            year=citation.get("year"),
            publisher=citation.get("publisher"),
            edition=citation.get("edition"),
            doi_or_isbn=citation.get("doi_or_isbn"),
            scope_note=citation.get("scope_note"),
        ),
        rights_holder=row["rights_holder"],
        access_basis=row["access_basis"],
        licence=row["licence"],
        reuse_class=row["reuse_class"],
        permitted_use=tuple(row["permitted_use"]),
        redistribution=row["redistribution"],
        quote_budget_words=row["quote_budget_words"],
        source_budget_words=row["source_budget_words"],
        locator_granularity=row["locator_granularity"],
        in_local_index=row["in_local_index"],
        redistributable=row["redistributable"],
        verified_at=row["verified_at"],
        verification_note=" ".join(row["verification_note"].split()),
    )
