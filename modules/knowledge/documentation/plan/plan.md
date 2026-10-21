---
Title: "Documentation — Plan"
Status: Draft
Start Date: 2026-10-16
ID: 497822
---
# Documentation — Plan
This document specifies the Plan facet: the record one agreed task is given in before it is worked, read by whoever carries it out. See [Documentation](../documentation.md) for what a Facet is, and [Documentation → Status](../documentation.md#status) for what it already says about the session records — where a plan's Status is written, which values it draws on, and the closed set that holds them. None of that is restated here.

## Abstract
A Plan-facet document is the file a session's plan takes: a record whose reader is about to carry out one agreed task and needs what was asked, what checks it is done, and what comes next, without the context of the session that agreed it. It is written at intake, before the material the work is about has been read, and it lives exactly as long as the folder of the session it belongs to. Its shape — the file name, the front-matter keys, the parts under them and their order — is a closed set declared once as a type, so this specification writes none of it as text: each is obtained from that declaration, or from the Status type for the values a plan may state. What this document states is what a plan must carry beyond its shape, who writes it and who reads it, what each part is for, and the requirements a party that did not write it can decide from a stated input.

## Introduction
### Motivation
A task that is handed from one session to the next arrives as nothing but a folder name unless something carries what was agreed. The failure this facet exists to prevent is concrete: a session stops mid-work, and whoever comes next — another agent, or the same person tomorrow — has a plan that either says what was asked and what would show it done, or does not, and in the second case the work either restarts from scratch or is taken on terms nobody agreed. The cost is not only re-reading; it is that a task gets *done* against an unstated acceptance check, and the person who asked never learns what was decided for them.

The same need makes a plan distinct from the records that already exist. A [changelog](../changelog/changelog.md#reader-relationship) is consulted to audit what changed; a [handoff](../handoff/handoff.md#reader-relationship) is read to resume a paused discussion; an [Explanation-facet specification](../explanation/explanation.md#reader-relationship) is studied to understand a subject. A plan is read to *begin* work that has been agreed but not started, and its reader is about to act on it rather than interpret it.

### Methodology
This specification was not designed in the abstract. The artifact it governs has been in daily use in this project long before it was named a facet, written by the services under `modules/management/task/services/` and read by every agent that takes a session up. The proposal that named it — what a plan is, whether it is a facet of its own, and what each specification must then carry — is `.agents/tasks/20261016-T003724Z-23508/report.md`, and the owner's answers of 2026-10-16 are what this document applies. Where a decision was the owner's it is cited as such; where the answers left a detail open, the decision and its reason are in this document's own changelog entry.

## Explanation
### What a Plan Is
A **plan** is one agreement about one task, in writing, made before the work is done: what was asked, what would show it done, why it is worth doing, how it will be attempted, and what the next party does first. The **Plan-facet document** is the file that holds it — a session's plan, named by the shape declared in `modules/knowledge/documentation/record.py`, which the file that opens a session writes beside the session's folder.

Two boundaries keep the definition from widening:

- **A plan is one task, not a conversation.** A conversation holds several tasks; each gets a session of its own, and each session's folder holds one plan. A plan that gives each request its own section with its own state makes one folder carry several states, and the sweep then has no single state to read.
- **A plan is scratch, not a document of record.** It goes when its folder goes. What outlives it — a topic's lasting open state — belongs in the handoff of the document that owns that topic, so a plan that outlived its folder would be a second handoff nobody maintains.

### Reader relationship
A plan is **read to begin work**: the reader is an agent or a person who is about to carry out one agreed task and knows nothing of the session that agreed it. What that reader needs is what was asked and what checks it done, so that they can tell done from merely attempted; the reason, so that they can tell a requirement from an accident of the moment; the attempt, so that they can tell what has already been ruled out; and what comes next, so that they need not guess where to pick up. What the reader does *not* need is how the work ended, which is the [report](../report/report.md)'s subject and is kept out of a plan.

This is not [Practice's reader relationship](../practice/practice.md#reader-relationship), which that specification states: a plan is followed to accomplish one thing once, agreed between named parties, with a shape a program must read to find the parts. The two artifacts do not overlap on the attribute that separates them, which is [Why this facet and the report facet stay separate](#why-this-facet-and-the-report-facet-stay-separate).

### Who writes a plan, and who reads it
A plan is written:

- by the session that takes the task up, at intake and before it reads the material the work is about, so that the plan binds the work rather than being shaped by it;
- by the session a new session came from, in exactly two cases — the agent that queues a session and writes its plan, and the agent that hands a session to a sub-agent and writes the whole task into its plan;
- by the services that change one field of it — the ones that queue or claim a session, set its place in the queue, set its subject, set what kind of act it is, and set the sessions it cannot start without — each rewriting one field in place and nothing else;
- by a person editing by hand, which a plan's tolerance of a mistyped value exists to allow: a field that cannot be read is read as its default rather than stopping the work.

A plan is read:

- by the agent taking the session up, before anything else, which `memar ai get-task-init-context` prints;
- by the person or agent who comes next, which is the reason the record exists;
- by a sub-agent, through the brief `memar ai get-task-init-context` prints;
- by the services that list, rank and gather sessions, and by the sweep that decides which folders go — each of which reads the plan to answer its own question and none of which reads the body for any other reason.

### What each part is for
Each part of a plan is for one job, and the jobs are these: to carry what was asked together with what checks the task is done; to carry the reason for the task in the writer's own words; to carry the steps, each decided to be local or delegated; and to carry what the next party does first. The parts that carry them, their headings, and their order are the declaration's, and no part of a plan is created, renamed or reordered by a writer — a plan that does not answer to that shape is not read as a plan at all, as [A plan written in another shape is not read as one](#the-requirements) says.

A plan carries one more thing that is not a part: the identifier of the session the plan belongs to, written in its front matter. The record must not presume that it is a file — a folder may be moved, renamed, or swept, and a reader looking at the document must be able to tell which session it records without reading the name of the folder it sits in.

### The requirements
Each requirement below is decidable from a stated input by a party that did not write the plan. None of them names a field, a part, a Status value or a count, because each of those is the closed set's, held in `modules/knowledge/documentation/record.py` or in `modules/knowledge/documentation/primitive/status.py` and reached by calling it.

1. **The plan states what was asked and what checks the task is done.** A plan whose statement of what was asked is empty is not ready and is not taken up.
2. **The plan's Status is one of the values the declaration gives a session plan.** The words are the Status type's, produced by calling it, and written nowhere in this specification.
3. **A plan written in another shape is not read as a plan, and no writer rewrites one into today's shape.** The service that reads it names what marks the earlier shape and says where today's is shown; it names no conversion, because a one-time conversion is the work of the session that does the change and is gone when that work is done.
4. **A machine rewrites only the line of one field, in place, and only for the verb that owns that field.** The Status is rewritten to queue, claim, block or release the session; a priority, a topic, a kind and the sessions it cannot start without (`Depends_on`) are each rewritten by the verb that sets them, and no verb rewrites another's. Every other change to a plan is a change a party makes deliberately.
5. **A plan carries no companion changelog and no companion handoff** — see [The exemption from the companion convention](#the-exemption-from-the-companion-convention).
6. **The plan states the identifier of the session it belongs to**, in its front matter, so that a reader finds it in the document rather than by reading a folder name.
7. **The plan's check is that something was done**: a change applied, or a decision recorded where it governs. A task whose outcome would be a finding or a proposal is a step of the plan of the work it improves ([A session is for work](../handoff/handoff.practice.md#a-session-is-for-work)), and a plan whose only check is a proposal is not ready.

### Where the code is, and what a reader does when it disagrees
The code that enforces the requirements above lives today under `modules/management/task/services/`, not in this module's `services/` folder: session `20261015-T123046Z-17544` moved the services out of `.agents/scripts/services/` into the module of their domain, and the session module holds a session's plan and report together. Whether the code that enforces this facet moves on into this module's `services/` folder is not decided, and no second move of the same code is made here.

Which service holds each requirement today, so that a reader looking for the enforcement does not have to search for it:

| Requirement | Enforced today by |
| --- | --- |
| what was asked and what checks it done | no code; a reader's judgement, and the practice a session follows at intake |
| the Status values a plan may take | `modules/knowledge/documentation/primitive/status.py`, read through the record declaration |
| an earlier shape not read | `modules/management/task/services/plan.py` |
| the Status line rewritten alone | `modules/knowledge/documentation/plan/services/status.py` and `modules/knowledge/documentation/plan/services/write.py` |
| no companion of either kind | no code; the exemption below |
| the session's identifier in the front matter | `modules/knowledge/documentation/primitive/record_key.py`, written by the plan and report writers |

**When this document and the code disagree, the document states the requirement and the code is brought to enforce it.** A reader who finds the code doing something else has found a defect in the realization, not a newer requirement, and records it as one; the code is not edited to match a document nobody read, and the document is not edited down to what the code happens to do.

### The exemption from the companion convention
A plan receives **no companion changelog and no companion handoff**, ever. The pattern is one this project already runs — a Changelog-facet file gets no companion changelog as a deliberate stop to the recursion ([changelog.md → Abstract](../changelog/changelog.md#abstract)), and a research receives neither as the same recursion stop ([research.md → Lifecycle and Integrity](../research/research.md#lifecycle-and-integrity)) — and the reason here is stronger than the recursion. The artifact goes with its folder: what is left open at the end of a session is routed by type to the handoff of the document that owns that subject, so a plan's own companions would hold state that another record already owns and nobody maintains. The exemption is stated here rather than assumed, because a reader meeting a plan in a project that pairs everything with a changelog would otherwise read the absence as an oversight.

### Why this facet and the report facet stay separate
The plan and the report are two kinds and not one, on the attribute where they do not overlap at all: **the file name, and the place each is consumed.** A plan is read before any work exists, to begin it; a report is read after, to account for it. They are written by different acts at different moments, they answer to different Status values, and no verb writes both. They are kept apart even though the two records share a type for their shape, because a shape is code and is shared without sharing a responsibility; the question of which types the two kinds should share, and whether the kinds should ever merge, belongs to the session that examines shared service types, `20261013-T161701Z-2296`, and to no session before it.

The plan is also not a Practice document, and the boundary is the artifact rather than the purpose: a Practice is a reusable procedure written to be followed again, while a plan is one agreement about one task, written once and reaped with its folder. A reader told to follow a Practice is being told how this project does a kind of work; a reader told to follow a plan is being told what this session agreed to do.

### Why the module is named `plan`
The module is named for the kind of document it governs, not for the session that uses it. `plan` is the word this project already uses for the artifact and for its type, and a name carrying the session would claim that the kind exists to serve a session — the same kind may be consumed elsewhere, as a template for the same agreement in another repository, and a module named for one consumer's word would make that use an address it does not fit. The facet's specification takes that same name beside it, as every other facet module's does.
