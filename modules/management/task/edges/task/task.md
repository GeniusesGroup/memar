# Task relation task

## Model

- Candidate (unconfirmed): `(task)-[:relation]->(task)` (name/direction unconfirmed) carrying labels `Blocking`, `Move`, `Parent`.

## Policies (rules)

- `Blocking` — stuck.
- `Move` — move from other project.
- `Parent`.

## Placement

- **Correct here — task's internal relations are the task module's own** (module skeleton: `task/edges/`; the task capability gives them meaning, no other module does; prefer existing homes over inventing new modules).
- `Parent` is a task hierarchy — same *pattern* as group's [parent](../../../group/edges/parent/parent.md) but a different domain (tasks, not groups); keeping it task-side avoids borrowing group semantics.
- `Blocking` implies processing (what a stuck task may/may not do) — if it *enforces* anything, that enforcement is rule material (core never knows Rule); as recorded it is a bare label with no trigger (no bare edges) → verdict stays candidate. `Move` is a provenance annotation (parameters-vs-semantics: no module for it).

## Open questions

- Blocking enforcement: does a blocking edge freeze status/assignment — rule or task processing? What triggers it?
- `Parent` vs group hierarchy: one general hierarchy pattern with per-domain edges, or a shared parent concept? Flagged here only — do not duplicate group's parent edge.
- `Move`: does it carry history/subtasks across projects, or only relabel origin?
- Direction/naming unconfirmed — nothing ratified.

