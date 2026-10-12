#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for taking the N queued sessions first in line, in `services/session_claims.py`.

    python .agents/scripts/services/tests/session_claims.py

The subject is `claims N` — how the queued sessions first in line come to be
owned by exactly one agent each, each taken the way `claim` takes one
(`session_claim.py` here tests that) — named for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).
The design it holds is the parent plan's, session 20261012T134849Z-25068-0,
"Design", as the owner's rulings of 2026-10-12, recorded in session
20261012T153414Z-28656-0, rework it: no runner and no launch; `claims N` takes
the N queued sessions first in line, the highest priority first and the oldest
opened first among equals. The owner's ruling recorded in session
20261012T163251Z-25244-0 makes the project required: no default, no all.

Nothing here writes outside its scratch folder: the Memar root the services
resolve is patched onto one, made under the folder `machine/fs_test_scratch.py`
names. The concurrent claims run two real processes, each importing the
service with the same root patched in, so the race is the operating system's.

What is pinned, and what each pin is for:

  ClaimsTakesN       `claims N` takes the N queued sessions first in line —
                     the highest priority first, the oldest opened first among
                     equals — and prints for each its id, title, priority,
                     plan, and brief; fewer queued than N is not an error; a
                     queued plan whose Request is empty is passed over;
                     --project is required, and without it `claims` refuses
                     saying one run serves one project; two projects' queued
                     sessions never mix; a session another
                     holds is passed over with why, on standard output and
                     nothing on standard error; N is at least 1; two
                     `claims` at once never take one session twice.
"""
from __future__ import annotations

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
SCRIPTS = TESTS.parent.parent
sys.path.insert(0, str(SCRIPTS))
sys.dont_write_bytecode = True

from machine.fs_test_scratch import suite_scratch

import machine.fs_memar as memar_fs
import services.session_brief as session_brief
import services.session_claim as session_claim
import services.session_claims as session_claims
import services.session_new as session_new
import services.session_plan as session_plan


def plan_text(
    status: str,
    request: str = "Do the thing.",
    title: str = "T",
    opened: str = "2026-10-12T00:00:00Z",
    priority: str | None = None,
    project: str = "P",
) -> str:
    ranked = f"priority: {priority}\n" if priority is not None else ""
    return (
        f"---\ntitle: {title}\nopened: {opened}\nproject: {project}\n{ranked}---\n# {title}\n"
        f"Status: {status}\n\n## Request\n{request}\n\n## Why\n\n## Steps\n\n## Next\n"
    )


class Fixture(unittest.TestCase):
    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.fake_root = Path(self.scratch.name)
        patched = unittest.mock.patch.object(memar_fs, "memar_root", return_value=self.fake_root)
        patched.start()
        self.addCleanup(patched.stop)
        project = unittest.mock.patch.object(session_new, "project_root", return_value=self.fake_root)
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


class ClaimsTakesN(Fixture):
    def setUp(self) -> None:
        super().setUp()
        self.project = self.git_project("project-x")

    def git_project(self, name: str) -> Path:
        folder = self.fake_root / name
        folder.mkdir()
        subprocess.run(["git", "init", "-q", str(folder)], check=True, capture_output=True)
        return folder

    def session(self, sid: str, status: str, **plan) -> Path:
        plan.setdefault("project", str(self.project))
        return super().session(sid, status, **plan)

    def claims(self, count: int, project: Path | None = None) -> tuple[list[str], str]:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            taken = session_claims.claims(count, str(project or self.project))
        return taken, out.getvalue()

    def test_the_highest_priority_comes_first_and_the_oldest_among_equals(self) -> None:
        low = self.session("20261012T000040Z-1-0", "queued", opened="2026-10-12T00:00:00Z", priority="2")
        plain_old = self.session("20261012T000041Z-1-0", "queued", opened="2026-10-12T01:00:00Z")
        high = self.session("20261012T000042Z-1-0", "queued", opened="2026-10-12T05:00:00Z", priority="9")
        plain_new = self.session("20261012T000043Z-1-0", "queued", opened="2026-10-12T02:00:00Z", priority="5")
        self.session("20261012T000044Z-1-0", "open", opened="2026-10-11T00:00:00Z", priority="10")
        taken, _ = self.claims(3)
        self.assertEqual(taken, [high.name, plain_old.name, plain_new.name])
        self.assertEqual(self.status_of(low), "queued")
        for folder in (high, plain_old, plain_new):
            self.assertEqual(self.status_of(folder), "open")
            self.assertTrue((folder / session_claim.CLAIM_NAME).is_file())

    def test_each_taken_session_is_printed_with_what_hands_it_over(self) -> None:
        folder = self.session("20261012T000045Z-1-0", "queued", title="Write the parser", priority="7")
        taken, text = self.claims(1)
        self.assertEqual(taken, [folder.name])
        self.assertIn(f"{folder.name}  Write the parser", text)
        self.assertIn("priority: 7", text)
        self.assertIn(f"plan: {folder / session_plan.PLAN_NAME}", text)
        self.assertIn(f"brief: {session_brief.brief_text(folder.name)}", text)

    def test_fewer_queued_than_asked_is_not_an_error(self) -> None:
        one = self.session("20261012T000046Z-1-0", "queued")
        taken, text = self.claims(5)
        self.assertEqual(taken, [one.name])
        self.assertIn("1 of 5", text)
        taken, text = self.claims(5)
        self.assertEqual(taken, [])
        self.assertIn("no queued session", text)

    def test_a_queued_plan_with_an_empty_request_is_passed_over(self) -> None:
        unwritten = self.session("20261012T000047Z-1-0", "queued", request="", priority="10")
        written = self.session("20261012T000048Z-1-0", "queued")
        taken, text = self.claims(2)
        self.assertEqual(taken, [written.name])
        self.assertEqual(self.status_of(unwritten), "queued")
        self.assertIn(f"{unwritten.name}  not ready", text)

    def test_a_missing_project_is_refused_saying_one_run_serves_one_project(self) -> None:
        waiting = self.session("20261012T000049Z-1-0", "queued")
        why = self.refused(session_claims.claims, 5, None)
        self.assertIn("--project", why)
        self.assertIn("one run serves one project", why)
        self.assertIn("ask the owner", why)
        self.assertEqual(self.status_of(waiting), "queued")
        self.assertFalse((waiting / session_claim.CLAIM_NAME).exists())

    def test_two_projects_queued_sessions_never_mix(self) -> None:
        other_project = self.git_project("project-y")
        theirs = self.session("20261012T000049Z-1-0", "queued", priority="10", project=str(other_project))
        unnamed = self.session("20261012T000036Z-1-0", "queued", priority="10", project="P")
        mine = self.session("20261012T000039Z-1-0", "queued")
        taken, _ = self.claims(5)
        self.assertEqual(taken, [mine.name])
        self.assertEqual(self.status_of(theirs), "queued")
        self.assertEqual(self.status_of(unnamed), "queued")
        taken, _ = self.claims(5, other_project)
        self.assertEqual(taken, [theirs.name])
        self.assertEqual(self.status_of(unnamed), "queued")

    def test_a_session_another_holds_is_passed_over_saying_why_and_nothing_on_stderr(self) -> None:
        # The moment between the listing and the claim: queued, and already claimed by another.
        held = self.session("20261012T000038Z-1-0", "queued", priority="10")
        (held / session_claim.CLAIM_NAME).write_text("claimed: now\n", encoding="utf-8")
        free = self.session("20261012T000037Z-1-0", "queued")
        errors = io.StringIO()
        with contextlib.redirect_stderr(errors):
            taken, text = self.claims(2)
        self.assertEqual(taken, [free.name])
        self.assertIn(f"{held.name}  not taken: ", text)
        self.assertIn("claimed by another agent", text)
        self.assertEqual(errors.getvalue(), "")
        self.assertEqual(self.status_of(held), "queued")

    def test_n_is_at_least_one(self) -> None:
        for count in (0, -1):
            with self.subTest(count=count):
                self.assertIn("at least 1", self.refused(session_claims.claims, count, str(self.project)))

    def test_two_claims_at_once_never_take_one_session_twice(self) -> None:
        folders = [self.session(f"20261012T00005{index}Z-1-0", "queued") for index in range(5)]
        start = time.time() + 2.0
        script = (
            "import sys, time, json, contextlib, io; sys.path.insert(0, sys.argv[1]); sys.dont_write_bytecode = True\n"
            "from pathlib import Path\n"
            "import machine.fs_memar as m\n"
            "m.memar_root = lambda: Path(sys.argv[2])\n"
            "import services.session_claims as c\n"
            "while time.time() < float(sys.argv[3]): pass\n"
            "with contextlib.redirect_stdout(io.StringIO()): taken = c.claims(4, sys.argv[4])\n"
            "print(json.dumps(taken))\n"
        )
        racers = [
            subprocess.Popen(
                [sys.executable, "-c", script, str(SCRIPTS), str(self.fake_root), str(start), str(self.project)],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            for _ in range(2)
        ]
        results = []
        for racer in racers:
            out, err = racer.communicate(timeout=120)
            self.assertEqual(racer.returncode, 0, err.decode("utf-8", "replace"))
            results.append(json.loads(out.decode("utf-8").strip().splitlines()[-1]))
        every = results[0] + results[1]
        self.assertEqual(len(every), len(set(every)))
        self.assertEqual(sorted(every), sorted(folder.name for folder in folders))
        for folder in folders:
            self.assertEqual(self.status_of(folder), "open")


if __name__ == "__main__":
    unittest.main()
