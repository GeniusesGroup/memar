#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
sys.dont_write_bytecode = True
BUDGET_SECONDS = 10
from modules.process.service.primitive.call_name import call_name
from modules.process.service.errors.call_name import InvalidCallName


class Details:
    def __init__(self, domain, name):
        self.domain, self.name = domain, name

    def Domain(self):
        return self.domain

    def Name(self):
        return self.name

    def Aliases(self):
        raise AssertionError('aliases are not call names')

    def Abbreviation(self):
        raise AssertionError('abbreviations are not call names')


class CallName(unittest.TestCase):
    def test_only_domain_and_name_make_the_key(self):
        self.assertEqual(call_name(Details('Task', 'Ensure')), 'task_ensure')

    def test_spaces_hyphens_and_underscores_have_one_spelling(self):
        self.assertEqual(call_name(Details(' Memar  Git ', 'Show-task__records')), 'memar_git_show_task_records')

    def test_both_components_are_required_and_invalid_components_are_refused(self):
        for domain, name in (('', 'run'), ('task', ''), (' ', 'run'), ('task', ' '), (None, 'run'), ('x/y', 'run'), ('task', '_run'), ('task', 'run.'), ('تسک', 'run')):
            with self.subTest(domain=domain, name=name), self.assertRaises(InvalidCallName):
                call_name(Details(domain, name))


if __name__ == '__main__':
    unittest.main()
