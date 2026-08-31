# SPDX-FileCopyrightText: 2026 W. Taylor Farrington
# SPDX-License-Identifier: Apache-2.0
"""The two rights rules, written as library functions and unit-tested here.

EP-6 wires these into CI. They are written and proven at EP-5 so that the
enforcement brief wires already-proven code rather than inventing checks under
time pressure.

The concept registry does not exist yet — **EP-9** defines it — so these run
against the contract rather than against a file, and their tests run on
fixtures. EP-10 makes them live. The contract is deliberately narrow:

    concepts:
      - concept_id: some-concept
        provenance:
          source_id: yalom-existential-psychotherapy-1980
          locator: "ch. 3"          # optional; chapter-level only (D-74)
          verbatim: null            # optional; must stay empty for a
                                    # non-redistributable source (D-10)

Anything EP-9 adds around those keys is ignored here. Anything it renames breaks
these checks loudly, which is the intended failure mode.
"""

from __future__ import annotations

import argparse
import pathlib
import sys
from collections.abc import Iterable, Sequence
from typing import Any

import yaml

from .load import load_sources
from .model import (
    LOCATOR_RE,
    ConceptProvenance,
    Finding,
    RightsError,
    SourceRegistry,
)
from .paths import concept_registry_dir, repo_root


def concept_paths(root: pathlib.Path | None = None) -> tuple[pathlib.Path, ...]:
    """Every concept file that currently exists. Empty until EP-9."""
    directory = concept_registry_dir(root)
    if not directory.is_dir():
        return ()
    return tuple(sorted(directory.rglob("*.yaml")))


def load_concepts(paths: Iterable[pathlib.Path | str]) -> tuple[ConceptProvenance, ...]:
    """Read concept provenance from the given files, against the EP-9 contract."""
    loaded: list[ConceptProvenance] = []
    for raw_path in paths:
        path = pathlib.Path(raw_path)
        document: Any = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(document, dict):
            raise RightsError(f"{path}: top level must be a mapping")
        concepts = document.get("concepts")
        if not isinstance(concepts, list):
            raise RightsError(f"{path}: `concepts` must be a list")
        origin = _display(path)
        for index, concept in enumerate(concepts):
            if not isinstance(concept, dict):
                raise RightsError(f"{origin}: concepts[{index}] must be a mapping")
            provenance = concept.get("provenance")
            if not isinstance(provenance, dict):
                raise RightsError(f"{origin}: concepts[{index}] has no `provenance` mapping")
            loaded.append(
                ConceptProvenance(
                    concept_id=str(concept.get("concept_id", f"concepts[{index}]")),
                    source_id=str(provenance.get("source_id", "")),
                    locator=provenance.get("locator"),
                    verbatim=provenance.get("verbatim"),
                    origin=origin,
                )
            )
    return tuple(loaded)


def check_source_refs(
    registry_paths: Iterable[pathlib.Path | str],
    registry: SourceRegistry | None = None,
) -> list[Finding]:
    """Every `concept.provenance.source_id` resolves to a row in `sources.yaml`.

    A dangling `source_id` is a concept with no rights record, which is exactly
    the state the rights table exists to make impossible.
    """
    sources = registry if registry is not None else load_sources()
    findings: list[Finding] = []
    for concept in load_concepts(registry_paths):
        if not concept.source_id:
            findings.append(
                Finding(
                    "source-ref",
                    f"{concept.origin}:{concept.concept_id}",
                    "provenance carries no `source_id`",
                )
            )
        elif concept.source_id not in sources:
            findings.append(
                Finding(
                    "source-ref",
                    f"{concept.origin}:{concept.concept_id}",
                    f"`source_id` {concept.source_id!r} is not in the rights record",
                )
            )
    return findings


def check_no_verbatim_from_nonredistributable(
    registry_paths: Iterable[pathlib.Path | str],
    registry: SourceRegistry | None = None,
) -> list[Finding]:
    """The D-10 rule: no verbatim field on a concept citing a source we may not redistribute.

    A source is non-redistributable if its row says so, and separately if its
    `reuse_class` is `reference-only*` (D-62). Both are checked, because the two
    statements of the rule in the EP-5 brief are not quite the same statement and
    the union is the safe reading.
    """
    sources = registry if registry is not None else load_sources()
    findings: list[Finding] = []
    for concept in load_concepts(registry_paths):
        if not concept.has_verbatim:
            continue
        source = sources.get(concept.source_id)
        if source is None:
            continue  # a dangling ref is check_source_refs's finding, not this one
        if source.redistributable and not source.reference_only:
            continue
        reason = (
            f"reuse_class {source.reuse_class!r}"
            if source.reference_only
            else "redistributable: false"
        )
        findings.append(
            Finding(
                "verbatim-from-nonredistributable",
                f"{concept.origin}:{concept.concept_id}",
                f"carries a verbatim field sourced from {source.source_id!r} ({reason}); "
                "verbatim spans live in the gitignored local index and are never committed "
                "(D-10, D-23)",
            )
        )
    return findings


def check_locators(
    registry_paths: Iterable[pathlib.Path | str],
    registry: SourceRegistry | None = None,
) -> list[Finding]:
    """Locators are chapter-level only (D-74). A page range fails."""
    del registry  # the rule is the same for every source; the parameter keeps the call shape
    findings: list[Finding] = []
    for concept in load_concepts(registry_paths):
        if concept.locator is None:
            continue
        if not LOCATOR_RE.match(str(concept.locator)):
            findings.append(
                Finding(
                    "locator-granularity",
                    f"{concept.origin}:{concept.concept_id}",
                    f"locator {concept.locator!r} is not chapter-level; use `ch. N`, "
                    "`ch. N–M`, or `whole-work`",
                )
            )
    return findings


ALL_CONCEPT_CHECKS = (
    check_source_refs,
    check_no_verbatim_from_nonredistributable,
    check_locators,
)


def run_all(
    registry_paths: Sequence[pathlib.Path | str],
    registry: SourceRegistry | None = None,
) -> list[Finding]:
    sources = registry if registry is not None else load_sources()
    findings: list[Finding] = []
    for check in ALL_CONCEPT_CHECKS:
        findings.extend(check(registry_paths, sources))
    return findings


def _display(path: pathlib.Path) -> str:
    try:
        return path.resolve().relative_to(repo_root()).as_posix()
    except ValueError:
        return path.as_posix()


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m epppsynth.rights.check",
        description=(
            "Check concept provenance against the source rights record: every source_id "
            "resolves, no verbatim field comes from a non-redistributable source, and every "
            "locator is chapter-level."
        ),
    )
    parser.add_argument(
        "--fixture",
        action="append",
        default=[],
        metavar="PATH",
        help="a concept file to check instead of the live registry; repeatable",
    )
    args = parser.parse_args(argv)

    paths: Sequence[pathlib.Path | str]
    if args.fixture:
        paths = [pathlib.Path(one) for one in args.fixture]
        missing = [str(one) for one in paths if not pathlib.Path(one).is_file()]
        if missing:
            print(f"no such fixture: {', '.join(missing)}", file=sys.stderr)
            return 2
    else:
        paths = concept_paths()
        if not paths:
            print(
                "no concept registry yet (EP-9 creates it); the rules are unit-tested on "
                "fixtures until then"
            )
            return 0

    try:
        findings = run_all(paths)
    except RightsError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    if findings:
        print(f"{len(findings)} rights finding(s):", file=sys.stderr)
        for finding in findings:
            print(f"  - {finding}", file=sys.stderr)
        return 1

    checked = ", ".join(_display(pathlib.Path(one)) for one in paths)
    print(f"0 rights findings over {len(list(paths))} file(s): {checked}")
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry
    sys.exit(main())
