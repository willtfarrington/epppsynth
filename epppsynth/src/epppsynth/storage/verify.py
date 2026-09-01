# SPDX-FileCopyrightText: 2026 W. Taylor Farrington
# SPDX-License-Identifier: Apache-2.0
"""The weight verifier: revision, format, and hash (D-31, D-44).

Four refusals, in the order a cheap check should precede an expensive one:

1. **Revision.** A 40-hex commit SHA or nothing. A branch name moves, and a
   weight pinned to a moving ref is not pinned.
2. **Extension.** GGUF, and safetensors where an embedding model requires it
   (D-44 applies the same rules to embedding models). Nothing else.
3. **Magic bytes.** The file is opened and its first bytes are read, because an
   extension is a claim and a magic number is evidence. A pickle-format file
   named ``.gguf`` is exactly the case an extension check misses, and pickle
   deserialisation is arbitrary code execution.
4. **Hash.** SHA-256 against the value pinned in ``METADATA.json``. A blob that
   does not match is an **unidentified blob**: it is recorded as one and it does
   not enter ``models.lock.json``.

``trust_remote_code`` appears in this package exactly once, as an unconditional
``False`` with no override path (D-31). A test greps the whole package source
for an assignment of ``True`` to it.

``--trust-cached`` skips step 4 only, and **records itself**: the resulting
:class:`Verification` carries ``trusted_cached=True`` and
:meth:`Verification.record` puts that in the benchmark packet (EP-32), so a fast
run can never be read as a verified one.
"""

from __future__ import annotations

import datetime as dt
import pathlib
import re
from dataclasses import dataclass

from .inventory import sha256_of
from .layout import Metadata

#: D-31, unconditionally. There is no parameter, no environment variable and no
#: configuration key that changes it. Remote code execution during model load is
#: the single largest supply-chain surface a local runtime has.
TRUST_REMOTE_CODE = False

#: GGUF is the runtime format (D-31). Safetensors is permitted only because an
#: embedding model may ship in no other non-pickle format (D-44).
ALLOWED_SUFFIXES = frozenset({".gguf", ".safetensors"})

REVISION_PATTERN = re.compile(r"^[0-9a-f]{40}$")

GGUF_MAGIC = b"GGUF"

#: A zip container. `torch.save` writes one, and what is inside it is a pickle.
ZIP_MAGIC = b"PK\x03\x04"

#: Pickle protocol 2-5 open with `0x80` and the protocol number. Protocol 0 and
#: 1 open with a bare opcode; the four below are the ones that begin a real
#: pickle stream in practice. The check is deliberately broad: a false positive
#: costs a re-download, a false negative costs arbitrary code execution.
PICKLE_PROTO_RANGE = range(2, 6)
PICKLE_OPCODES = frozenset({0x28, 0x5D, 0x7D, 0x63, 0x8A})

MAGIC_READ_BYTES = 16


class VerificationError(Exception):
    """Base for every refusal the verifier makes."""


class BadRevisionError(VerificationError):
    """The revision is not a 40-hex commit SHA (D-31)."""


class DisallowedFormatError(VerificationError):
    """The file is not GGUF or safetensors (D-31, D-44)."""


class PickleFormatError(DisallowedFormatError):
    """The file's bytes are a pickle or a pickle-bearing archive, whatever it is called."""


class HashMismatchError(VerificationError):
    """The computed SHA-256 does not match the pinned one: an unidentified blob."""


def detect_format(path: pathlib.Path) -> str:
    """The file's format from its first bytes: never from its name.

    Returns one of ``gguf``, ``safetensors``, ``pickle``, ``zip-archive`` or
    ``unknown``.
    """
    with open(path, "rb") as handle:
        head = handle.read(MAGIC_READ_BYTES)
    if head.startswith(GGUF_MAGIC):
        return "gguf"
    if head.startswith(ZIP_MAGIC):
        return "zip-archive"
    if len(head) >= 2 and head[0] == 0x80 and head[1] in PICKLE_PROTO_RANGE:
        return "pickle"
    if head and head[0] in PICKLE_OPCODES:
        return "pickle"
    if len(head) >= 9:
        header_length = int.from_bytes(head[:8], "little")
        if 0 < header_length < 100_000_000 and head[8:9] == b"{":
            return "safetensors"
    return "unknown"


@dataclass(frozen=True)
class Verification:
    """The outcome of verifying one weight, in the shape a packet can carry.

    ``sha256`` is the value that identifies the weight - recomputed from the
    file on a verified run, and taken from ``METADATA.json`` on a
    ``--trust-cached`` one. Which of the two it is is never left to inference:
    ``trusted_cached`` says so, and :meth:`record` prints it.
    """

    path: str
    repo: str
    revision: str
    detected_format: str
    bytes: int
    sha256: str | None
    trusted_cached: bool
    checked_at: str

    @property
    def hash_verified(self) -> bool:
        return self.sha256 is not None and not self.trusted_cached

    def record(self) -> dict[str, object]:
        """The record EP-32 embeds in a benchmark packet.

        ``verification`` is ``"sha256"`` or ``"trust-cached"``. A run that
        skipped the hash says so in its own packet; that is the whole reason the
        escape hatch is allowed to exist.
        """
        return {
            "repo": self.repo,
            "revision": self.revision,
            "filename": pathlib.Path(self.path).name,
            "format": self.detected_format,
            "bytes": self.bytes,
            "sha256": self.sha256,
            "verification": "trust-cached" if self.trusted_cached else "sha256",
            "trust_remote_code": TRUST_REMOTE_CODE,
            "checked_at": self.checked_at,
        }


def check_revision(revision: str) -> None:
    """Refuse anything that is not a 40-hex commit SHA."""
    if not REVISION_PATTERN.match(revision):
        raise BadRevisionError(
            f"revision {revision!r} is not a 40-hex commit SHA. A branch or tag name is a "
            "moving target, and a weight pinned to one is not pinned (D-31)."
        )


def check_format(path: pathlib.Path) -> str:
    """Refuse by extension, then refuse by magic bytes. Returns the detected format."""
    suffix = path.suffix.lower()
    if suffix not in ALLOWED_SUFFIXES:
        raise DisallowedFormatError(
            f"{path.name}: {suffix or 'no extension'} is not an accepted weight format. "
            f"Accepted: {', '.join(sorted(ALLOWED_SUFFIXES))} (D-31, D-44)."
        )
    detected = detect_format(path)
    if detected in {"pickle", "zip-archive"}:
        raise PickleFormatError(
            f"{path.name}: the file's first bytes are a {detected}, whatever its extension "
            "says. Pickle deserialisation is arbitrary code execution; D-31 refuses the "
            "format outright."
        )
    expected = "gguf" if suffix == ".gguf" else "safetensors"
    if detected != expected:
        raise DisallowedFormatError(
            f"{path.name}: extension claims {expected} but the first bytes read as "
            f"{detected}. The extension is a claim; the magic number is the evidence."
        )
    return detected


def verify_weight(
    path: pathlib.Path, metadata: Metadata, *, trust_cached: bool = False
) -> Verification:
    """Verify one weight against its ``METADATA.json`` record.

    Load-time re-verification is on by default. ``trust_cached=True`` skips the
    SHA-256 read - the expensive step on a multi-gigabyte file - and stamps the
    result so the skip travels with it.
    """
    check_revision(metadata.revision)
    detected = check_format(path)
    size = path.stat().st_size
    if size != metadata.bytes:
        raise HashMismatchError(
            f"{path.name}: {size} bytes on disk, {metadata.bytes} pinned in METADATA.json. "
            "An unidentified blob; it does not enter the lockfile."
        )
    digest: str | None = None
    if not trust_cached:
        digest = sha256_of(path)
        if digest != metadata.sha256:
            raise HashMismatchError(
                f"{path.name}: computed SHA-256 does not match the pinned value. The file "
                "is an unidentified blob, not a known model, and is excluded from the "
                "lockfile (D-31)."
            )
    return Verification(
        path=str(path),
        repo=metadata.repo,
        revision=metadata.revision,
        detected_format=detected,
        bytes=size,
        sha256=digest or metadata.sha256,
        trusted_cached=trust_cached,
        checked_at=dt.datetime.now(dt.UTC).isoformat(),
    )
