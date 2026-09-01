# PRIVACY

What this tool does with what you type, and — where it cannot control that — what it discloses
instead.

```
status: design
```

Design and planning artifact — v1 in progress; no release, no demo, no validation.

**Nothing in this repository runs.** There is no engine, no interface, and no logger, so nothing
here is currently processing anything. Every statement below is therefore one of two kinds, and the
document marks which: a **property of the design** that later work must keep, or a **residual
channel** that no amount of later work can close. The rule this document is written under is that
**every promise names its enforcement** — the mechanism, the work packet that builds it, and the
test that proves it — or it is written as a channel the project cannot close. A privacy document
that asserts "no retention" without naming the ways that is checked is a marketing document. §11 is
the register that makes the rule auditable in one pass.

Where this document and [`epppsynth/GOVERNANCE.md`](epppsynth/GOVERNANCE.md) disagree, governance
wins and this document is wrong. Decisions cited as `D-n` are in
[`epppsynth/DECISIONS.md`](epppsynth/DECISIONS.md); hazards cited as `R-n` are in
[`epppsynth/DESIGN.md`](epppsynth/DESIGN.md) §14; work packets cited as `EP-n` are in
[`roadmap/README.md`](roadmap/README.md).

---

## 1. The data boundary

The boundary, stated as governance states it (D-8):

> No PHI. No real cases. Manifestly fictional scenarios only. **No retention** of prompts or
> outputs. **No runtime network.** Offline-capable, not air-gapped: the machine keeps its network,
> and the *application* is proven silent.

Two words in that paragraph carry weight and are worth separating.

**"Offline-capable, not air-gapped."** The machine this runs on is an ordinary laptop with an
ordinary network connection. The claim is about the *application*, not the computer. Other software
on the same machine — the browser, the operating system, a backup agent, a sync client — keeps
doing what it does, and this project neither controls nor audits it. §7 is about exactly that gap.

**"Proven."** Proven is meant literally, and it is the reason §3 exists: the no-retention claim is
verified in three layers, and the no-egress claim in two, rather than asserted once and repeated.
Until those harnesses are built, the honest status of the claim is *specified, not yet verified*,
and §11's status column says so on every row.

## 2. What data exists, per mode, and how long

The three modes are (a) clinician pre-encounter reflection on fictional scenarios, (b) trainee
education and reflection, (c) clinician self-reflection — one engine, three purpose profiles
(D-13). The table is the design contract the runtime work packets are built against.

| Data class | Mode (a) | Mode (b) | Mode (c) | Persistence |
|---|---|---|---|---|
| **Input envelope** — the structured enums and declared hard-stop flags (`InputEnvelope`, *planned — EP-17*) | held in process for one request | same | same | **none** |
| **Free-text utterance** — the one free-text field (`UserUtterance`, *planned — EP-17*) | held in process for one request; quoted back to the reader and nothing more | same | same | **none** |
| **Selected concepts** — the concept IDs the deterministic selector chose | held in process for one request | same | same | **none** |
| **Model KV cache and activations** — only on the model path, which is not the default | process memory, freed at process exit | same | same | **none** |
| **Rendered output** — the waypoints themselves | browser DOM or terminal output, on the operator's screen | same | same | **none** — no export in v1 (D-6) |
| **Source-pane spans** — verbatim spans from the reader's own copy | screen only, from the local index | same | same | **none** — never emitted, exported, screenshotted, or serialized (D-23) |
| **Logs** | off by default; envelope **hash**, timings and the version triple only, when explicitly enabled | **never enabled** (D-52) | off by default; hash-only when explicitly enabled | **none** by default; when enabled, hashes and timings — never content, never identity |
| **Benchmark data** — cold/warm timings, peak memory, peak disk | measurement artifact, no user content | — | — | on disk and in the repository, by design; it contains no user data (*planned — EP-32, EP-35*) |

Every runtime class in that table has persistence **none**. The two rows that are not `none` are
the two that are not runtime user data: a log that the operator has to switch on, which records
hashes rather than content, and a benchmark packet, which records timings rather than anything a
person typed.

**No accounts. No telemetry. No analytics. No crash reporting.** There is no sign-in, no user
record, no usage counter, no event stream, no error-reporting service, and no phone-home of any
kind, in any mode. This is not a setting; there is no code path for any of it, and the mechanism
that keeps it that way is the same one that keeps the application silent on the network: the
egress test in §3, which fails on any outbound connection whatever its purpose.

## 3. How "no retention" is checked, rather than asserted

Three layers, each with the work packet that builds it. They are listed in the order they would
catch a defect — earliest first.

**Layer 1 — structural.** The free-text field is a distinct type, not a `str`: `UserUtterance` is a
frozen wrapper whose `__repr__` is `<redacted>`, so it cannot reach a log line, a traceback frame,
or a debug print by accident. It is accompanied by a logging filter that **raises in tests** when a
raw envelope is passed to it, so the failure mode is a red test rather than a quiet leak.
*Planned — EP-17.*

**Layer 2 — behavioural.** A filesystem-delta harness snapshots the disk before and after a full
inference session and asserts the delta is empty. This is the layer that catches retention nobody
wrote on purpose — a framework cache, a temporary file, a crash artifact. *Planned — EP-46.*

**Layer 3 — residual.** Everything neither of the first two layers can reach, disclosed in §8
rather than denied. Governance requires this disclosure rather than permitting it.

The companion claim, no runtime network, is verified in **two** layers for the same reason
(GOVERNANCE §5): an in-process socket guard proves only that the Python layer is quiet, and an
outbound block-and-log rule scoped to the interpreter, asserted to have **zero entries** across a
full inference session, is what proves the native layer is. *Planned — EP-46.*

**Status today: none of the three layers exists.** Every row of §11 carries that status until its
work packet lands.

## 4. Logging

The rule in one line (D-52): local logging is **off by default**, hash-only when enabled, and
**never in mode (b)**. There is no configuration that makes it record content.

- When it is off, nothing is written.
- When the operator explicitly turns it on, a log line may contain: a **hash** of the input
  envelope, timings, and the version triple (application, model, registry). Nothing else.
- It never contains the free-text utterance, the rendered waypoints, a concept's text, a source
  span, a username, a hostname, a file path outside the two declared roots, or any other identity.
- **It is never enabled in mode (b).** Not "off by default in mode (b)" — never enabled. The
  trainee guarantee has to hold structurally rather than by configuration, because a setting a
  trainee cannot verify is not a guarantee (D-19, D-52, R-8).

*Enforcement:* the `UserUtterance` redaction and the raising logging filter, *planned — EP-17*; the
mode-(b) prohibition as a mode gate, *planned — EP-47*; the filesystem-delta harness as the
behavioural check that an off-by-default logger is in fact off, *planned — EP-46*.

## 5. The local index

The tool reads a conceptual substrate from books the author lawfully holds. The derived index —
embeddings and verbatim spans — is a **local artifact only** (D-16).

- It lives at `C:\epppindex`, **outside the repository working tree** and separate from the model
  root, so that it is independently purgeable and independently excludable from backups (D-51).
- It is gitignored, never committed, never present in CI, and never in a release. CI runs a
  no-model, no-index path exclusively; tests that need it carry the `requires_index` marker and are
  deselected (D-42).
- Its spans are **never emitted**. Generated output is always paraphrase plus a chapter-level
  citation. Spans may be *displayed* in a local-only source pane, which is hard-excluded from
  export, screenshots, demo mode, CI, and any published artifact (D-23).
- Publicly, it appears only as a row in the generated per-source rights table (*planned — EP-5*).

*Enforcement:* the ignore rules and the clean-history assertion (EP-0, done); the index-dependent
tests' skip markers (EP-1, done); the span-leak canary and the index-outside-the-tree assertion,
*planned — EP-22, EP-46*; the type graph that makes a span unemittable rather than merely
forbidden, *planned — EP-17*. The hazard is R-19 — a local index leaking via a fixture, a
screenshot, or an error message — and that is the shape a leak here would actually take.

## 6. The trainee non-surveillance guarantee

Mode (b) is for people who are the least able to decline a tool their institution suggests. The
guarantee is therefore enumerated, and each item names what makes it true rather than who promises
it (D-19, D-52, GOVERNANCE §4.7, R-8).

| Promise | What makes it true | Built by |
|---|---|---|
| **No accounts.** There is no sign-in, no user identifier, and no per-user state. | No authentication code path exists; the loopback UI has no user model (D-32). | *planned — EP-40* |
| **No scoring.** Nothing rates, grades, ranks, or evaluates the trainee. | No scoring surface exists in the output contract; the mode (b) prompt profile is separately evaluated for it. | *planned — EP-47* |
| **No retention.** Nothing the trainee types or receives is stored. | The three layers of §3, plus the absolute in §4: logging is never enabled in mode (b). | *planned — EP-17, EP-46, EP-47* |
| **No export.** There is no save, download, or share. | No export path exists in v1 at all, in any mode (D-6). | *planned — EP-40* |
| **No employer visibility.** No educator dashboard, no aggregate report, no institutional feed. | There is nothing to feed one from: no accounts, no retention, no export, no network. Educator-visible artifacts are an excluded feature, not an unbuilt one (D-19). | *planned — EP-47* |
| **Voluntary use only.** | Stated in the mode (b) interstitial copy, and in this file. The project cannot enforce what an institution requires; it can refuse to build the observation surface that would make requiring it useful. | *planned — EP-47, EP-51* |

**Structural moral injury is never individualised.** Mode (b) names conditions, not deficiencies in
the person using it; the charter clause is in [`SAFETY.md`](SAFETY.md).

The last row is the honest one. A guarantee about *this software* is not a guarantee about an
employer, and the compensating control is that the data an employer would want does not exist
anywhere for it to ask for.

## 7. What the browser may keep, and what is done about it

The v1 interface is a single page served on loopback (D-32). A browser is a general-purpose program
that retains things on the user's behalf, and some of those things would be a retention channel
this project did not intend.

| Channel | What it would retain | What the design does | Built by |
|---|---|---|---|
| **Form history / autofill** | text typed into the free-text field, offered back later in a different context | `autocomplete="off"` on the form and on the free-text control | *planned — EP-42* |
| **Back-forward cache (bfcache)** | a rendered response, restorable by the back button after the session is over | `Cache-Control: no-store` on every response | *planned — EP-40* |
| **URL history and profile sync** | the one-shot launch token, synced to the browser vendor's account and to the user's other devices | the token is consumed at first load and the page redirects to a clean URL; `Referrer-Policy: no-referrer` prevents it leaving in a header (R-22) | *planned — EP-40, verified by the loopback suite at EP-41* |

These are mitigations, not eliminations. A browser extension with page access, a screenshot tool, or
an operating-system clipboard history sees what is on the screen regardless, and this project has
no control over any of them. That belongs in the next section, which is the point of the next
section.

## 8. Residual channels this project cannot close

This section exists because a privacy document that lists only the channels it closed is
misleading by omission. Each channel below is real, is not closed by anything above, and is
disclosed rather than denied (GOVERNANCE §5, R-18).

**Windows Error Reporting crash dumps.** If the process crashes, the operating system may write a
dump containing whatever was in memory at the time — which, mid-request, includes the free-text
utterance and the rendered output. **The project cannot close this channel.** What it does: a
redacting `excepthook` reduces what an ordinary unhandled exception puts in a traceback, and the
dump posture is documented rather than denied. What it cannot do: prevent the operating system from
writing a dump, or reach into one that was written. An operator who needs this channel shut has to
shut it at the operating-system level, outside this application. *The redacting excepthook is
planned — EP-46.*

**The operating-system page file.** Memory holding an utterance may be paged to disk by the
operating system, and the page file is not zeroed on write. **The project cannot close this
channel.** Nothing in an ordinary user-space Python and llama.cpp process can guarantee a page is
never written to disk, and claiming otherwise would require locking pages the runtime does not
control. Full-volume encryption changes who can read the page file; it does not stop it being
written.

**GPU memory not zeroed on free.** On the model path, activations and KV cache live in video
memory, and freeing a buffer does not zero it. A later process on the same GPU may observe residue.
**The project cannot close this channel.** It is bounded rather than removed: the model path is not
the default, the deterministic baseline is (D-17), and a session that never loads a model never
writes anything to video memory.

**Browser retention beyond §7's mitigations.** bfcache, form history and the launch token are
mitigated above. Extensions with page access, the operating system's clipboard history, accessibility
tooling, screen recording, and a synced browser profile are **not**, and cannot be from inside a
loopback page. **The project cannot close these channels.**

**Anything else on the machine.** Backup agents, endpoint-management and endpoint-detection
software, file-indexing services, and hypervisor snapshots all see the machine's disk and memory.
"Local" is not automatically private (GOVERNANCE §4.8), and this project makes no claim about
software it did not write.

What follows from this list: the data boundary — **manifestly fictional scenarios only, no PHI, no
real cases** — is not a formality layered on top of these controls. It is the control that makes
the residue in this section survivable. Every channel above is a channel for fictional material,
and it stays that way only because nothing real is ever typed in.

## 9. What this project does not do with data, at all

Stated plainly, because the absence of a thing is easy to leave unstated:

- Nothing is sent anywhere. There is no runtime network in any mode (D-8), verified by the two-layer
  egress test in §3.
- Nothing is used to train, fine-tune, or improve any model. There is no training path in this
  project at all; the model is a renderer of already-selected, authored material (D-54).
- Nothing the operator types is tokenised, keyword-scanned, classified, or mined for inference. The
  free-text field is an **inert echo**: it is quoted back to the reader and never changes what the
  engine emits (GOVERNANCE §4.2). This is also why the tool is not a risk detector.
- Nothing infers beliefs, culture, ethnicity, race, religion, disability, values, protected traits,
  or emotional state from anything typed (GOVERNANCE §4.2).
- No data is shared with any third party, because none leaves the process.

**This tool is not a risk detector and must not be used as one.** It never checks what is typed for
danger.

## 10. If you believe something leaked

Report it **privately**, through this repository's private vulnerability reporting — the path and
what to expect are in [`SECURITY.md`](SECURITY.md). Please do not open a public issue for anything
involving a leak.

If you believe this repository contains real patient, family, trainee, or employee material, or text
reproduced from a copyrighted source, use the same private path; it is treated as a leak rather than
as a bug.

## 11. Enforcement register

Every promise this document makes, with the mechanism that would make it true, the work packet that
builds the mechanism, and the test that proves it. A promise that cannot fill all three columns does
not belong in this file; the disclosures in §8 are in §8 precisely because they cannot.

| # | Promise | Mechanism | Built by | Proved by | Status |
|---|---|---|---|---|---|
| 1 | No PHI, no real cases; fictional scenarios only | intended-use and excluded-use text at the top of every public artifact; PHI-shaped pattern sweep over tracked files and fixtures | EP-2, EP-3 (done); EP-6 (done) | the pre-publication review packet, dated and commit-stamped | text landed; scanner runs in CI and in the pre-commit hook |
| 2 | No retention of prompts or outputs | `UserUtterance` redaction plus a logging filter that raises on a raw envelope | *planned — EP-17* | the filter's own raising tests | not built |
| 3 | No retention of prompts or outputs | filesystem-delta snapshot across a full session | *planned — EP-46* | empty-delta assertion | not built |
| 4 | No runtime network — Python layer | in-process socket guard | *planned — EP-46* | guard tests | not built |
| 5 | No runtime network — native layer | outbound block-and-log rule scoped to the interpreter | *planned — EP-46* | zero log entries across a full inference session | not built |
| 6 | No accounts, telemetry, analytics, or crash reporting | no such code path exists; any of them would be an outbound connection | *planned — EP-40, EP-46* | rows 4 and 5 | not built |
| 7 | Logging off by default; hash, timings and version triple only | logger default plus the redacting type | *planned — EP-17* | logger unit tests over an envelope containing a known string | not built |
| 8 | Logging **never** enabled in mode (b) | mode gate, not a setting | *planned — EP-47* | mode-(b) gate tests | not built |
| 9 | No export in any mode in v1 | no export path exists | *planned — EP-40* | UI contract tests | not built |
| 10 | Index never leaves the machine | index root outside the tree, gitignored, `requires_index` marker, no-model CI path | EP-0, EP-1 (done); *planned — EP-7* | clean-history assertion; CI deselects the marker | ignore rules and markers landed |
| 11 | Verbatim spans never emitted | the type graph makes a span unemittable, not merely forbidden | *planned — EP-17, EP-45* | span-leak canary | not built |
| 12 | Browser form history, bfcache, and launch-token retention mitigated | `autocomplete="off"`; `Cache-Control: no-store`; token consumed then redirected; `Referrer-Policy: no-referrer` | *planned — EP-40, EP-42* | the adversarial loopback suite | not built |
| 13 | Free text never influences what is emitted | the selector's signature excludes `UserUtterance` | *planned — EP-17, EP-19* | the stop criterion's free-text pivot, reported as an architectural property rather than a finding (GOVERNANCE §8) | not built |
| 14 | Crash dumps, page file, GPU residue, browser and machine software | **no mechanism — disclosed, not closed** | — | — | §8 |

Rows 1 and 10 are the only ones whose mechanism exists today. That ratio is the accurate summary of
this document: the boundary is specified in full and enforced almost nowhere, and it will stop being
so one row at a time.

---

*Last reviewed 2026-08-31, by the author, at EP-4. **Author review only** — no privacy officer,
counsel, or security assessor has read this document or the design it describes.*
