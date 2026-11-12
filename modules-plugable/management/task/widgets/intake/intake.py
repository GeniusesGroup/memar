#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/management/task/widgets/intake/intake.py — rank related subjects then ensure-parts.

Agent path: `memar intake`. It prints likeness hits (first build does not gate on them), then calls the
ensure parts. Duplicate hunting does not page `memar task ids` or any full-scan verb.
"""
from __future__ import annotations
from importlib import import_module
import argparse
from machine.console import note
from modules.computer.software.primitive.project_name import ProjectName
from modules.computer.software.services.project_find import add_project_flags, project_from_args

_m_rank = import_module('modules-plugable.knowledge.text.likeness.services.rank_likeness')
Likeness_Rank = _m_rank.Likeness_Rank
_m_store = import_module('modules-plugable.knowledge.text.likeness.services.likeness_memory_store')
Likeness_Memory_Store = _m_store.Likeness_Memory_Store
_m_parts = import_module('modules-plugable.management.task.services.parts_ensure')
parts_ensure = _m_parts.parts_ensure
_m_new = import_module('modules-plugable.management.task.services.new')

DOMAIN = 'intake'
SCOPE_TASKS = 'tasks'
DEFAULT_LIMIT = 10
DEFAULT_MIN_LIKENESS = 0.0


def words_of(text: str) -> tuple[str, ...]:
    return tuple(word.lower() for word in text.split() if len(word) >= 2)


class Intake:

    def __init__(self, rank=None, ensure=None, store=None, printer=note) -> None:
        self.rank = rank or Likeness_Rank()
        self.ensure = ensure or parts_ensure
        self.store = store if store is not None else Likeness_Memory_Store()
        self.printer = printer

    def open(self, scope, text: str, excluded=(), limit: int=DEFAULT_LIMIT, module='', role: str='', min_likeness: float=DEFAULT_MIN_LIKENESS, title: str | None=None, project: str | None=None, parent: str | None=None, queued: bool=False, priority=None, labels=None, depends_on=None, task_id: str | None=None):
        query = words_of(text if text.strip() else (title or ''))
        hits = self.rank.rank(
            scope=scope,
            query=query,
            store=self.store,
            excluded=excluded,
            limit=limit,
            module=module,
            role=role,
            min_likeness=min_likeness,
        )
        self.printer('hits:')
        if not hits:
            self.printer('  (none)')
        for subject, likeness in hits:
            self.printer(f'  {subject} {likeness:.4f}')
        sid, path = self.ensure(
            task_id=task_id,
            title=title,
            parent=parent,
            queued=queued,
            priority=priority,
            labels=labels,
            project=project,
            depends_on=depends_on,
        )
        return (hits, sid, path)


DESCRIPTION = f"""Open independent work after ranking related tasks by likeness.

Ranks within scope with module facet, optional role and min_likeness, prints the
hits (first build does not hold the maker), then calls the ensure parts. Agents
use this path instead of paging `memar task ids` to hunt duplicates. Continuing
an existing task stays `memar task ensure --task-id ID`. Engine-backed indexing
binds later; the request shape is the Memar contract now.

{ProjectName.either_words().capitalize()} names the project the new task belongs to."""


def describe(verbs):
    opener = verbs.add_parser(
        DOMAIN,
        help='rank related tasks then ensure one',
        description=DESCRIPTION,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    opener.add_argument('--title', required=True, help='one line saying what the task is')
    opener.add_argument('--text', default='', help='body ranked with the title; title alone when omitted')
    opener.add_argument('--module', required=True, help='module facet: module identity the subject belongs to')
    opener.add_argument('--role', default='', help='optional text role facet: title, body, label, or a module word')
    opener.add_argument('--min-likeness', type=float, default=DEFAULT_MIN_LIKENESS, metavar='N', help='drop hits below this likeness ratio (0 to 1); default prints all ranked')
    opener.add_argument('--scope', default=SCOPE_TASKS, help=f'likeness scope; default {SCOPE_TASKS}')
    opener.add_argument('--limit', type=int, default=DEFAULT_LIMIT, help=f'most hits to print; default {DEFAULT_LIMIT}')
    opener.add_argument('--parent', default=None, metavar='ID', help='the task this task came from')
    opener.add_argument('--queued', action='store_true', help='leave the task queued')
    Priority_Rank = import_module('modules-plugable.identity.thing.priority.primitive.rank').Priority_Rank
    opener.add_argument('--priority', type=int, default=None, metavar='N', help=f'after open, set Priority_Rank via Thing ({Priority_Rank.listing()}); higher goes sooner among queued peers; absence ranks as the lowest; owned by the ensure widget, not the ensure service')
    opener.add_argument('--label', action='append', default=None, metavar='KIND=WORD', help='label; may be repeated')
    add_project_flags(opener, 'the project the task belongs to', required=True)
    return run


def run(args: argparse.Namespace) -> None:
    project = project_from_args(args)
    named = {} if project is None else {'project': project}
    text = args.text if args.text.strip() else args.title
    hits, sid, path = Intake().open(
        scope=args.scope,
        text=text,
        limit=args.limit,
        module=args.module,
        role=args.role,
        min_likeness=args.min_likeness,
        title=args.title,
        parent=args.parent,
        queued=args.queued,
        priority=args.priority,
        labels=args.label,
        **named,
    )
    del hits, path
    note(f'task_id: {sid}')
    for kind in ('plan', 'report'):
        note(f'{kind}: write it with `memar conversation {_m_new.POST_COMMAND} --timeline {sid} --kind {kind} --content-file FILE`')
