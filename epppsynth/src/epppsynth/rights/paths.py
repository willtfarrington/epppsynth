# SPDX-FileCopyrightText: 2026 W. Taylor Farrington
# SPDX-License-Identifier: Apache-2.0
"""Canonical paths, resolved from the repository root rather than from the CWD.

The uv project is `epppsynth/` and the git root is its parent (CLAUDE.md), so a
path written relative to one is wrong relative to the other. Every canonical
path in this package is derived from the repository root so that the checks give
the same answer wherever they are run from.
"""

from __future__ import annotations

import pathlib

#: Files whose presence identifies the repository root, in the order tried.
_ROOT_MARKERS = ("REUSE.toml", ".git")


def repo_root(start: pathlib.Path | None = None) -> pathlib.Path:
    """Walk upward to the repository root.

    Falls back to the layout-derived answer — this file is
    `<root>/epppsynth/src/epppsynth/rights/paths.py` — so that the package still
    resolves its own paths in a tree where `.git` has been stripped.
    """
    here = (start or pathlib.Path(__file__)).resolve()
    for candidate in (here, *here.parents):
        if candidate.is_dir() and any((candidate / marker).exists() for marker in _ROOT_MARKERS):
            return candidate
    return pathlib.Path(__file__).resolve().parents[4]


def sources_yaml(root: pathlib.Path | None = None) -> pathlib.Path:
    return (root or repo_root()) / "epppsynth" / "registry" / "sources.yaml"


def rights_md(root: pathlib.Path | None = None) -> pathlib.Path:
    return (root or repo_root()) / "epppsynth" / "docs" / "rights.md"


def reuse_toml(root: pathlib.Path | None = None) -> pathlib.Path:
    return (root or repo_root()) / "REUSE.toml"


def concept_registry_dir(root: pathlib.Path | None = None) -> pathlib.Path:
    """Where EP-9 puts the concept registry. It does not exist yet."""
    return (root or repo_root()) / "epppsynth" / "registry" / "concepts"


def quotation_scan_paths(root: pathlib.Path | None = None) -> tuple[pathlib.Path, ...]:
    """The public prose the D-74 budget is counted over (EP-5 acceptance 8).

    `epppsynth/docs/**` plus `SAFETY.md`. EP-6 widens this when it wires the
    counter into CI; the set is named here so that the widening is a visible
    edit rather than an unstated default.
    """
    base = root or repo_root()
    docs = sorted((base / "epppsynth" / "docs").rglob("*.md"))
    return (*docs, base / "SAFETY.md")
