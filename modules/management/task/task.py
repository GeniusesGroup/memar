#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/management/task/task.py — `memar task`: its help, which groups its verbs.

**Two audiences, two texts, and this file is where each lives.** `DESCRIPTION`
below is what `memar task --help` prints: it is addressed to whoever is about
to work in a task and states only the domain's own work — what a task and a
task are, what a task folder's top holds (`task_layout`), the Status
words and how a task ends, who writes into another task's folder, and
where a task's records are kept. Everything from here down
is addressed to whoever opens this file. A person opening a scratch folder does
not need to know which module resolves the temp root, and help output that told
them would be a second, worse copy of this.

**Each help states its own work, and no sub-verb's.** A
sub-verb's command line, what it writes, and when to use it are in that
sub-verb's own `--help`, which argparse's list of verbs under this help leads
to: a domain help that repeated them grew with every sub-verb and drifted from
each. The recipe the owner's one-line request needs ("do some of the queued
Memar tasks") is therefore `claims`'s (`task_claims`), the verb the list
names for taking queued tasks.

This file declares the verb and nothing else of its own. Each sub-verb is one
service on this shelf, which declares it and holds why it is built as it is:
`task_new` opens a folder and links it to its conversation, `task_start`
prints what an agent taking one up runs first, and takes it up; `task_find` lists them,
`task_close` closes one, `task_gc` sweeps, `task_archive` keeps a
task's task records on its project's records branch (`task_keep` says
which files, `task_branch` is the one place git is spoken to; `close`
asks whether it has, the sweep does it), `task_show` prints a task's
records from its folder or the branch, `task_claim` takes a queued
one by its id for one agent and `task_claims` the N first in line, `task_priority`
moves one up or down that line, `task_label` and `task_labels` add, remove and list
the labels, among them the topic `claims` batches by, `task_depends_on` shows, adds and drops the
tasks one cannot start without (`task_depends` says what that does to its
Status), `task_digest` gathers the decisions they
hand back; `task_plan`,
`task_report`, `task_folder`, `task_layout`, `task_location`,
`task_log`, `task_temp`, and `task_id` are what those share. The domain only groups
its verbs: nothing is owed before every one, so its `describe` returns no run.
A one-time migration of task folders or of the files in them is no service
of this domain: it lives in the task that does the change
(the task that does the change, in its `services/` folder), and nothing here names it.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
from machine.plugable_import import load as plugable_load
_m_fs_memar = plugable_load('computer.memory.filesystem.services.fs_memar')
TEMP_FOLDER = _m_fs_memar.TEMP_FOLDER
from modules.management.task.primitive.claim import Claim
from modules.management.task.services.layout import TESTS_FOLDER, folders_listing, kinds_listing
_m_log = plugable_load('computer.git.services.log')
TASK_LOG_NAME = _m_log.TASK_LOG_NAME
from modules.management.task.services.plan_file import PLAN_NAME
from modules.management.task.primitive.record import PLAN, REPORT
from modules.management.task.report.primitive.report_key import ReportKey
from modules.management.task.services.report_file import REPORT_NAME
from modules.knowledge.status.primitive.status import Status

def status_meanings(statuses: tuple[Status, ...]) -> str:
    """STATUSES as help lines, each word and its meaning, obtained from the type."""
    return '\n'.join((f'    {status.word:<9}  {status.meaning}' for status in statuses))

def report_endings() -> str:
    """The Statuses a report may state, each with how a run that stated it ended, as help lines in the table's order."""
    return '\n'.join((f'    {ReportKey.STATUS.written}: {status.word:<9}  {status.report_ending}' for status in reversed(REPORT.statuses)))
TASK_COMMAND = 'task'
TASK_COMMAND = TASK_COMMAND
SUMMARY = 'open the scratch folder one piece of work gets; queue tasks, and take queued tasks to do'
DESCRIPTION = f"memar task — one folder for the task you are about to do\n\nA task is one thing the person asked for, done and checked. Its folder is its\nrecord: a folder holding its plan, its report, and whatever else the\nwork makes, kept so that another agent can continue it. One task is one\nfolder: another request in the same conversation, or a task handed to a\nsub-agent, gets a task of its own. Work inside the task's folder, not in\nthe checkout, the OS temporary directory, or a runtime's own scratch place: the files you write while working belong to your task, not to\nthe repository. To hand work to another agent — a sub-agent, a new chat, a\nqueued task — read what `ensure` says first.\n\nThe folder's top holds only {PLAN_NAME} and {REPORT_NAME}, besides its folders,\n{folders_listing()}, and the `{Claim.NAME}` file Memar writes there while an\nagent holds the task. Put nothing else at the top: anything else the task makes\ngoes in the folder of its kind,\n\n    {kinds_listing()},\n    a test in {TESTS_FOLDER}/;\n\nand a file of another kind, or what the record does not need, in {TEMP_FOLDER}/.\n\nA task's Status, in its {PLAN_NAME}'s front matter, is {Status.listing(PLAN.kind)},\nthe words `modules-plugable/knowledge/documentation/documentation.md` (section Status) defines for every document,\neach meaning:\n\n{status_meanings(PLAN.statuses)}\n\nA task ends — finished or not — when its {REPORT_NAME} states a Status and\nits {PLAN_NAME} states the same: {Status.COMPLETE.word} once its check has passed. The\nResult part of the report says which kind of end it was:\n\n{report_endings()}\n\nWrite only inside your own folder; reading another task's folder is fine.\nTwo writes reach another task's folder, both from the task it came\nfrom: the agent that queues a task, or hands one to a sub-agent, writes\nthat task's {PLAN_NAME}; and the agent of the delegating task writes the {REPORT_NAME} of\na sub-agent that could only return text, and sets that {PLAN_NAME}'s Status.\nThe verbs below that take or rank a task write there by themselves. Each\nlocation that holds task folders keeps its own log of what was done to its\nfolders, {TASK_LOG_NAME} at its top.\n\nA task's folder is scratch and goes once its task is done; its records\nstay, kept by `archive` on its project's records branch and never pushed.\n`close` and the sweep act only on a task already archived, and neither acts\non a task whose Status is Queued. `archive --help` says what is kept and where.\n\nEach verb below says what it does, and when to use it, in its own --help.\n"

def describe(verbs) -> None:
    """`memar task`, which only groups its verbs, each declared by its own service: nothing is owed before every one."""
    verbs.add_parser(TASK_COMMAND, help=SUMMARY, description=DESCRIPTION)
    return None
