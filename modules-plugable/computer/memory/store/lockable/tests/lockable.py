#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests the `lockable` group of the conformance suite on a store that does not declare the capability.

    python modules-plugable/computer/memory/store/lockable/tests/lockable.py

The subject is `lockable.py`, the group this module owes, named for the file that holds it per
[Test Naming](../../../../../../modules/process/test/rules/test-naming/test-naming.md), in the `tests/` folder of the
module that owns it per [Test Placement](../../../../../../modules/process/test/rules/test-placement/test-placement.md).
No adapter declares `lockable`, so the group runs on `volatile`, which does not: only `lock-refused-when-not-lockable`
applies, and the two cases that need a lockable store wait for one.
"""
from __future__ import annotations
import sys
import unittest
from importlib import import_module
from pathlib import Path
TESTS = Path(__file__).resolve().parent
TOP = next((p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()))
sys.path.insert(0, str(TOP))
sys.dont_write_bytecode = True
_m_volatile = import_module('modules.computer.memory.volatile.volatile')
_m_conformance = import_module('modules.computer.memory.conformance.conformance')
_m_group = import_module('modules-plugable.computer.memory.store.lockable.lockable')
_all = _m_conformance.test_case(lambda: _m_volatile.Volatile(), _m_group.CASES)
NotLockable = type('NotLockable', (unittest.TestCase,), {name: getattr(_all, name) for name in dir(_all) if name == 'test_lock_refused_when_not_lockable'})
del _all
if __name__ == '__main__':
    unittest.main()
