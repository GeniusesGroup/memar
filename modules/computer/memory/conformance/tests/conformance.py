#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import sys
import threading
import time
import unittest
from importlib import import_module
from pathlib import Path
from unittest import mock
TESTS = Path(__file__).resolve().parent
TOP = next((p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()))
sys.path.insert(0, str(TOP))
sys.dont_write_bytecode = True
TIER = 'unit'
BUDGET_SECONDS = 60
conformance = import_module('modules.computer.memory.conformance.conformance')
_m_volatile = import_module('modules.computer.memory.volatile.volatile')
LARGER = ('model-equivalence', 'kill-during-batch-is-atomic', 'reopen-sees-committed', 'killed-writer-leaves-no-lock', 'two-processes-lose-cleanly', 'one-process-sees-the-others-commit', 'changes-sees-other-process', 'paused-live-writer-is-not-overtaken', 'unknown-fate-settles-first')

def make():
    return _m_volatile.Volatile()

def passes(t, make):
    t.assertEqual(1, 1)

def fails(t, make):
    t.assertEqual(1, 2, 'the made-up difference')

def stalls(t, make):
    threading.Event().wait(20)

def applies(store):
    return True

def never(store):
    return False

def by_name():
    return {each.name: each for each in conformance.CASES}

class Budget(unittest.TestCase):

    def test_a_case_without_a_declared_budget_has_sixty_seconds(self) -> None:
        self.assertEqual(conformance.Case('x', applies, passes).budget, 60)

    def test_a_case_may_declare_more(self) -> None:
        self.assertEqual(conformance.Case('x', applies, passes, budget=300).budget, 300)

    def test_the_model_and_the_child_process_cases_declare_more(self) -> None:
        for name in LARGER:
            self.assertGreater(by_name()[name].budget, 60, name)

    def test_the_other_cases_keep_the_default(self) -> None:
        for each in conformance.CASES:
            if each.name not in LARGER and each.name != 'batch-visible-whole':
                self.assertEqual(each.budget, 60, each.name)

class Cost(unittest.TestCase):

    def test_a_case_without_a_declared_cost_spends_nothing(self) -> None:
        cost = conformance.Case('x', applies, passes).cost
        self.assertEqual((cost.subprocesses, cost.writes_files, cost.waits_on_clock), (0, False, False))

    def test_every_case_declares_its_cost(self) -> None:
        for each in conformance.CASES:
            self.assertIsInstance(each.cost, conformance.Cost, each.name)
            self.assertIsInstance(each.cost.subprocesses, int, each.name)
            self.assertIsInstance(each.cost.writes_files, bool, each.name)
            self.assertIsInstance(each.cost.waits_on_clock, bool, each.name)

    def test_the_cases_that_start_a_child_say_so(self) -> None:
        for name in ('reopen-sees-committed', 'killed-writer-leaves-no-lock', 'two-processes-lose-cleanly', 'one-process-sees-the-others-commit', 'changes-sees-other-process'):
            self.assertGreaterEqual(by_name()[name].cost.subprocesses, 1, name)
        self.assertEqual(by_name()['kill-during-batch-is-atomic'].cost.subprocesses, 200)

    def test_the_cases_that_wait_on_the_clock_say_so(self) -> None:
        for name in ('paused-live-writer-is-not-overtaken', 'unknown-fate-settles-first', 'killed-writer-leaves-no-lock'):
            self.assertTrue(by_name()[name].cost.waits_on_clock, name)

    def test_the_core_cases_start_no_process(self) -> None:
        for each in conformance.CASES:
            if each.group == 'core':
                self.assertEqual(each.cost.subprocesses, 0, each.name)

class Verdicts(unittest.TestCase):

    def test_a_case_that_keeps_the_contract_is_passed(self) -> None:
        result = conformance.Case('x', applies, passes).judge(make)
        self.assertIsInstance(result.verdict, conformance.Passed)

    def test_a_case_that_breaks_it_is_failed_with_the_message(self) -> None:
        result = conformance.Case('x', applies, fails).judge(make)
        self.assertIsInstance(result.verdict, conformance.Failed)
        self.assertIn('the made-up difference', result.message)

    def test_a_case_that_outruns_its_budget_is_exceeded_and_does_not_hold_the_run(self) -> None:
        started = time.monotonic()
        result = conformance.Case('x', applies, stalls, budget=0.3).judge(make)
        self.assertLess(time.monotonic() - started, 5)
        self.assertIsInstance(result.verdict, conformance.ExceededBudget)

    def test_an_owed_case_is_pending_and_is_not_run(self) -> None:
        ran = []
        result = conformance.Case('x', applies, lambda t, make: ran.append(1), owed=True).judge(make)
        self.assertIsInstance(result.verdict, conformance.Pending)
        self.assertEqual(ran, [])

    def test_a_case_that_does_not_apply_is_not_applicable_and_is_not_run(self) -> None:
        ran = []
        result = conformance.Case('x', never, lambda t, make: ran.append(1)).judge(make)
        self.assertIsInstance(result.verdict, conformance.NotApplicable)
        self.assertEqual(ran, [])

    def test_a_result_carries_its_case_and_what_it_spent(self) -> None:
        one = conformance.Case('x', applies, passes)
        result = one.judge(make)
        self.assertIs(result.case, one)
        self.assertGreaterEqual(result.spent, 0)

class Runner(unittest.TestCase):

    def test_run_gives_one_result_for_each_case_in_order(self) -> None:
        a = conformance.Case('x', applies, passes)
        b = conformance.Case('x', applies, fails)
        c = conformance.Case('x', applies, passes, owed=True)
        d = conformance.Case('x', never, passes)
        e = conformance.Case('x', applies, stalls, budget=0.3)
        with mock.patch.object(conformance, 'CASES', [a, b, c]):
            results = conformance.run(make, [d, e])
        self.assertEqual([each.case for each in results], [a, b, c, d, e])
        self.assertEqual([type(each.verdict) for each in results], [conformance.Passed, conformance.Failed, conformance.Pending, conformance.NotApplicable, conformance.ExceededBudget])

    def test_a_unittest_class_fails_the_test_of_a_case_that_outruns_its_budget(self) -> None:
        slow = conformance.Case('x', applies, stalls, budget=0.3)
        with mock.patch.object(conformance, 'CASES', []):
            suite = conformance.test_case(make, [slow])
        outcome = unittest.TestResult()
        unittest.defaultTestLoader.loadTestsFromTestCase(suite).run(outcome)
        self.assertEqual(outcome.testsRun, 1)
        self.assertEqual(len(outcome.failures), 1)
        self.assertIn('budget', outcome.failures[0][1])
if __name__ == '__main__':
    unittest.main()
