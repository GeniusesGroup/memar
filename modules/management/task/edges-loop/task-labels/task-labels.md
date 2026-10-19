# Task labels

## Model

- Candidate (unconfirmed): a label set on the task node itself (source was `package label` holding comments only, no edge code) — the "labels a task carries" vocabulary: defaults, kinds, repetitive marker, Scrum/XP states, rejection labels, Eisenhower view hint.

## Policies (rules)

- Default labels: Compliment, Suggestion, Issue.
- Kind labels: Project, Meeting, Event (consistent with the task-concept seed that a project IS a task — [task-concept](../../edges/task-concept.md)).
- "Repetitive task for staffs:::" → Shift.
- Scrum Board: Backlog, PlanToDo or ToDo, Doing, Done.
- Extreme Programming (XP) life cycle: Planning, Design, Coding, Testing, Listening.
- Rejection: Rejected, NotAccepted; NeedAlternate, NeedAlternateApprove, AlternateApprove; Rework, Rejection.
- Eisenhower Matrix ("It can show as table"): Urgent/Important → Do(now); Not-Urgent/Important → Schedule; Urgent/Not-Important → Delegate; Not-Urgent/Not-Important → Delete(avoid).

## Placement

- **Correct here — the task label vocabulary is the task capability's own** (module skeleton: `task/edges-loop/`; only task gives these labels meaning; prefer existing homes over inventing new modules).
- Scrum/XP/rejection states: recorded as *labels*, not core statuses — if an organization wants Scrum it labels/edges-loops them (pluggable organizational vocabulary), never hard-coded kernel states; who may set/reject is policy → rules (core never knows Rule).
- Eisenhower matrix is explicitly a *table view* of labels — a GUI projection, not stored semantics (projection ≠ domain model; boards view doc: [table](../table/table.md)).
- Rejection labels overlap the [hiring pipeline](../../../staff/edges/hiring-pipeline/hiring-pipeline.md) cooldown/approval vocabulary — flagged, not merged (see Open questions).

## Open questions

- Are Scrum/XP states organizational labels (pluggable) rather than core statuses?
- Is the Eisenhower matrix GUI-only (view over Important/Urgent flags), or does Urgent/Important become stored metadata?
- Do rejection labels (`NeedAlternate` family) converge with the staff [hiring pipeline](../../../staff/edges/hiring-pipeline/hiring-pipeline.md) rejections — one rejection vocabulary?
- Shift-as-repetitive-task-label vs the [shift](../../../shift/shift.md) module — label marker or module-owned repetition?
- Does `Project`/`Meeting`/`Event` duplicate kind-classification handled by other edges-loop type sets?

