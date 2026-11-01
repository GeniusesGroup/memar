---
Title: "Task Rule — A Question Belongs to a Task, and a Related Question Keeps It Open"
Start Date: 2026-11-01
---
# Task Rule — A Question Belongs to a Task, and a Related Question Keeps It Open
A rule of this repository for a question a task turns up that only the owner can answer. The statement is the owner's, 2026-10-31, with the 2026-10-15 ruling on the skill and the scripts. It replaces the older lines that "a question is its own task" and that a question is "an entry, never a task".

## The rule
- **A question belongs to a task, and a task holds as many as it turns up.** One that only the owner can answer is a `question` content of the task it concerns, never an entry in a file beside a document ([no record is written beside a document](../../../../knowledge/documentation/rules/no-record-beside-a-document/no-record-beside-a-document.md)). It stands alone: a session with no memory of the task can read it and know what is asked and what each answer would change ([the kinds](../../../../knowledge/documentation/handoff/handoff.md#the-kinds)); one that fails is rewritten before the task ends.
- **A related question keeps its task open.** While it stands the task is not Complete: it is Blocked, or Active when it can go on, and its report names the question under `Decisions needed`. The answer is a later content that refers to the question.
- **Only a large question unrelated to its task becomes a task of its own,** queued with the finding task as its parent and its plan written whole ([queue a further task](../queue-a-further-task-never-do-it-here/queue-a-further-task-never-do-it-here.md)).
- **A question about what the Memar skill or one of Memar's scripts should say or do is such a task at once.** Its check is that the change is applied; its first step is the study that settles what the owning material settles; it asks under `Decisions needed` only the rulings the owner alone can give, and while one is unanswered it is Blocked, never Complete. Both shape how every task works, so a question about them is worked fast and not parked.
- **The task that found a question writes it before it ends.** A sub-agent that may not write returns the text in its report, and the delegating agent writes it before the task counts as done.
- **A question reaches the owner only after an agent has tried it** ([the rule](../questions-go-to-an-agent-before-the-owner/questions-go-to-an-agent-before-the-owner.md)). An answer that agent is sure of, outside the kinds the Norm Application Points always send to the owner, is recorded as a Tentative decision with its reasons.
- **An answered question is graduated:** the answer goes where it governs, a decision or the governing document with a changelog content, and the changelog names the question so that it stays findable.

## Why it exists
A question left in scrollback sinks, and one left in a swept task's folder is read by no one. A question held as a content of its task is found with the task. Releasing the task of a question it depends on makes it look done while work is owed, and a task per question fills the queue with tasks that carry only a wait.

## Keep it or drop it
An organization may keep its open questions in a list of its own, and then keeps two places to look.

## What this rule does not claim
- It does not give the fields of a `question` content or the verbs that post it; the types of the handoff module and `memar conversation post --help` say them.
- It does not list the kinds that always reach the owner; [Cognition Practice → Norm Application Points](../../../../../docs/cognition.practice.md#norm-application-points) does.
- An entry already standing in a handoff file waits for its migration into a content of its task.
- This repository runs no check of it today.
