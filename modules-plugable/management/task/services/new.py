#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
"""modules-plugable/management/task/services/new.py — the verb `memar task_ensure`: its help, and what it prints once a task's folder is open.

Why one folder per task, under ONE root. Parallel agent tasks edit one
shared working tree with no coordination, and concurrent writes to one file
collide silently — shared-tree collisions. The per-file advisory locks in
`bundles/memar_adaptor/fs/services/text_edit_lock.py` answer that, and `memar content_write` and `edit` take one,
but advisory locks are honored by skill rule and not by the filesystem:
file-write tools bypass them, and only intent notes saying who plans what
against which base let a waiter that takes over a stale lock read what the dead
task meant. Intent notes and locks are scratch, and scratch needs a home that
survives the task: task folders give every task its own folder, and
every task works inside its own folder so nothing lands in git by accident.
That home is a `.agents/tasks/` folder inside the project (the Memar checkout's
own, for Memar), which git does not ignore, because an ignored folder is lost to
a clean or a re-clone while the task's records are not yet archived. OS temp dirs
are forbidden for the same reason: they are wiped by other apps while tasks last
days (the OS-temp wiped risk). Where exactly is
`bundles/memar/services/location/memar_location.py`'s answer, and it fails closed rather than guessing.

A task writes only inside its own folder: --task-id reuses an id only to
continue the same task, and two tasks writing one folder reintroduce the
unattributed mixing this exists to remove. Reading another task's folder is
fine; a task that needs something from an old folder copies it into its own.

One task is one folder, so a conversation that asks for several things, or
hands a step to a sub-agent, opens several tasks. Each records the task
it came from as its parent and the first task of the conversation, written
once with its plan: a link read off one file never needs a walk up a chain
whose folders may already be swept. The parent must be a task folder that
is there, because its conversation is read from it. A task opened with a
parent is most often one the parent is handing to a sub-agent, so `ensure` ends
by printing the text that hands it over (`plan_brief`).

A task can be opened, or its written plan left, `--queued`: waiting for an
agent to take it (`task_claim`) and hand it to a fresh sub-agent, rather
than worked by the conversation that opened it. Only an active plan no one has
claimed is queued again, so a task being worked, or one finished, is never
put back in line. `--priority` is owned by the ensure widget: after open it
sets Priority_Rank through Thing, so queuing and ranking a task is one
command without the ensure service doing Priority's work. `--label KIND=WORD`, repeatable, says what the task is
about and what act it is, the same way (`plan_label` widget, `plan_registry`); they are the
task's own, never copied from the parent's, since a copy would hide the
decision of what the new task is about. A topic is one the project declares;
a word declared nowhere is refused, naming the declared topics near it.

Opening is also when the day's sweep runs (`task_gc`), never touching the
task being opened or continued.

Where a new folder is made is asked of the project the plan names: a project
whose preferences set a task location gets its folders there, every other
one in .agents/tasks/ inside itself, and the Memar checkout in its own root
(`task_location`). Each run also ensures the
folder's shape — the plan and the report at its top (`task_plan`,
`task_report`), and the task's own folders for whatever else the task
makes (`task_layout`) — creating only what is missing, so a folder from an
earlier Memar is brought to the same shape as it is continued.

**What the help leaves out, kept here for whoever reads this file** (it is read in
development, not by the agent that runs the verb). Where the folder lies: in the
project you name, in its .agents/tasks/ folder, made if missing, which the
project's VCS does not ignore (owner, 2026-10-22), and which never enters the main
branch: `archive` keeps its records on the records branch. A custom location that
git does not ignore is said so by `ensure`, which changes nothing; in Memar's own checkout under .agents/tasks/ when the project
is Memar; a project that sets `tasks` in its preferences has it in that folder
instead, a path relative to the project's top folder or an absolute one, and one
that is the top folder itself or a drive or filesystem root is refused, as is one
inside Memar's own temp/; `ensure` says on a line of its own each time it makes or
continues a folder in a project's location. A folder an earlier Memar left
directly in temp/ is continued where it is when --task-id names it. A plan in
an earlier shape (keys in lower case, `Status:` under its heading, `open` or
`done`) is not read, and a verb that would write it refuses. Keys are written in
PascalCase. The plan's and the report's outlines are written by `task_plan`
and `task_report`, so the help does not restate them. With --parent the new
plan records its parent and the first task of the conversation. A queued plan
whose Request is empty is not taken. Once a day `ensure` also runs the sweep
`task_gc` runs on demand, of folders idle `TASK_IDLE_DAYS` days whose
status is complete; the task being opened or continued is never swept. The
agent handed a brief takes that task up and opens none, and does not rewrite
its Request (said by the brief's `start` output).

The folder itself is ensured by `task_ensure`, and its plan written or queued by
`task_plan_write`; this file is the verb's face over them.
"""

from __future__ import annotations
from importlib import import_module
_m_set_status = import_module('modules-plugable.knowledge.label.status.services.set_status')
SET_STATUS_LINE = 'memar status_set ID WORD --project NAME'
from machine.plugable_import import load as plugable_load
import argparse
from typing import Callable
from machine.console import note
from modules.computer.software.services.project_find import add_project_flags, project_from_args
_m_plan_brief = plugable_load('management.agency.services.get_task_plan_carry_out_brief.get_task_plan_carry_out_brief')
PLAN_BRIEF_COMMAND = _m_plan_brief.PLAN_BRIEF_COMMAND
brief_text = _m_plan_brief.brief_text
_m_ensure = import_module('modules-plugable.management.task.services.ensure')
ENSURE_COMMAND = _m_ensure.ENSURE_COMMAND
named_project = _m_ensure.named_project
recorded_project = _m_ensure.recorded_project
_m_depends = import_module('modules-plugable.management.task.services.depends')
DEPENDS_COMMAND = _m_depends.DEPENDS_COMMAND
_m_list = import_module('modules-plugable.management.task.services.list')
LIST_COMMAND = _m_list.LIST_COMMAND
_m_task_location = import_module('modules-plugable.management.task.services.task_location')
in_project_location = _m_task_location.in_project_location
memar_own_note = _m_task_location.memar_own_note
project_location_note = _m_task_location.project_location_note
unignored_note = _m_task_location.unignored_note
_m_plan_text = import_module('modules-plugable.knowledge.documentation.plan.services.plan_text')
_m_plan_front = import_module('modules-plugable.knowledge.documentation.plan.services.plan_front')
_m_plan_acts = import_module('modules-plugable.knowledge.documentation.plan.services.plan_acts')
MODEL_RULE = _m_plan_acts.MODEL_RULE
ACTS = _m_plan_acts.ACTS
TOPIC = _m_plan_front.TOPIC
kinds_listing = _m_plan_front.kinds_listing
OPENED_CHAT_RULE = '/modules-plugable/management/task/rules/opened-chat-is-left-alone/opened-chat-is-left-alone.md'
LATER_WORK_RULE = '/modules-plugable/management/task/rules/later-work-returns-to-its-task/later-work-returns-to-its-task.md'
DELEGATION_MODEL_RULE = '/modules-plugable/management/agency/rules/delegation-names-the-lowest-model/delegation-names-the-lowest-model.md'
HAND_BACK_RULE = '/modules-plugable/management/agency/rules/delegator-writes-the-refused-hand-back/delegator-writes-the-refused-hand-back.md'
ABSTRACTION_RULE = '/modules/computer/software/rules/abstraction-first/abstraction-first.md'
TESTS_RULE = '/modules/process/test/rules/tests-first-and-scoped/tests-first-and-scoped.md'
_m_acts = import_module('modules.management.agency.labels.acts')
Acts = _m_acts.Acts
Priority_Rank = import_module('modules-plugable.identity.thing.priority.primitive.rank').Priority_Rank
_m_record = import_module('modules-plugable.knowledge.documentation.primitive.record')
REPORT = _m_record.REPORT
_m_plan_key = import_module('modules-plugable.knowledge.documentation.plan.primitive.plan_key')
PlanKey = _m_plan_key.PlanKey
_m_report_text = import_module('modules-plugable.knowledge.documentation.report.services.report_text')
_m_task_files = import_module('modules-plugable.management.task.services.task_memory')
accepts_contents = _m_task_files.accepts_contents
plan_path = _m_task_files.plan_path
report_path = _m_task_files.report_path
_m_post = import_module('modules-plugable.management.timeline.widgets.conversation.services.post')
POST_COMMAND = _m_post.POST_COMMAND
_m_temp = import_module('modules-plugable.management.task.services.temp')
TEMP_SENTENCE = _m_temp.TEMP_SENTENCE
_m_task_id = import_module('modules-plugable.management.task.primitive.task_id')
TaskId = _m_task_id.TaskId
_m_new_chats = plugable_load('management.agency.services.get_new_chats_ask.get_new_chats_ask')
NEW_CHATS_COMMAND = _m_new_chats.NEW_CHATS_COMMAND
DEPENDS_FLAG = f'--{DEPENDS_COMMAND}'

def open_task(task_id: str | None, title: str | None, parent: str | None, queued: bool=False, priority: int | None=None, labels: list[str] | None=None, project: str | None=None, depends_on: list[str] | None=None) -> None:
    ensure_open = import_module('modules-plugable.management.task.widgets.ensure.ensure').open
    sid, path = ensure_open(task_id, title, parent, queued, priority, labels, project, depends_on)
    note(f'task_id: {sid}')
    for kind in ('plan', 'report'):
        note(f'{kind}: write it with `memar conversation_{POST_COMMAND} --timeline {sid} --kind {kind} --content-file FILE` (or the text on standard input); it is added as the next content of kind {kind}, the current {kind} being the latest')
    if (parent or '').strip():
        note('brief:')
        note(f'    {brief_text(sid)}')
    del path
DESCRIPTION = f"""Ensure one task on the records branch, and print its id, plan, and\nreport. Open one for work to be done, whose check is a change applied or a\ndecision recorded, before any other work of that task. A task whose outcome is\njust that it was done — committing, a rename, one edit, a lookup, a handful of\ntool calls — opens none and starts no sub-agent. An inquiry — looking into Memar or\nthe work to answer the task's own questions — opens none either: it is a step\nof the task it serves, and what it finds is a content of that task. A research that gathers and concludes what many other tasks will build\non, as Lexer's did, is a `research` task of its own, recorded as a Research document. Open\na new task only for work that is truly independent. A task is one thing asked with one check:\nlater work on a finished task's result (a problem found in it, a ruling applied to it, the rest of it\nan agent's limit left) goes back to that task, as a new plan content on the same task, and a ruling of the\nowner since is a content of kind `decision` on it; a full context, a plan a sub-agent can read or the end of a session is not a new thing asked,\nand a new task is for work new in itself (`memar content_resolve_path {LATER_WORK_RULE}`). Name the project with the flag for what you have, never\none in the other's place, and never turn a name you were told into a guessed\npath. A task with no plan content needs --title, one line saying what the task\nis; one that has a plan is continued as it is. Pass the printed id back as\n--task-id to continue the same task later. No filesystem path is printed:\nthe task lives on the records branch; write plan and report only with\n`memar conversation_{POST_COMMAND}`; set Status with `{SET_STATUS_LINE}`.\n\nA task holds contents, not files to write over: its plan is its latest content of\nkind plan and its report its latest of kind report, each a text added with\n`memar conversation_{POST_COMMAND} --timeline ID --kind plan|report --content-file FILE`\n(or the text on standard input), which prints the number of the new content; a\ntext is added and never written over, and the same verb adds a text of any other\nkind (see its --help). Read plan and report with `memar git_show_task_records`\n(by kind). The plan's sections are Request (what was asked, and what checks it is\ndone), Why (the reason, in your own words), Steps (each local or delegated, each\nnaming the governing documents it reads and the tests it adds or runs: a step that\nnames none cannot start) and Next (what the next task does first). Before you end,\npost the report (what ran, the check, the result) and set Status with\n`{SET_STATUS_LINE}`. An agent that ends a task someone else will read hands back\nshort: the Status and, only when it needs a decision, at most\n{REPORT.hand_back_max_lines} lines under `## {REPORT.hand_back_part}`.\n\nBefore handing work to another agent, decide where it runs by two questions, and\nwrite both answers in your plan for each task: does your conversation need\nits result, and does it need the owner during the work (questions, critique,\nback-and-forth)? Its result needed and the owner not: a sub-agent, which returns\nonly its hand-back. The owner needed, whether or not you wait for it: a new chat\n(`memar ai_{NEW_CHATS_COMMAND.replace("-", "_")}`). A chat opened for a task whose result your work does not need\nis then left alone: do not read it, poll it, ask it for news, or follow it up, because every\nlook spends your context for nothing and the owner answers its questions there; what a later\ntask needs is in that task's report. Its result not needed: independent, opened with no --parent, written\nwhole and then left: its chat opened independent, never as your child session, so that none of its messages come back to you (`memar content_resolve_path {OPENED_CHAT_RULE}`), or listed for the owner when it needs the\nowner, and otherwise a sub-agent once your own work leaves room, or, to only\nadd work, queued (below). A chat with nothing to ask the owner only gives the\nowner one more chat to watch. The owner's\nwords never pick: "open a task", "create a chat", "ask an agent" name the\nwork, not where it runs, and an agent app's own default does not pick either. An\napp's tool that starts a chat gives it at most your own model, so work whose\nneed is above your own is a sub-agent with the model named, as the rule\n(`memar content_resolve_path {MODEL_RULE}`) says.\n\nA sub-agent or a new chat that continues a task is handed that task: the new plan content, the decision contents and the brief\n`memar ai_{PLAN_BRIEF_COMMAND.replace("-", "_")} ID` prints, and no task is opened for it.\nTo hand a thing new in itself to a sub-agent: open its task with --parent (the task you\nwork in) and --label ACT (one of {', '.join(ACTS)}), post the whole task as its plan content — Request, the\ncheck that says it is done, the shape of its report, and Why — and hand the\nsub-agent only the brief `ensure` prints, which `memar ai_{PLAN_BRIEF_COMMAND.replace("-", "_")} ID` prints\nagain. Nothing else goes in the hand-over. Name the model when you start it, as the rule (`memar content_resolve_path {MODEL_RULE}`) says: an\napp's default may not be the level the task needs. Write in the plan who checks the result, and name the lowest level that is enough, never the strongest by habit (`memar content_resolve_path {DELEGATION_MODEL_RULE}`). If the harness refuses the sub-agent's report post, you post it (`memar content_resolve_path {HAND_BACK_RULE}`). Before any code of a software requirement, its abstraction is written in Khayyam and approved, and its tests come first, run scoped and under a time limit (`memar content_resolve_path {ABSTRACTION_RULE}`, `memar content_resolve_path {TESTS_RULE}`). While it works, do what its result cannot\nchange and wait for the rest, as you would for the owner's answer. A task may\nstop at any time and for any time, as an issue may: one that stops to wait on\nanother records it in its plan's Depends_on (`{DEPENDS_COMMAND}`) and is Blocked.\n\nTo only add work, open each task with --queued and a --priority and a --label {TOPIC}=T\n(the declared Topics are the label declarations in the `labels/` folders of the project's modules,\nfound with `memar content_search`), post its plan, then leave it: never do a queued task's work\nin your own context. A question only the owner can answer is a `question` content of the task it concerns, and a large unrelated one a task of its own.\n\nTo continue a task another task left, find it with `memar task_ids` or `memar content_find --from tasks`,\nopen it with `--task-id ID`, and start from its Next."""

def describe(verbs) -> Callable[[argparse.Namespace], None]:
    opener = verbs.add_parser(ENSURE_COMMAND, help='ensure one task and print its id', description=DESCRIPTION)
    TaskId.add_flag(opener, 'reuse this task id instead of minting one (rerun is idempotent)')
    opener.add_argument('--title', default=None, help='one line saying what the task is; required unless the task already has a plan content')
    opener.add_argument('--parent', default=None, metavar='ID', help='the task this task came from: the delegating task whose result it needs; none for an independent task')
    opener.add_argument('--queued', action='store_true', help='leave the task queued for an agent to claim rather than open for you: a new plan is written queued, and an existing active one no one has claimed is queued')
    opener.add_argument('--priority', type=int, default=None, metavar='N', help=f'after open, set Priority_Rank via Thing ({Priority_Rank.listing()}); higher goes sooner among queued peers; absence ranks as the lowest; owned by the ensure widget, not the ensure service')
    opener.add_argument('--label', action='append', default=None, metavar='WORD or KIND=WORD', help=f"a label: an act word, or a word that links the task to others (kinds {kinds_listing()}); may be repeated; add one only when another task is to be found by it. {TOPIC}=T is what the task is about: `claims` batches the queued tasks of one topic. A bare act word, {', '.join(ACTS)}, is a label of its own, written without a kind ({', '.join((word for word in Acts.titles() if word not in ACTS))} are refused): it says what act the task starts with, and only where the model it needs starts, `memar content_resolve_path {MODEL_RULE}` names the rule; a later act is a content posted with that word as its --kind. Not copied from --parent")
    opener.add_argument(DEPENDS_FLAG, action='append', default=None, metavar='REF', help=f"a task this one cannot start until it is Complete, ID or project/ID for a task of another project; may be repeated. Written to the plan's {PlanKey.DEPENDS_ON.written}; while one is not Complete the task is Blocked and cannot be claimed or started (`memar task_{DEPENDS_COMMAND.replace("-", "_")} --help`)")
    add_project_flags(opener, 'the project the task belongs to', required=True)
    return run

def run(args: argparse.Namespace) -> None:
    project = project_from_args(args)
    named = {} if project is None else {'project': project}
    if args.depends_on:
        named[PlanKey.DEPENDS_ON.key] = args.depends_on
    if args.label is not None:
        open_task(args.task_id, args.title, args.parent, args.queued, args.priority, args.label, **named)
    elif args.queued or args.priority is not None:
        open_task(args.task_id, args.title, args.parent, args.queued, args.priority, **named)
    else:
        open_task(args.task_id, args.title, args.parent, **named)
