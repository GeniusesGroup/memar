#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
from importlib import import_module
import argparse
import re
import sys
from pathlib import Path
_m_contents = import_module('modules-plugable.knowledge.documentation.services.contents_of_tasks')
_m_refs = import_module('modules-plugable.knowledge.documentation.services.content_refs')
QUESTION_KIND = 'question'
BLOCKING_MARK = '[blocks]'
EMPTY = '(no open questions)'
NO_DATE = '9999-99-99'
_HEADING = re.compile('^#{1,6}\\s+(.*?)\\s*#*\\s*$')
_BLOCKS = re.compile('^\\s*-\\s+\\*{0,2}Blocks(?: continuation)?\\*{0,2}\\s*:\\s*(.*)$', re.I)
_ASKED = re.compile('^\\s*-\\s+\\*{0,2}Asked\\*{0,2}\\s*:\\s*(\\d{4}-\\d{2}-\\d{2})', re.I)
_NO = re.compile('^(no|none|nothing)\\b', re.I)
_YES = re.compile('\\byes\\b', re.I)


def describe(verbs):
    from modules.computer.software.primitive.project_name import ProjectName
    from modules.computer.software.primitive.project_path import ProjectPath
    parser = verbs.add_parser('questions', help='list the open questions of the tasks as task#number: heading hits', description=f'List the contents of kind question that no later content refers to, one `task#number: heading` hit per line, blocking ones first (marked [blocks]), then by task and number. Every task of the project is read; {ProjectName.FLAG} {ProjectName.METAVAR} names a project by a name `memar project list` shows, {ProjectPath.FLAG} {ProjectPath.METAVAR} by its folder. No flag means the checkout. What could not be read, and why, is printed on standard error.', formatter_class=argparse.HelpFormatter)
    from modules.computer.software.services.project_find import add_project_flags
    add_project_flags(parser, 'read this project instead of the checkout')
    parser.add_argument('--blocking', action='store_true', help='list only questions that block')
    return run


def run(args: argparse.Namespace) -> None:
    from modules.knowledge.content.services.reference import content_root
    cmd_questions(args, content_root())


def is_blocking(text: str) -> bool:
    text = text.strip()
    if not text:
        return False
    return not (_NO.match(text) and (not _YES.search(text)))


def _fields(content) -> tuple:
    heading = None
    first = None
    blocking = False
    asked = NO_DATE
    for line in content.body.splitlines():
        if first is None and line.strip():
            first = line.strip()
        found = _HEADING.match(line)
        if found and line.startswith('###') and heading is None:
            heading = found.group(1)
            continue
        blocks = _BLOCKS.match(line)
        if blocks:
            blocking = is_blocking(blocks.group(1))
            continue
        date = _ASKED.match(line)
        if date:
            asked = date.group(1)
    return (heading if heading is not None else (first or ''), blocking, asked)


def _closes(task_id: str, content, key: tuple, placed: str | None) -> bool:
    if key not in _m_refs.refs_of(task_id, content):
        return False
    if task_id == key[0]:
        return content.number > key[1]
    later = content.header.get('placed_at')
    return not (later and placed) or later > placed


def open_questions(contents) -> list:
    held = list(contents)
    found = []
    for task_id, content in held:
        if content.header.get('kind') != QUESTION_KIND:
            continue
        key = (task_id, content.number)
        placed = content.header.get('placed_at')
        if any(_closes(other_task, other, key, placed) for other_task, other in held):
            continue
        heading, blocking, asked = _fields(content)
        found.append((task_id, content.number, heading, blocking, asked))
    found.sort(key=lambda entry: (not entry[3], entry[0], entry[1]))
    return found


def cmd_questions(args: argparse.Namespace, root: Path) -> None:
    from modules.computer.software.services.project_find import project_from_args
    project = project_from_args(args)
    notes: list = []
    found = open_questions(_m_contents.contents_of_tasks(project if project is not None else root, notes))
    for note in notes:
        print(f'note: {note}', file=sys.stderr)
    if args.blocking:
        found = [entry for entry in found if entry[3]]
    if not found:
        print(EMPTY)
        return
    for task_id, number, heading, blocking, _ in found:
        print(f'{task_id}#{number}: {heading}' + (f' {BLOCKING_MARK}' if blocking else ''))
