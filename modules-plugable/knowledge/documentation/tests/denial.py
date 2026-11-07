#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
from importlib import import_module
import sys
import unittest
from pathlib import Path
sys.dont_write_bytecode = True
denial = import_module('modules-plugable.knowledge.documentation.services.denial')
_m_markdown = import_module('modules-plugable.computer.codec.markdown.services.markdown')
BUDGET_SECONDS = 10


def findings(text: str) -> tuple[list[str], list[str]]:
    return denial.denial_findings(_m_markdown.without_code(text))


class DenialToName(unittest.TestCase):

    def test_a_sentence_whose_subject_holds_or_knows_nothing_is_a_problem(self) -> None:
        for sentence in ('A group holds no Topics or Status.', 'This module knows no file concept.', 'Task does not hold a title.', 'The store does not know the task.', 'Each record holds nothing of the plan.'):
            with self.subTest(sentence=sentence):
                problems, hints = findings(f'# T\nFirst line.\n{sentence}\n')
                self.assertEqual(len(problems), 1, problems)
                self.assertIn('line 3', problems[0])
                self.assertEqual(hints, [])

    def test_a_denying_sentence_after_another_in_a_line_or_a_list_item_is_judged(self) -> None:
        problems, _ = findings('# T\n- **A rule.** A group holds no Topics.\n')
        self.assertEqual(len(problems), 1, problems)

    def test_a_denying_heading_is_a_problem(self) -> None:
        for heading in ('## What a Group does not hold', '### The store knows no task', '## Content Knows No Module'):
            with self.subTest(heading=heading):
                problems, _ = findings(f'# T\n{heading}\nBody.\n')
                self.assertEqual(len(problems), 1, problems)

    def test_a_weaker_denial_in_a_heading_is_a_hint(self) -> None:
        for heading in ('## Group is not a queue', '## The Store Has No Index'):
            with self.subTest(heading=heading):
                problems, hints = findings(f'# T\n{heading}\nBody.\n')
                self.assertEqual(problems, [])
                self.assertEqual(len(hints), 1, hints)
                self.assertIn('line 2', hints[0])

    def test_a_heading_whose_denial_is_not_its_subjects_predicate_is_not_judged(self) -> None:
        for heading in ('## When a Module Has No Khayyam', '## A task that holds no plan', '## Why the Store Is Not a Queue'):
            with self.subTest(heading=heading):
                self.assertEqual(findings(f'# T\n{heading}\nBody.\n'), ([], []))

    def test_in_a_rule_document_a_denial_is_only_a_hint(self) -> None:
        text = _m_markdown.without_code('# T\n## The store knows no task\nA group holds no Topics.\n')
        problems, hints = denial.denial_findings(text, Path('modules/a/rules/r/r.md'))
        self.assertEqual(problems, [])
        self.assertEqual(len(hints), 2, hints)

    def test_the_problem_names_the_rule_and_where_it_is_stated(self) -> None:
        problems, _ = findings('# T\nA group holds no Topics.\n')
        self.assertIn('documentation.md#written-surface', problems[0])

    def test_a_weaker_denial_is_a_hint_and_not_a_problem(self) -> None:
        for sentence in ('A plan is not a schedule.', 'The store has no index.', 'A plan does not have a date.', 'The module owns no file.'):
            with self.subTest(sentence=sentence):
                problems, hints = findings(f'# T\n{sentence}\n')
                self.assertEqual(problems, [])
                self.assertEqual(len(hints), 1, hints)
                self.assertIn('line 2', hints[0])

    def test_a_denial_that_is_not_the_sentences_own_predicate_is_not_judged(self) -> None:
        for text in ('It applies when a task holds no plan.', 'A module with no errors has no `errors` folder.', 'Nor does a body deny to name it: "a group holds no Topics or Status".', 'A rule is stated once.', '```\nA group holds no Topics.\n```', 'Use `A group holds no Topics.` as the example.'):
            with self.subTest(text=text):
                self.assertEqual(findings(f'# T\n{text}\n'), ([], []))

    def test_a_closure_or_a_phrasal_verb_is_not_judged(self) -> None:
        for text in ('The file holds nothing else.', 'A folder holds no other file.', 'A registry inquiry does not hold this edge back.'):
            with self.subTest(text=text):
                self.assertEqual(findings(f'# T\n{text}\n'), ([], []))

    def test_front_matter_is_not_judged(self) -> None:
        self.assertEqual(findings('---\nTitle: "A group holds no Topics."\n---\n# T\n'), ([], []))
        self.assertEqual(findings('---\nTitle: x\nNote: >\n  A group holds no Topics.\n---\n# T\n'), ([], []))


if __name__ == '__main__':
    unittest.main(verbosity=2)
