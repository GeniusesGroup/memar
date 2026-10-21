#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the projects registry, in `modules/process/project/services/registry.py` and the verbs `project add`, `list`, `remove`.

    python modules/process/project/tests/registry.py

The subject is Memar's record of the projects it is told about: temp/projects.log
at the root of Memar's temp, one project a line, naming its folder and an array
of names, so that a verb is given a name and never a guessed folder. The rulings
it holds are the owner's of 2026-10-13, recorded in session
20261013T085819Z-27156-0: aliases are an array per project and may be in several
languages; Memar itself is an entry; names are unique without case; a missing
temp folder is made, never a block; an unreadable or missing file reads as
empty. Lookup by similarity is `project_find`'s and tested in its own file.
Named for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes outside its scratch folder: the Memar root the services
resolve is patched onto one made under the folder `modules-plugable/computer/filesystem/services/fs_test_scratch.py`
names.

What is pinned, and what each pin is for:

  Location        The file is temp/projects.log under the Memar root, its path
                  owned by `modules-plugable/computer/filesystem/services/fs_memar.py`; asking for it creates only the
                  missing temp folder.
  Reading         A missing file, a folder in its place, and lines that are not
                  entries read as empty or are skipped, never as an error.
  Adding          A project is stored as a line with its path and names array;
                  several languages survive; a second add for the same folder
                  merges names; a name or alias already another project's, in
                  any case, is refused; a path that is no folder is refused.
  Removing        By name, by alias, in any case; an unknown word is refused.
  Atomic          An update replaces the file whole; a failed replace leaves the
                  old file and no temporary file beside it.
  MemarEntry      Memar's own checkout is an entry named memar, added once.
  Verbs           `add` (with repeated --alias), `list`, and `remove` print what
                  they did.
"""
from __future__ import annotations
from machine.plugable_import import load as plugable_load
_m_fs_test_scratch = plugable_load('computer.filesystem.services.fs_test_scratch')
suite_scratch = _m_fs_test_scratch.suite_scratch
_m_fs_memar = plugable_load('computer.filesystem.services.fs_memar')
memar_fs = _m_fs_memar
import argparse
import contextlib
import io
import json
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parents[3] / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
import modules.process.project.services.add as project_add
import modules.process.project.services.list as project_list
import modules.process.project.services.registry as registry
import modules.process.project.services.remove as project_remove

class Fixture(unittest.TestCase):

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.base = Path(self.scratch.name)
        self.memar = self.folder('memar')
        patched = unittest.mock.patch.object(memar_fs, 'memar_root', return_value=self.memar)
        patched.start()
        self.addCleanup(patched.stop)

    def folder(self, name: str) -> Path:
        path = self.base / name
        path.mkdir(parents=True, exist_ok=True)
        return path

    def log_lines(self) -> list[str]:
        return memar_fs.projects_log().read_text(encoding='utf-8').splitlines()

    def printed(self, call, *args) -> str:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            call(*args)
        return out.getvalue()

    def refused(self, call, *args, **kwargs) -> str:
        with self.assertRaises(SystemExit) as raised:
            call(*args, **kwargs)
        return str(raised.exception.code)

class Location(Fixture):

    def test_the_log_is_temp_projects_log_under_the_memar_root(self) -> None:
        self.assertEqual(memar_fs.projects_log(), self.memar / 'temp' / 'projects.log')

    def test_a_missing_temp_folder_is_made_not_a_block(self) -> None:
        self.assertFalse((self.memar / 'temp').exists())
        registry.add_project('alpha', self.folder('alpha'))
        self.assertTrue(memar_fs.projects_log().is_file())

    def test_the_log_is_not_inside_the_sessions_folder(self) -> None:
        self.assertEqual(memar_fs.projects_log().parent, memar_fs.scratch_root())

class Reading(Fixture):

    def test_a_missing_file_reads_as_empty(self) -> None:
        self.assertEqual(registry.read_entries(), [])

    def test_a_folder_in_the_files_place_reads_as_empty(self) -> None:
        memar_fs.projects_log().mkdir(parents=True)
        self.assertEqual(registry.read_entries(), [])

    def test_lines_that_are_not_entries_are_skipped(self) -> None:
        good = {'path': str(self.folder('alpha')), 'names': ['alpha']}
        text = '\n'.join(['not json', json.dumps(good), '[1,2]', json.dumps({'path': 3, 'names': []}), ''])
        memar_fs.scratch_root()
        memar_fs.projects_log().write_text(text, encoding='utf-8')
        self.assertEqual([entry.names for entry in registry.read_entries()], [('alpha',)])

class Adding(Fixture):

    def test_a_project_is_one_line_with_its_path_and_names_array(self) -> None:
        registry.add_project('khayyam', self.folder('khayyam'), ['Khayyam-lang'])
        lines = self.log_lines()
        self.assertEqual(len(lines), 1)
        record = json.loads(lines[0])
        self.assertEqual(record['names'], ['khayyam', 'Khayyam-lang'])
        self.assertEqual(Path(record['path']), (self.base / 'khayyam').resolve())

    def test_names_in_several_languages_survive_as_written(self) -> None:
        registry.add_project('khayyam', self.folder('khayyam'), ['خیام', '海亚姆'])
        self.assertEqual(registry.read_entries()[0].names, ('khayyam', 'خیام', '海亚姆'))
        self.assertIn('خیام', memar_fs.projects_log().read_text(encoding='utf-8'))

    def test_adding_the_same_folder_again_merges_names(self) -> None:
        folder = self.folder('organization')
        registry.add_project('organization', folder, ['org'])
        registry.add_project('organization', folder, ['سازمان', 'ORG'])
        entries = registry.read_entries()
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].names, ('organization', 'org', 'سازمان'))

    def test_a_name_another_project_has_is_refused_in_any_case(self) -> None:
        registry.add_project('alpha', self.folder('alpha'))
        message = self.refused(registry.add_project, 'ALPHA', self.folder('beta'))
        self.assertIn('alpha', message)
        self.assertEqual(len(registry.read_entries()), 1)

    def test_an_alias_another_project_has_is_refused(self) -> None:
        registry.add_project('alpha', self.folder('alpha'), ['first'])
        self.refused(registry.add_project, 'beta', self.folder('beta'), ['First'])
        self.assertEqual(len(registry.read_entries()), 1)

    def test_names_equal_after_unicode_normalisation_are_the_same_name(self) -> None:
        registry.add_project('alpha', self.folder('alpha'), ['café'])
        self.refused(registry.add_project, 'beta', self.folder('beta'), ['café'])

    def test_a_path_that_is_no_folder_is_refused(self) -> None:
        self.refused(registry.add_project, 'ghost', self.base / 'nowhere')
        self.assertEqual(registry.read_entries(), [])

    def test_a_blank_name_is_refused(self) -> None:
        self.refused(registry.add_project, '  ', self.folder('alpha'))

class Removing(Fixture):

    def setUp(self) -> None:
        super().setUp()
        registry.add_project('alpha', self.folder('alpha'), ['ألفا'])
        registry.add_project('beta', self.folder('beta'))

    def test_by_name_in_any_case(self) -> None:
        registry.remove_project('ALPHA')
        self.assertEqual([entry.names[0] for entry in registry.read_entries()], ['beta'])

    def test_by_alias(self) -> None:
        registry.remove_project('ألفا')
        self.assertEqual([entry.names[0] for entry in registry.read_entries()], ['beta'])

    def test_an_unknown_word_is_refused_and_nothing_changes(self) -> None:
        self.refused(registry.remove_project, 'gamma')
        self.assertEqual(len(registry.read_entries()), 2)

    def test_removing_never_touches_the_folder(self) -> None:
        registry.remove_project('beta')
        self.assertTrue((self.base / 'beta').is_dir())

class Atomic(Fixture):

    def test_a_failed_replace_leaves_the_old_file_and_no_temporary(self) -> None:
        registry.add_project('alpha', self.folder('alpha'))
        before = memar_fs.projects_log().read_bytes()
        with unittest.mock.patch('os.replace', side_effect=OSError('disk')):
            with self.assertRaises((OSError, SystemExit)):
                registry.add_project('beta', self.folder('beta'))
        self.assertEqual(memar_fs.projects_log().read_bytes(), before)
        self.assertEqual(sorted((path.name for path in memar_fs.scratch_root().iterdir())), ['projects.log'])

    def test_no_lock_or_temporary_file_is_left_after_an_update(self) -> None:
        registry.add_project('alpha', self.folder('alpha'))
        registry.add_project('beta', self.folder('beta'))
        self.assertEqual(sorted((path.name for path in memar_fs.scratch_root().iterdir())), ['projects.log'])

class MemarEntry(Fixture):

    def test_memars_own_checkout_is_an_entry_named_memar(self) -> None:
        registry.ensure_memar_entry()
        entries = registry.read_entries()
        self.assertEqual([(entry.names, Path(entry.path)) for entry in entries], [(('memar',), self.memar.resolve())])

    def test_it_is_added_once(self) -> None:
        registry.ensure_memar_entry()
        registry.ensure_memar_entry()
        self.assertEqual(len(registry.read_entries()), 1)

    def test_a_name_already_taken_by_another_project_is_not_overwritten(self) -> None:
        registry.add_project('memar', self.folder('other'))
        registry.ensure_memar_entry()
        self.assertEqual([Path(entry.path) for entry in registry.read_entries()], [(self.base / 'other').resolve()])

class Verbs(Fixture):

    def test_add_with_repeated_alias_then_list_then_remove(self) -> None:
        folder = self.folder('organization')
        args = argparse.Namespace(name='organization', path=str(folder), alias=['org', 'سازمان'])
        said = self.printed(project_add.run, args)
        self.assertIn('organization', said)
        listed = self.printed(project_list.run, argparse.Namespace())
        for expected in ('organization', 'org', 'سازمان', str(folder.resolve()), 'memar'):
            self.assertIn(expected, listed)
        removed = self.printed(project_remove.run, argparse.Namespace(word='org'))
        self.assertIn('organization', removed)
        self.assertNotIn('organization', self.printed(project_list.run, argparse.Namespace()))

    def test_list_of_nothing_registered_still_names_memar(self) -> None:
        listed = self.printed(project_list.run, argparse.Namespace())
        self.assertEqual(len(listed.strip().splitlines()), 1)
        self.assertIn('memar', listed)
if __name__ == '__main__':
    unittest.main()
