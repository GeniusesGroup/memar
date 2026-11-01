#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
from machine.plugable_import import load as plugable_load
_m_fs_test_scratch = plugable_load('computer.memory.filesystem.services.fs_test_scratch')
suite_scratch = _m_fs_test_scratch.suite_scratch
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = next(p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()) / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.path.insert(2, str(TESTS))
sys.dont_write_bytecode = True
import earlier_shape
BUDGET_SECONDS = 30
files = import_module('modules-plugable.management.task.services.task_files')
timeline_files = import_module('modules.management.timeline.services.timeline_files')
generation = import_module('modules-plugable.management.task.services.task_generation')
adapter = import_module('modules-plugable.management.task.services.task_predecessor_adapter')
conversion = import_module('modules-plugable.management.task.services.task_conversion')
errors = import_module('modules-plugable.management.task.errors.errors')

PLAN_BODY = '# T\n\n## Request\nDo the thing.\n\n## Why\nw\n\n## Steps\n- [ ] 1. a\n\n## Next\nn\n'
REPORT_BODY = '# Report\n\n## Result\nIt came to this.\n\n## Decisions needed\n- none\n'


class Fixture(unittest.TestCase):

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)

    def old(self, name: str = 'T-1', status: str = 'active', report: str | None = 'complete') -> Path:
        folder = self.root / name
        folder.mkdir()
        earlier_shape.create_plan_md(folder, name, 'A: title', None, None, Path('/work'), status, 7, None, None)
        text = (folder / 'plan.md').read_text(encoding='utf-8')
        (folder / 'plan.md').write_text(text.rstrip('\n') + '\n\n## Extra\nkept\n', encoding='utf-8', newline='\n')
        if report is not None:
            (folder / 'report.md').write_text(f'---\nID: {name}\nTitle: A: title\nStatus: {report.capitalize()}\n---\n{REPORT_BODY}', encoding='utf-8', newline='\n')
        return folder

    def new(self, name: str = 'T-2') -> Path:
        folder = self.root / name
        folder.mkdir()
        files.create_task(folder, name, 'A: title', None, None, Path('/work'), 'queued', 7, None, None)
        timeline_files.add_text(folder, 'plan', PLAN_BODY, 'agent')
        return folder

    def unstamped(self, name: str = 'T-3') -> Path:
        folder = self.new(name)
        data = (folder / 'task.yaml').read_text(encoding='utf-8')
        (folder / 'task.yaml').write_text(''.join(line for line in data.splitlines(keepends=True) if not line.startswith('writer:')), encoding='utf-8', newline='\n')
        return folder


class Stamp(Fixture):

    def test_a_task_made_now_carries_the_stamp_of_the_current_module(self) -> None:
        self.assertEqual(generation.writer_of(self.new()), (generation.TASK_TYPE_UUID, True))

    def test_a_task_of_plan_md_has_no_stamp_and_is_counted_as_the_first_generation(self) -> None:
        self.assertEqual(generation.writer_of(self.old()), (generation.FIRST_GENERATION_TYPE_UUID, False))

    def test_a_task_yaml_without_a_stamp_is_counted_as_the_first_generation(self) -> None:
        self.assertEqual(generation.writer_of(self.unstamped()), (generation.FIRST_GENERATION_TYPE_UUID, False))

    def test_the_two_generations_have_different_identities(self) -> None:
        self.assertNotEqual(generation.TASK_TYPE_UUID, generation.FIRST_GENERATION_TYPE_UUID)

    def test_the_count_written_by_a_module_is_the_tasks_under_a_root_holding_its_stamp(self) -> None:
        self.old('A')
        self.old('B')
        self.new('C')
        self.assertEqual(generation.count_written_by(self.root, generation.FIRST_GENERATION_TYPE_UUID), 2)
        self.assertEqual(generation.count_written_by(self.root, generation.TASK_TYPE_UUID), 1)


class Adapter(Fixture):

    def test_the_plan_of_an_old_task_is_its_body_without_the_front_matter(self) -> None:
        text = adapter.read_plan(self.old())
        self.assertTrue(text.startswith('# '))
        self.assertIn('## Request', text)
        self.assertNotIn('---', text.splitlines()[0])

    def test_the_report_of_an_old_task_is_its_body_its_presence_and_its_status(self) -> None:
        self.assertEqual(adapter.read_report(self.old()), (REPORT_BODY, True, 'complete'))

    def test_an_old_task_with_no_report_answers_absent(self) -> None:
        self.assertEqual(adapter.read_report(self.old(report=None)), ('', False, ''))

    def test_the_facts_of_an_old_task_are_read_in_the_shape_of_the_facts(self) -> None:
        facts = adapter.read_facts(self.old())
        self.assertEqual((facts['title'], facts['status'], facts['priority']), ('A: title', 'active', '7'))

    def test_the_adapter_offers_no_service_that_writes(self) -> None:
        self.assertEqual([name for name in dir(adapter) if name.startswith(('write', 'replace', 'create', 'rewrite'))], [])


class Stamping(Fixture):

    def test_a_task_yaml_without_a_stamp_is_stamped_and_its_answers_are_kept(self) -> None:
        folder = self.unstamped()
        before = conversion.answers(folder)
        self.assertTrue(conversion.stamp_task(folder))
        self.assertEqual(generation.writer_of(folder), (generation.TASK_TYPE_UUID, True))
        self.assertEqual(conversion.answers(folder), before)

    def test_a_stamped_task_is_not_stamped_again(self) -> None:
        folder = self.new()
        before = (folder / 'task.yaml').read_bytes()
        self.assertFalse(conversion.stamp_task(folder))
        self.assertEqual((folder / 'task.yaml').read_bytes(), before)

    def test_a_task_of_plan_md_is_left_as_it_is(self) -> None:
        folder = self.old()
        self.assertFalse(conversion.stamp_task(folder))
        self.assertTrue((folder / 'plan.md').is_file())
        self.assertFalse((folder / 'task.yaml').exists())

    def test_a_step_reports_the_stamped_and_the_left(self) -> None:
        self.unstamped('A')
        self.unstamped('B')
        self.unstamped('C')
        self.old('D')
        done = conversion.stamp_tasks(self.root, 2)
        self.assertEqual((done.converted, done.left, done.refused), (2, 1, []))
        done = conversion.stamp_tasks(self.root, 10)
        self.assertEqual((done.converted, done.left), (1, 0))
        self.assertEqual(generation.count_written_by(self.root, generation.TASK_TYPE_UUID), 3)


class StampingKeepsAnswers(Fixture):

    def test_the_tasks_a_stamp_would_reach_are_counted_without_changing_one(self) -> None:
        folder = self.unstamped('A')
        self.new('B')
        self.old('C')
        before = (folder / 'task.yaml').read_bytes()
        self.assertEqual([name for name in conversion.pending_stamp(self.root)], ['A'])
        self.assertEqual((folder / 'task.yaml').read_bytes(), before)

    def test_a_stamp_that_would_change_an_answer_is_undone_and_refused(self) -> None:
        folder = self.unstamped('A')
        before = (folder / 'task.yaml').read_bytes()
        original = conversion._stamp

        def damaging(held):
            original(held)
            text = (held / 'task.yaml').read_text(encoding='utf-8').replace('status: queued', 'status: active')
            (held / 'task.yaml').write_text(text, encoding='utf-8', newline='\n')
        with unittest.mock.patch.object(conversion, '_stamp', damaging):
            done = conversion.stamp_tasks(self.root, 10)
        self.assertEqual((done.converted, [name for name, reason in done.refused]), (0, ['A']))
        self.assertEqual((folder / 'task.yaml').read_bytes(), before)


class Error(Fixture):

    def test_the_error_of_a_call_on_an_old_task_names_the_writer_the_successor_and_the_conversion(self) -> None:
        error = errors.Task_Error_WrittenByPredecessor(generation.FIRST_GENERATION_TYPE_UUID, generation.TASK_TYPE_UUID, conversion.SERVICE_NAME)
        self.assertEqual((error.writer, error.successor, error.conversion), (generation.FIRST_GENERATION_TYPE_UUID, generation.TASK_TYPE_UUID, conversion.SERVICE_NAME))


if __name__ == '__main__':
    unittest.main()
