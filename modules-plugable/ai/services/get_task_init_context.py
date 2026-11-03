#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
_m_fs_memar = import_module('modules-plugable.computer.memory.filesystem.services.fs_memar')
SKILL_RELATIVE = _m_fs_memar.SKILL_RELATIVE
import argparse
import re
import subprocess
import sys
Steps = import_module('modules-plugable.knowledge.documentation.plan.primitive.steps').Steps
from pathlib import Path
from typing import Callable
from machine.console import called_through_mcp, fail
from machine.console_parts import add_part_arguments, bound, next_command
from machine.console_parts import part_text as parted
from modules.knowledge.content.services.reference import content_root, read_text
_m_depends = import_module('modules-plugable.management.task.services.depends')
dependency_refusal = _m_depends.refusal
_m_folder = import_module('modules-plugable.management.task.services.folder')
folder_of = _m_folder.folder_of
is_task_folder = _m_folder.is_task_folder
_m_temp = import_module('modules-plugable.management.task.services.temp')
TEMP_SENTENCE = _m_temp.TEMP_SENTENCE
_m_ensure = import_module('modules-plugable.management.task.services.ensure')
ensure_task = _m_ensure.ensure_task
from modules.computer.software.edges.manifest.services.preferences import MOST_CHARACTERS_KEY, PREFERENCES_RELATIVE, most_characters_preference
_m_plan_file = import_module('modules-plugable.management.task.services.plan_file')
PLAN_NAME = _m_plan_file.PLAN_NAME
_m_task_files = import_module('modules-plugable.management.task.services.task_memory')
has_plan = _m_task_files.has_plan
plan_path = _m_task_files.plan_path
report_path = _m_task_files.report_path
plan_text = _m_task_files.plan_text
part_text = _m_plan_file.part_text
read_plan = _m_plan_file.read_plan
_m_plan_key = import_module('modules-plugable.knowledge.documentation.plan.primitive.plan_key')
PlanKey = _m_plan_key.PlanKey
_m_plan_labels = import_module('modules-plugable.management.task.services.plan_labels')
MODEL_RULE = _m_plan_labels.MODEL_RULE
TASK_KINDS = _m_plan_labels.TASK_KINDS
task_kind_of = _m_plan_labels.task_kind_of
_m_report_file = import_module('modules-plugable.management.task.services.report_file')
REPORT_NAME = _m_report_file.REPORT_NAME
_m_task_context = import_module('modules-plugable.ai.services.task_context')
Composed = _m_task_context.Composed
Ref = _m_task_context.Ref
context = _m_task_context.context
context_places = _m_task_context.context_places
write_record = _m_task_context.write_record
_m_task_kind = import_module('modules.management.task.labels.task_kind')
TaskKind = _m_task_kind.TaskKind
from modules.computer.software.primitive.project_name import ProjectName
from modules.computer.software.primitive.project_path import ProjectPath
_m_task_id = import_module('modules-plugable.management.task.primitive.task_id')
TaskId = _m_task_id.TaskId
START_COMMAND = 'get-task-init-context'
SKILL_FILE = (SKILL_RELATIVE / 'SKILL.md').as_posix()
SCRIPTS = _m_fs_memar.checkout_root() / 'bundles' / 'memar'
MEMAR = SCRIPTS / 'memar'
MARK = '==='
ALWAYS_HELP = (('task',), ('conversation', 'post'), ('content', 'write'))
CARD_LISTS_VERBS = (('task',),)
CARD_POINTER = 'Its verbs, each with its call shape, are on the card above (`=== commands ===`).'
commands = import_module('modules-plugable.computer.ui.command.command')
MOST_NAMED_COMMANDS = 8
HELP_TIMEOUT_SECONDS = 60
STEP_DOCUMENT = re.compile('(?<![\\w./-])/?((?:docs|modules|modules-plugable|bundles|\\.agents)/[\\w./-]+?\\.md)(?:#([\\w-]+))?')
NAMED_COMMAND = re.compile('`memar ([^`]+)`')
COMMAND_WORD = re.compile('[a-z][a-z-]*$')
MOST_COMMAND_WORDS = 3
ENDING = f"Do what the plan's Request says, without rewriting that Request. A read-only step takes no development or modeling act, so beyond what this prints it reads only what its step needs.\nEnd with its {REPORT_NAME} and Status as `memar task --help` says. Where you may write files, write the report of a task in the new shape (`task.yaml` and `content.NNNNN.md`) through `memar conversation post --timeline ID --kind report --content-file SCRATCHFILE`, SCRATCHFILE a file in the task's temp/ folder, which is never archived, so the report is not kept twice (a task in the old shape keeps `memar content write --create FILE --content-file SCRATCHFILE`). Where you may only return text, return the report as your final text, and the delegating task writes it as {REPORT_NAME} before its next step.\n{TEMP_SENTENCE}\n- A text of a task is added as a new content with `memar conversation post`, never written over; the current plan is the latest content of kind plan and the current report the latest of kind report; a fact of a task is changed through its store."

def marked_part(name: str, body: str) -> str:
    return marked_passages(name, [body])[0]

def marked_passages(name: str, blocks: list[str]) -> list[str]:
    kept = [block.strip() for block in blocks if block.strip()] or ['']
    kept[0] = f'{MARK} {name} {MARK}\n{kept[0]}'
    return [block + '\n' for block in kept]

def _task_part(task_id: str, folder: Path) -> str:
    return marked_part('task', f'task_id: {task_id}\npath: {folder}\nplan: {plan_path(folder)}\nreport: {report_path(folder)}')

def model_part(kind: str) -> str:
    rule = f'The model a task runs on follows what it needs, not its kind alone: the rule is {MODEL_RULE} (`memar content resolve-path {MODEL_RULE}` gives its path); the plan states the facts it reads.'
    too_weak = 'If you judge your reasoning too weak for this task, write that and why in its report, name the level you ran at and what it lacked, end Blocked, and ask for another agent one level above to take it up.'
    if kind in TaskKind.titles():
        body = f'kind: {kind}\n{rule} The kind is its starting point. {too_weak}'
    elif kind:
        body = f"kind: {kind}\n{kind!r} is not a kind; the kinds are {', '.join(TASK_KINDS)}. End Blocked saying so, for the task that handed you the task to correct it."
    else:
        body = f'kind: the plan states no kind.\n{rule} If its Request ideates, designs, or critiques, end Blocked saying the plan states no kind, for the delegator to state it. {too_weak}'
    return marked_part('model', body)

def _folder_part(folder: Path) -> str:
    entries = sorted(folder.rglob('*'), key=lambda path: path.relative_to(folder).as_posix().lower())
    lines = [path.relative_to(folder).as_posix() + ('/' if path.is_dir() else '') for path in entries]
    return marked_part('folder', '\n'.join(lines))

def step_documents(root: Path, steps: str) -> list[Ref]:
    found: list[Ref] = []
    for path, anchor in STEP_DOCUMENT.findall(steps):
        ref = Ref(root, path, anchor)
        if ref not in found:
            found.append(ref)
    return found

def documents(root: Path, kinds: list[TaskKind], named: list[Ref], project: Path | None) -> Composed:
    places, problems = context_places(root, project)
    return context(places, kinds, extra=named, project_named=project is not None, place_problems=problems)

def _kinds(kind: str) -> list[TaskKind]:
    found = TaskKind.read(kind)
    return [found] if found else []

def named_commands(plan: str) -> list[tuple[str, ...]]:
    found: list[tuple[str, ...]] = []
    for text in NAMED_COMMAND.findall(plan):
        words: list[str] = []
        for word in text.split():
            if not COMMAND_WORD.match(word) or len(words) == MOST_COMMAND_WORDS:
                break
            words.append(word)
        command = tuple(words)
        if command and command not in found and (command not in ALWAYS_HELP):
            found.append(command)
    return found

def _help_of(words: tuple[str, ...]) -> str | None:
    try:
        done = subprocess.run([sys.executable, str(MEMAR), *words, '--help'], capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=HELP_TIMEOUT_SECONDS)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return done.stdout.strip() if done.returncode == 0 and done.stdout.strip() else None

def _help_part(plan: str) -> list[str]:
    named = named_commands(plan)
    shown, left = (named[:MOST_NAMED_COMMANDS], named[MOST_NAMED_COMMANDS:])
    blocks = []
    for words in (*ALWAYS_HELP, *shown):
        command = 'memar ' + ' '.join(words)
        found = _help_of(words)
        if found is not None and words in CARD_LISTS_VERBS:
            found = found.split('\noptions:', 1)[0].rstrip() + '\n\n' + CARD_POINTER
        blocks.append(f'--- `{command} --help` ---\n' + (found if found is not None else f'no such command: `{command}`'))
    if left:
        blocks.append('--- not printed ---\n' + '\n'.join((f"`memar {' '.join(words)}`: ask `--help` of it" for words in left)))
    return marked_passages('help', blocks)

def start_passages(task_id: str, with_skill: bool=True) -> list[str]:
    folder = folder_of(task_id)
    if not is_task_folder(folder) or not has_plan(folder):
        fail(f'no task to start in {task_id}: it has no task folder with a {PLAN_NAME}. Open it with `memar task ensure --title T --parent ID {ProjectName.FLAG} {ProjectName.METAVAR}` (or `{ProjectPath.FLAG} {ProjectPath.METAVAR}`), ID the task handing it over, and write the task into its {PLAN_NAME} first')
    unmet = dependency_refusal(folder, 'start')
    if unmet:
        fail(unmet)
    _, folder = ensure_task(task_id)
    plan_file = plan_path(folder)
    plan = plan_text(folder)
    kind = task_kind_of(read_plan(folder / PLAN_NAME).front)
    root = content_root()
    composed = documents(root, _kinds(kind), step_documents(root, part_text(folder / PLAN_NAME, Steps.heading)), plan_project(task_id))
    write_record(folder, composed.printed)
    passages = [_task_part(task_id, folder), model_part(kind), marked_part(plan_file.name, plan), _folder_part(folder), *([marked_part('skill', read_text(root / SKILL_FILE))] if with_skill else []), *marked_passages('documents', composed.blocks), *([] if called_through_mcp() else [marked_part('commands', commands.card_text()), *_help_part(plan)]), marked_part('ending', ENDING)]
    return [passage + '\n' for passage in passages[:-1]] + passages[-1:]

def start_text(task_id: str, with_skill: bool=True) -> str:
    return ''.join(start_passages(task_id, with_skill))

def plan_project(task_id: str) -> Path | None:
    named = (read_plan(folder_of(task_id) / PLAN_NAME).front or {}).get(PlanKey.PROJECT.key, '').strip()
    return Path(named) if named else None

def get_task_init_context(task_id: str, with_skill: bool=True, part: int=1, most: int | None=None) -> None:
    words = ['memar', 'ai', START_COMMAND, TaskId.FLAG, task_id, *([] if with_skill else ['--without-skill'])]
    passages = start_passages(task_id, with_skill)
    limit = bound(most, most_characters_preference(plan_project(task_id)))
    sys.stdout.write(parted(passages, part, limit, next_command(words, most)))

def describe(verbs) -> Callable[[argparse.Namespace], None]:
    starter = verbs.add_parser(START_COMMAND, help='print, in one output, everything an agent taking up a task needs in its context', description=f"""For every agent that takes up a task: a sub-agent handed one, and the agent of a task after\n`ensure` opened its own. Print, in parts each opened by a line `=== NAME ===`, and in this\norder: the task's id and paths, the model its Kind needs, its {PLAN_NAME}, the folder's\nlisting, the Memar skill, the passages of Memar's documents the plan's Kind requires (as\n`memar content get-act-context --kind K` prints them; the core alone for a plan with no Kind) and\nthen the documents the plan's Steps name that those do not hold, the help of the commands\nevery task uses and those the plan names, and how to end. Run it first, once, and read\nnothing else before acting on the plan.\n\nA text too long for one tool output prints in ordered parts, each at most --most-characters\nlong: each part but the last ends with the exact command for the next (--part N), to run\nat once; read every part before acting. The same task prints the same parts, and each\npart says "part N of M of text H", H a hash of the whole text: a part naming another H\nis of another version of it.\n\nThe kinds a plan carries: {', '.join(TASK_KINDS)}.\n\nA task in the new shape holds contents: its plan is its latest content of kind plan and its report its latest of kind report, the paths printed above being those contents; a new plan or report is added with `memar conversation post`, never written over a content.\n\nIt is `ensure --task-id ID` as well, so the report and the role folders are there after it;\nit opens no new task, and refuses an ID that has no folder with a plan.""")
    TaskId.add_flag(starter, 'the task handed to you', required=True)
    starter.add_argument('--without-skill', action='store_true', help='leave the Memar skill out, for an agent whose runtime already loaded it')
    add_part_arguments(starter, f'the `{MOST_CHARACTERS_KEY}` in the {PREFERENCES_RELATIVE.as_posix()} of the project the plan names')
    return run

def run(args: argparse.Namespace) -> None:
    get_task_init_context(args.task_id, not args.without_skill, args.part, args.most_characters)
