#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
TIER = 'unit'
BUDGET_SECONDS = 30
import ast
import enum
import io
import tokenize
import typing
import sys
import unittest
from importlib import import_module
from pathlib import Path
TESTS = Path(__file__).resolve().parent
TOP = next((p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()))
sys.path.insert(0, str(TOP))
sys.dont_write_bytecode = True
_m_volatile = import_module('modules.computer.memory.volatile.volatile')
_m_conformance = import_module('modules.computer.memory.conformance.conformance')
_m_group = import_module('modules-plugable.computer.memory.store.lockable.lockable')
_all = _m_conformance.test_case(lambda: _m_volatile.Volatile(), _m_group.CASES)
NotLockable = type('NotLockable', (unittest.TestCase,), {name: getattr(_all, name) for name in dir(_all) if name == 'test_lock_refused_when_not_lockable'})
del _all
def bare(path):
    source = Path(path).read_text(encoding='utf-8')
    comments = [t.start[0] for t in tokenize.generate_tokens(io.StringIO(source).readline) if t.type == tokenize.COMMENT and t.start[0] > 2]
    documented = [getattr(n, 'lineno', 0) for n in ast.walk(ast.parse(source)) if isinstance(n, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) and ast.get_docstring(n, clean=False) is not None]
    return (comments, documented)

def own_error_types(module):
    return sorted((name for name, each in vars(module).items() if isinstance(each, type) and each.__module__ == module.__name__ and (issubclass(each, (BaseException, enum.Enum)) or 'Refus' in name)))

class Cases(unittest.TestCase):

    def test_the_cases_that_wait_declare_a_budget_and_a_cost_that_waits_on_the_clock(self) -> None:
        waiting = {'lock_excludes_second_holder', 'lock_lapses_with_lease'}
        for each in _m_group.CASES:
            with self.subTest(case=each.name):
                self.assertGreater(each.budget, 0)
                self.assertEqual(each.cost.waits_on_clock, each.check.__name__ in waiting)
                self.assertEqual(each.cost.subprocesses, 0)

    def test_lock_answers_what_get_would_or_a_refusal(self) -> None:
        hints = typing.get_type_hints(_m_group.Lockable.lock, globalns=vars(_m_group._m_lockable), localns=vars(_m_group._m_lockable))
        self.assertEqual(hints['return'], _m_group._m_store.Read | _m_group._m_store.Refused)

class NoComments(unittest.TestCase):

    def test_the_files_carry_no_comment_and_no_docstring(self) -> None:
        for path in (_m_group.__file__, _m_group._m_lockable.__file__, __file__):
            with self.subTest(path=Path(path).name):
                self.assertEqual(bare(path), ([], []))
if __name__ == '__main__':
    unittest.main()
