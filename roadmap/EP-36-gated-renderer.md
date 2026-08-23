# EP-36 — Gated LLM renderer, claim binding, baseline comparison

**Size:** L · **Mode:** a · **Core/Stretch:** core ·
**Depends on:** EP-21 (composition, linters, CLI), EP-35 (first measured run), EP-31 (paired
preference) ·
**Blocks:** EP-37 (reviewer recruitment pack, re-plan P4)

> **Charter.** **EP-31 (paired-preference harness, re-plan P3)** upgrades this to a full brief. The
> drop-rate threshold and wall-clock deadline below arrive from EP-35's measurements.

## Context

Implements D-17's gated path and D-54's rule that **the LLM is a renderer, not an author**. It
receives selected concept IDs, their authored paraphrases, and the user's quoted text — never the
registry wholesale, never the corpus index, never a raw span. Output is constrained by a JSON schema
compiled to a grammar, with every prose leaf sitting beside a required concept ID.

The dependency on EP-31 is the reason this brief sits at the end of P4 rather than the start: "beats
the baseline" is only meaningful against P3's suites, and the stop criterion must exist as a runnable
test before a path that could trip it is switched on at all. If the criterion trips on this arm, the
halt procedure in `GOVERNANCE.md` governs — the ladder's second rung is precisely "disable the LLM
path and fall back to the deterministic baseline", which this brief must make a one-flag operation.

The flag defaults **off**. Shipping is not the default outcome: if the arm does not beat the baseline,
leaving the flag off is a **pass**, not a failure, and the finding is published.

## Safety preconditions

- **D-54 boundary, tested:** a test proves the renderer never receives a registry object, an index
  path, or a verbatim span (D-23).
- **Output-side structural validation is the primary prompt-injection control** (D-55), not prompt
  phrasing: schema validation, citation resolution to a live registry ID, and a question-or-offer
  parse on every suggested utterance (D-26b). Anything failing is discarded and the tool abstains.
- Claim binding: every emitted sentence binds to a candidate concept ID; unbound sentences are
  dropped; past the drop threshold the whole response falls back to templates.
- The free-text field is passed inside a clearly marked quotation region and treated as data.
- Same abstention chain, same output type, same escalation panel — byte-identical on every response
  (D-57). No numeric confidence, no ranking, no probability language (D-26c).
- **D-56:** no public text calls this path deterministic; the version triple and the model identity
  are stamped in every bundle so any output can be traced to what produced it.

## Scope sketch (refine at re-plan)

1. Feature flag, default off, switchable in one place, with the off path proven to load no runtime.
2. Constrained render over selected concept IDs and authored paraphrases only; schema-to-grammar
   compilation; wall-clock deadline and cancellation from EP-35.
3. Claim-binding validator plus the drop-rate threshold and its template fallback.
4. Stamp the version triple, model repo/revision/hash and sampling parameters into the bundle.
5. Run the **full P3 suite set on both arms** — conceptual fidelity, uncertainty, coercion,
   counterfactual equity, abstention, hard-stop — and the paired-preference harness on the LLM arm.
6. Write the comparison report: per-suite, per-arm, with Wilson lower bounds and the multi-run
   variance figures; state plainly whether the arm beats the baseline.
7. If a stop-criterion trigger fires, execute EP-31's halt procedure rather than iterating quietly.

## Verification / acceptance (sketch)

- An injected unbound sentence is dropped; an over-threshold response falls back to templates.
- A test proves the renderer never receives a registry object or an index path.
- With the flag off, no runtime is imported and no model file is opened.
- Both arms complete the P3 suites and the comparison report exists in the evidence bundle.
- The hard-stop suite passes at 100 % on the LLM arm; the escalation panel hash is unchanged.
- *(judgement — author, then reviewers)* the rendered prose says nothing the concept IDs did not
  license.

## Parked → final-roadmap.md

- A standalone published LLM-vs-baseline comparison write-up (stretch).
- Any retrieval or similarity search on the emission path — rejected for v1; the index serves
  authoring and the source pane only.
