#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for where Memar lives on disk in `machine/fs_memar.py`.

    python .agents/scripts/machine/tests/fs_memar.py

The subject is the location surface of `machine/fs_memar.py`, named for the
file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the module that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes to the machine. Roots are patched onto a scratch folder
inside this one; the one test that touches the real checkout only reads
constant properties of it. Session folders are created under a scratch
folder and removed again.

What is pinned, and what each pin is for:

  DefaultLocation    Locks, intents, and session folders default under
                     <memar-root>/temp/, the ONE scratch root, so they can
                     only ever occupy the ignored temp entry and no ignore
                     rule is owed; an unresolvable root errors rather than
                     guessing.
  SessionDir         A session id names one folder segment under the sessions
                     root, temp/sessions/, and nothing else; anything shaped
                     like a path is refused, and readers never create.

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

from machine.fs_test_scratch import suite_scratch

import machine.fs_memar as memar_fs


class DefaultLocation(unittest.TestCase):
    def test_scratch_defaults_under_the_memar_temp_root(self) -> None:
        with tempfile.TemporaryDirectory(dir=suite_scratch()) as scratch:
            fake_root = Path(scratch)
            with unittest.mock.patch.object(
                memar_fs, "memar_root", return_value=fake_root
            ):
                self.assertEqual(
                    memar_fs.scratch_root(), fake_root / memar_fs.TEMP_DIRNAME
                )
                # Under temp/, the ONE root the .gitignore already ignores: the only
                # repo path scratch can occupy is an ignored one, so no rule is owed.

    def test_recorded_root_wins_over_the_checkout(self) -> None:
        with tempfile.TemporaryDirectory(dir=suite_scratch()) as scratch:
            fake_root = Path(scratch)
            with unittest.mock.patch.object(
                memar_fs, "recorded_root", return_value=fake_root
            ):
                self.assertEqual(memar_fs.memar_root(), fake_root)

    def test_checkout_is_used_when_nothing_is_recorded(self) -> None:
        with unittest.mock.patch.object(
            memar_fs, "recorded_root", return_value=None
        ):
            with unittest.mock.patch.object(
                memar_fs, "is_memar_repository", return_value=True
            ):
                self.assertEqual(memar_fs.memar_root(), memar_fs.checkout_root())

    def test_unresolvable_root_errors_rather_than_guessing(self) -> None:
        with unittest.mock.patch.object(
            memar_fs, "recorded_root", return_value=None
        ):
            with unittest.mock.patch.object(
                memar_fs, "checkout_root", return_value=Path("/no-such-checkout")
            ):
                with unittest.mock.patch.object(
                    memar_fs, "is_memar_repository", return_value=False
                ):
                    with self.assertRaises(SystemExit):
                        memar_fs.memar_root()

    def test_checkout_root_is_this_checkout(self) -> None:
        self.assertEqual(memar_fs.checkout_root(), CHECKOUT)


class SessionDir(unittest.TestCase):
    def test_session_dir_is_one_segment_under_the_sessions_root(self) -> None:
        with tempfile.TemporaryDirectory(dir=suite_scratch()) as scratch:
            fake_root = Path(scratch)
            with unittest.mock.patch.object(
                memar_fs, "memar_root", return_value=fake_root
            ):
                path = memar_fs.session_dir("s-1")
                self.assertEqual(path, fake_root / "temp" / "sessions" / "s-1")
                self.assertEqual(path.parent, memar_fs.sessions_root())
                self.assertFalse(path.exists())

    def test_session_dir_creates_only_when_asked(self) -> None:
        with tempfile.TemporaryDirectory(dir=suite_scratch()) as scratch:
            fake_root = Path(scratch)
            with unittest.mock.patch.object(
                memar_fs, "memar_root", return_value=fake_root
            ):
                path = memar_fs.session_dir("s-2", create=True)
                self.assertTrue(path.is_dir())

    def test_session_dir_refuses_anything_shaped_like_a_path(self) -> None:
        with tempfile.TemporaryDirectory(dir=suite_scratch()) as scratch:
            fake_root = Path(scratch)
            with unittest.mock.patch.object(
                memar_fs, "memar_root", return_value=fake_root
            ):
                for bad in ("", ".", "..", "a/b", "a\\b"):
                    with self.subTest(bad=bad):
                        with self.assertRaises(SystemExit):
                            memar_fs.session_dir(bad)


if __name__ == "__main__":
    unittest.main(verbosity=2)
