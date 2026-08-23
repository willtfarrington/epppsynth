# EP-33 — Runtime spike — GPU architecture go/no-go

**Size:** L · **Mode:** n/a (spike) · **Core/Stretch:** core ·
**Depends on:** EP-32 (benchmark packet schema and null packet) ·
**Blocks:** EP-34 (model and embedding rubric)

> **Charter.** **EP-31 (paired-preference harness, re-plan P3)** upgrades this to a full brief — but
> this spike's *result* is what the P4 re-plan (EP-37) mostly exists to absorb, so expect EP-37 to
> revise this brief after the go/no-go.

## Context

**This is the highest-uncertainty brief in the plan.** D-70 fixes the runtime as `llama-cpp-python`:
MIT, in-process, no daemon, no listener, an official Windows CUDA wheel index, and in-process
GBNF / JSON-schema constrained decoding. The alternative was rejected because it auto-downloads
updates on Windows and registers a background login-start service — both fatal to the no-runtime-
network rule (D-8) and to the no-egress release-gate item (D-35(4)).

The unknown is narrow and decisive: **the prebuilt CUDA wheel's coverage of the target GPU's compute
capability is undocumented and unverified.** The target is a current-generation NVIDIA laptop
discrete GPU in the 8 GB-VRAM class on Windows x64; if the prebuilt wheel ships no kernels for its
architecture, the GPU path is simply unavailable. Step 1 of this brief is therefore a **go/no-go**,
and everything downstream in P4 is conditional on it.

**Documented fallbacks, in order:** (1) the CPU-only wheel, measured as its own packet row and
possibly sufficient for a reflection aid that is not latency-critical; (2) the upstream prebuilt
`llama-server` binary — a documented fallback **only**, because it reintroduces a second local HTTP
listener and therefore a second trust boundary at exactly the point the loopback trust boundary is widest (D-70);
(3) a source build is **not** available — the required native toolchain is absent from the machine
and installing it is out of scope for v1.

## Safety preconditions

- No daemon, no listener, no background service, no auto-update; the wheel is pinned by version and
  hash in the lockfile so the runtime cannot drift under a measured packet (R-20, D-70).
- Any weight file used for the spike is **acquisition 1 of the three** in EP-32's model-acquisition
  budget — the spike weight, ≤ ~5 GB — individually confirmed, one at a time, with the storage
  floor and project ceiling checked before and after (D-30, D-78), and verified by revision plus
  file hash, GGUF only, no pickle formats, remote code execution disabled (D-31, D-44). It is not
  "the one download": EP-32 states the full budget and this brief spends one line of it.
- The spike may reach the network **once**, for that confirmed download. After it, the runtime is
  offline; no auto-download path may remain enabled.
- Nothing identifying the machine reaches a public artifact: the raw packet is local-private and only
  the generalized summary is published (EP-32).
- If the fallback listener is ever used, it is recorded as an explicit exception with its trust-boundary cost,
  never adopted silently.

## Scope sketch (refine at re-plan)

1. **Go/no-go.** Install the pinned prebuilt CUDA wheel into the project environment; load a small
   GGUF at full offload; confirm the GPU is actually engaged (non-zero VRAM in use). Record the
   answer either way.
2. On **no-go**: measure the CPU-only wheel path, record it as a packet row, and write the fallback
   decision — CPU-only or the listener binary — as an ADR addendum with its trade-off.
3. Confirm GBNF / JSON-schema constrained output round-trips in-process and produces a schema-valid
   object; a runtime that cannot constrain output is not usable under D-54/D-55 regardless of speed.
4. Record everything into an EP-32 packet, including the storage preflight results.
5. Write the ADR addendum recording the go/no-go, the evidence for it, and the chosen path.
6. Verify `uv sync --locked` reproduces the pinned wheel and that CI's no-model path is unaffected.

## Verification / acceptance (sketch)

- A packet exists showing either non-zero VRAM at full offload **or** a written no-go with the
  fallback named and its own measured row.
- A schema-valid constrained output is captured in the packet.
- The ADR addendum is committed and dated, and `DECISIONS.md` carries a dated addendum if the
  fallback changes anything D-70 stated.
- `uv sync --locked` reproduces the environment; the wheel's version and hash are in the lockfile.
- A check confirms no service, scheduled task, listening socket or auto-update path was created.
- *(judgement — author)* the go/no-go answer is unambiguous; "it seemed to work" is not an answer.

## Parked → final-roadmap.md

- Source-building the runtime once a native toolchain exists.
- Re-measuring on a different GPU class, and any multi-GPU or iGPU offload path.
