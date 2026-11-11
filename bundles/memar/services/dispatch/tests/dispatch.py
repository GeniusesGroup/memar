#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations

import io
import os
import sys
import tempfile
import unittest
from pathlib import Path

BUDGET_SECONDS = 30

TOP = Path(__file__).resolve().parents[4]
if str(TOP) not in sys.path:
    sys.path.insert(0, str(TOP))
SERVICES = TOP / 'bundles' / 'memar' / 'services'
if str(SERVICES) not in sys.path:
    sys.path.insert(0, str(SERVICES))


def _probe_run(args) -> int:
    print(getattr(args, 'word', ''), end='')
    return 0


def _boom(args) -> int:
    raise SystemExit('gone')


class DispatchRunsWithoutArgv(unittest.TestCase):

    def test_call_runs_named_refs_and_returns_answer(self) -> None:
        from bundles.memar.services.dispatch import dispatch

        with tempfile.TemporaryDirectory() as folder:
            call = {
                'fields': {'word': 'hello'},
                'runs': [f'{__name__}:_probe_run'],
                'cwd': folder,
                'env': dict(os.environ),
                'stdin': '',
            }
            answer = dispatch.handle(call)
        self.assertEqual(answer['status'], 0)
        self.assertEqual(answer['stdout'], 'hello')
        self.assertEqual(answer['stderr'], '')

    def test_refuses_argv_key(self) -> None:
        from bundles.memar.services.dispatch import dispatch

        with self.assertRaises(dispatch.Refused):
            dispatch.handle({'argv': ['task', 'list'], 'fields': {}, 'runs': [], 'cwd': os.getcwd(), 'env': {}, 'stdin': ''})

    def test_system_exit_becomes_status_not_a_crash(self) -> None:
        from bundles.memar.services.dispatch import dispatch

        with tempfile.TemporaryDirectory() as folder:
            answer = dispatch.handle({
                'fields': {},
                'runs': [f'{__name__}:_boom'],
                'cwd': folder,
                'env': dict(os.environ),
                'stdin': '',
            })
        self.assertEqual(answer['status'], 1)
        self.assertIn('gone', answer['stderr'])


if __name__ == '__main__':
    unittest.main()
