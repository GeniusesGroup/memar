#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import sys
import unittest
from importlib import import_module
from pathlib import Path

TESTS = Path(__file__).resolve().parent
TOP = next(p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir())
sys.path.insert(0, str(TOP / 'bundles' / 'memar' / 'services'))
sys.path.insert(1, str(TOP / 'bundles' / 'memar'))
sys.path.insert(2, str(TOP))
sys.dont_write_bytecode = True

BUDGET_SECONDS = 30

services_mod = import_module('modules.process.services.services')
Process_Services = services_mod.Process_Services


class _Face:

    def __init__(self, operation_id: str, media_type: str = '', summary: str = '') -> None:
        self._operation_id = operation_id
        self._media_type = media_type
        self._summary = summary
        self.calls: list[dict] = []

    def operation_id(self) -> str:
        return self._operation_id

    def media_type(self) -> str:
        return self._media_type

    def summary(self) -> str:
        return self._summary

    def do(self, **request):
        self.calls.append(request)
        return request.get('thing')


class ProcessServices(unittest.TestCase):

    def test_register_then_get_by_id(self) -> None:
        pool = Process_Services()
        face = _Face('aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee', 'application/test+service', 'a test service')
        pool.register(face)
        found = pool.get_by_id(face.operation_id())
        self.assertIs(found, face)
        self.assertEqual(found.do(thing='T', word='1'), 'T')
        self.assertEqual(face.calls, [{'thing': 'T', 'word': '1'}])

    def test_get_by_id_miss_is_none(self) -> None:
        pool = Process_Services()
        self.assertIsNone(pool.get_by_id('00000000-0000-0000-0000-000000000000'))

    def test_register_refuses_empty_operation_id(self) -> None:
        pool = Process_Services()
        with self.assertRaises(ValueError):
            pool.register(_Face(''))

    def test_register_refuses_duplicate_operation_id(self) -> None:
        pool = Process_Services()
        pool.register(_Face('aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee', 'a/one'))
        with self.assertRaises(ValueError):
            pool.register(_Face('aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee', 'a/two'))

    def test_get_by_media_type_and_services_list(self) -> None:
        pool = Process_Services()
        one = _Face('11111111-1111-1111-1111-111111111111', 'a/one')
        two = _Face('22222222-2222-2222-2222-222222222222', 'a/two')
        pool.register(one)
        pool.register(two)
        self.assertIs(pool.get_by_media_type('a/two'), two)
        self.assertEqual(pool.services(), [one, two])

    def test_delete_removes_by_id_and_media_type(self) -> None:
        pool = Process_Services()
        face = _Face('aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee', 'a/gone')
        pool.register(face)
        pool.delete(face)
        self.assertIsNone(pool.get_by_id(face.operation_id()))
        self.assertIsNone(pool.get_by_media_type('a/gone'))
        self.assertEqual(pool.services(), [])


if __name__ == '__main__':
    unittest.main()
