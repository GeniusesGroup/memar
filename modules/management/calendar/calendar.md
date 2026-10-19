# Calendar
Calendar records time-stamped entries (events, work periods) for persons and organizations.

## Identity

A calendar's identity is the thing domain's identity. This domain declares no UUID concept of its own; it includes the thing domain's declaration and keeps only the requirement that a calendar record can be named (`Field_CalendarID` with its accessor `CalendarID`).

The reason is the one the Go source recorded: a calendar record's ID is *usually some other domain's UUID* — an `invoice`, `form`, `department`, `role`, `task`, `user`, `production`, `batch`. The calendar does not mint identity; it is a time-stamped reading attached to whatever thing already has one. That is why the identity type is imported rather than declared.

## Idea backlog

Review discipline per [vocabulary-discipline.handoff.md](../vocabulary-discipline.handoff.md). Nothing below is ratified.

### Reason edges - moved to the pluggable module

- **Resolution**: the reason vocabulary (event, enter/exit, start/end, cooking, packaging) lives in [modules-plugable/management/calendar-reason](../../../modules-plugable/management/calendar-reason/README.md) under `edges-loop/` — reasons are organization policy, not management-core code. The core keeps only the calendar node and its generic time semantics. Calendar system kind (Gregorian, Persian, …) is a classification of that node: [edges-loop/type](edges-loop/type/README.md).
- **Open multi-typing question** (from the cooking comment): usually a calendar is a `product`, but it can also be other ones like a `task` - which identity does the calendar node take? (multi-typing principle)
