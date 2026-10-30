# Task Rule — A step is delegated by what it reads, not by what it is called
Status: Draft

## The rule
Delegate a step, with its acceptance check, when what it reads would take a large share of the context and the task needs only its conclusion — measured in bytes, not in files — or when it reruns a script until it comes out clean; keep only the report. Measure before reading; about 20 KB of output or of a single file, and about a quarter of the window for a step's whole reading, are the working marks, not laws. A step that stays under both marks stays local, whatever its kind and whatever its plan wrote: the plan's "delegated" mark is a forecast, and the step takes the test again when it starts. How large a task is, and when tasks are split or merged, is set by [Sizing a Task and Recording Follow-Ups](../../../../knowledge/documentation/handoff/handoff.practice.md#sizing-a-task-and-recording-follow-ups). What `memar ai get-task-init-context` and `memar content get-act-context` print does not count, whatever its size: it is read whole, in the context that acts. A step that crosses the line midway is delegated from there.

## Why it exists
Starting an agent costs its whole context again and returns only a report; for a small step that is more than doing it.

## How a check would run
Compare a delegated step's reading with the two marks; a step under both that was delegated is a defect. Moved on 2026-10-26 from the Memar skill (task 20261026-T120341Z-16244); this repository runs no automatic check of it today.
