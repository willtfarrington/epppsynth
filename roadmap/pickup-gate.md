# Pickup gate — owner input required before EP-9 starts

Opened at **EP-8, 2026-09-01**, the P0 re-plan. Three items closed P0 unresolved, and **none can be
settled by a session**: two need a human to look at something no session can reach, and one is a
judgement that anyone who has read the tree is disqualified from making.

**How this file is used.** The session picking up EP-9 opens it because EP-9's header block says to,
puts all three gates to the owner **before doing any EP-9 work**, and records each answer where its
gate says. Gate 3 is **blocking** — it can change EP-9 before EP-9 is executed. Gates 1 and 2 do not
block EP-9's content, but they are answered or **explicitly deferred in writing**; skipping them
silently is the failure this file exists to prevent.

**When all three are resolved,** delete the pointer block from `roadmap/EP-9-registry-schema.md`
and replace this file's body with a dated record of the three answers. Do not delete the file: the
next phase re-plan should be able to see that the gate existed and how it closed.

This file is not a brief. It is named by EP-9's header, which is what puts it inside load-order
item 6 (*only the source files the brief names*) rather than inside EP-9's own token budget — the
load order has 46 tokens of slack at its tightest point (owner ruling **OD-16**), and a gate that
cost a brief its headroom would be a gate that forced the brief to be split.

---

## Gate 1 · OD-2 — does `SAFETY.md` §4 match the approved wording?

**The situation.** §4, *What it does not know*, was **authored** at EP-3 from D-8, D-14, D-18, D-25,
D-63 and D-79 — not copied. D-69 approved four blocks of public wording; three shipped
byte-identical to EP-2's recorded baselines and are asserted by tests. This is the fourth, and the
approved draft's only surviving copy is private planning state, which no session may open (D-2).

**It is therefore the one block of approved public safety-facing wording whose shipped text has
never been compared against what was approved.** That is why it is a gate and not a task.

**What the owner does.** Open the approved draft, read it against `SAFETY.md` §4, and choose:

| | Answer | What the session then does |
|---|---|---|
| **(a)** | **Confirmed** — the authored text says what was approved | Write a dated addendum under **D-69** recording that the block was authored at EP-3 and matches the approved draft. Tick **OD-2** in `roadmap/owner-decisions.md`. |
| **(b)** | **Replaced** — the owner supplies the approved wording | Replace §4 **verbatim** with the supplied text. Record the replacement in the D-69 addendum, naming what changed. Re-run `uv run pytest -q` (the byte-identity and banned-phrase assertions live in `epppsynth/tests/test_safety_charter.py` and `test_rights.py`) and re-run pre-publication **item 7**. |
| **(c)** | **Cannot be compared** — the draft is lost or too ambiguous to diff | Record that **permanently** in the D-69 addendum: the block ships as authored and no comparison will ever be made. Do not leave it open. "Check it later" about an artifact nobody can produce is a fiction, and shipping approved-looking safety wording that was never approved deserves to be visible rather than pending. |

**Do not paste unrelated `.local/` content into the session.** The verdict, or the replacement §4
text alone, is all that may cross.

---

## Gate 2 · OD-8 — does the issue form render, and do its checkboxes block submission?

**The situation.** `.github/ISSUE_TEMPLATE/discussion.yml` is published on the default branch, at
the path the platform reads issue forms from. It has **never been seen to render**, and no path
available to a session can see it: the REST route `repos/{owner}/{repo}/issues/templates` does not
exist (it 404s with a `documentation_url` pointing at *get-an-issue*, which is very likely what EP-4
actually hit); GraphQL's `repository.issueTemplates` returns an empty list and is not known to cover
YAML issue *forms* as distinct from markdown templates; and an unauthenticated fetch of the chooser
returns the sign-in interstitial, exactly as the private-vulnerability-reporting form does.

**What the owner does.** Signed in, open

`https://github.com/willtfarrington/epppsynth/issues/new/choose`

and confirm three things:

1. a card titled **Discussion** appears, described *"Discussion only — not support, and never
   clinical advice."*;
2. opening it shows the markdown preamble — no clinical advice · no real patient, family, trainee or
   employee information · not a support channel · security reports go to the private path;
3. under **Before opening** there are **two checkboxes**, and **submission is blocked until both are
   ticked**.

Point 3 is the one that matters most and the one nobody has ever exercised. EP-4 asserted the
behaviour from the file's `required: true`; a file is not a rendering.

| | Answer | What the session then does |
|---|---|---|
| **(a)** | **All three behave** | Tick **OD-8** with the dated observation, naming what was seen. |
| **(b)** | **Renders, but submission is not blocked** | **A finding, not a tick.** EP-4's `required: true` claim is false as shipped. Open a new owner-decision row, and treat the acknowledgements as needing another home — a required textarea, or wording moved into the body where it cannot be skipped. |
| **(c)** | **Does not render at all** | The platform is not reading the file. Investigate before any further public claim about intake; `CONTRIBUTING.md`, `SECURITY.md` and `README.md` all describe an intake path that would not exist. |

---

## Gate 3 · EP-8 acceptance 12 — is EP-9 executable by a cold session? · **blocking**

**The situation.** EP-8's twelfth acceptance criterion reads: *"Handing any one P1 brief to a cold
session, with only the load order files, is sufficient to execute it."* It is marked
*(judgement — the project owner)*, and the session that executed EP-8 **could not rule it**: it had
read the whole tree, which is the one condition the criterion excludes. The owner held it open to
read EP-9 first.

**What the owner does.** Read, in this order and nothing else: `CLAUDE.md` →
`epppsynth/GOVERNANCE.md` → the `DECISIONS.md` **index block** → the **P1 table and its
standing-decisions paragraph** in `roadmap/README.md` → `roadmap/EP-9-registry-schema.md`. Judge the
brief **below its pointer block**; the pointer and this file are scaffolding and are not part of
what is being judged.

The question is not *"is this brief good?"* It is: **could a session that has read only those five
things execute it without opening anything the brief does not name?**

| | Answer | What the session then does |
|---|---|---|
| **(a)** | **Pass** | Record the verdict **and its basis** in `roadmap/owner-decisions.md` and append it to EP-8's completion note. A verdict without a basis is not evidence. |
| **(b)** | **Fail** | Name what was missing. Amend **EP-9 before executing it** — this is why the gate blocks. Then fix the cause, not just the instance: if the gap is a convention nobody wrote down, it belongs in `roadmap/_TEMPLATE.md`; if it is a file the load order should have named, it belongs in the load order. |
| **(c)** | **Unjudgeable** | Retire the criterion with its reason recorded, so that no later re-plan quietly re-opens a question nobody can answer. Note that the same criterion recurs at every phase re-plan, so retiring it here retires a pattern. |

---

## Why these three are grouped

They are not related by subject. They are related by **who can answer them**, which is the only
thing that matters for a gate: each one needs a human to do something no session can — open a
private draft, sign in to a web page, or read a brief without having read everything around it.
Every other item EP-8 opened was ruled on 2026-09-01 and closed.
