# Task — what the task asks of the domains that keep its texts
Status: Tentative

## Abstract
The kernel [Task](../../../modules/management/task/task.md) holds a task's intent, check, status and relations and nothing of any text. This document holds what the task needs from the domains that do keep texts: a record that today is a handoff entry or a changelog record is, here, a message with a template on a task. It names no file, folder or path: where a text is kept is [text](../../../modules/knowledge/text/text.md)'s, how it is joined to a task and ordered is [content](../../../modules/knowledge/content/content.md)'s and [timeline](../../../modules/management/timeline/timeline.md)'s, and each of them is asked, not told. The shape is Tentative (the owner reviews it) and the rules it applies are the [Task rules](rules/README.md).

## Explanation

### What a record is
A record of what a task learned or changed (a decision, a question, an assumption, a piece of anticipated work, a change record) is a content on the task's timeline whose text follows a template and which has an edge to the thing it concerns. There is no companion document that agents write: the handoff of a thing is the open records that concern it, found by the edge, and its changelog is the change records that concern it, found the same way. A handoff is therefore a template of a descriptive message on a task, not a document ([owner, 2026-10-30](../../../modules/management/task/task.handoff.md#critique-as-a-content-on-the-timeline-2026-10-30-tentative)).

### What the task asks of the other domains
Each question is raised in the handoff of the domain that owns the answer, and the task module assumes none.

| Asked of | The requirement |
| --- | --- |
| text | keeps the template's text, versions it, and finds a word in it; the template of a decision, a question and a change record is a text template ([documentation by text template or edge](rules/documentation-by-text-template-or-edge/documentation-by-text-template-or-edge.md)) |
| content | joins a record to the thing it concerns by an edge, and a reply to the content it answers; says what a label of a record kind is |
| timeline | gives every content a number that is assigned at placement, is never reused, and is the same wherever the content is read; says what reads the contents that concern one thing, across tasks |
| record and request | carries a change to a record as a change of state ([Request](../../../modules/computer/request/request.md)), so that an answered question is a reply and not an edit |

Until those domains answer, the rules of this module state only what a task must be able to do (a reply names numbers with reasons, an ask is addressed, a chain ends) and no way of storing it.

### Migration
The old handoffs and changelogs are not converted by a script that moves their text. Each handoff, alone or with the ones related to it, becomes one or more tasks that take the queue's statuses; the handoff's text becomes content on the timeline of that task, and what is open in it becomes asks that are open. A changelog record becomes a change record on the timeline of the task that made it, where its `Tasks` field names one, and on a task made for it where it names none. The migration is queued after the series of the memory-port programme (the task `20261023-T074642Z-5420` and what depends on it) has settled where tasks and texts are kept, so that no domain is rewritten against a file layout. Until then handoffs are not extended: a result that would have gone into a handoff is written as a message with the template on the task that finds it, and the creation of that task is made quick and checked for a related one first (task `20261030-T073507Z-6324`, which is to be done before the handoffs are removed).

### The size of what is migrated
Counted on 2026-10-30 by `services/inventory.py` in the design task's folder: 205 task folders; 199 plans, in 23 key sets and 13 section sets; 198 reports, in 16 section sets; 221 changelog files holding 1294 entries, of which 1281 carry an hour and 13 none; 256 handoff files, whose entries carry no time and seldom a task, so the task each belongs to has to be made and cannot be found. These numbers size the migration tasks; they are not a layout.

## Critique of the owner's model of the critic
The strengths, what the model lacked and what the rules add are recorded in [the Task handoff](../../../modules/management/task/task.handoff.md#critique-as-a-content-on-the-timeline-2026-10-30-tentative).
