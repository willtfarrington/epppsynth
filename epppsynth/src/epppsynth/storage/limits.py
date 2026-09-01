# SPDX-FileCopyrightText: 2026 W. Taylor Farrington
# SPDX-License-Identifier: Apache-2.0
r"""The two storage limits, which are two different things (D-78).

They are never collapsed into one number, and the difference is the whole point:

**Floor - the machine's.** At least 250 GiB free on the system volume at all
times, checked immediately before *and* after every write (D-49). It protects
the operator's non-project use of their own machine. It is **not** a project
allocation, and the project never claims the headroom above it.

**Ceiling - the project's.** The combined footprint of the model root and the
index root is warned at 20 GB and hard-stopped at 25 GB (D-78). Expected real
usage is one generation model of 5 GB or less, one small embedding model, a
local index of roughly 1-2 GB and JSON packets: about 8-12 GB.

The pre-existing third-party model cache on this machine is part of **neither**
figure (D-71). It is inventoried read-only and never touched.

**The units differ on purpose.** The floor is binary (GiB, ``1024**3``) and the
ceiling is decimal (GB, ``1000**3``), exactly as D-49 and D-78 state them.
Neither is normalised to the other; ``ADR-009`` records the mismatch so a later
reader knows it is deliberate transcription rather than a bug, and the P0
re-plan (EP-8) flags it.

This module also owns :func:`walk`, the reparse-point-aware file walk. It sits
here rather than in ``inventory`` because :func:`project_footprint` needs it and
``inventory`` must not be imported by the module that guards writes: the
inventory is read-only, and the dependency arrow points away from it.
"""

from __future__ import annotations

import os
import pathlib
import shutil
import stat as stat_module
import warnings
from collections.abc import Iterator
from dataclasses import dataclass

# -- the two roots -----------------------------------------------------------
#
# These two literals are the only place in the package source where either root
# is written down. `epppsynth scan`'s `roots` check (EP-6) forbids them in every
# other tracked non-documentation file and allowlists them here **by symbol**:
# `MODEL_ROOT` and `INDEX_ROOT`, on their assignment lines, in this file. Any
# other line of this file that names a root is still a finding. See
# `publicsafety/allowlist.py` section 4 and the ADR-008 amendment of 2026-09-01.

#: Weights, their metadata, the lockfile and benchmark packets (D-30).
MODEL_ROOT = pathlib.Path(r"C:\epppmodels")

#: The D-16 local index. A **separate root** on purpose (D-51): a different
#: rights class, independently purgeable and independently excludable from
#: backup. Merging the two would put copyright-derived content and freely
#: licensed weights under one retention policy.
INDEX_ROOT = pathlib.Path(r"C:\epppindex")


@dataclass(frozen=True)
class Roots:
    """The pair of roots the ceiling is measured over.

    Passed explicitly everywhere so the test suite can point the whole package
    at a temporary directory without monkeypatching a module constant.
    """

    models: pathlib.Path
    index: pathlib.Path

    def __iter__(self) -> Iterator[pathlib.Path]:
        return iter((self.models, self.index))


DEFAULT_ROOTS = Roots(MODEL_ROOT, INDEX_ROOT)

# -- the two limits ----------------------------------------------------------

#: D-49: 250 GiB, **binary**, free on the system volume at all times, checked
#: before and after every write. Raising this constant requires a written owner
#: decision recorded as a dated addendum in `epppsynth/DECISIONS.md`. A session
#: may not lower it to make a download fit.
RESERVE_FLOOR_BYTES = 250 * 1024**3

#: D-78: the project's own ceiling, **decimal**. Hard stop; no write proceeds.
#: Raising it requires a written owner decision recorded as a dated addendum.
PROJECT_CEILING_BYTES = 25 * 1000**3

#: D-78: the warn level, **decimal**. Warns on every call above it; it never
#: blocks anything. Changing it is the same written-decision path as the two
#: constants above.
PROJECT_WARN_BYTES = 20 * 1000**3

#: D-78's expected real usage, recorded so a footprint far outside it is
#: legible as a surprise rather than as normal growth.
EXPECTED_USAGE_BYTES = (8 * 1000**3, 12 * 1000**3)


# -- failures ----------------------------------------------------------------


class StorageError(Exception):
    """Base for every refusal this package makes."""


class ReserveFloorError(StorageError):
    """The 250 GiB machine floor would be, or has been, breached (D-49)."""


class WritesHaltedError(StorageError):
    """A post-write check failed earlier; the next write does not proceed."""


class ProjectCeilingError(StorageError):
    """The 25 GB project ceiling would be, or has been, breached (D-78)."""


class ProjectCeilingWarning(UserWarning):
    """The footprint is at or above the 20 GB warn level (D-78)."""


# -- the write halt ----------------------------------------------------------
#
# A post-write breach cannot un-write the bytes. What it can do is stop the
# *next* write, which is the only thing still in reach, so the failure latches.

_write_halt: str | None = None


def writes_halted() -> str | None:
    """The reason writes are halted, or ``None``."""
    return _write_halt


def halt_writes(reason: str) -> None:
    """Latch the halt. Called by :func:`postwrite_space`; nothing else calls it."""
    global _write_halt
    _write_halt = reason


def clear_write_halt() -> None:
    """Release the latch.

    Nothing calls this automatically. It exists so that an operator who has
    freed space can resume in the same process, and so the tests can run more
    than one guard case; a halt that cleared itself would guard nothing.
    """
    global _write_halt
    _write_halt = None


# -- free space --------------------------------------------------------------


def system_volume() -> pathlib.Path:
    """The volume the floor protects, resolved from the environment at run time.

    Read from the ``SystemDrive`` environment variable rather than written down,
    so no machine's drive layout is asserted in the source (D-3).
    """
    drive = os.environ.get("SystemDrive")
    if drive:
        return pathlib.Path(drive + os.sep)
    return pathlib.Path(pathlib.Path.home().anchor or os.sep)


def _disk_free(volume: pathlib.Path) -> int:
    """Free bytes on ``volume``. The seam the tests replace."""
    return shutil.disk_usage(volume).free


def free_space(volume: pathlib.Path | None = None) -> int:
    """Free bytes on ``volume``, defaulting to the system volume."""
    return _disk_free(volume if volume is not None else system_volume())


def preflight_space(volume: pathlib.Path | None, bytes_needed: int) -> int:
    """Refuse a write that would leave less than the floor free (D-49).

    Raises :class:`WritesHaltedError` if a previous post-write check latched the
    halt, and :class:`ReserveFloorError` if the write would breach the floor.
    Returns the free bytes observed, so a caller can log what it saw.
    """
    if _write_halt is not None:
        raise WritesHaltedError(
            f"writes are halted: {_write_halt}. Free space on the system volume and "
            "clear the halt deliberately; nothing clears it automatically."
        )
    target = volume if volume is not None else system_volume()
    free = _disk_free(target)
    remaining = free - bytes_needed
    if remaining < RESERVE_FLOOR_BYTES:
        raise ReserveFloorError(
            f"refusing to write {bytes_needed} byte(s): {remaining} byte(s) would remain "
            f"free, below the {RESERVE_FLOOR_BYTES}-byte reserve floor (D-49). The floor "
            "is the operator's, not the project's; it is not raised to fit a download."
        )
    return free


def postwrite_space(volume: pathlib.Path | None = None) -> int:
    """Check the floor after a write, and latch a halt if it was breached.

    The bytes are already on disk when this runs, so this is not a rollback. It
    is how the *next* write is stopped: a breach here latches the halt that
    :func:`preflight_space` refuses on.
    """
    target = volume if volume is not None else system_volume()
    free = _disk_free(target)
    if free < RESERVE_FLOOR_BYTES:
        reason = (
            f"post-write free space {free} byte(s) is below the {RESERVE_FLOOR_BYTES}-byte "
            "reserve floor (D-49); the write completed and the next one will not"
        )
        halt_writes(reason)
        raise ReserveFloorError(reason)
    return free


# -- the reparse-point-aware walk --------------------------------------------

#: ``FILE_ATTRIBUTE_REPARSE_POINT``. A junction, a symlink or a cloud-sync
#: placeholder all carry it, and following one turns a walk into an escape.
FILE_ATTRIBUTE_REPARSE_POINT = 0x400


def is_reparse_point(st: os.stat_result) -> bool:
    """Whether a ``stat`` taken with ``follow_symlinks=False`` is a reparse point."""
    attributes = getattr(st, "st_file_attributes", 0)
    if attributes & FILE_ATTRIBUTE_REPARSE_POINT:
        return True
    return stat_module.S_ISLNK(st.st_mode)


@dataclass(frozen=True)
class WalkedFile:
    """One file the walk reached, with the ``stat`` it was reached by."""

    path: pathlib.Path
    st: os.stat_result
    reparse_point: bool


def walk(root: pathlib.Path, *, skipped: list[pathlib.Path] | None = None) -> Iterator[WalkedFile]:
    """Every file under ``root``, never following a reparse point.

    A directory carrying the reparse-point attribute is appended to ``skipped``
    and **not descended into**; a file carrying it is yielded with the flag set
    and is never opened. Unreadable directories are stepped over rather than
    raised on: this walk runs over caches it does not own.
    """
    stack = [pathlib.Path(root)]
    while stack:
        current = stack.pop()
        try:
            entries = list(os.scandir(current))
        except OSError:
            continue
        for entry in entries:
            try:
                st = entry.stat(follow_symlinks=False)
                is_dir = entry.is_dir(follow_symlinks=False)
                is_file = entry.is_file(follow_symlinks=False)
            except OSError:
                continue
            flagged = is_reparse_point(st)
            if is_dir:
                if flagged:
                    if skipped is not None:
                        skipped.append(pathlib.Path(entry.path))
                    continue
                stack.append(pathlib.Path(entry.path))
            elif is_file or flagged:
                yield WalkedFile(pathlib.Path(entry.path), st, flagged)


def directory_size(root: pathlib.Path) -> int:
    """Total bytes of the regular files under ``root``; ``0`` if it is absent."""
    return sum(walked.st.st_size for walked in walk(root) if not walked.reparse_point)


# -- the ceiling -------------------------------------------------------------


def project_footprint(roots: Roots = DEFAULT_ROOTS) -> int:
    """The combined size of both roots, warning above the 20 GB level (D-78).

    Warns on **every** call above the warn level, deliberately: a warning that
    fires once is a warning nobody sees twice.
    """
    total = sum(directory_size(root) for root in roots)
    if total >= PROJECT_WARN_BYTES:
        warnings.warn(
            f"project footprint {total} byte(s) is at or above the "
            f"{PROJECT_WARN_BYTES}-byte warn level; the hard ceiling is "
            f"{PROJECT_CEILING_BYTES} bytes (D-78)",
            ProjectCeilingWarning,
            stacklevel=2,
        )
    return total


def assert_within_ceiling(additional_bytes: int = 0, roots: Roots = DEFAULT_ROOTS) -> int:
    """Refuse a write that would put the project at or above the ceiling (D-78).

    Returns the projected footprint. Every write path in this package calls it
    before writing, so a raise means no write proceeded.
    """
    projected = project_footprint(roots) + additional_bytes
    if projected >= PROJECT_CEILING_BYTES:
        raise ProjectCeilingError(
            f"refusing to write {additional_bytes} byte(s): the project footprint would "
            f"reach {projected} byte(s), at or above the {PROJECT_CEILING_BYTES}-byte "
            "ceiling (D-78). Raising the ceiling requires a written owner decision "
            "recorded as a dated addendum in DECISIONS.md, not a change to this constant."
        )
    return projected
