# Parent

## Model

- `(group)-[:parent_of]->(group)`
- `(group)-[:parent_is]->(group)`

## Policies (rules)

- Use to categorize and graph groups
- GUI projection: "Show in SameLevel, UpperLevel, LowerLevel" and "Provide drag and drop to change the groups relation" (from source ../../../../knowledge/question/widgets/question/gui.kh).

## Placement

- **Correct here — the group hierarchy edge stays with `management/group`.** Parent/child structure is what the group module manages (module skeleton: `edges/parent` beside the group capability); the group capability is the only one that gives this edge meaning — no move, no new module (prefer existing homes over inventing new modules).
- Drag-and-drop reparenting is a *view* behavior: GUI projects SameLevel / UpperLevel / LowerLevel (GUI is pluggable) — the kernel stores the current parent only, no GUI semantics in core.
- Who may reparent, and cycle guards, are policy → rules (core never knows Rule), not parent-edge code.
