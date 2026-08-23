# EP-46 — No-retention and no-egress harness, accessibility packet, re-plan P5

**Size:** L · **Mode:** a · **Core/Stretch:** core ·
**Depends on:** EP-40 (app shell), EP-41 (loopback controls), EP-42 (input form), EP-43 (waypoints
panel), EP-44 (escalation panel), EP-45 (provenance drawer) ·
**Blocks:** EP-47 (mode (b) trainee profile), EP-50 (release-gate evidence bundle), EP-51
(human-factors protocol and run)

> **Charter.** Scope and acceptance below are sketches; **EP-37** (reviewer recruitment pack,
> re-plan P4) upgrades this brief to full form. This brief is also the P5 re-plan, and per
> `roadmap/README.md` it is the brief that upgrades the P6 charters to full form and re-charters P7.
> Do not execute from the sketch alone.

> **Over-scoped for one L session — natural split seam.** The privacy verification (scope 1–3) and
> the accessibility packet (scope 4–6) are independent bodies of work with different tooling and
> different evidence artifacts; the P5 re-plan (scope 7) rides with whichever half runs last. Split
> at pickup along that seam if needed — both halves must land before EP-47, EP-50 or EP-51 start.

## Context

P5 has so far *asserted* two things the whole privacy posture rests on: that nothing is written, and
that nothing leaves the machine. This brief converts both into evidence, and adds the eighth
release-gate item.

**Verification, not assertion.** A **filesystem-delta harness** snapshots the relevant roots before
and after a full session and proves nothing was written. The **no-egress test is two-layer**, and the
distinction matters: an in-process socket guard proves only that the *Python* layer is silent, while
an **outbound firewall block-and-log rule scoped to the interpreter, asserted to have zero entries
over a full inference session**, proves the *native* layer is — a native library can open a socket
the Python guard never sees. Both ship, and the report says which claim each supports.

**Conflict to resolve before this brief runs: the firewall rule needs elevation, and EP-0 states the
project makes no elevated, machine-wide or registry change.** No session may quietly acquire
administrator rights to satisfy an acceptance criterion. Two permitted resolutions, and the brief
must pick one *in writing* rather than drifting into the first that works:
1. **Owner prerequisite (preferred).** The interpreter-scoped outbound block-and-log rule is created
   **once, by the project owner, as a named prerequisite step** recorded in the brief's Definition
   of Ready and in `PRIVACY.md` — rule name, scope, and how to remove it. The session then only
   *reads* the log and asserts zero entries, which needs no elevation. If the rule is absent at
   pickup, the brief is **blocked**, not started, and not downgraded silently.
2. **Documented weaker guarantee.** If the owner does not provision the rule, the native layer is
   verified only by the unprivileged evidence available — in-process socket guard plus a
   per-process connection observation — and the report states plainly that the native-layer claim
   rests on a weaker, per-process observation, not on a kernel-enforced block. The public wording
   must not describe that as "no egress verified".
Under **neither** resolution is the no-egress claim strengthened beyond what was actually run.

**Windows Error Reporting crash dumps are a residual retention channel** (R-18): a full-memory dump
can capture prompt text. It is documented in `PRIVACY.md` and the threat model with what the operator
can do about it — documented, not hidden.

**Accessibility is the eighth release-gate item** (D-67). Automated coverage is roughly half, so the
gate is axe-core **plus** a scripted manual pass: keyboard-only, screen reader, 400 % zoom, high
contrast. Windows Narrator is available on the target machine and NVDA is not installed, so the
public statement names the tool actually used. Public wording is fixed: *"built to WCAG 2.2 AA;
tested by …; not independently audited"* — **never** "compliant" (R-32).

## Safety preconditions

- **R-32.** No conformance claim beyond what was tested; every failure found in the manual pass is
  recorded with its date and result, including the ones not fixed.
- **D-8.** The harnesses themselves retain nothing: no prompt or output text in any log, artifact or
  CI upload.
- **R-33 / R-34.** The packet re-runs the two phase invariants end-to-end — uniform typography inside
  the waypoints region, and the single escalation-panel hash across the whole eval corpus.
- **Public artifact (D-3).** Checklist items 4 (the evidence bundle must carry a generalized machine
  description, never a hostname, username or exact hardware build), 5 (screenshots re-opened and read,
  EXIF stripped) and 7 (public claims).

## Scope sketch (refine at re-plan)

1. Filesystem-delta harness over a full session; report as an evidence artifact.
2. Two-layer no-egress harness: in-process socket guard plus the interpreter-scoped outbound
   block-and-log rule, with the zero-entry assertion over a full inference session; the report
   states the limit of each layer. Record which of the two elevation resolutions above was taken,
   and — if the second — the exact weaker wording used everywhere the claim appears.
3. Document the Windows Error Reporting channel and any browser-side residue (form history, bfcache)
   in `PRIVACY.md`.
4. axe-core via Playwright across every page state — empty, filled, results, abstention, hard stop,
   error; committed accessibility-tree snapshots; tab-order capture at 320 / 768 / 1280 CSS px;
   focus-obscured and target-size sweeps; 320 px reflow and text-spacing checks.
5. The scripted manual pass executed once and recorded: keyboard-only, Narrator, 400 % zoom, high
   contrast.
6. Write the honest accessibility statement into `README.md` and `DESIGN.md`; register the eighth
   gate item with EP-50.
7. **Re-plan P5:** retro and timings; mirror every P5 brief's `## Parked →` section into
   `final-roadmap.md`; upgrade EP-47 … EP-49, the P6 charters, to full briefs and re-charter P7;
   rewrite the README status paragraph and badge so a cold session reads something true.

## Verification / acceptance (sketch)

- Filesystem delta empty; **either** the owner-provisioned firewall log shows zero entries for the
  interpreter over a full session, **or** the completion note records resolution 2 and every public
  statement of the claim carries the weaker wording. No acceptance path involves a session
  elevating its own privileges.
- Zero axe violations in all six states; snapshots match committed fixtures; tab order matches the
  committed sequence at all three widths; `scrollWidth <= clientWidth` at 320 px.
- No focusable element intersects any fixed or sticky element.
- *(judgement, owner)* Every manual checklist item recorded with a date and a result, failures
  included; the public statement contains no claim beyond what was tested.

## Parked → final-roadmap.md

- Independent third-party accessibility audit.
- Screen-reader coverage beyond the one tool available on the target machine.
