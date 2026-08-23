# epppsynth — Extension roadmap (parked)

Everything deliberately **not** built in v1. Seeded 2026-08-23 from the planning session; each phase's
re-plan EP mirrors its briefs' `## Parked → final-roadmap.md` sections into this file.

Nothing here is a commitment. Items marked **excluded** are not "later" — they are governed by
[`../epppsynth/GOVERNANCE.md`](../epppsynth/GOVERNANCE.md) §9 and require external accountable parties
this project does not have.

## v1.x — plausible next increments

| Item | Why it is not in v1 | Prerequisite |
|---|---|---|
| Scenario library in the interface | v1 needs fictional scenarios for *evaluation*, not for the reader to browse; the two are different artifacts | EP-25 … EP-27 complete |
| Trainee-controlled opt-in local retention (mode b) | v1's non-surveillance guarantee is easier to keep absolute; opt-in retention needs a control surface the trainee fully owns | mode (b) gate |
| Export or sharing of output | v1 keeps output on screen and unexportable, which removes a whole class of leakage and chart-contamination hazards | an explicit decision plus a rights review of exported citations |
| Best-effort third-party installability | v1 is a personal tool with public source; installability is a support burden and an implied claim | a clean non-admin install from a path with spaces and non-ASCII characters, as an acceptance test |
| Local-only source pane | span display is safe only behind a double gate; the double gate is the work | EP-45, plus the index from EP-22 |
| A second escalation-resource locale | the shipped defaults are US and are labelled as such | verification of each number against its issuing authority |

## v2 and beyond

| Item | Why it is not in v1 |
|---|---|
| Generalised corpus ingest beyond the current single-source spine | the ingest module is authoring tooling, not the product; generalising it buys nothing until a second source is lawfully available and rights-cleared |
| Additional conceptual traditions inside the declared scope | breadth without review capacity is how a content model accretes unprovenanced concepts (R-13) |
| Fine-tuning of any model | gated behind measured baseline failure, lawful training data, governance, and an evaluation the project does not yet have |
| Retrieval over the local index on the emission path | would make output non-reproducible and reopen the rights boundary at exactly the wrong place; the index serves authoring and the source pane only |
| A packaged installer | implies a supported product |
| Any multi-user, hosted, or LAN-exposed deployment | a separate threat model and a separate release class |

## Excluded — not deferred

Governed by `GOVERNANCE.md` §9. Patient-specific point-of-care use · patient- or family-facing use ·
PHI processing · EHR integration · autonomous action · therapeutic use of any kind. The author will
not attempt these as a solo project. The seven preconditions each name an external accountable party.

**Non-Western and non-secular conceptual frameworks** are out of scope by decision, not by backlog.
The mitigation is an explicit scope label plus tested abstention. Adding them would require
compensated co-design with the communities concerned and qualified review — doing it badly is worse
than not doing it, and pretending the backlog will fix it is worse still.

## De-scoped during planning

- **"Hidden Dynamic / Empathic Wedge / Bridge"** as an output model. Retired. Three of the functions
  worth keeping — naming plausible unspoken concerns, suggesting an opening move, and naming the
  clinician's own reaction — survive in the three-part contract, reframed so that concerns are plural
  hypotheses with counter-readings and every suggested utterance is a question or an offer rather than
  a lever. The fourth, connecting values to options, was withdrawn with the contract's fourth part
  (see below).
- **The output contract's fourth part** — "neutral framing connecting stated values to
  clinician-verified options". Deleted, not deferred. It had no input field, no record type and no
  owning brief, so it would have shipped permanently empty while making the evaluation's substance
  tuple carry a constant. Restoring it would require all three of: an input field carrying the options
  as the clinician states them, a completeness invariant (each entered option appears exactly once,
  unranked, none added, none omitted, checked mechanically), and evidence that the part is worth the
  coercion surface it opens. Absent all three, the tool says nothing about clinical options at all.
- **A formal ontology (OWL/RDF) with a reasoner.** Buys inference the product does not need and
  imports an authority claim it must avoid.
- **Ollama as the local runtime.** Auto-downloads updates on Windows and registers a background
  service; both are incompatible with a verifiable no-runtime-network claim.
- **LLM-as-judge evaluation scoring.** Would collapse the independence of the deterministic control
  arm and add an unauditable dependency inside an offline boundary.
- **A widget-framework interface.** Rejected on architectural control: the output contract's semantics
  and the accessibility gate both require owning the markup. Recorded with the caveat that no
  accessibility claim was verified about the alternative.
- **A cache-purge tool.** The seven safety rules are written; the tool is not built, because nothing
  currently needs it.
