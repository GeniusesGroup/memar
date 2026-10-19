# Staff Handoff

## Topic & Purpose
Staffing-process decisions that attach to Staff rather than Role definitions — notably the org's multi-AI production process as Hybrid Agency.

## Status
Active — observation recorded; org implementation open.

## Decisions

### From Organization ideas backlog — Agency (`Agency - chatgpt.md`)

- **The org's own multi-AI production process is an instance of Hybrid Agency** — a human principal
  setting direction, one AI drafting, another AI reviewing against a specification. Treat the pattern
  as a first-class modeled workflow (with explicit delegation boundaries and acceptance criteria), not
  as ad-hoc chat usage; the agency document's reflexive open question ("does this document's own
  production instance the model?") is answered by exactly such an org implementation. *(observation;
  org implementation open)*

## Open Questions
- Org implementation of Hybrid Agency as a first-class modeled workflow. *(observation; org implementation open)*

## Khayyam conversion (2026-10-03)

### Status
Protocol layer converted. [`protocol/dt-uuid.kh`](protocol/dt-uuid.kh) is the only source in `protocol/` and the only file converted; it **accepts** against the Khayyam frontend (verified against a root where both `org/…` and `memar/…` resolve).

**The domain is not modelled.** What converted is identity. The attendance record, the shift preference, and the timing record all exist in this domain as Go source under `_import/` and none of them converted. See Decisions and Open Questions.

### Decisions

- **A staff member's identity is the user domain's identity.** *(Decided.)* The Go source wrote `type UUID user_p.UUID` with the comment "It is same as user_p.UUID" — it stated the identity explicitly. `user_p.UUID` is itself `thing_p.UUID`, so the file includes `UserUUID` from `modules/identity/user/protocol/dt-uuid.kh` and declares no `StaffUUID`. Result parameter `u`, matching the two `org_p.Field_OrganizationUUID` accessors that also return `UserUUID`.
- **`edges-loop/staff-attendance.kh` and `edges-loop/staff-status.kh` were left unconverted.** *(Decided.)* Both are `package label` holding only `iota` constants — vocabulary, which is data. `StaffAttendance_Type` (the *type* behind those six attendance constants) is declared in `_import/staff-attendance.kh`, not in the `edges-loop/` file; a converted `Field_…_Attendance_Type` has to be written when that record is converted, not here.
- **`_import/staff-timing-utc.kh`, `_import/staff-attendance.kh`, `_import/staff-shift-preference.kh` were left unconverted.** *(Decided, with a blocker recorded.)* All three carry real interface declarations, so this is not the vocabulary exemption. They are held for three reasons: (1) `_import/` is the legacy `package org` shim tree over the deleted `libgo/protocol`, `libgo/time/earth` and `libgo/time/utc`, and no `_import` file has been converted in any wave; (2) each of them re-states `StaffUUID`, which `protocol/dt-uuid.kh` owns, so converting them faithfully would mint rival identities; (3) all three import `urp.UserRequestUUID` from `modules/user-request/protocol` — **a module that no longer exists in this repository** (`modules/user-request` is absent). The surviving request concept is memar's `Observer_RequestID`, which is what the already-converted record files in this repository use, so the conversion is straightforward *once someone rules that `_import/` is in scope at all*.
- **`_import/person-position/approve-org-position-by-person.kh` was left unconverted.** *(Decided.)* It is a `var` service descriptor plus two `func` bodies with empty parameter lists, over the deleted `libgo/achaemenid`. There is nothing in it that is a protocol; it is implementation, and rule 1 sends implementation to the implementation layer.

### What the code says about shift timing (not settled here)

The brief for this wave asked whether shift timing is a staff attribute or a time-domain concept, and to report what the code says rather than decide. What the code says:

- **The timing record lives on the staff side, and nowhere else.** [`_import/staff-timing-utc.kh`](_import/staff-timing-utc.kh) declares `StaffTimingUTC` with `StaffID()`, `ShiftID()`, `Day() utc.DayElapsed`, `DayHours() earth.DayHours`, `Time() protocol.Time`, `RequestID()`. Its own comment on `DayHours` reads "what hours in a day **this staff** must active to provide services or do projects" — a per-staff statement, in the staff module, keyed by staff and shift and day.
- **A second, separate staff-side record carries the same two keys.** [`_import/staff-shift-preference.kh`](_import/staff-shift-preference.kh) declares `StaffShift` with `StaffID()`, `Day() utc.DayElapsed`, `ShiftID() ShiftUUID`, `Time()`, `RequestID()` — the same staff/day/shift triple without the hours. Two records, one relation, no shared type. Whether they are one record with an optional hours field or two is not stated anywhere.
- **The shift module has no timing at all.** [`../shift/protocol/dt-uuid.kh`](../shift/protocol/dt-uuid.kh) declares only `Field_ShiftID`; [`../shift/shift.md`](../shift/shift.md) says one line, "`Shift` is repetitive task", and models it as `(task)-[:shift]->(---)` with an undecided far end — a *relation from a task*, not a timed node. `Day()`, `DayHours()` and `AttendanceTime()` appear nowhere in the shift module.
- **`ShiftID()` is consumed only by staff.** Nothing in the repository composes `Field_ShiftID`. The shift module declares an identity nobody reaches.
- **Staff deliberately pushed shift states out of its own status set.** [`edges-loop/staff-status.kh`](edges-loop/staff-status.kh) comments out `Status_Active` and `Status_Inactive` with the inline note `Shift`. [`edges/staff-status/staff-status.md`](edges/staff-status/staff-status.md) records that and asks "Do shift states belong here or to [`shift`](../shift/shift.md)?" — unanswered.
- **The types the timing needs are gone.** `utc.DayElapsed` and `earth.DayHours` are `libgo` types with no successor in the tree. [`../calendar/calendar.handoff.md`](../calendar/calendar.handoff.md) records that memar's `Time` is an instant from an epoch with no civil date and no calendar system, and that memar has `modules/time/utc/epoch/day-in-week.kh` and `modules/time/utc/weekday.kh`; it names this file's `Day()` / `DayHours()` as the motivating example for "whether a recurring calendar entry is a repetition rule in the time domain or a repetition attribute on the entry".

**So the code puts the *values* on staff and leaves the *vocabulary* on shift, and nothing owns the span.** Whether that is a staff attribute, a shift attribute, or a time-domain concept cannot be answered from this tree: the answer decides whether `DayHours` needs an owner in the time domain or a field on a staff record, and no document in any of the three domains states it.

### Open Questions raised by the conversion

- **No `StaffModel` exists and none was written.** The domain document is one sentence — "Staff relates users to organizations as personnel" — and that relation is the two edge docs (`edges/group`, `edges/staff`), neither of which has code. A `StaffModel` over identity alone would be the empty extension point rule 6 names. What it would compose instead is the open question: a staff member is a user (`Field_StaffID` returns `UserUUID`), belongs to a group (`edges/group`), and has an employment lifecycle (`edges-loop/staff-status.kh`).
- **`edges-loop/staff-attendance.kh` and `edges-loop/staff-status.kh` sit at the root of `edges-loop/`, not in edge folders.** Phase 0's "one folder per edge" rule gives every other edge a `<name>/<name>.md`; these two are bare files under `edges-loop/` with a label vocabulary and no folder document, and [`edges/attendance/attendance.md`](edges/attendance/attendance.md) reaches into `_import/staff-attendance.kh` to describe the record that `edges-loop/staff-attendance.kh` is named for. Two files, one capability, split across `edges-loop/` root and `_import/`. The folder move is the Phase 0 review's, not this conversion's.
- **`(staff)-[:relation_staff]->(staff)` and `(staff)-[:relation_group]->(group)` are unconfirmed candidates with no code** ([`edges/staff/staff.md`](edges/staff/staff.md), [`edges/group/group.md`](edges/group/group.md)). Both docs note `Evaluation` appears on both, `HireBy`/`HireFor` are counterparts, and neither direction nor name is ratified. Converting either would ratify it.
- **The hiring pipeline is a vocabulary with no target node** ([`edges/hiring-pipeline/hiring-pipeline.md`](edges/hiring-pipeline/hiring-pipeline.md) — "Target node unconfirmed … labels read as annotations on a hiring Task or on the staff-candidate relation"). Nothing to convert, and the same document's open question about whether it converges with [`../task/edges-loop/task-labels/task-labels.md`](../task/edges-loop/task-labels/task-labels.md)'s `NeedAlternate` family is a one-rejection-vocabulary-or-two question that spans two domains.

## Role research pointer (2026-10-18)
[`../role/role.research.001.md`](../role/role.research.001.md) analyses this domain with role, department, shift and calendar. Proposals only (Tentative; nothing ratified) that reach this handoff:
- Employment (Hire, Fire, End) and holding a position are two relations; ending an employment ends that organization's occupancies by a rule. Contradiction 2 there: the Decided staff identity (the user's) cannot name two concurrent or successive employments of one user (research Open Questions 5 and 6).
- `PresentedID` ("alternate or replace") is an acting occupancy; `Evaluation` is the thing-level evaluation capability; `approveOrgPositionByPerson` is the acceptance step of an appointment.
- `StaffTimingUTC` is an obligation stated by the organization and `StaffShift` a preference stated by the person: two facts, not one record (Open Question 13).
- The hiring pipeline's unconfirmed target is a hiring task whose subject is a vacant position (Open Question 18).

## Related Artifacts
- [`README.md`](README.md)
- [`../role/role.handoff.md`](../role/role.handoff.md)
- Memar `agency.md`

## Notes
- Provenance: Organization ideas backlog → second-pass Agency Hybrid Agency bullet (2026-09-16 migration).
