#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
import os
import re
import shlex
import subprocess
import sys
import time
from pathlib import Path
from typing import Callable, NoReturn, TypeVar
from ..errors.errors import Locked
from . import _run as git_run
from ._run import plumb, run_captured, stderr_of
LOCK_NOTE = 'When another git process — often your editor, refreshing its status — holds a\nlock this command needs, it says so and how long it will wait for it. If it\nstill cannot finish, it stops and says what stage it reached, what git said, how\nold the lock is, and the exact command that finishes or undoes what was done. Do\nwhat that message says; never delete a lock file to get past one.'
LOCK_WAIT_SECONDS = 20
LOCK_FIRST_PAUSE_SECONDS = 0.1
LOCK_LONGEST_PAUSE_SECONDS = 2.0
LOCK_STALE_SECONDS = 60
LOCK_HELD = re.compile("Unable to create '([^']+?\\.lock)': File exists")
ROUTER = Path(__file__).resolve().parents[2] / 'memar' / 'memar'
Waited = TypeVar('Waited')

def lock_deadline() -> float:
    return time.monotonic() + LOCK_WAIT_SECONDS

def _waited(attempt: Callable[[], tuple[Waited, Path | None]], before: str, deadline: float) -> tuple[Waited, Path | None]:
    pause, named = (LOCK_FIRST_PAUSE_SECONDS, set())
    while True:
        result, held = attempt()
        left = deadline - time.monotonic()
        if held is None or left <= 0:
            return (result, held)
        if held not in named:
            named.add(held)
            print(f'waiting up to {max(1, round(left))} s more before {before}: {held} is held by another git process', file=sys.stderr)
        time.sleep(min(pause, left))
        pause = min(pause * 2, LOCK_LONGEST_PAUSE_SECONDS)

def locks_free(locks: list[Path], before: str, deadline: float) -> Path | None:
    _, held = _waited(lambda: (None, next((lock for lock in locks if lock.exists()), None)), before, deadline)
    return held

def patiently(args: list[str], root: Path, deadline: float, data: bytes | None=None) -> tuple[subprocess.CompletedProcess[bytes], Path | None]:

    def attempt() -> tuple[subprocess.CompletedProcess[bytes], Path | None]:
        completed = git_run.attempt(args, root, data=data)
        found = LOCK_HELD.search(stderr_of(completed)) if completed.returncode else None
        return (completed, Path(found.group(1)) if found else None)
    return _waited(attempt, f'git {args[0]}', deadline)

def shared_locks(root: Path) -> list[Path]:
    names = ['index', 'HEAD']
    branch = run_captured(['symbolic-ref', '-q', 'HEAD'], cwd=root).stdout.strip()
    if branch:
        names.append(branch)
    listed = plumb(['rev-parse', *(word for name in names for word in ('--git-path', name))], root)
    return [root / f'{line}.lock' for line in listed.splitlines()]
COUNT_INCLUDES = 'counting launcher shims and background daemons such as fsmonitor, so it may never reach 0' if os.name == 'nt' else 'not counting fsmonitor daemons'

def _git_processes() -> int | None:
    if os.name == 'nt':
        command = ['tasklist', '/FI', 'IMAGENAME eq git.exe', '/FO', 'CSV', '/NH']
        counts = lambda line: line.lower().startswith('"git.exe"')
    else:
        command = ['ps', '-A', '-o', 'args=']
        counts = lambda line: Path((line.split() or [''])[0]).name == 'git' and 'fsmonitor--daemon' not in line
    try:
        listed = subprocess.run(command, capture_output=True, text=True, errors='replace', timeout=10)
    except (OSError, subprocess.SubprocessError):
        return None
    if listed.returncode != 0:
        return None
    return sum((1 for line in listed.stdout.splitlines() if counts(line)))

def _lock_account(lock: Path) -> str:
    try:
        age = time.time() - lock.stat().st_mtime
    except OSError:
        return f'The lock {lock} is gone now: its holder let go after the wait ran out.'
    running = _git_processes()
    if running is None:
        seen = 'whether a git process is running could not be asked'
    else:
        seen = f'{running} git process(es) are running on this machine ({COUNT_INCLUDES})'
    if age < LOCK_STALE_SECONDS:
        verdict = 'a lock this young most likely belongs to a live git process — an editor refreshing its status, or another task — which lets go on its own'
    elif running == 0:
        verdict = 'a lock this old with no git process running was most likely left by one that crashed; a person may delete it once sure of that — this script never does'
    else:
        verdict = 'a lock this old is either a long git operation or one left by a crash; only once no git process is working on this repository may a person delete it — this script never does'
    return f'The lock {lock} was last written {age:.0f} s ago and {seen}: {verdict}.'

def stopped(stage: str, then: str, completed: subprocess.CompletedProcess[bytes] | None=None, lock: Path | None=None) -> NoReturn:
    said = [stage]
    if completed is not None:
        command = ' '.join((str(word) for word in completed.args[3:]))
        said.append(f'`git {command}` exited {completed.returncode}; git said:')
        said.extend((f'    {line}' for line in (stderr_of(completed) or '(nothing)').splitlines()))
    if lock is not None:
        said.append(_lock_account(lock))
    said.append(then)
    raise Locked('\n'.join(said))

def once(lock: Path | None) -> str:
    return 'once the lock is free' if lock is not None else 'once what git said above is dealt with'

def this_command(*arguments: str) -> str:
    words = [str(ROUTER), 'git', *arguments]
    if os.name == 'nt':
        return 'python ' + subprocess.list2cmdline(words)
    return shlex.join([sys.executable, *words])
