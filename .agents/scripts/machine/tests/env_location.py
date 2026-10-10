#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the one variable that says where Memar lives: read it, write it, resolve it.

    python .agents/scripts/machine/tests/env_location.py

The subject is `machine/env_location.py`, named for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

A check of a file this suite does not own belongs beside the file that owns it,
not here: what the installer does with these answers is pinned in
`services/tests/install.py`.
Nothing here writes to the machine — the platform's own record is read but never
written, and every folder a run reaches is a scratch folder removed again.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import contextlib
import io
import os
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path

TESTS = Path(__file__).resolve().parent
# This suite lives in the `tests/` folder of the shelf that owns its subject, so
# the scripts folder is two levels up and the checkout it resolves against is two
# above that. Running a file puts its OWN folder on the module search path and not
# its parent's, which is the one line this needs and the reason it carries one.
SCRIPTS = TESTS.parent.parent
CHECKOUT = SCRIPTS.parent.parent
sys.path.insert(0, str(SCRIPTS))
sys.dont_write_bytecode = True

from machine.fs_test_scratch import suite_scratch

import machine.env_location as location

VARIABLE = location.VARIABLE


class RecordOverSession(unittest.TestCase):
    """The record is the value; the process environment is a cache of it."""

    def setUp(self) -> None:
        self.saved = os.environ.get(VARIABLE)
        self.saved_notice = location.NOTICE_REPORTED
        self.saved_persisted = location.persisted_value
        location.NOTICE_REPORTED = False

    def tearDown(self) -> None:
        if self.saved is None:
            os.environ.pop(VARIABLE, None)
        else:
            os.environ[VARIABLE] = self.saved
        location.NOTICE_REPORTED = self.saved_notice
        location.persisted_value = self.saved_persisted

    def ask(self, record: str, session: str) -> str:
        """What a program sees when the record holds RECORD and its own copy holds SESSION."""
        location.persisted_value = lambda: record
        if session:
            os.environ[VARIABLE] = session
        else:
            os.environ.pop(VARIABLE, None)
        with contextlib.redirect_stdout(io.StringIO()):
            return location.recorded_value()

    def test_the_record_answers_when_the_session_reads_nothing(self):
        # The accident: the session that opened before the value was written.
        self.assertEqual(self.ask(r"C:\Users\you\Memar", ""), r"C:\Users\you\Memar")

    def test_the_record_answers_when_the_session_holds_another_value(self):
        # A cache is a copy of the record, so two different values is a stale
        # copy, not a decision. The record is the value.
        self.assertEqual(self.ask(r"C:\Users\you\Memar", r"D:\elsewhere"), r"C:\Users\you\Memar")

    def test_the_session_answers_when_the_record_is_silent(self):
        # Setting it for one session is a record for that session, and the
        # README makes it equivalent to writing it.
        self.assertEqual(self.ask("", r"D:\elsewhere"), r"D:\elsewhere")

    def test_a_stale_session_is_reported_rather_than_ignored(self):
        location.persisted_value = lambda: r"C:\Users\you\Memar"
        os.environ.pop(VARIABLE, None)
        printed = io.StringIO()
        with contextlib.redirect_stdout(printed):
            location.recorded_value()
        text = printed.getvalue()
        self.assertIn("disagrees with the record", text)
        self.assertIn("the record is used", text)
        self.assertIn(r"C:\Users\you\Memar", text)
        self.assertIn("unset", text)

    def test_a_stale_session_is_reported_once_not_once_per_read(self):
        location.persisted_value = lambda: r"C:\Users\you\Memar"
        os.environ.pop(VARIABLE, None)
        printed = io.StringIO()
        with contextlib.redirect_stdout(printed):
            for _ in range(3):
                location.recorded_value()
        self.assertEqual(printed.getvalue().count("disagrees with the record"), 1)

    def test_a_session_that_agrees_with_the_record_says_nothing(self):
        # The common case, every ordinary run: no line is added to the output.
        location.persisted_value = lambda: r"C:\Users\you\Memar"
        os.environ[VARIABLE] = r"C:\Users\you\Memar"
        printed = io.StringIO()
        with contextlib.redirect_stdout(printed):
            location.recorded_value()
        self.assertEqual(printed.getvalue(), "")

    def test_a_session_only_value_is_not_reported_as_stale(self):
        # A value the person set for this run is newer than the record, not
        # older, so the output does not gain a line on every such run.
        location.persisted_value = lambda: ""
        os.environ[VARIABLE] = r"D:\elsewhere"
        printed = io.StringIO()
        with contextlib.redirect_stdout(printed):
            location.recorded_value()
        self.assertEqual(printed.getvalue(), "")

class ProfileRoundTrip(unittest.TestCase):
    """What writes the record on POSIX is what reads it back."""

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.profile = Path(self.scratch.name) / ".bashrc"
        # Patched for the whole test, write included: a write that reached the
        # real profile would edit a file outside this repository.
        saved = location.shell_profile
        location.shell_profile = lambda: self.profile
        self.addCleanup(setattr, location, "shell_profile", saved)

    def ask(self) -> str:
        return location.profile_value()

    def test_what_written_is_what_read(self):
        location.write_profile_variable("/home/you/Memar")
        self.assertEqual(self.ask(), "/home/you/Memar")

    def test_rewriting_replaces_the_value_rather_than_appending_a_second(self):
        location.write_profile_variable("/home/you/Memar")
        location.write_profile_variable("/home/you/Other")
        self.assertEqual(self.ask(), "/home/you/Other")
        self.assertEqual(
            self.profile.read_text(encoding="utf-8").count(f"export {VARIABLE}="), 1
        )

    def test_a_value_written_by_hand_is_read_too(self):
        # The README makes setting the variable by hand equivalent.
        self.profile.write_text(
            f'# a line\nexport {VARIABLE}="/home/you/Memar"\n', encoding="utf-8"
        )
        self.assertEqual(self.ask(), "/home/you/Memar")

    def test_a_commented_assignment_is_not_a_value(self):
        self.profile.write_text(
            f'# export {VARIABLE}="/home/you/Memar"\n', encoding="utf-8"
        )
        self.assertEqual(self.ask(), "")

    def test_the_last_assignment_is_the_one_a_new_shell_gets(self):
        self.profile.write_text(
            f'export {VARIABLE}="/home/you/First"\n'
            f'export {VARIABLE}="/home/you/Memar"\n',
            encoding="utf-8",
        )
        self.assertEqual(self.ask(), "/home/you/Memar")

    def test_a_profile_that_is_not_there_reads_as_nothing(self):
        self.profile.unlink(missing_ok=True)
        self.assertEqual(self.ask(), "")

class RecordReadWrite(unittest.TestCase):
    """The Windows pair names one key, not two."""

    def test_read_and_write_name_the_same_key(self):
        # The registry read cannot be executed here without writing the user's
        # real HKCU\\Environment, so what is pinned is the one thing that made
        # the two disagree in the first place: the key they name.
        self.assertEqual(location.VARIABLE, "MEMAR_ROOT")
        self.assertEqual(location.WINDOWS_ENVIRONMENT_KEY, "Environment")
        for function in (location.user_environment_value, location.write_user_variable):
            names = function.__code__.co_names
            self.assertIn("WINDOWS_ENVIRONMENT_KEY", names, function.__name__)
            self.assertIn("VARIABLE", names, function.__name__)

    def test_the_windows_read_finds_what_the_registry_actually_holds(self):
        # The only way to read the record is to ask for it, and asking wrongly
        # — a predefined key and a backslash in a value name, which is not the
        # same thing — reports no value at all and is exactly the failure this
        # fix exists to remove. It is read here, never written.
        if os.name != "nt":
            self.skipTest("the registry-backed user environment is a Windows record")
        import winreg

        try:
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_QUERY_VALUE
            ) as key:
                expected, _ = winreg.QueryValueEx(key, "MEMAR_ROOT")
        except OSError:
            self.skipTest("this machine records no MEMAR_ROOT")
        self.assertEqual(location.user_environment_value(), location.expand_recorded(str(expected)))

    def test_the_windows_read_expands_what_the_windows_write_can_hold(self):
        # A value written as REG_EXPAND_SZ is expanded by Windows when it builds
        # a new process's environment, so reading it back expands it too: the
        # record and the copy agree by construction.
        self.assertEqual(location.expand_recorded(r"%USERPROFILE%\Memar"), str(Path.home() / "Memar"))

    def test_the_read_asks_the_platform_the_write_uses(self):
        # Two reads would be two answers, and a wrong one is the defect: the read
        # that never asked the registry is what concluded Memar was not
        # installed on a machine where it was.
        answered = []

        def registry() -> str:
            answered.append("registry")
            return r"C:\Users\you\Memar"

        def profile() -> str:
            answered.append("profile")
            return "/home/you/Memar"

        saved_registry = location.user_environment_value
        saved_profile = location.profile_value
        location.user_environment_value = registry
        location.profile_value = profile
        self.addCleanup(setattr, location, "user_environment_value", saved_registry)
        self.addCleanup(setattr, location, "profile_value", saved_profile)
        with unittest.mock.patch.object(os, "name", "nt"):
            self.assertEqual(location.persisted_value(), r"C:\Users\you\Memar")
        with unittest.mock.patch.object(os, "name", "posix"):
            self.assertEqual(location.persisted_value(), "/home/you/Memar")
        self.assertEqual(answered, ["registry", "profile"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
