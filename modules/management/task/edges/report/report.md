# Task relation content

## Model

- Candidate (unconfirmed): `(task)-[:reports]->(content)` (name/direction unconfirmed) carrying the label `Report to the public` — source was a label-only file, no edge code.

## Policies (rules)

- `Report to the public` — the task's result/content is published to the public.

## Placement

- **Correct here — recorded on the task's own relation file; the task module keeps it while it only says how a task relates to its content** (module skeleton: `task/edges/`; prefer existing homes over inventing new modules).
- Task is already decided to also be a Content ([task.handoff.md](../../task.handoff.md) — "Task itself is also a Content"); this relation may be the publication *aspect* of that content rather than a new edge — confirm before modeling (see Open questions).
- Public-vs-restricted publication is access policy → rules (core never knows Rule); the label alone records no audience set (no bare edges: who may publish, what it triggers, unrecorded).

## Open questions

- One edge to a content node vs a publication flag/label on the task's own content identity?
- Does "public" mean a rights/access rule (who may read) rather than an edge property?
- Converge with [knowledge/content](../../../../knowledge/content/content.md) discussion/publication threads instead of a task-specific edge?
- Direction/naming unconfirmed — nothing ratified.

