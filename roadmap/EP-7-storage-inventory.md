# EP-7 — Storage roots, cache inventory, reserve floor & project ceiling

**Size:** L · **Mode:** n/a · **Core/Stretch:** core ·
**Depends on:** EP-1 (toolchain, package skeleton, ADR framework, CI) · **Blocks:** EP-8 (roadmap tooling, re-plan P0), EP-22 (corpus ingest and local index), EP-32 (benchmark packet schema)

## Context

Nothing in this project may download a model, build an index, or write a benchmark packet until
there is a mechanism that refuses to do so when the machine cannot afford it. EP-7 is that
mechanism. It is independent of the documentation chain and may run in parallel with EP-2 … EP-6.

**The two limits are different things and must not be collapsed into one number** (D-78):

- **Floor (machine).** ≥ **250 GiB** free on the system volume **at all times**, checked
  immediately **before and after every write**. This protects the operator's non-project use of
  their own machine. It is not a project allocation and the project never claims the headroom
  above it.
- **Ceiling (project).** The total footprint of `C:\epppmodels` + `C:\epppindex` is capped at
  **25 GB**, warned at **20 GB**, and hard-stopped at 25 GB unless the owner raises it in writing.
  Expected real usage is one ≤ 5 GB generation model, one small embedding model, a local index of
  roughly 1–2 GB, and JSON packets — about **8–12 GB**.

A pre-existing third-party model cache of roughly **92 GB** exists on this machine. It is **out of
scope**, is **not** part of either figure (D-71), and **must not be touched**. EP-7 inventories it
**read-only** because D-30 requires the inventory to include it and because reuse of an already-
downloaded weight is preferred over a re-download when revision and hash verify.

**EP-7 builds no purge tool.** It writes the seven cache-purge safety rules as `ADR-007` so that any
future purge work starts from a specification rather than from improvisation, and it stops there.
The inventory is strictly read-only: it enumerates, it hashes on request, and it never deletes.

**Two separate roots, deliberately.** `C:\epppmodels` holds weights, metadata, the lockfile and
benchmark packets. `C:\epppindex` holds the D-16 local index — a **different rights class**,
independently purgeable and independently excludable from backup (D-51). Merging them would put
copyrighted-derived content and freely-licensed weights under one retention policy.

**What exists.** The uv project with a CLI entry point, `epppsynth/docs/adr/` with `ADR-007` and
`ADR-009` as stubs naming EP-7 as their author, and a green CI workflow that must never see either
root.

**What this brief creates.** `epppsynth/src/epppsynth/storage/` (preflight, inventory, layout,
verifier), two CLI subcommands, the `C:\epppmodels` and `C:\epppindex` trees with their schemas,
`ADR-007` (seven purge-safety rules) and `ADR-009` (roots, floor, ceiling).

Implements: D-30 (model root, one at a time, ≤ ~8 GB each, individually confirmed; inventory
includes the third-party cache), D-31 and D-44 (weights verified by revision + file hash; remote
code execution disabled; no pickle formats; GGUF only; identical rules for embedding models),
D-49 and D-78 (floor in GiB, checked before *and* after every write; project ceiling with a warn
level), D-51 (separate index root), D-71 (the third-party cache is kept and excluded from the
project budget; the purge rules ship as ADR-007 regardless). Mitigates R-21 (a future
cache-purge escaping the model root) and R-19 (index leaking into a published artifact).

## Safety preconditions

| Invariant at risk | Guard in this brief |
|---|---|
| Deleting or modifying the operator's pre-existing 92 GB cache (D-71) | The inventory module has **no delete, move, rename or write path into any scanned root**. It opens files read-only and only when hashing is explicitly requested. A unit test asserts the module imports nothing from `shutil`, `os.remove`, `os.unlink`, `pathlib.Path.unlink`, `pathlib.Path.rmdir` or `send2trash`, by AST inspection of the module source. That is a stronger guarantee than a code review. |
| Filling the system volume (D-78 floor) | `preflight_space(volume, bytes_needed)` asserts `free_bytes - bytes_needed >= 250 GiB` and is called **before** and **after** every write, with the post-write check treated as an error condition that halts further writes even though the bytes are already on disk — the point is to stop the *next* one. |
| Silent growth past the project ceiling (D-78) | `project_footprint()` sums both roots. Above 20 GB it warns on every call; at or above 25 GB it raises and no write proceeds. The threshold constants live in one module with a comment naming D-78 and stating that raising them requires a written owner decision recorded as a `DECISIONS.md` addendum. |
| A purge tool appearing by accident | This brief creates no deletion code path of any kind. `ADR-007` is written in the imperative for a *future* packet and its Status is `accepted — no implementation exists`. Acceptance criterion 8 asserts the repository contains no deletion call outside test cleanup. |
| Copyrighted-derived index content reaching a public artifact (D-16, D-51, R-19) | Both roots are outside the repository tree. Their paths appear in documentation and ADRs (deliberately public) but never as a default value in code — EP-6's root scanner enforces the distinction and EP-7's configuration reads the roots from a module constant that EP-6 explicitly allowlists by symbol, not by pattern. Index contents are never enumerated into any artifact that is committed. |
| Reparse points / junctions turning a walk into an escape | The inventory records `FILE_ATTRIBUTE_REPARSE_POINT` per entry and **does not follow** reparse points during the walk. A directory carrying the flag is recorded and skipped, with the skip visible in the output. |
| An unverified blob being treated as a known model (D-31) | A cached file is reusable only when its computed SHA-256 matches a pinned upstream revision recorded in `METADATA.json`. Otherwise it is recorded as an **unidentified blob** and excluded from `models.lock.json`. |
| Machine specifics leaking into a public artifact (D-3) | Inventory output is written **only** to `C:\epppmodels\inventory\<UTC>.json`, which is outside the repository. Nothing from a real inventory run is committed. Tests use a fake filesystem. The completion note reports **counts and totals**, never absolute paths, filenames or hardware identifiers. |

Pre-publication checklist items exercised here: **4 (local paths & hostname — the inventory output
is the single most likely source of both, and it is never committed)**, **6 (licence conformance —
`METADATA.json` carries each weight's licence id and URL)**.

## In scope

1. **`epppsynth/src/epppsynth/storage/limits.py`** — the constants and the two guards:
   `RESERVE_FLOOR_BYTES = 250 * 1024**3` (GiB, per D-49), `PROJECT_CEILING_BYTES = 25 * 1000**3`
   and `PROJECT_WARN_BYTES = 20 * 1000**3` (GB, per D-78), each with a comment naming its decision
   and stating that changing it requires a written owner decision recorded as a dated addendum.
   Functions: `free_space(volume)`, `preflight_space(volume, bytes_needed)`,
   `postwrite_space(volume)`, `project_footprint()`, `assert_within_ceiling(additional_bytes)`.
   > *Unit note:* the floor is binary (GiB) and the ceiling is decimal (GB) exactly as D-49 and
   > D-78 state them. Do not normalise one to the other; record the mismatch in `ADR-009` so a
   > later reader knows it is deliberate transcription, not a bug. Flag it at the P0 re-plan.
2. **`epppsynth/src/epppsynth/storage/inventory.py`** — the strictly read-only inventory over four
   roots: the LM Studio model directory, the Ollama model directory, the Hugging Face hub cache,
   and `C:\epppmodels`. Roots are resolved from environment variables (`%USERPROFILE%`-relative)
   at run time; **no absolute user path is written into the source**. Per entry: absolute path,
   size, mtime, extension class, reparse-point flag, and — opt-in only — SHA-256. Emits JSON to
   `C:\epppmodels\inventory\<UTC>.json`. A missing root is recorded as absent, not an error.
3. **`epppsynth/src/epppsynth/storage/layout.py`** — create and validate the two trees:

   ```
   C:\epppmodels\
     models.lock.json                    # authoritative: every weight the project may load
     models\<publisher>\<repo>\<revision>\<file>.gguf
     models\<publisher>\<repo>\<revision>\METADATA.json
     embeddings\<same shape>             # D-44: identical rules
     benchmarks\run-<UTC>-<shorthash>.json
     inventory\<UTC>.json
   C:\epppindex\                         # SEPARATE ROOT — D-16 index, different rights class
   ```

   `METADATA.json` fields: repo, revision (a commit SHA, never a branch), filename, sha256, bytes,
   quantization, licence id and URL, `acquired_at`, acceptable-use notes, `verified_at`.
4. **`epppsynth/src/epppsynth/storage/verify.py`** — the weight verifier:
   - SHA-256 of the file compared against `METADATA.json`;
   - **GGUF only** (and safetensors where an embedding model requires it) — refuse `.bin`, `.pt`,
     `.pth` and any pickle-format file by magic-byte inspection, not by extension alone;
   - `trust_remote_code=False` unconditionally, asserted as a constant with no override;
   - revision must be a 40-hex commit SHA;
   - load-time re-verification **on by default**, with a `--trust-cached` escape hatch that
     **records itself in the benchmark packet** so a fast run can never be mistaken for a verified
     one.
5. **CLI subcommands:** `epppsynth storage inventory [--hash]` and `epppsynth storage check`
   (footprint, floor, ceiling, lockfile integrity). Both print a summary; neither writes anything
   into the repository.
6. **Write `ADR-009 — storage roots and limits`**: the two roots and why they are separate; the
   floor and its before-and-after rule; the ceiling, the warn level and the expected 8–12 GB real
   usage; the statement that the project never claims the headroom above the floor; the deliberate
   GiB/GB transcription note; and the explicit exclusion of the pre-existing third-party cache
   (D-71) from both figures.
7. **Write `ADR-007 — cache-purge safety rules`** — the seven rules, verbatim in substance, with
   `Status: accepted — no implementation exists`:
   1. **One configured cache root**, absolute, from configuration — not from `argv`, not from an
      environment variable read at use time.
   2. **Prove descendancy**: fully resolve root and target (following symlinks and junctions), then
      require `target.is_relative_to(root)` **and** `target != root` **and**
      `len(target.parts) >= 4`.
   3. **Reject drive roots**, the user profile root, the Windows directory, `Program Files`, and any
      repository working tree (detected by walking up for `.git`) — as root **or** as target.
   4. **Reject unresolved variables and globs**: any residual `%…%`, `$env:`, `~`, or `* ? [ ]` is a
      hard error. No globbing at all — deletion consumes an explicit file list produced by the
      inventory step.
   5. **Refuse reparse-point traversal**: if any directory in the walk carries
      `FILE_ATTRIBUTE_REPARSE_POINT`, stop and demand explicit per-path approval.
   6. **Inventory → dry-run → confirm**: emit a plan file (path, bytes, reason, hash), print totals,
      and require the operator to confirm **that plan's hash**. Plans expire in 15 minutes.
   7. **Preserve the reserve and prefer recoverable deletion**: log pre- and post-free space; refuse
      to run if pre-purge free space is already below the floor and the plan does not remedy it;
      send to the Recycle Bin rather than unlinking; never recursively force-remove a directory.
8. **Run the inventory once, read-only**, against the real roots. Confirm the third-party cache is
   enumerated and untouched: record its file count and total size, compare mtimes before and after,
   and assert every mtime is unchanged. Report counts and totals only.
9. **Verify the roots are outside any cloud-sync scope** before anything is written into them
   (WS2-A5): check that neither root falls under a known sync provider's configured folders, and
   record the observation. A copyrighted-derived index syncing off-machine would be a rights
   incident, not an inconvenience.
10. **Tests.** A fake-filesystem test suite covering: preflight refusing a write that would breach
    the floor; postwrite detecting a breach; ceiling warn at 20 GB and hard-stop at 25 GB; verifier
    rejecting a hash mismatch, a `.pt` file, and a pickle-magic file with a `.gguf` extension;
    inventory recording and skipping a reparse point; the AST assertion that the inventory module
    contains no deletion call. All marked so CI's `-m "not requires_model"` filter still runs them
    (they use fixtures, not weights).
11. **Commits:** `feat(epppsynth): add storage roots, read-only inventory and reserve guards (EP-7)`
    then `docs(roadmap): record EP-7 commit hash`.

## Out of scope

- **Any purge, delete, move or cleanup tool.** ADR-007 is rules only. If one is ever built it is a
  `final-roadmap.md` item, and it starts by satisfying all seven rules.
- Downloading any weight, of any size, for any reason — **EP-34** (rubric) and **EP-35** (first
  measured run). D-30's one-at-a-time, individually-confirmed rule applies there, not here.
- Choosing models or embedding models — **EP-34**.
- Building the local index or ingesting the corpus — **EP-22**.
- The benchmark packet schema and the null packet — **EP-32**. EP-7 creates the `benchmarks\`
  directory and nothing that writes into it.
- `llama-cpp-python`, CUDA wheels and the `sm_120` go/no-go — **EP-33**.
- Any change to the pre-existing third-party cache, including deduplication or reorganisation —
  permanently out of scope by D-71.
- Backup or sync configuration on the machine. EP-7 **observes** whether the roots are in sync
  scope; changing that is an owner action, recorded in the completion note if needed.

## Verification / acceptance

Runnable:

```powershell
uv run epppsynth storage check
uv run epppsynth storage inventory            # read-only; writes only to C:\epppmodels\inventory\
uv run pytest epppsynth/tests/test_storage.py -q
Test-Path C:\epppmodels, C:\epppindex
Get-ChildItem C:\epppmodels -Recurse -Directory | Select-Object -ExpandProperty Name
```

Acceptance:

1. `epppsynth storage check` reports free space on the system volume, the current project
   footprint, and both limits, and exits 0 with the footprint at zero.
2. A unit test proves `preflight_space` **refuses** a hypothetical write that would leave less than
   250 GiB free, and a second proves `postwrite_space` raises when a simulated post-write state is
   below the floor.
3. Unit tests prove the ceiling **warns** at a simulated 20 GB footprint and **raises** at 25 GB,
   and that no write path proceeds past the raise.
4. The verifier rejects: a hash-mismatched fixture; a `.pt` file; a file with pickle magic bytes and
   a `.gguf` extension; and a `revision` that is a branch name rather than a 40-hex SHA. Four
   distinct failing tests.
5. `trust_remote_code` exists only as an unconditional `False` constant — asserted by a test that
   greps the package source for any assignment of `True` to it.
6. The inventory run enumerates all four roots (recording absent ones as absent), records the
   reparse-point flag, does not follow reparse points, and writes exactly one JSON file under
   `C:\epppmodels\inventory\`.
7. The pre-existing third-party cache is **unchanged**: file count and total size recorded, and
   every file's mtime identical before and after the run. Recorded in the completion note as
   counts and totals only — no paths, no filenames.
8. **No deletion code path exists.** The AST test over `epppsynth/src/epppsynth/storage/` finds no
   call to `os.remove`, `os.unlink`, `Path.unlink`, `Path.rmdir`, `shutil.rmtree`, `shutil.move`,
   or any Recycle-Bin helper. This test is the acceptance evidence that EP-7 built no purge tool.
9. `ADR-007` lists **all seven** rules, numbered, with `Status: accepted — no implementation
   exists`. `ADR-009` records both roots, both limits, the before-and-after rule, the expected
   8–12 GB usage, the deliberate GiB/GB transcription, and the D-71 exclusion.
10. Both root directories exist with the specified subtrees, and `epppsynth/docs/adr/ADR-007.md`
    and `ADR-009.md` are no longer stubs.
11. The cloud-sync observation (step 9) is recorded with its result.
12. `uv run epppsynth scan` (EP-6) is green — in particular the root scanner confirms that
    `C:\epppmodels` and `C:\epppindex` appear only in documentation and in the single allowlisted
    constants module, never in a fixture or a default value.
13. CI green, and no CI job references either root.

## Parked → final-roadmap.md

- A cache-purge tool implementing ADR-007. Explicitly parked, not forgotten: the rules exist so
  that if the owner ever needs the space back, the work starts from a specification.
- Deduplicating or reorganising the pre-existing third-party cache. Out of scope by D-71 and likely
  to stay so.
- A backup-exclusion configuration for `C:\epppindex`. The separate root exists precisely to make
  this easy; performing it is an owner machine action, not project code.
- Automated re-inventory on a schedule, and drift detection against `models.lock.json`. Useful once
  weights actually exist; revisit at the P4 re-plan.
- Hard-linking or reusing a verified weight from the third-party cache into `C:\epppmodels` rather
  than re-downloading. Attractive for the ceiling, but it makes the project's footprint depend on a
  directory the project does not own; needs an owner decision.

---

> **Completion note (2026-09-01).**
>
> All thirteen acceptance criteria met. `uv run ruff check`, `ruff format --check` and
> `pytest -m "not requires_index and not requires_model"` are green (**191 passed**, 43 of them new
> in `epppsynth/tests/test_storage.py`), `uv run epppsynth scan --history` is green across all nine
> checks plus the self-check, and `uv sync --locked` resolves unchanged.
>
> **What was observed on the real machine**, as counts and totals only (D-3):
>
> | | |
> |---|---|
> | Free on the system volume at the run | 391.8 GiB — 141.8 GiB of headroom above the 250 GiB floor |
> | Pre-existing third-party cache, before | **8 files, 98,707,247,360 bytes (91.93 GiB)** |
> | Pre-existing third-party cache, after | **identical** — same file count, same total, and every file's mtime unchanged, compared row by row |
> | Second third-party root | present and **empty** (0 files) |
> | Third third-party root | **absent**, recorded as absent rather than as an error |
> | Reparse points encountered in the real roots | **0**; the record-and-skip path is proved by a unit test that creates a real junction |
> | Project footprint after the run | 4,192 bytes — the one inventory JSON, and nothing else |
> | Inventory files written | exactly **1**, under the model root's `inventory/` subtree, outside the repository |
>
> `epppsynth storage check` was run **before** the roots existed (footprint 0, exit 0 — acceptance 1)
> and again after (both roots present with all four subtrees, lockfile absent, exit 0).
>
> **Cloud-sync observation (step 9, WS2-A5).** Checked before anything was written. Two sync scopes
> exist on this machine: one provider mounts a separate drive letter, and one provider's folder sits
> under the user profile. No known-folder redirection is configured and no mirrored-folder entry
> covers the system volume's root. **Neither root falls under any sync scope** — both sit directly
> under the system volume's root. Recorded in `ADR-009` under *Observations*. No machine
> configuration was changed; a backup exclusion for the index root remains an owner action and stays
> parked.
>
> **Deviations, and why.**
>
> 1. **The inventory module does not write its own output.** §2 asks it to emit JSON to
>    `C:\epppmodels\inventory\`, and the safety-preconditions table forbids it any write path *into
>    any scanned root* — and the model root **is** one of the four scanned roots. Both hold only if
>    the emit lives elsewhere: `inventory.collect()` returns a report and `layout.write_json()`
>    writes it through the package's single guarded write path. That is what lets the AST test assert
>    the read-only claim structurally rather than by care.
> 2. **The reparse-point-aware walk lives in `limits.py`, not `inventory.py`.** `project_footprint()`
>    needs the same walk, and putting it in `inventory` would have made the module that guards writes
>    import the module that must never write. The arrow points away from the read-only module
>    instead.
> 3. **`ADR-008` gained an amendment and EP-6's allowlist a fourth entry.** The brief requires the
>    roots to be read from "a module constant that EP-6 explicitly allowlists by symbol"; that
>    allowlist did not exist, so EP-7 created it — two symbols, one module, by exact path, with the
>    scan summary printing both skips on every run. The alternative that needs no exemption —
>    building the root from `%SystemDrive%` plus a fragment — was rejected in the ADR: it passes the
>    scanner *and* blinds it to every future module that does the same, trading a visible hole for an
>    invisible one. The OD-10 exemption table is untouched and still has three entries.
> 4. **The roots are created by `storage inventory`, not by `storage check`.** §5 names two
>    subcommands and describes `check` as reporting; creating directories is a side effect a
>    reporting command should not have. `check` reports an absent root and names the command that
>    creates it.
> 5. **The AST deletion test is name-based and deliberately over-strict.** It cannot tell `os.remove`
>    from any other object's `.remove`, and that is the point: a package that must never delete
>    anything can afford never to write the word. The banned set also covers `rename` and
>    `send2trash`, which the brief's list does not name.
> 6. **`guarded_write` opens with `xb`.** Overwriting is a deletion with a friendlier name, so the
>    one write path refuses it.
>
> **Pre-publication checklist items re-run.** Item 4 (local paths and machine identity) — the
> `identity` and `roots` checks are green, and the two root literals appear in exactly two places in
> tracked code, both inventoried in the scan summary. Item 6 (licence conformance) — the `rights`
> check is green, and `METADATA.json` carries `licence_id` and `licence_url` as required fields, so a
> weight whose licence nobody recorded cannot enter the lockfile. Nothing from the real inventory run
> is committed.
>
> **Nothing was deleted, moved or renamed**, on this machine or in this repository. `ADR-007` ships
> `Status: accepted — no implementation exists`, and
> `test_the_storage_package_contains_no_deletion_call` is the evidence for that line.
>
> **For the P0 re-plan (EP-8):** the deliberate GiB/GB transcription (floor binary, ceiling decimal)
> is recorded in `ADR-009` and asserted by a unit test; flagging it, as §1 requires. Deciding whether
> to normalise the units would be an owner decision, not a code change.
