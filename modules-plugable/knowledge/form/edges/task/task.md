# Form relation task
## Model
- Candidate (unconfirmed): `(form)-[:relation_task]->(task)` carrying labels `Creator` / `Pending` (direction unconfirmed).

## Policies (rules)
- `Creator` / `Pending` recorded without semantics — who the creator is, and what a pending task waits for, absent from the source (no bare edges).

## Placement
- **Correct here — the form's task link stays with the form capability** (placement by entry point: instantiated when a form spawns or references its work task; pluggable owns complete capability — edge + whatever session/work processing it feeds live together).
- **Not [management/task](../../../../../modules/management/task/task.md):** task stays the generic domain; a shortcut edge is owned and maintained by the capability that gives it meaning — a form-task link means nothing outside form answering (stated precedent in [respondent-task](../respondent-task/respondent-task.md)).
- **Not a new module and not bare-shipped:** two unannotated labels are not a module candidate (prefer existing homes over inventing new modules); if `Creator`/`Pending` drive workflow states, that is rule/task material to record first (no bare edges; core never knows Rule).
