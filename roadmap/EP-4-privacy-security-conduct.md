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

> **Completion note (2026-08-31).** Every result below is what was **observed**, not what was
> expected. The acceptance block was run verbatim in PowerShell from the repository root and its
> counts are recorded; the parts of it that need a machine comparison were additionally written as
> tests (`epppsynth/tests/test_public_docs.py`, 20 passing) so they re-run in CI rather than once.
>
> #### Deviation 1 — the advisory intake could not be observed rendering the form, so it was verified through the API instead
>
> Step 8 asks for the intake URL to be opened and the private reporting form observed. The
> repository's `/security/advisories/new` path **does not render a form to an unauthenticated
> fetch**: it returns GitHub's `Sign in to GitHub` page. That is the expected behaviour of the
> endpoint, not a fault, and it means the brief's step as written cannot produce the observation it
> asks for from this session.
>
> Verified through the platform API instead, which reports the setting itself rather than the page
> that depends on it: `gh api repos/<owner>/<repo>/private-vulnerability-reporting` →
> **`{"enabled":true}`**, observed **2026-08-31**. The reporting path is live; the *form* was not
> seen, and this note says so rather than implying it was.
>
> #### Deviation 2 — the issue template is not configured on the platform, so the committed file is the only version
>
> Step 7 says the owner "has configured" the template and asks whether the committed text matches it.
> **Nothing is configured.** Observed 2026-08-31: `gh api repos/<owner>/<repo>/contents/.github`
> returns `workflows` only, and `gh api repos/<owner>/<repo>/issues/templates` returns 404. There is
> no template to compare against, so the answer to "does the committed text match?" is that there is
> nothing on the other side of the comparison.
>
> This is benign and self-correcting: GitHub reads issue forms **from** `.github/ISSUE_TEMPLATE/`, so
> committing `discussion.yml` *is* configuring it. It takes effect on push. Worth the owner
> confirming afterwards that the form renders and that its two required checkboxes behave as
> intended.
>
> #### Deviation 3 — Projects is **on**, contrary to D-76
>
> Observed 2026-08-31 via `gh api repos/<owner>/<repo>`:
> `{"has_discussions":false,"has_issues":true,"has_projects":true,"has_wiki":false,"private":false}`.
> D-76 settles Discussions, Wiki **and Projects** as off; three of the four match and
> **`has_projects` is `true`**. This brief explicitly does not change repository settings, so nothing
> was touched. It is recorded here as an owner action: either turn Projects off, or record a dated
> addendum under D-76. Left silent it would be a small drift between a published decision and the
> platform it describes, which is the class of drift the badge scheme exists to prevent.
>
> #### Deviation 4 — there was no project contact address on record
>
> Safety precondition 5 and in-scope item 3 require "the project's public contact address" in the
> Code of Conduct and as the `SECURITY.md` fallback. **No such address exists anywhere in the
> repository**, and `.local/` may not be read. Used the address already public in this repository's
> own commit metadata — the git author address — so that filling the placeholder disclosed nothing
> that publishing the repository had not already disclosed. It appears twice: as the Covenant's
> enforcement contact, and as the `SECURITY.md` fallback, where it is labelled as not a monitored
> security inbox and as strictly worse than the private advisory path.
>
> **This is the one item in this brief the owner should overrule if they have a dedicated alias.**
> Substituting one is a two-line change plus the `CONTACT` constant in `test_public_docs.py`.
>
> #### Deviation 5 — the advisory intake is a platform-relative link, not an absolute URL
>
> Safety precondition 5 bars any account name from the four files, and the absolute intake URL
> contains the owner's GitHub handle. Written as `[report a vulnerability
> privately](../../security/advisories/new)` instead, which GitHub resolves against
> `/<owner>/<repo>/blob/<branch>/` to exactly the intake page, alongside the plain-text route
> (**Security → Advisories → Report a vulnerability**) for anyone reading the raw file. Acceptance's
> `security/advisories/new` pattern matches either form. The consequence: the link works on GitHub
> and not in a local markdown preview, and `test_every_relative_link_in_the_new_documents_resolves`
> skips `../../` for that reason, with the reason in the code.
>
> #### Deviation 6 — the README's no-PR sentence had to be rewritten for acceptance 10 to pass
>
> Acceptance 10 requires the no-PR wording to be identical across `README.md`, `CONTRIBUTING.md` and
> the Code of Conduct addendum, "compared programmatically, not by eye". The README said **"No pull
> requests in v1."** and `GOVERNANCE.md` §14 says **"No pull requests are accepted in v1."** — close
> enough to read as the same claim and not close enough to compare equal. Governance overrides, so
> two sentences were fixed as canonical and are now repeated verbatim in **six** places (`README.md`,
> `SAFETY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, and the issue template):
>
> - `No pull requests are accepted in v1.`
> - `Issues are open for discussion only — not support, and never clinical advice.`
>
> The comparison normalises whitespace and strips `**`, because the repository wraps at 100 columns
> and a canonical sentence that may not wrap would be a worse constraint than the one it enforces.
> `SAFETY.md` needed one further fix found by that test: its copy of the second sentence ended in an
> em dash rather than a full stop.
>
> #### Deviation 7 — two files outside the brief's list
>
> `epppsynth/tests/test_public_docs.py` (new, 20 tests) because acceptances 2, 3, 4, 5, 7, 8, 9 and
> 10 are structural properties that would otherwise be checked once and then drift; and
> `epppsynth/tests/test_safety_charter.py`, whose
> `test_every_relative_link_resolves_except_the_ep4_file` asserted `unresolved == ["SECURITY.md"]`
> and necessarily failed the moment this brief created that file. Updated — not deleted — to
> `test_every_relative_link_resolves`, asserting `unresolved == []`, exactly as EP-3's handoff note
> asked.
>
> The Contributor Covenant's integrity is checked **by hash rather than by eye**: the test restores
> the `[INSERT CONTACT METHOD]` placeholder, hashes everything above the addendum marker, and
> compares against the recorded SHA-256 of the upstream 2.1 text
> (`369bf7301883368fc19203bd0f1233fed2b83f0378ad19c4d0708bf61925339b`, fetched from the canonical
> `EthicalSource/contributor_covenant` release branch with the site's TOML front matter stripped). No
> second copy of the Covenant is vendored to make that possible.
>
> #### What was created
>
> `PRIVACY.md` — eleven sections, ending in an enforcement register of **14 rows**. `SECURITY.md` —
> eleven sections. `CODE_OF_CONDUCT.md` — Covenant 2.1 verbatim plus one marked addendum.
> `CONTRIBUTING.md` — **9 lines, 5 non-blank**. `.github/ISSUE_TEMPLATE/discussion.yml` — four
> blocks, two required acknowledgements, parses under `yaml.safe_load`.
> `epppsynth/tests/test_public_docs.py`. `README.md` and `SAFETY.md` updated: the four files are
> linked from both, the `planned — EP-4` markers are gone, and the `SAFETY.md` → `SECURITY.md` link
> EP-3 left dangling now resolves.
>
> #### Acceptance, as observed
>
> | # | Criterion | Observed |
> |---|---|---|
> | 1 | four files exist, linked from README; the EP-3 dangling link resolves | `Test-Path` → **True × 4**; the link sweep over README and SAFETY → **10 matches**; across all **76** tracked-and-new markdown files, **zero** unresolved relative links — previously exactly one |
> | 2 | every promise names mechanism and brief *(owner judgement)* | `PRIVACY.md` §11 **is** that list, generated as the document was written: 14 rows, 13 filling mechanism + brief + proof, and **one row — #14 — whose mechanism cell reads "no mechanism — disclosed, not closed"**. A test asserts that shape is the only permitted exception. Offered for the owner's walk |
> | 3 | residual section names WER, bfcache / form history / profile sync, page file, GPU memory, and says which cannot be closed | §8, five named channels; the phrase *"The project cannot close th…"* appears **4** times, plus the machine-software paragraph; `Windows Error Reporting|page file|bfcache` → **8 matches** |
> | 4 | data-class table with `none` persistence on every runtime class; logging rule including "never in mode (b)" | **8 data rows**, one column per mode; the **6 runtime rows** all read `**none**`; the two that do not are Logs and Benchmark data, named in the test so a ninth row cannot join them quietly. `never in mode (b)` → **1 match**, and §4 states it twice more in prose |
> | 5 | the eight required `SECURITY.md` statements | all present: no supported versions (`\| — \| there is no released version \|`); intake path → **2 matches**; best-effort / no-SLA plus a 90-day window; `loopback is not treated as a security boundary` → **2 matches**; third-party deployments out of scope; no runtime credentials; the seven model-loading rules; incident / rollback / end-of-support including immutable tags, latest-tag-only, and the archive procedure for R-9 |
> | 6 | intake URL renders the private form, recorded with a date | **not observed as written** — deviation 1. `{"enabled":true}` from the platform API, **2026-08-31** |
> | 7 | Covenant 2.1, contact filled, exactly one marked addendum | SHA-256 of the restored text equals the upstream digest; `[INSERT CONTACT METHOD]` occurs **0** times; the addendum contains **0** further `## ` headings |
> | 8 | `CONTRIBUTING.md` ten lines or fewer; posture, reason and trigger naming the brief | **9 lines** total, **5** non-blank; D-33, D-34 and D-27 cited; *planned — EP-37* named as the trigger |
> | 9 | identity sweep returns nothing | the brief's three patterns over all five files → **no output**. A second test asserts the only absolute paths present are the two declared roots |
> | 10 | no-PR wording consistent, compared programmatically | both canonical sentences present verbatim in **6** files; found and fixed one drift in `README.md` and one in `SAFETY.md` |
> | 11 | `pytest` and CI green | `ruff check` "All checks passed!"; `ruff format --check` "15 files already formatted"; `pytest -m "not requires_index and not requires_model" -q` → **36 passed**. No committed blob contains a carriage return |
>
> Pre-publication items re-run: **1 (secrets)** — `SECURITY.md` asserts no runtime credentials exist,
> written so EP-6 can test it; no secret-shaped string was introduced. **4 (local paths & hostname)**
> — the sweep above, plus the check that only the two declared roots appear. **7 (public claims)** —
> `README.md`, the badge, `SAFETY.md`, `PRIVACY.md` and `SECURITY.md` agree: `status: design`, no
> release, no supported version, author review only, no evidence of benefit. Both new documents carry
> an explicit "author review only" line naming the reviewers who have **not** read them.
>
> #### For later briefs
>
> - **EP-6** inherits three testable assertions from `SECURITY.md`: no runtime credentials anywhere in
>   the tree **or the full history**, no secret-shaped strings, and the identity sweep — already
>   implemented over five files in `test_public_docs.py` and wanting widening to all tracked files.
>   Its pattern block carries the `leak-scan-allow: rule-definition` marker the acceptance block
>   introduced, so the scanner needs to honour that marker.
> - **EP-38** must not be summarised into `SECURITY.md`; the file links it and says why. Its L1 … L8
>   control set is referenced by name.
> - **EP-17** owns rows 2, 7, 11 and 13 of the `PRIVACY.md` enforcement register; **EP-46** owns rows
>   3, 4, 5 and the redacting excepthook of §8; **EP-40 / EP-41 / EP-42** own row 12; **EP-47** owns
>   row 8 and four rows of the trainee table. Each will need its register row's status column moved
>   off *not built*, and that edit is the cheap way to keep the document honest.
> - **EP-8** should decide whether `PRIVACY.md` §11's status column becomes tool-checked
>   (`roadmap_check`) rather than hand-maintained. Hand-maintained is exactly the failure mode the
>   badge scheme was designed to avoid.
> - Owner actions from deviations 2, 3 and 4: confirm the issue form renders after push, resolve the
>   `has_projects` drift against D-76, and substitute a dedicated contact address if one is wanted.

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
