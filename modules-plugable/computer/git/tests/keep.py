#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for which files of a task folder are kept, in `modules-plugable/computer/git/services/keep.py`.

    python modules-plugable/management/task/tests/keep.py

The subject is the owner's ruling of 2026-10-15 on what a task's records
leave out, named for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes outside its scratch folder.

What is pinned, and what each pin is for:

  KeepsTheWholeFolder   Every file of the folder is kept, whatever role folder
                        holds it and whether or not the report links to it,
                        except the leave-outs below. A file the report only
                        mentions is kept: the record is the folder.
  LeavesOut             The claim, a Python cache, any path with a `.git` part,
                        a link, the task's own `temp` folder, a binary file
                        (a NUL in its first bytes), and a file over 256 KB that
                        is not a document, are left out; each with its reason,
                        its size, and for a folder how many files it held. A
                        document over the limit is kept; `temp` below the top
                        of the folder is an ordinary folder.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
from importlib import import_module
_m_fs_test_scratch = import_module('modules-plugable.computer.memory.filesystem.services.fs_test_scratch')
suite_scratch = _m_fs_test_scratch.suite_scratch
import sys
import tempfile
import unittest
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = next(p for p in TESTS.parents if p.name == 'modules-plugable').parent / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
task_keep = import_module('modules-plugable.computer.git.services.keep')
Reason = import_module('modules-plugable.computer.git.services.keep').Reason

class Fixture(unittest.TestCase):

    def setUp(self) -> None:
        scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(scratch.cleanup)
        self.folder = Path(scratch.name) / '20261015-T000000Z-1'
        self.folder.mkdir()

    def put(self, relative: str, data: bytes=b'text\n') -> Path:
        path = self.folder / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def left(self) -> dict[str, task_keep.Left]:
        return {each.path: each for each in task_keep.select(self.folder).left}

class KeepsTheWholeFolder(Fixture):

    def test_every_file_is_kept_whether_or_not_a_report_links_to_it(self) -> None:
        for name in ('plan.md', 'report.md', 'docs/entry.md', 'docs/scratch.txt', 'services/fix.py', 'tests/t.py', 'x/y/z.json'):
            self.put(name)
        self.assertEqual(task_keep.select(self.folder).kept, ('docs/entry.md', 'docs/scratch.txt', 'plan.md', 'report.md', 'services/fix.py', 'tests/t.py', 'x/y/z.json'))

    def test_nothing_left_out_means_nothing_listed(self) -> None:
        self.put('plan.md')
        self.assertEqual(task_keep.select(self.folder).left, ())

    def test_a_folder_that_holds_nothing_has_no_files(self) -> None:
        selection = task_keep.select(self.folder)
        self.assertEqual((selection.kept, selection.left), ((), ()))

class LeavesOut(Fixture):

    def test_the_claim_and_its_takeover_marker(self) -> None:
        self.put('plan.md')
        self.put('claim')
        self.put('claim.takeover')
        self.assertEqual(sorted(self.left()), ['claim', 'claim.takeover'])
        self.assertIs(self.left()['claim'].reason, Reason.CLAIM)
        self.assertEqual(task_keep.select(self.folder).kept, ('plan.md',))

    def test_a_claim_below_the_top_is_an_ordinary_file(self) -> None:
        self.put('docs/claim')
        self.assertEqual(task_keep.select(self.folder).kept, ('docs/claim',))

    def test_a_python_cache_folder_is_left_out_whole_and_counted(self) -> None:
        self.put('services/__pycache__/a.pyc', b'\x00\x00')
        self.put('services/__pycache__/b.pyc', b'\x00\x00\x00')
        self.put('services/fix.py')
        left = self.left()
        self.assertEqual(list(left), ['services/__pycache__'])
        self.assertIs(left['services/__pycache__'].reason, Reason.CACHE)
        self.assertEqual((left['services/__pycache__'].files, left['services/__pycache__'].size), (2, 5))
        self.assertEqual(task_keep.select(self.folder).kept, ('services/fix.py',))

    def test_any_path_with_a_git_part_is_left_out(self) -> None:
        self.put('lab/.git/config')
        self.put('lab/.git/objects/ab/cd')
        self.put('lab/readme.md')
        self.assertEqual(list(self.left()), ['lab/.git'])
        self.assertIs(self.left()['lab/.git'].reason, Reason.GIT)
        self.assertEqual(task_keep.select(self.folder).kept, ('lab/readme.md',))

    def test_the_tasks_own_temp_folder_is_left_out_whole(self) -> None:
        self.put('temp/draft.md')
        self.put('temp/out/run.log')
        left = self.left()
        self.assertEqual(list(left), ['temp'])
        self.assertIs(left['temp'].reason, Reason.TEMP)
        self.assertEqual(left['temp'].files, 2)
        self.assertEqual(task_keep.select(self.folder).kept, ())

    def test_a_temp_folder_below_the_top_is_an_ordinary_folder(self) -> None:
        self.put('docs/temp/note.md')
        self.assertEqual(task_keep.select(self.folder).kept, ('docs/temp/note.md',))

    def test_a_binary_file_is_left_out_with_its_size(self) -> None:
        self.put('docs/a.tar', b'abc\x00def' * 10)
        left = self.left()
        self.assertEqual(list(left), ['docs/a.tar'])
        self.assertIs(left['docs/a.tar'].reason, Reason.BINARY)
        self.assertEqual(left['docs/a.tar'].size, 70)

    def test_a_nul_after_the_probe_is_not_binary(self) -> None:
        self.put('docs/late.txt', b'x' * task_keep.BINARY_PROBE_BYTES + b'\x00')
        self.assertEqual(task_keep.select(self.folder).kept, ('docs/late.txt',))

    def test_a_document_with_a_nul_is_binary_too(self) -> None:
        self.put('docs/odd.md', b'a\x00b')
        self.assertIs(self.left()['docs/odd.md'].reason, Reason.BINARY)

    def test_a_file_over_256_kb_that_is_not_a_document_is_left_out(self) -> None:
        self.assertEqual(task_keep.KEEP_LIMIT_BYTES, 256 * 1024)
        self.put('services/big.py', b'x = 1\n' * 50000)
        self.put('services/edge.py', b'x' * task_keep.KEEP_LIMIT_BYTES)
        left = self.left()
        self.assertEqual(list(left), ['services/big.py'])
        self.assertIs(left['services/big.py'].reason, Reason.LARGE)
        self.assertEqual(left['services/big.py'].size, 300000)
        self.assertEqual(task_keep.select(self.folder).kept, ('services/edge.py',))

    def test_a_document_over_the_limit_is_kept(self) -> None:
        self.put('docs/long.md', b'line\n' * 100000)
        self.put('docs/LONG-TWO.MD', b'line\n' * 100000)
        self.assertEqual(task_keep.select(self.folder).kept, ('docs/LONG-TWO.MD', 'docs/long.md'))

    def test_a_link_is_left_out(self) -> None:
        target = self.put('docs/real.md')
        link = self.folder / 'docs' / 'link.md'
        try:
            link.symlink_to(target)
        except (OSError, NotImplementedError):
            self.skipTest('this machine does not let the test make a link')
        self.assertIs(self.left()['docs/link.md'].reason, Reason.LINK)
        self.assertEqual(task_keep.select(self.folder).kept, ('docs/real.md',))

    def test_a_name_a_manifest_cannot_carry_is_left_out(self) -> None:
        self.put('docs/ok.md')
        try:
            self.put('docs/tab\there.md')
        except OSError:
            self.skipTest('this machine does not allow a tab in a file name')
        self.assertIs(self.left()['docs/tab\there.md'].reason, Reason.NAME)

    def test_each_reason_reads_as_a_sentence(self) -> None:
        for reason in Reason:
            with self.subTest(reason=reason):
                self.assertTrue(reason.sentence)
                self.assertNotIn('\n', reason.sentence)
if __name__ == '__main__':
    unittest.main(verbosity=2)
