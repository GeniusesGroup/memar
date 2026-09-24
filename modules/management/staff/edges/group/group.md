# Staff relation group

## Model

- Candidate (unconfirmed): `(staff)-[:relation_group]->(group)` (name/direction unconfirmed) carrying labels `Evaluation`, `PresentedID`, `HireFor` — source was a label-only file, no edge code.

## Policies (rules)

- `Evaluation` — "it can be done by staff itself, manager, other staff, ..."
- `PresentedID` — "staff-take-leave-alternate or staff replace".
- `HireFor` — hire staff for a group (counterpart of `HireBy` on the staff-to-staff relation).

## Placement

- **Correct here — staff-to-group employment relations are the staff capability's own** (module skeleton: `staff/edges/`; hiring/evaluation give these labels meaning; prefer existing homes over inventing new modules).
- Not [group](../../../group/group.md) module: the entry point is the staff side (who evaluates/presents/hires this staff for which group); group keeps membership edges ([joined](../../../group/edges/joined/joined.md), [parent](../../../group/edges/parent/parent.md)).
- Bare edge as recorded (no bare edges): no who-may-evaluate and no what-it-triggers recorded — those are rule material (core never knows Rule); until defined, verdict stays candidate.

## Open questions

- Does `Evaluation` reuse the endorsement pattern from [knowledge/skill](../../../../knowledge/skill/skill.md) / knowledge_unit's `endorse` edge — one evaluation capability or staff-specific?
- `HireFor` (this file) vs `HireBy` ([staff](../staff/staff.md)) — two edges, or one hire edge with direction encoded?
- `PresentedID` also appears on the staff-to-staff relation — shared label on both, or one canonical edge?
- Direction/naming unconfirmed — nothing ratified.

