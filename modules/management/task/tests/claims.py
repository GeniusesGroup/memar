#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for taking the N queued tasks first in line, in `modules/management/task/services/claims.py`.

    python modules/management/task/tests/claims.py

The subject is `claims N` — how the queued tasks first in line come to be
owned by exactly one agent each, each taken the way `claim` takes one
(`task_claim.py` here tests that) — named for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).
The design it holds is the parent plan's, task 20261012T134849Z-25068-0,
"Design", as the owner's rulings of 2026-10-12, recorded in task
20261012T153414Z-28656-0, rework it: no runner and no launch; `claims N` takes
the N queued tasks first in line, the highest priority first and the oldest
opened first among equals. The owner's ruling recorded in task
20261012T163251Z-25244-0 makes the project required: no default, no all.

Nothing here writes outside its scratch folder: the Memar root the services
resolve is patched onto one, made under the folder `modules-plugable/computer/memory/filesystem/services/fs_test_scratch.py`
names. The concurrent claims run two real processes, each importing the
service with the same root patched in, so the race is the operating system's.

What is pinned, and what each pin is for:

  ClaimsTakesN       `claims N` takes the N queued tasks first in line —
                     the highest priority first, the oldest opened first among
                     equals — and prints for each its id, title, priority,
                     plan, and brief; fewer queued than N is not an error; a
                     queued plan whose Request is empty is passed over;
                     --project is required, and without it `claims` refuses
                     saying one run serves one project; two projects' queued
                     tasks never mix; a task another
                     holds is passed over with why, on standard output and
                     nothing on standard error; N is at least 1; two
                     `claims` at once never take one task twice.
"""
from __future__ import annotations
from machine.plugable_import import load as plugable_load
_m_fs_test_scratch = plugable_load('computer.memory.filesystem.services.fs_test_scratch')
suite_scratch = _m_fs_test_scratch.suite_scratch
_m_fs_memar = plugable_load('computer.memory.filesystem.services.fs_memar')
memar_fs = _m_fs_memar
from importlib import import_module
import argparse
import contextlib
import io
import json
import subprocess
import sys
import tempfile
import time
import unittest
import unittest.mock
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = next(p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()) / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
import modules.process.project.services.registry as registry
plan_brief = import_module('modules-plugable.ai.services.get_task_plan_carry_out_brief')
import modules.management.task.services.claim as task_claim
from modules.management.task.primitive.claim import Claim
import modules.management.task.services.claims as task_claims
import modules.management.task.services.temp as task_temp
import modules.management.task.services.ensure as task_ensure
import modules.management.task.services.plan_file as task_plan
import modules.management.task.services.plan_labels as task_plan_labels

def declare_topic(project: Path, fresh) -> None:
    """Declare the topic FRESH in PROJECT, as a module of it would: a file of a `labels/` folder holding `LABELS`."""
    where = project / 'work' / 'labels'
    where.mkdir(parents=True, exist_ok=True)
    (where / f"{fresh.label.word.replace('-', '_')}.py").write_text(f"from modules.knowledge.label.primitive.topic import topic\nLABELS = (topic({fresh.label.word!r}, {fresh.label.id!r}, 'work on {fresh.label.word}'),)\n", encoding='utf-8')
    task_plan_labels.forget()

def plan_text(status: str, request: str='Do the thing.', title: str='T', opened: str='2026-10-12T00:00:00Z', priority: str | None=None, project: str='P', topic: str | tuple[str, ...] | None=None) -> str:
    ranked = f'Priority: {priority}\n' if priority is not None else ''
    topics = () if topic is None else (topic,) if isinstance(topic, str) else tuple(topic)
    if topics:
        where = Path(project)
        lines = []
        for word in topics:
            label, fresh = task_plan_labels.registry_for(where).resolve(f'Topic={word}')
            if fresh is not None:
                declare_topic(where, fresh)
            lines.append(f'  - {label}\n')
        ranked += 'Labels:\n' + ''.join(lines)
    return f'---\nTitle: {title}\nStatus: {status.capitalize()}\nOpened: {opened}\nProject: {project}\n{ranked}---\n# {title}\n\n## Request\n{request}\n\n## Why\n\n## Steps\n\n## Next\n'

class Fixture(unittest.TestCase):

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.fake_root = Path(self.scratch.name)
        patched = unittest.mock.patch.object(memar_fs, 'memar_root', return_value=self.fake_root)
        patched.start()
        self.addCleanup(patched.stop)
        project = unittest.mock.patch.object(task_ensure, 'project_root', return_value=self.fake_root)
        project.start()
        self.addCleanup(project.stop)

    def task(self, sid: str, status: str, **plan) -> Path:
        folder = memar_fs.task_dir(sid)
        folder.mkdir(parents=True)
        (folder / task_plan.PLAN_NAME).write_text(plan_text(status, **plan), encoding='utf-8', newline='\n')
        return folder

    def status_of(self, folder: Path) -> str:
        return task_plan.read_plan(folder / task_plan.PLAN_NAME).status

    def refused(self, call, *args) -> str:
        with self.assertRaises(SystemExit) as raised:
            call(*args)
        return str(raised.exception.code)

class ClaimsTakesN(Fixture):

    def setUp(self) -> None:
        super().setUp()
        self.project = self.git_project('project-x')

    def git_project(self, name: str) -> Path:
        folder = self.fake_root / name
        folder.mkdir()
        subprocess.run(['git', 'init', '-q', str(folder)], check=True, capture_output=True)
        return folder

    def task(self, sid: str, status: str, **plan) -> Path:
        plan.setdefault('project', str(self.project))
        return super().task(sid, status, **plan)

    def claims(self, count: int, project: Path | None=None) -> tuple[list[str], str]:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            taken = task_claims.claims(count, str(project or self.project))
        return (taken, out.getvalue())

    def test_the_highest_priority_comes_first_and_the_oldest_among_equals(self) -> None:
        low = self.task('20261012T000040Z-1-0', 'queued', opened='2026-10-12T00:00:00Z', priority='2')
        plain_old = self.task('20261012T000041Z-1-0', 'queued', opened='2026-10-12T01:00:00Z')
        high = self.task('20261012T000042Z-1-0', 'queued', opened='2026-10-12T05:00:00Z', priority='9')
        plain_new = self.task('20261012T000043Z-1-0', 'queued', opened='2026-10-12T02:00:00Z', priority='5')
        self.task('20261012T000044Z-1-0', 'active', opened='2026-10-11T00:00:00Z', priority='10')
        taken, _ = self.claims(3)
        self.assertEqual(taken, [high.name, plain_old.name, plain_new.name])
        self.assertEqual(self.status_of(low), 'queued')
        for folder in (high, plain_old, plain_new):
            self.assertEqual(self.status_of(folder), 'active')
            self.assertTrue((folder / Claim.NAME).is_file())

    def test_each_taken_task_is_printed_with_what_hands_it_over(self) -> None:
        folder = self.task('20261012T000045Z-1-0', 'queued', title='Write the parser', priority='7')
        taken, text = self.claims(1)
        self.assertEqual(taken, [folder.name])
        self.assertIn(f'{folder.name}  Write the parser', text)
        self.assertIn('priority: 7', text)
        self.assertIn(f'plan: {folder / task_plan.PLAN_NAME}', text)
        self.assertIn(f'brief: {plan_brief.brief_text(folder.name)}', text)
        self.assertIn(task_temp.TEMP_SENTENCE, text)

    def test_fewer_queued_than_asked_is_not_an_error(self) -> None:
        one = self.task('20261012T000046Z-1-0', 'queued')
        taken, text = self.claims(5)
        self.assertEqual(taken, [one.name])
        self.assertIn('1 of 5', text)
        taken, text = self.claims(5)
        self.assertEqual(taken, [])
        self.assertIn('no queued task', text)

    def test_a_queued_plan_with_an_empty_request_is_passed_over(self) -> None:
        unwritten = self.task('20261012T000047Z-1-0', 'queued', request='', priority='10')
        written = self.task('20261012T000048Z-1-0', 'queued')
        taken, text = self.claims(2)
        self.assertEqual(taken, [written.name])
        self.assertEqual(self.status_of(unwritten), 'queued')
        self.assertIn(f'{unwritten.name}  not ready', text)

    def cli(self, *argv: str) -> None:
        """`memar task claims ARGV` as the router runs it."""
        parser = argparse.ArgumentParser()
        command = task_claims.describe(parser.add_subparsers())
        with contextlib.redirect_stdout(io.StringIO()):
            command(parser.parse_args(['claims', *argv]))

    def test_a_project_named_by_its_name_is_resolved_and_an_empty_one_refused(self) -> None:
        registry.add_project('project-x', self.project, ['iksz'])
        waiting = self.task('20261012T000050Z-1-0', 'queued')
        for flag in ('--project', '--project-path'):
            for empty in ('', '  '):
                with self.subTest(flag=flag, empty=empty):
                    self.assertIn(flag, self.refused(self.cli, '5', flag, empty))
                    self.assertEqual(self.status_of(waiting), 'queued')
        self.assertIn('--project-path', self.refused(self.cli, '5', '--project', str(self.project)))
        self.assertIn('--project NAME', self.refused(self.cli, '5', '--project-path', 'iksz'))
        self.assertEqual(self.status_of(waiting), 'queued')
        self.cli('5', '--project', 'iksz')
        self.assertEqual(self.status_of(waiting), 'active')

    def test_a_missing_project_is_refused_saying_one_run_serves_one_project(self) -> None:
        waiting = self.task('20261012T000049Z-1-0', 'queued')
        why = self.refused(task_claims.claims, 5, None)
        self.assertIn('--project', why)
        self.assertIn('one run serves one project', why)
        self.assertIn('ask the owner', why)
        self.assertEqual(self.status_of(waiting), 'queued')
        self.assertFalse((waiting / Claim.NAME).exists())

    def test_two_projects_queued_tasks_never_mix(self) -> None:
        other_project = self.git_project('project-y')
        theirs = self.task('20261012T000049Z-1-0', 'queued', priority='10', project=str(other_project))
        unnamed = self.task('20261012T000036Z-1-0', 'queued', priority='10', project='P')
        mine = self.task('20261012T000039Z-1-0', 'queued')
        taken, _ = self.claims(5)
        self.assertEqual(taken, [mine.name])
        self.assertEqual(self.status_of(theirs), 'queued')
        self.assertEqual(self.status_of(unnamed), 'queued')
        taken, _ = self.claims(5, other_project)
        self.assertEqual(taken, [theirs.name])
        self.assertEqual(self.status_of(unnamed), 'queued')

    def test_a_task_another_holds_is_passed_over_saying_why_and_nothing_on_stderr(self) -> None:
        held = self.task('20261012T000038Z-1-0', 'queued', priority='10')
        (held / Claim.NAME).write_text('claimed: now\n', encoding='utf-8')
        free = self.task('20261012T000037Z-1-0', 'queued')
        errors = io.StringIO()
        with contextlib.redirect_stderr(errors):
            taken, text = self.claims(2)
        self.assertEqual(taken, [free.name])
        self.assertIn(f'{held.name}  not taken: ', text)
        self.assertIn('claimed by another agent', text)
        self.assertEqual(errors.getvalue(), '')
        self.assertEqual(self.status_of(held), 'queued')

    def test_n_is_at_least_one(self) -> None:
        for count in (0, -1):
            with self.subTest(count=count):
                self.assertIn('at least 1', self.refused(task_claims.claims, count, str(self.project)))

    def test_two_claims_at_once_never_take_one_task_twice(self) -> None:
        folders = [self.task(f'20261012T00005{index}Z-1-0', 'queued') for index in range(5)]
        start = time.time() + 2.0
        script = (
            "import sys, time, json, contextlib, io; sys.path.insert(0, sys.argv[1]); "
            "sys.path.insert(1, __import__('os').path.dirname(__import__('os').path.dirname(sys.argv[1]))); "
            "sys.dont_write_bytecode = True\nfrom pathlib import Path\n"
            "from importlib import import_module\n"
            "m = import_module('modules-plugable.computer.memory.filesystem.services.fs_memar')\n"
            "m.memar_root = lambda: Path(sys.argv[2])\n"
            "import modules.management.task.services.claims as c\n"
            "while time.time() < float(sys.argv[3]): pass\n"
            "with contextlib.redirect_stdout(io.StringIO()): taken = c.claims(4, sys.argv[4])\n"
            "print(json.dumps(taken))\n"
        )
        racers = [subprocess.Popen([sys.executable, '-c', script, str(SCRIPTS), str(self.fake_root), str(start), str(self.project)], stdout=subprocess.PIPE, stderr=subprocess.PIPE) for _ in range(2)]
        results = []
        for racer in racers:
            out, err = racer.communicate(timeout=120)
            self.assertEqual(racer.returncode, 0, err.decode('utf-8', 'replace'))
            results.append(json.loads(out.decode('utf-8').strip().splitlines()[-1]))
        every = results[0] + results[1]
        self.assertEqual(len(every), len(set(every)))
        self.assertEqual(sorted(every), sorted((folder.name for folder in folders)))
        for folder in folders:
            self.assertEqual(self.status_of(folder), 'active')

class ClaimsByTopic(Fixture):
    """The batch rule: the first task's topic pulls the rest of the batch (the owner's ruling of 2026-10-13)."""

    def setUp(self) -> None:
        super().setUp()
        self.project = self.fake_root / 'project-x'
        self.project.mkdir()
        subprocess.run(['git', 'init', '-q', str(self.project)], check=True, capture_output=True)

    def task(self, sid: str, status: str, **plan) -> Path:
        plan.setdefault('project', str(self.project))
        return super().task(sid, status, **plan)

    def claims(self, count: int, project: Path | None=None, topic: str | None=None, fill: bool=False):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            taken = task_claims.claims(count, str(project or self.project), topic, fill)
        return (taken, out.getvalue())

    def queue(self, number: int, topic: str | None, priority: str | None=None, opened: str | None=None) -> Path:
        return self.task(f'20261013T0001{number:02d}Z-1-0', 'queued', topic=topic, priority=priority, opened=opened or f'2026-10-13T00:{number:02d}:00Z')

    def test_the_first_tasks_topic_pulls_the_rest_of_the_batch_in_line_order(self) -> None:
        first = self.queue(1, 'khayyam', priority='9')
        unrelated = self.queue(2, 'docs', priority='8')
        unrelated_plain = self.queue(3, None, priority='7')
        low_a = self.queue(4, 'khayyam', priority='2')
        low_b = self.queue(5, 'khayyam', priority='2')
        other = self.queue(6, 'khayyam', priority='3')
        taken, _ = self.claims(3)
        self.assertEqual(taken, [first.name, other.name, low_a.name])
        for folder in (unrelated, unrelated_plain, low_b):
            self.assertEqual(self.status_of(folder), 'queued')

    def test_other_topics_do_not_fill_the_remainder_by_default(self) -> None:
        first = self.queue(10, 'khayyam', priority='9')
        self.queue(11, 'docs', priority='8')
        self.queue(12, None)
        taken, text = self.claims(4)
        self.assertEqual(taken, [first.name])
        self.assertIn('claimed 1 of 4', text)

    def test_fill_takes_the_next_in_line_after_the_topic_is_exhausted(self) -> None:
        first = self.queue(20, 'khayyam', priority='9')
        second = self.queue(21, 'khayyam', priority='2')
        docs = self.queue(22, 'docs', priority='8')
        plain = self.queue(23, None, priority='7')
        left = self.queue(24, None, priority='1')
        taken, _ = self.claims(4, fill=True)
        self.assertEqual(taken, [first.name, second.name, docs.name, plain.name])
        self.assertEqual(self.status_of(left), 'queued')

    def test_a_first_task_with_no_topic_keeps_the_plain_line(self) -> None:
        first = self.queue(30, None, priority='9')
        docs = self.queue(31, 'docs', priority='8')
        khayyam = self.queue(32, 'khayyam', priority='7')
        taken, text = self.claims(3)
        self.assertEqual(taken, [first.name, docs.name, khayyam.name])
        self.assertNotIn('batch topic', text)

    def test_topic_names_the_topic_instead_of_the_first_task(self) -> None:
        self.queue(40, 'docs', priority='10')
        a = self.queue(41, 'khayyam', priority='3')
        b = self.queue(42, 'khayyam', priority='4')
        taken, text = self.claims(5, topic='Khayyam')
        self.assertEqual(taken, [b.name, a.name])
        self.assertIn('batch topic: khayyam', text)

    def test_topic_with_nothing_queued_under_it_takes_nothing_unless_fill(self) -> None:
        docs = self.queue(50, 'docs')
        taken, text = self.claims(2, topic='khayyam')
        self.assertEqual(taken, [])
        self.assertIn('no queued task', text)
        self.assertEqual(self.status_of(docs), 'queued')
        taken, _ = self.claims(2, topic='khayyam', fill=True)
        self.assertEqual(taken, [docs.name])

    def test_the_output_states_the_batch_topic_and_what_waits_under_it(self) -> None:
        self.queue(60, 'khayyam', priority='9')
        self.queue(61, 'khayyam', priority='8')
        self.queue(62, 'khayyam', priority='7')
        self.queue(63, 'khayyam', priority='6')
        _, text = self.claims(2)
        self.assertIn('batch topic: khayyam', text)
        self.assertIn('2 of 2 asked', text)
        self.assertIn('2 more queued under it', text)

    def test_the_output_lists_higher_priority_tasks_passed_over(self) -> None:
        self.queue(70, 'khayyam', priority='9')
        high = self.queue(71, 'docs', priority='8')
        mid = self.queue(72, None, priority='6')
        self.queue(73, 'khayyam', priority='2')
        level = self.queue(74, 'docs', priority='2')
        _, text = self.claims(2)
        passed = [line for line in text.splitlines() if line.startswith('passed over for topic')]
        self.assertEqual(len(passed), 1)
        self.assertIn(high.name, passed[0])
        self.assertIn(mid.name, passed[0])
        self.assertNotIn(level.name, passed[0])

    def test_nothing_is_said_of_passing_over_when_nothing_was(self) -> None:
        self.queue(80, 'khayyam', priority='9')
        self.queue(81, 'khayyam', priority='8')
        self.queue(82, 'docs', priority='1')
        _, text = self.claims(2)
        self.assertNotIn('passed over for topic', text)

    def test_a_first_task_another_caller_won_hands_the_topic_to_the_next(self) -> None:
        held = self.queue(90, 'khayyam', priority='10')
        (held / Claim.NAME).write_text('claimed: now\n', encoding='utf-8')
        docs = self.queue(91, 'docs', priority='9')
        other = self.queue(92, 'khayyam', priority='8')
        mine = self.queue(93, 'docs', priority='1')
        taken, _ = self.claims(3)
        self.assertEqual(taken, [docs.name, mine.name])
        self.assertEqual(self.status_of(other), 'queued')

    def test_a_task_with_two_topics_is_in_the_batch_of_either(self) -> None:
        both = self.task('20261013T000197Z-1-0', 'queued', topic=('docs', 'khayyam'), priority='9')
        other = self.queue(1, 'khayyam', priority='5')
        taken, text = self.claims(5, topic='khayyam')
        self.assertEqual(sorted(taken), sorted([both.name, other.name]))
        self.assertIn('batch topic: khayyam', text)

    def test_the_batch_flag_takes_a_topic_label_and_refuses_another_kind(self) -> None:
        self.assertEqual(task_claims.batch_topic('Topic=Khayyam LSP'), 'khayyam-lsp')
        self.assertIsNone(task_claims.batch_topic(None))
        with self.assertRaises(SystemExit) as refused:
            task_claims.batch_topic('TaskKind=design')
        self.assertIn('a batch is of one topic', str(refused.exception.code))

    def test_a_task_whose_request_is_empty_never_sets_the_topic(self) -> None:
        self.task('20261013T000195Z-1-0', 'queued', topic='docs', priority='10', request='')
        first = self.queue(96, 'khayyam', priority='5')
        self.queue(97, 'docs', priority='4')
        taken, _ = self.claims(2)
        self.assertEqual(taken, [first.name])
if __name__ == '__main__':
    unittest.main()
