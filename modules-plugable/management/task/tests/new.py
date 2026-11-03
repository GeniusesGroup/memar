#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for opening a task in `modules-plugable/management/task/services/ensure.py`.

    python modules-plugable/management/task/tests/new.py

The subject is how one task's folder and plan come to exist, named for the
file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes outside its scratch folder. The Memar root is patched onto
one, made under the folder `modules-plugable/computer/memory/filesystem/services/fs_test_scratch.py` names, and removed
again; task folders, locks, and intent notes land there and are removed
with it. The only subprocess is git's top-level, which writes nothing.

What is pinned, and what each pin is for:

  CreatesFolder      `ensure` ensures the task's folder and prints its id,
                     path, and plan, so every task works inside its own
                     folder and nothing lands in git by accident; an id shaped
                     like a path is refused.
  RerunIsIdempotent  Reusing one task id keeps the folder as is and reports
                     the same id and path again.
  TitleRequired      A folder gets its plan.md from `--title`, so a task is
                     not minted, nor a folder with no plan.md taken up, without
                     one; a folder that has a plan is continued without one.
  PlanWritten        The plan is written in UTF-8 with LF and no BOM, records
                     the project `ensure` resolves, which is the git top-level
                     else the current folder — asked of a given folder the
                     same way, which `list --project` relies on —
                     and is never overwritten: it is the record the next
                     task continues from.
  ParentLinked       `--parent` records the task a task came from and the
                     first task of its conversation, read off the parent's
                     own plan; a parent that is not there, or the task
                     itself, is refused, and a plan keeps the link it was
                     written with.
  ReportWritten      Beside the plan, `ensure` writes report.md's skeleton when
                     it is absent and never overwrites one, and prints where
                     it is.
  RoleFoldersMade    Every run makes the folders of the task's own layout
                     (`task_layout`, owner 2026-10-20) the task folder
                     lacks, and leaves what is in them alone.
  ProjectLocation    A project whose preferences set `tasks` gets its new
                     folders there, relative to its top folder or absolute;
                     with no preferences or an empty key, a project other
                     than the Memar checkout gets .agents/tasks/ inside
                     itself (and `ensure` says when git does not ignore it),
                     the checkout its own .agents/tasks/; a location inside
                     Memar's scratch is Memar's as before, and `ensure` says so. The project's top folder or
                     a root is refused, and a location that cannot be made
                     fails with a message, both with nothing made. A name
                     there that is not a task folder is refused and never
                     written into; a new one is made there. A
                     folder there is recorded, continued and linked to from
                     another project, and `ensure` says each time that it is the
                     project's and never swept; a recorded location that is
                     gone is passed over, and once `gc` has removed it, the
                     next folder made there records it again; a location a
                     `ensure` records while `gc` prunes is kept. The project is
                     a scratch folder, so a real project's preferences never
                     reach a test.
  ProjectNamed       `ensure` needs its project, a name or alias the registry
                     resolves or a folder (its git top-level), and refuses
                     none, an empty one, or an ambiguous name, saying why and
                     making nothing; the folder it runs in is never read; a
                     task already there is continued without one; a project
                     with no `tasks` preference is not refused, and Memar is
                     an entry like any other.
  KindWritten        `--label TaskKind=K` writes the plan's task kind, lower case,
                     into a new plan and adds it to one that is there; a word outside the
                     closed list, or a kind no plan carries, is refused and
                     makes nothing; the help lists the kinds from
                     `modules/management/task/labels/task_kind.py`.
  BriefPrinted       A task made with --parent ends with the brief that
                     hands it to a sub-agent, its id filled in; one without
                     a parent prints none.
  OpeningRecorded    Opening a folder is one line in the task log, naming
                     the parent when there is one; a folder in a project's
                     own location is recorded in that location's log, not
                     Memar's.
  LockSharesTheRoot  Locks and intent notes land under the same temp root the
                     task folders are under. How a lock behaves is pinned in
                     `machine/tests/fs_lock.py`, which owns it.
  UnresolvableRoot   With no root to resolve, opening errors rather than
                     guessing a folder.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
from machine.plugable_import import load as plugable_load
_m_fs_test_scratch = plugable_load('computer.memory.filesystem.services.fs_test_scratch')
suite_scratch = _m_fs_test_scratch.suite_scratch
_m_fs_lock = plugable_load('computer.memory.filesystem.services.fs_lock')
fs_lock = _m_fs_lock
_m_fs_memar = plugable_load('computer.memory.filesystem.services.fs_memar')
memar_fs = _m_fs_memar
from importlib import import_module
import argparse
import contextlib
import io
import os
import re
import shutil
import subprocess
import time
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
import modules.computer.software.edges.manifest.services.preferences as project_preferences
task_temp = import_module('modules-plugable.management.task.services.temp')
import modules.computer.software.services.project_registry as registry
task_ensure = import_module('modules-plugable.management.task.services.ensure')
task_new = import_module('modules-plugable.management.task.services.new')
task_files = import_module('modules-plugable.management.task.services.task_files')
timeline_files = import_module('modules.management.timeline.services.timeline_files')
task_report = import_module('modules-plugable.management.task.services.report_file')
_m_layout = import_module('modules-plugable.management.task.services.layout')
FOLDERS = _m_layout.FOLDERS
_m_folder = import_module('modules-plugable.management.task.services.folder')
read_task = _m_folder.read_task
_m_task_id = import_module('modules-plugable.management.task.primitive.task_id')
TaskId = _m_task_id.TaskId
_m_plan_brief = import_module('modules-plugable.ai.services.get_task_plan_carry_out_brief')
brief_text = _m_plan_brief.brief_text
_m_task_kind = import_module('modules.management.task.labels.task_kind')
TaskKind = _m_task_kind.TaskKind
task_location = import_module('modules-plugable.management.task.services.task_location')
import modules.computer.software.services.project_registry as project_registry
_m_task_location = import_module('modules-plugable.management.task.services.task_location')
prune_registry = _m_task_location.prune_registry
registered_locations = _m_task_location.registered_locations
_m_log = import_module('modules-plugable.computer.git.services.log')
TASK_LOG_NAME = _m_log.TASK_LOG_NAME
log_path = _m_log.log_path
_m_plan_file = import_module('modules-plugable.management.task.services.plan_file')
PLAN_NAME = _m_plan_file.PLAN_NAME
_m_report_file = import_module('modules-plugable.management.task.services.report_file')
REPORT_NAME = _m_report_file.REPORT_NAME
TITLE = 'Test the task services'
REPORT = f'---\nID: s-report\nTitle: {TITLE}\nStatus:\n---\n# Report\n\n## What ran\n## Check\n## Result\n## Left open\n'
OPENED = '\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}Z'
GIT_PROJECT_ROOT = task_location.project_root

class SkippedSeconds:
    """The clock `TaskId.new` reads, with the wait for the next second taken by moving the clock on: the seam named here, since the rule that one process never mints a second id in one second is pinned in `task_id.py`."""

    def __init__(self) -> None:
        self.moved = 0.0

    def time(self) -> float:
        return time.time() + self.moved

    def gmtime(self, seconds=None):
        return time.gmtime(self.time() if seconds is None else seconds)

    def strftime(self, form, moment=None):
        return time.strftime(form, moment if moment is not None else self.gmtime())

    def sleep(self, seconds: float) -> None:
        self.moved += seconds

BUDGET_SECONDS = 20
_EMPTY_REPOSITORY: list = []

def git_init(folder) -> None:
    """`git init` of FOLDER, made once per run and copied after, so a Test does not start git for it."""
    import atexit
    import shutil
    import tempfile
    if not _EMPTY_REPOSITORY:
        holder = tempfile.TemporaryDirectory(prefix='new-empty-repository-', ignore_cleanup_errors=True)
        atexit.register(holder.cleanup)
        subprocess.run(['git', 'init', '-q', holder.name], check=True, capture_output=True)
        _EMPTY_REPOSITORY.append(Path(holder.name) / '.git')
    shutil.copytree(_EMPTY_REPOSITORY[0], Path(folder) / '.git', dirs_exist_ok=True)

class Fixture(unittest.TestCase):

    def setUp(self) -> None:
        skipped = unittest.mock.patch.object(_m_task_id, 'time', SkippedSeconds())
        skipped.start()
        self.addCleanup(skipped.stop)
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.fake_root = Path(self.scratch.name)
        patched = unittest.mock.patch.object(memar_fs, 'memar_root', return_value=self.fake_root)
        patched.start()
        self.addCleanup(patched.stop)
        self.project = self.fake_root / 'project'
        self.project.mkdir()
        self.in_project(self.fake_root)

    def ensure(self, *arguments, **options):
        """`ensure_task` told the project this test works in, as `--project` tells it."""
        return task_ensure.ensure_task(*arguments, **{'project': str(self.current), **options})

    def call_open(self, *arguments, **options):
        return task_new.open_task(*arguments, **{'project': str(self.current), **options})

    def in_project(self, project: Path) -> None:
        self.current = project
        patched = unittest.mock.patch.object(task_ensure, 'project_root', return_value=project)
        patched.start()
        self.addCleanup(patched.stop)

    def prefer(self, project: Path, tasks: str) -> None:
        path = project_preferences.preferences_path(project)
        path.write_text(project_preferences.preferences_text({project_preferences.TASKS_KEY: tasks}), encoding='utf-8', newline='\n')

    def minted_folders(self) -> list[str]:
        root = memar_fs.task_dir('probe').parent
        return [entry.name for entry in root.iterdir() if TaskId.is_form(entry.name)] if root.is_dir() else []

class CreatesFolder(Fixture):

    def test_creates_the_folder_and_returns_its_id_and_path(self) -> None:
        sid, path = self.ensure('s-1', TITLE)
        self.assertEqual(sid, 's-1')
        self.assertTrue(path.is_dir())
        self.assertEqual(path, memar_fs.task_dir('s-1'))

    def test_open_prints_the_id_path_and_plan(self) -> None:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.call_open('s-2', TITLE, None)
        text = out.getvalue()
        path = memar_fs.task_dir('s-2')
        self.assertIn('task_id: s-2', text)
        self.assertIn(f'path: {path}', text)
        self.assertIn(f'memar conversation post --timeline s-2 --kind plan', text)
        self.assertIn(task_temp.TEMP_SENTENCE, text)

    def test_mints_an_id_when_none_is_given(self) -> None:
        sid, path = self.ensure(title=TITLE)
        self.assertTrue(TaskId.is_form(sid))
        self.assertEqual(path, memar_fs.task_dir(sid))

    def test_refuses_a_path_as_a_task_id(self) -> None:
        for bad in ('a/b', 'a\\b', '..', '.', ''):
            with self.subTest(bad=bad):
                with self.assertRaises(SystemExit):
                    self.ensure(bad, TITLE)

class RerunIsIdempotent(Fixture):

    def test_rerun_keeps_the_folder_and_reports_the_same_path(self) -> None:
        first_id, first_path = self.ensure('s-9', TITLE)
        marker = first_path / 'notes.md'
        marker.write_text('# Notes\n', encoding='utf-8', newline='\n')
        self.assertEqual(self.ensure('s-9'), (first_id, first_path))
        self.assertTrue(marker.is_file())

class TitleRequired(Fixture):

    def test_a_new_task_needs_a_title(self) -> None:
        for title in (None, '', '   ', 'two\nlines'):
            with self.subTest(title=title):
                with self.assertRaises(SystemExit):
                    self.ensure(title=title)
        self.assertEqual(self.minted_folders(), [])

    def test_a_folder_without_a_plan_needs_a_title(self) -> None:
        bare = memar_fs.task_dir('s-bare', create=True)
        with self.assertRaises(SystemExit):
            self.ensure('s-bare')
        self.assertFalse((bare / 'task.yaml').exists())
        self.ensure('s-bare', TITLE)
        self.assertTrue((bare / 'task.yaml').is_file())

    def test_a_folder_with_a_plan_is_continued_without_one(self) -> None:
        sid, path = self.ensure('s-plan', TITLE)
        self.assertEqual(self.ensure('s-plan'), (sid, path))

class PlanWritten(Fixture):

    def test_the_facts_are_utf8_lf_no_bom_and_name_the_project_and_no_plan_is_written(self) -> None:
        _, path = self.ensure('s-plan', TITLE)
        raw = (path / 'task.yaml').read_bytes()
        self.assertFalse(raw.startswith(bytes([0xef, 0xbb, 0xbf])))
        self.assertNotIn(bytes([13]), raw)
        facts = task_files.read_facts(path)
        self.assertEqual((facts['title'], facts['status']), (TITLE, 'active'))
        self.assertRegex(facts['start_date'], OPENED)
        self.assertEqual(Path(facts['project']), self.current)
        self.assertEqual(timeline_files.read_contents(path), [])

    def test_a_plan_posted_after_the_task_is_utf8_lf_no_bom(self) -> None:
        _, path = self.ensure('s-plan', TITLE)
        timeline_files.add_text(path, 'plan', '# Plan' + chr(10) + 'Written.' + chr(10), 'agent')
        raw = task_files.plan_path(path).read_bytes()
        self.assertFalse(raw.startswith(bytes([0xef, 0xbb, 0xbf])))
        self.assertNotIn(bytes([13]), raw)
        self.assertEqual(task_files.plan_text(path), '# Plan' + chr(10) + 'Written.' + chr(10))

    def test_continuing_never_overwrites_the_plan(self) -> None:
        sid, path = self.ensure('s-keep', TITLE)
        kept = [(content.number, content.header, content.body) for content in timeline_files.read_contents(path)]
        stores = task_files.stores_at(path)
        stores.replace_status(None, sid, 'complete', stores.read_status(None, sid)[1])
        self.ensure(sid)
        self.ensure(sid, 'Another title')
        self.assertEqual([(content.number, content.header, content.body) for content in timeline_files.read_contents(path)], kept)
        self.assertEqual(task_files.read_facts(path)['title'], TITLE)

    def test_the_project_is_the_git_top_level_else_the_folder_given_and_never_the_current_one(self) -> None:
        found = subprocess.CompletedProcess([], 0, stdout=f'{self.fake_root}\n', stderr='')
        refused = subprocess.CompletedProcess([], 128, stdout='', stderr='not a git repository')
        for outcome, expected in (({'return_value': found}, self.fake_root.resolve()), ({'return_value': refused}, self.project.resolve()), ({'side_effect': FileNotFoundError('git')}, self.project.resolve())):
            with self.subTest(expected=expected):
                with unittest.mock.patch.object(subprocess, 'run', **outcome):
                    self.assertEqual(GIT_PROJECT_ROOT(self.project), expected)

    def test_a_folders_project_is_asked_of_git_in_that_folder_else_is_the_folder(self) -> None:
        refused = subprocess.CompletedProcess([], 128, stdout='', stderr='not a git repository')
        with unittest.mock.patch.object(subprocess, 'run', return_value=refused) as run:
            self.assertEqual(GIT_PROJECT_ROOT(self.project), self.project.resolve())
        self.assertEqual(run.call_args.args[0][:3], ['git', '-C', str(self.project.resolve())])

class KindWritten(Fixture):

    def test_a_kind_is_written_into_a_new_plan_and_set_on_one_that_is_there(self) -> None:
        _, path = self.ensure('s-kind', TITLE, labels=['TaskKind=Design'])
        self.assertRegex(task_files.read_facts(path)['labels'], r'\Adesign\([0-9a-f-]{36}\)\Z')
        self.ensure('s-kind', labels=['TaskKind=mechanical'])
        self.assertRegex(task_files.read_facts(path)['labels'], r'\Adesign\([0-9a-f-]{36}\)' + chr(10) + r'mechanical\([0-9a-f-]{36}\)\Z')

    def test_a_plan_made_without_a_kind_has_none(self) -> None:
        _, path = self.ensure('s-nokind', TITLE)
        self.assertNotIn('Kind', task_files.read_facts(path).get('labels', ''))

    def label_help(self) -> str:
        parser = argparse.ArgumentParser()
        task_new.describe(parser.add_subparsers())
        new = parser._subparsers._group_actions[0].choices['ensure']
        return next((action.help for action in new._actions if '--label' in action.option_strings))

    def test_the_old_flags_are_gone(self) -> None:
        parser = argparse.ArgumentParser()
        task_new.describe(parser.add_subparsers())
        new = parser._subparsers._group_actions[0].choices['ensure']
        flags = {flag for action in new._actions for flag in action.option_strings}
        self.assertNotIn('--kind', flags)
        self.assertNotIn('--topic', flags)

    def test_the_help_lists_the_kinds_the_declaration_lets_a_plan_carry(self) -> None:
        help_text = self.label_help()
        self.assertIn(', '.join(TaskKind.titles(carried=True)), help_text)
        self.assertIn(f'{TaskKind.ANSWER.title}, {TaskKind.PLAN.title} are refused', help_text)
        self.assertIn('TaskKind, Topic', help_text)

    def test_the_description_sends_findings_and_questions_to_the_contents_of_a_task(self) -> None:
        text = ' '.join(task_new.DESCRIPTION.split())
        self.assertIn("what it finds is a content of that task", text)
        self.assertNotIn("research note", text)
        self.assertNotIn("docs/", text)
        self.assertIn("is a `research` task of its own, recorded as a Research document", text)
        self.assertNotIn("write its plan.md, then leave it", text)
        self.assertIn("A question only the owner can answer is a `question` content of the task it concerns, and a large unrelated one a task of its own.", text)
        self.assertNotIn("in the handoff of the document it concerns", text)

    def test_a_kind_no_plan_carries_is_refused_and_makes_nothing(self) -> None:
        with self.assertRaises(SystemExit):
            self.ensure('s-answer', TITLE, labels=[f'TaskKind={TaskKind.ANSWER.title}'])
        self.assertFalse(memar_fs.task_dir('s-answer').exists())

    def test_a_word_that_is_no_kind_is_refused_and_makes_nothing(self) -> None:
        with self.assertRaises(SystemExit):
            self.ensure('s-badkind', TITLE, labels=['TaskKind=modelling'])
        self.assertFalse(memar_fs.task_dir('s-badkind').exists())

class ReportWritten(Fixture):

    def test_no_report_is_written_until_one_is_posted(self) -> None:
        _, path = self.ensure('s-report', TITLE)
        self.assertEqual(timeline_files.read_contents(path), [])
        timeline_files.add_text(path, 'report', '# Report' + chr(10) + 'Written.' + chr(10), 'agent')
        raw = task_files.report_path(path).read_bytes()
        self.assertNotIn(bytes([13]), raw)
        self.assertEqual(timeline_files.read_contents(path)[0].header['kind'], 'report')

    def test_a_report_is_never_overwritten_by_ensuring_again(self) -> None:
        _, path = self.ensure('s-report', TITLE)
        timeline_files.add_text(path, 'report', '# Report' + chr(10) + 'Written.' + chr(10), 'agent')
        before = [content.body for content in timeline_files.read_contents(path)]
        self.ensure('s-report')
        self.assertEqual([content.body for content in timeline_files.read_contents(path)], before)
        self.assertEqual(task_files.report_text(path), '# Report' + chr(10) + 'Written.' + chr(10))

    def test_new_prints_where_the_report_is(self) -> None:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.call_open('s-said', TITLE, None)
        self.assertIn('memar conversation post --timeline s-said --kind report', out.getvalue())

class RoleFoldersMade(Fixture):

    def test_every_run_makes_the_role_folders_that_are_missing(self) -> None:
        _, path = self.ensure('s-roles', TITLE)
        self.assertEqual(sorted((entry.name for entry in path.iterdir() if entry.is_dir())), sorted(FOLDERS))
        (path / 'services' / 'note.py').write_text('# Note\n', encoding='utf-8', newline='\n')
        (path / 'tests').rmdir()
        self.ensure('s-roles')
        self.assertTrue((path / 'tests').is_dir())
        self.assertTrue((path / 'services' / 'note.py').is_file())

class ProjectLocation(Fixture):
    """A project gets its task folders in the location its preferences set, else in its own .agents/tasks/."""

    def setUp(self) -> None:
        super().setUp()
        self.in_project(self.project)

    def open(self, *arguments) -> tuple[str, Path, str]:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.call_open(*arguments)
        printed = out.getvalue()
        sid = re.search('task_id: (\\S+)', printed).group(1)
        return (sid, Path(re.search('path: (.+)', printed).group(1).strip()), printed)

    def test_without_preferences_or_with_an_empty_key_the_folder_is_in_the_project_itself(self) -> None:
        for prepare in (lambda: None, lambda: self.prefer(self.project, '')):
            with self.subTest(prepare=prepare):
                prepare()
                sid, path, printed = self.open(None, TITLE, None)
                location = self.project / '.agents' / 'tasks'
                self.assertEqual(path, location / sid)
                self.assertFalse(memar_fs.task_dir(sid).exists())
                self.assertIn(f"location: {location} is a project's own task location", printed)
                self.assertIn(location.resolve(), registered_locations())

    def test_the_memar_checkout_itself_keeps_its_folders_in_its_own_temp_tasks(self) -> None:
        for prepare in (lambda: None, lambda: self.prefer(self.fake_root, '')):
            with self.subTest(prepare=prepare):
                prepare()
                self.in_project(self.fake_root)
                sid, path, printed = self.open(None, TITLE, None)
                self.assertEqual(path, memar_fs.task_dir(sid))
                self.assertNotIn('location:', printed)
                self.assertEqual(registered_locations(), [])

    def test_a_preference_still_wins_over_the_default(self) -> None:
        self.prefer(self.project, 'work/tasks')
        sid, path, _ = self.open(None, TITLE, None)
        self.assertEqual(path, self.project / 'work' / 'tasks' / sid)
        self.assertFalse((self.project / 'temp').exists())

    def test_the_default_location_is_found_again_from_memar_and_from_another_project(self) -> None:
        sid, path, _ = self.open(None, TITLE, None)
        self.assertEqual(task_location.locations_of(self.project), [path.parent.resolve()])
        other = self.fake_root / 'other'
        other.mkdir()
        self.in_project(other)
        again, path_again, _ = self.open(sid, None, None)
        self.assertEqual((again, path_again), (sid, path))
        _, child, _ = self.open(None, 'Delegated step', sid)
        self.assertEqual(read_task(child).parent, sid)

    def test_a_custom_location_git_does_not_ignore_is_told_so_and_nothing_is_written_to_it(self) -> None:
        git_init(self.project)
        self.prefer(self.project, 'work/tasks')
        _, _, printed = self.open(None, TITLE, None)
        self.assertRegex(printed, 'not ignored by git')
        self.assertFalse((self.project / '.gitignore').exists())
        (self.project / '.gitignore').write_text('work/tasks\n', encoding='utf-8', newline='\n')
        _, _, printed = self.open(None, TITLE, None)
        self.assertNotIn('not ignored by git', printed)

    def test_the_default_location_is_left_for_git_to_see(self) -> None:
        git_init(self.project)
        _, _, printed = self.open(None, TITLE, None)
        self.assertNotIn('not ignored by git', printed)

    def test_a_relative_location_is_under_the_projects_top_folder(self) -> None:
        self.prefer(self.project, 'work/tasks')
        sid, path, printed = self.open(None, TITLE, None)
        location = self.project / 'work' / 'tasks'
        self.assertEqual(path, location / sid)
        self.assertTrue(task_files.plan_path(path).is_file())
        self.assertTrue(task_files.report_path(path).is_file())
        self.assertTrue(all(((path / folder).is_dir() for folder in FOLDERS)))
        self.assertFalse(memar_fs.task_dir(sid).exists())
        self.assertIn(f"location: {location} is a project's own task location", printed)
        self.assertIn("Memar's sweep never moves a folder there", printed)
        self.assertEqual(registered_locations(), [location.resolve()])

    def test_an_absolute_location_is_used_as_it_is(self) -> None:
        elsewhere = self.fake_root / 'elsewhere'
        self.prefer(self.project, str(elsewhere))
        sid, path, _ = self.open(None, TITLE, None)
        self.assertEqual(path, elsewhere / sid)

    def test_a_location_inside_memars_scratch_is_memars_own_and_new_says_so(self) -> None:
        self.prefer(self.project, str(memar_fs.tasks_root()))
        sid, path, printed = self.open(None, TITLE, None)
        self.assertEqual(path, memar_fs.task_dir(sid))
        self.assertNotRegex(printed, re.compile('^\\s*location:', re.M))
        said = [line for line in printed.splitlines() if "is Memar's own tasks folder" in line]
        self.assertEqual(len(said), 1, printed)
        self.assertIn(str(project_preferences.preferences_path(self.project)), said[0])
        self.assertEqual(registered_locations(), [])

    def test_the_projects_top_folder_or_a_root_is_refused_and_nothing_is_made(self) -> None:
        for value in ('.', 'work/..', str(self.project), Path(self.project.resolve().anchor).as_posix()):
            with self.subTest(value=value):
                self.prefer(self.project, value)
                before = sorted((entry.name for entry in self.project.iterdir()))
                with contextlib.redirect_stdout(io.StringIO()), self.assertRaises(SystemExit) as raised:
                    self.call_open(None, TITLE, None)
                self.assertIn('`tasks` in', str(raised.exception.code))
                self.assertEqual(sorted((entry.name for entry in self.project.iterdir())), before)
                self.assertEqual(self.minted_folders(), [])
                self.assertEqual(registered_locations(), [])

    def test_an_existing_folder_that_is_not_a_task_is_never_written_into(self) -> None:
        self.prefer(self.project, 'work')
        own = self.project / 'work' / 'src'
        own.mkdir(parents=True)
        (own / 'main.kh').write_text('x\n', encoding='utf-8', newline='\n')
        with contextlib.redirect_stdout(io.StringIO()), self.assertRaises(SystemExit) as raised:
            self.call_open('src', TITLE, None)
        self.assertIn('is not a task folder', str(raised.exception.code))
        self.assertEqual([entry.name for entry in own.iterdir()], ['main.kh'])
        self.assertFalse(memar_fs.task_dir('src').exists())
        self.assertEqual(registered_locations(), [])

    def test_a_new_name_in_the_location_is_still_made_there(self) -> None:
        self.prefer(self.project, 'work')
        sid, path, _ = self.open('my-task', TITLE, None)
        self.assertEqual((sid, path), ('my-task', self.project / 'work' / 'my-task'))
        again, path_again, _ = self.open('my-task', None, None)
        self.assertEqual((again, path_again), (sid, path))

    def test_a_location_that_is_a_file_fails_with_a_message(self) -> None:
        self.prefer(self.project, 'work')
        (self.project / 'work').write_text('not a folder\n', encoding='utf-8', newline='\n')
        with contextlib.redirect_stdout(io.StringIO()), self.assertRaises(SystemExit) as raised:
            self.call_open(None, TITLE, None)
        message = str(raised.exception.code)
        self.assertIn('could not be made', message)
        self.assertIn(str(project_preferences.preferences_path(self.project)), message)
        self.assertTrue((self.project / 'work').is_file())
        self.assertEqual(registered_locations(), [])

    def test_it_is_continued_and_linked_to_from_another_project_and_says_so_again(self) -> None:
        self.prefer(self.project, 'tasks')
        sid, path, _ = self.open(None, TITLE, None)
        other = self.fake_root / 'other'
        other.mkdir()
        self.in_project(other)
        again, path_again, printed = self.open(sid, None, None)
        self.assertEqual((again, path_again), (sid, path))
        self.assertIn('location:', printed)
        _, child, _ = self.open(None, 'Delegated step', sid)
        self.assertEqual(child, other / '.agents' / 'tasks' / child.name)
        self.assertEqual(read_task(child).parent, sid)

    def test_a_location_registered_once_and_gone_is_passed_over(self) -> None:
        self.prefer(self.project, 'tasks')
        self.open(None, TITLE, None)
        self.open(None, TITLE, None)
        entry, = [each for each in project_registry.read_entries() if each.locations]
        self.assertEqual(len(entry.locations), 1)
        self.assertEqual(Path(entry.path), self.project.resolve())
        project_registry.add_location(self.project, self.fake_root / 'unmounted')
        self.assertEqual(registered_locations(), [(self.project / 'tasks').resolve()])

    def test_a_location_pruned_once_gone_is_recorded_again_when_a_task_is_made_there(self) -> None:
        self.prefer(self.project, 'tasks')
        self.open(None, TITLE, None)
        location = (self.project / 'tasks').resolve()
        shutil.rmtree(location, onexc=lambda remove, path, error: (os.chmod(path, 0o600), remove(path)))
        self.assertEqual(prune_registry(), [location])
        self.assertEqual(registered_locations(), [])
        self.open(None, TITLE, None)
        self.assertEqual(registered_locations(), [location])

class ProjectNamed(Fixture):
    """`ensure` is told its project, by name or by folder, and never reads the folder it runs in."""

    def setUp(self) -> None:
        super().setUp()
        real = unittest.mock.patch.object(task_ensure, 'project_root', GIT_PROJECT_ROOT)
        real.start()
        self.addCleanup(real.stop)
        self.work = self.fake_root / 'work'
        self.work.mkdir()
        git_init(self.work)

    def refused(self, *arguments, **options) -> str:
        with self.assertRaises(SystemExit) as raised, contextlib.redirect_stdout(io.StringIO()):
            task_ensure.ensure_task(*arguments, **options)
        return str(raised.exception.code)

    def cli(self, *argv: str) -> str:
        """`memar task ensure ARGV` as the router runs it: the flags parsed, a name resolved, then the task made."""
        parser = argparse.ArgumentParser()
        command = task_new.describe(parser.add_subparsers())
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            command(parser.parse_args(['ensure', *argv]))
        return out.getvalue()

    def test_a_new_task_without_a_project_is_refused_with_the_reason_and_nothing_is_made(self) -> None:
        for options in ({}, {'project': ''}, {'project': '  '}):
            for sid in (None, 's-fresh'):
                with self.subTest(options=options, sid=sid):
                    self.assertRegex(self.refused(sid, TITLE, **options), '--project|name the project')
        self.assertEqual(self.minted_folders(), [])
        self.assertFalse(memar_fs.task_dir('s-fresh').exists())
        self.assertFalse((self.work / 'temp').exists())

    def test_the_folder_the_process_is_in_is_never_read(self) -> None:
        original = os.getcwd()
        os.chdir(self.work)
        try:
            with unittest.mock.patch.object(Path, 'cwd', side_effect=AssertionError('the calling folder was read')):
                self.assertIn('--project', self.refused(None, TITLE))
        finally:
            os.chdir(original)
        self.assertFalse((self.work / 'temp').exists())

    def test_a_project_named_by_a_name_or_an_alias_gets_its_folder_in_its_own_temp_tasks(self) -> None:
        registry.add_project('works', self.work, ['travaux'])
        for word in ('works', 'WORKS', 'travaux', 'work'):
            with self.subTest(word=word):
                text = self.cli('--title', TITLE, '--project', word)
                path = Path(re.search('^\\s*path: (.+)$', text, re.M).group(1))
                self.assertEqual(path.parent, self.work.resolve() / '.agents' / 'tasks')
                self.assertEqual(Path(task_files.read_facts(path)['project']), self.work.resolve())

    def test_a_folder_is_given_by_its_own_flag_and_never_in_place_of_a_name(self) -> None:
        text = self.cli('--title', TITLE, '--project-path', str(self.work))
        self.assertIn(str(self.work.resolve() / '.agents' / 'tasks'), text)
        for argv in (('--project', str(self.work)), ('--project-path', 'works')):
            with self.subTest(argv=argv), self.assertRaises(SystemExit) as raised:
                self.cli('--title', TITLE, *argv)
            self.assertIn('--project-path' if argv[0] == '--project' else '--project NAME', str(raised.exception.code))
        self.assertEqual(len([e for e in (self.work / '.agents' / 'tasks').iterdir() if TaskId.is_form(e.name)]), 1)

    def test_a_project_named_by_a_folder_inside_it_is_that_projects_top_level(self) -> None:
        inside = self.work / 'src'
        inside.mkdir()
        with contextlib.redirect_stdout(io.StringIO()):
            sid, path = task_ensure.ensure_task(None, TITLE, project=str(inside))
        self.assertEqual(path, self.work.resolve() / '.agents' / 'tasks' / sid)

    def test_an_ambiguous_name_prints_its_candidates_and_makes_nothing(self) -> None:
        other = self.fake_root / 'other'
        other.mkdir()
        registry.add_project('parser-a', self.work)
        registry.add_project('parser-b', other)
        with self.assertRaises(SystemExit) as raised:
            self.cli('--title', TITLE, '--project', 'parser')
        why = str(raised.exception.code)
        self.assertIn('parser-a', why)
        self.assertIn('parser-b', why)
        self.assertFalse((self.work / 'temp').exists())
        self.assertFalse((other / 'temp').exists())

    def test_a_task_that_is_there_is_continued_without_a_project(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()):
            sid, path = task_ensure.ensure_task('s-here', TITLE, project=str(self.work))
            self.assertEqual(task_ensure.ensure_task(sid), (sid, path))
        with unittest.mock.patch.object(task_ensure, 'project_root', return_value=self.fake_root):
            with contextlib.redirect_stdout(io.StringIO()):
                own, own_path = task_ensure.ensure_task('s-memar', TITLE, project=str(self.fake_root))
            self.assertEqual(own_path, memar_fs.task_dir(own))
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(task_ensure.ensure_task(own), (own, own_path))

    def test_open_task_continuing_without_a_project_says_where_it_is(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()):
            task_ensure.ensure_task('s-here', TITLE, project=str(self.work))
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            task_new.open_task('s-here', None, None)
        self.assertIn(str(self.work.resolve() / '.agents' / 'tasks' / 's-here'), out.getvalue())

    def test_a_project_with_no_tasks_preference_is_not_refused_and_its_folder_is_made(self) -> None:
        self.assertFalse((self.work / 'temp').exists())
        with contextlib.redirect_stdout(io.StringIO()):
            _, path = task_ensure.ensure_task(None, TITLE, project=str(self.work))
        self.assertTrue(path.is_dir())

    def test_a_missing_memar_temp_never_blocks_creating_a_task(self) -> None:
        shutil.rmtree(self.fake_root / 'temp', ignore_errors=True)
        with contextlib.redirect_stdout(io.StringIO()):
            _, path = task_ensure.ensure_task(None, TITLE, project=str(self.work))
        self.assertTrue(path.is_dir())

    def test_memar_is_the_same_kind_of_entry_as_any_project(self) -> None:
        for project in (self.work, self.fake_root):
            with self.subTest(project=project):
                self.assertEqual(task_location.default_location(project), project / '.agents' / 'tasks')
                self.assertEqual(task_location.configured_location(project), project / '.agents' / 'tasks')
        self.assertEqual(task_location.default_location(self.fake_root), memar_fs.tasks_root())
        self.assertIsNone(task_location.project_location(self.fake_root))
        self.assertEqual(task_location.project_location(self.work), self.work / '.agents' / 'tasks')

class BriefPrinted(Fixture):

    def opened(self, *arguments) -> str:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.call_open(*arguments)
        return out.getvalue()

    def test_a_task_made_with_a_parent_ends_with_its_brief_ready_to_paste(self) -> None:
        self.ensure('first', TITLE)
        printed = self.opened('second', 'Delegated step', 'first').splitlines()
        self.assertEqual(printed[-2], '    brief:')
        self.assertEqual(printed[-1], f"        {brief_text('second')}")
        self.assertIn('memar ai get-task-init-context --task-id second', printed[-1])

    def test_a_task_made_without_a_parent_prints_no_brief(self) -> None:
        self.assertNotIn('brief:', self.opened('first', TITLE, None))
        self.assertNotIn('brief:', self.opened('first', None, None))

class ParentLinked(Fixture):

    def test_a_task_opened_from_another_records_it_and_the_first_of_the_conversation(self) -> None:
        self.ensure('first', TITLE)
        _, second = self.ensure('second', 'Second task', parent='first')
        _, third = self.ensure('third', 'Delegated step', parent='second')
        two, three = (read_task(second), read_task(third))
        self.assertEqual((two.parent, two.conversation), ('first', 'first'))
        self.assertEqual((three.parent, three.conversation), ('second', 'first'))

    def test_a_parent_that_is_not_there_or_is_itself_is_refused(self) -> None:
        for sid, parent in (('child', 'absent'), ('child', 'child'), ('child', '../x')):
            with self.subTest(parent=parent):
                with contextlib.redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit):
                        self.ensure(sid, TITLE, parent=parent)
        self.assertFalse(memar_fs.task_dir('child').exists())

    def test_a_plan_keeps_the_link_it_was_written_with(self) -> None:
        self.ensure('first', TITLE)
        self.ensure('other', TITLE)
        self.ensure('second', TITLE, parent='first')
        self.assertEqual(self.ensure('second', parent='first')[0], 'second')
        with self.assertRaises(SystemExit):
            self.ensure('second', parent='other')
        self.assertEqual(read_task(memar_fs.task_dir('second')).parent, 'first')

class OpeningRecorded(Fixture):

    def test_opening_is_one_log_line_naming_the_parent(self) -> None:
        self.ensure('first', TITLE)
        self.ensure('second', TITLE, parent='first')
        self.ensure('second')
        opened = [line.split('\t')[1:4] for line in log_path().read_text(encoding='utf-8').splitlines()]
        opened = [event for event in opened if event[0] == 'opened']
        self.assertEqual(opened, [['opened', 'first', ''], ['opened', 'second', 'parent first']])

    def test_a_task_in_a_project_location_is_recorded_in_that_locations_log(self) -> None:
        self.in_project(self.project)
        self.prefer(self.project, 'tasks')
        self.ensure('first', TITLE)
        _, path = self.ensure('second', TITLE, parent='first')
        own = (self.project / 'tasks' / TASK_LOG_NAME).read_text(encoding='utf-8').splitlines()
        self.assertEqual([line.split('\t')[1:4] for line in own], [['opened', 'first', ''], ['opened', 'second', 'parent first']])
        self.assertEqual(log_path(path), path.parent / TASK_LOG_NAME)
        memars = log_path().read_text(encoding='utf-8') if log_path().is_file() else ''
        self.assertNotIn('\topened\t', memars)

class LockSharesTheRoot(Fixture):

    def test_a_lock_and_its_intent_note_land_under_the_temp_root(self) -> None:
        target = self.fake_root / 'notes.md'
        target.write_text('# Notes\n', encoding='utf-8', newline='\n')
        lock = fs_lock.edit_lock_path(target)
        self.assertEqual(lock.parent, memar_fs.scratch_root() / fs_lock.EDIT_LOCK_DIR_NAME)
        intent = fs_lock.edit_intent_path(lock)
        self.assertEqual(intent.parent, lock.parent)
        self.assertEqual(intent.name, lock.name + '.intent.json')
        _, path = self.ensure('s-3', TITLE)
        self.assertNotEqual(lock.parent, path)
        self.assertFalse(lock.parent.is_relative_to(path))

class UnresolvableRoot(unittest.TestCase):

    def test_errors_rather_than_guessing(self) -> None:
        with unittest.mock.patch.object(memar_fs, 'memar_root', side_effect=SystemExit('error: no root')):
            with self.assertRaises(SystemExit):
                task_ensure.ensure_task('s-1', TITLE, project=str(Path(__file__).resolve().parent))
class NewShapeVerbs(Fixture):

    def made(self, **options):
        return self.ensure(None, TITLE, None, queued=True, priority=7, **options)

    def test_a_task_made_new_is_facts_and_no_content_and_no_plan_md(self) -> None:
        sid, path = self.made()
        self.assertTrue((path / 'task.yaml').is_file())
        self.assertEqual(sorted(entry.name for entry in path.iterdir() if entry.is_file()), ['task.yaml'])
        self.assertFalse((path / 'plan.md').exists())
        self.assertFalse((path / 'report.md').exists())
        task = read_task(path)
        self.assertEqual((task.status, task.front['title']), ('queued', TITLE))

    def test_priority_depends_on_list_and_claims_work_on_it(self) -> None:
        sid, path = self.made()
        task_priority = import_module('modules-plugable.management.task.services.priority')
        task_list = import_module('modules-plugable.management.task.services.list')
        task_depends_on = import_module('modules-plugable.management.task.services.depends_on')
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            task_priority.set_task_priority(sid, '3')
            task_depends_on.change(sid, [], [])
            task_list.list_tasks(status='queued', project=str(self.current))
        self.assertIn('priority 3, was 7', out.getvalue())
        self.assertIn(sid, out.getvalue())
        self.assertEqual(read_task(path).front['priority'], '3')
        self.assertIn(sid, [task.id for task in task_list.find_tasks(status='queued', project=self.current)])

    def test_a_new_shape_task_is_claimed_and_its_status_set_in_task_yaml(self) -> None:
        sid, path = self.made()
        task_claim = import_module('modules-plugable.management.task.services.claim')
        self.assertIsNone(task_claim.try_claim(path))
        self.assertEqual(read_task(path).status, 'active')
        self.assertTrue((path / 'claim').is_file())

class OnlyTheNewShape(Fixture):

    def test_ensure_and_new_take_no_flag_that_selects_the_shape(self) -> None:
        import inspect
        self.assertFalse([name for name in inspect.signature(task_ensure.ensure_task).parameters if 'shape' in name])
        self.assertFalse([name for name in inspect.signature(task_new.open_task).parameters if 'shape' in name])

    def test_a_task_made_by_ensure_is_in_the_new_shape(self) -> None:
        _, path = self.ensure(None, TITLE)
        self.assertTrue((path / 'task.yaml').is_file())
        self.assertFalse((path / 'plan.md').exists())
        self.assertFalse((path / 'report.md').exists())

    def test_open_prints_the_latest_plan_and_report_contents(self) -> None:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.call_open(None, TITLE, None)
        self.assertRegex(out.getvalue(), r'plan: write it with `memar conversation post --timeline \S+ --kind plan')
        self.assertRegex(out.getvalue(), r'report: write it with `memar conversation post --timeline \S+ --kind report')
        self.assertNotIn('plan.md', out.getvalue())

    def test_ensuring_again_adds_nothing_to_a_task_made_new(self) -> None:
        sid, path = self.ensure(None, TITLE)
        before = sorted(entry.name for entry in path.iterdir())
        self.ensure(sid)
        self.assertEqual(sorted(entry.name for entry in path.iterdir()), before)

class OldShapeIsKept(Fixture):

    def made_old(self, sid: str) -> Path:
        path = memar_fs.task_dir(sid, create=True)
        earlier_shape.create_plan_md(path, sid, TITLE, None, None, self.project, 'queued', None, None, None)
        (path / 'report.md').write_text(task_report.report_skeleton(sid, TITLE), encoding='utf-8', newline=chr(10))
        return path

    def test_ensuring_an_old_task_again_never_rewrites_it_into_the_new_shape(self) -> None:
        path = self.made_old('old-1')
        before = {entry.name: entry.read_bytes() for entry in path.iterdir() if entry.is_file()}
        self.ensure('old-1')
        after = {entry.name: entry.read_bytes() for entry in path.iterdir() if entry.is_file()}
        self.assertEqual(after, before)
        self.assertFalse((path / 'task.yaml').exists())

    def test_ensuring_an_old_task_with_a_priority_refuses_and_leaves_plan_md_alone(self) -> None:
        path = self.made_old('old-2')
        before = (path / 'plan.md').read_bytes()
        with self.assertRaises(SystemExit):
            self.ensure('old-2', priority=4)
        self.assertEqual((path / 'plan.md').read_bytes(), before)
        self.assertFalse((path / 'task.yaml').exists())
        self.assertEqual(list(path.glob('content.*')), [])

if __name__ == '__main__':
    unittest.main(verbosity=2)
