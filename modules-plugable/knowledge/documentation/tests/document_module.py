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
document_module = import_module('modules-plugable.knowledge.documentation.services.document_module')
BUDGET_SECONDS = 20


class ModuleTree(unittest.TestCase):

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=_m_test_scratch.suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        self.cache: dict = {}

    def write(self, relative: str, text: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8', newline='\n')
        return path


class ModuleOf(ModuleTree):

    def setUp(self) -> None:
        super().setUp()
        self.write('modules/a/a.md', '# A\n')
        self.write('modules/a/b/b.md', '# B\n')
        self.write('modules/a/rules/r/r.md', '# R\n')
        self.write('modules/a/protocol/a.kh', 'tp A ab {\n}\n')
        self.write('docs/x.md', '# X\n')

    def module(self, relative: str) -> Path | None:
        return document_module.module_of(self.root / relative, self.root, self.cache)

    def test_a_main_document_is_its_folders_module(self) -> None:
        self.assertEqual(self.module('modules/a/a.md'), self.root / 'modules/a')

    def test_a_rule_belongs_to_the_module_holding_the_rules_folder(self) -> None:
        self.assertEqual(self.module('modules/a/rules/r/r.md'), self.root / 'modules/a')

    def test_a_khayyam_file_belongs_to_the_module_above_its_folder(self) -> None:
        self.assertEqual(self.module('modules/a/protocol/a.kh'), self.root / 'modules/a')

    def test_a_nested_module_is_its_own(self) -> None:
        self.assertEqual(self.module('modules/a/b/b.md'), self.root / 'modules/a/b')

    def test_a_base_document_has_no_module(self) -> None:
        self.assertIsNone(self.module('docs/x.md'))


class DeclaredNamesAndImports(ModuleTree):

    def setUp(self) -> None:
        super().setUp()
        self.write('modules/a/a.md', '# A\n')
        self.write('modules/a/protocol/a.kh', 'tp Text in "modules/c/protocol/c.kh"\ntp Thing ab {\n\tDetails\n\tsize W32\n}\n// tp Ghost ab {\n/*\ntp Phantom ab {\n\tspectre\n}\n*/\n\ntp GetName mt (self Thing) (at W32) (name Text)\n')
        self.write('modules/a/b/b.md', '# B\n')
        self.write('modules/a/b/protocol/b.kh', 'tp Hidden ab {\n}\n')
        self.write('modules/c/c.md', '# C\n')
        self.write('modules/c/protocol/c.kh', 'tp Text ab {\n}\n')
        self.write('modules/d/d.md', '# D\n')

    def test_names_are_the_types_methods_members_and_parameters(self) -> None:
        names = document_module.declared_names(self.root / 'modules/a', self.root, self.cache)
        for name in ('thing', 'getname', 'details', 'size', 'at', 'name'):
            with self.subTest(name=name):
                self.assertIn(name, names)

    def test_an_import_alias_and_self_are_not_names(self) -> None:
        names = document_module.declared_names(self.root / 'modules/a', self.root, self.cache)
        self.assertNotIn('text', names)
        self.assertNotIn('self', names)

    def test_a_commented_declaration_is_not_a_name(self) -> None:
        names = document_module.declared_names(self.root / 'modules/a', self.root, self.cache)
        for name in ('ghost', 'phantom', 'spectre'):
            with self.subTest(name=name):
                self.assertNotIn(name, names)

    def test_a_nested_modules_files_are_its_own(self) -> None:
        names = document_module.declared_names(self.root / 'modules/a', self.root, self.cache)
        self.assertNotIn('hidden', names)

    def test_imports_name_the_modules_of_the_imported_files(self) -> None:
        self.assertEqual(document_module.imported_modules(self.root / 'modules/a', self.root, self.cache), {self.root / 'modules/c'})

    def test_a_module_without_khayyam_has_no_known_imports(self) -> None:
        self.assertIsNone(document_module.imported_modules(self.root / 'modules/d', self.root, self.cache))


if __name__ == '__main__':
    unittest.main(verbosity=2)
