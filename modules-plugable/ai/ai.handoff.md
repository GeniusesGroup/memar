# AI Handoff
## Topic & Purpose
The abstraction that composes the text handing a task to a sub-agent, asked for by the making of a task (task 20261030-T163545Z-10624).

## Status
Active — `services/compose-plan-brief` written 2026-11-01, accepted by the Khayyam analyzer; no realization.

## Decisions
- **The brief is a `Text`, produced by `Plan_Brief_Compose` from the address of the task alone (Decided).**
- **Whether the task has a plan is not checked here (Decided, after review).** That is the task and plan owners'; the service is a pure address-to-text function and has no error.
