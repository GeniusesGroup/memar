# Task Rule — What a worker always holds, and what it loads
Status: Draft

## The rule
The only thing always held in a worker's context is the first content of the Task's timeline, or a chosen list from it, which is something like a plan and says the path of the work. The worker loads anything else by searching all content it can reach, not only the Tasks related to this one by an edge. No field or structure forces decisions or checks to be written for children. The way of caching is not tied to today's AI models.

## Why it exists
Each Task is independent; the context bound belongs to the reader, and the search finds what the Task needs.

## How a check would run
A required inheritance field, or a view that depends on the edges walked to reach a Task, breaks the rule. The statement is the owner's, recorded in [the Task handoff](../../../../../modules/management/task/task.handoff.md#owners-rulings-the-second-round-2026-10-18); this repository runs no automatic check of it today.
