# SPDX-FileCopyrightText: 2026 W. Taylor Farrington
# SPDX-License-Identifier: Apache-2.0
"""The three allowlists, kept apart on purpose.

An allowlist is how a scanner quietly stops working, so this module holds all
three of them in one place, each with its own scope, its own counting rule and
its own amendment path. **None of the three may be used to reach another's
scope** (EP-6 §9):

1. :data:`CANARY_ALLOWLIST` — one directory, by exact path. The committed canary
   fixtures live there and are inert by construction. Adding a second entry is an
   `ADR-008` amendment, and :func:`epppsynth.tests.test_publicsafety` fails until
   the ADR is amended.
2. :data:`MODALITY_EXEMPTIONS` — three files, each carrying the reason it is
   exempt from the retired-modality sweep. Owner-ratified on 2026-08-31 (ruling
   **OD-10**). It grows only by a further **owner ruling** — not by an ADR
   amendment and not by a session's judgement.
3. The **line marker** — :data:`RULE_DEFINITION_MARKER`. Every file that defines
   a rule necessarily contains that rule's own pattern, so a line may exempt
   itself. The exemption is line-scoped: never a block, never a file, never a
   directory, never a pattern, and never inherited by the next line.

The marker's literal is assembled from two fragments below so that this file,
which the scanners read like any other, does not accidentally exempt its own
lines. The same split-literal convention that EP-0 established for rule patterns
in prose applies to rule literals in code.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# ── 1. the canary directory ──────────────────────────────────────────────────

#: The one directory the scanners skip, named by exact path rather than by
#: pattern. A pattern-based exemption is how a real leak later hides.
CANARY_DIR = "epppsynth/tests/canaries"

#: Exactly one entry. `test_publicsafety` asserts the length, so a second entry
#: is a failing test and therefore a deliberate decision (ADR-008, EP-6 §9).
CANARY_ALLOWLIST: tuple[str, ...] = (CANARY_DIR,)

CANARY_REASON = (
    "the planted-canary fixtures that prove each scanner fires; inert by "
    "construction, header-declared, and confined to this one directory"
)

# ── 2. the retired-modality sweep's exemption table ──────────────────────────

#: Owner ruling OD-10, confirmed 2026-08-31, as three entries with reasons.
#: Two of the four rows EP-2 proposed are deliberately absent: `source
#: material/README.md` contains no occurrence, and an exemption for a file that
#: does not need one is a hole waiting for a future edit; and
#: `tools/epub_to_md_pipeline.py`'s exemption expired when OD-6 was ruled live
#: and the source spine moved out of the tracked file.
MODALITY_EXEMPTIONS: dict[str, str] = {
    "epppsynth/DECISIONS.md": ("D-4 records the retired expansion; the record must keep the word"),
    "roadmap/EP-2-canonical-docs.md": (
        "self-referential — the brief quotes the token in order to specify the sweep"
    ),
    "roadmap/EP-6-leak-prevention-ci.md": (
        "the brief that specifies this sweep, for the same reason"
    ),
}

#: Fixed by owner ruling OD-10. `test_publicsafety` asserts it, so a fourth row
#: is a failing test and needs a further ruling rather than an edit.
MODALITY_EXEMPTION_COUNT = 3

# ── 3. the line marker ───────────────────────────────────────────────────────

#: Assembled from fragments so that this line is not itself a marker.
RULE_DEFINITION_MARKER = "leak-scan-allow:" + " rule-definition"

#: Inline code spans are stripped before the marker is looked for, so that prose
#: *mentioning* the marker in backticks — as `CLAUDE.md`, EP-0 and EP-6 all do —
#: is a mention and not an exemption. A marker is only a marker in a comment.
_INLINE_CODE = re.compile(r"`[^`\n]*`")
_MARKER_IN_COMMENT = re.compile(r"(?:<!--|#|//)[^\n]*" + re.escape(RULE_DEFINITION_MARKER))


@dataclass(frozen=True)
class Skip:
    """One line a scanner did not report, and why it did not report it.

    Every skip is printed in `epppsynth scan`'s summary. An exemption nobody
    sees is an off switch, so the inventory is part of the output rather than
    part of the implementation.
    """

    path: str
    line: int | None
    reason: str
    detail: str = ""

    @property
    def where(self) -> str:
        return f"{self.path}:{self.line}" if self.line is not None else self.path

    def __str__(self) -> str:
        tail = f" - {self.detail}" if self.detail else ""
        return f"{self.where}  [{self.reason}]{tail}"


def is_canary(path: str) -> bool:
    """Whether a repository-relative POSIX path is inside the canary directory."""
    return any(path == entry or path.startswith(entry + "/") for entry in CANARY_ALLOWLIST)


def marked_lines(text: str) -> frozenset[int]:
    """The 1-based line numbers carrying the marker, in a comment, on that line."""
    marked = set()
    for number, line in enumerate(text.splitlines(), start=1):
        if _MARKER_IN_COMMENT.search(_INLINE_CODE.sub("", line)):
            marked.add(number)
    return frozenset(marked)
