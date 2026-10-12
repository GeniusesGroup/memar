---
Title: "Documentation — Changelog"
Status: Proposed
Start Date: 2026-07-25
ID: 496040
---

# Documentation — Changelog
This document specifies the Changelog facet: a companion file, named `<base-filename>.changelog.md`, that records why and how its paired artifact changed over time. The paired artifact is not necessarily a document — it can be an image, a piece of code, or anything else a change history is worth keeping for. See [Documentation](./documentation.md) for what a facet is.

**Exception**: a Changelog-facet file does not itself get a companion changelog. This is a deliberate stop to the recursion, not an oversight; the rejected alternative is recorded in [documentation-changelog.changelog.md](./documentation-changelog.changelog.md). (This exception applies to Changelog-facet files — the `.changelog.md` companions — not to this specification itself, which is an Explanation-facet document and does have a companion changelog: [documentation-changelog.changelog.md](./documentation-changelog.changelog.md).)

## Abstract
A Changelog-facet document is an append-only, chronologically-ordered record of changes to one paired artifact. It is not a substitute for other organizational records — chat transcripts, meeting recordings, decision threads — and does not try to preserve those in full; it keeps only a concise, minutes-style summary of each change: what changed, why, on what evidence, who did what, and what else it should affect. Everything that used to live in a base document's own front matter as `Citations`, `Contributors`, and `Applied to` now lives here instead, since a reader of the base artifact needs its current state, not its provenance — provenance belongs in history, and history belongs here.

The same reader-relationship makes this facet the home of two more content classes the base document's own relevance discipline ([documentation-explanation.md → Relevance discipline](./documentation-explanation.md#relevance-discipline)) excludes from the body: **decision-shaping context** — where and with whom positions were formed, which counter-arguments were weighed and why they were accepted or rejected, the chronology of a revision, the anecdotes and debates that shaped a decision — and **comparative prior-art surveys** (how other projects organize the same problem and how this project differed, as opposed to premise evidence, which stays cited inline at the claim it supports). This material is usually true and often valuable, but it serves the reader auditing how the current state came to be, not the reader understanding the state itself — so it belongs here, in the entry that made the change, not in the base document's body. Open questions are the third excluded class and go to the paired [Handoff](./documentation-handoff.md), not here — they are mutable current state, not history.

## Introduction
### Motivation
Base documents were accumulating two kinds of front-matter weight that their actual readers don't need: a full contributor roster (irrelevant to understanding the subject the document describes) and a citations list whose only real purpose was justifying past decisions (relevant only when auditing history, not when reading the current design). Both are pure cognitive and token cost to a reader who just wants to understand the subject. Separating them out keeps base documents lean and keeps this file's purpose narrow and honest: a historical record, not a second copy of the design itself.

## Explanation

### File format
A Changelog-facet file has no YAML front matter — just a plain H1 title, following the pattern `# {Base Document's Title} Changelog` (e.g. `documentation-explanation.md`, titled "Documentation — Explanation", pairs with `documentation-explanation.changelog.md`, titled "Documentation — Explanation Changelog"). Everything else in this specification — `## Changelog` and its entries, `CONTRIBUTORS.md` references — is body content beneath that title; there is no `Status`, `Start Date`, or `ID` to track, since a changelog never reaches a settled "design" the way an Explanation-facet document does.

### Changelog scope
A changelog is paired to a **base artifact**, not to each file that belongs to the artifact's topic. The base artifact's Practice-facet companion (`<base>.practice.md`) is part of that topic: changes to the companion are recorded in the base artifact's changelog, and the companion never receives a changelog of its own. Each entry's `What changed` section names which file or files the change touched, so a reader can find one file's history inside the shared ledger.

A boundary note on the pattern: the companion rule keys on the **dot** — `modeling.practice.md` is a companion of `modeling.md` — and does not reach hyphenated standalone documents that merely end in "practice" or similar. `documentation-practice.md`, the Practice facet's own governing specification, is an independent base artifact, not a companion of `documentation.md`; its changelog remains its own `documentation-practice.changelog.md`.

This is the same recursion stop the facet already applies to changelog files themselves (a `.changelog.md` file gets no companion changelog), extended one step: a practice companion is not an independent artifact whose history stands apart from the thing it procedures — it is the base topic's how-to half, and its changes usually follow from the base document's changes, so one ledger keeps that causal link locally visible instead of splitting it across two files that must reference each other.

### Changelog membership: what may be recorded here
An entry records an **event bearing on the artifact's state**, and the event need not be a change to the artifact's own text. Three kinds have no other home and belong here, and the last two have catalog sections of their own below:

1. **A change** to the artifact or its topic's companions — the ordinary case.
2. **A decision the artifact records but did not make**, and a question the artifact now carries as settled or settled-against, where the reasoning and the rejected alternative would otherwise have no home.
3. **A survey of what the artifact already holds** — an audit against an outside list, a comparison against a neighbouring project, a check that the documents already carry what an external source says — whose negative result is the finding. Nothing changed, and that is exactly why the result would be lost: a ledger entry is the only place a "we looked, and it is already there" can live without becoming either body text (which would be a second copy that drifts) or a handoff entry (which is work still to do).
4. **Material examined and deliberately not adopted**, with the reason.

The boundary against the [Handoff](./documentation-handoff.md) facet is the test each case passes: if the material is **still to be done**, it is a handoff entry, whatever else it is; if it is **settled, settled-against, or already held**, it is recorded here. A survey that produced open questions records the survey here and the questions in the handoffs that own them — which is why the catalog has a section for the survey and none for the questions.

### Structure
All entries live under a single `## Changelog` heading - never one `##` per entry - so the top-level heading list stays small and stable even as entries accumulate indefinitely. Entries are ordered chronologically, **oldest first**, so a contributor appends the next entry at the **end of the file** without searching for an insertion point. Newest-first ordering is forbidden: it forces every writer to read or rewrite the head of a growing file, and it is the failure mode this rule exists to prevent. Each entry is a `###` with a short, descriptive title (not a timestamp). Directly under the title, a short list of metadata bullets - mirroring how a document's own YAML front matter holds its short, structured facts separately from its prose body; an entry's bullets are that same idea at entry scale. Actual content follows as real `####` headings, since it's prose, not metadata.

**Appending without loading the file.** An agent writing a new entry must not open the changelog into context to discover where the entry goes — the answer is always end-of-file. Prefer `memar content changelog-append` (interface via its `--help`), which writes mechanically and only peeks at the file's tail for separator hygiene. Reading a prior entry remains legitimate when the work itself needs that history; reading the whole changelog solely to append is not.

```
## Changelog

### {short, descriptive title of the change}
- Time: {ISO 8601 timestamp, e.g. 2026-07-25T14:00:00Z}
- Type: {optional, free text - see Type below}
- Cited:
  - [{Title}]({URI}) - {Relation}: {why this source was used as evidence for this change}
- Propagates to:
  - {Other artifact}: {Pending | Done | Rejected} - {what needs to happen there, or why it was rejected}
- Tasks:
  - {Task reference (URI or identifier)}: {Closed | Partial | Reference} - {why}
- Contributors:
  - [{Name}](../CONTRIBUTORS.md#{name}) ({ModelName} via [{ToolName}](../CONTRIBUTORS.md#{tool})) - {short role tags only, e.g. claimed, decided}

#### What changed
{the change itself, as structured statements - claims carrying inline attribution only where authorship varies across the entry, per [Contributors](#contributors-entry-field)}
```

A small wording fix from one person needs almost none of this - `What changed` and a one-line `Contributors` bullet are enough. `What changed` states the outcome of the change, not the process that produced it: positions raised, counters, and what tipped the balance belong in [Deliberation](#deliberation) when the entry records a deliberation. Attribution in `What changed` is required only where authorship varies across the entry's claims; where the `Contributors` tags already answer "who stands behind every claim" uniformly, per-claim tags are omitted - one fact, one home. Decision and position claims (who proposed, who required, what tipped the balance) live only in `Deliberation`; `What changed` states outcomes without re-narrating who decided them.

### Optional Sections
A non-exhaustive catalog of content sections a changelog entry's author may include - nowhere is any of these mandatory, and this list may grow. An entry includes whichever sections the change genuinely has content for; unused items are simply omitted, not left as empty headers. New sections may be added as real entries demonstrate the need, following the same pattern. Each carries its attribution inline in parentheses, per [Contributors](#contributors-entry-field).

#### Considered and not done
Alternatives examined and not applied in this change, each with its reason - the structured home of rejected-alternative reasoning, per [documentation-explanation.md - Relevance discipline](./documentation-explanation.md#relevance-discipline), which excludes it from base documents' bodies.

#### Surveyed
What was checked, against what, and what the check found - stated so a later session does not repeat it. Each item names the source examined and where this artifact already carries it, or that it does not; a survey whose result is "already held" says so plainly, because a negative result is invisible in a diff and is the finding most worth keeping. Distinct from [Related work](#related-work) (how another project organizes the problem) in that the material examined is a source rather than a project, and distinct from [Considered and not done](#considered-and-not-done) in that nothing was chosen between alternatives: the question was whether the artifact already says it.

#### Examined and not adopted
Material examined against this artifact and deliberately not carried, each with the reason it was not - a claim from an external source that is wrong for this project, belongs to another subject, is already rejected, is a measurement rather than an architectural fact, or is a position this artifact has settled against. It exists because a rejected claim has no change to hang from, and a claim examined once and rejected must not be examined again without a reader knowing it was. Distinct from [Considered and not done](#considered-and-not-done), which records alternatives weighed *inside one decision*, and from [Surveyed](#surveyed), which records the check as a whole.

#### Related work
Comparative surveys of how other projects organize the same problem and how this project differed - the retired body title `Prior art` migrates here.

#### Deliberation
The chronology of positions in a multi-participant session - who claimed what, what was countered, and what tipped the balance - as claim-shaped sentences each carrying its own inline attribution, ordered by the exchange rather than by person. This is the named home for the decision-shaping context the Abstract promises; it is distinct from [Considered and not done](#considered-and-not-done) (which records rejected alternatives as outcomes) and [Decision](#decision) (which records the final ruling). Included only when the entry records a deliberation; single-contributor changes never need it. It records only the exchange the entry's own text evidences; where none was recorded, its absence is honest, not a gap.

#### Decision
The final ruling on what was and was not applied, when the entry records a deliberation rather than a single change.

### Session consolidation
A single working session that touches one base artifact produces **one entry**, not one entry per edit made during the session. Multiple edits to the same file in the same session are consolidated into a single entry whose `What changed` section lists the individual changes as bullets. A new entry is added only when the *kind* of work changes (for example, a `refactor` pass followed by a substantive `Added` change), not when the same kind of work is applied in several passes. This prevents the changelog from becoming a session transcript - the audit reader needs the outcome, not the keystroke history.

### Trivial changes
A change with nothing to audit receives **no entry**. The test is the audit reader this facet exists for: a broken-link repair, a typo fix, or a cosmetic correction carries no decision, no reasoning, and no consequence beyond the fix itself — the diff is the whole record, and an entry would only restate it. Two boundaries keep this exception from swallowing the facet: the moment a change discloses something worth auditing — why a link pointed where it pointed, what a mistake revealed about the document's assumptions — it is no longer trivial and earns an entry; and a trivial fix made alongside a substantive change to the same artifact rides inside that session's consolidated entry (see [Session consolidation](#session-consolidation)) rather than earning its own. Where a change is trivial but a cross-referencing entry elsewhere describes its outcome, that entry states the fix happened and moves on — it does not link to an entry that does not exist.

**Same-session undone mistakes.** An entry whose only content is that a writer briefly applied a wrong change and then reverted or relocated it in the same session, before any durable snapshot of that wrong state existed for a reader, has nothing to audit — delete it; do not keep it as "we fixed our confusion," and do not invent value for it under Session consolidation. Session consolidation records *outcomes that remain*; it does not turn corrected keystroke history into provenance.

### Commit economy
The same economy applies one level up, to the repository's commit history: **a trivial change does not earn its own commit**. Version control already records what changed; a standalone commit for a cosmetic fix adds a permanent history entry, review weight, and attention cost with no audit value the change itself does not already carry. A trivial fix folds into the task's one commit, made by the coordinating session after the human approves the task's result — the batching this facet's [Trivial changes](#trivial-changes) rule applies to entries, applied to commits; a sub-agent never commits. One boundary keeps this from becoming accumulation: batching is a delay in recording, not a substitute for recording — once the human approves, what the task left is in the task's one commit; uncommitted working state is not a storage medium. A move keeps a commit of its own only where an edit would push the moved file below git's rename threshold, so that history follows the move ([Scripts → Deleting, moving, restoring, and committing](../.agents/scripts/README.md#deleting-moving-restoring-and-committing)).

### CONTRIBUTORS.md
A single, project-wide file — not paired to any one artifact — listing every contributor across the whole project. Each contributor — a natural person or a legal entity — gets their own `##` heading carrying a short, recognizable name (`## Microsoft`, `## Xiaomi`), with a `Full Legal Name` bullet holding the precise entity and an optional `Alias Legal Name` bullet only when more than one entity could claim the contribution; the heading is directly linkable from any changelog entry (`../CONTRIBUTORS.md#omid-hekayati`) instead of repeating identity data in every file. Brands, tools, and models never earn a `##`: each sits as a `###` section under the entity that owns it (`### Claude` under `## Anthropic`, `### Cursor` under `## Anysphere`) — each opening with a one-line `Bio` stating what the section is. Under each heading, an open, non-exhaustive list of bullets — `URI` (one or more: email, personal site, a social profile), `Donate` (a tip/coffee link), a short optional `Bio`, or anything else a contributor wants recorded about themselves. This list is not closed; a contributor may add a bullet field for themselves that isn't one of these examples.

For an example, this repository's own [CONTRIBUTORS.md](../CONTRIBUTORS.md) at the repository root is the reference: field shapes and entries are read from it directly rather than copied here, so no duplicated, cached copy of the data exists to drift out of sync.

For an AI contributor, only `Name` and the officially documented `Model` identifier are recorded here as stable facts. Models are listed chronologically, oldest first, with each new model appended at the end — the same append-only convention as changelog entries, so adding a model never requires re-sorting. A model may carry a link to its official documentation page where one exists and has been verified. The host tool (Cursor, ZCode, Claude Code, …) is recorded as its own `###` section under the owning entity, not under the model Name. `Effort`, and anything else that can genuinely vary between one contribution and the next, belongs inline in that specific changelog entry's own `Contributors` bullet instead, using the entry-field shape `{ModelName} via {ToolName}` (e.g. "Claude (claude-sonnet-5 via Cursor, extended thinking) — rewrote"), not here.

Of the open bullet fields, two carry conventions an AI contributor needs at commit time. `[eMail]` is the contributor's public correspondence address. `Co-authored-by:` holds the exact git trailer in `Name <email>` form — angle brackets required, since GitHub links a co-author only in that form — and is recorded in the owning tool's `###` section only: the trailer is the host agent's commit identity, not the model's. Which model actually ran stays out of this file: it is recorded in each changelog entry's `Contributors` bullet as `{ModelName} via {ToolName}`. An agent committing in this repository appends the trailer of the tool it runs through; a tool with no `Co-authored-by:` bullet publishes no official trailer, and none may be invented.

The same preservation rule as elsewhere applies: while a contributor is still actively working on any unfinished (non-`Final`) artifact, they may add or extend their own entry here; no one edits another's entry.

### Contributors (entry field)
Each changelog entry's `Contributors` bullet names who was involved and what role they played, as a link to that person's `CONTRIBUTORS.md` heading. The bullet stays **short**: presence plus role tag only (`claimed`, `argued`, `reviewed`, `rewrote`, `tested`, `approved`, `requested` being common examples - the vocabulary is intentionally open, not a closed list; a more formal, fixed role taxonomy exists in academic publishing, the CRediT - Contributor Roles Taxonomy - system, as a model for how far formalization could go if ever needed). The bullet does not carry narrative.

When the entry names the host tool (`via {ToolName}`), the label stays the tool's own name and its link resolves to that tool's `###` section inside the owning entity's entry — the reference lands on the legal person without losing which tool ran.

The narrative lives in the entry's structured sections, where claims carry their attribution inline at the point of the claim - `(Omid Hekayati)`, `(Super Z)` - so statements and their authors never separate into different parts of the entry, and no reader has to reconstruct who argued what from a detached role list. The inline tag is required wherever authorship varies across a section's claims; where one contributor stands behind all of them, the `Contributors` tags already say it and the per-claim repetition is dropped - duplicated attribution is itself a drift risk, the two copies being free to diverge. Splitting them is how attribution errors happen: a role bullet grows into prose, prose drifts away from the claims it describes, and the reader can no longer tell which contributor holds which statement. Where an earlier migration relocated prose verbatim into an entry, rewriting it into this claim-shaped form is expected, not forbidden: the constraint that governs such relocations is against losing information, not against changing its shape.

#### Approval Requires a Reviewer Who Did Not Do the Work
`approved` is the one role tag in that open vocabulary that is a **judgement about the entry's own correctness**, and it is separated from the rest for the same reason [Test → What a Passing Suite Establishes](./modules/process/test.md#what-a-passing-suite-establishes) separates what a green run proves from the claim that the work is finished: the party that performed the work cannot judge it, because it holds the model of what it meant to do and reads its own output as that model.

Three conditions, and all three are required:

1. **The reviewer did not do the work.** An agent that authored, edited, or drafted the change may not approve it. Where the work was done by one cognitive system, the reviewer is another - in this project's practice, a sub-agent given the claim to assess and the evidence to assess it from. That is the internal-audit half of how certification actually works: the body that performs the work is not the body that audits it.
2. **The reviewer returns a verdict, not an impression.** A verdict is the reviewer's own comparison of what now holds against what the entry claims, and it names what it examined and what it found; where a command can show the claim false if it were false, the verdict names that command and what it returned. A verdict may rest on reading alone where reading decides the claim — a wording change is not improved by a run and not degraded without one — but an opinion naming nothing examined has established nothing, and an approval resting on it is the unverified claim wearing a verified one's name. What keeps the tag from becoming self-certification is the first condition, not the presence of a command: the comparison is made by a party that did not do the work.
3. **No verdict, no `approved`.** Where the reviewer withholds permission, the entry carries the reviewer's reason and no approval tag. An entry left unapproved is the correct state for work that has not been checked, and is not a defect to be tidied away.

The approval names the reviewer alongside the other contributors, so a reader can see who judged and not only who acted. An approved entry therefore carries two roles where an unapproved one carries only the first: the one that did the work, and the one that said it holds. That separation is the whole content of the tag - without it, `approved` records that someone was satisfied, which the word `satisfied` already says.

The procedure that satisfies these conditions is in [Documentation Changelog Practice → Recording an approval](./documentation-changelog.practice.md#recording-an-approval), and it is deliberately not part of any agent skill: the conditions bind whoever writes the entry, and a rule that lives in the tooling disappears with the tooling.

This is not a certificate. An audit by a party that did not do the work, over evidence it gathered and weighed itself, is the strongest form of scrutiny available inside one collaboration, and [Terminology → On Independent Verification, Today](./terminology.md#on-independent-verification-today) states plainly what that is worth against an outside institution. The tag records that a second party checked; it does not record that the work is correct in general.

### Type
Free text, not a controlled vocabulary — what counts as a meaningful category of change varies too much across artifact kinds to close this off. Two existing vocabularies are offered as a starting point, not a requirement: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)'s `Added`/`Changed`/`Deprecated`/`Removed`/`Fixed`/`Security`, and [Conventional Commits](https://www.conventionalcommits.org/)' `feat`/`fix`/`docs`/`style`/`refactor`/`perf`/`test`/`build`/`ci`/`chore`/`revert`. Both are written for software releases and commits specifically; a documentation change may need a word neither offers (e.g. "clarified," "merged," "split"). Use whichever word is most accurate, from either vocabulary or outside it.

### Cited
Replaces the base artifact's former `Citations` field, now describing what this specific change relied on, not a standing property of the base artifact. The `Relation` vocabulary and source-selection criteria are defined in [documentation.md → Citations](./documentation.md#citations) as cross-cutting concerns, applying wherever citations appear; this section covers only what is specific to a Changelog entry's `Cited` field. A source cited here does not need to be named anywhere in the base artifact's own body — citing it here is sufficient provenance. The one exception: if the base artifact's own body genuinely needs a source at the point a reader is reading it — not as evidence for a past decision, but as something the reader themselves needs to follow — link it directly and normally in the body itself, the same as any other hyperlink, never as an unlinked "see X" pointer.

### Propagates to
Replaces the base artifact's former `Applied to` field, and generalizes it: instead of one artifact declaring where its own design "landed," each change explicitly names every other artifact it should affect, with a status. `Pending` is the open state — a `Pending` entry is exactly what a future contributor (human or AI) should search for to find undone propagation work across the whole documentation set. `Done` and `Rejected` are closed: `Rejected` closes that search result permanently once a propagation is considered and deliberately not done, with the reason recorded, so it doesn't keep surfacing as an open task.

### Tasks
An optional reference to an external task-tracking entry (however that ends up being modeled — this specification does not assume or require a specific Task system), with one of three relations: `Closed` (this change completes that task), `Partial` (this change is progress toward it but doesn't complete it), or `Reference` (mentioned for context, no completion claim either way). The deferral is a considered position rather than an omission: the concept is larger than this framework, and [Terminology → A Term Deliberately Left Open](./terminology.md#a-term-deliberately-left-open) records that the word is left undefined here on purpose.
