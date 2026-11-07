#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
from importlib import import_module
import sys
import tempfile
import unittest
from pathlib import Path
_m_test_scratch = import_module('modules.process.test.services.test_scratch')
sys.dont_write_bytecode = True
foreign_domain = import_module('modules-plugable.knowledge.documentation.services.foreign_domain')
_m_markdown = import_module('modules-plugable.computer.codec.markdown.services.markdown')
BUDGET_SECONDS = 20


class ForeignDomain(unittest.TestCase):

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=_m_test_scratch.suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        self.cache: dict = {}
        self.write('modules/a/a.md', '# A\n')
        self.write('modules/a/protocol/a.kh', 'tp B in "modules/b/protocol/b.kh"\ntp A ab {\n\tB\n}\n')
        self.write('modules/a/sub/sub.md', '# Sub\n')
        self.write('modules/b/b.md', '# B\n')
        self.write('modules/b/protocol/b.kh', 'tp B ab {\n}\n')
        self.write('modules/b/child/child.md', '# Child\n')
        self.write('modules/c/c.md', '# C\n')
        self.write('modules/c/README.md', '# C\n')
        self.write('modules/c/protocol/c.kh', 'tp C ab {\n}\n')
        self.write('modules/c/rules/r/r.md', '# R\n')
        self.write('modules/c/inner/inner.md', '# Inner\n')
        self.write('modules/c/inner/protocol/inner.kh', 'tp Inner ab {\n}\n')
        self.write('modules/d/d.md', '# D\n')
        self.write('modules/e/e.md', '# E\n')
        self.write('modules/e/protocol/e.kh', 'tp Inner in "modules/c/inner/protocol/inner.kh"\ntp E ab {\n\tInner\n}\n')
        self.write('bundles/f/f.md', '# F\n')
        self.write('docs/x.md', '# X\n')

    def write(self, relative: str, text: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8', newline='\n')
        return path

    def hints(self, relative: str, body: str) -> list[str]:
        path = self.write(relative, f'# T\n{body}\n')
        return foreign_domain.foreign_domain_hints(path, _m_markdown.without_code(path.read_text(encoding='utf-8')), self.cache, self.root)

    def test_a_link_to_the_concept_of_a_module_not_imported_is_a_hint(self) -> None:
        for relative, link in (('modules/a/a.md', '../c/c.md'), ('modules/a/a.md', '/modules/c/c.md#c'), ('modules/a/a.md', '../c/README.md'), ('modules/a/a.md', '../c/'), ('modules/a/a.md', '../c'), ('modules/a/rules/r/r.md', '../../../c/c.md')):
            with self.subTest(relative=relative, link=link):
                found = self.hints(relative, f'See [C]({link}).')
                self.assertEqual(len(found), 1, found)
                self.assertIn('line 2', found[0])
                self.assertIn('modules/c', found[0])
                self.assertIn('document-names-only-its-own-domain.md', found[0])

    def test_a_link_to_an_imported_module_or_a_relative_is_not_judged(self) -> None:
        for relative, link in (('modules/a/a.md', '../b/b.md'), ('modules/a/a.md', '../b/'), ('modules/a/a.md', './sub/sub.md'), ('modules/a/sub/sub.md', '../a.md'), ('modules/a/a.md', '../../docs/x.md'), ('modules/a/a.md', '../c/rules/r/r.md'), ('modules/a/a.md', '#a'), ('modules/a/a.md', 'https://example.com/c.md')):
            with self.subTest(relative=relative, link=link):
                self.assertEqual(self.hints(relative, f'See [X]({link}).'), [])

    def test_importing_a_sub_module_permits_naming_its_parent(self) -> None:
        self.assertEqual(self.hints('modules/e/e.md', 'See [C](../c/c.md).'), [])

    def test_naming_a_child_of_an_imported_module_is_a_hint(self) -> None:
        found = self.hints('modules/a/a.md', 'See [Child](../b/child/child.md).')
        self.assertEqual(len(found), 1, found)
        self.assertIn('modules/b/child', found[0])

    def test_a_module_whose_imports_cannot_be_read_gets_a_hint(self) -> None:
        found = self.hints('modules/d/d.md', 'See [C](../c/c.md).')
        self.assertEqual(len(found), 1, found)
        self.assertIn('modules/c', found[0])

    def test_a_document_outside_every_module_is_not_judged(self) -> None:
        self.assertEqual(self.hints('docs/y.md', 'See [C](../modules/c/c.md).'), [])

    def test_a_bundle_is_not_judged(self) -> None:
        self.assertEqual(self.hints('bundles/f/f.md', 'See [C](../../modules/c/c.md).'), [])

    def test_a_widget_document_is_not_judged(self) -> None:
        self.assertEqual(self.hints('modules/a/widgets/w/w.md', 'See [C](../../../c/c.md).'), [])

    def test_a_link_in_code_is_not_judged(self) -> None:
        self.assertEqual(self.hints('modules/a/a.md', 'See `[C](../c/c.md)`.'), [])


if __name__ == '__main__':
    unittest.main(verbosity=2)
