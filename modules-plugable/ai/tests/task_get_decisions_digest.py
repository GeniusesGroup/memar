#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the one digest of decisions tasks hand back, in `modules-plugable/ai/services/task_get_decisions_digest.py`.

    python modules-plugable/ai/tests/task_get_decisions_digest.py

The subject is the digest — every `Decisions needed` entry across the
tasks' reports gathered into one text the owner reads — named for the file
that holds it per
[Test Naming](../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../modules/process/test/rules/test-placement/test-placement.md).
The design it holds is the parent plan's, task 20261012T134849Z-25068-0,
"Design": `memar task get-decisions-digest` gathers every `Decisions needed` entry across
reports into one digest.

Nothing here writes outside its scratch folder: the Memar root the services
resolve is patched onto one, made under the folder `modules-plugable/computer/memory/filesystem/services/fs_test_scratch.py`
names.

What is pinned, and what each pin is for:

  OneDigest          Every task whose report has entries under `Decisions
                     needed` is in the one digest, with its id, title, Stop,
                     and report path, and its entries as written; a task
                     with none is left out; the digest says how many tasks
                     and entries it holds; with none anywhere it says so;
                     `--conversation` narrows it to one conversation. Each
                     task shows its priority, and one whose report is not
                     a hand-back — no Stop, more than ten lines, or a Stop its
                     plan's status disagrees with — is in it marked as a failed
                     hand-back, with entries or without. A done task is
                     left out, its task over, and so is a queued one, which
                     has handed nothing back yet.
                     (A done task whose report has entries is in it, since
                     its decisions are still the owner's to read.) A task
                     not done that looks finished or abandoned is flagged
                     beside its entries (`task_concerns`).
  DayReview          With `--day` (today, yesterday, or a date) the digest is
                     the owner's review: every task not queued that
                     changed on that day, one by one, each with its status,
                     Stop, a line of its report's Result, its entries, its
                     flags, and the one command that closes it once the owner
                     confirms it finished. The review closes nothing; a day
                     that is not one is refused; a day with no task is said.
  OpenHandoffQuestions  The open entries `content questions` lists form one
                     section, blocking first and oldest first; an entry a
                     `Decisions needed` line points to (its path with the
                     heading or the line) is shown there only; a pointer to a
                     file or line holding no open question is a failed
                     hand-back; `--day` keeps the entries asked that day;
                     `--project` reads that project's handoffs; a
                     `--conversation` digest leaves them out.
  ProjectScope       `--project` reads a project's tasks in its own
                     location, as `list --project` does; the default does not.
"""
from __future__ import annotations
from importlib import import_module
from machine.plugable_import import load as plugable_load
_m_fs_test_scratch = plugable_load('computer.memory.filesystem.services.fs_test_scratch')
suite_scratch = _m_fs_test_scratch.suite_scratch
_m_fs_memar = plugable_load('computer.memory.filesystem.services.fs_memar')
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
from datetime import datetime, timedelta
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = next(p for p in TESTS.parents if p.name == 'modules-plugable').parent / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
import modules.process.project.services.preferences as project_preferences
import modules.process.project.services.registry as registry
task_digest = import_module('modules-plugable.ai.services.task_get_decisions_digest')
import modules.process.project.services.task_location as task_location
task_plan = import_module('modules-plugable.management.task.services.plan_file')
task_plan_priority = import_module('modules-plugable.management.task.services.plan_priority')
task_report = import_module('modules-plugable.management.task.services.report_file')

class Fixture(unittest.TestCase):
    ENDS = {'success': 'complete', 'blocked': 'blocked', 'approval-required': 'blocked', 'exhausted': 'active'}

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        patched = unittest.mock.patch.object(memar_fs, 'memar_root', return_value=Path(self.scratch.name))
        patched.start()
        self.addCleanup(patched.stop)

    def task(self, sid: str, title: str, outcome: str, decisions: list[str], conversation: str='', status: str='') -> Path:
        """A task whose report ends as the word OUTCOME says and holds DECISIONS; its plan's STATUS agrees with it unless given."""
        status = status or self.ENDS.get(outcome, 'active')
        folder = memar_fs.task_dir(sid)
        folder.mkdir(parents=True)
        heading = '\n## Decisions needed\n' + '\n'.join(decisions) + '\n' if decisions else ''
        linked = f'Parent: {conversation}\nConversation: {conversation}\n' if conversation else ''
        plan = f'---\nTitle: {title}\nStatus: {status.capitalize()}\nOpened: 2026-10-12T00:00:00Z\nProject: P\n{linked}---\n# {title}\n\n## Request\nx\n'
        report_status = self.ENDS.get(outcome, '').capitalize()
        report = f'---\nStatus: {report_status}\n---\n# Report\n{heading}\n## What ran\nx\n'
        (folder / task_plan.PLAN_NAME).write_text(plan, encoding='utf-8')
        (folder / task_report.REPORT_NAME).write_text(report, encoding='utf-8')
        return folder

    def digest(self, conversation: str | None=None) -> str:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            task_digest.get_decisions_digest(conversation)
        return out.getvalue()

class OneDigest(Fixture):

    def test_every_tasks_decisions_are_in_one_digest(self) -> None:
        first = self.task('20261012T050000Z-1-0', 'First task', 'approval-required', ['- Rename X? Options: keep, rename. Recommend rename.'])
        second = self.task('20261012T050001Z-1-0', 'Second task', 'blocked', ['- Which module owns Y? Options: a, b. Recommend a.', '- Delete Z? Recommend no.'])
        quiet = self.task('20261012T050002Z-1-0', 'Quiet task', 'success', [])
        text = self.digest()
        self.assertEqual(text.count('Decisions needed'), 1)
        self.assertIn('2 tasks, 3 entries', text)
        for folder, title, stop in ((first, 'First task', 'approval-required'), (second, 'Second task', 'blocked')):
            self.assertIn(f'{folder.name}  {title}', text)
            self.assertIn('report: blocked', text)
            self.assertIn(str(folder / task_report.REPORT_NAME), text)
        self.assertIn('- Which module owns Y? Options: a, b. Recommend a.', text)
        self.assertIn('- Delete Z? Recommend no.', text)
        self.assertNotIn(quiet.name, text)

    def test_each_task_shows_its_priority(self) -> None:
        folder = self.task('20261012T050007Z-1-0', 'Ranked', 'blocked', ['- Q?'])
        plan = folder / task_plan.PLAN_NAME
        task_plan_priority.set_priority(plan, 8)
        self.assertIn('priority: 8', self.digest())

    def test_a_report_that_is_not_a_hand_back_is_marked(self) -> None:
        self.task('20261012T050008Z-1-0', 'Long', 'blocked', [f'- Q{index}?' for index in range(11)])
        self.task('20261012T050009Z-1-0', 'Disagrees', 'success', ['- Q?'], status='blocked')
        text = self.digest()
        self.assertIn('failed hand-back: 11 lines under Decisions needed, more than 10', text)
        self.assertIn("failed hand-back: report.md Status complete is not the plan's blocked", text)

    def test_a_failed_hand_back_with_no_decisions_is_in_it(self) -> None:
        silent = self.task('20261012T050010Z-1-0', 'No stop', '', [], status='blocked')
        wrong = self.task('20261012T050011Z-1-0', 'Disagrees quietly', 'success', [], status='blocked')
        text = self.digest()
        self.assertIn(f'{silent.name}  No stop', text)
        self.assertIn('failed hand-back: report.md has no Status', text)
        self.assertIn(f'{wrong.name}  Disagrees quietly', text)
        self.assertIn("failed hand-back: report.md Status complete is not the plan's blocked", text)

    def test_a_done_task_with_decisions_is_in_it_and_a_quiet_done_or_queued_one_is_not(self) -> None:
        done = self.task('20261012T050012Z-1-0', 'Done', 'success', ['- Settled?'])
        quiet = self.task('20261012T050014Z-1-0', 'Quiet done', 'success', [])
        queued = self.task('20261012T050013Z-1-0', 'Waiting', '', [], status='queued')
        text = self.digest()
        self.assertIn(done.name, text)
        self.assertIn('- Settled?', text)
        self.assertNotIn(quiet.name, text)
        self.assertNotIn(queued.name, text)

    def test_a_not_done_task_that_looks_finished_is_flagged_beside_its_decisions(self) -> None:
        folder = self.task('20261012T050015Z-1-0', 'Forgot', 'blocked', ['- Q?'], status='active')
        plan = folder / task_plan.PLAN_NAME
        steps = '## Request\nx\n\n## Steps\n- [x] 1. a'
        plan.write_text(plan.read_text(encoding='utf-8').replace('## Request\nx', steps), encoding='utf-8')
        self.assertIn('concerns: every step is checked, yet the status is active', self.digest())

    def test_with_no_decisions_anywhere_it_says_so(self) -> None:
        self.task('20261012T050003Z-1-0', 'Quiet', 'success', [])
        self.assertIn('no decisions needed', self.digest())

    def test_conversation_narrows_it(self) -> None:
        root = self.task('20261012T050004Z-1-0', 'Root', 'success', [])
        inside = self.task('20261012T050005Z-1-0', 'Inside', 'blocked', ['- In?'], conversation=root.name)
        self.task('20261012T050006Z-1-0', 'Outside', 'blocked', ['- Out?'])
        text = self.digest(root.name)
        self.assertIn(inside.name, text)
        self.assertNotIn('- Out?', text)

class DayReview(Fixture):
    """`digest --day`: every task of one day, summarized one by one, each with the word that closes it."""

    def settle(self, folder: Path, days_ago: float) -> Path:
        when = time.time() - days_ago * 24 * 60 * 60
        for entry in sorted(folder.rglob('*'), key=lambda path: len(path.parts), reverse=True):
            os.utime(entry, (when, when))
        os.utime(folder, (when, when))
        return folder

    def review(self, day: str) -> str:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            task_digest.get_decisions_digest(day=day)
        return out.getvalue()

    def test_only_the_tasks_changed_on_that_day_are_reviewed(self) -> None:
        today = self.task('20261012T060000Z-1-0', 'Today task', 'success', [])
        old = self.settle(self.task('20261011T060000Z-1-0', 'Old task', 'success', []), 3)
        text = self.review('today')
        self.assertIn(f'{today.name}  Today task', text)
        self.assertNotIn(old.name, text)
        self.assertIn(old.name, self.review((datetime.now() - timedelta(days=3)).date().isoformat()))

    def test_each_task_is_summarized_with_its_result_and_how_to_close_it(self) -> None:
        folder = self.task('20261012T060001Z-1-0', 'Summarised', 'success', ['- Keep it?'])
        report = folder / task_report.REPORT_NAME
        report.write_text('---\nStatus: Complete\n---\n# Report\n\n## What ran\nlong text\n\n## Result\nFirst result line.\nSecond line.\n\n## Decisions needed\n- Keep it?\n', encoding='utf-8')
        text = self.review('today')
        self.assertIn('status: complete', text)
        self.assertIn('report: complete', text)
        self.assertIn('result: First result line.', text)
        self.assertIn('- Keep it?', text)
        self.assertIn(f'close, once the owner confirms it is finished: memar git trash-task-folder --task-id {folder.name}', text)
        self.assertTrue(folder.is_dir())

    def test_a_sound_task_without_decisions_is_reviewed_too_but_a_queued_one_is_not(self) -> None:
        quiet = self.task('20261012T060002Z-1-0', 'Quiet', 'success', [])
        queued = self.task('20261012T060003Z-1-0', 'Waiting', '', [], status='queued')
        text = self.review('today')
        self.assertIn(quiet.name, text)
        self.assertNotIn(queued.name, text)

    def test_a_review_of_a_day_with_no_task_says_so(self) -> None:
        self.assertIn('no task changed on', self.review('2020-01-01'))

    def test_the_review_does_not_close_anything(self) -> None:
        folder = self.task('20261012T060004Z-1-0', 'Stays', 'success', [])
        self.review('today')
        self.assertTrue(folder.is_dir())

    def test_a_bad_day_is_refused(self) -> None:
        with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
            self.review('lately')

class ProjectScope(Fixture):
    """`digest --project`: a project keeps its tasks in its own location, which the default digest does not read."""

    def test_the_default_reads_memars_tasks_and_project_reads_the_projects_own_location(self) -> None:
        project = Path(self.scratch.name) / 'project'
        project.mkdir()
        subprocess.run(['git', 'init', '-q', str(project)], check=True, capture_output=True)
        preferences = project_preferences.preferences_path(project)
        preferences.write_text(project_preferences.preferences_text({project_preferences.TASKS_KEY: 'tasks'}), encoding='utf-8', newline='\n')
        location = project / 'tasks'
        folder = location / '20261012T070000Z-1-0'
        folder.mkdir(parents=True)
        (folder / task_plan.PLAN_NAME).write_text(f'---\nTitle: Project task\nStatus: Blocked\nOpened: 2026-10-12T00:00:00Z\nProject: {project}\n---\n# Project task\n\n## Request\nx\n', encoding='utf-8')
        (folder / task_report.REPORT_NAME).write_text('---\nStatus: Blocked\n---\n# Report\n\n## Decisions needed\n- In the project?\n', encoding='utf-8')
        task_location.register(location)
        own = self.task('20261012T070001Z-1-0', 'Memar task', 'blocked', ['- In memar?'])
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            task_digest.get_decisions_digest()
        self.assertIn(own.name, out.getvalue())
        self.assertNotIn('In the project?', out.getvalue())
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            task_digest.get_decisions_digest(project=str(project))
        self.assertIn('- In the project?', out.getvalue())
        registry.add_project('theproject', project)
        with self.assertRaises(SystemExit) as raised:
            task_digest.get_decisions_digest(project='')
        self.assertIn('--project-path', str(raised.exception.code))
        parser = argparse.ArgumentParser()
        command = task_digest.describe(parser.add_subparsers())
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            command(parser.parse_args(['get-decisions-digest', '--project', 'theproject']))
        self.assertIn('- In the project?', out.getvalue())

class OpenHandoffQuestions(Fixture):
    """The digest's `Open handoff questions` section: the entries `content questions` lists, beside the decisions."""

    def handoff(self, relative: str, entries: list[tuple[str, str, str]], root: Path | None=None) -> Path:
        """A handoff at RELATIVE holding ENTRIES, each (heading, Blocks text, Asked date)."""
        path = (root or Path(self.scratch.name)) / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        body = ''.join((f'### {heading}\n- Blocks: {blocks}\n- Asked: {asked}, Claude\n\n' for heading, blocks, asked in entries))
        path.write_text(f'# X handoff\n\n## Open Questions\n{body}', encoding='utf-8', newline='\n')
        return path

    def test_open_entries_are_listed_blocking_first_oldest_first(self) -> None:
        self.handoff('docs/x.handoff.md', [('Later free?', 'no', '2026-10-02'), ('Early free?', 'nothing', '2026-10-01'), ('Late blocker?', 'the lint', '2026-10-05'), ('Early blocker?', 'the gate', '2026-10-03')])
        text = self.digest()
        self.assertIn('Open handoff questions', text)
        self.assertIn('4 entries', text)
        order = [text.index(name) for name in ('Early blocker?', 'Late blocker?', 'Early free?', 'Later free?')]
        self.assertEqual(order, sorted(order))
        self.assertIn('docs/x.handoff.md:16: Early blocker? [blocks]', text.replace('\\', '/'))
        self.assertNotIn('Early free? [blocks]', text)

    def test_no_entries_no_section(self) -> None:
        self.task('20261012T080000Z-1-0', 'Asks', 'blocked', ['- Q?'])
        self.assertNotIn('Open handoff questions', self.digest())

    def test_entries_show_even_when_no_task_asks(self) -> None:
        self.handoff('docs/x.handoff.md', [('Lone?', 'no', '2026-10-02')])
        text = self.digest()
        self.assertIn('Lone?', text)
        self.assertNotIn('no decisions needed', text)

    def test_an_entry_a_decision_points_to_is_listed_once_in_the_decision(self) -> None:
        self.handoff('docs/x.handoff.md', [('Pointed to?', 'the gate', '2026-10-03'), ('Not pointed to?', 'no', '2026-10-04')])
        self.task('20261012T080001Z-1-0', 'Asks', 'blocked', ['- Pointed to? Recommend yes. See docs/x.handoff.md'])
        text = self.digest()
        self.assertEqual(text.count('Pointed to?'), 1)
        self.assertIn('Not pointed to?', text)
        self.assertNotIn('failed hand-back', text)

    def test_a_pointer_by_line_hides_the_entry_at_that_line(self) -> None:
        path = self.handoff('docs/x.handoff.md', [('Worded otherwise?', 'no', '2026-10-04')])
        self.task('20261012T080002Z-1-0', 'Asks', 'blocked', ['- Q? Recommend yes. docs/x.handoff.md:4'])
        self.assertEqual(self.digest().count('Worded otherwise?'), 0, path)

    def test_a_pointer_to_a_file_that_is_not_there_is_a_failed_hand_back(self) -> None:
        self.task('20261012T080003Z-1-0', 'Asks', 'blocked', ['- Q? Recommend yes. docs/gone.handoff.md'])
        text = self.digest()
        self.assertIn('failed hand-back: Decisions needed points to docs/gone.handoff.md, which does not exist', text)

    def test_a_pointer_to_a_line_with_no_entry_is_a_failed_hand_back(self) -> None:
        self.handoff('docs/x.handoff.md', [('Real?', 'no', '2026-10-04')])
        self.task('20261012T080004Z-1-0', 'Asks', 'blocked', ['- Q? Recommend yes. docs/x.handoff.md:99'])
        self.assertIn('failed hand-back: Decisions needed points to docs/x.handoff.md:99, which holds no open question there', self.digest())

    def test_a_pointer_to_a_file_with_no_open_question_is_a_failed_hand_back(self) -> None:
        path = Path(self.scratch.name) / 'docs' / 'empty.handoff.md'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('# E\n\n## Open Questions\nNone.\n', encoding='utf-8')
        self.task('20261012T080005Z-1-0', 'Asks', 'blocked', ['- Q? docs/empty.handoff.md'])
        self.assertIn('docs/empty.handoff.md, which holds no open question', self.digest())

    def test_day_review_lists_only_entries_asked_that_day(self) -> None:
        today = datetime.now().date().isoformat()
        self.handoff('docs/x.handoff.md', [('Asked today?', 'no', today), ('Asked long ago?', 'no', '2020-01-01')])
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            task_digest.get_decisions_digest(day='today')
        self.assertIn('Asked today?', out.getvalue())
        self.assertNotIn('Asked long ago?', out.getvalue())

    def test_project_reads_that_projects_handoffs_and_not_memars(self) -> None:
        project = Path(self.scratch.name) / 'project'
        project.mkdir()
        subprocess.run(['git', 'init', '-q', str(project)], check=True, capture_output=True)
        self.handoff('docs/x.handoff.md', [('In memar?', 'no', '2026-10-02')])
        self.handoff('docs/y.handoff.md', [('In project?', 'no', '2026-10-02')], root=project)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            task_digest.get_decisions_digest(project=str(project))
        self.assertIn('In project?', out.getvalue())
        self.assertNotIn('In memar?', out.getvalue())

    def test_a_conversation_digest_leaves_them_out(self) -> None:
        root = self.task('20261012T080006Z-1-0', 'Root', 'success', [])
        self.task('20261012T080007Z-1-0', 'Inside', 'blocked', ['- In?'], conversation=root.name)
        self.handoff('docs/x.handoff.md', [('Unrelated?', 'no', '2026-10-02')])
        self.assertNotIn('Unrelated?', self.digest(root.name))

class EarlierShapes(Fixture):

    def test_a_task_in_an_earlier_shape_is_shown_with_where_todays_shape_is_shown(self) -> None:
        folder = memar_fs.task_dir('20261012-T090000Z-1')
        folder.mkdir(parents=True)
        (folder / task_plan.PLAN_NAME).write_text('---\ntitle: Old\nopened: 2026-10-12T00:00:00Z\nproject: P\n---\n# Old\nStatus: done\n\n## Request\nx\n', encoding='utf-8')
        (folder / task_report.REPORT_NAME).write_text('# Report\nStop: success\n\n## Decisions needed\n- Q?\n', encoding='utf-8')
        text = self.digest()
        self.assertIn(task_plan.EARLIER_SHAPE_REMEDY, text)
        self.assertIn('failed hand-back', text)
        self.assertIn('concerns: its plan is in an earlier shape', text)
if __name__ == '__main__':
    unittest.main()
