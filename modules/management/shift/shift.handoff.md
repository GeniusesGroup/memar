# Shift Handoff

## Topic & Purpose
Converting the Khayyam protocol layer of `modules/management/shift`: the identity surface (`protocol/dt-uuid.kh`), under the governing rules in [`../../../Khayyam.practice.md`](../../../Khayyam.practice.md). `git ls-files modules/management/shift` returns five files; one was a source with declarations and it was converted.

## Status
Protocol layer converted (2026-10-03). `protocol/dt-uuid.kh` accepts against the Khayyam frontend, against a root where both `org/…` and `memar/…` resolve.

**The domain is not modelled.** What converted is identity. [`shift.md`](shift.md) is nine lines long and models shift as `(task)-[:shift]->(---)` — a relation from a task with an undecided far end. Everything that would make a shift a timed thing lives in another domain; see Open Questions.

## Decisions

- **A shift's identity is the thing domain's identity.** *(Decided.)* The Go source wrote `type UUID task_p.UUID`; `task_p.UUID` is itself `group_p.UUID`, itself `user_p.UUID`, itself `thing_p.UUID` — the fourth link in the chain. Khayyam has no alias form, so the file includes `ThingUUID` from `modules/identity/thing/protocol/dt-uuid.kh` and declares no `ShiftUUID`. Result parameter `t`, matching `Field_EdgeID` / `Field_EstateID`.
- **`edges-loop/shift.kh` was left unconverted.** *(Decided.)* It is `package label` holding two `iota` constants (`Type_Strict`, `Type_Float`) and nothing else — vocabulary, which is data. It is also the only file under `edges-loop/`, at the folder's root rather than in an edge folder, and there is no `edges-loop/shift/shift.md`; Phase 0's "one folder per edge" rule has no document for it. See Open Questions.
- **`Field_ShiftID` is declared and nothing composes it.** *(Carried, not fixed.)* Nothing in the repository reaches `ShiftID`. The one caller is `ShiftID()` on two staff-side records under `../staff/_import/` (`staff-timing-utc.kh`, `staff-shift-preference.kh`), which were left unconverted. Writing a consumer for it here would be inventing a domain.

## Open Questions

- **Shift timing belongs to no domain, and this conversion does not settle where it goes.** *(The question the staff wave asked, answered from the code.)* The code says the following, and nothing more:
  - `../staff/_import/staff-timing-utc.kh` declares `StaffTimingUTC` with `StaffID()`, `ShiftID()`, `Day() utc.DayElapsed`, `DayHours() earth.DayHours` (commented "what hours in a day this staff must active to provide services or do projects"), `Time()`, `RequestID()`. `../staff/_import/staff-shift-preference.kh` declares `StaffShift` with the same `StaffID()` / `Day()` / `ShiftID()` triple minus the hours.
  - **This module holds none of it.** `Day()`, `DayHours()` and `AttendanceTime()` appear nowhere under `modules/management/shift/`. The shift module's own model is one line — "`Shift` is repetitive task" — expressed as `(task)-[:shift]->(---)`, a relation from a task rather than a timed node.
  - So the *values* are on the staff side and the *vocabulary* is here, and the span between a shift's start and its end is owned by nobody. Whether that is a staff attribute, a shift attribute, or a time-domain concept is not answerable from this tree. It decides whether `DayHours` needs an owner among `modules/identity/time` / `modules/management/calendar` or a field on a staff record, and no document in any of the three domains states it. [`../staff/staff.handoff.md`](../staff/staff.handoff.md) → *What the code says about shift timing* carries the same evidence from the staff side; the two agree and neither settles it.
  - `edges-loop/shift.kh`'s two constants (`Type_Strict`, `Type_Float`) look like *shift types* — a strict (fixed-window) shift and a float (flexible-hours) shift. That reading would make this module's own vocabulary about timing, which is the strongest hint in the tree that timing is meant to be here, and it is a two-constant hint with no document behind it.
- **`(task)-[:shift]->(---)` has an undecided far end**, and it decides what a shift *is*. If the far end is the staff member, the edge is a task-to-person assignment and `../staff/_import/staff-shift-preference.kh` is its record. If the far end is a time window, shift is the missing timed node the calendar handoff also found missing. If the far end is a group or a department, shift is a property of the organisation's structure.
- **Shift is described as a repetitive task, and the repetition question is open in three domains at once.** [`shift.md`](shift.md) says "Shift is repetitive task"; [`../task/edges-loop/repetitive/repetitive.md`](../task/edges-loop/repetitive/repetitive.md) says a repetitive task "MUST made other related task when need to do the task in that period" and that the related task "MUST made by rule domain by `rules-engine` not human process"; [`../task/edges-loop/task-labels/task-labels.md`](../task/edges-loop/task-labels/task-labels.md) asks "Shift-as-repetitive-task-label vs the [shift] module — label marker or module-owned repetition?" Whether a recurring shift is a repetition rule in the time domain or a repetition attribute on a task is the same question [`../calendar/calendar.handoff.md`](../calendar/calendar.handoff.md) asks, and it decides whether a shift record is one row or many.
- **`edges-loop/shift.kh` is a bare file at the root of `edges-loop/` with no edge folder and no document.** The other bare label files in this wave's domains are [`../staff/edges-loop/staff-attendance.kh`](../staff/edges-loop/staff-attendance.kh) and [`../staff/edges-loop/staff-status.kh`](../staff/edges-loop/staff-status.kh), and they are documented by [`../staff/edges/staff-status/staff-status.md`](../staff/edges/staff-status/staff-status.md). This one has neither. The Phase 0 review's folder move is not this conversion's to make.
- **Nothing consumes `Field_ShiftID`.** The same state `../calendar/calendar.handoff.md` recorded for `Field_CalendarID` and `../department/department.handoff.md` recorded for `Field_DepartmentID`: the accessor has no consumer in the tree.

## Role research pointer (2026-10-18)
[`../role/role.research.001.md`](../role/role.research.001.md) analyses this domain with role, staff, department and calendar. Proposals only (Tentative; nothing ratified) that reach this handoff:
- "Shift" is three things in the documents: a pattern (the morning shift), a duty instance (this Tuesday's duty, a task made from a repetition rule) and an assignment (who holds the duty). The proposal makes the pattern the thing of a `coverage` capability of a position, with `Type_Strict` and `Type_Float` classifying the pattern (Open Question 12; the survey default P12).
- `Field_ShiftID` has no consumer once the instance is a task (Open Question 12).

## Related Artifacts

| Artifact | Relation | Action |
| --- | --- | --- |
| [`shift.md`](shift.md) | Domain document; the one-line model and the repetitive-task policy | Keep in sync |
| [`../staff/_import/staff-timing-utc.kh`](../staff/_import/staff-timing-utc.kh) | The record that carries `ShiftID()`, `Day()` and `DayHours()` — the code that puts shift timing on the staff side | None (left unconverted) |
| [`../staff/_import/staff-shift-preference.kh`](../staff/_import/staff-shift-preference.kh) | The second staff-side record with the same staff/day/shift triple | None (left unconverted) |
| [`../staff/edges-loop/staff-status.kh`](../staff/edges-loop/staff-status.kh) | Comments `Status_Active` / `Status_Inactive` out with the note `Shift` | None (read) |
| [`../staff/staff.handoff.md`](../staff/staff.handoff.md) | The same timing question, read from the staff side | Keep in sync |
| [`../task/edges-loop/repetitive/repetitive.md`](../task/edges-loop/repetitive/repetitive.md) | "Repetitive task" — the policy half of "shift is repetitive task" | None (read) |
| [`../task/task.handoff.md`](../task/task.handoff.md) | The task wave of this conversion | None |
| [`../calendar/calendar.handoff.md`](../calendar/calendar.handoff.md) | Asks the same repetition question for a calendar entry | None (read) |
| [`../../../Khayyam.practice.md`](../../../Khayyam.practice.md) | Governing rules 1–7 | None (read) |

## Notes

- **Frontend result.** `modules/management/shift/protocol/dt-uuid.kh` — **accept**. Nothing was suppressed and nothing was refused.
- **How it was verified.** Against `…\khroot_copy\`, built by copying every `.kh` in the organization repository to `org/` and every `.kh` in the memar repository to `memar/`, preserving relative paths (physically — Node does not follow Windows junctions). This file was checked after the other eight files of the wave, so the sweep against a single root stayed consistent.
- **Line endings.** `protocol/dt-uuid.kh` is CRLF, matching the converted `.kh` files in the repository; this file is LF, matching the Markdown. No BOM in either. Verified by reading the bytes.
- **No empty abstraction was written without recording it.** Rule 6 is satisfied by argument: `Field_ShiftID ab` is empty because the requirement it carries is the accessor beside it and the body is generated (rule 2) — the same shape as `Field_TextID` / `Field_CalendarID` / `Field_EdgeID`. No `ShiftModel` was written, because nothing in the tree states a requirement beyond identity, and one composed of identity alone would be the empty extension point rule 6 names.
