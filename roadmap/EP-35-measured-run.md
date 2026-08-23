# EP-35 — First measured run, degradation and cancellation ladders

**Size:** L · **Mode:** n/a (measurement) · **Core/Stretch:** core ·
**Depends on:** EP-34 (model and embedding selection rubric) ·
**Blocks:** EP-36 (gated LLM renderer), EP-37 (reviewer recruitment pack, re-plan P4)

> **Charter.** **EP-31 (paired-preference harness, re-plan P3)** upgrades this to a full brief. The
> measurement grid below is the sketch; the exact context and offload rows are fixed against what
> EP-33 finds.

> **Over-scoped for one L session — natural split seam.** Acquisition plus the measurement grid
> (scope 1–2) is one session; the degradation and cancellation ladders (scope 3 onward) is another.
> The seam is clean because the ladders are behaviour under failure, not measurement, and they need
> only the packet the first half produces. Split at pickup if the first half runs long.

## Context

Implements D-35(3) end to end: the first complete benchmark packet, plus the two ladders that decide
what the tool does when inference cannot deliver. Quality **thresholds** are not set here — P3 owns
them (D-17: the model ships only if it beats the baseline on the eval suites). This brief produces
the measured behaviour those thresholds will be applied to.

Two ladders. **Degradation:** full offload → partial offload → CPU-only → the deterministic baseline,
which is the permanent fallback (D-17). **Cancellation:** a per-token callback plus a per-request
wall-clock deadline, because a hang is not merely a performance problem — the clinician is waiting
mid-workflow, which makes it a clinical hazard. D-75 leaves the wall-clock deadline and the
claim-binding drop threshold to be set here against measured behaviour; record both as dated
addenda rather than as edits.

Every row lands in an EP-32 packet: cold and warm, p50 and p95 latency and throughput, peak RAM,
VRAM and disk, sampling parameters and seeds, and the full version identity — **including a CPU-only
row**, which is also the fallback evidence if EP-33 returned a no-go.

## Safety preconditions

- Storage floor (≥ 250 GiB free) and project ceiling (25 GB, warn at 20 GB) checked before **and**
  after the download and again at run start; recorded in the packet (D-78).
- This brief performs **acquisitions 2 and 3** of EP-32's model-acquisition budget — the measured
  generation weight (≤ ~8 GB, D-30) and the embedding model for the authoring-side index (≤ ~1 GB,
  D-44). They are two separate, individually confirmed acquisitions, not one; each is verified by
  revision and file hash, GGUF only, no pickle, remote code execution disabled (D-31), and each is
  bracketed by the floor and ceiling checks. Together with EP-33's spike weight they must stay
  inside the 25 GB project ceiling; if they will not, a superseded weight is deleted first and the
  deletion recorded in the packet.
- **No retention** (D-8): packets and logs carry metrics and version identity — never a prompt, a
  response body, or case text.
- **D-56:** the packet records greedy decoding with a fixed seed as a best-effort reproducibility
  setting; no artifact calls this path deterministic.
- The runtime stays in-process with no listener and no auto-update; a runtime version change
  invalidates the packet and forces a re-run (R-20).
- The degradation ladder must end at the deterministic baseline, never at an error page or a blank
  result: the baseline is the shipped default and the permanent fallback.

## Scope sketch (refine at re-plan)

1. Perform acquisitions 2 and 3 from EP-32's budget — each separately confirmed; verify hash and
   revision for each; write the metadata and lock entries for both.
2. Measurement grid: cold and warm × three context sizes × full / partial / zero offload, plus the
   CPU-only row; p50 and p95 for latency and throughput; peak RAM, VRAM and disk per row.
3. Implement the per-token cancellation callback and the per-request wall-clock deadline; measure
   how long cancellation actually takes, not just that it works.
4. Implement the degradation ladder and prove each rung, including a **forced-OOM** test that walks
   the whole ladder and lands on the deterministic baseline.
5. Missing-model and corrupt-model tests: the verifier refuses, the app falls back, nothing crashes.
6. Propose the wall-clock deadline and the claim-binding drop threshold from the measurements, for
   EP-36 to consume; record both as dated addenda.
7. Emit the complete packet and its generalized public summary.

## Verification / acceptance (sketch)

- A packet with **every** required field populated across all rows, including the CPU-only row.
- A log showing the OOM ladder stepping down rung by rung and landing on the deterministic baseline.
- Cancellation returns within the recorded deadline in a test, and the partial response is discarded.
- A corrupt-model fixture is refused by the verifier; a missing model falls back without an exception.
- Storage floor and ceiling assertions appear in the packet before and after the download.
- The public summary passes the leak scanners.

## Parked → final-roadmap.md

- Batch or concurrent inference — v1 is single-flight by design.
- Quantization sweeps beyond the single acquired file, and any second model.
