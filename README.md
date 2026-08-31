# epppsynth

**existential perspectives for physicians & patients**

```
status: design
```

Design and planning artifact — v1 in progress; no release, no demo, no validation.

## What this is

`epppsynth` is the **design for** a local, offline-capable reflection aid: given a few explicitly
supplied, structured facts about a fictional clinical encounter and a stated purpose, it is intended
to produce three to five concise waypoints — what is known and unknown, plural possible concerns each
carrying a counter-reading and an insufficient-basis clause, and disconfirming questions a clinician
might ask. Nothing here runs yet: this repository currently holds a roadmap, the governance and
design documents, and an empty package skeleton. It is built for its author's private local use; the
repository is public as a source and portfolio artifact, and public source availability is not
evidence of efficacy, safety, approval, or suitability.

## Intended use, in short

For a clinician or trainee, on **manifestly fictional scenarios only**, away from the point of care,
as preparation for thinking — never during an encounter, never with real patient information, and
never to make, support, justify, or document a clinical decision. The sole accountable human is the
person operating it.

**This tool is not a risk detector and must not be used as one.** It never checks what is typed for
danger.

The full four-block text — Intended use / Excluded uses / What it does not know / Status — is in
[`SAFETY.md`](SAFETY.md), the clinical-ethics charter, together with the invariants, the abstention
taxonomy, the deterministic hard-stop rule, the published banned-phrase list, and the stop criterion
that would end this project. [`epppsynth/GOVERNANCE.md`](epppsynth/GOVERNANCE.md) §2 and §3 remain
the binding statement where the two differ.

## Modes

One engine, three purpose profiles, built (a) → (b) → (c). Each mode carries its own evaluation set
and its own release gate, so a failing mode is withheld without blocking the others.

| Mode | Purpose | Status | Badge |
|---|---|---|---|
| (a) | clinician pre-encounter reflection on fictional scenarios | not started | `status: design` |
| (b) | trainee education and reflection, strictly local and non-surveilling | not started | `status: design` |
| (c) | clinician self-reflection on the structural and existential dimensions of a clinical experience | not started | `status: design` |

Patient-specific point-of-care use and patient- or family-facing use are **excluded release
classes**, with named preconditions rather than a schedule — see
[`epppsynth/GOVERNANCE.md`](epppsynth/GOVERNANCE.md) §9.

## Maturity badge

The badge above is a plain-text string, not an image: a shield would be a network fetch on a page
the project does not control. It is a claim about **evidence**, not about effort, and CI resolves it
to an evidence file whose checklist must be fully ticked (*checker planned — EP-6*).

| Badge string | Meaning | Earned when | Evidence file |
|---|---|---|---|
| `status: design` | design and planning artifact | roadmap and canonical docs exist; no engine exists | [`epppsynth/docs/evidence/design.md`](epppsynth/docs/evidence/design.md) |
| `status: skeleton` | runs; not evaluated | the deterministic engine and CLI run end-to-end on fixtures | `epppsynth/docs/evidence/skeleton.md` |
| `status: self-evaluated — mode (x)` | mode (x) evaluated **by this project's own suites**, not by any external body | all eight release-gate items satisfied for mode (x) | `epppsynth/docs/evidence/mode-x-gate.md` |
| `status: v1 — mode (x)` | v1 tagged for mode (x) | the row above, plus a cut tag and a recorded IP-clearance checkpoint | `epppsynth/docs/evidence/mode-x-release.md` |

The third rung reads **`self-evaluated`**, not `evaluated`. Every suite behind it is written and run
by this project; a bare "evaluated" would read as external validation, and none exists.

**Parse contract**, fixed here so the CI checker has something exact to implement: the badge is a
single line inside a fenced block in this file matching

```
^status: (design|skeleton|self-evaluated — mode \([abc]\)|v1 — mode \([abc]\))$
```

and the checker maps it to its evidence path by the table above, failing if the file is missing or
any box in it is unticked.

## What the evidence supports

**No evidence of benefit exists for this tool or for its class.** The closest analogues are
null-to-adverse: a randomized trial of simulation-based serious-illness communication training found
no improvement in patient- or family-reported communication quality **and a significant increase in
patient depressive symptoms**; the flagship structured-guide trial was null on both coprimary patient
outcomes and positive only on process measures. No study of this intervention class exists at all.

The defensible analogue is therefore a **question-generation aid** — a thing demonstrated to change
what gets asked, not to change outcomes. The project's own success criterion is a measure of
**feasibility and acceptability**, and never of effectiveness. Nothing here should be read as
implying that communication preparation is inherently benign.

## Review status

**Author review only.** No clinician, educator, patient, ethicist, or accessibility reviewer has
reviewed this project. Recruited, role-identified reviewers become the release gate for mode (a)
only — a clinician in serious-illness care, a clinician-educator, and a person with lived experience
of serious illness — recruited once an engine runs end-to-end (*planned — EP-37, EP-52*). Modes (b)
and (c) will ship carrying a public "author review only" label.

## Reading paths

- **Anyone deciding whether this may be used, and on what** — [`SAFETY.md`](SAFETY.md), the
  clinical-ethics charter: intended and excluded uses, what the tool does not know, what it refuses
  to do, and what would make the author stop building it.
- **Clinical or non-technical reader** — a plain-language narrative, `epppsynth/docs/for-clinical-readers.md`, *planned — EP-53*.
- **Engineer** — [`epppsynth/DESIGN.md`](epppsynth/DESIGN.md) for the technical design, [`epppsynth/GOVERNANCE.md`](epppsynth/GOVERNANCE.md) for the invariants that override it, and [`epppsynth/DECISIONS.md`](epppsynth/DECISIONS.md) for why each choice was made.
- **Anyone executing a roadmap brief** — [`CLAUDE.md`](CLAUDE.md), then the load order it names.
- **Roadmap** — [`roadmap/README.md`](roadmap/README.md).

## Licence

*Placed by EP-5.* The split is Apache-2.0 for code and CC BY 4.0 for the content model, ontology and
documentation, REUSE-conformant, with `NOTICE` and a generated per-source rights table.

## Citation

*Placed by EP-5,* as `CITATION.cff`. Its `abstract` and any status text it carries must match this
file's expansion and status line character for character.

## Contributing

**No pull requests in v1.** Issues are open for discussion only — not support, and never clinical
advice. Security and safety concerns go through the repository's private vulnerability reporting.
Third-party deployment is not an intended use. Expanded by `CONTRIBUTING.md`, `SECURITY.md`,
`CODE_OF_CONDUCT.md` and `PRIVACY.md`, *planned — EP-4*.
