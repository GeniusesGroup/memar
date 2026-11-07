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
restated_fields = import_module('modules-plugable.knowledge.documentation.services.restated_fields')
BUDGET_SECONDS = 20
KHAYYAM = 'tp Text in "modules/c/protocol/c.kh"\ntp Thing ab {\n\tDetails\n}\n\ntp GetName mt (self Thing) () (name Text)\n\ntp GetSize mt (self Thing) () (size Text)\n\ntp GetColor mt (self Thing) () (color Text)\n'


class RestatedFields(unittest.TestCase):

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=_m_test_scratch.suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        self.cache: dict = {}
        self.write('modules/a/protocol/a.kh', KHAYYAM)
        self.write('modules/a/a.md', '# A\n')
        self.write('modules/b/b.md', '# B\n')

    def write(self, relative: str, text: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8', newline='\n')
        return path

    def problems(self, path: Path) -> list[str]:
        return restated_fields.restated_field_problems(path, path.read_text(encoding='utf-8'), self.cache, self.root)

    def test_a_table_whose_first_column_names_three_declared_members_is_a_problem(self) -> None:
        path = self.write('modules/a/a.md', '# A\nIntro.\n\n| Method | Meaning |\n|---|---|\n| `GetName` | its name |\n| GetSize | its size |\n| getcolor() | its color |\n')
        found = self.problems(path)
        self.assertEqual(len(found), 1, found)
        self.assertIn('line 4', found[0])
        self.assertIn('protocol/a.kh', found[0])
        self.assertIn('document-restates-no-code.md', found[0])

    def test_a_first_cell_that_links_a_declared_name_counts_as_that_name(self) -> None:
        path = self.write('modules/a/a.md', '# A\n| Method | Meaning |\n|---|---|\n| [GetName](./protocol/a.kh) | x |\n| [`GetSize`](./protocol/a.kh#L8) | y |\n| [getcolor()](./protocol/a.kh) | z |\n')
        self.assertEqual(len(self.problems(path)), 1)

    def test_parameter_names_count_as_declared(self) -> None:
        path = self.write('modules/a/rules/r/r.md', '# R\n| Field | Meaning |\n|---|---|\n| name | x |\n| size | y |\n| color | z |\n')
        self.assertEqual(len(self.problems(path)), 1)

    def test_two_declared_names_are_not_enough(self) -> None:
        path = self.write('modules/a/a.md', '# A\n| Method | Meaning |\n|---|---|\n| GetName | x |\n| GetSize | y |\n| Other | z |\n')
        self.assertEqual(self.problems(path), [])

    def test_the_header_row_is_not_counted(self) -> None:
        path = self.write('modules/a/a.md', '# A\n| GetName | GetSize |\n|---|---|\n| GetColor | x |\n| Other | y |\n')
        self.assertEqual(self.problems(path), [])

    def test_another_modules_table_is_not_judged_by_these_names(self) -> None:
        path = self.write('modules/b/b.md', '# B\n| Method | Meaning |\n|---|---|\n| GetName | x |\n| GetSize | y |\n| GetColor | z |\n')
        self.assertEqual(self.problems(path), [])

    def test_a_table_in_a_fenced_block_is_not_judged(self) -> None:
        path = self.write('modules/a/a.md', '# A\n```\n| Method | Meaning |\n|---|---|\n| GetName | x |\n| GetSize | y |\n| GetColor | z |\n```\n')
        self.assertEqual(self.problems(path), [])

    def test_a_document_outside_every_module_is_not_judged(self) -> None:
        path = self.write('docs/x.md', '# X\n| Method | Meaning |\n|---|---|\n| GetName | x |\n| GetSize | y |\n| GetColor | z |\n')
        self.assertEqual(self.problems(path), [])


if __name__ == '__main__':
    unittest.main(verbosity=2)
