# Form respondent relation task

## Model

- Candidate (unconfirmed): `(form_respondent)-[:relation]->(task)` — respondent-to-task link (direction unconfirmed) carrying labels `Creator`, `Pending`.
- Respondent identity already has a home in this module: [respondent/protocol/data_model.go](../../respondent/protocol/data_model.go).

## Policies (rules)

- "It is announcement that user tell the system to start answer to questions." — the task announces (and presumably starts) an answering session.
- Labels `Creator`, `Pending` recorded without semantics — who the creator is, and what a pending announcement waits for, unconfirmed.

## Placement

- **Correct here — the respondent's task link stays with the form capability** (placement by entry point: instantiated when a user announces/starts answering; the respondent lifecycle already lives in this module — pluggable owns complete capability: edge + session-start processing together).
- **Not [management/task](../../../../../modules/management/task/task.md):** task stays the generic domain; a shortcut edge is owned and maintained by the capability that gives it meaning — the announcement task means nothing outside form answering.
- `Creator`/`Pending` are bare labels: if they drive workflow states, that is rule/task material to record before ratifying the edge (no bare edges).

## Open questions

- Duplicate of the form–task relation filed in [task](../task/task.md) (labels Creator/Pending)? One edge (form → task) with a respondent implied, or two distinct edges (form → task, respondent → task)?
- Announcement semantics: what does creating the task start (session, timer, notification), and who may create it (no bare edges)?
- Are `Creator`/`Pending` task-role labels, statuses, or respondent states — [task](../task/task.md) already asks this (merge candidate, not a second question of record).
- Direction/naming unconfirmed — nothing ratified.

