# SPDX-FileCopyrightText: 2026 W. Taylor Farrington
# SPDX-License-Identifier: Apache-2.0
"""EP-3 acceptance, as tests: the charter's structural promises, checked mechanically.

`SAFETY.md` is consumed programmatically by four later work packets, so its shape is a contract
rather than a matter of prose style. Everything here is an acceptance criterion of EP-3 that could
otherwise only be verified by eye.
"""

from __future__ import annotations

import importlib.util
import pathlib
import re
import tomllib

ROOT = pathlib.Path(__file__).resolve().parents[2]
SAFETY = ROOT / "SAFETY.md"
BANNED = ROOT / "epppsynth" / "copy" / "banned-phrases.toml"
RENDERER = ROOT / "tools" / "render_banned_phrases.py"

# Byte lengths recorded by EP-2 for the approved public strings. Assert on bytes, not on
# character count: the em dash is U+2014, three bytes, so the status line is 82 chars / 84 bytes.
STATUS_LINE = "Design and planning artifact — v1 in progress; no release, no demo, no validation."
STATUS_BYTES = 84
RISK_DETECTOR = (
    "This tool is not a risk detector and must not be used as one. "
    "It never checks what is typed for danger."
)
RISK_DETECTOR_BYTES = 103


def _text() -> str:
    return SAFETY.read_text(encoding="utf-8")


def _flat(text: str) -> str:
    """Strip bold markers and collapse whitespace, so a wrapped sentence still compares."""
    return re.sub(r"\s+", " ", text.replace("**", ""))


def _renderer():
    spec = importlib.util.spec_from_file_location("render_banned_phrases", RENDERER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# ── the machine-readable half ────────────────────────────────────────────────


def test_banned_phrases_parse_and_are_complete():
    entries = tomllib.loads(BANNED.read_text(encoding="utf-8"))["phrases"]
    assert len(entries) >= 16
    for entry in entries:
        assert entry["phrase"].strip()
        assert entry["reason"].strip()
        assert entry["d_ref"].strip()
    ids = [entry["id"] for entry in entries]
    assert len(set(ids)) == len(ids)


def test_safety_renders_the_banned_phrase_file_entry_for_entry():
    module = _renderer()
    assert module.main(["--check"]) == 0
    text = _text()
    block = text.split(module.BEGIN, 1)[1].split(module.END, 1)[0]
    for entry in module.load():
        assert entry["id"] in block
        assert entry["phrase"] in block
        assert entry["reason"] in block


# ── the approved public text ─────────────────────────────────────────────────


def test_approved_strings_are_verbatim_and_the_recorded_byte_length():
    text = _text()
    assert STATUS_LINE in text.splitlines()
    assert len(STATUS_LINE.encode("utf-8")) == STATUS_BYTES
    assert RISK_DETECTOR in _flat(text)
    assert len(RISK_DETECTOR.encode("utf-8")) == RISK_DETECTOR_BYTES


def test_risk_detector_line_is_repeated_in_the_hard_stop_section():
    """Acceptance 7: the line lives in the excluded-uses block *and* beside the escalation copy."""
    assert _flat(_text()).count(RISK_DETECTOR) >= 2


# ── the abstention taxonomy ──────────────────────────────────────────────────


def test_five_abstention_triggers_each_with_exactly_one_worked_example():
    text = _text()
    headings = re.findall(r"^### Abstention trigger ([1-5])\b", text, flags=re.MULTILINE)
    assert headings == ["1", "2", "3", "4", "5"]
    assert len(re.findall(r"^\*Example\.\*", text, flags=re.MULTILINE)) == 5


def test_over_abstention_ceiling_is_stated():
    assert "10 %" in _text()


# ── the output contract ──────────────────────────────────────────────────────


def test_retired_framings_are_named_as_retired():
    text = _text()
    for framing in ("Hidden Dynamic", "Empathic Wedge", "Consensus Generation"):
        assert framing in text


def test_deleted_fourth_part_and_surviving_prohibition():
    flat = _flat(_text())
    assert "deleted" in flat
    assert "no-ranking prohibition is unaffected" in flat


# ── hard stops, mode (c), the stop criterion ─────────────────────────────────


def test_hard_stop_section_states_the_settled_rules():
    flat = _flat(_text())
    assert "never a generative classifier" in flat
    assert "stop card in the waypoints region" in flat
    assert "If you are worried about someone's safety" in flat


def test_mode_c_charter_clause_is_verbatim():
    clause = "moral injury arises from conditions, not individual deficiency"
    assert clause in _flat(_text())


def test_stop_criterion_states_its_numbers_and_its_limits():
    flat = _flat(_text())
    assert "10 %" in flat
    assert "5 %" in flat
    assert "Wilson" in flat
    assert "A passing result is not evidence of safety." in flat


# ── the enforcement column ───────────────────────────────────────────────────


def test_every_prohibition_row_names_an_implementer_a_verifier_and_a_status():
    rows = [line for line in _text().splitlines() if re.match(r"^\| P-\d+ \|", line)]
    assert len(rows) >= 10
    for row in rows:
        cells = [cell.strip() for cell in row.strip("|").split("|")]
        assert len(cells) == 5, row
        assert all(cells), row
        assert re.search(r"EP-\d+", cells[4]), row


# ── links ────────────────────────────────────────────────────────────────────


def test_every_relative_link_resolves():
    unresolved = []
    for target in re.findall(r"\]\(([^)]+)\)", _text()):
        if target.startswith(("http", "#", "mailto:")):
            continue
        if not (ROOT / target.split("#", 1)[0]).exists():
            unresolved.append(target)
    # `SECURITY.md` was the one deliberate exception until EP-4 wrote it (EP-3 deviation 5).
    assert unresolved == []
