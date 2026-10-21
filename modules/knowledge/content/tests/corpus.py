#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the checkout's corpus in `modules/knowledge/content/services/corpus.py`.

    python modules/knowledge/content/tests/corpus.py

The subject is which files of a checkout are its content and which its ledgers,
named for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes outside its scratch folder: every checkout is laid out in
one, made under the folder `modules-plugable/computer/filesystem/services/fs_test_scratch.py` names, and removed
again, and no test walks the repository's own tree.

What is pinned, and what each pin is for:

  CorpusIsTheCheckout  The boundary is the whole checkout — `docs/`, `modules/`,
                       `bundles/`, `.agents/` — because a tool named for content that could
                       not search code would be a tool for documents. Pinned
                       per folder, because a tool that quietly stopped at
                       `docs/` reported a narrower world under the wider name.
                       Generated and dependency folders stay out by the decision
                       already written for the two things that copy a checkout,
                       and the work-list reads every ledger of the checkout,
                       not only the ones under `docs/`.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
from machine.plugable_import import load as plugable_load
_m_fs_test_scratch = plugable_load('computer.filesystem.services.fs_test_scratch')
suite_scratch = _m_fs_test_scratch.suite_scratch
import sys
import tempfile
import unittest
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parents[3] / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
import modules.knowledge.content.services.corpus as content_corpus

class CorpusIsTheCheckout(unittest.TestCase):
    """The corpus is the whole checkout, so the tool's name is not narrower than its reach.

    `docs/` is where the model is argued, not where the repository's content
    ends: the model definitions, the rule catalog, the protocol implementations
    and the sources all live under `modules/`, what runs or aggregates them
    under `bundles/`, and the configuration a session is driven by lives under
    `.agents/`. A tool named for content that could not reach them reported a
    narrower world under the wider name.
    """

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)

    def write(self, relative: str, text: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8', newline='\n')
        return path

    def a_checkout(self) -> Path:
        for folder in ('docs', 'modules', 'modules-plugable', 'bundles', '.agents'):
            (self.root / folder).mkdir(parents=True, exist_ok=True)
        (self.root / 'README.md').write_text('# R\n', encoding='utf-8', newline='\n')
        return self.root

    def test_the_corpus_reaches_each_folder_the_content_lives_in(self) -> None:
        root = self.a_checkout()
        for folder in ('docs', 'modules', 'modules-plugable', 'bundles', '.agents'):
            self.write(f'{folder}/note.md', '# Note\n')
        self.write('README.md', '# R\n')
        found = {path.relative_to(root).parts[0] for path in content_corpus.content_files(root)}
        self.assertEqual(found, {'docs', 'modules', 'modules-plugable', 'bundles', '.agents', 'README.md'})

    def test_a_folder_that_is_not_content_stays_out(self) -> None:
        root = self.a_checkout()
        self.write('docs/kept.md', '# Kept\n')
        self.write('node_modules/vendored/vendored.md', '# Vendored\n')
        self.write('temp/s-1/scratch.md', '# Scratch\n')
        self.write('.agents/tasks/s-2/plan.md', '# Plan\n')
        found = {path.relative_to(root).as_posix() for path in content_corpus.content_files(root)}
        self.assertIn('docs/kept.md', found)
        self.assertNotIn('node_modules/vendored/vendored.md', found)
        self.assertNotIn('temp/s-1/scratch.md', found)
        self.assertNotIn('.agents/tasks/s-2/plan.md', found)

    def test_a_sessions_folder_under_agents_is_no_longer_left_out(self) -> None:
        root = self.a_checkout()
        self.write('.agents/tasks/s-3/report.md', '# Report\n')
        self.write('.agents/tasks/s-3/docs/entry.changelog.md', '# Changelog\n')
        self.write('.agents/skills/memar/SKILL.md', '# Skill\n')
        found = {path.relative_to(root).as_posix() for path in content_corpus.content_files(root)}
        ledgers = {path.relative_to(root).as_posix() for path in content_corpus.ledger_files(root)}
        self.assertIn('.agents/tasks/s-3/report.md', found)
        self.assertIn('.agents/tasks/s-3/docs/entry.changelog.md', ledgers)
        self.assertIn('.agents/skills/memar/SKILL.md', found)

    def test_a_folder_holding_none_of_the_content_folders_is_refused(self) -> None:
        empty = self.root / 'not-a-checkout'
        empty.mkdir()
        with self.assertRaises(SystemExit) as raised:
            content_corpus.content_files(empty)
        self.assertIn('not a Memar checkout', str(raised.exception))

    def test_the_search_corpus_excludes_ledgers_and_ledgers_are_still_reachable(self) -> None:
        root = self.a_checkout()
        self.write('docs/one.changelog.md', '# One\n')
        self.write('modules/two.changelog.md', '# Two\n')
        searched = {path.name for path in content_corpus.content_files(root)}
        ledgers = {path.name for path in content_corpus.ledger_files(root)}
        self.assertNotIn('one.changelog.md', searched)
        self.assertEqual(ledgers, {'one.changelog.md', 'two.changelog.md'})
if __name__ == '__main__':
    unittest.main(verbosity=2)
