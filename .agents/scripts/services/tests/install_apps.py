#!/usr/bin/env python3
"""Tests for what memar-install-apps.py does with a skill copy already there.

    python .agents/scripts/tests/memar-install-apps.py

The subject is the copy into an agent app, per
[Test Naming](../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns the installer per
[Test Placement](../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes to a real agent app. The source and the destination are
scratch folders inside this one, and the trash is a stand-in that only removes
the path so the new copy can land. The platform's trash is not this test's to
call.

What is pinned, and what each pin is for:

  ReplacingACopyTrashesIt  An earlier copy may hold a local edit. It is moved
                           to the trash before the checkout's skill is written,
                           so the edit can be taken back. A dry run does not
                           touch it.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import importlib.util
import shutil
import sys
import tempfile
import unittest
import unittest.mock
from importlib.machinery import SourceFileLoader
from pathlib import Path

TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parent
sys.path.insert(0, str(SCRIPTS))
sys.dont_write_bytecode = True

# A hyphenated name is not a legal module name, so the loader is named rather
# than inferred. A spec inferred from the suffix declines a file it does not
# recognize, and a test that could not load its own subject would be a test of
# nothing.
_spec = importlib.util.spec_from_loader(
    "memar_install_apps",
    SourceFileLoader("memar_install_apps", str(SCRIPTS / "memar-install-apps.py")),
)
apps = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(apps)


class ReplacingACopyTrashesIt(unittest.TestCase):
    """An earlier skill copy is trashed, not deleted, before the new one lands."""

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=TESTS)
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
        source = (SCRIPTS / "memar-install-apps.py").read_text(encoding="utf-8")
        self.assertNotIn("rmtree", source)
        self.assertNotIn("unlink(", source)
        self.assertIn("soft_delete", source)

    def test_a_dry_run_leaves_the_existing_copy_where_it_is(self) -> None:
        with unittest.mock.patch.object(apps, "soft_delete") as trash:
            apps.copy_skill(self.source, self.dest, dry_run=True)
        trash.assert_not_called()
        self.assertTrue((self.dest / "local-edit.md").is_file())


if __name__ == "__main__":
    unittest.main(verbosity=2)
