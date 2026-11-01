---
Title: "Documentation — Changelog"
Start Date: 2026-08-03
ID: 496040
---
# Documentation — Changelog
This document specifies the Changelog template: the shape of a content of kind `changelog` placed in the timeline of a task, recording why and how what the task changed came to change. It names no file, directory, path or file name: where a content is kept is the store's concern, and a record is a content of a task, never written beside the thing it concerns ([No Record Is Written Beside a Document](../rules/no-record-beside-a-document/no-record-beside-a-document.md)). See [Documentation](../documentation.md) for what a template is.

## Abstract
A changelog content is one concise, minutes-style record of one change: what changed, why, on what evidence, and what else it affects. Its time is the time it was placed, and who wrote it is who placed it; neither is repeated in it. A record is a content of a task and is never edited: a later change, a correction, or an approval is a new content that refers to it. The history of a thing is the changelog contents of the tasks that changed it, read in the order of their placement.

The same reader-relationship makes the record the home of what a reader of the current state must not be burdened with: the evidence a change relied on, and the other things it affects. Positions weighed and rejected belong to a `decision` content ([Handoff](../handoff/handoff.md)), a survey whose result is that nothing changed to a `research` content ([Research](../research/research.md)), and an open question to a `question` content; none of them is part of a changelog record.

## Introduction
### Motivation
A document's readers need its current state, not its provenance. Provenance (the evidence a change relied on, the other documents it should reach) is history, and history is read by an auditor who is a different reader. A record that serves the auditor, kept as a content of the task that made the change and not as a file beside the document, keeps the document lean and the history findable by the task, by time and by what it propagates to.

### Methodology
The record was first kept as a companion file of its document. That model recorded the same history twice, once in the file and once in the task that did the work, and made every tool that read the history read a file. Moving the record into the task's timeline makes the task the single home of the change and leaves this specification with the shape of the record alone.

## Explanation
### Reader relationship
Content meant to be *consulted* to audit history: a chronologically ordered series of records, each of one change — what changed, why, on what evidence, and what else it should affect. The reader arrives to learn how a thing came to be as it is, so its current state is never what they are given; what they are given is the record's shape and the fields it may carry. The boundary this template draws against the [Handoff](../handoff/handoff.md) kinds is where a mutable record stops being this one: what is still to be done is a `question`, `assumption` or `anticipated-work`, and what is settled is recorded here or as a `decision`.

### What a record holds
A record is of an **event bearing on the state of a thing**, and the event need not be a change to the thing's own text. Its kind is `changelog` and its fields are:

| Field | Held when | What it holds |
|---|---|---|
| Type | optional | Free text naming the category of change; see [Type](#type) |
| Cited | the change relied on a source | The sources the change relied on, each with its relation and why |
| Propagates to | the change affects anything else | Every thing the change affects, the changed document first, each with a state |
| What changed | always | The change itself, as structured statements |

The time of the record is the time of its placement and its writer is its placer: neither is a field. A task the change belongs to is the task whose timeline holds the record, so no field names it; a reference to another task is made in the text where it is meant. A contributor other than the placer is named in a `Contributors` field, optional, only where someone took part whose part the timeline does not show.

```
### {short, descriptive title of the change}
- Type: {optional}
- Cited:
  - [{Title}]({URI}) - {Relation}: {why this source was used as evidence for this change}
- Propagates to:
  - {the changed document}: {Pending | Done | Rejected} - {what needs to happen there, or why it was rejected}
  - {another thing the change affects}: {Pending | Done | Rejected} - {what, or why}
- Contributors: {optional; name and short role tags, only for who the timeline does not show}

#### What changed
{the change itself, as structured statements; a claim carries inline attribution only where authorship varies across the record}
```

A small wording fix needs almost none of this: `What changed` alone is a record. `What changed` states the outcome of the change, not the process that produced it: positions raised, counters, and what tipped the balance are a `decision` content.

### Never edited, corrected by a new record
A record is never edited after it is placed. A mistaken record is answered by a later record that says what was wrong and what holds now, and an approval of a record is its own content ([Approval](../approval/approval.md)) that names the record it judges. The state of a propagation is the latest state any record of the timeline gives it.

### Trivial changes
A change with nothing to audit receives **no record**. The test is the audit reader this template exists for: a typo fix or a cosmetic correction carries no decision, no reasoning, and no consequence beyond the fix itself, and a record would only restate it. Two boundaries keep this exception from swallowing the template: the moment a change discloses something worth auditing — why a link pointed where it pointed, what a mistake revealed about the document's assumptions — it is no longer trivial and earns a record; and a trivial fix made in the same task as a substantive change rides inside that change's record rather than earning its own.

A question recorded so it is not forgotten has nothing to audit: it is a `question` content and its own task, and earns no changelog record. It earns one when the addition carries a decision — alternatives were weighed and this question, framing or placement chosen over them.

### Type
Free text, not a controlled vocabulary — what counts as a meaningful category of change varies too much across kinds of thing to close this off. Two existing vocabularies are offered as a starting point, not a requirement: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)'s `Added`/`Changed`/`Deprecated`/`Removed`/`Fixed`/`Security`, and [Conventional Commits](https://www.conventionalcommits.org/)' `feat`/`fix`/`docs`/`style`/`refactor`/`perf`/`test`/`build`/`ci`/`chore`/`revert`. Use whichever word is most accurate, from either vocabulary or outside it.

### Cited
Describes what this specific change relied on, not a standing property of the thing changed. The `Relation` vocabulary and source-selection criteria are defined in [documentation.md → Citations](../documentation.md#citations) as cross-cutting concerns; this section covers only what is specific to a record's `Cited` field. A source cited here does not need to be named anywhere in the changed document's own body — citing it here is sufficient provenance. The one exception: if the document's own body genuinely needs a source at the point a reader is reading it, link it directly and normally in the body.

### Propagates to
Lists everything the change affects, the changed document first, each with a state. `Pending` is the open state — a `Pending` item is exactly what a future contributor (human or AI) should search for to find undone propagation work across the whole documentation set. `Done` and `Rejected` are closed: `Rejected` closes that result permanently once a propagation is considered and deliberately not done, with the reason recorded, so it does not keep surfacing as an open task. A state is not edited: a later record names the same item with its new state, and the latest governs.
