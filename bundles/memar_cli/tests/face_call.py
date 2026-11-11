#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations

import importlib.machinery
import importlib.util
import sys
import unittest
from pathlib import Path

BUDGET_SECONDS = 60
TESTS = Path(__file__).resolve().parent
FACE = TESTS.parent
TOP = FACE.parent.parent
SERVER = TOP / 'bundles' / 'memar'
for folder in (TOP, FACE, SERVER, SERVER / 'services'):
    if str(folder) not in sys.path:
        sys.path.insert(0, str(folder))


def load_face():
    path = FACE / 'memar'
    loader = importlib.machinery.SourceFileLoader('memar_cli_face_test', str(path))
    module = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = module
    loader.exec_module(module)
    return module


class FaceBuildsServerCallWithoutHandingArgv(unittest.TestCase):

    def test_parsed_verb_becomes_fields_and_runs(self) -> None:
        face = load_face()
        top, _ = face.assemble(face.services())
        parsed = top.parse_args(['commands'])
        call = face.server_call(parsed)
        self.assertNotIn('argv', call)
        self.assertIn('fields', call)
        self.assertTrue(call['runs'])
        from bundles.memar.services.dispatch import dispatch
        answer = dispatch.handle(call)
        self.assertEqual(answer['status'], 0)
        self.assertIn('memar', answer['stdout'])


if __name__ == '__main__':
    unittest.main()
