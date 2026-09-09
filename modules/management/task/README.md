# Task
Task is any piece of work that is undertaken or attempted. Or in other words, a specific piece of work required to be done as a duty or for a specific fee.

## Assign task rules

- Task assign to users(staffs) by same skill requirements as task need.
So if a task need `Design` skill, related user(staff) with `Designer` or `Designing` skill will suggest to assign.
In this way `Technology Department` can hire a user with `cognitive science` skills.
And for each task, You can team up some user just for that task and break it at end of task.
- ...

## Idea backlog from edge code comments

Raw proposals from comment notes inside edge .go files (comments remain in code as source). Review discipline per [vocabulary-discipline.handoff.md](../vocabulary-discipline.handoff.md). Nothing below is ratified.

### Task labels - edges-loop/task.go
- **Idea**: default labels (Compliment, Suggestion, Issue); Project/Meeting/Event as task labels (consistent with the task-concept seed: a project IS a task); Shift as repetitive-task label; Scrum board states (Backlog, ToDo, Doing, Done); XP lifecycle (Planning, Design, Coding, Testing, Listening); rejection labels (Rejected, NotAccepted, NeedAlternate + NeedAlternateApprove/AlternateApprove, Rework, Rejection); Eisenhower matrix as a table view (Urgent/Not-Urgent x Important/Not-Important -> Do/Schedule/Delegate/Delete).
- **Review questions**: are Scrum/XP states organizational labels (pluggable) rather than core statuses? Is the boards view (below) GUI-only?

### Production sub-labels - edges/task-relation-production.go
- **Idea**: Manufacturing (tangible raw materials) vs Fabrication (combining parts) vs Production (both raw materials and intangible resources like money/credit); production lines CustomProduction/MassProduction; ByProduct; dependency note (car needs engine); job-order / production-planning; production statuses (Created, ManagerApprove, WarehouseApprove, ActiveWithApprove, ActiveWithoutApprove, ActiveWithOrderer, Inactive, Normal, Reject).
- **Review questions**: production statuses vs the general status domain (knowledge/status); is the Manufacturing/Fabrication/Production distinction a term fix or three different task kinds?

### Skill-requirement vocabulary - edges/task-relation-skill.go
- **Idea**: requirement levels as labels: Mandatory (MUST, obligatory, binding), SHOULD (nice to have, optional, conditional), MAY (not needed) - RFC-2119 style.
- **Review questions**: is this a general constraint vocabulary reusable beyond tasks (rights law? rule domain)?

### Other task relations - edges/task-relation-content.go, task-relation-invoice.go, task-relation-estate.go
- **Idea**: Report-to-the-public (task-content); Negotiation (task-invoice for price negotiation, CRM-flavored); Site (task-estate - where the task happens).
- **Review questions**: does Site intersect the estate domain spatial-relations work (see modules/identity/estate/estate.handoff.md)?

### Boards view - edges-loop/task-relation-table.go
- **Idea**: tables/boards as a GUI visual aid to access tasks (Table: TODO/DOING/DONE).
- **Review questions**: is a board a GUI projection (per projection != domain model) or a persisted grouping?