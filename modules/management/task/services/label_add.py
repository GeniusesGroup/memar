#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/management/task/services/label_add.py — a task's label added or removed.

Why a verb of its own, as `priority` is. What a task is about is known when it
is queued, but is also seen later: the owner reads the labels in use
(`memar label list`) and finds a task filed under too wide a subject. Anyone
may re-label it, so it is a verb, not a hand edit that would be one more place
the block could be written two ways. What a label is, how a plan carries it,
and which words a plan may take are `plan_labels.py`'s; this file finds the
task and says what changed.

Why an undeclared topic is refused and not written. A topic is declared as
code by the domain whose it is ([Label → Where labels are declared](../../../knowledge/label/label.md#where-labels-are-declared)),
with the sentence that says what it means, so a new subject is that
declaration, written where it belongs; a word written here first would be a
label nobody defined, and a typo would split one subject in two for `claims`.
The refusal names the declaration to write and the declared topics near the
word, so a typo is met by the word meant.

Removal takes out a label the plan carries even when its word is declared
nowhere, so a plan written by hand can always be cleaned. A label is added
only when another task is to be found by it, and a plan takes as many as it
needs. Any status is accepted, as a priority is: a task open or blocked now may
be queued later.
"""
from __future__ import annotations
import argparse
from typing import Callable
from machine.console import fail
from machine.modules_import import load as modules_load
_task_folder = modules_load('management', 'task', 'services', 'folder')
folder_of = _task_folder.folder_of
is_task_folder = _task_folder.is_task_folder
from modules.management.task.services.plan_file import PLAN_NAME, read_plan
from modules.management.task.services.plan_labels import add_label, checked_label, kinds_listing, label_to_remove, labels_of, project_of, remove_label
from modules.management.task.primitive.task_id import TaskId
LABEL_COMMAND = 'add'

def carried(task_id: str, plan: Path) -> str:
    """What the plan at PLAN carries, one line: `labels: docs, design`, or `labels: (none)`."""
    labels = labels_of(read_plan(plan).front)
    return f'{task_id}  labels: ' + (', '.join((label.word for label in labels)) or '(none)')

def set_task_label(task_id: str, text: str, remove: bool) -> None:
    """`label`: add the label TEXT (`KIND=WORD`) to TASK_ID's plan, or with REMOVE take it out, and say what the plan carries now."""
    folder = folder_of(task_id)
    plan = folder / PLAN_NAME
    if not is_task_folder(folder) or not plan.is_file():
        fail(f"no task {task_id} with a {PLAN_NAME}, so there is no label to {('remove' if remove else 'add')}")
    front = read_plan(plan).front
    project = project_of(front)
    if remove:
        label = label_to_remove(text, project, labels_of(front))
        if label is None:
            print(f"{task_id}  does not carry {text.partition('=')[2].strip()}")
        else:
            has = any((item.id == label.id for item in labels_of(front)))
            remove_label(plan, label)
            print(f'{task_id}  removed {label.word}' if has else f'{task_id}  does not carry {label.word}')
    else:
        label = checked_label(text, project)
        has = any((item.id == label.id for item in labels_of(front)))
        add_label(plan, label)
        print(f'{task_id}  added {label.word}' if not has else f'{task_id}  already carries {label.word}')
    print(carried(task_id, plan))

def describe(verbs) -> Callable[[argparse.Namespace], None]:
    """`memar label add`."""
    tagger = verbs.add_parser(LABEL_COMMAND, help='add a label to a task, or remove one', description=f"Add the label KIND=WORD to the task ID's plan, or with --remove take\nit out. A label links the task to others outside the structure of\ntheir ids: Topic=T is the subject the task is about, so that `claims`\nhands one agent the queued tasks of one topic; TaskKind=K is the act the\ntask is. The kinds are {kinds_listing()}. A topic is written in\nlower case with spaces as hyphens, and is one the project declares as\ncode: by the module it names, or, for a stream of work, by the task\ndomain, in a `labels/` folder. A word declared nowhere is refused with\nthe declaration to write and the declared topics near it, and an ended\ntopic with the ones that replaced it; `memar label list` lists the\ndeclared topics and the labels in use: run it first, to reuse a topic\nrather than write the same subject another way. A plan takes as many labels as it needs and none it does not: add one\nonly when another task is to be found by it. Labels are not copied\nfrom a task's parent. Anyone may change them, whatever the task's\nstatus.")
    TaskId.add_positional(tagger, 'the task to label')
    tagger.add_argument('label', metavar='KIND=WORD', help='the label to add, e.g. Topic=memar-scripts')
    tagger.add_argument('--remove', action='store_true', help='take the label out instead of adding it')
    return run

def run(args: argparse.Namespace) -> None:
    set_task_label(args.task_id, args.label, args.remove)
