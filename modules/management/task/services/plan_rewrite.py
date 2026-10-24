#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/management/task/services/plan_rewrite.py — the one way a plan's lines are replaced, and the line helpers every field's writer uses.

Several writers reach one plan — a claim, a priority, a person editing — so a rewrite is never a
read followed blindly by a write that would put back what another changed meanwhile: it is
checked against the plan as it is just before it lands, and lands whole.
"""
from __future__ import annotations
import os
import time
from pathlib import Path
from typing import Callable
from machine.console import fail
from modules.management.task.services.plan_file import REWRITE_ATTEMPTS, REWRITE_PAUSE_SECONDS, plan_shape_problem, read_bytes

def rewrite(path: Path, change: Callable[[list[str]], list[str]]) -> None:
    """Rewrite PATH as CHANGE makes its lines, starting over when another writer changed it meanwhile.

    Each line keeps its newline, so CHANGE keeps every line it does not touch
    as written. The new text is written to a temporary file beside the plan
    and put in its place by `os.replace`, so a reader never sees half a plan;
    just before that, the plan is read again, and when it is no longer what
    CHANGE was given — a claim, a priority, a person's edit landed meanwhile —
    the rewrite starts over from what is there now, so that change is kept
    rather than written over. What is left is the moment between that second
    read and the replace.
    """
    for _ in range(REWRITE_ATTEMPTS):
        data = read_bytes(path)
        lines = data.decode('utf-8-sig').splitlines(keepends=True)
        problem = plan_shape_problem([line.rstrip('\r\n') for line in lines])
        if problem:
            fail(f'{path}: {problem}; nothing was written')
        text = ''.join(change(lines))
        temporary = path.with_name(f'.{path.name}.{os.getpid()}.tmp')
        try:
            with temporary.open('w', encoding='utf-8', newline='') as written:
                written.write(text)
            if read_bytes(path) == data:
                os.replace(temporary, path)
                return
        except PermissionError:
            time.sleep(REWRITE_PAUSE_SECONDS)
        finally:
            temporary.unlink(missing_ok=True)
    fail(f'{path} kept changing while it was being rewritten, so nothing was written; try again')

def key_of(line: str) -> str:
    """The key a front-matter LINE sets, as written; empty when the line sets none."""
    key, colon, _ = line.partition(':')
    return key.strip() if colon else ''

def line_end(line: str) -> str:
    """LINE's line ending, a newline when it has none."""
    return line[len(line.rstrip('\r\n')):] or '\n'
