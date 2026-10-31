#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
from importlib import import_module
from machine.plugable_import import load as plugable_load
_m_fs_test_scratch = plugable_load('computer.memory.filesystem.services.fs_test_scratch')
suite_scratch = _m_fs_test_scratch.suite_scratch
_m_fs_memar = plugable_load('computer.memory.filesystem.services.fs_memar')
memar_fs = _m_fs_memar
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
sys.dont_write_bytecode = True
BUDGET_SECONDS = 30
files = import_module('modules-plugable.management.task.services.task_files')
folder_module = import_module('modules-plugable.management.task.services.folder')
task_concerns = import_module('modules-plugable.management.task.services.concerns')
task_records = import_module('modules-plugable.management.task.services.task_records')
task_claims = import_module('modules-plugable.management.task.services.claims')
task_ensure = import_module('modules-plugable.management.task.services.ensure')
dependency = import_module('modules-plugable.management.task.services.dependency')
report_file = import_module('modules-plugable.management.task.services.report_file')
report_summary = import_module('modules-plugable.management.task.services.report_summary')
plan_file = import_module('modules-plugable.management.task.services.plan_file')
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

    def old(self, sid: str, status: str = 'active', request: str = 'Do the thing.', steps: str = '- [ ] 1. a', report: str | None = None, decisions: str = '- none') -> Path:
        folder = memar_fs.task_dir(sid, create=True)
        files.create_plan_md(folder, sid, 'T', None, None, self.project, status, None, None, None)
        text = (folder / 'plan.md').read_text(encoding='utf-8')
        (folder / 'plan.md').write_text(text.replace('## Request\n', f'## Request\n{request}\n').replace('## Steps\n', f'## Steps\n{steps}\n'), encoding='utf-8', newline='\n')
        status_line = f'Status: {report.capitalize()}' if report else 'Status:'
        (folder / 'report.md').write_text(f'---\nID: {sid}\nTitle: T\n{status_line}\n---\n{report_body(decisions)}', encoding='utf-8', newline='\n')
        return folder

    def new(self, sid: str, status: str = 'active', request: str = 'Do the thing.', steps: str = '- [ ] 1. a', report: str | None = None, decisions: str = '- none') -> Path:
        folder = memar_fs.task_dir(sid, create=True)
        files.create_task(folder, sid, 'T', None, None, self.project, status, None, None, None)
        files.add_text(folder, 'plan', plan_body(request, steps), 'agent')
        files.add_text(folder, 'report', report_body(decisions), 'agent', fields={'status': report} if report else None)
        return folder

    def both(self, sid: str, **options):
        return (('old', self.old(sid + '-o', **options)), ('new', self.new(sid + '-n', **options)))

class Folders(Fixture):

    def test_a_task_is_read_and_is_a_task_folder_in_either_shape(self) -> None:
        for shape, folder in self.both('named'):
            with self.subTest(shape=shape):
                self.assertTrue(folder_module.is_task_folder(folder))
                task = folder_module.read_task(folder)
                self.assertTrue(task.has_plan)
                self.assertEqual((task.status, task.front['title']), ('active', 'T'))

    def test_a_queued_report_keeps_a_task_queued_in_either_shape(self) -> None:
        for shape, folder in self.both('queued', status='active', report='queued'):
            with self.subTest(shape=shape):
                self.assertIn('Queued', folder_module.queued_why(folder_module.read_task(folder)))

class Concerns(Fixture):

    def test_every_step_checked_and_active_is_flagged_in_either_shape(self) -> None:
        for shape, folder in self.both('steps', steps='- [x] 1. a'):
            with self.subTest(shape=shape):
                self.assertIn('every step is checked, yet the status is active', task_concerns.concerns(folder_module.read_task(folder)))

    def test_a_sound_task_has_none_in_either_shape(self) -> None:
        for shape, folder in self.both('sound'):
            with self.subTest(shape=shape):
                self.assertEqual(task_concerns.concerns(folder_module.read_task(folder)), [])

class Reports(Fixture):

    def test_the_status_the_decisions_and_the_summary_are_read_in_either_shape(self) -> None:
        for shape, folder in self.both('report', status='complete', report='complete', decisions='- one\n- two'):
            with self.subTest(shape=shape):
                self.assertEqual(report_file.read_report_status(folder), 'complete')
                self.assertEqual(report_file.decisions_needed(folder), ['- one', '- two'])
                self.assertIsNone(report_file.handback_problem(folder, 'complete'))
                self.assertEqual(report_summary.summary_lines(folder), ['result: It came to this.'])

    def test_a_report_with_no_status_is_not_a_hand_back_in_either_shape(self) -> None:
        for shape, folder in self.both('nostatus'):
            with self.subTest(shape=shape):
                self.assertEqual(report_file.handback_problem(folder, 'active'), f'{files.report_path(folder).name} has no Status')

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

    def test_a_cited_task_is_met_only_when_its_plan_and_report_are_complete_in_either_shape(self) -> None:
        for shape, folder in self.both('done', status='complete', report='complete'):
            with self.subTest(shape=shape):
                self.assertEqual(self.unmet(folder.name), [])
        for shape, folder in self.both('lags', status='complete', report='active'):
            with self.subTest(shape=shape):
                self.assertEqual(self.unmet(folder.name), [f'{folder.name} (plan complete, report active)'])

    def test_a_closed_task_is_read_from_the_branch_in_either_shape(self) -> None:
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

    def test_the_live_folders_of_a_project_hold_a_task_of_either_shape(self) -> None:
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
        self.assertTrue(layout.belongs_at_top('plan.md'))

class OldShapeStays(Fixture):

    def snapshot(self, folder: Path) -> dict:
        return {path.name: path.read_bytes() for path in folder.iterdir() if path.is_file()}

    def test_a_reader_never_rewrites_an_old_task_into_the_new_shape(self) -> None:
        folder = self.old('stays', status='queued')
        before = self.snapshot(folder)
        folder_module.read_task(folder)
        task_concerns.concerns(folder_module.read_task(folder))
        report_file.read_report_status(folder)
        report_file.handback_problem(folder, 'queued')
        plan_file.part_text(folder / 'plan.md', 'Request')
        files.plan_text(folder)
        files.report_text(folder)
        self.assertEqual(self.snapshot(folder), before)
        self.assertFalse((folder / 'task.yaml').exists())

    def test_a_writer_keeps_an_old_task_in_its_shape(self) -> None:
        folder = self.old('writer', status='queued')
        priority = import_module('modules-plugable.management.task.services.priority')
        with contextlib.redirect_stdout(io.StringIO()):
            priority.set_task_priority('writer', '3')
            task_ensure.ensure_task('writer', project=str(self.project))
        self.assertFalse((folder / 'task.yaml').exists())
        self.assertEqual(list(folder.glob('content.*')), [])
        self.assertIn('Priority: 3', (folder / 'plan.md').read_text(encoding='utf-8'))

class Claims(Fixture):

    def test_claims_name_the_plan_of_a_task_of_either_shape(self) -> None:
        for shape, build in (('old', self.old), ('new', self.new)):
            folder = build(f'20261031T000000Z-{shape}-0', status='queued')
            out = io.StringIO()
            with contextlib.redirect_stdout(out), unittest.mock.patch.object(task_claims, 'brief_text', return_value='brief'):
                task_claims.claims(1, str(self.project))
            with self.subTest(shape=shape):
                self.assertIn(f'plan: {files.plan_path(folder)}', out.getvalue())
            stores = files.stores_at(folder)
            stores.replace_status(None, folder.name, 'complete', stores.read_status(None, folder.name)[1])
            (folder / 'claim').unlink(missing_ok=True)
        self.assertEqual(files.plan_path(folder).name, 'content.00003.md')

class Digest(Fixture):

    def test_the_digest_names_the_report_of_a_task_of_either_shape(self) -> None:
        digest = import_module('modules-plugable.ai.services.task_get_decisions_digest')
        for shape, folder in self.both('digest', status='complete', report='complete'):
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                digest.print_task(folder_module.read_task(folder), [], None, [], review=True)
            with self.subTest(shape=shape):
                self.assertIn(f'report: {files.report_path(folder)}', out.getvalue())
                self.assertIn('result: It came to this.', out.getvalue())

class Sweep(Fixture):

    def test_a_finished_task_is_known_to_be_finished_and_an_active_one_is_not_in_either_shape(self) -> None:
        sweep = import_module('modules-plugable.computer.git.services.sweep_idle_task_folders')
        for shape, folder in self.both('done', status='complete', report='complete'):
            with self.subTest(shape=shape):
                self.assertIsNone(sweep.unfinished(folder_module.read_task(folder)))
        for shape, folder in self.both('running'):
            with self.subTest(shape=shape):
                self.assertEqual(sweep.unfinished(folder_module.read_task(folder)), 'its status is active')

class Scratch(Fixture):

    def test_a_scratch_file_in_a_task_folder_of_either_shape_is_refused_outside_its_temp(self) -> None:
        write = plugable_load('computer.memory.filesystem.services.content_write')
        for shape, folder in self.both('scratch'):
            (folder / 'docs').mkdir(exist_ok=True)
            source = folder / 'docs' / 'x.txt'
            source.write_text('x', encoding='utf-8')
            with self.subTest(shape=shape):
                with self.assertRaises(SystemExit):
                    write.refuse_kept_scratch(source)

if __name__ == '__main__':
    unittest.main(verbosity=2)
