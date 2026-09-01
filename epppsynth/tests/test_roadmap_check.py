# SPDX-FileCopyrightText: 2026 W. Taylor Farrington
# SPDX-License-Identifier: Apache-2.0
"""Unit tests for `tools/roadmap_check.py` (EP-8), over fixture roadmaps.

Every check is tested twice: once against a fixture roadmap that is internally
consistent, and once against the same roadmap with exactly one thing broken.
A check that has only ever been seen to pass is a check nobody has seen work,
and this file is what lets the real red runs in EP-8's completion note be
seven deliberate experiments rather than seven hopes.

The fixture is a real git repository. `--hashes` resolves commits and
`--immutable` reads blobs, so a fixture built out of strings alone would test
neither. It is tiny - three briefs, one phase, two hazards - because the point
is the rule, not the roadmap.
"""

from __future__ import annotations

import importlib.util
import pathlib
import subprocess
import sys

import pytest

_TOOL = pathlib.Path(__file__).resolve().parents[2] / "tools" / "roadmap_check.py"
_SPEC = importlib.util.spec_from_file_location("roadmap_check", _TOOL)
assert _SPEC is not None and _SPEC.loader is not None
rc = importlib.util.module_from_spec(_SPEC)
sys.modules["roadmap_check"] = rc
_SPEC.loader.exec_module(rc)


# -- the fixture roadmap ------------------------------------------------------

CLAUDE = "# CLAUDE.md\n\nSession rules.\n"

GOVERNANCE = "# GOVERNANCE\n\nThe invariants.\n"

DECISIONS = """# DECISIONS

## Index

| # | Title | Decides |
|---|---|---|
| D-1 | Sizing | S/M/L = 30 min / 1 h / 2 h. |

---

**D-1 Sizing.** As above.
"""

DESIGN = """# DESIGN

## 14. Hazard register

| ID | Hazard | Affected | L/S | Prevention | Brief | Gate |
|---|---|---|---|---|---|---|
| R-1 | A thing goes wrong | readers | M/H | a mechanism | EP-0 | every publication |
| R-2 | Another thing | readers | L/M | another mechanism | EP-1 | P0 exit |

## 15. Traceability

Elsewhere.
"""

README = """# fixture

```
status: design
```

Design and planning artifact — v1 in progress; no release, no demo, no validation.
"""

CITATION = """cff-version: 1.2.0
title: "fixture"
version: "0.0.0"
abstract: >-
  Design and planning artifact — v1 in progress; no release, no demo, no
  validation.
"""

EVIDENCE = """# Evidence — `status: design`

**Badge string:** `status: design`

## Checklist

- [x] **A roadmap exists.** It does.
"""

ROADMAP_README = """# fixture roadmap

**Sizes** (D-22): Current mix: **1 S · 1 M · 1 L ≈ 3.5 h**

## Phase P0 — Fixture

| # | Brief | Size | Depends on | Core | Done |
|---|-------|------|-----------|------|------|
| EP-0 | [Alpha](EP-0-alpha.md) | S | — | core | ☑ HASH |
| EP-1 | [Beta](EP-1-beta.md) | M | EP-0 | core | ☐ |
| EP-2 | [Gamma](EP-2-gamma.md) | L | — | core | ☐ |

**Standing decisions for P0.** Nothing surprising.

---
"""

FINAL_ROADMAP = """# fixture — parked

- Scenario library in the interface — not in v1. *(parked at EP-0)*
- Export or sharing of output — not in v1.
- Trainee-controlled opt-in local retention — not in v1.
- Best-effort third-party installability — not in v1.
- Generalised corpus ingest beyond the current single-source spine — not in v1.
- Fine-tuning of any model — not in v1.
- Patient-specific point-of-care use and patient- or family-facing use are excluded.
"""

EP0 = """# EP-0 — Alpha

**Size:** S · **Mode:** n/a · **Core/Stretch:** core ·
**Depends on:** — · **Blocks:** EP-1 (beta)

## Context

The first brief. Mitigates R-1.

## Safety preconditions

n/a — this brief touches no public artifact.

## In scope

1. Do the thing.

## Out of scope

- The other thing — **EP-1**.

## Verification / acceptance

```
uv run pytest -q
```

## Parked → final-roadmap.md

- A scenario library in the interface, which v1 does not need.

---

> **Completion note (2026-08-23).** Executed as written.
"""

EP1 = """# EP-1 — Beta

**Size:** M · **Mode:** n/a · **Core/Stretch:** core ·
**Depends on:** EP-0 (alpha) · **Blocks:** —

## Context

The second brief. Mitigates R-2.

## Safety preconditions

n/a — this brief touches no public artifact.

## In scope

1. Do the other thing.

## Out of scope

- The first thing — **EP-0**.

## Verification / acceptance

1. `uv run pytest -q` exits 0.

## Parked → final-roadmap.md

- none
"""

EP2 = """# EP-2 — Gamma

**Size:** L · **Mode:** n/a · **Core/Stretch:** core ·
**Depends on:** — · **Blocks:** —

> **Charter.** **EP-1 (beta)** upgrades this to a full brief. Do not execute
> from the sketch alone.

## Context

A charter brief.

## Safety preconditions

n/a — nothing public is touched from a sketch.

## Scope sketch (refine at re-plan)

- Sketch a thing.

## Verification / acceptance (sketch)

- The thing is sketched.

## Parked → final-roadmap.md

- none
"""

FILES = {
    "CLAUDE.md": CLAUDE,
    "README.md": README,
    "CITATION.cff": CITATION,
    "epppsynth/GOVERNANCE.md": GOVERNANCE,
    "epppsynth/DECISIONS.md": DECISIONS,
    "epppsynth/DESIGN.md": DESIGN,
    "epppsynth/docs/evidence/design.md": EVIDENCE,
    "roadmap/README.md": ROADMAP_README,
    "roadmap/final-roadmap.md": FINAL_ROADMAP,
    "roadmap/EP-0-alpha.md": EP0,
    "roadmap/EP-1-beta.md": EP1,
    "roadmap/EP-2-gamma.md": EP2,
}


def _git(root: pathlib.Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", "-c", "commit.gpgsign=false", *args],
        cwd=root,
        capture_output=True,
        text=True,
        check=True,
    )
    return proc.stdout.strip()


@pytest.fixture
def roadmap(tmp_path: pathlib.Path) -> pathlib.Path:
    """A consistent fixture roadmap, in a real git repository."""
    for relpath, content in FILES.items():
        target = tmp_path / relpath
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    _git(tmp_path, "init", "-q", "-b", "main")
    # Deliberately not address-shaped. Git accepts any string here, and EP-6's
    # PHI scanner reads this file like any other: a plausible-looking address
    # in a fixture is exactly the shape it exists to refuse.
    _git(tmp_path, "config", "user.email", "fixture")
    _git(tmp_path, "config", "user.name", "Fixture")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "fixture")
    short = _git(tmp_path, "rev-parse", "--short", "HEAD")
    write(tmp_path, "roadmap/README.md", ROADMAP_README.replace("HASH", short))
    return tmp_path


def write(root: pathlib.Path, relpath: str, content: str) -> None:
    (root / relpath).write_text(content, encoding="utf-8")


def read(root: pathlib.Path, relpath: str) -> str:
    return (root / relpath).read_text(encoding="utf-8")


def failures(root: pathlib.Path, *checks: str) -> list[str]:
    """The rule ids a run produced, which is what a test should assert on."""
    report = rc.run(root, list(checks) or list(rc.CHECKS))
    return [finding.rule for finding in report.findings]


# -- the fixture is green -----------------------------------------------------


def test_the_fixture_roadmap_passes_every_check(roadmap: pathlib.Path) -> None:
    report = rc.run(roadmap, list(rc.CHECKS))
    assert report.ok, report.render()
    assert [result.check for result in report.results] == list(rc.CHECKS)


def test_every_check_is_independently_runnable(roadmap: pathlib.Path) -> None:
    for check in rc.CHECKS:
        report = rc.run(roadmap, [check])
        assert [result.check for result in report.results] == [check]
        assert report.ok, f"{check}: {report.render()}"


def test_main_exits_zero_on_a_consistent_roadmap(
    roadmap: pathlib.Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert rc.main(["--all", "--root", str(roadmap)]) == 0
    assert "no findings." in capsys.readouterr().out


def test_main_exits_one_on_an_inconsistent_roadmap(
    roadmap: pathlib.Path, capsys: pytest.CaptureFixture[str]
) -> None:
    write(roadmap, "roadmap/final-roadmap.md", FINAL_ROADMAP.replace("*(parked at EP-0)*", ""))
    assert rc.main(["--parked", "--root", str(roadmap)]) == 1
    assert "parked-count-mismatch" in capsys.readouterr().out


# -- hashes -------------------------------------------------------------------


def test_a_ticked_box_carrying_an_unresolvable_hash_fails(roadmap: pathlib.Path) -> None:
    write(roadmap, "roadmap/README.md", ROADMAP_README.replace("HASH", "0badbad"))
    assert failures(roadmap, "hashes") == ["hash-unresolvable"]


def test_a_ticked_box_with_no_hash_at_all_fails(roadmap: pathlib.Path) -> None:
    write(roadmap, "roadmap/README.md", ROADMAP_README.replace("☑ HASH", "☑"))
    assert "ticked-without-hash" in failures(roadmap, "hashes")


def test_a_ticked_brief_with_no_completion_note_fails(roadmap: pathlib.Path) -> None:
    write(roadmap, "roadmap/EP-0-alpha.md", EP0.split("\n---\n")[0])
    assert "no-completion-note" in failures(roadmap, "hashes")


def test_a_completion_note_on_an_unticked_brief_fails(roadmap: pathlib.Path) -> None:
    write(
        roadmap,
        "roadmap/EP-1-beta.md",
        EP1 + "\n---\n\n> **Completion note (2026-08-24).** Done.\n",
    )
    assert "note-without-tick" in failures(roadmap, "hashes")


def test_the_landing_state_accepts_a_note_and_still_resolves_its_hashes(
    roadmap: pathlib.Path,
) -> None:
    """`◐` is done-but-not-landed. EP-6 earned it, and the state recurs."""
    current = read(roadmap, "roadmap/README.md")
    write(roadmap, "roadmap/README.md", current.replace("☑ ", "◐ "))
    assert failures(roadmap, "hashes") == []


# -- deps ---------------------------------------------------------------------


def test_a_dependency_cycle_fails(roadmap: pathlib.Path) -> None:
    write(
        roadmap, "roadmap/EP-0-alpha.md", EP0.replace("**Depends on:** —", "**Depends on:** EP-1")
    )
    write(roadmap, "roadmap/EP-1-beta.md", EP1.replace("**Blocks:** —", "**Blocks:** EP-0"))
    assert "cycle" in failures(roadmap, "deps")


def test_a_dependency_on_a_brief_that_does_not_exist_fails(roadmap: pathlib.Path) -> None:
    write(roadmap, "roadmap/EP-1-beta.md", EP1.replace("**Blocks:** —", "**Blocks:** EP-99"))
    assert "blocks-missing" in failures(roadmap, "deps")


def test_an_asymmetric_pair_fails(roadmap: pathlib.Path) -> None:
    write(roadmap, "roadmap/EP-0-alpha.md", EP0.replace("**Blocks:** EP-1 (beta)", "**Blocks:** —"))
    assert failures(roadmap, "deps") == ["asymmetric"]


def test_a_charter_note_is_not_read_as_a_dependency(roadmap: pathlib.Path) -> None:
    """The bug this check was written blind to.

    EP-2's charter note names EP-1 as its upgrader. Reading the header to the
    next `## ` heading swept that EP-1 into `Blocks` and invented an asymmetry
    in every one of the roadmap's 31 charter briefs.
    """
    briefs = rc.load_briefs(roadmap)
    assert briefs[2].blocks == set()
    assert briefs[2].depends == set()
    assert rc._charter_upgrader(briefs[2]) == {1}


# -- table --------------------------------------------------------------------


def test_a_size_that_disagrees_with_the_brief_fails(roadmap: pathlib.Path) -> None:
    write(roadmap, "roadmap/EP-1-beta.md", EP1.replace("**Size:** M", "**Size:** L"))
    assert "size-mismatch" in failures(roadmap, "table")


def test_a_row_with_no_brief_file_fails(roadmap: pathlib.Path) -> None:
    (roadmap / "roadmap" / "EP-2-gamma.md").unlink()
    assert "row-without-file" in failures(roadmap, "table")


def test_a_stale_size_mix_in_the_header_fails(roadmap: pathlib.Path) -> None:
    current = read(roadmap, "roadmap/README.md")
    write(roadmap, "roadmap/README.md", current.replace("≈ 3.5 h", "≈ 90 h"))
    assert failures(roadmap, "table") == ["size-mix-stale"]


def test_the_size_mix_is_recomputed_from_the_tables(roadmap: pathlib.Path) -> None:
    mix, hours = rc.size_mix(rc.load_rows(roadmap))
    assert mix == {"S": 1, "M": 1, "L": 1}
    assert hours == 3.5


def test_a_range_in_the_depends_column_expands(roadmap: pathlib.Path) -> None:
    """`EP-9 … EP-15` is four briefs' worth of dependency written as two.

    The literal here is the *folded* form. `load_rows` runs `_normalise` over
    the README before parsing, so an ellipsis reaches this helper as three
    dots; testing the raw glyph would test a path that never runs.
    """
    assert rc._normalise("EP-9 … EP-15") == "EP-9 ... EP-15"
    assert rc._expand_ranges("EP-9 ... EP-15") == set(range(9, 16))
    assert rc._expand_ranges("EP-1, EP-4") == {1, 4}


# -- sections -----------------------------------------------------------------


def test_a_brief_with_no_safety_preconditions_section_fails(roadmap: pathlib.Path) -> None:
    broken = EP1.replace(
        "## Safety preconditions\n\nn/a — this brief touches no public artifact.\n\n", ""
    )
    write(roadmap, "roadmap/EP-1-beta.md", broken)
    assert failures(roadmap, "sections") == ["missing-section", "empty-safety-preconditions"]


def test_an_empty_safety_preconditions_section_fails(roadmap: pathlib.Path) -> None:
    write(
        roadmap,
        "roadmap/EP-1-beta.md",
        EP1.replace("n/a — this brief touches no public artifact.\n", ""),
    )
    assert failures(roadmap, "sections") == ["empty-safety-preconditions"]


def test_sections_out_of_order_fail(roadmap: pathlib.Path) -> None:
    swapped = (
        EP1.replace("## In scope", "## PLACEHOLDER")
        .replace("## Out of scope", "## In scope")
        .replace("## PLACEHOLDER", "## Out of scope")
    )
    write(roadmap, "roadmap/EP-1-beta.md", swapped)
    assert failures(roadmap, "sections") == ["section-order"]


def test_a_parked_section_below_a_completion_note_still_counts(roadmap: pathlib.Path) -> None:
    """EP-3 and EP-4 both did this, and executed briefs are append-only."""
    body, note = EP0.split("\n---\n")
    parked = "## Parked → final-roadmap.md"
    head, tail = body.split(parked)
    write(roadmap, "roadmap/EP-0-alpha.md", f"{head}\n---\n{note}\n{parked}{tail}")
    assert failures(roadmap, "sections") == []
    assert failures(roadmap, "parked") == []


# -- acceptance ---------------------------------------------------------------


def test_an_acceptance_section_naming_no_command_fails(roadmap: pathlib.Path) -> None:
    write(roadmap, "roadmap/EP-1-beta.md", EP1.replace("`uv run pytest -q` exits 0", "It works"))
    assert failures(roadmap, "acceptance") == ["no-command"]
    assert "core-without-evidence" in failures(roadmap, "hazards")


def test_a_fenced_block_counts_as_a_command(roadmap: pathlib.Path) -> None:
    assert rc._names_a_command("```\nanything\n```")
    assert rc._names_a_command("run `uv sync --locked` first")
    assert not rc._names_a_command("the `manifest` is written")


def test_a_charter_brief_is_exempt_but_must_name_its_upgrader(roadmap: pathlib.Path) -> None:
    assert failures(roadmap, "acceptance") == []
    write(roadmap, "roadmap/EP-2-gamma.md", EP2.replace("**EP-1 (beta)**", "a later re-plan"))
    assert failures(roadmap, "acceptance") == ["charter-without-upgrader"]


# -- hazards ------------------------------------------------------------------


def test_a_hazard_naming_no_brief_fails(roadmap: pathlib.Path) -> None:
    write(roadmap, "epppsynth/DESIGN.md", DESIGN.replace("| EP-1 | P0 exit |", "| — | P0 exit |"))
    assert "no-brief" in failures(roadmap, "hazards")


def test_a_hazard_naming_no_gate_fails(roadmap: pathlib.Path) -> None:
    write(roadmap, "epppsynth/DESIGN.md", DESIGN.replace("| EP-1 | P0 exit |", "| EP-1 | — |"))
    assert "no-gate" in failures(roadmap, "hazards")


def test_a_brief_citing_a_hazard_that_does_not_exist_fails(roadmap: pathlib.Path) -> None:
    write(roadmap, "roadmap/EP-1-beta.md", EP1.replace("Mitigates R-2", "Mitigates R-99"))
    assert "hazard-unknown" in failures(roadmap, "hazards")


def test_a_gap_in_the_register_fails(roadmap: pathlib.Path) -> None:
    write(roadmap, "epppsynth/DESIGN.md", DESIGN.replace("| R-1 |", "| R-3 |"))
    assert "hazard-missing" in failures(roadmap, "hazards")


# -- context budget -----------------------------------------------------------


def test_a_bloated_brief_fails_the_context_budget(roadmap: pathlib.Path) -> None:
    write(roadmap, "roadmap/EP-1-beta.md", EP1 + "\nfiller. " * 10_000)
    report = rc.run(roadmap, ["context-budget"])
    assert [f.rule for f in report.findings] == ["over-budget"]
    # Owner ruling OD-16: the finding carries its own remedy, so the session
    # that trips the gate is not left choosing between the four shared files.
    assert "split this brief" in report.findings[0].detail
    assert "never raise the ceiling" in report.findings[0].detail


def test_the_budget_measures_the_brief_without_its_completion_note(roadmap: pathlib.Path) -> None:
    """A completion note is the record of execution, never an instruction for it."""
    briefs = rc.load_briefs(roadmap)
    _, before = rc.context_budget(roadmap, briefs[0], 0, rc.CHARS_PER_TOKEN)
    write(roadmap, "roadmap/EP-0-alpha.md", EP0 + "\nfiller. " * 10_000)
    briefs = rc.load_briefs(roadmap)
    _, after = rc.context_budget(roadmap, briefs[0], 0, rc.CHARS_PER_TOKEN)
    assert before == after


def test_the_ratio_is_an_argument_because_it_is_an_assumption(roadmap: pathlib.Path) -> None:
    briefs = rc.load_briefs(roadmap)
    _, four = rc.context_budget(roadmap, briefs[1], 0, 4.0)
    _, three = rc.context_budget(roadmap, briefs[1], 0, 3.0)
    assert three > four
    report = rc.run(roadmap, ["context-budget"])
    assert "APPROXIMATED at 4 characters per token" in report.render()


def test_a_brief_no_phase_table_lists_fails(roadmap: pathlib.Path) -> None:
    write(roadmap, "roadmap/EP-3-delta.md", EP1.replace("EP-1", "EP-3").replace("Beta", "Delta"))
    assert "no-phase" in failures(roadmap, "context-budget")


# -- parked -------------------------------------------------------------------


def test_a_parked_item_missing_from_final_roadmap_fails(roadmap: pathlib.Path) -> None:
    write(roadmap, "roadmap/final-roadmap.md", FINAL_ROADMAP.replace(" *(parked at EP-0)*", ""))
    assert failures(roadmap, "parked") == ["parked-count-mismatch"]


def test_a_residual_item_missing_from_final_roadmap_fails(roadmap: pathlib.Path) -> None:
    write(
        roadmap,
        "roadmap/final-roadmap.md",
        FINAL_ROADMAP.replace("Fine-tuning of any model — not in v1.\n", ""),
    )
    assert failures(roadmap, "parked") == ["residual-missing"]


def test_an_unexecuted_brief_is_not_yet_mirrored(roadmap: pathlib.Path) -> None:
    """Its own phase re-plan mirrors it; this one would be mirroring the future."""
    write(roadmap, "roadmap/EP-1-beta.md", EP1.replace("- none", "- Something for later."))
    assert failures(roadmap, "parked") == []


# -- immutable ----------------------------------------------------------------


def test_an_edited_context_in_an_executed_brief_fails(roadmap: pathlib.Path) -> None:
    write(roadmap, "roadmap/EP-0-alpha.md", EP0.replace("The first brief.", "The revised brief."))
    assert failures(roadmap, "immutable") == ["context-edited"]


def test_an_annotated_context_also_fails_because_annotation_goes_elsewhere(
    roadmap: pathlib.Path,
) -> None:
    """`> **EP-n pickup note.**` is appended to the brief, not spliced into its Context."""
    write(
        roadmap,
        "roadmap/EP-0-alpha.md",
        EP0.replace("The first brief.", "The first brief.\n\n> **EP-8 pickup note.** Stale."),
    )
    assert failures(roadmap, "immutable") == ["context-edited"]


def test_editing_anything_but_the_context_is_allowed(roadmap: pathlib.Path) -> None:
    write(roadmap, "roadmap/EP-0-alpha.md", EP0.replace("1. Do the thing.", "1. Do two things."))
    assert failures(roadmap, "immutable") == []


# -- status -------------------------------------------------------------------


def test_a_badge_whose_evidence_file_is_missing_fails(roadmap: pathlib.Path) -> None:
    (roadmap / "epppsynth" / "docs" / "evidence" / "design.md").unlink()
    assert failures(roadmap, "status") == ["evidence-missing"]


def test_an_unticked_evidence_box_fails(roadmap: pathlib.Path) -> None:
    write(roadmap, "epppsynth/docs/evidence/design.md", EVIDENCE.replace("- [x]", "- [ ]"))
    assert failures(roadmap, "status") == ["unticked-box"]


def test_a_citation_version_that_outruns_the_badge_fails(roadmap: pathlib.Path) -> None:
    write(roadmap, "CITATION.cff", CITATION.replace('version: "0.0.0"', 'version: "1.0.0"'))
    assert failures(roadmap, "status") == ["version-mismatch"]


def test_a_readme_that_drops_the_status_line_fails(roadmap: pathlib.Path) -> None:
    write(roadmap, "README.md", README.replace("Design and planning artifact — v1", "Ready — v1"))
    assert failures(roadmap, "status") == ["status-paragraph"]


def test_an_abstract_that_drops_the_status_line_fails(roadmap: pathlib.Path) -> None:
    write(roadmap, "CITATION.cff", CITATION.replace("no release, no demo, no\n  validation.", "."))
    assert failures(roadmap, "status") == ["abstract-status"]


def test_the_badge_maps_to_its_evidence_file(roadmap: pathlib.Path) -> None:
    assert rc._evidence_name("design") == "design.md"
    assert rc._evidence_name("skeleton") == "skeleton.md"
    assert rc._evidence_name("self-evaluated - mode (a)") == "mode-a-gate.md"
    assert rc._evidence_name("v1 - mode (b)") == "mode-b-release.md"
