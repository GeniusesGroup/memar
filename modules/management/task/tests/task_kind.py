#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the kinds of task, in `modules/management/task/labels/task_kind.py`.

    python modules/management/task/tests/task_kind.py

The subject is the one declaration of the kind words, named for the file that
holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).
What each kind reads is the normative-references lists', pinned in
`modules-plugable/knowledge/documentation/tests/normative_references.py` and `modules-plugable/ai/tests/task_context.py`.

Nothing here writes; the source files read are the scripts' own.

What is pinned, and what each pin is for:

  Words            The kinds, in their order, each a lower-case word with one
                   sentence on when it applies; a word is read in any case and
                   a word that is no kind is None, never a guess.
  Carried          A plan may carry every kind but `answer` and `plan`: a
                   question answered in chat opens no task, and `plan` is
                   the context a coordinating task adds to its own kind.
  NoPassages       A kind holds its word, when it applies and whether a plan
                   carries it, and no passage: the declaration names no
                   document's section, since what an act reads is the
                   normative-references lists'.
  NothingAboutWho  The declaration names no AI and no class of AI (a model,
                   a tier) in its own words: which one runs a kind is not the
                   kind's fact.
  WrittenOnce      No source file but the declaration and its reader spells a
                   kind word, nor a retired one, as a string of its own.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
import ast
import re
import sys
import unittest
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = next(p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()) / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
from modules.management.task.labels.task_kind import TaskKind
DECLARATION = SCRIPTS.parent.parent / 'modules/management/task/labels/task_kind.py'
READER = SCRIPTS.parent.parent / 'modules/management/task/plan/primitive/task_plan_kind.py'
RETIRED = ('ideation', 'modeling')
WHO_RUNS = re.compile('\\b(models?|tiers?|strong|stronger|strongest|cheap|cheaper|small|smaller|claude|opus|sonnet|haiku|fable|gpt)\\b', re.IGNORECASE)

class Words(unittest.TestCase):

    def test_the_kinds_in_their_order(self) -> None:
        self.assertEqual([kind.word for kind in TaskKind], ['answer', 'plan', 'design', 'critique', 'implement', 'document', 'mechanical'])

    def test_each_word_is_lower_case_with_one_sentence_on_when_it_applies(self) -> None:
        for kind in TaskKind:
            with self.subTest(kind=kind.word):
                self.assertRegex(kind.word, '^[a-z]+$')
                self.assertTrue(kind.applies.endswith('.'))
                self.assertEqual(kind.applies.count('. '), 0, 'one sentence')

    def test_a_word_is_read_in_any_case_and_a_word_that_is_no_kind_is_none(self) -> None:
        self.assertIs(TaskKind.read(' Design '), TaskKind.DESIGN)
        for word in ('', 'modelling', *RETIRED):
            with self.subTest(word=word):
                self.assertIsNone(TaskKind.read(word))

class Carried(unittest.TestCase):

    def test_a_plan_carries_every_kind_but_answer_and_plan(self) -> None:
        self.assertEqual(TaskKind.words(carried=True), ('design', 'critique', 'implement', 'document', 'mechanical'))
        self.assertFalse(TaskKind.ANSWER.carried)
        self.assertFalse(TaskKind.PLAN.carried)

    def test_without_the_filter_every_word_is_listed(self) -> None:
        self.assertEqual(TaskKind.words(), tuple((kind.word for kind in TaskKind)))

class NoPassages(unittest.TestCase):

    def test_a_kind_holds_its_word_when_it_applies_and_whether_carried_and_no_passage(self) -> None:
        for kind in TaskKind:
            with self.subTest(kind=kind.word):
                self.assertEqual(len(kind.value), 3)
                self.assertFalse(hasattr(kind, 'passages'))

    def test_the_declaration_names_no_document_section(self) -> None:
        text = DECLARATION.read_text(encoding='utf-8')
        tree = ast.parse(text)
        docstring = tree.body[0].value if isinstance(tree.body[0], ast.Expr) else None
        cited = [node.value for node in ast.walk(tree) if isinstance(node, ast.Constant) and node is not docstring and isinstance(node.value, str) and re.search('\\.md#', node.value)]
        self.assertEqual(cited, [])

class NothingAboutWho(unittest.TestCase):

    def test_the_declaration_names_no_ai_and_no_class_of_ai(self) -> None:
        text = DECLARATION.read_text(encoding='utf-8')
        found = sorted({match.group(0).lower() for match in WHO_RUNS.finditer(text)})
        self.assertEqual(found, [])

    def test_the_check_would_see_such_a_word(self) -> None:
        self.assertTrue(WHO_RUNS.search('runs on the strongest model'))

def sources() -> list[Path]:
    """Every Python source of the scripts but the suites, the declaration and its reader."""
    skipped = {DECLARATION.resolve(), READER.resolve()}
    top = SCRIPTS.parent.parent
    found = [path for path in sorted(SCRIPTS.rglob('*.py')) if 'tests' not in path.relative_to(SCRIPTS).parts[:-1] and path.resolve() not in skipped]
    for module in ('modules/knowledge/content', 'modules/process', 'modules/computer/module', 'modules/management/task/plan/primitive', 'modules/knowledge/label', 'modules/management/task', 'modules-plugable/ai', 'bundles/memar'):
        found.extend((path for path in sorted((top / module).rglob('*.py')) if 'tests' not in path.relative_to(top).parts and '__pycache__' not in path.parts and (path.resolve() not in skipped)))
    return found

class WrittenOnce(unittest.TestCase):

    def test_no_other_source_spells_a_kind_word_as_a_string_of_its_own(self) -> None:
        words = {*TaskKind.words(), *RETIRED}
        spelt = []
        for path in sources():
            tree = ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Constant) and isinstance(node.value, str) and (node.value.strip().lower() in words):
                    spelt.append(f'{path.relative_to(SCRIPTS.parent.parent).as_posix()}:{node.lineno} {node.value!r}')
        self.assertEqual(spelt, [], 'name the kind through `modules/management/task/labels/task_kind.py`')

    def test_the_scan_reads_the_shelves(self) -> None:
        top = SCRIPTS.parent.parent
        names = {path.relative_to(top).as_posix() for path in sources()}
        self.assertIn('modules/management/task/services/ensure.py', names)
        self.assertIn('modules-plugable/ai/services/get_task_init_context.py', names)
        self.assertNotIn('modules/management/task/labels/task_kind.py', names)

class WordsAreLabels(unittest.TestCase):
    """TaskKind is a closed kind: each word a plan may carry is a label whose definition takes the label TaskKind."""

    def test_each_carried_word_is_defined_once_taking_the_task_kind_label(self) -> None:
        from modules.management.task.labels.task_kind import LABEL_KIND, TASK_KIND_LABEL
        self.assertEqual([d.label.word for d in LABEL_KIND.closed], list(TaskKind.words(carried=True)))
        for definition in LABEL_KIND.closed:
            self.assertTrue(definition.is_a(TASK_KIND_LABEL))
        self.assertEqual(len({d.label.id for d in LABEL_KIND.closed}), len(LABEL_KIND.closed))

    def test_a_word_no_plan_carries_has_no_label(self) -> None:
        from modules.knowledge.label.primitive.label import LabelProblem
        from modules.management.task.labels.task_kind import LABEL_KIND
        with self.assertRaises(LabelProblem):
            LABEL_KIND.normalize(TaskKind.ANSWER.word)
if __name__ == '__main__':
    unittest.main(verbosity=2)
