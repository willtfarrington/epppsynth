# epppsynth — package

The uv project. Run every command from this directory:

```
uv sync --locked
uv run ruff check . && uv run ruff format --check .
uv run pytest -m "not requires_index and not requires_model" -q
```

Nothing here implements the tool yet — `src/epppsynth/` holds a package skeleton and a CLI that
prints a version triple of placeholders.

Read [`GOVERNANCE.md`](GOVERNANCE.md) first: it states the invariants, the data boundary and the
excluded release classes, and it overrides [`DESIGN.md`](DESIGN.md) and every roadmap brief.
[`DECISIONS.md`](DECISIONS.md) records why each choice was made; its index block is the intended
entry point. Public front matter, the maturity badge and its evidence file live at the repository
root — see [`../README.md`](../README.md) and [`../CLAUDE.md`](../CLAUDE.md).
