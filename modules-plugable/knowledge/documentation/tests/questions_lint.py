#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
from importlib import import_module
import sys
import unittest
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = next(p for p in TESTS.parents if p.name == 'modules-plugable').parent / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
BUDGET_SECONDS = 10
lint = import_module('modules-plugable.knowledge.documentation.services.questions_lint')
Content = import_module('modules.management.timeline.services.timeline_files').Content


def question(body: str, kind: str = 'question') -> Content:
    return Content(1, {'kind': kind}, body)


class QuestionWarnings(unittest.TestCase):

    def test_a_complete_question_is_clean(self) -> None:
        self.assertEqual(lint.question_warnings(question('### Whole?\n- State: x\n- Options: a, b\n- Anchor: f.md:1\n- Blocks: nothing\n- Asked: 2026-10-13, Claude\n')), [])

    def test_missing_fields_are_named_in_the_catalog_order(self) -> None:
        self.assertEqual(lint.question_warnings(question('### Q?\n- State: x\n- Blocks: no\n')), ['question lacks Options, Anchor'])

    def test_a_bare_question_lacks_all_four(self) -> None:
        self.assertEqual(lint.question_warnings(question('### Q?\nJust a paragraph.\n')), ['question lacks State, Options, Anchor, Blocks'])

    def test_bold_markers_and_a_colon_inside_the_bold_count(self) -> None:
        body = '### Q?\n- **State**: x\n- **Options:** a\n- **Anchor**: y\n- **Blocks:** no\n'
        self.assertEqual(lint.question_warnings(question(body)), [])

    def test_the_older_blocks_continuation_counts_as_blocks(self) -> None:
        body = '### Q?\n- State: x\n- Options: a\n- Anchor: y\n- Blocks continuation: no\n'
        self.assertEqual(lint.question_warnings(question(body)), [])

    def test_a_field_inside_a_code_fence_does_not_count(self) -> None:
        body = '### Q?\n- State: x\n- Options: a\n- Anchor: y\n```\n- Blocks: no\n```\n'
        self.assertEqual(lint.question_warnings(question(body)), ['question lacks Blocks'])

    def test_a_content_of_another_kind_gives_nothing(self) -> None:
        self.assertEqual(lint.question_warnings(question('### D\nbare\n', kind='decision')), [])


if __name__ == '__main__':
    unittest.main(verbosity=2)
