# SPDX-FileCopyrightText: 2026 W. Taylor Farrington
# SPDX-License-Identifier: Apache-2.0
"""Licence coverage: every tracked file maps to exactly one licence.

`reuse lint` answers the same question and is the acceptance path when it
installs. This exists anyway, for three reasons. It is stdlib-only, so it runs
in the no-model CI path (D-42) without adding a dependency tree. It answers the
*doubly*-matched question, which REUSE tolerates but which means two annotations
disagree about a file. And it checks that the SPDX header inside each `.py` file
agrees with the `REUSE.toml` annotation covering it — `precedence = "aggregate"`
means the header silently wins, so a header that drifts from the table changes
the licence of a file without changing the table anybody reads.

`LICENSE` and `LICENSES/**` are exempt, by name and with a reason, rather than
by being quietly skipped: they are verbatim third-party licence texts reproduced
under the terms each licence states for its own reproduction.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import subprocess
import sys
import tomllib
from collections.abc import Sequence
from dataclasses import dataclass, field

from .paths import repo_root, reuse_toml

#: Paths outside the coverage requirement, each with the reason it is outside.
EXEMPTIONS: dict[str, str] = {
    "LICENSE": (
        "the Apache-2.0 licence text itself, at the root so that licence detection finds it; "
        "reproduced under the terms the licence states for its own reproduction"
    ),
    "LICENSES/**": (
        "verbatim licence texts in the REUSE layout; REUSE excludes this directory from "
        "coverage by definition"
    ),
}

# REUSE-IgnoreStart
# The two patterns below name the SPDX tags, and `reuse lint` would otherwise read
# them as this file's own licence header. The markers are REUSE's own mechanism
# for saying "this is a rule about the tag, not the tag itself"; coverage for this
# file still comes from REUSE.toml and is unaffected.
_SPDX_HEADER = re.compile(r"^#\s*SPDX-License-Identifier:\s*(?P<identifier>.+?)\s*$", re.MULTILINE)
_COPYRIGHT_HEADER = re.compile(r"^#\s*SPDX-FileCopyrightText:\s*(?P<text>.+?)\s*$", re.MULTILINE)
_MISSING_LICENCE_HEADER = "no `SPDX-License-Identifier` header"
_MISSING_COPYRIGHT_HEADER = "no `SPDX-FileCopyrightText` header"
# REUSE-IgnoreEnd


@dataclass
class CoverageReport:
    tracked: tuple[str, ...] = ()
    exempt: tuple[str, ...] = ()
    licence_of: dict[str, str] = field(default_factory=dict)
    unmatched: tuple[str, ...] = ()
    doubly_matched: dict[str, tuple[str, ...]] = field(default_factory=dict)
    header_mismatches: tuple[str, ...] = ()
    unused_patterns: tuple[str, ...] = ()

    @property
    def ok(self) -> bool:
        return not (
            self.unmatched or self.doubly_matched or self.header_mismatches or self.unused_patterns
        )

    def render(self) -> str:
        lines = [
            "licence coverage - REUSE.toml over `git ls-files`",
            f"  tracked files        : {len(self.tracked)}",
            f"  exempt licence texts : {len(self.exempt)}",
            f"  matched exactly once : {len(self.licence_of)}",
            f"  unmatched            : {len(self.unmatched)}",
            f"  doubly-matched       : {len(self.doubly_matched)}",
        ]
        for path in self.unmatched:
            lines.append(f"    ! no annotation covers {path}")
        for path, patterns in sorted(self.doubly_matched.items()):
            lines.append(
                f"    ! {path} is covered by {len(patterns)} patterns: {', '.join(patterns)}"
            )
        for pattern in self.unused_patterns:
            lines.append(
                f"    ! pattern {pattern!r} matches no tracked file (REUSE calls this an error)"
            )
        for message in self.header_mismatches:
            lines.append(f"    ! {message}")
        for pattern, reason in sorted(EXEMPTIONS.items()):
            lines.append(f"  exempt {pattern}: {reason}")
        return "\n".join(lines)


def tracked_files(root: pathlib.Path | None = None) -> tuple[str, ...]:
    """Every file git tracks, as repository-relative POSIX paths."""
    base = root or repo_root()
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=base,
        capture_output=True,
        check=True,
        text=True,
    )
    return tuple(sorted(entry for entry in result.stdout.split("\0") if entry))


def annotations(root: pathlib.Path | None = None) -> tuple[dict[str, object], ...]:
    """The `[[annotations]]` blocks of `REUSE.toml`, in file order."""
    document = tomllib.loads(reuse_toml(root).read_text(encoding="utf-8"))
    blocks = document.get("annotations", [])
    return tuple(blocks)


def pattern_to_regex(pattern: str) -> re.Pattern[str]:
    """Translate a REUSE path pattern. `**` crosses directories; `*` does not."""
    out: list[str] = []
    index = 0
    while index < len(pattern):
        character = pattern[index]
        if pattern.startswith("**", index):
            out.append(".*")
            index += 2
        elif character == "*":
            out.append("[^/]*")
            index += 1
        elif character == "?":
            out.append("[^/]")
            index += 1
        else:
            out.append(re.escape(character))
            index += 1
    return re.compile("^" + "".join(out) + "$")


def is_exempt(path: str) -> bool:
    return any(pattern_to_regex(pattern).match(path) for pattern in EXEMPTIONS)


def licence_coverage(root: pathlib.Path | None = None) -> CoverageReport:
    """Map every tracked file to exactly one licence, and say where that fails."""
    base = root or repo_root()
    files = tracked_files(base)
    exempt = tuple(path for path in files if is_exempt(path))
    covered = [path for path in files if path not in set(exempt)]

    matchers: list[tuple[str, re.Pattern[str], str]] = []
    for block in annotations(base):
        identifier = str(block.get("SPDX-License-Identifier", ""))
        for pattern in block.get("path", []) or []:
            matchers.append((str(pattern), pattern_to_regex(str(pattern)), identifier))

    licence_of: dict[str, str] = {}
    unmatched: list[str] = []
    doubly: dict[str, tuple[str, ...]] = {}
    used: set[str] = set()

    for path in covered:
        hits = [
            (pattern, identifier) for pattern, regex, identifier in matchers if regex.match(path)
        ]
        used.update(pattern for pattern, _ in hits)
        if not hits:
            unmatched.append(path)
        elif len(hits) > 1:
            doubly[path] = tuple(pattern for pattern, _ in hits)
        else:
            licence_of[path] = hits[0][1]

    unused = tuple(sorted({pattern for pattern, _, _ in matchers} - used))
    return CoverageReport(
        tracked=files,
        exempt=exempt,
        licence_of=licence_of,
        unmatched=tuple(unmatched),
        doubly_matched=doubly,
        header_mismatches=_header_mismatches(base, licence_of),
        unused_patterns=unused,
    )


def _header_mismatches(root: pathlib.Path, licence_of: dict[str, str]) -> tuple[str, ...]:
    """Every `.py` file carries an SPDX header, and it agrees with the table."""
    problems: list[str] = []
    for path, identifier in sorted(licence_of.items()):
        if not path.endswith(".py"):
            continue
        text = (root / path).read_text(encoding="utf-8")
        header = _SPDX_HEADER.search(text)
        if header is None:
            problems.append(f"{path}: {_MISSING_LICENCE_HEADER}")
        elif header.group("identifier") != identifier:
            problems.append(
                f"{path}: header says {header.group('identifier')!r}, REUSE.toml says "
                f'{identifier!r}; `precedence = "aggregate"` means the header would win'
            )
        if _COPYRIGHT_HEADER.search(text) is None:
            problems.append(f"{path}: {_MISSING_COPYRIGHT_HEADER}")
    return tuple(problems)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m epppsynth.rights.coverage",
        description="Assert every tracked file maps to exactly one licence under REUSE.toml.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit non-zero if any file is unmatched or doubly-matched (the default behaviour)",
    )
    args = parser.parse_args(argv)
    del args  # --check is accepted for the documented invocation; the check always runs

    report = licence_coverage()
    print(report.render())
    return 0 if report.ok else 1


if __name__ == "__main__":  # pragma: no cover - CLI entry
    sys.exit(main())
