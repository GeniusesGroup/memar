---
Title: "Task Rule — A Blocking Task Is Recorded in Depends_on"
Status: Draft
Start Date: 2026-11-01
---

# Task Rule — A Blocking Task Is Recorded in Depends_on
A rule of this repository for a conversation that cannot go on without another task. Moved on 2026-11-01 from the Handoff Practice.

## The rule
- **A task the conversation cannot go on without is blocking:** a step still to come reads its result, or its result could change the plan. Every other queued task is independent of it.
- **The conversation records what it waits for in its own plan's `Depends_on`,** is Blocked, and tells the owner at once. A queued task whose `Depends_on` is not yet met is itself Blocked, and is not claimed or started until each cited task is Complete ([relations between tasks](../task-relations/task-relations.md)).
- **The conversation resumes when the owner says the task is done,** reading the hand-back alone, and consumes the decisions made without re-entering their reasons, unless its own work meets a problem with one.
- **A problem found later in a finished task's work returns to that task's chat** as a prompt stating the problem and the new ask. A new task is opened only where the work is new.

## Why it exists
A conversation that proceeds on a result it has not read builds on a guess, and one that re-opens every reason of a finished task spends the context the task was run apart to save.

## Keep it or drop it
An organization may let a conversation wait without a record, and then cannot tell from the plan what it is waiting for.

## What this rule does not claim
- It does not say where each task runs: [where a task runs follows two questions](../where-a-task-runs-follows-two-questions/where-a-task-runs-follows-two-questions.md).
- It does not give the verbs; `memar task depends-on --help` and `memar git show-task-records --help` say them.
- This repository runs no check of it today.
