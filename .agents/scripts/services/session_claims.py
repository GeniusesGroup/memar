#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/session_claims.py — the N queued sessions first in line, made one agent's.

Why through `try_claim`. Taking the N first in line is the act `claim`
does — the exclusive create, the status moved — tried on several sessions in
turn, so each is taken by `session_claim.try_claim` and by nothing here: one
place takes a session, not two that could take it two ways. `claims` tries the
queued sessions in line order and skips any another caller won meanwhile, so
two callers asking at once each get sessions, never the same one.

Why that line. The plan's priority first, the higher sooner (`session_plan`),
then the oldest opened, so among equals what has waited longest goes first;
the id breaks a tie in time. A queued plan whose Request is still empty has
not been written yet — its session was opened queued before its task was —
and is passed over until it is. N is the caller's: the owner says how much
work a night holds ("do five tonight"), the agent passes 5, and nothing here
defaults or caps it, since a cap here would be a policy no one chose.

Why Memar starts no agent. How an agent runtime starts a sub-agent is the
runtime's, known to the agent already in a conversation and to nothing else;
so `claims` prints, for each session it took, the brief that hands it over
(`session_brief`), and the agent that called it delegates each one the way its
runtime does.

Why the project is named, never defaulted. One run of `claims` serves one
project: the sessions it takes become one coordinator's work, landing in that
project. A default — Memar's own folder, every project's, or the current
folder's guessed — would hide which project the work lands in, and taking from
two projects at once would mix their work in one run. So the caller names the
project with `--project`, and `claims` refuses without it; an agent that does
not know the project asks the owner rather than guessing.
"""
from __future__ import annotations

import argparse
from typing import Callable

from machine.console import fail, note
from services.session_brief import brief_text
from services.session_claim import try_claim
from services.session_find import find_sessions, project_of
from services.session_folder import Session
from services.session_plan import PLAN_NAME, QUEUED_STATUS, part_text, priority_of

CLAIMS_COMMAND = "claims"


PROJECT_REQUIRED = (
    f"{CLAIMS_COMMAND} needs --project PATH: one run serves one project, and naming it "
    "keeps the work from landing in a project no one chose; if you do not know which "
    "project the tasks are for, ask the owner"
)


def in_line(project: str) -> list[Session]:
    """The queued sessions of PROJECT in the order `claims` takes them: highest priority, then oldest opened, then id.

    That project's wherever they lie, as `list --project` finds them
    (`session_find`); the current folder's when PROJECT is empty.
    """
    queued = find_sessions(status=QUEUED_STATUS, project=project_of(project))
    return sorted(
        queued,
        key=lambda session: (-priority_of(session.front), (session.front or {}).get("opened", ""), session.id),
    )


def take(count: int, project: str) -> list[Session]:
    """Claim up to COUNT queued sessions of PROJECT in line order, saying which are passed over; the ones taken."""
    taken: list[Session] = []
    for session in in_line(project):
        if len(taken) >= count:
            break
        if not part_text(session.path / PLAN_NAME, "Request"):
            print(f"{session.id}  not ready: its Request is empty")
            continue
        why = try_claim(session.path)
        if why:
            # Most often another caller won it between the listing and the claim.
            print(f"{session.id}  not taken: {why}")
            continue
        taken.append(session)
    return taken


def claims(count: int, project: str | None) -> list[str]:
    """`claims`: claim the COUNT queued sessions of PROJECT first in line, and print what hands each over; their ids.

    PROJECT None — no project named — is refused (`PROJECT_REQUIRED`).
    """
    if project is None:
        fail(PROJECT_REQUIRED)
    if count < 1:
        fail(f"{CLAIMS_COMMAND} N counts the sessions to take; N is at least 1")
    taken = take(count, project)
    if not taken:
        note("no queued session to claim")
        return []
    print(f"claimed {len(taken)} of {count}")
    for session in taken:
        print()
        print(f"{session.id}  {(session.front or {}).get('title', '')}")
        note(f"priority: {priority_of(session.front)}")
        note(f"plan: {session.path / PLAN_NAME}")
        note(f"brief: {brief_text(session.id)}")
    return [session.id for session in taken]


def describe(verbs) -> Callable[[argparse.Namespace], None]:
    """`memar session claims`."""
    taker = verbs.add_parser(
        CLAIMS_COMMAND,
        help="take the N queued sessions first in line, and print the brief for each",
        description=(
            "Take the N queued sessions first in line — the highest priority first,\n"
            "the oldest opened first among equals — and claim each for yourself, as\n"
            "`claim` does. For each it prints its id and title, its priority, its\n"
            "plan, and the brief to hand one fresh sub-agent per session. N is\n"
            "yours to choose, from what you were asked: there is no default and no\n"
            "cap. Fewer queued than N is not an error: you get what there is. A\n"
            "queued plan whose Request is empty is not ready and is passed over,\n"
            "and so, saying why, is one another agent took meanwhile.\n"
            "--project is required: one run serves one project, so it takes only\n"
            "that project's queued sessions, wherever they lie, and never mixes two\n"
            "projects'; there is no default project and no way to take from all.\n"
            "\"Do 5 tasks of X\" means `claims 5 --project X`; if you do not know\n"
            "which project the tasks are for, ask the owner rather than guess.\n"
            "Two agents asking at once never get the same session. Memar starts no\n"
            "agent: you hand each brief over the way your runtime starts a\n"
            "sub-agent. What to do with each is said in `memar session --help`."
        ),
    )
    taker.add_argument("count", type=int, metavar="N", help="how many queued sessions to take, at least 1")
    taker.add_argument(
        "--project",
        nargs="?",
        const="",
        default=None,
        metavar="PATH",
        help=(
            "required: the project whose queued sessions to take, as `list --project` finds them: "
            "the project PATH is in, or without PATH the current folder's"
        ),
    )
    return run


def run(args: argparse.Namespace) -> None:
    claims(args.count, args.project)
