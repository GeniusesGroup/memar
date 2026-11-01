#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import unittest
from importlib import import_module
from typing import Any, Callable
_m_store = import_module('modules.computer.memory.store.protocol.store')
_m_conformance = import_module('modules.computer.memory.conformance.conformance')
Capability = _m_store.Capability
Case = _m_conformance.Case
Committed = _m_store.Committed
Found = _m_store.Found
address = _m_conformance.address
token = _m_store.token
value = _m_conformance.value

def medium_is_working_tree(store: Any) -> bool:
    return Capability.DURABLE in store.capabilities and Capability.LEAVES_WORKING_TREE_UNTOUCHED not in store.capabilities

def committed_batch_is_visible_as_files(t: unittest.TestCase, make: Callable[[], Any]) -> None:
    adapter = make()
    root = adapter.get_memory_root().host_path()
    store = adapter.open()
    written = [(address(store, i), value(store, i)) for i in (1, 2, 3)]
    t.assertEqual(store.batch([], written), Committed())
    for at, data in written:
        file = adapter.file_at(at)
        t.assertTrue(file.exists(), at.hex())
        t.assertEqual(file.get_file_data(), data)
        t.assertTrue(str(file.host_path()).startswith(str(root)))
        t.assertTrue(file.host_path().is_relative_to(root) if hasattr(file.host_path(), 'is_relative_to') else str(file.host_path()).startswith(str(root)))
    found = store.get([at for at, _ in written])
    t.assertEqual(found, [Found(data, token(data)) for _, data in written])

CASES = [Case('working-tree', medium_is_working_tree, committed_batch_is_visible_as_files)]
