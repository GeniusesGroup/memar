# Task
A Task is the declared intent of a unit of work, together with the one thing that says when it is done. Work undertaken and work required of someone are not the Task itself: they are relations and events around it. The dictionary sense — "any piece of work that is undertaken or attempted", "a specific piece of work required to be done as a duty or for a specific fee" — holds two clauses that come apart (a todo never started is required and not undertaken; a change recorded after the fact is undertaken and was never required), so the definition rests on what both share, the intent.

A project, a production run, an issue, a support ticket, a leave request, a reminder, a retroactive record of a change, a user's complaint against the organization and the building of an inner partition wall on the second floor are each a Task. Size is not part of the concept, and neither is the kind of worker or of work: the concept holds with no AI model and with no code anywhere. Memar leaves Task undefined on purpose ([Terminology → A Term Deliberately Left Open](../../../docs/terminology.md#a-term-deliberately-left-open)), so this document is its definition. Organization's own concepts are Task, User, AI model and how agents run; Memar defines none of them.

Status of this document: **Tentative** (shape still settling). The reading of the node as intent is **Decided** (sitting 8 / Research 001 question 1, owner batch yes 2026-10-20). Other kernel edges and capabilities still follow open questions in the [handoff](task.handoff.md).

## What Task owns, and what it does not
Each domain does its own work. Task answers four questions about a piece of work — what is to be achieved, how it relates to other work, where it stands, and what came of it — and refers to the owner of everything else.

| Concern | Owner | What Task holds |
|---|---|---|
| The words of the intent, the reason, the discussion, the report, a timeline of any of them | [content](../../knowledge/content/content.md) | a reference to the content; a Task is also a content, and holds none of the text |
| Keeping, versioning, translating that text, and finding a word or phrase in it | [text](../../knowledge/text/text.md) | nothing; Task and content understand nothing of text, so search is text's |
| The discussion of a Task as a sequence over time | [timeline](../timeline/timeline.md) | nothing; each Task has one timeline, and every participant, human or not, writes in that same one |
| Who is on the Task, and in which role | [group](../group/group.md) | nothing; a Task gains a group when people join it |
| Who may act for whom; accepting or declining a duty | [delegate](../../rights/delegate/delegate.md) | nothing; assignment is a delegation |
| What the Task requires of the worker (skills) | [skill](../../knowledge/skill/skill.md), [requires](edges/requires/requires.md) | the requirement edge only |
| The check, the cycle guard, any policy | [rule](../../computer/rule/rule.md), attached through `condition_is` | the attachment point |
| The kinds a Task is of, and why it carries one | [label](../../knowledge/label/label.md) | nothing; a kind is a label with its explanation |
| The words that mark a position (Queued, Active, …) | [status](../../knowledge/status/status.md) | the position, as the shared loop-edge |
| Time, calendars, notification, budget | their own domains | nothing |
| How records are stored or exchanged | storage, and the adapters of the bridge to Memar | nothing; no file system or version-control concept is part of a Task |

A Task never carries the text of a plan, a report or a timeline, and never decides how such text is kept. When a need seems to require that, the need belongs to content or text and is raised there. This module imports nothing of documentation: the Plan and Report facets are [Documentation's](../../../modules-plugable/knowledge/documentation/plan/plan.md), and the services that keep a task as a folder holding a `plan.md` and a `report.md` are the pluggable [task module's](../../../modules-plugable/management/task/) (owner, 2026-10-30; an earlier move of the facets into this module, to cut a cycle, was reversed because the dependence, not the facets, was what had to go).

## Model
These elements make the kernel. Each is stated with who may create or remove it and what it triggers; an edge without those does not exist ([Modules → Placement](../../modules.md#placement)).

- **Identity.** A Task is a thing; its identity is the thing domain's (`ThingUUID`, `Field_TaskID`), the same through every edit of its intent, every move, and every change of status. Any participant with authority in the organization may create one. Removal is never a delete: history is the point.
- **Intent.** What is to be achieved, as content: text, images, audio. The creator writes it; a revision is an event on the same identity.
- **Acceptance check.** The one condition that says the Task is done, attached by `condition_is` to a rule. A Task whose check is empty is not ready to be taken up. The check is decidable by a party that did not write it: a change applied, or a decision recorded, in the place that change or decision governs.
- **`part_of`** `(task)-[:part_of]->(task)`. Containment; many parents allowed, acyclic. The steps of a plan are the Task's children, each a Task of its own with its own check. The owner of both ends creates it; removal is an event; a cycle is refused by a rule.
- **`blocks`** `(task)-[:blocks]->(task)`. The first must reach its end before the second may start. This is dependence, and it is not containment: they differ in cycle rules, in what removal means, and in what they trigger. Memar's `Depends_on` is this relation read from the blocked end.
- **`changes`** `(task)-[:changes]->(content revision)`. The revisions the Task produced; this is the Change Set. A report is a content reached this way. The Task is the history a version-control message only imitates.

- **`same_ask`** `(task)-[:same_ask]->(task)`. Two Tasks ask the same thing, a duplicate being one such case. When the one it points to is Complete, this one is Complete with it, or ends at once as a duplicate. Created by someone with authority over this Task; removal is an event. Further relations are wanted and their names are open: a Task that does more than the Task it closes, and a Task closed because a new decision conflicts with an earlier one.

Before it changes a content, a Task is related to that content by an edge, so that everyone can see which Tasks intend to change it and which have. When the Task ends the edge is removed or becomes another edge. The name of this edge, and whether it also keeps two Tasks from writing the same content at once, are open ([handoff](task.handoff.md#owners-rulings-the-second-round-2026-10-18)).

Not in the kernel: assigner, assignee, reviewer, approver, deadline, priority, claim, recurrence, completion policy, outcome vocabulary, skill matching, place, budget, campaign. Each is a relation with rules or a pluggable capability.

### Task as a unit of agreement
One Task is one thing asked, with one check. A request with two checks is two Tasks. Each Task has one timeline of its own, owned by content, that all its participants use. Any participant may add to a content in that timeline as many texts as it wants, each related to the content by an edge of its own kind and for its own reason, some of which only the author knows and uses on its way to the Task's output; no other participant is obliged to read them.

A Task that only produced a finding or a proposal is not Complete. It is a step of the Task it improves (a child through `part_of`), or it waits for an approval and is Blocked. The finding itself is content and changes nothing by being written.

## Status
A Task's position is one of four words, each a loop-edge on the Task as [Status](../../knowledge/status/status.md#what-a-status-is) describes, so that code uses the edge type.

| Status | Meaning |
|---|---|
| Queued | Declared and waiting to be taken up; nobody holds it. |
| Active | Being carried out now by a holder. |
| Blocked | Cannot continue until something outside the work arrives: an answer, an approval, or the end of a Task that `blocks` it. The record states what it waits for. |
| Complete | The acceptance check passed. A Task that was found to need nothing is Complete because the check already held. |

- A move from one status to another is an event; a rule may allow or refuse it; the user who set it and when are recorded. The event is a Request ([Request → Recording a change of state](../../computer/request/request.md#recording-a-change-of-state)): the Task keeps only the current Status, and the Request keeps who asked, when and what it replaced. The same holds for a claim, a priority, a dependence, a label and a parent.
- Blocked is derived when an unended Task `blocks` this one; it is set by hand when the wait is on an answer or an approval, which the Task states.
- A parent's progress is discovered from its children, not stored as acquired data. Whether a parent may end with open children is a completion policy, a pluggable capability, and the kernel never closes a parent by itself.
- A Task that ended without passing its check is not Complete. Its outcome (cancelled, abandoned, rejected, partial) is a separate fact from its position, kept under the shared status home; the vocabulary is an open question.
- A correction is a new fact that refers to the one it corrects, never a rewrite. A reopened Task is a new Task that supersedes the first.

## How a Task is stored
A Task is a node of the [record contract](../../../modules-plugable/computer/memory/store/record/record.md), stored in the class its project binds to work records, and a plan, a report and every other content are nodes of their own. What a kernel module takes of that store is only the reference to an address ([Memory Address](../../computer/memory/address/address.md)): a Task is named by an address. The rest of this section (parts, domain keys, labels) is only `record`'s and is asked of the owner in the handoff ([Does the Task need more of `record` than the reference to an address?](task.handoff.md#does-the-task-need-more-of-record-than-the-reference-to-an-address)). Each domain keeps one part on a node under its key. The parts of the domains of this section (the Task, the timeline, the Request, the placement and the content) are the JSON Canonicalization Scheme of RFC 8785 applied to the value; the choice is these domain modules' and not the record contract's, and another organization's domains may choose another encoding and key by writing it into their own module. The scheme is: UTF-8, keys in sorted order, no insignificant whitespace, integers only, an absent field omitted, an id written as its lowercase hyphenated text, so that equal values are equal bytes and a token compares values. The scheme is written once in code, and each domain module states its parts' encoding by pointing to it. Three parts are not JSON: `text` is the bytes of a text as they are, `blob` the bytes of a content that is not text, and `labels` the port's own concatenation of ids. The payload of a Request, `request-data`, is the JSON object that maps the string `node id/domain key` to the base64url text of the new bytes of that part. A new encoding of a part is a new domain key.
- **The Task's node** holds `task`, issued by this module: the legacy id (`legacy_id`), the title, the Status as the word of the Status vocabulary (Blocked is written only when the wait is on an answer; a task blocked by the tasks it depends on is shown so by the reader that computes it from `depends_on` and never has it written), the holder, the instant of the claim (`claimed_at`), the priority, the parents as a sorted list of ids, the tasks it depends on as a sorted list of ids, the id of its conversation, and its start. It holds `timeline`, issued by the timeline module: a map from the name of a content to the id of its current content. It holds `group`, issued by the group module, absent until someone joins. It holds `request-head`, issued by the Request domain, and `labels`, the port's.
- **A Request** is a node with the parts `request` and `request-data`, a **placement** a node with `placement` and, once ended, `placement-end`, a **content** a node with `content` (its name, its media type and the id of its text or its blob), a **text** a node with `text` and a **blob** a node with `blob`. A conversation is a node with `group`, which holds its legacy id and nothing else until members join, and it is created in the batch of the creation Request of the first task that names it.
- **Labels** classify nodes: one for each kind of node above, the kinds of a content (the plan, the report, a document, a script, a test, scratch), the id of the timeline on a placement, the id of each node a Request changed, and the syntax of a text. The text nodes of a plan, a report and every document of Markdown carry the label of documentation, which attaches that domain's check to them. Each label is declared by the module that owns its meaning, in that module's `labels/`, as [Label](../../knowledge/label/label.md) says; the layout of a view maps them to folders and is the project's.
- **A content is revised** by writing a new content with the same name, placing it, and moving the Task's `timeline` entry for that name to it in one batch with an expectation on the token read, which is a change of state recorded by a Request. A name is a relative path, `plan.md`, `report.md` or `docs/options.md`, written with `/`, with no empty segment, no `.` or `..` segment and no root, and unique when compared without regard to case; the current content of a name is the one its entry points to.
- **The change of a part that holds a current value** (all but `request-head`, which is written with the Request it names, and the immutable nodes) is a change of state, recorded as [Recording a change of state](../../computer/request/request.md#recording-a-change-of-state) says. The fields above are named once, in code, when the verbs are built.

Owed: memory.stored-shape

## Hand-back
When a Task ends, or stops, it hands back to whoever needs its result: its status, the report content reached through `changes`, and the questions only the asker can answer. A question for the asker is raised on the Task, as discussion content, and blocks the Tasks that need the answer. The Task does not carry the report's text.

## Queueing and claiming (capability)
Ranking and taking Tasks is not the kernel's. A pluggable capability owns it:

- **Queue.** Orders the Tasks in Queued by priority, a whole number from 1 to 10, the higher sooner; a Task with none counts as 5. Anyone, a person or an agent, may change a priority, whatever the status; the change is an event.
- **Claim.** A holder takes one Queued Task so no other takes it. The claim makes the holder a member of the Task's team with a role, moves the Task to Active, and is refused if another holder has it. The holder is a person, or a thing (a software agent, a machine) acting for a principal who stays accountable.
- **Fill.** A holder asks for the first N Queued Tasks in line and claims them together, optionally only those of one label.

Its home is not yet decided; see Open questions.

## Dependencies
`blocks` and `part_of` are the only relations the kernel knows between Tasks. A Task that cannot start until another ends is `blocks`-ed; the status of the blocked Task follows. A Task that is a step of another is `part_of`. Several Tasks may name one Task as a step: one inspection can serve two phases.

## Memar task-record terms to Task terms
The work item of Memar's tooling, once called a session, is this module's Task (owner, 2026-10-20), and the folder of records it keeps is that Task's record. The tooling is kept as it is and nothing more is built on it beyond this module. A task id in a commit message stays as it is. This table maps the terms of that record to the Task concept's terms; it does not define what a task is as a concept — that meaning is still open (see the handoff section Owner intake — Session versus Task span).

| Memar task-record term | Task concept term |
|---|---|
| Task folder (the record) | the Task's record: its declared state and the content reached through `changes` |
| Project (the task's subject) | the organization or group the Task belongs to |
| Conversation | the Task's own timeline, owned by content; a chat is a way a participant reads and writes it, not a record of its own |
| Parent task | `part_of` parent |
| Plan | the Task's declared state: intent, check, reason, children, successors |
| Request | intent (content) and acceptance check (rule) |
| Check, acceptance check | acceptance check |
| Why | reason, content on the Task |
| Steps | child Tasks through `part_of` |
| Step marked local | child Task held by the same holder |
| Step marked delegated | child Task held by another holder through a delegation |
| Next | the Tasks it `blocks`, and the first move written as content |
| Report | a content reached through `changes` |
| Result (Complete, Blocked, Active) | status; the outcome when the Task ended without passing |
| Hand-back | hand-back |
| Decisions needed | questions raised on the Task for the asker; they block |
| Status Queued, Active, Blocked, Complete | the same four words |
| Depends_on | `blocks`, read from the blocked end |
| Depends_for | `blocks`, read from the blocking end |
| Priority (1 to 10) | priority, owned by the queue capability |
| Labels (kind such as design or mechanical) | labels on the Task |
| Claim, claims, fill | claim, fill in the queue capability |
| Claim holder | a member of the Task's team with a role |
| Sub-agent | a holder that is a thing, acting through a delegation |
| Coordinator | the holder of a parent Task with open children |
| Task log | the Task's events |
| Task folder, scratch | no counterpart: working material is content, and where it is kept is not part of the concept |
| Archive, close, sweep | no counterpart: nothing is lost; what is shown is a visibility question for authorization |
| Commit naming task ids | `changes` |
| One task folder holds one task | one Task, one thing asked, one check |

## Assign task rules
- A Task is assigned to users (staff) by the skill it requires. If a Task needs `Design`, a user with `Designer` or `Designing` skill is suggested. In this way `Technology Department` can hire a user with `cognitive science` skills. A team may be formed for one Task and dissolved at its end.
- Assignment is a delegation: a principal with authority gives a Task to a holder. The holder's acceptance is its own act, and silence is not acceptance. Where the authority comes from a law or a case and not a person, the delegate domain owns that question.
- A Task needs neither an assigner, an assignee, a deadline nor a payment to exist; a reminder, a communal job and a record written after the work are Tasks.
- A holder that is a thing (a software agent, a machine) is a first-class case; the principal stays accountable.

## Open questions
Only the owner can decide these. The defaults are those of [Research 001](task.research.001.md#open-questions), and the full list is in [task.handoff.md](task.handoff.md#research-001-questions-and-next-steps-2026-10-15).

- **Is the node the declared intent, or a unit of work required of someone?** Default used above: the declared intent. Changing it rewrites the definition and the Assign task rules.
- **Does a Task have a team from birth, or acquire one when people join?** Default used above: acquired.
- **Is completion propagation kernel or pluggable?** Default used above: pluggable.
- **Where does the queue capability live?** It ranks and claims Tasks and owns no text; it is pluggable. No `modules-plugable/management/` module holds it yet.
- **Is Blocked a stored position or a derived one?** Used above: derived from `blocks`, stored when the wait is on an answer.
- **What is the outcome vocabulary, and does it live with the shared status home?** Default: completed, partial, rejected, cancelled, abandoned, apart from position.
- **Do the statuses live as `status/<name>/` under this module, and the Scrum and XP words as labels?** Default: yes; [task-status.kh](edges-loop/status/task-status.kh) mixes both.

## Idea backlog
Nothing below is ratified.

### Task and rule
- **Idea**: a separate task-to-rule attachment was doubted in the note itself. The same note asks whether the need is really a relation to content, to an object, or to an invoice, and whether comment types should grow to carry those relations.
- **Review questions**: if comment types can say "this comment is about an invoice", is there any task-rule edge left? Invoice price shown in a GUI is a projection, not a new edge.
