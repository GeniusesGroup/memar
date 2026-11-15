---
Title: "Task Rule — Later Work on a Task's Result Returns to That Task"
Start Date: 2026-11-06
---
# Task Rule — Later Work on a Task's Result Returns to That Task
A rule of this repository for work that continues, corrects or applies a ruling to the result of a task that is finished, blocked or whose agent's context is full. The statement is the owner's, 2026-11-06.

## The rule
- **A task is one thing asked with one check.** What the task's result still needs, a correction of it, a ruling applied to it, the rest of it that an agent's limit left undone, is that same thing and that same check, and so it is work of that task and not of a new one. A limit of an agent (a full context, a plan a sub-agent can read, the end of a session) is not a new thing asked.
- **The work goes back to the task.** It is a new plan content on the same task, and a ruling the owner gave since is a content of kind `decision` on it; the task is taken up again by `memar task_ensure --task-id ID`, its Status set Active, and set again at its end ([a task ends with its report and Status](../task-ends-with-report-and-status/task-ends-with-report-and-status.md)). A text of the task is added and never replaced ([a text of a task is added, never replaced](../a-text-of-a-task-is-added-never-replaced/a-text-of-a-task-is-added-never-replaced.md)).
- **A sub-agent or a new chat that continues the work is handed that task,** with its brief (`memar agency_get_task_plan_carry_out_brief ID`), the new plan content and the decision contents. No task is opened to give it a plan it can read: the plan is a content of the task it continues.
- **A new task is opened only for work new in itself:** a thing asked whose check is not the check of any task before it ([a task is for work](../a-task-is-for-work/a-task-is-for-work.md)). Work that merely follows a task, in the same files or under the same check, is not new.
- **A task that cannot be told apart by a test is judged by the check.** If the work's done-or-not-done is the check of an earlier task, it returns to that task; if it needs its own check, its own accepting person, or can be done with the earlier task never having existed, it is a task of its own.

## Why it exists
A work opened as several tasks is scattered over their timelines, each paying a load again and each spending the owner's attention to follow; the cause was an agent's limit, not the thing asked.

## Keep it or drop it
An organization may open a task per hand-over, and then keeps one work in many records, none of which says whether the work is done.

## What this rule does not claim
- It does not forbid a child task for a thing new in itself, nor a sub-agent: [where a task runs follows two questions](/modules-plugable/management/agency/rules/where-a-task-runs-follows-two-questions/where-a-task-runs-follows-two-questions.md).
- It does not let a task be re-opened to change a text that records what was done: the report of a finished work is added to, never replaced.
- It is not decidable by code as a refusal: `task ensure` that sees `--parent` of a Complete task, or a title naming that task's result, cannot tell a continuation from a new thing, since that is the judgment of the check above, and a refusal would block the legitimate child. This repository runs no check of it today; the `task ensure` help and the printed lists carry the rule.
