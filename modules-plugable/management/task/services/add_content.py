#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
from importlib import import_module
import argparse
import sys
from pathlib import Path
from typing import Callable
from machine.console import fail
_m_folder = import_module('modules-plugable.management.task.services.folder')
folder_of = _m_folder.folder_of
is_task_folder = _m_folder.is_task_folder
_m_task_files = import_module('modules-plugable.management.task.services.task_files')
AUTHOR = _m_task_files.AUTHOR
OLD_SHAPE_READER = _m_task_files.OLD_SHAPE_READER
has_task = _m_task_files.has_task
is_new = _m_task_files.is_new
read_facts = _m_task_files.read_facts
stores_at = _m_task_files.stores_at
_m_errors = import_module('modules-plugable.management.task.errors.errors')
Task_Error_Changed = _m_errors.Task_Error_Changed
Task_Error_NotFound = _m_errors.Task_Error_NotFound
_m_content_add = import_module('modules-plugable.management.task.services.task_content_add')
add_text = _m_content_add.add_text
_m_plan_labels = import_module('modules-plugable.management.task.services.plan_labels')
TOPIC = _m_plan_labels.TOPIC
checked_label = _m_plan_labels.checked_label
registry_for = _m_plan_labels.registry_for
_m_task_id = import_module('modules-plugable.management.task.primitive.task_id')
TaskId = _m_task_id.TaskId
from modules.knowledge.label.primitive.label import LabelProblem
ADD_CONTENT_COMMAND = 'add-content'
FIXED_KINDS = ('plan', 'report', 'changelog', 'message')
KIND_FLAG = '--kind'


def checked_kind(kind: str, project: Path | None) -> str:
    word = kind.strip()
    if word in FIXED_KINDS:
        return word
    registry = registry_for(project)
    for name in registry.kinds:
        try:
            label, fresh = registry.resolve(f'{name}={word}')
        except LabelProblem:
            continue
        if fresh is None:
            return label.word
    checked_label(f'{TOPIC}={word}', project, registry)
    return word


def _text(content_file: str | None) -> str:
    if content_file:
        try:
            return Path(content_file).read_bytes().decode('utf-8-sig')
        except OSError as problem:
            fail(f'{content_file} cannot be read: {problem}')
    return sys.stdin.buffer.read().decode('utf-8-sig') if hasattr(sys.stdin, 'buffer') else sys.stdin.read()


def add_task_content(task_id: str, kind: str, content_file: str | None, author: str | None) -> int:
    folder = folder_of(task_id)
    if not is_task_folder(folder) or not has_task(folder):
        fail(f'no task {task_id}, so there is nothing to add a content to')
    if not is_new(folder):
        fail(f'task {task_id} is in the old shape (plan.md and report.md), which {OLD_SHAPE_READER} reads; a content cannot be added to it and nothing was written')
    project = (read_facts(folder) or {}).get('project', '').strip()
    word = checked_kind(kind, Path(project) if project else None)
    text = _text(content_file)
    try:
        number = add_text(stores_at(folder), None, task_id, word, text, author or AUTHOR)
    except Task_Error_Changed:
        fail(f'another content of kind {word} was added to task {task_id} meanwhile, so nothing was written; add it again')
    except Task_Error_NotFound:
        fail(f'no task {task_id} in the shape that holds contents, so nothing was written')
    print(f'{task_id}  added content {number} of kind {word}')
    return number


def describe(verbs) -> Callable[[argparse.Namespace], None]:
    adder = verbs.add_parser(ADD_CONTENT_COMMAND, help='add a text to a task as a content of a kind', description=f"Add a text to the task as its next content of the kind KIND, and print\nthe number of the new content. A task has contents: each text it holds is\none, numbered in the order added, and a text is added and never written\nover. The current plan of a task is its latest content of kind plan, its\ncurrent report the latest of kind report; to change either, add a new one.\nKIND is a word of the label module: plan, report, changelog, message, a\ntask kind, or a word the project declares (`memar label list`); any other\nword is refused as the label module refuses an undeclared one. The text is\nany text: this verb does not know a plan from a report and checks it\nagainst no template, which is the caller's. It is read from --content-file,\nor from standard input when none is given. The author defaults to the agent\nname '{AUTHOR}', never to a person. A task in the old shape (plan.md and\nreport.md) is refused and nothing is written to it. When another content of\nthe kind is added between the read and the write, nothing is written and\nthe call is refused: add it again.")
    TaskId.add_flag(adder, 'the task to add the content to', required=True)
    adder.add_argument(KIND_FLAG, required=True, metavar='KIND', help='the label word of the template the text is written to: plan, report, changelog, message, or a word the project declares')
    adder.add_argument('--content-file', default=None, metavar='FILE', help='the file holding the text; standard input when not given')
    adder.add_argument('--author', default=None, metavar='A', help=f"who wrote the text; the agent name '{AUTHOR}' when not given")
    return run


def run(args: argparse.Namespace) -> None:
    add_task_content(args.task_id, args.kind, args.content_file, args.author)
