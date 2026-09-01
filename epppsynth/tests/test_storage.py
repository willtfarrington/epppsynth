# SPDX-FileCopyrightText: 2026 W. Taylor Farrington
# SPDX-License-Identifier: Apache-2.0
"""EP-7 acceptance, as tests: the floor, the ceiling, the verifier, the inventory.

Everything here runs on a fake filesystem - a `tmp_path` tree plus two injected
seams, `limits._disk_free` and `limits.directory_size`. Nothing downloads a
weight, nothing needs the real roots, and nothing needs 25 GB of disk to prove a
25 GB ceiling. That is why none of these tests carry `requires_model` or
`requires_index`: CI's `-m "not requires_model"` filter still runs all of them
(D-42).

The load-bearing test in this file is the last one. `test_the_storage_package
_contains_no_deletion_call` parses every module in the package and fails on a
call to `os.remove`, `os.unlink`, `Path.unlink`, `Path.rmdir`, `shutil.rmtree`,
`shutil.move` or a Recycle-Bin helper. EP-7 builds **no purge tool** (D-71), and
that assertion is the acceptance evidence for it - a stronger guarantee than a
code review, because it survives the next session.
"""

from __future__ import annotations

import ast
import hashlib
import json
import os
import pathlib
import re
import subprocess
import warnings

import pytest

from epppsynth.storage import cli as storage_cli
from epppsynth.storage import inventory, layout, limits, verify

PACKAGE = pathlib.Path(limits.__file__).resolve().parent
SOURCE_ROOT = PACKAGE.parent

GIB = 1024**3
GB = 1000**3


@pytest.fixture(autouse=True)
def _no_latched_halt():
    """The write halt is process-global by design; no test may leak one to the next."""
    limits.clear_write_halt()
    yield
    limits.clear_write_halt()


@pytest.fixture
def roomy_disk(monkeypatch):
    """A volume with a terabyte free, so a floor test is the only thing testing the floor."""
    monkeypatch.setattr(limits, "_disk_free", lambda volume: 1000 * GIB)


@pytest.fixture
def roots(tmp_path) -> limits.Roots:
    """The two roots, pointed at a temporary tree. Never the real ones."""
    return limits.Roots(models=tmp_path / "models-root", index=tmp_path / "index-root")


def _free(monkeypatch, free_bytes: int) -> None:
    monkeypatch.setattr(limits, "_disk_free", lambda volume: free_bytes)


def _footprint(monkeypatch, total_bytes: int) -> None:
    """Simulate a project footprint without writing gigabytes to a test runner."""
    monkeypatch.setattr(limits, "directory_size", lambda root: total_bytes // 2)


# ── the two limits are two different things, in two different units ──────────


def test_the_floor_is_binary_and_the_ceiling_is_decimal_exactly_as_stated():
    """D-49 says GiB and D-78 says GB. ADR-009 records that the mismatch is deliberate."""
    assert limits.RESERVE_FLOOR_BYTES == 250 * 1024**3
    assert limits.PROJECT_CEILING_BYTES == 25 * 1000**3
    assert limits.PROJECT_WARN_BYTES == 20 * 1000**3
    assert limits.RESERVE_FLOOR_BYTES != 250 * 1000**3
    assert limits.PROJECT_CEILING_BYTES != 25 * 1024**3


def test_the_third_party_cache_is_not_counted_against_either_limit(roots):
    """D-71. The footprint sums the project's two roots and nothing else."""
    footprint_roots = list(roots)
    assert footprint_roots == [roots.models, roots.index]
    assert len(footprint_roots) == 2


# ── acceptance 2 — the floor, before and after ───────────────────────────────


def test_preflight_refuses_a_write_that_would_breach_the_floor(monkeypatch):
    """EP-7 acceptance 2. The floor is the machine's; it is not raised to fit a download."""
    _free(monkeypatch, limits.RESERVE_FLOOR_BYTES + 4 * GIB)
    with pytest.raises(limits.ReserveFloorError):
        limits.preflight_space(None, 5 * GIB)


def test_preflight_allows_a_write_that_leaves_the_floor_intact(monkeypatch):
    _free(monkeypatch, limits.RESERVE_FLOOR_BYTES + 8 * GIB)
    assert limits.preflight_space(None, 5 * GIB) == limits.RESERVE_FLOOR_BYTES + 8 * GIB


def test_postwrite_raises_when_the_write_has_already_breached_the_floor(monkeypatch):
    """EP-7 acceptance 2. The bytes are on disk; the point is to stop the next one."""
    _free(monkeypatch, limits.RESERVE_FLOOR_BYTES - 1)
    with pytest.raises(limits.ReserveFloorError):
        limits.postwrite_space()


def test_a_postwrite_breach_halts_the_next_write_even_once_space_returns(monkeypatch):
    """The halt latches. A guard that cleared itself on the next call would guard nothing."""
    _free(monkeypatch, limits.RESERVE_FLOOR_BYTES - 1)
    with pytest.raises(limits.ReserveFloorError):
        limits.postwrite_space()
    assert limits.writes_halted() is not None
    _free(monkeypatch, 1000 * GIB)
    with pytest.raises(limits.WritesHaltedError):
        limits.preflight_space(None, 1)
    limits.clear_write_halt()
    assert limits.preflight_space(None, 1) == 1000 * GIB


# ── acceptance 3 — the ceiling, warn then stop ───────────────────────────────


def test_the_footprint_warns_at_the_twenty_gigabyte_level(monkeypatch, roots):
    """EP-7 acceptance 3. It warns on every call, not once."""
    _footprint(monkeypatch, 20 * GB)
    with pytest.warns(limits.ProjectCeilingWarning):
        assert limits.project_footprint(roots) == 20 * GB
    with pytest.warns(limits.ProjectCeilingWarning):
        limits.project_footprint(roots)


def test_the_footprint_is_quiet_below_the_warn_level(monkeypatch, roots):
    """The expected real usage is 8-12 GB (D-78); that must not be a noisy state."""
    _footprint(monkeypatch, 12 * GB)
    with warnings.catch_warnings(record=True) as raised:
        warnings.simplefilter("always")
        assert limits.project_footprint(roots) == 12 * GB
    assert not [r for r in raised if issubclass(r.category, limits.ProjectCeilingWarning)]


def test_the_ceiling_raises_at_twenty_five_gigabytes(monkeypatch, roots):
    """EP-7 acceptance 3. A hard stop, not a warning."""
    _footprint(monkeypatch, 25 * GB)
    with pytest.warns(limits.ProjectCeilingWarning), pytest.raises(limits.ProjectCeilingError):
        limits.assert_within_ceiling(0, roots)


def test_no_write_proceeds_past_the_ceiling_raise(monkeypatch, roots, roomy_disk):
    """EP-7 acceptance 3. The raise is not advisory: the file is not there afterwards."""
    monkeypatch.setattr(limits, "directory_size", lambda root: 13 * GB)
    destination = roots.models / "inventory" / "would-not-fit.json"
    with pytest.warns(limits.ProjectCeilingWarning), pytest.raises(limits.ProjectCeilingError):
        layout.write_json(destination, {"nothing": "written"}, roots=roots)
    assert not destination.exists()


def test_the_ceiling_message_says_raising_it_needs_a_written_owner_decision(monkeypatch, roots):
    """D-78. A constant a session may edit is not a limit."""
    _footprint(monkeypatch, 25 * GB)
    with (
        pytest.warns(limits.ProjectCeilingWarning),
        pytest.raises(limits.ProjectCeilingError) as excinfo,
    ):
        limits.assert_within_ceiling(0, roots)
    assert "written owner decision" in str(excinfo.value)


# ── the layout ───────────────────────────────────────────────────────────────


def test_ensure_layout_creates_both_roots_and_the_four_subtrees(roots, roomy_disk):
    """EP-7 acceptance 10, on a fake filesystem; acceptance 10 proper is the real run."""
    layout.ensure_layout(roots)
    assert roots.models.is_dir() and roots.index.is_dir()
    for name in layout.MODEL_SUBDIRS:
        assert (roots.models / name).is_dir(), name
    assert layout.validate_layout(roots).ok


def test_ensure_layout_is_idempotent(roots, roomy_disk):
    layout.ensure_layout(roots)
    layout.ensure_layout(roots)
    assert layout.validate_layout(roots).ok


def test_validate_layout_reports_an_absent_root_rather_than_creating_it(roots):
    report = layout.validate_layout(roots)
    assert not report.ok
    assert "the model root is absent" in report.problems
    assert not roots.models.exists()


def test_one_root_for_both_is_a_layout_problem(tmp_path, roomy_disk):
    """D-51 keeps them apart because they are different rights classes."""
    shared = limits.Roots(models=tmp_path / "one", index=tmp_path / "one")
    layout.ensure_layout(shared)
    assert any(
        "different rights classes" in problem for problem in layout.validate_layout(shared).problems
    )


def test_an_absent_lockfile_is_not_a_problem(roots, roomy_disk):
    """No weight is downloaded yet, and D-30 gates that on a confirmed decision."""
    layout.ensure_layout(roots)
    assert layout.read_lockfile(roots) is None
    assert layout.check_lockfile(roots) == []


def test_a_lockfile_entry_without_its_metadata_file_is_a_problem(roots, roomy_disk):
    layout.ensure_layout(roots)
    record = _metadata(sha256="0" * 64, size=4)
    layout.write_json(layout.lockfile_path(roots), {"weights": [record.as_dict()]}, roots=roots)
    problems = layout.check_lockfile(roots)
    assert problems and layout.METADATA_NAME in problems[0]


def test_the_model_path_carries_the_revision_and_refuses_a_branch(roots):
    """D-31: the path itself records what was verified."""
    revision = "a" * 40
    path = layout.model_dir("publisher", "repo", revision, roots=roots)
    assert path == roots.models / "models" / "publisher" / "repo" / revision
    embedding = layout.model_dir("publisher", "repo", revision, embedding=True, roots=roots)
    assert embedding.parts[-4] == "embeddings"  # D-44: identical shape
    with pytest.raises(layout.LayoutError):
        layout.model_dir("publisher", "repo", "main", roots=roots)


def test_a_write_never_overwrites(roots, roomy_disk):
    """Overwriting is a deletion with a friendlier name."""
    destination = roots.models / "inventory" / "once.json"
    layout.write_json(destination, {"first": True}, roots=roots)
    with pytest.raises(FileExistsError):
        layout.write_json(destination, {"second": True}, roots=roots)


def test_metadata_carries_the_licence_id_and_url(roots):
    """Pre-publication checklist item 6, reaching into the model root."""
    assert "licence_id" in layout.METADATA_FIELDS
    assert "licence_url" in layout.METADATA_FIELDS
    record = _metadata(sha256="0" * 64, size=1)
    assert set(record.as_dict()) == set(layout.METADATA_FIELDS)


def _metadata(*, sha256: str, size: int, revision: str = "b" * 40) -> layout.Metadata:
    return layout.Metadata(
        repo="publisher/repo",
        revision=revision,
        filename="weight.gguf",
        sha256=sha256,
        bytes=size,
        quantization="Q4_K_M",
        licence_id="Apache-2.0",
        licence_url="https://www.apache.org/licenses/LICENSE-2.0",
        acquired_at="2026-09-01T00:00:00+00:00",
        acceptable_use="no acceptable-use restriction recorded",
        verified_at="",
    )


# ── acceptance 4 — the verifier's four refusals ──────────────────────────────


def _gguf(path: pathlib.Path, body: bytes = b"\x00" * 32) -> layout.Metadata:
    """A minimally well-formed GGUF fixture and the metadata that pins it."""
    payload = b"GGUF" + body
    path.write_bytes(payload)
    return _metadata(sha256=hashlib.sha256(payload).hexdigest(), size=len(payload))


def test_the_verifier_accepts_a_matching_gguf(tmp_path):
    path = tmp_path / "weight.gguf"
    record = _gguf(path)
    result = verify.verify_weight(path, record)
    assert result.detected_format == "gguf"
    assert result.hash_verified
    assert result.record()["verification"] == "sha256"


def test_the_verifier_rejects_a_hash_mismatch(tmp_path):
    """EP-7 acceptance 4a. An unidentified blob is not a known model."""
    path = tmp_path / "weight.gguf"
    record = _gguf(path)
    wrong = layout.Metadata.from_dict({**record.as_dict(), "sha256": "f" * 64})
    with pytest.raises(verify.HashMismatchError):
        verify.verify_weight(path, wrong)


def test_the_verifier_rejects_a_pt_file(tmp_path):
    """EP-7 acceptance 4b. D-31 accepts GGUF, and safetensors only where D-44 forces it."""
    path = tmp_path / "weight.pt"
    path.write_bytes(b"PK\x03\x04rest of a torch archive")
    record = layout.Metadata.from_dict(
        {**_metadata(sha256="0" * 64, size=1).as_dict(), "filename": "weight.pt"}
    )
    with pytest.raises(verify.DisallowedFormatError):
        verify.verify_weight(path, record)


def test_the_verifier_rejects_pickle_magic_behind_a_gguf_extension(tmp_path):
    """EP-7 acceptance 4c. The extension is a claim; the magic number is the evidence."""
    path = tmp_path / "disguised.gguf"
    path.write_bytes(b"\x80\x04\x95 a pickle wearing another name")
    record = _metadata(sha256="0" * 64, size=path.stat().st_size)
    with pytest.raises(verify.PickleFormatError):
        verify.verify_weight(path, record)
    assert verify.detect_format(path) == "pickle"


def test_the_verifier_rejects_a_branch_name_as_a_revision():
    """EP-7 acceptance 4d. A weight pinned to a moving ref is not pinned."""
    with pytest.raises(verify.BadRevisionError):
        verify.check_revision("main")
    with pytest.raises(verify.BadRevisionError):
        verify.check_revision("v1.0")
    verify.check_revision("c" * 40)


def test_a_zip_archive_named_gguf_is_refused_as_pickle_bearing(tmp_path):
    path = tmp_path / "archive.gguf"
    path.write_bytes(b"PK\x03\x04still a zip")
    with pytest.raises(verify.PickleFormatError):
        verify.check_format(path)


# ── acceptance 5 — trust_remote_code ─────────────────────────────────────────


def test_trust_remote_code_is_an_unconditional_false_constant():
    """EP-7 acceptance 5. No parameter, no environment variable, no override."""
    assert verify.TRUST_REMOTE_CODE is False
    assignment = re.compile(r"trust_remote_code\s*[:=]\s*True", re.IGNORECASE)
    definitions = 0
    for path in SOURCE_ROOT.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert not assignment.search(text), path
        definitions += len(re.findall(r"^TRUST_REMOTE_CODE\s*=", text, re.MULTILINE))
    assert definitions == 1


def test_the_trust_cached_escape_hatch_records_itself(tmp_path):
    """A fast run can never be mistaken for a verified one (EP-32 reads this record)."""
    path = tmp_path / "weight.gguf"
    record = _gguf(path)
    trusted = verify.verify_weight(path, record, trust_cached=True)
    assert trusted.trusted_cached is True
    assert trusted.hash_verified is False
    assert trusted.record()["verification"] == "trust-cached"
    assert trusted.record()["trust_remote_code"] is False


# ── acceptance 6 — the inventory ─────────────────────────────────────────────


def test_an_absent_root_is_recorded_as_absent_and_not_as_an_error(tmp_path):
    report = inventory.inventory_root("nowhere", tmp_path / "missing", owned=False)
    assert report.present is False
    assert report.file_count == 0
    assert report.total_bytes == 0


def test_the_inventory_records_size_mtime_extension_class_and_the_reparse_flag(tmp_path):
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "weight.gguf").write_bytes(b"GGUF" + b"\x00" * 12)
    (tmp_path / "sub" / "notes.json").write_text("{}", encoding="utf-8")
    report = inventory.inventory_root("fake", tmp_path, owned=False)
    by_name = {pathlib.Path(entry.path).name: entry for entry in report.entries}
    assert by_name["weight.gguf"].extension_class == "weights-gguf"
    assert by_name["weight.gguf"].bytes == 16
    assert by_name["notes.json"].extension_class == "metadata"
    assert all(entry.mtime.endswith("+00:00") for entry in report.entries)
    assert all(entry.reparse_point is False for entry in report.entries)
    assert all(entry.sha256 is None for entry in report.entries)


def test_a_pickle_format_extension_is_classified_as_such_not_as_a_weight(tmp_path):
    """An inventory that filed `.pt` under "weights" would describe it as usable."""
    assert inventory.classify(pathlib.Path("x.pt")) == "pickle-format"
    assert inventory.classify(pathlib.Path("x.bin")) == "pickle-format"
    assert inventory.classify(pathlib.Path("x.gguf")) == "weights-gguf"


def test_hashing_is_opt_in(tmp_path):
    (tmp_path / "weight.gguf").write_bytes(b"GGUF")
    plain = inventory.inventory_root("fake", tmp_path, owned=False)
    hashed = inventory.inventory_root("fake", tmp_path, owned=False, hash_files=True)
    assert plain.entries[0].sha256 is None
    assert hashed.entries[0].sha256 == hashlib.sha256(b"GGUF").hexdigest()


def _make_junction(link: pathlib.Path, target: pathlib.Path) -> None:
    """A real reparse point, by whatever means this platform allows."""
    if os.name == "nt":
        result = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(link), str(target)],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return
        pytest.skip(f"this machine will not create a junction: {result.stderr.strip()}")
    try:
        os.symlink(target, link, target_is_directory=True)
    except OSError as error:  # pragma: no cover - platform dependent
        pytest.skip(f"this machine will not create a symlink: {error}")


def test_the_walk_records_a_reparse_point_and_does_not_follow_it(tmp_path):
    """EP-7 acceptance 6. Following one turns a walk into an escape."""
    scanned = tmp_path / "scanned"
    outside = tmp_path / "outside"
    (scanned / "inner").mkdir(parents=True)
    outside.mkdir()
    (scanned / "inner" / "kept.gguf").write_bytes(b"GGUF")
    (outside / "must-not-be-reached.gguf").write_bytes(b"GGUF" + b"\x01" * 8)
    _make_junction(scanned / "elsewhere", outside)

    report = inventory.inventory_root("fake", scanned, owned=False)
    names = {pathlib.Path(entry.path).name for entry in report.entries}
    assert "kept.gguf" in names
    assert "must-not-be-reached.gguf" not in names
    assert len(report.skipped_reparse_points) == 1
    assert report.skipped_reparse_points[0].endswith("elsewhere")
    assert "skipped_reparse_points" in report.as_dict()


def test_is_reparse_point_reads_the_windows_attribute(tmp_path):
    """A unit over the attribute itself, so the property holds where junctions do not."""

    class _Stat:
        st_file_attributes = limits.FILE_ATTRIBUTE_REPARSE_POINT
        st_mode = 0o100644

    assert limits.is_reparse_point(_Stat())

    class _Plain:
        st_file_attributes = 0
        st_mode = 0o100644

    assert not limits.is_reparse_point(_Plain())


def test_collect_enumerates_four_roots_with_the_project_root_flagged_as_owned(roots, monkeypatch):
    """EP-7 acceptance 6: three third-party caches plus this project's model root."""
    monkeypatch.setattr(
        inventory,
        "third_party_roots",
        lambda: {
            "lmstudio": roots.index / "a",
            "ollama": roots.index / "b",
            "huggingface": roots.index / "c",
        },
    )
    report = inventory.collect(roots)
    assert [root.name for root in report.roots] == [
        "lmstudio",
        "ollama",
        "huggingface",
        "project-models",
    ]
    assert [root.owned for root in report.roots] == [False, False, False, True]
    assert report.as_dict()["third_party_bytes_excluded_from_limits"] == 0


def test_the_third_party_roots_come_from_the_environment_not_from_the_source(monkeypatch):
    """No absolute user path is written into this package (D-3)."""
    monkeypatch.setenv("USERPROFILE", str(pathlib.Path("/fake/profile")))
    monkeypatch.delenv("LMSTUDIO_HOME", raising=False)
    monkeypatch.delenv("OLLAMA_MODELS", raising=False)
    monkeypatch.delenv("HF_HOME", raising=False)
    monkeypatch.delenv("HUGGINGFACE_HUB_CACHE", raising=False)
    resolved = inventory.third_party_roots()
    assert all(str(pathlib.Path("/fake/profile")) in str(path) for path in resolved.values())
    monkeypatch.setenv("OLLAMA_MODELS", str(pathlib.Path("/elsewhere/ollama")))
    assert "elsewhere" in str(inventory.third_party_roots()["ollama"])


def test_the_inventory_writes_exactly_one_json_file_under_the_model_root(
    roots, roomy_disk, monkeypatch
):
    """EP-7 acceptance 6, and checklist item 4: the output never enters the repository."""
    monkeypatch.setattr(
        inventory, "third_party_roots", lambda: {"lmstudio": roots.index / "absent"}
    )
    assert storage_cli.inventory(roots) == 0
    written = list((roots.models / "inventory").glob("*.json"))
    assert len(written) == 1
    payload = json.loads(written[0].read_text(encoding="utf-8"))
    assert payload["schema_version"] == inventory.SCHEMA_VERSION
    assert payload["roots"][0]["present"] is False


def test_storage_check_reports_both_limits_and_exits_zero_on_an_empty_project(
    roots, roomy_disk, capsys
):
    """EP-7 acceptance 1."""
    layout.ensure_layout(roots)
    assert storage_cli.check(roots) == 0
    out = capsys.readouterr().out
    assert "reserve floor" in out and "hard ceiling" in out
    assert "0.00 GB" in out
    assert "D-71" in out


def test_storage_check_fails_when_the_floor_is_already_breached(roots, monkeypatch, capsys):
    _free(monkeypatch, limits.RESERVE_FLOOR_BYTES - GIB)
    assert storage_cli.check(roots) == 1
    assert "BELOW FLOOR" in capsys.readouterr().out


# ── acceptance 8 — no deletion code path exists ──────────────────────────────

#: Every name that removes, moves or recycles something. The test is deliberately
#: name-based rather than type-resolving: it cannot tell `os.remove` from some
#: other object's `.remove`, and that over-strictness is the point. A package
#: that must never delete anything can afford to never write the word.
DELETION_NAMES = frozenset(
    {
        "remove",
        "unlink",
        "rmdir",
        "removedirs",
        "rmtree",
        "move",
        "rename",
        "send2trash",
        "Send2Trash",
        "recycle",
    }
)

#: What `inventory.py` additionally may not do. The inventory is read-only in a
#: stronger sense than the rest of the package: it walks roots this project does
#: not own, so it may not create a file either.
WRITE_NAMES = frozenset({"write_text", "write_bytes", "mkdir", "makedirs", "touch", "write"})


def _module_sources() -> list[tuple[pathlib.Path, ast.Module]]:
    return [
        (path, ast.parse(path.read_text(encoding="utf-8"), filename=str(path)))
        for path in sorted(PACKAGE.glob("*.py"))
    ]


def _called_names(tree: ast.Module) -> set[str]:
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Attribute):
                names.add(func.attr)
            elif isinstance(func, ast.Name):
                names.add(func.id)
    return names


def test_the_storage_package_contains_no_deletion_call():
    """EP-7 acceptance 8. This assertion **is** the evidence that no purge tool was built.

    ADR-007 writes the seven rules a purge tool would have to satisfy. It has
    `Status: accepted - no implementation exists`, and this test is what makes
    that status a fact rather than a claim (D-71).
    """
    modules = _module_sources()
    assert modules, "the storage package has no modules to inspect"
    for path, tree in modules:
        offending = _called_names(tree) & DELETION_NAMES
        assert not offending, f"{path.name} calls {sorted(offending)}"


def test_the_inventory_module_imports_nothing_that_could_delete_or_write():
    """EP-7 safety preconditions, row 1. Stronger than a code review, and it lasts."""
    path = PACKAGE / "inventory.py"
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
    assert "shutil" not in imported
    assert "send2trash" not in imported
    called = _called_names(tree)
    assert not called & DELETION_NAMES
    assert not called & WRITE_NAMES


def test_the_inventory_opens_files_only_for_reading():
    """`open` appears once, with mode `rb`, in the hash helper."""
    path = PACKAGE / "inventory.py"
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    modes = []
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "open"
        ):
            assert len(node.args) >= 2, "an `open` with no explicit mode"
            assert isinstance(node.args[1], ast.Constant)
            modes.append(node.args[1].value)
    assert modes == ["rb"]


def test_the_package_names_adr_007_so_a_future_purge_starts_from_the_rules():
    text = (PACKAGE / "__init__.py").read_text(encoding="utf-8")
    assert "ADR-007" in text
