# Task relation user

## Model

- Candidate (unconfirmed): `(task)-[:relation_user]->(user)` carrying the labels below (source was `package label` holding comments only, no edge code).

## Policies (rules)

- Participation/assignment labels: `Participant`, `Assigner`, `Reviewer`, `Assigned`, `Approver`.
- `WaitList`.
- `Invited` — "RequestID of making relation is made by inviter user."; "Invited user CAN check who invite itself to this task".
- No who-may-assign/what-it-triggers recorded — labels must not be ratified as edges (no bare edges).

## Placement

- **Not an edge of ownership; strip.** Task participation grants no ownership: rights come first and ownership arises from rights ([rights.md](../../../rights.md)) — participant roles must not become ownership primitives. Removing it distorts nothing in ownership (core-by-necessity fails).
- Candidate homes by label: `Assigned`/`Assigner` overlap the folder-mate [assigner](../assigner/assigner.md) (one label set, not two); task-participation review belongs with [task](../../../../management/task/task.md); `Invited` + inviter-RequestID overlaps the existing [invite](../../../../../modules-plugable/management/invite/invite.md) capability — if invitation is real, its complete capability already has a home there; do not fork it (pluggable owns complete capability).
- Not a new module: the label set alone carries no processing semantics (parameters vs semantics).

## Open questions

- Why does a task-relation live under ownership at all (assignment is not ownership)? Reconcile with the rights-first ordering — the standing question the ownership backlog used to hold ([ownership.md](../../ownership.md)).
- Is `Invited` the invite capability's edge (invite owns RequestID semantics), or only a label task carries?
- `Reviewer` was recorded against task, chat, and comment — one reviewer edge across surfaces, or per-surface labels (parameters vs semantics)?
- Loop-edge shape and direction unconfirmed — nothing ratified.

