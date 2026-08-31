# SPDX-FileCopyrightText: 2026 W. Taylor Farrington
# SPDX-License-Identifier: Apache-2.0
"""The D-74 quotation budget, as a counter: 25 words per quote, 150 per source.

EP-6 runs this in CI over the public prose. It is written and proven here.

What counts as a quotation is a judgement, and the judgement is made explicit
rather than left to a regex nobody reads:

* A quotation is a span between paired double quotation marks — straight `"…"`
  or curly `“…”` — in markdown prose.
* Code is not prose. Fenced blocks and inline code spans are blanked out before
  scanning, with their length preserved so that reported line numbers stay true.
  Without this, a regex in a test file or a shell snippet in a brief would be
  counted as a quotation of somebody.
* A span may be attributed to a source by an inline marker directly after the
  closing mark: `[source_id]` or `(source_id, ch. 3)`. An unattributed span is
  still budgeted per quote; only attributed spans accumulate toward a source's
  150-word total, because a total nobody can attribute is not a total.
* A span may be exempted by `<!-- quote-budget-allow: <reason> -->` on the same
  line or the line above, following the `# leak-scan-allow:` precedent already
  in this repository. The reason is required and is reported; an exemption
  nobody has to justify is not an exemption, it is an off switch.

Self-quotation — this project quoting its own governance text — is the common
case in these documents and is not distinguishable by pattern from any other
quotation. It does not need to be: the budget is small enough that project prose
stays under it, and a span that does not is worth a second look regardless of
who wrote it.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field

from .load import load_sources
from .model import (
    DEFAULT_QUOTE_BUDGET_WORDS,
    DEFAULT_SOURCE_BUDGET_WORDS,
    Finding,
    SourceRegistry,
)
from .paths import quotation_scan_paths, repo_root

_FENCED = re.compile(r"^(?P<fence>```+|~~~+).*?^(?P=fence)[ \t]*$", re.DOTALL | re.MULTILINE)
_INLINE_CODE = re.compile(r"`[^`\n]*`")
_CURLY = re.compile(r"“([^”]*)”", re.DOTALL)
#: A straight-quoted span may wrap across lines but never across a blank line —
#: an unpaired quotation mark otherwise swallows the rest of the document.
_STRAIGHT = re.compile(r'"([^"\n]*(?:\n(?![ \t]*\n)[^"\n]*)*)"')
_ATTRIBUTION = re.compile(r"^[ \t]*[\[(]\s*([a-z0-9][a-z0-9-]*)\s*(?:,[^\])]*)?[\])]")
_ALLOW = re.compile(r"<!--\s*quote-budget-allow:\s*(?P<reason>[^>]*?)\s*-->")

UNATTRIBUTED = "unattributed"


@dataclass(frozen=True)
class Quotation:
    """One quoted span, with where it is and what it counts against."""

    path: str
    line: int
    words: int
    text: str
    source_id: str | None
    allowed_reason: str | None = None

    @property
    def attributed(self) -> bool:
        return self.source_id is not None

    @property
    def exempt(self) -> bool:
        return self.allowed_reason is not None


@dataclass
class QuotationReport:
    """What the counter found. `ok` is the single question EP-6 asks it."""

    quotations: list[Quotation] = field(default_factory=list)
    findings: list[Finding] = field(default_factory=list)
    per_source_words: dict[str, int] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return not self.findings

    @property
    def counted(self) -> list[Quotation]:
        return [quote for quote in self.quotations if not quote.exempt]

    def summary(self) -> str:
        lines = [
            f"{len(self.quotations)} quoted span(s), "
            f"{len(self.quotations) - len(self.counted)} exempted, "
            f"{len(self.findings)} over budget"
        ]
        for source_id in sorted(self.per_source_words):
            lines.append(f"  {source_id}: {self.per_source_words[source_id]} word(s)")
        return "\n".join(lines)


def count_quotations(
    paths: Iterable[pathlib.Path | str] | None = None,
    registry: SourceRegistry | None = None,
) -> QuotationReport:
    """Count quoted spans in the given markdown files and enforce the D-74 budget."""
    targets = tuple(paths) if paths is not None else quotation_scan_paths()
    sources = registry
    report = QuotationReport()

    for raw_path in targets:
        path = pathlib.Path(raw_path)
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        prose = _blank_code(text)
        lines = text.splitlines()
        display = _display(path)

        for match in _spans(prose):
            span, start = match
            line_number = prose.count("\n", 0, start) + 1
            words = len(span.split())
            if words == 0:
                continue
            source_id = _attribution(prose, start + len(span) + 1)
            reason = _exemption(lines, line_number)
            quote = Quotation(
                path=display,
                line=line_number,
                words=words,
                text=" ".join(span.split()),
                source_id=source_id,
                allowed_reason=reason,
            )
            report.quotations.append(quote)
            if reason is not None:
                if not reason:
                    report.findings.append(
                        Finding(
                            "quote-budget-allow",
                            f"{display}:{line_number}",
                            "an exemption must state a reason",
                        )
                    )
                continue

            if sources is None and source_id is not None:
                sources = load_sources()
            ceiling = DEFAULT_QUOTE_BUDGET_WORDS
            if source_id is not None and sources is not None:
                known = sources.get(source_id)
                if known is not None:
                    ceiling = known.quote_budget_words
            if words > ceiling:
                report.findings.append(
                    Finding(
                        "quote-budget",
                        f"{display}:{line_number}",
                        f"{words} words in one quotation, over the {ceiling}-word "
                        f"limit (D-74): {_excerpt(quote.text)}",
                    )
                )
            if source_id is not None:
                report.per_source_words[source_id] = (
                    report.per_source_words.get(source_id, 0) + words
                )

    for source_id, total in sorted(report.per_source_words.items()):
        ceiling = DEFAULT_SOURCE_BUDGET_WORDS
        if sources is not None:
            known = sources.get(source_id)
            if known is not None:
                ceiling = known.source_budget_words
        if total > ceiling:
            report.findings.append(
                Finding(
                    "source-budget",
                    source_id,
                    f"{total} quoted words across the scanned files, over the "
                    f"{ceiling}-word per-source limit (D-74)",
                )
            )
    return report


def _spans(prose: str) -> list[tuple[str, int]]:
    """Every quoted span with its start offset, in document order."""
    found = [(match.group(1), match.start(1)) for match in _CURLY.finditer(prose)]
    curly_ranges = [(match.start(), match.end()) for match in _CURLY.finditer(prose)]
    for match in _STRAIGHT.finditer(prose):
        start = match.start()
        if any(low <= start < high for low, high in curly_ranges):
            continue
        found.append((match.group(1), match.start(1)))
    found.sort(key=lambda pair: pair[1])
    return found


def _blank_code(text: str) -> str:
    """Replace code with spaces, preserving length so offsets and lines survive."""

    def blank(match: re.Match[str]) -> str:
        return "".join(character if character == "\n" else " " for character in match.group(0))

    return _INLINE_CODE.sub(blank, _FENCED.sub(blank, text))


def _attribution(prose: str, after: int) -> str | None:
    match = _ATTRIBUTION.match(prose[after : after + 120])
    return match.group(1) if match else None


def _exemption(lines: Sequence[str], line_number: int) -> str | None:
    for candidate in (line_number - 1, line_number - 2):
        if 0 <= candidate < len(lines):
            match = _ALLOW.search(lines[candidate])
            if match:
                return match.group("reason").strip()
    return None


def _excerpt(text: str, limit: int = 60) -> str:
    return repr(text if len(text) <= limit else text[: limit - 1] + "…")


def _display(path: pathlib.Path) -> str:
    try:
        return path.resolve().relative_to(repo_root()).as_posix()
    except ValueError:
        return path.as_posix()


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m epppsynth.rights.quotes",
        description="Count quoted spans and enforce the D-74 budget (25/quote, 150/source).",
    )
    parser.add_argument("paths", nargs="*", metavar="PATH", help="markdown files to scan")
    parser.add_argument("--verbose", action="store_true", help="list every counted span")
    args = parser.parse_args(argv)

    report = count_quotations([pathlib.Path(one) for one in args.paths] or None)
    if args.verbose:
        for quote in report.quotations:
            mark = "exempt" if quote.exempt else str(quote.words)
            print(f"{quote.path}:{quote.line}: [{mark}] {_excerpt(quote.text)}")
    print(report.summary())
    for finding in report.findings:
        print(f"  - {finding}", file=sys.stderr)
    return 0 if report.ok else 1


if __name__ == "__main__":  # pragma: no cover - CLI entry
    sys.exit(main())
