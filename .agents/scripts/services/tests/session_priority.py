#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for changing a session's priority, in `services/session_priority.py`.

    python .agents/scripts/services/tests/session_priority.py

The subject is `memar session priority ID N` — anyone, a person or an agent,
moving a session up or down the line `claims` takes from — named for the file
that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).
The ruling it holds is the owner's of 2026-10-12, recorded in session
20261012T153414Z-28656-0: a priority is 1 to 10, 5 when absent, higher sooner,
and anyone may change it.

Nothing here writes outside its scratch folder: the Memar root the services
resolve is patched onto one, made under the folder `machine/fs_test_scratch.py`
names.

What is pinned, and what each pin is for:

  SetPriority     The verb writes N into the session's plan and says what it
                  was and is now, whatever the session's status; the plan's
                  status and the rest of it are kept; N outside 1 to 10, or a
                  session that is not there, is refused and nothing changes.
"""
from __future__ import annotations

import contextlib
import io
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path

TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parent.parent
sys.path.insert(0, str(SCRIPTS))
sys.dont_write_bytecode = True

from machine.fs_test_scratch import suite_scratch

import machine.fs_memar as memar_fs
import services.session_plan as session_plan
import services.session_priority as session_priority


class SetPriority(unittest.TestCase):
    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        patched = unittest.mock.patch.object(memar_fs, "memar_root", return_value=Path(self.scratch.name))
        patched.start()
        self.addCleanup(patched.stop)

    def session(self, sid: str, status: str) -> Path:
        folder = memar_fs.session_dir(sid)
        folder.mkdir(parents=True)
        (folder / session_plan.PLAN_NAME).write_text(
            f"---\ntitle: T\nopened: 2026-10-12T00:00:00Z\nproject: P\n---\n# T\nStatus: {status}\n\n## Request\nx\n",
            encoding="utf-8",
            newline="\n",
        )
        return folder

    def plan(self, folder: Path) -> session_plan.Plan:
        return session_plan.read_plan(folder / session_plan.PLAN_NAME)

    def test_the_verb_writes_the_priority_and_says_what_it_was(self) -> None:
        for index, status in enumerate(("queued", "open", "blocked")):
            with self.subTest(status=status):
                folder = self.session(f"20261012T06000{index}Z-1-0", status)
                out = io.StringIO()
                with contextlib.redirect_stdout(out):
                    session_priority.set_session_priority(folder.name, "8")
                self.assertIn(f"{folder.name}  priority 8, was 5", out.getvalue())
                plan = self.plan(folder)
                self.assertEqual(session_plan.priority_of(plan.front), 8)
                self.assertEqual(plan.status, status)
                self.assertEqual(plan.front["title"], "T")

    def test_a_priority_outside_1_to_10_or_a_missing_session_is_refused(self) -> None:
        folder = self.session("20261012T060010Z-1-0", "queued")
        before = (folder / session_plan.PLAN_NAME).read_bytes()
        for value in ("0", "11", "soon"):
            with self.subTest(value=value):
                with self.assertRaises(SystemExit):
                    session_priority.set_session_priority(folder.name, value)
        self.assertEqual((folder / session_plan.PLAN_NAME).read_bytes(), before)
        with self.assertRaises(SystemExit):
            session_priority.set_session_priority("20261012T060011Z-1-0", "3")


if __name__ == "__main__":
    unittest.main()
