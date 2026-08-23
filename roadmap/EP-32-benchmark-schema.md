# EP-32 — Benchmark packet schema and null packet

**Size:** M · **Mode:** n/a (measurement) · **Core/Stretch:** core ·
**Depends on:** EP-7 (storage roots, cache inventory, reserve floor & project ceiling) ·
**Blocks:** EP-33 (runtime spike)

> **Charter.** **EP-31 (paired-preference harness, re-plan P3)** upgrades this to a full brief:
> `## Scope sketch` splits into `## In scope` / `## Out of scope`, and each criterion becomes a named
> command or artifact.

## Context

Implements D-35(3). The packet schema exists **before** the spike so the spike's output is a
comparable artifact rather than a note — every later measurement, including the CPU-only fallback and
any re-measurement forced by a runtime version change, lands in the same shape and can be diffed.

Fields the packet must capture: OS and driver versions; runtime version and its bundled inference
library commit; model repo, revision, filename, file hash, quantization; the prompt, registry, schema
and eval versions; `n_ctx`, `n_batch`, offload setting and KV cache type; sampling parameters and
seeds; cold vs warm; a quality score slot (P3 owns the thresholds, not this brief); latency and
throughput at **p50 and p95**; peak RAM, VRAM and disk; and a row for the CPU-only path. Storage
context comes from EP-7: floor **≥ 250 GiB free** on the system volume at all times, project ceiling
**25 GB** across the model and index roots, warned at 20 GB (D-78).

The harness must run with **no model at all** and emit a schema-valid *null packet*, which is what
makes this brief executable before anything has been downloaded and what gives CI's no-model path
(D-42) something to validate against.

**The model-acquisition budget for P4, stated once, here.** Three separate acquisitions — not "the
one download" — each individually confirmed, one at a time, GGUF only, verified by revision plus
file hash (D-30, D-31, D-44), and each preceded *and* followed by the floor and ceiling checks:

| # | Acquisition | Brief | Per-item ceiling |
|---|---|---|---|
| 1 | Spike weight — the smallest credible GGUF that exercises the runtime and constrained decoding | EP-33 | ≤ ~5 GB |
| 2 | Benchmark / candidate generation weight — the shortlisted candidate actually measured | EP-35 | ≤ ~8 GB (D-30) |
| 3 | Embedding model for the authoring-side index | EP-35 (rules set in EP-34) | ≤ ~1 GB |

The three together must sit inside the **25 GB project ceiling** shared with the index root, warned
at 20 GB (D-78) — roughly 14 GB of weights against a 25 GB budget, which leaves the index room but
no room for a fourth. Acquisition 1 may be *reused* as acquisition 2 only if the spike weight is
also the measured candidate, in which case the packet records that reuse explicitly; a superseded
weight is deleted before the next acquisition and the deletion is recorded. Any acquisition beyond
these three is a **new owner decision**, recorded as a dated addendum, not a session's judgement.
EP-33, EP-34 and EP-35 reference this table rather than restating a budget of their own.

## Safety preconditions

- The raw packet is **local-private**: it records host specifics. Only a **generalized** public
  summary is published — a hardware class, not a build, driver revision, serial, hostname, username
  or free-space figure (D-3, D-42, pre-publication checklist).
- The public summary passes the leak scanners: no local paths, no model-root or index-root strings,
  no username (EP-6).
- **D-56:** greedy decoding with a fixed seed is recorded as a *best-effort reproducibility setting*,
  never as determinism. GPU kernels are not bit-deterministic even with a fixed seed, and no public
  text may call the LLM path deterministic.
- No prompt text and no output body enters a packet (D-8). Packets carry metrics and version identity.
- A packet records whether hash re-verification was skipped for a cached weight file, so a shortcut
  can never be invisible in the evidence.

## Scope sketch (refine at re-plan)

1. JSON Schema for the packet with every field above required or explicitly nullable — a missing p95
   or a missing peak-VRAM figure must fail validation, not default to zero.
2. A `benchmark` harness entry point that runs with no model and emits the null packet.
3. Commit the null packet as a fixture and validate it in CI.
4. A public-summary renderer: generalized hardware target, quantization, context, p50/p95, peak
   memory class — and nothing that identifies the machine.
5. Storage assertions wired in from EP-7: the reserve preflight and the project-ceiling check run at
   packet start and are recorded in the packet.
6. A stable packet identity (UTC timestamp + short build hash) and a written naming convention under
   the project model root's benchmark directory.

## Verification / acceptance (sketch)

- The committed null packet validates; a mutated copy missing p95 or peak VRAM fails validation.
- The harness emits the null packet on a machine with no model present, exit 0.
- The public-summary renderer's output passes the leak scanners and contains no build, driver, serial,
  hostname, username or free-space figure.
- A test asserts the packet contains no prompt or output field.
- *(judgement — author)* a reader of two packets can tell exactly what differed between the runs.

## Parked → final-roadmap.md

- Automated packet-to-packet regression alerting across releases.
- Energy or thermal measurement — out of scope for v1.
