---
name: documentation-handoff
description: defines how a handoff between tasks is produced and consumed, and how a task handles what falls outside its own task — a mid-task tangent, another task's wrong work, queued work, a question only the owner can answer, a task's size and its follow-ups; use when a task or conversation ends with decisions, open questions, or continuation to preserve, when work starts from a handoff, or when one of those cases arises. Not for a trivial exchange that decided and opened nothing, not what a handoff is (handoff.md), and not a changelog entry (documentation-changelog)
---

# Documentation — Handoff Practice
> **Purpose:** This practice defines how a handoff is produced at the end of a task and how it is consumed at the start of the next one. It is the procedural companion to [handoff.md](./handoff.md), which defines what a handoff is, why its structure is what it is, and the risks it controls — that document is assumed reading, and its rules are not restated here.

---

## When This Practice Applies
A conversation ends only when the person who started it declares the work finished, not when one reply or task is complete; until then, keep its state. A task is narrower than a conversation, which holds several of them: a task ends when its check passes or it stops (`memar task --help`). Produce a handoff when a task or a conversation ends with any of these true:

- the discussion reached decisions or resolutions worth preserving
- ambiguities were resolved whose reasoning would otherwise be lost
- open questions or assumptions exist that a future task needs to know about
- the topic will continue in a later task, or a different agent may pick it up
- the task's work touched other artifacts in ways those artifacts do not yet reflect

Do not produce a handoff when:

- the exchange was trivial (simple Q&A, quick factual answer)
- nothing was decided, resolved, or opened
- no continuation is anticipated
- everything the task concluded has already graduated into governed documents (see the graduation rule in [handoff.md → What a Handoff Is](./handoff.md#what-a-handoff-is))

The lists above govern task end. A tangent detected mid-task is a separate trigger — see [Mid-Task Tangents](#mid-task-tangents).

---

## Mid-Task Tangents
A **tangent** is a request that opens a development thread whose context the current task will not otherwise need. Clarifying questions and small edits related to the task's topic are not tangents. Bounded work the current task needs integrated is not a tangent either — it is delegation to a sub-agent per the skill's runtime rules, and it stays in this task.

When a tangent appears mid-task, produce the handoff at once rather than at task end:

1. Propose a separate task for the tangent — once; the person's choice to continue here is final.
2. Record the tangent's state into the appropriate handoff (see [Placement](#placement)) so the fresh task starts from it instead of from scrollback.
3. State in one line what was recorded and where — a silent handoff hides its selection asymmetry.
4. Load no more of the tangent's context into the current task than recording requires.

---

## Correcting Another Task's Work
A task that finds another task's work in the shared medium wrong — a claim its source does not support, a deleted record, a question closed without an answer — may correct it; work does not belong to the task that wrote it. Two conditions bind the correction:

- **The other task has finished.** A task still running may be about to change the same passage, and a correction made under it is either overwritten or overwrites. Before correcting, establish that it has ended: its plan's Status is Complete or Blocked rather than Active or Queued, or the person who started it says it is done; a task the agent cannot see the state of is asked about, not assumed finished. Then confirm the problem still stands in the current text, since the task may have fixed it before ending. A small defect that is certain (a corrupted sentence, a stale line, a broken test) is fixed in the same turn without asking the owner, even in a committed file or another task's work, and reported in one line (the owner, 2026-10-13); a fix that is large, or whose intent is unclear, is queued as a task.
- **The correction is reported.** Each correction is recorded where the changed document records changes, and listed at the end of the correcting task's report, and in what it tells the person, so the person and the original author learn what was changed in their work and why.

---

## Committing the Work of a Task
A commit is the owner's to allow, and a task's commit is shaped so that the history stays readable.

- **Permission.** Nothing is committed without the owner's say-so, and a sub-agent never commits (the owner, 2026-10-13). A standing word, such as "commit when the chat is finished", is the owner's say-so for that chat only, and for the files below.
- **Whose files.** A chat commits only the files it changed, with the small earlier changes already in those files; the work of other chats in the same tree is theirs to commit, and a folder the owner says two chats are working in is left to them (the owner, 2026-10-16). A small touch, such as one repaired link in a file the commit is not about, waits for a later commit and does not widen this one.
- **When.** Once the chat has said it has nothing left to do, not before.
- **Shape.** A commit made by mistake or left incomplete, before it is pushed, is amended or folded (`git commit --amend` when only the intended files are staged, or `modules-plugable/computer/git/services/_host_git_cli.py commit --fold N`), and is not followed by a second commit; after committing, `git status` is read, since a file the same task staged and left out is a defect (the owner, 2026-10-14). Commits are grouped by top folder and are few: each commit has a cost in history and in review (the owner, 2026-10-15). A move that git must record as a rename is committed alone, as a pure move with no other edit, so that its similarity check sees a rename and not a deletion and an addition; the repairs the move makes necessary follow in a later commit.
- **A small task gets no task.** Committing a batch, one edit, staging, or a lookup is done in place, with no task and no sub-agent: a task exists to make a task's decisions persist, and opening one with a sub-agent for a commit costs far more than the work (the owner, 2026-10-15).

---

## Old Task Folders
Rulings of the owner on 2026-10-13, for the folders the daily sweep leaves behind. A task whose plan has no text is treated as finished, since no plan will be written for it. A task about another repository, the organization repository for one, is moved to that repository's `.agents/tasks` for review there, since this side has no view of whether it was done. A finished folder is moved to the recycle bin with `memar git trash-task-folder`. A plan that holds several tasks is checked task by task, and the checking agent does the small leftovers itself.

---

## Queued Work and Its Hand-Back
Every task a conversation carries spends its context, so a further task is recorded rather than done there. The commands, their options, and the limits they enforce are declared by the `--help` of `memar task` and of each of its verbs, each stating its own; this section says why the work runs as it does and what each participant owes. The conversation opens a further task as a queued task, writes its plan whole — the Request, the check that says it is done, the shape of its report, and its Why — and leaves it. A conversation may queue any number of tasks, and never does a queued task's work in its own context. Status Queued means planned and taken by no one; it becomes Active when an agent claims it. A queued plan whose Request is empty is not ready, and is not taken.

- **Priority.** A plan carries a priority that orders the queue, in the range and with the default `memar task priority --help` gives. Anyone, a person or an agent, may change it, whatever the task's status, and says in that plan why: a priority is a judgment about the task, and the next reader of the plan weighs it only when its reason is there.
- **Taking queued work.** An agent asked to do some of the queued tasks works them as the delegating agent. `memar task claims N` takes the N first in line — the highest priority first, the oldest opened first among equals — claims each so that no other agent takes it, and prints each one's brief. When the first in line carries a topic, `claims` takes that topic's queued tasks next, in line order, rather than unrelated ones that rank above them, and says which higher-priority tasks it passed over; a task of another topic fills what is left only when the delegating agent asks. It takes only from the one project the delegating agent names, with no default and no way to take from all, because one run serves one project and a guessed or spanning scope would hide which project the work lands in — so a delegating agent that does not know the project asks the owner, and how the project is named is said in its help. A project is named with the flag for the kind of thing the delegating agent has — `--project NAME` for a name, which `memar project find` resolves, `--project-path PATH` for a folder — and never one in the other's place; a word is never reasoned about nor turned into a guessed path ([`add_project_flags`](../../../../modules/process/project/services/find.py)). The delegating agent hands a batch of one topic to one fresh sub-agent, each task in it keeping its own plan and its own report, and never one sub-agent tasks of different topics; it works none of them in its own context. Memar starts no agent: the delegating agent starts each the way its runtime starts a sub-agent. Nothing keeps a claim fresh, so a claim left by an agent that died lapses after the time `memar task claim --help` gives, and the task can then be taken or queued again.
- **The hand-back.** A task that another will read ends with a short hand-back: its report.md's Status and path, and, only when it needs someone's decision, the few lines `memar task ensure --help` allows under a `## Decisions needed` heading, each the question, its options, and the one it recommends. Everything else stays in report.md. A hand-back with no Status, with more lines than that, or with a Status that disagrees with its plan is a failed hand-back ([Status](../documentation.md#status)), and the delegating agent does not count that task done. A sub-agent that could only return text hands its report back, and the delegating agent writes it as its report.md and sets its Status.
- **Blocking tasks.** A task the conversation cannot go on without — a step still to come reads its Result, or its Result could change the plan — is blocking; every other queued task is independent of it. The conversation records what it waits for in its own plan's `Depends_on` (the key a task's plan carries for the tasks it cannot start without, [Plan](../../../../modules/management/task/plan/plan.md)), is Blocked, and tells the owner at once; a queued task with a `Depends_on` that is not yet met is itself Blocked, and cannot be claimed or started until each cited task is Complete. Where a task runs follows two questions: whether the conversation needs its result, and whether it needs the owner (questions, critique, back-and-forth). A task whose result the conversation needs and that needs no owner is carried out by a sub-agent that returns only its hand-back. A task that needs the owner, blocking or not, is carried out in a new chat, because a conversation that takes in several tasks' reading and the owner's answers grows large and every later turn pays for all of it. Whether the task needs the owner alone decides a new chat: a chat with nothing to ask the owner only gives the owner one more chat to watch. A task whose result the conversation does not need, such as a requirement B found while developing A, is independent: the conversation writes its plan whole and is done with it, following neither its exchanges with the owner nor its end; it opens its chat when the task needs the owner, and otherwise hands it to a sub-agent once its own work leaves room, or leaves it queued. A conversation that waits for tasks in new chats cannot learn that they ended, so it asks the owner to tell it. The new chat is handed `memar ai get-task-plan-carry-out-brief ID`, and the owner is shown `memar ai get-new-chats-ask --task-id ID ID...`, which reads what blocks from the delegating task's `Depends_on`. The conversation resumes when the owner says the task is done, reading the hand-back alone with `memar git show-task-records --hand-back`, and consumes the decisions made without re-entering their reasons, unless its own work meets a problem with one. A problem found later in a finished task's work returns to that task's chat as a prompt stating the problem and the new ask, and opens a task only where the work is new. `memar ai get-new-chats-ask --help` says how a runtime that cannot open a chat says so.
- **The digest.** Last, the delegating agent runs `memar task get-decisions-digest` for its own conversation, as the help says, and gives the owner that one digest rather than a question per task. It gathers every task's `Decisions needed` into a single list, each task's entries under its title, priority, Status, and report, and every failed hand-back, with decisions or without, marked as one, and flags (`concerns`) a task not Complete that looks finished or abandoned; a Complete task is in it only when it holds decisions or a failed hand-back. The same command with `--day` is the owner's review: every task that changed that day, one by one with a summary of its Result, which the owner and an agent read together, and the agent then archives (`memar git archive-task-records`) and closes with `memar git trash-task-folder` the tasks the owner confirms finished and no other; a project that wants its finished tasks kept sets `tasks` in its preferences and closes none, and what lasts is in the output and the changelog. The digest exists so that the owner's attention goes only where it is needed: the owner reads one list of decisive questions, each with its options and a recommendation, instead of thirty reports. Which questions reach it, and which an agent settles itself, is set in [Cognition Practice → Norm Application Points](../../../../docs/cognition.practice.md#norm-application-points).

---

## Questions Found During a Task
A question the task turns up that only the owner can answer is written where it lasts: an entry under Open Questions in the handoff of the document it concerns ([Placement](#placement)). The fields an entry carries, and the test it passes, are in [handoff.md → Open Questions](./handoff.md#open-questions) and are not repeated here. The conversation, a report, and a task hold at most a pointer to the entry, because none is where the question lasts: the conversation sinks under later text, and a task's folder is swept once finished while its plan and report are kept on the project's records branch only as the record of a task done, where no reader looks for a question still open.

- **Never a task.** A question for the owner is written as an entry and is never queued as a task of its own, save the one case the next bullet names: recording a question needs no task, however large or small the question. If investigation could make it smaller, the task that found it does that investigation, or names it under Options as work the answer waits for, and writes the question that survives; if the owning material settles it, ask nothing and record the decision Tentative, as [Cognition Practice → Norm Application Points](../../../../docs/cognition.practice.md#norm-application-points) says. A queued task titled as the recording of a question is a mistake: its question is written as an entry and its folder is trashed, not archived. The conversation asks the one question being answered now, and is never the only place it is written.
- **A question about the Memar skill or Memar's scripts is a task at once.** A question about what the skill (`.agents/skills/memar/SKILL.md`) or one of Memar's scripts (`.agents/scripts/`) should say or do is queued, when it is found, as a task with `--parent` naming the task that found it and its plan written whole ([Queued Work and Its Hand-Back](#queued-work-and-its-hand-back)). Its task is the change, not a decision about it: the plan's check is that the change is applied, its first step is the study that settles what the owning material settles, and it asks under its report's `Decisions needed` only the rulings the owner alone can give, which the digest gathers; while one is unanswered the task is Blocked, never Complete ([A task is for work](#a-task-is-for-work)). The reason is the owner's (2026-10-15): the skill and the scripts shape how every task works, so a question about them bears on the whole development path, and an entry left waiting for the owner's reading lets every task meanwhile work by the rule in doubt; such a question is therefore worked fast rather than parked, and neither the skill nor the scripts has a handoff where an entry would be read. A question about any other document stays an entry.
- **Who writes it.** The task that found it, before it ends. A sub-agent that may not write files returns the entry text in its report, and the delegating agent writes it before the task counts as done.
- **The task is done at once.** The task that raised the question is done when its own check passes; its report's Left open names the entries, and its `Decisions needed` holds one line per entry — the question, the recommended option, the path of the handoff. Where the task cannot meet its check without the answer, it ends blocked or approval-required, with the entry written and cited. Resuming is a new task that reads the handoff ([Consuming a Handoff](#consuming-a-handoff)); nothing keeps a task open to carry a question.
- **How it is answered.** The owner, or an agent on the owner's word, writes the answer where it belongs — a Decided decision, or the governing document with a changelog entry — and removes the entry, as the graduation rule says; the changelog names the entry's heading, so the question stays findable after it is gone. Before a question reaches the owner, the delegating agent hands it to an agent with `memar ai get-task-questions-answer-brief ID`; an answer that agent is sure of, outside the four kinds the Norm Application Points always send to the owner, is written as a Tentative decision with its reasons and the entry removed.
- **A limit.** An entry in a tree that is not committed lives on that machine only; another machine can answer it after it is committed.

---

## Sizing a Task and Recording Follow-Ups
This section holds for every project that works the Memar way, so it is stated here once and not in a project's preferences. What a delegation must establish is in [Agency → Interaction With an Agent](../../../../docs/agency.md#interaction-with-an-agent); this section says how large the task delegated or queued should be, and what becomes of the work the task turns up.

### The size of a task
A task carries a load before it does any work: the skill, the Cognition sections, the plan, and the governing documents its steps name. That load is paid again by every new task, and every turn re-reads everything the task has accumulated. A task's size is therefore set by weighing the load of a task against the work it holds, together with what its tasks share — the files they change and the reading that governs them — and not by a count of files or a fixed number of tokens, which no measurement here supports: a module of a hundred small files is one task and one context, while a single very large output may not be.

- **Split** a task at a decision the owner must take; at a change that can be tested alone and whose files and governing reading differ from its neighbours'; and at a unit that can run in parallel with the rest.
- **Merge** tasks that follow one another on the same files and the same governing reading: they pay one load, and the second finds the first's reading already in its context.
- **Hand related tasks queued under one topic to one agent**, each task still keeping its own plan and report, so that the review of one decision stays separate from the review of the next.
- **Bound a task** above by the context it can hold (the skill's Delegation section names the working marks): past about half the window, the rest goes to a new task linked to this one. Batching is not free, since the re-reads of a growing context outgrow a fresh task's load after a while; it pays only for tasks that share files and reading.
- **Cut the cost per task first by loading less** for the kind of step — a read-only or mechanical step needs less than a step that reasons — before merging tasks to share a load.

The small task keeps its own worth: isolation, a cheap restart after a failure, one reviewable change per decision, and no compaction in the middle of the work. So tasks are small in their decisions, not in their steps. No numeric threshold for merging is set until a real task's cost, load and re-reads both counted, has been measured; this rule is provisional until then.

### Recording follow-ups
A task that turns up further work records it, when it is work, as a queued task opened with `--parent` naming the task's own task, with its plan written whole, as [Queued Work and Its Hand-Back](#queued-work-and-its-hand-back) says; it does not do that work in its own context. It is work when its plan can state a change to be applied or a decision to be recorded as the check; a finding that must first be studied is that work's first step, not a task of its own. A question only the owner can answer is not follow-up work: it is an entry ([Questions Found During a Task](#questions-found-during-a-task)), never a task, save a question about the Memar skill or Memar's scripts, which that section makes a task at once. What is not worth doing is not recorded; what is worth doing but not yet decidable is recorded with the decision it waits for, as an entry.

### A task is for work
A task's check is that something was done: a change applied, or a decision recorded where it governs. A task whose check is a finding, a survey, or a proposal for approval is a step of the task of the work it improves, never a task of its own: it is written into that plan as a step, the finding revises the plan, and the task stays Active, or Blocked while it waits for a ruling. Complete means the check passed, so a task that only proposed is not Complete. An inquiry — looking into Memar or the work to answer the task's own questions — is a step of the task it serves, and what it finds is a research note in that task's `docs/`, not a task of its own. A research that gathers and concludes what many other tasks will build on, as the one that made Lexer's concept clear did, is a task of its own, recorded as a [Research](../research/research.md) document; an investigation that no work waits on and that is no such research is a question entry. A new task is opened only for work that is truly independent (the owner, 2026-10-22). The cost this prevents is real: a finished-looking task for a proposal is archived, swept and forgotten while the work it was for was never done.

---

## Producing a Handoff
1. **Inventory the task against the skeleton.** Walk the section list in [handoff.md → Structure](./handoff.md#structure) and ask, for each: did this task produce anything in this category? This walk is the selection-asymmetry control — omissions happen section by section, visibly, not by habit.
2. **Mark confidence while it is fresh.** Assign each decision its confidence level (Decided / Tentative / Explored-but-unresolved / Deferred) and each assumption its stability (Strong / Weak / Unexamined) before the task's actual certainty fades — category drift (tentative hardening into decided) is the most common distillation error, and it happens in the minutes after the discussion, not later.
3. **Capture reasoning with every decision.** What options existed, what criteria were used, what tipped the balance. A decision without reasoning cannot be safely revised or defended by the receiving task.
4. **Record dissent and rejected alternatives.** Where a conclusion had competing considerations, they travel with the conclusion — this preserves nuance and prevents future re-litigation of settled issues.
5. **Link artifacts and sources.** Reference the documents, models, chat logs, or transcripts the discussion drew on or affected, with the action needed on each (None / Update / Review / Create).
6. **Apply the file format.** Name it `<base>.handoff.md` (or a dated topic-named file for conversations not tied to one document — see [handoff.md → File Format](./handoff.md#file-format) and the placement note below). Write only sections with content; leave no empty headers.
7. **Self-check against the reader who was not there.** Re-read the draft as the next task will: could a task with no memory of this discussion pick up every thread from this file alone? Anything answered "no" goes back to step 3.

### Placement
A handoff is placed by the rule that governs where its base artifact goes: [Documentation → File Naming](../documentation.md#file-naming). One handoff per topic — a multi-topic discussion is split into one handoff per topic so each can resume, conclude, and retire independently — and each is written as `<base>.handoff.md` beside the base artifact it belongs to.

A discussion not yet tied to a governed document is placed the same way, because a handoff's base artifact need not be a document ([Documentation — Handoff → File Format](./handoff.md#file-format)). Name it after the thing the discussion is about, and put it beside the documents the task read. Where that subject has no home yet, the folder the subject belongs in gets opened by the handoff: a task that is about to establish a model writes `<name>.handoff.md` into the new folder before the model exists, which is how `modules/computer/binding/` and `modules/process/construction/` were opened. There is no separate location for untied discussions and none outside the tree — a file a reader cannot open is not a handoff's home.

---

## Consuming a Handoff
At the start of a task that continues from a handoff:

1. **Read it completely before responding.** A partial read defeats the artifact — the sections are interdependent (an assumption may qualify a decision; an open question may block a next step).
2. **Acknowledge the state before advancing.** State the decisions you are building on and their confidence levels, so misreadings surface at the start rather than mid-work.
3. **Do not re-argue Decided points unless asked or unless new evidence exists.** Tentative points may be revisited — that is what the marker means. Re-arguing without new evidence repeats the cost the handoff was produced to avoid.
4. **Update the handoff as the task moves the state.** New decisions are added with their confidence; resolved questions move to Ambiguities Resolved - but only until their resolution graduates into the governed documents: a graduated item is removed from the handoff, since the specification carries the answer and the changelog carries the record (see the graduation rule in [handoff.md → What a Handoff Is](./handoff.md#what-a-handoff-is)); a changed direction rewrites the affected sections. The handoff is a living state-capture, not an append-only history — stale state is worse than absent state, because it is trusted.
5. **Graduate conclusions when they stabilize.** When a decision hardens into settled design, propose it into the governing Explanation-facet document, and wait for approval before modifying project documents; once the decision is durably recorded in the governing document and its changelog, remove it from the handoff's Decisions section - the specification carries the rule and the changelog carries the record, the same graduation that removes resolved questions (step 4). A documentation-improvement proposal:
   - identifies the **exact document and section**, and provides **replacement-ready text in English** (the project's documentation language);
   - states **what ambiguity the change resolves** — documentation serves understanding, not volume: an addition that answers no currently-unanswerable question is not an improvement;
   - names its **type**: ambiguity resolution (existing text can be read multiple ways), gap filling (something is missing or incomplete), decision recording (a concluded decision is not yet captured), terminology alignment (the same term carries different meanings across documents), or structural improvement (organization hinders comprehension);
   - keeps proposed text **self-contained, precise, defined** (key terms defined or referenced), and **cross-referenced** (related documents and terms linked, not left for the reader to find).

---

## Quality Checklist
Before closing a handoff, verify:

- [ ] Every decision carries reasoning and a confidence level
- [ ] No graduated decision remains in Decisions (a decision recorded in the governing document and its changelog has left the handoff)
- [ ] Every resolved ambiguity records *how* it was resolved, not only the verdict
- [ ] Every open question states why it matters and whether it blocks
- [ ] Every assumption states its stability and the consequence of its failure
- [ ] Rejected alternatives and dissenting considerations are recorded where they existed
- [ ] Next steps are ordered with dependencies
- [ ] The confidence vocabulary is used as defined (no invented levels)
- [ ] A task with no prior participation could resume from this file alone

---

## Relation to Other Artifacts
| Artifact | Connection |
|----------|-----------|
| [handoff.md](./handoff.md) | Governing specification — the concept, structure, and rationale this practice follows |
| [explanation.md](../explanation/explanation.md) | Conclusions that stabilize graduate from a handoff into Explanation-facet documents |
| [changelog.md](../changelog/changelog.md) | Graduated changes are recorded in the base artifact's changelog; handoffs and changelogs reference each other but do not absorb each other |

---

*This Practice is part of the Memar project collaboration framework. It should evolve as the project's collaboration patterns become clearer.*
