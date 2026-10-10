#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for what the agent-app layer, `services/install_apps.py`, does with a skill copy already there.

    python .agents/scripts/services/tests/install_apps.py

The subject is the copy into an agent app, per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns the installer per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes to a real agent app. The source, the destination, and the
home folder the apps are looked for in are scratch folders inside this one, and
the trash is a stand-in that only removes
the path so the new copy can land. The platform's trash is not this test's to
call.

What is pinned, and what each pin is for:

  ReplacingACopyTrashesIt  An earlier copy may hold a local edit. It is moved
                           to the trash before the checkout's skill is written,
                           so the edit can be taken back. A dry run does not
                           touch it.
  StaleCopiesNamed         A copy already in an agent app that is not what
                           copying the checkout's skill would write — a file
                           changed, added, or gone, leaving out what a copy
                           never carries — is named on one line with the
                           command that refreshes it, and nothing is written;
                           when every copy matches nothing is printed, since
                           `memar update` relays these lines as its own. A
                           refresh of the existing copies rewrites only the
                           copies that differ.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import contextlib
import io
import shutil
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

from machine.fs_test_scratch import suite_scratch

import services.install_apps as apps


class ReplacingACopyTrashesIt(unittest.TestCase):
    """An earlier skill copy is trashed, not deleted, before the new one lands."""

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        root = Path(self.scratch.name)
        self.source = root / "source"
        self.source.mkdir()
        (self.source / "SKILL.md").write_text("from the checkout\n", encoding="utf-8")
        self.dest = root / "skills" / "memar"
        self.dest.mkdir(parents=True)
        (self.dest / "local-edit.md").write_text("keep me\n", encoding="utf-8")

    def test_an_existing_copy_is_trashed_before_the_new_one_is_written(self) -> None:
        def move_aside(path: Path) -> None:
            shutil.rmtree(path)

        with unittest.mock.patch.object(apps, "soft_delete", side_effect=move_aside) as trash:
            apps.copy_skill(self.source, self.dest, dry_run=False)
        trash.assert_called_once_with(self.dest)
        self.assertEqual((self.dest / "SKILL.md").read_text(encoding="utf-8"), "from the checkout\n")
        self.assertFalse((self.dest / "local-edit.md").exists())
        source = Path(apps.__file__).read_text(encoding="utf-8")
        self.assertNotIn("rmtree", source)
        self.assertNotIn("unlink(", source)
        self.assertIn("soft_delete", source)

    def test_a_dry_run_leaves_the_existing_copy_where_it_is(self) -> None:
        with unittest.mock.patch.object(apps, "soft_delete") as trash:
            apps.copy_skill(self.source, self.dest, dry_run=True)
        trash.assert_not_called()
        self.assertTrue((self.dest / "local-edit.md").is_file())


class StaleCopiesNamed(unittest.TestCase):
    """A copy that is not what copying the checkout's skill would write is named; nothing is written."""

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        root = Path(self.scratch.name)
        self.home = root / "home"
        self.home.mkdir()
        self.source = root / "checkout" / ".agents" / "skills" / "memar"
        (self.source / "part").mkdir(parents=True)
        (self.source / "SKILL.md").write_text("the skill\n", encoding="utf-8")
        (self.source / "part" / "more.md").write_text("more\n", encoding="utf-8")
        patched = unittest.mock.patch.object(Path, "home", return_value=self.home)
        patched.start()
        self.addCleanup(patched.stop)

    def copy_into(self, app_dir: str) -> Path:
        dest = self.home / app_dir / "skills" / "memar"
        shutil.copytree(self.source, dest, ignore=apps.NEVER_COPIED)
        return dest

    def test_copies_that_match_are_not_named_and_nothing_is_printed(self) -> None:
        self.copy_into(".agents")
        self.copy_into(".cursor")
        (self.home / ".claude").mkdir()
        self.assertEqual(apps.stale_copies(self.source), [])
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            apps.warn_stale(self.source)
        self.assertEqual(out.getvalue(), "")

    def test_a_changed_added_or_missing_file_makes_a_copy_stale(self) -> None:
        changed = self.copy_into(".agents")
        (changed / "SKILL.md").write_text("the skill, as it was\n", encoding="utf-8")
        added = self.copy_into(".cursor")
        (added / "local.md").write_text("mine\n", encoding="utf-8")
        missing = self.copy_into(".claude")
        (missing / "part" / "more.md").unlink()
        self.copy_into(".codex")
        self.assertEqual(apps.stale_copies(self.source), [changed, added, missing])

    def test_what_a_copy_never_carries_is_left_out_of_the_comparison(self) -> None:
        (self.source / "__pycache__").mkdir()
        (self.source / "__pycache__" / "x.pyc").write_bytes(b"\0")
        dest = self.copy_into(".agents")
        (dest / ".DS_Store").write_bytes(b"\0")
        (dest / "part" / "y.pyc").write_bytes(b"\0")
        self.assertEqual(apps.stale_copies(self.source), [])

    def test_each_stale_copy_gets_one_line_naming_the_refresh(self) -> None:
        dest = self.copy_into(".agents")
        (dest / "SKILL.md").write_text("old\n", encoding="utf-8")
        out = io.StringIO()
        with unittest.mock.patch.object(apps, "resolve_root", return_value=self.source.parents[2]):
            with unittest.mock.patch.object(apps, "soft_delete") as trash:
                with contextlib.redirect_stdout(out):
                    apps.warn_stale(apps.checkout_skill())
        trash.assert_not_called()
        lines = out.getvalue().splitlines()
        self.assertEqual(len(lines), 1)
        self.assertIn(str(dest), lines[0])
        self.assertIn("memar update --apply", lines[0])
        self.assertEqual((dest / "SKILL.md").read_text(encoding="utf-8"), "old\n")

    def test_update_rewrites_only_the_copies_that_differ(self) -> None:
        stale = self.copy_into(".agents")
        (stale / "SKILL.md").write_text("old\n", encoding="utf-8")
        current = self.copy_into(".cursor")
        out = io.StringIO()
        with unittest.mock.patch.object(apps, "resolve_root", return_value=self.source.parents[2]):
            with unittest.mock.patch.object(apps, "soft_delete", side_effect=shutil.rmtree) as trash:
                with contextlib.redirect_stdout(out):
                    apps.into_apps(existing_only=True)
        trash.assert_called_once_with(stale)
        self.assertEqual((stale / "SKILL.md").read_text(encoding="utf-8"), "the skill\n")
        self.assertIn(f"already current: {current}", out.getvalue())

    def test_a_checkout_without_the_skill_names_nothing(self) -> None:
        self.copy_into(".agents")
        self.assertEqual(apps.stale_copies(self.home / "nowhere"), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
