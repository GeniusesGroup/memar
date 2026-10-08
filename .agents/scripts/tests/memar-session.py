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
  IdleSessionsReaped `new` moves to the trash every session folder nothing
                     inside has changed in for the idle limit, so no session
                     has to spend a message asking for its own close. Idle is
                     measured over every file inside, because a folder's own
                     time does not change when a nested file is edited. Only
                     folders named as this tool names a session are reaped,
                     never the one being opened or continued. The limit is the
                     number `SESSION_IDLE_DAYS` in the tool's own file. The
                     caller is not told what was reaped: that was not their
                     session. A folder that will not go does not stop the new
                     session from opening.
  SweptOnceADay      Only the first `new` of a day walks the session folders;
                     every later one that day reads one small file and stops,
                     because a person opening dozens of sessions a day would
                     otherwise walk hundreds of folders each time.
  SessionLog         Opening, closing, reaping, and each day's sweep are
                     recorded as one line each in the scratch root's session
                     log, which is where a person looks for a folder that is no
                     longer there. The day's sweep also moves lines older than
                     four idle limits out of the log and into the trash, so the
                     log stays small and nothing in it is lost for good.

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
import time
import unittest
import unittest.mock
from datetime import datetime, timedelta, timezone
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
        for phrase in (
            "memar session new",
            "memar session close",
            "--session-id",
            "person who started",
            "recycle bin",
            f"{session_tool.SESSION_IDLE_DAYS} days",
            "Once a day",
        ):
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


DAY = 24 * 60 * 60
# Ids in the form this tool mints, so the reaper recognizes them as sessions.
IDLE = "1111-18dc000000000001-0"
OTHER = "2222-18dc000000000002-0"


def make_idle(path: Path, days: float) -> None:
    """Set every time inside PATH, and PATH's own, to DAYS ago."""
    when = time.time() - days * DAY
    for entry in sorted(path.rglob("*"), key=lambda p: len(p.parts), reverse=True):
        os.utime(entry, (when, when))
    os.utime(path, (when, when))


class ScratchWithTrash(Fixture):
    """A scratch root with session folders of chosen ages and a stand-in trash."""

    def setUp(self) -> None:
        super().setUp()
        self.temp = self.fake_root / memar_fs.TEMP_DIRNAME
        self.temp.mkdir(parents=True, exist_ok=True)
        self.trashed: list[Path] = []

        # The platform trash is not this suite's to call. The stand-in records
        # the path and removes it, inside this scratch.
        def move_aside(path: Path) -> None:
            self.trashed.append(Path(path))
            if Path(path).is_dir():
                shutil.rmtree(path)
            else:
                Path(path).unlink()

        self.trash = unittest.mock.patch.object(session_tool, "soft_delete", side_effect=move_aside)
        self.trash.start()
        self.addCleanup(self.trash.stop)

    def folder(self, name: str, idle_days: float, *, recent_file: bool = False) -> Path:
        path = self.temp / name
        (path / "work").mkdir(parents=True)
        (path / "work" / "notes.md").write_text("# Notes\n", encoding="utf-8", newline="\n")
        make_idle(path, idle_days)
        if recent_file:
            os.utime(path / "work" / "notes.md", None)
        return path

    def run_new(self, *arguments: str, new_day: bool = True) -> tuple[str, str]:
        if new_day:
            (self.temp / session_tool.SWEPT_MARKER_NAME).unlink(missing_ok=True)
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = session_tool.main(["new", *arguments])
        self.assertEqual(code, 0)
        return out.getvalue(), err.getvalue()


class IdleSessionsReaped(ScratchWithTrash):
    def test_a_session_idle_past_the_limit_goes_to_the_trash(self) -> None:
        idle = self.folder(IDLE, 8)
        self.run_new()
        self.assertEqual(self.trashed, [idle])

    def test_a_session_inside_the_limit_is_kept(self) -> None:
        kept = self.folder(IDLE, 6)
        self.run_new()
        self.assertEqual(self.trashed, [])
        self.assertTrue(kept.is_dir())

    def test_a_file_changed_deep_inside_keeps_the_session(self) -> None:
        # The folder's own time is old; only the nested file is recent. That is
        # what a session editing its notes looks like on Windows.
        kept = self.folder(IDLE, 8, recent_file=True)
        self.run_new()
        self.assertEqual(self.trashed, [])
        self.assertTrue(kept.is_dir())

    def test_only_folders_named_as_sessions_are_reaped(self) -> None:
        for name in ("images", "memar-edit-locks", "s-old"):
            self.folder(name, 30)
        self.run_new()
        self.assertEqual(self.trashed, [])

    def test_the_session_being_continued_is_never_reaped(self) -> None:
        kept = self.folder(IDLE, 30)
        self.run_new("--session-id", IDLE)
        self.assertEqual(self.trashed, [])
        self.assertTrue(kept.is_dir())

    def test_the_limit_is_the_number_in_the_tools_file(self) -> None:
        self.assertEqual(session_tool.SESSION_IDLE_DAYS, 7)
        self.assertNotIn("os.environ", Path(session_tool.__file__).read_text(encoding="utf-8"))
        with unittest.mock.patch.object(session_tool, "SESSION_IDLE_DAYS", 10):
            self.folder(IDLE, 8)
            older = self.folder(OTHER, 11)
            self.run_new()
        self.assertEqual(self.trashed, [older])

    def test_the_caller_is_not_told_what_was_reaped(self) -> None:
        self.folder(IDLE, 8)
        out, err = self.run_new()
        self.assertEqual(len(self.trashed), 1)
        self.assertNotIn(IDLE, out + err)

    def test_a_folder_that_will_not_go_does_not_stop_the_new_session(self) -> None:
        stuck = self.folder(IDLE, 8)
        idle = self.folder(OTHER, 8)
        self.trash.stop()

        def refuse_one(path: Path) -> None:
            if Path(path) == stuck:
                raise SystemExit(f"error: Recycle Bin move failed: {path}")
            self.trashed.append(Path(path))
            shutil.rmtree(path)

        with unittest.mock.patch.object(session_tool, "soft_delete", side_effect=refuse_one):
            self.run_new()
        self.trash.start()
        self.assertEqual(self.trashed, [idle])
        self.assertTrue(stuck.is_dir())


class SweptOnceADay(ScratchWithTrash):
    def test_a_later_new_on_the_same_day_does_not_sweep(self) -> None:
        self.run_new()
        idle = self.folder(IDLE, 8)
        with unittest.mock.patch.object(session_tool, "last_change") as walked:
            self.run_new(new_day=False)
        walked.assert_not_called()
        self.assertEqual(self.trashed, [])
        self.assertTrue(idle.is_dir())

    def test_the_first_new_of_the_next_day_sweeps_again(self) -> None:
        self.run_new()
        idle = self.folder(IDLE, 8)
        marker = self.temp / session_tool.SWEPT_MARKER_NAME
        marker.write_text("2000-01-01\n", encoding="utf-8", newline="\n")
        self.run_new(new_day=False)
        self.assertEqual(self.trashed, [idle])
        self.assertNotEqual(marker.read_text(encoding="utf-8"), "2000-01-01\n")


class SessionLog(ScratchWithTrash):
    def log(self) -> str:
        return (self.temp / session_tool.SESSION_LOG_NAME).read_text(encoding="utf-8")

    def events(self) -> list[tuple[str, str]]:
        return [tuple(line.split("\t")[1:3]) for line in self.log().splitlines()]

    def test_opening_and_closing_are_recorded(self) -> None:
        self.run_new("--session-id", OTHER)
        with contextlib.redirect_stdout(io.StringIO()):
            session_tool.main(["close", "--session-id", OTHER])
        self.assertIn(("opened", OTHER), self.events())
        self.assertIn(("closed", OTHER), self.events())

    def test_the_log_keeps_four_idle_limits(self) -> None:
        self.assertEqual(session_tool.LOG_KEEP_DAYS, 4 * session_tool.SESSION_IDLE_DAYS)

    def test_old_lines_leave_the_log_for_the_trash(self) -> None:
        now = datetime.now(timezone.utc)
        old = (now - timedelta(days=session_tool.LOG_KEEP_DAYS + 1)).isoformat(timespec="seconds")
        recent = (now - timedelta(days=1)).isoformat(timespec="seconds")
        log = self.temp / session_tool.SESSION_LOG_NAME
        log.write_text(
            f"{old}\topened\t{IDLE}\t\n{recent}\topened\t{OTHER}\t\nnot a record\n",
            encoding="utf-8",
            newline="\n",
        )
        moved: list[str] = []
        self.trash.stop()

        def keep_what_was_moved(path: Path) -> None:
            if Path(path).is_file():
                moved.append(Path(path).read_text(encoding="utf-8"))
                Path(path).unlink()

        with unittest.mock.patch.object(session_tool, "soft_delete", side_effect=keep_what_was_moved):
            self.run_new()
        self.trash.start()
        self.assertEqual(moved, [f"{old}\topened\t{IDLE}\t\n"])
        text = self.log()
        self.assertNotIn(old, text)
        self.assertIn(f"{recent}\topened\t{OTHER}", text)
        self.assertIn("not a record", text)

    def test_each_days_sweep_is_recorded_once(self) -> None:
        self.run_new()
        self.run_new(new_day=False)
        self.assertEqual([event for event, _ in self.events() if event == "swept"], ["swept"])

    def test_a_reap_is_recorded_with_how_long_it_was_idle(self) -> None:
        self.folder(IDLE, 8)
        self.run_new("--session-id", OTHER)
        reaped = [line.split("\t") for line in self.log().splitlines() if f"\treaped\t{IDLE}" in line]
        self.assertEqual(len(reaped), 1)
        self.assertIn("idle", reaped[0][3])


class MintedIdUnique(unittest.TestCase):
    """The id a session gets when it does not bring one.

    Minting happens in the module beside the command rather than in the command,
    so a caller that needs an id without running a session can have one; what
    makes it an identity rather than a label is that no two calls agree, which is
    the one property a shared scratch root depends on.
    """

    def test_two_minted_ids_differ(self) -> None:
        self.assertNotEqual(memar_session.new_session_id(), memar_session.new_session_id())

    def test_a_name_sort_is_creation_order(self) -> None:
        # The clock leads, so any file listing sorted by name lists sessions in
        # the order they were opened, and the date is readable off the name.
        import time

        minted = memar_session.new_session_id()
        self.assertRegex(minted, r"^\d{8}T\d{6}Z-")
        self.assertTrue(minted.startswith(time.strftime("%Y%m%d", time.gmtime())))
        self.assertLess("20261008T082722Z-99999-0", "20261008T082723Z-1-0")
        self.assertTrue(memar_session.is_session_id(minted))

    def test_a_folder_named_in_the_earlier_form_is_still_a_session(self) -> None:
        # Folders opened before the clock came first must still be reaped.
        self.assertTrue(memar_session.is_session_id("34852-18dc8080b906c944-0"))
        self.assertFalse(memar_session.is_session_id("repo_tree.md"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
