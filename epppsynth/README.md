# epppsynth — package

The uv project. Run every command from this directory:

```
uv sync --locked
uv run ruff check . ../tools/roadmap_check.py
uv run ruff format --check . ../tools/roadmap_check.py
uv run pytest -m "not requires_index and not requires_model" -q
uv run epppsynth scan --history
uv run python ../tools/roadmap_check.py --all
```

**Nothing here implements the tool yet.** `src/epppsynth/` holds a CLI and three packages, every one
of which checks the project rather than being it: `publicsafety/` (the leak-prevention scanners),
`rights/` (the per-source rights and licence checks) and `storage/` (the two roots, the reserve floor
and the project ceiling). No registry, no composer, no selection, no abstention chain, no renderer,
no interface. `tools/roadmap_check.py` sits outside this project, at the repository root, and is
linted here by name because CI depends on it.

Read [`GOVERNANCE.md`](GOVERNANCE.md) first: it states the invariants, the data boundary and the
excluded release classes, and it overrides [`DESIGN.md`](DESIGN.md) and every roadmap brief.
[`DECISIONS.md`](DECISIONS.md) records why each choice was made; its index block is the intended
entry point. Public front matter, the maturity badge and its evidence file live at the repository
root — see [`../README.md`](../README.md) and [`../CLAUDE.md`](../CLAUDE.md).
