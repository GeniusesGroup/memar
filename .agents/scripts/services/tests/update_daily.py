#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the daily background update in `services/update_daily.py`.

    python .agents/scripts/services/tests/update_daily.py

The subject is what the router runs before every verb, named for the file
that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here starts a real update or writes outside its scratch folder: the
Memar root is patched onto one, made under the folder
`machine/fs_test_scratch.py` names, and the start of the background run is
patched to record its command, except in the one test that starts a harmless
child to prove it outlives no caller's output.

What is pinned, and what each pin is for:

  DeclaredAsAHook     `describe` registers no verb and returns `before`, so
                      the router runs it before every verb, `--help` too;
                      `before` asks with the first word typed, asks nothing
                      for the background run itself, and fails no verb.
  OnceADay            The first verb of a day starts the run, through the
                      launcher as `memar update --background`, and every later
                      one does not; `memar update` itself never starts it.
  OneRunAtATime       A run that finds another holding the lock is told so and
                      takes nothing; the lock is released when a run ends.
  OptOut              MEMAR_NO_AUTO_UPDATE set to anything but empty or 0
                      starts nothing and makes nothing, and a notice another
                      service left is still printed once.
  TestRunsAreSuppressed
                      A suite is a test run, so is a child it starts, and a
                      test run starts nothing even on the day's first verb.
  NoticeIsPrintedOnce The line a run leaves is printed on stderr by the next
                      verb and by no later one; stdout is never written. A
                      newer update line replaces one not yet printed, each
                      subject keeps its own, and an added line follows.
  NeverFailsTheVerb   A state folder that cannot be made, or a start that
                      fails, raises nothing and prints nothing.
  DetachedChildRuns   The detached start really starts its command, with its
                      output in the log.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import contextlib
import io
import os
import subprocess
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path

TESTS = Path(__file__).resolve().parent
# This suite lives in the `tests/` folder of the shelf that owns its subject, so
# the scripts folder is two levels up. Running a file puts its OWN folder on the
# module search path and not its parent's, which is the one line this needs and
# the reason it carries one.
SCRIPTS = TESTS.parent.parent
sys.path.insert(0, str(SCRIPTS))
sys.dont_write_bytecode = True

import machine.fs_test_scratch as test_scratch
from machine.fs_test_scratch import suite_scratch

import machine.fs_memar as memar_fs
import services.update_daily as daily

AWAKE: dict[str, str] = {}


class Fixture(unittest.TestCase):
    """A scratch Memar root and a start that only records what it was asked."""

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        patched = unittest.mock.patch.object(memar_fs, "memar_root", return_value=Path(self.scratch.name))
        patched.start()
        self.addCleanup(patched.stop)
        self.started: list[list[str]] = []
        starting = unittest.mock.patch.object(daily, "detach", lambda command, log: self.started.append(command))
        starting.start()
        self.addCleanup(starting.stop)

    def ask(self, verb: str | None, environ: dict[str, str] | None = None, testing: bool = False) -> tuple[str, str]:
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            daily.before_verb(verb, environ=AWAKE if environ is None else environ, testing=testing)
        return out.getvalue(), err.getvalue()


class DeclaredAsAHook(unittest.TestCase):
    class Verbs:
        def __init__(self) -> None:
            self.added: list[str] = []

        def add_parser(self, name: str, **kwargs) -> None:
            self.added.append(name)

    def test_describe_registers_nothing_and_returns_before(self) -> None:
        verbs = self.Verbs()
        self.assertIs(daily.describe(verbs), daily.before)
        self.assertEqual(verbs.added, [])

    def test_before_asks_with_the_first_word_typed(self) -> None:
        asked: list[str | None] = []
        with unittest.mock.patch.object(daily, "before_verb", asked.append):
            for argv in (["content", "search", "x"], ["--help"], [], [daily.UPDATE_VERB, "--apply"]):
                daily.before(argv)
        self.assertEqual(asked, ["content", "--help", None, daily.UPDATE_VERB])

    def test_the_background_run_itself_is_asked_nothing(self) -> None:
        asked: list[str | None] = []
        with unittest.mock.patch.object(daily, "before_verb", asked.append):
            daily.before([daily.UPDATE_VERB, daily.BACKGROUND_FLAG])
            daily.before([daily.UPDATE_VERB, "--offline", daily.BACKGROUND_FLAG])
        self.assertEqual(asked, [])

    def test_before_fails_no_verb_when_its_imports_fail(self) -> None:
        out, err = io.StringIO(), io.StringIO()
        with unittest.mock.patch.dict(sys.modules, {"machine.fs_memar": None}):
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                daily.before(["content"])
        self.assertEqual((out.getvalue(), err.getvalue()), ("", ""))


class OnceADay(Fixture):
    def test_the_first_verb_of_the_day_starts_the_run_and_no_later_one_does(self) -> None:
        for verb in ("content", "session", None, "install"):
            self.assertEqual(self.ask(verb), ("", ""))
        self.assertEqual(
            self.started,
            [[sys.executable, str(daily.LAUNCHER), daily.UPDATE_VERB, daily.BACKGROUND_FLAG]],
        )
        self.assertTrue(daily.LAUNCHER.is_file())
        self.assertEqual(daily.LAUNCHER.parent, SCRIPTS)

    def test_a_marker_from_yesterday_starts_it_again(self) -> None:
        self.ask("content")
        (daily.state_dir() / daily.DAILY_MARKER_NAME).write_text("2000-01-01\n", encoding="utf-8")
        self.ask("content")
        self.assertEqual(len(self.started), 2)

    def test_memar_update_itself_does_not_start_it_or_spend_the_day(self) -> None:
        self.ask("update")
        self.assertEqual(self.started, [])
        self.ask("content")
        self.assertEqual(len(self.started), 1)

    def test_the_state_lives_under_temp_update(self) -> None:
        self.ask("content")
        directory = daily.state_dir()
        self.assertEqual(directory, Path(self.scratch.name) / memar_fs.TEMP_DIRNAME / daily.UPDATE_DIRNAME)
        self.assertTrue((directory / daily.DAILY_MARKER_NAME).is_file())


class OneRunAtATime(Fixture):
    def test_a_second_run_while_one_holds_the_lock_is_told_no(self) -> None:
        directory = daily.state_dir()
        with daily.daily_run(directory) as first:
            self.assertTrue(first)
            with daily.daily_run(directory) as second:
                self.assertFalse(second)
        with daily.daily_run(directory) as again:
            self.assertTrue(again)
        self.assertFalse((directory / daily.LOCK_NAME).exists())


class OptOut(Fixture):
    def test_the_opt_out_starts_nothing_and_makes_nothing(self) -> None:
        for value in ("1", "yes", "true"):
            with self.subTest(value=value):
                self.assertEqual(self.ask("content", {daily.OPT_OUT_VARIABLE: value}), ("", ""))
        self.assertEqual(self.started, [])
        self.assertFalse((memar_fs.scratch_root() / daily.UPDATE_DIRNAME).exists())

    def test_a_notice_left_is_still_printed_once_under_the_opt_out(self) -> None:
        daily.leave_notice(daily.state_dir(), "another service's line")
        stopped = {daily.OPT_OUT_VARIABLE: "1"}
        self.assertEqual(self.ask("content", stopped), ("", "memar: another service's line\n"))
        self.assertEqual(self.ask("content", stopped), ("", ""))
        self.assertEqual(self.started, [])
        self.assertFalse((daily.state_dir() / daily.DAILY_MARKER_NAME).exists())

    def test_empty_or_zero_is_not_an_opt_out(self) -> None:
        for value in ("", "0"):
            with self.subTest(value=value):
                self.assertIsNone(daily.suppressed({daily.OPT_OUT_VARIABLE: value}, testing=False))
        self.ask("content", {daily.OPT_OUT_VARIABLE: "0"})
        self.assertEqual(len(self.started), 1)


class TestRunsAreSuppressed(Fixture):
    def test_a_suite_and_its_children_are_test_runs(self) -> None:
        self.assertTrue(test_scratch.in_test_run())
        self.assertEqual(os.environ.get(test_scratch.TEST_RUN_VARIABLE), "1")
        child = subprocess.run(
            [sys.executable, "-c", f"import os; print(os.environ.get({test_scratch.TEST_RUN_VARIABLE!r}))"],
            capture_output=True, text=True, check=True,
        )
        self.assertEqual(child.stdout.strip(), "1")

    def test_a_test_run_starts_nothing_on_the_days_first_verb(self) -> None:
        daily.leave_notice(daily.state_dir(), "Memar was updated")
        self.assertEqual(self.ask("content", testing=True), ("", ""))
        self.assertEqual(self.started, [])
        self.assertTrue((daily.state_dir() / daily.NOTICE_NAME).exists())

    def test_the_launchers_default_asks_whether_this_is_a_test_run(self) -> None:
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            daily.before_verb("content", environ=AWAKE)
        self.assertEqual((out.getvalue(), err.getvalue(), self.started), ("", "", []))


class NoticeIsPrintedOnce(Fixture):
    def test_the_next_verb_prints_the_line_on_stderr_and_no_later_one_does(self) -> None:
        daily.leave_notice(daily.state_dir(), "Memar was updated: moved 2 commit(s)")
        out, err = self.ask("content")
        self.assertEqual(out, "")
        self.assertEqual(err, "memar: Memar was updated: moved 2 commit(s)\n")
        self.assertEqual(self.ask("content"), ("", ""))
        self.assertEqual(list(daily.state_dir().glob(f"{daily.NOTICE_NAME}*")), [])

    def test_a_newer_line_replaces_one_not_yet_printed(self) -> None:
        daily.leave_notice(daily.state_dir(), "first")
        daily.leave_notice(daily.state_dir(), "second")
        self.assertEqual(self.ask("update"), ("", "memar: second\n"))

    def test_the_line_takes_no_subject_and_no_add(self) -> None:
        with self.assertRaises(TypeError):
            daily.leave_notice(daily.state_dir(), "an event", subject="other")
        with self.assertRaises(TypeError):
            daily.leave_notice(daily.state_dir(), "an event", add=True)


class NeverFailsTheVerb(Fixture):
    def test_a_state_folder_that_cannot_be_made_is_silent(self) -> None:
        with unittest.mock.patch.object(daily, "state_dir", side_effect=SystemExit("error: no root")):
            self.assertEqual(self.ask("content"), ("", ""))
        with unittest.mock.patch.object(daily, "state_dir", side_effect=OSError("denied")):
            self.assertEqual(self.ask("content"), ("", ""))

    def test_a_start_that_fails_is_silent(self) -> None:
        with unittest.mock.patch.object(daily, "detach", side_effect=OSError("no python")):
            self.assertEqual(self.ask("content"), ("", ""))


class DetachedChildRuns(unittest.TestCase):
    def test_the_detached_command_runs_with_its_output_in_the_log(self) -> None:
        with tempfile.TemporaryDirectory(dir=suite_scratch()) as folder:
            log = Path(folder) / daily.LOG_NAME
            done = Path(folder) / "done"
            child = daily.detach(
                [sys.executable, "-c", f"import pathlib; print('ran'); pathlib.Path({str(done)!r}).write_text('x')"],
                log,
            )
            self.assertEqual(child.wait(timeout=30), 0)
            self.assertTrue(done.exists())
            self.assertIn("ran", log.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
