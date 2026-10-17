#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the session locations kept in the projects registry, in `modules/process/session/services/location.py` and `modules/process/project/services/registry.py`.

    python modules/process/session/tests/location.py

The subject is where Memar remembers the session locations of the projects it
has made folders in: no longer the file temp/sessions/sessions.projects (one
path a line, no project), but the `locations` array of the project's own entry
in temp/projects.log, so a location is found from its project and a project is
always named. The rulings are the owner's of 2026-10-13, recorded in session
20261013T085819Z-27156-0. Named for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md).

Nothing here writes outside its scratch folder: the Memar root is patched onto
one made under the folder `machine/fs_test_scratch.py` names.

What is pinned, and what each pin is for:

  Register    A location is stored on its project's entry; the project is the
              one given, else the git top-level of the location, else the
              folder above it; an entry is made from the folder name when the
              project has none; a name another project holds is reported and
              nothing is renamed or stored.
  Read        `registered_locations` and `locations_of` read the entries, pass
              over a location that is gone, and never one inside Memar's scratch;
              a nested project's location is its own.
  Prune       A location that is gone is removed from its entry, which stays.
  EarlierRecord  The old sessions.projects is not read: a reader of locations
              says so on stderr, and that a location it lists is recorded again
              when `memar session new` next makes or continues a session there;
              it names no conversion script, and leaves the file alone.
"""
from __future__ import annotations

import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path

TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parents[3] / ".agents" / "scripts"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))  # the checkout's top, where `modules/` is imported from
sys.dont_write_bytecode = True

from machine.fs_test_scratch import suite_scratch

import machine.fs_memar as memar_fs
import modules.process.project.services.registry as registry
import modules.process.session.services.location as session_location
from modules.process.session.services.location import locations_of, prune_registry, register, registered_locations


def git_init(folder: Path) -> Path:
    folder.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init", "-q", str(folder)], check=True, capture_output=True)
    return folder


class Fixture(unittest.TestCase):
    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.base = Path(self.scratch.name).resolve()
        self.memar = self.base / "memar"
        self.memar.mkdir()
        patched = unittest.mock.patch.object(memar_fs, "memar_root", return_value=self.memar)
        patched.start()
        self.addCleanup(patched.stop)
        # The scratch lies inside Memar's own repository; git must not find it from a plain folder here.
        ceiling = unittest.mock.patch.dict(os.environ, {"GIT_CEILING_DIRECTORIES": str(self.base)})
        ceiling.start()
        self.addCleanup(ceiling.stop)

    def project(self, name: str) -> Path:
        return git_init(self.base / name)

    def location(self, project: Path, name: str = "sessions") -> Path:
        path = project / name
        path.mkdir(parents=True, exist_ok=True)
        return path

    def entries(self) -> dict[str, registry.Entry]:
        return {entry.names[0]: entry for entry in registry.read_entries()}

    def err(self, call):
        error = io.StringIO()
        with contextlib.redirect_stderr(error):
            call()
        return error.getvalue()


class Register(Fixture):
    def test_a_project_without_an_entry_gets_one_named_from_its_folder_with_the_location(self) -> None:
        project = self.project("organization")
        location = self.location(project)
        register(location, project)
        found = self.entries()["organization"]
        self.assertEqual(Path(found.path), project)
        self.assertEqual([Path(each) for each in found.locations], [location])
        self.assertEqual(registered_locations(), [location])

    def test_the_project_is_the_git_top_level_of_the_location_when_not_given(self) -> None:
        project = self.project("organization")
        register(self.location(project, "work/sessions"))
        self.assertEqual(Path(self.entries()["organization"].path), project)

    def test_a_location_in_no_repository_belongs_to_the_folder_above_it(self) -> None:
        plain = self.base / "plain"
        register(self.location(plain))
        self.assertEqual(Path(self.entries()["plain"].path), plain)

    def test_a_location_is_recorded_once(self) -> None:
        project = self.project("organization")
        location = self.location(project)
        register(location, project)
        register(location, project)
        self.assertEqual(len(self.entries()["organization"].locations), 1)

    def test_the_location_goes_on_the_entry_the_project_already_has_and_its_names_stay(self) -> None:
        project = self.project("organization")
        registry.add_project("org", project, ["سازمان"])
        register(self.location(project), project)
        found = registry.read_entries()
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].names, ("org", "سازمان"))
        self.assertEqual(len(found[0].locations), 1)

    def test_a_name_another_project_holds_is_reported_and_nothing_is_renamed_or_stored(self) -> None:
        holder = self.project("holder")
        registry.add_project("organization", holder)
        project = self.project("organization")
        said = self.err(lambda: register(self.location(project), project))
        self.assertIn("organization", said)
        self.assertIn(str(holder), said)
        self.assertEqual([(entry.names, entry.locations) for entry in registry.read_entries()], [(("organization",), ())])
        self.assertEqual(registered_locations(), [])

    def test_a_location_inside_the_memar_scratch_is_not_a_project_location(self) -> None:
        inside = memar_fs.sessions_root()
        register(inside, self.memar)
        self.assertEqual(registered_locations(), [])

    def test_nothing_is_made_by_reading_when_nothing_was_registered(self) -> None:
        self.assertEqual(registered_locations(), [])
        self.assertFalse(memar_fs.projects_log().exists())
        self.assertFalse(memar_fs.project_sessions_registry().exists())


class Read(Fixture):
    def test_a_location_that_is_gone_is_passed_over_and_stays_recorded(self) -> None:
        project = self.project("organization")
        gone = self.location(project, "gone")
        kept = self.location(project, "kept")
        register(gone, project)
        register(kept, project)
        gone.rmdir()
        self.assertEqual(registered_locations(), [kept])
        self.assertEqual(len(self.entries()["organization"].locations), 2)

    def test_locations_of_a_project_are_its_preferred_one_and_its_recorded_ones(self) -> None:
        project = self.project("organization")
        other = self.project("other")
        mine = self.location(project, "work/sessions")
        register(mine, project)
        register(self.location(other), other)
        self.assertEqual(locations_of(project), [mine.resolve()])
        self.assertEqual(locations_of(other), [(other / "sessions").resolve()])

    def test_a_nested_projects_location_is_its_own_not_the_enclosing_ones(self) -> None:
        project = self.project("organization")
        inner = git_init(project / "inner")
        register(self.location(inner))
        self.assertEqual(locations_of(project), [])
        self.assertEqual(locations_of(inner), [(inner / "sessions").resolve()])

    def test_a_folder_that_is_no_project_owns_no_location_beneath_it(self) -> None:
        project = self.project("organization")
        register(self.location(project))
        self.assertEqual(locations_of(self.base), [])

    def test_a_location_equal_to_its_project_is_not_listed(self) -> None:
        project = self.project("organization")
        register(project, project)
        self.assertEqual(locations_of(project), [])


class Prune(Fixture):
    def test_a_location_that_is_gone_is_removed_from_its_entry_which_stays(self) -> None:
        project = self.project("organization")
        gone = self.location(project, "gone")
        kept = self.location(project, "kept")
        register(gone, project)
        register(kept, project)
        gone.rmdir()
        self.assertEqual(prune_registry(), [gone])
        found = self.entries()["organization"]
        self.assertEqual([Path(each) for each in found.locations], [kept])
        self.assertEqual(prune_registry(), [])

    def test_a_location_pruned_is_recorded_again_by_the_next_register(self) -> None:
        project = self.project("organization")
        location = self.location(project)
        register(location, project)
        location.rmdir()
        prune_registry()
        location.mkdir()
        register(location, project)
        self.assertEqual(registered_locations(), [location])

    def test_pruning_when_nothing_is_recorded_makes_no_file(self) -> None:
        self.assertEqual(prune_registry(), [])
        self.assertFalse(memar_fs.projects_log().exists())

    def test_a_location_added_while_pruning_is_kept(self) -> None:
        project = self.project("organization")
        gone = self.location(project, "gone")
        register(gone, project)
        gone.rmdir()
        added = self.location(project, "added")
        original = registry.forget_missing_locations

        def add_then_forget():
            register(added, project)
            return original()

        with unittest.mock.patch.object(session_location, "forget_missing_locations", side_effect=add_then_forget):
            self.assertEqual(prune_registry(), [gone])
        self.assertEqual(registered_locations(), [added])


class EarlierRecord(Fixture):
    def legacy(self, *lines: Path | str) -> Path:
        old = memar_fs.project_sessions_registry()
        old.write_text("".join(f"{line}\n" for line in lines), encoding="utf-8", newline="\n")
        return old

    def test_the_old_file_is_not_read_and_a_reader_says_how_its_locations_come_back(self) -> None:
        project = self.project("organization")
        old = self.legacy(self.location(project))
        said = self.err(lambda: self.assertEqual(registered_locations(), []))
        self.assertIn("sessions.projects", said)
        self.assertIn(session_location.EARLIER_RECORD_REMEDY, said)
        self.assertIn("memar session new", said)
        self.assertNotIn(".py", said)
        self.assertEqual(self.entries(), {})
        self.assertTrue(old.is_file())

    def test_every_reader_and_writer_of_locations_says_it(self) -> None:
        project = self.project("organization")
        self.legacy(self.location(project))
        for call in (registered_locations, lambda: locations_of(project), prune_registry):
            with self.subTest(call=call):
                self.assertIn(session_location.EARLIER_RECORD_REMEDY, self.err(call))

    def test_without_the_old_file_or_with_only_its_kept_name_nothing_is_said(self) -> None:
        self.assertEqual(self.err(registered_locations), "")
        (memar_fs.sessions_root() / (memar_fs.PROJECT_SESSIONS_NAME + ".migrated")).write_text("x\n", encoding="utf-8")
        self.assertEqual(self.err(registered_locations), "")


class EntryFormat(Fixture):
    def test_locations_are_a_json_array_on_the_line_and_absent_when_there_are_none(self) -> None:
        project = self.project("organization")
        registry.add_project("organization", project)
        self.assertNotIn("locations", json.loads(memar_fs.projects_log().read_text(encoding="utf-8")))
        location = self.location(project)
        register(location, project)
        line = json.loads(memar_fs.projects_log().read_text(encoding="utf-8").splitlines()[0])
        self.assertEqual(line["locations"], [str(location)])

    def test_an_add_for_the_same_folder_keeps_the_locations(self) -> None:
        project = self.project("organization")
        register(self.location(project), project)
        registry.add_project("org", project)
        (found,) = registry.read_entries()
        self.assertEqual(found.names, ("organization", "org"))
        self.assertEqual(len(found.locations), 1)

    def test_a_damaged_locations_value_costs_the_locations_not_the_entry(self) -> None:
        memar_fs.projects_log().write_text(json.dumps({"path": str(self.base), "names": ["x"], "locations": "no"}) + "\n", encoding="utf-8", newline="\n")
        (found,) = registry.read_entries()
        self.assertEqual((found.names, found.locations), (("x",), ()))


if __name__ == "__main__":
    unittest.main()
