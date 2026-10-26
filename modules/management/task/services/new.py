#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/management/task/services/new.py — the verb `memar task ensure`: its help, and what it prints once a task's folder is open.

Why one folder per task, under ONE root. Parallel agent tasks edit one
shared working tree with no coordination, and concurrent writes to one file
collide silently — shared-tree collisions. The per-file advisory locks in
`modules-plugable/computer/memory/filesystem/services/fs_lock.py` answer that, and `memar content write` and `edit` take one,
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
`modules-plugable/computer/memory/filesystem/services/fs_memar.py`'s answer, and it fails closed rather than guessing.

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
put back in line. `--priority` says where in that line: written into a new
plan, or set on the one that is there (`task_plan`), so queuing and ranking
a task is one command. `--label KIND=WORD`, repeatable, says what the task is
about and what act it is, the same way (`task_plan_labels`); they are the
task's own, never copied from the parent's, since a copy would hide the
decision of what the new task is about. A topic is one the project declares;
a word declared nowhere is refused, naming the declared topics near it
(`plan_labels.checked_label`).

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
from machine.plugable_import import load as plugable_load
import argparse
from typing import Callable
from machine.console import note
from modules.process.project.services.find import add_project_flags, project_from_args
_m_plan_brief = plugable_load('ai.services.get_task_plan_carry_out_brief')
PLAN_BRIEF_COMMAND = _m_plan_brief.PLAN_BRIEF_COMMAND
brief_text = _m_plan_brief.brief_text
from modules.management.task.services.ensure import ENSURE_COMMAND, ensure_task, named_project, recorded_project
from modules.management.task.services.depends import DEPENDS_COMMAND
from modules.management.task.services.list import LIST_COMMAND
from modules.process.project.services.task_location import in_project_location, memar_own_note, project_location_note, unignored_note
from modules.management.task.services.plan_file import PLAN_NAME
from modules.management.task.services.plan_labels import CHEAPER_KINDS, STRONG_KINDS, TASK_KIND, TASK_KINDS, TOPIC, kinds_listing
from modules.management.task.labels.task_kind import TaskKind
from modules.management.task.plan.primitive.priority import Priority
from modules.management.task.primitive.record import REPORT
from modules.management.task.plan.primitive.plan_key import PlanKey
from modules.management.task.services.report_file import REPORT_NAME
from modules.management.task.services.temp import TEMP_SENTENCE
from modules.management.task.services.label_add import LABEL_COMMAND
from modules.management.task.services.label_list import LABELS_COMMAND
from modules.management.task.primitive.task_id import TaskId
_m_new_chats = plugable_load('ai.services.get_new_chats_ask')
NEW_CHATS_COMMAND = _m_new_chats.NEW_CHATS_COMMAND
DEPENDS_FLAG = f'--{DEPENDS_COMMAND}'

def open_task(task_id: str | None, title: str | None, parent: str | None, queued: bool=False, priority: int | None=None, labels: list[str] | None=None, project: str | None=None, depends_on: list[str] | None=None) -> None:
    """`ensure`: ensure the task folder and print its id, path, plan, and report, where it is when that is a project's, and with PARENT its brief."""
    sid, path = ensure_task(task_id, title, parent, queued, priority, labels, project, depends_on)
    note(f'task_id: {sid}')
    note(f'path: {path}')
    note(f'plan: {path / PLAN_NAME}')
    note(f'report: {path / REPORT_NAME}')
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
    if (parent or '').strip():
        note('brief:')
        note(f'    {brief_text(sid)}')
DESCRIPTION = f"""Ensure one task folder, for one task, and print its id, path, plan, and\nreport. Open one for work to be done, whose check is a change applied or a\ndecision recorded, before any other work of that task. A task whose outcome is\njust that it was done — committing, a rename, one edit, a lookup, a handful of\ntool calls — opens none and starts no sub-agent. An inquiry — looking into Memar or\nthe work to answer the task's own questions — opens none either: it is a step\nof the task it serves, and what it finds is a research note in that task's\ndocs/. A research that gathers and concludes what many other tasks will build\non, as Lexer's did, is a task of its own, recorded as a Research document. Open\na new task only for work that is truly independent. A problem found later in\na finished task's work goes back to that task's chat; a new task is\nfor work new in itself. Name the project with the flag for what you have, never\none in the other's place, and never turn a name you were told into a guessed\npath. A folder with no {PLAN_NAME} needs --title, one line saying what the task\nis; a folder that has one is continued as it is. Pass the printed id back as\n--task-id to continue the same task later. The path is absolute: use it\nas printed, and never make a folder of the same name elsewhere instead. If your\nfile tool cannot reach it, write there through `memar content write`.\n\nIt writes the folders the folder lacks, {PLAN_NAME} and {REPORT_NAME}, never\noverwriting one that is there. The plan's sections are Request (what was asked,\nand what checks it is done), Why (the reason, in your own words), Steps (each\nlocal or delegated, each naming the governing documents it reads and the tests\nit adds or runs: a step that names none cannot start) and Next (what the next\ntask does first); keep its Status line current as the task moves. Before you end, write the report: what ran, the\ncheck, the result, its Status. An agent that ends a task someone else will\nread hands back short: the report's Status and path, and, only when it needs a\ndecision, at most {REPORT.hand_back_max_lines} lines under `## {REPORT.hand_back_part}`.\n\nBefore handing work to another agent, decide where it runs by two questions, and\nwrite both answers in your plan for each task: does your conversation need\nits result, and does it need the owner during the work (questions, critique,\nback-and-forth)? Its result needed and the owner not: a sub-agent, which returns\nonly its hand-back. The owner needed, whether or not you wait for it: a new chat\n(`memar ai {NEW_CHATS_COMMAND}`). A chat opened for a task whose result your work does not need\nis then left alone: do not read it, poll it, ask it for news, or follow it up, because every\nlook spends your context for nothing and the owner answers its questions there; what a later\ntask needs is in that task's report. Its result not needed: independent, written\nwhole and then left: its chat opened or listed for the owner when it needs the\nowner, and otherwise a sub-agent once your own work leaves room, or, to only\nadd work, queued (below). A chat with nothing to ask the owner only gives the\nowner one more chat to watch. The owner's\nwords never pick: "open a task", "create a chat", "ask an agent" name the\nwork, not where it runs, and an agent app's own default does not pick either. A\nnew chat never reaches a stronger model: an app's tool that starts a chat gives\nit at most your own model, so work that needs a stronger one — research the\nowner wants brought back included — is a sub-agent with the model named.\n\nTo hand a task to a sub-agent: open its task with --parent (the task you\nwork in) and --label {TASK_KIND}=KIND, write the whole task into its {PLAN_NAME} — Request, the\ncheck that says it is done, the shape of its report, and Why — and hand the\nsub-agent only the brief `ensure` prints, which `memar ai {PLAN_BRIEF_COMMAND} ID` prints\nagain. Nothing else goes in the hand-over. Name the model when you start it: an\napp's default may be weaker than the kind needs. While it works, do what its result cannot\nchange and wait for the rest, as you would for the owner's answer. A task may\nstop at any time and for any time, as an issue may: one that stops to wait on\nanother records it in its plan's Depends_on (`{DEPENDS_COMMAND}`) and is Blocked.\n\nTo only add work, open each task with --queued and a --priority and a --label {TOPIC}=T\n(`memar label {LABELS_COMMAND}` lists them; `memar label {LABEL_COMMAND}` adds or removes one\nlater), write its {PLAN_NAME}, then leave it: never do a queued task's work\nin your own context. A question only the owner can answer is not a task: write\nit in the handoff of the document it concerns.\n\nTo continue a task another task left, find it with `memar task {LIST_COMMAND}`,\nopen it with `--task-id ID`, and start from its Next."""

def describe(verbs) -> Callable[[argparse.Namespace], None]:
    """`memar task ensure`."""
    opener = verbs.add_parser(ENSURE_COMMAND, help='ensure one task folder for one task and print its id and path', description=DESCRIPTION)
    TaskId.add_flag(opener, 'reuse this task id instead of minting one (rerun is idempotent)')
    opener.add_argument('--title', default=None, help=f'one line saying what the task is; required unless the folder has a {PLAN_NAME}')
    opener.add_argument('--parent', default=None, metavar='ID', help='the task this task came from: the delegating task, or the previous task of the conversation')
    opener.add_argument('--queued', action='store_true', help='leave the task queued for an agent to claim rather than open for you: a new plan is written queued, and an existing active one no one has claimed is queued')
    opener.add_argument('--priority', type=int, default=None, metavar='N', help=f'how soon a queued task is taken, {Priority.range_words()}: the higher goes sooner; {Priority.default_words()}')
    opener.add_argument('--label', action='append', default=None, metavar='KIND=WORD', help=f"a word that links the task to others (kinds {kinds_listing()}); may be repeated; add one only when another task is to be found by it. {TOPIC}=T is what the task is about: `claims` batches the queued tasks of one topic. {TASK_KIND}=K is what it is: {', '.join(TASK_KINDS)} ({', '.join((word for word in TaskKind.words() if word not in TASK_KINDS))} are refused); {', '.join(CHEAPER_KINDS)} runs on a cheaper model, the others on the strongest the runtime offers. Not copied from --parent")
    opener.add_argument(DEPENDS_FLAG, action='append', default=None, metavar='REF', help=f"a task this one cannot start until it is Complete, ID or project/ID for a task of another project; may be repeated. Written to the plan's {PlanKey.DEPENDS_ON.written}; while one is not Complete the task is Blocked and cannot be claimed or started (`memar task {DEPENDS_COMMAND} --help`)")
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
