#!/usr/bin/env python3
"""Tests for `memar session` in `memar-session.py`.

    python .agents/scripts/tests/memar-session.py

The subject is the session tool, named for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the module that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes to the machine. The Memar root the tool resolves is
patched onto a scratch folder — this one by default, the `MEMAR_TEST_SCRATCH`
folder when that variable points at one that already exists — and removed
again; session folders, locks, and intent notes land there and are removed with
it. The one subprocess run asks for `--help` only, which writes nothing.

What is pinned, and what each pin is for:

  CreatesFolder      `new` ensures <temp>/<id>/ and prints its id and
                     path, so every session works inside its own folder and
                     nothing lands in git by accident.
  RerunIsIdempotent  Reusing one session id keeps the folder as is and reports
                     the same id and path again.
  UnresolvableRoot   With neither a recorded location nor a checkout to run
                     inside, the tool errors rather than guessing a folder.
  HelpCarriesTheWhy  `memar session --help` says what to run and what to do
                     at the end of the work, and says nothing about how the
                     folder is arranged: the mechanism is a DevActionNote, and
                     a caller reading it in help output is reading the module
                     docstring a second time, one step removed from where it
                     can be maintained. The why is pinned to the docstring.
  LockSharesThisRoot The lock and intent files land under the same <root>/temp/
                     root the session folders share, and closing one session's
                     folder cannot reach the lock directory beside it. How a
                     lock behaves is pinned in `machine/tests/fs_lock.py`, which
                     owns it.
  MintedIdUnique     Two ids minted without a session differ, so two sessions
                     opening a shared scratch root cannot land on one folder.
  RecoverableClose   `close` hands the folder to recoverable storage instead of
                     destroying it, so a session closed by mistake costs one
                     trip to the trash rather than the files it held; a trash
                     that fails leaves the folder where it was, because a
                     failed recovery is not a successful close.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import os
import shutil
import subprocess
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

import machine.fs_lock as fs_lock
import machine.fs_memar as memar_fs

# The command is loaded under the name of the file that holds it, which is a
# hyphen and no module; the module beside it that answers `new_session_id` is
# imported under its own path, and the two are separate subjects with separate
# tests because the separator is the only thing that tells them apart.
import memar_session

_spec = importlib.util.spec_from_loader(
    "memar_session_command",
    SourceFileLoader("memar_session_command", str(SCRIPTS / "memar-session.py")),
)
session_tool = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(session_tool)


def run_help() -> subprocess.CompletedProcess:
    environment = dict(
        os.environ,
        COLUMNS="80",
        PYTHONIOENCODING="utf-8",
        PYTHONDONTWRITEBYTECODE="1",
    )
    return subprocess.run(
        [sys.executable, str(SCRIPTS / "memar-session.py"), "--help"],
        capture_output=True,
        env=environment,
    )


class Fixture(unittest.TestCase):
    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=os.environ.get("MEMAR_TEST_SCRATCH", TESTS))
        self.addCleanup(self.scratch.cleanup)
        self.fake_root = Path(self.scratch.name)
        # One patch, applied once: the locks resolve through the same root
        # lookup the session folders do, so the shared-root claim is proved by
        # pointing at one place rather than by patching it twice and calling
        # that two places.
        patched = unittest.mock.patch.object(
            memar_fs, "memar_root", return_value=self.fake_root
        )
        patched.start()
        self.addCleanup(patched.stop)


class CreatesFolder(Fixture):
    def test_creates_the_folder_and_returns_its_id_and_path(self) -> None:
        sid, path = session_tool.ensure_session("s-1")
        self.assertEqual(sid, "s-1")
        self.assertTrue(Path(path).is_dir())
        self.assertEqual(Path(path), self.fake_root / "temp" / "s-1")

    def test_the_command_prints_the_id_and_path_it_created(self) -> None:
        # Asked of `main`, not of a copy of its own two print statements: a test
        # that repeats what the code prints proves the repeat, and not the
        # command a caller actually types.
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = session_tool.main(["new", "--session-id", "s-2"])
        self.assertEqual(code, 0)
        text = out.getvalue()
        self.assertIn("s-2", text)
        self.assertIn(str(self.fake_root / "temp" / "s-2"), text)

    def test_mints_an_id_when_none_is_given(self) -> None:
        sid, path = session_tool.ensure_session()
        self.assertTrue(sid)
        self.assertTrue(path.is_dir())
        self.assertEqual(path, self.fake_root / "temp" / sid)

    def test_refuses_a_path_as_a_session_id(self) -> None:
        for bad in ("a/b", "a\\b", "..", ".", ""):
            with self.subTest(bad=bad):
                with self.assertRaises(SystemExit):
                    session_tool.ensure_session(bad)


class RerunIsIdempotent(Fixture):
    def test_rerun_keeps_the_folder_and_reports_the_same_path(self) -> None:
        first_id, first_path = session_tool.ensure_session("s-9")
        marker = first_path / "notes.md"
        marker.write_text("# Notes\n", encoding="utf-8", newline="\n")
        second_id, second_path = session_tool.ensure_session("s-9")
        self.assertEqual(second_id, first_id)
        self.assertEqual(second_path, first_path)
        self.assertTrue(marker.is_file())


class UnresolvableRoot(unittest.TestCase):
    def test_errors_rather_than_guessing(self) -> None:
        with unittest.mock.patch.object(
            memar_fs, "memar_root", side_effect=SystemExit("error: no root")
        ):
            with self.assertRaises(SystemExit):
                session_tool.ensure_session("s-1")


class HelpCarriesTheWhy(Fixture):
    """The help says what to do, and the file says why — never the reverse.

    A person opening a scratch folder needs to know which command to run and
    what to do at the end of the work. The mechanism that gives each session its
    own folder is the implementer's, and printing it to the caller turns help
    into a second copy of the module docstring that will drift from it. So the
    absence of the mechanism is pinned as deliberately as its presence.
    """

    MECHANISM = (
        "shared-tree collisions",
        "advisory locks",
        "intent notes",
        "OS-temp",
        "fails closed",
    )

    def test_the_help_says_what_to_run_and_what_to_do_afterwards(self) -> None:
        completed = run_help()
        self.assertEqual(completed.returncode, 0)
        text = completed.stdout.decode("utf-8").replace("\r\n", "\n")
        for phrase in ("memar session new", "memar session close", "--session-id", "person who started", "recycle bin"):
            self.assertIn(phrase, text)

    def test_the_help_does_not_carry_the_implementation(self) -> None:
        completed = run_help()
        text = completed.stdout.decode("utf-8").replace("\r\n", "\n")
        for phrase in self.MECHANISM:
            self.assertNotIn(phrase, text)

    def test_the_why_is_in_the_file_the_implementer_reads(self) -> None:
        # Not a second copy: the module's own docstring, which is the one text
        # addressed to whoever opens it.
        for phrase in ("shared-tree collisions", "advisory locks", "intent notes"):
            self.assertIn(phrase, session_tool.__doc__)


class LockSharesThisRoot(Fixture):
    """The locks and the session folders live under the same root, and that is all
    this file claims. How a lock behaves — taking it, releasing it, refusing an
    absent or ambiguous base — belongs to `machine/tests/fs_lock.py`, which owns it;
    a test of the same behavior in two files is two places to update and one of
    them to forget.
    """

    def test_a_lock_for_a_file_lands_under_this_sessions_root(self) -> None:
        target = self.fake_root / "notes.md"
        target.write_text("# Notes\n", encoding="utf-8", newline="\n")
        lock = fs_lock.edit_lock_path(target)
        self.assertEqual(
            lock.parent,
            self.fake_root / memar_fs.TEMP_DIRNAME / fs_lock.EDIT_LOCK_DIR_NAME,
        )

    def test_the_intent_note_lands_beside_its_lock_under_that_root(self) -> None:
        target = self.fake_root / "notes.md"
        lock = fs_lock.edit_lock_path(target)
        intent = fs_lock.edit_intent_path(lock)
        self.assertEqual(intent.parent, lock.parent)
        self.assertEqual(intent.name, lock.name + ".intent.json")

    def test_closing_this_sessions_folder_leaves_the_lock_root_alone(self) -> None:
        # The scratch root is shared; a session's own folder is not the world.
        # Reaping one must not be able to reach the lock directory beside it.
        sid, path = session_tool.ensure_session("s-3")
        with unittest.mock.patch.object(session_tool, "soft_delete") as trash:
            closed, closed_path, removed = session_tool.close_session(sid)
        self.assertTrue(removed)
        self.assertEqual(closed_path, Path(path))
        trash.assert_called_once_with(path)
        self.assertTrue(self.fake_root.is_dir())


class RecoverableClose(Fixture):
    def test_close_moves_the_folder_with_its_contents_to_recoverable_storage(self) -> None:
        sid, path = session_tool.ensure_session("s-recover")
        marker = path / "notes.md"
        marker.write_text("# Keep me\n", encoding="utf-8", newline="\n")
        bin_path = self.fake_root / "recycle-bin"
        bin_path.mkdir()

        def move_to_bin(source: Path) -> None:
            shutil.move(str(source), str(bin_path / source.name))

        with unittest.mock.patch.object(session_tool, "soft_delete", side_effect=move_to_bin) as trash:
            closed, closed_path, removed = session_tool.close_session(sid)
            self.assertEqual((closed, closed_path, removed), (sid, path, True))
            trash.assert_called_once_with(path)
            self.assertFalse(path.exists())
            self.assertEqual((bin_path / sid / "notes.md").read_text(encoding="utf-8"), "# Keep me\n")
            self.assertEqual(session_tool.close_session(sid), (sid, path, False))
            trash.assert_called_once()
            shutil.move(str(bin_path / sid), str(path))
            self.assertEqual(marker.read_text(encoding="utf-8"), "# Keep me\n")

    def test_failed_trash_leaves_the_folder_in_place(self) -> None:
        sid, path = session_tool.ensure_session("s-failed")
        with unittest.mock.patch.object(session_tool, "soft_delete", side_effect=OSError("trash unavailable")):
            with self.assertRaises(OSError):
                session_tool.close_session(sid)
        self.assertTrue(path.is_dir())


class MintedIdUnique(unittest.TestCase):
    """The id a session gets when it does not bring one.

    Minting happens in the module beside the command rather than in the command,
    so a caller that needs an id without running a session can have one; what
    makes it an identity rather than a label is that no two calls agree, which is
    the one property a shared scratch root depends on.
    """

    def test_two_minted_ids_differ(self) -> None:
        self.assertNotEqual(memar_session.new_session_id(), memar_session.new_session_id())


if __name__ == "__main__":
    unittest.main(verbosity=2)
