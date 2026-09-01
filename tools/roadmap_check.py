# SPDX-FileCopyrightText: 2026 W. Taylor Farrington
# SPDX-License-Identifier: Apache-2.0
"""roadmap_check - the checks that keep this roadmap honest (EP-8).

Every rule below was previously a convention: a sentence in `roadmap/README.md`
or `CLAUDE.md` that a session was trusted to follow. Eight executed briefs is
enough to know which conventions drift. Here each one is a check that fails.

The ten checks, by id:

==================  ===========================================================
``hashes``          every done box carries a hash git resolves, and the
                    completion notes and the boxes agree in both directions
``deps``            `Depends on` / `Blocks` name real briefs, mirror each
                    other exactly, and form no cycle
``table``           the phase tables and the brief files agree, and the
                    README's size mix is recomputed from the tables
``sections``        every brief carries the template's sections, in order,
                    with a non-empty `## Safety preconditions`
``acceptance``      every brief's acceptance section names a command
``hazards``         every hazard in `DESIGN.md` 14 names a mitigating brief
                    and a verifying gate; every core brief names acceptance
                    evidence; every cited `R-n` exists
``context-budget``  load-order items 1-5 for a brief fit the ceiling
``parked``          every executed brief's parked items reached
                    `final-roadmap.md`, and the residual list is represented
``immutable``       executed briefs' `## Context` sections are unchanged since
                    the commit their box records
``status``          the README badge, the README status paragraph, the badge's
                    evidence file and `CITATION.cff` all agree
==================  ===========================================================

**The token count is an approximation and says so.** No tokenizer is available
offline, and adding one would mean a network fetch and a new dependency, so
``context-budget`` divides characters by a stated constant. The constant is
printed on every run, because a silent approximation is worse than a stated
one, and a real tokenizer is parked in `roadmap/final-roadmap.md` so that the
approximation cannot quietly become permanent. The constant is load-bearing,
and ``--chars-per-token`` exists so that anyone can see how load-bearing.

**This tool checks the roadmap, not the work.** A green run means the roadmap
describes itself consistently. It does not mean a brief was executed well, and
it is not one of EP-6's leak scanners - those are `epppsynth scan`.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import subprocess
import sys
from dataclasses import dataclass, field

# -- the check ids -----------------------------------------------------------

CHECKS: tuple[str, ...] = (
    "hashes",
    "deps",
    "table",
    "sections",
    "acceptance",
    "hazards",
    "context-budget",
    "parked",
    "immutable",
    "status",
)

PASSED, FAILED = "passed", "failed"

#: D-22: S is 30 min, M is 1 h, L is 2 h of one supervised session.
SIZE_HOURS: dict[str, float] = {"S": 0.5, "M": 1.0, "L": 2.0}

#: Load-order items 1-5 must fit this, per `roadmap/README.md`. The brief says
#: "~15k"; a tool needs a number, and rounding the tilde upward would be the
#: project marking its own exam.
CONTEXT_CEILING = 15_000

#: What to do when the ceiling is breached, decided in advance so that the
#: session which trips the gate is not left improvising (owner ruling OD-16,
#: 2026-09-01). The remedy is always the offending brief, never the four files
#: every session shares and never the ceiling: D-22 already says a unit larger
#: than L is split at pickup, and this is that rule reaching the load order.
OVER_BUDGET_REMEDY = (
    "split this brief (D-22, owner ruling OD-16); never trim CLAUDE.md, GOVERNANCE.md, "
    "the DECISIONS index or a brief's self-containment, and never raise the ceiling"
)

#: Characters per token. Not measured - assumed, and printed on every run. 4.0
#: is the common English-prose rule of thumb. Dense markdown - tables, pipes,
#: backticks, em dashes - tokenizes worse than prose, so this figure is
#: optimistic, and the ceiling it is compared against was set against the same
#: rule of thumb.
CHARS_PER_TOKEN = 4.0

#: The six template sections, in order (`roadmap/_TEMPLATE.md`).
CANON_SECTIONS: tuple[str, ...] = (
    "Context",
    "Safety preconditions",
    "In scope",
    "Out of scope",
    "Verification / acceptance",
    "Parked -> final-roadmap.md",
)

#: The charter variant declared in `roadmap/README.md`, for the P3-P7 briefs a
#: phase re-plan upgrades. Five sections, not six: a charter states one scope
#: sketch rather than an in/out pair, because the cutline is what the re-plan
#: draws.
CHARTER_SECTIONS: tuple[str, ...] = (
    "Context",
    "Safety preconditions",
    "Scope sketch (refine at re-plan)",
    "Verification / acceptance (sketch)",
    "Parked -> final-roadmap.md",
)

#: First words that make a backticked span a command rather than a filename.
COMMAND_WORDS: frozenset[str] = frozenset(
    {
        "uv",
        "git",
        "gh",
        "python",
        "python3",
        "py",
        "pytest",
        "ruff",
        "curl",
        "epppsynth",
        "reuse",
        "powershell",
        "pwsh",
        "cmake",
        "pandoc",
        "axe",
        "npx",
    }
)

#: The public residual list of EP-8's in-scope item 4, one entry per named
#: item, with the phrase `final-roadmap.md` must carry for it to count as
#: represented. Named here rather than inferred, so that dropping one is a
#: failure rather than a silence.
RESIDUALS: tuple[tuple[str, str], ...] = (
    ("scenario-library UI", "Scenario library in the interface"),
    ("export and sharing", "Export or sharing of output"),
    ("trainee opt-in retention", "opt-in local retention"),
    ("third-party installability", "third-party installability"),
    ("generalized corpus ingest", "corpus ingest beyond the current single-source spine"),
    ("fine-tuning", "Fine-tuning of any model"),
    ("patient-facing mode", "patient- or family-facing use"),
)

#: The badge string a `CITATION.cff` version of 0.0.0 is allowed to accompany.
PRE_RELEASE_BADGE = "design"
PRE_RELEASE_VERSION = "0.0.0"

#: The D-24 status line, in the folded punctuation `_normalise` produces.
STATUS_LINE = "Design and planning artifact - v1 in progress; no release, no demo, no validation."

BADGE_RE = re.compile(
    r"^status: (design|skeleton|self-evaluated - mode \([abc]\)|v1 - mode \([abc]\))$",
    re.M,
)

BRIEF_FILE_RE = re.compile(r"^EP-(\d+)-[a-z0-9-]+\.md$")
EP_TOKEN_RE = re.compile(r"EP-(\d+)")
RANGE_RE = re.compile(r"EP-(\d+)\s*\.\.\.\s*EP-(\d+)")
HAZARD_ID_RE = re.compile(r"\bR-(\d+)\b")
SHORT_HASH_RE = re.compile(r"\b([0-9a-f]{7,40})\b")
COMPLETION_NOTE_RE = re.compile(r"^> \*\*Completion note \(", re.M)


# -- findings ----------------------------------------------------------------


@dataclass(frozen=True)
class Finding:
    """One inconsistency: where it is, which rule, and what the rule means."""

    check: str
    subject: str
    rule: str
    detail: str

    def render(self) -> str:
        return f"{self.check}\t{self.subject}\t{self.rule}\t{self.detail}"


@dataclass
class CheckResult:
    check: str
    findings: list[Finding] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    @property
    def status(self) -> str:
        return FAILED if self.findings else PASSED

    def add(self, subject: str, rule: str, detail: str) -> None:
        self.findings.append(Finding(self.check, subject, rule, detail))


@dataclass
class Report:
    root: pathlib.Path
    results: list[CheckResult] = field(default_factory=list)

    @property
    def findings(self) -> list[Finding]:
        return [f for r in self.results for f in r.findings]

    @property
    def ok(self) -> bool:
        return not self.findings

    def render(self) -> str:
        width = max((len(r.check) for r in self.results), default=0)
        lines = [f"roadmap_check - {self.root}"]
        for result in self.results:
            count = f"{len(result.findings)} finding(s)" if result.findings else ""
            lines.append(f"  {result.check:<{width}}  {result.status:<6}  {count}".rstrip())
        notes = [note for result in self.results for note in result.notes]
        if notes:
            lines.append("")
            lines.extend(notes)
        lines.append("")
        if self.findings:
            lines.append(f"{len(self.findings)} finding(s) - check, subject, rule, meaning:")
            lines.extend(f.render() for f in self.findings)
        else:
            lines.append("no findings.")
        return "\n".join(lines)


# -- the model ---------------------------------------------------------------


def _normalise(text: str) -> str:
    """Fold the punctuation this repository writes into the ASCII rules match.

    The roadmap is written with real em dashes, ellipses and arrows. Matching
    those literally in source would put a mojibake hazard in every rule and
    make this file unreadable; folding them once here keeps the rules plain.
    The two done-box glyphs are deliberately *not* folded - they carry meaning
    and are matched as themselves.
    """
    return (
        text.replace("—", "-")
        .replace("–", "-")
        .replace("…", "...")
        .replace("→", "->")
        .replace("’", "'")
    )


@dataclass
class Brief:
    number: int
    path: pathlib.Path
    relpath: str
    title: str
    size: str
    mode: str
    core: str
    depends: set[int]
    blocks: set[int]
    sections: list[str]
    is_charter: bool
    text: str
    #: The brief as a cold session receives it: everything before the first
    #: completion note, because a completion note is the record of execution
    #: and never an instruction for it.
    brief_text: str
    has_completion_note: bool

    @property
    def label(self) -> str:
        return f"EP-{self.number}"


def _split_completion_note(text: str) -> str:
    match = COMPLETION_NOTE_RE.search(text)
    if match is None:
        return text
    cut = match.start()
    separator = text.rfind("\n---\n", 0, cut)
    if separator != -1 and text[separator:cut].strip("-\n \t") == "":
        return text[:separator]
    return text[:cut]


def _expand_ranges(cell: str) -> set[int]:
    """`EP-9 ... EP-15` in a table cell means the seven briefs it spans."""
    numbers: set[int] = set()
    for low, high in RANGE_RE.findall(cell):
        numbers.update(range(int(low), int(high) + 1))
    numbers.update(int(n) for n in EP_TOKEN_RE.findall(RANGE_RE.sub("", cell)))
    return numbers


def _header_block(brief_text: str) -> str:
    """The `**Size:** ... **Blocks:** ...` block, and nothing after it.

    Stopping at the first `## ` is not enough: a charter brief carries a
    `> **Charter.**` note between the header and `## Context`, and that note
    names the re-plan EP that upgrades it. Reading to the next heading swept
    that EP into `Blocks` and invented a dependency in every P3-P7 brief.
    """
    lines = brief_text.splitlines()
    for index, line in enumerate(lines):
        if "**Size:**" in line:
            block: list[str] = []
            for candidate in lines[index:]:
                if not candidate.strip():
                    break
                block.append(candidate)
            return " ".join(block)
    return ""


def _header_field(header: str, name: str) -> str:
    match = re.search(
        rf"\*\*{re.escape(name)}:\*\*(.*?)(?=\*\*[A-Z][A-Za-z/ ]*:\*\*|$)", header, re.S
    )
    return " ".join(match.group(1).split()) if match else ""


def load_brief(path: pathlib.Path, relpath: str) -> Brief:
    raw = _normalise(path.read_text(encoding="utf-8"))
    number = int(BRIEF_FILE_RE.match(path.name).group(1))  # type: ignore[union-attr]
    brief_text = _split_completion_note(raw)

    title_match = re.search(r"^# EP-\d+ - (.+)$", brief_text, re.M)
    header = _header_block(brief_text)

    size = _header_field(header, "Size")
    core = _header_field(header, "Core/Stretch")
    return Brief(
        number=number,
        path=path,
        relpath=relpath,
        title=title_match.group(1).strip() if title_match else "",
        size=size.split()[0] if size else "",
        mode=_header_field(header, "Mode"),
        core=core.split()[0] if core else "",
        depends={int(n) for n in EP_TOKEN_RE.findall(_header_field(header, "Depends on"))},
        blocks={int(n) for n in EP_TOKEN_RE.findall(_header_field(header, "Blocks"))},
        sections=re.findall(r"^## (.+?)\s*$", raw, re.M),
        is_charter="> **Charter.**" in brief_text,
        text=raw,
        brief_text=brief_text,
        has_completion_note=COMPLETION_NOTE_RE.search(raw) is not None,
    )


def load_briefs(root: pathlib.Path) -> dict[int, Brief]:
    briefs: dict[int, Brief] = {}
    for path in sorted((root / "roadmap").glob("EP-*.md")):
        match = BRIEF_FILE_RE.match(path.name)
        if match:
            briefs[int(match.group(1))] = load_brief(path, f"roadmap/{path.name}")
    return briefs


@dataclass
class Row:
    phase: int
    number: int
    filename: str
    size: str
    depends: set[int]
    core: str
    done: str
    hashes: list[str]

    @property
    def ticked(self) -> bool:
        return self.done.startswith("☑")

    @property
    def landing(self) -> bool:
        """`done but not landed` - EP-6 earned this state and it recurs."""
        return self.done.startswith("◐")


def load_rows(root: pathlib.Path) -> list[Row]:
    text = _normalise((root / "roadmap" / "README.md").read_text(encoding="utf-8"))
    rows: list[Row] = []
    phase = -1
    for line in text.splitlines():
        phase_match = re.match(r"^## Phase P(\d) ", line)
        if phase_match:
            phase = int(phase_match.group(1))
            continue
        if phase < 0 or not line.startswith("| EP-"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 6:
            continue
        link = re.search(r"\]\(([^)]+)\)", cells[1])
        rows.append(
            Row(
                phase=phase,
                number=int(EP_TOKEN_RE.match(cells[0]).group(1)),  # type: ignore[union-attr]
                filename=link.group(1) if link else "",
                size=cells[2],
                depends=_expand_ranges(cells[3]),
                core=cells[4],
                done=cells[5],
                hashes=SHORT_HASH_RE.findall(cells[5]),
            )
        )
    return rows


def _section_body(text: str, heading: str) -> str:
    """The text under `## heading`, up to the next `## ` heading."""
    pattern = rf"^## {re.escape(heading)}\s*$\n(.*?)(?=^## |\Z)"
    match = re.search(pattern, text, re.M | re.S)
    return match.group(1) if match else ""


def _acceptance_body(brief: Brief) -> str:
    for heading in ("Verification / acceptance", "Verification / acceptance (sketch)"):
        body = _section_body(brief.brief_text, heading)
        if body:
            return body
    return ""


def _names_a_command(body: str) -> bool:
    if "```" in body:
        return True
    for span in re.findall(r"`([^`\n]+)`", body):
        words = span.strip().split()
        if words and words[0].strip("$>").lower() in COMMAND_WORDS:
            return True
    return False


def _git(root: pathlib.Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )


# -- the checks --------------------------------------------------------------


def check_hashes(root: pathlib.Path, briefs: dict[int, Brief], rows: list[Row]) -> CheckResult:
    """A done box is a claim about a commit. Resolve it, and in both directions."""
    result = CheckResult("hashes")
    for row in rows:
        if row.ticked and not row.hashes:
            result.add(f"EP-{row.number}", "ticked-without-hash", "a done box records a commit")
        for short in row.hashes:
            if _git(root, "rev-parse", "--verify", "--quiet", f"{short}^{{commit}}").returncode:
                result.add(
                    f"EP-{row.number}",
                    "hash-unresolvable",
                    f"`{short}` is not a commit in this repository",
                )
        brief = briefs.get(row.number)
        if brief is None:
            continue
        if (row.ticked or row.landing) and not brief.has_completion_note:
            result.add(
                f"EP-{row.number}",
                "no-completion-note",
                "a ticked or landing brief records what was observed",
            )
        if not row.ticked and not row.landing and brief.has_completion_note:
            result.add(
                f"EP-{row.number}",
                "note-without-tick",
                "a completion note without a ticked box hides finished work",
            )
    return result


def check_deps(briefs: dict[int, Brief]) -> CheckResult:
    """`Depends on` and `Blocks` are one relation, written twice."""
    result = CheckResult("deps")
    for number, brief in sorted(briefs.items()):
        for other in sorted(brief.depends):
            if other not in briefs:
                result.add(brief.label, "depends-on-missing", f"EP-{other} has no brief file")
            elif number not in briefs[other].blocks:
                result.add(
                    brief.label,
                    "asymmetric",
                    f"depends on EP-{other}, which does not list it under Blocks",
                )
        for other in sorted(brief.blocks):
            if other not in briefs:
                result.add(brief.label, "blocks-missing", f"EP-{other} has no brief file")
            elif number not in briefs[other].depends:
                result.add(
                    brief.label,
                    "asymmetric",
                    f"blocks EP-{other}, which does not list it under Depends on",
                )

    colour: dict[int, int] = {}
    seen_cycles: set[tuple[int, ...]] = set()

    def visit(node: int, trail: list[int]) -> None:
        colour[node] = 1
        for nxt in sorted(briefs[node].depends & briefs.keys()):
            if colour.get(nxt) == 1:
                cycle = tuple(trail[trail.index(nxt) :]) if nxt in trail else (nxt,)
                if min(cycle) not in {min(c) for c in seen_cycles}:
                    seen_cycles.add(cycle)
                    result.add(
                        f"EP-{nxt}",
                        "cycle",
                        " -> ".join(f"EP-{n}" for n in [*cycle, nxt]),
                    )
            elif colour.get(nxt, 0) == 0:
                visit(nxt, [*trail, nxt])
        colour[node] = 2

    for number in sorted(briefs):
        if colour.get(number, 0) == 0:
            visit(number, [number])
    return result


def size_mix(rows: list[Row]) -> tuple[dict[str, int], float]:
    mix = {size: sum(1 for row in rows if row.size == size) for size in ("S", "M", "L")}
    return mix, sum(mix[size] * SIZE_HOURS[size] for size in mix)


def check_table(root: pathlib.Path, briefs: dict[int, Brief], rows: list[Row]) -> CheckResult:
    """The tables and the files are one plan, and the header is derived from it."""
    result = CheckResult("table")

    # `load_briefs` keys by number, so a second file matching `EP-<n>-*.md`
    # would not collide loudly - it would silently shadow the first, and every
    # other check would then run against whichever one sorted last. EP-8 came
    # one filename away from doing this to itself with a pickup-gate note.
    by_number: dict[int, list[str]] = {}
    for path in sorted((root / "roadmap").glob("EP-*.md")):
        match = BRIEF_FILE_RE.match(path.name)
        if match:
            by_number.setdefault(int(match.group(1)), []).append(path.name)
    for number, names in sorted(by_number.items()):
        if len(names) > 1:
            result.add(
                f"EP-{number}",
                "duplicate-number",
                f"{len(names)} files share this number: {', '.join(names)}",
            )

    listed = {row.number for row in rows}
    for number in sorted(briefs.keys() - listed):
        result.add(f"EP-{number}", "file-without-row", "a brief no phase table lists")
    for row in rows:
        brief = briefs.get(row.number)
        if brief is None:
            result.add(f"EP-{row.number}", "row-without-file", f"no `roadmap/{row.filename}`")
            continue
        if row.filename != brief.path.name:
            result.add(f"EP-{row.number}", "wrong-link", f"the row links `{row.filename}`")
        if row.size != brief.size:
            result.add(
                f"EP-{row.number}", "size-mismatch", f"table {row.size!r}, brief {brief.size!r}"
            )
        if row.core != brief.core:
            result.add(
                f"EP-{row.number}", "core-mismatch", f"table {row.core!r}, brief {brief.core!r}"
            )
        if row.depends != brief.depends:
            result.add(
                f"EP-{row.number}",
                "depends-mismatch",
                f"table {sorted(row.depends)}, brief header {sorted(brief.depends)}",
            )

    mix, hours = size_mix(rows)
    recomputed = f"{mix['S']} S | {mix['M']} M | {mix['L']} L ~ {hours:g} h"
    result.notes.append(
        f"  size mix recomputed from {len(rows)} table rows: {recomputed}"
        f"   (S={SIZE_HOURS['S']:g}h, M={SIZE_HOURS['M']:g}h, L={SIZE_HOURS['L']:g}h - D-22)"
    )
    readme = (root / "roadmap" / "README.md").read_text(encoding="utf-8")
    declared = re.search(
        r"Current mix: \*\*(\d+) S · (\d+) M · (\d+) L ≈ (\d+(?:\.\d+)?) h\*\*",
        readme,
    )
    if declared is None:
        result.add(
            "roadmap/README.md",
            "no-size-mix",
            "the header carries no `Current mix: **n S | n M | n L = n h**` line",
        )
    else:
        found = (
            f"{declared.group(1)} S | {declared.group(2)} M | "
            f"{declared.group(3)} L ~ {float(declared.group(4)):g} h"
        )
        if found != recomputed:
            result.add(
                "roadmap/README.md",
                "size-mix-stale",
                f"the header says {found}; the tables say {recomputed}",
            )
    return result


def check_sections(briefs: dict[int, Brief]) -> CheckResult:
    """The template is a contract; the charter brief is its declared variant.

    Order is checked over the canonical headings only, and a heading is counted
    at its first occurrence. Two things make that the right rule rather than a
    concession. A completion note may restate a heading - EP-2's does - and a
    completion note may be appended above the `## Parked ->` section rather
    than below it, which EP-3 and EP-4 both did. Executed briefs are
    append-only (`CLAUDE.md`), so neither can be tidied; a checker that
    demanded otherwise would be demanding a rule violation.
    """
    result = CheckResult("sections")
    for _, brief in sorted(briefs.items()):
        expected = CHARTER_SECTIONS if brief.is_charter else CANON_SECTIONS
        seen: list[str] = []
        for heading in brief.sections:
            if heading in expected and heading not in seen:
                seen.append(heading)
        if seen != list(expected):
            missing = [s for s in expected if s not in seen]
            if missing:
                result.add(brief.label, "missing-section", f"no `## {missing[0]}`")
            else:
                result.add(
                    brief.label,
                    "section-order",
                    f"canonical sections run {seen}, expected {list(expected)}",
                )
        if not _section_body(brief.brief_text, "Safety preconditions").strip():
            result.add(
                brief.label,
                "empty-safety-preconditions",
                "`n/a` counts and must be written; an omitted or empty section does not",
            )
    return result


def _charter_upgrader(brief: Brief) -> int | None:
    """The **first** EP named in the charter note, which is the one that upgrades it.

    The note names others in passing - the brief whose cell count a quota
    waits on, the phase a re-plan re-charters - and counting all of them made
    the exemption inventory read `EP-25 (upgraded by EP-23, EP-24)`, which is
    false. Every charter follows the same convention: the upgrader comes
    first and in bold. So the first token is the answer and the rest are
    context.
    """
    match = re.search(r"^> \*\*Charter\.\*\*.*?(?=\n\n)", brief.brief_text, re.M | re.S)
    if match is None:
        return None
    named = EP_TOKEN_RE.search(match.group(0))
    return int(named.group(1)) if named else None


def check_acceptance(briefs: dict[int, Brief]) -> CheckResult:
    """A criterion nobody can run is a wish.

    A charter brief is the one declared exception, and it is an exception with
    a price. Its criteria are a sketch by construction - its own note says "do
    not execute from the sketch alone" and promises that each sketched
    criterion becomes a named command or artifact at the re-plan that upgrades
    it. So a charter is exempt from naming a command and is instead required to
    name the brief that will make it name one. The exemptions are counted and
    listed, because a charter nobody ever upgrades is exactly the failure this
    check exists to surface.
    """
    result = CheckResult("acceptance")
    exempt: list[str] = []
    for _, brief in sorted(briefs.items()):
        body = _acceptance_body(brief)
        if not body.strip():
            result.add(brief.label, "no-acceptance-section", "no verification/acceptance section")
            continue
        if brief.is_charter:
            upgrader = _charter_upgrader(brief)
            if upgrader is None:
                result.add(
                    brief.label,
                    "charter-without-upgrader",
                    "a charter note that names no re-plan EP is a permanent sketch",
                )
            elif upgrader not in briefs:
                result.add(
                    brief.label,
                    "upgrader-missing",
                    f"names EP-{upgrader}, which has no brief file",
                )
            exempt.append(
                f"{brief.label} (upgraded by {f'EP-{upgrader}' if upgrader else 'nobody'})"
            )
            continue
        if not _names_a_command(body):
            result.add(
                brief.label,
                "no-command",
                "acceptance names no fenced block and no command token",
            )
    if exempt:
        result.notes.append(
            f"  {len(exempt)} charter brief(s) exempt from naming a command, each naming its\n"
            "  upgrader instead - every exemption, inventoried:"
        )
        for index in range(0, len(exempt), 3):
            result.notes.append("    " + " | ".join(exempt[index : index + 3]))
    return result


def load_hazards(root: pathlib.Path) -> dict[int, tuple[set[int], str]]:
    """`DESIGN.md` 14 is the single hazard register (owner ruling OD-11)."""
    design = _normalise((root / "epppsynth" / "DESIGN.md").read_text(encoding="utf-8"))
    section = re.search(r"^## 14\. .*?(?=^## 15\.|\Z)", design, re.M | re.S)
    hazards: dict[int, tuple[set[int], str]] = {}
    if section is None:
        return hazards
    for line in section.group(0).splitlines():
        if not line.startswith("| R-"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 7:
            continue
        match = HAZARD_ID_RE.match(cells[0])
        if match:
            hazards[int(match.group(1))] = (
                {int(n) for n in EP_TOKEN_RE.findall(cells[5])},
                cells[6],
            )
    return hazards


def check_hazards(root: pathlib.Path, briefs: dict[int, Brief]) -> CheckResult:
    """A hazard with no owning brief is a hazard nobody is carrying."""
    result = CheckResult("hazards")
    hazards = load_hazards(root)
    if not hazards:
        result.add("epppsynth/DESIGN.md", "no-register", "section 14 holds no hazard rows")
        return result
    for missing in sorted(set(range(1, max(hazards) + 1)) - hazards.keys()):
        result.add(f"R-{missing}", "hazard-missing", "the register is not contiguous")
    for number, (named, gate) in sorted(hazards.items()):
        if not named:
            result.add(f"R-{number}", "no-brief", "names no mitigating brief")
        for ep in sorted(named - briefs.keys()):
            result.add(f"R-{number}", "brief-missing", f"names EP-{ep}, which has no brief file")
        if not gate or gate in {"-", "n/a"}:
            result.add(f"R-{number}", "no-gate", "names no verifying gate")

    for _, brief in sorted(briefs.items()):
        for cited in sorted(
            {int(n) for n in HAZARD_ID_RE.findall(brief.brief_text)} - hazards.keys()
        ):
            result.add(brief.label, "hazard-unknown", f"cites R-{cited}, not in the register")
        # Charter briefs are sketches by construction; `acceptance` holds them
        # to naming their upgrader instead, and this check does not double-count.
        if brief.core == "core" and not brief.is_charter:
            if not _names_a_command(_acceptance_body(brief)):
                result.add(
                    brief.label,
                    "core-without-evidence",
                    "a core brief names no acceptance artifact",
                )
    result.notes.append(
        f"  {len(hazards)} hazards, R-1 ... R-{max(hazards)}, each naming a brief and a gate"
    )
    return result


def _decisions_index(root: pathlib.Path) -> str:
    """Load-order item 3: the index block, never the whole log."""
    text = (root / "epppsynth" / "DECISIONS.md").read_text(encoding="utf-8")
    match = re.search(r"^## Index\n(.*?)\n---\n", text, re.M | re.S)
    return match.group(1) if match else ""


def _phase_slice(root: pathlib.Path, phase: int) -> str:
    """Load-order item 4: the one phase table, plus its standing decisions."""
    text = _normalise((root / "roadmap" / "README.md").read_text(encoding="utf-8"))
    section = re.search(
        rf"^## Phase P{phase} .*?(?=^## Phase P{phase + 1} |^---\s*$|\Z)", text, re.M | re.S
    )
    if section is None:
        return ""
    body = section.group(0)
    table = "\n".join(line for line in body.splitlines() if line.startswith("|"))
    standing = re.search(r"\*\*Standing decisions for P\d\.\*\*.*?(?=\n\n|\Z)", body, re.S)
    return table + "\n" + (standing.group(0) if standing else "")


def context_budget(
    root: pathlib.Path, brief: Brief, phase: int, chars_per_token: float
) -> tuple[dict[str, int], int]:
    def tokens(text: str) -> int:
        return round(len(text) / chars_per_token)

    items = {
        "1": tokens((root / "CLAUDE.md").read_text(encoding="utf-8")),
        "2": tokens((root / "epppsynth" / "GOVERNANCE.md").read_text(encoding="utf-8")),
        "3": tokens(_decisions_index(root)),
        "4": tokens(_phase_slice(root, phase)),
        "5": tokens(brief.brief_text),
    }
    return items, sum(items.values())


def check_context_budget(
    root: pathlib.Path,
    briefs: dict[int, Brief],
    rows: list[Row],
    chars_per_token: float,
    only: int | None = None,
) -> CheckResult:
    """The load order promises a cold session fits. Measure it, and say how."""
    result = CheckResult("context-budget")
    phases = {row.number: row.phase for row in rows}
    result.notes.append(
        f"  tokens are APPROXIMATED at {chars_per_token:g} characters per token - no tokenizer is\n"
        "  available offline. The figure is optimistic for dense markdown, and a real tokenizer\n"
        "  is parked in `roadmap/final-roadmap.md` so the approximation cannot become permanent.\n"
        f"  Ceiling {CONTEXT_CEILING:,} tokens over load-order items 1-5: 1 CLAUDE.md, "
        "2 GOVERNANCE.md,\n  3 the DECISIONS index block, 4 the phase table and its standing "
        "decisions, 5 the brief\n  up to its completion note."
    )
    result.notes.append(
        f"  {'brief':<8}{'phase':<7}{'1':>7}{'2':>7}{'3':>7}{'4':>7}{'5':>8}"
        f"{'total':>9}{'margin':>9}"
    )
    tightest: tuple[int, str] | None = None
    for number, brief in sorted(briefs.items()):
        if only is not None and number != only:
            continue
        phase = phases.get(number)
        if phase is None:
            result.add(brief.label, "no-phase", "no phase table lists this brief")
            continue
        items, total = context_budget(root, brief, phase, chars_per_token)
        margin = CONTEXT_CEILING - total
        columns = "".join(f"{value:>7,}" for value in list(items.values())[:4])
        result.notes.append(
            f"  {brief.label:<8}P{phase:<6}{columns}{items['5']:>8,}{total:>9,}{margin:>9,}"
            f"{'   OVER' if total > CONTEXT_CEILING else ''}"
        )
        if tightest is None or margin < tightest[0]:
            tightest = (margin, brief.label)
        if total > CONTEXT_CEILING:
            result.add(
                brief.label,
                "over-budget",
                f"{total:,} tokens against a {CONTEXT_CEILING:,} ceiling - {OVER_BUDGET_REMEDY}",
            )
    if tightest is not None:
        fixed = round(
            (
                len((root / "CLAUDE.md").read_text(encoding="utf-8"))
                + len((root / "epppsynth" / "GOVERNANCE.md").read_text(encoding="utf-8"))
                + len(_decisions_index(root))
            )
            / chars_per_token
        )
        result.notes.append(
            f"  headroom: the tightest brief is {tightest[1]} with {tightest[0]:,} tokens to"
            f" spare.\n  Items 1-3 cost {fixed:,} tokens before any brief is opened - "
            f"{fixed / CONTEXT_CEILING:.0%} of the ceiling,\n  and they are paid by every session."
        )
    return result


def check_parked(root: pathlib.Path, briefs: dict[int, Brief]) -> CheckResult:
    """A parked item that exists in only one of the two places is a lost item."""
    result = CheckResult("parked")
    final = _normalise((root / "roadmap" / "final-roadmap.md").read_text(encoding="utf-8"))
    mirrored_total = 0
    for _, brief in sorted(briefs.items()):
        if not brief.has_completion_note:
            continue  # its own phase re-plan mirrors it, not this one
        # The full text, not `brief_text`: EP-3 and EP-4 carry their parked
        # section below their completion note, and both are append-only now.
        body = _section_body(brief.text, "Parked -> final-roadmap.md")
        bullets = [
            line
            for line in body.splitlines()
            if line.startswith("- ") and line.strip().lower() != "- none"
        ]
        mirrored = final.count(f"(parked at {brief.label})")
        mirrored_total += mirrored
        if mirrored != len(bullets):
            result.add(
                brief.label,
                "parked-count-mismatch",
                f"{len(bullets)} parked item(s) in the brief, {mirrored} entry(ies) tagged "
                f"`(parked at {brief.label})` in final-roadmap.md",
            )
    for key, phrase in RESIDUALS:
        if phrase not in final:
            result.add(key, "residual-missing", f"final-roadmap.md carries no {phrase!r}")
    result.notes.append(
        f"  {mirrored_total} mirrored parked entry(ies); "
        f"{len(RESIDUALS)} residual-list items checked one for one"
    )
    return result


def check_immutable(root: pathlib.Path, briefs: dict[int, Brief], rows: list[Row]) -> CheckResult:
    """An executed brief's `## Context` is the historical record, not a draft."""
    result = CheckResult("immutable")
    checked = 0
    for row in rows:
        brief = briefs.get(row.number)
        if brief is None or not row.hashes:
            continue
        commit = row.hashes[0]
        proc = _git(root, "show", f"{commit}:{brief.relpath}")
        if proc.returncode:
            result.add(
                brief.label, "blob-unreadable", f"`git show {commit}:{brief.relpath}` failed"
            )
            continue
        then = _section_body(_normalise(proc.stdout), "Context").strip()
        now = _section_body(brief.brief_text, "Context").strip()
        if not then:
            result.add(brief.label, "no-context-at-commit", f"no `## Context` at {commit}")
        elif then != now:
            result.add(
                brief.label,
                "context-edited",
                f"`## Context` differs from the blob at {commit}; annotate, never rewrite",
            )
        checked += 1
    result.notes.append(f"  {checked} executed brief(s) compared against their recorded commits")
    return result


def _evidence_name(badge: str) -> str:
    """EP-2's badge -> evidence-file mapping (D-59), as the README table states it."""
    if badge in {"design", "skeleton"}:
        return f"{badge}.md"
    mode = badge[badge.index("(") + 1]
    return f"mode-{mode}-{'gate' if badge.startswith('self-evaluated') else 'release'}.md"


def check_status(root: pathlib.Path) -> CheckResult:
    """The one rewrite a re-plan makes mandatory, checked four ways (R-9, R-36)."""
    result = CheckResult("status")
    readme = _normalise((root / "README.md").read_text(encoding="utf-8"))
    badges = BADGE_RE.findall(readme)
    if len(badges) != 1:
        result.add(
            "README.md",
            "badge-unparseable",
            f"{len(badges)} line(s) match the EP-2 badge contract; exactly one must",
        )
        return result
    badge = badges[0]
    result.notes.append(f"  badge `status: {badge}`, checked against the README paragraph,")
    result.notes.append(f"  epppsynth/docs/evidence/{_evidence_name(badge)} and CITATION.cff")

    if STATUS_LINE not in readme:
        result.add("README.md", "status-paragraph", "the D-24 status line is not in the README")

    evidence = root / "epppsynth" / "docs" / "evidence" / _evidence_name(badge)
    if not evidence.exists():
        result.add(
            f"epppsynth/docs/evidence/{evidence.name}",
            "evidence-missing",
            f"the badge claims `status: {badge}` and its evidence file does not exist",
        )
    else:
        text = _normalise(evidence.read_text(encoding="utf-8"))
        if f"**Badge string:** `status: {badge}`" not in text:
            result.add(
                f"epppsynth/docs/evidence/{evidence.name}",
                "evidence-badge-mismatch",
                f"the file does not declare `status: {badge}`",
            )
        unticked = len(re.findall(r"^- \[ \]", text, re.M))
        if unticked:
            result.add(
                f"epppsynth/docs/evidence/{evidence.name}",
                "unticked-box",
                f"{unticked} unticked box(es); the claim is not made until every box is ticked",
            )

    citation = _normalise((root / "CITATION.cff").read_text(encoding="utf-8"))
    version = re.search(r'^version: "([^"]+)"', citation, re.M)
    if version is None:
        result.add("CITATION.cff", "no-version", "no `version:` field")
    elif badge == PRE_RELEASE_BADGE and version.group(1) != PRE_RELEASE_VERSION:
        result.add(
            "CITATION.cff",
            "version-mismatch",
            f"`status: {badge}` tracks version {PRE_RELEASE_VERSION}, "
            f"the file says {version.group(1)}",
        )
    elif badge != PRE_RELEASE_BADGE and version.group(1) == PRE_RELEASE_VERSION:
        result.add(
            "CITATION.cff",
            "version-stale",
            f"the badge advanced to `{badge}` and the version still reads {PRE_RELEASE_VERSION}",
        )
    if " ".join(STATUS_LINE.split()) not in " ".join(citation.split()):
        result.add("CITATION.cff", "abstract-status", "the abstract does not carry the status line")
    return result


# -- driver ------------------------------------------------------------------


def repo_root() -> pathlib.Path:
    return pathlib.Path(__file__).resolve().parent.parent


def run(
    root: pathlib.Path,
    checks: list[str],
    *,
    chars_per_token: float = CHARS_PER_TOKEN,
    budget_only: int | None = None,
) -> Report:
    briefs = load_briefs(root)
    rows = load_rows(root)
    report = Report(root=root)
    for check in checks:
        if check == "hashes":
            report.results.append(check_hashes(root, briefs, rows))
        elif check == "deps":
            report.results.append(check_deps(briefs))
        elif check == "table":
            report.results.append(check_table(root, briefs, rows))
        elif check == "sections":
            report.results.append(check_sections(briefs))
        elif check == "acceptance":
            report.results.append(check_acceptance(briefs))
        elif check == "hazards":
            report.results.append(check_hazards(root, briefs))
        elif check == "context-budget":
            report.results.append(
                check_context_budget(root, briefs, rows, chars_per_token, budget_only)
            )
        elif check == "parked":
            report.results.append(check_parked(root, briefs))
        elif check == "immutable":
            report.results.append(check_immutable(root, briefs, rows))
        elif check == "status":
            report.results.append(check_status(root))
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="roadmap_check",
        description=(
            "The roadmap's own consistency checks (EP-8). A green run means the roadmap "
            "describes itself consistently; it is not a claim about the work."
        ),
    )
    parser.add_argument("--all", action="store_true", help="run every check; this is what CI calls")
    for check in CHECKS:
        if check == "context-budget":
            parser.add_argument(
                "--context-budget",
                nargs="?",
                const="",
                default=None,
                metavar="EP-n",
                help="run the context-budget check, for one brief or (bare) for every brief",
            )
        else:
            parser.add_argument(
                f"--{check}", action="store_const", const="", default=None, help=f"run {check}"
            )
    parser.add_argument(
        "--chars-per-token",
        type=float,
        default=CHARS_PER_TOKEN,
        help=(
            f"the context-budget approximation, default {CHARS_PER_TOKEN:g}. Stated, not "
            "measured; lower it to see how sensitive the ceiling is to the assumption."
        ),
    )
    parser.add_argument("--root", type=pathlib.Path, default=None, help="repository root")
    args = parser.parse_args(argv)

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    selected = [check for check in CHECKS if getattr(args, check.replace("-", "_")) is not None]
    if args.all or not selected:
        selected = list(CHECKS)

    budget_only = None
    if args.context_budget:
        match = EP_TOKEN_RE.fullmatch(args.context_budget.strip())
        if match is None:
            parser.error(f"--context-budget takes an EP-n, not {args.context_budget!r}")
        budget_only = int(match.group(1))

    report = run(
        args.root or repo_root(),
        selected,
        chars_per_token=args.chars_per_token,
        budget_only=budget_only,
    )
    print(report.render())
    return 0 if report.ok else 1


if __name__ == "__main__":  # pragma: no cover - CLI entry
    sys.exit(main())
