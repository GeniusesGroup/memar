# Task — the folder that keeps a task
Status: Tentative

## Abstract
The kernel [Task](../../../modules/management/task/task.md) holds a task's intent, check, status and relations and nothing of any text. This document is the pluggable module's: how one task is kept as a folder, and how what the task makes about each domain is written so that it can be moved, by a script that reads no text, to the document it concerns. The shape is Tentative (the owner reviews it) and the rules it applies are the [Task rules](rules/README.md).

## Explanation

### What the folder is for
A folder is the file realization of a task's node, its timeline and its edges to the documents it changes. Every content of the timeline is one file; a file's place is decided by the edge that says which document it concerns, so the path is the edge and the move to the home is a rename.

### The shape
```
<task id>/
  plan.md            the current plan (the first content of the timeline, and the one a worker always has)
  report.md          the current report
  claim              written by Memar while an agent holds the task
  timeline/          NNNN-<kind>.md      contents that concern no domain: earlier plans and reports, calls, asks, replies, critiques
  domains/<domain path>/
    @handoff/        NNNN-<slug>.md      one entry each: a decision, a question, an assumption, a piece of anticipated work
    @changelog/      NNNN-<slug>.md      one record each, in the form the changelog facet gives
  docs/  services/  tests/  temp/        as `layout.py` gives them today
```
- **`NNNN` is the content's number on the task's timeline** ([A reply names what to read](rules/a-reply-names-what-to-read/a-reply-names-what-to-read.md)): one number space for the whole folder, so the timeline is the files of `timeline/` and of every `domains/` folder sorted by `NNNN`, and the number is meant to be the same in the folder and in the memory store.
- **The path under `domains/` is the domain's path in the repository**, for example `domains/modules/management/timeline/@changelog/0007-storage-decisions.md` concerns `modules/management/timeline/timeline.changelog.md`. The names `@handoff` and `@changelog` are reserved, so a domain whose own folder is called `handoff` or `changelog` (the documentation facets) is not confused with a records folder. A document that is not a module's base document, a `.kh` file included, has its own file path as the folder (`domains/modules/computer/type/protocol/detail.kh/@handoff/`). A task's plan and report are not split by domain: a plan is one agreement of one task ([Plan](../../knowledge/documentation/plan/plan.md#what-a-plan-is)).
- **Two names are kept apart.** `NNNN` is the number on the task's timeline; the name a record takes at its home is `<instant>-<task id>-<slug>.md`, and the number is kept in its front matter.
- **A number is taken by creating its file exclusively** (the next number, retried when the file exists), so two agents writing at once never share one, and a file is never deleted, so a number is never reused. This realization supersedes the note of [Plan](../../knowledge/documentation/plan/plan.md#a-task-holds-rounds-of-plans) that a second round overwrites `plan.md`.
- **It rests on option 1 of the open question in the [Timeline Handoff](../../../modules/management/timeline/timeline.handoff.md)** (a stored number, a stored `reply_to`); the handoff of 2026-10-23 said replies and positions are not stored, and the folder is only how they are carried until that is settled.
- **A reply is a file like any other**; the `reply_to` edge, the participant it asks and the numbers it asks to be read are in its front matter, and a critique called for by an ask is a file of `timeline/` or of the domain folder of the document it examines.
- **A superseded plan or report moves to `timeline/` under its number when the next round starts**; `plan.md` and `report.md` at the top are always the current ones, so the services that read them keep working, and nothing is overwritten.

### Moving a record to its home
When a task ends and its records are kept, a script moves each file under `domains/` beside the document it concerns, keeping its name: `<document folder>/<base>.changelog/<instant>-<task id>-<slug>.md` and `<document folder>/<base>.handoff/…`. The assembled `<base>.changelog.md` and `<base>.handoff.md` stay at their paths as views the `view refresh` verb makes from those files, in the order of their instants; the view's head (`## Topic & Purpose` and `## Status`) is a state of the document, not an entry, and is the one part an agent still writes in place (open for the owner), so every link and anchor in the repository keeps resolving while the move is made. The records are nodes of the memory store when the programme of the memory port reaches them: the folder is only how they are carried until then.

### What the old shape holds
Counted on 2026-10-30 by a script kept in the design task's `services/` (`inventory.py`), over the 205 task folders that exist and the files that Git tracks:

| Old shape | Count | Is the move mechanical |
| --- | --- | --- |
| task folders; `plan.md`; `report.md` | 205; 199; 198 | the top files stay where they are (the current plan and report) |
| plan front matter key sets | 23 | yes: one reading of the keys, missing keys defaulted; `ID`, `Start Date`, `Conversation` are the ones some lack |
| plan section sets | 13 (140 of `Request, Why, Steps, Next`; 42 of `Request, Acceptance check, Steps, Next`) | yes: a part is renamed by a table of the thirteen |
| report section sets | 16 (170 of `What ran, Check, Result, Left open`) | yes, by the same kind of table |
| `*.changelog.md` files; entries (`### ` under `## Changelog`) | 221; 1294 | partly: an entry begins at `### ` and ends at the line `---` or the next `### `; 1281 of the 1294 carry `- Time:` (an hour, so ties are broken by file order) and the other 13 go to `0000-undated-` names; `- Tasks:` is optional, so the task of most entries is not recoverable and the name has none; the 47 heading shapes are counted and not yet read one by one |
| `*.handoff.md` files | 256 | partly, and not by instant: an entry of a handoff carries no `Time` and seldom a task, and is edited in place later (Tentative becomes Decided), so it is named `0000-<slug>` with the order of the file kept in a front matter line, and the authoring task is unknown; `## Open Questions` (241 files), `## Decisions` (152), `## Status` (134), `## Related Artifacts` (113) split at `### `; a `## Status` and a `## Topic & Purpose` are one state per file and are kept as the head of the view, not as entries |
| `*.research.NNN.md`, `*.practice.md` | 47; 15 | not moved: they are documents, not records |

An entry that has no `### ` heading (a bullet under a `##`) is not split by the script; it stays in the view's head and is listed for a person, which is the one part that is not mechanical. The count of such entries is the first output of the migration script's dry run.

### The migration of old tasks, in order
1. The script reads each old plan and report into one front matter and one section order, and writes nothing else of the task.
2. It splits every changelog into one file per entry and every handoff's entries into one file per `### `, under the document's own folder (`<base>.changelog/`, `<base>.handoff/`), naming them by their instant where there is one and `0000-undated-` where there is none, and lists those for a person.
3. It makes the assembled view from them and compares it, entry by entry, with the file it replaces; a view that is not equal to the old file stops the move.
4. The files that still carry text outside any entry are listed, and a person decides them.
5. Only then are the services that append to a changelog or a handoff changed to write an entry file instead (the build task of the queue that reshapes them).

## Critique of the owner's model of the critic
The strengths, what the model lacked and what the rules add are recorded in [the Task handoff](../../../modules/management/task/task.handoff.md#critique-as-a-content-on-the-timeline-2026-10-30-tentative).
