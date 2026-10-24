#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for `memar content backlinks` in `modules-plugable/computer/codec/markdown/services/content_backlinks.py`.

    python modules-plugable/computer/codec/markdown/tests/content_backlinks.py

The subject is which documents link to a file, named for the file that holds it
per [Test Naming](../../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes outside its scratch folder: every document is written into
one, made under the folder `modules-plugable/computer/filesystem/services/fs_test_scratch.py` names, and removed
again, and no test reads the repository's own `docs/`.

What is pinned, and what each pin is for:

  BacklinksAreResolvedPaths  `backlinks` answers which documents link here,
                             and nothing else; the class says pin by pin why.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
from importlib import import_module
from machine.plugable_import import load as plugable_load
_m_fs_test_scratch = plugable_load('computer.filesystem.services.fs_test_scratch')
suite_scratch = _m_fs_test_scratch.suite_scratch
import contextlib
import io
import sys
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parents[3] / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
content_backlinks = import_module('modules-plugable.computer.codec.markdown.services.content_backlinks')

class BacklinksAreResolvedPaths(unittest.TestCase):
    """`backlinks` answers which documents link here, and nothing else.

    A mention without a link is not a backlink; a link inside code is text
    about links; a link naming a file that is not there matches nothing; and
    the target's own self-links are not incoming links. What is pinned, and
    what each pin is for:

      LinkerListed        A document linking here is reported with its line
                        and fragment — the whole point, which is letting an
                        agent changing a document see who depends on it.
      SelfIsNotIncoming  The target's own in-page links are navigation, not
                        dependence; counting them would report every
                        sectioned document as its own dependent.
      MentionIsNotALink  Prose naming a filename is not a reference an agent
                        can follow, so it must not appear in the answer.
      MissingSpelling   A link whose spelling names no file matches nothing
                        rather than matching nearly — the near-miss is a
                        `check` finding, not a backlink.
      CodeIsNotALink    The same text in backticks or a fenced block is
                        quoted, not linked.
      LonelyReportsNone A document nothing links to reports just that, so
                        the verb stays an answer rather than an empty run.
      RootRelativeCounts A link written from the checkout's root
                        (`/docs/...`), the form the Memar skill writes every
                        link in, resolves as `memar content resolve-path` resolves it,
                        against the checkout, and is a backlink like any other.
      PerAnchor         `FILE#anchor` keeps only the links whose fragment is
                        that anchor, so the dependents of one section are
                        seen apart from the document's; an anchor no heading
                        answers to is said to be one, not just left empty.
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

    def make_tree(self) -> Path:
        self.write('docs/target.md', '# Target\n## Part\n')
        self.write('docs/a.md', '# A\nSee [T](./target.md#part).\n')
        self.write('docs/b.md', '# B\nSee [T](./target.md).\n')
        self.write('docs/unrelated.md', '# U\nNo links here.\n')
        return self.root / 'docs' / 'target.md'

    def docs(self) -> list[Path]:
        return sorted((self.root / 'docs').glob('*.md'))

    def test_linkers_are_listed_with_line_and_fragment(self) -> None:
        target = self.make_tree()
        found = content_backlinks.find_backlinks(target, self.docs(), self.root, None)
        self.assertEqual(found, [(self.root / 'docs' / 'a.md', 2, 'part'), (self.root / 'docs' / 'b.md', 2, '')])

    def test_self_links_are_not_incoming(self) -> None:
        target = self.make_tree()
        self.write('docs/target.md', '# Target\n## Part\nSee [P](#part).\n')
        found = content_backlinks.find_backlinks(target, self.docs(), self.root, None)
        self.assertEqual(len(found), 2, found)

    def test_a_mention_without_a_link_is_not_a_backlink(self) -> None:
        target = self.make_tree()
        self.write('docs/c.md', '# C\ntarget.md is discussed a lot here.\n')
        found = content_backlinks.find_backlinks(target, self.docs(), self.root, None)
        self.assertEqual(len(found), 2, found)

    def test_a_link_naming_a_missing_spelling_matches_nothing(self) -> None:
        target = self.make_tree()
        self.write('docs/c.md', '# C\nSee [T](./targte.md).\n')
        found = content_backlinks.find_backlinks(target, self.docs(), self.root, None)
        self.assertEqual(len(found), 2, found)

    def test_a_link_inside_code_is_text_about_links(self) -> None:
        target = self.make_tree()
        self.write('docs/c.md', '# C\n`[T](./target.md)`\n')
        found = content_backlinks.find_backlinks(target, self.docs(), self.root, None)
        self.assertEqual(len(found), 2, found)

    def test_nothing_linking_reports_nothing(self) -> None:
        self.make_tree()
        lonely = self.write('docs/lonely.md', '# Lonely\n')
        self.assertEqual(content_backlinks.find_backlinks(lonely, self.docs(), self.root, None), [])

    def test_cmd_prints_linker_hits_per_target(self) -> None:
        self.make_tree()
        with contextlib.redirect_stdout(io.StringIO()) as printed:
            content_backlinks.cmd_backlinks(Namespace(files=['docs/target.md']), self.root)
        out = printed.getvalue()
        self.assertIn(f"== {Path('docs/target.md')} ==", out)
        self.assertIn(f"{Path('docs/a.md')}:2#part", out)
        self.assertIn(f"{Path('docs/b.md')}:2", out)
        self.assertNotIn('unrelated', out)

    def test_a_root_relative_link_is_a_backlink(self) -> None:
        target = self.make_tree()
        self.write('docs/c.md', '# C\nSee [T](/docs/target.md#part).\n')
        self.write('modules/m/m.md', '# M\nSee [T](/docs/target.md).\n')
        docs = self.docs() + [self.root / 'modules' / 'm' / 'm.md']
        found = content_backlinks.find_backlinks(target, docs, self.root, None)
        self.assertIn((self.root / 'docs' / 'c.md', 2, 'part'), found)
        self.assertIn((self.root / 'modules' / 'm' / 'm.md', 2, ''), found)
        self.assertEqual(len(found), 4, found)

    def test_a_root_relative_link_resolves_against_the_root_given(self) -> None:
        target = self.make_tree()
        self.write('docs/c.md', '# C\nSee [T](/target.md).\n')
        found = content_backlinks.find_backlinks(target, self.docs(), self.root, None)
        self.assertEqual(len(found), 2, found)

    def test_an_anchor_keeps_only_the_links_to_that_section(self) -> None:
        target = self.make_tree()
        self.write('docs/c.md', '# C\nSee [T](/docs/target.md#part) and [T](./target.md#target).\n')
        found = content_backlinks.find_backlinks(target, self.docs(), self.root, 'part')
        self.assertEqual(found, [(self.root / 'docs' / 'a.md', 2, 'part'), (self.root / 'docs' / 'c.md', 2, 'part')])

    def test_cmd_takes_file_hash_anchor(self) -> None:
        self.make_tree()
        with contextlib.redirect_stdout(io.StringIO()) as printed:
            content_backlinks.cmd_backlinks(Namespace(files=['docs/target.md#part']), self.root)
        out = printed.getvalue()
        self.assertIn(f"== {Path('docs/target.md')}#part ==", out)
        self.assertIn(f"{Path('docs/a.md')}:2#part", out)
        self.assertNotIn(f"{Path('docs/b.md')}", out)

    def test_cmd_says_when_no_heading_answers_to_the_anchor(self) -> None:
        self.make_tree()
        with contextlib.redirect_stdout(io.StringIO()) as printed:
            content_backlinks.cmd_backlinks(Namespace(files=['docs/target.md#gone']), self.root)
        out = printed.getvalue()
        self.assertIn('(no incoming links)', out)
        self.assertIn('no heading in this file answers to #gone', out)
if __name__ == '__main__':
    unittest.main(verbosity=2)
