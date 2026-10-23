#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for finding tasks in `modules/management/task/services/list.py`.

    python modules/management/task/tests/find.py

The subject is `list`'s answer, named for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes outside its scratch folder. The Memar root is patched onto
one, made under the folder `modules-plugable/computer/filesystem/services/fs_test_scratch.py` names, and removed
again.

What is pinned, and what each pin is for:

  Listed          Every task folder is listed newest first with its title,
                  project, status, priority (5 when none is written), and
                  path; a folder without a readable plan is listed and marked;
                  a plan in an earlier shape reads as one with no status and is
                  marked with where today's shape is shown.
  TextFilter      TEXT matches the id, title, or project, in any case; an id
                  prefix finds a task with no plan.
  StatusAndIdle   --status keeps the tasks in that status, in any case, and
                  takes no old word; --idle-days keeps those quiet
                  that long and says how long; together they find stalled work;
                  a negative --idle-days is refused.
  Conversations   The tasks of one conversation are listed together, where
                  its newest falls, each naming its parent and conversation;
                  --conversation, given any task of it, keeps only that
                  conversation, also once its first task is gone.
  ProjectLocations
                  By default only Memar's own tasks are listed. --project
                  lists every task folder in the project's own location,
                  a name the project chose among them, and each of Memar's
                  whose plan names the project, compared resolved and, on
                  Windows, in any case; it combines with TEXT, --status, and
                  --idle-days. --project always takes a value, a name the
                  registry resolves or a folder the project of which is
                  meant; none, or an empty one, is refused, the calling
                  folder is never read, and an ambiguous name prints its
                  candidates and lists nothing. A recorded location is
                  a project's only when its own project is that one: a
                  nested project's is not the enclosing one's, and a folder
                  that is no project owns none beneath it.
                  --conversation lists a conversation's tasks wherever
                  they lie; a recorded location that is gone is passed over.
  ConcernsMarked  A task that looks finished or abandoned yet is not complete
                  (every step checked while active; an empty Request quiet for a
                  day; no status) carries a `concerns:` line saying why; a
                  sound one, and a complete one, do not. Listing writes nothing.
  ReportMarks     A task whose report.md Status does not agree with its
                  plan's status, whose status is outside queued, active,
                  blocked, complete, or whose Status is not one a report may
                  state, is marked with why; one that agrees, an empty Status,
                  or no report, is not; a report in an earlier shape is marked
                  with where today's shape is shown.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
from machine.plugable_import import load as plugable_load
_m_fs_test_scratch = plugable_load('computer.filesystem.services.fs_test_scratch')
suite_scratch = _m_fs_test_scratch.suite_scratch
_m_fs_memar = plugable_load('computer.filesystem.services.fs_memar')
memar_fs = _m_fs_memar
import argparse
import contextlib
import io
import os
import subprocess
import sys
import tempfile
import time
import unittest
import unittest.mock
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parents[3] / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
import modules.process.project.services.find as project_find
import modules.process.project.services.registry as registry
import modules.process.project.services.preferences as project_preferences
import modules.management.task.services.list as task_find
import modules.process.project.services.task_location as task_location
import modules.knowledge.documentation.plan.services.plan as task_plan
from modules.process.project.services.task_location import register
from modules.knowledge.documentation.plan.services.plan import PLAN_NAME, plan_skeleton
from modules.knowledge.documentation.report.services.report import REPORT_NAME
DAY = 24 * 60 * 60
EARLIER_FORM = '1111-18dc000000000001-0'
OLDEST = '20261001-T000000Z-1'
MIDDLE = '20261002-T000000Z-1'
NEWEST = '20261003-T000000Z-1'
LATEST = '20261004-T000000Z-1'

def plan(title: str, project: str='/work', status: str='active', **link: str) -> str:
    """A plan with STATUS in today's shape (PascalCase keys, Status in the front matter)."""
    text = plan_skeleton('20261001-T000000Z-1', title, '2026-10-01T00:00:00Z', Path(project), **link)
    return text.replace('Status: Active', f'Status: {status.capitalize()}', 1)

def earlier_plan(title: str, status: str='open') -> str:
    """A plan in the shape written before: lower-case keys, `Status:` in the body."""
    return f'---\ntitle: {title}\nopened: 2026-10-01T00:00:00Z\nproject: /work\n---\n# {title}\nStatus: {status}\n\n## Request\n\n## Why\n\n## Steps\n\n## Next\n'

def git_init(path: Path) -> None:
    """Make PATH a git repository of its own, so its project is PATH and not the checkout the scratch lies in."""
    path.mkdir(parents=True, exist_ok=True)
    subprocess.run(['git', 'init', '-q', str(path)], check=True, capture_output=True)

def make_idle(path: Path, days: float) -> None:
    when = time.time() - days * DAY
    for entry in sorted(path.rglob('*'), key=lambda p: len(p.parts), reverse=True):
        os.utime(entry, (when, when))
    os.utime(path, (when, when))

class Fixture(unittest.TestCase):

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.fake_root = Path(self.scratch.name)
        patched = unittest.mock.patch.object(memar_fs, 'memar_root', return_value=self.fake_root)
        patched.start()
        self.addCleanup(patched.stop)

    def task(self, sid: str, text: str | bytes | None=None) -> Path:
        path = memar_fs.task_dir(sid, create=True)
        if isinstance(text, bytes):
            (path / PLAN_NAME).write_bytes(text)
        elif text is not None:
            (path / PLAN_NAME).write_text(text, encoding='utf-8', newline='\n')
        return path

    def run_list(self, *arguments: str | float | None, **filters) -> str:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            task_find.list_tasks(*arguments, **filters)
        return out.getvalue()

    def run_cli(self, *argv: str) -> str:
        """`memar task list ARGV` as the router runs it: the flags parsed, a name resolved, then the listing."""
        parser = argparse.ArgumentParser()
        command = task_find.describe(parser.add_subparsers())
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            command(parser.parse_args(['list', *argv]))
        return out.getvalue()

    def listed(self, text: str) -> list[str]:
        """The ids in TEXT, in order: each entry's first line is the one not indented."""
        return [line.split()[0] for line in text.splitlines() if line and (not line.startswith(' '))]

class Listed(Fixture):

    def test_tasks_are_listed_newest_first_and_only_tasks(self) -> None:
        for sid in (MIDDLE, EARLIER_FORM, NEWEST, OLDEST):
            self.task(sid, plan(sid))
        for name in ('images', 'memar-edit-locks', 's-old'):
            (memar_fs.tasks_root() / name).mkdir()
        self.assertEqual(self.listed(self.run_list()), [NEWEST, MIDDLE, OLDEST, EARLIER_FORM])

    def test_an_entry_shows_title_project_status_and_path(self) -> None:
        path = self.task(NEWEST, plan('Parser: phase two', 'C:/work/parser', 'blocked'))
        text = self.run_list()
        self.assertIn(f'{NEWEST}  Parser: phase two', text)
        self.assertIn(f"project: {Path('C:/work/parser')}", text)
        self.assertIn('status: blocked', text)
        self.assertIn(f'path: {path}', text)
        self.assertNotIn('tasks:', text)
        self.assertNotIn('parent:', text)

    def test_an_entry_shows_its_priority_the_default_when_none_is_written(self) -> None:
        self.task(NEWEST, plan('Ranked', priority=9))
        self.task(MIDDLE, plan('Plain'))
        text = self.run_list()
        self.assertIn('priority: 9', text)
        self.assertIn('priority: 5', text)

    def test_a_plan_in_an_earlier_shape_has_no_status_and_is_marked_with_the_remedy(self) -> None:
        self.task(NEWEST, earlier_plan('Old plan'))
        text = self.run_list()
        self.assertIn('status: none', text)
        self.assertIn(f'{task_find.CONCERNS} its plan is in an earlier shape', text)
        self.assertIn(task_plan.EARLIER_SHAPE_REMEDY, text)
        self.assertNotIn('it has no status', text)

    def test_a_folder_without_a_readable_plan_is_listed_and_marked(self) -> None:
        bare = self.task(OLDEST)
        self.task(MIDDLE, '# Notes only\nStatus: active\n')
        self.task(NEWEST, b'\xff\xfe')
        text = self.run_list()
        self.assertEqual(self.listed(text), [NEWEST, MIDDLE, OLDEST])
        self.assertIn(f'{OLDEST}  {task_find.NO_PLAN}', text)
        self.assertIn(f'path: {bare}', text)
        self.assertIn(f'{MIDDLE}  {task_find.NO_FRONT_MATTER}', text)
        self.assertIn(f'{NEWEST}  {task_find.UNREADABLE_PLAN}', text)
        self.assertEqual(text.count('status:'), 1)

    def test_a_plan_without_a_status_is_listed_saying_so(self) -> None:
        self.task(NEWEST, plan('Old').replace('Status: Active\n', ''))
        text = self.run_list()
        self.assertEqual(self.listed(text), [NEWEST])
        self.assertIn('status: none', text)

    def test_nothing_to_list_is_said(self) -> None:
        self.assertIn('no task folder', self.run_list())
        self.assertIn('no task folder matches', self.run_list('anything'))

class TextFilter(Fixture):

    def test_text_filters_over_id_title_and_project_in_any_case(self) -> None:
        self.task(OLDEST, plan('Ship the parser', '/work/parser'))
        self.task(MIDDLE, plan('Fix login'))
        self.task(NEWEST, plan('Write docs', '/work/website'))
        self.task(LATEST)
        self.assertEqual(self.listed(self.run_list('PARSER')), [OLDEST])
        self.assertEqual(self.listed(self.run_list('Website')), [NEWEST])
        self.assertEqual(self.listed(self.run_list('20261002')), [MIDDLE])
        self.assertEqual(self.listed(self.run_list('20261004')), [LATEST])
        self.assertEqual(self.listed(self.run_list('LOGIN')), [MIDDLE])
        self.assertEqual(self.listed(self.run_list('nothing like it')), [])

class StatusAndIdle(Fixture):

    def test_status_keeps_only_the_tasks_in_that_state(self) -> None:
        self.task(OLDEST, plan('Ship', status='active'))
        self.task(MIDDLE, plan('Fix', status='complete'))
        self.task(NEWEST, plan('Wait', status='blocked'))
        self.task(LATEST)
        self.assertEqual(self.listed(self.run_list(status='active')), [OLDEST])
        self.assertEqual(self.listed(self.run_list(status='blocked')), [NEWEST])
        self.assertEqual(self.listed(self.run_list(status='complete')), [MIDDLE])

    def test_status_matches_in_any_case_and_not_a_plan_in_an_earlier_shape(self) -> None:
        self.task(OLDEST, earlier_plan('Old shape', status='open'))
        self.task(MIDDLE, plan('New shape', status='Active'))
        self.task(NEWEST, plan('New done', status='Complete'))
        self.assertEqual(self.listed(self.run_list(status='ACTIVE')), [MIDDLE])
        self.assertEqual(self.listed(self.run_list(status='complete')), [NEWEST])
        self.assertIn('status: active', self.run_list(MIDDLE))

    def test_the_status_option_takes_any_case_and_no_old_word_on_the_command_line(self) -> None:
        parser = argparse.ArgumentParser()
        verbs = parser.add_subparsers()
        task_find.describe(verbs)
        for given, read in (('ACTIVE', 'active'), ('Complete', 'complete'), ('queued', 'queued')):
            with self.subTest(given=given):
                self.assertEqual(parser.parse_args(['list', '--status', given]).status, read)
        for refused in ('paused', 'open', 'done'):
            with self.subTest(refused=refused):
                with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
                    parser.parse_args(['list', '--status', refused])

    def test_complete_lists_only_the_word_complete(self) -> None:
        self.task(OLDEST, plan('Ship', status='Complete'))
        self.task(MIDDLE, plan('Fix', status='Complete (2026-10-09)'))
        self.task(NEWEST, plan('Other', status='incomplete'))
        self.assertEqual(self.listed(self.run_list(status='complete')), [OLDEST])

    def test_idle_days_keeps_only_the_tasks_quiet_that_long(self) -> None:
        stale = self.task(OLDEST, plan('Ship'))
        self.task(NEWEST, plan('Fresh'))
        make_idle(stale, 9)
        text = self.run_list(idle_days=7)
        self.assertEqual(self.listed(text), [OLDEST])
        self.assertIn('idle: 9.0 days', text)

    def test_both_filters_together_find_the_tasks_work_stalled_in(self) -> None:
        stalled = self.task(OLDEST, plan('Stalled'))
        self.task(MIDDLE, plan('Busy'))
        finished = self.task(NEWEST, plan('Finished', status='complete'))
        make_idle(stalled, 8)
        make_idle(finished, 8)
        text = self.run_list(status='active', idle_days=7)
        self.assertEqual(self.listed(text), [OLDEST])
        self.assertIn('idle: 8.0 days', text)

    def test_a_negative_idle_days_is_refused(self) -> None:
        with self.assertRaises(SystemExit):
            self.run_list(idle_days=-1)

class Conversations(Fixture):

    def setUp(self) -> None:
        super().setUp()
        self.task(OLDEST, plan('First request'))
        self.task(MIDDLE, plan('Delegated step', parent=OLDEST, conversation=OLDEST))
        self.task(NEWEST, plan('Unrelated'))
        self.task(LATEST, plan('Second request', parent=MIDDLE, conversation=OLDEST))

    def test_a_conversations_tasks_are_listed_together_where_its_newest_falls(self) -> None:
        text = self.run_list()
        self.assertEqual(self.listed(text), [LATEST, MIDDLE, OLDEST, NEWEST])
        self.assertIn(f'parent: {MIDDLE}', text)
        self.assertIn(f'conversation: {OLDEST}', text)

    def test_any_task_names_its_conversation(self) -> None:
        for named in (OLDEST, MIDDLE, LATEST):
            with self.subTest(named=named):
                self.assertEqual(self.listed(self.run_list(conversation=named)), [LATEST, MIDDLE, OLDEST])
        self.assertEqual(self.listed(self.run_list(conversation=NEWEST)), [NEWEST])

    def test_a_conversation_whose_first_task_is_gone_is_still_found(self) -> None:
        first = memar_fs.task_dir(OLDEST)
        (first / PLAN_NAME).unlink()
        first.rmdir()
        self.assertEqual(self.listed(self.run_list(conversation=OLDEST)), [LATEST, MIDDLE])

class ProjectLocations(Fixture):

    def setUp(self) -> None:
        super().setUp()
        self.project = self.fake_root / 'project'
        git_init(self.project)
        preferences = project_preferences.preferences_path(self.project)
        preferences.write_text(project_preferences.preferences_text({project_preferences.TASKS_KEY: 'tasks'}), encoding='utf-8', newline='\n')
        self.location = self.project / 'tasks'
        self.in_location(LATEST, plan("The project's", str(self.project), 'blocked', parent=MIDDLE, conversation=MIDDLE))
        self.in_location('my-task', plan('Named by the project', str(self.project)))
        (self.location / 'notes').mkdir()
        (self.location / 'src').mkdir()
        (self.location / 'src' / PLAN_NAME).write_text('# Not a task\n', encoding='utf-8', newline='\n')
        register(self.location)
        register(self.fake_root / 'unmounted')
        named = str(self.project).upper() if os.name == 'nt' else str(self.project)
        self.task(MIDDLE, plan('Opened from the project', named))
        self.task(OLDEST, plan("Another project's", str(self.fake_root / 'other')))

    def in_location(self, sid: str, text: str) -> Path:
        path = self.location / sid
        path.mkdir(parents=True)
        (path / PLAN_NAME).write_text(text, encoding='utf-8', newline='\n')
        return path

    def test_by_default_only_memars_own_tasks_are_listed(self) -> None:
        self.assertEqual(self.listed(self.run_list()), [MIDDLE, OLDEST])
        self.assertEqual(self.listed(self.run_list(status='blocked')), [])

    def test_project_lists_its_own_location_and_memars_tasks_that_name_it(self) -> None:
        text = self.run_list(project=str(self.project))
        self.assertEqual(self.listed(text), [LATEST, MIDDLE, 'my-task'])
        self.assertIn(f"path: {self.location / 'my-task'}", text)
        self.assertNotIn('notes', text)
        self.assertNotIn(f"path: {self.location / 'src'}", text)

    def test_project_combines_with_text_status_and_idle_days(self) -> None:
        make_idle(self.location / LATEST, 9)
        self.assertEqual(self.listed(self.run_list('named', project=str(self.project))), ['my-task'])
        self.assertEqual(self.listed(self.run_list(status='blocked', project=str(self.project))), [LATEST])
        self.assertEqual(self.listed(self.run_list(idle_days=7, project=str(self.project))), [LATEST])

    def test_project_by_name_is_resolved_through_the_registry(self) -> None:
        registry.add_project('parser', self.project, ['analyseur'])
        for word in ('parser', 'PARSER', 'analyseur', 'pars'):
            with self.subTest(word=word):
                self.assertEqual(self.listed(self.run_cli('--project', word)), [LATEST, MIDDLE, 'my-task'])
        self.assertEqual(self.listed(self.run_cli('--project-path', str(self.project))), [LATEST, MIDDLE, 'my-task'])

    def test_a_name_in_place_of_a_path_and_a_path_in_place_of_a_name_are_refused(self) -> None:
        registry.add_project('parser', self.project)
        with self.assertRaises(SystemExit) as raised:
            self.run_cli('--project', str(self.project))
        self.assertIn('--project-path', str(raised.exception.code))
        with self.assertRaises(SystemExit) as raised:
            self.run_cli('--project-path', 'parser')
        self.assertIn('--project NAME', str(raised.exception.code))

    def test_project_with_no_value_is_refused_saying_to_name_it_and_never_reads_the_calling_folder(self) -> None:
        with unittest.mock.patch.object(Path, 'cwd', side_effect=AssertionError('the calling folder was read')):
            for value in ('', '   '):
                with self.subTest(value=value):
                    with self.assertRaises(SystemExit) as raised:
                        self.run_list(project=value)
                    self.assertIn('--project-path', str(raised.exception.code))
        original = os.getcwd()
        os.chdir(self.project)
        try:
            with self.assertRaises(SystemExit):
                self.run_list(project='')
        finally:
            os.chdir(original)

    def test_project_that_is_ambiguous_prints_the_candidates_and_lists_nothing(self) -> None:
        registry.add_project('parser-a', self.project)
        other = self.fake_root / 'other'
        other.mkdir()
        registry.add_project('parser-b', other)
        with self.assertRaises(SystemExit) as raised:
            self.run_cli('--project', 'parser')
        why = str(raised.exception.code)
        self.assertIn('parser-a', why)
        self.assertIn('parser-b', why)

    def test_project_that_names_nothing_is_refused_with_what_was_tried(self) -> None:
        with unittest.mock.patch.object(project_find, 'search_locally', return_value=None):
            with self.assertRaises(SystemExit) as raised:
                self.run_cli('--project', 'nothing-like-it')
        self.assertIn('memar project', str(raised.exception.code))

    def test_project_of_nothing_asked_is_none(self) -> None:
        self.assertIsNone(task_find.project_of(None))

    def test_project_root_takes_a_folder_and_has_no_calling_folder_default(self) -> None:
        with self.assertRaises(TypeError):
            task_location.project_root()

    def test_project_with_a_path_in_a_subfolder_is_that_folders_project(self) -> None:
        subfolder = self.project / 'src' / 'deep'
        subfolder.mkdir(parents=True)
        self.assertEqual(self.listed(self.run_list(project=str(subfolder))), [LATEST, MIDDLE, 'my-task'])

    def test_a_nested_projects_location_is_its_own_not_the_enclosing_ones(self) -> None:
        inner = self.project / 'inner'
        git_init(inner)
        folder = inner / 'tasks' / 'inner-task'
        folder.mkdir(parents=True)
        (folder / PLAN_NAME).write_text(plan("The inner project's", str(inner)), encoding='utf-8', newline='\n')
        register(inner / 'tasks')
        self.assertEqual(self.listed(self.run_list(project=str(self.project))), [LATEST, MIDDLE, 'my-task'])
        self.assertEqual(self.listed(self.run_list(project=str(inner))), ['inner-task'])
        self.assertEqual(task_location.locations_of(self.project), [self.location.resolve()])

    def test_a_folder_that_is_no_project_owns_no_location_beneath_it(self) -> None:
        inner = self.project / 'inner'
        git_init(inner)
        (inner / 'tasks').mkdir()
        register(inner / 'tasks')
        self.assertEqual(task_location.locations_of(self.fake_root), [])
        with unittest.mock.patch.object(task_find, 'project_root', return_value=self.fake_root):
            self.assertEqual(self.listed(self.run_list(project=str(self.fake_root))), [])

    def test_a_project_named_task_is_listed_in_a_recorded_location(self) -> None:
        self.assertIn('my-task', self.listed(self.run_list(project=str(self.project))))
        self.assertEqual(self.listed(self.run_list(conversation='my-task')), ['my-task'])

    def test_conversation_lists_its_tasks_wherever_they_lie_and_a_gone_location_is_passed_over(self) -> None:
        for named in (MIDDLE, LATEST):
            with self.subTest(named=named):
                self.assertEqual(self.listed(self.run_list(conversation=named)), [LATEST, MIDDLE])

class ConcernsMarked(Fixture):

    def concerns_of(self, sid: str, text: str, idle: float=3) -> list[str]:
        path = self.task(sid, text)
        make_idle(path, idle)
        return [line.strip() for line in self.run_list(sid).splitlines() if line.strip().startswith(task_find.CONCERNS)]

    def test_every_step_checked_yet_open_is_marked(self) -> None:
        text = plan(NEWEST).replace('## Request', '## Request' + chr(10) + 'asked').replace('## Steps', '## Steps\n- [x] 1. a')
        self.assertEqual(self.concerns_of(NEWEST, text), [f'{task_find.CONCERNS} every step is checked, yet the status is active'])

    def test_an_empty_request_quiet_for_days_is_marked(self) -> None:
        found = self.concerns_of(NEWEST, plan(NEWEST), idle=5)
        self.assertEqual(found, [f'{task_find.CONCERNS} its Request is empty and nothing has changed for 5.0 days'])

    def test_a_done_task_and_a_fresh_one_are_not_marked(self) -> None:
        self.assertEqual(self.concerns_of(NEWEST, plan(NEWEST, status='complete'), idle=5), [])
        self.assertEqual(self.concerns_of(MIDDLE, plan(MIDDLE), idle=0.1), [])

class ReportMarks(Fixture):

    def report(self, sid: str, status: str, report_status: str | None) -> Path:
        path = self.task(sid, plan(sid, status=status))
        if report_status is not None:
            (path / REPORT_NAME).write_text(f'---\nStatus: {report_status}\n---\n# Report\n\n## What ran\n', encoding='utf-8', newline='\n')
        return path

    def mark_of(self, sid: str) -> str | None:
        text = self.run_list(sid)
        found = [line.strip() for line in text.splitlines() if line.strip().startswith(task_find.DISAGREES)]
        return found[0] if found else None

    def test_a_report_status_that_agrees_with_the_plans_is_not_marked(self) -> None:
        for index, (status, report) in enumerate((('complete', 'Complete'), ('blocked', 'Blocked'), ('active', 'Active'))):
            sid = f'2026100{index}-T000000Z-7'
            with self.subTest(report=report):
                self.report(sid, status, report)
                self.assertIsNone(self.mark_of(sid))

    def test_a_report_status_that_disagrees_is_marked_with_why(self) -> None:
        self.report(NEWEST, 'active', 'Complete')
        self.assertEqual(self.mark_of(NEWEST), f"{task_find.DISAGREES} {REPORT_NAME} Status complete is not the plan's active")
        self.report(MIDDLE, 'complete', 'Blocked')
        self.assertIn("Status blocked is not the plan's complete", self.mark_of(MIDDLE))

    def test_an_empty_status_or_no_report_is_not_marked(self) -> None:
        self.report(NEWEST, 'complete', '')
        self.report(MIDDLE, 'active', None)
        self.assertIsNone(self.mark_of(NEWEST))
        self.assertIsNone(self.mark_of(MIDDLE))

    def test_a_status_outside_the_vocabulary_or_a_report_status_not_allowed_is_marked(self) -> None:
        self.report(NEWEST, 'archived', None)
        self.assertEqual(self.mark_of(NEWEST), f'{task_find.DISAGREES} status archived is not one of queued, active, blocked, complete')
        self.report(MIDDLE, 'complete', 'Finished')
        self.assertIn('Status finished is not one of', self.mark_of(MIDDLE))

    def test_a_report_in_an_earlier_shape_is_marked_with_the_remedy_and_says_no_status(self) -> None:
        for index, body in enumerate(('# Report\nStop: success\n', '---\nStatus:\nOutcome: success\n---\n# Report\n')):
            sid = f'2026100{index}-T000000Z-8'
            path = self.task(sid, plan(sid, status='complete'))
            (path / REPORT_NAME).write_text(body, encoding='utf-8', newline='\n')
            with self.subTest(body=body):
                text = self.run_list(sid)
                self.assertIn(f'{task_find.CONCERNS} {REPORT_NAME} is in an earlier shape', text)
                self.assertIn(task_plan.EARLIER_SHAPE_REMEDY, text)
                self.assertIsNone(self.mark_of(sid))
if __name__ == '__main__':
    unittest.main(verbosity=2)
