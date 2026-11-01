# Task Rule — Relations between Tasks
Status: Draft

## The rule
- **Task-to-Task relations are those with a trigger.** Each is a kind (a label) plus a target task. A task may hold many relations, including several of the same kind when the kind allows it. They are read as `Task_Relations` / `Task_Relation` on the task lens (`protocol/task-relations.kh`), not as a single parent field or a `ProjectUUID`.
- **Decided kinds:** `part_of` (includes what was once stored as a single parent), `blocks`, `supersedes`, `same_ask` (two tasks ask the same thing; a duplicate is one), and `project` (this task belongs to the task that carries the label `project` — see [Project](../../../project/project.md)). More are wanted and their names are open: a task that does more than the task it closes needs a relation to it, and a task closed because a new decision conflicts with an earlier one needs a relation to that decision.
- **A mention, a follow-up and a related-to are not Task relations.**
- **“Which project?” is a query** over relations of kind `project`, not a second stored edge.

## Why it exists
A relation with no trigger is vocabulary.

## How a check would run
Each relation names who creates and removes it and what it triggers. The statement is the owner's, recorded in the Task handoff; this repository runs no automatic check of it today.
