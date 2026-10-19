# Task Rule — A Task announces what it will change
Status: Draft

## The rule
Before it changes a content, a Task is related to that content by an edge so that every Task and participant can see which Tasks intend to change or have changed it. At its end the edge is removed or becomes another edge. The edge orders no writes. When several Tasks change one thing, their coordination may be done by a service like a database transaction, or conceptually by relating the Tasks and doing them together; neither is forced.

## Why it exists
It is a version-control commit made visible before the change, not after it.

## How a check would run
A Task that changes a content with no such edge on it breaks the rule. The statement is the owner's, recorded in [the Task handoff](../../../../../modules/management/task/task.handoff.md#owners-answers-to-the-six-questions-2026-10-18); this repository runs no automatic check of it today.
