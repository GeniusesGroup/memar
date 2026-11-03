#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the paginated listing of task ids in `modules-plugable/management/task/services/ids.py`, the rows of `ids_source.py` and the refusal of `list`.

    python modules-plugable/management/task/tests/ids.py

The subject is the answer of `ids` and the refusal `list` gives, named for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

The listing reads rows and nothing else, so these tests give it rows through the source's one function and touch no file, folder or branch.

What is pinned, and what each pin is for:

  Paged           A page holds at most the limit asked, newest first, ids and
                  nothing else; its token begins the next page, and the last
                  page's token is empty; the pages together are every match,
                  once each, also when a task is made between two calls.
  Narrowed        Words, label, parent and conversation each keep only what
                  they name, and together keep what all name; a status is a
                  label, and the listing has no status of its own.
  Rows            A row built from a task carries its status as a label.
  Bounded         A limit below one or above the highest, and a token that is
                  no task id, are refused with their own errors; with no limit
                  the default is taken.
  Refused         `list` returns nothing and fails with an error naming the
                  ways that find a task; `ids` given no way of narrowing fails
                  the same way, while the service pages an unnarrowed
                  listing for a widget.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
from importlib import import_module
import argparse
import contextlib
import io
import sys
import unittest
import unittest.mock
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = next(p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()) / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
from modules.knowledge.label.primitive.label import Label
task_ids = import_module('modules-plugable.management.task.services.ids')
task_source = import_module('modules-plugable.management.task.services.ids_source')
task_list = import_module('modules-plugable.management.task.services.list')
task_errors = import_module('modules-plugable.management.task.errors.errors')
IDS = [f'2026100{day}-T000000Z-1' for day in range(1, 8)]
LISTS = Label('lists', '0a0a0a0a-0a0a-7a0a-8a0a-0a0a0a0a0a0a')
BLOCKED = Label('Blocked', '01a14a04-6528-7000-8000-000000000001')

class Fixture(unittest.TestCase):

    def setUp(self) -> None:
        self.rows: list = []
        patched = unittest.mock.patch.object(task_source, 'records_rows', side_effect=lambda project=None: list(self.rows))
        patched.start()
        self.addCleanup(patched.stop)

    def task(self, sid: str, title: str | None=None, labels: tuple=(), parent: str='', conversation: str | None=None) -> None:
        self.rows.append(task_source.TaskRow(sid, f"{sid} {title or sid} /work", labels, parent, conversation or sid))

    def make_all(self) -> None:
        for sid in IDS:
            self.task(sid)

    def page(self, **arguments):
        return task_ids.ids_page(**arguments)

    def run_cli(self, *argv: str) -> str:
        parser = argparse.ArgumentParser()
        command = task_ids.describe(parser.add_subparsers())
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            command(parser.parse_args(['ids', *argv]))
        return out.getvalue()

class Paged(Fixture):

    def test_a_page_holds_at_most_the_limit_newest_first(self) -> None:
        self.make_all()
        page = self.page(limit=3)
        self.assertEqual(list(page.ids), [IDS[6], IDS[5], IDS[4]])
        self.assertEqual(page.next, IDS[4])

    def test_the_token_begins_the_next_page_and_the_last_token_is_empty(self) -> None:
        self.make_all()
        seen: list[str] = []
        token = ''
        while True:
            page = self.page(limit=3, after=token)
            seen.extend(page.ids)
            token = page.next
            if not token:
                break
        self.assertEqual(seen, list(reversed(IDS)))

    def test_a_task_made_between_two_calls_moves_no_id_from_one_page_to_the_other(self) -> None:
        self.make_all()
        first = self.page(limit=3)
        self.task('20261008-T000000Z-1')
        second = self.page(limit=3, after=first.next)
        self.assertEqual(list(second.ids), [IDS[3], IDS[2], IDS[1]])

    def test_a_page_holds_ids_and_nothing_of_a_task(self) -> None:
        self.task(IDS[0], 'A distinctive title', (BLOCKED,))
        out = self.run_cli('--label', 'blocked')
        self.assertIn(IDS[0], out)
        for detail in ('A distinctive title', 'status:', 'project:', 'path:', 'priority:', 'Blocked'):
            self.assertNotIn(detail, out)

    def test_the_cli_prints_one_id_a_line_then_the_token_of_the_next_page(self) -> None:
        self.make_all()
        lines = self.run_cli('--words', '2026', '--limit', '2').splitlines()
        self.assertEqual(lines[:2], [IDS[6], IDS[5]])
        self.assertEqual(lines[2], f'next: {IDS[5]}')
        last = self.run_cli('--words', '2026', '--limit', '100').splitlines()
        self.assertEqual(last[-1], 'next:')

class Narrowed(Fixture):

    def test_words_label_parent_and_conversation_each_keep_what_they_name(self) -> None:
        self.task(IDS[0], 'Ship the parser')
        self.task(IDS[1], 'Fix login', (BLOCKED,))
        self.task(IDS[2], 'Write docs', parent=IDS[0])
        self.task(IDS[3], 'More docs', parent=IDS[0], conversation=IDS[0])
        self.assertEqual(list(self.page(words='PARSER').ids), [IDS[0]])
        self.assertEqual(list(self.page(label='blocked').ids), [IDS[1]])
        self.assertEqual(list(self.page(parent=IDS[0]).ids), [IDS[3], IDS[2]])
        self.assertEqual(list(self.page(conversation=IDS[0]).ids), [IDS[3], IDS[0]])
        self.assertEqual(list(self.page(parent=IDS[0], words='more').ids), [IDS[3]])

    def test_a_label_keeps_the_tasks_that_carry_it_by_word_or_id(self) -> None:
        self.task(IDS[0], 'Labelled', (LISTS,))
        self.task(IDS[1], 'Plain')
        self.assertEqual(list(self.page(label='lists').ids), [IDS[0]])
        self.assertEqual(list(self.page(label=LISTS.id).ids), [IDS[0]])

class Rows(unittest.TestCase):

    def test_a_status_is_read_as_a_label(self) -> None:
        self.assertEqual([held.title for held in task_source.status_label('blocked')], ['Blocked'])
        self.assertEqual(task_source.status_label(''), ())
        self.assertEqual(task_source.status_label('no-such-status'), ())

    def test_a_row_carries_its_plans_labels_and_its_status_label(self) -> None:
        task = task_list.Task(Path(IDS[0]), True, {'title': 'T', 'project': '/work', 'labels': '  - lists(0a0a0a0a-0a0a-7a0a-8a0a-0a0a0a0a0a0a)'}, 'blocked')
        with unittest.mock.patch.object(task_source, 'find_tasks', return_value=[task]):
            row = task_source.records_rows()[0]
        self.assertEqual(row.id, IDS[0])
        self.assertEqual({held.title for held in row.labels}, {'lists', 'Blocked'})
        self.assertIn('T', row.words)

class Bounded(Fixture):

    def test_a_limit_outside_the_bounds_is_refused(self) -> None:
        self.make_all()
        for limit in (0, -1, task_ids.LIMIT_HIGHEST + 1):
            with self.assertRaises(task_errors.Task_Error_LimitRefused):
                self.page(limit=limit)

    def test_no_limit_takes_the_default(self) -> None:
        for number in range(task_ids.LIMIT_DEFAULT + 3):
            self.task(f'20261101-T{number:06d}Z-1')
        self.assertEqual(len(self.page().ids), task_ids.LIMIT_DEFAULT)

    def test_a_token_that_is_no_task_id_is_refused(self) -> None:
        self.make_all()
        with self.assertRaises(task_errors.Task_Error_PageTokenRefused):
            self.page(after='not-a-task-id')

class Refused(Fixture):

    def test_list_fails_naming_the_ways_that_find_a_task(self) -> None:
        self.make_all()
        parser = argparse.ArgumentParser()
        command = task_list.describe(parser.add_subparsers())
        out = io.StringIO()
        with contextlib.redirect_stdout(out), self.assertRaises(SystemExit):
            command(parser.parse_args(['list']))
        self.assertEqual(out.getvalue(), '')

    def test_the_refusal_names_every_way_that_finds(self) -> None:
        message = str(task_ids.ListRefused())
        for way in ('content find', 'task ids', '--label', '--parent', '--conversation', 'task claims', 'task claim'):
            self.assertIn(way, message)
        self.assertNotIn('--status', message)

    def test_ids_has_no_status_of_its_own(self) -> None:
        parser = argparse.ArgumentParser()
        task_ids.describe(parser.add_subparsers())
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            parser.parse_args(['ids', '--status', 'blocked'])

    def test_ids_given_no_way_of_narrowing_is_refused_and_prints_nothing(self) -> None:
        self.make_all()
        out = io.StringIO()
        with contextlib.redirect_stdout(out), self.assertRaises(SystemExit):
            self.run_cli()
        self.assertEqual(out.getvalue(), '')

    def test_the_service_pages_an_unnarrowed_listing_for_a_widget(self) -> None:
        self.make_all()
        self.assertEqual(list(self.page(limit=2).ids), [IDS[6], IDS[5]])

if __name__ == '__main__':
    unittest.main()
