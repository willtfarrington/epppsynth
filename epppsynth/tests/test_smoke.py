"""Smoke tests (EP-1): the package imports, has a version, and the CLI exits 0."""

import epppsynth
from epppsynth import cli


def test_package_imports():
    assert epppsynth is not None


def test_version_is_string():
    assert isinstance(epppsynth.__version__, str)
    assert epppsynth.__version__


def test_cli_main_exits_zero(capsys):
    assert cli.main() == 0
    out = capsys.readouterr().out
    assert epppsynth.__version__ in out
    assert "contract=" in out
