# Repository instructions

## Memar
Before any other work in a session, load and follow [`.agents/skills/memar/SKILL.md`](.agents/skills/memar/SKILL.md).

## Records branch `memar`
Never check out, push, pull, fetch-into, reset, rebase, merge, delete, rename, or otherwise move the git branch named `memar`. It is the task-records branch (`RECORDS_BRANCH`); it must never be HEAD in a worktree an agent uses. Change task records only through Memar services (`task ensure`, `conversation post`, `git show-task-records`, …), which write via `record` without touching HEAD, the shared index, or the working tree. Do not run raw `git` against that branch.
