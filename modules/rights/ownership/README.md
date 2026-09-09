# Ownership
Any `thing` that can be own by any `user` (`person`, `organization`, `group`, ...) have some responsibility for the `owner`!

## Open questions (from the rights domain-boundaries proposal - awaiting review; estate session)

- **Bare edge or node?** Is `owner --owner_is--> thing` sufficient, or is Ownership a legal relation with subject, object, scope, fraction, start/end, restrictions, origin, and transferability - i.e. a node that *creates* rights/duties (and possibly more edges: `heir_is`, transfer, lease, mortgage, ...)? Note `heir` already exists as an edge here; the estate session confirmed that taking an ownership edge opens the path to further edges - the question is whether those edges hang on a node or pair directly.
- **Rights-first ordering** (Omid, confirmed in the estate session): rights exist first; ownership/legal relations *arise from* rights - so the model here must not make ownership the primitive that grants rights.
- Ownership is not estate-specific (anything can be owned) - it lives here, not in the estate domain.

## Idea backlog from edge code comments

Raw proposals from comment notes inside edge .go files (comments remain in code as source). Review discipline per modules/management/vocabulary-discipline.handoff.md. Nothing below is ratified.

### Task-staff relations in edges-loop - edges-loop/task-relation-staff.go, task-relation-group.go, task-relation-user.go
- **Idea**: task-relation-staff carries a full HR/leave taxonomy (Interview, OverTime, TakeLeave, Mission, Meeting, Negotiation, Deal, Study + leave types Vacation through Volunteer) - likely misfiled here; the staff module README holds the review. task-relation-group: Assigned (group as a team working a task) plus the production-dependency note (car needs engine). task-relation-user: Reviewer (for task, chat, comment), WaitList, Invited (the inviting user's RequestID is recorded; the invited user CAN check who invited them).
- **Review questions**: why do task-relations live under ownership at all (assignment is not ownership)? Reconcile with the rights-first ordering and the ownership edge list.