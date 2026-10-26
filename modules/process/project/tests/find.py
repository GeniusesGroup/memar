#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for finding a project by name, in `modules/process/project/services/find.py` and the verb `memar project find`.

    python modules/process/project/tests/find.py

The subject is the lookup that turns a word into a project folder, so that no
agent reasons about names or guesses a path. The rulings it holds are the
owner's of 2026-10-13, recorded in task 20261013T085819Z-27156-0: an exact
name or alias, in any case, is one answer; otherwise the word is compared by
similarity on Unicode-normalised text against the whole name and each alias, a
prefix counting as near, only so that the name need not be exact; one near
project is one answer, several are returned as candidates and never picked;
with none, a bounded search (seconds, never minutes) for a repository of that
name beside the Memar checkout and beside the folders already registered runs
before an error, and what it finds is recorded. Named for the file that holds it
per [Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes outside its scratch folder, and the Memar root is patched
onto a folder inside it, so "beside the Memar checkout" is the scratch folder
and no real sibling is searched.

What is pinned, and what each pin is for:

  Table           One table of (word, expected kind, expected project): exact,
                  case, typo, a mistyped non-Latin name, an alias in another
                  language, prefix, two near, none.
  Candidates      Several near projects are all returned, in the order
                  registered, and the function for other verbs refuses with
                  every one named, never picking.
  BoundedSearch   A repository beside the Memar checkout, or beside a registered
                  project, is found and recorded; a folder with no .git is not a
                  repository; a name not there is an error naming what was
                  tried; an exhausted budget stops the search.
  MissingFile     No projects.log reads as empty and the lookup still answers.
  Flags           `--project NAME` is a registry name, `--project-path PATH` a
                  folder; neither stands in for the other, both together are
                  refused, and a name that looks like a path says which flag.
  Verb            `find` prints the folder alone for one answer and exits
                  non-zero, printing the candidates, otherwise.
"""
from __future__ import annotations
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
import modules.process.project.services.find as project_find
import modules.process.project.services.registry as registry

class Fixture(unittest.TestCase):

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.base = Path(self.scratch.name)
        self.memar = self.folder('memar')
        patched = unittest.mock.patch.object(memar_fs, 'memar_root', return_value=self.memar)
        patched.start()
        self.addCleanup(patched.stop)

    def folder(self, name: str, *, parent: Path | None=None, repository: bool=False) -> Path:
        path = (parent or self.base) / name
        path.mkdir(parents=True, exist_ok=True)
        if repository:
            (path / '.git').mkdir(exist_ok=True)
        return path

    def printed(self, call, *args) -> tuple[str, str]:
        out, err = (io.StringIO(), io.StringIO())
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                call(*args)
            except SystemExit as stopped:
                self.stopped = stopped.code
                err.write(str(stopped.code))
            else:
                self.stopped = 0
        return (out.getvalue(), err.getvalue())

class Registered(Fixture):

    def setUp(self) -> None:
        super().setUp()
        self.khayyam = self.folder('khayyam')
        self.organization = self.folder('organization')
        self.chapar_core = self.folder('chapar-core')
        self.chapar_cli = self.folder('chapar-cli')
        registry.add_project('khayyam', self.khayyam, ['خیام'])
        registry.add_project('organization', self.organization, ['org', 'سازمان'])
        registry.add_project('chapar-core', self.chapar_core)
        registry.add_project('chapar-cli', self.chapar_cli)

    def path_of(self, name: str) -> Path:
        return {'khayyam': self.khayyam, 'organization': self.organization, 'memar': self.memar}[name].resolve()

class Table(Registered):
    CASES = (('exact', 'khayyam', 'exact', 'khayyam'), ('exact alias', 'org', 'exact', 'organization'), ('case', 'KhAyYaM', 'exact', 'khayyam'), ('case of alias', 'ORG', 'exact', 'organization'), ('typo, a letter changed', 'khayyem', 'near', 'khayyam'), ('typo, a letter missing', 'khayam', 'near', 'khayyam'), ('typo, two letters swapped', 'organizatoin', 'near', 'organization'), ('mistyped non-Latin name', 'خیم', 'near', 'khayyam'), ('alias in another language, exact', 'سازمان', 'exact', 'organization'), ('alias in another language, mistyped', 'سازمن', 'near', 'organization'), ('prefix of a name', 'organ', 'near', 'organization'), ('prefix of a name, one letter off the rest', 'khay', 'near', 'khayyam'), ('composed and decomposed forms are one text', 'khayyám', 'near', 'khayyam'), ('two near projects', 'chapar', 'candidates', None), ('nothing like it', 'zzzzqq', 'none', None))

    def test_each_case(self) -> None:
        for label, word, kind, project in self.CASES:
            with self.subTest(label):
                with unittest.mock.patch.object(project_find, 'search_locally', return_value=None):
                    found = project_find.lookup(word)
                self.assertEqual(found.kind, kind)
                if project is not None:
                    self.assertEqual([Path(entry.path) for entry in found.entries], [self.path_of(project)])

    def test_memar_itself_is_found(self) -> None:
        found = project_find.lookup('memar')
        self.assertEqual((found.kind, [Path(entry.path) for entry in found.entries]), ('exact', [self.memar.resolve()]))

    def test_an_exact_name_wins_over_a_longer_name_it_is_a_prefix_of(self) -> None:
        found = project_find.lookup('chapar-core')
        self.assertEqual((found.kind, len(found.entries)), ('exact', 1))

    def test_the_word_is_not_trimmed_into_another_name(self) -> None:
        self.assertEqual(project_find.lookup('  khayyam ').kind, 'exact')

class Candidates(Registered):

    def test_all_near_projects_are_returned_in_registered_order(self) -> None:
        found = project_find.lookup('chapar')
        self.assertEqual([entry.names[0] for entry in found.entries], ['chapar-core', 'chapar-cli'])

    def test_the_function_for_other_verbs_never_picks_one(self) -> None:
        with self.assertRaises(SystemExit) as raised:
            project_find.resolve_project('chapar')
        message = str(raised.exception.code)
        self.assertIn('chapar-core', message)
        self.assertIn('chapar-cli', message)

    def test_the_function_for_other_verbs_returns_the_path_of_one_answer(self) -> None:
        self.assertEqual(project_find.resolve_project('khayyem'), self.khayyam.resolve())

    def test_an_alias_of_a_project_and_its_name_near_the_word_are_one_candidate(self) -> None:
        found = project_find.lookup('organi')
        self.assertEqual(len(found.entries), 1)

class BoundedSearch(Fixture):

    def test_a_repository_beside_the_memar_checkout_is_found_and_recorded(self) -> None:
        wanted = self.folder('Newproj', repository=True)
        found = project_find.lookup('newproj')
        self.assertEqual((found.kind, [Path(entry.path) for entry in found.entries]), ('found', [wanted.resolve()]))
        self.assertEqual([Path(entry.path) for entry in registry.read_entries() if entry.names[0] == 'Newproj'], [wanted.resolve()])
        self.assertEqual(project_find.lookup('newproj').kind, 'exact')

    def test_a_repository_beside_a_registered_project_is_found(self) -> None:
        elsewhere = self.folder('elsewhere')
        registered = self.folder('known', parent=elsewhere, repository=True)
        registry.add_project('known', registered)
        wanted = self.folder('sibling-repo', parent=elsewhere, repository=True)
        found = project_find.lookup('sibling-repo')
        self.assertEqual((found.kind, [Path(entry.path) for entry in found.entries]), ('found', [wanted.resolve()]))

    def test_a_git_file_marks_a_repository_as_a_worktree_does(self) -> None:
        wanted = self.folder('worktree')
        (wanted / '.git').write_text('gitdir: elsewhere\n', encoding='utf-8')
        self.assertEqual(project_find.lookup('worktree').kind, 'found')

    def test_a_folder_with_no_git_is_not_a_repository(self) -> None:
        self.folder('plain')
        self.assertEqual(project_find.lookup('plain').kind, 'none')
        self.assertEqual([entry.names[0] for entry in registry.read_entries()], ['memar'])

    def test_a_name_not_there_is_none_and_records_nothing(self) -> None:
        self.folder('other', repository=True)
        found = project_find.lookup('missing-project')
        self.assertEqual((found.kind, found.entries), ('none', []))
        self.assertEqual([entry.names[0] for entry in registry.read_entries()], ['memar'])

    def test_an_exhausted_budget_stops_the_search(self) -> None:
        self.folder('late', repository=True)
        self.assertEqual(project_find.lookup('late', budget=-1.0).kind, 'none')

    def test_the_default_budget_is_seconds_not_minutes(self) -> None:
        self.assertLessEqual(project_find.SEARCH_SECONDS, 5)
        self.assertGreater(project_find.SEARCH_SECONDS, 0)

    def test_a_search_only_lists_direct_children(self) -> None:
        nested = self.folder('deep', parent=self.folder('nest'), repository=True)
        self.assertTrue(nested.is_dir())
        self.assertEqual(project_find.lookup('deep').kind, 'none')

    def test_a_found_name_another_project_has_is_not_recorded_over_it(self) -> None:
        registry.add_project('clash', self.folder('one'), ['twin'])
        self.folder('TWIN', repository=True)
        found = project_find.lookup('twin')
        self.assertEqual((found.kind, len(found.entries)), ('exact', 1))
        self.assertEqual(len(registry.read_entries()), 2)

class MissingFile(Fixture):

    def test_lookup_with_no_log_answers_and_does_not_fail(self) -> None:
        self.assertFalse(memar_fs.projects_log().exists())
        self.assertEqual(project_find.lookup('anything').kind, 'none')

    def test_lookup_with_no_log_still_finds_memar(self) -> None:
        self.assertEqual(project_find.lookup('memar').kind, 'exact')

    def test_an_unreadable_log_reads_as_empty(self) -> None:
        memar_fs.scratch_root()
        memar_fs.projects_log().mkdir()
        self.assertEqual(project_find.lookup('anything').kind, 'none')

class Verb(Registered):

    def test_one_answer_prints_the_folder_alone(self) -> None:
        out, _ = self.printed(project_find.run, argparse.Namespace(word='khayyem'))
        self.assertEqual(out.strip(), str(self.khayyam.resolve()))
        self.assertEqual(self.stopped, 0)

    def test_candidates_exit_non_zero_and_are_all_printed(self) -> None:
        out, err = self.printed(project_find.run, argparse.Namespace(word='chapar'))
        self.assertNotEqual(self.stopped, 0)
        self.assertEqual(out, '')
        self.assertIn('chapar-core', err)
        self.assertIn('chapar-cli', err)

    def test_none_exits_non_zero_and_says_what_was_tried(self) -> None:
        _, err = self.printed(project_find.run, argparse.Namespace(word='zzzzqq'))
        self.assertNotEqual(self.stopped, 0)
        self.assertIn('zzzzqq', err)
        self.assertIn('project add', err)

class Flags(Registered):
    """One flag per kind: `--project NAME` is a name, `--project-path PATH` a folder, neither is taken for the other."""

    def parse(self, *argv: str) -> argparse.Namespace:
        parser = argparse.ArgumentParser(prog='verb')
        project_find.add_project_flags(parser, 'the project to act on')
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            try:
                return parser.parse_args(list(argv))
            except SystemExit:
                self.error = err.getvalue()
                raise

    def test_a_name_is_resolved_through_the_registry(self) -> None:
        self.assertEqual(project_find.project_from_args(self.parse('--project', 'khayyem')), self.khayyam.resolve())

    def test_a_path_is_taken_as_it_is_and_needs_no_registration(self) -> None:
        other = self.folder('unregistered')
        self.assertEqual(project_find.project_from_args(self.parse('--project-path', str(other))), other.resolve())

    def test_neither_flag_is_no_project(self) -> None:
        self.assertIsNone(project_find.project_from_args(self.parse()))

    def test_both_flags_are_refused_by_the_parser(self) -> None:
        with self.assertRaises(SystemExit):
            self.parse('--project', 'khayyam', '--project-path', str(self.khayyam))
        self.assertIn('not allowed with', self.error)

    def test_a_name_that_looks_like_a_path_is_an_error_naming_the_other_flag(self) -> None:
        for value in (str(self.khayyam), './khayyam', 'a/b', 'a' + chr(92) + 'b', '~/x', '..', 'C:khayyam'):
            with self.subTest(value=value):
                _, err = self.printed(project_find.project_from_args, self.parse('--project', value))
                self.assertNotEqual(self.stopped, 0)
                self.assertIn('--project-path', err)

    def test_a_path_that_is_not_a_folder_is_an_error_and_a_bare_word_points_to_the_name_flag(self) -> None:
        _, err = self.printed(project_find.project_from_args, self.parse('--project-path', str(self.base / 'nothing')))
        self.assertNotEqual(self.stopped, 0)
        self.assertIn('not a folder', err)
        _, err = self.printed(project_find.project_from_args, self.parse('--project-path', 'khayyam-no-such-folder'))
        self.assertIn('--project NAME', err)

    def test_an_empty_value_is_refused_for_either_flag(self) -> None:
        for flag in ('--project', '--project-path'):
            with self.subTest(flag=flag):
                _, err = self.printed(project_find.project_from_args, self.parse(flag, ' '))
                self.assertNotEqual(self.stopped, 0)
                self.assertIn(flag, err)

    def test_the_old_single_argument_function_is_gone(self) -> None:
        self.assertFalse(hasattr(project_find, 'project_argument'))

    def test_help_says_which_flag_takes_which(self) -> None:
        parser = argparse.ArgumentParser(prog='verb')
        project_find.add_project_flags(parser, 'the project to act on')
        text = parser.format_help()
        self.assertIn('--project NAME', text)
        self.assertIn('--project-path PATH', text)

class Similarity(unittest.TestCase):

    def test_pairs(self) -> None:
        for word, name, expected in (('khayyam', 'khayyam', True), ('kayyam', 'khayyam', True), ('kh', 'khayyam', True), ('k', 'khayyam', False), ('org', 'organization', True), ('ogr', 'org', True), ('xyz', 'org', False), ('memar', 'memory', False), ('خیم', 'خیام', True), ('', 'khayyam', False)):
            with self.subTest(word=word, name=name):
                self.assertEqual(project_find.is_near(word, name), expected)
if __name__ == '__main__':
    unittest.main()
