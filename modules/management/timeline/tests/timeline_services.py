#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the services of the timeline domain and its file adapter, `services/timeline_place.py`, `services/timeline_latest.py` and `services/timeline_files.py`.

    python modules/management/timeline/tests/timeline_services.py

The subject is `Timeline_Place`, `Timeline_Latest` and `Timeline_Placement_Store` (`services/`, `protocol/`) under the
rule a placement is added and never written over (`rules/a-placement-is-added-never-written-over/`). What is pinned:

  Place      The service stamps the instant and passes it to the store with the number the caller read.
  Latest     The service answers the store's latest placement of a kind.
  Adapter    The one place that opens `content.NNNNN.md`; the extension is one constant; a placement is a numbered
             file written once and made read-only; the number is the next of the timeline across all kinds; the
             `after` check compares only the latest of the same kind; a UUID that is no timeline is not found.
"""
from __future__ import annotations
from importlib import import_module
from machine.plugable_import import load as plugable_load
_m_fs_test_scratch = plugable_load('computer.memory.filesystem.services.fs_test_scratch')
suite_scratch = _m_fs_test_scratch.suite_scratch
import os
import stat
import sys
import tempfile
import unittest
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = next(p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()) / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
place = import_module('modules.management.timeline.services.timeline_place')
latest = import_module('modules.management.timeline.services.timeline_latest')
files = import_module('modules.management.timeline.services.timeline_files')
errors = import_module('modules.management.timeline.errors.placement')


class Recording:

    def __init__(self) -> None:
        self.added = []

    def read_latest_placement(self, timeline, kind):
        return (4, 'c-4', True)

    def add_placement(self, timeline, content, kind, placer, placed_at, after):
        self.added.append((timeline, content, kind, placer, placed_at, after))
        return 9


class Services(unittest.TestCase):

    def test_the_instant_is_stamped_and_passed_with_the_number_read(self) -> None:
        store = Recording()
        self.assertEqual(place.place_content(store, 'T', 'c', 'plan', 'u', 4, clock=lambda: 1234), 9)
        self.assertEqual(store.added, [('T', 'c', 'plan', 'u', 1234, 4)])

    def test_the_latest_of_a_kind_is_the_stores(self) -> None:
        self.assertEqual(latest.read_latest(Recording(), 'T', 'plan'), (4, 'c-4', True))


class Fixture(unittest.TestCase):

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.folder = Path(self.scratch.name) / 'T-1'
        self.folder.mkdir()
        self.exists = True
        self.timeline = files.FileTimeline(lambda timeline: self.folder, lambda folder: self.exists, home=self.folder)

    def put(self, kind: str, text: str, after: int = 0, placer: str = 'u') -> int:
        content = self.timeline.add_content(kind, text)
        return self.timeline.add_placement('T-1', content, kind, placer, 1761868800, after)


class Adapter(Fixture):

    def test_the_extension_of_a_content_is_one_constant(self) -> None:
        self.assertEqual(files.CONTENT_EXTENSION, '.md')
        self.put('plan', 'one\n')
        self.assertTrue((self.folder / f'content.00001{files.CONTENT_EXTENSION}').is_file())

    def test_a_content_created_and_not_placed_leaves_no_file(self) -> None:
        self.timeline.add_content('plan', 'one\n')
        self.assertEqual(list(self.folder.iterdir()), [])

    def test_the_first_placement_is_numbered_one_and_the_header_holds_what_was_placed(self) -> None:
        content = self.timeline.add_content('plan', 'one\n')
        number = self.timeline.add_placement('T-1', content, 'plan', 'someone', 1761868800, 0)
        self.assertEqual(number, 1)
        stored = files.read_contents(self.folder)[0]
        self.assertEqual((stored.header['kind'], stored.header['author'], stored.header['content'], stored.header['placed_at'], stored.body), ('plan', 'someone', content, '2025-10-31T00:00:00Z', 'one\n'))
        self.assertNotIn('follows', stored.header)

    def test_the_number_is_the_next_of_the_timeline_across_all_kinds(self) -> None:
        self.assertEqual([self.put('plan', 'a\n'), self.put('report', 'b\n'), self.put('message', 'c\n')], [1, 2, 3])

    def test_the_latest_of_a_kind_is_read_with_found_false_when_none(self) -> None:
        self.put('plan', 'a\n')
        content = self.timeline.read_latest_placement('T-1', 'plan')
        self.assertEqual((content[0], content[2]), (1, True))
        self.assertEqual(self.timeline.read_latest_placement('T-1', 'message'), (0, '', False))

    def test_a_content_is_read_by_its_uuid_from_the_created_or_the_placed(self) -> None:
        content = self.timeline.add_content('plan', 'one\n')
        self.assertEqual(self.timeline.read_content(content), ('plan', 'one\n', True))
        self.timeline.add_placement('T-1', content, 'plan', 'u', 1761868800, 0)
        fresh = files.FileTimeline(lambda timeline: self.folder, lambda folder: True, home=self.folder)
        self.assertEqual(fresh.read_content(content), ('plan', 'one\n', True))
        self.assertEqual(fresh.read_content('nope'), ('', '', False))

    def test_a_placement_is_read_only_and_never_opened_for_writing_again(self) -> None:
        self.put('plan', 'one\n')
        path = self.folder / 'content.00001.md'
        self.assertFalse(os.stat(path).st_mode & stat.S_IWRITE)
        with self.assertRaises(OSError):
            path.open('w')

    def test_a_stale_number_of_the_same_kind_is_refused_and_nothing_is_written(self) -> None:
        self.put('plan', 'one\n')
        self.put('plan', 'two\n', after=1)
        with self.assertRaises(errors.Timeline_Error_Changed):
            self.put('plan', 'late\n', after=1)
        with self.assertRaises(errors.Timeline_Error_Changed):
            self.put('plan', 'late\n', after=0)
        self.assertEqual([c.number for c in files.read_contents(self.folder)], [1, 2])

    def test_a_placement_of_another_kind_does_not_make_a_number_stale(self) -> None:
        self.put('plan', 'one\n')
        self.put('critique', 'c\n')
        self.assertEqual(self.put('plan', 'two\n', after=1), 3)
        self.assertEqual(files.read_contents(self.folder)[2].header['follows'], '1')

    def test_a_uuid_that_is_no_timeline_is_not_found(self) -> None:
        content = self.timeline.add_content('plan', 'x\n')
        self.exists = False
        with self.assertRaises(errors.Timeline_Error_NotFound):
            self.timeline.add_placement('T-1', content, 'plan', 'u', 1761868800, 0)
        with self.assertRaises(errors.Timeline_Error_NotFound):
            self.timeline.read_latest_placement('T-1', 'plan')
        self.assertEqual(list(self.folder.iterdir()), [])


class Files(Fixture):

    def test_the_first_content_is_numbered_one_in_five_digits(self) -> None:
        self.assertEqual(files.write_content(self.folder, 'plan', 'hello\n', 'agent'), 1)
        self.assertTrue((self.folder / 'content.00001.md').is_file())

    def test_the_header_holds_kind_author_placed_at_follows_refs_and_the_body_is_the_text(self) -> None:
        files.write_content(self.folder, 'plan', 'one\n', 'agent', placed_at='2026-10-31T00:00:00Z')
        files.write_content(self.folder, 'plan', 'two\n', 'agent', follows=1, refs=['a.md'], fields={'type': 'x'})
        second = files.read_contents(self.folder)[1]
        self.assertEqual((second.number, second.header['kind'], second.header['follows'], second.header['refs'], second.header['type'], second.header['author'], second.body), (2, 'plan', '1', 'a.md', 'x', 'agent', 'two\n'))

    def test_numbers_never_repeat_even_when_a_file_is_present_already(self) -> None:
        (self.folder / 'content.00001.md').write_text('---\nkind: plan\n---\nx')
        self.assertEqual(files.write_content(self.folder, 'critique', 'c\n', 'agent'), 2)

    def test_a_write_that_follows_an_older_content_than_the_highest_of_its_kind_is_refused(self) -> None:
        files.write_content(self.folder, 'plan', 'one\n', 'agent')
        files.write_content(self.folder, 'plan', 'two\n', 'agent', follows=1)
        with self.assertRaises(errors.Timeline_Error_Changed):
            files.write_content(self.folder, 'plan', 'late\n', 'agent', follows=1)
        self.assertEqual([c.number for c in files.read_contents(self.folder)], [1, 2])

    def test_the_latest_of_a_kind_is_its_highest_number(self) -> None:
        files.write_content(self.folder, 'plan', 'one\n', 'agent')
        files.write_content(self.folder, 'plan', 'two\n', 'agent', follows=1)
        self.assertEqual(files.latest_content(self.folder, 'plan').number, 2)
        self.assertIsNone(files.latest_content(self.folder, 'report'))

    def test_a_content_file_is_recognised_by_name(self) -> None:
        self.assertTrue(files.is_content_file(Path('x/content.00128.md')))
        self.assertFalse(files.is_content_file(Path('x/content.128.md')))
        self.assertFalse(files.is_content_file(Path('x/plan.md')))

    def test_a_text_is_added_after_the_latest_of_its_kind(self) -> None:
        files.add_text(self.folder, 'plan', 'one\n', 'agent')
        self.assertEqual(files.add_text(self.folder, 'plan', 'two\n', 'agent'), 2)
        self.assertEqual(files.read_contents(self.folder)[1].header['follows'], '1')
        number = files.add_text(self.folder, 'critique', 'c\n', 'agent')
        self.assertNotIn('follows', files.read_contents(self.folder)[number - 1].header)


if __name__ == '__main__':
    unittest.main()
