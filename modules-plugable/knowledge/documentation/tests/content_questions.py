#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
from importlib import import_module
from machine.plugable_import import load as plugable_load
_m_fs_test_scratch = plugable_load('computer.memory.filesystem.services.fs_test_scratch')
suite_scratch = _m_fs_test_scratch.suite_scratch
import contextlib
import io
import sys
import tempfile
import unittest
import unittest.mock
from argparse import Namespace
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = next(p for p in TESTS.parents if p.name == 'modules-plugable').parent / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
BUDGET_SECONDS = 30
content_questions = import_module('modules-plugable.knowledge.documentation.services.content_questions')
task_records = import_module('modules-plugable.management.task.services.task_records')
Content = import_module('modules.management.timeline.services.timeline_files').Content


def question(number: int, heading: str, blocks: str = 'no.', asked: str = '2026-10-01, Claude, for Omid.', placed_at: str = '2026-10-01T00:00:00Z') -> Content:
    body = f'### {heading}\n- State: x\n- Blocks: {blocks}\n- Asked: {asked}\n'
    return Content(number, {'kind': 'question', 'placed_at': placed_at}, body)


def answer(number: int, refs: str, kind: str = 'decision', placed_at: str = '2026-10-02T00:00:00Z') -> Content:
    return Content(number, {'kind': kind, 'refs': refs, 'placed_at': placed_at}, '### Settled\n')


class OpenQuestions(unittest.TestCase):

    def test_a_question_nobody_refers_to_is_open_with_its_fields(self) -> None:
        found = content_questions.open_questions([('T-1', question(3, 'Which one?', 'the lint.', '2026-10-05, Claude'))])
        self.assertEqual(found, [('T-1', 3, 'Which one?', True, '2026-10-05')])

    def test_a_question_without_a_heading_line_takes_its_first_line(self) -> None:
        content = Content(1, {'kind': 'question'}, 'Plain first line?\n- Blocks: no.\n')
        self.assertEqual(content_questions.open_questions([('T-1', content)])[0][2], 'Plain first line?')

    def test_only_contents_of_kind_question_are_questions(self) -> None:
        self.assertEqual(content_questions.open_questions([('T-1', Content(1, {'kind': 'decision'}, '### D\n'))]), [])

    def test_a_later_content_of_the_same_task_that_refers_to_it_closes_it(self) -> None:
        contents = [('T-1', question(1, 'Q?')), ('T-1', answer(2, '1'))]
        self.assertEqual(content_questions.open_questions(contents), [])

    def test_a_later_content_of_another_task_that_refers_to_it_closes_it(self) -> None:
        contents = [('T-1', question(1, 'Q?')), ('T-2', answer(1, 'T-1:1', kind='message'))]
        self.assertEqual(content_questions.open_questions(contents), [])

    def test_a_content_placed_before_the_question_does_not_close_it(self) -> None:
        contents = [('T-2', answer(1, 'T-1:1', placed_at='2026-09-01T00:00:00Z')), ('T-1', question(1, 'Q?'))]
        self.assertEqual(len(content_questions.open_questions(contents)), 1)

    def test_an_earlier_number_of_the_same_task_does_not_close_it(self) -> None:
        contents = [('T-1', answer(1, '2')), ('T-1', question(2, 'Q?'))]
        self.assertEqual(len(content_questions.open_questions(contents)), 1)

    def test_blocking_comes_first_then_task_and_number(self) -> None:
        contents = [('T-2', question(1, 'B free', 'no.')), ('T-1', question(2, 'A free', 'nothing')), ('T-3', question(1, 'C blocker', 'the verb.')), ('T-1', question(3, 'D blocker', 'the lint.'))]
        found = content_questions.open_questions(contents)
        self.assertEqual([entry[2] for entry in found], ['D blocker', 'C blocker', 'A free', 'B free'])

    def test_a_mixed_answer_blocks_and_a_plain_no_does_not(self) -> None:
        contents = [('T-1', question(1, 'Mixed?', 'no for M1; yes for M2.')), ('T-1', question(2, 'Plain?', 'no; it gates later.'))]
        found = {entry[2]: entry[3] for entry in content_questions.open_questions(contents)}
        self.assertEqual(found, {'Mixed?': True, 'Plain?': False})

    def test_bold_field_names_are_read(self) -> None:
        content = Content(1, {'kind': 'question'}, '### Q?\n- **Blocks**: the gate\n- **Asked**: 2026-10-09, Claude\n')
        self.assertEqual(content_questions.open_questions([('T-1', content)]), [('T-1', 1, 'Q?', True, '2026-10-09')])


class TheVerb(unittest.TestCase):

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        elsewhere = self.root / 'memar-tasks'
        elsewhere.mkdir()
        patched = unittest.mock.patch.object(task_records, 'tasks_root', return_value=elsewhere)
        patched.start()
        self.addCleanup(patched.stop)

    def task(self, task_id: str, number: int, text: str) -> None:
        folder = self.root / '.agents' / 'tasks' / task_id
        folder.mkdir(parents=True, exist_ok=True)
        (folder / 'task.yaml').write_text('title: t\n', encoding='utf-8', newline='\n')
        (folder / f'content.{number:05d}.md').write_text(text, encoding='utf-8', newline='\n')

    def run_verb(self, **kw) -> str:
        args = Namespace(project=None, blocking=False)
        for key, value in kw.items():
            setattr(args, key, value)
        with contextlib.redirect_stdout(io.StringIO()) as printed:
            content_questions.cmd_questions(args, self.root)
        return printed.getvalue()

    def test_a_question_prints_as_task_hash_number_heading_and_blocking_is_marked(self) -> None:
        self.task('T-1', 1, '---\nkind: question\n---\n### Does it block?\n- Blocks: the verb.\n')
        self.task('T-1', 2, '---\nkind: question\n---\n### Free?\n- Blocks: no.\n')
        self.assertEqual(self.run_verb().splitlines(), ['T-1#1: Does it block? [blocks]', 'T-1#2: Free?'])

    def test_the_blocking_filter_drops_the_rest(self) -> None:
        self.task('T-1', 1, '---\nkind: question\n---\n### Does it block?\n- Blocks: the verb.\n')
        self.task('T-1', 2, '---\nkind: question\n---\n### Free?\n- Blocks: no.\n')
        self.assertEqual(self.run_verb(blocking=True).splitlines(), ['T-1#1: Does it block? [blocks]'])

    def test_an_answered_question_is_not_listed_and_none_prints_the_marker(self) -> None:
        self.task('T-1', 1, '---\nkind: question\n---\n### Q?\n')
        self.task('T-1', 2, '---\nkind: decision\nrefs: 1\n---\n### A\n')
        self.assertEqual(self.run_verb().strip(), '(no open questions)')

    def test_the_file_walking_of_handoffs_is_gone(self) -> None:
        self.assertFalse(hasattr(content_questions, 'handoff_files'))
        self.assertFalse(hasattr(content_questions, 'HANDOFF_SUFFIX'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
