---
Title: "Documentation Rule — No Record Is Written Beside a Document"
Status: Draft
Start Date: 2026-10-31
---

# Documentation Rule — No Record Is Written Beside a Document
A rule of this repository, held for [Documentation](../../documentation.md). The owner's ruling of 2026-10-31, made while task 20261025-T141522Z-25344 was taken up: the history and the open questions of a document are not a file beside it.

## The rule
- **A change record, a decision, a question, an assumption, a finding and a piece of anticipated work is a content placed on the timeline of a task, never an entry in a file beside the document it concerns.** The change record is written with `memar conversation post --timeline ID --kind changelog`. A handoff, a changelog and a research are templates for writing such a content; they name no file.
- **The record names what it concerns.** Its Propagates to field lists every content the change affects, the first being the document, the code or the skill that was changed; the record is then reached from that content by the edge.
- **Nothing is appended to a file that already exists.** No `*.changelog.md`, `*.handoff.md` or `*.research.NNN.md` is created or added to; the files that exist wait for their migration, which reads them whole and loses nothing. The verb that appended to such a file is removed.
- **A content is never edited.** A correction is a new content that replies to the earlier one. A change that cannot be made in the task it was found in is made by a new task.
- **A question is its own task.** Questions that are related are one content on an existing task, and a question is never written on an unrelated task.
- **A practice is a rule.** A new `*.practice.md` is not written beside a document; what it would say is a rule of the module that owns the subject, in its `rules` folder.

## Why it exists
A document that carries its own history was appended to by every task: racing writers into files that outgrow one reading, with the reason for a change kept apart from the task that made it. A record on a task keeps the whole path of the work, has one writer and one place, and answers why a content changed by the task it came from.

## How a check would run
An agent that creates or appends a `*.changelog.md`, `*.handoff.md` or `*.research.NNN.md`, or that writes a question as an entry in a document, breaks the rule. No verb writes such a file any longer; this repository runs no automatic check beyond that.
