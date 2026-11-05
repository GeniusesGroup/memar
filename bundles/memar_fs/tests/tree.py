#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
TIER = 'system'
BUDGET_SECONDS = 60
import re
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _scratch import ScratchFolder, bundle, errors, junction_or_symlink

def tree(*args, **keywords):
    return bundle('services.tree').tree(*args, **keywords)

def names(listing: str) -> list[str]:
    return [re.sub('^[\\s|`+\\\\/-]*', '', line).rstrip('/') for line in listing.splitlines() if line.strip()]

class TreeDrawsAFolder(ScratchFolder):

    def setUp(self) -> None:
        super().setUp()
        self.top = self.root / 'top'
        for folder in ('Beta', 'alpha', 'alpha/inner'):
            (self.top / folder).mkdir(parents=True)
        for file in ('zeta.md', 'Eta.md', 'alpha/inner/leaf.md'):
            (self.top / file).write_text('x\n', encoding='utf-8', newline='\n')

    def test_the_first_line_is_the_name_of_the_root_and_the_drawing_is_ascii(self) -> None:
        listing = tree(self.top)
        self.assertEqual(listing.splitlines()[0].strip(), 'top')
        self.assertTrue(listing.isascii())

    def test_folders_come_before_files_each_group_in_case_insensitive_name_order(self) -> None:
        self.assertEqual(names(tree(self.top)), ['top', 'alpha', 'inner', 'leaf.md', 'Beta', 'Eta.md', 'zeta.md'])

    def test_with_dirs_only_no_file_is_listed(self) -> None:
        self.assertEqual(names(tree(self.top, dirs_only=True)), ['top', 'alpha', 'inner', 'Beta'])

    def test_entries_named_git_pycache_venv_or_node_modules_are_left_out_with_all_they_hold(self) -> None:
        for skipped in ('.git', '__pycache__', '.venv', 'node_modules'):
            (self.top / skipped).mkdir()
            (self.top / skipped / 'hidden.md').write_text('x\n', encoding='utf-8', newline='\n')
        (self.top / 'alpha' / 'node_modules').write_text('a file of that name\n', encoding='utf-8', newline='\n')
        listing = names(tree(self.top))
        for skipped in ('.git', '__pycache__', '.venv', 'node_modules', 'hidden.md'):
            self.assertNotIn(skipped, listing)

    def test_a_link_to_a_folder_counts_as_a_folder_and_is_followed(self) -> None:
        if not junction_or_symlink(self.top / 'via', self.top / 'alpha'):
            self.skipTest('this machine makes no folder link')
        listing = names(tree(self.top))
        self.assertEqual(listing.count('leaf.md'), 2)
        self.assertLess(listing.index('via'), listing.index('Eta.md'))

class TreeRefuses(ScratchFolder):

    def test_a_root_that_is_not_a_folder_is_refused(self) -> None:
        plain = self.root / 'plain.md'
        plain.write_text('x\n', encoding='utf-8', newline='\n')
        for root in (plain, self.root / 'absent'):
            with self.subTest(root=root.name):
                with self.assertRaises(errors().NotAFolder):
                    tree(root)
if __name__ == '__main__':
    unittest.main(verbosity=2)
