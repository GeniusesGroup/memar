# Group relation estate (department–estate "Office")

## Model

- Candidate (unconfirmed): `(group)-[:relation]->(estate)` (name/direction unconfirmed) carrying labels `Office`, `Meeting` — source was a label-only file, no edge code; a Department is a Group ([group.md](../../../group/group.md)), so the department reading rides the group edge file.

## Policies (rules)

- "Let staffs register enter and exit time by their mobiles in specific location." — mobile enter/exit registration at the estate.
- Source TODO: "Isn't it a rule??" — the comment itself doubts the edge reading.
- Labels: `Office`, `Meeting`.

## Placement

- **Verdict: candidate here while it stays a department–place edge, but the recording behavior the comment describes is rule/event material — convergence with [attendance](../../../staff/edges/attendance/attendance.md) undecided.** Department is the capability that gives "this group has an office" meaning (module skeleton: `department/edges/`; prefer existing homes); the enter/exit *registration* (who may register, what a registration triggers) is policy → rules (core never knows Rule) — the source's own TODO already asks this.
- The staff-side [attendance](../../../staff/edges/attendance/attendance.md) doc already owns staff-estate recording (`edges/`, `edges-loop/`, `_import/` complete capability) and flags this parallel: if location-attendance is one capability, its review belongs with attendance — do not stand up two recording paths (module keeps its complete capability).
- Connects to the estate spatial-relations questions ([estate.handoff.md](../../../../identity/estate/estate.handoff.md) — first-class edges vs derived observations blocks edge design); not an estate-side move today.

## Open questions

- Is the department–estate relation an edge, or a rule evaluation over staff-location events (the source's own "Isn't it a rule?")?
- Converge with staff [attendance](../../../staff/edges/attendance/attendance.md) — one location-attendance pattern (staff-side) with departments only naming the place, or a separate department capability?
- `Office` vs `Meeting` — place *kind* labels on one edge, or two relations (permanent office vs meeting venue)?
- Connects to the estate spatial-relations questions ([estate.handoff.md](../../../../identity/estate/estate.handoff.md)) — do not pre-empt the estate definition.

