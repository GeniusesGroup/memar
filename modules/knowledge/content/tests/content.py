#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for flat content calls (`content_search`, …).

    python modules/knowledge/content/tests/content.py

Public calls are flat: CLI and MCP share one name. Grouped spellings
(`memar content <verb>`) are refused. Each verb's own behaviour is pinned by
the suite named for that verb's file.

Nothing here writes anything: every test asks the launcher for help or for an
error, as a person would type it.
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
LAUNCHER = SCRIPTS.parent / 'memar_adaptor' / 'cli' / 'memar'

def run_memar(*arguments: str) -> subprocess.CompletedProcess:
    environment = dict(os.environ, COLUMNS='80', PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1', MEMAR_NO_AUTO_UPDATE='1')
    return subprocess.run([sys.executable, str(LAUNCHER), *arguments], capture_output=True, env=environment)

def flat_of(verb: str) -> str:
    return 'content_' + verb.replace('-', '_')

class FlatContentCalls(unittest.TestCase):
    EVERY_VERB = ('backlinks', 'check', 'edit', 'find', 'get-act-context', 'get-meta', 'get-section', 'hour-id', 'list-ai-only-changelog-records', 'list-undischarged-propagations', 'meta', 'path', 'questions', 'resolve-path', 'search', 'section', 'write')

    def test_every_flat_call_has_help(self) -> None:
        for verb in self.EVERY_VERB:
            call = flat_of(verb)
            with self.subTest(call=call):
                asked = run_memar(call, '--help')
                self.assertEqual(asked.returncode, 0, asked.stderr)
                shown = asked.stdout.decode('utf-8', 'replace')
                self.assertIn(f'usage: memar {call}', shown)

    def test_grouped_spellings_are_refused(self) -> None:
        for verb in self.EVERY_VERB:
            with self.subTest(verb=verb):
                completed = run_memar('content', verb, '--help')
                self.assertNotEqual(completed.returncode, 0, verb)
                err = completed.stderr.decode('utf-8', 'replace')
                self.assertIn('invalid choice', err, verb)

    def test_content_is_not_a_public_group(self) -> None:
        asked = run_memar('content', '--help')
        self.assertNotEqual(asked.returncode, 0, asked.stderr)
        self.assertIn('invalid choice', asked.stderr.decode('utf-8', 'replace'))

    def test_content_search_is_a_verb_of_memar(self) -> None:
        asked = run_memar('--help')
        self.assertEqual(asked.returncode, 0, asked.stderr)
        shown = asked.stdout.decode('utf-8', 'replace')
        self.assertIn('content_search', ' '.join(shown.split()))

class RootVerbIsNotHere(unittest.TestCase):

    def test_no_verb_of_this_domain_answers_where_memar_lives(self) -> None:
        completed = run_memar('content_root', '--help')
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn('invalid choice', completed.stderr.decode('utf-8', 'replace'))
        self.assertFalse((SCRIPTS.parent.parent / 'modules' / 'knowledge' / 'content' / 'services' / 'root.py').exists())
if __name__ == '__main__':
    unittest.main(verbosity=2)
