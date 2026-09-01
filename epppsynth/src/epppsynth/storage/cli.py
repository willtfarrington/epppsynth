# SPDX-FileCopyrightText: 2026 W. Taylor Farrington
# SPDX-License-Identifier: Apache-2.0
"""``epppsynth storage check`` and ``epppsynth storage inventory`` (EP-7).

Neither subcommand writes anything into the repository. ``check`` writes nothing
at all; ``inventory`` writes exactly one JSON file, under the model root's
``inventory/`` subtree, through the package's single guarded write path.

Neither prints a per-file path. The inventory output is the single most likely
source of a local path or a machine identifier in this project (pre-publication
checklist item 4), so the console summary is counts and totals, and the file
that holds the paths lives outside the repository tree.
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

from . import inventory as inventory_module
from . import layout
from .limits import (
    DEFAULT_ROOTS,
    EXPECTED_USAGE_BYTES,
    PROJECT_CEILING_BYTES,
    PROJECT_WARN_BYTES,
    RESERVE_FLOOR_BYTES,
    Roots,
    free_space,
    project_footprint,
    system_volume,
    writes_halted,
)


def gib(value: int) -> str:
    return f"{value / 1024**3:,.1f} GiB"


def gb(value: int) -> str:
    return f"{value / 1000**3:,.2f} GB"


def check(roots: Roots = DEFAULT_ROOTS) -> int:
    """Free space, the floor, the footprint, the ceiling, and lockfile integrity."""
    volume = system_volume()
    free = free_space(volume)
    headroom = free - RESERVE_FLOOR_BYTES
    print("epppsynth storage check")
    print(f"  system volume      {volume}")
    print(f"  free               {gib(free)}")
    print(f"  reserve floor      {gib(RESERVE_FLOOR_BYTES)}  (D-49, binary, machine's not the")
    print("                     project's; the project never claims the headroom above it)")
    print(f"  headroom           {gib(headroom)}  {'OK' if headroom >= 0 else 'BELOW FLOOR'}")
    footprint = project_footprint(roots)
    print(f"  project footprint  {gb(footprint)}")
    print(f"  warn level         {gb(PROJECT_WARN_BYTES)}  (D-78, decimal)")
    print(f"  hard ceiling       {gb(PROJECT_CEILING_BYTES)}  (D-78, decimal)")
    low, high = EXPECTED_USAGE_BYTES
    print(f"  expected usage     {gb(low)} - {gb(high)}")
    print("  the pre-existing third-party model cache is outside both figures (D-71)")

    report = layout.validate_layout(roots)
    if report.ok:
        print("  layout             both roots present with the expected subtrees")
    else:
        for problem in report.problems:
            print(f"  layout             {problem}")
        print("  run `epppsynth storage inventory` to create the roots")
    lock = layout.read_lockfile(roots)
    if lock is None:
        print(f"  lockfile           {layout.LOCKFILE_NAME} absent - no weight is downloaded yet")
    else:
        weights = lock.get("weights") if isinstance(lock, dict) else None
        count = len(weights) if isinstance(weights, list) else 0
        print(f"  lockfile           {count} weight(s) recorded")
    halt = writes_halted()
    if halt is not None:
        print(f"  WRITES HALTED      {halt}")

    if headroom < 0 or halt is not None:
        return 1
    return 0


def inventory(roots: Roots = DEFAULT_ROOTS, *, hash_files: bool = False) -> int:
    """Enumerate the four roots read-only and write one JSON file outside the repository."""
    layout.ensure_layout(roots)
    report = inventory_module.collect(roots, hash_files=hash_files)
    destination = roots.models / "inventory" / f"{layout.utc_stamp()}.json"
    layout.write_json(destination, report.as_dict(), roots=roots)

    print("epppsynth storage inventory  (read-only; nothing under a scanned root is modified)")
    for root in report.roots:
        owner = "project" if root.owned else "third-party (D-71: outside both limits)"
        if not root.present:
            print(f"  {root.name:<16} absent                              {owner}")
            continue
        skipped = len(root.skipped_reparse_points)
        note = f"  {skipped} reparse point(s) recorded and not followed" if skipped else ""
        size = gib(root.total_bytes)
        print(f"  {root.name:<16} {root.file_count:>6} file(s)  {size:>12}  {owner}{note}")
    print(f"  project total      {gb(report.project_bytes)}")
    print(f"  third-party total  {gib(report.third_party_bytes)}  (excluded from both limits)")
    print(
        f"  hashed             {'yes' if report.hashed else 'no (pass --hash to compute SHA-256)'}"
    )
    print(f"  written to         {destination}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="epppsynth storage",
        description=(
            "Storage roots, the 250 GiB machine floor and the 25 GB project ceiling (EP-7). "
            "Read-only: this command group builds no purge tool and deletes nothing. The "
            "seven rules a purge tool would have to satisfy are in ADR-007."
        ),
    )
    subcommands = parser.add_subparsers(dest="subcommand", required=True)
    subcommands.add_parser(
        "check", help="free space, the floor, the project footprint, the ceiling, the lockfile"
    )
    run = subcommands.add_parser(
        "inventory", help="enumerate the four model roots read-only and write one JSON file"
    )
    run.add_argument(
        "--hash",
        action="store_true",
        dest="hash_files",
        help="also compute SHA-256 per file; opt-in, because it reads every byte of every weight",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if args.subcommand == "check":
        return check()
    return inventory(hash_files=args.hash_files)


if __name__ == "__main__":  # pragma: no cover - CLI entry
    sys.exit(main())
