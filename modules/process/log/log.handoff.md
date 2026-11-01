# Log Handoff

## Topic & Purpose
The abstraction that records an event in a log, asked for by the making of a task (task 20261030-T163545Z-10624).

## Status
Active — `services/record-event` and `errors/` written 2026-11-01, accepted by the Khayyam analyzer; no realization.

## Decisions
- **Recording knows no event (Decided).** `Log_Record.Record(logger, event)` appends any `ProcessLog_Event`; opened and blocked are events the task domain raises, with their words in the message. - reason: one owner; the log does one thing.
- **A failed write is returned as `Log_Error_NotRecorded` (Decided).** The caller decides whether to disregard it, as the Python did by printing a warning.

## Open Questions
- **Which `Logger` serves a folder?** Today the log of a project task location is its own and else Memar's own. That choice is the project module's (`task_location`) and is its gap, not this module's.
- **Trimming old lines** of a log (28 days, to the recycle bin) is not covered; it is a service of its own if wanted.
