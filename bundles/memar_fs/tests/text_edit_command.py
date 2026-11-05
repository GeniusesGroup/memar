#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
TIER = 'system'
BUDGET_SECONDS = 60
import argparse
import contextlib
import io
import sys
import unittest
import unittest.mock
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _scratch import ScratchFolder, bundle


def command():
    return bundle('services.text_edit_command')


class Invoked:

    def __init__(self, code, out: str) -> None:
        self.code = code
        self.out = out

    @property
    def failed(self) -> bool:
        return isinstance(self.code, str) and self.code.startswith('error: ')


def invoke(verb: str, *argv: str, stdin: str = '') -> Invoked:
    parser = argparse.ArgumentParser()
    verbs = parser.add_subparsers()
    describe = command().describe_edit if verb == 'edit' else command().describe_write
    run = describe(verbs)
    arguments = verbs.choices[verb].parse_args(list(argv))
    out = io.StringIO()
    code = 0
    with contextlib.redirect_stdout(out), unittest.mock.patch.object(sys, 'stdin', io.StringIO(stdin)):
        try:
            run(arguments)
        except SystemExit as stopped:
            code = stopped.code
    return Invoked(code, out.getvalue())


class Shape(unittest.TestCase):

    def test_edit_takes_a_file_and_the_flags_it_always_took(self) -> None:
        verbs = argparse.ArgumentParser().add_subparsers()
        command().describe_edit(verbs)
        arguments = verbs.choices['edit'].parse_args(['f.md', '--old', 'a', '--new', 'b', '--all', '--newline', 'crlf'])
        self.assertEqual((arguments.file, arguments.old, arguments.new, arguments.all, arguments.newline), ('f.md', 'a', 'b', True, 'crlf'))
        arguments = verbs.choices['edit'].parse_args(['f.md', '--old-file', 'o', '--new-file', 'n'])
        self.assertEqual((arguments.old_file, arguments.new_file, arguments.all, arguments.newline), ('o', 'n', False, None))

    def test_edit_refuses_a_newline_other_than_lf_or_crlf(self) -> None:
        verbs = argparse.ArgumentParser().add_subparsers()
        command().describe_edit(verbs)
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            verbs.choices['edit'].parse_args(['f.md', '--newline', 'cr'])

    def test_write_takes_a_file_and_the_flags_it_always_took(self) -> None:
        verbs = argparse.ArgumentParser().add_subparsers()
        command().describe_write(verbs)
        arguments = verbs.choices['write'].parse_args(['f.md', '--content-file', 'c', '--newline', 'lf', '--create'])
        self.assertEqual((arguments.file, arguments.content_file, arguments.newline, arguments.create), ('f.md', 'c', 'lf', True))
        arguments = verbs.choices['write'].parse_args(['f.md'])
        self.assertEqual((arguments.content_file, arguments.newline, arguments.create), (None, None, False))


class EditReplacesExactText(ScratchFolder):

    def setUp(self) -> None:
        super().setUp()
        self.target = self.root / 'notes.md'
        self.target.write_text('# Notes\n\nBody\n', encoding='utf-8', newline='\n')

    def test_a_unique_text_is_replaced_and_the_answer_names_the_file_and_one_replacement(self) -> None:
        done = invoke('edit', str(self.target), '--old', '# Notes', '--new', '# Renamed')
        self.assertEqual(done.code, 0)
        self.assertEqual(done.out.strip(), f'edited {self.target.resolve()} (1 replacement)')
        self.assertEqual(self.target.read_bytes(), b'# Renamed\n\nBody\n')

    def test_all_replaces_each_occurrence_and_the_answer_is_plural(self) -> None:
        self.target.write_text('a b a b a\n', encoding='utf-8', newline='\n')
        done = invoke('edit', str(self.target), '--old', 'a', '--new', 'z', '--all')
        self.assertEqual(done.code, 0)
        self.assertIn('(3 replacements)', done.out)
        self.assertEqual(self.target.read_bytes(), b'z b z b z\n')

    def test_the_text_to_replace_and_the_replacement_may_each_be_named_files(self) -> None:
        old = self.root / 'old.txt'
        new = self.root / 'new.txt'
        old.write_bytes('# Notes'.encode('utf-8'))
        new.write_bytes('# Ünï'.encode('utf-8'))
        done = invoke('edit', str(self.target), '--old-file', str(old), '--new-file', str(new))
        self.assertEqual(done.code, 0)
        self.assertEqual(self.target.read_bytes(), '# Ünï\n\nBody\n'.encode('utf-8'))

    def test_a_named_file_wins_over_the_text_given_beside_it(self) -> None:
        old = self.root / 'old.txt'
        new = self.root / 'new.txt'
        old.write_bytes(b'Body')
        new.write_bytes(b'From file')
        invoke('edit', str(self.target), '--old', '# Notes', '--old-file', str(old), '--new', 'ignored', '--new-file', str(new))
        self.assertEqual(self.target.read_bytes(), b'# Notes\n\nFrom file\n')

    def test_a_byte_order_mark_is_removed_and_said_so(self) -> None:
        self.target.write_bytes(b'\xef\xbb\xbf# Notes\n')
        done = invoke('edit', str(self.target), '--old', '# Notes', '--new', '# Renamed')
        self.assertEqual(self.target.read_bytes(), b'# Renamed\n')
        self.assertIn('note: notes.md had a BOM; the write removes it', done.out)

    def test_the_newline_asked_for_is_written_and_the_files_own_is_kept_otherwise(self) -> None:
        invoke('edit', str(self.target), '--old', 'Body', '--new', 'Text', '--newline', 'crlf')
        self.assertEqual(self.target.read_bytes(), b'# Notes\r\n\r\nText\r\n')
        invoke('edit', str(self.target), '--old', 'Text', '--new', 'Last')
        self.assertEqual(self.target.read_bytes(), b'# Notes\r\n\r\nLast\r\n')
        invoke('edit', str(self.target), '--old', 'Last', '--new', 'Back', '--newline', 'lf')
        self.assertEqual(self.target.read_bytes(), b'# Notes\n\nBack\n')

    def test_the_edit_waits_for_the_lock_of_the_file_and_leaves_none_behind(self) -> None:
        self.blocked_while_locked(self.target, lambda: invoke('edit', str(self.target), '--old', '# Notes', '--new', '# Renamed'))
        self.assertEqual(self.target.read_bytes(), b'# Renamed\n\nBody\n')
        self.assertEqual(self.held_locks(), [])


class EditRefuses(ScratchFolder):

    def setUp(self) -> None:
        super().setUp()
        self.target = self.root / 'notes.md'
        self.target.write_text('# Notes\n\nBody\n', encoding='utf-8', newline='\n')

    def refused(self, *argv: str, said: str = '') -> None:
        before = self.target.read_bytes()
        done = invoke('edit', *argv)
        self.assertTrue(done.failed, done.code)
        self.assertIn(said, done.code)
        self.assertEqual(self.target.read_bytes(), before)
        self.assertEqual(self.held_locks(), [])

    def test_an_absent_match_is_refused_and_says_nothing_was_written(self) -> None:
        self.refused(str(self.target), '--old', '# Absent', '--new', 'x', said='Nothing was written')

    def test_an_ambiguous_match_is_refused_and_says_how_many_times_it_occurs(self) -> None:
        self.target.write_text('a a\n', encoding='utf-8', newline='\n')
        self.refused(str(self.target), '--old', 'a', '--new', 'z', said='occurs 2 times')

    def test_an_empty_text_to_replace_is_refused(self) -> None:
        self.refused(str(self.target), '--old', '', '--new', 'x', said='must not be empty')

    def test_a_call_naming_no_text_to_replace_or_no_replacement_is_refused(self) -> None:
        self.refused(str(self.target), '--new', 'x', said='needs the text to replace')
        self.refused(str(self.target), '--old', '# Notes', said='needs the replacement')

    def test_a_path_that_is_not_a_file_is_refused(self) -> None:
        for path in (self.root, self.root / 'absent.md'):
            with self.subTest(path=path.name):
                done = invoke('edit', str(path), '--old', 'a', '--new', 'b')
                self.assertTrue(done.failed, done.code)

    def test_a_content_of_a_task_is_refused_and_left_as_it_is(self) -> None:
        content = self.root / 'content.00001.md'
        content.write_text('---\nkind: plan\n---\nkept\n', encoding='utf-8', newline='\n')
        before = content.read_bytes()
        done = invoke('edit', str(content), '--old', 'kept', '--new', 'lost')
        self.assertTrue(done.failed, done.code)
        self.assertIn('content of a task', done.code)
        self.assertEqual(content.read_bytes(), before)

    def test_a_file_that_is_not_utf8_is_refused(self) -> None:
        self.target.write_bytes(b'caf\xe9\n')
        self.refused(str(self.target), '--old', 'caf', '--new', 'x', said='not valid UTF-8')

    def test_a_named_text_that_is_not_utf8_is_a_failure_and_nothing_is_written(self) -> None:
        old = self.root / 'old.txt'
        old.write_bytes(b'caf\xe9')
        self.refused(str(self.target), '--old-file', str(old), '--new', 'x', said='not valid UTF-8')

    def test_a_named_file_that_cannot_be_read_is_a_failure(self) -> None:
        self.refused(str(self.target), '--old-file', str(self.root / 'absent.txt'), '--new', 'x', said='cannot read')
        self.refused(str(self.target), '--old', '# Notes', '--new-file', str(self.root / 'absent.txt'), said='cannot read')


class WritePutsAWholeText(ScratchFolder):

    def setUp(self) -> None:
        super().setUp()
        self.target = self.root / 'notes.md'
        self.target.write_text('# Notes\n', encoding='utf-8', newline='\n')

    def test_a_text_from_standard_input_is_written_as_utf8_without_a_mark_and_the_answer_says_so(self) -> None:
        done = invoke('write', str(self.target), stdin='# Ünï\n')
        data = self.target.read_bytes()
        self.assertEqual(done.code, 0)
        self.assertEqual(data, '# Ünï\n'.encode('utf-8'))
        self.assertEqual(done.out.strip(), f"rewrote {self.target.resolve()} ({len(data)} bytes, utf-8, no BOM, '\\n' newlines)")

    def test_a_final_newline_is_added(self) -> None:
        invoke('write', str(self.target), stdin='# A')
        self.assertEqual(self.target.read_bytes(), b'# A\n')

    def test_a_new_file_needs_create_gets_lf_and_missing_parent_folders_and_the_answer_says_wrote(self) -> None:
        fresh = self.root / 'deep' / 'er' / 'fresh.md'
        done = invoke('write', str(fresh), '--create', stdin='# A\n\nB\n')
        self.assertEqual(done.code, 0)
        self.assertTrue(done.out.startswith('wrote '))
        self.assertEqual(fresh.read_bytes(), b'# A\n\nB\n')

    def test_the_text_may_be_the_content_of_a_named_file_and_the_file_wins(self) -> None:
        source = self.root / 'payload.md'
        source.write_bytes('# From disk ü\n'.encode('utf-8'))
        invoke('write', str(self.target), '--content-file', str(source), stdin='ignored')
        self.assertEqual(self.target.read_bytes(), '# From disk ü\n'.encode('utf-8'))

    def test_a_leading_mark_in_the_named_file_stays_as_the_character_u_feff(self) -> None:
        source = self.root / 'payload.md'
        source.write_bytes(b'\xef\xbb\xbf# Marked\n')
        invoke('write', str(self.target), '--content-file', str(source))
        self.assertEqual(self.target.read_bytes(), b'\xef\xbb\xbf# Marked\n')

    def test_a_mark_in_an_overwritten_file_is_removed_and_said_so(self) -> None:
        self.target.write_bytes(b'\xef\xbb\xbf# Notes\n')
        done = invoke('write', str(self.target), stdin='# New\n')
        self.assertEqual(self.target.read_bytes(), b'# New\n')
        self.assertIn('note: notes.md had a BOM; the write removes it', done.out)

    def test_the_newline_asked_for_is_written_and_the_files_own_is_kept_otherwise(self) -> None:
        for flag, expected in (('crlf', b'# A\r\n\r\nB\r\n'), ('lf', b'# A\n\nB\n')):
            with self.subTest(flag=flag):
                invoke('write', str(self.target), '--newline', flag, stdin='# A\n\nB\n')
                self.assertEqual(self.target.read_bytes(), expected)
        self.target.write_bytes(b'# Old\r\n')
        invoke('write', str(self.target), stdin='# A\n\nB\n')
        self.assertEqual(self.target.read_bytes(), b'# A\r\n\r\nB\r\n')

    def test_a_named_file_in_a_temp_folder_of_a_task_is_read(self) -> None:
        task = self.root / '20261017-T000000Z-1111'
        for part in ('docs', 'temp'):
            (task / part).mkdir(parents=True)
        (task / 'plan.md').write_text('---\nTitle: T\n---\n', encoding='utf-8')
        scratch = task / 'temp' / '_draft.md'
        scratch.write_text('x\n', encoding='utf-8', newline='\n')
        done = invoke('write', str(self.target), '--content-file', str(scratch))
        self.assertEqual(done.code, 0)
        self.assertEqual(self.target.read_bytes(), b'x\n')

    def test_the_write_waits_for_the_lock_of_the_file_and_leaves_none_behind(self) -> None:
        self.blocked_while_locked(self.target, lambda: invoke('write', str(self.target), stdin='# Later\n'))
        self.assertEqual(self.target.read_bytes(), b'# Later\n')
        self.assertEqual(self.held_locks(), [])


class WriteRefuses(ScratchFolder):

    def setUp(self) -> None:
        super().setUp()
        self.target = self.root / 'notes.md'
        self.target.write_text('# Notes\n', encoding='utf-8', newline='\n')

    def test_an_absent_file_is_not_created_unless_asked_for(self) -> None:
        absent = self.root / 'absent.md'
        done = invoke('write', str(absent), stdin='x\n')
        self.assertTrue(done.failed, done.code)
        self.assertIn('Nothing was written', done.code)
        self.assertFalse(absent.exists())

    def test_a_folder_is_not_a_file_to_write_unless_creating_is_asked(self) -> None:
        done = invoke('write', str(self.root), stdin='x\n')
        self.assertTrue(done.failed, done.code)

    def test_an_empty_or_blank_text_is_refused_and_the_file_is_kept(self) -> None:
        for text in ('', '  \n\t\n'):
            with self.subTest(text=text):
                done = invoke('write', str(self.target), stdin=text)
                self.assertTrue(done.failed, done.code)
                self.assertIn('Nothing was written', done.code)
                self.assertEqual(self.target.read_bytes(), b'# Notes\n')

    def test_a_named_file_that_is_not_utf8_is_refused(self) -> None:
        source = self.root / 'payload.md'
        source.write_bytes(b'caf\xe9\n')
        done = invoke('write', str(self.target), '--content-file', str(source))
        self.assertTrue(done.failed, done.code)
        self.assertIn('not valid UTF-8', done.code)
        self.assertEqual(self.target.read_bytes(), b'# Notes\n')

    def test_an_overwritten_file_that_is_not_utf8_is_refused(self) -> None:
        self.target.write_bytes(b'caf\xe9\n')
        done = invoke('write', str(self.target), stdin='# New\n')
        self.assertTrue(done.failed, done.code)
        self.assertEqual(self.target.read_bytes(), b'caf\xe9\n')

    def test_a_write_over_a_content_of_a_task_is_refused_and_leaves_it_as_it_is(self) -> None:
        content = self.root / 'content.00001.md'
        content.write_text('---\nkind: plan\n---\nkept\n', encoding='utf-8', newline='\n')
        before = content.read_bytes()
        done = invoke('write', str(content), stdin='# New\n')
        self.assertTrue(done.failed, done.code)
        self.assertIn('content of a task', done.code)
        self.assertEqual(content.read_bytes(), before)

    def test_a_new_content_of_a_task_is_not_made_by_hand_either(self) -> None:
        content = self.root / 'content.00002.md'
        done = invoke('write', str(content), '--create', stdin='# New\n')
        self.assertTrue(done.failed, done.code)
        self.assertFalse(content.exists())

    def test_a_named_file_in_a_task_folder_outside_its_temp_folder_is_refused(self) -> None:
        task = self.root / '20261017-T000000Z-1111'
        for part in ('docs', 'temp'):
            (task / part).mkdir(parents=True)
        (task / 'plan.md').write_text('---\nTitle: T\n---\n', encoding='utf-8')
        kept = task / 'docs' / '_draft.md'
        kept.write_text('x\n', encoding='utf-8', newline='\n')
        done = invoke('write', str(self.target), '--content-file', str(kept))
        self.assertTrue(done.failed, done.code)
        self.assertIn('outside its temp/ folder', done.code)
        self.assertEqual(self.target.read_bytes(), b'# Notes\n')

    def test_a_named_file_that_cannot_be_read_is_a_failure(self) -> None:
        done = invoke('write', str(self.target), '--content-file', str(self.root / 'absent.md'))
        self.assertTrue(done.failed, done.code)
        self.assertIn('cannot read', done.code)


class WriteFails(ScratchFolder):

    def test_creating_at_the_path_of_a_folder_is_a_failure(self) -> None:
        folder = self.root / 'folder'
        folder.mkdir()
        done = invoke('write', str(folder), '--create', stdin='x\n')
        self.assertTrue(done.failed, done.code)


if __name__ == '__main__':
    unittest.main(verbosity=2)
