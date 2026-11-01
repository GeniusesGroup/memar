#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
import argparse
import sys
from pathlib import Path
_m_changelog_record = import_module('modules-plugable.knowledge.documentation.services.changelog_record')
_m_contents = import_module('modules-plugable.knowledge.documentation.services.contents_of_tasks')
EMPTY = '(no changelog record has only AI authors)'
CONTRIBUTORS_FILE = 'CONTRIBUTORS.md'


def describe(verbs):
    parser = verbs.add_parser('list-ai-only-changelog-records', help='list the changelog contents only AI authors stand behind, as task#number: title hits', description='List the contents of kind changelog whose author is a CONTRIBUTORS.md brand or tool (a ### heading) and to which no content of kind approval, with the verdict approved, placed by someone who is not such a brand or tool refers, one `task#number: title` hit per line, oldest placement first. A human reviews one by placing an approval content that refers to it. What could not be read, and why, is printed on standard error.', formatter_class=argparse.HelpFormatter)
    parser.add_argument('--after', default=None, metavar='INSTANT', help='keep only the contents placed after this instant, as written in the placed_at of a content (2026-10-01T00:00:00Z)')
    return run


def run(args: argparse.Namespace) -> None:
    from modules.knowledge.content.services.reference import content_root
    list_ai_only(args, content_root())


def list_ai_only(args: argparse.Namespace, root: Path) -> None:
    sections = _m_changelog_record.contributor_sections(root / CONTRIBUTORS_FILE)
    notes: list = []
    found = _m_changelog_record.ai_only_changelogs(_m_contents.contents_of_tasks(root, notes), sections)
    for note in notes:
        print(f'note: {note}', file=sys.stderr)
    if args.after:
        found = [entry for entry in found if entry[3] > args.after]
    if not found:
        print(EMPTY)
        return
    for task_id, number, title, _ in found:
        print(f'{task_id}#{number}: {title}')
