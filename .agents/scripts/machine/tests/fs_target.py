#!/usr/bin/env python3
"""Tests for the folder a run would use, and the one place that refuses a temporary one.

    python .agents/scripts/target/tests/fs_target.py

The subject is `machine/fs_target.py`, named for the file that holds it per
[Test Naming](../../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../../modules/process/test/rules/test-placement/test-placement.md).

A check of a file this suite does not own belongs beside the file that owns it,
not here: what the installer does with these answers is pinned in
`tests/memar-install.py`. The classes here reach the installer's own binding of
the shelf rather than the shelf's, because the installer's binding is the one
the run calls, and they stay with the module rather than with the caller.
Nothing here writes to the machine — the platform's own record is read but never
written, and every folder a run reaches is a scratch folder removed again.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

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

import machine.fs_target as target
import importlib.util
from importlib.machinery import SourceFileLoader

# The installer is a command, so its name carries a hyphen and no import can
# reach it; the loader is named rather than inferred for the same reason the
# launcher's own test names one.
_spec = importlib.util.spec_from_loader(
    "memar_install", SourceFileLoader("memar_install", str(SCRIPTS / "memar-install.py"))
)
memar_install = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(memar_install)


class TemporaryRefusal(unittest.TestCase):
    """Every refusal names the directory the check actually used, and one function decides."""

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=TESTS)
        self.addCleanup(self.scratch.cleanup)
        self.saved_temp = os.environ.get("TEMP")
        os.environ["TEMP"] = self.scratch.name

    def tearDown(self) -> None:
        if self.saved_temp is None:
            os.environ.pop("TEMP", None)
        else:
            os.environ["TEMP"] = self.saved_temp

    def refused(self, path: Path, consequence: str) -> str:
        with self.assertRaises(SystemExit) as raised:
            target.refuse_temporary(path, consequence)
        return str(raised.exception.code)

    def test_the_refusal_names_the_directory_the_check_used(self):
        below = Path(self.scratch.name) / "Memar"
        message = self.refused(below, "because it does not survive.")
        self.assertIn(str(Path(self.scratch.name).resolve()), message)
        self.assertIn(str(below), message)

    def test_a_folder_outside_it_is_not_refused(self):
        outside = SCRIPTS / "not-a-temp-folder"
        self.assertIsNone(target.refuse_temporary(outside, "unused"))

    def test_the_directory_is_asked_once_and_used_for_both(self):
        # A check that reads the directory and a message that reads it again can
        # print a directory the decision was not made against.
        asked = []
        saved = target.temporary_directory

        def counted() -> Path:
            asked.append(1)
            return saved()

        target.temporary_directory = counted
        self.addCleanup(setattr, target, "temporary_directory", saved)
        with self.assertRaises(SystemExit):
            target.refuse_temporary(Path(self.scratch.name) / "Memar", "because.")
        self.assertEqual(len(asked), 1)

    def test_every_mode_refuses_through_the_same_decision(self):
        # The refusal a record prints and the refusal a check prints come from
        # one check, so neither can drift from the other. Both are called with
        # the refusal itself stubbed out, which is the only way to ask what each
        # one would have decided.
        decided = []

        def recorder(path: Path, consequence: str) -> None:
            decided.append((str(path), consequence))
            raise RuntimeError("refused")

        saved = memar_install.refuse_temporary
        memar_install.refuse_temporary = recorder
        self.addCleanup(setattr, memar_install, "refuse_temporary", saved)
        with self.assertRaises(RuntimeError):
            memar_install.register(str(Path(self.scratch.name) / "Memar"))
        with self.assertRaises(RuntimeError):
            memar_install.check(str(Path(self.scratch.name) / "Memar"))
        self.assertEqual(len(decided), 2)
        self.assertEqual({path for path, _ in decided}, {str(Path(self.scratch.name) / "Memar")})
        for _, consequence in decided:
            self.assertTrue(consequence)

    def test_the_register_refusal_names_the_directory_it_kept_quiet_about(self):
        below = Path(self.scratch.name) / "Memar"
        message = self.refused(below, "unused")
        self.assertIn(str(Path(self.scratch.name).resolve()), message)


if __name__ == "__main__":
    unittest.main(verbosity=2)
