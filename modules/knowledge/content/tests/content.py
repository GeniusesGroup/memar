#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the `memar content` verb tree in `modules/knowledge/content/content.py`.

    python modules/knowledge/content/tests/content.py

The subject is the content domain's verb, named for the file that declares it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).
Each verb's own behaviour is pinned by the suite named for that verb's file.

Nothing here writes anything: every test asks the launcher for help or for an
error, as a person would type it.

What is pinned, and what each pin is for:

  OneVerbHoldsThemAll  Every verb nests under `content`, so one subject has one
                       name and the flat spellings error rather than leaving a
                       second interface beside the first.
  RootVerbIsNotHere    Where Memar lives moved out of this domain and into the
                       installer, as `--root`: it is not a question about
                       content, and `bundles/memar/services/install/tests/install.py` holds its pins.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
import os
import subprocess
import sys
import unittest
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = next(p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()) / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
LAUNCHER = SCRIPTS / 'memar'

def run_memar(*arguments: str) -> subprocess.CompletedProcess:
    environment = dict(os.environ, COLUMNS='80', PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1', MEMAR_NO_AUTO_UPDATE='1')
    return subprocess.run([sys.executable, str(LAUNCHER), *arguments], capture_output=True, env=environment)

class OneVerbHoldsThemAll(unittest.TestCase):
    """Every verb lives under `content`, and nowhere else.

    One subject, one word. An earlier state had three verbs nested and nine flat,
    which is neither the grouping nor the flat set: `content` then named nothing
    a reader could place, and the write verbs were left outside the verb whose
    name was what they acted on. The flat spellings must error, so no second
    interface survives beside the first — and the check is by name rather than by
    hash, because argparse wraps help to the terminal width and a byte pin is a
    property of the machine as much as of the file.
    """
    EVERY_VERB = ('path', 'meta', 'section', 'context', 'search', 'find', 'backlinks', 'obligations', 'questions', 'changelog-append', 'list-ai-only-changelog-records', 'add-human-approval-to-changelog-record', 'hour-id', 'write', 'edit', 'check')

    def test_every_verb_is_accepted_under_content(self) -> None:
        for verb in self.EVERY_VERB:
            with self.subTest(verb=verb):
                asked = run_memar('content', verb, '--help')
                self.assertEqual(asked.returncode, 0, asked.stderr)
                shown = asked.stdout.decode('utf-8', 'replace')
                self.assertIn(f'usage: memar content {verb}', shown)

    def test_the_flat_spellings_are_gone(self) -> None:
        for verb in self.EVERY_VERB:
            with self.subTest(verb=verb):
                completed = run_memar(verb, '--help')
                self.assertNotEqual(completed.returncode, 0, verb)
                self.assertIn('invalid choice', completed.stderr.decode('utf-8', 'replace'), verb)

    def test_content_groups_exactly_these_verbs(self) -> None:
        asked = run_memar('content', '--help')
        self.assertEqual(asked.returncode, 0, asked.stderr)
        shown = asked.stdout.decode('utf-8', 'replace')
        listed = {line.split()[0] for line in shown.splitlines() if line.startswith('    ') and (not line.startswith('     '))}
        self.assertEqual(listed, set(self.EVERY_VERB))

    def test_content_is_a_verb_of_memar(self) -> None:
        asked = run_memar('--help')
        self.assertEqual(asked.returncode, 0, asked.stderr)
        shown = asked.stdout.decode('utf-8', 'replace')
        self.assertIn('memar content search <term>', ' '.join(shown.split()))

class RootVerbIsNotHere(unittest.TestCase):

    def test_no_verb_of_this_domain_answers_where_memar_lives(self) -> None:
        completed = run_memar('content', 'root')
        self.assertEqual(completed.returncode, 2)
        self.assertIn('invalid choice', completed.stderr.decode('utf-8', 'replace'))
        self.assertFalse((SCRIPTS.parent.parent / 'modules' / 'knowledge' / 'content' / 'services' / 'root.py').exists())
if __name__ == '__main__':
    unittest.main(verbosity=2)
