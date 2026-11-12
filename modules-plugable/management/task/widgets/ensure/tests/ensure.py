#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import sys
import unittest
from importlib import import_module
from pathlib import Path
from unittest import mock

TESTS = Path(__file__).resolve().parent
TOP = next(p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir())
sys.path.insert(0, str(TOP / 'bundles' / 'memar' / 'services'))
sys.path.insert(1, str(TOP / 'bundles' / 'memar'))
sys.path.insert(2, str(TOP))
sys.dont_write_bytecode = True

BUDGET_SECONDS = 30

ensure_widget = import_module('modules-plugable.management.task.widgets.ensure.ensure')


class EnsureWidget(unittest.TestCase):

    def test_open_without_priority_does_not_set_rank(self) -> None:
        with mock.patch.object(ensure_widget, 'ensure_task', return_value=('T', Path('T'))) as opened, mock.patch.object(ensure_widget, 'set_on') as set_on:
            sid, path = ensure_widget.open(None, 'Title', None, False, None, None, 'p', None)
        self.assertEqual(sid, 'T')
        self.assertEqual(path, Path('T'))
        opened.assert_called_once_with(None, 'Title', None, False, None, 'p', None)
        set_on.assert_not_called()

    def test_open_with_priority_sets_rank_after_ensure(self) -> None:
        with mock.patch.object(ensure_widget, 'ensure_task', return_value=('T', Path('T'))) as opened, mock.patch.object(ensure_widget, 'set_on') as set_on:
            ensure_widget.open(None, 'Title', None, True, 8, ['Topic=docs'], 'p', ['s-0'])
        opened.assert_called_once_with(None, 'Title', None, True, ['Topic=docs'], 'p', ['s-0'])
        set_on.assert_called_once_with('T', 8, 'p')


if __name__ == '__main__':
    unittest.main()
