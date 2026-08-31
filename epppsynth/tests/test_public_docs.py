# SPDX-FileCopyrightText: 2026 W. Taylor Farrington
# SPDX-License-Identifier: Apache-2.0
"""EP-4 acceptance, as tests: the four root policy documents, checked mechanically.

`PRIVACY.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md` and `CONTRIBUTING.md` each make a promise a
stranger reads before anything else, and EP-4's discipline is that every promise names its
enforcement. The parts of that discipline a machine can check are here rather than in a one-time
manual pass, so they re-run in CI: the required explicit statements, the data-class table's
persistence column, the Contributor Covenant's integrity against its upstream hash, the no-PR
wording being one sentence rather than four paraphrases, link resolution, and the identity sweep.
"""

from __future__ import annotations

import hashlib
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[2]

PRIVACY = ROOT / "PRIVACY.md"
SECURITY = ROOT / "SECURITY.md"
CONDUCT = ROOT / "CODE_OF_CONDUCT.md"
CONTRIBUTING = ROOT / "CONTRIBUTING.md"
README = ROOT / "README.md"
SAFETY = ROOT / "SAFETY.md"
ISSUE_TEMPLATE = ROOT / ".github" / "ISSUE_TEMPLATE" / "discussion.yml"

NEW_FILES = (PRIVACY, SECURITY, CONDUCT, CONTRIBUTING, ISSUE_TEMPLATE)

# The two sentences that carry the contribution posture. `GOVERNANCE.md` §14 is their source, and
# they are repeated verbatim rather than paraphrased so that drift is a failing test (EP-4 step 6).
NO_PR = "No pull requests are accepted in v1."
DISCUSSION_ONLY = "Issues are open for discussion only — not support, and never clinical advice."

# SHA-256 of Contributor Covenant 2.1, verbatim, as published at
# https://raw.githubusercontent.com/EthicalSource/contributor_covenant/release/content/version/2/1/code_of_conduct.md
# with the site's TOML front matter stripped, LF line endings, one trailing newline. Recorded at
# EP-4 so the Covenant's integrity is checked without vendoring a second copy of it.
COVENANT_2_1_SHA256 = "369bf7301883368fc19203bd0f1233fed2b83f0378ad19c4d0708bf61925339b"
COVENANT_PLACEHOLDER = "[INSERT CONTACT METHOD]"
ADDENDUM_MARKER = "\n---\n\n## Project addendum (not part of the Contributor Covenant)\n"
CONTACT = "william.t.farrington@gmail.com"


def _read(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8")


def _flat(text: str) -> str:
    """Strip bold markers and collapse whitespace, so a wrapped sentence still compares."""
    return re.sub(r"\s+", " ", text.replace("**", ""))


# ── the files exist and are reachable ────────────────────────────────────────


def test_all_four_documents_exist():
    for path in (PRIVACY, SECURITY, CONDUCT, CONTRIBUTING, ISSUE_TEMPLATE):
        assert path.is_file(), path


def test_readme_and_safety_link_every_one_of_them():
    """Acceptance 1, including the SECURITY.md link EP-3 deliberately left dangling."""
    readme, safety = _read(README), _read(SAFETY)
    for name in ("PRIVACY.md", "SECURITY.md", "CODE_OF_CONDUCT.md", "CONTRIBUTING.md"):
        assert f"]({name})" in readme, name
    for name in ("PRIVACY.md", "SECURITY.md", "CODE_OF_CONDUCT.md", "CONTRIBUTING.md"):
        assert f"]({name})" in safety, name


def test_every_relative_link_in_the_new_documents_resolves():
    unresolved = []
    for path in (PRIVACY, SECURITY, CONDUCT, CONTRIBUTING):
        for target in re.findall(r"\]\(([^)]+)\)", _read(path)):
            if target.startswith(("http", "#", "mailto:", "../../")):
                continue  # ../../ is the platform-relative advisory intake; see SECURITY.md
            if not (ROOT / target.split("#", 1)[0]).exists():
                unresolved.append(f"{path.name} -> {target}")
    assert unresolved == []


# ── PRIVACY.md ───────────────────────────────────────────────────────────────


def test_privacy_data_class_table_marks_every_runtime_class_as_persisting_nothing():
    """Acceptance 4: the persistence column is `none` for every runtime data class."""
    rows = [
        line
        for line in _read(PRIVACY).splitlines()
        if line.startswith("| **") and line.count("|") == 6
    ]
    runtime = [row for row in rows if not row.startswith(("| **Logs**", "| **Benchmark data**"))]
    assert len(runtime) >= 6, rows
    for row in runtime:
        persistence = row.strip("|").split("|")[-1].strip()
        assert persistence.startswith("**none**"), row
    # The two non-runtime rows are named explicitly, so a new row cannot join them silently.
    assert len(rows) - len(runtime) == 2


def test_privacy_states_the_logging_rule_including_the_mode_b_absolute():
    """Acceptance 4: the D-52 rule, with the part that is an absolute rather than a default."""
    flat = _flat(_read(PRIVACY))
    assert "never in mode (b)" in flat
    assert "off by default" in flat
    assert "hash-only when enabled" in flat


def test_privacy_names_every_residual_channel_and_says_it_cannot_close_them():
    """Acceptance 3: the disclosure exists, cannot be skimmed past, and is honest."""
    text = _read(PRIVACY)
    assert "## 8. Residual channels this project cannot close" in text
    section = text.split("## 8. Residual channels this project cannot close", 1)[1]
    section = section.split("\n## ", 1)[0]
    for channel in ("Windows Error Reporting", "page file", "GPU memory", "bfcache"):
        assert channel in section, channel
    # Four of the five channels say so in the same words; the fifth is the machine-software one.
    assert section.count("cannot close th") >= 4


def test_privacy_enforcement_register_leaves_no_promise_without_a_mechanism():
    """Acceptance 2, mechanised: every register row fills mechanism, brief and proof, or is §8."""
    rows = [line for line in _read(PRIVACY).splitlines() if re.match(r"^\| \d+ \|", line)]
    assert len(rows) >= 13
    for row in rows:
        cells = [cell.strip() for cell in row.strip("|").split("|")]
        assert len(cells) == 6, row
        assert all(cells), row
        mechanism, built_by, proved_by = cells[2], cells[3], cells[4]
        if mechanism.startswith("**no mechanism"):
            # The single permitted shape: a channel disclosed rather than closed.
            assert built_by == "—" and proved_by == "—", row
            continue
        assert re.search(r"EP-\d+", built_by), row
        assert proved_by, row


def test_privacy_enumerates_the_trainee_guarantee_with_an_enforcement_per_item():
    """D-19 written as six promises, each naming what makes it true and who builds it."""
    text = _read(PRIVACY)
    section = text.split("## 6. The trainee non-surveillance guarantee", 1)[1].split("\n## ", 1)[0]
    for promise in (
        "**No accounts.**",
        "**No scoring.**",
        "**No retention.**",
        "**No export.**",
        "**No employer visibility.**",
        "**Voluntary use only.**",
    ):
        assert promise in section, promise
    rows = [line for line in section.splitlines() if line.startswith("| **No ")]
    for row in rows:
        assert re.search(r"EP-\d+", row), row


# ── SECURITY.md ──────────────────────────────────────────────────────────────


def test_security_states_everything_acceptance_5_requires():
    text = _read(SECURITY)
    flat = _flat(text)
    assert "## Supported versions" in text
    assert "there is no released version" in flat
    assert "security/advisories/new" in text
    assert "loopback is not treated as a security boundary" in flat
    assert "Best effort. No SLA." in flat
    assert "Coordinated disclosure window: 90 days." in flat
    assert "Third-party deployments." in flat
    assert "This project holds no runtime credentials." in flat
    assert "only the latest tag is supported" in flat.lower()
    assert "Tags are **immutable**" in text or "Tags are immutable" in flat


def test_security_states_the_model_loading_rules_as_security_rules():
    flat = _flat(_read(SECURITY))
    for rule in (
        "revision SHA",
        "SHA-256 verified before load",
        "Remote code execution disabled unconditionally",
        "No pickle formats",
        "GGUF or safetensors only",
        "No auto-download at runtime",
        "Embedding models are models",
    ):
        assert rule in flat, rule


def test_security_links_the_threat_model_as_planned_and_does_not_summarise_it():
    text = _read(SECURITY)
    assert "*planned — EP-38*" in text
    assert "](roadmap/EP-38" not in text  # planned work is never rendered as a link (EP-2)


def test_security_names_no_supported_version():
    """Acceptance 5's first item, as a table a reader cannot misread."""
    table = [line for line in _read(SECURITY).splitlines() if line.startswith("| — |")]
    assert table == ["| — | there is no released version |"]


# ── CODE_OF_CONDUCT.md ───────────────────────────────────────────────────────


def test_conduct_is_contributor_covenant_2_1_unedited_apart_from_contact_and_addendum():
    """Acceptance 7, as a hash rather than as an eyeball diff."""
    text = _read(CONDUCT)
    assert "Contributor Covenant" in text
    assert "version 2.1" in text
    assert ADDENDUM_MARKER in text
    covenant, addendum = text.split(ADDENDUM_MARKER, 1)
    assert covenant.count(f"<{CONTACT}>") == 1
    restored = covenant.replace(f"<{CONTACT}>", COVENANT_PLACEHOLDER)
    digest = hashlib.sha256(restored.encode("utf-8")).hexdigest()
    assert digest == COVENANT_2_1_SHA256, "the Covenant text above the addendum has been edited"
    assert COVENANT_PLACEHOLDER not in text  # the contact is filled in, not left as a placeholder
    assert addendum.count("## ") == 0  # exactly one added section, not several


def test_conduct_addendum_is_marked_as_not_part_of_the_covenant():
    addendum = _read(CONDUCT).split(ADDENDUM_MARKER, 1)[1]
    assert "is not part of the Covenant" in addendum
    assert "verbatim" in addendum


# ── CONTRIBUTING.md ──────────────────────────────────────────────────────────


def test_contributing_is_ten_lines_or_fewer():
    """Acceptance 8. Counted over every line in the file, blanks included."""
    assert len(_read(CONTRIBUTING).splitlines()) <= 10


def test_contributing_states_the_posture_the_reason_and_the_trigger():
    flat = _flat(_read(CONTRIBUTING))
    assert NO_PR in flat
    assert "not a product" in flat
    assert "D-33" in flat and "D-34" in flat and "D-27" in flat
    assert "EP-37" in flat  # what would change it names its brief


# ── one posture, stated once ─────────────────────────────────────────────────


def test_the_no_pr_wording_is_identical_everywhere_it_appears():
    """Acceptance 10: compared programmatically, because four paraphrases are four claims."""
    for path in (README, SAFETY, CONTRIBUTING, CONDUCT, SECURITY, ISSUE_TEMPLATE):
        flat = _flat(_read(path))
        assert NO_PR in flat, path.name
        assert DISCUSSION_ONLY in flat, path.name


def test_no_stale_ep4_planned_markers_survive():
    """The four files exist now, so nothing may still call them planned work."""
    for path in (README, SAFETY):
        text = _read(path)
        for name in ("PRIVACY.md", "SECURITY.md", "CODE_OF_CONDUCT.md", "CONTRIBUTING.md"):
            for match in re.finditer(re.escape(name), text):
                tail = text[match.end() : match.end() + 120]
                assert "planned — EP-4" not in tail, f"{path.name}: {name}"


# ── the identity sweep ───────────────────────────────────────────────────────

# EP-4 step 9, as a test rather than a one-time pass. The two declared roots are the only absolute
# paths any public file may contain (D-30, D-51); everything else is a machine identifier.
# leak-scan-allow: rule-definition
IDENTITY_PATTERNS = (
    r"C:\\Users\\",
    r"\\\\[A-Za-z0-9]",  # a UNC path is a machine name by definition
    r"[A-Z]:\\(?!epppmodels|epppindex)",
    r"\$env:USERNAME|%USERNAME%|%USERPROFILE%",
)


def test_identity_sweep_over_the_new_files_returns_nothing():
    """Acceptance 9. The sweep runs over the four documents plus the issue template."""
    hits = []
    for path in NEW_FILES:
        text = _read(path)
        for pattern in IDENTITY_PATTERNS:
            for match in re.finditer(pattern, text):
                line = text.count("\n", 0, match.start()) + 1
                hits.append(f"{path.name}:{line}: {match.group(0)!r}")
    assert hits == []


def test_the_only_absolute_paths_in_the_new_files_are_the_two_declared_roots():
    found = set()
    for path in NEW_FILES:
        found.update(re.findall(r"[A-Z]:\\[A-Za-z0-9_\\-]*", _read(path)))
    assert found <= {r"C:\epppmodels", r"C:\epppindex"}, found
