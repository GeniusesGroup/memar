#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for queuing a task and claiming it by its id, in `modules-plugable/management/task/services/claim.py`.

    python modules-plugable/management/task/tests/claim.py

The subject is the claim — how a task that is planned but owned by no one
(`queued`) comes to be owned by exactly one agent (`open`), by its id — named
for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).
The design it holds is the parent plan's, task 20261012T134849Z-25068-0,
"Design", as the owner's rulings of 2026-10-12, recorded in task
20261012T153414Z-28656-0, rework it: no runner and no launch; nothing keeps a
claim fresh, so one lapses only after a day. Taking the N first in line is
`modules-plugable/management/task/services/claims.py`'s, and its tests are `task_claims.py` here.

Nothing here writes outside its scratch folder: the Memar root the services
resolve is patched onto one, made under the folder `modules-plugable/computer/memory/filesystem/services/fs_test_scratch.py`
names. The concurrent claims run two real processes, each importing the
service with the same root patched in, so the race is the operating system's.

What is pinned, and what each pin is for:

  QueuedIsAStatus    A plan whose Status is queued reads as queued, `list
                     --status queued` finds it, and its report disagrees with
                     nothing yet; `new --queued` writes a new plan queued, with
                     its priority when one is given, queues an existing open
                     plan no one has claimed, and refuses one that is done or
                     claimed.
  ClaimTakesOne      A claim moves queued to open and leaves a claim file; it
                     refuses a task that is open without a claim, done, or
                     already claimed; a claim lapses only after a day, since
                     nothing refreshes it, and a lapsed one is taken over; two
                     claims at once on one task yield exactly one winner,
                     and so do two takers over one stale claim; trying a claim
                     says why one was not taken rather than failing.
"""
from __future__ import annotations
from importlib import import_module
from machine.plugable_import import load as plugable_load
_m_fs_test_scratch = plugable_load('computer.memory.filesystem.services.fs_test_scratch')
suite_scratch = _m_fs_test_scratch.suite_scratch
_m_fs_memar = plugable_load('computer.memory.filesystem.services.fs_memar')
memar_fs = _m_fs_memar
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
SCRIPTS = next(p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()) / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
task_claim = import_module('modules-plugable.management.task.services.claim')
_m_claim = import_module('modules-plugable.management.task.primitive.claim')
Claim = _m_claim.Claim
task_find = import_module('modules-plugable.management.task.services.list')
task_temp = import_module('modules-plugable.management.task.services.temp')
task_ensure = import_module('modules-plugable.management.task.services.ensure')
task_plan = import_module('modules-plugable.management.task.services.plan_file')
_m_priority = import_module('modules-plugable.knowledge.documentation.plan.primitive.priority')
Priority = _m_priority.Priority
task_report = import_module('modules-plugable.management.task.services.report_file')
from modules.knowledge.status.primitive.status import DocumentKind, Status

def plan_text(status: str, request: str='Do the thing.', title: str='T', opened: str='2026-10-12T00:00:00Z', priority: str | None=None) -> str:
    ranked = f'Priority: {priority}\n' if priority is not None else ''
    return f'---\nTitle: {title}\nStatus: {status.capitalize()}\nOpened: {opened}\nProject: P\n{ranked}---\n# {title}\n\n## Request\n{request}\n\n## Why\n\n## Steps\n\n## Next\n'

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

class QueuedIsAStatus(Fixture):

    def test_a_queued_plan_reads_as_queued_and_is_listed_by_that_status(self) -> None:
        folder = self.task('20261012T000001Z-1-0', 'queued')
        self.task('20261012T000002Z-1-0', 'active')
        self.assertEqual(self.status_of(folder), 'queued')
        self.assertIn('queued', Status.keys(DocumentKind.PLAN))
        found = [task.id for task in task_find.find_tasks(status='queued')]
        self.assertEqual(found, [folder.name])
        self.assertIsNone(task_report.disagreement('queued', ''))

    def test_new_queued_writes_a_new_plan_queued(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()):
            sid, path = task_ensure.ensure_task(None, 'Queued task', None, queued=True, project=str(self.fake_root))
        self.assertEqual(self.status_of(path), 'queued')
        self.assertEqual(Priority.of(task_plan.read_plan(path / task_plan.PLAN_NAME).front), 5)

    def test_new_queued_with_a_priority_records_it(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()):
            sid, path = task_ensure.ensure_task(None, 'Urgent task', None, queued=True, priority=9, project=str(self.fake_root))
        front = task_plan.read_plan(path / task_plan.PLAN_NAME).front
        self.assertEqual(Priority.of(front), 9)
        self.assertEqual(self.status_of(path), 'queued')

    def test_new_queued_queues_an_open_plan_no_one_has_claimed(self) -> None:
        folder = self.task('20261012T000003Z-1-0', 'active')
        with contextlib.redirect_stdout(io.StringIO()):
            task_ensure.ensure_task(folder.name, None, None, queued=True)
            task_ensure.ensure_task(folder.name, None, None, queued=True)
        self.assertEqual(self.status_of(folder), 'queued')
        self.assertIn('Do the thing.', (folder / task_plan.PLAN_NAME).read_text(encoding='utf-8'))

    def test_new_queued_refuses_a_done_or_claimed_task(self) -> None:
        done = self.task('20261012T000004Z-1-0', 'complete')
        self.assertIn('complete', self.refused(task_ensure.ensure_task, done.name, None, None, True))
        claimed = self.task('20261012T000005Z-1-0', 'queued')
        task_claim.claim_folder(claimed)
        self.assertIn('claimed', self.refused(task_ensure.ensure_task, claimed.name, None, None, True))

class ClaimTakesOne(Fixture):

    def test_a_claim_moves_queued_to_open_and_leaves_a_claim_file(self) -> None:
        folder = self.task('20261012T000010Z-1-0', 'queued')
        task_claim.claim_folder(folder)
        self.assertEqual(self.status_of(folder), 'active')
        self.assertTrue((folder / Claim.NAME).is_file())

    def test_a_claim_leaves_the_rest_of_the_plan_and_a_plan_in_an_earlier_shape_is_refused_naming_the_script(self) -> None:
        folder = self.task('20261012T000012Z-1-0', 'queued')
        plan = folder / task_plan.PLAN_NAME
        before = plan.read_text(encoding='utf-8')
        task_claim.claim_folder(folder)
        self.assertEqual(plan.read_text(encoding='utf-8'), before.replace('Status: Queued', 'Status: Active'))
        old = self.task('20261012T000013Z-1-0', 'queued')
        old_plan = old / task_plan.PLAN_NAME
        old_plan.write_text('---\ntitle: T\nopened: 2026-10-12T00:00:00Z\nproject: P\n---\n# T\nStatus: queued\n\n## Request\n', encoding='utf-8', newline='\n')
        written = old_plan.read_bytes()
        self.assertIn(task_plan.EARLIER_SHAPE_REMEDY, self.refused(task_claim.claim_folder, old))
        self.assertIn(task_plan.EARLIER_SHAPE_REMEDY, task_claim.try_claim(old))
        self.assertEqual(old_plan.read_bytes(), written)
        self.assertFalse((old / Claim.NAME).exists())

    def test_the_claim_verb_claims_by_id(self) -> None:
        folder = self.task('20261012T000011Z-1-0', 'queued')
        with contextlib.redirect_stdout(io.StringIO()) as out:
            task_claim.claim(folder.name)
        self.assertIn(folder.name, out.getvalue())
        self.assertIn(task_temp.TEMP_SENTENCE, out.getvalue())
        self.assertEqual(self.status_of(folder), 'active')

    def test_a_claim_refuses_a_task_that_is_not_queued(self) -> None:
        for index, (status, read) in enumerate((('active', 'active'), ('blocked', 'blocked'), ('complete', 'complete'))):
            with self.subTest(status=status):
                folder = self.task(f'20261012T00002{index}Z-1-0', status)
                self.assertIn('not queued', self.refused(task_claim.claim_folder, folder))
                self.assertEqual(self.status_of(folder), read)

    def test_a_claim_refuses_a_task_already_claimed(self) -> None:
        folder = self.task('20261012T000030Z-1-0', 'queued')
        task_claim.claim_folder(folder)
        self.assertIn('claimed', self.refused(task_claim.claim_folder, folder))

    def test_trying_a_claim_says_why_it_was_not_taken_and_does_not_fail(self) -> None:
        folder = self.task('20261012T000035Z-1-0', 'queued')
        self.assertIsNone(task_claim.try_claim(folder))
        self.assertIn('claimed', task_claim.try_claim(folder))
        done = self.task('20261012T000036Z-1-0', 'complete')
        self.assertIn('not queued', task_claim.try_claim(done))

    def test_a_stale_claim_is_taken_over(self) -> None:
        folder = self.task('20261012T000031Z-1-0', 'queued')
        task_claim.claim_folder(folder)
        old = time.time() - Claim.STALE_SECONDS - 60
        os.utime(folder / Claim.NAME, (old, old))
        task_claim.claim_folder(folder)
        self.assertEqual(self.status_of(folder), 'active')
        self.assertGreater((folder / Claim.NAME).stat().st_mtime, old + 60)

    def test_a_claim_lapses_only_after_a_day(self) -> None:
        self.assertEqual(Claim.STALE_SECONDS, 24 * 60 * 60)
        folder = self.task('20261012T000032Z-1-0', 'queued')
        task_claim.claim_folder(folder)
        hours_ago = time.time() - 23 * 60 * 60
        os.utime(folder / Claim.NAME, (hours_ago, hours_ago))
        self.assertTrue(task_claim.is_claimed(folder))

    def test_two_claims_at_once_yield_exactly_one_winner(self) -> None:
        folder = self.task('20261012T000033Z-1-0', 'queued')
        start = time.time() + 1.5
        script = "import sys, time; sys.path.insert(0, sys.argv[1]); sys.path.insert(1, __import__('os').path.dirname(__import__('os').path.dirname(sys.argv[1]))); sys.dont_write_bytecode = True\nfrom pathlib import Path\nimport importlib; c = importlib.import_module('modules-plugable.management.task.services.claim')\nwhile time.time() < float(sys.argv[3]): pass\nc.claim_folder(Path(sys.argv[2]))\n"
        racers = [subprocess.Popen([sys.executable, '-c', script, str(SCRIPTS), str(folder), str(start)], stdout=subprocess.PIPE, stderr=subprocess.PIPE) for _ in range(2)]
        codes = sorted((racer.wait(timeout=60) for racer in racers))
        for racer in racers:
            racer.stdout.close()
            racer.stderr.close()
        self.assertEqual(codes[0], 0)
        self.assertNotEqual(codes[1], 0)
        self.assertEqual(self.status_of(folder), 'active')

    def test_two_takers_over_one_stale_claim_yield_exactly_one_winner(self) -> None:
        folder = self.task('20261012T000034Z-1-0', 'queued')
        claim = folder / Claim.NAME
        claim.write_text('claimed: long ago\n', encoding='utf-8')
        old = time.time() - Claim.STALE_SECONDS - 60
        os.utime(claim, (old, old))
        signals = Path(self.scratch.name) / 'signals'
        signals.mkdir()
        racers = [subprocess.Popen([sys.executable, '-c', PACED_TAKER, str(SCRIPTS), str(folder), str(signals), role], stdout=subprocess.PIPE, stderr=subprocess.PIPE) for role in ('first', 'second')]
        codes = [racer.wait(timeout=60) for racer in racers]
        for racer in racers:
            racer.stdout.close()
            racer.stderr.close()
        self.assertEqual(sorted((code == 0 for code in codes)), [False, True], f'exit codes {codes}')
        self.assertEqual(self.status_of(folder), 'active')
PACED_TAKER = '\nimport pathlib, sys, time\nsys.path.insert(0, sys.argv[1]); sys.path.insert(1, __import__(\'os\').path.dirname(__import__(\'os\').path.dirname(sys.argv[1]))); sys.dont_write_bytecode = True\nimport importlib; c = importlib.import_module(\'modules-plugable.management.task.services.claim\')\nClaim = importlib.import_module(\'modules-plugable.management.task.primitive.claim\').Claim\nfolder, signals, role = pathlib.Path(sys.argv[2]), pathlib.Path(sys.argv[3]), sys.argv[4]\n\ndef signal(name):\n    (signals / name).touch()\n\ndef wait(name, seconds=3.0):\n    deadline = time.time() + seconds\n    while not (signals / name).exists() and time.time() < deadline:\n        time.sleep(0.01)\n\nreal_open, real_unlink, real_is_claimed = pathlib.Path.open, pathlib.Path.unlink, c.is_claimed\nif role == "first":\n    seen = []\n    def is_claimed(f):\n        answer = real_is_claimed(f)\n        if not seen:\n            seen.append(answer)\n            signal("first_saw_stale")\n            wait("second_creating")\n        return answer\n    def unlink(self, *args, **kwargs):\n        if self.name == Claim.NAME:\n            signal("first_unlinking")\n            wait("second_created")\n        return real_unlink(self, *args, **kwargs)\n    c.is_claimed = is_claimed\n    pathlib.Path.unlink = unlink\nelse:\n    wait("first_saw_stale")\n    def open_(self, mode="r", *args, **kwargs):\n        if self.name == Claim.NAME and "x" in mode:\n            signal("second_creating")\n            wait("first_unlinking")\n            try:\n                return real_open(self, mode, *args, **kwargs)\n            finally:\n                signal("second_created")\n        return real_open(self, mode, *args, **kwargs)\n    pathlib.Path.open = open_\nc.claim_folder(folder)\n'
if __name__ == '__main__':
    unittest.main()
