# Documentation — Report Handoff
## Topic & Purpose
The Report facet's specification was written on 2026-10-16 by applying the owner's answers to the proposal in `.agents/tasks/20261016-T003724Z-23508/report.md`. The proposal and the answers are recorded there and in that session's plan; what is settled needs no entry here. This handoff carries the edges the specification leaves open.

## Status
Active

## Open Questions
- **Whether the report and the plan merge into one facet.** The owner deferred this to the session that examines shared service types (`20261013-T161701Z-2296`); the two specifications state the separation on the attribute where they do not overlap and point there. Anchor: [report.md → Why this facet and the plan facet stay separate](./report.md#why-this-facet-and-the-plan-facet-stay-separate).
- **Whether a report's hand-back stays optional.** The declaration marks the hand-back part optional and gives it a line limit; a report written without it says there is nothing to decide, which the reading party takes as the whole answer. Whether a report whose task did end in something undecided is ever complete without one is not stated anywhere, and the specification does not decide it. Anchor: [report.md → What each part is for](./report.md#what-each-part-is-for).
- **Where a report's services land.** The owner's ruling is that a facet module holds its own services; the session services were moved from `.agents/scripts/` into `modules/management/task/` by session `20261015-T123046Z-17544`, and whether this module's `services/` folder is their destination is not decided. Anchor: [report.md → Where the code is](./report.md#where-the-code-is-and-what-a-reader-does-when-it-disagrees).

## Anticipated Work
- The paired practice file, once writing a report has accumulated a procedure beyond what the Memar skill states at closing.
