#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for `memar content find` and the index it ranks, in `modules/knowledge/text/services/content_find.py` and `modules/knowledge/text/services/index.py`.

    python modules/knowledge/text/tests/content_find.py

The subject is the retrieval of proposal v3, sections 10.1 to 10.4: sections of the checkout's
content ranked by word similarity to a query, for what no normative-references list reaches.
Named for the file that holds it per
[Test Naming](../../../process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../process/test/rules/test-placement/test-placement.md).

Pinned on small documents of the suite's own in a scratch checkout, so no pin depends on what the
real documents say; on the real tree only that the command answers and that its output is
informative. The ranking's constants are not pinned to a value: the proposal's probe supports none
better, so a test that fixed one would fix a judgment as a fact. What is pinned is what a reader
relies on.

What is pinned, and what each pin is for:

  Units      A Markdown section runs from its heading to the next heading of any level; the text
             before the first heading is a unit of its own; a `#` inside a fenced block opens no
             section; a `.kh` file is one unit; a repeated heading gets the anchor the anchor
             check gives it.
  Ranking    A section whose heading holds the query's words ranks above one that mentions them
             once in its body; a query with no word in the corpus gives nothing; stop words
             decide nothing; at most two sections of one document are ranked.
  Links      A section a hit links by anchor is printed under it, once, marked as linked; with
             `--no-links` none is; a linked section that is itself a hit is not printed twice.
  Output     The first line says the output is informative and where the normative references of
             an act are printed; a hit is one line: root, path and anchor, heading, the first
             sentence cut at 160 characters with links reduced to their text, and the hash of the
             section as `memar content get-section --hash` prints it; a `.kh` hit is marked.
  Command    `memar content find` answers on the real tree, takes `--top`, `--no-links` and a
             project, and refuses a folder that is no checkout.
  Index      The index is built in memory on each call and keeps nothing between calls; its
             docstring carries the TODO for the Memar server.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
from machine.plugable_import import load as plugable_load
_m_fs_test_scratch = plugable_load('computer.memory.filesystem.services.fs_test_scratch')
suite_scratch = _m_fs_test_scratch.suite_scratch
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = next(p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()) / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
from modules.knowledge.text.services.content_find import INFORMATIVE, find_lines
from modules.knowledge.text.services.index import build
_m_content_section = plugable_load('computer.codec.markdown.services.content_section')
by_anchor = _m_content_section.by_anchor
section_hash = _m_content_section.section_hash
ROOT = SCRIPTS.parent.parent
LAUNCHER = SCRIPTS / 'memar'
LONG = 'Word ' * 80
DOCS = {'docs/alpha.md': 'Before any heading, the preamble speaks of lanterns.\n\n# Alpha\n\nAlpha intro.\n\n## Harbor Tides\n\nHarbor tides are read before sailing. See [the beacon](beta.md#beacon) for signals.\n\n### Deep Tide Tables\n\nTide tables, kept by the harbor master.\n\n## Other\n\nOne passing mention of harbor.\n\n```\n# Not A Heading\n```\n\n## Other\n\nSecond other.\n', 'docs/beta.md': '# Beta\n\n## Beacon\n\nThe beacon is lit at dusk. See [Harbor Tides](alpha.md#harbor-tides).\n\n## Fog Horn\n\nThe horn sounds in fog.\n', 'docs/crowd.md': '# Crowd\n\n## Gull One\n\ngull gull gull\n\n## Gull Two\n\ngull gull\n\n## Gull Three\n\ngull\n', 'docs/long.md': f'# Long\n\n## Wordy\n\nThe [first link](beta.md#beacon) sentence is {LONG}and ends here. Next sentence.\n', 'docs/gamma.md': '# Gamma\n\n## Misc\n\nA passing mention of harbor, once.\n', 'docs/model.kh': 'declaration of a lighthouse keeper\n'}

class Fixture(unittest.TestCase):

    def setUp(self) -> None:
        scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(scratch.cleanup)
        self.root = Path(scratch.name).resolve() / 'orchard'
        for name, text in DOCS.items():
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding='utf-8', newline='\n')

    def lines(self, query: str, **given) -> list[str]:
        return find_lines(self.root, query, **given)

    def hits(self, query: str, **given) -> list[str]:
        """The unindented hit lines, each reduced to its `path#anchor`."""
        return [line.split(' | ')[0].split(':', 1)[1] for line in self.lines(query, **given)[1:] if not line.startswith(' ')]

class Units(Fixture):

    def test_a_section_runs_to_the_next_heading_of_any_level_and_the_preamble_is_a_unit(self) -> None:
        index = build(self.root)
        found = {(unit.path, unit.anchor): unit for unit in index.units}
        alpha = (self.root / 'docs/alpha.md').read_text(encoding='utf-8')
        tides = found['docs/alpha.md', 'harbor-tides']
        self.assertIn('Harbor tides are read', alpha[tides.start:tides.end])
        self.assertNotIn('Tide tables', alpha[tides.start:tides.end])
        self.assertIn(('docs/alpha.md', ''), found)
        self.assertIn('lanterns', alpha[found['docs/alpha.md', ''].start:found['docs/alpha.md', ''].end])

    def test_a_hash_in_a_fenced_block_opens_no_section_and_a_repeated_heading_is_suffixed(self) -> None:
        anchors = [unit.anchor for unit in build(self.root).units if unit.path == 'docs/alpha.md']
        self.assertNotIn('not-a-heading', anchors)
        self.assertEqual(anchors.count('other'), 1)
        self.assertIn('other-1', anchors)

    def test_a_kh_file_is_one_unit(self) -> None:
        unit, = [unit for unit in build(self.root).units if unit.path == 'docs/model.kh']
        self.assertTrue(unit.kh)
        self.assertEqual(unit.anchor, '')

class Ranking(Fixture):

    def test_a_heading_that_holds_the_words_ranks_above_one_body_mention(self) -> None:
        found = self.hits('harbor')
        self.assertLess(found.index('docs/alpha.md#harbor-tides'), found.index('docs/gamma.md#misc'))

    def test_a_query_with_no_word_in_the_corpus_gives_nothing(self) -> None:
        self.assertEqual(self.hits('zeppelin'), [])

    def test_stop_words_decide_nothing(self) -> None:
        self.assertEqual(self.hits('the of and'), [])

    def test_at_most_two_sections_of_one_document_are_ranked(self) -> None:
        self.assertEqual(len([hit for hit in self.hits('gull') if hit.startswith('docs/crowd.md')]), 2)

    def test_a_kh_file_is_ranked_and_marked(self) -> None:
        line, = [each for each in self.lines('lighthouse keeper') if 'docs/model.kh' in each]
        self.assertIn('(kh)', line)

class Links(Fixture):

    def test_a_section_a_hit_links_is_printed_under_it_once_marked_as_linked(self) -> None:
        lines = self.lines('tides', top=1)
        at = next((number for number, line in enumerate(lines) if 'docs/alpha.md#harbor-tides' in line))
        self.assertTrue(lines[at + 1].startswith('    linked from above: orchard'), lines)
        self.assertIn('docs/beta.md#beacon', lines[at + 1])
        self.assertEqual(sum(('docs/beta.md#beacon' in line for line in lines)), 1)

    def test_no_links_prints_none(self) -> None:
        lines = self.lines('tides', top=1, links=False)
        self.assertFalse(any((line.startswith(' ') for line in lines)), lines)

    def test_a_linked_section_that_is_a_hit_is_not_printed_twice(self) -> None:
        lines = self.lines('tides beacon dusk', top=5)
        self.assertEqual(sum(('docs/beta.md#beacon' in line for line in lines)), 1)

class Output(Fixture):

    def test_the_first_line_says_it_is_informative_and_where_the_references_are(self) -> None:
        first = self.lines('harbor')[0]
        self.assertEqual(first, INFORMATIVE)
        self.assertTrue(first.startswith('informative: ranked by word similarity; the normative references of an act are printed by `memar content get-act-context`'))

    def test_a_hit_is_root_path_anchor_heading_first_sentence_and_the_sections_hash(self) -> None:
        line, = [each for each in self.lines('fog horn', top=1) if '#fog-horn' in each]
        root, heading, sentence, mark = line.split(' | ')
        self.assertEqual(root, 'orchard:docs/beta.md#fog-horn')
        self.assertEqual(heading, 'Fog Horn')
        self.assertEqual(sentence, 'The horn sounds in fog.')
        text = (self.root / 'docs/beta.md').read_text(encoding='utf-8')
        self.assertEqual(mark, section_hash(by_anchor(text, 'fog-horn')))

    def test_the_sentence_has_its_links_reduced_to_their_text_and_is_cut_at_160(self) -> None:
        line, = [each for each in self.lines('wordy', top=1) if '#wordy' in each and (not each.startswith(' '))]
        sentence = line.split(' | ')[2]
        self.assertTrue(sentence.startswith('The first link sentence is Word'), sentence)
        self.assertNotIn('](', sentence)
        self.assertLessEqual(len(sentence), 160)
        self.assertTrue(sentence.endswith('…'))

class Command(unittest.TestCase):

    def run_memar(self, *arguments: str) -> subprocess.CompletedProcess:
        environment = dict(os.environ, COLUMNS='100', PYTHONIOENCODING='utf-8', MEMAR_NO_AUTO_UPDATE='1')
        return subprocess.run([sys.executable, str(LAUNCHER), 'content', 'find', *arguments], capture_output=True, env=environment)

    def test_it_answers_on_the_real_tree_informatively_and_takes_top(self) -> None:
        done = self.run_memar('normative references', '--top', '3', '--no-links')
        self.assertEqual(done.returncode, 0, done.stderr)
        lines = done.stdout.decode('utf-8').splitlines()
        self.assertEqual(lines[0], INFORMATIVE)
        self.assertEqual(len(lines) - 1, 3)
        self.assertTrue(all((line.startswith('memar:') for line in lines[1:])), lines)

    def test_a_named_project_is_the_corpus(self) -> None:
        with tempfile.TemporaryDirectory(dir=suite_scratch()) as folder:
            (Path(folder) / 'docs').mkdir()
            (Path(folder) / 'docs' / 'own.md').write_text('# Own\n\n## Orchard Rows\n\nPears.\n', encoding='utf-8', newline='\n')
            done = self.run_memar('orchard rows', '--project-path', folder)
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertIn(':docs/own.md#orchard-rows | Orchard Rows | Pears. | ', done.stdout.decode('utf-8'))

    def test_a_folder_that_is_no_checkout_is_refused(self) -> None:
        with tempfile.TemporaryDirectory(dir=suite_scratch()) as folder:
            done = self.run_memar('anything', '--project-path', folder)
        self.assertNotEqual(done.returncode, 0)

class Index(unittest.TestCase):

    def test_the_index_is_built_in_memory_and_its_docstring_carries_the_todo(self) -> None:
        text = (SCRIPTS.parent.parent / 'modules' / 'knowledge' / 'text' / 'services' / 'index.py').read_text(encoding='utf-8')
        self.assertIn('TODO(when the Memar server exists)', text)
        self.assertIn('20261016-T135247Z-15464', text)
        self.assertNotIn('pickle', text)
if __name__ == '__main__':
    unittest.main(verbosity=2)
