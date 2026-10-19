# Task Rule — Relations between Tasks
Status: Draft

## The rule
Task-to-Task relations are those with a trigger. `part_of`, `blocks` and `supersedes` are decided; `same_ask` (two Tasks ask the same thing, and a duplicate is one) is accepted. More are wanted and their names are open: a Task that does more than the Task it closes needs a relation to it, and a Task closed because a new decision conflicts with an earlier one needs a relation to that decision. A mention, a follow-up and a related-to are not Task relations.

## Why it exists
A relation with no trigger is vocabulary.

## How a check would run
Each relation names who creates and removes it and what it triggers. The statement is the owner's, recorded in [the Task handoff](../../../../../modules/management/task/task.handoff.md#owners-answers-to-the-six-questions-2026-10-18); this repository runs no automatic check of it today.
