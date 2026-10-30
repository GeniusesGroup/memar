#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import sys
import unittest
from importlib import import_module
from pathlib import Path
TESTS = Path(__file__).resolve().parent
TOP = next((p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()))
for _each in (TOP / 'bundles' / 'memar' / 'services', TOP):
    if str(_each) not in sys.path:
        sys.path.insert(0, str(_each))
sys.dont_write_bytecode = True
_m_fast = import_module('modules-plugable.computer.memory.store.git-store.tests.git-store')
TIER = 'system'
BUDGET_SECONDS = 600
LocalSlow = _m_fast._only(_m_fast.BASES['Local'], _m_fast.SLOW_LOCAL, 'LocalSlow')
LocalRecordSlow = _m_fast._only(_m_fast.BASES['LocalRecord'], _m_fast.SLOW_RECORD, 'LocalRecordSlow')

def tearDownModule() -> None:
    _m_fast.clean_up()
if __name__ == '__main__':
    unittest.main()
