# SPDX-FileCopyrightText: 2026 W. Taylor Farrington
# SPDX-License-Identifier: Apache-2.0
"""Command-line entry point (D-21).

The CLI exists from day one as the cheapest end-to-end smoke test the project
has. With no subcommand it prints the package version and the (contract,
registry, template) version triple; all three are placeholders until EP-17
(contracts) and EP-18 (registry loader) give them real values.

`epppsynth scan` (EP-6) runs the leak-prevention checks. It is the single entry
point CI and the pre-commit hook both invoke, so the two cannot drift.

`epppsynth storage` (EP-7) reports the machine's free-space floor and the
project's storage ceiling, and runs the read-only model-cache inventory. CI
never invokes it: no CI job may touch a model root or an index root (D-42).
"""

import argparse
import sys
from collections.abc import Sequence

from epppsynth import __version__

# Placeholders — EP-17 / EP-18 replace these with real, loaded versions.
CONTRACT_VERSION = "none"
REGISTRY_VERSION = "none"
TEMPLATE_VERSION = "none"


def _version() -> int:
    print(f"epppsynth {__version__}")
    print(f"contract={CONTRACT_VERSION} registry={REGISTRY_VERSION} template={TEMPLATE_VERSION}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="epppsynth",
        description="Local, offline-capable reflection aid — deterministic core with a CLI.",
    )
    subcommands = parser.add_subparsers(dest="command")
    subcommands.add_parser(
        "scan",
        add_help=False,
        help="run the leak-prevention scanners (EP-6); see `epppsynth scan --help`",
    )
    subcommands.add_parser(
        "storage",
        add_help=False,
        help="storage limits and the read-only inventory (EP-7); see `epppsynth storage --help`",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] == "scan":
        from epppsynth.publicsafety.scan import main as scan_main

        return scan_main(argv[1:])
    if argv and argv[0] == "storage":
        from epppsynth.storage.cli import main as storage_main

        return storage_main(argv[1:])
    build_parser().parse_args(argv)
    return _version()


if __name__ == "__main__":
    sys.exit(main())
