"""Render `epppsynth/copy/banned-phrases.toml` into the generated block of `SAFETY.md` (EP-3).

The banned-phrase list lives in exactly one place. `SAFETY.md` publishes it and the EP-39 lint
consumes it; if the published list were retyped it would drift from the linted one within a
release. This script is the transclusion step, and `--check` is the drift alarm.

    python tools/render_banned_phrases.py            # rewrite the block in SAFETY.md
    python tools/render_banned_phrases.py --check    # exit 1 if the block is stale
"""

from __future__ import annotations

import pathlib
import sys
import tomllib

ROOT = pathlib.Path(__file__).resolve().parents[1]
TOML_PATH = ROOT / "epppsynth" / "copy" / "banned-phrases.toml"
SAFETY_PATH = ROOT / "SAFETY.md"

BEGIN = "<!-- BEGIN GENERATED: banned-phrases (source: epppsynth/copy/banned-phrases.toml) -->"
END = "<!-- END GENERATED: banned-phrases -->"


def load(toml_path: pathlib.Path = TOML_PATH) -> list[dict]:
    """Return the phrase entries, in file order."""
    return tomllib.loads(toml_path.read_text(encoding="utf-8"))["phrases"]


def _cell(text: str) -> str:
    return text.replace("|", r"\|").strip()


def render(toml_path: pathlib.Path = TOML_PATH) -> str:
    """Return the markdown block, without the surrounding markers."""
    rows = [
        "| # | Phrase | Applies | Why it is banned | Enforces |",
        "|---|---|---|---|---|",
    ]
    for entry in load(toml_path):
        applies = _cell(entry.get("condition", "always")) if entry.get("condition") else "always"
        rows.append(
            f"| `{_cell(entry['id'])}` | **{_cell(entry['phrase'])}** | {applies} "
            f"| {_cell(entry['reason'])} | {_cell(entry['d_ref'])} |"
        )
    rows.append("")
    rows.append(
        f"*{len(load(toml_path))} entries, rendered from "
        "[`epppsynth/copy/banned-phrases.toml`](epppsynth/copy/banned-phrases.toml). "
        "Edit the file, not this table.*"
    )
    return "\n".join(rows)


def splice(document: str, block: str) -> str:
    """Return `document` with the generated block replaced by `block`."""
    start = document.index(BEGIN) + len(BEGIN)
    end = document.index(END)
    return f"{document[:start]}\n\n{block}\n\n{document[end:]}"


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    document = SAFETY_PATH.read_text(encoding="utf-8")
    updated = splice(document, render())
    if "--check" in argv:
        if updated != document:
            print("SAFETY.md banned-phrase block is stale; run tools/render_banned_phrases.py")
            return 1
        print("SAFETY.md banned-phrase block matches epppsynth/copy/banned-phrases.toml")
        return 0
    SAFETY_PATH.write_text(updated, encoding="utf-8", newline="\n")
    print(f"rendered {len(load())} entries into SAFETY.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
