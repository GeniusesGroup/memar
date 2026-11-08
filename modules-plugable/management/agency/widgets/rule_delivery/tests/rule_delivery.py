#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
import sys
import unittest
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = next(p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()) / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS / 'services'))
sys.path.insert(1, str(SCRIPTS))
sys.path.insert(2, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
_m = import_module('modules-plugable.management.agency.widgets.rule_delivery.rule_delivery')
RuleDelivery = _m.RuleDelivery
_rule = import_module('modules.process.rule.services.find_rules')
RuleHit = _rule.RuleHit

class FakeFind:

    def __init__(self) -> None:
        self.calls: list[tuple[str, list[str], int]] = []

    def do(self, subject: str, topics: list[str], most: int) -> list[RuleHit]:
        self.calls.append((subject, topics, most))
        return [RuleHit('modules/a/rules/r/r.md', 'the-rule', 'Why.')]

class ForSubject(unittest.TestCase):

    def test_the_declared_labels_named_in_the_subject_become_topics(self) -> None:
        find = FakeFind()
        delivery = RuleDelivery(find, lambda: ('agency', 'document', 'design'))
        hits = delivery.for_subject('Document the agency rule for a delegated step')
        self.assertEqual(find.calls[0][1], ['document', 'agency'])
        self.assertEqual(find.calls[0][0], 'Document the agency rule for a delegated step')
        self.assertEqual(hits[0].document, 'modules/a/rules/r/r.md')

    def test_a_subject_naming_no_label_has_no_topics(self) -> None:
        find = FakeFind()
        RuleDelivery(find, lambda: ('agency',)).for_subject('split a long step')
        self.assertEqual(find.calls[0][1], [])

    def test_an_empty_subject_is_refused_and_asks_nothing(self) -> None:
        find = FakeFind()
        with self.assertRaises(ValueError):
            RuleDelivery(find, lambda: ()).for_subject('   ')
        self.assertEqual(find.calls, [])

if __name__ == '__main__':
    unittest.main()
