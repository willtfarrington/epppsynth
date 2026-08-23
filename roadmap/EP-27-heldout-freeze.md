# EP-27 — Frozen held-out set, freeze ritual, contamination checks

**Size:** L · **Mode:** a · **Core/Stretch:** core ·
**Depends on:** EP-24 (eval harness, scenario schema, taxonomy) ·
**Blocks:** EP-29 (equity and coercion suites), EP-30 (abstention suites)

> **Charter.** **EP-23 (engine integration, fixtures, re-plan P2)** upgrades this to a full brief.
> The freeze ritual below is the sketch; the re-plan fixes the exact tag name and CI wiring.

## Context

Implements D-36's held-out tier and mitigates R-23 (held-out contamination). ~10–15 scenarios,
**author-written only**, authored **before any tuning run**, frozen under an annotated git tag, and
executed **at most once per release candidate**. It is the only evidence in the plan that the engine
generalises past the set it was built against; every mechanism here exists because that evidence is
worthless the moment the set leaks into development.

Timing matters and is easy to get wrong: this brief runs early in P3, in parallel with EP-25/EP-26,
and its authoring must **precede** the first tuning pass against the dev set. If the dev set has
already driven engine changes when this brief is picked up, say so in the completion note — the
freeze is still worth doing, but the claim it supports is weaker and the release note must say so.

**Repair rule (non-negotiable, D-36):** a held-out failure may be repaired only by changing the dev
set and re-authoring; never by editing the held-out case, and never by re-running the same slice
against the fix.

## Safety preconditions

- Author-written only. No LLM-generated case, and no case derived from a dev or red-team case, may
  enter the held-out set (D-36, R-23).
- Same public-safety envelope as every scenario: manifestly fictional, attestation required, no PHI,
  no real institution, no local path, hostname or username (D-3, D-8, D-42).
- The contamination checks are **blocking**, not advisory; a warn-level check requires a written,
  dated disposition, not a dismissal.
- The embedding-overlap check is **not built in P3**: no embedding model exists until P4 (EP-34
  selects one; EP-22 explicitly excludes embeddings from ingest). It is parked below as a P4
  follow-up. When it is built it will depend on the local corpus index, which lives outside the
  repository tree and never enters CI (D-16, D-51), so it will be skip-marked in CI and run locally
  only.
- The usage ledger is a public artifact and must carry build hashes and dates, not case content.

## Scope sketch (refine at re-plan)

1. Author ~10–15 held-out scenarios covering the same `expected_class` spread as the dev set, with
   their own near-miss negatives.
2. **Freeze ritual:** emit `heldout.manifest.sha256`; commit it; create an **annotated (unsigned)**
   git tag whose message carries the manifest hash; record the tag name, the tagged commit hash and
   the manifest hash in the roadmap and in `DECISIONS.md` as a dated addendum. Commit and tag
   signing is **parked in EP-0** and no `D-n` requires it, so the freeze must not depend on it: the
   integrity claim rests on the committed manifest hash plus the tag-to-commit binding, both of
   which CI re-checks. If the owner wants cryptographic provenance, provisioning a signing key is a
   **named prerequisite step for the owner**, recorded as a dated addendum before this brief runs
   — not something a session sets up in passing.
3. **CI assertions:** the manifest matches the files on disk; no held-out file's git history post-dates
   the freeze tag; any modification to a held-out file fails the build.
4. **Contamination checks, P3 scope:** (a) exact content-hash collision across sets ⇒ fail;
   (b) token-level Jaccard ≥ 0.6 between any held-out and any dev/red-team scenario ⇒ fail;
   (c) the **usage ledger**. The embedding-cosine check is deferred to P4 — see the parked section;
   (a) and (b) are the blocking checks for v1 and neither needs a model.
5. **Usage ledger:** an append-only record — date, build hash, release candidate, result summary —
   asserting at most one held-out run per release candidate.
6. Write the repair rule into `GOVERNANCE.md` (or confirm it is already there) and link it from the
   ledger, so the rule is reachable at the moment someone is tempted to break it.

## Verification / acceptance (sketch)

- The annotated tag exists, `git cat-file tag <tag>` shows the manifest hash in its message, and
  the tag resolves to the commit that contains that manifest; the manifest verifies against the
  tree. No `git verify-tag` step: nothing in the plan provisions a signing key.
- CI goes red on an injected near-duplicate at Jaccard ≥ 0.6 and on an edited held-out file.
- The ledger check fails when a second entry is appended for the same build hash.
- Running the held-out set emits the same result-schema artifact as every other suite, with the tag
  name and manifest hash recorded in it.
- *(judgement — author)* the held-out cases are not paraphrases of dev cases; a reader comparing the
  two sets would call them independently authored.

## Parked → final-roadmap.md

- **Embedding-cosine contamination check (former check (c)) — P4 follow-up.** Cosine ≥ 0.9 between
  a held-out and a dev/red-team scenario as a warn plus a written disposition. Cannot run in P3:
  EP-22 excludes embeddings from corpus ingest and EP-34 is where an embedding model is first
  selected. Re-open it at the P4 re-plan (EP-37) once a model exists, as a local-only,
  CI-skip-marked check; until then (a) and (b) carry the contamination claim and the completion
  note must say so.
- Signed freeze tags, once a signing key is provisioned. Depends on the signed-commit policy parked
  in **EP-0**; until then the manifest hash plus the tag-to-commit binding is the integrity claim.
- A second held-out slice for post-v1 release candidates (the ledger will exhaust this one).
- Automated authorship-style comparison between the sets — manual judgement for v1.
