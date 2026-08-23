# EP-40 — Loopback application shell

**Size:** M · **Mode:** a · **Core/Stretch:** core ·
**Depends on:** EP-38 (threat model), EP-39 (UI contract, copy deck, banned-phrase lint) ·
**Blocks:** EP-41 (loopback security controls), EP-42 (input form), EP-44 (escalation panel), EP-46
(verification, accessibility packet, re-plan P5)

> **Charter.** Scope and acceptance below are sketches. **EP-37** (reviewer recruitment pack,
> re-plan P4) upgrades this to a full brief: `## Scope sketch` splits into `## In scope` /
> `## Out of scope`, and each criterion becomes a named command or artifact. Do not execute from the
> sketch alone.

## Context

The first line of UI code in the project. It stands up the page, the base template, the CSS, the
vendored script and the launch command — and nothing else. The form, the panels and the security
controls are separate briefs so each is reviewable on its own terms.

The stack is settled (D-68): **Starlette + Jinja2 server-rendered HTML + one vendored copy of htmx
(0BSD, version pinned, SHA-256 recorded in `NOTICE`) + hand-written CSS.** No npm, no build step, no
CDN, no fonts fetched, no component library. htmx is the only front-end dependency and it is
**optional**: a **tested** no-JS full-page-POST fallback is mandatory, so the failure mode of the
script not loading is a working application rather than a broken one. The divergence from the sibling
Streamlit precedent is deliberate and rests on architectural control over the DOM, not on any
verified accessibility claim about Streamlit.

Templates are **CSP-clean from the first commit** — no inline `<style>`, no inline `<script>`, no
inline event handlers — because EP-38 has already fixed `default-src 'none'`, and retrofitting a CSP
onto inline handlers is a rewrite. The eight loopback controls are specified but not implemented;
EP-41 owns them, and this brief must not leave a temporary permissive header behind for it to tighten.

## Safety preconditions

- **D-8, no runtime network.** System font stack, inline SVG, no remote image, no analytics, no
  telemetry, no crash reporting. Proved properly in EP-46; asserted opportunistically here.
- **D-8, no retention.** `Cache-Control: no-store` and `Referrer-Policy: no-referrer` on every
  response; no session file, no log of prompts or outputs, no writable path inside the repository.
- **R-38.** The launch interstitial repeats the excluded uses on every launch, so a third party who
  runs the app from the public repository cannot miss that it is not validated (D-33).
- **Public artifact (D-3).** Pre-publication checklist items 4 (local paths, hostname, username must
  never appear in a rendered page, an error page or a title bar), 5 (screenshots) and 6 (licence
  conformance — `NOTICE` gains the htmx entry with its vendored path, version and hash).
- **R-39 (pressure to use it on a real case).** v1 is fictional-only, so the tool has no legitimate
  place in the workflow it was designed around — which is exactly the pressure that produces a
  real-case use. Guard: the launch interstitial repeats the exclusion every launch, and no input
  affordance invites patient-identifying text.

## Scope sketch (refine at re-plan)

1. `epppsynth/src/epppsynth/ui/` — Starlette app; `GET /` renders the whole page server-side; the
   state-changing route is reachable by the no-JS path as a full-page render.
2. Base Jinja2 template with EP-39's three regions in DOM order and skip links to waypoints and to
   escalation; the "nothing you type is saved" header line.
3. Vendored `htmx.min.js` at a pinned version, served from `'self'`, hash recorded in `NOTICE`.
4. Hand-written CSS: system font stack; single column at narrow widths with escalation placed above
   waypoints; no fixed heights on text containers; `prefers-reduced-motion` respected globally; no
   animation anywhere in the waypoints region.
5. Emit the security-header set exactly as EP-38 specified it, so EP-41 tests an existing set.
6. `epppsynth ui` CLI subcommand; the first-run interstitial on **every** launch (D-60) — there is no
   persistence with which to remember a dismissal, and the friction is the safety feature.
7. Measure p95 render on the deterministic path (A-9). Above roughly 400 ms a static "Working" text
   is permitted — never a spinner, a progress indicator or a streaming reveal.
8. **Provision the accessibility dev-dependencies — in scope here, because EP-42 is the first brief
   whose acceptance calls them and EP-46 (which builds the packet) runs last.** Add the axe-core
   driver and its browser automation to a `dev` dependency group in `pyproject.toml`, hash-locked in
   `uv.lock` like every other dependency, and run the browser-binary download **once**, explicitly,
   recording the versions and the on-disk size in the completion note.
   This is a **development-time acquisition, not a runtime dependency**, and the distinction is the
   whole point of putting it here rather than leaving it implicit: EP-1's empty-runtime-dependency
   posture is unchanged, the shipped application still has no front-end build and no runtime
   package beyond the vendored htmx, and a test asserts that nothing in the `dev` group is
   importable from `epppsynth.ui` at runtime. The browser binaries live outside the repository, are
   gitignored, and are excluded from the D-78 project ceiling in the same way the third-party model
   cache is (D-71) — record their footprint in the storage inventory rather than silently growing
   it. CI keeps running the deterministic no-model path (D-42); the axe pass is a local dev job
   unless and until EP-46 decides otherwise, and this brief writes down which it is.
   Smoke test: one axe-core run against the empty shell page, green, so the tooling is proven
   working before EP-42 depends on it.

## Verification / acceptance (sketch)

- The page renders and the form round-trips **with JavaScript disabled** — a named test, not a claim.
- A scripted assertion finds no inline `style` attribute, no inline `<script>` and no `on*` handler in
  any rendered response.
- The listener binds to the loopback interface only; a bind on any other interface fails the suite.
- `NOTICE`'s recorded htmx hash equals the hash of the vendored file (scripted).
- p95 render recorded in the completion note together with the decision it drove.
- `uv run` executes one axe-core check against the shell page and it is clean; the dev-group
  versions and the browser-binary footprint are recorded; `uv sync --no-dev` still produces a
  working `epppsynth ui`, asserted, so the accessibility tooling is provably development-time only.

## Parked → final-roadmap.md

- Any second page, any navigation, any client-side routing.
- The fictional scenario-library UI (v1.x, D-32).
