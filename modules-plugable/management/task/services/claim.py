#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/management/task/services/claim.py — a queued task made one agent's, by its id.

Why a claim. A conversation queues tasks instead of working them in its own
context (`queued`: planned, owned by no one), and an agent later takes some of
them and hands each to a fresh sub-agent of its own. Two agents taking at once
— two conversations, a scheduled one over a manual one — must not both take
one task, which would write one folder twice. So a task is taken by
creating a file in its folder with exclusive create, which the filesystem
grants to exactly one caller; only the winner then moves the plan's status
from queued to active.

Why the claim's mechanics are here. Taking the N first in line
(`task_claims`) is this same act — the exclusive create, the status moved —
tried on several tasks in turn, so it takes each through `try_claim` here,
which says why a task was not taken instead of failing; one place takes a
task, not two that could take it two ways.

What a claim is, and why it lapses, is the type's (`modules-plugable/management/task/primitive/claim.py`). A claim
still unfinished past its life is taken as a dead agent's: a later claim takes it
over. A takeover is itself taken by exclusive create, and held from before the
stale claim is dropped until the new claim exists, so two takers racing over one
stale claim still yield one winner (`_take_over`).

The claim file is the claiming agent's, not the task's: it says who took the
task and when. It stays when the task ends; once the plan is complete or
blocked the claim decides nothing, since only a queued task is claimed, and
a task left active by a sub-agent that ran out is either handed again by the
agent holding it or, once the claim has lapsed, queued again
(`new --task-id ID --queued`).
"""
from __future__ import annotations
from modules.identity.thing.labels.Queued import Label_Queued
from modules.identity.thing.labels.Active import Label_Active
from importlib import import_module
import argparse
import os
import socket
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable
from machine.console import fail, note
_m_claim = import_module('modules-plugable.management.task.primitive.claim')
Claim = _m_claim.Claim
_m_folder = import_module('modules-plugable.management.task.services.folder')
folder_of = _m_folder.folder_of
is_task_folder = _m_folder.is_task_folder
_m_temp = import_module('modules-plugable.management.task.services.temp')
TEMP_SENTENCE = _m_temp.TEMP_SENTENCE
_m_plan_file = import_module('modules-plugable.management.task.services.plan_file')
PLAN_NAME = _m_plan_file.PLAN_NAME
plan_file_problem = _m_plan_file.plan_file_problem
read_plan = _m_plan_file.read_plan
_m_task_files = import_module('modules-plugable.management.task.services.task_memory')
stores_at = _m_task_files.stores_at
has_plan = _m_task_files.has_plan
_m_plan_status = import_module('modules-plugable.management.task.services.plan_status')
set_status = _m_plan_status.set_status
_m_depends = import_module('modules-plugable.management.task.services.depends')
dependency_refusal = _m_depends.refusal
_m_task_id = import_module('modules-plugable.management.task.primitive.task_id')
TaskId = _m_task_id.TaskId
CLAIM_COMMAND = 'claim'

def _id(task) -> str:
    return task if isinstance(task, str) else Path(task).name

def claim_path(task) -> Path:
    return Claim.of(task).path

def is_claimed(task) -> bool:
    """Whether TASK (id or Path handle) holds a claim that has not gone stale."""
    return Claim.of(task).is_fresh()

def _create_claim(task) -> str | None:
    """Create TASK's claim by exclusive create; None when this caller made it, else why not."""
    tid = _id(task)
    claim = claim_path(tid)
    stamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    try:
        with claim.open('x', encoding='utf-8', newline='\n') as written:
            written.write(Claim.body(stamp, socket.gethostname(), os.getpid()))
    except FileExistsError:
        return f'task {tid} is claimed by another agent; its claim is in {claim}'
    return None

def _take_over(task) -> str | None:
    """Replace TASK's stale claim with this caller's, holding the takeover until it exists; None when done, else why not.

    Two takers racing over one stale claim must not both win. Dropping the
    stale claim and creating the new one are therefore one act under one
    takeover, itself taken by exclusive create: its holder checks again that
    the claim is stale, drops it, and lets go only once its own claim exists.
    A taker that read the claim as stale a moment ago, and comes to the
    takeover after, finds the new claim fresh and drops nothing; while the
    takeover is held, nothing else can make a claim either, since the stale one
    is still there or the holder's is. A takeover left behind by a caller that
    died mid-way lapses like a claim.
    """
    tid = _id(task)
    takeover = Claim.of(tid).takeover_path
    try:
        if time.time() - takeover.stat().st_mtime >= Claim.STALE_SECONDS:
            takeover.unlink()
    except OSError:
        pass
    try:
        takeover.open('x').close()
    except FileExistsError:
        return f'task {tid} is being taken over by another agent'
    try:
        if is_claimed(tid):
            return f'task {tid} is claimed by another agent; its claim is in {claim_path(tid)}'
        try:
            claim_path(tid).unlink()
        except FileNotFoundError:
            pass
        return _create_claim(tid)
    finally:
        takeover.unlink()

def try_claim(task) -> str | None:
    """Make TASK this caller's: queued (or active under a stale claim) becomes active, claimed; None when it did, else why not.

    TASK is a task id string, or a transitional Path handle. Not taken when
    there is no plan, when the plan is neither queued nor active under a stale
    claim, or when another caller holds a claim that has not gone stale —
    including one that won a race a moment ago. Saying why rather than failing
    lets `claims`, trying several tasks in turn, pass over one it did not get
    and say nothing for it.

    A task whose `Depends_on` names one that is not Complete is not taken
    whatever its Status, and the refusal names the unmet ones; one Memar
    blocked for them that are all met since is queued again first, so it is
    taken as an ordinary queued task (`task_depends`).
    """
    tid = _id(task)
    if not has_plan(tid):
        return f'task {tid} has no plan, so there is no task to claim'
    held_task = import_module('modules-plugable.management.task.services.folder').read_task(tid)
    if held_task.shape:
        return f'task {tid}: {held_task.shape}'
    unmet = dependency_refusal(tid, CLAIM_COMMAND)
    if unmet:
        return unmet
    status = held_task.status
    claim = claim_path(tid)
    held = claim.exists()
    if held and is_claimed(tid):
        return f'task {tid} is claimed by another agent; its claim is in {claim}'
    if status != Label_Queued.key and (not (status == Label_Active.key and held)):
        return f"task {tid} is not queued (its status is {status or 'none'}), so it is not free to claim"
    why = _take_over(tid) if held else _create_claim(tid)
    if why:
        return why
    try:
        set_status(stores_at(tid), None, tid, Label_Active.key, only_from=(Label_Queued.key, Label_Active.key))
    except SystemExit as refused:
        claim.unlink(missing_ok=True)
        return str(refused.code).removeprefix('error: ')
    return None

def claim_folder(task) -> None:
    """Make TASK this caller's, as `try_claim` does; refused, with why, when it is not taken."""
    why = try_claim(task)
    if why:
        fail(why)

def claim(task_id: str) -> None:
    """`claim`: claim TASK_ID's task and say so."""
    if not is_task_folder(task_id):
        fail(f'no task folder {task_id}')
    claim_folder(task_id)
    print(f'claimed {task_id}')
    note(f'claim: {claim_path(task_id)}')
    note(TEMP_SENTENCE)

def describe(verbs) -> Callable[[argparse.Namespace], None]:
    """`memar task claim`."""
    claimer = verbs.add_parser(CLAIM_COMMAND, help='take one queued task by its id, so no other agent takes it', description=f"Take the queued task ID for yourself: its status becomes active and a\nclaim is left in its folder, saying who took the task. A task that is\nnot queued, or that another agent holds, is refused. Nothing keeps a\nclaim fresh, so a claim older than {Claim.stale_hours()} hours is a dead agent's, and is\ntaken over: the task can then be taken again or queued again. Use it\nto take one named task; `claims N` takes the N first in line instead.")
    TaskId.add_positional(claimer, 'the queued task to claim')
    return run

def run(args: argparse.Namespace) -> None:
    claim(args.task_id)
