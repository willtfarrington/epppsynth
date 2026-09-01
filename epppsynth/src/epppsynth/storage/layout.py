# SPDX-FileCopyrightText: 2026 W. Taylor Farrington
# SPDX-License-Identifier: Apache-2.0
"""The two root trees, the lockfile, ``METADATA.json``, and the only write path.

The shape, fixed here so nothing downstream invents its own::

    <model root>/
      models.lock.json                    authoritative: every weight the project may load
      models/<publisher>/<repo>/<revision>/<file>.gguf
      models/<publisher>/<repo>/<revision>/METADATA.json
      embeddings/<same shape>             D-44: an embedding model is a model
      benchmarks/run-<UTC>-<shorthash>.json
      inventory/<UTC>.json
    <index root>/                         SEPARATE ROOT - D-16 index, different rights class

``<revision>`` is a 40-hex commit SHA, never a branch name, so the path itself
records what was verified (D-31).

**Every write in this package goes through :func:`guarded_write`**, which calls
the floor guard before, the ceiling guard before, and the floor guard again
after. That is not politeness: D-49 requires the check on both sides of the
write, and having exactly one write path is what makes "every write" checkable
rather than asserted.

This module creates directories and writes JSON. It never deletes, moves or
renames anything - see the package docstring for the test that proves it.
"""

from __future__ import annotations

import datetime as dt
import json
import pathlib
import re
from dataclasses import asdict, dataclass, field

from .limits import (
    DEFAULT_ROOTS,
    Roots,
    assert_within_ceiling,
    postwrite_space,
    preflight_space,
)

#: The four subtrees of the model root. The index root has no imposed shape:
#: EP-22 owns it, and this brief only guarantees it exists and is separate.
MODEL_SUBDIRS: tuple[str, ...] = ("models", "embeddings", "benchmarks", "inventory")

LOCKFILE_NAME = "models.lock.json"
METADATA_NAME = "METADATA.json"

#: A 40-hex commit SHA. A branch name moves; a path built from one lies.
REVISION_PATTERN = re.compile(r"^[0-9a-f]{40}$")

#: The `METADATA.json` fields, in order. `licence_id` and `licence_url` are
#: item 6 of the pre-publication checklist (licence conformance) reaching into
#: the model root: a weight whose licence nobody wrote down is a weight nobody
#: can clear for publication.
METADATA_FIELDS: tuple[str, ...] = (
    "repo",
    "revision",
    "filename",
    "sha256",
    "bytes",
    "quantization",
    "licence_id",
    "licence_url",
    "acquired_at",
    "acceptable_use",
    "verified_at",
)


class LayoutError(Exception):
    """The tree, the lockfile or a metadata record is not the shape it must be."""


def utc_stamp(moment: dt.datetime | None = None) -> str:
    """A filesystem-safe UTC timestamp, used for inventory and benchmark names."""
    moment = moment or dt.datetime.now(dt.UTC)
    return moment.astimezone(dt.UTC).strftime("%Y%m%dT%H%M%SZ")


@dataclass(frozen=True)
class Metadata:
    """One weight's record, written beside it and mirrored in the lockfile."""

    repo: str
    revision: str
    filename: str
    sha256: str
    bytes: int
    quantization: str
    licence_id: str
    licence_url: str
    acquired_at: str
    acceptable_use: str
    verified_at: str = ""

    def __post_init__(self) -> None:
        if not REVISION_PATTERN.match(self.revision):
            raise LayoutError(
                f"revision {self.revision!r} is not a 40-hex commit SHA. A branch name "
                "moves under the project's feet; D-31 pins a revision, not a ref."
            )

    def as_dict(self) -> dict[str, object]:
        return {key: asdict(self)[key] for key in METADATA_FIELDS}

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> Metadata:
        missing = [key for key in METADATA_FIELDS if key not in payload]
        if missing:
            raise LayoutError(f"metadata is missing required field(s): {', '.join(missing)}")
        return cls(**{key: payload[key] for key in METADATA_FIELDS})  # type: ignore[arg-type]


@dataclass
class LayoutReport:
    """What :func:`validate_layout` found, as findings rather than an exception."""

    roots: Roots
    problems: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.problems


# -- the one write path ------------------------------------------------------


def guarded_write(path: pathlib.Path, text: str, *, roots: Roots = DEFAULT_ROOTS) -> int:
    """Write ``text`` to ``path`` with the floor checked on both sides (D-49, D-78).

    Order, and it matters: floor before, ceiling before, write, floor after. The
    post-write check cannot un-write the bytes; it latches the halt that stops
    the next write.

    The mode is ``xb``: exclusive create. Overwriting is not a thing this
    package does, because overwriting is a deletion with a friendlier name.
    """
    payload = text.encode("utf-8")
    preflight_space(None, len(payload))
    assert_within_ceiling(len(payload), roots)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "xb") as handle:
        handle.write(payload)
    postwrite_space()
    return len(payload)


def write_json(path: pathlib.Path, payload: object, *, roots: Roots = DEFAULT_ROOTS) -> int:
    """Serialise ``payload`` and hand it to :func:`guarded_write`."""
    return guarded_write(path, json.dumps(payload, indent=2, sort_keys=False) + "\n", roots=roots)


# -- creating and validating the trees ---------------------------------------


def ensure_layout(roots: Roots = DEFAULT_ROOTS) -> Roots:
    """Create both roots and the model root's four subtrees, idempotently.

    Directory creation is guarded by the floor but not by the ceiling: an empty
    directory is a handful of bytes of metadata, and a ceiling check that
    refused to create ``inventory/`` would leave the operator unable to run the
    read-only inventory that tells them why they are out of room.
    """
    preflight_space(None, 0)
    roots.models.mkdir(parents=True, exist_ok=True)
    for name in MODEL_SUBDIRS:
        (roots.models / name).mkdir(parents=True, exist_ok=True)
    roots.index.mkdir(parents=True, exist_ok=True)
    postwrite_space()
    return roots


def validate_layout(roots: Roots = DEFAULT_ROOTS) -> LayoutReport:
    """Report what is missing or misshapen, without creating anything."""
    report = LayoutReport(roots)
    if not roots.models.is_dir():
        report.problems.append("the model root is absent")
    else:
        for name in MODEL_SUBDIRS:
            if not (roots.models / name).is_dir():
                report.problems.append(f"the model root has no {name}/ subtree")
    if not roots.index.is_dir():
        report.problems.append("the index root is absent")
    if roots.models == roots.index:
        report.problems.append(
            "the two roots are the same directory; D-51 keeps them separate because "
            "they are different rights classes"
        )
    report.problems.extend(check_lockfile(roots))
    return report


def model_dir(
    publisher: str,
    repo: str,
    revision: str,
    *,
    embedding: bool = False,
    roots: Roots = DEFAULT_ROOTS,
) -> pathlib.Path:
    """The directory one weight lives in. Embedding models use the same shape (D-44)."""
    if not REVISION_PATTERN.match(revision):
        raise LayoutError(f"revision {revision!r} is not a 40-hex commit SHA (D-31)")
    subtree = "embeddings" if embedding else "models"
    return roots.models / subtree / publisher / repo / revision


def lockfile_path(roots: Roots = DEFAULT_ROOTS) -> pathlib.Path:
    return roots.models / LOCKFILE_NAME


def read_lockfile(roots: Roots = DEFAULT_ROOTS) -> dict[str, object] | None:
    """The lockfile as a dict, or ``None`` when it does not exist yet."""
    path = lockfile_path(roots)
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise LayoutError(f"{LOCKFILE_NAME} is present but unreadable: {error}") from error


def check_lockfile(roots: Roots = DEFAULT_ROOTS) -> list[str]:
    """Lockfile integrity: shape, revisions, and a metadata file per entry.

    An absent lockfile is **not** a problem. No weight has been downloaded yet
    and D-30 gates that on an individually confirmed decision, so an empty model
    root is the expected state of a correctly behaving project.
    """
    try:
        data = read_lockfile(roots)
    except LayoutError as error:
        return [str(error)]
    if data is None:
        return []
    problems: list[str] = []
    entries = data.get("weights")
    if not isinstance(entries, list):
        return [f"{LOCKFILE_NAME} has no `weights` list"]
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            problems.append(f"{LOCKFILE_NAME} weights[{index}] is not an object")
            continue
        try:
            record = Metadata.from_dict(entry)
        except LayoutError as error:
            problems.append(f"{LOCKFILE_NAME} weights[{index}]: {error}")
            continue
        publisher, _, repo = record.repo.partition("/")
        if not publisher or not repo:
            problems.append(
                f"{LOCKFILE_NAME} weights[{index}]: repo {record.repo!r} is not <publisher>/<repo>"
            )
            continue
        directory = model_dir(publisher, repo, record.revision, roots=roots)
        alternative = model_dir(publisher, repo, record.revision, embedding=True, roots=roots)
        if (
            not (directory / METADATA_NAME).is_file()
            and not (alternative / METADATA_NAME).is_file()
        ):
            problems.append(
                f"{LOCKFILE_NAME} weights[{index}]: no {METADATA_NAME} beside {record.filename}"
            )
    return problems
