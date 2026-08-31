<!-- GENERATED FILE. Do not edit by hand. -->
<!-- Source: epppsynth/registry/sources.yaml · Generator: epppsynth.rights.render -->

# Rights and reuse, per source

**This file is generated.** Its source of truth is
[`../registry/sources.yaml`](../registry/sources.yaml) and its generator is
`epppsynth.rights.render`. Edit the YAML, never this file, and regenerate with, from
`epppsynth/`:

```
uv run python -m epppsynth.rights.render
```

Regenerating and then finding a diff here is a build failure, not a discrepancy for somebody to
notice later.

## Why this file exists

This project's conceptual substrate is copyrighted and its repository is public. D-10 keeps both
facts true by splitting the problem in two. The **public** artifact is hand-authored original prose
that cites its sources and reproduces none of them. The **local** path builds a gitignored index
from a copy the reader lawfully holds, and ships nothing derived from it. Neither path works if
nobody records, per source, which one it is on.

So this table is not documentation of a policy. It is the policy, in the form a check can read:
`epppsynth.rights` refuses to generate this file, and EP-6 will refuse to build, when a rule below
is broken.

Nothing here has been reviewed by counsel. It is issue-spotting.

## Summary

| source | kind | reuse class | in local index | may redistribute | terms checked |
|---|---|---|---|---|---|
| `ahrq-patient-engagement-materials` | source-family | `reference-only-pending-rights-check` | no | no | **no** |
| `fda-cds-final-guidance-2026` | work | `reference-only` | no | no | **no** |
| `moral-injury-literature` | source-family | `owner-copy-read-as-input` | no | no | 2026-08-31 |
| `samhsa-trauma-informed-approach-2014` | work | `reference-only-pending-rights-check` | no | no | **no** |
| `serious-illness-communication-literature` | source-family | `owner-copy-read-as-input` | no | no | 2026-08-31 |
| `who-lmm-guidance-2024` | work | `reference-only` | no | no | 2026-08-23 |
| `yalom-existential-psychotherapy-1980` | work | `owner-copy-read-as-input` | yes | no | 2026-08-31 |


## How to read a row

Each source below carries three plain-language lines, and they are the point of the file:

- **May** — what this project is permitted to do with the source.
- **May never** — what it is not, including the things that would be easy to do by accident.
- **Checked** — whether anyone has confirmed the source's reuse terms against the rights holder's
  own statement, and on what date. `No` means no. It does not mean *probably fine*.

The remaining fields are the machine-readable form of the same three answers, and are validated
against a closed enumeration on load, so a value nobody anticipated is a failure rather than a
pass-through.

## Rights verified

Verified means somebody recorded what they checked, when, and against what. Read each note
before relying on a row: some of these verify a posture that needs no permission - original
prose plus citation, nothing reproduced - rather than a licence somebody granted, and each one
says which it is.

### `moral-injury-literature`
**The moral-injury literature.** A family of sources, not a single publication.

*Scope.* The mode (c) substrate. Definitionally contested: competing definitions were developed
for different populations and do not transfer cleanly, which EP-14 records as a property of the
literature rather than as a problem to resolve by choosing one. The project's charter clause is
that moral injury arises from conditions, not individual deficiency.

**May** — be read as input while this project authors original prose about it; and be cited in
public documentation, with a chapter-level locator and nothing finer.

**May never** — be redistributed, republished, or have any of its text shipped in this
repository or in anything this project emits; enter the local derived index; be quoted beyond 25
words in one quotation or 150 words in total; and be cited with a page range, have a chapter
title reused as a concept label, or be given a sequence of locators that reconstructs its
outline.

**Checked** — Yes, on 2026-08-31. What was checked is in the note below; read it before relying
on this row.

| field | value |
|---|---|
| rights holder | The respective publishers and authors of each work |
| access basis | `open-access` |
| licence | `unknown` |
| reuse class | `owner-copy-read-as-input` |
| permitted use | `read-as-input`, `short-citation-in-docs`, `redistribution-none` |
| redistribution | `none` |
| quotation budget | 25 words per quote |
| source budget | 150 words in total |
| locator granularity | `chapter` |
| in local index | no |
| redistributable | no |
| verified at | 2026-08-31 |

*Note.* Verified on the same basis as the serious-illness communication family on 2026-08-31:
original prose plus citation, nothing reproduced, no reuse permission relied on or claimed.
Per-work licences vary and are not enumerated. Nothing from this family enters the local index.

### `serious-illness-communication-literature`
**The serious-illness communication evidence base.** A family of sources, not a single
publication.

*Scope.* Peer-reviewed trials and syntheses of serious-illness communication, including the
null-to-adverse results GOVERNANCE.md §11 records: a randomised trial of simulation-based
training that found no improvement in patient- or family-reported communication quality and a
significant increase in patient depressive symptoms, and a structured-guide trial null on both
coprimary patient outcomes. Individual articles are cited from the concept registry, each under
its own terms; the family is the unit of the rights record because no single article is the
source.

**May** — be read as input while this project authors original prose about it; and be cited in
public documentation, with a chapter-level locator and nothing finer.

**May never** — be redistributed, republished, or have any of its text shipped in this
repository or in anything this project emits; enter the local derived index; be quoted beyond 25
words in one quotation or 150 words in total; and be cited with a page range, have a chapter
title reused as a concept label, or be given a sequence of locators that reconstructs its
outline.

**Checked** — Yes, on 2026-08-31. What was checked is in the note below; read it before relying
on this row.

| field | value |
|---|---|
| rights holder | The respective publishers and authors of each article |
| access basis | `open-access` |
| licence | `unknown` |
| reuse class | `owner-copy-read-as-input` |
| permitted use | `read-as-input`, `short-citation-in-docs`, `redistribution-none` |
| redistribution | `none` |
| quotation budget | 25 words per quote |
| source budget | 150 words in total |
| locator granularity | `chapter` |
| in local index | no |
| redistributable | no |
| verified at | 2026-08-31 |

*Note.* What is verified is the posture, not a licence. This project reads these articles,
writes original prose, and cites them; it reproduces no article text, so no reuse permission is
relied on and none is claimed. Per-article licences vary and are deliberately not enumerated
here — enumerating them would imply a permission the project neither has nor needs. The licence
field is therefore unknown while verified_at is set: the row's claim is that nothing is reused,
and that claim was checked on 2026-08-31. Nothing from this family enters the local index.

### `who-lmm-guidance-2024`
World Health Organization, *Ethics and governance of artificial intelligence for health:
guidance on large multi-modal models*. World Health Organization, Geneva, 2024, first edition.

**May** — be cited in public documentation, with a chapter-level locator and nothing finer.

**May never** — be redistributed, republished, or have any of its text shipped in this
repository or in anything this project emits; be ingested — it is referenced and never ingested,
so no wording of it may inform text that ships under CC BY 4.0; enter the local derived index;
be quoted beyond 25 words in one quotation or 150 words in total; and be cited with a page
range, have a chapter title reused as a concept label, or be given a sequence of locators that
reconstructs its outline.

**Checked** — Yes, on 2026-08-23. What was checked is in the note below; read it before relying
on this row.

| field | value |
|---|---|
| rights holder | World Health Organization |
| access basis | `open-access` |
| licence | `CC-BY-NC-SA-3.0-IGO` |
| reuse class | `reference-only` |
| permitted use | `short-citation-in-docs`, `redistribution-none` |
| redistribution | `none` |
| quotation budget | 25 words per quote |
| source budget | 150 words in total |
| locator granularity | `chapter` |
| in local index | no |
| redistributable | no |
| verified at | 2026-08-23 |

*Note.* Licence recorded on the authority of D-62, settled with the project owner at the
planning session of 2026-08-23; it was not independently re-confirmed against the publisher's
record in this session. The licence is non-commercial and share-alike, so ingesting this
guidance into a CC BY 4.0 tree would be the licence contamination R-15 names. It is referenced
and never ingested, and this row grants no read-as-input permission for that reason. The
identifier is left null rather than recorded from memory: retrieval from the publisher's
repository returned HTTP 403 on 2026-08-31, so nothing here was confirmed against it.

### `yalom-existential-psychotherapy-1980`
Irvin D. Yalom, *Existential Psychotherapy*. Basic Books, 1980, first edition, ISBN
978-0-465-02147-5.

**May** — be read as input while this project authors original prose about it; be cited in
public documentation, with a chapter-level locator and nothing finer; and have spans held in the
gitignored local index, which is never committed and never leaves the machine.

**May never** — be redistributed, republished, or have any of its text shipped in this
repository or in anything this project emits; be quoted beyond 25 words in one quotation or 150
words in total; and be cited with a page range, have a chapter title reused as a concept label,
or be given a sequence of locators that reconstructs its outline.

**Checked** — Yes, on 2026-08-31. What was checked is in the note below; read it before relying
on this row.

| field | value |
|---|---|
| rights holder | Irvin D. Yalom / Basic Books |
| access basis | `owner-purchased-copy` |
| licence | `all-rights-reserved` |
| reuse class | `owner-copy-read-as-input` |
| permitted use | `read-as-input`, `short-citation-in-docs`, `redistribution-none` |
| redistribution | `none` |
| quotation budget | 25 words per quote |
| source budget | 150 words in total |
| locator granularity | `chapter` |
| in local index | yes |
| redistributable | no |
| verified at | 2026-08-31 |

*Note.* Rights posture verified from first principles on 2026-08-31, which is what is verifiable
here: the work is in copyright, the author holds a purchased copy, and holding a copy confers no
right to redistribute, embed, train on, or publish derivatives of it. This row therefore claims
nothing beyond reading it as input and citing it. The bibliographic record — author, title,
year, publisher, ISBN — was checked against Open Library on 2026-08-31. The derived index built
from this copy is gitignored and lives outside the working tree; no span from it is ever
emitted, exported or committed (D-16, D-23).

## Rights not yet verified

Nobody has read the reuse terms of the sources below. They are listed apart from the rest for one
reason: a table that mixes checked and unchecked rows implies a uniformity it does not have, and a
reader skimming for a green light would find one.

Until a row here is cleared, it may be cited and may not be ingested, and **no public
intended-use, regulatory-status or reuse claim may rest on it**. Clearing them is an owner-gated
reading task carried as a P1 blocker, not a nice-to-have.

### `ahrq-patient-engagement-materials`
**Agency for Healthcare Research and Quality materials on patient and family engagement and
shared decision-making.** A family of sources, not a single publication.

*Scope.* Recorded as a family because the specific items this project will draw on are not yet
fixed. Naming one document here would imply a selection nobody has made. The family is narrowed
to named items by the owner-gated rights packet, at which point this row is split.

**May** — be cited in public documentation, with a chapter-level locator and nothing finer.

**May never** — be redistributed, republished, or have any of its text shipped in this
repository or in anything this project emits; be ingested — it is referenced and never ingested,
so no wording of it may inform text that ships under CC BY 4.0; enter the local derived index;
be quoted beyond 25 words in one quotation or 150 words in total; and be cited with a page
range, have a chapter title reused as a concept label, or be given a sequence of locators that
reconstructs its outline.

**Checked** — **No. Nobody has checked this source's reuse terms.** No public claim may rest on
it, and it may not be ingested. The note below records what was attempted and what was observed.

| field | value |
|---|---|
| rights holder | Agency for Healthcare Research and Quality (US Department of Health and Human Services) |
| access basis | `government-work` |
| licence | `unknown` |
| reuse class | `reference-only-pending-rights-check` |
| permitted use | `short-citation-in-docs`, `redistribution-none` |
| redistribution | `none` |
| quotation budget | 25 words per quote |
| source budget | 150 words in total |
| locator granularity | `chapter` |
| in local index | no |
| redistributable | no |
| verified at | **never** |

*Note.* UNVERIFIED, on the same basis as the SAMHSA row and by the same D-62 ruling: retrieval
returned HTTP 403 at the planning session of 2026-08-23, and no rights statement has been read.
Two things are unknown here rather than one — which items the project will use, and what those
items permit. Held at reference-only-pending-rights-check until both are settled.

### `fda-cds-final-guidance-2026`
United States Food and Drug Administration, *Clinical decision support software — final
guidance, superseding the 2022 guidance*. United States Food and Drug Administration, 2026,
final guidance issued 2026-01-06.

**May** — be cited in public documentation, with a chapter-level locator and nothing finer.

**May never** — be redistributed, republished, or have any of its text shipped in this
repository or in anything this project emits; be ingested — it is referenced and never ingested,
so no wording of it may inform text that ships under CC BY 4.0; enter the local derived index;
be quoted beyond 25 words in one quotation or 150 words in total; and be cited with a page
range, have a chapter title reused as a concept label, or be given a sequence of locators that
reconstructs its outline.

**Checked** — **No. Nobody has checked this source's reuse terms.** No public claim may rest on
it, and it may not be ingested. The note below records what was attempted and what was observed.

| field | value |
|---|---|
| rights holder | United States Food and Drug Administration |
| access basis | `government-work` |
| licence | `unknown` |
| reuse class | `reference-only` |
| permitted use | `short-citation-in-docs`, `redistribution-none` |
| redistribution | `none` |
| quotation budget | 25 words per quote |
| source budget | 150 words in total |
| locator granularity | `chapter` |
| in local index | no |
| redistributable | no |
| verified at | **never** |

*Note.* UNVERIFIED, and unverified in the way that matters most: nobody on this project has read
this document. D-62 records it as issued 2026-01-06 and superseding the 2022 guidance, and
requires that it be read before any public intended-use language ships. That is an owner-gated
reading task, not a code task, and it is carried as a P1 blocker rather than as a nice-to-have.
Until it is done, no public text may make or imply a regulatory-status claim. Its reuse terms
are also unread, so the licence is recorded as unknown rather than presumed to be a
public-domain federal work.

### `samhsa-trauma-informed-approach-2014`
Substance Abuse and Mental Health Services Administration (US), *SAMHSA's concept of trauma and
guidance for a trauma-informed approach*. Substance Abuse and Mental Health Services
Administration, Rockville, MD, 2014, HHS Publication No. (SMA) 14-4884.

**May** — be cited in public documentation, with a chapter-level locator and nothing finer.

**May never** — be redistributed, republished, or have any of its text shipped in this
repository or in anything this project emits; be ingested — it is referenced and never ingested,
so no wording of it may inform text that ships under CC BY 4.0; enter the local derived index;
be quoted beyond 25 words in one quotation or 150 words in total; and be cited with a page
range, have a chapter title reused as a concept label, or be given a sequence of locators that
reconstructs its outline.

**Checked** — **No. Nobody has checked this source's reuse terms.** No public claim may rest on
it, and it may not be ingested. The note below records what was attempted and what was observed.

| field | value |
|---|---|
| rights holder | Substance Abuse and Mental Health Services Administration (US Department of Health and Human Services) |
| access basis | `government-work` |
| licence | `unknown` |
| reuse class | `reference-only-pending-rights-check` |
| permitted use | `short-citation-in-docs`, `redistribution-none` |
| redistribution | `none` |
| quotation budget | 25 words per quote |
| source budget | 150 words in total |
| locator granularity | `chapter` |
| in local index | no |
| redistributable | no |
| verified at | **never** |

*Note.* UNVERIFIED. Retrieval of the publisher's own rights statement returned HTTP 403 at the
planning session of 2026-08-23 (D-62), and no statement has been read since; a further attempt
on 2026-08-31 was redirected and not followed to a rights page. A US federal agency publication
is commonly assumed to be a public-domain government work, and that assumption is exactly what
this row refuses to make: the material may incorporate third-party content under separate terms,
and an unverified federal text ingested into a CC BY 4.0 tree is the licence contamination R-15
names. Held at reference-only-pending-rights-check until an owner-gated rights packet clears it.
The publication number above is recorded as commonly cited and is itself unconfirmed.

## Standing rules, which apply to every source above

- **Citations are chapter-level locators only** (D-74). No page ranges. A journal article's own
  page span belongs to its bibliographic identity and is permitted in a source record's citation
  field; it stays forbidden in a concept's short citation.
- **Quotation budget: 25 words per quote,
  150 words per source.** A row may set a stricter budget and may never
  set a looser one; the loader rejects a row that tries.
- **No quoted phrase, and no chapter title, is used as a concept label**, and no sequence of
  locators may reconstruct a source's outline. A book's title plus its chapter list is a
  navigable derivative of that book.
- **Verbatim spans never leave the local index.** They are never emitted, exported, screenshotted
  or serialized, and no exportable type has a field to put one in. That is enforced by the type
  graph, not by discipline (D-23).
- **Normative guidance under a non-commercial or share-alike licence is referenced, never
  ingested** (D-62). Ingesting one into a CC BY 4.0 tree is licence contamination, and it is
  expensive to unwind after the fact rather than merely embarrassing.

## Where the repository's own licences are recorded

This file covers the **sources** the project reads. The licences of the repository's own files are
a separate question, answered by [`../../REUSE.toml`](../../REUSE.toml) — the machine-readable
boundary — and restated in prose in [`../../NOTICE`](../../NOTICE).
