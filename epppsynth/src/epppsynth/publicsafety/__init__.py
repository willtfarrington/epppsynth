# SPDX-FileCopyrightText: 2026 W. Taylor Farrington
# SPDX-License-Identifier: Apache-2.0
"""Public-safety scanners: the checks that stop a leak reaching a public commit.

`epppsynth scan` runs all nine, in CI on `windows-latest` and in an identical
pre-commit hook. `scan.py` holds the checks, `allowlist.py` the three separately
counted allowlists, and `ledger.py` the one check that reads private planning
state and reports only positions inside the already-public file.

`.gitignore`, pre-commit hooks and CI scanners are **defense in depth. They are
not proof that nothing leaked.** The proof is the pre-publication review packet
in `epppsynth/docs/pre-publication-checklist.md`, performed by a human, recorded
with a date and a commit hash.
"""

from __future__ import annotations

from .allowlist import (
    CANARY_ALLOWLIST,
    CANARY_DIR,
    MODALITY_EXEMPTIONS,
    RULE_DEFINITION_MARKER,
    Skip,
    is_canary,
    marked_lines,
)
from .scan import CHECKS, CheckResult, Finding, ScanReport, main, run_scan

__all__ = [
    "CANARY_ALLOWLIST",
    "CANARY_DIR",
    "CHECKS",
    "CheckResult",
    "Finding",
    "MODALITY_EXEMPTIONS",
    "RULE_DEFINITION_MARKER",
    "ScanReport",
    "Skip",
    "is_canary",
    "main",
    "marked_lines",
    "run_scan",
]
