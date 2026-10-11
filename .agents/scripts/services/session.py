#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/session.py — `memar session`: its help, and what every one of its verbs owes first.

**Two audiences, two texts, and this file is where each lives.** `DESCRIPTION`
below is what `memar session --help` prints: it is addressed to whoever is about
to open a session and says what to run and when its starter may close it.
Everything from here down is addressed to whoever opens this file. A person
opening a scratch folder does not need to know which module resolves the temp
root, and help output that told them would be a second, worse copy of this.

This file declares the verb and nothing else of its own. Each sub-verb is one
service on this shelf, which declares it and holds why it is built as it is:
`session_new` opens a folder and links it to its conversation, `session_find`
lists them, `session_close` closes one, `session_gc` sweeps; `session_plan`,
`session_report`, `session_folder`, `session_location`, `session_log`, and
`session_id` are what those share. Before
any sub-verb runs, and after its arguments are parsed so that asking for help
moves nothing, `session_migrate` moves the session folders an earlier Memar
left directly in temp/, once each is quiet: that is what every sub-verb owes,
so it is said once, here.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import argparse
from textwrap import indent
from typing import Callable

from services.project_preferences import PREFERENCES_RELATIVE, SESSIONS_KEY
from services.session_gc import SESSION_IDLE_DAYS
from services.session_plan import PLAN_NAME, STATUSES
from services.session_report import REPORT_NAME, report_skeleton, stop_table

SESSION_COMMAND = "session"

SUMMARY = "open the scratch folder one piece of work gets"

DESCRIPTION = f"""memar session — one folder for the task you are about to do

One session is one task: one thing the person asked for, done and checked.
Work inside its folder, not in the checkout: the files you write while working
belong to your session, not to the repository.

    memar session new --title TITLE     open a folder and print its id and path
    memar session new --title TITLE --parent ID
                                        open one linked to the session ID
    memar session list [TEXT]           find session folders, newest first
    memar session list --conversation ID
                                        list every session of ID's conversation
    memar session list --status STATUS [--idle-days DAYS]
                                        find the sessions in that state
    memar session close                 move one to the OS recycle bin / Trash
    memar session gc                    sweep idle finished folders now,
                                        and say what was moved and kept

`new` prints an id and a path; pass that id back as `--session-id` to continue
the same session later. The path is absolute: use it as printed, and never make
a folder of the same name elsewhere instead. It lies in Memar's own checkout,
under temp/sessions/, also when you work in another project — unless that
project sets `{SESSIONS_KEY}` in its {PREFERENCES_RELATIVE.as_posix()}, and then it lies
in that folder, which `new` says on a line of its own each time it makes or
continues a folder there. The value is a path relative to the project's top
folder, or an absolute one; one that is that top folder itself or a drive or
filesystem root is refused, and one inside Memar's own temp/ is not used, which
`new` says too. If your file tool cannot reach the path,
write there through `memar content write`. A folder an earlier Memar left
directly in temp/ keeps its id and is moved into temp/sessions/ by a session
command once nothing in it has changed for a day, or when `new --session-id`
continues it; until then it is listed, continued, and closed where it is. Each
move is printed, and the next `memar` command says it once more.

A new session needs `--title`, one line saying what the task is, and so does a
folder that has no {PLAN_NAME} yet. `new` then writes the folder's {PLAN_NAME},
and never overwrites one that is there:

    ---
    title: TITLE
    opened: the UTC time it was written, e.g. 2026-10-08T13:20:34Z
    project: the git top-level of where you ran `new`, else that folder
    parent: ID, and conversation: the first session's id, with --parent
    ---
    # TITLE
    Status: open

    ## Request
    ## Steps
    ## Next

Request is what was asked, in the person's words, and what checks it is done;
Steps, each marked local or delegated, with its state; Next, what the next
session does first. Status is open, blocked, or done: change that line as the
task moves, and set done once its check has passed. Keep {PLAN_NAME} as you
work, so another session can continue from it.

The folder's top holds {PLAN_NAME} and {REPORT_NAME}. Anything else the task makes
goes in the role folder of its kind, which `new` makes in the folder each time
it runs; modules/README.md in the Memar checkout says what each holds. `new`
writes {REPORT_NAME} beside the plan, and never overwrites one that is there:

{indent(report_skeleton(), "    ")}
Before you end work on the task — finished or not — write {REPORT_NAME}: its Stop
line, what ran, and the check and its outcome. Then set {PLAN_NAME}'s Status to
agree with the Stop:

{stop_table()}

`list` marks a session whose report and plan disagree, and one whose status is
not {", ".join(STATUSES[:-1])}, or {STATUSES[-1]}.

Each further task gets a session of its own — another request in the same
conversation, or a task handed to a sub-agent, which works in its own session.
Open it with `--parent` naming the session it came from; `list` shows the
sessions of one conversation together.

To continue a task another session left:

    memar session list TEXT             find it by id, title, or project
    memar session list --status open    find every session whose task is open
    memar session new --session-id ID   take that folder up as your session
then read its {PLAN_NAME} and start from its Next.

Write only inside your own folder; reading another session's folder is fine.

You do not have to close a session. Once a day, the first `new` moves to the
recycle bin every session folder in which nothing has changed for
{SESSION_IDLE_DAYS} days and whose status is done — a folder with no {PLAN_NAME}
counts as finished too — so a folder whose task is not done is never swept,
however long it sits; it goes when its status is done or a person closes it.
Run `close` only when the person who started the session has already said the
work is finished; never ask them to, and never close a session you did not
open. `gc` runs that sweep at once, by the same rules, and lists the idle
folders it kept because their task is not done.

The sweep reaches only Memar's own temp/sessions/. A folder in a project's own
session location is never swept: keeping, committing, or deleting it is the
project's, and `gc` names those locations as the ones it did not sweep.
"""


def describe(verbs) -> Callable[[argparse.Namespace], None]:
    """`memar session`, whose sub-verbs its capabilities declare."""
    verbs.add_parser(SESSION_COMMAND, help=SUMMARY, description=DESCRIPTION)
    return run


def run(args: argparse.Namespace) -> None:
    """What every sub-verb owes before its own run: the left folders moved."""
    from services.session_migrate import migrate

    migrate()
