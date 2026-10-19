# Task relation table

## Model

- Not a domain edge: tables/boards are recorded as a *visual aid*, not as graph structure — no candidate edge (source was `package label` holding one comment).

## Policies (rules)

- "Table or boards is visual aid to help users access tasks in GUI e.g.Table(TODO, DOING, DONE)" — a board is a view over task labels (the TODO/DOING/DONE columns reuse the Scrum labels in [task-labels](../task-labels/task-labels.md)).

## Placement

- **Verdict: not an edge — GUI projection only; belongs to pluggable GUI, never task kernel.** The source itself says "visual aid ... in GUI"; projection ≠ domain model, and the handoff already fixed the same point ("A GitHub-Issues-style GUI for tasks is optional and must not influence the model" — [task.handoff.md](../../task.handoff.md)).
- Recorded here only because the comment sat in the module's `edges-loop/` — the folder documents the source, it does not promote boards to a stored grouping.
- If a board ever becomes persisted state (a saved grouping users create), that would be a stored node/edge and a new review — nothing in the source says so.

## Open questions

- Is a board a GUI projection (per projection ≠ domain model) or a persisted grouping?
- Column vocabulary is shared with Scrum labels ([task-labels](../task-labels/task-labels.md)) — one vocabulary consumed by the view, or does the board define its own states?
- Eisenhower "table view" in [task-labels](../task-labels/task-labels.md) — same projection family?

