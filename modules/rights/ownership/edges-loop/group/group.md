# Task relation group

## Model

- Candidate (unconfirmed): `(task)-[:relation_group]->(group)` carrying the labels below (source was `package label` holding comments only, no edge code).
- "Group here can treated as a team work on a task."

## Policies (rules)

- `Assigned` — the group as the team working the task.
- `Reviewer`, `Authorization`.
- Chat-surface labels: `Chats_Participant`, `Chats_Reviewer`, `Chats_Approver`.
- Production dependency: "Some product as material need or pend on other production,.e.g. car needs engine, ..."
- No who-may-assign/what-it-triggers recorded — labels must not be ratified as edges (no bare edges).

## Placement

- **Not an edge of ownership; strip.** Team assignment and production dependency grant no ownership: rights come first and ownership arises from rights ([rights.md](../../../rights.md)) — assignment labels must not become ownership primitives. Removing it distorts nothing in ownership (core-by-necessity fails).
- `Assigned` (group as team) already has a folder-mate home in [assigner](../assigner/assigner.md) — one `Assigned` label, not two (prefer existing homes).
- Production dependency (car needs engine) is task/production structure — belongs with [task](../../../../management/task/task.md) (or its production sibling); if it needs processing, edge and processing live together there (a module keeps its complete capability).
- Not a new module: the label set alone carries no processing semantics (parameters vs semantics).

## Open questions

- Why does a task-relation live under ownership at all (assignment is not ownership)? Reconcile with the rights-first ordering — the standing question the ownership backlog used to hold ([ownership.md](../../ownership.md)).
- Is `Assigned` on group the same label as [assigner](../assigner/assigner.md)'s, and do the `Chats_*` labels belong to a chat/content capability instead of task?
- Production dependency: a separate `depends_on` edge under task/production, or a rule the task domain already reads?
- Loop-edge shape and direction unconfirmed — nothing ratified.

