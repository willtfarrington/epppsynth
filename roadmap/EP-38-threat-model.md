# EP-38 — Threat model

**Size:** L · **Mode:** a · **Core/Stretch:** core ·
**Depends on:** EP-1 (toolchain, package skeleton, ADR framework, CI) ·
**Blocks:** EP-40 (loopback app shell)

> **Charter.** Scope and acceptance below are sketches, not a final step list. **EP-37** (reviewer
> recruitment pack, re-plan P4) upgrades this brief to full form.

## Context

A loopback UI raises a browser trust boundary at the same moment v1 has no authentication, so the
threat-model packet is owed **before** the first UI brief. That ordering is why this brief
is first in P5: the content security policy fixed here is what forces every template to be CSP-clean
from its first commit — no inline style, no inline script, no inline event handlers — and a CSP
retrofitted onto inline handlers is a rewrite, not a header.

At pickup the tree has no `ui` package and no threat model. D-21 and D-32 exist, and **D-32 as
written is incomplete**: it names an Origin/CSRF check and a one-shot launch token but no Host-header
allowlist. That is a real gap: Origin/CSRF does **not** provide the DNS-rebinding
control (R-26). This brief writes the corrected eight-control set down and justifies each control
against a named adversary; EP-41 implements and tests them.

**Loopback is not a security boundary.** Any local process, browser tab or browser extension can
reach the loopback interface; same-origin policy restricts *reading* responses, not *sending*
requests. Loopback is a reachability reduction and nothing more, and `SECURITY.md` says exactly that.

## Safety preconditions

- **Public artifact (D-3).** Pre-publication checklist items 4 (local paths, hostname, username —
  the document describes a bind address and a port, never a machine) and 7 (public claims — it may
  not imply the tool is hardened or audited) are re-run before commit.
- **Overclaim (R-32/R-9).** The document states the posture as *layered reachability reduction*,
  never "secure". Every control is written with the attack it does **not** stop.
- **Retention (D-8).** The document itself names the residual channels rather than hiding them:
  Windows Error Reporting crash dumps, browser form history, and bfcache. Documented, not denied.
- **No new attack surface** — this brief writes prose and an ADR only; `n/a` for runtime invariants.

## Scope sketch (refine at re-plan)

1. `epppsynth/docs/threat-model.md`: assets (the reader's free text first, then the local index,
   model files, the registry, the machine); adversaries in realistic order (a page in another
   browser tab; a compromised dependency or Action; the reader's own mistake; a malicious
   contributor, post-v1 only per D-34); the explicit non-adversary (a remote network attacker,
   because there is no runtime network — *to be verified in EP-46, not assumed*).
2. The **eight layered controls**, each written so EP-41 can test it independently: L1 bind to
   loopback on an ephemeral port, never a wildcard address; L2 Host-header allowlist on exact match;
   L3 `Origin` / `Sec-Fetch-Site` check; L4 one-shot launch token ≥ 128 bits exchanged immediately
   for a host-only session cookie and then invalidated; L5 session-bound CSRF token; L6 strict CSP
   (`default-src 'none'` …, narrowed only by `connect-src 'self'` for L8's heartbeat) plus the
   security-header set; L7 **no CORS headers at all**; L8 single session, with an explicit Quit
   control and a documented process-level idle-timeout heartbeat.
3. Record against L4 and L8 the settled correction: the launch token binds at **first load with no
   idle expiry**. An expiry mid-form is both an accessibility failure (2.2.1 Timing Adjustable) and
   a data-loss event with no persistence to recover from. The original "idle timeout" element of L8
   is struck as a *session* control.
4. Record against L8 why **"the server exits when the tab closes" was rejected as unimplementable
   here**: `default-src 'none'` and the deliberate closure of the beacon path leave no trustworthy
   unload signal, and the mandatory no-JS full-page-POST fallback (D-68) means a supported reader
   may run with no script at all, so tab-close detection would silently do nothing for exactly
   those readers; inferring a closed tab from absent traffic is the struck idle timeout renamed.
   What L8 ships instead: single session; an explicit Quit control that works with scripting
   disabled; a server-side inactivity timer that ends the **process**, never the session or the
   form; and an optional heartbeat under `connect-src 'self'` that refreshes that timer. Write the
   rejection down here so a later session does not reinstate it. EP-41 implements and tests all
   three parts.
5. Prompt injection: the free-text field is **data**; output-side structural validation — schema,
   citation resolution, question-or-offer parse — is the primary control (D-55), not input filtering.
6. Exfiltration, resource exhaustion, inert-output, least-privilege, dependency and Actions
   sections; an ADR recording the CSP as binding on every later UI brief; `SECURITY.md` cross-link.

## Verification / acceptance (sketch)

- Every one of L1–L8 names a test that EP-41 can implement; a scripted check asserts each control ID
  appears in both `threat-model.md` and the EP-41 test-name list.
- The document contains no local user-profile path, no username and no hostname (leak scanner, EP-6).
- The CSP string in the document is byte-identical to the one the shell emits at EP-40 *(checked
  again by EP-41's header-equality test)*.
- *(judgement, owner)* Every control states what it does not stop.

## Parked → final-roadmap.md

- Post-v1 contributor-attestation and PR-intake threat surface (D-34 revisit once reviewers exist).
- Any hardening that assumes a multi-user or shared machine.
