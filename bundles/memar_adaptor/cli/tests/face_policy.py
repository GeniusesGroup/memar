#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import sys
import unittest
from pathlib import Path
FACE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(FACE))
sys.dont_write_bytecode = True
BUDGET_SECONDS = 10
import face_policy

def named_run(arguments) -> None:
    return None

def make_closure():
    def run(arguments) -> None:
        return None
    return run

class RunRef(unittest.TestCase):

    def test_a_run_the_server_can_load_by_name_has_a_ref(self) -> None:
        sys.modules[__name__] = sys.modules['__main__'] if __name__ == '__main__' else sys.modules[__name__]
        self.assertEqual(face_policy.run_ref(named_run), f'{named_run.__module__}:named_run')

    def test_a_closure_or_lambda_has_no_ref_so_the_face_runs_it_itself(self) -> None:
        self.assertIsNone(face_policy.run_ref(make_closure()))
        self.assertIsNone(face_policy.run_ref(lambda arguments: None))


class FlatEntryPolicy(unittest.TestCase):
    def test_the_flat_transport_and_resident_calls_keep_their_special_entry(self):
        for name, kind in (('mcp_serve', 'relay'), ('resident_serve', 'server'),
                           ('resident_status', 'only-if-running'), ('resident_stop', 'only-if-running'),
                           ('memar_update', 'send')):
            with self.subTest(name=name):
                self.assertEqual(face_policy.kind_of([name]), kind)

    def test_help_for_a_special_call_is_a_help_request_not_a_started_transport(self):
        for name in ('mcp_serve', 'resident_serve', 'resident_status', 'resident_stop'):
            for help_flag in ('--help', '-h'):
                self.assertEqual(face_policy.kind_of([name, help_flag]), 'send')

    def test_old_group_words_are_not_special_calls(self):
        self.assertEqual(face_policy.kind_of(['mcp', 'serve']), 'send')

if __name__ == '__main__':
    unittest.main()
