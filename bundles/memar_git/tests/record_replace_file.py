#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the folders `_host_git_cli.py record` empties, in `modules-plugable/computer/git/services/_record.py`.

    python modules-plugable/computer/git/tests/record_replace_file.py

What is pinned: the folders to replace may be given in a file as well as with
`--replace`, because a command line of many thousand folders is refused by the
host (Windows stops a command at 32,767 characters), and the archive of a
task with thousands of descendants must still be one commit.
"""
from __future__ import annotations
import sys
import tempfile
import unittest
from importlib import import_module
from pathlib import Path
BUDGET_SECONDS = 20
ROOT = next(p for p in Path(__file__).resolve().parents if p.name == 'modules-plugable').parent
sys.path.insert(0, str(ROOT / 'bundles' / 'memar' / 'services'))
sys.path.insert(1, str(ROOT))
sys.dont_write_bytecode = True
record = import_module('modules-plugable.computer.git.services._record')

class FoldersToReplace(unittest.TestCase):

    def test_the_folders_of_the_flag_and_of_the_file_are_both_replaced_in_order(self) -> None:
        with tempfile.TemporaryDirectory() as scratch:
            listing = Path(scratch) / 'replace.txt'
            listing.write_bytes('.agents/tasks/b\n.agents/tasks/c\n'.encode('utf-8'))
            self.assertEqual(record.folders_to_replace(['.agents/tasks/a'], listing), ['.agents/tasks/a', '.agents/tasks/b', '.agents/tasks/c'])

    def test_a_blank_line_and_a_trailing_slash_are_dropped(self) -> None:
        with tempfile.TemporaryDirectory() as scratch:
            listing = Path(scratch) / 'replace.txt'
            listing.write_bytes('\n.agents/tasks/b/\n\n'.encode('utf-8'))
            self.assertEqual(record.folders_to_replace([], listing), ['.agents/tasks/b'])

    def test_no_file_means_the_flags_alone(self) -> None:
        self.assertEqual(record.folders_to_replace(['x'], None), ['x'])

if __name__ == '__main__':
    unittest.main(verbosity=2)
