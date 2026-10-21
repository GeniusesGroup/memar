#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/management/task/services/depends_on.py — the verb `memar task depends-on`: a session's dependencies shown, added and dropped.

What a dependency is and when it is met is `modules/management/task/services/dependency.py`'s; the
key is written by `session_plan_depends`; what it does to a session's Status
is `session_depends`'s. This file is the verb's face over them: it checks what
is added, writes the key, brings the Status up to date and says what is.
"""
from __future__ import annotations
import argparse
from typing import Callable
from machine.console import fail, note
from modules.management.task.services.dependency import DEPENDS_FOR, DependsOn, Reader, Ref, refused_for_writing
from modules.management.task.services.depends import DEPENDS_COMMAND, concerns_for, home_of, notes_for, problems, reconcile
from modules.management.task.services.list import find_sessions
from modules.management.task.services.folder import folder_of, is_task_folder, read_session
from modules.knowledge.documentation.plan.services.plan import PLAN_NAME
from modules.knowledge.documentation.plan.services.depends import set_depends_on
from modules.knowledge.documentation.plan.primitive.plan_key import PlanKey
from modules.knowledge.documentation.primitive.status import Status

def change(task_id: str, add: list[str], drop: list[str]) -> None:
    """`depends-on`: add and drop references in TASK_ID's key, checked, then bring its Status up to date and say what is."""
    folder = folder_of(task_id)
    plan = folder / PLAN_NAME
    if not is_task_folder(folder) or not plan.is_file():
        fail(f'no session {task_id} with a {PLAN_NAME}, so there is no {PlanKey.DEPENDS_ON.written} to set')
    session = read_session(folder)
    was = DependsOn.of(session.front)
    reader = Reader(home_of(session))
    if add or drop:
        dropped = [Ref.parse(word) for word in drop]
        missing = [str(ref) for ref in dropped if ref not in was]
        if missing:
            fail(f"{', '.join(missing)} is not in {task_id}'s {PlanKey.DEPENDS_ON.written} ({was.text() or 'none'}), so it is not dropped")
        added = DependsOn.normalized((Ref.parse(word) for word in add))
        now = DependsOn.normalized([*(ref for ref in was if ref not in dropped), *added])
        refused_for_writing(task_id, now, reader, added)
        set_depends_on(plan, now)
        session = read_session(folder)
        reconcile(session, reader)
        session = read_session(folder)
        print(f"{task_id}  {PlanKey.DEPENDS_ON.written}: {now.text() or '(none)'}, was {was.text() or '(none)'}")
    else:
        print(f"{task_id}  {PlanKey.DEPENDS_ON.written}: {was.text() or '(none)'}")
        reconcile(session, reader)
        session = read_session(folder)
    note(f'status: {session.status}')
    for line in notes_for(session, reader, find_sessions(project=home_of(session))):
        note(line)
    for line in concerns_for(session, reader):
        note(f'concerns: {line}')
    if session.status == Status.ACTIVE.key and problems(session, reader):
        note('it is Active, so its Status is not changed; set it Blocked if it cannot go on until they are Complete')

def describe(verbs) -> Callable[[argparse.Namespace], None]:
    """`memar task depends-on`."""
    key = PlanKey.DEPENDS_ON.written
    changer = verbs.add_parser(DEPENDS_COMMAND, help='show, add or drop the sessions a session cannot start without', description=f"A session's {key} names the sessions that must be Complete (their plan and their report both)\nbefore it can start: it cannot be claimed or started until they are, and while one is not, its\nStatus is Blocked, with the unmet ids as the reason. Each is an id, or project/id for a session\nof another project, the project resolved as `memar project find` resolves a name. Without --add\nand --drop this shows the key, where each stands, and the sessions that depend on this one\n({DEPENDS_FOR}, derived, never written). --add is refused for the session itself, an id or a\nproject that does not resolve, and a cycle of any length; --drop is how a dependency that no\nlonger exists is removed. A queued session with an unmet dependency becomes Blocked; one whose\ndependencies are all met after Memar blocked it becomes queued again; an Active session is\nnot changed. Why a session waits goes in its plan's Next, and whoever makes its own session\nwait tells the owner at once that the work waits. Anyone may change it. ({key} means\nwhat the documents' Depends_on means, stronger in time: it cannot start until the cited session is Complete.)")
    changer.add_argument('task_id', metavar='ID', help='the session whose dependencies to show or change')
    changer.add_argument('--add', action='append', default=[], metavar='REF', help='a session to depend on, ID or project/ID; may be repeated')
    changer.add_argument('--drop', action='append', default=[], metavar='REF', help='a dependency to remove, as it is written in the key; may be repeated')
    return run

def run(args: argparse.Namespace) -> None:
    change(args.task_id, args.add, args.drop)
