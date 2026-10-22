# Scripts Rule — Normative References Changelog

## Changelog

### The rule and its lists written, migrated from the passages of `task_kind.py`
- Time: 2026-10-16T14:30:00Z
- Type: Added
- Cited:
  - Proposal, version 3, of session 20261016-T123037Z-21048 (on the records branch dev-knowledge, `.agents/sessions/20261016-T123037Z-21048/`, file `docs/proposal.md`), sections 4 and 12 - Depends_on: the rule's name, its home, the shape of a list and of an entry, the declared places, the format and its conditions, and the migration; approved by the owner on 2026-10-16, its names and its format provisionally.
  - [`task_kind.py`](../../../documentation/plan/primitive/task_kind.py) - Evidence: the passages each kind required, which the lists carry over.
- Propagates to:
  - `.agents/scripts/services/task_kind.py`: Done (session 20261016-T135247Z-13740) - its passages are deleted; the composer reads these lists, and the faithful-migration test passed before the deletion.
  - `.agents/skills/memar/SKILL.md`: Done (session 20261016-T135247Z-13740) - its "Consult the governing document before each act" section links `normative_references.md` as the owner of the claim.
- Tasks:
  - dev-knowledge:.agents/sessions/20261016-T135246Z-24600/: Closed - the session that wrote this folder.
- Contributors:
  - [Omid Hekayati](../../../../../CONTRIBUTORS.md#omid-hekayati) - requested
  - [Claude](../../../../../CONTRIBUTORS.md#claude) (Opus 5.5 via Claude Code) - drafted, migrated

#### What changed
- [normative_references.md](./normative_references.md): the rule's main document — its claim, which it now owns, its reason, the sense of *normative* and *informative*, the shape of a list and of an entry, the declared places, its enforcement classes, its scope, keeping and dropping, the format and the conditions for changing it, what it does not claim, and that its names are provisional.
- Eight lists, one for every act and one for each kind `task_kind.py` declared on this day, with 53 entries naming 43 distinct sections. Each passage range of `task_kind.py` ("from A through B") became one entry for each heading at the first heading's level from A through B, and each kind's sections are the same set as `task_kind.py` gives it, `CORE` being the every-act list's.
- Each entry's mark is the hash `memar content section FILE '#anchor' --hash` printed for its section at the migration. The marks carry over the judgment of `task_kind.py`'s hand lists that these sections govern these acts; they record no fresh review of any section. The why sentence of each entry is new, written at the migration.
- The marks are 12 hexadecimal digits, the length `memar content section --hash` prints, not the 8 the proposal's sections 4.4 and 5.3 give.

---

### The composer reads the lists; the hand lists deleted
- Time: 2026-10-16T16:00:00Z
- Type: Changed
- Cited:
  - Proposal, version 3, of session 20261016-T123037Z-21048 (on the records branch dev-knowledge, `.agents/sessions/20261016-T123037Z-21048/`, file `docs/proposal.md`), sections 4.8, 4.9, 5 and 7 - Depends_on: how the code finds the lists, the checks, the composer and `--after`; approved by the owner on 2026-10-16.
- Propagates to:
  - `.agents/scripts/services/normative_references.py`: Done (session 20261016-T135247Z-13740) - reads the lists of the declared places given, Memar's place a constant.
  - `.agents/scripts/services/task_context.py`: Done (session 20261016-T135247Z-13740) - composes the sections the lists name, marks a changed or broken entry, prints a drop where its passage stood, counts on the first line, and records what it printed in the session's `temp/context_read.txt`.
  - `.agents/scripts/services/normative_references_check.py`: Done (session 20261016-T135247Z-13740) - the checks that need no project.
  - `.agents/skills/memar/SKILL.md`: Done (session 20261016-T135247Z-13740) - `--after` with `--session-id`, and what an agent does on a changed or missing entry.
- Tasks:
  - dev-knowledge:.agents/sessions/20261016-T135247Z-13740/: Closed - the session that made the change.
- Contributors:
  - [Omid Hekayati](../../../../../CONTRIBUTORS.md#omid-hekayati) - requested
  - [Claude](../../../../../CONTRIBUTORS.md#claude) (Opus 5.5 via Claude Code) - implemented

#### What changed
- [normative_references.md](./normative_references.md): the Enforcement section's transitional sentence now says the composer reads this folder and `task_kind.py` names no section, and what is not read or checked yet.
- The faithful-migration check of session 20261016-T135246Z-24600 ran as a test before the deletion and passed; with the deletion its Process ended, and the test is kept in this session's folder, not in the tree.

---

### Review marks renewed after the files they name moved
- Time: 2026-10-17T10:41:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../../../../../CONTRIBUTORS.md#omid-hekayati) - decided
  - [Claude](../../../../../CONTRIBUTORS.md#claude) (Sonnet 5.5 via Claude Code) - applied

#### What changed
- Nine `reviewed` marks in the lists were renewed, over seven sections. Six changed only in link targets, because documents they link moved (`docs/content.md`, `docs/rule.md` and the media types, among others), and each was re-read at its new text; the seventh, [Documentation → File Naming](../../../../../modules/knowledge/documentation/documentation.md#file-naming), gained one sentence pointing to [Label](../../../../../modules/knowledge/label/label.md), read as part of the same renewal. Every link in the lists was rewritten to the moved path.

---

### Review marks renewed again after `process.md` moved
- Time: 2026-10-17T12:30:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../../../../../CONTRIBUTORS.md#omid-hekayati) - decided
  - [Claude](../../../../../CONTRIBUTORS.md#claude) (Sonnet 5.5 via Claude Code) - applied

#### What changed
- Three `reviewed` marks of the implement list were renewed: the sections [The Cycle](../../../../../modules/process/test/test.practice.md#the-cycle), [Failure Modes](../../../../../modules/process/test/test.practice.md#failure-modes) and [Boundary: When a Test Is Not the Artifact](../../../../../modules/process/test/test.practice.md#boundary-when-a-test-is-not-the-artifact) changed only in link targets, because `docs/process.md` moved to `modules/process/process.md`. Each was re-read at its new text.

---

### Review marks renewed after commits came to name their sessions
- Time: 2026-10-17T14:00:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../../../../../CONTRIBUTORS.md#omid-hekayati) - decided
  - [Claude](../../../../../CONTRIBUTORS.md#claude) (Opus 5.5 via Claude Code) - applied

#### What changed
- The `reviewed` marks of [Scripts → Deleting, moving, restoring, and committing](../../../../../modules/knowledge/content/content.md#deleting-moving-restoring-and-committing) in the implement and mechanical lists were renewed. The section gained one rule, that every commit names the sessions it carries out through `host/git.py commit --session-id` or says `--no-session`; it was re-read at its new text, and each list's reason for reading it still holds.

---

### Scripts → committing re-reviewed after it took the skill's commit rule
- Time: 2026-10-20T09:00:00Z
- Type: Changed
- Cited:
  - Proposal of session 20261019-T193605Z-16144 (`docs/proposal.md`, cut C3) - Depends_on: approved by the owner on 2026-10-20, with the ruling that the skill's commit rule (by area, the whole work) stands and is written into the scripts README.
- Tasks:
  - 20261019-T193605Z-16144: Closed - the session that moved the rule and renewed the marks.
- Contributors:
  - [Omid Hekayati](../../../../../CONTRIBUTORS.md#omid-hekayati) - decided
  - [Claude](../../../../../CONTRIBUTORS.md#claude) (Opus 5.5 via Claude Code) - applied

#### What changed
- The `reviewed` marks of [Scripts → Deleting, moving, restoring, and committing](../../../../../modules/knowledge/content/content.md#deleting-moving-restoring-and-committing) in the implement and mechanical lists were renewed. The section now holds the commit rule the skill carried (commits follow the whole piece of work, by area, staged in place) in place of "One session task gets one commit", and why `memar content check` runs before the commit. It was re-read at its new text, and each list's reason for reading it still holds.

---

### Queued Work re-reviewed after the task verbs took the skill's delegation rules
- Time: 2026-10-22T12:00:00Z
- Type: Changed
- Cited:
  - Review of task 20261020-T090906Z-5096 (its report.md, Restore 2 and 3) - Evidence: the section's pointer to the skill was stale, and its rule on consuming decisions had lost its exception.
- Tasks:
  - 20261019-T193605Z-16144: Closed - the task that applied the restorations and renewed the marks.
- Contributors:
  - [Omid Hekayati](../../../../../CONTRIBUTORS.md#omid-hekayati) - decided
  - [Claude](../../../../../CONTRIBUTORS.md#claude) (Opus 5.5 via Claude Code) - applied

#### What changed
- The plan list's `reviewed` marks of [Handoff Practice → Queued Work and Its Hand-Back](../../../../../modules/knowledge/documentation/handoff/handoff.practice.md#queued-work-and-its-hand-back) and [Questions Found During a Task](../../../../../modules/knowledge/documentation/handoff/handoff.practice.md#questions-found-during-a-task) were renewed. Queued Work now sends a runtime that cannot open a chat to `memar ai get-new-chats-ask --help`, where that text moved from the skill, and keeps "unless its own work meets a problem with one" on consuming decisions. Both sections otherwise changed only by the renames of the session verbs to task verbs. Each was re-read at its new text, and the list's reasons for reading them still hold.
- Two links to Scripts → Deleting, moving, restoring, and committing, whose README is gone, now point to [Content → Deleting, moving, restoring, and committing](../../../../../modules/knowledge/content/content.md#deleting-moving-restoring-and-committing), which took its place in the lists.

---

### Sizing a Task re-reviewed after the owner told an inquiry from a research
- Time: 2026-10-22T16:00:00Z
- Type: Changed
- Cited:
  - The owner's answers of 2026-10-22 in task 20261019-T193605Z-16144 - Depends_on: an inquiry is a step of its task, its findings a note in that task's `docs/`; a research others build on is a task of its own; a new task only for truly independent work.
- Tasks:
  - 20261019-T193605Z-16144: Closed - the task that wrote the ruling and renewed the mark.
- Contributors:
  - [Omid Hekayati](../../../../../CONTRIBUTORS.md#omid-hekayati) - decided
  - [Claude](../../../../../CONTRIBUTORS.md#claude) (Opus 5.5 via Claude Code) - applied

#### What changed
- The plan list's `reviewed` mark of [Handoff Practice → Sizing a Task and Recording Follow-Ups](../../../../../modules/knowledge/documentation/handoff/handoff.practice.md#sizing-a-task-and-recording-follow-ups) was renewed. Its subsection "A session is for work" now tells an inquiry, which is a step of the task it serves with its findings in that task's `docs/`, from a research that gathers and concludes what many other tasks build on, which is a task of its own recorded as a Research document. It was re-read at its new text, and the list's reason for reading it still holds.
