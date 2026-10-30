#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for what stands at a task folder's top, and where the rest goes, in `modules-plugable/management/task/services/layout.py`.

    python modules-plugable/management/task/tests/layout.py

The subject is the layout every task service reads,
named for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes anything: names are read and compared.

What is pinned, and what each pin is for:

  TopHoldsOnly   The top holds plan.md and report.md, and the claim Memar
                 writes there while an agent holds the task (with its
                 takeover), and nothing else; the names are the ones the
                 services that write those files declare.
  OwnLayout      The task keeps its own small layout (owner, 2026-10-20,
                 C4): one folder per kind, tests/ and temp/, the last named
                 by `modules-plugable/computer/memory/filesystem/services/fs_memar.py`; it asks no module profile for it.
  KindsGoToRoles Each kind's folder is one of the task's folders; a note (.md)
                 goes in docs/ and a script (.py, .mjs, .js, .ps1, .sh) in
                 services/ (owner, 2026-10-14); a file of no kind named here,
                 and a folder, have no kind, so nothing guesses where they go.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
from importlib import import_module
from machine.plugable_import import load as plugable_load
_m_fs_memar = plugable_load('computer.memory.filesystem.services.fs_memar')
memar_fs = _m_fs_memar
import sys
import unittest
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = next(p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()) / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
task_layout = import_module('modules-plugable.management.task.services.layout')
task_temp = import_module('modules-plugable.management.task.services.temp')
_m_layout = import_module('modules-plugable.management.task.services.layout')
FOLDERS = _m_layout.FOLDERS
_m_claim = import_module('modules-plugable.management.task.primitive.claim')
Claim = _m_claim.Claim
_m_plan_file = import_module('modules-plugable.management.task.services.plan_file')
PLAN_NAME = _m_plan_file.PLAN_NAME
_m_report_file = import_module('modules-plugable.management.task.services.report_file')
REPORT_NAME = _m_report_file.REPORT_NAME

class TopHoldsOnly(unittest.TestCase):

    def test_the_top_holds_the_plan_the_report_and_the_claim(self) -> None:
        self.assertEqual(task_layout.TOP_NAMES, (PLAN_NAME, REPORT_NAME, Claim.NAME, Claim.TAKEOVER_NAME))
        self.assertEqual((PLAN_NAME, REPORT_NAME, Claim.NAME), ('plan.md', 'report.md', 'claim'))

    def test_a_folder_of_the_layout_belongs_at_the_top_and_a_stray_does_not(self) -> None:
        for name in (*task_layout.TOP_NAMES, *FOLDERS):
            with self.subTest(name=name):
                self.assertTrue(task_layout.belongs_at_top(name))
        for name in ('entry.md', 'make_reviews.py', 'msg1.txt', 'scratch', 'Plan.md'):
            with self.subTest(name=name):
                self.assertFalse(task_layout.belongs_at_top(name))

class OwnLayout(unittest.TestCase):

    def test_the_layout_is_the_kinds_folders_then_tests_and_temp(self) -> None:
        self.assertEqual(FOLDERS, ('docs', 'services', 'tests', 'temp'))

    def test_it_reads_no_module_profile(self) -> None:
        source = Path(task_layout.__file__).read_text(encoding='utf-8')
        self.assertNotIn('role_folders', source)
        self.assertNotIn('module-skeleton', source)
        self.assertNotIn('MODULE_SKELETON', source)

class TempIsNotKept(unittest.TestCase):
    """The task's `temp` role folder (owner, 2026-10-15): what is made there is not part of the task's record."""

    def test_temp_is_a_role_folder_and_may_stand_at_the_top(self) -> None:
        self.assertEqual(task_temp.TEMP_FOLDER, 'temp')
        self.assertIs(task_temp.TEMP_FOLDER, memar_fs.TEMP_FOLDER)
        self.assertIn(task_temp.TEMP_FOLDER, FOLDERS)
        self.assertTrue(task_layout.belongs_at_top('temp'))

    def test_the_sentence_that_tells_an_agent_names_the_folder_and_what_goes_in_it(self) -> None:
        said = task_temp.TEMP_SENTENCE
        self.assertEqual(said.count('.'), 1, said)
        for words in ('temp/', 'draft changelog record', 'script', 'never archived'):
            self.assertIn(words, said)

    def test_no_kind_files_into_temp(self) -> None:
        self.assertNotIn(task_temp.TEMP_FOLDER, [kind.folder for kind in task_layout.KINDS])

class KindsGoToRoles(unittest.TestCase):

    def test_each_kinds_folder_is_a_folder_of_the_layout(self) -> None:
        for kind in task_layout.KINDS:
            with self.subTest(kind=kind.name):
                self.assertIn(kind.folder, FOLDERS)

    def test_a_note_goes_in_docs_and_a_script_in_services(self) -> None:
        for name, folder in (('entry.md', 'docs'), ('NOTES.MD', 'docs'), ('make_reviews.py', 'services'), ('probe.mjs', 'services'), ('run.js', 'services'), ('go.ps1', 'services'), ('go.sh', 'services')):
            with self.subTest(name=name):
                kind = task_layout.kind_of(name)
                self.assertIsNotNone(kind)
                self.assertEqual(kind.folder, folder)

    def test_a_file_of_no_kind_named_here_has_none(self) -> None:
        for name in ('msg1.txt', 'run.log', 'c1.plan.json', 'a.diff', 'claim.pyc', 'README'):
            with self.subTest(name=name):
                self.assertIsNone(task_layout.kind_of(name))

    def test_the_kinds_read_as_one_line_for_the_help(self) -> None:
        self.assertEqual(task_layout.kinds_listing(), 'a note (.md) in docs/, a script (.py, .mjs, .js, .ps1, .sh) in services/')
if __name__ == '__main__':
    unittest.main(verbosity=2)
