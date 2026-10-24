---
Title: "Documentation — Report"
Status: Draft
Start Date: 2026-10-16
ID: 497823
---
# Documentation — Report
This document specifies the Report facet: the record one pass of work is accounted for in when it ends. See [Documentation](../../../../modules-plugable/knowledge/documentation/documentation.md) for what a Facet is, and [Documentation → Status](../../../../modules-plugable/knowledge/documentation/documentation.md#status) for what it already says about the task records — where a report's Status is written, which values it draws on, when a plan and its report agree, and the closed set that holds them. None of that is restated here.

## Abstract
A Report-facet document is the file a task's report takes: a record whose reader did not do the work and needs to know what ran, what the task's own check found, how the run ended, and what is still open — held to a stated agreement about which of those they read. It is written when the task ends, whether it ended finished or not, and it lives exactly as long as the folder of the task it belongs to. Its shape — the file name, the front-matter keys, the parts under them and their order, and the limit on a hand-back — is a closed set declared once as a type, so this specification writes none of it as text. What this document states is what a report must carry beyond its shape, who writes it and who reads it, what each part is for, the exemption from the companion convention, and the requirements a party that did not write it can decide from a stated input.

## Introduction
### Motivation
Work that ends silently cannot be accounted for. A task that stops — because its budget ran out, because it is waiting on an answer, or because its check passed — leaves the same folder either way, and a reader who opens it later finds the work's residue with nothing that says whether it was finished or merely stopped. The failure this facet exists to prevent is a task read as done that was not, or a task read as unfinished that met every condition it set for itself: both cost the person who asked more than the work did.

The account is short by design. The party that reads a hand-back — a delegating task waiting on a sub-agent, the owner reviewing a day's tasks — needs a verdict, a place to look, and at most a few lines of what it must decide. A report that carries the task's context back into that reader's has undone the separation it exists to make, so the length of a hand-back is a limit the record's shape carries rather than a matter of the writer's restraint.

### Methodology
This specification was not designed in the abstract. The artifact it governs has been in daily use in this project long before it was named a facet, written by the services under `modules/management/task/services/` and read by every agent that ends a task or waits for one. The proposal that named it — what a report is, whether it is a facet of its own, and what each specification must then carry — is `.agents/tasks/20261016-T003724Z-23508/report.md`, and the owner's answers of 2026-10-16 are what this document applies. Where a decision was the owner's it is cited as such; where the answers left a detail open, the decision and its reason are in this document's own changelog entry.

## Explanation
### What a Report Is
A **report** is one pass of work accounted for: what ran, what the task's own check found, how the run ended, and what the next party still has to open. The **Report-facet document** is the file that holds it — a task's report, named by the shape declared in `modules/management/task/primitive/record.py`, which the file that opens a task writes beside the task's plan.

Two boundaries keep the definition from widening:

- **A report accounts for a pass, not for a subject.** It does not state what was learned about the world; the finding graduates into the document that owns its subject, and what the report keeps is that the work ran and what it showed. A negative result belongs here because the pass that produced it would otherwise leave nothing.
- **A report is scratch, not a document of record.** It goes when its folder goes, and what outlives it is routed by type to the documents that own the material.

### A task holds rounds of reports
A report is bound to a pass of work, not to the task for good: each round of critique ends in a report of what ran and what is to be done, so one task may hold several, as it may hold several plans ([plan.md → A task holds rounds of plans](../plan/plan.md#a-task-holds-rounds-of-plans)). The owner ruled so on 2026-10-23.

- **A report is a content in the task's timeline, not a file of the task**, placed there when the pass ends. A report that is there is never overwritten or removed; the next pass writes another, so each round's account stays as it was written.
- **The current report is the latest placed**, and it is the one the delegating side, `list` and the digest read. A reader that wants the history reads the timeline.
- **A report's Status is a claim in its text, not the task's Status.** The task's Status is held by the task and changed only by a Request ([Request](../../../computer/request/request.md)); the report states the Status its pass ended in, and the task's is changed to agree by the agent that ends the pass. [Documentation → Status](../../../../modules-plugable/knowledge/documentation/documentation.md#status) pairs a plan's and a report's Status today; that pairing becomes this one in the task that re-bases the services on the memory port.
- **A round and a new task are told apart as the plan's specification says**: unchanged request and check make another round with a new plan and a new report; a changed request or check makes a new task that cites the old.
- **Today's realization is one `report.md` per task folder**, which a second round cannot add to without overwriting what requirement 3 forbids; that is a defect of the realization against this section, recorded in the handoff, and no writer gives rounds file names of their own.

### Reader relationship
A report is **read to account for a pass of work**: the reader did not do the work and asks one question — did it do what it said it would, and what is left. What that reader needs is the verdict, in the Status, and the check's own finding behind it; the work that ran, so that the verdict can be weighed against the effort; and what is still open, so that nothing is taken as settled that was not. What the reader does *not* need is the reasoning the writer used to reach the verdict — that is a handoff's material, and the short hand-back exists precisely so the report does not carry it.

Two readers get less than that, and the difference is deliberate. A hand-back is read by one party acting for another, and gets only the Status, the path, and the lines under the hand-back part. The owner reviewing a day gets the same account through `memar task get-decisions-digest`.

This is not [Practice's reader relationship](../../../../modules-plugable/knowledge/documentation/practice/practice.md#reader-relationship), which that specification states: a report is read once, after the fact, to settle whether one pass met its own condition, and is examined for the account of a single pass.

### Who writes a report, and who reads it
A report is written:

- by the agent that ends the task, before it closes, and whether it finished or not;
- by the agent of the delegating task, on behalf of a sub-agent that could only return text, so that the sub-agent's own task carries a record;
- by the service that opens a task, once, when the folder is made — and by nothing else afterwards, since a report that is there is never overwritten.

A report is read:

- by the delegating side, which reads the Status, the path, and the hand-back lines and nothing more;
- by a later task, through `memar git show-task-records`, which prints the plan and the report together;
- by the services that list tasks, which read its Status to mark a task whose report and plan disagree;
- by the owner, through `memar task get-decisions-digest`, which gathers the hand-backs of a day or a conversation;
- by the debrief, which reads the reports of the tasks a task produced.

### What each part is for
Each part of a report is for one job, and the jobs are these: to carry what ran; to carry what the task's own check found; to carry how the run ended, which is the Status the report states together with this part; and to carry what is left open. The parts that carry them, their headings, and their order are the declaration's. A report may carry one further part, which the declaration marks optional: the part a task adds when it needs someone to decide something, held to the line limit the declaration gives, and omitted entirely when there is nothing to decide — its absence is what says there is nothing.

A report carries one more thing that is not a part: the identifier of the task the report belongs to, written in its front matter, for the reason [the plan's specification gives](../plan/plan.md#who-writes-a-plan-and-who-reads-it) — the record must not presume that it is a file.

### The requirements
Each requirement below is decidable from a stated input by a party that did not write the report. None of them names a field, a part, a Status value or a count, because each of those is the closed set's, held in `modules/management/task/primitive/record.py` or in `modules/knowledge/status/primitive/status.py` and reached by calling it.

1. **The report states what the task's own check found**, and is read against the check its plan states.
2. **The report's Status is one of the values the declaration gives a task report.** A value outside them is named rather than guessed, and a report whose Status is empty states nothing yet and is not checked.
3. **A report that is there is never overwritten.** The service that writes a report creates the file and leaves an existing one untouched.
4. **A report is a hand-back exactly when it states a Status the vocabulary gives a report, that Status agrees with its plan's as [Documentation → Status](../../../../modules-plugable/knowledge/documentation/documentation.md#status) states once for the pair, and its hand-back part holds no more lines than the declaration allows.**
5. **A report carries no companion changelog and no companion handoff** — see [The exemption from the companion convention](#the-exemption-from-the-companion-convention).
6. **The report states the identifier of the task it belongs to**, in its front matter, so that a reader finds it in the document rather than by reading a folder name.
7. **A task may hold several reports, and a report is never rewritten into an earlier one.** The current report is the latest placed in the task's timeline; each round ends in a report of its own ([A task holds rounds of reports](#a-task-holds-rounds-of-reports)).

### Where the code is, and what a reader does when it disagrees
The code that enforces the requirements above lives today under `modules/management/task/services/`, not in this module's `services/` folder: task `20261015-T123046Z-17544` moved the services out of `.agents/scripts/services/` into the module of their domain, and the task module holds a task's plan and report together. Whether the code that enforces this facet moves on into this module's `services/` folder is not decided, and no second move of the same code is made here.

Which service holds each requirement today, so that a reader looking for the enforcement does not have to search for it:

| Requirement | Enforced today by |
| --- | --- |
| what the check found | no code; a reader's judgement, reading the report against the plan's check |
| the Status values a report may take | `modules/knowledge/status/primitive/status.py`, read through the record declaration |
| a report that is there is never overwritten | `modules/management/task/services/report.py` |
| what makes a hand-back | `modules/management/task/services/report.py`, read by the services that digest a day's decisions |
| no companion of either kind | no code; the exemption below |
| the task's identifier in the front matter | `modules/knowledge/content/primitive/record_key.py`, written by the report writer |

**When this document and the code disagree, the document states the requirement and the code is brought to enforce it.** A reader who finds the code doing something else has found a defect in the realization, not a newer requirement, and records it as one; the code is not edited to match a document nobody read, and the document is not edited down to what the code happens to do.

### The exemption from the companion convention
A report receives **no companion changelog and no companion handoff**, ever. The pattern is one this project already runs — a Changelog-facet file gets no companion changelog as a deliberate stop to the recursion ([changelog.md → Abstract](../../../../modules-plugable/knowledge/documentation/changelog/changelog.md#abstract)), and a research receives neither as the same recursion stop ([research.md → Lifecycle and Integrity](../../../../modules-plugable/knowledge/documentation/research/research.md#lifecycle-and-integrity)) — and the reason here is stronger than the recursion. The artifact goes with its folder: what lasts of a pass is routed by type to the documents that own the material, so a report's own companions would hold state another record already owns and nobody maintains. The exemption is stated here rather than assumed, because a reader meeting a report in a project that pairs everything with a changelog would otherwise read the absence as an oversight.

### Why this facet and the plan facet stay separate
The report and the plan are two kinds and not one, on the attribute where they do not overlap at all: **the file name, and the place each is consumed.** A plan is read before any work exists, to begin it; a report is read after, to account for it. They are written by different acts at different moments, they answer to different Status values, and no verb writes both. They are kept apart even though the two records share a type for their shape, because a shape is code and is shared without sharing a responsibility; the question of which types the two kinds should share, and whether the kinds should ever merge, belongs to the task that examines shared service types, `20261013-T161701Z-2296`, and to no task before it.

### Why the module is named `report`
The module is named for the kind of document it governs, not for the task that uses it. `report` is the word this project already uses for the artifact and for its type, and a name carrying the task would claim that the kind exists to serve a task — the same kind may be consumed elsewhere, as a template for the same account in another repository, and a module named for one consumer's word would make that use an address it does not fit. The facet's specification takes that same name beside it, as every other facet module's does.
