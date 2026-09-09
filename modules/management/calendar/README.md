# Calendar
Calendar records time-stamped entries (events, work periods) for persons and organizations.

## Idea backlog from edge code comments

Raw proposals from comment notes inside edge .go files (comments remain in code as source). Review discipline per [vocabulary-discipline.handoff.md](../vocabulary-discipline.handoff.md). Nothing below is ratified.

### Reason edges - moved to the pluggable module

- **Resolution**: the reason vocabulary (event, enter/exit, start/end, cooking, packaging) moved to the pluggable module [modules-plugable/management/calendar-reason](../../../modules-plugable/management/calendar-reason/README.md) - reasons are organization policy, not management-core code. The core keeps only the calendar node and its generic time semantics. Each reason carries its own "Policy (rule)" placeholder there.
- **Open multi-typing question** (from the cooking comment): usually a calendar is a `product`, but it can also be other ones like a `task` - which identity does the calendar node take? (multi-typing principle)