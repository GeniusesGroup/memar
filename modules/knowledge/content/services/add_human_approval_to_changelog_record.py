#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/knowledge/content/services/add_human_approval_to_changelog_record.py — `memar content add-human-approval-to-changelog-record`: a person's `approved` added to one record.

changelog.md → Approval Requires a Reviewer Who Did Not Do the Work: the
approval names the reviewer alongside the other contributors, as one more
`Contributors` sub-bullet whose role tag is `approved`. This verb writes exactly
that sub-bullet, `[Name](path#anchor) - approved`, after the record's last
contributor, and nothing else: the record's prose is history and is not
touched, and no other record is.

**Who may approve.** The reviewer is named by their CONTRIBUTORS.md anchor, never
taken from the machine or the git user, and must be a natural person — a `##`
heading without `Full Legal Name`. A record is approvable here only when it is
one `list-ai-only-changelog-records` lists: every contributor a brand or tool.
That also keeps the first condition of the approval rule: a person among the
record's contributors did the work, and a record with one is refused.

**How it is written.** The read, the choice of the line, and the write happen
under the per-file lock, as `edit` does, so the record numbered is the record
written to; the text goes through `content_text`, keeping the ledger's own line
endings. The link path is the one the record's own contributor links use.
"""
from __future__ import annotations
from machine.plugable_import import load as plugable_load
_m_fs_lock = plugable_load('computer.filesystem.services.fs_lock')
edit_task = _m_fs_lock.edit_task
import argparse
import sys

def describe(verbs):
    parser = verbs.add_parser('add-human-approval-to-changelog-record', help="add a person's `approved` to one changelog record whose contributors are all AI", description='Append `- [Name](CONTRIBUTORS.md#anchor) - approved` to the Contributors of record N of FILE, the number list-ai-only-changelog-records prints. The record must have only AI contributors, and the reviewer must be a natural person in CONTRIBUTORS.md.', formatter_class=argparse.HelpFormatter)
    parser.add_argument('file', help='the *.changelog.md holding the record')
    parser.add_argument('--record', type=int, required=True, help="the record's number in the ledger")
    parser.add_argument('--reviewer', required=True, help='your CONTRIBUTORS.md heading anchor, e.g. omid-hekayati')
    return run

def run(args: argparse.Namespace) -> None:
    from modules.knowledge.content.services.changelog_record import APPROVED, NATURAL_PERSON, Directory, changelog_records, classify, lines_of
    from modules.knowledge.content.services.text import detect_newline, plain_path, read_utf8_strict, write_utf8, writer_id
    ledger = plain_path(args.file)
    if not ledger.is_file() or not ledger.name.endswith('.changelog.md'):
        sys.exit(f'error: not a *.changelog.md file: {ledger}')
    with edit_task(ledger, task_id=writer_id(), plan_summary=f"add {args.reviewer}'s approval to record {args.record} of {ledger.name}"):
        text, _ = read_utf8_strict(ledger)
        records = changelog_records(text)
        if not 1 <= args.record <= len(records):
            sys.exit(f'error: {ledger.name} has records 1 to {len(records)}, not {args.record}. Nothing was written.')
        chosen = records[args.record - 1]
        directory = Directory(ledger)
        if chosen not in classify([chosen], directory).listed:
            sys.exit(f'error: record {chosen.number} ({chosen.title}) does not have only AI contributors that CONTRIBUTORS.md holds. Nothing was written.')
        if chosen.insert_at is None:
            sys.exit(f'error: record {chosen.number} writes its Contributors on one line, not as sub-bullets. Nothing was written.')
        target = chosen.contributors[0].target
        reviewer = directory.section(_named(target, args.reviewer))
        if reviewer is None or reviewer.kind != NATURAL_PERSON:
            found = 'is not in CONTRIBUTORS.md' if reviewer is None else f'is a {reviewer.kind}'
            sys.exit(f"error: reviewer '{args.reviewer}' {found}, not a natural person. Nothing was written.")
        lines = lines_of(text)
        lines.insert(chosen.insert_at, f'{chosen.indent}- [{reviewer.name}]({target}#{reviewer.anchor}) - {APPROVED}')
        write_utf8(ledger, '\n'.join(lines), detect_newline(ledger))
    print(f'approved record {chosen.number} ({chosen.title}) of {ledger} as {reviewer.name}')

def _named(target: str, anchor: str):
    from modules.knowledge.content.services.changelog_record import Contributor
    return Contributor(anchor, target, anchor, -1)
