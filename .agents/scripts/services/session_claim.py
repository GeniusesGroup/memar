#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/session_claim.py — a queued session made one agent's, by its id.

Why a claim. A conversation queues sessions instead of working them in its own
context (`queued`: planned, owned by no one), and an agent later takes some of
them and hands each to a fresh sub-agent of its own. Two agents taking at once
— two conversations, a scheduled one over a manual one — must not both take
one session, which would write one folder twice. So a session is taken by
creating a file in its folder with exclusive create, which the filesystem
grants to exactly one caller; only the winner then moves the plan's status
from queued to active.

Why the claim's mechanics are here. Taking the N first in line
(`session_claims`) is this same act — the exclusive create, the status moved —
tried on several sessions in turn, so it takes each through `try_claim` here,
which says why a session was not taken instead of failing; one place takes a
session, not two that could take it two ways.

Why a claim lapses after a day. Nothing keeps a claim fresh: no process of
Memar's watches the sub-agent, so a claim's age is only the time since it was
taken. A dead agent's claim must still lapse, or its session is held forever;
but the lapse must not take a session from a sub-agent still at work, and one
evening's batch of sessions, handed out one after another, can run through
the night. A day outlasts that batch, and a claim still unfinished a day later
is taken as a dead agent's: a later claim takes it over. A takeover is itself
taken by exclusive create, and held from before the stale claim is dropped
until the new claim exists, so two takers racing over one stale claim still
yield one winner (`_take_over`).

The claim file is the claiming agent's, not the task's: it says who took the
session and when. It stays when the session ends; once the plan is complete or
blocked the claim decides nothing, since only a queued session is claimed, and
a session left active by a sub-agent that ran out is either handed again by the
agent holding it or, once the claim has lapsed, queued again
(`new --session-id ID --queued`).
"""
from __future__ import annotations

import argparse
import os
import socket
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from machine.console import fail, note
from services.status import Status
from services.session_folder import folder_of, is_session_folder
from services.session_temp import TEMP_SENTENCE
from services.session_plan import PLAN_NAME, plan_file_problem, read_plan
from services.session_plan_status import set_status

CLAIM_COMMAND = "claim"
CLAIM_NAME = "claim"
# Held only while a stale claim is replaced (`_take_over`).
CLAIM_TAKEOVER_NAME = f"{CLAIM_NAME}.takeover"
# A claim this old is a dead agent's: nothing refreshes it, so it must outlast
# a night's batch of sub-agents (see the docstring).
CLAIM_STALE_SECONDS = 24 * 60 * 60


def claim_path(folder: Path) -> Path:
    return folder / CLAIM_NAME


def is_claimed(folder: Path) -> bool:
    """Whether FOLDER holds a claim that has not gone stale."""
    try:
        touched = claim_path(folder).stat().st_mtime
    except OSError:
        return False
    return time.time() - touched < CLAIM_STALE_SECONDS


def _create_claim(folder: Path) -> str | None:
    """Create FOLDER's claim by exclusive create; None when this caller made it, else why not."""
    claim = claim_path(folder)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        with claim.open("x", encoding="utf-8", newline="\n") as written:
            written.write(f"claimed: {stamp}\nhost: {socket.gethostname()}\npid: {os.getpid()}\n")
    except FileExistsError:
        return f"session {folder.name} is claimed by another agent; its claim is in {claim}"
    return None


def _take_over(folder: Path) -> str | None:
    """Replace FOLDER's stale claim with this caller's, holding the takeover until it exists; None when done, else why not.

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
    takeover = folder / CLAIM_TAKEOVER_NAME
    try:
        if time.time() - takeover.stat().st_mtime >= CLAIM_STALE_SECONDS:
            takeover.unlink()
    except OSError:
        pass
    try:
        takeover.open("x").close()
    except FileExistsError:
        return f"session {folder.name} is being taken over by another agent"
    try:
        if is_claimed(folder):
            return f"session {folder.name} is claimed by another agent; its claim is in {claim_path(folder)}"
        try:
            claim_path(folder).unlink()
        except FileNotFoundError:
            pass
        return _create_claim(folder)
    finally:
        takeover.unlink()


def try_claim(folder: Path) -> str | None:
    """Make FOLDER's session this caller's: queued (or active under a stale claim) becomes active, claimed; None when it did, else why not.

    Not taken when the folder has no plan, when the plan is neither queued nor
    active under a stale claim, or when another caller holds a claim that has
    not gone stale — including one that won a race a moment ago. Saying why
    rather than failing lets `claims`, trying several sessions in turn, pass
    over one it did not get and say nothing for it.
    """
    plan = folder / PLAN_NAME
    if not plan.is_file():
        return f"{folder} has no {PLAN_NAME}, so there is no task to claim"
    shape = plan_file_problem(plan)
    if shape:
        return f"session {folder.name}: {shape}"
    status = read_plan(plan).status
    claim = claim_path(folder)
    held = claim.exists()
    if held and is_claimed(folder):
        return f"session {folder.name} is claimed by another agent; its claim is in {claim}"
    if status != Status.QUEUED.key and not (status == Status.ACTIVE.key and held):
        return f"session {folder.name} is not queued (its status is {status or 'none'}), so it is not free to claim"
    why = _take_over(folder) if held else _create_claim(folder)
    if why:
        return why
    # The claim is this caller's alone, so the status is moved only from what
    # made it free; a plan someone changed meanwhile is left as they made it,
    # and the claim taken back.
    try:
        set_status(plan, Status.ACTIVE.key, expected=(Status.QUEUED.key, Status.ACTIVE.key))
    except SystemExit as refused:
        claim.unlink(missing_ok=True)
        return str(refused.code).removeprefix("error: ")
    return None


def claim_folder(folder: Path) -> None:
    """Make FOLDER's session this caller's, as `try_claim` does; refused, with why, when it is not taken."""
    why = try_claim(folder)
    if why:
        fail(why)


def claim(session_id: str) -> None:
    """`claim`: claim SESSION_ID's session and say so."""
    folder = folder_of(session_id)
    if not is_session_folder(folder):
        fail(f"no session folder {session_id}")
    claim_folder(folder)
    print(f"claimed {session_id}")
    note(f"claim: {claim_path(folder)}")
    note(TEMP_SENTENCE)


def describe(verbs) -> Callable[[argparse.Namespace], None]:
    """`memar session claim`."""
    claimer = verbs.add_parser(
        CLAIM_COMMAND,
        help="take one queued session by its id, so no other agent takes it",
        description=(
            "Take the queued session ID for yourself: its status becomes active and a\n"
            "claim is left in its folder, saying who took the task. A session that is\n"
            "not queued, or that another agent holds, is refused. Nothing keeps a\n"
            f"claim fresh, so a claim older than {CLAIM_STALE_SECONDS // 3600} hours is a dead agent's, and is\n"
            "taken over: the task can then be taken again or queued again. Use it\n"
            "to take one named task; `claims N` takes the N first in line instead."
        ),
    )
    claimer.add_argument("session_id", metavar="ID", help="the queued session to claim")
    return run


def run(args: argparse.Namespace) -> None:
    claim(args.session_id)
