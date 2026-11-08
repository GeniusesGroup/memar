#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
import sys
import atexit
import shutil
import tempfile
import unittest
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = next(p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()) / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS / 'services'))
sys.path.insert(1, str(SCRIPTS))
sys.path.insert(2, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
_m = import_module('modules.process.rule.services.find_rules')
FindRules = _m.FindRules
RuleHit = _m.RuleHit

FILES = {
    'modules/a/rules/split-a-step/split-a-step.md': '# Rule — Split a step\nStatus: Draft\n\n## The rule\nA step that reads many files is split into smaller steps.\n\n## Why it exists\nA long step fills the context.\n',
    'modules/b/rules/name-a-file/name-a-file.md': '# Rule — Name a file\n\n## The rule\nA file is named for the concept it holds.\n\n## Why it exists\nA name states the subject.\n',
    'modules/c/c.md': '# Concept\n\n## About\nA step that reads many files is a concept, not a rule.\n',
    'modules/d/rules/README.md': '# Rules of d\n\nA step that reads many files.\n',
}

def _root(files: dict[str, str]) -> Path:
    root = Path(tempfile.mkdtemp(prefix='find_rules_'))
    atexit.register(shutil.rmtree, root, True)
    for name, text in files.items():
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding='utf-8', newline='\n')
    return root

class OnlyRules(unittest.TestCase):

    def test_a_hit_is_a_rule_document_and_never_another_document(self) -> None:
        root = _root(FILES)
        hits = FindRules(root).do('a step that reads many files', [], 10)
        self.assertEqual([h.document for h in hits], ['modules/a/rules/split-a-step/split-a-step.md'])

class HitShape(unittest.TestCase):

    def test_a_hit_carries_document_anchor_and_why(self) -> None:
        root = _root(FILES)
        hit = FindRules(root).do('split a step', [], 10)[0]
        self.assertIsInstance(hit, RuleHit)
        self.assertTrue(hit.anchor)
        self.assertEqual(hit.why, 'A long step fills the context.')

    def test_a_rule_without_a_why_section_has_the_first_sentence_of_its_rule(self) -> None:
        root = _root({'modules/e/rules/plain/plain.md': '# Rule — Plain\n\n## The rule\nA plain rule states one thing. And another.\n'})
        hit = FindRules(root).do('plain rule', [], 10)[0]
        self.assertEqual(hit.why, 'A plain rule states one thing.')

class Order(unittest.TestCase):

    def test_most_cuts_the_list_and_a_rule_appears_once(self) -> None:
        root = _root(FILES)
        hits = FindRules(root).do('file name step concept', [], 1)
        self.assertEqual(len(hits), 1)
        both = FindRules(root).do('file name step concept', [], 10)
        self.assertEqual(len({h.document for h in both}), len(both))

    def test_a_topic_in_the_path_ranks_its_rules_first(self) -> None:
        root = _root(FILES)
        plain = FindRules(root).do('file step', [], 10)
        topical = FindRules(root).do('file step', ['b'], 10)
        self.assertEqual(topical[0].document, 'modules/b/rules/name-a-file/name-a-file.md')
        self.assertEqual({h.document for h in plain}, {h.document for h in topical})

    def test_a_subject_no_rule_has_a_word_of_returns_nothing(self) -> None:
        root = _root(FILES)
        self.assertEqual(FindRules(root).do('zebra', [], 10), [])

if __name__ == '__main__':
    unittest.main()
