#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
TIER = 'system'
BUDGET_SECONDS = 120
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _scratch import ScratchFolder, bundle, errors, junction_or_symlink

def trash(*args, **keywords):
    return bundle('services.trash').trash(*args, **keywords)

class TrashMovesToTheRecycleBin(ScratchFolder):

    def setUp(self) -> None:
        super().setUp()
        self.first = self.root / 'first.md'
        self.second = self.root / 'second'
        self.first.write_text('one\n', encoding='utf-8', newline='\n')
        self.second.mkdir()
        (self.second / 'inner.md').write_text('two\n', encoding='utf-8', newline='\n')

    def test_a_file_and_a_folder_are_no_longer_where_they_were(self) -> None:
        trash([self.first, self.second])
        self.assertFalse(self.first.exists())
        self.assertFalse(self.second.exists())

    def test_a_link_whose_target_is_gone_counts_as_present_and_is_moved(self) -> None:
        gone = self.root / 'gone'
        gone.mkdir()
        dangling = self.root / 'dangling'
        if not junction_or_symlink(dangling, gone):
            self.skipTest('this machine makes no folder link')
        gone.rmdir()
        trash([dangling])
        self.assertFalse(dangling.is_symlink())
        self.assertFalse(dangling.exists())

class TrashRefuses(ScratchFolder):

    def test_an_absent_path_is_refused(self) -> None:
        with self.assertRaises(errors().PathAbsent):
            trash([self.root / 'absent.md'])

    def test_the_paths_go_one_by_one_so_those_before_a_refused_one_are_already_moved(self) -> None:
        before = self.root / 'before.md'
        after = self.root / 'after.md'
        before.write_text('b\n', encoding='utf-8', newline='\n')
        after.write_text('a\n', encoding='utf-8', newline='\n')
        with self.assertRaises(errors().PathAbsent):
            trash([before, self.root / 'absent.md', after])
        self.assertFalse(before.exists())
        self.assertTrue(after.exists())
if __name__ == '__main__':
    unittest.main(verbosity=2)
