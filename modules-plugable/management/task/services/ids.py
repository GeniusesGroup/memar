#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/management/task/services/ids.py — a page of the ids of the tasks that match, and nothing of any task.

The abstraction is `services/task-ids-list/task-ids-list.kh`; the rule that a
service returns a list of identities or the detail of one, never both, is
[A Service Lists Identities or Gives One Detail](../../../../modules/process/service/rules/ids-or-detail-never-both/ids-or-detail-never-both.md).
The tasks are many, so a page holds at most `LIMIT_HIGHEST` ids, newest first,
and the token it returns is the last id it held: the next page is the ids
before it, so a task made between two calls moves no id from one page to the
other. The service pages an unnarrowed listing for a widget of a user
interface; the verb is for an agent, and an agent holds no list of all tasks, so
the verb is refused when none of words, label, parent or conversation
is given, with the error `list` fails with, which names the ways that find a task.
"""
from __future__ import annotations
from importlib import import_module
import argparse
import re
from typing import Callable, NamedTuple
from machine.console import fail
_m_errors = import_module('modules-plugable.management.task.errors.errors')
Task_Error_ListRefused = _m_errors.Task_Error_ListRefused
Task_Error_PageTokenRefused = _m_errors.Task_Error_PageTokenRefused
Task_Error_LimitRefused = _m_errors.Task_Error_LimitRefused
_m_source = import_module('modules-plugable.management.task.services.ids_source')
TaskRow = _m_source.TaskRow
TASK_IDS_COMMAND = 'ids'
LIMIT_HIGHEST = 100
LIMIT_DEFAULT = 20
TOKEN_SHAPE = re.compile(r'\d{8}-?T\d{6}Z-\d+(-\d+)?')
WAYS = 'words (`memar content find TEXT --from tasks`); label (a status is a label), parent or conversation (`memar task ids --label L | --parent ID | --conversation ID`, with --words W); a claim (`memar task claims N`, `memar task claim ID`)'

class Page(NamedTuple):
    ids: tuple[str, ...]
    next: str

class ListRefused(Task_Error_ListRefused):

    def __init__(self) -> None:
        super().__init__(f'no verb lists all tasks: there are too many for any agent to hold; find a task by {WAYS}; read one task with `memar git show-task-records`')

def labelled(row: TaskRow, label: str) -> bool:
    wanted = label.strip().casefold()
    return any((wanted in (held.title.casefold(), held.id.casefold()) for held in row.labels))

def ids_page(words: str | None=None, label: str | None=None, parent: str | None=None, conversation: str | None=None, limit: int | None=None, after: str='', project=None) -> Page:
    """The page of ids after AFTER (the first when empty) of the tasks every given way keeps, at most LIMIT of them (the default when None)."""
    if limit is None:
        limit = LIMIT_DEFAULT
    if limit < 1 or limit > LIMIT_HIGHEST:
        raise Task_Error_LimitRefused(f'a page holds from 1 to {LIMIT_HIGHEST} ids; {limit} was asked')
    if after and TOKEN_SHAPE.fullmatch(after) is None:
        raise Task_Error_PageTokenRefused(f'{after!r} is not a token a listing of task ids returned; start again with none')
    needle = words.casefold() if words else ''
    kept = [row for row in _m_source.records_rows(project) if (not needle or needle in row.words.casefold()) and (not label or labelled(row, label)) and (not parent or row.parent == parent) and (not conversation or row.conversation == conversation)]
    ids = sorted((row.id for row in kept), reverse=True)
    if after:
        ids = [each for each in ids if each < after]
    held = ids[:limit]
    return Page(tuple(held), held[-1] if len(ids) > limit else '')

def narrowing(*ways: str | None) -> bool:
    return any((way for way in ways))

def ids_for_agent(words: str | None=None, label: str | None=None, parent: str | None=None, conversation: str | None=None, limit: int | None=None, after: str='', project=None) -> None:
    """`ids`: print a page of ids, one a line, then `next: TOKEN` (empty on the last page); refused when no way of narrowing is given."""
    if not narrowing(words, label, parent, conversation):
        fail(str(ListRefused()))
    try:
        page = ids_page(words, label, parent, conversation, limit, after, project)
    except (Task_Error_LimitRefused, Task_Error_PageTokenRefused) as error:
        fail(str(error))
    for each in page.ids:
        print(each)
    print(f'next: {page.next}'.rstrip())

def describe(verbs) -> Callable[[argparse.Namespace], None]:
    """`memar task ids`."""
    ids = verbs.add_parser(TASK_IDS_COMMAND, help='list a page of the ids of the tasks that match, and the token of the next page', description=f'List the ids of the tasks that every way given keeps, newest first, one a line, then `next: TOKEN`, empty on the last page; pass the token as --after to get the page after. A page holds ids and nothing of any task: read one task with `memar git show-task-records`. At least one of --words, --label, --parent and --conversation is required, since no agent holds all tasks. A page holds from 1 to {LIMIT_HIGHEST} ids, {LIMIT_DEFAULT} when --limit is not given.')
    ids.add_argument('--words', default=None, help='keep tasks whose id, title or project holds these words, in any case')
    ids.add_argument('--label', default=None, help='keep tasks that carry this label, by its word or its id; a status is a label, so --label blocked keeps the blocked ones')
    ids.add_argument('--parent', default=None, metavar='ID', help='keep the tasks made from this task')
    ids.add_argument('--conversation', default=None, metavar='ID', help='keep the tasks of the conversation this task belongs to')
    ids.add_argument('--limit', type=int, default=None, help=f'the most ids one page holds, up to {LIMIT_HIGHEST}')
    ids.add_argument('--after', default='', metavar='TOKEN', help='the token of the page before the one wanted, from its `next:` line')
    return run

def run(args: argparse.Namespace) -> None:
    ids_for_agent(args.words, args.label, args.parent, args.conversation, args.limit, args.after)
