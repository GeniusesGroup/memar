#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for opening a class of nodes: `open(project, class_name, needs)`, in `bundles/memar/services/memory/memory.py`.

    python bundles/memar/services/memory/tests/memory.py

The subject is `memory.py`, named for the file that holds it per
[Test Naming](../../../../../modules/process/test/rules/test-naming/test-naming.md), in the `tests/` folder of the module
that owns it per [Test Placement](../../../../../modules/process/test/rules/test-placement/test-placement.md); its
expectations are [Memory Record → Binding adapters to classes](../../../../../modules-plugable/computer/memory/store/record/record.md#binding-adapters-to-classes),
and the form of the key `memory` is the one `modules/process/project/services/preferences.py` declares, pinned here
because this is the service that reads it. Pinned on scratch projects of the suite's own, with a stand-in adapter
module whose `bind` lays `volatile` under each class; no adapter of a medium is used.

  Opens        A class the key binds is opened as `record` over the bound adapter, and reads what it writes.
  NotBound     A class the key does not name, and a project with no manifest or no key, are refused, naming the
               class and the line to add.
  LessThanNeeded
               An adapter that declares less than the needs, in a capability or a limit, or keeps a store `record`
               cannot be laid over, is refused; one that declares no limit meets any.
  SharedStore  Two classes whose adapter names one store are refused when either is opened.
  Malformed    A key whose form is broken, and one naming an adapter no module offers, are refused as malformed.
  InTheEntryPoint
               The entry point of `bundles/memar` declares `open`, and it is this one.
"""
from __future__ import annotations
import importlib.util
import sys
import tempfile
import types
import unittest
import unittest.mock
from importlib import import_module
from importlib.machinery import SourceFileLoader
from pathlib import Path
from typing import Any
TESTS = Path(__file__).resolve().parent
SCRIPTS = next((p for p in TESTS.parents if p.name == 'memar' and p.parent.name == 'bundles'))
TOP = SCRIPTS.parent.parent
for _folder in (TOP, SCRIPTS, SCRIPTS / 'services'):
    if str(_folder) not in sys.path:
        sys.path.insert(0, str(_folder))
sys.dont_write_bytecode = True
_m_fs_test_scratch = import_module('modules-plugable.computer.memory.filesystem.services.fs_test_scratch')
suite_scratch = _m_fs_test_scratch.suite_scratch
_m_store = import_module('modules.computer.memory.store.protocol.store')
_m_volatile = import_module('modules.computer.memory.volatile.volatile')
_m_record = import_module('modules-plugable.computer.memory.store.record.record')
_m_preferences = import_module('modules.process.project.services.preferences')
memory = import_module('bundles.memar.services.memory.memory')
Capability = _m_store.Capability
Committed = _m_store.Committed
Found = _m_store.Found
Limits = _m_store.Limits
Parameters = _m_store.Parameters
Needs = _m_record.Needs
Record = _m_record.Record
Volatile = _m_volatile.Volatile
OpeningRefusal = memory.OpeningRefusal
OpenRefused = memory.OpenRefused
REAL_ADAPTER_MODULE = memory.adapter_module
AT = bytes.fromhex('019a2000000070008000000000000001')

class StandIn:
    """An adapter for one class: `volatile` with the given declarations, keeping the store `store` names."""

    def __init__(self, store: str, parameters: Parameters, limits: Limits) -> None:
        self.store = store
        self.volatile = Volatile(parameters, limits)

    def open(self) -> Volatile:
        return self.volatile.open()

class Fixture(unittest.TestCase):

    def setUp(self) -> None:
        scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(scratch.cleanup)
        self.project = Path(scratch.name).resolve() / 'orchard'
        self.project.mkdir()
        self.stores: dict[str, str] = {}
        self.parameters, self.limits = (Parameters(), Limits())
        module = types.SimpleNamespace(bind=lambda project, class_name: StandIn(self.stores.get(class_name, class_name), self.parameters, self.limits))
        patch = unittest.mock.patch.object(memory, 'adapter_module', lambda name: module if name == 'stand-in' else None)
        patch.start()
        self.addCleanup(patch.stop)

    def prefer(self, value: str | None) -> None:
        line = '' if value is None else f'  {_m_preferences.MEMORY_KEY}: {value}\n'
        _m_preferences.preferences_path(self.project).write_text(f'name: orchard\n{_m_preferences.BLOCK_KEY}:\n{line}', encoding='utf-8', newline='\n')

    def refused(self, class_name: str, reason: Any, needs: Needs=Needs()) -> str:
        answer = memory.open(self.project, class_name, needs)
        self.assertIsInstance(answer, OpenRefused)
        self.assertEqual(answer.reason, reason)
        self.assertIn(class_name, answer.detail)
        return answer.detail

class Opens(Fixture):

    def test_a_bound_class_opens_as_record_over_its_adapter(self) -> None:
        self.prefer('work-records=stand-in, other=stand-in')
        opened = memory.open(self.project, 'work-records', Needs(frozenset({Capability.ATOMIC_BATCH})))
        self.assertIsInstance(opened, Record)
        self.assertEqual(opened.batch([], [(AT + b'alpha', b'a')]), Committed())
        self.assertEqual(opened.get([AT + b'alpha']), [Found(b'a', _m_store.token(b'a'))])
        self.assertEqual(opened.parts([AT]), [(('alpha', _m_store.token(b'a')),)])

class NotBound(Fixture):

    def test_a_class_the_key_does_not_name_is_refused_with_the_line_to_add(self) -> None:
        self.prefer('other=stand-in')
        detail = self.refused('work-records', OpeningRefusal.NOT_BOUND)
        self.assertIn(f'{_m_preferences.MEMORY_KEY}: other=stand-in, work-records=', detail)

    def test_no_manifest_and_no_key_are_refused(self) -> None:
        self.refused('work-records', OpeningRefusal.NOT_BOUND)
        self.prefer(None)
        detail = self.refused('work-records', OpeningRefusal.NOT_BOUND)
        self.assertIn(f'{_m_preferences.MEMORY_KEY}: work-records=', detail)

class LessThanNeeded(Fixture):

    def test_a_capability_not_declared_is_refused(self) -> None:
        self.prefer('work-records=stand-in')
        detail = self.refused('work-records', OpeningRefusal.LESS_THAN_NEEDED, Needs(frozenset({Capability.DURABLE})))
        self.assertIn(Capability.DURABLE.value, detail)

    def test_a_limit_below_the_needs_is_refused_and_no_limit_meets_any(self) -> None:
        self.prefer('work-records=stand-in')
        needs = Needs(limits=Limits(writes_per_batch=100))
        self.limits = Limits(writes_per_batch=99)
        self.assertIn('writes_per_batch', self.refused('work-records', OpeningRefusal.LESS_THAN_NEEDED, needs))
        self.limits = Limits(writes_per_batch=100)
        self.assertIsInstance(memory.open(self.project, 'work-records', needs), Record)
        self.limits = Limits()
        self.assertIsInstance(memory.open(self.project, 'work-records', needs), Record)

    def test_a_store_record_cannot_be_laid_over_is_refused(self) -> None:
        self.prefer('work-records=stand-in')
        self.parameters = Parameters(address_length=8)
        self.refused('work-records', OpeningRefusal.LESS_THAN_NEEDED)

class SharedStore(Fixture):

    def test_two_classes_naming_one_store_are_refused(self) -> None:
        self.prefer('work-records=stand-in, drafts=stand-in')
        self.stores = {'work-records': 'one', 'drafts': 'one'}
        self.assertIn('drafts', self.refused('work-records', OpeningRefusal.SHARED_STORE))
        self.refused('drafts', OpeningRefusal.SHARED_STORE)
        self.stores = {}
        self.assertIsInstance(memory.open(self.project, 'drafts', Needs()), Record)

class Malformed(Fixture):

    def test_a_broken_form_is_refused(self) -> None:
        for value in ('work-records', 'work-records=', '=stand-in', 'work-records=stand-in, work-records=stand-in', 'work-records=stand-in,,'):
            with self.subTest(value=value):
                self.prefer(value)
                self.refused('work-records', OpeningRefusal.MALFORMED)

    def test_an_adapter_no_module_offers_is_refused(self) -> None:
        patch = unittest.mock.patch.object(memory, 'adapter_module', REAL_ADAPTER_MODULE)
        patch.start()
        self.addCleanup(patch.stop)
        for adapter in ('no-such-adapter', 'record', '..', 'Stand-In'):
            with self.subTest(adapter=adapter):
                self.prefer(f'work-records={adapter}')
                self.assertIn(adapter, self.refused('work-records', OpeningRefusal.MALFORMED))

class InTheEntryPoint(unittest.TestCase):

    def test_the_entry_point_declares_this_open(self) -> None:
        spec = importlib.util.spec_from_loader('memar_launcher', SourceFileLoader('memar_launcher', str(SCRIPTS / 'memar')))
        launcher = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(launcher)
        self.assertIs(launcher.open, memory.open)
if __name__ == '__main__':
    unittest.main()
