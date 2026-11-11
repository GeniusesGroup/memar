#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations

import ast
import unittest
from pathlib import Path

BUDGET_SECONDS = 10
ROOT = Path(__file__).resolve().parents[1]


class DispatchHasNoArgparseFace(unittest.TestCase):

    def test_dispatch_source_imports_no_argparse(self) -> None:
        tree = ast.parse((ROOT / 'dispatch.py').read_text(encoding='utf-8'))
        names = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names.update(alias.name.split('.')[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                names.add(node.module.split('.')[0])
        self.assertNotIn('argparse', names)


if __name__ == '__main__':
    unittest.main()
