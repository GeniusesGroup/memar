#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/session_new.py — the verb `memar session new`: its help, and what it prints once a session's folder is open.

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
by printing the text that hands it over (`prompts_plan_brief`).

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

**What the help leaves out, kept here for whoever reads this file** (it is read in
development, not by the agent that runs the verb). Where the folder lies: in the
project you name, in its temp/sessions/ folder, made if missing, which the
project's VCS should ignore as Memar's does (`new` says when git does not and
changes nothing); in Memar's own checkout under temp/sessions/ when the project
is Memar; a project that sets `sessions` in its preferences has it in that folder
instead, a path relative to the project's top folder or an absolute one, and one
that is the top folder itself or a drive or filesystem root is refused, as is one
inside Memar's own temp/; `new` says on a line of its own each time it makes or
continues a folder in a project's location. A folder an earlier Memar left
directly in temp/ is continued where it is when --session-id names it. A plan in
an earlier shape (keys in lower case, `Status:` under its heading, `open` or
`done`) is not read, and a verb that would write it refuses. Keys are written in
PascalCase. The plan's and the report's outlines are written by `session_plan`
and `session_report`, so the help does not restate them. With --parent the new
plan records its parent and the first session of the conversation. A queued plan
whose Request is empty is not taken. Once a day `new` also runs the sweep
`session_gc` runs on demand, of folders idle `SESSION_IDLE_DAYS` days whose
status is complete; the session being opened or continued is never swept. The
agent handed a brief takes that session up and opens none, and does not rewrite
its Request (said by the brief's `start` output).

The folder itself is ensured by `session_ensure`, and its plan written or queued by
`session_plan_write`; this file is the verb's face over them.
"""
from __future__ import annotations

import argparse
from typing import Callable

from machine.console import note
from services.project_find import add_project_flags, project_from_args
from services.prompts import PROMPTS_COMMAND
from services.prompts_plan_brief import PLAN_BRIEF_COMMAND, brief_text
from services.session_ensure import NEW_COMMAND, ensure_session, named_project, recorded_project
from services.session_depends import DEPENDS_COMMAND
from services.session_find import LIST_COMMAND
from services.session_location import in_project_location, memar_own_note, project_location_note, unignored_note
from services.session_plan import PLAN_NAME
from services.session_plan_kind import CHEAPER_KINDS, KINDS, STRONG_KINDS
from services.task_kind import TaskKind
from services.priority import Priority
from services.session_record import REPORT, PlanKey
from services.session_report import REPORT_NAME
from services.session_temp import TEMP_SENTENCE
from services.session_topic import TOPIC_COMMAND
from services.session_topics import TOPICS_COMMAND


DEPENDS_FLAG = f"--{DEPENDS_COMMAND}"


def open_session(
    session_id: str | None,
    title: str | None,
    parent: str | None,
    queued: bool = False,
    priority: int | None = None,
    topic: str | None = None,
    project: str | None = None,
    kind: str | None = None,
    depends_on: list[str] | None = None,
) -> None:
    """`new`: ensure the session and print its id, path, plan, and report, where it is when that is a project's, and with PARENT its brief."""
    sid, path = ensure_session(session_id, title, parent, queued, priority, topic, project, kind, depends_on)
    note(f"session_id: {sid}")
    note(f"path: {path}")
    note(f"plan: {path / PLAN_NAME}")
    note(f"report: {path / REPORT_NAME}")
    note(TEMP_SENTENCE)
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
as printed, and never make a folder of the same name elsewhere instead. If your
file tool cannot reach it, write there through `memar content write`.

It writes the role folders the folder lacks, {PLAN_NAME} and {REPORT_NAME}, never
overwriting one that is there. The plan's sections are Request (what was asked,
and what checks it is done), Why (the reason, in your own words), Steps (each
local or delegated) and Next (what the next session does first); keep its Status
line current as the task moves. Before you end, write the report: what ran, the
check, the result, its Status. An agent that ends a session someone else will
read hands back short: the report's Status and path, and, only when it needs a
decision, at most {REPORT.hand_back_max_lines} lines under `## {REPORT.hand_back_part}`.

To hand a task to a sub-agent: open its session with --parent (the session you
work in) and --kind, write the whole task into its {PLAN_NAME} — Request, the
check that says it is done, the shape of its report, and Why — and hand the
sub-agent only the brief `new` prints, which `memar {PROMPTS_COMMAND} {PLAN_BRIEF_COMMAND} ID` prints
again. Nothing else goes in the hand-over.

To only add work, open each task with --queued and a --priority and a --topic
(`memar session {TOPICS_COMMAND}` lists the topics in use; `memar session {TOPIC_COMMAND}` sets one
later), write its {PLAN_NAME}, then leave it: never do a queued session's work
in your own context. A question only the owner can answer is not a task: write
it in the handoff of the document it concerns.

To continue a task another session left, find it with `memar session {LIST_COMMAND}`,
open it with `--session-id ID`, and start from its Next."""


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
            f"how soon a queued task is taken, {Priority.range_words()}: the higher goes sooner; "
            f"{Priority.default_words()}"
        ),
    )
    opener.add_argument(
        "--topic",
        default=None,
        metavar="T",
        help=(
            "what the task is about, narrower than a project: lower case, spaces as hyphens; "
            "`claims` hands an agent the queued tasks of one topic together. An empty one removes it; "
            "not copied from --parent"
        ),
    )
    opener.add_argument(
        "--kind",
        default=None,
        metavar="K",
        help=(
            f"what the task is, one of {', '.join(KINDS)}; "
            f"{', '.join(word for word in TaskKind.words() if word not in KINDS)} are refused, since no plan carries them. "
            f"{', '.join(word for word in KINDS if word in STRONG_KINDS)} run on the strongest model "
            f"the runtime offers, {', '.join(CHEAPER_KINDS)} on a cheaper one"
        ),
    )
    opener.add_argument(
        DEPENDS_FLAG,
        action="append",
        default=None,
        metavar="REF",
        help=(
            f"a session this one cannot start until it is Complete, ID or project/ID for a session of another project; may be repeated. "
            f"Written to the plan's {PlanKey.DEPENDS_ON.written}; while one is not Complete the session is Blocked and cannot be claimed "
            f"or started (`memar session {DEPENDS_COMMAND} --help`)"
        ),
    )
    add_project_flags(
        opener,
        "the project the task belongs to",
        required=True,
    )
    return run


def run(args: argparse.Namespace) -> None:
    project = project_from_args(args)
    named = {} if project is None else {"project": project}
    if args.kind is not None:
        named["kind"] = args.kind
    if args.depends_on:
        named[PlanKey.DEPENDS_ON.key] = args.depends_on
    if args.topic is not None:
        open_session(args.session_id, args.title, args.parent, args.queued, args.priority, args.topic, **named)
    elif args.queued or args.priority is not None:
        open_session(args.session_id, args.title, args.parent, args.queued, args.priority, **named)
    else:
        open_session(args.session_id, args.title, args.parent, **named)
