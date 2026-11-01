---
Title: "Task Rule — Tasks Are Split at Decisions and Merged on Shared Reading"
Start Date: 2026-11-01
---
# Task Rule — Tasks Are Split at Decisions and Merged on Shared Reading
A rule of this repository for how large a delegated or queued task should be. Moved on 2026-11-01 from the Handoff Practice; provisional until a real task's cost has been measured. How a step is delegated is [delegate by size of reading](../delegate-by-size-of-reading/delegate-by-size-of-reading.md), and a step is judged by [its cost over the whole work](../step-cost-over-the-whole-work/step-cost-over-the-whole-work.md).

## The rule
- **A task carries a load before it does any work** (the skill, the Cognition sections, the plan, the governing documents its steps name), and every new task pays it again. Its size is set by weighing that load against the work it holds and what its tasks share, the files they change and the reading that governs them, and not by a count of files or a fixed number of tokens.
- **Split** at a decision the owner must take; at a change that can be tested alone and whose files and governing reading differ from its neighbours'; and at a unit that can run in parallel with the rest.
- **Merge** tasks that follow one another on the same files and the same governing reading: they pay one load.
- **Related tasks queued under one topic go to one agent,** each keeping its own plan and report ([queued work is handed out by one topic](../one-topic-one-project-per-delegated-batch/one-topic-one-project-per-delegated-batch.md)).
- **Past about half the window, the rest goes to a new task linked to this one.** Batching is not free, since the re-reads of a growing context outgrow a fresh task's load after a while; it pays only for tasks that share files and reading.
- **Load less for the kind of step before merging to share a load:** a read-only or mechanical step needs less than a step that reasons.
- **Tasks are small in their decisions, not in their steps.** A small task keeps isolation, a cheap restart after a failure, one reviewable change per decision, and no compaction in the middle of the work.

## Why it exists
A module of a hundred small files is one task and one context, while a single very large output may not be; a count cannot tell them apart. No measurement yet supports a threshold.

## Keep it or drop it
An organization may fix a size by number of files, and then splits what should be together and merges what should be apart.

## What this rule does not claim
- It sets no numeric threshold for merging; none is set until the cost of a real task, load and re-reads both counted, has been measured.
- This repository runs no check of it today.
