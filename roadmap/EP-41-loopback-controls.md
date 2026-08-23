# EP-41 — Loopback security controls and adversarial suite

**Size:** M · **Mode:** a · **Core/Stretch:** core ·
**Depends on:** EP-40 (loopback application shell) ·
**Blocks:** EP-42 (input form), EP-46 (verification, accessibility packet, re-plan P5)

> **Charter.** Scope and acceptance below are sketches. **EP-37** (reviewer recruitment pack,
> re-plan P4) upgrades this to a full brief: `## Scope sketch` splits into `## In scope` /
> `## Out of scope`, and each criterion becomes a named command or artifact. Do not execute from the
> sketch alone.

## Context

Separated from EP-40 on purpose, so the eight controls are built and tested **as controls** — each
with its own failing-case test and its own evidence artifact — rather than as incidental behaviour of
a shell that happens to work. Gate item 4 of D-35 requires the loopback controls to be *verified*; a
control with no failing-case test is an assertion.

EP-38 has fixed the control set and EP-40 emits the header set. Nothing enforces anything yet.

**Loopback is not a security boundary** — the premise, not a caveat. Any local process, browser tab
or browser extension can send requests to the loopback interface, and same-origin policy restricts
reading responses, not sending requests.

Two corrections to D-32 as originally written land here. **First,** the Host-header allowlist is the
DNS-rebinding control (R-26) and Origin/CSRF does **not** provide it — shipping D-32 verbatim would
ship a known-vulnerable pattern. **Second,** the launch token binds at **first load with no idle
expiry**, because an expiry mid-form is both an accessibility failure (2.2.1 Timing Adjustable) and a
data-loss event with no persistence to recover from. The idle-timeout element of the original session
control is therefore struck.

**Third — control 8 is rewritten, because "the server exits when the tab closes" is not
implementable here.** There is no unload signal the server can trust under this project's own rules:
the CSP is `default-src 'none'` with no `connect-src` to the origin, `sendBeacon` is closed
deliberately as an exfiltration control, and the **mandatory no-JS full-page-POST fallback** (D-68)
means a supported reader may run the interface with no script at all — so any tab-close detection
would be a JS-only feature that silently does nothing for the exact readers the fallback exists for.
Detecting a closed tab by absence of traffic is an idle timeout wearing a different name, and that
is what the second correction just struck.

What ships instead: **single session, an explicit Quit control, and a documented idle-timeout
heartbeat that ends the *process*, never the session.** Concretely — (i) a visible **Quit** control
that POSTs (CSRF-checked, and a plain form so it works with no JS) and shuts the server down; (ii) a
server-side inactivity timer with a **generous, documented** default that exits the process when no
request has arrived for that long, so a forgotten tab does not leave a listener running overnight;
(iii) an optional heartbeat that a scripted client may send under `connect-src 'self'` — the one
narrowing of the CSP this requires, to the origin only, no other host — which refreshes that timer
and lets a reader who *is* running JS keep a long-idle session alive. The timer governs process
lifetime only: it never expires the launch token or the session mid-form, so it does not reintroduce
the 2.2.1 Timing Adjustable failure. Record the rejection of the tab-close variant, with these
reasons, in `threat-model.md` beside control 8, so a later session does not "fix" it back.

## Safety preconditions

- **R-22.** The launch token never appears in a URL the results page links to; it is exchanged
  immediately for a host-only session cookie and then invalidated, keeping it out of browser history
  and browser sync. A replayed token is a 403, tested.
- **Exfiltration (D-8).** `default-src 'none'` also closes the beacon path, and **no CORS header is
  ever emitted** — a test asserts `Access-Control-Allow-Origin` is absent from every response.
- **Availability is a clinical hazard.** A hang leaves the clinician waiting mid-workflow, so the
  input cap, single-flight queue and per-request deadline are safety items, not tuning.
- **Public artifact (D-3).** Checklist item 7 (public claims): the evidence file records what was
  tested and states the residual exposure. It never says "secure" or "hardened".

## Scope sketch (refine at re-plan)

1. Implement and independently test the eight controls: loopback bind on an ephemeral port; exact
   **Host-header allowlist**; `Origin` / `Sec-Fetch-Site` check rejecting any non-exact origin and any
   `cross-site`; one-shot launch token of at least 128 bits exchanged for a host-only session cookie
   and invalidated; session-bound CSRF token on every state-changing request; the strict CSP and
   security-header set (`connect-src 'self'` and nothing wider, for the heartbeat only);
   **no CORS headers at all**; single session, refused rather than queued, with an explicit Quit
   control and a documented idle-timeout heartbeat governing **process** lifetime.
2. Adversarial suite, one named test per row: foreign `Origin` → 403 · a rebinding-shaped `Host` →
   403 · replayed launch token → 403 · POST without a CSRF token → 403 · second concurrent session →
   refused · response headers byte-equal to the expected set · no CORS header present anywhere.
3. The no-idle-expiry case, written as a **positive** test: load, idle well past the token's
   nominal lifetime, submit, assert success and no loss of typed input — the process-level idle
   timer must not touch this path.
4. Control 8's three parts, each with its own test: Quit shuts the server down and works with
   scripting disabled; the inactivity timer exits the process after its documented interval with no
   traffic; the heartbeat refreshes the timer and is reachable under `connect-src 'self'` and from
   nowhere else. `threat-model.md` carries the written rejection of the tab-close variant.
5. Resource-exhaustion bounds: free-text length cap, single-flight request queue, per-request
   wall-clock deadline, maximum output size.
6. Emit `loopback-tests.xml` in the shape EP-50's evidence bundle expects.

## Verification / acceptance (sketch)

- Every control ID in `threat-model.md` resolves to at least one failing-case test; a scripted
  cross-check fails if a control has no test.
- The emitted CSP string is byte-identical to the one recorded in `threat-model.md`, and the only
  fetch directive it permits is `connect-src 'self'`.
- The whole suite passes a second time with scripting disabled, exercising the no-JS fallback path
  (D-68) — including Quit.
- The full adversarial suite runs in CI on the deterministic no-model path (D-42) and produces its
  evidence file.
- *(judgement, owner)* The residual-exposure paragraph is honest about what a local process can
  still do.

## Parked → final-roadmap.md

- Per-request authentication, multi-user support, or anything that treats loopback as a boundary.
- Post-v1 contributor and PR-intake threat surface (D-34, revisited once reviewers exist).
