#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
TIER = 'system'
BUDGET_SECONDS = 60
import os
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _scratch import ScratchFolder, bundle


def held(path: Path):
    return bundle('services.text_edit_store').Text_Edit_Store_Held(path)


def text_errors():
    from importlib import import_module
    return import_module('modules.knowledge.text.errors.edit')


class Exists(ScratchFolder):

    def test_a_file_is_a_held_text(self) -> None:
        target = self.root / 'notes.md'
        target.write_bytes(b'x\n')
        self.assertTrue(held(target).exists())

    def test_an_absent_path_is_not(self) -> None:
        self.assertFalse(held(self.root / 'absent.md').exists())

    def test_a_folder_is_not(self) -> None:
        self.assertFalse(held(self.root).exists())


class GetBytes(ScratchFolder):

    def test_the_bytes_of_the_file_are_answered_as_they_are(self) -> None:
        target = self.root / 'notes.md'
        target.write_bytes(b'\xef\xbb\xbf# A\r\n\xe9')
        self.assertEqual(held(target).get_bytes(), b'\xef\xbb\xbf# A\r\n\xe9')

    def test_a_file_that_cannot_be_read_is_a_failure_and_not_a_refusal(self) -> None:
        for path in (self.root / 'absent.md', self.root):
            with self.subTest(path=path.name):
                with self.assertRaises(text_errors().Text_Error_Edit_ReadFailed) as failed:
                    held(path).get_bytes()
                self.assertNotIsInstance(failed.exception, text_errors().Text_Error_Edit_Refusal)


class ReplaceBytes(ScratchFolder):

    def test_the_bytes_replace_those_of_the_file_exactly(self) -> None:
        target = self.root / 'notes.md'
        target.write_bytes(b'old\n')
        held(target).replace_bytes(b'\xef\xbb\xbfnew\r\n')
        self.assertEqual(target.read_bytes(), b'\xef\xbb\xbfnew\r\n')

    def test_what_the_held_text_needs_to_exist_is_made(self) -> None:
        target = self.root / 'deep' / 'er' / 'fresh.md'
        held(target).replace_bytes(b'x\n')
        self.assertEqual(target.read_bytes(), b'x\n')

    def test_a_write_that_cannot_be_made_is_a_failure_and_not_a_refusal(self) -> None:
        folder = self.root / 'folder'
        folder.mkdir()
        with self.assertRaises(text_errors().Text_Error_Edit_WriteFailed) as failed:
            held(folder).replace_bytes(b'x\n')
        self.assertNotIsInstance(failed.exception, text_errors().Text_Error_Edit_Refusal)


class GetStamp(ScratchFolder):

    def setUp(self) -> None:
        super().setUp()
        self.target = self.root / 'notes.md'
        self.target.write_bytes(b'one\n')
        self.store = held(self.target)

    def test_a_text_that_did_not_move_has_the_same_stamp(self) -> None:
        first = self.store.get_stamp()
        second = self.store.get_stamp()
        self.assertTrue(first.is_same(second))
        self.assertTrue(second.is_same(first))

    def test_an_absent_text_stamps_the_same_while_it_stays_absent(self) -> None:
        absent = held(self.root / 'absent.md')
        self.assertTrue(absent.get_stamp().is_same(absent.get_stamp()))

    def test_a_text_that_appears_or_disappears_has_another_stamp(self) -> None:
        absent = held(self.root / 'later.md')
        before = absent.get_stamp()
        (self.root / 'later.md').write_bytes(b'x\n')
        self.assertFalse(before.is_same(absent.get_stamp()))
        after = absent.get_stamp()
        (self.root / 'later.md').unlink()
        self.assertFalse(after.is_same(absent.get_stamp()))

    def test_changed_content_has_another_stamp(self) -> None:
        before = self.store.get_stamp()
        stat = self.target.stat()
        self.target.write_bytes(b'two\n')
        os.utime(self.target, ns=(stat.st_atime_ns, stat.st_mtime_ns))
        self.assertFalse(before.is_same(self.store.get_stamp()))

    def test_a_touch_that_leaves_the_content_has_another_stamp(self) -> None:
        before = self.store.get_stamp()
        stat = self.target.stat()
        os.utime(self.target, ns=(stat.st_atime_ns, stat.st_mtime_ns + 5_000_000_000))
        self.assertFalse(before.is_same(self.store.get_stamp()))


if __name__ == '__main__':
    unittest.main(verbosity=2)
