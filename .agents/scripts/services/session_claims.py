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

Why the first task's topic pulls the batch. An agent given several tasks of one
subject keeps its context on that subject, so the batch is one subject when the
queue allows (the owner's ruling of 2026-10-13, which accepts that strict
priority is disturbed for it). The first task is the first in line, as ever,
and is never displaced; its `topic` (`session_plan`) is the batch's, and the
rest of the N are that topic's queued tasks in line order. Other tasks do not
fill the remainder, since the owner's reason, focus, argues against it, unless
the caller passes `fill`, which takes the next in line once the topic is used
up. `topic` names the topic in place of the first task's, for a caller whose
context is already about it. A first task with no topic leaves the line as it
was. An unrelated task is overtaken only by the batch of one call: the next
call starts again from the first in line, so a high-priority task is never
passed, being always the first of its call; and what a batch passed over is
printed, so the displacement is seen. No counter of displacements is kept; the
owner can ask for one if displacement is seen in use.

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
from services.status import Status
from services.session_brief import brief_text
from services.session_claim import CLAIM_COMMAND, try_claim
from services.project_find import add_project_flags, project_from_args
from services.session_digest import DIGEST_COMMAND
from services.session_find import LIST_COMMAND, find_sessions, project_of
from services.session_folder import Session
from services.session_plan import PLAN_NAME, checked_topic, part_text, priority_of, topic_of
from services.session_record import REPORT
from services.session_report import REPORT_NAME

CLAIMS_COMMAND = "claims"


PROJECT_REQUIRED = (
    f"{CLAIMS_COMMAND} needs --project NAME or --project-path PATH: one run serves one project, and naming it "
    "keeps the work from landing in a project no one chose; if you do not know which "
    "project the tasks are for, ask the owner"
)


def in_line(project: str) -> list[Session]:
    """The queued sessions of PROJECT in the order `claims` takes them: highest priority, then oldest opened, then id.

    That project's wherever they lie, as `list --project` finds them
    (`session_find`); PROJECT is a name or a folder, and an empty one is refused.
    """
    queued = find_sessions(status=Status.QUEUED.key, project=project_of(project))
    return sorted(
        queued,
        key=lambda session: (-priority_of(session.front), (session.front or {}).get("opened", ""), session.id),
    )


def take(count: int, project: str, topic: str | None = None, fill: bool = False) -> list[Session]:
    """Claim up to COUNT queued sessions of PROJECT in line order, by topic; the ones taken.

    TOPIC, when named, is the batch's topic from the start. Otherwise the first
    session taken sets it: when it has one, only that topic's sessions are
    taken after it; with none, the line is followed as it is. With FILL, the
    sessions not of the topic are taken once its own are used up. A session
    passed over as not ready or not taken is said once.
    """
    taken: list[Session] = []
    tried: set[str] = set()
    batch: str | None = checked_topic(topic) if topic is not None else None

    def attempt(session: Session) -> None:
        tried.add(session.id)
        if not part_text(session.path / PLAN_NAME, "Request"):
            print(f"{session.id}  not ready: its Request is empty")
            return
        why = try_claim(session.path)
        if why:
            # Most often another caller won it between the listing and the claim.
            print(f"{session.id}  not taken: {why}")
            return
        taken.append(session)

    line = in_line(project)
    for session in line:
        if len(taken) >= count:
            break
        if batch and topic_of(session.front) != batch:
            continue
        attempt(session)
        if batch is None and taken:
            # The first one taken sets the batch; "" is a first with no topic, and the line goes on as it is.
            batch = topic_of(taken[0].front)
    if fill:
        for session in line:
            if len(taken) >= count:
                break
            if session.id not in tried:
                attempt(session)
    return taken


def batch_report(taken: list[Session], count: int, project: str, topic: str | None) -> list[str]:
    """The lines saying the batch's topic, what waits under it, and what it passed over; none when the batch has no topic."""
    batch = checked_topic(topic) if topic else topic_of(taken[0].front)
    if not batch:
        return []
    own = sum(1 for session in taken if topic_of(session.front) == batch)
    waiting = [session for session in in_line(project) if part_text(session.path / PLAN_NAME, "Request")]
    under = sum(1 for session in waiting if topic_of(session.front) == batch)
    said = f"batch topic: {batch} ({own} of {count} asked"
    if own < len(taken):
        said += f"; {len(taken) - own} more filled from other topics"
    if under:
        said += f"; {under} more queued under it are not taken only because N was reached"
    lines = [said + ")"]
    lowest = min(priority_of(session.front) for session in taken)
    passed = [
        session for session in waiting
        if topic_of(session.front) != batch and priority_of(session.front) > lowest
    ]
    if passed:
        listed = ", ".join(f"{session.id} (priority {priority_of(session.front)})" for session in passed)
        lines.append(f"passed over for topic: {listed}")
    return lines


def claims(count: int, project: str | None, topic: str | None = None, fill: bool = False) -> list[str]:
    """`claims`: claim the COUNT queued sessions of PROJECT first in line, and print what hands each over; their ids.

    PROJECT None — no project named — is refused (`PROJECT_REQUIRED`). The
    batch follows the first task's topic, or TOPIC when named; FILL takes the
    next in line once that topic is used up (`take`).
    """
    if project is None:
        fail(PROJECT_REQUIRED)
    if count < 1:
        fail(f"{CLAIMS_COMMAND} N counts the sessions to take; N is at least 1")
    taken = take(count, project, topic, fill)
    if not taken:
        note("no queued session to claim" + (f" under topic {checked_topic(topic)}" if topic else ""))
        return []
    print(f"claimed {len(taken)} of {count}")
    for line in batch_report(taken, count, project, topic):
        print(line)
    for session in taken:
        print()
        print(f"{session.id}  {(session.front or {}).get('title', '')}")
        note(f"priority: {priority_of(session.front)}")
        if topic_of(session.front):
            note(f"topic: {topic_of(session.front)}")
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
            "`claim` does. The first is the first in line; when it has a topic\n"
            "(`memar session topic`), the rest are that topic's queued sessions in\n"
            "line order, so one agent works one subject, even where that takes\n"
            "lower-priority sessions ahead of unrelated ones that rank above them.\n"
            "Other sessions do not fill what is left, unless --fill. --topic T names\n"
            "the topic instead of the first session's. A first session with no topic\n"
            "keeps the plain line. The output states the batch topic and lists the\n"
            "higher-priority sessions passed over. For each session taken it prints\n"
            "its id and title, its priority and topic, its plan, and the brief to\n"
            "hand one fresh sub-agent per batch of one topic. N is\n"
            "yours to choose, from what you were asked: there is no default and no\n"
            "cap. Fewer queued than N is not an error: you get what there is. A\n"
            "queued plan whose Request is empty is not ready and is passed over,\n"
            "and so, saying why, is one another agent took meanwhile.\n"
            "--project NAME or --project-path PATH is required: one run serves one project, so it takes only\n"
            "that project's queued sessions, wherever they lie, and never mixes two\n"
            "projects'; there is no default project and no way to take from all.\n"
            "\"Do 5 tasks of X\" means `claims 5 --project X` (or `--project-path` with its folder); if you do not know\n"
            "which project the tasks are for, ask the owner rather than guess.\n"
            "Two agents asking at once never get the same session.\n"
            "\n"
            "When you are asked to do some of the queued tasks — \"do some of the\n"
            "queued tasks\", \"do 5 tasks of project X\" — work them this way, as the\n"
            "coordinator:\n"
            "\n"
            f"  1. `memar session {LIST_COMMAND} --status queued` shows what waits, each with\n"
            "     its priority; add --project NAME (or --project-path PATH) for one\n"
            "     project's.\n"
            "  2. `claims N --project X` takes them and prints a brief for each;\n"
            f"     `memar session {CLAIM_COMMAND} ID` takes one named task instead.\n"
            "  3. Hand the batch of one topic to one fresh sub-agent, as your runtime\n"
            f"     starts one, each session keeping its own {PLAN_NAME} and {REPORT_NAME} and\n"
            "     the sub-agent working them one after another; a batch of another\n"
            "     topic goes to another sub-agent: never in your own context, and\n"
            "     never one sub-agent for sessions of different topics. Memar starts\n"
            "     no agent: you do.\n"
            f"  4. When each ends, read its {REPORT_NAME}: its Status and its\n"
            f"     {REPORT.hand_back_part}. Its Status must equal its plan's: a sub-agent that\n"
            "     could only return text hands back the report, and you write it as\n"
            f"     its {REPORT_NAME} and set its Status. A report with no Status, more\n"
            "     lines than allowed, or a Status that disagrees with its plan, is a\n"
            "     failed hand-back: say so, and do not count that task done.\n"
            f"  5. Last, run `memar session {DIGEST_COMMAND} --conversation ID`, ID your own\n"
            "     session's, and give the owner that one digest rather than a\n"
            "     question per task."
        ),
    )
    taker.add_argument("count", type=int, metavar="N", help="how many queued sessions to take, at least 1")
    add_project_flags(taker, "the project whose queued sessions to take, as `list` finds them", required=True)
    taker.add_argument(
        "--topic",
        default=None,
        metavar="T",
        help="take the queued sessions of topic T instead of those of the first session's topic",
    )
    taker.add_argument(
        "--fill",
        action="store_true",
        help="when the topic's sessions are used up before N, take the next in line, whatever its topic",
    )
    return run


def run(args: argparse.Namespace) -> None:
    if args.topic is not None or args.fill:
        claims(args.count, project_from_args(args), args.topic, args.fill)
    else:
        claims(args.count, project_from_args(args))
