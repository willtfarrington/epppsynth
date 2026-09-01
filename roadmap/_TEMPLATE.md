# EP-<n> — <Title>

**Size:** S|M|L · **Mode:** a|b|c|n/a · **Core/Stretch:** core|stretch ·
**Depends on:** EP-x (title), … · **Blocks:** EP-y (title), …

## Context

Why this brief exists now, which `D-n` it implements, what already exists in the tree, and what does
not. Self-contained: a session that has read only this brief plus the load-order files
(`CLAUDE.md` → `epppsynth/GOVERNANCE.md` → the `DECISIONS.md` index block → this phase's table in
`roadmap/README.md` → this brief) can execute it without reading any other brief.

## Safety preconditions

Which invariants this brief could violate, and the specific guard for each. `n/a` is a valid answer
but must be written, not omitted. Every brief that touches a public artifact names the relevant
pre-publication checklist items here.

## In scope

Numbered, ordered, concrete steps.

## Out of scope

Each excluded item names the `EP-n` or `final-roadmap.md` entry that owns it.

## Verification / acceptance

Mechanically checkable wherever possible. Every brief names at least one command. Judgement-based
criteria are marked *(judgement)* and say who judges.

## Parked → final-roadmap.md

Items discovered during this brief that belong to a later release. Mirrored into
`final-roadmap.md` at the phase re-plan. `none` is a valid entry.

---

## Rules the template carries, checked by `tools/roadmap_check.py`

Ratified at **EP-8** against the nine P0 briefs executed from it. The six sections above were
confirmed unchanged; what follows was **added**, because nine executions showed each of these was a
convention nobody had written down.

- **The header is one contiguous block**, from `**Size:**` to the end of `**Blocks:**`, terminated
  by a blank line. Nothing else goes inside it. A charter note is a separate block below it.
- **`Depends on` and `Blocks` are exact mirrors** and name immediate neighbours only. The phase
  table's `Depends on` column is the authority; `--deps` fails on any asymmetry, and `--table` fails
  when the row and the header disagree.
- **The completion note is appended at the very end of the file**, below `## Parked →`. EP-3 and
  EP-4 put it above, and because executed briefs are append-only (`CLAUDE.md`) neither can now be
  tidied — so `--sections` checks the canonical headings' relative order and tolerates this, and the
  template says where the note goes so no later brief repeats it.
- **A completion note records what was observed, not what was expected**, names its deviations, and
  **may not claim CI green without naming the run as a linked id** (owner ruling OD-15).
- **A brief is never rewritten once executed.** `## Context` is the historical record and
  `--immutable` compares it against the blob at the commit its done box records. Staleness is
  annotated with `> **EP-n pickup note.**` appended below, never spliced into `## Context`.

### The charter variant (P3 … P7)

A charter brief is a declared five-section variant, and `--sections` checks it as such:

```
## Context · ## Safety preconditions · ## Scope sketch (refine at re-plan) ·
## Verification / acceptance (sketch) · ## Parked → final-roadmap.md
```

It carries, directly below the header block:

```
> **Charter.** **EP-n (title)** upgrades this to a full brief: `## Scope sketch` splits into
> `## In scope` / `## Out of scope`, and each sketched criterion below becomes a named command or
> artifact. Do not execute from the sketch alone.
```

A charter is the one form exempt from naming a command in its acceptance section, and the exemption
has a price: `--acceptance` requires the charter note to name a re-plan EP that exists, counts every
exemption, and prints them. A charter nobody ever upgrades is what the count is for.
