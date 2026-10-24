# Documentation — Report Changelog

## Changelog

### Created the Report facet specification
- Time: 2026-10-16T15:15:30Z
- Type: Added
- Cited:
  - [Documentation](../../../../modules-plugable/knowledge/documentation/documentation.md) - Depends_on: defines the Facet system this specification joins, and states once what it says about a task's plan and report, which is not restated here.
  - [Documentation — Handoff](../../../../modules-plugable/knowledge/documentation/handoff/handoff.md) - Reference: the reader-relationship discipline and the recursion stop a Changelog-facet file applies to itself, which this specification extends to the report artifact.
  - [Documentation — Research](../../../../modules-plugable/knowledge/documentation/research/research.md) - Reference: a record that receives neither companion and the reason it gives for that, which is the pattern this specification follows.
  - [Documentation — Changelog](../../../../modules-plugable/knowledge/documentation/changelog/changelog.md) - Reference: the companion-file pairing and naming rules this specification follows for its own folder.
- Propagates to:
  - .agents/scripts/services/session_record.py and the services beside it: Done (task `20261016-T141543Z-22844`) - the shape they enforce now carries the session's identifier, as the sixth requirement of this specification states.
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) - ruled (2026-10-16)
  - [Space Bunny Alpha](../../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../../CONTRIBUTORS.md#opencode)) - drafted, applied

#### What changed
- Created `report.md` (ID 497823) as the governing specification for the Report facet: a task's report is the record one pass of work is accounted for in when it ends, held to a stated agreement about which of its contents a reader gets. It states the reader relationship, what each part of a report is for, who writes one and who reads one, the exemption from the companion convention, and six requirements a party that did not write it can decide from a stated input (Omid Hekayati - ruled the facet and its requirements; Space Bunny Alpha - drafted and applied).
- The specification writes no front-matter key, no part name, no Status value and no count as text: the line limit on a hand-back is the declaration's, reached by calling it, and the words are kept nowhere else (Space Bunny Alpha - drafted).
- The rule that a plan and its report agree when their Statuses are equal is not restated here; the specification points at [Documentation → Status](../../../../modules-plugable/knowledge/documentation/documentation.md#status), which states it once for the pair (Space Bunny Alpha - drafted).
- Created this changelog and the paired handoff, which carries what is still open (Space Bunny Alpha - drafted).

#### Considered and not done
- **A companion practice file** (`report.practice.md`): no procedure has accumulated beyond what the Memar skill states at closing, and [report.handoff.md](./report.handoff.md) carries the open edges instead.
- **Moving the report's services into this module's `services/` folder** (the owner's ruling of 2026-10-16, answer 3 and 5): the migration is queued as its own task, `20261015-T123046Z-17544`, and doing it here would move the same code twice. This specification names the queued session and states the requirement the move must leave the code enforcing.
- **Naming the hand-back part and its line limit in the requirements**: the closed set's rule is that this specification lists no value of the type, so requirement 4 says "the part a session adds when it needs someone to decide something" and "no more lines than the declaration allows".

---

### The Report specification points at Practice instead of restating it
- Time: 2026-10-16T18:06:00Z
- Type: Changed
- Propagates to:
  - modules/content/documentation/documentation.md: Done (task `20261016-T150928Z-4276`) - the passage this entry moved here no longer stands there.
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) — ruled (2026-10-16)
  - [Claude](../../../../CONTRIBUTORS.md#claude) (Sonnet 5.5) — applied

#### What changed
- [Reader relationship](./report.md#reader-relationship): the sentence that contrasted a report with Practice by describing what Practice's reader learns now points at Practice's own section and keeps only what is the report's: read once, after the fact, for the account of a single pass.
- This is the second facet that `documentation.md` never defined, and it still reads whole after the move.
- Made in task 20261016-T150928Z-4276, finishing answer 6 of the owner's rulings of 2026-10-16: a new facet edits only its own module.

#### Considered and not done
- **Restating the other facets' reader relationships here to contrast this one with them**: each facet's own specification states its relationship, and a restatement is a second place to edit when one changes; this specification points at the other's section instead.

---

### The declarations this specification names moved out of services/
- Time: 2026-10-17T09:30:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) — ruled (2026-10-17)
  - [Claude](../../../../CONTRIBUTORS.md#claude) (Sonnet 5.5) — applied

#### What changed
- The paths this specification names for the closed sets it points at are now `modules/content/documentation/record.py` (the record's shape), `modules/content/documentation/primitive/record_key.py` (the session field) and `modules/content/documentation/primitive/status.py` (the Status values); the keys of a report's front matter are in `report/primitive/report_key.py`. No requirement changed.
- Why: the owner's rulings of 2026-10-17 place a module's primitive types in the module's own `primitive/` and the shapes built from them in its root; the Status type and the task record's shape were the first moved out of the scripts' `services/`.
- Made in task 20261017-T082614Z-25876.

---

### A task may hold several reports
- Time: 2026-10-23T08:00:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) — ruled (2026-10-22, 2026-10-23)
  - [Claude](../../../../CONTRIBUTORS.md#claude) (Sonnet 5.5) — applied

#### What changed
- [A task holds rounds of reports](./report.md#a-task-holds-rounds-of-reports) is new, and requirement 7 states it: a task may hold several reports, each a content in its timeline and never rewritten; the current report is the latest; a report's Status is a claim in its text and the task's Status is changed by a Request.
- Why: the same ruling as the plan's entry of the same date; a report is bound to a pass of work, as this specification's first line says.
- Made in task 20261022-T185903Z-15504.

#### Considered and not done
- **Merging the two kinds' rounds into one record of a round**: the question of merging the facets belongs to `20261013-T161701Z-2296` and is not touched.
