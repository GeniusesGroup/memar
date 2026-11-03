#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/management/task/services/ids_source.py — where the rows a listing of task ids is cut from are read.

The abstraction is `protocol/task-ids-source.kh`. This is its one realization
today, over what `find_tasks` reads; the listing in `ids.py` knows no folder,
no plan and no branch, only rows, so a store that answers a page by itself
replaces this file and nothing else. A task's status is one of its labels
(`Label_Status`), so it is read here as a label and the listing has no
status of its own: the label domain owns that concept.
"""
from __future__ import annotations
from importlib import import_module
from typing import NamedTuple
from modules.knowledge.label.primitive.label import Label
from modules.knowledge.label.labels.Status import Label_Status
_m_list = import_module('modules-plugable.management.task.services.list')
find_tasks = _m_list.find_tasks
_m_plan_labels = import_module('modules-plugable.management.task.services.plan_labels')
labels_of = _m_plan_labels.labels_of

class TaskRow(NamedTuple):
    id: str
    words: str
    labels: tuple[Label, ...]
    parent: str
    conversation: str

def status_label(status: str) -> tuple[Label, ...]:
    member = Label_Status.read(status) if status else None
    return (Label(member.title, member.id),) if member is not None else ()

def records_rows(project=None) -> list[TaskRow]:
    """Every task the records read, as rows."""
    rows = []
    for task in find_tasks(project=project):
        front = task.front or {}
        words = ' '.join((task.id, front.get('title', ''), front.get('project', '')))
        rows.append(TaskRow(task.id, words, (*labels_of(task.front), *status_label(task.status)), task.parent, task.conversation))
    return rows
