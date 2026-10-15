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

The folder itself is ensured by `session_ensure`, and its plan written or queued by
`session_plan_write`; this file is the verb's face over them.
"""
from __future__ import annotations

import argparse
from textwrap import indent
from typing import Callable

from machine.console import note
from services.project_find import add_project_flags, project_from_args
from services.project_preferences import PREFERENCES_RELATIVE, SESSIONS_KEY
from services.session_brief import BRIEF_COMMAND, brief_text
from services.session_ensure import NEW_COMMAND, ensure_session, named_project, recorded_project
from services.session_find import LIST_COMMAND
from services.session_gc import GC_COMMAND, SESSION_IDLE_DAYS
from services.session_location import in_project_location, memar_own_note, project_location_note, unignored_note
from services.session_plan import PLAN_NAME
from services.session_plan_kind import CHEAPER_KINDS, KINDS, STRONG_KINDS
from services.session_plan_priority import DEFAULT_PRIORITY, HIGHEST_PRIORITY, LOWEST_PRIORITY
from services.session_record import PLAN, REPORT
from services.session_report import REPORT_NAME, report_skeleton
from services.session_temp import TEMP_SENTENCE
from services.session_topic import TOPIC_COMMAND
from services.session_topics import TOPICS_COMMAND


def open_session(
    session_id: str | None,
    title: str | None,
    parent: str | None,
    queued: bool = False,
    priority: int | None = None,
    topic: str | None = None,
    project: str | None = None,
    kind: str | None = None,
) -> None:
    """`new`: ensure the session and print its id, path, plan, and report, where it is when that is a project's, and with PARENT its brief."""
    sid, path = ensure_session(session_id, title, parent, queued, priority, topic, project, kind)
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
temp/ is continued where it is when --session-id names it.

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
the brief `new` prints, which `memar session {BRIEF_COMMAND} ID` prints again. The brief
is one fixed sentence that sends the agent to `memar session start`, which
prints its plan and the rest of what it must have read, so nothing else goes
in the hand-over: what it needs is in the plan. Say in the plan what kind of
task it is with --kind, so that `start` names the model it needs. The agent
handed a brief takes that session up and opens none, and does not rewrite its
Request.

To only add work — you were asked to plan or record tasks, not to do them —
open each with --queued and a --priority, or queue one you opened with
`--session-id ID --queued`, and write its {PLAN_NAME} as above (a queued plan
whose Request is empty is not taken), then leave it: never do a queued
session's work in your own context. Give each queued task a --topic, after
`memar session {TOPICS_COMMAND}` shows the ones the project already has; `memar session {TOPIC_COMMAND}`
sets one later. A question only the owner can answer is not a task to queue:
write it as an entry in the handoff of the document it concerns, at once.

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
    opener.add_argument(
        "--kind",
        default=None,
        metavar="K",
        help=(
            f"what the task is, one of {', '.join(KINDS)}; "
            f"{', '.join(STRONG_KINDS)} are judgment and run on the strongest model the runtime offers, "
            f"{', '.join(CHEAPER_KINDS)} on a cheaper one. `start` tells the sub-agent which. "
            "A plan without one leaves the Request to say"
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
    if args.kind is not None:
        named["kind"] = args.kind
    if args.topic is not None:
        open_session(args.session_id, args.title, args.parent, args.queued, args.priority, args.topic, **named)
    elif args.queued or args.priority is not None:
        open_session(args.session_id, args.title, args.parent, args.queued, args.priority, **named)
    else:
        open_session(args.session_id, args.title, args.parent, **named)
