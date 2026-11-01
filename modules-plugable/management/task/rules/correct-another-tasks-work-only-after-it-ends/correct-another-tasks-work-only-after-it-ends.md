---
Title: "Task Rule — Another Task's Work Is Corrected Only After It Ends, and the Correction Is Reported"
Start Date: 2026-11-01
---
# Task Rule — Another Task's Work Is Corrected Only After It Ends, and the Correction Is Reported
A rule of this repository for a task that finds another task's work in the shared medium wrong: a claim its source does not support, a deleted record, a question closed without an answer. The statement is the owner's, 2026-10-13.

## The rule
- **Work does not belong to the task that wrote it,** so any task may correct it.
- **The other task must have finished.** A task still running may be about to change the same passage, and a correction made under it is overwritten or overwrites. Establish that it ended before correcting: its Status is Complete or Blocked and not Active or Queued, or the person who started it says it is done. A task whose state the agent cannot see is asked about, not assumed finished. Then confirm the problem still stands in the current text, since the task may have fixed it before ending.
- **A small defect that is certain** (a corrupted sentence, a stale line, a broken test) is fixed in the same turn without asking the owner, even in a committed file or another task's work. A fix that is large, or whose intent is unclear, is queued as a task ([queue a further task](../queue-a-further-task-never-do-it-here/queue-a-further-task-never-do-it-here.md)).
- **The correction is reported.** It is recorded as a changelog content of the correcting task, and listed in that task's report and in what it tells the person, so that the person and the original author learn what was changed in their work and why.

## Why it exists
A correction under a running task is lost or destroys that task's edit; a silent correction leaves the author with a document that no longer says what they wrote and no way to learn why.

## Keep it or drop it
An organization may leave a task alone with its own work, and then keeps a wrong passage until its author returns.

## What this rule does not claim
- It does not say how a changelog content is written; `memar conversation post --help` says that.
- It does not allow an edit of a task's own contents: [a text of a task is added, never replaced](../a-text-of-a-task-is-added-never-replaced/a-text-of-a-task-is-added-never-replaced.md).
- This repository runs no check of it today.
