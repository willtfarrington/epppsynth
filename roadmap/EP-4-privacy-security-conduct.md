# EP-4 — PRIVACY, SECURITY, CODE_OF_CONDUCT, CONTRIBUTING

**Size:** M · **Mode:** n/a · **Core/Stretch:** core ·
**Depends on:** EP-2 (canonical docs), EP-3 (SAFETY charter) ·
**Blocks:** EP-8 (roadmap tooling, re-plan P0)

## Context

These four files are the ones a stranger opens on GitHub before reading anything else, and each of
them makes a promise. This brief's discipline is that **every promise names its enforcement** — the
mechanism, the brief that builds it, and the test that proves it — or is written as a residual
channel the project cannot close. A privacy document that asserts "no retention" without naming the
three ways that is verified is a marketing document; this one is not allowed to be.

**What exists.** `README.md` with the approved status line and the no-PR sentence; `GOVERNANCE.md`
with the data boundary (D-8) and the trainee non-surveillance guarantee (D-19); `SAFETY.md` linking
to a `SECURITY.md` that does not yet exist (EP-3 recorded that dangling link deliberately).
`DECISIONS.md` with the index. No `PRIVACY.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md` or
`CONTRIBUTING.md`.

**Platform state, already settled by the owner (D-76).** Issues are **on**, with a "discussion only,
no support, no clinical advice" template; Discussions, Wiki and Projects are **off**; GitHub private
vulnerability reporting is **enabled**. `SECURITY.md` therefore needs nothing further from the
platform — it points at the repository's private advisory intake path. This brief writes the
documents; it does not change repository settings.

Implements: D-8 (data boundary), D-16 / D-23 / D-51 (what the local index may contain and that it
never leaves the machine), D-19 (trainee non-surveillance, written as a promise with its
enforcement listed), D-33 (third-party use is not an intended use), D-34 (no PRs in v1; issues
open; private reporting path; Code of Conduct present), D-52 (local logging off by default,
hash-only when enabled, never in mode (b)), D-76 (repository settings and the advisory path).
Mitigates R-8 (trainee surveillance / compelled disclosure), R-18 (Windows Error Reporting crash
dumps capturing prompts), R-19 (local index leaking via fixture, screenshot or error message),
R-22 (launch token persisting in browser history/sync), R-29 (supply-chain), R-38 (a third party
runs the app and treats it as validated).

## Safety preconditions

| Invariant at risk | Guard in this brief |
|---|---|
| A privacy promise that is not true (D-8, R-18) | Residual channels are **named, not hidden**: Windows Error Reporting crash dumps; browser bfcache, form history and profile sync; the OS page file; GPU memory not zeroed on free. `PRIVACY.md` states each, states what the project does about it, and states plainly where the project cannot close the channel. This is the conservative-public-claims invariant applied to the privacy document itself. |
| "No retention" asserted rather than verified | The document names all three verification layers and the brief that builds each: *structural* — `UserUtterance` is a distinct type whose `__repr__` is `<redacted>`, with a logging filter that **raises in tests** on a raw envelope (EP-17); *behavioural* — the filesystem-delta harness (EP-46); *residual* — this disclosure. |
| Loopback described as a security boundary | `SECURITY.md` states explicitly that **loopback is not treated as a security boundary**, gives the one-sentence reason (any local process, browser tab or extension can reach `127.0.0.1`; same-origin policy restricts reading responses, not sending requests; DNS rebinding defeats it entirely), and links the threat model as *planned — EP-38*. |
| An honest support posture (D-33, R-38) | `SECURITY.md` states a best-effort, no-SLA response posture for a single unpaid maintainer, a 90-day coordinated-disclosure window, and that third-party deployments are out of scope. `CONTRIBUTING.md` and the Code of Conduct addendum both state that issues are for discussion, not support, and that no clinical advice will be given. |
| Contact details in a public file | The Code of Conduct enforcement contact and the `SECURITY.md` secondary contact are the project's public contact address only. **No** hostname, machine name, account name, or local path appears in any of the four files; step 9 sweeps for them. |
| Trainee guarantee weakened by omission (D-19, R-8) | The non-surveillance guarantee is written as an enumerated promise — no accounts, no scoring, no retention, no export, no employer visibility, voluntary use only — with each item's enforcement named, plus D-52's absolute: **local logging is never enabled in mode (b)**. |

Pre-publication checklist items exercised here: **1 (secrets — `SECURITY.md` asserts the project
holds no runtime credentials, and the assertion is testable)**, **4 (local paths & hostname)**,
**7 (public claims)**.

## In scope

1. **`PRIVACY.md`** at the repository root:
   - the data boundary verbatim (D-8): no PHI, no real cases, manifestly fictional scenarios only,
     no retention of prompts or outputs, no runtime network, offline-capable but **not**
     air-gapped;
   - a data-class table — input envelope, free-text utterance, selected concepts, model KV /
     activations, rendered output, source-pane spans, logs, benchmark data — with one column per
     mode and a persistence column whose value is `none` everywhere it should be;
   - no accounts, no telemetry, no analytics, no crash reporting;
   - **what the browser may retain anyway** and what the operator can do: form history (mitigated
     by `autocomplete="off"`), back-button bfcache (mitigated by `Cache-Control: no-store`), the
     one-shot launch token in history and profile sync (mitigated by consuming the token and
     redirecting to a clean URL, plus `Referrer-Policy: no-referrer`) — each naming EP-40/EP-42 as
     the implementing brief;
   - the residual-channel disclosure (safety precondition 1) in its own section, titled so it
     cannot be skimmed past;
   - logging policy (D-52): off by default; when enabled, envelope **hash** plus timings plus the
     version triple only; never any identity; **never in mode (b)**;
   - what the local index may contain and that it never leaves the machine (D-16, D-23, D-51): it
     lives at `C:\epppindex`, outside the repository tree, gitignored, never in CI, never in a
     release, and appears publicly only as a row in the rights table;
   - the trainee non-surveillance guarantee (D-19) as an enumerated promise with enforcement.
2. **`SECURITY.md`** at the repository root:
   - **Supported versions: none.** Nothing is released; the badge is `status: design`.
   - Reporting path: GitHub private vulnerability reporting at the repository's
     `/security/advisories/new` intake (enabled by the owner, D-76), plus the project's public
     contact address as a fallback.
   - Response posture, honestly stated: best effort, no SLA, single unpaid maintainer, 90-day
     coordinated-disclosure window.
   - **Loopback is not treated as a security boundary**, with the reason.
   - Out of scope: third-party deployments (D-33); anything requiring the operator to have
     installed the tool in a supported configuration, because no such configuration is claimed.
   - **No runtime secrets exist by design**, stated as an assertion EP-6 tests.
   - Model-loading rules as a security statement (D-31, D-44): weights pinned by repository plus
     revision SHA, SHA-256 verified before load, remote code execution disabled unconditionally, no
     pickle formats, GGUF or safetensors only, no auto-download at runtime.
   - Incident, rollback and end-of-support policy: assess → if a released artifact is affected,
     yank the tag and publish an advisory → record a dated addendum in `DECISIONS.md`; tags are
     immutable and the previous tag remains supported with a documented downgrade note; only the
     latest tag is supported; and a stated archive/deprecation procedure so that a public
     clinical-looking repository cannot quietly become unmaintained (R-9).
   - Threat model link, marked *planned — EP-38*.
3. **`CODE_OF_CONDUCT.md`** — Contributor Covenant 2.1 **verbatim**, with the enforcement contact
   filled in, plus exactly one added paragraph: issues are for discussion, not support, and
   clinical advice will not be given in issues. Do not edit the Covenant text itself; the added
   paragraph is clearly marked as a project addendum.
4. **`CONTRIBUTING.md`** (D-60) — short, six to ten lines: no pull requests are accepted in v1
   (D-34); issues are open for discussion; **why** (this is a personal, local tool published as a
   source and design artifact, not a product — D-33); and what will change when reviewers exist
   (D-27), naming the brief.
5. **Cross-link the four documents** from `README.md` and from `SAFETY.md`, and resolve the
   dangling `SAFETY.md` → `SECURITY.md` link EP-3 left behind.
6. **State the same thing in all places.** The no-PR posture now appears in `README.md`,
   `CONTRIBUTING.md` and the Code of Conduct addendum; the wording must be consistent, and step 10
   checks it.
7. **Issue-template alignment.** The owner has configured the "discussion only, no support, no
   clinical advice" template on the platform (D-76). Commit its text to
   `.github/ISSUE_TEMPLATE/discussion.yml` so the wording is versioned and reviewable rather than
   living only in repository settings, and note in the completion note whether the committed text
   matches what is configured.
8. **Verify the reporting path is live** — open the advisory intake URL and confirm it renders the
   private reporting form. Record the observation (not a screenshot) in the completion note.
9. **Run the identity sweep** over the four new files plus the issue template.
10. **Commits:** `docs(epppsynth): add PRIVACY, SECURITY, CODE_OF_CONDUCT and CONTRIBUTING (EP-4)`
    then `docs(roadmap): record EP-4 commit hash`.

## Out of scope

- The threat model itself — **EP-38**. `SECURITY.md` links to it as planned; it does not summarise
  it, because a summary that drifts from the model is worse than a link.
- The eight loopback controls (L1–L8) and their adversarial tests — **EP-40**, **EP-41**.
- The filesystem-delta no-retention harness and the network-disabled egress test — **EP-46**.
- The `UserUtterance` type and the raising logging filter — **EP-17**.
- Secret and PHI-pattern scanners, and the CI assertion that no secret-shaped string exists —
  **EP-6**.
- SBOM generation and dependency auditing — **EP-41** (hardening pass) and **EP-50** (release
  evidence).
- The safety charter itself — **EP-3**.
- Licence files and the rights table — **EP-5**.
- Changing any repository setting on the platform. Settled by the owner under D-76; this brief only
  versions the issue-template text and observes that the advisory path is live.

## Verification / acceptance

Runnable, from the repository root:

```powershell
# all four files exist and are linked from README and SAFETY
Test-Path PRIVACY.md, SECURITY.md, CODE_OF_CONDUCT.md, CONTRIBUTING.md
Select-String -Path README.md,SAFETY.md -Pattern 'PRIVACY\.md|SECURITY\.md|CODE_OF_CONDUCT\.md|CONTRIBUTING\.md'

# every promise names an enforcement: no bare "we do not" without a named mechanism
Select-String -Path PRIVACY.md -Pattern '^\|' | Measure-Object      # data-class table present

# the required explicit statements
Select-String -Path SECURITY.md -SimpleMatch 'loopback is not treated as a security boundary'
Select-String -Path SECURITY.md -SimpleMatch 'Supported versions'
Select-String -Path SECURITY.md -Pattern 'security/advisories/new'
Select-String -Path PRIVACY.md  -SimpleMatch 'never in mode (b)'
Select-String -Path PRIVACY.md  -Pattern 'Windows Error Reporting|page file|bfcache'

# Contributor Covenant present and unedited apart from the marked addendum
Select-String -Path CODE_OF_CONDUCT.md -SimpleMatch 'Contributor Covenant','version 2.1'

# identity sweep over the new files
Select-String -Path PRIVACY.md,SECURITY.md,CODE_OF_CONDUCT.md,CONTRIBUTING.md,.github/ISSUE_TEMPLATE/discussion.yml `
  -Pattern 'C:\\Users\\','\\\\','[A-Z]:\\(?!epppmodels|epppindex)'   # → no output; leak-scan-allow: rule-definition

# all links resolve
git ls-files "*.md" | ForEach-Object { Select-String -Path $_ -Pattern '\]\(([^)#h][^)]*)\)' -AllMatches }
```

Acceptance:

1. All four files exist, are linked from `README.md`, and the `SAFETY.md` → `SECURITY.md` link left
   dangling by EP-3 now resolves.
2. Every promise in `PRIVACY.md` names its enforcement mechanism and the brief that builds it.
   Checked by walking the document once and listing promise → mechanism → brief; zero promises
   without all three. *(judgement — the project owner, working from the generated list.)*
3. `PRIVACY.md` contains the residual-channel section naming, at minimum, Windows Error Reporting
   crash dumps, browser bfcache/form-history/profile-sync, the OS page file, and unzeroed GPU
   memory — and says which of these the project cannot close.
4. `PRIVACY.md` contains the data-class table with a `none` persistence value for every runtime
   class, and the logging rule including "never in mode (b)".
5. `SECURITY.md` states: no supported versions; the private advisory intake URL; a best-effort,
   no-SLA posture with a 90-day window; **loopback is not a security boundary**; third-party
   deployments out of scope; no runtime secrets by design; the model-loading rules; and the
   incident / rollback / end-of-support policy.
6. The advisory intake URL renders the private reporting form; the observation is recorded in the
   completion note with the date.
7. `CODE_OF_CONDUCT.md` is Contributor Covenant 2.1 with the contact filled and exactly one clearly
   marked project addendum. Diff against the upstream 2.1 text shows changes only in the contact
   placeholder and the appended addendum.
8. `CONTRIBUTING.md` is ten lines or fewer and states the no-PR posture, the reason, and what would
   change it, naming the brief.
9. The identity sweep returns nothing across all five new files.
10. The no-PR wording is consistent across `README.md`, `CONTRIBUTING.md` and the Code of Conduct
    addendum — compared programmatically, not by eye.
11. `uv run pytest -q` and CI stay green.

## Parked → final-roadmap.md

- A contributor attestation (DCO or equivalent) and a PR intake process. D-34 defers both until
  reviewers exist (D-27); `CONTRIBUTING.md` names that trigger so the parked item has a condition,
  not just a date.
- A published security advisory log. Nothing to log while nothing is released; revisit when the
  first tag is cut (EP-52).
- A `SECURITY.md` PGP key or encrypted reporting channel. GitHub private vulnerability reporting
  covers it; revisit only if a reporter asks.
- A documented data-protection or records-retention posture beyond "nothing is retained". Would
  become relevant only if the excluded modes (d)/(e) were ever reopened, which D-61 forecloses.
