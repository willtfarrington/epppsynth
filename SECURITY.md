# SECURITY

How to report a vulnerability, what will happen when you do, and what this project does **not**
claim to defend.

```
status: design
```

Design and planning artifact — v1 in progress; no release, no demo, no validation.

Where this document and [`epppsynth/GOVERNANCE.md`](epppsynth/GOVERNANCE.md) disagree, governance
wins and this document is wrong. Decisions cited as `D-n` are in
[`epppsynth/DECISIONS.md`](epppsynth/DECISIONS.md); work packets cited as `EP-n` are in
[`roadmap/README.md`](roadmap/README.md). The privacy posture, including the residual channels this
project cannot close, is in [`PRIVACY.md`](PRIVACY.md).

---

## Supported versions

**None.**

| Version | Supported |
|---|---|
| — | there is no released version |

No version has been tagged. No release, package, binary, installer, demo, or hosted instance exists.
The badge above reads `status: design`, and it resolves to an evidence file whose checklist has to
be fully ticked before it can move (D-59). Nothing is released, so nothing is under support, and
there is no version whose security you can rely on.

When a tag does exist, the policy is the one in *Incident, rollback and end of support* below:
**only the latest tag is supported.**

## Reporting a vulnerability

Report privately. **Please do not open a public issue** for anything involving a vulnerability, a
safety defect, or a leak.

1. **Preferred — GitHub private vulnerability reporting.** It is enabled on this repository. Use the
   repository's **Security → Advisories → Report a vulnerability** button, which is the
   `/security/advisories/new` path on this repository:
   [report a vulnerability privately](../../security/advisories/new). The report is visible only to
   you and to the maintainer until an advisory is published.
2. **Fallback — email.** If the private advisory form is unavailable to you,
   <william.t.farrington@gmail.com>. This is the project's public contact address and the same one
   in the repository's commit metadata; it is not a monitored security inbox, and the private
   advisory path is strictly better.

Useful things to include, none of them required: what you did, what happened, what you expected,
and the commit hash you were looking at. There is no bug bounty, no reward, and no swag.

**Also report privately, through the same path:** real patient, family, trainee, or employee
material found anywhere in this repository; text reproduced from a copyrighted source beyond the
declared quotation budget; a secret, credential, machine identifier, or local path in the history;
or anything the local index should never have touched. Those are treated as leaks rather than as
bugs, and a leak is more urgent than a vulnerability here.

## Response posture, stated honestly

This is a personal project maintained by **one unpaid person**, alongside clinical work.

- **Best effort. No SLA.** There is no guaranteed acknowledgement time, no triage rota, no
  on-call, and no commitment that any given report is fixed at all.
- **Coordinated disclosure window: 90 days.** Please give the maintainer 90 days from your report
  before public disclosure. If nothing has happened by then, publish; a silent maintainer is not a
  reason for a defect to stay unknown, and this sentence is here so you do not have to ask.
- **A fix may be a documentation change or a withdrawal.** With nothing released, the honest remedy
  for many findings is to correct a claim, narrow the design, or withdraw a mode — not to patch.
- **No security assessor has reviewed this project.** Not the design, not the threat model, not any
  code. Review is author-only (D-27), and it says so on every public artifact.

## Loopback is not treated as a security boundary

Stated plainly, because the opposite assumption is the most common way a local web tool is built
wrong: **loopback is not treated as a security boundary** (D-32).

The reason, in one sentence: any local process, browser tab, or extension can reach `127.0.0.1`,
the same-origin policy restricts *reading* responses rather than *sending* requests, and DNS
rebinding defeats the origin distinction entirely.

Two consequences are already fixed as design corrections rather than left to the implementer
(D-32): an Origin/CSRF check does **not** stop DNS rebinding, so a **Host-header allowlist** is a
separate and required control; and the one-shot launch token must bind at first load with **no idle
expiry**, because an expiry mid-form is simultaneously a WCAG 2.2.1 failure and a data-loss event in
a tool with no persistence to recover from.

The full control set and its adversarial tests are the threat model's, not this file's — see below.

## Threat model

The threat model — assets, adversaries, trust boundaries, the loopback control set L1 … L8, and one
passing adversarial test per control — is *planned — EP-38*, with the controls built at *EP-41* and
the egress and retention harnesses at *EP-46*. Release-gate item 4 requires every loopback control
to have a passing adversarial test and the no-egress log to be empty (GOVERNANCE §8).

This file deliberately does not summarise the threat model. A summary that drifts from the model is
worse than a link, and there is nothing to summarise yet.

## Out of scope

- **Third-party deployments.** Running this tool is not an intended use (D-33). There is no
  installability guarantee, no supported configuration, and no supported machine. A report that
  depends on the operator having installed the tool in a supported configuration is out of scope
  because **no such configuration is claimed** — this is not a dodge, it is the same statement as
  "status: design".
- **Vulnerabilities in the operating system, the browser, the GPU driver, or other software on the
  machine.** Report those to their vendors. What this project owes you about them is disclosure,
  and that is [`PRIVACY.md`](PRIVACY.md) §8.
- **The residual channels in [`PRIVACY.md`](PRIVACY.md) §8** — crash dumps, the page file, GPU
  memory not zeroed on free, browser retention beyond the stated mitigations. They are already
  disclosed as channels the project cannot close, so a report that they exist is confirmation
  rather than a finding. A report that one of them is **worse than disclosed**, or that a channel
  is missing from that list, is very much in scope.
- **Denial of service against a single-user local tool.** The operator can close the window.
- **Clinical correctness of generated text.** That is a safety concern, not a vulnerability, and it
  belongs to [`SAFETY.md`](SAFETY.md) — though the reporting path is the same private one.

## No runtime secrets exist, by design

**This project holds no runtime credentials.** There is no API key, token, password, connection
string, or service account anywhere in it, in any mode. This follows from the design rather than
from discipline: there is no runtime network (D-8), so there is nothing to authenticate to.

The two things that might look like exceptions are not credentials:

- The **one-shot launch token** in the loopback URL is a single-use CSRF and tab-binding value
  generated per launch, consumed at first load, and never stored (D-32).
- **CI holds no secrets.** The workflow declares `permissions: contents: read`, pins third-party
  actions to commit SHAs, and no job may reference a secret, a model root, an index root, or the
  corpus directory (D-42; `epppsynth/docs/adr/ADR-008-ci-scope-and-pinning.md`).

This is written as an assertion so it can be tested rather than believed. `epppsynth scan` sweeps
every tracked file for secret-shaped strings, and `epppsynth scan --history` sweeps
`git log -p --all` as well — because this repository's history was erased and re-created, and a
clean tree is not a clean history claim. The CI `scan` job runs the full-history form on every
push and is the only job that fetches the whole history.

## Model and weight loading

Loading a model is the largest supply-chain surface this project has (R-29), so the rules are stated
here as security rules rather than left in the runtime design (D-31, D-44):

- **Pinned by repository plus revision SHA.** A model is identified by both; a moving tag is not an
  identifier.
- **SHA-256 verified before load.** The file hash is checked against the recorded value, and a
  mismatch is a hard failure, not a warning.
- **Remote code execution disabled unconditionally.** No `trust_remote_code`, no execution of
  anything that arrives with a model, under any flag.
- **No pickle formats.** GGUF or safetensors only. A pickle-format weight file is refused rather
  than loaded carefully.
- **No auto-download at runtime.** Weights are fetched deliberately, one model at a time, ≤ ~8 GB
  each, confirmed individually (D-30) — never as a side effect of starting the application.
- **Weights are never in Git or LFS.** They live at `C:\epppmodels`, outside the repository tree.
- **Embedding models are models.** Every rule above applies to the index's embedding model
  identically (D-44). It is the easiest supply-chain gap to leave open, which is why it is named
  rather than implied.

Enforcement is *planned — EP-33* for the loader and *EP-41* for the hardening pass; the SBOM and
dependency audit are *planned — EP-41 and EP-50*.

## Incident, rollback and end of support

The procedure, fixed here so that it is not invented under pressure:

1. **Assess.** Determine whether any *released* artifact is affected. Today the answer is
   structurally no, because nothing is released.
2. **If a released artifact is affected:** yank the affected tag and publish a GitHub Security
   Advisory. Tags are **immutable** — a fix is a new tag, never a re-pointed one.
3. **Record.** Append a dated addendum to [`epppsynth/DECISIONS.md`](epppsynth/DECISIONS.md).
   Decisions are never rewritten (D-1, D-2), so the incident stays visible in the public record
   after it is closed.
4. **Downgrade.** The previous tag remains supported until the replacement ships, with a documented
   downgrade note. Otherwise "yank the tag" would leave a user with nothing.
5. **Support scope.** **Only the latest tag is supported.** There are no long-term-support branches
   and no backports.

**Archive and deprecation.** A public repository that looks clinical must not be able to become
quietly unmaintained. If this project stops being maintained, the following happens **before** it
goes quiet, not after:

- the README status line and the badge are changed to say so, in the same place the status has
  always been stated;
- any published advisory and any recorded halt stay published — a halt that is not visible is
  itself an overclaim (GOVERNANCE §8);
- the repository is archived on the platform, which makes it read-only and marks it archived in the
  interface, so a reader can see the state without reading commit dates;
- issues are closed with a pointer to this section.

Archiving is the end state, not deletion: the design record is the artifact, and withdrawing it
would remove the evidence for the claims already made in public.

## Contribution and support posture

No pull requests are accepted in v1. Issues are open for discussion only — not support, and never
clinical advice. The reasoning and what would change it are in [`CONTRIBUTING.md`](CONTRIBUTING.md);
conduct is [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).

---

*Last reviewed 2026-08-31, by the author, at EP-4. **Author review only** — no security assessor,
privacy officer, or counsel has reviewed this project or any artifact in it.*
