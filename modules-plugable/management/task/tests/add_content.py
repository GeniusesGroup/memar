#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the verb that adds a text to a task as a content, `modules-plugable/management/task/services/add_content.py`, its core service `task_content_add.py` and the store it takes in `task_files.py`.

    python modules-plugable/management/task/tests/add_content.py

The subject is the Khayyam of 2026-10-31, `protocol/task-content-store.kh` and
`services/task-content-add/task-content-add.kh`, under the rule a text of a task
is added and never replaced. What is pinned:

  Core       The service takes a store and opens no file; it reads the latest
             content of the kind and adds the text after it, the number zero
             when there is none; it accepts any text and any kind.
  Store      The adapter reads the latest of a kind, adds after the number it is
             given, refuses a stale number with Task_Error_Changed, and refuses a
             task in the old shape or none with Task_Error_NotFound; the
             extension of a content is one constant.
  Verb       The text is read from a file or standard input and the new number
             printed; a second text of the kind follows the first; the author
             defaults to the agent name; a kind that is no label is refused with
             the label module's refusal; a task in the old shape is refused,
             naming its reader, and nothing is written to it.
"""
from __future__ import annotations
from importlib import import_module
from machine.plugable_import import load as plugable_load
_m_fs_test_scratch = plugable_load('computer.memory.filesystem.services.fs_test_scratch')
suite_scratch = _m_fs_test_scratch.suite_scratch
_m_fs_memar = plugable_load('computer.memory.filesystem.services.fs_memar')
memar_fs = _m_fs_memar
import contextlib
import io
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = next(p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()) / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
files = import_module('modules-plugable.management.task.services.task_files')
errors = import_module('modules-plugable.management.task.errors.errors')
core = import_module('modules-plugable.management.task.services.task_content_add')
verb = import_module('modules-plugable.management.task.services.add_content')
_m_plan_file = import_module('modules-plugable.management.task.services.plan_file')


class Recording:

    def __init__(self, latest=None) -> None:
        self.latest = latest
        self.added = []

    def read_latest_content(self, project, task, kind):
        if self.latest is None:
            return (0, '', False)
        return (self.latest, 'text', True)

    def add_content(self, project, task, kind, text, author, after):
        self.added.append((kind, text, author, after))
        return 9


class Core(unittest.TestCase):

    def test_the_first_text_of_a_kind_is_added_after_zero(self) -> None:
        store = Recording()
        self.assertEqual(core.add_text(store, None, 'T', 'plan', 'x', 'a'), 9)
        self.assertEqual(store.added, [('plan', 'x', 'a', 0)])

    def test_a_later_text_is_added_after_the_latest_of_its_kind(self) -> None:
        store = Recording(latest=4)
        core.add_text(store, None, 'T', 'report', 'y', 'a')
        self.assertEqual(store.added, [('report', 'y', 'a', 4)])

    def test_any_text_and_any_kind_is_accepted_unchecked(self) -> None:
        store = Recording()
        core.add_text(store, None, 'T', 'anything', 'not a template at all', 'a')
        self.assertEqual(store.added, [('anything', 'not a template at all', 'a', 0)])


class Fixture(unittest.TestCase):

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        self.project = self.root / 'project-x'
        self.project.mkdir()
        patched = unittest.mock.patch.object(memar_fs, 'memar_root', return_value=self.root)
        patched.start()
        self.addCleanup(patched.stop)
        self.folder = self.root / 'T-1'
        self.folder.mkdir()
        located = unittest.mock.patch.object(verb, 'folder_of', return_value=self.folder)
        located.start()
        self.addCleanup(located.stop)

    def made(self) -> None:
        files.create_task(self.folder, 'T-1', 'A title', None, None, self.project, 'queued', 7, None, None)

    def old(self) -> None:
        (self.folder / _m_plan_file.PLAN_NAME).write_text('---\nTitle: T\nStatus: Queued\nStart Date: 2026-10-13T00:00:00Z\n---\n# T\n', encoding='utf-8', newline='\n')

    def added(self, kind: str, text: str, author: str | None = None) -> str:
        out = io.StringIO()
        with contextlib.redirect_stdout(out), unittest.mock.patch.object(sys, 'stdin', io.StringIO(text)):
            verb.add_task_content('T-1', kind, None, author)
        return out.getvalue()

    def refused(self, call, *args) -> str:
        with self.assertRaises(SystemExit) as raised:
            call(*args)
        return str(raised.exception.code)


class Store(Fixture):

    def test_the_extension_of_a_content_is_one_constant(self) -> None:
        self.assertEqual(files.CONTENT_EXTENSION, '.md')
        self.made()
        self.assertTrue((self.folder / f'content.00001{files.CONTENT_EXTENSION}').is_file())

    def test_the_latest_of_a_kind_is_read_with_found_false_when_none(self) -> None:
        self.made()
        stores = files.stores_at(self.folder)
        number, text, found = stores.read_latest_content(None, 'T-1', 'plan')
        self.assertEqual((number, found), (1, True))
        self.assertEqual(stores.read_latest_content(None, 'T-1', 'message'), (0, '', False))

    def test_a_text_is_added_after_the_number_read(self) -> None:
        self.made()
        stores = files.stores_at(self.folder)
        self.assertEqual(stores.add_content(None, 'T-1', 'plan', 'two\n', 'a', 1), 3)
        self.assertEqual(stores.read_latest_content(None, 'T-1', 'plan')[0], 3)

    def test_a_stale_number_is_refused_and_nothing_is_written(self) -> None:
        self.made()
        stores = files.stores_at(self.folder)
        stores.add_content(None, 'T-1', 'plan', 'two\n', 'a', 1)
        with self.assertRaises(errors.Task_Error_Changed):
            stores.add_content(None, 'T-1', 'plan', 'late\n', 'a', 1)
        with self.assertRaises(errors.Task_Error_Changed):
            stores.add_content(None, 'T-1', 'plan', 'late\n', 'a', 0)
        self.assertEqual([c.number for c in files.read_contents(self.folder)], [1, 2, 3])

    def test_a_task_in_the_old_shape_or_none_is_not_found(self) -> None:
        stores = files.stores_at(self.folder)
        with self.assertRaises(errors.Task_Error_NotFound):
            stores.add_content(None, 'T-1', 'plan', 'x', 'a', 0)
        self.old()
        with self.assertRaises(errors.Task_Error_NotFound):
            stores.add_content(None, 'T-1', 'plan', 'x', 'a', 0)
        with self.assertRaises(errors.Task_Error_NotFound):
            stores.read_latest_content(None, 'T-1', 'plan')


class Verb(Fixture):

    def test_a_plan_is_added_to_a_new_task_and_its_number_printed(self) -> None:
        self.made()
        self.assertIn('3', self.added('plan', '# Plan\n'))
        content = files.latest_content(self.folder, 'plan')
        self.assertEqual((content.number, content.body, content.header['author']), (3, '# Plan\n', 'memar'))
        self.assertEqual(content.header['follows'], '1')

    def test_a_second_text_of_the_kind_follows_the_first(self) -> None:
        self.made()
        self.added('plan', 'one\n')
        self.added('plan', 'two\n')
        content = files.latest_content(self.folder, 'plan')
        self.assertEqual((content.number, content.header['follows']), (4, '3'))

    def test_a_kind_with_none_yet_is_added_without_follows(self) -> None:
        self.made()
        self.added('message', 'hello\n')
        self.assertNotIn('follows', files.latest_content(self.folder, 'message').header)

    def test_the_author_is_the_one_given(self) -> None:
        self.made()
        self.added('report', 'r\n', 'someone')
        self.assertEqual(files.latest_content(self.folder, 'report').header['author'], 'someone')

    def test_the_text_is_read_from_a_file_when_one_is_given(self) -> None:
        self.made()
        source = self.root / 'source.txt'
        source.write_bytes(b'from file\n')
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            verb.add_task_content('T-1', 'plan', str(source), None)
        self.assertEqual(files.latest_content(self.folder, 'plan').body, 'from file\n')

    def test_a_kind_that_is_no_label_is_refused_and_nothing_is_written(self) -> None:
        self.made()
        said = self.refused(self.added, 'no-such-kind-anywhere', 'x\n')
        self.assertIn('no-such-kind-anywhere', said)
        self.assertEqual([c.number for c in files.read_contents(self.folder)], [1, 2])

    def test_a_task_kind_word_is_a_kind(self) -> None:
        self.made()
        self.added('design', 'd\n')
        self.assertEqual(files.latest_content(self.folder, 'design').number, 3)

    def test_a_task_in_the_old_shape_is_refused_by_name_and_untouched(self) -> None:
        self.old()
        before = sorted(path.name for path in self.folder.iterdir())
        said = self.refused(self.added, 'plan', 'x\n')
        self.assertIn(files.OLD_SHAPE_READER, said)
        self.assertEqual(sorted(path.name for path in self.folder.iterdir()), before)

    def test_a_task_that_is_not_there_is_refused(self) -> None:
        said = self.refused(self.added, 'plan', 'x\n')
        self.assertIn('T-1', said)


if __name__ == '__main__':
    unittest.main()
