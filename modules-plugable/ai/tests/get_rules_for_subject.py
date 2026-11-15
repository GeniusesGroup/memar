#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
import sys
import unittest
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = next(p for p in TESTS.parents if p.name == 'modules-plugable').parent / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS / 'services'))
sys.path.insert(1, str(SCRIPTS))
sys.path.insert(2, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
_m = import_module('modules-plugable.management.agency.services.get_rules_for_subject.get_rules_for_subject')
_rule = import_module('modules.process.rule.services.find_rules')
RuleHit = _rule.RuleHit

class Text(unittest.TestCase):

    def test_each_hit_is_a_line_with_its_link_anchor_and_why(self) -> None:
        text = _m.text_of([RuleHit('modules/a/rules/r/r.md', 'the-rule', 'Why.')])
        self.assertEqual(text.splitlines()[-1], '/modules/a/rules/r/r.md#the-rule | Why.')

    def test_a_long_why_is_cut_at_the_limit(self) -> None:
        text = _m.text_of([RuleHit('modules/a/rules/r/r.md', 'the-rule', 'W' * 500)])
        self.assertEqual(len(text.splitlines()[-1].split(' | ', 1)[1]), _m.WHY_LIMIT)

    def test_no_hit_says_so_and_names_the_search_it_stands_for(self) -> None:
        text = _m.text_of([])
        self.assertIn('no rule', text)
        self.assertIn('memar content_find', text)

    def test_the_verb_declares_itself_with_one_subject_argument(self) -> None:
        declared = _m.DECLARATIONS[0]
        self.assertEqual(declared.name, _m.COMMAND)
        self.assertEqual([(each.name, each.shape) for each in declared.fields], [('subject', 'word')])

if __name__ == '__main__':
    unittest.main()
