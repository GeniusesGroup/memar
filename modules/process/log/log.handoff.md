# Log Handoff

## Topic & Purpose
The abstraction that records an event in a log, asked for by the making of another abstraction (record 20261030-T163545Z-10624).

## Status
Active — `services/record-event` and `errors/` written 2026-11-01, accepted by the Khayyam analyzer; no realization.

## Decisions
- **Recording takes any event (Decided).** `Log_Record.Record(logger, event)` appends any `ProcessLog_Event`; events such as opened and blocked are raised by the domain that owns them, with their words in the message. - reason: one owner; the log does one thing.
- **A failed write is returned as `Log_Error_NotRecorded` (Decided).** The caller decides whether to disregard it, as the Python did by printing a warning.
