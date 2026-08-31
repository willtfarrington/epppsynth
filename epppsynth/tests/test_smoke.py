# SPDX-FileCopyrightText: 2026 W. Taylor Farrington
# SPDX-License-Identifier: Apache-2.0
"""Smoke tests (EP-1): the package imports, has a version, and the CLI exits 0."""

import epppsynth
from epppsynth import cli


def test_package_imports():
    assert epppsynth is not None


def test_version_is_string():
    assert isinstance(epppsynth.__version__, str)
    assert epppsynth.__version__


def test_cli_main_exits_zero(capsys):
    # An explicit empty argv: `main()` reads `sys.argv[1:]` for the console-script
    # entry point, and under pytest that is pytest's own arguments (EP-6 added the
    # `scan` subcommand, so the CLI now parses what it is given).
    assert cli.main([]) == 0
    out = capsys.readouterr().out
    assert epppsynth.__version__ in out
    assert "contract=" in out
