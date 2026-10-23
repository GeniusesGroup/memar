#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""computer/git/services/_tasks.py — the tasks a commit carries out, named in its message (owner, 2026-10-16).

A commit that cites no task cannot be traced to the decisions that produced it, so `commit`
refuses one unless the caller says it carries out none. The form is one git trailer a task,
`Task: <id>`, with the bare id: `git log --format=%(trailers:key=Task,valueonly)` reads it
back one id a line, a fold of several commits keeps the union of their lines, and `memar task
show` resolves the id to the task's folder or its records wherever they are today, so no
branch name is written into history.

The caller names each task with `--task-id` and the verb writes the trailer itself, through
`git interpret-trailers`, into the message's own trailer block, so a `Co-Authored-By:` stays a
trailer. A `Task:` the message already holds is refused: an id reaches history only by the one
route that checks it.

The check is `memar git show-task-records --list` run as a process, the same lookup a reader of the commit
will use, with the repository committed to as its project. This shelf imports nothing from
`services/`: the two meet at the command line, which is the interface `services/` offers anyone,
so the lookup has one implementation and this file holds none of its knowledge (where a task
folder is, which branch keeps records).
"""
from __future__ import annotations
import os
import subprocess
import sys
from pathlib import Path
from modules.process.project.primitive.project_path import ProjectPath
from ._run import plumb
TRAILER = 'Task'
NO_TASK_FLAG = '--no-task'
TASK_FLAG = '--task-id'
ROUTER = Path(__file__).resolve().parents[4] / 'bundles' / 'memar' / 'memar'

def cited_by_hand(message: str, root: Path) -> list[str]:
    """The `Task:` trailers MESSAGE already holds."""
    parsed = plumb(['interpret-trailers', '--parse', '--no-divider'], root, data=message.encode('utf-8'))
    return [value.strip() for key, _, value in (line.partition(':') for line in parsed.splitlines()) if key.strip().lower() == TRAILER.lower()]

def carried(parent: str, head: str, root: Path) -> list[str]:
    """The tasks the commits after PARENT up to HEAD cite, oldest first, each once: what a fold of them keeps."""
    if parent == head:
        return []
    listed = plumb(['log', '--reverse', f'--format=%(trailers:key={TRAILER},valueonly)', f'{parent}..{head}'], root)
    return list(dict.fromkeys((line.strip() for line in listed.splitlines() if line.strip())))

def not_found(task_ids: list[str], root: Path) -> list[str]:
    """For each of TASK_IDS that `memar git show-task-records` cannot find in ROOT's project, what it said."""
    env = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1')
    said: list[str] = []
    for task_id in task_ids:
        shown = subprocess.run([sys.executable, str(ROUTER), 'git', 'show-task-records', '--task-id', task_id, '--list', ProjectPath.FLAG, str(root)], capture_output=True, text=True, encoding='utf-8', errors='replace', env=env)
        if shown.returncode != 0:
            said.append((shown.stderr.strip() or shown.stdout.strip() or f'no task {task_id}').removeprefix('error: '))
    return said

def checked(message: str, given: list[str], no_task: bool, parent: str, head: str, root: Path) -> list[str]:
    """The tasks the commit cites, in order: those the commits it folds cite, then GIVEN; refused, naming the form, when there are none and NO_TASK is not said."""
    if no_task and given:
        sys.exit(f'error: {NO_TASK_FLAG} says the commit carries out no task, and {TASK_FLAG} names one; give one of the two. Nothing was committed.')
    by_hand = cited_by_hand(message, root)
    if by_hand:
        sys.exit(f"error: the message names {', '.join(by_hand)} in a `{TRAILER}:` trailer of its own; take it out and pass {TASK_FLAG} ID instead, so the id is checked and the trailer written. Nothing was committed.")
    missing = not_found(list(dict.fromkeys(given)), root)
    if missing:
        sys.exit("error: a task cited is not one Memar knows, in its folder or on the project's records branch: " + '; '.join(missing) + f'. Check the id with `memar git show-task-records --task-id ID {ProjectPath.FLAG} {root}`. Nothing was committed.')
    tasks = list(dict.fromkeys([*carried(parent, head, root), *given]))
    if not tasks and (not no_task):
        sys.exit(f'error: a commit names the tasks it carries out. Pass {TASK_FLAG} ID once for each, and a `{TRAILER}: ID` trailer is written for each into the message; a commit that carries out no task (a task that opened none: committing, staging, a rename, one edit) says so with {NO_TASK_FLAG}. Nothing was committed.')
    return tasks

def with_trailers(message: str, tasks: list[str], root: Path) -> str:
    """MESSAGE with one `Task:` trailer for each of TASKS, in its own trailer block."""
    if not tasks:
        return message
    trailers = [argument for task_id in tasks for argument in ('--trailer', f'{TRAILER}: {task_id}')]
    return plumb(['interpret-trailers', '--where', 'end', '--if-exists', 'addIfDifferent', '--if-missing', 'add', *trailers], root, data=(message + '\n').encode('utf-8'))
