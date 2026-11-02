#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import os
import subprocess
import sys
from pathlib import Path
from modules.computer.software.primitive.project_path import ProjectPath
from ..errors.errors import ServerUnreachable, TaskByHand, TaskNotCited, TaskUnknown
from ._run import plumb
TRAILER = 'Task'
NO_TASK_FLAG = '--no-task'
TASK_FLAG = '--task-id'
ROUTER = Path(__file__).resolve().parents[2] / 'memar' / 'memar'
SERVER_SECONDS = 120

def server(arguments: list[str]) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1')
    return subprocess.run([sys.executable, str(ROUTER), *arguments], capture_output=True, text=True, encoding='utf-8', errors='replace', env=env, timeout=SERVER_SECONDS)

def cited_by_hand(message: str, root: Path) -> list[str]:
    parsed = plumb(['interpret-trailers', '--parse', '--no-divider'], root, data=message.encode('utf-8'))
    return [value.strip() for key, _, value in (line.partition(':') for line in parsed.splitlines()) if key.strip().lower() == TRAILER.lower()]

def carried(parent: str, head: str, root: Path) -> list[str]:
    if parent == head:
        return []
    listed = plumb(['log', '--reverse', f'--format=%(trailers:key={TRAILER},valueonly)', f'{parent}..{head}'], root)
    return list(dict.fromkeys((line.strip() for line in listed.splitlines() if line.strip())))

def not_found(task_ids: list[str], root: Path) -> list[str]:
    said: list[str] = []
    for task_id in task_ids:
        try:
            shown = server(['git', 'show-task-records', '--task-id', task_id, '--list', ProjectPath.FLAG, str(root)])
        except (OSError, subprocess.TimeoutExpired) as unreachable:
            raise ServerUnreachable(f'the Memar server could not be asked about the task {task_id}: {unreachable}') from None
        if shown.returncode != 0:
            said.append((shown.stderr.strip() or shown.stdout.strip() or f'no task {task_id}').removeprefix('error: '))
    return said

def checked(message: str, given: list[str], no_task: bool, parent: str, head: str, root: Path) -> list[str]:
    if no_task and given:
        raise TaskNotCited(f'{NO_TASK_FLAG} says the commit carries out no task, and {TASK_FLAG} names one; give one of the two. Nothing was committed.')
    by_hand = cited_by_hand(message, root)
    if by_hand:
        raise TaskByHand(f"the message names {', '.join(by_hand)} in a `{TRAILER}:` trailer of its own; take it out and pass {TASK_FLAG} ID instead, so the id is checked and the trailer written. Nothing was committed.")
    missing = not_found(list(dict.fromkeys(given)), root)
    if missing:
        raise TaskUnknown("a task cited is not one Memar knows, in its folder or on the project's records branch: " + '; '.join(missing) + f'. Check the id with `memar git show-task-records --task-id ID {ProjectPath.FLAG} {root}`. Nothing was committed.')
    tasks = list(dict.fromkeys([*carried(parent, head, root), *given]))
    if not tasks and (not no_task):
        raise TaskNotCited(f'a commit names the tasks it carries out. Pass {TASK_FLAG} ID once for each, and a `{TRAILER}: ID` trailer is written for each into the message; a commit that carries out no task (a task that opened none: committing, staging, a rename, one edit) says so with {NO_TASK_FLAG}. Nothing was committed.')
    return tasks

def with_trailers(message: str, tasks: list[str], root: Path) -> str:
    if not tasks:
        return message
    trailers = [argument for task_id in tasks for argument in ('--trailer', f'{TRAILER}: {task_id}')]
    return plumb(['interpret-trailers', '--where', 'end', '--if-exists', 'addIfDifferent', '--if-missing', 'add', *trailers], root, data=(message + '\n').encode('utf-8'))
