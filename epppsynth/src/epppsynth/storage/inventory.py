# SPDX-FileCopyrightText: 2026 W. Taylor Farrington
# SPDX-License-Identifier: Apache-2.0
"""A strictly read-only inventory of four model caches (D-30, D-71).

Four roots are enumerated: the LM Studio model directory, the Ollama model
directory, the Hugging Face hub cache, and this project's own model root. The
first three are **not this project's storage**. They are inventoried because
D-30 requires the inventory to include them, and because reusing an
already-downloaded weight beats re-downloading one when revision and hash
verify. They are never counted against either limit (D-71) and they are never
touched.

**This module has no write path and no deletion path at all.** It enumerates,
it stats, and - only when hashing is explicitly requested - it opens a file for
reading. It does not even write its own output: :func:`collect` returns a
report and the caller hands it to ``layout.write_json``, which is the package's
single guarded write path. That keeps the read-only claim structural rather
than careful, and ``tests/test_storage.py`` asserts it by parsing this module:
no ``shutil`` import, no deletion call, no write call.

Roots are resolved from the environment at run time. No absolute user path
appears in this source, because a user-profile path carries an account name
(D-3).
"""

from __future__ import annotations

import datetime as dt
import hashlib
import os
import pathlib
from dataclasses import dataclass, field

from .limits import Roots, WalkedFile, walk

#: The inventory JSON's own version, so a later reader can tell what shape it is.
SCHEMA_VERSION = 1

#: Read in 1 MiB blocks: large enough that a multi-gigabyte weight does not take
#: all afternoon, small enough that hashing one never holds it in memory.
HASH_BLOCK_BYTES = 1024 * 1024

#: What each extension means, so a reader can separate weights from bookkeeping
#: without opening anything. `pickle-format` is its own class rather than a
#: subclass of `weights`: D-31 refuses those formats outright, and an inventory
#: that filed them under "weights" would be describing them as usable.
EXTENSION_CLASSES: dict[str, str] = {
    ".gguf": "weights-gguf",
    ".safetensors": "weights-safetensors",
    ".onnx": "weights-onnx",
    ".bin": "pickle-format",
    ".pt": "pickle-format",
    ".pth": "pickle-format",
    ".ckpt": "pickle-format",
    ".json": "metadata",
    ".yaml": "metadata",
    ".yml": "metadata",
    ".txt": "metadata",
    ".md": "metadata",
    ".model": "tokenizer",
    ".tiktoken": "tokenizer",
    ".zip": "archive",
    ".gz": "archive",
    ".tar": "archive",
}

DEFAULT_EXTENSION_CLASS = "other"


def classify(path: pathlib.Path) -> str:
    """The extension class of one file. Extension only - nothing is opened here."""
    return EXTENSION_CLASSES.get(path.suffix.lower(), DEFAULT_EXTENSION_CLASS)


def _env_path(*names: str) -> pathlib.Path | None:
    """The first of ``names`` set in the environment, as a path."""
    for name in names:
        value = os.environ.get(name)
        if value:
            return pathlib.Path(value)
    return None


def _profile() -> pathlib.Path:
    """The user profile directory, from the environment, never written down."""
    return _env_path("USERPROFILE", "HOME") or pathlib.Path.home()


def third_party_roots() -> dict[str, pathlib.Path]:
    """The three caches this project does not own, resolved from the environment.

    Each honours its tool's own override variable first and falls back to that
    tool's documented default location under the user profile. A root that does
    not exist is still returned: :func:`collect` records it as absent, which is
    a fact worth recording, rather than dropping it silently.
    """
    profile = _profile()
    lmstudio = _env_path("LMSTUDIO_HOME")
    huggingface = _env_path("HUGGINGFACE_HUB_CACHE")
    if huggingface is None:
        hf_home = _env_path("HF_HOME")
        huggingface = (hf_home / "hub") if hf_home else profile / ".cache" / "huggingface" / "hub"
    return {
        "lmstudio": (lmstudio / "models") if lmstudio else profile / ".lmstudio" / "models",
        "ollama": _env_path("OLLAMA_MODELS") or profile / ".ollama" / "models",
        "huggingface": huggingface,
    }


@dataclass(frozen=True)
class Entry:
    """One file, as the inventory records it."""

    path: str
    bytes: int
    mtime: str
    extension: str
    extension_class: str
    reparse_point: bool
    sha256: str | None = None

    def as_dict(self) -> dict[str, object]:
        return {
            "path": self.path,
            "bytes": self.bytes,
            "mtime": self.mtime,
            "extension": self.extension,
            "extension_class": self.extension_class,
            "reparse_point": self.reparse_point,
            "sha256": self.sha256,
        }


@dataclass
class RootReport:
    """One root's inventory: present or absent, with what was found and skipped."""

    name: str
    path: str
    owned: bool
    present: bool
    entries: list[Entry] = field(default_factory=list)
    skipped_reparse_points: list[str] = field(default_factory=list)

    @property
    def file_count(self) -> int:
        return len(self.entries)

    @property
    def total_bytes(self) -> int:
        return sum(entry.bytes for entry in self.entries if not entry.reparse_point)

    def as_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "path": self.path,
            "owned_by_this_project": self.owned,
            "present": self.present,
            "file_count": self.file_count,
            "total_bytes": self.total_bytes,
            "skipped_reparse_points": self.skipped_reparse_points,
            "entries": [entry.as_dict() for entry in self.entries],
        }


@dataclass
class InventoryReport:
    """Every root, plus the totals a completion note may quote."""

    generated_at: str
    hashed: bool
    roots: list[RootReport] = field(default_factory=list)
    schema_version: int = SCHEMA_VERSION

    @property
    def project_bytes(self) -> int:
        """Bytes under roots this project owns - the only ones the ceiling counts."""
        return sum(root.total_bytes for root in self.roots if root.owned)

    @property
    def third_party_bytes(self) -> int:
        """Bytes under roots it does not own. Excluded from both limits (D-71)."""
        return sum(root.total_bytes for root in self.roots if not root.owned)

    def as_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "generated_at": self.generated_at,
            "hashed": self.hashed,
            "project_bytes": self.project_bytes,
            "third_party_bytes_excluded_from_limits": self.third_party_bytes,
            "roots": [root.as_dict() for root in self.roots],
        }


def sha256_of(path: pathlib.Path) -> str:
    """SHA-256 of one file, read in blocks. Opened read-only, and only on request."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while block := handle.read(HASH_BLOCK_BYTES):
            digest.update(block)
    return digest.hexdigest()


def _entry(walked: WalkedFile, *, hash_files: bool) -> Entry:
    mtime = dt.datetime.fromtimestamp(walked.st.st_mtime, dt.UTC).isoformat()
    digest: str | None = None
    # A reparse point is never opened. Hashing one would follow it, which is the
    # escape the walk exists to refuse.
    if hash_files and not walked.reparse_point:
        try:
            digest = sha256_of(walked.path)
        except OSError:
            digest = None
    return Entry(
        path=str(walked.path),
        bytes=walked.st.st_size,
        mtime=mtime,
        extension=walked.path.suffix.lower(),
        extension_class=classify(walked.path),
        reparse_point=walked.reparse_point,
        sha256=digest,
    )


def inventory_root(
    name: str, root: pathlib.Path, *, owned: bool, hash_files: bool = False
) -> RootReport:
    """Walk one root. An absent root is recorded as absent, never as an error."""
    if not root.is_dir():
        return RootReport(name=name, path=str(root), owned=owned, present=False)
    skipped: list[pathlib.Path] = []
    report = RootReport(name=name, path=str(root), owned=owned, present=True)
    for walked in walk(root, skipped=skipped):
        report.entries.append(_entry(walked, hash_files=hash_files))
    report.entries.sort(key=lambda entry: entry.path)
    report.skipped_reparse_points = sorted(str(path) for path in skipped)
    return report


def collect(roots: Roots, *, hash_files: bool = False) -> InventoryReport:
    """The whole inventory: three third-party caches plus this project's model root.

    Returns the report. It does **not** write it: writing is
    ``layout.write_json``'s job, and keeping the two apart is what lets this
    module carry no write path at all.
    """
    report = InventoryReport(
        generated_at=dt.datetime.now(dt.UTC).isoformat(),
        hashed=hash_files,
    )
    for name, path in third_party_roots().items():
        report.roots.append(inventory_root(name, path, owned=False, hash_files=hash_files))
    report.roots.append(
        inventory_root("project-models", roots.models, owned=True, hash_files=hash_files)
    )
    return report
