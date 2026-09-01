---
Title: "Documentation — Changelog"
Status: Proposed
Start Date: 2026-07-25
ID: 496040
---

# Documentation — Changelog
This document specifies the Changelog facet: a companion file, named `<base-filename>.changelog.md`, that records why and how its paired artifact changed over time. The paired artifact is not necessarily a document — it can be an image, a piece of code, or anything else a change history is worth keeping for. See [Documentation](./documentation.md) for what a facet is.

**Exception**: a Changelog-facet file does not itself get a companion changelog. This is a deliberate stop to the recursion, not an oversight — see Discussion. (This exception applies to Changelog-facet files — the `.changelog.md` companions — not to this specification itself, which is an Explanation-facet document and does have a companion changelog: [documentation-changelog.changelog.md](./documentation-changelog.changelog.md).)

## Abstract
A Changelog-facet document is an append-only, chronologically-ordered record of changes to one paired artifact. It is not a substitute for other organizational records — chat transcripts, meeting recordings, decision threads — and does not try to preserve those in full; it keeps only a concise, minutes-style summary of each change: what changed, why, on what evidence, who did what, and what else it should affect. Everything that used to live in a base document's own front matter as `Citations`, `Contributors`, and `Applied to` now lives here instead, since a reader of the base artifact needs its current state, not its provenance — provenance belongs in history, and history belongs here.

## Introduction
### Motivation
Base documents were accumulating two kinds of front-matter weight that their actual readers don't need: a full contributor roster (irrelevant to understanding the subject the document describes) and a citations list whose only real purpose was justifying past decisions (relevant only when auditing history, not when reading the current design). Both are pure cognitive and token cost to a reader who just wants to understand the subject. Separating them out keeps base documents lean and keeps this file's purpose narrow and honest: a historical record, not a second copy of the design itself.

## Explanation

### File format
A Changelog-facet file has no YAML front matter — just a plain H1 title, following the pattern `# {Base Document's Title} Changelog` (e.g. `documentation-explanation.md`, titled "Documentation — Explanation", pairs with `documentation-explanation.changelog.md`, titled "Documentation — Explanation Changelog"). Everything else in this specification — `## Changelog` and its entries, `CONTRIBUTORS.md` references — is body content beneath that title; there is no `Status`, `Start Date`, or `ID` to track, since a changelog never reaches a settled "design" the way an Explanation-facet document does.

### Changelog scope
A changelog is paired to a **base artifact**, not to each file that belongs to the artifact's topic. The base artifact's Practice-facet companion (`<base>.practice.md`) is part of that topic: changes to the companion are recorded in the base artifact's changelog, and the companion never receives a changelog of its own. Each entry's `Summary` names which file or files the change touched, so a reader can find one file's history inside the shared ledger.

A boundary note on the pattern: the companion rule keys on the **dot** — `modeling.practice.md` is a companion of `modeling.md` — and does not reach hyphenated standalone documents that merely end in "practice" or similar. `documentation-practice.md`, the Practice facet's own governing specification, is an independent base artifact, not a companion of `documentation.md`; its changelog remains its own `documentation-practice.changelog.md`.

This is the same recursion stop the facet already applies to changelog files themselves (a `.changelog.md` file gets no companion changelog), extended one step: a practice companion is not an independent artifact whose history stands apart from the thing it procedures — it is the base topic's how-to half, and its changes usually follow from the base document's changes, so one ledger keeps that causal link locally visible instead of splitting it across two files that must reference each other.

#### Discussion

##### Rationale and alternatives
- **A separate changelog per practice file (rejected)**: the coupling between a base specification and its procedure runs one way — a companion's changes exist to keep it in line with the base artifact's changes — so per-file changelogs either duplicate the same change as two entries or split one narrative across two ledgers referencing each other, and they multiply files for no reader benefit.
- **Extend the sharing rule to Handoff companions now (rejected for now)**: a handoff is mutable working state rather than a procedure, and whether its churn is worth changelog history at all is an open question in the Handoff facet ([documentation-handoff.md → Unresolved questions](./documentation-handoff.md#unresolved-questions)); deciding it here would preempt that question without new evidence.

##### Unresolved questions
The boundary note above keys the companion rule on the dot, with hyphenated standalone documents as counter-examples. If a future document legitimately falls between the two patterns — a hyphenated name that *is* a companion, or a dotted name that is not — the rule needs a principled criterion (for example, derivability of the relationship from the name alone) rather than case-by-case judgment.

### Structure
All entries live under a single `## Changelog` heading — never one `##` per entry — so the top-level heading list stays small and stable even as entries accumulate indefinitely. Entries are ordered chronologically, oldest first, so a contributor appends the next entry at the end of the file without needing to search for where it goes. Each entry is a `###` with a short, descriptive title (not a timestamp — see Rationale and alternatives). Directly under the title, a short list of metadata bullets — mirroring how a document's own YAML front matter holds its short, structured facts separately from its prose body; an entry's bullets are that same idea at entry scale. Actual content (`Summary`, and optionally `Rationale and alternatives`) follows as real `####` headings, since it's prose, not metadata:

```
## Changelog

### {short, descriptive title of the change}
- Time: {ISO 8601 timestamp, e.g. 2026-07-25T14:00:00Z}
- Type: {optional, free text — see Type below}
- Cited:
  - [{Title}]({URI}) — {Relation}: {why this source was used as evidence for this change}
- Propagates to:
  - {Other artifact}: {Pending | Done | Rejected} — {what needs to happen there, or why it was rejected}
- Tasks:
  - {Task reference (URI or identifier)}: {Closed | Partial | Reference} — {why}
- Contributors:
  - [{Name}](../CONTRIBUTORS.md#{name}) — {role}: {what — see [Contributors](#contributors-entry-field) for the role vocabulary}

#### Summary
{what changed and why, concise — this is the one field nearly every entry has}

#### Rationale and alternatives
{optional — for a change substantial enough to have had real arguments for and against, or rejected alternatives; omit for small or uncontested changes}
```

A small wording fix from one person needs almost none of this — `Summary` and a one-line `Contributors` bullet are enough.

#### Discussion
##### Rationale and alternatives
- **Timestamp as the entry's own `###` heading (an earlier draft; not chosen)**: put a machine-format string where a human-scannable title should be, and gave no better way to identify an entry in conversation ("the change from `2026-07-25T14:00:00Z`" is a worse handle than a short title). Time is a fact about the entry, not its identity, so it moved into a `Time` bullet in the body instead.
- **A `####` heading for every field, including the short metadata ones (an earlier draft; not chosen)**: gave each field its own anchor, but for fields that are genuinely metadata about the entry (`Time`, `Type`, `Cited`, `Propagates to`, `Tasks`, `Contributors`) rather than its content, a heading is more structural weight than the field needs — nobody links directly to "the Time field of entry X." Grouping them as bullets directly under the entry's own title mirrors the same split already used at the whole-document level, between YAML front matter (short, structured facts) and the Markdown body (prose, real headings) — the same distinction, just applied one level down, to a single entry instead of a whole file. `Summary` and `Rationale and alternatives` keep real `####` headings, since they are the entry's actual content.

### CONTRIBUTORS.md
A single, project-wide file — not paired to any one artifact — listing every contributor across the whole project. Each contributor gets their own `##` heading, named after them (e.g. `## Omid Hekayati`), directly linkable from any changelog entry (`../CONTRIBUTORS.md#omid-hekayati`) instead of repeating identity data in every file. Underneath, an open, non-exhaustive list of bullets — `URI` (one or more: email, personal site, a social profile), `Donate` (a tip/coffee link), a short optional `Bio`, or anything else a contributor wants recorded about themselves. This list is not closed; a contributor may add a bullet field for themselves that isn't one of these examples.

```markdown
## Omid Hekayati
- URI: mailto:omid@geniuses.group
- URI: https://geniuses.group
- Donate: https://...
- Bio: Lead architect of the Memar framework.

## Claude
- Models:
  - [claude-opus-5]()
  - [claude-sonnet-5]()
  - [claude-fable-5]()
```

For an AI contributor, only `Name` and the officially documented `Model` identifier are recorded here as stable facts. `Effort`, and anything else that can genuinely vary between one contribution and the next, belongs inline in that specific changelog entry's own `Contributors` bullet instead (e.g. "Claude (claude-sonnet-5, extended thinking) — rewrote: ..."), not here.

The same preservation rule as elsewhere applies: while a contributor is still actively working on any unfinished (non-`Final`) artifact, they may add or extend their own entry here; no one edits another's entry.

### Contributors (entry field)
Each changelog entry's `Contributors` bullet names who was involved and what role they played, as a link to that person's `CONTRIBUTORS.md` heading. The role vocabulary is intentionally open, not a closed list — `claimed`, `argued`, `reviewed`, `rewrote`, `tested`, `approved`, and `requested` are common examples, not the only ones. A more formal, fixed role taxonomy exists in academic publishing (the CRediT — Contributor Roles Taxonomy — system, with roles like Conceptualization, Writing, Supervision) as a model for how far this could be formalized if it's ever needed; nothing that granular is imposed here today.

### Type
Free text, not a controlled vocabulary — what counts as a meaningful category of change varies too much across artifact kinds to close this off. Two existing vocabularies are offered as a starting point, not a requirement: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)'s `Added`/`Changed`/`Deprecated`/`Removed`/`Fixed`/`Security`, and [Conventional Commits](https://www.conventionalcommits.org/)' `feat`/`fix`/`docs`/`style`/`refactor`/`perf`/`test`/`build`/`ci`/`chore`/`revert`. Both are written for software releases and commits specifically; a documentation change may need a word neither offers (e.g. "clarified," "merged," "split"). Use whichever word is most accurate, from either vocabulary or outside it.

### Cited
Replaces the base artifact's former `Citations` field, now describing what this specific change relied on, not a standing property of the base artifact. The `Relation` vocabulary and source-selection criteria are defined in [documentation.md → Citations](./documentation.md#citations) as cross-cutting concerns, applying wherever citations appear; this section covers only what is specific to a Changelog entry's `Cited` field. A source cited here does not need to be named anywhere in the base artifact's own body — citing it here is sufficient provenance. The one exception: if the base artifact's own body genuinely needs a source at the point a reader is reading it — not as evidence for a past decision, but as something the reader themselves needs to follow — link it directly and normally in the body itself, the same as any other hyperlink, never as an unlinked "see X" pointer.

### Propagates to
Replaces the base artifact's former `Applied to` field, and generalizes it: instead of one artifact declaring where its own design "landed," each change explicitly names every other artifact it should affect, with a status. `Pending` and `Rejected` are both closed, searchable states — a `Pending` entry is exactly what a future contributor (human or AI) should search for to find undone propagation work across the whole documentation set; `Rejected` closes that search result permanently once a propagation is considered and deliberately not done, with the reason recorded, so it doesn't keep surfacing as an open task.

#### Discussion
##### Rationale and alternatives
- **A single `Applied to` field on the base artifact, as before (rejected)**: could only express "where the current design already landed," not "what changes are still owed elsewhere," and couldn't distinguish which specific change a propagation obligation came from.
- **`Pending`/`Done` only, no `Rejected` (considered, not chosen)**: a propagation that's considered and deliberately declined would have no way to stop appearing as outstanding work in a future search.

### Tasks
An optional reference to an external task-tracking entry (however that ends up being modeled — this specification does not assume or require a specific Task system), with one of three relations: `Closed` (this change completes that task), `Partial` (this change is progress toward it but doesn't complete it), or `Reference` (mentioned for context, no completion claim either way).

## Results
Insufficient time has passed since this specification was adopted to report real, observed outcomes from its use. This section will be filled in once there is such experience to draw on.

## Discussion

### Rationale and alternatives
- **Giving a Changelog-facet file its own companion changelog (rejected)**: would recurse indefinitely (a changelog for the changelog, then a changelog for that changelog...) with no natural stopping point. Version control already records what changed in a changelog file itself, which is sufficient — the whole reason a Changelog facet exists for other artifacts is that version control alone doesn't capture *why*, but a changelog entry's own reason for existing *is* already "recording why," so the same gap doesn't recur one level up.
- **Treating Changelog as an ad-hoc per-document convention rather than a named Facet (rejected)**: this project's own Methodology warns against designing structure in the abstract, but it equally warns against leaving a real, repeated structural need unnamed. Once the same `<base>.changelog.md` pattern was being applied across multiple artifacts, naming it as a Facet — with its own governing specification, its own entry in `documentation.md`'s facet list, and the same extension mechanism the existing two facets already use — was the smaller conceptual cost than leaving it as implicit convention.

### Unresolved questions
1. How to handle historical entries migrated from a base document's former `## Change Rationale` section (which have no real timestamp, only relative order) is a process question, not a structural one — covered in `documentation-changelog.practice.md` rather than here.
2. Entry titles are short and author-chosen, with no uniqueness requirement — two entries could plausibly land on the same title, which would be ambiguous if ever linked to directly by anchor. Not addressed here; entries are expected to be found by reading top-to-bottom or full-text search, not by anchor, unless this becomes a real problem.
