#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
from importlib import import_module
_m_test_scratch = import_module('modules.process.test.services.test_scratch')
suite_scratch = _m_test_scratch.suite_scratch
_m_memar_location = import_module('bundles.memar.services.location.memar_location')
memar_fs = _m_memar_location
import contextlib
import io
import subprocess
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
BUDGET_SECONDS = 30
task_files_mod = import_module('modules-plugable.management.task.services.task_files')
_gen = import_module('modules-plugable.management.task.services.task_generation')
files = import_module('modules-plugable.management.task.services.task_memory')
timeline_files = import_module('modules.management.timeline.services.timeline_files')
folder_module = import_module('modules-plugable.management.task.services.folder')
task_concerns = import_module('modules-plugable.management.task.services.concerns')
task_records = import_module('modules-plugable.management.task.services.task_records')
task_claims = import_module('modules-plugable.management.task.services.claims')
task_ensure = import_module('modules-plugable.management.task.services.ensure')
dependency = import_module('modules-plugable.management.task.services.dependency')
report_text = import_module('modules-plugable.knowledge.documentation.report.services.report_text')
report_summary = import_module('modules-plugable.knowledge.documentation.report.services.report_summary')
plan_text = import_module('modules-plugable.knowledge.documentation.plan.services.plan_text')
layout = import_module('modules-plugable.management.task.services.layout')
Reader = dependency.Reader
Ref = dependency.Ref

def plan_body(request: str = 'Do the thing.', steps: str = '- [ ] 1. a') -> str:
    return f'# T\n\n## Request\n{request}\n\n## Why\nw\n\n## Steps\n{steps}\n\n## Next\nn\n'

def report_body(decisions: str = '- none') -> str:
    return f'# Report\n\n## Result\nIt came to this.\n\n## Decisions needed\n{decisions}\n'

class Fixture(unittest.TestCase):

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.fake_root = Path(self.scratch.name)
        patched = unittest.mock.patch.object(memar_fs, 'memar_root', return_value=self.fake_root)
        patched.start()
        self.addCleanup(patched.stop)
        self.project = self.fake_root / 'project-x'
        self.project.mkdir()
        subprocess.run(['git', 'init', '-q', str(self.project)], check=True, capture_output=True)
        project = unittest.mock.patch.object(task_ensure, 'project_root', return_value=self.project)
        project.start()
        self.addCleanup(project.stop)

    def new(self, sid: str, status: str = 'active', request: str = 'Do the thing.', steps: str = '- [ ] 1. a', report: str | None = None, decisions: str = '- none') -> Path:
        folder = memar_fs.task_dir(sid, create=True)
        from datetime import datetime, timezone
        opened = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        held = {'title': 'T', 'status': status, 'project': str(self.project), 'start_date': opened, 'writer': _gen.TASK_TYPE_UUID}
        (folder / task_files_mod.TASK_FACTS_NAME).write_bytes(task_files_mod.facts_bytes(held))
        timeline_files.add_text(folder, 'plan', plan_body(request, steps), 'agent')
        timeline_files.add_text(folder, 'report', report_body(decisions), 'agent', fields={'status': report} if report else None)
        return folder

    def both(self, sid: str, **options):
        return (('new', self.new(sid + '-n', **options)),)

class Folders(Fixture):

    def test_a_task_is_read_and_is_a_task_folder(self) -> None:
        for shape, folder in self.both('named'):
            with self.subTest(shape=shape):
                self.assertTrue(folder_module.is_task_folder(folder))
                task = folder_module.read_task(folder)
                self.assertTrue(task.has_plan)
                self.assertEqual((task.status, task.front['title']), ('active', 'T'))

    def test_only_the_task_status_queued_keeps_a_task_queued(self) -> None:
        for shape, folder in self.both('queued', status='queued', report='active'):
            with self.subTest(shape=shape):
                self.assertIn('Queued', folder_module.queued_why(folder_module.read_task(folder)))
        for shape, folder in self.both('notqueued', status='active', report='queued'):
            with self.subTest(shape=shape):
                self.assertIsNone(folder_module.queued_why(folder_module.read_task(folder)))

class Concerns(Fixture):

    def test_every_step_checked_and_active_is_flagged(self) -> None:
        for shape, folder in self.both('steps', steps='- [x] 1. a'):
            with self.subTest(shape=shape):
                self.assertIn('every step is checked, yet the status is active', task_concerns.concerns(folder_module.read_task(folder)))

    def test_a_sound_task_has_none(self) -> None:
        for shape, folder in self.both('sound'):
            with self.subTest(shape=shape):
                self.assertEqual(task_concerns.concerns(folder_module.read_task(folder)), [])

class Reports(Fixture):

    def test_the_status_the_decisions_and_the_summary_are_read(self) -> None:
        for shape, folder in self.both('report', status='complete', report='complete', decisions='- one\n- two'):
            with self.subTest(shape=shape):
                self.assertEqual(report_text.read_report_status(folder), '')
                self.assertEqual(folder_module.read_task(folder).status, 'complete')
                self.assertEqual(report_text.decisions_needed(folder), ['- one', '- two'])
                self.assertIsNone(report_text.handback_problem(folder, 'complete'))
                self.assertEqual(report_summary.summary_lines(folder), ['result: It came to this.'])

    def test_a_report_without_a_status_field_is_still_a_hand_back(self) -> None:
        for shape, folder in self.both('nostatus'):
            with self.subTest(shape=shape):
                self.assertIsNone(report_text.handback_problem(folder, 'active'))

class Dependencies(Fixture):

    def setUp(self) -> None:
        super().setUp()
        self.branch: dict[tuple[str, str], bytes] = {}
        read = unittest.mock.patch.object(dependency, 'read_many_from_branch', side_effect=lambda project, sid, names: {name: self.branch[(sid, name)] for name in names if (sid, name) in self.branch})
        read.start()
        self.addCleanup(read.stop)
        held = unittest.mock.patch.object(dependency, 'held_on_branch', side_effect=lambda project, sid: {name: 'blob' for (kept, name) in self.branch if kept == sid})
        held.start()
        self.addCleanup(held.stop)

    def unmet(self, sid: str) -> list:
        return Reader(self.fake_root).unmet([Ref.parse(sid)])

    def test_a_cited_task_is_met_when_its_status_is_complete(self) -> None:
        for shape, folder in self.both('done', status='complete', report='complete'):
            with self.subTest(shape=shape):
                self.assertEqual(self.unmet(folder.name), [])
        for shape, folder in self.both('lags', status='complete', report='active'):
            with self.subTest(shape=shape):
                self.assertEqual(self.unmet(folder.name), [])
        for shape, folder in self.both('running', status='active', report='complete'):
            with self.subTest(shape=shape):
                self.assertEqual(self.unmet(folder.name), [f'{folder.name} (active)'])

    def test_a_closed_task_is_read_from_the_branch(self) -> None:
        for shape, folder in self.both('closed', status='complete', report='complete'):
            kept = {path.name: path.read_bytes() for path in folder.iterdir() if path.is_file()}
            for path in folder.iterdir():
                if path.is_file():
                    path.chmod(0o600)
                    path.unlink()
            folder.rmdir()
            self.branch.update({(folder.name, name): data for name, data in kept.items()})
            with self.subTest(shape=shape):
                self.assertEqual(self.unmet(folder.name), [])

class Records(Fixture):

    def test_the_live_folders_of_a_project_hold_a_task(self) -> None:
        own = self.fake_root / '.agents' / 'tasks'
        own.mkdir(parents=True)
        for shape, folder in self.both('live'):
            with self.subTest(shape=shape):
                found = [path.name for path in task_records.live_folders(self.fake_root)]
                self.assertIn(folder.name, found)

class Layout(Fixture):

    def test_the_facts_and_the_contents_belong_at_the_top_of_a_task_folder(self) -> None:
        self.assertTrue(layout.belongs_at_top('task.yaml'))
        self.assertTrue(layout.belongs_at_top('content.00001.md'))
        self.assertFalse(layout.belongs_at_top('content.1.md'))
        self.assertFalse(layout.belongs_at_top('notes.md'))

class Claims(Fixture):

    def test_claims_name_the_plan_of_a_task(self) -> None:
        for shape, build in (('new', self.new),):
            folder = build('20261031T000000Z-new-0', status='queued', request='Work to claim.')
            out = io.StringIO()
            with contextlib.redirect_stdout(out), unittest.mock.patch.object(task_claims, 'brief_text', return_value='brief'):
                task_claims.claims(1, str(self.project))
            with self.subTest(shape=shape):
                self.assertIn(f'plan: {files.plan_path(folder)}', out.getvalue())
            stores = files.stores_at(folder)
            stores.replace_status(None, folder.name, 'complete', stores.read_status(None, folder.name)[1])
            (folder / 'claim').unlink(missing_ok=True)

class Digest(Fixture):

    def test_the_digest_names_the_report_of_a_task(self) -> None:
        digest = import_module('modules-plugable.ai.services.task_get_decisions_digest')
        for shape, folder in self.both('digest', status='complete', report='complete'):
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                digest.print_task(folder_module.read_task(folder), [], None, [], [], review=True)
            with self.subTest(shape=shape):
                self.assertIn(f'report: {files.report_path(folder)}', out.getvalue())
                self.assertIn('result: It came to this.', out.getvalue())

class Sweep(Fixture):

    def test_a_finished_task_is_known_to_be_finished_and_an_active_one_is_not(self) -> None:
        sweep = import_module('bundles.memar_git.services.sweep_idle_task_folders')
        for shape, folder in self.both('done', status='complete', report='complete'):
            with self.subTest(shape=shape):
                self.assertIsNone(sweep.unfinished(folder_module.read_task(folder)))
        for shape, folder in self.both('running'):
            with self.subTest(shape=shape):
                self.assertEqual(sweep.unfinished(folder_module.read_task(folder)), 'its status is active')

class Scratch(Fixture):

    def test_a_scratch_file_in_a_task_folder_is_refused_outside_its_temp(self) -> None:
        write = import_module('bundles.memar_fs.services.text_edit_command')
        refused = import_module('bundles.memar_fs.errors.errors').ScratchInTaskFolder
        for shape, folder in self.both('scratch'):
            (folder / 'docs').mkdir(exist_ok=True)
            source = folder / 'docs' / 'x.txt'
            source.write_text('x', encoding='utf-8')
            with self.subTest(shape=shape):
                with self.assertRaises(refused):
                    write.refuse_kept_scratch(source)

if __name__ == '__main__':
    unittest.main(verbosity=2)
