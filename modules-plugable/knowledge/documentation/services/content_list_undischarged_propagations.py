#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
from importlib import import_module
import argparse
import sys
from pathlib import Path
_m_contents = import_module('modules-plugable.knowledge.documentation.services.contents_of_tasks')
_m_propagation = import_module('modules-plugable.knowledge.documentation.services.propagation')
from modules.knowledge.content.services.reference import content_root
COMMAND = 'list-undischarged-propagations'


def describe(verbs):
    verbs.add_parser(COMMAND, help='list the propagations a change record left Pending, as task#number:line hits', description='List the items of the `Propagates to` field that are still `Pending`, one `task#number:line: item` hit per line: the task whose timeline holds the content, the number of the content, the line of the item in it, and the item. Every changelog content of every task, live and archived, is read; an item is identified by the artifact it names, and the latest content naming it gives its state, so a later `Done` or `Rejected` closes it. What could not be read, and why, is printed on standard error.', formatter_class=argparse.HelpFormatter)
    return run


def run(args: argparse.Namespace) -> None:
    list_undischarged(content_root())


def list_undischarged(root: Path) -> None:
    notes: list = []
    found = _m_propagation.open_propagations(_m_contents.contents_of_tasks(root, notes))
    for note in notes:
        print(f'note: {note}', file=sys.stderr)
    if not found:
        print('(no undischarged propagations)')
        return
    for task_id, number, line, item in found:
        print(f'{task_id}#{number}:{line}: {item}')
