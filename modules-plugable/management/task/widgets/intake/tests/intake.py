#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the intake widget: text rank with module facet and min_likeness, then ensure-parts.

    python modules-plugable/management/task/widgets/intake/tests/intake.py

The subject is Intake.Open over Likeness_Rank and Parts_Ensure. What is pinned:

  Rank       Hits below min_likeness are dropped; a different module facet is
             not returned; an optional role narrows further; excluded subjects
             are left out.
  Intake     Hits are printed before ensure-parts runs; the first build does
             not refuse on hits; ensure-parts receives the title and project.
  AgentPath  The verb help names the intake path and does not put task ids on
             the critical path for duplicate hunting.
"""
from __future__ import annotations
from importlib import import_module
import argparse
import io
import sys
import unittest
from pathlib import Path

TESTS = Path(__file__).resolve().parent
ROOT = next(p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir())
SCRIPTS = ROOT / 'bundles' / 'memar'
for folder in (SCRIPTS, SCRIPTS / 'services', ROOT):
    if str(folder) not in sys.path:
        sys.path.insert(0, str(folder))
sys.dont_write_bytecode = True

intake_mod = import_module('modules-plugable.management.task.widgets.intake.intake')
store_mod = import_module('modules-plugable.knowledge.text.likeness.services.likeness_memory_store')
rank_mod = import_module('modules-plugable.knowledge.text.likeness.services.rank-likeness.rank-likeness')

BUDGET_SECONDS = 30


class RankFacets(unittest.TestCase):

    def setUp(self) -> None:
        self.store = store_mod.Likeness_Memory_Store()
        self.store.put('tasks', 'a', 't1', ('intake', 'widget', 'rank'), module='task', role='body')
        self.store.put('tasks', 'b', 't2', ('intake', 'widget'), module='task', role='title')
        self.store.put('tasks', 'c', 't3', ('intake', 'widget', 'rank'), module='agency', role='body')
        self.rank = rank_mod.Likeness_Rank()

    def test_module_facet_keeps_only_that_module(self) -> None:
        hits = self.rank.rank('tasks', ('intake', 'widget', 'rank'), intake_mod._FacetStore(self.store, 'task', ''), (), 10, min_likeness=0.0)
        self.assertEqual([subject for subject, _ in hits], ['a', 'b'])

    def test_role_narrows(self) -> None:
        hits = self.rank.rank('tasks', ('intake', 'widget', 'rank'), intake_mod._FacetStore(self.store, 'task', 'body'), (), 10, min_likeness=0.0)
        self.assertEqual([subject for subject, _ in hits], ['a'])

    def test_min_likeness_drops_weaker_hits(self) -> None:
        hits = self.rank.rank('tasks', ('intake', 'widget', 'rank'), intake_mod._FacetStore(self.store, 'task', ''), (), 10, min_likeness=0.9)
        self.assertEqual([subject for subject, _ in hits], ['a'])

    def test_excluded_subjects_are_left_out(self) -> None:
        hits = self.rank.rank('tasks', ('intake', 'widget', 'rank'), intake_mod._FacetStore(self.store, 'task', ''), ('a',), 10, min_likeness=0.0)
        self.assertEqual([subject for subject, _ in hits], ['b'])


class IntakeWidget(unittest.TestCase):

    def test_prints_hits_then_calls_ensure_parts_without_gating(self) -> None:
        store = store_mod.Likeness_Memory_Store()
        store.put('tasks', 'dup', 't1', ('same', 'request'), module='task', role='body')
        seen = []
        lines = []

        def ensure(**kwargs):
            seen.append(kwargs)
            return ('new-id', Path('unused'))

        widget = intake_mod.Intake(ensure=ensure, store=store, printer=lines.append)
        hits, sid, _ = widget.open(
            scope='tasks',
            text='same request body',
            module='task',
            role='body',
            min_likeness=0.0,
            title='Same request',
            project='memar',
        )
        self.assertEqual(sid, 'new-id')
        self.assertEqual([subject for subject, _ in hits], ['dup'])
        self.assertTrue(any(line.startswith('hits:') for line in lines))
        self.assertTrue(any('dup' in line for line in lines))
        self.assertEqual(seen[0]['title'], 'Same request')
        self.assertEqual(seen[0]['project'], 'memar')

    def test_empty_hits_still_ensure(self) -> None:
        seen = []

        def ensure(**kwargs):
            seen.append(kwargs)
            return ('made', Path('unused'))

        lines = []
        widget = intake_mod.Intake(ensure=ensure, store=store_mod.Likeness_Memory_Store(), printer=lines.append)
        hits, sid, _ = widget.open(scope='tasks', text='brand new idea', module='task', title='Brand new', project='p')
        self.assertEqual((hits, sid), ([], 'made'))
        self.assertIn('  (none)', lines)
        self.assertEqual(len(seen), 1)


class AgentPath(unittest.TestCase):

    def test_help_names_the_unavailable_related_task_index(self) -> None:
        parser = argparse.ArgumentParser()
        verbs = parser.add_subparsers()
        intake_mod.describe(verbs)
        help_text = verbs.choices['intake'].description
        self.assertIn('min_likeness', help_text.lower().replace('-', '_'))
        self.assertIn('module', help_text.lower())
        self.assertIn('existing tasks were not searched', help_text.lower())

    def test_default_store_does_not_claim_existing_tasks_were_searched(self) -> None:
        lines = []
        widget = intake_mod.Intake(ensure=lambda **kw: ('made', Path('unused')), printer=lines.append)
        widget.open(scope='tasks', text='new idea', module='task', title='New idea')
        self.assertTrue(any('existing tasks were not searched' in line for line in lines))


if __name__ == '__main__':
    unittest.main()
