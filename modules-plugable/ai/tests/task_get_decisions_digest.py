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
"Design": `memar task_get_decisions_digest` gathers every `Decisions needed` entry across
reports into one digest.

Nothing here writes outside its scratch folder: the Memar root the services
resolve is patched onto one, made under the folder `modules/process/test/services/test_scratch.py`
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
  OpenQuestions      The open `question` contents of the tasks (those no later
                     content refers to) form one section, blocking first, then
                     by task and number; a question a `Decisions needed` line
                     names as `task#number` is shown there only; a `task#number`
                     naming no open question is a failed hand-back; `--day`
                     keeps the questions asked that day; `--project` reads that
                     project's tasks; a `--conversation` digest leaves them out.
  DecisionContents   The review shows each task's `decision` contents with their
                     Decided, Confidence and Reason fields.
  ProjectScope       `--project` reads a project's tasks in its own
                     location, as `list --project` does; the default does not.
"""
from __future__ import annotations
from importlib import import_module
_m_test_scratch = import_module('modules.process.test.services.test_scratch')
suite_scratch = _m_test_scratch.suite_scratch
_m_memar_location = import_module('bundles.memar.services.location.memar_location')
memar_fs = _m_memar_location
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
sys.path.insert(0, str(SCRIPTS / 'services'))
sys.path.insert(1, str(SCRIPTS))
sys.path.insert(2, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
task_files = import_module('modules-plugable.management.task.services.task_files')

def stores_over(path):
    return task_files.stores_at(Path(path).parent)
import modules.computer.software.edges.manifest.services.preferences as project_preferences
import modules.computer.software.services.project_registry as registry
task_digest = import_module('modules-plugable.management.task.services.task_get_decisions_digest.task_get_decisions_digest')
task_location = import_module('modules-plugable.management.task.services.task_location')
import shape
task_files_mod = import_module('modules-plugable.management.task.services.task_memory')
task_plan = import_module('modules-plugable.knowledge.documentation.plan.services.plan_text')
task_report = import_module('modules-plugable.knowledge.documentation.report.services.report_text')

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
        shape.from_plan_text(folder, plan)
        body = report.split('---\n', 2)[2]
        shape.add_report(folder, report_status.lower(), body)
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
            self.assertIn(f'report: {task_files_mod.report_path(folder)}', text)
        self.assertIn('- Which module owns Y? Options: a, b. Recommend a.', text)
        self.assertIn('- Delete Z? Recommend no.', text)
        self.assertNotIn(quiet.name, text)

    def test_each_task_shows_its_priority(self) -> None:
        folder = self.task('20261012T050007Z-1-0', 'Ranked', 'blocked', ['- Q?'])
        facts = (folder / shape.FACTS_NAME).read_text(encoding='utf-8')
        (folder / shape.FACTS_NAME).write_text(facts.replace('status:', 'priority: 8\nstatus:', 1), encoding='utf-8', newline='\n')
        self.assertIn('priority: 8', self.digest())

    def test_a_report_that_is_not_a_hand_back_is_marked(self) -> None:
        self.task('20261012T050008Z-1-0', 'Long', 'blocked', [f'- Q{index}?' for index in range(11)])
        text = self.digest()
        self.assertIn('failed hand-back: 11 lines under Decisions needed, more than 10', text)

    def test_a_failed_hand_back_with_no_decisions_is_in_it(self) -> None:
        missing = self.task('20261012T050010Z-1-0', 'No report body', '', [], status='blocked')
        for path in missing.glob('content.*.md'):
            if 'kind: report' in path.read_text(encoding='utf-8'):
                path.unlink()
        text = self.digest()
        self.assertIn(f'{missing.name}  No report body', text)
        self.assertIn('failed hand-back: report is missing', text)

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
        for path in folder.glob('content.*.md'):
            if path.read_text(encoding='utf-8').startswith('---\nkind: plan\n'):
                path.write_text(path.read_text(encoding='utf-8').replace('## Request\nx', '## Request\nx\n\n## Steps\n- [x] 1. a'), encoding='utf-8', newline='\n')
                break
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
        shape.add_report(folder, 'complete', '# Report\n\n## What ran\nlong text\n\n## Result\nFirst result line.\nSecond line.\n\n## Decisions needed\n- Keep it?\n')
        text = self.review('today')
        self.assertIn('status: complete', text)
        self.assertIn('report: complete', text)
        self.assertIn('result: First result line.', text)
        self.assertIn('- Keep it?', text)
        self.assertIn(f'close, once the owner confirms it is finished: memar git_trash_task_folder --task-id {folder.name}', text)
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
        shape.from_plan_text(folder, f'---\nTitle: Project task\nStatus: Blocked\nOpened: 2026-10-12T00:00:00Z\nProject: {project}\n---\n# Project task\n\n## Request\nx\n')
        shape.add_report(folder, 'blocked', '# Report\n\n## Decisions needed\n- In the project?\n')
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
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            task_digest.get_decisions_digest(project='theproject')
        self.assertIn('- In the project?', out.getvalue())
        self.assertEqual('-'.join(task_digest.DECLARATIONS[0].name.split()), 'get-decisions-digest')

class OpenQuestions(Fixture):
    """The digest's `Open questions` section: the open `question` contents, beside the decisions."""

    def content(self, folder: Path, number: int, kind: str, body: str, refs: str='', placed: str='2026-10-01T00:00:00Z') -> None:
        refs_line = f'refs: {refs}\n' if refs else ''
        (folder / f'content.{number:05d}.md').write_text(f'---\nkind: {kind}\nplaced_at: {placed}\n{refs_line}---\n{body}', encoding='utf-8', newline='\n')

    def ask(self, folder: Path, number: int, heading: str, blocks: str, asked: str) -> None:
        self.content(folder, number, 'question', f'### {heading}\n- Blocks: {blocks}\n- Asked: {asked}, Claude\n')

    def test_open_questions_are_listed_blocking_first_then_by_task_and_number(self) -> None:
        folder = self.task('20261012T080000Z-1-0', 'Asker', 'success', [])
        self.ask(folder, 1, 'Later free?', 'no', '2026-10-02')
        self.ask(folder, 2, 'Early blocker?', 'the gate', '2026-10-03')
        self.ask(folder, 3, 'Other free?', 'no', '2026-10-01')
        text = self.digest()
        self.assertIn('Open questions', text)
        self.assertIn('3 entries', text)
        order = [text.index(name) for name in ('Early blocker?', 'Later free?', 'Other free?')]
        self.assertEqual(order, sorted(order))
        self.assertIn(f'{folder.name}#2: Early blocker? [blocks]', text)
        self.assertNotIn('Later free? [blocks]', text)

    def test_no_questions_no_section(self) -> None:
        self.task('20261012T080001Z-1-0', 'Asks', 'blocked', ['- Q?'])
        self.assertNotIn('Open questions', self.digest())

    def test_a_question_shows_even_when_no_task_asks_for_a_decision(self) -> None:
        folder = self.task('20261012T080002Z-1-0', 'Quiet', 'success', [])
        self.ask(folder, 1, 'Lone?', 'no', '2026-10-02')
        text = self.digest()
        self.assertIn('Lone?', text)
        self.assertNotIn('no decisions needed', text)

    def test_an_answered_question_is_not_listed(self) -> None:
        folder = self.task('20261012T080003Z-1-0', 'Answered', 'success', [])
        self.ask(folder, 1, 'Settled?', 'no', '2026-10-02')
        self.content(folder, 2, 'decision', '### Settled\n- Decided: yes\n', refs='1', placed='2026-10-03T00:00:00Z')
        self.assertNotIn('Settled?', self.digest())

    def test_a_question_a_decision_line_points_to_is_listed_once_in_the_decision(self) -> None:
        folder = self.task('20261012T080004Z-1-0', 'Asks', 'blocked', ['- Pointed to? Recommend yes. See 20261012T080004Z-1-0#1'])
        self.ask(folder, 1, 'Pointed to?', 'the gate', '2026-10-03')
        self.ask(folder, 2, 'Not pointed to?', 'no', '2026-10-04')
        text = self.digest()
        self.assertEqual(text.count('Pointed to?'), 1)
        self.assertIn('Not pointed to?', text)
        self.assertNotIn('failed hand-back', text)

    def test_a_pointer_to_a_question_that_is_not_open_is_a_failed_hand_back(self) -> None:
        self.task('20261012T080005Z-1-0', 'Asks', 'blocked', ['- Q? Recommend yes. 20261012T080099Z-1-0#4'])
        self.assertIn('failed hand-back: Decisions needed points to 20261012T080099Z-1-0#4, which holds no open question', self.digest())

    def test_day_review_lists_only_questions_asked_that_day(self) -> None:
        today = datetime.now().date().isoformat()
        folder = self.task('20261012T080006Z-1-0', 'Asker', 'success', [])
        self.ask(folder, 1, 'Asked today?', 'no', today)
        self.ask(folder, 2, 'Asked long ago?', 'no', '2020-01-01')
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            task_digest.get_decisions_digest(day='today')
        self.assertIn('Asked today?', out.getvalue())
        self.assertNotIn('Asked long ago?', out.getvalue())

    def test_project_reads_that_projects_questions_and_not_memars(self) -> None:
        project = Path(self.scratch.name) / 'project'
        project.mkdir()
        subprocess.run(['git', 'init', '-q', str(project)], check=True, capture_output=True)
        memar_task = self.task('20261012T080007Z-1-0', 'Memar asker', 'success', [])
        self.ask(memar_task, 1, 'In memar?', 'no', '2026-10-02')
        there = project / '.agents' / 'tasks' / '20261012T080008Z-1-0'
        there.mkdir(parents=True)
        shape.from_plan_text(there, f'---\nTitle: There\nStatus: Complete\nOpened: 2026-10-12T00:00:00Z\nProject: {project}\n---\n# There\n\n## Request\nx\n')
        self.ask(there, 1, 'In project?', 'no', '2026-10-02')
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            task_digest.get_decisions_digest(project=str(project))
        self.assertIn('In project?', out.getvalue())
        self.assertNotIn('In memar?', out.getvalue())

    def test_a_conversation_digest_leaves_them_out(self) -> None:
        root = self.task('20261012T080009Z-1-0', 'Root', 'success', [])
        self.task('20261012T080010Z-1-0', 'Inside', 'blocked', ['- In?'], conversation=root.name)
        self.ask(root, 1, 'Unrelated?', 'no', '2026-10-02')
        self.assertNotIn('Unrelated?', self.digest(root.name))

class DecisionContents(Fixture):
    """The review shows each task's `decision` contents beside its entries."""

    def test_the_review_shows_a_tasks_decision_contents_with_their_fields(self) -> None:
        folder = self.task('20261012T090100Z-1-0', 'Decider', 'success', [])
        (folder / 'content.00001.md').write_text('---\nkind: decision\n---\n### Naming\n- Decided: keep the name\n- Confidence: strong\n- Reason: it is already used\n', encoding='utf-8', newline='\n')
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            task_digest.get_decisions_digest(day='today')
        self.assertIn('decision: keep the name', out.getvalue())
        self.assertIn('confidence: strong', out.getvalue())
        self.assertIn('reason: it is already used', out.getvalue())

    def test_the_default_digest_does_not_list_a_quiet_tasks_decisions(self) -> None:
        folder = self.task('20261012T090101Z-1-0', 'Decider', 'success', [])
        (folder / 'content.00001.md').write_text('---\nkind: decision\n---\n### Naming\n- Decided: keep the name\n', encoding='utf-8', newline='\n')
        self.assertNotIn('keep the name', self.digest())

class EarlierShapes(Fixture):

        folder = memar_fs.task_dir('20261012-T090000Z-1')
        folder.mkdir(parents=True)
        text = self.digest()
        self.assertIn(task_plan.EARLIER_SHAPE_REMEDY, text)
        self.assertIn('failed hand-back', text)
        self.assertIn('concerns: its plan is in an earlier shape', text)
if __name__ == '__main__':
    unittest.main()
