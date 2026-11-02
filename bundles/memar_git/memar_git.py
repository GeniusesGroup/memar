#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
GIT_COMMAND = 'git'
SUMMARY = 'commit, take back, rename, remove, stash, restore and recover work in a working tree several tasks share, and keep task records'
DESCRIPTION = '''memar git: git operations that do not lose work, and the task records on the records branch

Deleting, moving, discarding, stashing, restoring and committing in a working tree other tasks share go through
these verbs, never through the host's own rm, git rm, git restore, git checkout of paths, git clean or a plain
git commit, nor a command a runtime rewrites. Commit only this task's paths; every commit names the tasks it
carries out with --task-id for each, or says --no-task. Every verb that acts on a repository takes --repository
PATH and never reads the folder it is run from. When a commit stops partway, do what its message says, and never
delete a lock file to get past one.

A file that matches .gitignore but is already tracked still shows as modified: ignoring does not untrack, and
restoring it away is not the fix.

Each verb below says what it does in its own --help.
'''

def describe(verbs) -> None:
    verbs.add_parser(GIT_COMMAND, help=SUMMARY, description=DESCRIPTION)
    return None
