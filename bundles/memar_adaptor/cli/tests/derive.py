#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for `derive.py`: the command line of a service is made from its declaration and from nothing else.

    python bundles/memar_adaptor/cli/tests/derive.py

What is pinned:

  VerbIsDerived     The verb's words, its positional words, its flags, a list flag and a true-or-false flag come
                    from the function's signature; the function holds no verb and no flag.
  RunCallsFunction  The parsed values reach the function by their names and what it answers is printed.
  RealStatusVerb    The Status of a task is a verb of the task domain only because the task widget declares it.
"""
from __future__ import annotations

import argparse
import io
import sys
import unittest
from typing import Literal
import contextlib
from importlib import import_module
from pathlib import Path

TESTS = Path(__file__).resolve().parent
TOP = TESTS.parent.parent.parent.parent
for folder in (TOP, TESTS.parent, TOP / 'bundles' / 'memar', TOP / 'bundles' / 'memar' / 'services'):
    if str(folder) not in sys.path:
        sys.path.insert(0, str(folder))
sys.dont_write_bytecode = True
BUDGET_SECONDS = 20
declare = import_module('modules.process.service.primitive.declaration').declare
derive = import_module('bundles.memar_adaptor.cli.derive')


def greet(name, times=2, loud=False, tags: tuple[str, ...] | None = None, project=None):
    """A function that knows nothing of a command line."""
    return f'{name} {times} {loud} {tags} {project}'


def shaped(files: tuple[str, ...], maybe=None, /, *, kind: Literal['a', 'b'], limit: int = 5, links: bool = True, source: Path | None = None):
    return (files, maybe, kind, limit, links, source)


def file_paths(paths: tuple[Path, ...], /, *, extras: tuple[Path, ...] | None = None):
    return all(isinstance(p, Path) for p in (*paths, *(extras or ())))


def reserved(*, from_: str, as_: tuple[str, ...] | None = None, message_file: Path, message: str | None = None, verbose: bool = False):
    return (from_, as_, message_file, message, verbose)


def in_project(*, project):
    return project


def parser_of(declaration):
    top = argparse.ArgumentParser(prog='memar')
    verbs = top.add_subparsers(dest='verb')

    class Level:
        def add_parser(self, name, **kwargs):
            return verbs.add_parser(name, **kwargs)
    run = derive.describer(declaration)(Level())
    return top, run


class VerbIsDerived(unittest.TestCase):

    def test_words_flags_and_kinds_come_from_the_signature(self) -> None:
        top, _ = parser_of(declare(greet, name='say hello', summary='greet', takes=('name', 'times', 'loud', 'tags')))
        parsed = top.parse_args(['say-hello', 'Ada', '--times', '3', '--loud', '--tags', 'a,b', '--tags', 'c'])
        self.assertEqual((parsed.name, parsed.times, parsed.loud, parsed.tags), ('Ada', 3, True, ['a,b', 'c']))

    def test_a_declared_parameter_the_function_lacks_is_refused(self) -> None:
        with self.assertRaises(ValueError):
            declare(greet, name='x', summary='x', takes=('nobody',))


class ShapesFollowTheSignature(unittest.TestCase):

    def test_a_required_project_keeps_the_existing_two_flag_help_contract(self) -> None:
        top, _ = parser_of(declare(in_project, name='project', summary='s'))
        parsed = top.parse_args(['project'])
        self.assertIsNone(parsed.project)
        out = io.StringIO()
        with contextlib.redirect_stdout(out), self.assertRaises(SystemExit):
            top.parse_args(['project', '--help'])
        self.assertIn('required, one of the two', out.getvalue())

    def test_python_keyword_escape_and_existing_short_flags_are_adaptor_conventions(self) -> None:
        top, run = parser_of(declare(reserved, name='reserved', summary='s'))
        parsed = top.parse_args(['reserved', '--from', 'HEAD', '--as', 'a=b', '-F', 'm', '-m', 'note', '-v'])
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            run(parsed)
        self.assertEqual(out.getvalue().strip(), "('HEAD', ('a=b',), " + repr(Path('m')) + ", 'note', True)")

    def test_path_collections_keep_the_element_type_for_words_and_repeated_flags(self) -> None:
        top, run = parser_of(declare(file_paths, name='paths', summary='s'))
        parsed = top.parse_args(['paths', 'a', 'b', '--extras', 'c,d', '--extras', 'e'])
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            run(parsed)
        self.assertEqual(out.getvalue().strip(), 'True')

    def test_a_comma_in_a_repeated_path_is_part_of_the_path(self) -> None:
        top, _ = parser_of(declare(file_paths, name='paths', summary='s'))
        parsed = top.parse_args(['paths', 'a', '--extras', 'c,d'])
        found = import_module('modules.computer.software.services.project_find')
        extra = next(f for f in declare(file_paths, name='paths', summary='s').fields if f.name == 'extras')
        self.assertEqual(derive.value_of(parsed, extra, found), (Path('c,d'),))

    def test_positional_only_are_words_keyword_only_are_flags_and_a_true_default_is_negated(self) -> None:
        top, run = parser_of(declare(shaped, name='shape', summary='s'))
        parsed = top.parse_args(['shape', 'x', 'y', '--kind', 'a', '--no-links', '--limit', '2', '--source', 'p'])
        self.assertEqual((parsed.files, parsed.kind, parsed.limit, parsed.links, parsed.source), (['x', 'y'], 'a', 2, False, Path('p')))

    def test_a_needed_keyword_and_a_choice_are_enforced(self) -> None:
        top, _ = parser_of(declare(shaped, name='shape', summary='s'))
        for wrong in (['shape', 'x'], ['shape', 'x', '--kind', 'c']):
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                top.parse_args(wrong)


class RunCallsFunction(unittest.TestCase):

    def test_positional_only_values_reach_the_function_in_order(self) -> None:
        top, run = parser_of(declare(shaped, name='shape', summary='s'))
        parsed = top.parse_args(['shape', 'x', 'y', '--kind', 'a', '--no-links'])
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            run(parsed)
        self.assertEqual(out.getvalue().strip(), "(('x', 'y'), None, 'a', 5, False, None)")

    def test_values_reach_the_function_by_name_and_the_answer_is_printed(self) -> None:
        top, run = parser_of(declare(greet, name='say hello', summary='greet', takes=('name', 'times', 'loud', 'tags')))
        parsed = top.parse_args(['say-hello', 'Ada', '--tags', 'a, b', '--tags', 'c'])
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            run(parsed)
        self.assertEqual(out.getvalue().strip(), "Ada 2 False ('a', 'b', 'c') None")


class RealStatusVerb(unittest.TestCase):

    def test_the_task_widget_declares_the_status_verb_and_the_router_finds_it(self) -> None:
        router = import_module('bundles.memar_adaptor.cli.router')
        top, _ = router.assemble(router.services())
        out = io.StringIO()
        with contextlib.redirect_stdout(out), self.assertRaises(SystemExit):
            top.parse_args(['status_set', '--help'])
        text = out.getvalue()
        self.assertIn('THING', text)
        self.assertIn('--only-from', text)
        self.assertIn('--project-path', text)


if __name__ == '__main__':
    unittest.main()
