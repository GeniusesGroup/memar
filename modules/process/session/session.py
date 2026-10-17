#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/process/session/session.py — `memar session`: its help, which groups its verbs.

**Two audiences, two texts, and this file is where each lives.** `DESCRIPTION`
below is what `memar session --help` prints: it is addressed to whoever is about
to work in a session and states only the domain's own work — what a task and a
session are, what a session folder's top holds (`session_layout`), the Status
words and how a session ends, who writes into another session's folder, and
where a session's records are kept. Everything from here down
is addressed to whoever opens this file. A person opening a scratch folder does
not need to know which module resolves the temp root, and help output that told
them would be a second, worse copy of this.

**Each help states its own work, and no sub-verb's.** A
sub-verb's command line, what it writes, and when to use it are in that
sub-verb's own `--help`, which argparse's list of verbs under this help leads
to: a domain help that repeated them grew with every sub-verb and drifted from
each. The recipe the owner's one-line request needs ("do some of the queued
Memar tasks") is therefore `claims`'s (`session_claims`), the verb the list
names for taking queued tasks.

This file declares the verb and nothing else of its own. Each sub-verb is one
service on this shelf, which declares it and holds why it is built as it is:
`session_new` opens a folder and links it to its conversation, `session_start`
prints what an agent taking one up runs first, and takes it up; `session_find` lists them,
`session_close` closes one, `session_gc` sweeps, `session_archive` keeps a
task's session records on its project's records branch (`session_keep` says
which files, `session_branch` is the one place git is spoken to; `close`
asks whether it has, the sweep does it), `session_show` prints a session's
records from its folder or the branch, `session_claim` takes a queued
one by its id for one agent and `session_claims` the N first in line, `session_priority`
moves one up or down that line, `session_label` and `session_labels` add, remove and list
the labels, among them the topic `claims` batches by, `session_depends_on` shows, adds and drops the
sessions one cannot start without (`session_depends` says what that does to its
Status), `session_digest` gathers the decisions they
hand back; `session_plan`,
`session_report`, `session_folder`, `session_layout`, `session_location`,
`session_log`, `session_temp`, and `session_id` are what those share. The domain only groups
its verbs: nothing is owed before every one, so its `describe` returns no run.
A one-time migration of session folders or of the files in them is no service
of this domain: it lives in the session that does the change
(.agents/scripts/README.md), and nothing here names it.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

from modules.process.session.primitive.claim import Claim
from modules.process.session.services.layout import kinds_listing
from modules.process.session.services.log import SESSION_LOG_NAME
from modules.knowledge.documentation.plan.services.plan import PLAN_NAME
from modules.knowledge.documentation.record import PLAN, REPORT
from modules.knowledge.documentation.report.primitive.report_key import ReportKey
from modules.knowledge.documentation.report.services.report import REPORT_NAME
from modules.knowledge.documentation.primitive.status import Status



def status_meanings(statuses: tuple[Status, ...]) -> str:
    """STATUSES as help lines, each word and its meaning, obtained from the type."""
    return "\n".join(f"    {status.word:<9}  {status.meaning}" for status in statuses)


def report_endings() -> str:
    """The Statuses a report may state, each with how a run that stated it ended, as help lines in the table's order."""
    return "\n".join(
        f"    {ReportKey.STATUS.written}: {status.word:<9}  {status.report_ending}" for status in reversed(REPORT.statuses)
    )


SESSION_COMMAND = "session"
SUMMARY = "open the scratch folder one piece of work gets; queue tasks, and take queued tasks to do"

DESCRIPTION = f"""memar session — one folder for the task you are about to do

A task is one thing the person asked for, done and checked. A session is the
record of one task: a folder holding its plan, its report, and whatever else the
work makes, kept so that another session can continue it. One session is one
task: another request in the same conversation, or a task handed to a
sub-agent, gets a session of its own. Agent, sub-agent, and conversation are
defined in `memar --help`. Work inside the session's folder, not in the
checkout: the files you write while working belong to your session, not to the
repository.

The folder's top holds only {PLAN_NAME} and {REPORT_NAME}, besides its role
folders and the `{Claim.NAME}` file Memar writes there while an agent holds the
task. Put nothing else at the top: anything else the task makes goes in the
role folder of its kind,

    {kinds_listing()},
    a test in tests/;

and a file of another kind goes in the role folder that holds it.
`memar module folders --help` names the role folders and prints what each
holds and does not.

A session's Status, in its {PLAN_NAME}'s front matter, is {Status.listing(PLAN.kind)},
the words `modules/knowledge/documentation/documentation.md` (section Status) defines for every document,
each meaning:

{status_meanings(PLAN.statuses)}

A session ends — finished or not — when its {REPORT_NAME} states a Status and
its {PLAN_NAME} states the same: {Status.COMPLETE.word} once its check has passed. The
Result part of the report says which kind of end it was:

{report_endings()}

Write only inside your own folder; reading another session's folder is fine.
Two writes reach another session's folder, both from the session it came
from: the agent that queues a session, or hands one to a sub-agent, writes
that session's {PLAN_NAME}; and the coordinator writes the {REPORT_NAME} of
a sub-agent that could only return text, and sets that {PLAN_NAME}'s Status.
The verbs below that take or rank a session write there by themselves. Each
location that holds session folders keeps its own log of what was done to its
folders, {SESSION_LOG_NAME} at its top.

A session's folder is scratch and goes once its task is done; its records
stay, kept by `archive` on its project's records branch and never pushed.
`close` and the sweep act only on a session already archived, and neither acts
on a session whose Status is Queued. `archive --help` says what is kept and where.

Each verb below says what it does, and when to use it, in its own --help.
"""


def describe(verbs) -> None:
    """`memar session`, which only groups its verbs, each declared by its own service: nothing is owed before every one."""
    verbs.add_parser(SESSION_COMMAND, help=SUMMARY, description=DESCRIPTION)
    return None
