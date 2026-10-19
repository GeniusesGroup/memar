# Task relation estate

## Model

- Candidate (unconfirmed): `(task)-[:site]->(estate)` (name/direction unconfirmed) carrying the label `Site` — "Where task" — source was a label-only file, no edge code.

## Policies (rules)

- `Site` — the place where the task happens.

## Placement

- **Correct here as recorded — where-a-task-happens is the task's own relation file; keep it task-side until the estate spatial-relations questions decide otherwise** (module skeleton: `task/edges/`; prefer existing homes over inventing new modules).
- Intersects [identity/estate](../../../../identity/estate/estate.handoff.md): that handoff's blocking open question is whether spatial relations are first-class edges or derived observations — this label is evidence *for* a first-class edge but must not pre-empt the estate definition (definition precedes term).
- Not a new module: a place pointer on a task is one label, not processing semantics (parameters-vs-semantics).

## Open questions

- Does Site intersect the estate domain spatial-relations work (see [estate.handoff.md](../../../../identity/estate/estate.handoff.md) — "Spatial relations: first-class edges or derived observations" blocks edge design)?
- Same Site pattern as the department–estate [estate](../../../department/edges/estate/estate.md) ("Office") and staff [attendance](../../../staff/edges/attendance/attendance.md) — one place-link family per domain, or shared estate capability?
- Is the site a fixed location on the edge or an event/time-varying assignment?
- Direction/naming unconfirmed — nothing ratified.

