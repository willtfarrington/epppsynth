# EP-34 — Model and embedding selection rubric (no weights chosen)

**Size:** M · **Mode:** n/a (selection criteria) · **Core/Stretch:** core ·
**Depends on:** EP-33 (runtime spike — GPU architecture go/no-go) ·
**Blocks:** EP-35 (first measured run)

> **Charter.** **EP-31 (paired-preference harness, re-plan P3)** upgrades this to a full brief. The
> criteria list below is the sketch; the re-plan turns it into a scoring sheet with a filled example.

## Context

Implements D-31's rule that **the model list is earned by the benchmark packet, not chosen now**.
This brief writes the rubric and the shortlist procedure, and deliberately **names no weights and
assigns no weights** — no candidate is selected, no numeric criterion weighting is fixed, and nothing
is downloaded. That discipline is the point: a rubric with weights invented before measurement is a
rationalisation of a choice already made.

**Reuse of existing third-party model caches on the machine yields essentially nothing.** The
inventory from EP-7 shows every locally cached candidate either exceeds the VRAM budget for the
target 8 GB-class GPU or sits at a quantization that is not a defensible quality floor for a
safety-sensitive text task. Plan against **EP-32's model-acquisition budget**, which states the
whole of P4's acquisition in one place: three items — the spike weight (EP-33), the measured
generation weight ≤ ~8 GB (EP-35, D-30), and the embedding model for the authoring-side index
(EP-35, D-44) — all inside the 25 GB project ceiling. This brief downloads none of them; it decides
what would qualify. A cached file may be reused only when its computed hash matches a pinned
upstream revision; otherwise it is an unidentified blob and is excluded.

The same hard rules apply to embedding models as to generation models — this is D-44, and it is the
rule most likely to be forgotten because an embedding model does not feel like "a model".

## Safety preconditions

- **Weights are verified by revision plus file hash**; remote code execution disabled; no pickle
  formats; **GGUF only**; identical rules for embedding models (D-31, D-44).
- Downloads are **one at a time, individually confirmed**, each preceded and followed by the storage
  floor (≥ 250 GiB free) and project-ceiling (25 GB, warn at 20 GB) checks (D-30, D-78).
- Model **licences carry field-of-use clauses an SBOM scanner cannot see** — licence screening is a
  named rubric criterion with a written finding per candidate, not an afterthought (D-28).
- Models live in the project model root, **never** in Git or LFS.
- Nothing is downloaded during this brief; the model root must be byte-identical at the end of it.

## Scope sketch (refine at re-plan)

1. Write the rubric as a checklist of **pass/fail gates** plus recorded observations — no scores, no
   weights:
   - licence permits this use, with no conflicting field-of-use clause (written finding);
   - GGUF available at a **pinned revision** with a verifiable file hash;
   - weight file fits the VRAM budget at the target context, or an explicit measured partial-offload
     case is declared;
   - native context sufficient for the composed prompt with headroom;
   - behaves under GBNF / JSON-schema constrained decoding (evidenced by EP-33's finding);
   - no remote code, no pickle formats.
2. Embedding-model addendum: retrieval quality evidence, dimensionality against index size and the
   project storage ceiling, licence, plus every rule above (D-44).
3. The **shortlist procedure**: how candidates are found, how a finding is recorded, who confirms the
   download, and what disqualifies a candidate outright.
4. The `models.lock.json` / per-file metadata entry each accepted candidate must produce, wired to
   EP-7's verifier.
5. Score three candidates **on paper**, without downloading, as a dry run of the procedure.

## Verification / acceptance (sketch)

- The rubric is committed and contains no model name as a recommendation and no criterion weighting.
- Three candidates are recorded with a pass/fail per gate and a written licence finding each.
- The scoring sheet refuses a candidate lacking a pinned revision or a verifiable hash.
- Zero new bytes under the project model root at the end of the brief.
- The embedding-model section repeats every hard rule explicitly rather than by cross-reference.
- *(judgement — author)* a reader could apply the rubric to a candidate this brief never saw and
  reach the same disposition.

## Parked → final-roadmap.md

- Re-screening candidates as new releases appear; the rubric is written to outlive any candidate.
- A quantization-quality comparison across formats — deferred until a measured baseline exists.
