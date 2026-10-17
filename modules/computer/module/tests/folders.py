#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for making a module's role folders in `modules/computer/module/services/folders.py`.

    python modules/computer/module/tests/folders.py

The subject is `memar module folders` and the role list it makes, named for
the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).
The domain verb, `modules/computer/module/module.py`, only groups it, so its help is pinned
here too.

Nothing here writes outside its scratch folder: each folder the roles are made
in is made under the folder `machine/fs_test_scratch.py` names, and removed
again. `modules/README.md` is read, never written. The subprocesses run ask
for `--help` only, which writes nothing.

What is pinned, and what each pin is for:

  RolesMatchTheReadme  The role names are the ones `modules/README.md` lists in
                       its bullet "By role inside a module", which points at
                       `modules/computer/module/services/folders.py` for what each role holds;
                       a role added there and not here, or here and not there,
                       fails. Only the bare `name/` paths of the sentence that
                       lists the roles are read, so `services/<name>/`, the
                       padded and singular names the bullet warns against, and
                       modules such as `process/test/` are not taken for roles.
                       Every role carries what it holds and what it does not,
                       and the README retypes neither: a description is in the
                       code once.
  MakesOnlyWhatIsMissing
                       Each missing role folder is made, one already there is
                       left with what is in it, nothing is deleted or renamed,
                       and a file standing in a role's place is reported and
                       left.
  CommandSaysWhatItDid `memar module folders PATH` makes them in PATH, prints
                       what it made and what was already there, and refuses a
                       PATH that is not a folder, and no PATH: the current
                       folder is never read.
  HelpDeclaresIt       `memar module --help` says where what each role folder
                       holds is printed, and carries no command line of
                       `folders`; `memar module folders --help` names the role
                       folders it makes and prints, by calling the enum, what
                       each holds and what it does not.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import os
import re
import subprocess
import sys
import tempfile
import unittest
import unittest.mock
from importlib.machinery import SourceFileLoader
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

from machine.fs_memar import checkout_root
import modules.computer.module.services.folders as module_folders

LAUNCHER = SCRIPTS / "memar"
MODULES_README = checkout_root() / "modules" / "README.md"
ROLE_BULLET = "- **By role inside a module**"
# The sentence of the bullet that lists the roles, and where it ends.
ROLES_START = "The roles in use are"
ROLES_END = "The list is not closed"
BARE_ROLE = re.compile(r"^[a-z][a-z0-9-]*/$")

_spec = importlib.util.spec_from_loader("memar_launcher", SourceFileLoader("memar_launcher", str(LAUNCHER)))
launcher = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(launcher)
MODULE_SERVICES = [name for name in launcher.services() if name.partition(launcher.DOMAIN_SEPARATOR)[0] == "module"]


def readme_roles() -> list[str]:
    """The bare role names the roles sentence of the README's bullet lists, in order."""
    lines = [line for line in MODULES_README.read_text(encoding="utf-8").splitlines() if line.startswith(ROLE_BULLET)]
    assert len(lines) == 1, f"{MODULES_README} has {len(lines)} bullets starting {ROLE_BULLET!r}"
    sentence = lines[0].partition(ROLES_START)[2].partition(ROLES_END)[0]
    assert sentence, f"the bullet no longer says {ROLES_START!r} ... {ROLES_END!r}"
    return [path[:-1] for path in re.findall(r"`([^`]+)`", sentence) if BARE_ROLE.match(path)]


def command(*arguments: str) -> tuple[int, str]:
    """`memar module ARGUMENTS`, assembled from the module services alone, and what it printed."""
    out = io.StringIO()
    with unittest.mock.patch.object(launcher, "services", return_value=MODULE_SERVICES), \
            contextlib.redirect_stdout(out):
        code = launcher.main(["module", *arguments])
    return code, out.getvalue()


def run_help(*arguments: str) -> str:
    environment = dict(os.environ, COLUMNS="80", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
    completed = subprocess.run(
        [sys.executable, str(LAUNCHER), "module", *arguments, "--help"], capture_output=True, env=environment
    )
    assert completed.returncode == 0, completed.stderr
    return " ".join(completed.stdout.decode("utf-8").split())


class Fixture(unittest.TestCase):
    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.folder = Path(self.scratch.name)


class RolesMatchTheReadme(unittest.TestCase):
    def test_the_roles_are_the_ones_the_readme_lists(self) -> None:
        self.assertEqual(readme_roles(), list(module_folders.ROLE_FOLDERS))
        self.assertEqual(list(module_folders.ROLE_FOLDERS), [role.folder for role in module_folders.Role])

    def test_primitive_is_a_role_singular_like_protocol(self) -> None:
        self.assertIn("primitive", module_folders.ROLE_FOLDERS)
        self.assertNotIn("primitives", module_folders.ROLE_FOLDERS)
        self.assertNotIn("capsules", module_folders.ROLE_FOLDERS)

    def test_every_role_says_what_it_holds_and_what_it_does_not(self) -> None:
        for role in module_folders.Role:
            with self.subTest(role=role.folder):
                self.assertGreater(len(role.holds.split()), 5)
                self.assertGreater(len(role.holds_not.split()), 2)

    def test_the_readme_points_at_the_code_and_retypes_no_description(self) -> None:
        bullet = next(
            line for line in MODULES_README.read_text(encoding="utf-8").splitlines() if line.startswith(ROLE_BULLET)
        )
        self.assertIn("services/folders.py", bullet)
        flat = " ".join(bullet.split())
        for role in module_folders.Role:
            with self.subTest(role=role.folder):
                self.assertNotIn(" ".join(role.holds.split()), flat)
                self.assertNotIn(" ".join(role.holds_not.split()), flat)

    def test_the_enum_says_it_owns_the_descriptions(self) -> None:
        said = module_folders.Role.__doc__ or ""
        self.assertIn("modules/README.md", said)
        self.assertIn("the list is open", said)

    def test_temp_is_a_role_and_its_name_is_defined_once(self) -> None:
        # Every module has a `temp` folder, every session included (owner,
        # 2026-10-15): the name is the role's constant here, and the session's
        # temporary-files sentence takes it from here rather than a copy.
        self.assertEqual(module_folders.TEMP_FOLDER, "temp")
        self.assertIn(module_folders.TEMP_FOLDER, module_folders.ROLE_FOLDERS)
        import modules.process.session.services.temp as session_temp
        self.assertIs(session_temp.TEMP_FOLDER, module_folders.TEMP_FOLDER)
        source = Path(session_temp.__file__).read_text(encoding="utf-8")
        self.assertNotIn("TEMP_FOLDER = ", source)
        self.assertNotIn('"temp"', source)


class MakesOnlyWhatIsMissing(Fixture):
    def test_each_missing_role_folder_is_made_and_one_there_is_left_with_its_contents(self) -> None:
        (self.folder / "rules").mkdir()
        (self.folder / "rules" / "kept.md").write_text("# Kept\n", encoding="utf-8", newline="\n")
        (self.folder / "test").mkdir()
        done = module_folders.ensure_role_folders(self.folder)
        self.assertEqual(done.present, ["rules"])
        self.assertEqual(done.made, [role for role in module_folders.ROLE_FOLDERS if role != "rules"])
        self.assertEqual(done.blocked, [])
        self.assertTrue((self.folder / "rules" / "kept.md").is_file())
        self.assertTrue((self.folder / "test").is_dir())
        again = module_folders.ensure_role_folders(self.folder)
        self.assertEqual((again.made, again.present), ([], list(module_folders.ROLE_FOLDERS)))

    def test_a_file_in_a_roles_place_is_reported_and_left(self) -> None:
        (self.folder / "docs").write_text("not a folder\n", encoding="utf-8", newline="\n")
        done = module_folders.ensure_role_folders(self.folder)
        self.assertEqual(done.blocked, ["docs"])
        self.assertEqual((self.folder / "docs").read_text(encoding="utf-8"), "not a folder\n")


class CommandSaysWhatItDid(Fixture):
    def test_path_given_makes_them_there_and_says_what_was_made_and_there(self) -> None:
        (self.folder / "tests").mkdir()
        code, printed = command("folders", str(self.folder))
        self.assertEqual(code, 0)
        self.assertIn("made: protocol/, primitive/, rules/, errors/, services/, docs/, temp/", printed)
        self.assertIn("already there: tests/", printed)
        _, printed = command("folders", str(self.folder))
        self.assertNotIn("made:", printed)
        self.assertIn("already there: protocol/, primitive/, rules/, errors/, tests/, services/, docs/, temp/", printed)

    def test_no_path_is_refused_and_the_current_folder_is_never_read(self) -> None:
        # A script is told its folder (.agents/scripts/README.md, "A script is
        # told its project"): with none given nothing is made, wherever it runs.
        with contextlib.chdir(self.folder), contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                command("folders")
        self.assertEqual(list(self.folder.iterdir()), [])

    def test_a_path_that_is_not_a_folder_is_refused(self) -> None:
        with self.assertRaises(SystemExit):
            command("folders", str(self.folder / "absent"))
        self.assertFalse((self.folder / "absent").exists())

    def test_a_file_in_the_way_is_a_non_zero_status(self) -> None:
        (self.folder / "errors").write_text("", encoding="utf-8")
        code, printed = command("folders", str(self.folder))
        self.assertEqual(code, 1)
        self.assertIn("not made, a file of that name is there: errors/", printed)


class HelpDeclaresIt(unittest.TestCase):
    def test_the_domain_and_its_verb_say_what_they_make_and_where_the_roles_are_said(self) -> None:
        # Each help states its own work (owner, 2026-10-14): the domain says
        # what a module's role folders are and where their roles are said, and
        # leaves `folders`'s command line to `folders`'s own help.
        domain = run_help()
        self.assertNotIn("memar module folders", domain)
        self.assertIn("help of its verb folders", domain)
        verb = run_help("folders")
        self.assertNotIn("current folder", verb)
        self.assertIn("protocol/, primitive/, rules/, errors/, tests/, services/, docs/, temp/", verb)
        self.assertIn("nothing is deleted or renamed", verb)
        self.assertIn("modules/README.md", verb)
        for role in module_folders.Role:
            with self.subTest(role=role.folder):
                self.assertIn(" ".join(role.holds.split()), verb)
                self.assertIn(" ".join(role.holds_not.split()), verb)


if __name__ == "__main__":
    unittest.main(verbosity=2)
