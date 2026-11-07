#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
from importlib import import_module
import sys
import unittest
sys.dont_write_bytecode = True
open_questions = import_module('modules-plugable.knowledge.documentation.services.open_questions')
_m_markdown = import_module('modules-plugable.computer.codec.markdown.services.markdown')
BUDGET_SECONDS = 10


def problems(text: str) -> list[str]:
    return open_questions.open_questions_problems(_m_markdown.without_code(text))


class OpenQuestionsSection(unittest.TestCase):

    def test_each_heading_of_questions_held_beside_a_document_is_a_problem(self) -> None:
        for heading in ('## Open Questions', '### open questions', '# OPEN QUESTIONS', '## Unresolved questions', '#### Review Questions', '## Open questions:', '## Open questions (from the Estate session, 2026-08-05)', '# Open questions (from the rights proposal)', '## Open question for the owner', '### Questions for the owner', '## 3. Open Questions', '## **Open questions**'):
            with self.subTest(heading=heading):
                found = problems(f'# T\nBody.\n{heading}\n- Q?\n')
                self.assertEqual(len(found), 1, found)
                self.assertIn('line 3', found[0])

    def test_the_problem_names_the_rule_and_where_it_is_stated(self) -> None:
        found = problems('# T\n## Open Questions\n- Q?\n')
        self.assertIn('no-record-beside-a-document.md', found[0])
        self.assertIn('question', found[0])

    def test_other_headings_and_prose_are_not_judged(self) -> None:
        for text in ('# T\n## Questions\n', '# T\n## Open questions of the owner and their answers\n', '# T\nNo document has an Open Questions section.\n', '# T\n```\n## Open Questions\n```\n'):
            with self.subTest(text=text):
                self.assertEqual(problems(text), [])


if __name__ == '__main__':
    unittest.main(verbosity=2)
