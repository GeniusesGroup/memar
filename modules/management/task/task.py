#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/management/task/task.py — `memar task`: its help, which groups its verbs.

**Two audiences, two texts, and this file is where each lives.** `DESCRIPTION`
below is what `memar task --help` prints: it is addressed to whoever is about
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
`session_log`, `session_temp`, and `task_id` are what those share. The domain only groups
its verbs: nothing is owed before every one, so its `describe` returns no run.
A one-time migration of session folders or of the files in them is no service
of this domain: it lives in the session that does the change
(the session that does the change, in its `services/` folder), and nothing here names it.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
from machine.plugable_import import load as plugable_load
_m_fs_memar = plugable_load('computer.filesystem.services.fs_memar')
TEMP_FOLDER = _m_fs_memar.TEMP_FOLDER
from modules.management.task.primitive.claim import Claim
from modules.management.task.services.layout import TESTS_FOLDER, folders_listing, kinds_listing
_m_log = plugable_load('computer.git.services.log')
SESSION_LOG_NAME = _m_log.SESSION_LOG_NAME
from modules.knowledge.documentation.plan.services.plan import PLAN_NAME
from modules.knowledge.documentation.record import PLAN, REPORT
from modules.knowledge.documentation.report.primitive.report_key import ReportKey
from modules.knowledge.documentation.report.services.report import REPORT_NAME
from modules.knowledge.documentation.primitive.status import Status

def status_meanings(statuses: tuple[Status, ...]) -> str:
    """STATUSES as help lines, each word and its meaning, obtained from the type."""
    return '\n'.join((f'    {status.word:<9}  {status.meaning}' for status in statuses))

def report_endings() -> str:
    """The Statuses a report may state, each with how a run that stated it ended, as help lines in the table's order."""
    return '\n'.join((f'    {ReportKey.STATUS.written}: {status.word:<9}  {status.report_ending}' for status in reversed(REPORT.statuses)))
TASK_COMMAND = 'task'
SESSION_COMMAND = TASK_COMMAND
SUMMARY = 'open the scratch folder one piece of work gets; queue tasks, and take queued tasks to do'
DESCRIPTION = f"memar task — one folder for the task you are about to do\n\nA task is one thing the person asked for, done and checked. A session is the\nrecord of one task: a folder holding its plan, its report, and whatever else the\nwork makes, kept so that another session can continue it. One session is one\ntask: another request in the same conversation, or a task handed to a\nsub-agent, gets a session of its own. Work inside the session's folder, not in\nthe checkout, the OS temporary directory, or a runtime's own scratch place: the files you write while working belong to your session, not to\nthe repository. To hand work to another agent — a sub-agent, a new chat, a\nqueued session — read what `ensure` says first. Memar's session is not developed\nfurther, since organization's Task replaces it: add nothing to it unless it is\nindispensable, and say in one line why.\n\nThe folder's top holds only {PLAN_NAME} and {REPORT_NAME}, besides its folders,\n{folders_listing()}, and the `{Claim.NAME}` file Memar writes there while an\nagent holds the task. Put nothing else at the top: anything else the task makes\ngoes in the folder of its kind,\n\n    {kinds_listing()},\n    a test in {TESTS_FOLDER}/;\n\nand a file of another kind, or what the record does not need, in {TEMP_FOLDER}/.\n\nA session's Status, in its {PLAN_NAME}'s front matter, is {Status.listing(PLAN.kind)},\nthe words `modules/knowledge/documentation/documentation.md` (section Status) defines for every document,\neach meaning:\n\n{status_meanings(PLAN.statuses)}\n\nA session ends — finished or not — when its {REPORT_NAME} states a Status and\nits {PLAN_NAME} states the same: {Status.COMPLETE.word} once its check has passed. The\nResult part of the report says which kind of end it was:\n\n{report_endings()}\n\nWrite only inside your own folder; reading another session's folder is fine.\nTwo writes reach another session's folder, both from the session it came\nfrom: the agent that queues a session, or hands one to a sub-agent, writes\nthat session's {PLAN_NAME}; and the coordinator writes the {REPORT_NAME} of\na sub-agent that could only return text, and sets that {PLAN_NAME}'s Status.\nThe verbs below that take or rank a session write there by themselves. Each\nlocation that holds session folders keeps its own log of what was done to its\nfolders, {SESSION_LOG_NAME} at its top.\n\nA session's folder is scratch and goes once its task is done; its records\nstay, kept by `archive` on its project's records branch and never pushed.\n`close` and the sweep act only on a session already archived, and neither acts\non a session whose Status is Queued. `archive --help` says what is kept and where.\n\nEach verb below says what it does, and when to use it, in its own --help.\n"

def describe(verbs) -> None:
    """`memar task`, which only groups its verbs, each declared by its own service: nothing is owed before every one."""
    verbs.add_parser(TASK_COMMAND, help=SUMMARY, description=DESCRIPTION)
    return None
