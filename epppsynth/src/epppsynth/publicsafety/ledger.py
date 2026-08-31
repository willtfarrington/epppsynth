# SPDX-FileCopyrightText: 2026 W. Taylor Farrington
# SPDX-License-Identifier: Apache-2.0
"""Check 9 — shared passages between `DECISIONS.md` and private planning state.

The **refined** D-2 invariant, as owner ruling **OD-3** settled it on 2026-08-31:
every eight-word sequence shared between `epppsynth/DECISIONS.md` and any file
under `.local/` must fall **inside a published decision entry or the index
block**. A shared passage in the surrounding prose is a finding.

The literal form of the rule — *no* shared eight-word sequence — is unsatisfiable
by construction. The ledger records each decision in the words it was settled in,
and D-2 requires publishing those settled decisions; EP-2 measured 124 shared
passages, 19.7 % by word count, longest 42 words, and every one of them inside an
entry. Refusing that is refusing D-2, not enforcing it.

**How this runs is part of the specification.** The module reads `.local/` and
reports only positions and counts inside the already-public file. It never
returns, prints, logs or stores the matched text, a line of private content, or
the name of a private file. That is what makes a check over `.local/` compatible
with the never-read rule in `CLAUDE.md`: a script reads it, a person does not,
and nothing private reaches a session transcript, a CI log or a public file.

It is **local and pre-commit only**. `.local/` does not exist on a CI runner, so
the check reports *skipped — no ledger present* there and is counted as skipped,
never as passed. A skip counted as a pass is exactly how this check would quietly
stop working.
"""

from __future__ import annotations

import hashlib
import pathlib
import re
from collections.abc import Iterator
from dataclasses import dataclass, field

#: The shingle width fixed by OD-3.
SHINGLE_WORDS = 8

#: Where private planning state lives (D-2). Never read by a person.
LEDGER_DIR = ".local"

#: Suffixes read from the ledger. Anything else is skipped: a binary file cannot
#: share a word sequence with a markdown document, and reading one would only
#: waste time.
_LEDGER_SUFFIXES = frozenset({".md", ".markdown", ".txt", ".yaml", ".yml", ".json", ".csv"})

_WORD = re.compile(r"[A-Za-z0-9']+")

#: A published decision entry starts here.
_ENTRY_START = re.compile(r"^\*\*D-\d+\b")
#: …and ends at the next entry, the next section heading, or the next rule.
_ENTRY_END = re.compile(r"^(?:\*\*D-\d+\b|## |---\s*$)")
_INDEX_HEADING = re.compile(r"^## Index\s*$")
#: An addendum is published decision content by definition (D-1: a decision is
#: never edited, it is appended to). Most sit inside the entry they refine and
#: need no special case; one — the 2026-08-23 page-span addendum under D-74 —
#: sits after a section rule, so blockquote addenda are recognised wherever they
#: are rather than only where the entry spans happen to reach.
_ADDENDUM_START = re.compile(r"^>\s*\*\*Addendum\b")
_BLOCKQUOTE = re.compile(r"^>")


@dataclass(frozen=True)
class LedgerReport:
    """Positions and counts inside the public file. Never any text."""

    shared_passages: int = 0
    inside_published: int = 0
    outside_published: tuple[int, ...] = ()
    public_words: int = 0
    shared_words: int = 0
    ledger_files_read: int = 0
    published_line_count: int = 0
    _unused: tuple[()] = field(default=(), repr=False)

    @property
    def ok(self) -> bool:
        return not self.outside_published

    def summary(self) -> str:
        share = (self.shared_words / self.public_words * 100) if self.public_words else 0.0
        return (
            f"{self.shared_passages} shared eight-word passage(s) "
            f"({share:.1f} % of the public file by word count); "
            f"{self.inside_published} inside a published entry or the index block, "
            f"{len(self.outside_published)} outside"
        )


def published_lines(text: str) -> frozenset[int]:
    """The 1-based lines of `DECISIONS.md` that are inside a published region.

    Three regions count as published: the **index block** — from `## Index` to
    the next section heading or horizontal rule — every **decision entry**, from
    a line opening `**D-n` to the next entry, heading or rule, and every
    **addendum blockquote**, which is published decision content wherever it
    sits. Everything else is the surrounding prose the refined invariant
    protects: the preamble, the section headings, and any text between them.
    """
    lines = text.splitlines()
    published: set[int] = set()

    index = None
    for number, line in enumerate(lines, start=1):
        if _INDEX_HEADING.match(line):
            index = number
            break
    if index is not None:
        for number in range(index, len(lines) + 1):
            line = lines[number - 1]
            if number > index and (line.startswith("## ") or line.rstrip() == "---"):
                break
            published.add(number)

    entry: int | None = None
    for number, line in enumerate(lines, start=1):
        if entry is not None and _ENTRY_END.match(line) and number > entry:
            entry = None
        if _ENTRY_START.match(line):
            entry = number
        if entry is not None:
            published.add(number)

    addendum: int | None = None
    for number, line in enumerate(lines, start=1):
        if _ADDENDUM_START.match(line):
            addendum = number
        elif addendum is not None and not _BLOCKQUOTE.match(line):
            addendum = None
        if addendum is not None:
            published.add(number)
    return frozenset(published)


def _shingles(text: str) -> Iterator[tuple[bytes, int]]:
    """Hashed eight-word shingles with the character offset of each first word."""
    words = [(match.group(0).lower(), match.start()) for match in _WORD.finditer(text)]
    for start in range(len(words) - SHINGLE_WORDS + 1):
        window = words[start : start + SHINGLE_WORDS]
        digest = hashlib.blake2b(
            " ".join(word for word, _ in window).encode("utf-8"), digest_size=16
        ).digest()
        yield digest, window[0][1]


def _ledger_shingles(directory: pathlib.Path) -> tuple[set[bytes], int]:
    """Hash every eight-word shingle under `.local/`. The text is never kept.

    Only 16-byte digests survive this function. Nothing that reaches a caller can
    be turned back into a sentence, which is the property that lets the check run
    at all.
    """
    digests: set[bytes] = set()
    read = 0
    for path in sorted(directory.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in _LEDGER_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        read += 1
        digests.update(digest for digest, _ in _shingles(text))
    return digests, read


def compare(public_path: pathlib.Path, ledger_dir: pathlib.Path) -> LedgerReport:
    """Compare one public file against the ledger, reporting positions only."""
    text = public_path.read_text(encoding="utf-8")
    allowed = published_lines(text)
    digests, read = _ledger_shingles(ledger_dir)

    shared = 0
    inside = 0
    outside: list[int] = []
    shared_word_offsets: set[int] = set()
    total = 0

    for digest, offset in _shingles(text):
        total += 1
        if digest not in digests:
            continue
        shared += 1
        line = text.count("\n", 0, offset) + 1
        if line in allowed:
            inside += 1
        else:
            outside.append(line)
        shared_word_offsets.add(offset)

    return LedgerReport(
        shared_passages=shared,
        inside_published=inside,
        outside_published=tuple(sorted(set(outside))),
        public_words=total + SHINGLE_WORDS - 1 if total else 0,
        shared_words=len(shared_word_offsets),
        ledger_files_read=read,
        published_line_count=len(allowed),
    )
