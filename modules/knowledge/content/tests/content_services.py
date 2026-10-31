#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the services of the content domain, `services/content_add.py` and `services/content_read.py`.

    python modules/knowledge/content/tests/content_services.py

The subject is `Content_Add` and `Content_Read` (`services/content-add/`, `services/content-read/`): they take
a content store, open no file, know no task and no timeline, and check no template.
"""
from __future__ import annotations
from importlib import import_module
import sys
import unittest
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = next(p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()) / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
add = import_module('modules.knowledge.content.services.content_add')
read = import_module('modules.knowledge.content.services.content_read')


class Recording:

    def __init__(self) -> None:
        self.added = []

    def add_content(self, kind, text):
        self.added.append((kind, text))
        return 'uuid-1'

    def read_content(self, content):
        return ('plan', 'x\n', True) if content == 'uuid-1' else ('', '', False)


class Add(unittest.TestCase):

    def test_a_text_and_a_kind_make_a_content_whose_uuid_is_returned(self) -> None:
        store = Recording()
        self.assertEqual(add.add_content(store, 'hello\n', 'message'), 'uuid-1')
        self.assertEqual(store.added, [('message', 'hello\n')])

    def test_any_text_and_any_kind_is_accepted_unchecked(self) -> None:
        store = Recording()
        add.add_content(store, 'not a template at all', 'anything')
        self.assertEqual(store.added, [('anything', 'not a template at all')])


class Read(unittest.TestCase):

    def test_a_content_is_read_by_its_uuid_with_its_kind(self) -> None:
        self.assertEqual(read.read_content(Recording(), 'uuid-1'), ('plan', 'x\n', True))

    def test_an_unknown_uuid_is_not_found(self) -> None:
        self.assertEqual(read.read_content(Recording(), 'nope'), ('', '', False))


if __name__ == '__main__':
    unittest.main()
