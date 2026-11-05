#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/management/task/task.py — `memar task`: its help, which groups its verbs.

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
from modules.knowledge.label.labels.Status import Label_Status
from modules.identity.thing.labels.Complete import Label_Complete
from importlib import import_module
from machine.plugable_import import load as plugable_load
_m_memar_location = import_module('bundles.memar.services.location.memar_location')
TEMP_FOLDER = _m_memar_location.TEMP_FOLDER
_m_claim = import_module('modules-plugable.management.task.primitive.claim')
Claim = _m_claim.Claim
_m_layout = import_module('modules-plugable.management.task.services.layout')
TESTS_FOLDER = _m_layout.TESTS_FOLDER
folders_listing = _m_layout.folders_listing
kinds_listing = _m_layout.kinds_listing
_m_log = plugable_load('computer.git.services.log')
TASK_LOG_NAME = _m_log.TASK_LOG_NAME
_m_plan_file = import_module('modules-plugable.management.task.services.plan_file')
PLAN_NAME = _m_plan_file.PLAN_NAME
TASK_FACTS_NAME = import_module('modules-plugable.management.task.services.task_memory').TASK_FACTS_NAME
_m_record = import_module('modules-plugable.knowledge.documentation.primitive.record')
PLAN = _m_record.PLAN
REPORT = _m_record.REPORT
_m_report_file = import_module('modules-plugable.management.task.services.report_file')
REPORT_NAME = _m_report_file.REPORT_NAME

def status_meanings(words: tuple[type, ...]) -> str:
    """WORDS as help lines, each word and its meaning, obtained from the type."""
    return '\n'.join((f'    {status.title:<9}  {status.Overview()}' for status in words))

def report_endings() -> str:
    """How a run that ends in each Status narrates that end in the report's Result, as help lines."""
    return '\n'.join((f'    {status.title:<9}  {status.report_ending}' for status in reversed(REPORT.statuses)))
TASK_COMMAND = 'task'
TASK_COMMAND = TASK_COMMAND
SUMMARY = 'open the scratch folder one piece of work gets; queue tasks, and take queued tasks to do'
DESCRIPTION = f"memar task — one piece of work, its plan and its report\n\nA task is one thing the person asked for, done and checked. Its record lives on\nthe project's records branch: its facts (status, title, priority, …), its timeline\nof contents (plan, report, …), and whatever else the work makes, kept so that\nanother agent can continue it. One task is one id: another request in the same\nconversation, or a task handed to a sub-agent, gets a task of its own. Scratch\nwhile working goes in the task's temp/, not in the checkout or a runtime's own\nscratch place. To hand work to another agent — a sub-agent, a new chat, a queued\ntask — read what `ensure` says first.\n\nRole folders the work may use: {folders_listing()}, and a test in {TESTS_FOLDER}/;\nwhat the record does not need goes in {TEMP_FOLDER}/. A claim while an agent holds\nthe task is Memar's (`{Claim.NAME}`), not written by the agent.\n\nA task's Status is {Label_Status.listing(PLAN.kind)}, the words\n`modules-plugable/knowledge/documentation/documentation.md` (section Status) defines\nfor every document, each meaning:\n\n{status_meanings(PLAN.statuses)}\n\nA task ends — finished or not — when its Status is set with `memar task status`:\n{Label_Complete.title} once its check has passed. Post the report with\n`memar conversation post --kind report`, then set Status. The Result part of the\nreport narrates which kind of end it was; the report does not repeat the Status:\n\n{report_endings()}\n\nRead plan and report with `memar git show-task-records` (by kind, not by filename).\nAdd a text only with `memar conversation post --kind …`. Change facts through the\ntask verbs. The agent that queues a task, or hands one to a sub-agent, posts that\ntask's plan; and the agent of the delegating task posts the report of a sub-agent\nthat could only return text, and sets that task's Status.\n\nA task's scratch goes once its task is done; its records stay on its project's\nrecords branch and are never pushed. `close` and the sweep act only on a task\nalready archived, and neither acts on a task whose Status is Queued.\n\nEach verb below says what it does, and when to use it, in its own --help.\n"

def describe(verbs) -> None:
    """`memar task`, which only groups its verbs, each declared by its own service: nothing is owed before every one."""
    verbs.add_parser(TASK_COMMAND, help=SUMMARY, description=DESCRIPTION)
    return None
