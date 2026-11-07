---
Title: "Log"
Labels: Draft
Start Date: 2026-11-06
ID: 498319
---
# Log

## Abstract
A **log** is the record a service keeps of what it did and what it saw: its own events, one after another, for the people and agents who look after it. A service writes a log entry through [`Log_Record`](services/record-event/record-event.kh) to a [`Logger`](protocol/log.kh), and the entry is a [`ProcessLog_Event`](protocol/log-event.kh): an [Event](../event/event.md) with a level, a message and the stack it was raised at. The domain is `process/log`. A log is about the service; it is not about the things the service acts on, and no domain fact is read from it.

## What a log is not
- **Not the history of a change of state.** A change to a domain's acquired value is recorded by a Request, and the chain of Requests is that value's history and its audit trail ([Request → Recording a change of state](../request/request.md#recording-a-change-of-state)). The Request is written in the same batch as the change and signed; a log entry is written after the act, may fail without failing the act ([`Log_Error_NotRecorded`](errors/errors.kh) is the caller's to disregard), and may be trimmed. Whatever a log says, the Requests and the domain's current values are what decide.
- **Not an error.** An error is addressed to the caller of a refused request; a log entry is addressed to whoever looks after the service ([`Error`](../error/protocol/error.kh) says the two do not mix).

## What a log holds
What a service did and saw that no domain records: a reading, a refusal, a slow call, a retry, a warning, the output of a process it started, and the service's own account of a change it also recorded by a Request. Where a log is kept, how long, and which `Logger` serves a service are the composition's choice, not this module's.

## What the verbs that write a log become
| Today | Becomes |
| --- | --- |
| A service's log file under `temp/` (events such as opened, closed, recorded, flushed, blocked, released), and its trim in the daily sweep | A log of that service, written through `Log_Record`; its home is this domain, not git's. Opened, closed, blocked and released are changes of state and are recorded by their Requests as well; the log line is only the service's account. The trim is the log's, under a period the composition sets. |
| A verb that reads a log to learn whether Memar set a state | A read of the Request chain: the last Request on that state, by `request-head`, and who asked it. No service reads a log to decide. |
| `slow.log` of the resident server | A log of the resident server: what it saw about its own calls. |
| `temp/update/update.log` of the daily update | A log of the update service: the output of the process it started. |
| A registry of names kept in a log file | Not a log: it holds acquired values that verbs read to decide, so it is a domain's record, and each change of it a Request. |
| `git log`, read by the git bundle | Git's, not a log in this sense. |
