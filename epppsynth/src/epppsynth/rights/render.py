# SPDX-FileCopyrightText: 2026 W. Taylor Farrington
# SPDX-License-Identifier: Apache-2.0
"""Generate `epppsynth/docs/rights.md` from the source rights record.

The rendered table answers three questions per source and is arranged so that a
reader cannot get two of the three without the third: what the project may do
with it, what it may never do, and whether anyone has actually checked. Sources
whose terms nobody has read are rendered under their own heading, separated from
the rest, because a table that mixes checked and unchecked rows implies a
uniformity it does not have.

The output is deterministic — sorted by `source_id`, wrapped at a fixed width,
and carrying no timestamp, hostname or path outside the repository — so that
`git diff --exit-code` on it is a meaningful check.

The generator refuses to emit if a concept sourced from a non-redistributable
row carries a verbatim field (D-10). That check has nothing to read until EP-9
builds the concept registry; wiring it here means EP-10 turns it on rather than
remembering to add it.
"""

from __future__ import annotations

import argparse
import pathlib
import sys
import textwrap
from collections.abc import Sequence

from .check import check_no_verbatim_from_nonredistributable, concept_paths
from .load import load_sources
from .model import DEFAULT_QUOTE_BUDGET_WORDS, DEFAULT_SOURCE_BUDGET_WORDS, Source, SourceRegistry
from .paths import rights_md, sources_yaml

WIDTH = 96

_HEADER = """<!-- GENERATED FILE. Do not edit by hand. -->
<!-- Source: epppsynth/registry/sources.yaml · Generator: epppsynth.rights.render -->

# Rights and reuse, per source

**This file is generated.** Its source of truth is
[`../registry/sources.yaml`](../registry/sources.yaml) and its generator is
`epppsynth.rights.render`. Edit the YAML, never this file, and regenerate with, from
`epppsynth/`:

```
uv run python -m epppsynth.rights.render
```

Regenerating and then finding a diff here is a build failure, not a discrepancy for somebody to
notice later.
"""

_WHY = """
## Why this file exists

This project's conceptual substrate is copyrighted and its repository is public. D-10 keeps both
facts true by splitting the problem in two. The **public** artifact is hand-authored original prose
that cites its sources and reproduces none of them. The **local** path builds a gitignored index
from a copy the reader lawfully holds, and ships nothing derived from it. Neither path works if
nobody records, per source, which one it is on.

So this table is not documentation of a policy. It is the policy, in the form a check can read:
`epppsynth.rights` refuses to generate this file, and EP-6 will refuse to build, when a rule below
is broken.

Nothing here has been reviewed by counsel. It is issue-spotting.
"""

_HOW_TO_READ = """
## How to read a row

Each source below carries three plain-language lines, and they are the point of the file:

- **May** — what this project is permitted to do with the source.
- **May never** — what it is not, including the things that would be easy to do by accident.
- **Checked** — whether anyone has confirmed the source's reuse terms against the rights holder's
  own statement, and on what date. `No` means no. It does not mean *probably fine*.

The remaining fields are the machine-readable form of the same three answers, and are validated
against a closed enumeration on load, so a value nobody anticipated is a failure rather than a
pass-through.
"""

_STANDING_RULES = f"""
## Standing rules, which apply to every source above

- **Citations are chapter-level locators only** (D-74). No page ranges. A journal article's own
  page span belongs to its bibliographic identity and is permitted in a source record's citation
  field; it stays forbidden in a concept's short citation.
- **Quotation budget: {DEFAULT_QUOTE_BUDGET_WORDS} words per quote,
  {DEFAULT_SOURCE_BUDGET_WORDS} words per source.** A row may set a stricter budget and may never
  set a looser one; the loader rejects a row that tries.
- **No quoted phrase, and no chapter title, is used as a concept label**, and no sequence of
  locators may reconstruct a source's outline. A book's title plus its chapter list is a
  navigable derivative of that book.
- **Verbatim spans never leave the local index.** They are never emitted, exported, screenshotted
  or serialized, and no exportable type has a field to put one in. That is enforced by the type
  graph, not by discipline (D-23).
- **Normative guidance under a non-commercial or share-alike licence is referenced, never
  ingested** (D-62). Ingesting one into a CC BY 4.0 tree is licence contamination, and it is
  expensive to unwind after the fact rather than merely embarrassing.

## Where the repository's own licences are recorded

This file covers the **sources** the project reads. The licences of the repository's own files are
a separate question, answered by [`../../REUSE.toml`](../../REUSE.toml) — the machine-readable
boundary — and restated in prose in [`../../NOTICE`](../../NOTICE).
"""

_UNVERIFIED_WARNING = """
## Rights not yet verified

Nobody has read the reuse terms of the sources below. They are listed apart from the rest for one
reason: a table that mixes checked and unchecked rows implies a uniformity it does not have, and a
reader skimming for a green light would find one.

Until a row here is cleared, it may be cited and may not be ingested, and **no public
intended-use, regulatory-status or reuse claim may rest on it**. Clearing them is an owner-gated
reading task carried as a P1 blocker, not a nice-to-have.
"""


def render_rights_md(
    registry: SourceRegistry | None = None,
    registry_paths: Sequence[pathlib.Path | str] | None = None,
) -> str:
    """Render the rights table, or raise if a concept-side rule is broken."""
    sources = registry if registry is not None else load_sources()
    concepts = tuple(registry_paths) if registry_paths is not None else concept_paths()
    findings = check_no_verbatim_from_nonredistributable(concepts, sources)
    if findings:
        listing = "\n".join(f"  - {finding}" for finding in findings)
        raise RuntimeError(
            "refusing to generate the rights table: a concept sourced from a "
            f"non-redistributable row carries a verbatim field (D-10):\n{listing}"
        )

    verified = [source for source in sources.sorted_by_id() if source.verified]
    unverified = [source for source in sources.sorted_by_id() if not source.verified]

    parts = [_HEADER, _WHY, _summary_table(sources), _HOW_TO_READ]
    parts.append("\n## Rights verified\n\n")
    if verified:
        parts.append(
            _wrap(
                "Verified means somebody recorded what they checked, when, and against what. "
                "Read each note before relying on a row: some of these verify a posture that "
                "needs no permission - original prose plus citation, nothing reproduced - "
                "rather than a licence somebody granted, and each one says which it is."
            )
            + "\n"
        )
        parts.extend(_source_block(source) for source in verified)
    else:
        parts.append("No source's reuse terms have been verified.\n")

    parts.append(_UNVERIFIED_WARNING)
    if unverified:
        parts.extend(_source_block(source) for source in unverified)
    else:
        parts.append("\nNo source is waiting on a rights check.\n")

    parts.append(_STANDING_RULES)
    return "".join(parts).rstrip("\n") + "\n"


def _summary_table(sources: SourceRegistry) -> str:
    lines = [
        "\n## Summary\n",
        "| source | kind | reuse class | in local index | may redistribute | terms checked |",
        "|---|---|---|---|---|---|",
    ]
    for source in sources.sorted_by_id():
        lines.append(
            f"| `{source.source_id}` "
            f"| {source.source_kind} "
            f"| `{source.reuse_class}` "
            f"| {_yes_no(source.in_local_index)} "
            f"| {_yes_no(source.redistributable)} "
            f"| {source.verified_at if source.verified else '**no**'} |"
        )
    lines.append("")
    return "\n".join(lines) + "\n"


def _source_block(source: Source) -> str:
    citation = source.citation
    lines = [f"\n### `{source.source_id}`\n", _wrap(_bibliography(source)) + "\n"]

    if citation.scope_note:
        lines.append("\n" + _wrap(f"*Scope.* {citation.scope_note}") + "\n")

    lines.append("\n" + _wrap(f"**May** — {_may(source)}") + "\n")
    lines.append("\n" + _wrap(f"**May never** — {_may_never(source)}") + "\n")
    lines.append("\n" + _wrap(f"**Checked** — {_checked(source)}") + "\n")

    lines.append("\n| field | value |\n|---|---|\n")
    rows = [
        ("rights holder", source.rights_holder),
        ("access basis", f"`{source.access_basis}`"),
        ("licence", f"`{source.licence}`"),
        ("reuse class", f"`{source.reuse_class}`"),
        ("permitted use", ", ".join(f"`{use}`" for use in source.permitted_use)),
        ("redistribution", f"`{source.redistribution}`"),
        ("quotation budget", f"{source.quote_budget_words} words per quote"),
        ("source budget", f"{source.source_budget_words} words in total"),
        ("locator granularity", f"`{source.locator_granularity}`"),
        ("in local index", _yes_no(source.in_local_index)),
        ("redistributable", _yes_no(source.redistributable)),
        ("verified at", source.verified_at or "**never**"),
    ]
    lines.extend(f"| {name} | {value} |\n" for name, value in rows)
    lines.append("\n" + _wrap(f"*Note.* {source.verification_note}") + "\n")
    return "".join(lines)


def _bibliography(source: Source) -> str:
    citation = source.citation
    if source.source_kind == "source-family":
        return f"**{citation.title}.** A family of sources, not a single publication."
    pieces = [piece for piece in (citation.author, f"*{citation.title}*") if piece]
    tail = [
        str(piece)
        for piece in (citation.publisher, citation.year, citation.edition, citation.doi_or_isbn)
        if piece is not None
    ]
    return ". ".join([", ".join(pieces), ", ".join(tail)]) + "."


def _may(source: Source) -> str:
    permissions: list[str] = []
    if "read-as-input" in source.permitted_use:
        permissions.append("be read as input while this project authors original prose about it")
    if "short-citation-in-docs" in source.permitted_use:
        permissions.append(
            "be cited in public documentation, with a chapter-level locator and nothing finer"
        )
    if source.in_local_index:
        permissions.append(
            "have spans held in the gitignored local index, which is never committed and never "
            "leaves the machine"
        )
    if not permissions:
        permissions.append("be named, and nothing more")
    return _join(permissions) + "."


def _may_never(source: Source) -> str:
    prohibitions = [
        "be redistributed, republished, or have any of its text shipped in this repository or in "
        "anything this project emits"
    ]
    if source.reference_only:
        prohibitions.append(
            "be ingested — it is referenced and never ingested, so no wording of it may inform "
            "text that ships under CC BY 4.0"
        )
    if not source.in_local_index:
        prohibitions.append("enter the local derived index")
    prohibitions.append(
        f"be quoted beyond {source.quote_budget_words} words in one quotation or "
        f"{source.source_budget_words} words in total"
    )
    prohibitions.append(
        "be cited with a page range, have a chapter title reused as a concept label, or be given "
        "a sequence of locators that reconstructs its outline"
    )
    return _join(prohibitions) + "."


def _checked(source: Source) -> str:
    if source.verified:
        return (
            f"Yes, on {source.verified_at}. What was checked is in the note below; read it before "
            "relying on this row."
        )
    return (
        "**No. Nobody has checked this source's reuse terms.** No public claim may rest on it, "
        "and it may not be ingested. The note below records what was attempted and what was "
        "observed."
    )


def _join(items: Sequence[str]) -> str:
    if len(items) == 1:
        return items[0]
    return "; ".join(items[:-1]) + "; and " + items[-1]


def _yes_no(value: bool) -> str:
    return "yes" if value else "no"


def _wrap(text: str) -> str:
    return "\n".join(
        textwrap.wrap(
            " ".join(text.split()),
            width=WIDTH,
            break_long_words=False,
            break_on_hyphens=False,
        )
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m epppsynth.rights.render",
        description="Generate epppsynth/docs/rights.md from epppsynth/registry/sources.yaml.",
    )
    parser.add_argument(
        "--out", metavar="PATH", help="where to write (default: the canonical path)"
    )
    parser.add_argument(
        "--sources", metavar="PATH", help="the rights record to read (default: the canonical path)"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="do not write; exit non-zero if the file on disk differs from the render",
    )
    args = parser.parse_args(argv)

    registry = load_sources(args.sources or sources_yaml())
    try:
        rendered = render_rights_md(registry)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    out = pathlib.Path(args.out) if args.out else rights_md()
    if args.check:
        current = out.read_text(encoding="utf-8") if out.is_file() else ""
        if current != rendered:
            print(f"{out} is out of date; regenerate it", file=sys.stderr)
            return 1
        print(f"{out} is up to date ({len(registry)} sources)")
        return 0

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(rendered, encoding="utf-8", newline="\n")
    print(f"wrote {out} ({len(registry)} sources, {len(rendered.splitlines())} lines)")
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry
    sys.exit(main())
