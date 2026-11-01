---
Title: "Documentation — Plan"
Status: Draft
Start Date: 2026-10-16
ID: 497822
---
# Documentation — Plan
This document specifies the Plan template: the shape of a content of kind `plan` placed in the timeline of a task, the agreement one task is given in before it is worked. It names no file, directory, path or file name: where a content is kept is the store's concern. See [Documentation](../documentation.md) for what a template is.

## Abstract
A plan content is a record whose reader is about to carry out one agreed task and needs what was asked, what checks it is done, and what comes next, without the context of the task that agreed it. It is written at intake, before the material the work is about has been read. Its shape, the parts and their order, is declared once in code ([plan/protocol](protocol/plan.kh), [record.py](../primitive/record.py), [content_kinds.py](content_kinds.py)), so this specification writes none of it as text. What it states is what a plan must carry beyond its shape, who writes it and who reads it, what each part is for, and the requirements a party that did not write it can decide from a stated input.

## Introduction
### Motivation
A task handed from one party to the next arrives as nothing unless something carries what was agreed. A task stops mid-work, and whoever comes next has a plan that either says what was asked and what would show it done, or does not. In the second case the work restarts from scratch or is taken on terms nobody agreed, and the task gets done against an unstated acceptance check.

A plan is distinct from the records that already exist. A [changelog](../changelog/changelog.md#reader-relationship) is consulted to audit what changed; a [handoff](../handoff/handoff.md#reader-relationship) kind is read to resume a paused discussion; an [Explanation-facet specification](../explanation/explanation.md#reader-relationship) is studied to understand a subject. A plan is read to begin work that has been agreed but not started, and its reader is about to act on it rather than interpret it.

### Methodology
The artifact had been in daily use in this project long before it was named. The owner's rulings of 2026-10-16, on what a plan is and what each specification must carry, and of 2026-10-23 and 2026-10-31, on rounds and on the task's facts, are what this document applies. Moving the plan into the timeline of the task made the task the single home of its facts and left this specification with the template alone.

## Explanation
### What a Plan Is
A **plan** is one agreement about one task, in writing, made before the work is done: what was asked, what would show it done, why it is worth doing, how it will be attempted, and what the next party does first. Two boundaries keep the definition from widening:

- **A plan is one agreement of one task, not of a conversation.** A conversation holds several tasks, each one thing asked with one check. A plan that gives each request its own section makes one content carry several agreements, and the reader has no single one to read.
- **A plan is scratch, not a document of record.** What outlives it is routed by type to the documents that own the material. What is left open is a `question`, `assumption` or `anticipated-work` content of the task ([Handoff → The kinds](../handoff/handoff.md#the-kinds)).

The task's identifier is not a field of the plan: the task is the timeline that holds it. A task has one Status, held by the task and changed only by a Request ([Request](../../../../modules/computer/request/request.md)); a plan does not repeat it.

### Rounds
Each round of critique can end in a separate plan, so one task may hold several; the same holds for its reports ([Report → Rounds](../report/report.md#rounds)). The owner ruled so on 2026-10-23.

- **A plan is a content and is never overwritten or removed.** A later plan is one more content in the same timeline, so each round keeps its own history and nothing else needs to record it.
- **The current plan is the latest of its kind.** A reader that wants one plan reads the current one; a reader that wants the history reads the timeline.
- **A change to a finished task is a round or a new task by what it changes.** If the request and the check the task was agreed with are unchanged, the work was not done as asked, and the change is another round of the same task: a new plan and later a new report. If the request or the check changes, it is a new task, with an edge to the one it follows.

### Reader relationship
A plan is **read to begin work**: the reader is an agent or a person who is about to carry out one agreed task and knows nothing of the task that agreed it. It needs what was asked and what checks it done, to tell done from merely attempted; the reason, to tell a requirement from an accident of the moment; the attempt, to tell what has been ruled out; and what comes next, so as not to guess where to pick up. It does not need how the work ended, which is the [report](../report/report.md)'s subject.

This is not [Practice's reader relationship](../practice/practice.md#reader-relationship): a plan is followed to accomplish one thing once, agreed between named parties, with a shape a program must read to find the parts.

### Who writes a plan, and who reads it
A plan is written by the party that takes a task up, at intake and before it reads the material the work is about, so that the plan binds the work rather than being shaped by it. It is also written by a party that queues a task for another, and by a party that hands a task to a sub-agent and writes the whole task into the plan.

A plan is read by the party taking the task up, before anything else; by the party that comes next, which is the reason the record exists; by a sub-agent, through the brief the delegating party composes; and by the parties that list, rank and gather tasks, each to answer its own question.

### What each part is for
Each part is for one job: to carry what was asked together with what checks the task is done; to carry the reason for the task in the writer's own words; to carry the steps, each decided to be local or delegated; and to carry what the next party does first. The parts, their headings and their order are the declaration's, and no writer creates, renames or reorders one.

### The requirements
Each requirement is decidable from a stated input by a party that did not write the plan. None names a part or a count, because those are the declaration's. The shape is declared once in code ([plan/protocol](protocol/plan.kh), [record.py](../primitive/record.py), [content_kinds.py](content_kinds.py)).

1. **The plan states what was asked and what checks the task is done.** A plan whose statement of what was asked is empty is not ready and is not taken up.
2. **The plan's check is that something was done**: a change applied, or a decision recorded where it governs. A task whose outcome would be a finding or a proposal is a step of the plan of the work it improves ([A task is for work](../../../management/task/rules/a-task-is-for-work/a-task-is-for-work.md)), and a plan whose only check is a proposal is not ready.
3. **A task may hold several plans, and a plan is never rewritten into an earlier one** ([Rounds](#rounds)).
4. **A plan receives no record beside it** ([No Record Is Written Beside a Document](../rules/no-record-beside-a-document/no-record-beside-a-document.md)).

### Why plan and report stay separate
The plan and the report are two kinds and not one, on the attribute where they do not overlap: the place each is consumed. A plan is read before any work exists, to begin it; a report is read after, to account for it. They are written by different acts at different moments. They are kept apart even though they may share a type for their shape, because a shape is code and is shared without sharing a responsibility.

A plan is also not a Practice document. A Practice is a reusable procedure written to be followed again; a plan is one agreement about one task, written once.

### Why the module is named `plan`
The module is named for the kind of content it governs, not for the task that uses it. `plan` is the word this project already uses for the artifact, and a name carrying the task would claim that the kind exists to serve a task, when the same kind may be consumed elsewhere as a template for the same agreement.
