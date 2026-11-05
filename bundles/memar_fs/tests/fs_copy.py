#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
TIER = 'system'
BUDGET_SECONDS = 60
import shutil
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _scratch import ScratchFolder, bundle, errors, junction_or_symlink

def copy(*args, **keywords):
    return bundle('services.fs_copy').copy(*args, **keywords)

IGNORE = shutil.ignore_patterns('*.pyc', 'node_modules')

class Fixture(ScratchFolder):

    def setUp(self) -> None:
        super().setUp()
        self.source = self.root / 'source'
        (self.source / 'part').mkdir(parents=True)
        (self.source / 'a.md').write_text('alpha\n', encoding='utf-8')
        (self.source / 'part' / 'b.md').write_text('beta\n', encoding='utf-8')
        self.dest = self.root / 'dest'
        shutil.copytree(self.source, self.dest, ignore=IGNORE)

class CopyMatches(Fixture):

    def test_a_copy_matches_its_source(self) -> None:
        self.assertFalse(copy(self.source, self.dest, IGNORE))

    def test_what_the_ignore_leaves_out_is_not_compared_on_either_side(self) -> None:
        (self.source / 'node_modules').mkdir()
        (self.source / 'node_modules' / 'dep.js').write_text('dev\n', encoding='utf-8')
        (self.dest / 'part' / 'x.pyc').write_bytes(b'\x00')
        self.assertFalse(copy(self.source, self.dest, IGNORE))

    def test_a_folder_whose_name_is_left_out_is_not_entered(self) -> None:
        (self.dest / 'node_modules' / 'deep').mkdir(parents=True)
        (self.dest / 'node_modules' / 'deep' / 'x.js').write_text('x\n', encoding='utf-8')
        self.assertFalse(copy(self.source, self.dest, IGNORE))

    def test_ignore_is_given_each_folder_reached_with_the_names_it_holds(self) -> None:
        reached: dict = {}

        def ignore(folder, held):
            reached[Path(folder).name] = sorted(held)
            return []
        copy(self.source, self.dest, ignore)
        self.assertEqual(reached['source'], ['a.md', 'part'])
        self.assertEqual(reached['part'], ['b.md'])

class CopyDiffers(Fixture):

    def test_a_change_an_addition_or_a_removal_differs(self) -> None:
        cases = (lambda: (self.dest / 'a.md').write_text('alphA\n', encoding='utf-8'), lambda: (self.dest / 'extra.md').write_text('mine\n', encoding='utf-8'), lambda: (self.dest / 'part' / 'b.md').unlink())
        for change in cases:
            with self.subTest(change=change):
                shutil.rmtree(self.dest)
                shutil.copytree(self.source, self.dest, ignore=IGNORE)
                change()
                self.assertTrue(copy(self.source, self.dest, IGNORE))

    def test_a_change_on_the_source_side_differs(self) -> None:
        (self.source / 'a.md').write_text('alphA\n', encoding='utf-8')
        self.assertTrue(copy(self.source, self.dest, IGNORE))

    def test_a_missing_copy_differs_from_a_source_that_holds_a_file_and_never_raises(self) -> None:
        self.assertTrue(copy(self.source, self.root / 'absent', IGNORE))

    def test_two_absent_folders_do_not_differ(self) -> None:
        self.assertFalse(copy(self.root / 'absent-one', self.root / 'absent-two', IGNORE))

    def test_a_link_to_a_folder_is_neither_entered_nor_counted(self) -> None:
        elsewhere = self.root / 'elsewhere'
        elsewhere.mkdir()
        (elsewhere / 'e.md').write_text('e\n', encoding='utf-8')
        if not junction_or_symlink(self.source / 'via', elsewhere):
            self.skipTest('this machine makes no folder link')
        self.assertFalse(copy(self.source, self.dest, IGNORE))
if __name__ == '__main__':
    unittest.main(verbosity=2)
