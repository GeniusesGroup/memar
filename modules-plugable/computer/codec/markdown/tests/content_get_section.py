#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for one section of a document, in `modules-plugable/computer/codec/markdown/services/content_get_section.py`, and its verb `memar content get-section`.

    python modules-plugable/computer/codec/markdown/tests/content_get_section.py

The subject is the section a name gives — the fragment a link uses, or the
heading's text — and its hash, named for the file that holds it per
[Test Naming](../../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../../modules/process/test/rules/test-placement/test-placement.md).
Only `Verb` touches the filesystem, in a temporary folder.

What is pinned, and what each pin is for:

  ByAnchor   A heading is found by its slug, the heading line is part of what
             is returned, and the section runs to the next heading at its
             level or above; a `#` inside a fenced block is no heading; an
             anchor no heading answers to is None.
  Through    With a last heading, the text runs on to the end of that
             section, so neighbouring sections are one read; a last heading
             that is not after the first is None.
  Named      A name opening with `#` is an anchor, GitHub's `-1` suffix naming
             a heading's repeat, counted as the anchor check counts it; any
             other name is a heading's text, the first heading outside a fence
             that reads so; both give the same text.
  Hash       A section's hash is the hash every part of a long text names,
             taken of the section's text; it covers the subsections, so an
             edit inside one changes it, and an edit outside the section does
             not; the line endings the file was read with do not.
  Verb       `memar content get-section FILE '#anchor'` prints the section, and
             `--hash` prints only its hash.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
from importlib import import_module
import argparse
import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parents[3] / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
from machine.console_parts import text_id
_m_content_get_section = import_module('modules-plugable.computer.codec.markdown.services.content_get_section')
by_anchor = _m_content_get_section.by_anchor
cmd_section = _m_content_get_section.cmd_section
named = _m_content_get_section.named
section_hash = _m_content_get_section.section_hash
TEXT = '# Title\n\n## Alpha Part\nalpha text\n### Inner (Detail)\ninner text\n\n## Beta Part\n```\n## not a heading\n```\nbeta text\n\n## Gamma Part\ngamma text\n'

class ByAnchor(unittest.TestCase):

    def test_a_section_is_found_by_its_slug_with_its_heading_line_and_runs_to_the_next_at_its_level(self) -> None:
        found = by_anchor(TEXT, 'alpha-part')
        self.assertTrue(found.startswith('## Alpha Part'))
        self.assertIn('inner text', found)
        self.assertNotIn('beta text', found)

    def test_a_deeper_heading_is_found_and_ends_at_the_next_heading_above_it(self) -> None:
        found = by_anchor(TEXT, 'inner-detail')
        self.assertEqual(found, '### Inner (Detail)\ninner text')

    def test_a_hash_inside_a_fenced_block_is_no_heading(self) -> None:
        found = by_anchor(TEXT, 'beta-part')
        self.assertIn('## not a heading', found)
        self.assertIn('beta text', found)
        self.assertIsNone(by_anchor(TEXT, 'not-a-heading'))

    def test_an_anchor_no_heading_answers_to_is_none(self) -> None:
        self.assertIsNone(by_anchor(TEXT, 'nowhere'))

    def test_an_anchor_may_carry_its_hash(self) -> None:
        self.assertEqual(by_anchor(TEXT, '#gamma-part'), by_anchor(TEXT, 'gamma-part'))

class Through(unittest.TestCase):

    def test_the_text_runs_on_to_the_end_of_the_last_section(self) -> None:
        found = by_anchor(TEXT, 'alpha-part', 'Beta Part')
        self.assertIn('alpha text', found)
        self.assertIn('beta text', found)
        self.assertNotIn('gamma text', found)

    def test_a_last_heading_that_is_not_after_the_first_is_none(self) -> None:
        self.assertIsNone(by_anchor(TEXT, 'gamma-part', 'Alpha Part'))
        self.assertIsNone(by_anchor(TEXT, 'alpha-part', 'No Such Heading'))
REPEATS = '# Notes\n\n## Notes\nfirst notes\n```\n## Notes\n```\n\n## Notes\nsecond notes\n'

class Named(unittest.TestCase):

    def test_a_name_opening_with_a_hash_is_an_anchor(self) -> None:
        self.assertEqual(named(TEXT, '#alpha-part'), by_anchor(TEXT, 'alpha-part'))

    def test_the_suffix_names_a_repeated_heading_counted_from_the_top_heading(self) -> None:
        self.assertEqual(named(REPEATS, '#notes-1'), '## Notes\nfirst notes\n```\n## Notes\n```')
        self.assertEqual(named(REPEATS, '#notes-2'), '## Notes\nsecond notes')

    def test_a_heading_inside_a_fence_takes_no_suffix(self) -> None:
        self.assertIsNone(named(REPEATS, '#notes-3'))

    def test_a_heading_text_gives_the_same_text_as_its_anchor(self) -> None:
        self.assertEqual(named(TEXT, 'Alpha Part'), named(TEXT, '#alpha-part'))
        self.assertEqual(named(TEXT, 'alpha part'), named(TEXT, '#alpha-part'))

    def test_a_heading_text_inside_a_fence_is_not_matched(self) -> None:
        self.assertIsNone(named(TEXT, 'not a heading'))

    def test_a_name_no_heading_answers_to_is_none(self) -> None:
        self.assertIsNone(named(TEXT, '#nowhere'))
        self.assertIsNone(named(TEXT, 'Nowhere'))

class Hash(unittest.TestCase):

    def test_the_hash_is_the_text_hash_of_the_section(self) -> None:
        self.assertEqual(section_hash(named(TEXT, '#alpha-part')), text_id(named(TEXT, '#alpha-part')))

    def test_an_edit_in_a_subsection_changes_the_hash(self) -> None:
        edited = TEXT.replace('inner text', 'inner text, edited')
        self.assertNotEqual(section_hash(named(edited, '#alpha-part')), section_hash(named(TEXT, '#alpha-part')))

    def test_an_edit_outside_the_section_leaves_the_hash(self) -> None:
        edited = TEXT.replace('beta text', 'beta text, edited')
        self.assertEqual(section_hash(named(edited, '#alpha-part')), section_hash(named(TEXT, '#alpha-part')))

    def test_line_endings_do_not_change_the_hash(self) -> None:
        crlf = TEXT.replace('\n', '\r\n')
        self.assertEqual(section_hash(named(crlf, '#alpha-part')), section_hash(named(TEXT, '#alpha-part')))

class Verb(unittest.TestCase):

    def run_verb(self, name: str, hashed: bool) -> str:
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'doc.md').write_text(TEXT, encoding='utf-8', newline='\n')
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                cmd_section(argparse.Namespace(file='/doc.md', heading=name, hash=hashed), root)
            return out.getvalue()

    def test_an_anchor_prints_the_section(self) -> None:
        self.assertEqual(self.run_verb('#inner-detail', False), '### Inner (Detail)\ninner text\n')

    def test_hash_prints_only_the_sections_hash(self) -> None:
        self.assertEqual(self.run_verb('#alpha-part', True), section_hash(named(TEXT, '#alpha-part')) + '\n')
if __name__ == '__main__':
    unittest.main(verbosity=2)
