#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
TIER = 'system'
BUDGET_SECONDS = 120
import io
import re
import sys
import tokenize
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _scratch import BUNDLE, ScratchRepository, bundle

VERBS = ('commit', 'uncommit', 'reindex', 'remove', 'rename', 'restore', 'stash', 'undelete')
TOP = BUNDLE.parent.parent

class TheRouterFindsTheVerbs(ScratchRepository):

    def listing(self) -> str:
        done = self.router('commands')
        self.assertEqual(done.returncode, 0, done.stderr)
        return done.stdout

    def test_the_commands_listing_has_every_verb_of_the_bundle(self) -> None:
        listed = self.listing()
        for verb in VERBS:
            with self.subTest(verb=verb):
                self.assertRegex(listed, f'(?m)^memar git {verb}\\b')

    def test_each_listed_verb_takes_the_repository(self) -> None:
        listed = self.listing()
        for verb in VERBS:
            with self.subTest(verb=verb):
                line = next((each for each in listed.splitlines() if re.match(f'memar git {verb}\\b', each)), '')
                self.assertIn('--repository', line)

    def test_the_listing_names_a_line_of_purpose_under_each_verb(self) -> None:
        lines = self.listing().splitlines()
        for verb in VERBS:
            with self.subTest(verb=verb):
                at = next((number for number, each in enumerate(lines) if re.match(f'memar git {verb}\\b', each)), None)
                self.assertIsNotNone(at)
                self.assertTrue(lines[at + 1].strip())
                self.assertFalse(lines[at + 1].startswith('memar '))

    def test_each_verb_says_its_own_constraint_in_its_help(self) -> None:
        for verb in VERBS:
            with self.subTest(verb=verb):
                done = self.router('git', verb, '--help')
                self.assertEqual(done.returncode, 0, done.stderr)
                self.assertGreater(len(done.stdout.split()), 25)
                self.assertIn('--repository', done.stdout)

    def test_the_verbs_are_files_of_the_bundle_that_describe_themselves(self) -> None:
        for verb in VERBS:
            with self.subTest(verb=verb):
                module = bundle(f'services.{verb}')
                self.assertTrue(callable(getattr(module, 'describe', None)))

    def test_the_old_script_of_the_module_is_not_where_the_verbs_come_from(self) -> None:
        for verb in VERBS:
            with self.subTest(verb=verb):
                self.assertEqual(Path(bundle(f'services.{verb}').__file__).resolve().parent, (BUNDLE / 'services').resolve())

class TheBundleKeepsTheRules(unittest.TestCase):

    def sources(self) -> list[Path]:
        return [file for file in sorted(BUNDLE.rglob('*.py')) if 'tests' not in file.parts and '__pycache__' not in file.parts]

    def test_the_bundle_has_the_files_the_abstraction_names(self) -> None:
        self.assertTrue(self.sources())
        for verb in VERBS:
            with self.subTest(verb=verb):
                self.assertTrue((BUNDLE / 'services' / f'{verb}.py').is_file())
        self.assertTrue((BUNDLE / 'memar_git.py').is_file())
        self.assertTrue((BUNDLE / 'errors' / 'errors.py').is_file())

    def test_no_code_carries_a_comment_or_a_docstring(self) -> None:
        for file in self.sources():
            with self.subTest(file=file.name):
                text = file.read_text(encoding='utf-8')
                comments = [token.string for token in tokenize.generate_tokens(io.StringIO(text).readline) if token.type == tokenize.COMMENT and token.start[0] > 2 and not token.string.startswith('#!')]
                self.assertEqual(comments, [])
                import ast
                tree = ast.parse(text)
                for node in ast.walk(tree):
                    if isinstance(node, (ast.Module, ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
                        self.assertIsNone(ast.get_docstring(node))

    def test_no_code_stops_the_process_where_an_error_of_the_errors_folder_is_meant(self) -> None:
        for file in self.sources():
            if file.name in ('memar_git.py',) or file.parent.name == 'errors':
                continue
            with self.subTest(file=file.name):
                self.assertNotIn('sys.exit(', file.read_text(encoding='utf-8'))

    def test_the_bundle_does_not_import_the_module_it_replaces_except_to_forward_the_records_verbs(self) -> None:
        for file in self.sources():
            if file.name == '_records.py':
                continue
            with self.subTest(file=file.name):
                text = file.read_text(encoding='utf-8')
                self.assertNotIn('computer.git', text)
                self.assertNotIn('computer/git', text)

    def test_every_error_of_the_abstraction_is_a_class_of_the_errors_folder(self) -> None:
        declared = re.findall(r'(?m)^tp Error_Memar_Git_(\w+) ab', (BUNDLE / 'errors' / 'errors.kh').read_text(encoding='utf-8'))
        python = bundle('errors.errors')
        self.assertGreaterEqual(len(declared), 24)
        for name in declared:
            with self.subTest(error=name):
                self.assertTrue(issubclass(getattr(python, name), Exception))

    def test_a_refusal_is_an_error_and_a_git_failure_a_lock_and_an_unreachable_server_are_not_refusals(self) -> None:
        python = bundle('errors.errors')
        for name in ('NotNamed', 'PathAbsent', 'TaskUnknown', 'NotConfirmed'):
            self.assertTrue(issubclass(getattr(python, name), python.Refusal))
        for name in ('GitFailed', 'Locked', 'ServerUnreachable'):
            self.assertFalse(issubclass(getattr(python, name), python.Refusal))
            self.assertTrue(issubclass(getattr(python, name), python.Error))

if __name__ == '__main__':
    unittest.main()
