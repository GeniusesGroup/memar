# Task
A Task is the declared intent of a unit of work, together with the one thing that says when it is done. Work undertaken and work required of someone are not the Task itself: they are relations and events around it. The dictionary sense — "any piece of work that is undertaken or attempted", "a specific piece of work required to be done as a duty or for a specific fee" — holds two clauses that come apart (a todo never started is required and not undertaken; work recorded after the fact is undertaken and was never required), so the definition rests on what both share, the intent.

A project, a production run, an issue, a support ticket, a leave request, a reminder, a retroactive record of work done, a user's complaint against the organization and the building of an inner partition wall on the second floor are each a Task. Size is not part of the concept, and neither is the kind of worker or of work: the concept holds with no AI model, with no code and with no text anywhere. Memar leaves Task undefined on purpose ([Terminology → A Term Deliberately Left Open](../../../modules/knowledge/terminology/terminology.md#a-term-deliberately-left-open)), so this document is its definition. Organization's own concepts are Task, User, AI model and how agents run; Memar defines none of them.

Status of this document: **Tentative** (shape still settling). The reading of the node as intent is **Decided** (sitting 8 / Research 001 question 1, owner batch yes 2026-10-20). That Task knows no content, no change, no claim and no storage, and that its stored shape is edges declared by their domains in both directions, is the owner's ruling of 2026-11-05 (task `20261105-T082056Z-24244`), and the reverse names `has_part` and `blocked_by` are the owner's of the same day (task `20261101-T073218Z-4460`, content 90).

## What Task owns, and what it does not
Each domain does its own work. Task answers how a piece of work relates to other work and where it stands, and refers to the owner of everything else. A Task may be the building of a wall: it cannot know what a content, a change, a file or a version is.

| Concern | Owner | What Task holds |
|---|---|---|
| The words of the intent, the reason, the discussion, the report, and their order | [timeline](../timeline/timeline.md), over [content](../../knowledge/content/content.md) | nothing; the timeline whose identity is the Task's identity holds them |
| Keeping, versioning, translating a text, and finding a word in it | [text](../../knowledge/text/text.md) | nothing |
| A content proposed to replace another, and its approval | [content](../../knowledge/content/content.md) | nothing |
| Who is on the work, in which role, and who carries it out now | [group](../group/group.md) | nothing; the group whose identity is the Task's identity holds them |
| Who may act for whom; accepting or declining a duty | [delegate](../../rights/delegate/delegate.md) | nothing; assignment is a delegation |
| Which work goes first | a UI widget of the plural `tasks` domain | nothing |
| What the Task requires of the worker (skills) | [skill](../../knowledge/skill/skill.md), [requires](edges/requires/requires.md) | the requirement edge only |
| The check, the cycle guard, any policy | [rule](../../process/rule/rule_node.md), through the generic `condition_is` | the attachment point |
| The kinds a Task is of, and the words of its position | [label](../../knowledge/label/label.md), through its [`label` edge](../../knowledge/label/edges/label/label.md) | nothing of its own; the word is a label on the Task |
| Time, calendars, notification, budget | their own domains | nothing |
| How an edge or a vertex is written, read or exchanged | the [Graph store](../../../modules-plugable/computer/memory/store/graph/graph.md) and its medium adapters | nothing |

This module imports nothing of documentation, of content and of storage. The Plan and Report facets are [Documentation's](../../../modules-plugable/knowledge/documentation/plan/facet.md), and the services that keep Memar's task records are the pluggable [task module's](../../../modules-plugable/management/task/) (owner, 2026-10-30).

## Model
These elements make the kernel. Each is stated with who may create or remove it and what it triggers; an edge without those does not exist ([Modules → Placement](../../modules.md#placement)).

- **Identity.** A Task is a [thing](../../identity/thing/thing.md), and its identity is Thing's, the same through every move and every change of status; Task declares no identity type of its own. Any participant with authority in the organization may create one. Removal is never a delete: history is the point. The timeline and the group of a Task carry the same identity, so neither needs an edge from the Task to be found.
- **Intent.** What is to be achieved. Its words, images or sounds are placed on the timeline that carries the Task's identity, and each revision is that domain's event.
- **Acceptance check.** The one condition that says the Task is done, attached by the generic `condition_is` to a rule. A Task whose check is empty is not ready to be taken up. The check is decidable by a party that did not write it, in the place the work governs.

### Edges
Task declares two edges between Tasks, containment (`part_of`) and dependence (`blocks`), each written with its reverse; they are declared, with their policies, in [edges/task](edges/task/task.md#model). They differ in cycle rules, in what removal means and in what they trigger, which is why they are two. The steps of a plan are the Task's parts, each a Task of its own with its own check. Memar's `Depends_on` is `blocked_by`; its `Depends_for` is `blocks`. The Task's position and its kinds are words on Label's own [`label` edge](../../knowledge/label/edges/label/label.md), which Task uses and does not restate.

A duplicate Task is superseded by the Task it duplicates, through Thing's [supersedes](../../identity/thing/edges/supersedes/supersedes.md), so Task declares no edge for it. Further relations are wanted and their names are open: a Task that does more than the Task it closes, and a Task closed because a new decision conflicts with an earlier one. None of them is declared until the Modeling Workflow has placed it ([Modeling Rule → Modeling Workflow](../../knowledge/modeling/rules/modeling-workflow/modeling-workflow.md)).

Not in the kernel: assigner, assignee, holder, reviewer, approver, deadline, priority, claim, recurrence, completion policy, outcome vocabulary, skill matching, place, budget, campaign. Each is a relation of its own domain with rules, or a pluggable capability.

### Task as a unit of agreement
One Task is one thing asked, with one check. A request with two checks is two Tasks. A Task that only produced a finding or a proposal is not Complete. It is a part of the Task it improves (`part_of`), or it waits for an approval and is Blocked. Writing a finding changes nothing.

## Status
A Task's position is one of four Status-kind words, Queued, Active, Blocked and Complete, each a [label](../../knowledge/label/label.md) declared by Status under [status/labels](/modules-plugable/knowledge/label/status/labels/), with its meaning, and on the Task through Label's edge ([Documentation → Status](../../../modules-plugable/knowledge/label/status/status.md)).

- A move from one status to another is an event; a rule may allow or refuse it; the user who set it and when are recorded. The event is a Request ([Request → Recording a change of state](../../process/request/request.md#recording-a-change-of-state)): the Task's label edge holds only the current word, and the Request keeps who asked, when and what it replaced. The same holds for a dependence, a label and a parent.
- Blocked is derived when an unended Task `blocks` this one; it is set by hand when the wait is on an answer or an approval.
- A parent's progress is discovered from its parts, not stored as acquired data. Whether a parent may end with open parts is a completion policy, a pluggable capability, and the kernel never closes a parent by itself.
- A Task that ended without passing its check is not Complete. Its outcome (cancelled, abandoned, rejected, partial) is a separate fact from its position, kept under the shared status home.
- A correction is a new fact that refers to the one it corrects, never a rewrite. A reopened Task is a new Task that supersedes the first.

## A Task in the graph
A Task is a vertex and nothing more: what is known of it is the edges above, each with its reverse. Every fact about a Task is an edge, a content on its timeline or a label word, never a field of the Task and never a blob of another domain's facts ([Graph → Refusal contract](../../../modules-plugable/computer/memory/store/graph/graph.md#refusal-contract-graph-forces-its-shape)). Because each edge is written with its reverse, "which Tasks are blocked by this one" and "which are the parts of this one" are reads of one vertex's sides, never a reading of every Task. A title is a content on the Task's timeline, a status is a label word, and showing a Task's facts together is a UI widget (owner, 2026-11-05, task `20261101-T073218Z-4460`, content 93).

## Hand-back
When a Task ends, or stops, it hands back to whoever needs its result: its Status, and the questions only the asker can answer, each blocking the Tasks that need the answer. Where the result and the questions are written is the timeline's.

## Moved to their owners
Each point this module used to state about content, change, claim, holder, priority or a timeline of names is now a need of its owner domain, raised on that domain's task.

| Need | Owner domain | Task |
|---|---|---|
| The contents of a Task's timeline, the replies between them and their order, with no "latest plan" or "latest report"; the report as a content placed there | timeline | `20261105-T082100Z-24244` |
| A content related to the content it intends to change before the change exists, so everyone can see who intends to change it and who has; the revisions a piece of work produced | content: a proposal replies to its target and carries `Proposed`, and acceptance is Thing's `supersedes` ([Content → Proposals and replacement](../../knowledge/content/content.md#proposals-and-replacement)) | `20261105-T082103Z-24244` |
| Taking up work as joining the group with the Task's identity, one `joined` edge per role; the holder is Ownership's `claimer_is`, one holder at a time a Rights rule over it; who sets Active | group ([Group → Membership](../group/group.md#membership)) | `20261105-T082106Z-24244` |
| Ranking queued work and taking a task | a UI widget of the plural `tasks` domain over base reads of Task and Group | `20261105-T082109Z-24244` |
| The position as a Status-kind word and the acts (design, implement, ...) as labels of their own | label | none; the `label` edge already serves, and the call that sets a Status is `memar status set ID WORD --project NAME` |

## Dependencies
`part_of` and `blocks` are the only relations the kernel knows between Tasks. A Task that cannot start until another ends is `blocked_by` it; the status of the blocked Task follows. A Task that is a step of another is `part_of` it. Several Tasks may name one Task as a part: one inspection can serve two phases.

## Memar task-record terms to Task terms
The work item of Memar's tooling, once called a session, is this module's Task (owner, 2026-10-20). The tooling is migrated to the domains it acts on by the service-migration tasks. This table maps the terms of that tooling to the Task concept or to the domain that owns them.

| Memar task-record term | Task concept term, or its owner |
|---|---|
| Project (the task's subject) | a Task carrying the label `project`, reached by `part_of` |
| Conversation | the timeline that carries the Task's identity (timeline); a chat is a way a participant reads and writes it |
| Parent task | `part_of` |
| Plan, Request, Why, Report | contents placed on the Task's timeline (timeline, content) |
| Check, acceptance check | acceptance check |
| Steps | Tasks `part_of` this one |
| Step marked local, delegated | a part carried out by the same member, or by another through a delegation (group, delegate) |
| Next | the Tasks it `blocks` |
| Result (Complete, Blocked, Active) | Status; the outcome when the Task ended without passing |
| Hand-back | hand-back |
| Decisions needed | questions for the asker; they block |
| Status Queued, Active, Blocked, Complete | the same four words, as labels |
| Depends_on | `blocked_by` |
| Depends_for | `blocks` |
| Labels (kind such as design or mechanical) | labels on the Task |
| Claim, claims, fill | joining the Task's group with a role (group), chosen in a UI widget of the plural `tasks` domain |
| Claim holder | Ownership's `claimer_is` on the Task (rights) |
| Sub-agent | a member that is a thing, acting through a delegation |
| Coordinator | the member carrying out a parent Task with open parts |
| Task log | no counterpart in Task: the task services' own [log](../../process/log/log.md); a change of the Task is a Request |
| Task folder, scratch, archive, close, sweep | no counterpart: where material is kept, and what is shown, are not part of the concept |
| Commit naming task ids | no counterpart in Task |
| One task folder holds one task | one Task, one thing asked, one check |

## Assign task rules
- A Task is assigned to users (staff) by the skill it requires. If a Task needs `Design`, a user with `Designer` or `Designing` skill is suggested. In this way `Technology Department` can hire a user with `cognitive science` skills. A team may be formed for one Task and dissolved at its end.
- Assignment is a delegation: a principal with authority gives a Task to a holder. The holder's acceptance is its own act, and silence is not acceptance. Where the authority comes from a law or a case and not a person, the delegate domain owns that question.
- A Task needs neither an assigner, an assignee, a deadline nor a payment to exist; a reminder, a communal job and a record written after the work are Tasks.
- A holder that is a thing (a software agent, a machine) is a first-class case; the principal stays accountable.

## Idea backlog
Nothing below is ratified.

### Task and rule
- **Idea**: a separate task-to-rule attachment was doubted in the note itself. The same note asks whether the need is really a relation to content, to an object, or to an invoice, and whether comment types should grow to carry those relations.
