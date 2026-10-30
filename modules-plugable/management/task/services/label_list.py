#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/management/task/services/label_list.py — the labels a project's tasks carry, by kind, with how many, and the topics it declares.

Why a listing. A topic is declared by the domain whose it is
(`modules/knowledge/label/primitive/topic.py`), in files spread over
the project's modules, so whoever queues a task needs one place that shows
them, to reuse one rather than declare the same subject a second way, and the
owner needs to see what is waiting by subject. The counts are read from the
plans, as `list` is, the words from the declarations, and both are kept
nowhere else. A declared topic no task carries is listed with none; a label a
plan carries that nothing declares is listed as undeclared, by the word the
plan wrote.

A project is named as `list --project` names it: a name the registry resolves, or
a folder whose project is meant; the folder the command runs in is never read. Every task of the project is counted,
wherever its folder lies and whatever its status, with how many of them are
queued, since the queued ones are what `claims` batches by topic. The largest
first, then by kind and word, so the order does not depend on the order folders were read.
"""
from __future__ import annotations
import argparse
from typing import Callable
from machine.console import fail, note
from modules.knowledge.status.primitive.status import Status
from modules.process.project.services.find import add_project_flags, project_from_args
from machine.modules_import import load as modules_load
_task_list = modules_load('management', 'task', 'services', 'list')
_task_folder = modules_load('management', 'task', 'services', 'folder')
find_tasks = _task_list.find_tasks
project_of = _task_list.project_of
Task = _task_folder.Task
from modules.management.task.services.plan_labels import TOPIC, labels_of, registry_for
from modules.process.project.primitive.project_name import ProjectName
LABELS_COMMAND = 'list'
UNDECLARED = 'undeclared'
PROJECT_REQUIRED = f'{LABELS_COMMAND} needs {ProjectName.either_words()}: name the project whose labels to list'

def labels_in_use(project) -> dict[str, list[Task]]:
    """The labels PROJECT's tasks carry and the topics it declares, each written `Kind: word` (an ended one with `(ended)`), with its tasks."""
    registry = registry_for(project)

    def written(label) -> str:
        definition = registry.definition(label)
        if definition is None or not definition.takes:
            return f'{UNDECLARED}: {label}'
        return f"{definition.takes[0].word}: {definition.label.word}" + (' (ended)' if definition.ended else '')
    found: dict[str, list[Task]] = {written(definition.label): [] for definition in registry.definitions(TOPIC)}
    for task in find_tasks(project=project):
        for label in dict.fromkeys((written(label) for label in labels_of(task.front))):
            found.setdefault(label, []).append(task)
    return found

def list_labels(project: str | None) -> None:
    """`labels`: print each label of PROJECT's tasks and each topic it declares with its counts, or say that none is; a missing or empty PROJECT is refused."""
    if project is None:
        fail(PROJECT_REQUIRED)
    found = labels_in_use(project_of(project))
    if not found:
        note('no label in use or declared in this project')
        return
    for label, tasks in sorted(found.items(), key=lambda item: (-len(item[1]), item[0])):
        queued = sum((1 for task in tasks if task.status == Status.QUEUED.key))
        count = f'{len(tasks)} task' + ('' if len(tasks) == 1 else 's')
        print(f'{label}  {count}, {queued} queued')

def describe(verbs) -> Callable[[argparse.Namespace], None]:
    """`memar label list`."""
    lister = verbs.add_parser(LABELS_COMMAND, help="list the labels a project's tasks carry, with how many", description=f"List the labels the project's tasks carry and the topics the project\ndeclares, each written Kind: word, the most used first, each with how\nmany tasks have it and how many of those are queued; a label nothing\ndeclares is written {UNDECLARED}: word(id). Use it before queuing a task,\nto reuse a topic rather than declare the same subject another way. {ProjectName.either_words()} names the\nproject; one is required, and the current folder is never read.")
    add_project_flags(lister, 'the project whose labels to list', required=True)
    return run

def run(args: argparse.Namespace) -> None:
    list_labels(project_from_args(args))
