# Documentation — Plan Handoff
## Topic & Purpose
The Plan facet's specification was written on 2026-10-16 by applying the owner's answers to the proposal in `.agents/tasks/20261016-T003724Z-23508/report.md`. The proposal and the answers are recorded there and in that task's plan; what is settled needs no entry here. This handoff carries the edges the specification leaves open.

## Status
Active

## Open Questions
- **Whether the plan and the report merge into one facet.** The owner deferred this to the session that examines shared service types (`20261013-T161701Z-2296`), on the ground that the two kinds share a type for their shape and may share more once that type is examined. The two specifications state the separation on the attribute where they do not overlap — the file name and the place of consumption — and point at that chat as the place the question belongs. Anchor: [plan.md → Why this facet and the report facet stay separate](plan.md#why-this-facet-and-the-report-facet-stay-separate).
- **Whether the plan's acceptance check gets a part or a front-matter key of its own.** It is prose today, inside the part that carries what was asked, and the closed shape in `modules-plugable/knowledge/documentation/plan/primitive/plan_key.py` has no field for it. Giving it one changes the shape, which is the owner's call; the proposal raised it and it was not answered. Anchor: `.agents/tasks/20261016-T003724Z-23508/report.md`, decision D5 and its *Decisions needed* entry 2.
- **Where a plan's services land.** The owner's ruling is that a facet module holds its own services; the migration of the session services under `.agents/scripts/` into `modules/` is queued as task `20261015-T123046Z-17544`. Whether that migration creates this module's `services/` folder as its destination, or moves the code elsewhere and leaves the folder for a later step, is not decided. Anchor: [plan.md → Where the code is](plan.md#where-the-code-is-and-what-a-reader-does-when-it-disagrees).
- **The code holds one plan file per task folder, against rounds (owner, 2026-10-23).** [A task holds rounds of plans](plan.md#a-task-holds-rounds-of-plans) says a task may hold several plans as contents in its timeline; `record.py`, `plan_key.py` and the plan services still read and write one `plan.md`, and a second round overwrites it. The shape types and the verbs `ensure`, `list`, `claims`, `digest` follow when the services are re-based on the memory port; the programme and its order are in `.agents/tasks/20261022-T185903Z-15504/docs/change-plan.md`. Until then no writer names a round's file.

## Anticipated Work
- The paired practice file, once writing a plan has accumulated a procedure beyond what the Memar skill states at intake.
- The same words for what each part of a plan is for stand in `memar task ensure --help` (`modules-plugable/management/task/services/ensure.py`), whose test pins them; reconciling the two is the session that reviews this specification.
