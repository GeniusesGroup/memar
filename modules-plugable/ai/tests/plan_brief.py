#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Stable-verb face for get-task-plan-carry-out-brief; contract tests live on the agency widget.

    python modules-plugable/ai/tests/plan_brief.py

Composition is `modules-plugable/management/agency/widgets/plan_carry_out_brief/`;
this file loads that suite so the prior path still runs the same checks.
"""
from __future__ import annotations
from importlib import import_module
import sys
from pathlib import Path
import unittest
TESTS = Path(__file__).resolve().parent
SCRIPTS = next(p for p in TESTS.parents if p.name == 'modules-plugable').parent / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS / 'services'))
sys.path.insert(1, str(SCRIPTS))
sys.path.insert(2, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
BUDGET_SECONDS = 10
_suite = import_module('modules-plugable.management.agency.widgets.plan_carry_out_brief.tests.plan_carry_out_brief')

def load_tests(loader, tests, pattern):
    return loader.loadTestsFromModule(_suite)

if __name__ == '__main__':
    unittest.main(module=_suite, verbosity=2)
