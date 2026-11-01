#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the conversation widget and its verbs, `conversation.py`, `services/post.py` and `services/latest.py`.

    python modules-plugable/management/timeline/widgets/conversation/tests/conversation.py

The subject is the Khayyam of `conversation.kh` (`Post`, `Latest`, `Share`) over `Content_Add`, `Content_Read`,
`Timeline_Place` and `Timeline_Latest`. What is pinned:

  Widget     `Post` checks the bytes and the kind's own check, creates the content, places it and answers the
             number; a refused check creates nothing; a refused placement leaves the content unplaced; `Latest`
             answers the latest text of a kind; `Share` places a content with the kind it was created with.
  Verb       `memar conversation post` reads the text from a file or standard input and places it in the timeline
             of the UUID; a second post follows it; a stale latest is refused and nothing is written; a UUID that is
             no timeline, or a task in the old shape, is refused; `latest` prints the text.
"""
from __future__ import annotations
from importlib import import_module
from machine.plugable_import import load as plugable_load
_m_fs_test_scratch = plugable_load('computer.memory.filesystem.services.fs_test_scratch')
suite_scratch = _m_fs_test_scratch.suite_scratch
_m_fs_memar = plugable_load('computer.memory.filesystem.services.fs_memar')
memar_fs = _m_fs_memar
import argparse
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
base = 'modules-plugable.management.timeline.widgets.conversation'
conversation = import_module(f'{base}.conversation')
post = import_module(f'{base}.services.post')
latest = import_module(f'{base}.services.latest')
task_files = import_module('modules-plugable.management.task.services.task_memory')
plan_file = import_module('modules-plugable.management.task.services.plan_file')
timeline_files = import_module('modules.management.timeline.services.timeline_files')
placement_errors = import_module('modules.management.timeline.errors.placement')
bytes_errors = import_module('modules.knowledge.text.errors.bytes')
structure_errors = import_module('modules.knowledge.text.errors.structure')


class Memory:

    def __init__(self) -> None:
        self.contents = {}
        self.placements = []
        self.fail_with = None

    def add_content(self, kind, text):
        uuid = f'c-{len(self.contents) + 1}'
        self.contents[uuid] = (kind, text)
        return uuid

    def read_content(self, content):
        kind, text = self.contents.get(content, ('', ''))
        return (kind, text, content in self.contents)

    def read_latest_placement(self, timeline, kind):
        found = [p for p in self.placements if p[0] == timeline and p[2] == kind]
        return (len(found) and found[-1][5], found[-1][1], True) if found else (0, '', False)

    def add_placement(self, timeline, content, kind, placer, placed_at, after):
        if self.fail_with:
            raise self.fail_with
        number = len(self.placements) + 1
        self.placements.append((timeline, content, kind, placer, placed_at, number))
        return number


class Widget(unittest.TestCase):

    def test_a_text_is_checked_created_and_placed_and_its_number_returned(self) -> None:
        memory = Memory()
        number = conversation.Conversation().post(memory, memory, 'T', 'hello\n', 'message', 'u', 0)
        self.assertEqual(number, 1)
        self.assertEqual(memory.contents, {'c-1': ('message', 'hello\n')})
        self.assertEqual(memory.placements[0][:4], ('T', 'c-1', 'message', 'u'))

    def test_a_text_whose_bytes_are_refused_creates_nothing(self) -> None:
        memory = Memory()
        with self.assertRaises(bytes_errors.Text_Error_Bytes_NoFinalNewline):
            conversation.Conversation().post(memory, memory, 'T', 'no newline', 'message', 'u', 0)
        self.assertEqual((memory.contents, memory.placements), ({}, []))

    def test_the_check_of_a_kind_with_a_template_runs_and_a_kind_without_one_has_none(self) -> None:
        memory = Memory()
        seen = []

        def refuse(text):
            seen.append(text)
            raise ValueError('not a plan')
        widget = conversation.Conversation(kind_checks={'plan': refuse})
        with self.assertRaises(ValueError):
            widget.post(memory, memory, 'T', 'x\n', 'plan', 'u', 0)
        self.assertEqual((seen, memory.contents), (['x\n'], {}))
        widget.post(memory, memory, 'T', 'x\n', 'message', 'u', 0)
        self.assertEqual(seen, ['x\n'])

    def test_a_text_of_only_headings_and_blank_lines_creates_nothing(self) -> None:
        memory = Memory()
        for text in ('# Plan\n', '# Plan\n\n## Part\n', '\n', '\n\n'):
            with self.assertRaises(structure_errors.Text_Error_Structure_Empty):
                conversation.Conversation().post(memory, memory, 'T', text, 'message', 'u', 0)
        self.assertEqual((memory.contents, memory.placements), ({}, []))

    def test_a_refused_placement_leaves_the_content_unplaced(self) -> None:
        memory = Memory()
        memory.fail_with = placement_errors.Timeline_Error_Changed()
        with self.assertRaises(placement_errors.Timeline_Error_Changed):
            conversation.Conversation().post(memory, memory, 'T', 'x\n', 'message', 'u', 0)
        self.assertEqual((len(memory.contents), memory.placements), (1, []))

    def test_the_latest_of_a_kind_answers_its_number_and_text(self) -> None:
        memory = Memory()
        widget = conversation.Conversation()
        self.assertEqual(widget.latest(memory, memory, 'T', 'message'), (0, '', False))
        widget.post(memory, memory, 'T', 'one\n', 'message', 'u', 0)
        self.assertEqual(widget.latest(memory, memory, 'T', 'message'), (1, 'one\n', True))

    def test_a_content_is_shared_with_the_kind_it_was_created_with(self) -> None:
        memory = Memory()
        content = memory.add_content('critique', 'c\n')
        number = conversation.Conversation().share(memory, memory, content, 'T2', 'u', 0)
        self.assertEqual((number, memory.placements[0][:3]), (1, ('T2', content, 'critique')))


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
        located = unittest.mock.patch.object(conversation, 'folder_of', return_value=self.folder)
        located.start()
        self.addCleanup(located.stop)

    def made(self) -> None:
        task_files.create_task(self.folder, 'T-1', 'A title', None, None, self.project, 'queued', 7, None, None)

    def old(self) -> None:
        (self.folder / plan_file.PLAN_NAME).write_text('---\nTitle: T\nStatus: Queued\nStart Date: 2026-10-13T00:00:00Z\n---\n# T\n', encoding='utf-8', newline='\n')

    def posted(self, kind: str, text: str, author: str | None = None, refs: tuple = ()) -> str:
        out = io.StringIO()
        with contextlib.redirect_stdout(out), unittest.mock.patch.object(sys, 'stdin', io.StringIO(text)):
            post.post_text('T-1', kind, None, author, refs)
        return out.getvalue()

    def refused(self, call, *args) -> str:
        with self.assertRaises(SystemExit) as raised:
            call(*args)
        return str(raised.exception.code)


class Verb(Fixture):

    def test_a_plan_is_posted_to_a_new_task_and_its_number_printed(self) -> None:
        self.made()
        self.assertIn('1', self.posted('plan', 'Plan text\n'))
        stored = timeline_files.latest_content(self.folder, 'plan')
        self.assertEqual((stored.number, stored.body, stored.header['author']), (1, 'Plan text\n', 'memar'))
        self.assertNotIn('follows', stored.header)

    def test_a_second_post_of_the_kind_follows_the_first(self) -> None:
        self.made()
        self.posted('plan', 'one\n')
        self.posted('plan', 'two\n')
        stored = timeline_files.latest_content(self.folder, 'plan')
        self.assertEqual((stored.number, stored.header['follows']), (2, '1'))

    def test_a_kind_with_none_yet_is_posted_without_follows(self) -> None:
        self.made()
        self.posted('message', 'hello\n')
        self.assertNotIn('follows', timeline_files.latest_content(self.folder, 'message').header)

    def test_refs_are_written_to_the_header_a_bare_number_meaning_this_timeline(self) -> None:
        self.made()
        self.posted('message', 'r\n', None, ('5', 'OTHER-2:3'))
        self.assertEqual(timeline_files.latest_content(self.folder, 'message').header['refs'], 'T-1:5\nOTHER-2:3')

    def test_a_post_without_refs_has_no_refs_field(self) -> None:
        self.made()
        self.posted('message', 'r\n')
        self.assertNotIn('refs', timeline_files.latest_content(self.folder, 'message').header)

    def test_a_ref_that_is_no_number_is_refused_and_nothing_is_written(self) -> None:
        self.made()
        for bad in ('abc', 'T-2:x', 'T-2:0', ':4', '-1'):
            with self.subTest(bad=bad):
                self.refused(self.posted, 'message', 'r\n', None, (bad,))
        self.assertEqual(timeline_files.read_contents(self.folder), [])

    def test_the_verb_declares_a_repeatable_refs_argument(self) -> None:
        parser = argparse.ArgumentParser()
        verbs = parser.add_subparsers()
        post.describe(verbs)
        given = parser.parse_args(['post', '--timeline', 'T-1', '--kind', 'message', '--refs', '5', '--refs', 'X:2'])
        self.assertEqual(given.refs, ['5', 'X:2'])

    def test_the_placer_is_the_one_given(self) -> None:
        self.made()
        self.posted('report', 'r\n', 'someone')
        self.assertEqual(timeline_files.latest_content(self.folder, 'report').header['author'], 'someone')

    def test_the_text_is_read_from_a_file_when_one_is_given(self) -> None:
        self.made()
        source = self.root / 'source.txt'
        source.write_bytes(b'from file\n')
        with contextlib.redirect_stdout(io.StringIO()):
            post.post_text('T-1', 'plan', str(source), None)
        self.assertEqual(timeline_files.latest_content(self.folder, 'plan').body, 'from file\n')

    def test_a_stale_latest_is_refused_and_nothing_is_written(self) -> None:
        self.made()
        real = timeline_files.FileTimeline.read_latest_placement

        def raced(this, timeline, kind):
            answer = real(this, timeline, kind)
            timeline_files.write_content(self.folder, 'plan', 'rival\n', 'other')
            return answer
        with unittest.mock.patch.object(timeline_files.FileTimeline, 'read_latest_placement', raced):
            said = self.refused(self.posted, 'plan', 'mine\n')
        self.assertIn('T-1', said)
        self.assertEqual([c.body for c in timeline_files.read_contents(self.folder) if c.header['kind'] == 'plan'][-1], 'rival\n')
        self.assertEqual(len(timeline_files.read_contents(self.folder)), 1)

    def test_a_text_whose_bytes_are_refused_writes_nothing(self) -> None:
        self.made()
        said = self.refused(self.posted, 'plan', 'no newline')
        self.assertIn('newline', said)
        self.assertEqual(len(timeline_files.read_contents(self.folder)), 0)

    def test_a_kind_that_is_no_label_is_refused_and_nothing_is_written(self) -> None:
        self.made()
        said = self.refused(self.posted, 'no-such-kind-anywhere', 'x\n')
        self.assertIn('no-such-kind-anywhere', said)
        self.assertEqual(len(timeline_files.read_contents(self.folder)), 0)

    def test_a_text_of_only_headings_and_blank_lines_is_refused_and_nothing_is_written(self) -> None:
        self.made()
        for text in ('# Plan\n', '# Plan\n\n## Part\n', '\n'):
            said = self.refused(self.posted, 'plan', text)
            self.assertIn('nothing was written', said)
        self.assertEqual(len(timeline_files.read_contents(self.folder)), 0)

    def test_the_kinds_of_the_templates_are_the_kinds_the_documentation_modules_declare(self) -> None:
        self.assertEqual(post.FIXED_KINDS, ('message',))
        self.assertEqual(set(post.template_kinds()), {'plan', 'report', 'changelog', 'question', 'decision', 'assumption', 'anticipated-work', 'research', 'approval'})

    def test_a_kind_with_no_declared_template_is_checked_as_a_label(self) -> None:
        self.assertNotIn('no-such-kind-anywhere', post.template_kinds())
        said = self.refused(post.checked_kind, 'no-such-kind-anywhere', self.project)
        self.assertIn('no-such-kind-anywhere', said)
        self.assertEqual(post.checked_kind('plan', self.project), 'plan')

    def test_a_task_in_the_old_shape_is_refused_by_name_and_untouched(self) -> None:
        self.old()
        before = sorted(path.name for path in self.folder.iterdir())
        said = self.refused(self.posted, 'plan', 'x\n')
        self.assertIn(task_files.OLD_SHAPE_READER, said)
        self.assertEqual(sorted(path.name for path in self.folder.iterdir()), before)

    def test_a_uuid_that_is_no_timeline_is_refused(self) -> None:
        said = self.refused(self.posted, 'plan', 'x\n')
        self.assertIn('T-1', said)

    def test_latest_prints_the_text_of_the_latest_of_a_kind(self) -> None:
        self.made()
        self.posted('message', 'first\n')
        self.posted('message', 'second\n')
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            latest.latest_text('T-1', 'message')
        self.assertEqual(out.getvalue(), 'second\n')

    def test_latest_of_a_kind_with_none_is_refused(self) -> None:
        self.made()
        said = self.refused(latest.latest_text, 'T-1', 'message')
        self.assertIn('message', said)


if __name__ == '__main__':
    unittest.main()
