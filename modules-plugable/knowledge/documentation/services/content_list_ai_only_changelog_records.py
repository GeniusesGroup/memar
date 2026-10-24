#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/knowledge/documentation/services/content_list_ai_only_changelog_records.py — `memar content list-ai-only-changelog-records`: one ledger's records no person contributed to.

A record whose contributors are all models has had no human's eyes, and the
owner asked for a cheap way to give it one (2026-10-16). Every such record of
the checkout at once is a list too long to be read, so this verb works one
ledger at a time: the human names the ledger, or is offered the first one, in
path order, that still holds such a record; `--after` steps past a ledger the
human chose to leave. The ledger's count is printed with its list, and how many
ledgers after it still hold such records, so the human sees the size of what
is left without reading it.

What a record is and who a contributor is are read in
`content_changelog_record.py`, shared with the verb that adds the approval.
Each listed line is `path:line: number title`, the number being the one
`add-human-approval-to-changelog-record --record` takes.
"""
from __future__ import annotations
from importlib import import_module
import argparse
from pathlib import Path
from modules.knowledge.content.services.reference import content_root
from modules.knowledge.text.services.file_text import plain_path
APPROVE = 'memar content add-human-approval-to-changelog-record'

def describe(verbs):
    parser = verbs.add_parser('list-ai-only-changelog-records', help="list one ledger's changelog records whose contributors are all AI, for a human to review", description='List the records of one *.changelog.md whose every contributor is a CONTRIBUTORS.md brand or tool (a ### heading), each as path:line: number title. Without FILE, the first ledger of the checkout, in path order, that holds such a record is listed.', formatter_class=argparse.HelpFormatter)
    parser.add_argument('file', nargs='?', default=None, help='the ledger to list')
    parser.add_argument('--after', default=None, help='without FILE: offer the first such ledger after this one')
    return run

def run(args: argparse.Namespace) -> None:
    _m_changelog_record = import_module('modules-plugable.knowledge.documentation.services.changelog_record')
    ai_only_records = _m_changelog_record.ai_only_records
    root = content_root()
    if args.file:
        ledger = plain_path(args.file)
        if not ledger.is_file():
            raise SystemExit(f'error: not a file: {ledger}')
        _print(ledger, ai_only_records(ledger), root)
        return
    from modules.knowledge.text.services.corpus import ledger_files
    ledgers = ledger_files(root)
    if args.after:
        after = plain_path(args.after)
        ledgers = [path for path in ledgers if path > after]
    offered = None
    waiting = 0
    for ledger in ledgers:
        try:
            reading = ai_only_records(ledger)
        except (OSError, UnicodeDecodeError) as error:
            print(f'note: {_shown(ledger, root)} was not read: {error}')
            continue
        if not reading.listed:
            continue
        if offered is None:
            offered = (ledger, reading)
        else:
            waiting += 1
    if offered is None:
        print('no ledger' + (' after that one' if args.after else '') + ' holds a record whose contributors are all AI')
        return
    _print(*offered, root)
    plural = 'ledger after it holds' if waiting == 1 else 'ledgers after it hold'
    print(f'{waiting} more {plural} such records; `--after {_shown(offered[0], root)}` offers the next')

def _shown(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)

def _print(ledger: Path, reading, root: Path) -> None:
    shown = _shown(ledger, root)
    print(f'{shown}: {len(reading.listed)} of {reading.total} records have only AI contributors')
    for item in reading.listed:
        print(f'{shown}:{item.line + 1}: {item.number} {item.title}')
    if reading.unknown:
        numbers = ', '.join((str(item.number) for item in reading.unknown))
        noun = 'record names' if len(reading.unknown) == 1 else 'records name'
        print(f'{len(reading.unknown)} {noun} a contributor CONTRIBUTORS.md does not hold: {numbers}')
    if reading.listed:
        print(f'approve one: {APPROVE} {shown} --record N --reviewer YOUR-CONTRIBUTORS-ANCHOR')
