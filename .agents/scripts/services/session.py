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
`session_new` opens a folder and links it to its conversation, `session_brief`
holds the text that hands one to a sub-agent, `session_find` lists them,
`session_close` closes one, `session_gc` sweeps, `session_claim` takes a queued
one by its id for one agent and `session_claims` the N first in line, `session_priority`
moves one up or down that line, `session_digest` gathers the decisions they
hand back; `session_plan`,
`session_report`, `session_folder`, `session_location`, `session_log`, and
`session_id` are what those share. Before
any sub-verb runs, and after its arguments are parsed so that asking for help
moves nothing, `session_migrate` moves the session folders an earlier Memar
left directly in temp/, once each is quiet: that is what every sub-verb owes,
so it is said once, here.

Why the help carries the whole recipe for queued work. The owner hands an agent
one line — "do some of the queued Memar tasks", "do 5 tasks of project X" — and
nothing else, so `DESCRIPTION` must let an agent that has loaded only the skill
work out every step: find the queue, take N, delegate each brief to its own
sub-agent, read what comes back, and end with one digest. Memar starts no
agent itself: how a runtime starts a sub-agent is known only to the agent
already in a conversation (`session_claims`).

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import argparse
from textwrap import indent
from typing import Callable

from services.project_preferences import PREFERENCES_RELATIVE, SESSIONS_KEY
from services.session_claim import CLAIM_STALE_SECONDS
from services.session_gc import SESSION_IDLE_DAYS
from services.session_log import SESSION_LOG_NAME
from services.session_plan import DEFAULT_PRIORITY, HIGHEST_PRIORITY, LOWEST_PRIORITY, PLAN_NAME, STATUSES
from services.session_report import (
    DECISIONS_HEADING,
    MAX_DECISION_LINES,
    REPORT_NAME,
    report_skeleton,
    stop_table,
)

SESSION_COMMAND = "session"

SUMMARY = "open the scratch folder one piece of work gets; queue tasks, and take queued tasks to do"

DESCRIPTION = f"""memar session — one folder for the task you are about to do

A task is one thing the person asked for, done and checked. A session is the
record of one task: a folder holding its plan, its report, and whatever else the
work makes, kept so that another session can continue it.
One session is one task. Agent, sub-agent, and conversation are defined in
`memar --help`. Work inside its folder, not in the checkout: the files you write while working
belong to your session, not to the repository.

    memar session new --title TITLE     open a folder and print its id and path
    memar session new --title TITLE --parent ID
                                        open one linked to the session ID,
                                        and print the brief that hands it over
    memar session brief ID              print that brief again
    memar session new --title TITLE --parent ID --queued [--priority N]
                                        open one queued for some agent to take
                                        later, not you
    memar session priority ID N         change how soon a queued one is taken
    memar session list --status queued  find the tasks waiting to be taken
    memar session claims N --project [PATH]
                                        take that project's N queued tasks
                                        first in line, and print the brief
                                        for each
    memar session claim ID              take one queued task by its id
    memar session digest [--conversation ID]
                                        gather every decision needed into one
    memar session list [TEXT]           find Memar's own session folders,
                                        newest first
    memar session list --project [PATH]
                                        find every session of the project
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
    priority: N, with --priority
    ---
    # TITLE
    Status: open

    ## Request
    ## Why
    ## Steps
    ## Next

Request is what was asked, in the person's words, and what checks it is done;
Why, the reason the person asked for it, so that whoever does the work can
contribute and not only comply — written by the session that opens the plan,
in its own words, from the person's request; Steps, each marked local or delegated, with its state; Next, what the next
session does first. Status is queued, open, blocked, or done: queued while the
task waits for an agent to take it, open while someone works it; change that
line as the task moves, and set done once its check has passed. Keep
{PLAN_NAME} as you work, so another session can continue from it. A plan's
priority: a whole number from {LOWEST_PRIORITY} to {HIGHEST_PRIORITY}, {DEFAULT_PRIORITY} when absent; the higher goes sooner
when queued tasks are taken. Anyone may change it, a person or an agent, with
`memar session priority ID N`.

The folder's top holds {PLAN_NAME} and {REPORT_NAME}. Anything else the task makes
goes in the role folder of its kind, which `new` makes in the folder each time
it runs; `memar module folders --help` names them and says where what each
holds is written. `new` writes {REPORT_NAME} beside the plan, and never
overwrites one that is there:

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

To hand a task to a sub-agent, open its session yourself with `--parent`,
write the whole task into its {PLAN_NAME} — the Request, the check that says it
is done, the shape of its report, and its Why, in your own words from the
person's request — and hand the sub-agent only the brief
`new` prints, which `brief ID` prints again. The agent handed a brief takes
that session up and opens none, and does not rewrite its Request.

A task need not be done by the conversation that opens it. To only add work —
you were asked to plan or record tasks, not to do them — open each with
`new --title TITLE --parent ID --queued --priority N`, or queue one you opened
with `new --session-id ID --queued`, and write its {PLAN_NAME} as above (a
queued plan whose Request is empty is not taken), then leave it: never do a
queued session's work in your own context.

When you are asked to do some of the queued tasks — "do some of the queued
tasks", "do 5 tasks of project X" — work them this way, as the coordinator:

  1. `memar session list --status queued` shows what waits, each with its
     priority; add `--project [PATH]` for one project's.
  2. `memar session claims N --project X` takes project X's N first in
     line — the highest priority first, the oldest first among equals — and
     claims each for you, so no other agent takes it. `--project` is
     required: one run serves one project, so "do 5 tasks of X" means
     `claims 5 --project X`, which takes only X's, wherever they lie, and
     never another's; there is no default project and no way to take from
     all. If you do not know which project the tasks are for, ask the owner
     rather than guess. N is yours to choose from what you were asked; fewer
     may be queued, and you get what there is. For each it prints the session's id, title,
     priority, plan, and brief, and for a session it passed over, why.
     `memar session claim ID` takes one named task instead.
  3. Hand each printed brief to one fresh sub-agent per session, as your
     runtime starts one; never in your own context, and never two sessions
     to one sub-agent. Memar starts no agent: you do.
  4. When each ends, read its {REPORT_NAME}: its Stop and its Decisions needed. Its
     Status must agree with its Stop (the table above): a sub-agent that
     could only return text hands back the report, and you write it as its
     {REPORT_NAME} and set its Status. A report with no Stop, more lines than
     allowed, or a Stop that disagrees with its plan, is a failed hand-back:
     say so, and do not count that task done.
  5. Last, run `memar session digest --conversation ID`, ID your own
     session's, and give the owner that one digest rather than a question
     per task. Without `--conversation` it reads every session in Memar's
     own temp/sessions/ that is not done or queued.

A claim says who took a task; nothing keeps a claim fresh, so one a dead
agent left lapses after {CLAIM_STALE_SECONDS // 3600} hours, and the task can then be taken again or
queued again.

An agent that ends a session someone else will read hands back short: its
{REPORT_NAME}'s Stop line and path, and, only when it needs someone's
decision, at most {MAX_DECISION_LINES} lines under a `## {DECISIONS_HEADING}` heading —
each the question, its options, and the one it recommends. A longer one, one
with no Stop, or one whose Stop disagrees with the plan is a failed
hand-back, and `digest` marks it so. `digest` gathers into one every
session's {DECISIONS_HEADING} and every failed hand-back, with decisions or
without; it leaves out done sessions, whose task is over, and queued ones,
which have handed nothing back yet.

To continue a task another session left:

    memar session list TEXT             find it by id, title, or project
    memar session list --status open    find every session whose task is open
    memar session new --session-id ID   take that folder up as your session
then read its {PLAN_NAME} and start from its Next.

Write only inside your own folder; reading another session's folder is fine.
Two writes reach another session's folder, both from the session it came
from: the agent that queues a session, or hands one to a sub-agent, writes
that session's {PLAN_NAME}; and the coordinator writes the {REPORT_NAME} of
a sub-agent that could only return text, and sets that {PLAN_NAME}'s
Status. `claim`, `claims`, and `priority` write there too, by those verbs.

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
project's, and `gc` names those locations as the ones it did not sweep, and
those it no longer records because their folder is gone. `list` shows such a
folder only when asked: `--project` lists every session of a project, in its
own location or in Memar's, and `--conversation` every session of a
conversation, wherever it lies. Each location keeps its own log of what was
done to its folders, {SESSION_LOG_NAME} at its top.
"""


def describe(verbs) -> Callable[[argparse.Namespace], None]:
    """`memar session`, whose sub-verbs its capabilities declare."""
    verbs.add_parser(SESSION_COMMAND, help=SUMMARY, description=DESCRIPTION)
    return run


def run(args: argparse.Namespace) -> None:
    """What every sub-verb owes before its own run: the left folders moved."""
    from services.session_migrate import migrate

    migrate()
