#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/management/task/services/claims.py — the N queued tasks first in line, made one agent's.

Why through `try_claim`. Taking the N first in line is the act `claim`
does — the exclusive create, the status moved — tried on several tasks in
turn, so each is taken by `task_claim.try_claim` and by nothing here: one
place takes a task, not two that could take it two ways. `claims` tries the
queued tasks in line order and skips any another caller won meanwhile, so
two callers asking at once each get tasks, never the same one.

Why that line. The plan's priority first, the higher sooner (`task_plan`),
then the oldest opened, so among equals what has waited longest goes first;
the id breaks a tie in time. A queued plan whose Request is still empty has
not been written yet — its task was opened queued before its task was —
and is passed over until it is. N is the caller's: the owner says how much
work a night holds ("do five tonight"), the agent passes 5, and nothing here
defaults or caps it, since a cap here would be a policy no one chose.

Why the first task's topic pulls the batch. An agent given several tasks of one
subject keeps its context on that subject, so the batch is one subject when the
queue allows, which accepts that strict
priority is disturbed for it. The first task is the first in line, as ever,
and is never displaced; its first `Topic` label (`task_plan_labels`) is the
batch's, and the rest of the N are the queued tasks that carry that label, in
line order; a task either carries it or does not, whatever other topics it has. Other tasks do not
fill the remainder, since the owner's reason, focus, argues against it, unless
the caller passes `fill`, which takes the next in line once the topic is used
up. `--label Topic=T` names the topic in place of the first task's, for a caller whose
context is already about it. A first task with no topic leaves the line as it
was. An unrelated task is overtaken only by the batch of one call: the next
call starts again from the first in line, so a high-priority task is never
passed, being always the first of its call; and what a batch passed over is
printed, so the displacement is seen. No counter of displacements is kept; the
owner can ask for one if displacement is seen in use.

Why Memar starts no agent. How an agent runtime starts a sub-agent is the
runtime's, known to the agent already in a conversation and to nothing else;
so `claims` prints, for each task it took, the brief that hands it over
(`plan_brief`), and the agent that called it delegates each one the way its
runtime does.

Why the project is named, never defaulted. One run of `claims` serves one
project: the tasks it takes become one agent's work, landing in that
project. A default — Memar's own folder, every project's, or the current
folder's guessed — would hide which project the work lands in, and taking from
two projects at once would mix their work in one run. So the caller names the
project with `--project`, and `claims` refuses without it; an agent that does
not know the project asks the owner rather than guessing.
"""
from __future__ import annotations
from importlib import import_module
from machine.plugable_import import load as plugable_load
import argparse
_m_plan_part = import_module('modules-plugable.knowledge.documentation.plan.primitive.plan_part')
PlanPart = _m_plan_part.PlanPart
from typing import Callable
from machine.console import fail, note
from modules.knowledge.status.primitive.status import Status
_m_plan_brief = plugable_load('ai.services.get_task_plan_carry_out_brief')
brief_text = _m_plan_brief.brief_text
_m_claim = import_module('modules-plugable.management.task.services.claim')
CLAIM_COMMAND = _m_claim.CLAIM_COMMAND
try_claim = _m_claim.try_claim
_m_dependency = import_module('modules-plugable.management.task.services.dependency')
DependsOn = _m_dependency.DependsOn
Reader = _m_dependency.Reader
_m_depends = import_module('modules-plugable.management.task.services.depends')
problems = _m_depends.problems
reconcile_all = _m_depends.reconcile_all
from modules.process.project.services.find import add_project_flags, project_from_args
_m_task_get_decisions_digest = plugable_load('ai.services.task_get_decisions_digest')
DIGEST_COMMAND = _m_task_get_decisions_digest.DIGEST_COMMAND
_m_list = import_module('modules-plugable.management.task.services.list')
LIST_COMMAND = _m_list.LIST_COMMAND
find_tasks = _m_list.find_tasks
project_of = _m_list.project_of
_m_folder = import_module('modules-plugable.management.task.services.folder')
Task = _m_folder.Task
_m_temp = import_module('modules-plugable.management.task.services.temp')
TEMP_SENTENCE = _m_temp.TEMP_SENTENCE
_m_plan_file = import_module('modules-plugable.management.task.services.plan_file')
PLAN_NAME = _m_plan_file.PLAN_NAME
part_text = _m_plan_file.part_text
_m_priority = import_module('modules-plugable.knowledge.documentation.plan.primitive.priority')
Priority = _m_priority.Priority
from modules.knowledge.label.primitive.topic import Topic
_m_plan_labels = import_module('modules-plugable.management.task.services.plan_labels')
TOPIC = _m_plan_labels.TOPIC
topics_of = _m_plan_labels.topics_of
_m_record = import_module('modules-plugable.knowledge.documentation.primitive.record')
REPORT = _m_record.REPORT
_m_report_file = import_module('modules-plugable.management.task.services.report_file')
REPORT_NAME = _m_report_file.REPORT_NAME
from modules.process.project.primitive.project_name import ProjectName
from modules.process.project.primitive.project_path import ProjectPath
_m_plan_key = import_module('modules-plugable.knowledge.documentation.plan.primitive.plan_key')
PlanKey = _m_plan_key.PlanKey
CLAIMS_COMMAND = 'claims'
PROJECT_REQUIRED = f'{CLAIMS_COMMAND} needs {ProjectName.either_words()}: one run serves one project, and naming it keeps the work from landing in a project no one chose; if you do not know which project the tasks are for, ask the owner'

def in_line(project: str) -> list[Task]:
    """The queued tasks of PROJECT in the order `claims` takes them: highest priority, then oldest opened, then id.

    That project's wherever they lie, as `list --project` finds them
    (`task_find`); PROJECT is a name or a folder, and an empty one is refused.
    Their Status is first brought up to date with their dependencies, so a
    task that waits for another is Blocked and not in line, and one whose
    dependencies are all Complete is queued and in it (`task_depends`).
    """
    reconcile_all(find_tasks(project=project_of(project)))
    queued = find_tasks(status=Status.QUEUED.key, project=project_of(project))
    return sorted(queued, key=lambda task: (-Priority.of(task.front), (task.front or {}).get(PlanKey.START_DATE.key, ''), task.id))

def held_back(project: str) -> None:
    """Say, for each Blocked task of PROJECT waiting for its dependencies, that it is passed over and for which."""
    reader = Reader(None)
    for task in find_tasks(status=Status.BLOCKED.key, project=project_of(project)):
        if DependsOn.of(task.front) and (unmet := problems(task, reader)):
            print(f"{task.id}  waiting: {', '.join(unmet)}")

def first_topic(task: Task) -> str:
    """The first topic TASK carries; empty when it has none."""
    return next(iter(topics_of(task.front)), '')

def take(count: int, project: str, topic: str | None=None, fill: bool=False) -> list[Task]:
    """Claim up to COUNT queued tasks of PROJECT in line order, by topic; the ones taken.

    TOPIC, when named, is the batch's topic from the start. Otherwise the first
    task taken sets it: when it has one, only that topic's tasks are
    taken after it; with none, the line is followed as it is. With FILL, the
    tasks not of the topic are taken once its own are used up. A task
    passed over as not ready or not taken is said once.
    """
    taken: list[Task] = []
    tried: set[str] = set()
    batch: str | None = Topic.checked(topic) if topic is not None else None

    def attempt(task: Task) -> None:
        tried.add(task.id)
        if not part_text(task.path / PLAN_NAME, PlanPart.REQUEST.heading):
            print(f'{task.id}  not ready: its Request is empty')
            return
        why = try_claim(task.path)
        if why:
            print(f'{task.id}  not taken: {why}')
            return
        taken.append(task)
    line = in_line(project)
    held_back(project)
    for task in line:
        if len(taken) >= count:
            break
        if batch and batch not in topics_of(task.front):
            continue
        attempt(task)
        if batch is None and taken:
            batch = first_topic(taken[0])
    if fill:
        for task in line:
            if len(taken) >= count:
                break
            if task.id not in tried:
                attempt(task)
    return taken

def batch_report(taken: list[Task], count: int, project: str, topic: str | None) -> list[str]:
    """The lines saying the batch's topic, what waits under it, and what it passed over; none when the batch has no topic."""
    batch = Topic.checked(topic) if topic else first_topic(taken[0])
    if not batch:
        return []
    own = sum((1 for task in taken if batch in topics_of(task.front)))
    waiting = [task for task in in_line(project) if part_text(task.path / PLAN_NAME, PlanPart.REQUEST.heading)]
    under = sum((1 for task in waiting if batch in topics_of(task.front)))
    said = f'batch topic: {batch} ({own} of {count} asked'
    if own < len(taken):
        said += f'; {len(taken) - own} more filled from other topics'
    if under:
        said += f'; {under} more queued under it are not taken only because N was reached'
    lines = [said + ')']
    lowest = min((Priority.of(task.front) for task in taken))
    passed = [task for task in waiting if batch not in topics_of(task.front) and Priority.of(task.front) > lowest]
    if passed:
        listed = ', '.join((f'{task.id} (priority {Priority.of(task.front)})' for task in passed))
        lines.append(f'passed over for topic: {listed}')
    return lines

def claims(count: int, project: str | None, topic: str | None=None, fill: bool=False) -> list[str]:
    """`claims`: claim the COUNT queued tasks of PROJECT first in line, and print what hands each over; their ids.

    PROJECT None — no project named — is refused (`PROJECT_REQUIRED`). The
    batch follows the first task's topic, or TOPIC when named; FILL takes the
    next in line once that topic is used up (`take`).
    """
    if project is None:
        fail(PROJECT_REQUIRED)
    if count < 1:
        fail(f'{CLAIMS_COMMAND} N counts the tasks to take; N is at least 1')
    taken = take(count, project, topic, fill)
    if not taken:
        note('no queued task to claim' + (f' under topic {Topic.checked(topic)}' if topic else ''))
        return []
    print(f'claimed {len(taken)} of {count}')
    note(TEMP_SENTENCE)
    for line in batch_report(taken, count, project, topic):
        print(line)
    for task in taken:
        print()
        print(f"{task.id}  {(task.front or {}).get('title', '')}")
        note(f'priority: {Priority.of(task.front)}')
        if topics_of(task.front):
            note(f"topics: {', '.join(topics_of(task.front))}")
        note(f'plan: {task.path / PLAN_NAME}')
        note(f'brief: {brief_text(task.id)}')
    return [task.id for task in taken]

def describe(verbs) -> Callable[[argparse.Namespace], None]:
    """`memar task claims`."""
    taker = verbs.add_parser(CLAIMS_COMMAND, help='take the N queued tasks first in line, and print the brief for each', description=f"""Take the N queued tasks first in line — the highest priority first,\nthe oldest opened first among equals — and claim each for yourself, as\n`claim` does. The first is the first in line; when it has a topic\n(a `Topic` label, `memar label add`), the rest are the queued tasks\nthat carry that topic, in\nline order, so one agent works one subject, even where that takes\nlower-priority tasks ahead of unrelated ones that rank above them.\nOther tasks do not fill what is left, unless --fill. --label Topic=T names\nthe topic instead of the first task's. A first task with no topic\nkeeps the plain line. The output states the batch topic and lists the\nhigher-priority tasks passed over. For each task taken it prints\nits id and title, its priority and topic, its plan, and the brief to\nhand one fresh sub-agent per batch of one topic. N is\nyours to choose, from what you were asked: there is no default and no\ncap. Fewer queued than N is not an error: you get what there is. A\nqueued plan whose Request is empty is not ready and is passed over,\nand so, saying why, is one another agent took meanwhile.\n{ProjectName.either_words()} is required: one run serves one project, so it takes only\nthat project's queued tasks, wherever they lie, and never mixes two\nprojects'; there is no default project and no way to take from all.\n"Do 5 tasks of X" means `claims 5 {ProjectName.FLAG} X` (or `{ProjectPath.FLAG}` with its folder); if you do not know\nwhich project the tasks are for, ask the owner rather than guess.\nTwo agents asking at once never get the same task.\n\nWhen you are asked to do some of the queued tasks — "do some of the\nqueued tasks", "do 5 tasks of project X" — work them this way, as the\nagent that takes them:\n\n  1. `memar task {LIST_COMMAND} --status queued` shows what waits, each with\n     its priority; add {ProjectName.FLAG} {ProjectName.METAVAR} (or {ProjectPath.FLAG} {ProjectPath.METAVAR}) for one\n     project's.\n  2. `claims N {ProjectName.FLAG} X` takes them and prints a brief for each;\n     `memar task {CLAIM_COMMAND} ID` takes one named task instead.\n  3. Hand the batch of one topic to one fresh sub-agent, as your runtime\n     starts one, each task keeping its own {PLAN_NAME} and {REPORT_NAME} and\n     the sub-agent working them one after another; a batch of another\n     topic goes to another sub-agent: never in your own context, and\n     never one sub-agent for tasks of different topics. Memar starts\n     no agent: you do.\n  4. When each ends, read its {REPORT_NAME}: its Status and its\n     {REPORT.hand_back_part}. Its Status must equal its plan's: a sub-agent that\n     could only return text hands back the report, and you write it as\n     its {REPORT_NAME} and set its Status. A report with no Status, more\n     lines than allowed, or a Status that disagrees with its plan, is a\n     failed hand-back: say so, and do not count that task done.\n  5. Last, run `memar task {DIGEST_COMMAND} --conversation ID`, ID your own\n     task's, and give the owner that one digest rather than a\n     question per task.""")
    taker.add_argument('count', type=int, metavar='N', help='how many queued tasks to take, at least 1')
    add_project_flags(taker, 'the project whose queued tasks to take, as `list` finds them', required=True)
    taker.add_argument('--label', default=None, metavar='Topic=T', help="take the queued tasks that carry the topic T instead of those of the first task's topic")
    taker.add_argument('--fill', action='store_true', help="when the topic's tasks are used up before N, take the next in line, whatever its topic")
    return run

def batch_topic(text: str | None) -> str | None:
    """The topic a `--label` names, `Topic=T`; refused when it names a label of another kind, since a batch is of one topic."""
    if text is None:
        return None
    kind, found, word = text.partition('=')
    if not found or kind.strip() != TOPIC:
        fail(f'a batch is of one topic: --label {TOPIC}=T, not {text!r}')
    return Topic.checked(word)

def run(args: argparse.Namespace) -> None:
    if args.label is not None or args.fill:
        claims(args.count, project_from_args(args), batch_topic(args.label), args.fill)
    else:
        claims(args.count, project_from_args(args))
