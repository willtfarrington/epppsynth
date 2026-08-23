# EP-50 — Release-gate evidence bundle and CI enforcement

**Size:** L · **Mode:** a · **Core/Stretch:** core ·
**Depends on:** EP-46 (verification and re-plan P5) ·
**Blocks:** EP-52 (mode (a) gate assembly)

> **Charter.** Scope and acceptance below are sketches. **EP-49** (per-mode eval sets, author-review
> labels, re-plan P6) upgrades this to a full brief: `## Scope sketch` splits into `## In scope` /
> `## Out of scope`, and each criterion becomes a named command or artifact. Do not execute from the
> sketch alone.

## Context

Builds the evidence machinery **before** the gate is assembled, so EP-52 is a check rather than a
construction. What "done" means for v1 is not feature completion but evidence: the `v1 — mode (a)`
tag is cut only when the **eight** gate items are satisfied and their artifacts exist in
`release-evidence/<tag>/`.

Eight, not seven: D-35 shipped with seven and the omission was recorded afterwards; **accessibility is the
eighth item** (D-67), with EP-46's packet as its artifact.

Everything lands under `release-evidence/<tag>/` beneath a `MANIFEST.sha256`. A CI release job
asserts that every required file exists, that the manifest verifies, and that **the recorded build
hash equals the tagged commit** — the tag cannot be created otherwise. That last equality is the
whole point of R-30: a gate that passes against a build other than the one tagged is not a gate.

The **maturity badge is a static README string** that CI resolves to an evidence file and **refuses
to upgrade without it** (D-59). Without the mechanical tie, a badge "tied to evidence" is
indistinguishable from one tied to effort under hiring pressure (R-9).

## Safety preconditions

- **R-30.** Build-hash equality is asserted, never eyeballed; a mismatch is a hard CI failure with no
  override flag.
- **R-9 / R-32.** No evidence file may contain a claim the artifact beneath it does not support, and
  the bundle's README states what each item does *not* establish.
- **D-37 / R-9.** If a stop-criterion trigger ever fires, **the halt and its resolution appear in the
  public README**. A halt that is not visible is itself an overclaim, so the bundle carries the slot
  for it whether or not one has fired.
- **Public artifact (D-3).** Checklist items 1 (secrets), 2 (PHI in any bundled report), 4 (the
  benchmark packet ships a **generalized** machine description — never a hostname, username or exact
  hardware build) and 7 (public claims).

## Scope sketch (refine at re-plan)

1. `release-evidence/<tag>/` layout and `MANIFEST.sha256`; a generator that assembles the bundle from
   the artifacts each phase already produces.
2. The eight items, each with its mechanical check, artifact and signer: (1) eval suites against
   thresholds with the held-out usage ledger; (2) at least two reviewer sign-offs by role; (3) the
   benchmark packet; (4) threat model plus verified loopback controls plus the two-layer no-egress
   evidence; (5) public-safety scan; (6) employment/IP clearance (D-29); (7) docs stating review
   status and limitations; (8) **accessibility packet** (D-67).
3. The CI release job: existence, manifest verification, build-hash equality, badge-to-evidence
   resolution.
4. The stop-criterion disclosure slot in the public README and in the bundle.
5. A generalized public summary of the benchmark packet, derived from the private measurements.

## Verification / acceptance (sketch)

- Four deliberate red runs recorded in the completion note: a missing artifact; a corrupted manifest;
  a build hash that does not match the tag; a badge upgraded without its evidence file.
- The bundle generator is reproducible — running it twice on the same build produces the same
  manifest.
- A scripted check that every one of the eight items resolves to a file that actually exists.
- No local user-profile path, hostname or username anywhere in the bundle (leak scanner).

## Parked → final-roadmap.md

- Signed tags, provenance attestation, or SBOM publication beyond the per-candidate CycloneDX file.
- Per-mode release bundles for modes (b) and (c) (their gates are EP-49's).
