---
Title: "Documentation — Report"
Status: Draft
Start Date: 2026-10-16
ID: 497823
---
# Documentation — Report
This document specifies the Report template: the shape of a content of kind `report` placed in the timeline of a task, the account of one pass of work when it ends. It names no file, directory, path or file name: where a content is kept is the store's concern. See [Documentation](../documentation.md) for what a template is.

## Abstract
A report content is a record whose reader did not do the work and needs to know what ran, what the task's own check found, how the run ended, and what is still open. It is written when the pass ends, whether it ended finished or not. Its shape, the parts and their order and the limit on a hand-back, is declared once in code ([report/protocol](protocol/report.kh), [record.py](../primitive/record.py), [content_kinds.py](content_kinds.py)), so this specification writes none of it as text. What it states is what a report must carry beyond its shape, who writes it and who reads it, what each part is for, and the requirements a party that did not write it can decide from a stated input.

## Introduction
### Motivation
Work that ends silently cannot be accounted for. A task that stops, because its budget ran out, because it waits on an answer, or because its check passed, leaves the same residue either way, and a later reader cannot tell whether it was finished or merely stopped. A task read as done that was not, or as unfinished that met every condition it set for itself, costs the person who asked more than the work did.

The account is short by design. The party that reads a hand-back, a delegating party waiting on a sub-agent or the owner reviewing a day, needs a verdict, a reference to look at, and at most a few lines of what it must decide. A report that carries the task's context back into that reader's has undone the separation it exists to make, so the length of a hand-back is a limit the declaration carries rather than a matter of the writer's restraint.

### Methodology
The artifact had been in daily use in this project long before it was named. The owner's rulings of 2026-10-16, on what a report is and what each specification must carry, and of 2026-10-23 and 2026-10-31, on rounds and on the task's facts, are what this document applies. Moving the report into the timeline of the task made the task the single home of its facts and left this specification with the template alone.

## Explanation
### What a Report Is
A **report** is one pass of work accounted for: what ran, what the task's own check found, how the run ended, and what the next party still has to open. Two boundaries keep the definition from widening:

- **A report accounts for a pass, not for a subject.** It does not state what was learned about the world; the finding graduates into the document that owns its subject, and what the report keeps is that the work ran and what it showed. A negative result belongs here because the pass that produced it would otherwise leave nothing.
- **A report is scratch, not a document of record.** What outlives it is routed by type to the documents that own the material. What is left open is a `question`, `assumption` or `anticipated-work` content of the task ([Handoff → The kinds](../handoff/handoff.md#the-kinds)).

The task's identifier is not a field of the report: the task is the timeline that holds it. A task has one Status, held by the task and changed only by a Request ([Request](../../../../modules/computer/request/request.md)); a report does not repeat it.

### Rounds
A report is bound to a pass of work, not to the task for good: each round of critique ends in a report of what ran and what is to be done, so one task may hold several, as it may hold several plans ([Plan → Rounds](../plan/plan.md#rounds)). The owner ruled so on 2026-10-23.

- **A report is a content and is never overwritten or removed.** The next pass places another, so each round's account stays as it was written.
- **The current report is the latest of its kind.** A reader that wants one report reads the current one; a reader that wants the history reads the timeline.
- **A round and a new task are told apart as the plan's specification says**: an unchanged request and check make another round with a new plan and a new report; a changed request or check makes a new task that cites the old.

### Reader relationship
A report is **read to account for a pass of work**: the reader did not do the work and asks one question, did it do what it said it would, and what is left. It needs the verdict and the check's own finding behind it; the work that ran, so that the verdict can be weighed against the effort; and what is still open, so that nothing is taken as settled that was not. It does not need the reasoning the writer used to reach the verdict. That is a `decision` content's material ([Handoff → The kinds](../handoff/handoff.md#the-kinds)), and the short hand-back exists so the report does not carry it.

A delegating party reads less than that: the lines of the hand-back part, whose limit the declaration gives. The owner reviewing a day gets the same account gathered across the tasks of the day.

This is not [Practice's reader relationship](../practice/practice.md#reader-relationship): a report is read once, after the fact, to settle whether one pass met its own condition.

### Who writes a report, and who reads it
A report is written by the party that ends the task, before it closes, whether it finished or not. It is also written by the delegating party on behalf of a sub-agent that could only return text, so that the sub-agent's task carries a record.

A report is read by the delegating party, which reads the hand-back and nothing more; by a later party, together with the plan it answers; by the parties that list tasks; by the owner, through the digest of a day's hand-backs; and by the debrief of a task that produced tasks.

### What each part is for
Each part is for one job: to carry what ran; to carry what the task's own check found; to carry how the run ended; and to carry what is left open. One further part, which the declaration marks optional and limits in lines, is the hand-back: the decisions the task hands back. It is omitted entirely when there is nothing to decide, and its absence is what says so. The parts, their headings and their order are the declaration's.

### The requirements
Each requirement is decidable from a stated input by a party that did not write the report. None names a part or a count, because those are the declaration's. The shape is declared once in code ([report/protocol](protocol/report.kh), [record.py](../primitive/record.py), [content_kinds.py](content_kinds.py)).

1. **The report states what the task's own check found**, and is read against the check its plan states.
2. **A report is never overwritten** ([Rounds](#rounds)).
3. **A hand-back part holds no more lines than the declaration allows.**
4. **A task may hold several reports, and a report is never rewritten into an earlier one.**
5. **A report receives no record beside it** ([No Record Is Written Beside a Document](../rules/no-record-beside-a-document/no-record-beside-a-document.md)).

### Why report and plan stay separate
The report and the plan are two kinds and not one, on the attribute where they do not overlap: the place each is consumed. A plan is read before any work exists, to begin it; a report is read after, to account for it. They are written by different acts at different moments, and they are kept apart even though they may share a type for their shape, because a shape is code and is shared without sharing a responsibility. See [Plan → Why plan and report stay separate](../plan/plan.md#why-plan-and-report-stay-separate).

### Why the module is named `report`
The module is named for the kind of content it governs, not for the task that uses it. `report` is the word this project already uses for the artifact, and a name carrying the task would claim that the kind exists to serve a task, when the same kind may be consumed elsewhere as a template for the same account.
