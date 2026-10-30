# Documentation — Plan Changelog

## Changelog

### Created the Plan facet specification
- Time: 2026-10-16T15:15:00Z
- Type: Added
- Cited:
  - [Documentation](../documentation.md) - Depends_on: defines the Facet system this specification joins, and states once what it says about a task's plan and report, which is not restated here.
  - [Documentation — Handoff](../handoff/handoff.md) - Reference: the reader-relationship discipline, the open-catalog section pattern, and the recursion stop that a Changelog-facet file applies to itself, which this specification extends to the plan artifact.
  - [Documentation — Changelog](../changelog/changelog.md) - Reference: the companion-file pairing and naming rules this specification follows for its own folder.
- Propagates to:
  - modules-plugable/management/task/services/ensure.py: Pending - its help says what each part of a plan is for, in words that now have their home in this specification; the two copies should be reconciled in the session that reviews this specification.
  - .agents/scripts/services/session_record.py and the services beside it: Done (task `20261016-T141543Z-22844`) - the shape they enforce now carries the session's identifier, as the sixth requirement of this specification states.
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) - ruled (2026-10-16)
  - [Space Bunny Alpha](../../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../../CONTRIBUTORS.md#opencode)) - drafted, applied

#### What changed
- Created `plan.md` (ID 497822) as the governing specification for the Plan facet: a task's plan is the record one agreed task is given in before it is worked and read by whoever carries it out, written at intake and reaped with its task's folder. It states the reader relationship, what each part of a plan is for, who writes one and who reads one, the exemption from the companion convention, and six requirements a party that did not write it can decide from a stated input (Omid Hekayati - ruled the facet and its requirements; Space Bunny Alpha - drafted and applied).
- The specification writes no front-matter key, no part name, no Status value and no count as text: each is reached by calling `.agents/scripts/services/session_record.py` or `.agents/scripts/services/status.py`, and the specification says so rather than restating them (Space Bunny Alpha - drafted).
- Created this changelog and the paired handoff, which carries what is still open (Space Bunny Alpha - drafted).

#### Considered and not done
- **A companion practice file** (`plan.practice.md`): no procedure has accumulated yet beyond the one the Memar skill states at intake, and [handoff.md](plan.handoff.md) carries the open edges instead.
- **Moving the plan's services into this module's `services/` folder** (the owner's ruling of 2026-10-16, answer 3 and 5): the migration is queued as its own task, `20261015-T123046Z-17544`, and doing it here would move the same code twice. This specification names the queued session and states the requirement the move must leave the code enforcing.
- **Writing the plan's part names in prose** so the requirements could name the parts they concern: the closed set's rule is that this specification lists no value of the type, so each requirement says what the part must carry instead and points at the declaration.

---

### The Plan specification points at Practice instead of restating it
- Time: 2026-10-16T18:06:00Z
- Type: Changed
- Propagates to:
  - modules/content/documentation/documentation.md: Done (task `20261016-T150928Z-4276`) - the passage this entry moved here no longer stands there.
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) — ruled (2026-10-16)
  - [Claude](../../../../CONTRIBUTORS.md#claude) (Sonnet 5.5) — applied

#### What changed
- [Reader relationship](plan.md#reader-relationship): the paragraph that contrasted a plan with Practice by restating Practice's relationship (a document followed again and again) now points at Practice's own section and keeps only what is the plan's: followed once, between named parties, in a shape a program reads.
- This is the first facet that `documentation.md` never defined, and it still reads whole after the move: nothing it said depended on a definition kept there.
- Made in task 20261016-T150928Z-4276, finishing answer 6 of the owner's rulings of 2026-10-16: a new facet edits only its own module.

#### Considered and not done
- **Restating the other facets' reader relationships here to contrast this one with them**: each facet's own specification states its relationship, and a restatement is a second place to edit when one changes; this specification points at the other's section instead.

---

### A plan may carry the sessions it cannot start without, and a machine may rewrite that one key
- Time: 2026-10-16T20:00:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) — ruled (2026-10-16)
  - [Claude](../../../../CONTRIBUTORS.md#claude) (Sonnet 5.5) — applied

#### What changed
- [The requirements](plan.md#the-requirements), requirement 4, said that only the Status line is rewritten by a machine and only to queue or claim. The code already rewrote a priority, a topic and a kind by their own verbs, so the requirement disagreed with it; it now says that a machine rewrites one field's line in place, only for the verb that owns that field, and lists the Status (to queue, claim, block or release), and the priority, topic, kind and `Depends_on`.
- [Who writes a plan](plan.md#who-writes-a-plan-and-who-reads-it) names the sessions a plan cannot start without among the fields the services set.
- Why: the owner ruled on 2026-10-16 that a plan states the sessions it cannot start without as `Depends_on`, and left to the code's own rules whether a field verb may rewrite its own key: it may, because the code already does for three other keys, and one key per verb keeps each key's writer in one place.

#### Considered and not done
- **Keeping requirement 4 as it was and writing `Depends_on` only by hand**: the requirement was already untrue of the code, and a hand-written key is one more place it could be written two ways.

---

### The declarations this specification names moved out of services/
- Time: 2026-10-17T09:30:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) — ruled (2026-10-17)
  - [Claude](../../../../CONTRIBUTORS.md#claude) (Sonnet 5.5) — applied

#### What changed
- The paths this specification names for the closed sets it points at are now `modules/content/documentation/record.py` (the record's shape), `modules/content/documentation/primitive/record_key.py` (the session field) and `modules/content/documentation/primitive/status.py` (the Status values); the keys of a plan's front matter are in `plan/primitive/plan_key.py`. No requirement changed.
- Why: the owner's rulings of 2026-10-17 place a module's primitive types in the module's own `primitive/` and the shapes built from them in its root; the Status type and the task record's shape were the first moved out of the scripts' `services/`.
- Made in task 20261017-T082614Z-25876.

---

### A plan's check is that something was done
- Time: 2026-10-17T15:00:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) — ruled (2026-10-17)
  - [Claude](../../../../CONTRIBUTORS.md#claude) (Sonnet 5.5) — applied

#### What changed
- Requirement 7: a plan's check is a change applied or a decision recorded; a plan whose only check is a finding or proposal is not ready.
- Why: see the entry of the same date in the Handoff practice's changelog; session 22960 passed its check with a proposal alone.

---

### A task may hold several plans
- Time: 2026-10-23T08:00:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) — ruled (2026-10-22, 2026-10-23)
  - [Claude](../../../../CONTRIBUTORS.md#claude) (Sonnet 5.5) — applied

#### What changed
- [A task holds rounds of plans](plan.md#a-task-holds-rounds-of-plans) is new, and requirement 8 states it: a task may hold several plans, each a content in its timeline; the current plan is the latest; a change that keeps the request and the check is another round, one that changes either is a new task citing the old; a task has one Status, changed by a Request.
- The boundary [A plan is one agreement of one task](plan.md#what-a-plan-is) was "one task, not a conversation" with one plan per folder; it keeps the conversation half and points to the rounds.
- Why: the owner holds that each round of critique writes a separate plan, and that a task never carries the text of a plan (Task), so one record per task folder could not be the rule. The realization (one `plan.md`) is recorded as a defect in the handoff and follows with the memory port.
- Made in task 20261022-T185903Z-15504.

#### Considered and not done
- **Numbered plan files in the task folder (`plan.2.md`)**: every reader would pick the highest number, and the folder is to leave the repository's working tree.
- **A new task for every change to a finished task**: a work not done as asked would lose its request and its history; the line is whether the request or the check changed.
- **Rounds kept in a `rounds/` folder**: the same objection to a folder, and a state change would again have no single owner.
