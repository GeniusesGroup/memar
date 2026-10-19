# Staff relation staff

## Model

- Candidate (unconfirmed): `(staff)-[:relation_staff]->(staff)` (name/direction unconfirmed) carrying labels `Evaluation`, `Referral`, `PresentedID`, `HireBy` — source was a label-only file, no edge code.

## Policies (rules)

- `Evaluation` — "it can be done by staff itself, manager, other staff, ..."
- `Referral` — staff referral of other staff.
- `PresentedID` — "staff-take-leave-alternate or staff replace".
- `HireBy` — hired by a staff member (counterpart of `HireFor` on the staff-to-group relation).

## Placement

- **Correct here — staff-to-staff employment relations are the staff capability's own** (module skeleton: `staff/edges/`; only staff gives these labels meaning; prefer existing homes over inventing new modules).
- Not [group](../../../group/group.md): both endpoints are staff; no group participation is implied. Not a new module — referral/evaluation are parameters of the existing staff relation (parameters-vs-semantics).
- Bare edge as recorded (no bare edges): no who-may-refer/evaluate and no what-it-triggers — rule material (core never knows Rule); verdict stays candidate until those exist.

## Open questions

- Does `Evaluation` reuse the endorsement pattern from [knowledge/skill](../../../../knowledge/skill/skill.md) / knowledge_unit's `endorse` edge?
- `HireBy` (this file) vs `HireFor` ([group](../group/group.md)) — two edges, or one hire edge with direction?
- `Referral` also appears in the [hiring pipeline](../hiring-pipeline/hiring-pipeline.md) labels — same concept, pipeline-stage annotation, or two things?
- `PresentedID` shared with the staff-to-group relation — one label set across both, or split?
- Direction/naming unconfirmed — nothing ratified.

