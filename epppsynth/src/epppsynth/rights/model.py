# SPDX-FileCopyrightText: 2026 W. Taylor Farrington
# SPDX-License-Identifier: Apache-2.0
"""The rights vocabulary: closed enumerations, patterns, and the loaded shapes.

Everything the rest of `epppsynth.rights` is allowed to believe about a source is
declared here. The enumerations are **closed** on purpose (D-62): licence
contamination is cheap to prevent and expensive to unwind, so a value nobody
anticipated is a validation failure rather than a pass-through.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# ── closed enumerations ──────────────────────────────────────────────────────

SOURCE_KINDS = frozenset({"work", "source-family"})

ACCESS_BASES = frozenset(
    {"owner-purchased-copy", "open-access", "public-domain", "government-work"}
)

#: D-62. `reference-only*` means the source may be cited and never ingested.
#: `owner-copy-read-as-input` means it may be read while authoring original
#: prose. Only `cc-by-4.0-compatible` permits a source's wording to inform text
#: that then ships under CC BY 4.0.
REUSE_CLASSES = frozenset(
    {
        "cc-by-4.0-compatible",
        "reference-only",
        "reference-only-pending-rights-check",
        "owner-copy-read-as-input",
    }
)

PERMITTED_USES = frozenset({"read-as-input", "short-citation-in-docs", "redistribution-none"})

REDISTRIBUTION_MODES = frozenset({"none", "with-attribution"})

#: Fixed by D-74. A source without chapters is cited `whole-work`, which is
#: coarser; the granularity is an upper bound on precision, not a requirement.
LOCATOR_GRANULARITIES = frozenset({"chapter"})

# ── the D-74 budget, as data ─────────────────────────────────────────────────

DEFAULT_QUOTE_BUDGET_WORDS = 25
DEFAULT_SOURCE_BUDGET_WORDS = 150

# ── patterns ─────────────────────────────────────────────────────────────────

SOURCE_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

#: An SPDX identifier, `all-rights-reserved`, or `unknown`. No spaces: a licence
#: field that reads like a sentence is a note, and notes go in the note field.
LICENCE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9.+-]*$")

#: Chapter-level locators only (D-74). `ch. 3`, `ch. 3–4`, or `whole-work` for a
#: source that has no chapters. Anything finer fails, which is what makes the
#: published artifact refuse to function as a navigable derivative of a source.
LOCATOR_RE = re.compile(r"^(?:ch\. \d{1,3}(?:–\d{1,3})?|whole-work)$")

#: The banned shape, checked as text rather than as structure, because a page
#: range is a leak wherever it appears and not only in a locator field.
PAGE_RANGE_RE = re.compile(r"\bpp?\.\s*\d+\s*[-–—]\s*\d+")

# ── errors and findings ──────────────────────────────────────────────────────


class RightsError(ValueError):
    """A rights record that does not validate. Raised with every problem at once."""


@dataclass(frozen=True)
class Finding:
    """One rule violation, reported rather than raised.

    The checks return findings instead of raising so that a caller — EP-6's CI
    job, or a test — sees the whole picture in one run. A partial report invites
    fixing one leak and shipping the next.
    """

    rule: str
    where: str
    detail: str

    def __str__(self) -> str:
        return f"{self.rule}: {self.where}: {self.detail}"


# ── loaded shapes ────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class Citation:
    """A source's bibliographic identity, and nothing about its interior.

    There is deliberately no field for a chapter title, a chapter list, or a page
    range. A book's title plus its chapter list reconstructs the source's
    outline, which is the leak the 2026-08-31 addendum to D-74 closed.
    """

    author: str | None
    title: str
    year: int | None
    publisher: str | None
    edition: str | None
    doi_or_isbn: str | None
    scope_note: str | None = None


@dataclass(frozen=True)
class Source:
    """One row of the rights record."""

    source_id: str
    source_kind: str
    citation: Citation
    rights_holder: str
    access_basis: str
    licence: str
    reuse_class: str
    permitted_use: tuple[str, ...]
    redistribution: str
    quote_budget_words: int
    source_budget_words: int
    locator_granularity: str
    in_local_index: bool
    redistributable: bool
    verified_at: str | None
    verification_note: str

    @property
    def verified(self) -> bool:
        """Whether anyone has actually checked this row's reuse terms."""
        return self.verified_at is not None

    @property
    def reference_only(self) -> bool:
        """Whether this source is referenced and never ingested (D-62)."""
        return self.reuse_class.startswith("reference-only")

    @property
    def display_title(self) -> str:
        return self.citation.title


@dataclass(frozen=True)
class SourceRegistry:
    """The loaded, validated `sources.yaml`."""

    schema_version: int
    sources: tuple[Source, ...]

    def __iter__(self):
        return iter(self.sources)

    def __len__(self) -> int:
        return len(self.sources)

    def __contains__(self, source_id: object) -> bool:
        return any(source.source_id == source_id for source in self.sources)

    def get(self, source_id: str) -> Source | None:
        for source in self.sources:
            if source.source_id == source_id:
                return source
        return None

    def __getitem__(self, source_id: str) -> Source:
        source = self.get(source_id)
        if source is None:
            raise KeyError(source_id)
        return source

    @property
    def ids(self) -> tuple[str, ...]:
        return tuple(source.source_id for source in self.sources)

    def sorted_by_id(self) -> tuple[Source, ...]:
        return tuple(sorted(self.sources, key=lambda source: source.source_id))


@dataclass(frozen=True)
class ConceptProvenance:
    """The concept-side contract this module checks against.

    The concept registry does not exist yet — **EP-9** defines it — so this is
    written against the contract rather than against a file, and is unit-tested
    on fixtures. EP-10 makes it live. The contract EP-9 must honour is narrow: a
    concept file is a mapping with a `concepts` list, and each concept carries
    `concept_id` and a `provenance` mapping with `source_id`, an optional
    chapter-level `locator`, and an optional `verbatim` field that must be empty
    for every non-redistributable source.
    """

    concept_id: str
    source_id: str
    locator: str | None
    verbatim: str | None
    origin: str

    @property
    def has_verbatim(self) -> bool:
        return bool(self.verbatim and self.verbatim.strip())
