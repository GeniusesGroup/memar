# Attendance

## Model

- Candidate (unconfirmed): `(staff)-[:attendance]->(estate)` — the staff–estate relation labeled "Attendance" (source was a staff-to-estate label file).
- The attendance record already has structure in the staff module: `StaffAttendance` (StaffID, Type, AttendanceTime, Time, RequestID) — see [../../edges-loop/staff-attendance.kh](../../_import/staff-attendance.kh).

## Policies (rules)

- Label: `Attendance`.
- Attendance types already coded in the staff module ([staff-attendance.kh](../../edges-loop/staff-attendance.kh)): Enter, Exit, ManualEnter, ManualExit, Start, End.

## Placement

- **Correct here — the staff module already owns the complete attendance capability.** Edge + processing + record live together in `management/staff` (`edges/`, `edges-loop/`, `_import/`) — a module owns its complete capability, and the existing home is preferred over any new module; moving only the edge to estate would split edge from processing.
- Entry point: attendance is recorded *by staff at work*; the estate only supplies the location — placement by entry point keeps the edge staff-side, not [identity/estate](../../../../identity/estate/)-side.
- Parallel candidate: the department–estate "Office" label in [estate](../../../department/edges/estate/estate.md) ("Isn't it a rule?") — if location-attendance is one capability its review belongs there too; who may record ManualEnter/ManualExit is policy → rules (core never knows Rule).

## Open questions

- Converge with the department–estate "Office" candidate ([estate](../../../department/edges/estate/estate.md)) — one location-attendance pattern per module, or a shared estate capability?
- Is the edge a place link with the record as events (Enter/Exit/Start/End types), or does the edge itself carry times?
- Manual vs automatic capture — device/GPS event, or rule (geofence)?
- RequestID ties attendance to user-request — does the edge sit beside request processing?

