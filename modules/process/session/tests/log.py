#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the session log in `modules/process/session/services/log.py`.

    python modules/process/session/tests/log.py

The subject is the log a person reads for a folder that is gone, named for the
file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes outside its scratch folder: the Memar root is patched onto
one, made under the folder `machine/fs_test_scratch.py` names, and removed
again.

What is pinned, and what each pin is for:

  OneLinePerEvent  Each event is appended as one tab-separated line — time,
                   event, id, detail — in UTF-8 with LF, beside the session
                   folders; a log that cannot be written warns and does not
                   stop what was being done. Each location keeps its own
                   log in its root: a session in a project's own location
                   is recorded there, one in Memar's own or left in temp/
                   in Memar's. Which events are recorded is pinned by the
                   suites of the services that record them.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import contextlib
import io
import sys
import tempfile
import unittest
import unittest.mock
from datetime import datetime
from pathlib import Path

TESTS = Path(__file__).resolve().parent
# This suite lives in the `tests/` folder of the shelf that owns its subject, so
# the scripts folder is two levels up. Running a file puts its OWN folder on the
# module search path and not its parent's, which is the one line this needs and
# the reason it carries one.
SCRIPTS = TESTS.parents[3] / ".agents" / "scripts"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))  # the checkout's top, where `modules/` is imported from
sys.dont_write_bytecode = True

from machine.fs_test_scratch import suite_scratch

import machine.fs_memar as memar_fs
import modules.process.session.services.log as session_log


class OneLinePerEvent(unittest.TestCase):
    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.fake_root = Path(self.scratch.name)
        patched = unittest.mock.patch.object(memar_fs, "memar_root", return_value=self.fake_root)
        patched.start()
        self.addCleanup(patched.stop)

    def test_each_event_is_one_tab_separated_line_beside_the_folders(self) -> None:
        session_log.record("opened", "s-1")
        session_log.record("reaped", "s-2", "idle 8.0 days")
        log = session_log.log_path()
        self.assertEqual(log.parent, memar_fs.session_dir("s-1").parent)
        raw = log.read_bytes()
        self.assertNotIn(b"\r", raw)
        lines = [line.split("\t") for line in raw.decode("utf-8").splitlines()]
        self.assertEqual([line[1:] for line in lines], [["opened", "s-1", ""], ["reaped", "s-2", "idle 8.0 days"]])
        datetime.fromisoformat(lines[0][0])

    def test_each_location_keeps_its_own_log_in_its_root(self) -> None:
        location = self.fake_root / "project" / "sessions"
        project_session = location / "my-task"
        project_session.mkdir(parents=True)
        left = memar_fs.scratch_root() / "20261009T120000Z-42-0"
        left.mkdir()
        session_log.record("opened", "my-task", folder=project_session)
        session_log.record("opened", left.name, folder=left)
        session_log.record("opened", "s-1", folder=memar_fs.session_dir("s-1", create=True))
        self.assertEqual(session_log.log_path(project_session), location / session_log.SESSION_LOG_NAME)
        self.assertEqual(session_log.log_path(left), session_log.log_path())
        own = [line.split("\t")[1:3] for line in session_log.log_path(project_session).read_text(encoding="utf-8").splitlines()]
        memars = [line.split("\t")[1:3] for line in session_log.log_path().read_text(encoding="utf-8").splitlines()]
        self.assertEqual(own, [["opened", "my-task"]])
        self.assertEqual(memars, [["opened", left.name], ["opened", "s-1"]])

    def test_a_log_that_cannot_be_written_warns_and_goes_on(self) -> None:
        session_log.log_path().mkdir(parents=True)
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            session_log.record("opened", "s-1")
        self.assertIn("the session log could not be written", err.getvalue())


if __name__ == "__main__":
    unittest.main(verbosity=2)
