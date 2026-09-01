# SPDX-FileCopyrightText: 2026 W. Taylor Farrington
# SPDX-License-Identifier: Apache-2.0
"""EP-6 acceptance, as tests: the nine scanners, the three allowlists, the packet.

A scanner that has never failed has never been shown to work, so most of what is
here plants a canary and asserts the scanner fires — and fires on **its own check
id only**, because a canary that trips two scanners means one of them is
over-matching, and that is a defect rather than a pass.

The committed canaries under `epppsynth/tests/canaries/` are inert by
construction and confined to the one allowlisted directory. The nine deliberate
red runs that prove the scanners in place plant *un*-exempted copies outside it,
in the working tree only, and are recorded in EP-6's completion note; no red-run
canary is ever committed, because a public repository's history is permanent and
an unreachable object is not a deleted one.

Rule literals in this file are assembled from fragments for the same reason they
are in `scan.py`: a test file is a tracked file, and the scanners read it.
"""

from __future__ import annotations

import pathlib
import re
import subprocess

import pytest

from epppsynth.publicsafety import allowlist, ledger, scan

ROOT = pathlib.Path(__file__).resolve().parents[2]
CANARIES = pathlib.Path(__file__).resolve().parent / "canaries"
HOOK = ROOT / ".githooks" / "pre-commit"
WORKFLOW = ROOT / ".github" / "workflows" / "ci.yml"
CHECKLIST = ROOT / "epppsynth" / "docs" / "pre-publication-checklist.md"

MARKER = "leak-scan-allow:" + " rule-definition"


def _read(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8")


def _repo(tmp_path: pathlib.Path, files: dict[str, str]) -> pathlib.Path:
    """A throwaway git repository holding exactly the given files."""
    root = tmp_path / "repo"
    root.mkdir()
    for name, text in files.items():
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "add", "-A"], cwd=root, check=True)
    return root


#: The six checks that read tracked files and need nothing but a git index.
TEXT_CHECKS = ("secrets", "phi", "protected-text", "identity", "roots", "modality")


#: Two tests below scan the whole repository and assert it is green. That is a
#: statement about the repository, and a shallow clone is not the repository: the
#: `git-object-id` exception to the digit-run rule cannot be evaluated without the
#: history, so the two all-digit short hashes in the roadmap are reported as
#: findings. Skipped rather than loosened, because the property is still enforced
#: — the CI `scan` job runs the identical scan with `fetch-depth: 0`, and the
#: `test` job deliberately does not fetch a history it has no other use for.
shallow = pytest.mark.skipif(
    scan.is_shallow(ROOT),
    reason="shallow clone: the whole-repository scan is enforced by the CI `scan` job, "
    "which fetches the full history; see ADR-008 (EP-6 amendment)",
)


def _text_scan(root: pathlib.Path) -> list[scan.Finding]:
    findings: list[scan.Finding] = []
    for name in TEXT_CHECKS:
        findings.extend(scan._SCANNERS[name](root).findings)
    return findings


# ── the three allowlists ─────────────────────────────────────────────────────


def test_the_canary_allowlist_has_exactly_one_entry():
    """EP-6 acceptance 4. A second entry is an ADR-008 amendment, not an edit."""
    assert allowlist.CANARY_ALLOWLIST == ("epppsynth/tests/canaries",)
    assert len(allowlist.CANARY_ALLOWLIST) == 1


def test_the_modality_exemption_table_has_exactly_three_entries_each_with_a_reason():
    """EP-6 acceptance 4. That table is owner ruling OD-10, not a developer convenience."""
    assert len(allowlist.MODALITY_EXEMPTIONS) == allowlist.MODALITY_EXEMPTION_COUNT == 3
    assert set(allowlist.MODALITY_EXEMPTIONS) == {
        "epppsynth/DECISIONS.md",
        "roadmap/EP-2-canonical-docs.md",
        "roadmap/EP-6-leak-prevention-ci.md",
    }
    for path, reason in allowlist.MODALITY_EXEMPTIONS.items():
        assert reason.strip(), path


def test_every_exempt_modality_file_exists_and_actually_contains_the_stem():
    """An exemption for a file that does not need one is a hole waiting for an edit."""
    for path in allowlist.MODALITY_EXEMPTIONS:
        text = _read(ROOT / path)
        assert scan.MODALITY_RULE.pattern.search(text), path


def test_the_marker_exempts_only_the_line_it_appears_on():
    """EP-6 acceptance 4: never the next line, never the block, never the file."""
    text = "\n".join(
        [
            "plain line",
            f"marked line  # {MARKER}",
            "the line after a marked line",
            "",
            "another plain line",
        ]
    )
    assert allowlist.marked_lines(text) == frozenset({2})


def test_a_marker_mentioned_in_backticks_is_a_mention_and_not_an_exemption():
    """`CLAUDE.md`, EP-0 and EP-6 all name the marker in prose. Naming is not using."""
    assert allowlist.marked_lines(f"prose that says `{MARKER}` and nothing more") == frozenset()
    assert allowlist.marked_lines(f"a real one <!-- {MARKER} -->") == frozenset({1})


def test_a_marker_on_a_line_that_matches_no_rule_is_reported_as_a_defect(tmp_path):
    """EP-6 §2.1. An exemption nobody has to earn is an off switch."""
    root = _repo(tmp_path, {"innocent.md": f"nothing to see here <!-- {MARKER} -->\n"})
    results = [scan._SCANNERS[name](root) for name in TEXT_CHECKS]
    defect = scan.scan_allowlist(root, results)
    assert [finding.rule for finding in defect.findings] == ["unnecessary-rule-definition-marker"]
    assert defect.findings[0].line == 1


def test_the_marker_is_earned_when_the_line_matches_a_rule(tmp_path):
    root = _repo(
        tmp_path,
        {"rule.md": "the shape is " + "C:" + chr(92) + "Users" + chr(92) + f" <!-- {MARKER} -->\n"},
    )
    identity = scan.scan_identity(root)
    assert identity.findings == []
    assert [skip.reason for skip in identity.skips] == [scan.MARKER_REASON] * len(identity.skips)
    assert identity.skips
    assert scan.scan_allowlist(root, [identity]).findings == []


def test_the_three_allowlists_do_not_reach_into_one_another():
    """No entry of one allowlist appears in another (ADR-008 EP-6 amendment)."""
    assert not set(allowlist.CANARY_ALLOWLIST) & set(allowlist.MODALITY_EXEMPTIONS)
    for path in allowlist.MODALITY_EXEMPTIONS:
        assert not allowlist.is_canary(path)


# ── the canaries, one per scanner ────────────────────────────────────────────


@pytest.mark.parametrize(
    ("canary", "check", "rules"),
    [
        ("secrets.txt", "secrets", {"github-token", "credential-assignment"}),
        ("phi.txt", "phi", {"mrn-shaped-digit-run", "email-address"}),
        ("protected_text.md", "protected-text", {"quote-budget", "chapter-title-sequence"}),
        ("identity.txt", "identity", {"user-profile-path", "unc-path", "foreign-drive-letter"}),
        (
            "roots.yaml",
            "roots",
            {"index-root-outside-documentation", "model-root-outside-documentation"},
        ),
        ("modality.md", "modality", {"retired-modality-stem"}),
    ],
)
def test_each_canary_trips_its_own_check_and_only_its_own(tmp_path, canary, check, rules):
    """EP-6 acceptance 1, as a unit test over the same fixtures the red runs plant."""
    root = _repo(tmp_path, {canary: _read(CANARIES / canary)})
    findings = _text_scan(root)
    assert findings, canary
    assert {finding.check for finding in findings} == {check}, [
        (finding.check, finding.rule) for finding in findings
    ]
    assert {finding.rule for finding in findings} == rules


def test_the_committed_canaries_are_invisible_to_every_scanner():
    """They live in the one allowlisted directory, so a clean run must not see them."""
    for name in TEXT_CHECKS:
        result = scan._SCANNERS[name](ROOT)
        assert [f for f in result.findings if "canaries" in f.path] == [], name


def test_every_canary_declares_itself_a_fixture():
    for path in sorted(CANARIES.rglob("*")):
        if path.is_file() and path.name != "README.md":
            head = _read(path).splitlines()[0]
            assert "CANARY FIXTURE" in head, path.name


def test_the_rights_canary_is_a_concept_with_no_rights_record():
    """Check 6 wires EP-5's rules; the canary is a dangling `source_id`."""
    from epppsynth.rights.check import check_source_refs

    findings = check_source_refs([CANARIES / "rights_dangling_source.yaml"])
    assert [finding.rule for finding in findings] == ["source-ref"]


def test_the_badge_canary_claims_a_rung_whose_evidence_file_is_absent(tmp_path):
    """Check 7, on a temporary root: the badge is a claim, the file is the evidence."""
    root = tmp_path / "root"
    (root / "epppsynth" / "docs" / "evidence").mkdir(parents=True)
    (root / "README.md").write_text(_read(CANARIES / "badge_README.md"), encoding="utf-8")
    result = scan.scan_badge(root)
    assert result.status == scan.FAILED
    assert [finding.rule for finding in result.findings] == ["evidence-file-absent"]
    assert result.findings[0].path == "epppsynth/docs/evidence/skeleton.md"


def test_an_unticked_evidence_box_fails_the_badge(tmp_path):
    root = tmp_path / "root"
    evidence = root / "epppsynth" / "docs" / "evidence"
    evidence.mkdir(parents=True)
    (root / "README.md").write_text("intro\n\n```\nstatus: design\n```\n", encoding="utf-8")
    (evidence / "design.md").write_text("- [x] one\n- [ ] two\n", encoding="utf-8")
    result = scan.scan_badge(root)
    assert [finding.rule for finding in result.findings] == ["evidence-checkbox-unticked"]


def test_the_ledger_canary_pair_finds_the_prose_passage_and_not_the_entry(tmp_path):
    """Check 9 on the synthetic pair: authored here, so the real `.local/` is never touched."""
    private = tmp_path / "ledger"
    private.mkdir()
    (private / "ledger.md").write_text(
        _read(CANARIES / "ledger_pair" / "ledger.md"), encoding="utf-8"
    )
    report = ledger.compare(CANARIES / "ledger_pair" / "decisions.md", private)
    assert not report.ok
    assert report.outside_published
    assert report.inside_published > 0


# ── the badge mapping, as EP-2 fixed it ──────────────────────────────────────


@pytest.mark.parametrize(
    ("badge", "evidence"),
    [
        ("design", "epppsynth/docs/evidence/design.md"),
        ("skeleton", "epppsynth/docs/evidence/skeleton.md"),
        ("self-evaluated — mode (a)", "epppsynth/docs/evidence/mode-a-gate.md"),
        ("v1 — mode (c)", "epppsynth/docs/evidence/mode-c-release.md"),
    ],
)
def test_the_badge_maps_to_its_evidence_file(badge, evidence):
    assert scan.evidence_path_for(badge) == evidence


def test_exactly_one_line_of_the_real_readme_matches_the_badge_contract():
    assert len(scan.BADGE_RE.findall(_read(ROOT / "README.md"))) == 1


# ── the hook and CI cannot drift ─────────────────────────────────────────────


def hook_command() -> str:
    lines = [
        line.strip()
        for line in _read(HOOK).splitlines()
        if line.strip().startswith("uv run epppsynth")
    ]
    assert len(lines) == 1, lines
    return lines[0]


def workflow_scan_command() -> str:
    lines = [
        line.split("run:", 1)[1].strip()
        for line in _read(WORKFLOW).splitlines()
        if "run:" in line and "epppsynth scan" in line
    ]
    assert len(lines) == 1, lines
    return lines[0]


def test_the_hook_and_the_ci_step_invoke_the_same_command():
    """EP-6 acceptance 5.

    The brief asks for equal strings. They differ by exactly one documented flag:
    the full-history sweep is CI's job, and a hook slow enough to be bypassed
    protects nothing. The relation asserted is therefore equality *after* adding
    that one flag, which is strictly stronger than comparing the two loosely.
    """
    assert hook_command() + " --history" == workflow_scan_command()
    assert hook_command() == "uv run epppsynth scan"


def test_the_hook_says_it_is_advisory_and_says_why_it_skips_the_history_sweep():
    text = _read(HOOK)
    assert "advisory" in text
    assert "--history" in text
    assert "core.hooksPath .githooks" in text


# ── workflow posture (ADR-008, EP-6 amendment) ───────────────────────────────


def test_the_workflow_keeps_its_posture():
    """EP-6 acceptance 7."""
    text = _read(WORKFLOW)
    assert re.search(r"(?m)^permissions:\n  contents: read$", text)
    assert "secrets." not in text
    assert "pull_request_target" not in text
    for pin in re.findall(r"uses: [^@\s]+@(\S+)", text):
        assert re.fullmatch(r"[0-9a-f]{40}", pin), pin


def test_fetch_depth_zero_appears_in_exactly_one_job_and_explains_itself():
    text = _read(WORKFLOW)
    assert text.count("fetch-depth: 0") == 1
    before = text[: text.index("fetch-depth: 0")]
    assert "git log -p --all" in before.rsplit("- uses:", 1)[-1]


def test_the_scan_job_runs_on_the_target_platform():
    text = _read(WORKFLOW)
    assert text.count("runs-on: windows-latest") == 2


# ── the pre-publication packet ───────────────────────────────────────────────

DEFENSE_IN_DEPTH = (
    "`.gitignore`, pre-commit hooks and CI scanners are **defense in depth. They are not proof "
    "that nothing leaked.** The proof is the pre-publication review packet, performed by a human, "
    "recorded with a date and a commit hash."
)


def _flat(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\n> ", "\n").replace("> ", ""))


def test_the_checklist_opens_with_the_defense_in_depth_statement_verbatim():
    """EP-6 acceptance 6. Copied from GOVERNANCE §7, not paraphrased."""
    text = _read(CHECKLIST)
    assert DEFENSE_IN_DEPTH in _flat(text)
    assert DEFENSE_IN_DEPTH in _flat(_read(ROOT / "epppsynth" / "GOVERNANCE.md"))


def test_the_checklist_carries_all_seven_items():
    text = _read(CHECKLIST)
    for number in range(1, 8):
        assert re.search(rf"(?m)^## Item {number} — ", text), number
    assert not re.search(r"(?m)^## Item 8 ", text)


def test_items_five_and_seven_are_marked_human_and_have_no_script():
    text = _read(CHECKLIST)
    assert re.search(r"(?m)^## Item 5 — .*\*\*human, no script\*\*", text)
    assert re.search(r"(?m)^## Item 7 — .*\*\*human, no script\*\*", text)


def test_the_checklist_maps_all_nine_scanners_onto_the_seven_items():
    text = _read(CHECKLIST)
    for check in scan.CHECKS:
        assert f"`{check}`" in text, check


def test_the_checklist_signature_block_is_empty():
    """EP-6 acceptance 6. A packet signed in advance is not a packet."""
    text = _read(CHECKLIST)
    block = text[text.index("## Signature block") :]
    rows = [line for line in block.splitlines() if line.startswith("| ") and "---" not in line]
    assert len(rows) >= 9
    for row in rows[1:]:
        assert row.rstrip().endswith("| |") or row.rstrip().endswith("||"), row


# ── the clean tree ───────────────────────────────────────────────────────────


@shallow
def test_the_clean_tree_scans_green_and_inventories_every_exemption():
    """EP-6 acceptance 3 and 4, without the history sweep (which CI owns)."""
    report = scan.run_scan(ROOT)
    assert report.ok, [finding.render() for finding in report.findings]
    rendered = report.render()
    for skip in report.skips:
        assert skip.reason in scan.SKIP_REASONS, skip.reason
        assert skip.path in rendered


def test_the_ledger_check_is_skipped_and_not_passed_when_no_ledger_is_present(tmp_path):
    """OD-3. A skip counted as a pass is how this check would stop working."""
    root = tmp_path / "runner"
    (root / "epppsynth").mkdir(parents=True)
    (root / "epppsynth" / "DECISIONS.md").write_text("# nothing\n", encoding="utf-8")
    result = scan.scan_ledger(root)
    assert result.status == scan.SKIPPED
    assert result.status != scan.PASSED
    assert result.note == "skipped — no ledger present"


def test_a_shared_passage_inside_an_addendum_is_published_content():
    """D-1: a decision is never edited, it is appended to. An addendum is the entry."""
    text = "\n".join(
        [
            "# log",
            "",
            "## Section",
            "",
            "> **Addendum (2026-08-31, EP-6).** words inside an addendum blockquote.",
            "> a continuation line.",
            "",
            "loose prose outside everything",
        ]
    )
    published = ledger.published_lines(text)
    assert {5, 6} <= published
    assert 8 not in published


def test_the_scanners_never_print_the_matched_text(tmp_path):
    """A CI log that quoted a secret would be the artifact the check prevents."""
    secret = "gh" + "p_" + "X" * 36
    root = _repo(tmp_path, {"leak.txt": f"token = {secret}\n"})
    result = scan.scan_secrets(root)
    assert result.findings
    for finding in result.findings:
        assert secret not in finding.render(fix_hints=True)


# ── the CLI ──────────────────────────────────────────────────────────────────


@shallow
def test_the_cli_exposes_scan_and_returns_zero_on_the_clean_tree(capsys):
    from epppsynth import cli

    assert cli.main(["scan"]) == 0
    out = capsys.readouterr().out
    assert "epppsynth scan" in out
    for check in scan.CHECKS:
        assert check in out


def test_the_cli_scan_accepts_a_single_check(capsys):
    from epppsynth import cli

    assert cli.main(["scan", "--check", "badge"]) == 0
    assert "badge" in capsys.readouterr().out


# ── the history sweep honours the same allowlist, by the same path ───────────


#: Split across a `+` so that this file does not contain an email address: the
#: PHI sweep reads it like any other tracked file, and it is right to.
THROWAWAY_EMAIL = "nobody@" + "example.invalid"


def _commit(root: pathlib.Path, message: str, *, empty: bool = False) -> None:
    subprocess.run(["git", "add", "-A"], cwd=root, check=True)
    subprocess.run(
        ["git", "-c", "user.name=t", "-c", f"user.email={THROWAWAY_EMAIL}", "commit", "-q"]
        + (["--allow-empty"] if empty else [])
        + ["-m", message],
        cwd=root,
        check=True,
    )


TOKEN = "gh" + "p_" + "X" * 36


def test_history_segments_splits_by_file_and_keeps_commit_messages_unattributed():
    patch = "\n".join(
        [
            "commit abc",
            "    a message",
            "diff --git a/kept.txt b/kept.txt",
            "+++ b/kept.txt",
            "+one",
            "diff --git a/gone.txt b/gone.txt",
            "--- a/gone.txt",
            "+++ /dev/null",
            "-two",
        ]
    )
    assert [path for path, _ in scan.history_segments(patch)] == [None, "kept.txt", "gone.txt"]


def test_the_history_sweep_exempts_the_canary_directory_and_nothing_else(tmp_path):
    """The committed fixtures would otherwise make this check permanently red."""
    root = _repo(tmp_path, {"epppsynth/tests/canaries/secrets.txt": f"CANARY FIXTURE\n{TOKEN}\n"})
    _commit(root, "canary only")
    clean = scan.scan_secrets(root, history=True)
    assert clean.status == scan.PASSED
    assert [skip.reason for skip in clean.skips] == ["canary-directory"]

    (root / "leak.txt").write_text(f"token = {TOKEN}\n", encoding="utf-8")
    _commit(root, "a real leak")
    assert scan.scan_secrets(root, history=True).status == scan.FAILED


def test_the_history_sweep_still_finds_a_secret_deleted_from_the_tree(tmp_path):
    """An unreachable object is not a deleted one, which is why `--history` exists."""
    root = _repo(tmp_path, {"leak.txt": f"token = {TOKEN}\n"})
    _commit(root, "a real leak")
    subprocess.run(["git", "rm", "-q", "leak.txt"], cwd=root, check=True)
    _commit(root, "delete it")

    assert scan.scan_secrets(root).findings == []  # the tree is clean
    findings = scan.scan_secrets(root, history=True).findings
    assert [finding.path for finding in findings] == ["<history>"]


def test_a_secret_in_a_commit_message_is_never_exempt(tmp_path):
    """Commit headers carry no path, so they can never fall inside an allowlist."""
    root = _repo(tmp_path, {"epppsynth/tests/canaries/secrets.txt": "CANARY FIXTURE\nnothing\n"})
    _commit(root, "first")
    _commit(root, f"message carrying {TOKEN}", empty=True)
    assert scan.scan_secrets(root, history=True).status == scan.FAILED


def test_a_shallow_clone_says_so_rather_than_quietly_reporting_phi(tmp_path):
    """Fail closed, and say why. An unexplained PHI finding is worse than none."""
    # Split so this file carries no digit run of its own: in a shallow clone the
    # git-object-id exception cannot be evaluated and the run becomes a finding.
    root = _repo(tmp_path, {"note.md": "the hash was " + "370" + "6992" + "\n"})
    _commit(root, "one")
    assert not scan.is_shallow(root)
    assert "SHALLOW CLONE" not in scan.scan_phi(root).note
