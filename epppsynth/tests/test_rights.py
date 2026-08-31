# SPDX-FileCopyrightText: 2026 W. Taylor Farrington
# SPDX-License-Identifier: Apache-2.0
"""EP-5 acceptance, as tests: the licensing pack and the per-source rights table.

The point of EP-5 is that "we do not redistribute" stops being a posture and
becomes a constraint the build enforces. A posture that is checked once by hand
is a posture again the next morning, so every acceptance criterion that a
machine can hold is held here rather than in a one-time pass — the licence
boundary, the CFF metadata, the schema's closed enumerations, the two rights
rules, the quotation budget, and the generated table's freshness.

Each rule is exercised in both directions. A check that only ever passes is not
evidence that it discriminates, so every rule is also run against a fixture
built to break it.
"""

from __future__ import annotations

import pathlib
import re
import subprocess
import sys
import tomllib

import pytest
import yaml

from epppsynth.rights import coverage as coverage_module
from epppsynth.rights.check import (
    check_locators,
    check_no_verbatim_from_nonredistributable,
    check_source_refs,
)
from epppsynth.rights.load import load_sources
from epppsynth.rights.model import (
    ACCESS_BASES,
    DEFAULT_QUOTE_BUDGET_WORDS,
    DEFAULT_SOURCE_BUDGET_WORDS,
    LOCATOR_RE,
    PAGE_RANGE_RE,
    REUSE_CLASSES,
    RightsError,
)
from epppsynth.rights.paths import quotation_scan_paths
from epppsynth.rights.quotes import count_quotations
from epppsynth.rights.render import render_rights_md

ROOT = pathlib.Path(__file__).resolve().parents[2]
FIXTURES = pathlib.Path(__file__).resolve().parent / "fixtures"

LICENSE = ROOT / "LICENSE"
LICENSE_CONTENT = ROOT / "LICENSE-CONTENT"
NOTICE = ROOT / "NOTICE"
CITATION = ROOT / "CITATION.cff"
REUSE = ROOT / "REUSE.toml"
LICENSES_DIR = ROOT / "LICENSES"
README = ROOT / "README.md"
SAFETY = ROOT / "SAFETY.md"
SOURCES = ROOT / "epppsynth" / "registry" / "sources.yaml"
RIGHTS_MD = ROOT / "epppsynth" / "docs" / "rights.md"

#: `NOTICE` must carry this exactly. It is the sentence a stranger reads to
#: learn what this repository does and does not contain (D-10(i)).
RIGHTS_POSTURE = (
    "this repository contains no third-party copyrighted source text; "
    "the concept registry is original prose that cites its sources"
)

#: `CITATION.cff`'s abstract must end with this, because a citation that travels
#: without the status is a citation that overstates the artifact.
CFF_CLOSING = "Work in progress; not validated; not for clinical use."

EXPANSION = "existential perspectives for physicians & patients"
STATUS_LINE = "Design and planning artifact — v1 in progress; no release, no demo, no validation."


def _read(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8")


def _flat(text: str) -> str:
    """Strip bold markers and collapse whitespace, so a wrapped sentence compares."""
    return re.sub(r"\s+", " ", text.replace("**", ""))


@pytest.fixture(scope="module")
def registry():
    return load_sources(SOURCES)


# ── acceptance 1: the licensing pack exists, and covers everything ───────────


def test_every_licensing_file_exists():
    for path in (
        LICENSE,
        LICENSE_CONTENT,
        NOTICE,
        CITATION,
        REUSE,
        LICENSES_DIR / "Apache-2.0.txt",
        LICENSES_DIR / "CC-BY-4.0.txt",
    ):
        assert path.is_file(), path


def test_the_root_licence_is_the_apache_text_itself():
    """GitHub's licence detection reads `LICENSE`; REUSE reads `LICENSES/`."""
    assert _read(LICENSE) == _read(LICENSES_DIR / "Apache-2.0.txt")
    assert "Apache License" in _read(LICENSE)
    assert "Version 2.0, January 2004" in _read(LICENSE)


def test_license_content_points_rather_than_duplicating():
    """D-40 keeps `LICENSE-CONTENT` as a pointer; a second copy of a licence drifts."""
    text = _read(LICENSE_CONTENT)
    assert "CC BY 4.0" in text
    assert "LICENSES/CC-BY-4.0.txt" in text
    # A pointer, not the legal code: the real text is thousands of words long.
    assert len(text.split()) < 400


# ── acceptance 11: every tracked file maps to exactly one licence ────────────


def test_licence_coverage_has_no_unmatched_and_no_doubly_matched_file():
    report = coverage_module.licence_coverage(ROOT)
    assert report.unmatched == (), report.render()
    assert report.doubly_matched == {}, report.render()
    assert report.unused_patterns == (), report.render()
    assert report.header_mismatches == (), report.render()
    assert len(report.licence_of) + len(report.exempt) == len(report.tracked)


def test_the_only_exempt_files_are_verbatim_licence_texts():
    """An exemption is named with its reason, never a silent skip."""
    report = coverage_module.licence_coverage(ROOT)
    assert set(report.exempt) == {
        "LICENSE",
        "LICENSES/Apache-2.0.txt",
        "LICENSES/CC-BY-4.0.txt",
    }
    assert all(reason.strip() for reason in coverage_module.EXEMPTIONS.values())


def test_every_python_file_carries_an_spdx_header_agreeing_with_the_table():
    report = coverage_module.licence_coverage(ROOT)
    python_files = [path for path in report.licence_of if path.endswith(".py")]
    assert len(python_files) >= 10
    assert report.header_mismatches == ()
    for path in python_files:
        assert report.licence_of[path] == "Apache-2.0", path


def test_the_reuse_pattern_translation_distinguishes_one_level_from_recursive():
    single = coverage_module.pattern_to_regex("epppsynth/*.md")
    recursive = coverage_module.pattern_to_regex("epppsynth/**")
    assert single.match("epppsynth/DESIGN.md")
    assert not single.match("epppsynth/docs/rights.md")
    assert recursive.match("epppsynth/docs/adr/ADR-001-python-uv-src-layout.md")


# ── acceptance 3 and 10: NOTICE and README state the same boundary ───────────


def _reuse_paths() -> dict[str, set[str]]:
    document = tomllib.loads(_read(REUSE))
    by_licence: dict[str, set[str]] = {}
    for block in document["annotations"]:
        identifier = block["SPDX-License-Identifier"]
        by_licence.setdefault(identifier, set()).update(block["path"])
    return by_licence


def test_notice_states_the_split_with_the_exact_path_boundaries():
    notice = _read(NOTICE)
    for paths in _reuse_paths().values():
        for path in paths:
            assert path in notice, path
    assert "Apache-2.0" in notice and "CC BY 4.0" in notice


def test_notice_carries_the_rights_posture_sentence_verbatim():
    assert RIGHTS_POSTURE in _read(NOTICE)


def test_notice_states_the_vendoring_position_and_names_the_one_third_party_text():
    """Acceptance 3, corrected: the Contributor Covenant *is* vendored third-party text.

    EP-5 asked NOTICE to say that nothing is vendored. That is true of source
    code and false of `CODE_OF_CONDUCT.md`, which reproduces the Contributor
    Covenant verbatim under CC BY 4.0 — a licence whose one condition is
    attribution. NOTICE therefore says both things, and this test holds it to
    both, because the attribution is a licence obligation and not a courtesy.
    """
    flat = _flat(_read(NOTICE))
    assert "No third-party source code is vendored into this repository." in flat
    assert "nothing is vendored today" in flat
    assert "Contributor Covenant, version 2.1" in flat
    assert "CC BY 4.0" in flat
    assert "htmx" in flat and "EP-40" in flat  # what will be vendored, and when


def test_notice_points_at_the_rights_table():
    assert "epppsynth/docs/rights.md" in _read(NOTICE)


def _readme_licence_paths() -> dict[str, set[str]]:
    section = _read(README).split("\n## Licence\n", 1)[1].split("\n## ", 1)[0]
    rows = {}
    for line in section.splitlines():
        if line.startswith("| Apache-2.0 |") or line.startswith("| CC BY 4.0 |"):
            name, paths = line.strip("|").split("|", 1)
            key = {"Apache-2.0": "Apache-2.0", "CC BY 4.0": "CC-BY-4.0"}[name.strip()]
            rows[key] = set(re.findall(r"`([^`]+)`", paths))
    return rows


def test_the_readme_licence_split_matches_the_reuse_boundary_exactly():
    """Acceptance 10. Compared as sets, because prose that merely agrees drifts."""
    assert _readme_licence_paths() == _reuse_paths()


def test_the_readme_marks_the_two_boundary_paths_that_do_not_exist_yet_as_planned():
    """Public text uses present tense only for what exists (GOVERNANCE.md §1)."""
    section = _read(README).split("\n## Licence\n", 1)[1].split("\n## ", 1)[0]
    for path in ("epppsynth/schemas/**", "epppsynth/templates/**"):
        assert path in section, path
        assert not (ROOT / path.replace("/**", "")).exists(), path
    assert "*planned — EP-9, EP-11*" in section
    assert "](roadmap/EP-9" not in section  # planned work is never rendered as a link


def test_the_readme_citation_paragraph_resolves_to_the_citation_file():
    section = _read(README).split("\n## Citation\n", 1)[1].split("\n## ", 1)[0]
    assert "](CITATION.cff)" in section
    assert (ROOT / "CITATION.cff").is_file()
    assert STATUS_LINE in _flat(section)


def test_no_ep5_placeholder_survives_in_the_readme():
    assert "*Placed by EP-5" not in _read(README)


# ── acceptance 2: CITATION.cff ───────────────────────────────────────────────


@pytest.fixture(scope="module")
def citation():
    return yaml.safe_load(_read(CITATION))


def test_citation_is_cff_1_2_0_with_the_required_fields(citation):
    assert citation["cff-version"] == "1.2.0"
    assert citation["type"] == "software"
    assert citation["version"] == "0.0.0"
    assert citation["license"] == "Apache-2.0"
    assert citation["repository-code"].startswith("https://github.com/")
    assert citation["authors"]
    assert citation["message"].strip()
    assert citation["date-released"] == "2026-08-23"


def test_citation_abstract_names_the_content_licence_and_ends_with_the_status(citation):
    """CFF has one licence field, so the other half of the split lives in the abstract."""
    abstract = _flat(citation["abstract"]).strip()
    assert "CC BY 4.0" in abstract
    assert "Apache-2.0" in abstract
    assert abstract.endswith(CFF_CLOSING), abstract[-120:]


def test_citation_abstract_matches_the_readme_expansion_and_status_line(citation):
    """The README requires this character for character; whitespace folding aside."""
    abstract = _flat(citation["abstract"])
    assert EXPANSION in abstract
    assert STATUS_LINE in abstract
    readme = _flat(_read(README))
    assert EXPANSION in readme
    assert STATUS_LINE in readme


def test_citation_references_point_at_the_primary_sources_and_at_the_rights_table(citation):
    """D-14's traditions, so a citer is pointed past this project's paraphrase."""
    references = citation["references"]
    assert len(references) >= 4
    for reference in references:
        assert reference["title"].strip()
        assert reference["authors"]
        assert reference["type"] in {"book", "report", "generic", "article"}
    blob = _flat(yaml.safe_dump(references, allow_unicode=True))
    assert "epppsynth/docs/rights.md" in blob
    assert "UNVERIFIED" in blob  # the unverified source is named as such here too


def test_citation_makes_no_claim_of_review_validation_or_release(citation):
    abstract = _flat(citation["abstract"]).lower()
    assert "author-only" in abstract or "review is author-only" in abstract
    for overclaim in ("validated", "peer-reviewed", "approved by", "cleared by"):
        if overclaim in abstract:
            # The word may appear only inside an explicit negation.
            assert f"not {overclaim}" in abstract or "no clinician" in abstract, overclaim


# ── acceptance 4: the source rights record ───────────────────────────────────


def test_sources_yaml_validates(registry):
    assert len(registry) == 7
    assert len(set(registry.ids)) == len(registry)


def test_every_row_uses_the_closed_enumerations(registry):
    for source in registry:
        assert source.reuse_class in REUSE_CLASSES, source.source_id
        assert source.access_basis in ACCESS_BASES, source.source_id
        assert source.locator_granularity == "chapter", source.source_id
        assert source.verification_note.strip(), source.source_id


def test_every_row_respects_the_d74_budget_as_a_ceiling(registry):
    for source in registry:
        assert 0 < source.quote_budget_words <= DEFAULT_QUOTE_BUDGET_WORDS
        assert 0 < source.source_budget_words <= DEFAULT_SOURCE_BUDGET_WORDS


def test_the_owners_purchased_copy_is_recorded_as_read_only_and_never_redistributable(registry):
    source = registry["yalom-existential-psychotherapy-1980"]
    assert source.access_basis == "owner-purchased-copy"
    assert source.redistributable is False
    assert source.redistribution == "none"
    assert source.in_local_index is True
    assert set(source.permitted_use) == {
        "read-as-input",
        "short-citation-in-docs",
        "redistribution-none",
    }


def test_the_who_guidance_is_reference_only_with_its_share_alike_licence_named(registry):
    """D-62: an NC/SA source ingested into a CC BY 4.0 tree is licence contamination."""
    source = registry["who-lmm-guidance-2024"]
    assert source.reuse_class == "reference-only"
    assert source.licence == "CC-BY-NC-SA-3.0-IGO"
    assert source.in_local_index is False
    assert "read-as-input" not in source.permitted_use


@pytest.mark.parametrize(
    "source_id",
    [
        "samhsa-trauma-informed-approach-2014",
        "ahrq-patient-engagement-materials",
        "fda-cds-final-guidance-2026",
    ],
)
def test_the_unverified_rows_say_so_and_carry_a_dated_note(registry, source_id):
    source = registry[source_id]
    assert source.verified_at is None
    assert source.reuse_class in {"reference-only", "reference-only-pending-rights-check"}
    assert "UNVERIFIED" in source.verification_note
    assert re.search(r"\d{4}-\d{2}-\d{2}", source.verification_note), source_id


def test_the_two_403_rows_record_the_observation_and_its_date(registry):
    for source_id in ("samhsa-trauma-informed-approach-2014", "ahrq-patient-engagement-materials"):
        note = registry[source_id].verification_note
        assert "HTTP 403" in note, source_id
        assert "2026-08-23" in note, source_id


def test_the_fda_row_blocks_public_intended_use_language(registry):
    note = registry["fda-cds-final-guidance-2026"].verification_note
    assert "2026-01-06" in note
    assert "intended-use" in note


# ── acceptance 9: no page-range locator anywhere ─────────────────────────────


def test_no_page_range_locator_in_the_rights_record_or_the_public_docs():
    offenders = []
    targets = [SOURCES, *sorted((ROOT / "epppsynth" / "docs").rglob("*.md"))]
    for path in targets:
        for match in PAGE_RANGE_RE.finditer(_read(path)):
            line = _read(path).count("\n", 0, match.start()) + 1
            offenders.append(f"{path.name}:{line}: {match.group(0)!r}")
    assert offenders == []


def test_the_locator_pattern_accepts_chapter_level_and_rejects_everything_finer():
    for good in ("ch. 1", "ch. 12", "ch. 3–4", "whole-work"):
        assert LOCATOR_RE.match(good), good
    for bad in ("pp. 12–19", "p. 44", "ch. 3, p. 44", "section 2.1.4", "loc. 4180", "3"):
        assert not LOCATOR_RE.match(bad), bad


def test_a_page_range_locator_on_a_concept_is_a_finding(registry, tmp_path):
    planted = tmp_path / "page_range.yaml"
    planted.write_text(
        "concepts:\n"
        "  - concept_id: fixture-page-range\n"
        "    provenance:\n"
        "      source_id: yalom-existential-psychotherapy-1980\n"
        '      locator: "pp. 12-19"\n',
        encoding="utf-8",
    )
    findings = check_locators([planted], registry)
    assert len(findings) == 1
    assert findings[0].rule == "locator-granularity"


# ── acceptance 6 and 7: the two rights rules, in both directions ─────────────


def test_check_source_refs_passes_on_the_clean_fixture(registry):
    assert check_source_refs([FIXTURES / "clean_concepts.yaml"], registry) == []


def test_check_source_refs_fails_on_the_planted_dangling_source_id(registry):
    findings = check_source_refs([FIXTURES / "dangling_source.yaml"], registry)
    assert len(findings) == 1
    assert findings[0].rule == "source-ref"
    assert "a-source-that-was-never-recorded" in findings[0].detail


def test_check_no_verbatim_passes_on_the_clean_fixture(registry):
    assert (
        check_no_verbatim_from_nonredistributable([FIXTURES / "clean_concepts.yaml"], registry)
        == []
    )


def test_check_no_verbatim_fails_on_the_planted_leak(registry):
    """D-10: a verbatim span from a non-redistributable source, in a tracked file."""
    findings = check_no_verbatim_from_nonredistributable(
        [FIXTURES / "verbatim_leak.yaml"], registry
    )
    assert len(findings) == 2
    concepts = {finding.where.split(":")[-1] for finding in findings}
    assert concepts == {"fixture-leaks", "fixture-leaks-from-reference-only"}
    assert all(finding.rule == "verbatim-from-nonredistributable" for finding in findings)


def test_the_renderer_refuses_to_emit_while_the_leak_is_in_the_concept_set(registry):
    """The rule is not advisory: the generator will not produce a table beside a leak."""
    with pytest.raises(RuntimeError, match="refusing to generate"):
        render_rights_md(registry, [FIXTURES / "verbatim_leak.yaml"])


def test_the_dangling_fixture_cli_exits_non_zero():
    """Acceptance 7's runnable form, exactly as the brief writes it."""
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "epppsynth.rights.check",
            "--fixture",
            str(FIXTURES / "dangling_source.yaml"),
        ],
        cwd=ROOT / "epppsynth",
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1, result.stdout + result.stderr
    assert "a-source-that-was-never-recorded" in result.stderr


# ── acceptance 5: the rights table is generated, and stays fresh ─────────────


def test_rights_md_regenerates_byte_identically(registry):
    assert RIGHTS_MD.is_file()
    assert _read(RIGHTS_MD) == render_rights_md(registry, [])


def test_rights_md_says_it_is_generated_and_names_the_regenerating_command():
    text = _read(RIGHTS_MD)
    assert "GENERATED FILE" in text
    assert "uv run python -m epppsynth.rights.render" in text
    assert "epppsynth/registry/sources.yaml" in text


def test_rights_md_puts_the_unverified_rows_under_their_own_heading(registry):
    text = _read(RIGHTS_MD)
    assert "## Rights verified" in text
    assert "## Rights not yet verified" in text
    verified_block, unverified_block = text.split("## Rights not yet verified", 1)
    verified_block = verified_block.split("## Rights verified", 1)[1]
    for source in registry:
        heading = f"### `{source.source_id}`"
        target = verified_block if source.verified else unverified_block
        other = unverified_block if source.verified else verified_block
        assert heading in target, source.source_id
        assert heading not in other, source.source_id


def test_rights_md_answers_all_three_questions_for_every_source(registry):
    """Acceptance 12's machine-checkable half: may, may never, and has anyone checked."""
    blocks = _read(RIGHTS_MD).split("### `")[1:]
    assert len(blocks) == len(registry)
    for block in blocks:
        assert "**May** —" in block
        assert "**May never** —" in block
        assert "**Checked** —" in block
        assert "*Note.*" in block


def test_rights_md_never_softens_an_unverified_row(registry):
    text = _read(RIGHTS_MD)
    unverified = text.split("## Rights not yet verified", 1)[1]
    assert "**No. Nobody has checked this source's reuse terms.**" in unverified
    count = unverified.count("**No. Nobody has checked this source's reuse terms.**")
    assert count == len([source for source in registry if not source.verified])


def test_rights_md_render_is_deterministic(registry):
    assert render_rights_md(registry, []) == render_rights_md(registry, [])


# ── acceptance 8: the D-74 quotation budget ──────────────────────────────────


def test_the_scanned_set_is_the_public_docs_plus_the_safety_charter():
    """Acceptance 8 names the scope; EP-6 widens it, and the widening is a visible edit."""
    scanned = set(quotation_scan_paths(ROOT))
    assert SAFETY in scanned
    assert RIGHTS_MD in scanned
    assert scanned == {*(ROOT / "epppsynth" / "docs").rglob("*.md"), SAFETY}


def test_no_over_budget_quotation_in_the_public_docs_or_the_safety_charter():
    report = count_quotations(quotation_scan_paths(ROOT))
    assert report.findings == [], report.summary()
    assert report.quotations, "the counter found nothing at all, which means it is not looking"


def test_the_counter_fails_on_the_planted_thirty_word_quotation():
    report = count_quotations([FIXTURES / "over_budget_quote.md"])
    over = [finding for finding in report.findings if finding.rule == "quote-budget"]
    assert len(over) == 1
    assert "30 words" in over[0].detail


def test_the_counter_still_passes_short_quotations_in_the_same_file():
    report = count_quotations([FIXTURES / "over_budget_quote.md"])
    short = [quote for quote in report.quotations if quote.words <= DEFAULT_QUOTE_BUDGET_WORDS]
    assert short and all(not quote.exempt for quote in short)


def test_an_exemption_is_honoured_and_must_state_a_reason(tmp_path):
    exempted = [
        quote
        for quote in count_quotations([FIXTURES / "over_budget_quote.md"]).quotations
        if quote.exempt
    ]
    assert len(exempted) == 1
    assert exempted[0].allowed_reason

    reasonless = tmp_path / "reasonless.md"
    reasonless.write_text(
        '<!-- quote-budget-allow:  -->\n"' + " ".join(["word"] * 40) + '"\n',
        encoding="utf-8",
    )
    report = count_quotations([reasonless])
    assert [finding.rule for finding in report.findings] == ["quote-budget-allow"]


def test_code_is_not_counted_as_prose(tmp_path):
    """A regex in a fenced block is not somebody's sentence."""
    path = tmp_path / "with_code.md"
    path.write_text(
        "```\n"
        '"' + " ".join(["fenced"] * 40) + '"\n'
        "```\n\n"
        'An inline span `"' + " ".join(["inline"] * 40) + '"` is code too.\n',
        encoding="utf-8",
    )
    report = count_quotations([path])
    assert report.quotations == []
    assert report.ok


def test_the_per_source_budget_is_enforced_separately_from_the_per_quote_budget(registry, tmp_path):
    """Seven attributed 24-word quotes are each in budget and together are not."""
    quote = " ".join(["word"] * 24)
    path = tmp_path / "many_short_quotes.md"
    path.write_text(
        "\n\n".join(f'"{quote}" [yalom-existential-psychotherapy-1980, ch. 3]' for _ in range(7))
        + "\n",
        encoding="utf-8",
    )
    report = count_quotations([path], registry)
    assert [finding.rule for finding in report.findings] == ["source-budget"]
    assert report.per_source_words["yalom-existential-psychotherapy-1980"] == 168


# ── the schema is closed, and says no in every direction ─────────────────────


def _mutate(tmp_path: pathlib.Path, old: str, new: str) -> pathlib.Path:
    text = _read(SOURCES)
    assert old in text, old
    target = tmp_path / "sources.yaml"
    target.write_text(text.replace(old, new, 1), encoding="utf-8")
    return target


def test_an_unknown_reuse_class_is_rejected(tmp_path):
    path = _mutate(tmp_path, "reuse_class: owner-copy-read-as-input", "reuse_class: probably-fine")
    with pytest.raises(RightsError, match="reuse_class"):
        load_sources(path)


def test_an_unknown_field_is_rejected_because_the_schema_is_closed(tmp_path):
    path = _mutate(
        tmp_path,
        '    rights_holder: "Irvin D. Yalom / Basic Books"',
        '    rights_holder: "Irvin D. Yalom / Basic Books"\n    probably_fine: true',
    )
    with pytest.raises(RightsError, match="unknown field"):
        load_sources(path)


def test_a_loosened_quotation_budget_is_rejected(tmp_path):
    path = _mutate(tmp_path, "    quote_budget_words: 25", "    quote_budget_words: 250")
    with pytest.raises(RightsError, match="D-74 ceiling"):
        load_sources(path)


def test_loosening_the_file_wide_defaults_is_rejected(tmp_path):
    path = _mutate(tmp_path, "  quote_budget_words: 25", "  quote_budget_words: 40")
    with pytest.raises(RightsError, match="D-74"):
        load_sources(path)


def test_a_contradictory_redistribution_pair_is_rejected(tmp_path):
    path = _mutate(
        tmp_path,
        "    redistributable: false",
        "    redistributable: true",
    )
    with pytest.raises(RightsError, match="contradicts"):
        load_sources(path)


def test_a_reference_only_source_may_not_be_in_the_local_index(tmp_path):
    text = _read(SOURCES)
    block = text.split("- source_id: who-lmm-guidance-2024", 1)[1]
    assert "in_local_index: false" in block
    target = tmp_path / "sources.yaml"
    head, tail = text.split("- source_id: who-lmm-guidance-2024", 1)
    target.write_text(
        head
        + "- source_id: who-lmm-guidance-2024"
        + tail.replace("in_local_index: false", "in_local_index: true", 1),
        encoding="utf-8",
    )
    with pytest.raises(RightsError, match="referenced and never ingested"):
        load_sources(target)


def test_a_local_index_entry_requires_an_owned_copy(tmp_path):
    path = _mutate(
        tmp_path, "    access_basis: owner-purchased-copy", "    access_basis: open-access"
    )
    with pytest.raises(RightsError, match="owner-purchased-copy"):
        load_sources(path)


def test_a_row_without_a_verification_note_is_rejected(tmp_path):
    text = _read(SOURCES)
    target = tmp_path / "sources.yaml"
    target.write_text(
        re.sub(
            r"verification_note: >-\n(?:      .*\n)+",
            'verification_note: ""\n',
            text,
            count=1,
        ),
        encoding="utf-8",
    )
    with pytest.raises(RightsError, match="verification_note"):
        load_sources(target)


def test_a_source_family_may_not_claim_a_publisher(tmp_path):
    text = _read(SOURCES)
    head, tail = text.split("- source_id: moral-injury-literature", 1)
    target = tmp_path / "sources.yaml"
    target.write_text(
        head
        + "- source_id: moral-injury-literature"
        + tail.replace("publisher: null", 'publisher: "A publisher"', 1),
        encoding="utf-8",
    )
    with pytest.raises(RightsError, match="source-family"):
        load_sources(target)


def test_a_page_range_in_the_rights_record_is_rejected(tmp_path):
    path = _mutate(tmp_path, 'edition: "first edition"', 'edition: "first edition, pp. 12-19"')
    with pytest.raises(RightsError, match="page-range"):
        load_sources(path)
