#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for queuing a session and claiming it by its id, in `services/session_claim.py`.

    python .agents/scripts/services/tests/session_claim.py

The subject is the claim — how a session that is planned but owned by no one
(`queued`) comes to be owned by exactly one agent (`open`), by its id — named
for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).
The design it holds is the parent plan's, session 20261012T134849Z-25068-0,
"Design", as the owner's rulings of 2026-10-12, recorded in session
20261012T153414Z-28656-0, rework it: no runner and no launch; nothing keeps a
claim fresh, so one lapses only after a day. Taking the N first in line is
`services/session_claims.py`'s, and its tests are `session_claims.py` here.

Nothing here writes outside its scratch folder: the Memar root the services
resolve is patched onto one, made under the folder `machine/fs_test_scratch.py`
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
                     refuses a session that is open without a claim, done, or
                     already claimed; a claim lapses only after a day, since
                     nothing refreshes it, and a lapsed one is taken over; two
                     claims at once on one session yield exactly one winner,
                     and so do two takers over one stale claim; trying a claim
                     says why one was not taken rather than failing.
"""
from __future__ import annotations

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
SCRIPTS = TESTS.parent.parent
sys.path.insert(0, str(SCRIPTS))
sys.dont_write_bytecode = True

from machine.fs_test_scratch import suite_scratch

import machine.fs_memar as memar_fs
import services.session_claim as session_claim
from services.claim import Claim
import services.session_find as session_find
import services.session_temp as session_temp
import services.session_ensure as session_ensure
import services.session_plan as session_plan
from services.priority import Priority
import services.session_report as session_report
from services.status import Kind, Status


def plan_text(
    status: str,
    request: str = "Do the thing.",
    title: str = "T",
    opened: str = "2026-10-12T00:00:00Z",
    priority: str | None = None,
) -> str:
    ranked = f"Priority: {priority}\n" if priority is not None else ""
    return (
        f"---\nTitle: {title}\nStatus: {status.capitalize()}\nOpened: {opened}\nProject: P\n{ranked}---\n# {title}\n"
        f"\n## Request\n{request}\n\n## Why\n\n## Steps\n\n## Next\n"
    )


class Fixture(unittest.TestCase):
    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.fake_root = Path(self.scratch.name)
        patched = unittest.mock.patch.object(memar_fs, "memar_root", return_value=self.fake_root)
        patched.start()
        self.addCleanup(patched.stop)
        project = unittest.mock.patch.object(session_ensure, "project_root", return_value=self.fake_root)
        project.start()
        self.addCleanup(project.stop)

    def session(self, sid: str, status: str, **plan) -> Path:
        folder = memar_fs.session_dir(sid)
        folder.mkdir(parents=True)
        (folder / session_plan.PLAN_NAME).write_text(plan_text(status, **plan), encoding="utf-8", newline="\n")
        return folder

    def status_of(self, folder: Path) -> str:
        return session_plan.read_plan(folder / session_plan.PLAN_NAME).status

    def refused(self, call, *args) -> str:
        with self.assertRaises(SystemExit) as raised:
            call(*args)
        return str(raised.exception.code)


class QueuedIsAStatus(Fixture):
    def test_a_queued_plan_reads_as_queued_and_is_listed_by_that_status(self) -> None:
        folder = self.session("20261012T000001Z-1-0", "queued")
        self.session("20261012T000002Z-1-0", "active")
        self.assertEqual(self.status_of(folder), "queued")
        self.assertIn("queued", Status.keys(Kind.SESSION_PLAN))
        found = [session.id for session in session_find.find_sessions(status="queued")]
        self.assertEqual(found, [folder.name])
        self.assertIsNone(session_report.disagreement("queued", ""))

    def test_new_queued_writes_a_new_plan_queued(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()):
            sid, path = session_ensure.ensure_session(None, "Queued task", None, queued=True, project=str(self.fake_root))
        self.assertEqual(self.status_of(path), "queued")
        self.assertEqual(Priority.of(session_plan.read_plan(path / session_plan.PLAN_NAME).front), 5)

    def test_new_queued_with_a_priority_records_it(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()):
            sid, path = session_ensure.ensure_session(None, "Urgent task", None, queued=True, priority=9, project=str(self.fake_root))
        front = session_plan.read_plan(path / session_plan.PLAN_NAME).front
        self.assertEqual(Priority.of(front), 9)
        self.assertEqual(self.status_of(path), "queued")

    def test_new_queued_queues_an_open_plan_no_one_has_claimed(self) -> None:
        folder = self.session("20261012T000003Z-1-0", "active")
        with contextlib.redirect_stdout(io.StringIO()):
            session_ensure.ensure_session(folder.name, None, None, queued=True)
            session_ensure.ensure_session(folder.name, None, None, queued=True)
        self.assertEqual(self.status_of(folder), "queued")
        # The rest of the plan is kept as written.
        self.assertIn("Do the thing.", (folder / session_plan.PLAN_NAME).read_text(encoding="utf-8"))

    def test_new_queued_refuses_a_done_or_claimed_session(self) -> None:
        done = self.session("20261012T000004Z-1-0", "complete")
        self.assertIn("complete", self.refused(session_ensure.ensure_session, done.name, None, None, True))
        claimed = self.session("20261012T000005Z-1-0", "queued")
        session_claim.claim_folder(claimed)
        self.assertIn("claimed", self.refused(session_ensure.ensure_session, claimed.name, None, None, True))


class ClaimTakesOne(Fixture):
    def test_a_claim_moves_queued_to_open_and_leaves_a_claim_file(self) -> None:
        folder = self.session("20261012T000010Z-1-0", "queued")
        session_claim.claim_folder(folder)
        self.assertEqual(self.status_of(folder), "active")
        self.assertTrue((folder / Claim.NAME).is_file())

    def test_a_claim_leaves_the_rest_of_the_plan_and_a_plan_in_an_earlier_shape_is_refused_naming_the_script(self) -> None:
        folder = self.session("20261012T000012Z-1-0", "queued")
        plan = folder / session_plan.PLAN_NAME
        before = plan.read_text(encoding="utf-8")
        session_claim.claim_folder(folder)
        self.assertEqual(plan.read_text(encoding="utf-8"), before.replace("Status: Queued", "Status: Active"))
        old = self.session("20261012T000013Z-1-0", "queued")
        old_plan = old / session_plan.PLAN_NAME
        old_plan.write_text(
            "---\ntitle: T\nopened: 2026-10-12T00:00:00Z\nproject: P\n---\n# T\nStatus: queued\n\n## Request\n",
            encoding="utf-8",
            newline="\n",
        )
        written = old_plan.read_bytes()
        self.assertIn(session_plan.EARLIER_SHAPE_REMEDY, self.refused(session_claim.claim_folder, old))
        self.assertIn(session_plan.EARLIER_SHAPE_REMEDY, session_claim.try_claim(old))
        self.assertEqual(old_plan.read_bytes(), written)
        self.assertFalse((old / Claim.NAME).exists())

    def test_the_claim_verb_claims_by_id(self) -> None:
        folder = self.session("20261012T000011Z-1-0", "queued")
        with contextlib.redirect_stdout(io.StringIO()) as out:
            session_claim.claim(folder.name)
        self.assertIn(folder.name, out.getvalue())
        self.assertIn(session_temp.TEMP_SENTENCE, out.getvalue())
        self.assertEqual(self.status_of(folder), "active")

    def test_a_claim_refuses_a_session_that_is_not_queued(self) -> None:
        for index, (status, read) in enumerate((("active", "active"), ("blocked", "blocked"), ("complete", "complete"))):
            with self.subTest(status=status):
                folder = self.session(f"20261012T00002{index}Z-1-0", status)
                self.assertIn("not queued", self.refused(session_claim.claim_folder, folder))
                self.assertEqual(self.status_of(folder), read)

    def test_a_claim_refuses_a_session_already_claimed(self) -> None:
        folder = self.session("20261012T000030Z-1-0", "queued")
        session_claim.claim_folder(folder)
        self.assertIn("claimed", self.refused(session_claim.claim_folder, folder))

    def test_trying_a_claim_says_why_it_was_not_taken_and_does_not_fail(self) -> None:
        folder = self.session("20261012T000035Z-1-0", "queued")
        self.assertIsNone(session_claim.try_claim(folder))
        self.assertIn("claimed", session_claim.try_claim(folder))
        done = self.session("20261012T000036Z-1-0", "complete")
        self.assertIn("not queued", session_claim.try_claim(done))

    def test_a_stale_claim_is_taken_over(self) -> None:
        folder = self.session("20261012T000031Z-1-0", "queued")
        session_claim.claim_folder(folder)
        old = time.time() - Claim.STALE_SECONDS - 60
        os.utime(folder / Claim.NAME, (old, old))
        session_claim.claim_folder(folder)
        self.assertEqual(self.status_of(folder), "active")
        self.assertGreater((folder / Claim.NAME).stat().st_mtime, old + 60)

    def test_a_claim_lapses_only_after_a_day(self) -> None:
        self.assertEqual(Claim.STALE_SECONDS, 24 * 60 * 60)
        folder = self.session("20261012T000032Z-1-0", "queued")
        session_claim.claim_folder(folder)
        hours_ago = time.time() - 23 * 60 * 60
        os.utime(folder / Claim.NAME, (hours_ago, hours_ago))
        self.assertTrue(session_claim.is_claimed(folder))

    def test_two_claims_at_once_yield_exactly_one_winner(self) -> None:
        folder = self.session("20261012T000033Z-1-0", "queued")
        start = time.time() + 1.5
        script = (
            "import sys, time; sys.path.insert(0, sys.argv[1]); sys.dont_write_bytecode = True\n"
            "from pathlib import Path\n"
            "import services.session_claim as c\n"
            "while time.time() < float(sys.argv[3]): pass\n"
            "c.claim_folder(Path(sys.argv[2]))\n"
        )
        racers = [
            subprocess.Popen(
                [sys.executable, "-c", script, str(SCRIPTS), str(folder), str(start)],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            for _ in range(2)
        ]
        codes = sorted(racer.wait(timeout=60) for racer in racers)
        for racer in racers:
            racer.stdout.close()
            racer.stderr.close()
        self.assertEqual(codes[0], 0)
        self.assertNotEqual(codes[1], 0)
        self.assertEqual(self.status_of(folder), "active")

    def test_two_takers_over_one_stale_claim_yield_exactly_one_winner(self) -> None:
        # Two real processes, paced by signal files at the moments a takeover
        # race turns on: the first has read the claim as stale; the second
        # takes the stale claim over and is about to create its own; the first
        # is about to drop what it still reads as the stale claim. A takeover
        # that let go before its new claim existed let the first drop the
        # second's fresh claim, and both won.
        folder = self.session("20261012T000034Z-1-0", "queued")
        claim = folder / Claim.NAME
        claim.write_text("claimed: long ago\n", encoding="utf-8")
        old = time.time() - Claim.STALE_SECONDS - 60
        os.utime(claim, (old, old))
        signals = Path(self.scratch.name) / "signals"
        signals.mkdir()
        racers = [
            subprocess.Popen(
                [sys.executable, "-c", PACED_TAKER, str(SCRIPTS), str(folder), str(signals), role],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            for role in ("first", "second")
        ]
        codes = [racer.wait(timeout=60) for racer in racers]
        for racer in racers:
            racer.stdout.close()
            racer.stderr.close()
        self.assertEqual(sorted(code == 0 for code in codes), [False, True], f"exit codes {codes}")
        self.assertEqual(self.status_of(folder), "active")


# One taker of a stale claim, paced by files in a signals folder (see the test
# above). Each wait is bounded, so a taker the other's pacing never reaches
# goes on alone.
PACED_TAKER = r"""
import pathlib, sys, time
sys.path.insert(0, sys.argv[1]); sys.dont_write_bytecode = True
import services.session_claim as c
from services.claim import Claim
folder, signals, role = pathlib.Path(sys.argv[2]), pathlib.Path(sys.argv[3]), sys.argv[4]

def signal(name):
    (signals / name).touch()

def wait(name, seconds=3.0):
    deadline = time.time() + seconds
    while not (signals / name).exists() and time.time() < deadline:
        time.sleep(0.01)

real_open, real_unlink, real_is_claimed = pathlib.Path.open, pathlib.Path.unlink, c.is_claimed
if role == "first":
    seen = []
    def is_claimed(f):
        answer = real_is_claimed(f)
        if not seen:
            seen.append(answer)
            signal("first_saw_stale")
            wait("second_creating")
        return answer
    def unlink(self, *args, **kwargs):
        if self.name == Claim.NAME:
            signal("first_unlinking")
            wait("second_created")
        return real_unlink(self, *args, **kwargs)
    c.is_claimed = is_claimed
    pathlib.Path.unlink = unlink
else:
    wait("first_saw_stale")
    def open_(self, mode="r", *args, **kwargs):
        if self.name == Claim.NAME and "x" in mode:
            signal("second_creating")
            wait("first_unlinking")
            try:
                return real_open(self, mode, *args, **kwargs)
            finally:
                signal("second_created")
        return real_open(self, mode, *args, **kwargs)
    pathlib.Path.open = open_
c.claim_folder(folder)
"""


if __name__ == "__main__":
    unittest.main()
