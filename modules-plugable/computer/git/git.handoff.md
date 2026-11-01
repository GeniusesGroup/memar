# Git Handoff

## Topic & Purpose
The abstraction that sweeps idle task folders, asked for by the making of a task (task 20261030-T163545Z-10624).

## Status
Active — `services/sweep-idle-folders`, `protocol/sweep-reaped.kh` and `errors/` written 2026-11-01, accepted by the Khayyam analyzer; no realization.

## Decisions
- **The sweep does one thing (Decided).** It moves the idle candidates it is given, except the named one, and returns what it moved. Choosing candidates (only folders of a task-id form, finished, not Queued), keeping their records first (a folder whose records cannot be kept must not be moved), once a day, logging and trimming the log are other services and the widget's join; records-then-move is a requirement on that widget. - reason: a service never aggregates.
- **What finished means is not the sweep's (Decided).** A `finished` port is the plan module's to declare (today `is_complete`); it is the plan's gap and git imports it when it exists.

## Open Questions
- **Is a folder a `MemoryAddress`?** The sweep names folders by address as the task id does; if folders are another kind of place, the parameter changes.

- **Folders, age and the recycle bin may belong to the filesystem module.** The reviewer found nothing here git-specific; it sits in git because the Python did. Owner to rule whether the service moves there.
- **The per-folder outcomes the Python printed** (kept with why, flagged, stuck) are not returned; `Sweep_Reaped` holds only what moved.
