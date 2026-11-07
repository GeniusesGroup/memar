# Task relation task

## Model

- `(task)-[:part_of]->(task)` — containment; reverse `(task)-[:has_part]->(task)`.
- `(task)-[:blocks]->(task)` — dependence; reverse `(task)-[:blocked_by]->(task)`.
- Each edge is written with its reverse, together, so that the parts of a Task and the Tasks it blocks or is blocked by are each read from one vertex ([Graph → Services](../../../../../modules-plugable/computer/memory/store/graph/graph.md#services)). The reverse names are the owner's (2026-11-05, task `20261101-T073218Z-4460`, content 90). Why there are two edges is stated in [Task → Edges](../../task.md#edges).
- The steps of a plan are a Task's parts, each a Task with its own check. `blocks`: the first must reach its end before the second may start.

## Policies (rules)

- `part_of`: many parents allowed; a cycle is refused by a rule; the owner of both ends creates it; removal is an event.
- `blocks`: a Task `blocked_by` an unended Task is Blocked; a cycle is refused by a rule; removal is an event.
- Each rule attaches through the generic `condition_is`; this edge never references the rule domain.

## Placement

- **Correct here — a Task's relations to other Tasks are the task module's own**, and only these two are declared.
- `part_of` is a task hierarchy — same *pattern* as group's [parent](../../../group/edges/parent/parent.md) but a different domain; keeping it task-side avoids borrowing group semantics.
- The earlier candidate labels on one generic `relation` edge resolve so: `Parent` is `part_of`, `Blocking` is `blocks`. `Move` (a Task moved from another project) is a provenance annotation and no edge.
