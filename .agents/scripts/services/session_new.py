#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/session_new.py — one session's scratch folder opened, or taken up again.

Why one folder per session, under ONE root. Parallel agent sessions edit one
shared working tree with no coordination, and concurrent writes to one file
collide silently — shared-tree collisions. The per-file advisory locks in
`machine/fs_lock.py` answer that, and `memar content write` and `edit` take one,
but advisory locks are honored by skill rule and not by the filesystem:
file-write tools bypass them, and only intent notes saying who plans what
against which base let a waiter that takes over a stale lock read what the dead
session meant. Intent notes and locks are scratch, and scratch needs a home that
survives the session: session folders give every session its own folder, and
every session works inside its own folder so nothing lands in git by accident.
That home is under <memar-root>/temp/, the ONE root the root .gitignore already
ignores — OS temp dirs are forbidden, because they are wiped by other apps
while sessions last days (the OS-temp wiped risk). Where exactly is
`machine/fs_memar.py`'s answer, and it fails closed rather than guessing.

A session writes only inside its own folder: --session-id reuses an id only to
continue the same session, and two sessions writing one folder reintroduce the
unattributed mixing this exists to remove. Reading another session's folder is
fine; a session that needs something from an old folder copies it into its own.

One session is one task, so a conversation that asks for several things, or
hands a step to a sub-agent, opens several sessions. Each records the session
it came from as its parent and the first session of the conversation, written
once with its plan: a link read off one file never needs a walk up a chain
whose folders may already be swept. The parent must be a session folder that
is there, because its conversation is read from it. A session opened with a
parent is most often one the parent is handing to a sub-agent, so `new` ends
by printing the text that hands it over (`session_brief`).

A session can be opened, or its written plan left, `--queued`: waiting for an
agent to take it (`session_claim`) and hand it to a fresh sub-agent, rather
than worked by the conversation that opened it. Only an active plan no one has
claimed is queued again, so a session being worked, or one finished, is never
put back in line. `--priority` says where in that line: written into a new
plan, or set on the one that is there (`session_plan`), so queuing and ranking
a task is one command. `--topic` says what the task is about, the same way
(`session_plan`); it is the session's own, never copied from the parent's, since
a copy would hide the decision of what the new task is about. A topic near one
the project already uses is warned about (`session_topic`).

Opening is also when the day's sweep runs (`session_gc`), never touching the
session being opened or continued.

Where a new folder is made is asked of the project the plan names: a project
whose preferences set a session location gets its folders there, every other
one in temp/sessions/ inside itself, and the Memar checkout in its own root
(`session_location`). Each run also ensures the
folder's shape — the plan and the report at its top (`session_plan`,
`session_report`), and a module's role folders for whatever else the task makes
(`module_folders`) — creating only what is missing, so a folder from an
earlier Memar is brought to the same shape as it is continued.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
from textwrap import indent
from typing import Callable

from machine.console import fail, note
from machine.fs_memar import session_dir
from services.status import Status
from services.module_folders import ensure_role_folders
from services.project_find import add_project_flags, project_by_path, project_from_args
from services.project_preferences import PREFERENCES_RELATIVE, SESSIONS_KEY, preferences_path
from services.session_brief import BRIEF_COMMAND, brief_text
from services.session_find import LIST_COMMAND
from services.session_folder import folder_of, project_folder_of, read_session
from services.session_gc import GC_COMMAND, SESSION_IDLE_DAYS, reap_once_a_day
from services.session_id import new_session_id
from services.session_location import (
    in_project_location,
    memar_own_note,
    unignored_note,
    project_location,
    project_location_note,
    project_root,
    register,
)
from services.session_log import record
from services.session_migrate import take_up
from services.session_claim import is_claimed
from services.session_plan import (
    DEFAULT_PRIORITY,
    HIGHEST_PRIORITY,
    LOWEST_PRIORITY,
    PLAN_NAME,
    checked_priority,
    checked_title,
    checked_topic,
    plan_file_problem,
    plan_skeleton,
    read_plan,
    set_priority,
    set_status,
    set_topic,
)
from services.session_record import PLAN, REPORT
from services.session_report import REPORT_NAME, report_skeleton, write_report
from services.session_topic import TOPIC_COMMAND, warn_near
from services.session_topics import TOPICS_COMMAND

NEW_COMMAND = "new"
PROJECT_REQUIRED = (
    f"{NEW_COMMAND} needs --project NAME or --project-path PATH to make a session: the project is always named, "
    "by a name `memar project find` resolves or by a folder, and the folder this runs in is never read; "
    "a session that is already there is continued without it"
)


def named_project(project: str | None) -> Path | None:
    """The project whose folder is PROJECT, its git top-level, or None when none was named.

    The flags (`add_project_flags`) have already turned a name into a folder;
    `project_by_path` refuses an empty value or one that is not a folder;
    nothing here reads the folder the process runs in.
    """
    if project is None:
        return None
    return project_root(project_by_path(project))


def recorded_project(folder: Path) -> Path | None:
    """The project FOLDER's plan records, when it names a folder that is there, else None."""
    named = ((read_session(folder).front or {}).get("project") or "").strip()
    if not named:
        return None
    where = Path(named)
    return where if where.is_dir() else None


def linked_conversation(session_id: str, parent: str) -> str:
    """The conversation a session opened from PARENT belongs to; PARENT must be a session folder."""
    if parent == session_id:
        fail("--parent names this session itself; name the session this task came from")
    folder = folder_of(parent)
    if not folder.is_dir():
        fail(f"no session folder {parent}: --parent names a session that is there, the one this task came from")
    return read_session(folder).conversation


def write_plan(
    folder: Path,
    title: str,
    parent: str | None = None,
    conversation: str | None = None,
    project: Path | None = None,
    status: str = Status.ACTIVE.key,
    priority: int | None = None,
    topic: str | None = None,
) -> None:
    """Create FOLDER's plan.md unless one is there; an existing plan is never touched."""
    opened = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if project is None:
        fail(PROJECT_REQUIRED)
    text = plan_skeleton(
        title, opened, project, parent=parent, conversation=conversation, status=status, priority=priority, topic=topic
    )
    try:
        with (folder / PLAN_NAME).open("x", encoding="utf-8", newline="\n") as plan:
            plan.write(text)
    except FileExistsError:
        pass


def queue_plan(folder: Path) -> None:
    """Queue FOLDER's existing plan: active and unclaimed becomes queued, queued stays; anything else is refused."""
    shape = plan_file_problem(folder / PLAN_NAME)
    if shape:
        fail(f"session {folder.name}: {shape}")
    status = read_plan(folder / PLAN_NAME).status
    if status == Status.QUEUED.key:
        return
    if is_claimed(folder):
        fail(f"session {folder.name} is claimed by an agent; it is queued again only once that claim has lapsed")
    if status != Status.ACTIVE.key:
        fail(f"session {folder.name} is {status or 'without a status'}; only an active session is queued")
    set_status(folder / PLAN_NAME, Status.QUEUED.key)


def ensure_session(
    session_id: str | None = None,
    title: str | None = None,
    parent: str | None = None,
    queued: bool = False,
    priority: int | str | None = None,
    topic: str | None = None,
    project: str | None = None,
) -> tuple[str, Path]:
    """Ensure the session's folder, its plan.md and report.md, and its role folders exist; return its id and path.

    TITLE is required when the folder has no plan.md yet, and unused when it
    has one. PARENT links a new plan to the session it came from; a plan that
    is there keeps the link it was written with, and a different one is
    refused rather than ignored. A rerun with the same id is idempotent: the
    folder, its plan, and its report are kept as they are and the same id and
    path are reported again. A session an earlier Memar left in temp/ is moved
    into temp/sessions/ as it is continued, or goes on in temp/ when the system
    will not move it; no second folder is made for it. A session in a project's
    own location is continued there. A folder that is nowhere yet is made in
    the location the project's preferences set, else temp/sessions/ inside the project (the Memar checkout's own is under Memar's root); a
    name already taken there by anything that is not a session folder is
    refused, and a location that cannot be made fails with a message. The
    first call of a day also reaps the session folders that have been idle past
    the limit, other than this one. QUEUED leaves a new plan queued, or queues
    an active one; PRIORITY, checked before anything is made, is written into a
    new plan or set on the one that is there; so is TOPIC, normalized, and a
    topic near one the project uses is warned about, not refused.

    PROJECT, a name or a folder, is required to make a folder, and an empty
    one is refused: the project is always named, and the folder the process
    runs in is never read. A folder that is there is continued without it, its
    project the one its plan records.
    """
    priority = None if priority is None else checked_priority(priority)
    topic = None if topic is None else checked_topic(topic)
    sid = new_session_id() if session_id is None else session_id
    folder = session_dir(sid)
    project = named_project(project)
    location = project_location(project) if project is not None else None
    if session_id is not None and not folder.is_dir():
        folder = take_up(sid) or project_folder_of(sid, also=location) or folder
    if project is None and folder.is_dir():
        project = recorded_project(folder)
        location = project_location(project) if project is not None else None
    if project is None and not (folder.is_dir() and (folder / PLAN_NAME).is_file()):
        fail(PROJECT_REQUIRED)
    if not folder.is_dir() and location is not None:
        folder = location / sid
        if folder.exists() or folder.is_symlink():
            fail(
                f"{folder} is there and is not a session folder; `new` never writes into it. "
                "Pass --session-id a name not used in that location, or none to mint one"
            )
    existed = folder.is_dir()
    has_plan = (folder / PLAN_NAME).is_file()
    title = checked_title(title, required=not has_plan)
    parent = (parent or "").strip() or None
    conversation = None
    if parent is not None:
        if has_plan:
            recorded = read_session(folder).parent
            if recorded != parent:
                fail(
                    f"session {sid} was opened with parent {recorded or '(none)'}; "
                    "a session's link is written once, with its plan"
                )
        else:
            conversation = linked_conversation(sid, parent)
    path = folder
    if not existed:
        try:
            path.mkdir(parents=True, exist_ok=True)
        except OSError as error:
            where = f"; check `{SESSIONS_KEY}` in {preferences_path(project)}" if location is not None and project is not None else ""
            fail(f"the session folder {path} could not be made ({error.strerror or error}){where}")
        record("opened", sid, f"parent {parent}" if parent else "", folder=path)
    if in_project_location(path):
        register(path.parent, project)
    if not has_plan:
        write_plan(path, title, parent, conversation, project, Status.QUEUED.key if queued else Status.ACTIVE.key, priority, topic)
    else:
        if queued:
            queue_plan(path)
        if priority is not None:
            set_priority(path / PLAN_NAME, priority)
        if topic is not None:
            set_topic(path / PLAN_NAME, topic)
    if topic and project is not None:
        warn_near(topic, project, sid)
    write_report(path, (read_session(path).front or {}).get("title"))
    ensure_role_folders(path)
    reap_once_a_day(keep=sid)
    return sid, path


def open_session(
    session_id: str | None,
    title: str | None,
    parent: str | None,
    queued: bool = False,
    priority: int | None = None,
    topic: str | None = None,
    project: str | None = None,
) -> None:
    """`new`: ensure the session and print its id, path, plan, and report, where it is when that is a project's, and with PARENT its brief."""
    sid, path = ensure_session(session_id, title, parent, queued, priority, topic, project)
    note(f"session_id: {sid}")
    note(f"path: {path}")
    note(f"plan: {path / PLAN_NAME}")
    note(f"report: {path / REPORT_NAME}")
    if in_project_location(path):
        note(project_location_note(path))
        unignored = unignored_note(path.parent)
        if unignored is not None:
            note(unignored)
    where = named_project(project) or recorded_project(path)
    ignored = memar_own_note(where) if where is not None else None
    if ignored is not None:
        note(ignored)
    if (parent or "").strip():
        note("brief:")
        note(f"    {brief_text(sid)}")


DESCRIPTION = f"""Ensure one session folder, for one task, and print its id, path, plan, and
report. A folder with no {PLAN_NAME} needs --title, one line saying what the task
is; a folder that has one is continued as it is. Pass the printed id back as
--session-id to continue the same session later. The path is absolute: use it
as printed, and never make a folder of the same name elsewhere instead.

Where the folder lies. In the project you name, in its temp/sessions/ folder,
made if it is missing, which the project's VCS should ignore as Memar's does
(`new` says when git does not, and changes nothing); in Memar's own checkout,
under temp/sessions/, when the project is Memar. A project that sets
`{SESSIONS_KEY}` in its {PREFERENCES_RELATIVE.as_posix()} has it in that folder instead; `new`
says on a line of its own each time it makes or continues a folder in a
project's location. The value is a path relative to the project's top folder,
or an absolute one; one that is that top folder itself or a drive or
filesystem root is refused, and one inside Memar's own temp/ is not used,
which `new` says too. If your file tool cannot reach the path, write there
through `memar content write`. A folder an earlier Memar left directly in
temp/ keeps its id and is moved into temp/sessions/ when --session-id
continues it.

What it writes. Each run makes the role folders the folder lacks, and writes
{PLAN_NAME}, and never overwrites one that is there:

{indent(PLAN.outline(), "    ")}
Request is what was asked, in the person's words, and what checks it is done;
Why, the reason the person asked for it, so that whoever does the work can
contribute and not only comply — written by the session that opens the plan,
in its own words, from the person's request; Steps, each marked local or
delegated, with its state; Next, what the next session does first. Keys are
written in PascalCase. Change the Status line as the task moves, and keep
{PLAN_NAME} as you work, so another session can continue from it. A plan in an
earlier shape (keys in lower case, `Status:` under its heading, `open` or
`done`) is not read, and a verb that would write it refuses; rewrite it in the
shape above. Beside the plan it writes {REPORT_NAME}, and never
overwrites one that is there either:

{indent(report_skeleton("TITLE"), "    ")}
Before you end work on the task, write in it what ran, the check and its
result, and its Status. Left open names each entry the task wrote in a
handoff (a question only the owner can answer is written there, not here), by
the handoff's path and the entry's heading. An agent that ends a session
someone else will read hands back short: its {REPORT_NAME}'s Status and path,
and, only when it needs someone's decision, at most {REPORT.hand_back_max_lines} lines under a
`## {REPORT.hand_back_part}` heading — each the question, its options, and the one
it recommends.

With --parent, the new plan records the session this task came from and the
first session of that conversation, and `new` ends with the brief that hands
the session to a sub-agent. To hand a task to a sub-agent, open its session
yourself with `--parent`, write the whole task into its {PLAN_NAME} — the
Request, the check that says it is done, the shape of its report, and its
Why, in your own words from the person's request — and hand the sub-agent only
the brief `new` prints, which `memar session {BRIEF_COMMAND} ID` prints again. The agent
handed a brief takes that session up and opens none, and does not rewrite its
Request.

To only add work — you were asked to plan or record tasks, not to do them —
open each with --queued and a --priority, or queue one you opened with
`--session-id ID --queued`, and write its {PLAN_NAME} as above (a queued plan
whose Request is empty is not taken), then leave it: never do a queued
session's work in your own context. Give each queued task a --topic, after
`memar session {TOPICS_COMMAND}` shows the ones the project already has; `memar session {TOPIC_COMMAND}`
sets one later.

To continue a task another session left, find it with `memar session {LIST_COMMAND}`, take
its folder up with `--session-id ID`, then read its {PLAN_NAME} and start from
its Next.

Once a day `new` also runs the sweep `memar session {GC_COMMAND}` runs at once, of
folders idle {SESSION_IDLE_DAYS} days whose status is complete; the session being opened or
continued is never swept."""


def describe(verbs) -> Callable[[argparse.Namespace], None]:
    """`memar session new`."""
    opener = verbs.add_parser(
        NEW_COMMAND,
        help="ensure one session folder for one task and print its id and path",
        description=DESCRIPTION,
    )
    opener.add_argument(
        "--session-id",
        default=None,
        help="reuse this session id instead of minting one (rerun is idempotent)",
    )
    opener.add_argument(
        "--title",
        default=None,
        help=f"one line saying what the task is; required unless the folder has a {PLAN_NAME}",
    )
    opener.add_argument(
        "--parent",
        default=None,
        metavar="ID",
        help="the session this task came from: the delegating session, or the previous task of the conversation",
    )
    opener.add_argument(
        "--queued",
        action="store_true",
        help=(
            "leave the task queued for an agent to claim rather than open for you: "
            "a new plan is written queued, and an existing active one no one has claimed is queued"
        ),
    )
    opener.add_argument(
        "--priority",
        type=int,
        default=None,
        metavar="N",
        help=(
            f"how soon a queued task is taken, {LOWEST_PRIORITY} to {HIGHEST_PRIORITY}: the higher goes sooner; "
            f"a plan without one counts as {DEFAULT_PRIORITY}"
        ),
    )
    opener.add_argument(
        "--topic",
        default=None,
        metavar="T",
        help=(
            "what the task is about, one subject one context can hold, narrower than a project; "
            "`claims` hands an agent the queued tasks of one topic together. Free text, written in lower "
            "case with spaces as hyphens; an empty one removes it. A topic near one already used is "
            "warned about; `topics` lists them. It is not copied from --parent"
        ),
    )
    add_project_flags(
        opener,
        "the project the task belongs to (the folder `new` runs in is never read; "
        "a session that is already there is continued without either)",
        required=True,
    )
    return run


def run(args: argparse.Namespace) -> None:
    project = project_from_args(args)
    named = {} if project is None else {"project": project}
    if args.topic is not None:
        open_session(args.session_id, args.title, args.parent, args.queued, args.priority, args.topic, **named)
    elif args.queued or args.priority is not None:
        open_session(args.session_id, args.title, args.parent, args.queued, args.priority, **named)
    else:
        open_session(args.session_id, args.title, args.parent, **named)
