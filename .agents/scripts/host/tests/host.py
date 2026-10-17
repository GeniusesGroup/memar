#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the constraints `host/fs.py` and `host/git.py` hold a session to.

    python .agents/scripts/host/tests/host.py

Nothing here deletes anything but the scratch repository the commit tests make
for themselves beside this file. The trash verbs are asserted by what they refuse
and by what they would do, and the one path the suite would have had to remove
is never created: a test that trashes a real file proves a platform API works,
which is the platform's test, and the failure mode it leaves behind is a file
this repository no longer has.

What is pinned, and what each pin is for:

  NothingIsPermanent     No verb in this shelf deletes. Permanent deletion is
                         the failure both files exist to prevent: a session that
                         deep-deletes then needs the file pays for it in
                         reconstructed tokens.
  RefusesWhenAbsent      A path that is not there is reported rather than
                         resolved against something else. A typo in a delete is
                         worse than no delete.
  RestoreRefusesFirst    Discarding uncommitted work needs an explicit
                         irreversible token, because tidying status is exactly
                         what sessions do when they lose work by accident.
  RenameIsHistoryKeeping A move goes through `git mv`, which records the rename;
                         a plain move leaves history behind claiming the file
                         was always somewhere else.
  StashIsNotDiscard      Parking work is recoverable, and ignored paths are
                         left alone — a stash that claimed to hold everything
                         would be a way to lose an ignored file.
  TempIsNotAPath         There is no verb that prints the operating system's
                         temporary directory. Session scratch has one home
                         under the checkout, and a command whose output is the
                         path that rule forbids invites the failure the rule
                         exists to stop.
  HelpStatesItsOwnWork   Neither file's overview lists or describes its own
                         commands: argparse lists them, and each command's own
                         --help states its work.
  ShelfIsNotRouted       Neither file is a `memar` verb, and the path carries
                         that claim: these constrain the host's tools, which is
                         not a thing Memar offers.
  CommitTakesOnlyWhatItNames
                         A commit in a shared tree carries the paths it names
                         and nothing another session staged, and a fold never
                         rewrites what is already upstream. A move `rename`
                         staged is taken only when both of its paths are named,
                         the destination through `--as` only when its file is
                         the staged blob, and a removal `remove` staged only
                         when the file is gone from the tree too. The shared
                         index gets the commit's entries in one write,
                         whatever the names, modes, additions and removals.
  UncommitKeepsTheWork   Taking back a commit moves HEAD to its parent only
                         when the caller named that commit, it has one parent,
                         and it is not upstream; its work stays in the tree,
                         unstaged, another session's staging stays staged, and
                         the commit stays in the reflog the command points to.
  CommitWaitsOutALock    A lock another git process holds is waited for, and a
                         commit finishes once it is let go. One held past the
                         wait stops the commit before HEAD moves, naming the
                         lock, its age, and the stage, and so does an uncommit;
                         one taken after HEAD moved stops either with the
                         commands that finish or undo it, which work and
                         refuse once a path is staged or HEAD has moved since,
                         and the undo once the finish has run. A staged rename
                         the commit took is no one else's staging: it finishes,
                         and an undo leaves it staged.
                         A failure that is not a lock is not retried. No lock
                         is ever deleted by the command.
  CommitCitesItsSessions A commit names the sessions it carries out, one
                         `Session:` trailer each, which the verb writes from
                         `--session-id` and `git log` reads back beside the
                         message's other trailers. One that cites none is
                         refused with the form it wants unless it says
                         `--no-session`; an id `memar session show` cannot
                         find, or one written into the message by hand, is
                         refused; a fold keeps the sessions it replaces.
"""

from __future__ import annotations

import ast
import importlib.util
import re
import sys
import unittest
from importlib.machinery import SourceFileLoader
from pathlib import Path

TESTS = Path(__file__).resolve().parent
HOST = TESTS.parent
SCRIPTS = HOST.parent
# This file is itself named host.py: its own folder must not hide the `host` package from the verbs' imports.
sys.path[:] = [entry for entry in sys.path if Path(entry or ".").resolve() != TESTS]
sys.path.insert(0, str(SCRIPTS))
# The checkout's top too: the records branch's layout is asked of `services/`, whose types import from `modules/`.
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True

from machine.fs_test_scratch import suite_scratch


def read(name: str) -> str:
    """A file of the shelf; `git.py` is read as all the files it is made of, entry and verbs together."""
    if name == "git.py":
        files = [HOST / "git.py", *sorted(HOST.glob("git_*.py"))]
        texts = [file.read_text(encoding="utf-8") for file in files]
        return "\n".join(text.replace("from __future__ import annotations", "") for text in texts)
    return (HOST / name).read_text(encoding="utf-8")


def verbs(name: str) -> set[str]:
    """The verbs a file declares, read from its parser rather than its prose.

    Read from the source because a test that runs the command to learn what it
    accepts would be a test of argparse on this machine. `--help` is the
    authority for usage; this is the authority for what a test may call.
    """
    found: set[str] = set()
    for node in ast.walk(ast.parse(read(name))):
        if not isinstance(node, ast.Call):
            continue
        function = node.func
        if not isinstance(function, ast.Attribute):
            continue
        if function.attr not in ("add_parser", "add_argument"):
            continue
        if not node.args:
            continue
        first = node.args[0]
        if isinstance(first, ast.Constant) and isinstance(first.value, str):
            found.add(first.value)
    return found


class NothingIsPermanent(unittest.TestCase):
    def test_no_verb_asks_the_host_to_delete_unrecoverably(self) -> None:
        for name in ("fs.py", "git.py"):
            with self.subTest(name=name):
                source = read(name).lower()
                for forbidden in ("unlink(", "os.remove", "rmtree(", "shutil.rm"):
                    self.assertNotIn(forbidden, source)

    def test_the_recoverable_delete_is_the_one_the_fs_shelf_uses(self) -> None:
        self.assertIn("soft_delete", read("fs.py"))
        self.assertIn("from machine.fs_trash import soft_delete", read("fs.py"))

    def test_the_git_shelf_delegates_deletion_to_the_fs_shelf(self) -> None:
        source = read("git.py")
        self.assertIn('"trash"', source)
        self.assertIn("fs.py", source)


class RefusesWhenAbsent(unittest.TestCase):
    def test_trashing_something_that_is_not_there_is_refused(self) -> None:
        from machine.fs_trash import soft_delete

        missing = TESTS / "no-such-path-to-trash"
        with self.assertRaises(SystemExit) as raised:
            soft_delete(missing)
        self.assertIn("does not exist", str(raised.exception))

    def test_a_source_that_is_not_there_is_refused_rather_than_moved(self) -> None:
        self.assertIn("source does not exist", read("git.py"))


class RestoreRefusesFirst(unittest.TestCase):
    TOKEN = "DISCARD-UNCOMMITTED"

    def test_the_token_is_declared_once_and_used_once(self) -> None:
        source = read("git.py")
        self.assertIn(f'DISCARD_CONFIRM = "{self.TOKEN}"', source)
        # A second spelling of the token would be a second way to discard, and
        # the token's whole weight is that there is exactly one.
        self.assertEqual(source.count(f'"{self.TOKEN}"'), 1)

    def test_discarding_without_the_token_refuses_and_says_what_to_do(self) -> None:
        from importlib.machinery import SourceFileLoader

        module = _load("host_git_restore", "git_restore.py")
        with self.assertRaises(SystemExit) as raised:
            module.cmd_restore(TESTS, [TESTS], None)
        message = str(raised.exception)
        self.assertIn("refusing to discard", message)
        self.assertIn("stash", message)
        self.assertIn(self.TOKEN, message)

    def test_discarding_needs_a_path_too(self) -> None:
        module = _load("host_git_restore", "git_restore.py")
        with self.assertRaises(SystemExit) as raised:
            module.cmd_restore(TESTS, [], self.TOKEN)
        self.assertIn("requires one or more paths", str(raised.exception))


class RenameIsHistoryKeeping(unittest.TestCase):
    def test_a_move_goes_through_git_mv_not_a_plain_move(self) -> None:
        source = read("git.py")
        self.assertIn('run_git(["mv",', source)
        for plain in ("shutil.move(", "os.rename(", "os.replace("):
            self.assertNotIn(plain, source)

    def test_a_rename_rides_with_the_task_while_git_detects_it(self) -> None:
        # A rename whose edit breaks rename detection defeats the history this
        # command exists to preserve; the rule says the rename rides with the
        # task's commit only while git still detects it.
        self.assertIn("The rename rides with the task's commit", read("git.py"))
        self.assertIn("while git still detects it", read("git.py"))


class StashIsNotDiscard(unittest.TestCase):
    def test_stashing_carries_untracked_work_and_says_ignored_is_left_alone(self) -> None:
        source = read("git.py")
        self.assertIn("--include-untracked", source)
        self.assertIn("Ignored paths were not included", source)

    def test_a_clean_tree_is_not_stashed_at_all(self) -> None:
        # Parking work is for work there is; a stash of nothing is a stash entry
        # a later session will have to read to learn that nothing happened.
        module = _load("host_git_stash", "git_stash.py")
        module._working_tree_dirty = lambda root: False
        import io
        import contextlib

        with contextlib.redirect_stderr(io.StringIO()) as said:
            module.cmd_stash(TESTS, None)
        self.assertIn("nothing to stash", said.getvalue())


class TempIsNotAPath(unittest.TestCase):
    """The absent command, pinned so its absence is not read as an oversight."""

    def test_no_verb_prints_the_operating_system_temporary_directory(self) -> None:
        for name in ("fs.py", "git.py"):
            with self.subTest(name=name):
                self.assertNotIn("temp", verbs(name))
                source = read(name)
                self.assertNotIn("tempfile.gettempdir", source)
                self.assertNotIn("canonical_temp", source)

    def test_the_absence_is_stated_rather_than_left_to_a_reader(self) -> None:
        # An absent command looks like a missing one until the file says why.
        self.assertIn("temporary directory", read("fs.py"))


class HelpStatesItsOwnWork(unittest.TestCase):
    """Each help states its own work (owner, 2026-10-14): argparse lists the commands."""

    def test_neither_files_overview_lists_or_describes_its_commands(self) -> None:
        for name in ("fs.py", "git.py"):
            spec = importlib.util.spec_from_file_location(f"host_{Path(name).stem}", HOST / name)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            commands = {
                node.args[0].value
                for node in ast.walk(ast.parse(read(name)))
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "add_parser"
                and node.args and isinstance(node.args[0], ast.Constant)
            }
            self.assertTrue(commands)
            for command in commands:
                with self.subTest(name=name, command=command):
                    self.assertIsNone(re.search(rf"^\s+{re.escape(command)}\s{{2,}}\S", module.DESCRIPTION, re.MULTILINE))
                    self.assertNotIn(f"`{command}`", module.DESCRIPTION)


class ShelfIsNotRouted(unittest.TestCase):
    def test_the_router_routes_no_file_of_this_shelf(self) -> None:
        # The launcher may name the shelf's README to say why it is absent — that
        # is the routing being explained. What it must not do is route there: it
        # assembles its verbs from the services shelf alone, so no file of this
        # shelf may be one of those services, and no constant may name one.
        launcher = (SCRIPTS / "memar").read_text(encoding="utf-8")
        for name in ("fs.py", "git.py", '"host"', "'host'"):
            with self.subTest(name=name):
                self.assertNotIn(name, launcher)
        spec = importlib.util.spec_from_loader("memar_launcher", SourceFileLoader("memar_launcher", str(SCRIPTS / "memar")))
        router = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(router)
        services = router.services()
        for name in ("fs.py", "git.py"):
            with self.subTest(name=name):
                self.assertTrue((HOST / name).is_file())
                self.assertNotIn(Path(name).stem, services)
                self.assertFalse(any(path.endswith("." + Path(name).stem) for path in router.catalog().values()))

    def test_neither_file_is_a_memar_verb(self) -> None:
        import os
        import subprocess

        for verb in ("fs", "git"):
            with self.subTest(verb=verb):
                asked = subprocess.run(
                    [sys.executable, str(SCRIPTS / "memar"), verb, "--help"],
                    capture_output=True, text=True, encoding="utf-8", errors="replace",
                    env=dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1"),
                )
                self.assertEqual(asked.returncode, 2, asked.stdout)
                self.assertIn("invalid choice", asked.stderr)

    def test_the_shelf_states_why_it_is_not_under_memar(self) -> None:
        readme = (HOST / "README.md").read_text(encoding="utf-8")
        self.assertIn("not under `memar`", readme)
        self.assertIn("host tool", readme.lower())


class ScratchRepository(unittest.TestCase):
    """A throwaway repository with three files committed once, and git asked of it."""

    def setUp(self) -> None:
        import tempfile

        scratch = tempfile.TemporaryDirectory(
            dir=suite_scratch(),
            prefix="tmp-host-commit-",
            ignore_cleanup_errors=True,
        )
        self.addCleanup(scratch.cleanup)
        self.repo = Path(scratch.name)
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.name", "Test")
        self.git("config", "user.email", "test@example.org")
        self.git("config", "core.autocrlf", "false")
        for name in ("mine.md", "theirs.md", "shared.md"):
            self.put(name, "base\n")
        self.git("add", ".")
        self.git("commit", "-q", "-m", "base")
        self.base = self.git("rev-parse", "HEAD")
        self.message = self.repo / ".git" / "message.txt"
        self.message.write_text("subject\n", encoding="utf-8", newline="\n")
        # Another repository, the folder the repository verbs are run from: a verb
        # that read the current folder would act on it, and its tip would move.
        elsewhere = tempfile.TemporaryDirectory(
            dir=suite_scratch(),
            prefix="tmp-host-elsewhere-",
            ignore_cleanup_errors=True,
        )
        self.addCleanup(elsewhere.cleanup)
        self.elsewhere = Path(elsewhere.name)
        self.git_in(self.elsewhere, "init", "-q", "-b", "main")
        self.git_in(self.elsewhere, "config", "user.name", "Other")
        self.git_in(self.elsewhere, "config", "user.email", "other@example.org")
        (self.elsewhere / "other.md").write_text("other\n", encoding="utf-8", newline="\n")
        self.git_in(self.elsewhere, "add", ".")
        self.git_in(self.elsewhere, "commit", "-q", "-m", "other")
        self.elsewhere_tip = self.git_in(self.elsewhere, "rev-parse", "HEAD")
        self.addCleanup(self.assert_elsewhere_untouched)

    def git(self, *args: str) -> str:
        return self.git_in(self.repo, *args)

    def git_in(self, folder: Path, *args: str) -> str:
        import subprocess

        return subprocess.run(
            ["git", "-C", str(folder), *args],
            capture_output=True, text=True, check=True,
        ).stdout.strip()

    def assert_elsewhere_untouched(self) -> None:
        self.assertEqual(self.git_in(self.elsewhere, "rev-parse", "HEAD"), self.elsewhere_tip)
        self.assertEqual(self.git_in(self.elsewhere, "status", "--porcelain"), "")

    def put(self, name: str, text: str) -> None:
        (self.repo / name).write_text(text, encoding="utf-8", newline="\n")

    # The verbs that act on a repository the caller names, and are run from
    # another folder to prove they do not read the one they are run from.
    REPOSITORY_VERBS = ("commit", "uncommit", "reindex", "record", "rename", "remove", "stash", "restore", "undelete")

    def host_git(self, *args: str):
        import subprocess

        if args[0] in self.REPOSITORY_VERBS:
            return subprocess.run(
                [sys.executable, str(HOST / "git.py"), args[0], "--repository", str(self.repo), *args[1:]],
                cwd=self.elsewhere, capture_output=True, text=True,
            )
        return subprocess.run(
            [sys.executable, str(HOST / "git.py"), *args],
            cwd=self.repo, capture_output=True, text=True,
        )

    def commit(self, *args: str):
        """A commit that carries out no session, as every test of what a commit takes makes: the sessions it cites are `CommitCitesItsSessions`' subject."""
        return self.host_git("commit", "-F", str(self.message), "--no-session", *args)

    def a_file_long_enough_to_keep_a_rename(self) -> str:
        """Commit mine.md long enough that a license header added to it leaves git pairing a move of it."""
        body = "".join(f"line {number}\n" for number in range(20))
        self.put("mine.md", body)
        self.git("commit", "-q", "-am", "body")
        self.base = self.git("rev-parse", "HEAD")
        return body


class EveryWorkingVerbTakesTheRepository(ScratchRepository):
    """rename, remove, stash, restore and undelete act on the repository --repository names, never the folder they run from."""

    def test_each_of_them_requires_the_repository_flag(self) -> None:
        import subprocess

        for verb, rest in (
            ("rename", ["mine.md", "moved.md"]),
            ("remove", ["mine.md"]),
            ("stash", []),
            ("restore", ["mine.md"]),
            ("undelete", ["mine.md"]),
        ):
            with self.subTest(verb=verb):
                done = subprocess.run(
                    [sys.executable, str(HOST / "git.py"), verb, *rest],
                    cwd=self.repo, capture_output=True, text=True,
                )
                self.assertNotEqual(done.returncode, 0)
                self.assertIn("--repository", done.stderr)
        self.assertEqual(self.git("status", "--porcelain"), "")

    def test_a_rename_moves_inside_the_repository_named_with_relative_paths(self) -> None:
        done = self.host_git("rename", "mine.md", "moved.md")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertTrue((self.repo / "moved.md").exists())
        self.assertFalse((self.repo / "mine.md").exists())
        self.assertIn("R  mine.md -> moved.md", self.git("status", "--porcelain"))

    def test_a_remove_trashes_and_stages_inside_the_repository_named(self) -> None:
        done = self.host_git("remove", "mine.md")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertFalse((self.repo / "mine.md").exists())
        self.assertIn("D  mine.md", self.git("status", "--porcelain"))

    def test_a_stash_sets_aside_the_work_of_the_repository_named(self) -> None:
        self.put("mine.md", "edited\n")
        done = self.host_git("stash")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(self.git("status", "--porcelain"), "")
        self.assertIn("stash@{0}", self.git("stash", "list"))

    def test_a_restore_discards_in_the_repository_named_only_with_the_token(self) -> None:
        self.put("mine.md", "edited\n")
        refused = self.host_git("restore", "mine.md")
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("M mine.md", self.git("status", "--porcelain"))
        done = self.host_git("restore", "--confirm", "DISCARD-UNCOMMITTED", "mine.md")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(self.git("status", "--porcelain"), "")

    def test_an_undelete_brings_a_path_back_in_the_repository_named(self) -> None:
        (self.repo / "mine.md").unlink()
        done = self.host_git("undelete", "mine.md")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual((self.repo / "mine.md").read_text(encoding="utf-8"), "base\n")
        self.assertEqual(self.git("status", "--porcelain"), "")

    def test_a_path_outside_the_repository_is_refused(self) -> None:
        done = self.host_git("remove", str(self.elsewhere / "other.md"))
        self.assertNotEqual(done.returncode, 0)
        self.assertIn("not inside the repository", done.stderr)
        self.assertTrue((self.elsewhere / "other.md").exists())

    def test_no_verb_that_acts_on_a_repository_reads_the_folder_it_runs_from(self) -> None:
        source = read("git.py")
        self.assertNotIn("def run_git(args: list[str])", source)
        self.assertNotIn("cwd=str(cwd) if cwd else None", source)


class CommitTakesOnlyWhatItNames(ScratchRepository):
    def test_a_named_path_is_committed_and_another_sessions_staging_stays_staged(self) -> None:
        self.put("mine.md", "mine\n")
        self.put("theirs.md", "theirs\n")
        self.git("add", "theirs.md")
        done = self.commit("mine.md")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(self.git("show", "--name-only", "--format=", "HEAD"), "mine.md")
        self.assertEqual(self.git("diff", "--cached", "--name-only"), "theirs.md")
        self.assertEqual(self.git("status", "--porcelain", "--", "mine.md"), "")

    def test_a_path_someone_else_staged_is_refused(self) -> None:
        self.put("theirs.md", "theirs\n")
        self.git("add", "theirs.md")
        done = self.commit("theirs.md")
        self.assertNotEqual(done.returncode, 0)
        self.assertIn("staged change", done.stderr)
        self.assertEqual(self.git("rev-parse", "HEAD"), self.base)

    def test_a_move_rename_staged_is_committed_with_an_edit_that_keeps_the_rename(self) -> None:
        body = self.a_file_long_enough_to_keep_a_rename()
        moved = self.host_git("rename", "mine.md", "moved.md")
        self.assertEqual(moved.returncode, 0, moved.stderr)
        self.put("moved.md", "/* license */\n\n" + body)
        done = self.commit("mine.md", "moved.md")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertTrue(self.git("show", "HEAD:moved.md").startswith("/* license */"))
        self.assertRegex(self.git("diff-tree", "-r", "-M", "--name-status", "HEAD^", "HEAD"), r"^R\d+\tmine.md\tmoved.md$")
        self.assertEqual(self.git("status", "--porcelain", "--", "mine.md", "moved.md"), "")

    def test_a_move_staged_with_an_edit_another_session_staged_is_committed(self) -> None:
        body = self.a_file_long_enough_to_keep_a_rename()
        self.git("mv", "mine.md", "moved.md")
        self.put("moved.md", "/* license */\n\n" + body)
        self.git("add", "moved.md")
        done = self.commit("mine.md", "moved.md")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertRegex(self.git("diff-tree", "-r", "-M", "--name-status", "HEAD^", "HEAD"), r"^R\d+\tmine.md\tmoved.md$")
        self.assertEqual(self.git("diff", "--cached", "--name-only"), "")

    def test_a_move_whose_edit_loses_the_rename_is_refused(self) -> None:
        moved = self.host_git("rename", "mine.md", "moved.md")
        self.assertEqual(moved.returncode, 0, moved.stderr)
        self.put("moved.md", "something else entirely\n")
        done = self.commit("mine.md", "moved.md")
        self.assertNotEqual(done.returncode, 0)
        self.assertIn("no longer sees mine.md -> moved.md as a rename", done.stderr)
        self.assertEqual(self.git("rev-parse", "HEAD"), self.base)
        self.assertEqual(self.git("diff", "--cached", "-M", "--name-status"), "R100\tmine.md\tmoved.md")

    def test_a_staged_move_named_at_one_end_only_is_refused(self) -> None:
        self.host_git("rename", "mine.md", "moved.md")
        done = self.commit("moved.md")
        self.assertNotEqual(done.returncode, 0)
        self.assertIn("staged change", done.stderr)
        self.assertEqual(self.git("rev-parse", "HEAD"), self.base)

    def test_a_staged_move_edited_since_is_committed_alone_through_as(self) -> None:
        moved = self.host_git("rename", "mine.md", "moved.md")
        self.assertEqual(moved.returncode, 0, moved.stderr)
        self.put("moved.md", "base\nedited\n")
        staged = self.repo / ".git" / "moved.staged"
        staged.write_text("base\n", encoding="utf-8", newline="\n")
        done = self.commit("mine.md", "--as", f"moved.md={staged}")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(
            self.git("diff-tree", "-r", "-M100%", "--name-status", "HEAD^", "HEAD"), "R100\tmine.md\tmoved.md"
        )
        self.assertEqual(self.git("diff", "--cached", "--name-only"), "")
        self.assertEqual(self.git("diff", "--name-only"), "moved.md")
        self.assertEqual((self.repo / "moved.md").read_text(encoding="utf-8"), "base\nedited\n")

    def test_an_as_file_that_is_not_the_staged_blob_does_not_make_a_move(self) -> None:
        self.host_git("rename", "mine.md", "moved.md")
        self.put("moved.md", "base\nedited\n")
        other = self.repo / ".git" / "moved.other"
        other.write_text("base\nedited\n", encoding="utf-8", newline="\n")
        done = self.commit("mine.md", "--as", f"moved.md={other}")
        self.assertNotEqual(done.returncode, 0)
        self.assertIn("staged change", done.stderr)
        self.assertEqual(self.git("rev-parse", "HEAD"), self.base)
        self.assertEqual(self.git("diff", "--cached", "-M", "--name-status"), "R100\tmine.md\tmoved.md")

    def test_a_removal_staged_by_remove_is_committed(self) -> None:
        # `remove` trashes the file and stages its removal; the stand-in does
        # the same without reaching the platform trash.
        (self.repo / "mine.md").unlink()
        self.git("rm", "-q", "--cached", "mine.md")
        done = self.commit("mine.md")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(self.git("ls-tree", "--name-only", "HEAD", "mine.md"), "")
        self.assertEqual(self.git("status", "--porcelain", "--", "mine.md"), "")

    def test_a_staged_removal_of_a_file_still_there_is_refused(self) -> None:
        self.git("rm", "-q", "--cached", "mine.md")
        done = self.commit("mine.md")
        self.assertNotEqual(done.returncode, 0)
        self.assertIn("staged change", done.stderr)
        self.assertEqual(self.git("rev-parse", "HEAD"), self.base)

    def test_a_fold_replaces_the_last_commit_and_leaves_out_a_change_unstaged(self) -> None:
        self.put("mine.md", "mine\n")
        self.put("shared.md", "shared\n")
        self.git("commit", "-q", "-am", "second")
        done = self.commit("--fold", "1", "--leave-out", "shared.md")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(self.git("rev-parse", "HEAD^"), self.base)
        self.assertEqual(self.git("show", "HEAD:mine.md"), "mine")
        self.assertEqual(self.git("show", "HEAD:shared.md"), "base")
        self.assertEqual(self.git("diff", "--cached", "--name-only"), "")
        self.assertEqual(self.git("diff", "--name-only"), "shared.md")

    def test_a_prepared_file_commits_only_its_own_hunk(self) -> None:
        self.put("shared.md", "base\nmine\ntheirs\n")
        prepared = self.repo / ".git" / "shared.prepared"
        prepared.write_text("base\nmine\n", encoding="utf-8", newline="\n")
        done = self.commit("--as", f"shared.md={prepared}")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(self.git("show", "HEAD:shared.md"), "base\nmine")
        self.assertEqual(
            (self.repo / "shared.md").read_text(encoding="utf-8"), "base\nmine\ntheirs\n"
        )
        self.assertEqual(self.git("diff", "--cached", "--name-only"), "")

    def test_a_fold_reaching_upstream_is_refused(self) -> None:
        self.put("mine.md", "mine\n")
        self.git("commit", "-q", "-am", "second")
        self.git("branch", "published")
        self.git("branch", "--set-upstream-to=published")
        before = self.git("rev-parse", "HEAD")
        done = self.commit("--fold", "1")
        self.assertNotEqual(done.returncode, 0)
        self.assertIn("published history", done.stderr)
        self.assertEqual(self.git("rev-parse", "HEAD"), before)

    def test_the_shared_index_gets_spaces_unicode_modes_additions_and_removals_in_one_write(self) -> None:
        import os
        import subprocess

        def listed(*args: str) -> list[str]:
            out = subprocess.run(["git", "-C", str(self.repo), *args], capture_output=True, check=True).stdout
            return sorted(entry for entry in out.decode("utf-8").split("\0") if entry)

        odd = "dir with space/ünïcode.md"
        (self.repo / "dir with space").mkdir()
        self.put(odd, "odd\n")
        self.put("run.sh", "echo base\n")
        os.chmod(self.repo / "run.sh", 0o755)
        self.put("gone.md", "gone\n")
        self.git("add", "--", odd, "run.sh", "gone.md")
        self.git("update-index", "--chmod=+x", "run.sh")
        self.git("commit", "-q", "-m", "second")

        self.put(odd, "odd\nedited\n")
        self.put("run.sh", "echo edited\n")
        self.put("new file.md", "new\n")
        (self.repo / "gone.md").unlink()
        self.put("theirs.md", "theirs\n")
        self.git("add", "theirs.md")
        named = (odd, "run.sh", "new file.md", "gone.md")
        done = self.commit(*named)
        self.assertEqual(done.returncode, 0, done.stderr)

        in_head = listed("ls-tree", "-r", "-z", "HEAD", "--", *named)
        self.assertEqual(sorted(entry.split("\t")[1] for entry in in_head), sorted([odd, "new file.md", "run.sh"]))
        self.assertIn("100755 blob", next(entry for entry in in_head if entry.endswith("\trun.sh")))
        in_index = listed("ls-files", "-s", "-z", "--", *named)
        self.assertEqual(
            sorted(entry.replace(" blob ", " ") for entry in in_head),
            sorted(entry.replace(" 0\t", "\t") for entry in in_index),
        )
        self.assertEqual(listed("status", "--porcelain", "-z"), ["M  theirs.md"])


class UncommitKeepsTheWork(ScratchRepository):
    def setUp(self) -> None:
        super().setUp()
        self.put("mine.md", "mine\n")
        self.put("shared.md", "shared\n")
        self.git("commit", "-q", "-am", "second")
        self.second = self.git("rev-parse", "HEAD")

    def uncommit(self, expect: str):
        return self.host_git("uncommit", "--expect", expect)

    def test_head_goes_back_and_the_work_stays_in_the_tree_unstaged(self) -> None:
        self.put("theirs.md", "theirs\n")
        self.git("add", "theirs.md")
        done = self.uncommit(self.second[:12])
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(self.git("rev-parse", "HEAD"), self.base)
        self.assertEqual((self.repo / "mine.md").read_text(encoding="utf-8"), "mine\n")
        self.assertEqual(self.git("diff", "--name-only"), "mine.md\nshared.md")
        # Another session's staging is not the commit's, and stays staged.
        self.assertEqual(self.git("diff", "--cached", "--name-only"), "theirs.md")
        self.assertIn("reflog", done.stderr)
        self.assertIn(self.second, done.stderr)
        self.assertIn(self.second, self.git("reflog", "-n", "2", "--format=%H"))

    def test_a_commit_that_is_not_head_is_refused(self) -> None:
        done = self.uncommit(self.base)
        self.assertNotEqual(done.returncode, 0)
        self.assertIn("nothing was changed", done.stderr)
        self.assertEqual(self.git("rev-parse", "HEAD"), self.second)

    def test_a_name_instead_of_an_id_is_refused(self) -> None:
        done = self.uncommit("HEAD")
        self.assertNotEqual(done.returncode, 0)
        self.assertIn("--expect", done.stderr)
        self.assertEqual(self.git("rev-parse", "HEAD"), self.second)

    def test_a_commit_without_exactly_one_parent_is_refused(self) -> None:
        self.git("checkout", "-q", "-b", "side", self.base)
        self.put("theirs.md", "side\n")
        self.git("commit", "-q", "-am", "side")
        self.git("checkout", "-q", "main")
        self.git("merge", "-q", "--no-ff", "--no-edit", "side")
        merge = self.git("rev-parse", "HEAD")
        done = self.uncommit(merge)
        self.assertNotEqual(done.returncode, 0)
        self.assertIn("2 parents", done.stderr)
        self.assertEqual(self.git("rev-parse", "HEAD"), merge)
        self.git("checkout", "-q", "--orphan", "fresh")
        self.git("commit", "-q", "-m", "root")
        root = self.git("rev-parse", "HEAD")
        done = self.uncommit(root)
        self.assertIn("0 parents", done.stderr)
        self.assertEqual(self.git("rev-parse", "HEAD"), root)

    def test_a_commit_already_upstream_is_refused(self) -> None:
        self.git("branch", "published")
        self.git("branch", "--set-upstream-to=published")
        done = self.uncommit(self.second)
        self.assertNotEqual(done.returncode, 0)
        self.assertIn("published history", done.stderr)
        self.assertEqual(self.git("rev-parse", "HEAD"), self.second)

    def test_a_path_of_the_commit_with_its_own_staged_change_is_refused(self) -> None:
        self.put("mine.md", "mine, and more\n")
        self.git("add", "mine.md")
        done = self.uncommit(self.second)
        self.assertNotEqual(done.returncode, 0)
        self.assertIn("staged change", done.stderr)
        self.assertEqual(self.git("rev-parse", "HEAD"), self.second)
        self.assertEqual(self.git("diff", "--cached", "--name-only"), "mine.md")


class CommitWaitsOutALock(ScratchRepository):
    """Run in this process, so the wait can be shortened and git's answers stood in for."""

    def setUp(self) -> None:
        import os

        super().setUp()
        self.module = importlib.import_module("host.git_commit")
        self.uncommit_module = importlib.import_module("host.git_uncommit")
        self.lock_module = importlib.import_module("host.git_lock")
        self.run_module = importlib.import_module("host.git_run")
        self.lock = self.repo / ".git" / "index.lock"
        here = Path.cwd()
        os.chdir(self.repo)
        self.addCleanup(os.chdir, here)
        self.addCleanup(lambda: self.lock.exists() and self.lock.unlink())
        self.put("mine.md", "mine\n")

    def here(self, verb, *patches) -> tuple[str | None, str]:
        """The verb's exit message, None when it succeeded, and what it said on stderr."""
        import contextlib
        import io
        import unittest.mock

        said = io.StringIO()
        with contextlib.ExitStack() as stack:
            stack.enter_context(contextlib.redirect_stderr(said))
            stack.enter_context(contextlib.redirect_stdout(io.StringIO()))
            stack.enter_context(unittest.mock.patch.object(self.lock_module, "LOCK_WAIT_SECONDS", 0.5))
            stack.enter_context(unittest.mock.patch.object(self.lock_module, "LOCK_FIRST_PAUSE_SECONDS", 0.05))
            for patch in patches:
                stack.enter_context(patch)
            try:
                verb()
            except SystemExit as stopped:
                return str(stopped.code), said.getvalue()
        return None, said.getvalue()

    def commit_here(self, *patches) -> tuple[str | None, str]:
        return self.here(lambda: self.module.cmd_commit(self.repo, [Path("mine.md")], [], [], 0, self.message, sessions=[], no_session=True), *patches)

    def uncommit_here(self, expect: str, *patches) -> tuple[str | None, str]:
        return self.here(lambda: self.uncommit_module.cmd_uncommit(self.repo, expect), *patches)

    def grabbed_after_update_ref(self):
        """Another git process taking the index lock the moment HEAD has moved."""
        import unittest.mock

        real = self.run_module.attempt

        def grabbed(args, root, env=None, data=None):
            done = real(args, root, env, data)
            if args[0] == "update-ref":
                self.lock.write_text("", encoding="utf-8")
            return done

        return unittest.mock.patch.object(self.run_module, "attempt", grabbed)

    def held_for_an_hour(self) -> None:
        import os
        import time

        self.lock.write_text("", encoding="utf-8")
        hour_ago = time.time() - 3600
        os.utime(self.lock, (hour_ago, hour_ago))

    def stopped_after_head_moved(self) -> str:
        stopped, _ = self.commit_here(self.grabbed_after_update_ref())
        self.assertIsNotNone(stopped)
        self.lock.unlink()
        return self.git("rev-parse", "HEAD")

    def test_a_lock_let_go_within_the_wait_is_waited_for_and_the_commit_finishes(self) -> None:
        import unittest.mock

        self.lock.write_text("", encoding="utf-8")
        released = unittest.mock.patch.object(
            self.lock_module.time, "sleep", side_effect=lambda seconds: self.lock.unlink(missing_ok=True)
        )
        stopped, said = self.commit_here(released)
        self.assertIsNone(stopped, said)
        self.assertIn("waiting up to", said)
        self.assertIn("index.lock", said)
        self.assertEqual(self.git("rev-parse", "HEAD^"), self.base)
        self.assertEqual(self.git("status", "--porcelain", "--", "mine.md"), "")

    def test_a_lock_held_past_the_wait_stops_before_head_moves_and_says_why(self) -> None:
        self.held_for_an_hour()
        stopped, said = self.commit_here()
        self.assertIsNotNone(stopped)
        self.assertEqual(self.git("rev-parse", "HEAD"), self.base)
        self.assertIn("HEAD was not moved", stopped)
        self.assertIn(str(self.lock.resolve()), stopped)
        self.assertRegex(stopped, r"last written 36\d\d s ago")
        self.assertIn("never does", stopped)
        self.assertIn("rerun the same command", stopped)
        self.assertTrue(self.lock.exists())
        self.assertEqual(self.git("diff", "--name-only"), "mine.md")

    def test_a_lock_taken_after_head_moved_says_how_to_finish_and_the_finish_works(self) -> None:
        stopped, _ = self.commit_here(self.grabbed_after_update_ref())
        self.assertIsNotNone(stopped)
        made = self.git("rev-parse", "HEAD")
        self.assertEqual(self.git("rev-parse", "HEAD^"), self.base)
        self.assertIn(f"HEAD moved from {self.base} to the commit {made}", stopped)
        self.assertIn("shared index was not updated", stopped)
        self.assertIn("as it held them before this command", stopped)
        self.assertIn("update-index -z --index-info", stopped)
        self.assertIn("Unable to create", stopped)
        self.assertIn("a lock this young", stopped)
        self.assertIn("once the lock is free", stopped)
        self.assertIn(f"reindex --repository {self.repo} --from {made} --was {self.base} -- mine.md", stopped)
        self.assertIn(f"reindex --repository {self.repo} --undo --from {made} --was {self.base} -- mine.md", stopped)
        self.assertNotIn("update-ref HEAD", stopped)
        self.assertEqual(stopped.count("\n    python "), 2)
        self.assertEqual(self.git("diff", "--cached", "--name-only"), "mine.md")

        self.lock.unlink()
        finished = self.host_git("reindex", "--from", made, "--was", self.base, "--", "mine.md")
        self.assertEqual(finished.returncode, 0, finished.stderr)
        self.assertEqual(self.git("status", "--porcelain", "--", "mine.md"), "")

    def test_the_printed_undo_moves_head_back_and_leaves_the_index_as_it_was(self) -> None:
        made = self.stopped_after_head_moved()
        undone = self.host_git("reindex", "--undo", "--from", made, "--was", self.base, "--", "mine.md")
        self.assertEqual(undone.returncode, 0, undone.stderr)
        self.assertEqual(self.git("rev-parse", "HEAD"), self.base)
        self.assertEqual(self.git("diff", "--cached", "--name-only"), "")
        self.assertEqual(self.git("diff", "--name-only"), "mine.md")

        again = self.host_git("reindex", "--undo", "--from", made, "--was", self.base, "--", "mine.md")
        self.assertNotEqual(again.returncode, 0)
        self.assertIn("it has moved since", again.stderr)
        self.assertIn("Nothing was changed", again.stderr)
        self.assertEqual(self.git("rev-parse", "HEAD"), self.base)

    def test_the_undo_refuses_once_the_finish_has_run(self) -> None:
        made = self.stopped_after_head_moved()
        finished = self.host_git("reindex", "--from", made, "--was", self.base, "--", "mine.md")
        self.assertEqual(finished.returncode, 0, finished.stderr)
        refused = self.host_git("reindex", "--undo", "--from", made, "--was", self.base, "--", "mine.md")
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("no longer holds these paths", refused.stderr)
        self.assertIn("Nothing was changed", refused.stderr)
        self.assertEqual(self.git("rev-parse", "HEAD"), made)
        self.assertEqual(self.git("status", "--porcelain", "--", "mine.md"), "")

    def stopped_rename_after_head_moved(self) -> str:
        moved = self.host_git("rename", "mine.md", "moved.md")
        self.assertEqual(moved.returncode, 0, moved.stderr)
        stopped, _ = self.here(
            lambda: self.module.cmd_commit(self.repo, [Path("mine.md"), Path("moved.md")], [], [], 0, self.message, sessions=[], no_session=True),
            self.grabbed_after_update_ref(),
        )
        self.assertIsNotNone(stopped)
        made = self.git("rev-parse", "HEAD")
        self.assertIn(f"reindex --repository {self.repo} --undo --from {made} --was {self.base} -- mine.md moved.md", stopped)
        self.lock.unlink()
        return made

    def test_the_undo_of_a_staged_rename_leaves_it_staged(self) -> None:
        self.put("mine.md", "base\n")
        made = self.stopped_rename_after_head_moved()
        undone = self.host_git("reindex", "--undo", "--from", made, "--was", self.base, "--", "mine.md", "moved.md")
        self.assertEqual(undone.returncode, 0, undone.stderr)
        self.assertEqual(self.git("rev-parse", "HEAD"), self.base)
        self.assertEqual(self.git("diff", "--cached", "-M", "--name-status"), "R100\tmine.md\tmoved.md")

    def test_the_finish_of_an_edited_staged_rename_works(self) -> None:
        body = self.a_file_long_enough_to_keep_a_rename()
        self.put("mine.md", "/* license */\n\n" + body)
        made = self.stopped_rename_after_head_moved()
        finished = self.host_git("reindex", "--from", made, "--was", self.base, "--", "mine.md", "moved.md")
        self.assertEqual(finished.returncode, 0, finished.stderr)
        self.assertEqual(self.git("status", "--porcelain", "--", "mine.md", "moved.md"), "")

    def test_the_finish_refuses_once_head_has_moved_since(self) -> None:
        made = self.stopped_after_head_moved()
        self.git("update-ref", "HEAD", self.base)
        refused = self.host_git("reindex", "--from", made, "--was", self.base, "--", "mine.md")
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("it has moved since", refused.stderr)
        self.assertIn("Nothing was changed", refused.stderr)
        self.assertEqual(self.git("rev-parse", "HEAD"), self.base)
        self.assertEqual(self.git("diff", "--cached", "--name-only"), "")

    def test_an_uncommit_held_off_past_the_wait_changes_nothing(self) -> None:
        self.git("commit", "-q", "-am", "second")
        second = self.git("rev-parse", "HEAD")
        self.held_for_an_hour()
        stopped, _ = self.uncommit_here(second)
        self.assertIsNotNone(stopped)
        self.assertIn(f"nothing was changed: HEAD is still {second}", stopped)
        self.assertIn(str(self.lock.resolve()), stopped)
        self.assertIn("rerun the same command", stopped)
        self.assertTrue(self.lock.exists())
        self.assertEqual(self.git("rev-parse", "HEAD"), second)
        self.assertEqual(self.git("diff", "--cached", "--name-only"), "")

    def test_an_uncommit_stopped_after_head_moved_finishes_with_the_printed_command(self) -> None:
        self.git("commit", "-q", "-am", "second")
        second = self.git("rev-parse", "HEAD")
        stopped, _ = self.uncommit_here(second, self.grabbed_after_update_ref())
        self.assertIsNotNone(stopped)
        self.assertEqual(self.git("rev-parse", "HEAD"), self.base)
        self.assertIn(f"HEAD moved from {second} back to its parent {self.base}", stopped)
        self.assertIn(f"reindex --repository {self.repo} --from {self.base} --was {second} -- mine.md", stopped)
        self.assertIn(f"reindex --repository {self.repo} --undo --from {self.base} --was {second} -- mine.md", stopped)
        self.assertEqual(self.git("diff", "--cached", "--name-only"), "mine.md")

        self.lock.unlink()
        finished = self.host_git("reindex", "--from", self.base, "--was", second, "--", "mine.md")
        self.assertEqual(finished.returncode, 0, finished.stderr)
        self.assertEqual(self.git("diff", "--cached", "--name-only"), "")
        self.assertEqual(self.git("diff", "--name-only"), "mine.md")

    def test_the_finish_refuses_a_path_staged_since(self) -> None:
        self.put("theirs.md", "theirs\n")
        self.git("add", "theirs.md")
        refused = self.host_git("reindex", "--from", "HEAD", "--was", "HEAD", "--", "theirs.md")
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("Nothing was changed", refused.stderr)
        self.assertEqual(self.git("diff", "--cached", "--name-only"), "theirs.md")

    def test_a_failure_that_is_not_a_lock_is_not_retried(self) -> None:
        import subprocess
        import unittest.mock

        real, calls = self.run_module.attempt, []

        def refused(args, root, env=None, data=None):
            if args[0] != "update-ref":
                return real(args, root, env, data)
            calls.append(args)
            return subprocess.CompletedProcess(
                ["git", "-C", str(root), *args], 128, b"",
                b"fatal: update_ref failed for ref 'HEAD': cannot lock ref 'HEAD': is at 1234 but expected 5678\n",
            )

        stopped, said = self.commit_here(unittest.mock.patch.object(self.run_module, "attempt", refused))
        self.assertIsNotNone(stopped)
        self.assertEqual(len(calls), 1)
        self.assertNotIn("waiting", said)
        self.assertIn("is at 1234 but expected 5678", stopped)
        self.assertIn("HEAD was not moved", stopped)
        self.assertIn("Once what git said above is dealt with, rerun", stopped)
        self.assertNotIn("once the lock is free", stopped)
        self.assertEqual(self.git("rev-parse", "HEAD"), self.base)


class CommitKnowsItsRepositoryAndKeepsItsOwnIndex(ScratchRepository):
    """The two defects the study of 2026-10-15 saw in `commit`: the folder it was run from, and one index name for everyone."""

    def test_the_repository_is_the_one_named_never_the_folder_it_is_run_from(self) -> None:
        # Run from another repository, whose tip and status the cleanup checks are unmoved.
        self.put("mine.md", "mine\n")
        done = self.commit("mine.md")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(self.git("show", "--name-only", "--format=", "HEAD"), "mine.md")

    def test_each_of_the_three_verbs_refuses_to_run_without_a_repository(self) -> None:
        import subprocess

        for verb, rest in (
            ("commit", ["-F", str(self.message), "mine.md"]),
            ("uncommit", ["--expect", self.base]),
            ("reindex", ["--from", self.base, "--was", self.base, "mine.md"]),
        ):
            with self.subTest(verb=verb):
                refused = subprocess.run(
                    [sys.executable, str(HOST / "git.py"), verb, *rest],
                    cwd=self.repo, capture_output=True, text=True,
                )
                self.assertNotEqual(refused.returncode, 0)
                self.assertIn("--repository", refused.stderr)

    def test_a_folder_that_is_no_repository_is_refused(self) -> None:
        import subprocess

        nowhere = self.repo / "no-such-folder"
        done = subprocess.run(
            [sys.executable, str(HOST / "git.py"), "commit", "--repository", str(nowhere), "-F", str(self.message), "x"],
            cwd=self.repo, capture_output=True, text=True,
        )
        self.assertNotEqual(done.returncode, 0)
        self.assertIn("not inside a git repository", done.stderr)

    def test_no_index_name_is_fixed_and_none_is_left_behind(self) -> None:
        self.assertNotIn("memar-host-commit.index", read("git.py"))
        self.put("mine.md", "mine\n")
        self.assertEqual(self.commit("mine.md").returncode, 0)
        self.assertEqual([entry.name for entry in (self.repo / ".git").glob("memar-host*")], [])

    def test_two_commits_at_once_do_not_share_an_index(self) -> None:
        import subprocess
        import threading

        # Two sessions, each its own path, at the same moment: with one index
        # file between them one would commit the other's path.
        for name in ("a.md", "b.md"):
            self.put(name, f"{name}\n")
            self.message.with_name(f"{name}.msg").write_text(f"add {name}\n", encoding="utf-8", newline="\n")
        done: dict[str, subprocess.CompletedProcess] = {}

        def commit(name: str) -> None:
            done[name] = subprocess.run(
                [sys.executable, str(HOST / "git.py"), "commit", "--repository", str(self.repo),
                 "-F", str(self.message.with_name(f"{name}.msg")), "--no-session", name],
                cwd=self.elsewhere, capture_output=True, text=True,
            )

        threads = [threading.Thread(target=commit, args=(name,)) for name in ("a.md", "b.md")]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        landed = [name for name, result in done.items() if result.returncode == 0]
        self.assertTrue(landed, {name: result.stderr for name, result in done.items()})
        for commit_id in self.git("rev-list", f"{self.base}..HEAD").split():
            self.assertEqual(len(self.git("show", "--name-only", "--format=", commit_id).split()), 1)


class CommitCitesItsSessions(ScratchRepository):
    """`commit` names the sessions it carries out in `Session:` trailers it writes itself, each one a session `memar session show` finds."""

    KNOWN = "20000101-T000000Z-1"
    OTHER = "20000101-T000000Z-2"
    # No session folder and no record anywhere: the form of an id, and nothing behind it.
    UNKNOWN = "20000101-T000000Z-9"

    def setUp(self) -> None:
        super().setUp()
        for session_id in (self.KNOWN, self.OTHER):
            self.keep_on_records_branch(session_id)
        self.put("mine.md", "mine\n")

    def keep_on_records_branch(self, session_id: str) -> None:
        """Put SESSION_ID's plan on the scratch repository's records branch, where `archive` would have kept it."""
        import os
        import subprocess

        from machine.fs_memar import RECORDS_BRANCH
        from modules.process.session.services.branch import folder_on_branch

        env = dict(os.environ, GIT_INDEX_FILE=str(self.repo / ".git" / "records.index"))

        def plumb(*args: str, data: str | None = None) -> str:
            return subprocess.run(
                ["git", "-C", str(self.repo), *args], input=data, capture_output=True, text=True, check=True, env=env
            ).stdout.strip()

        tip = plumb("rev-parse", "--verify", "--quiet", RECORDS_BRANCH) if self.has_branch(RECORDS_BRANCH) else ""
        if tip:
            plumb("read-tree", tip)
        blob = plumb("hash-object", "-w", "--stdin", data=f"# {session_id}\n")
        plumb("update-index", "--add", "--cacheinfo", f"100644,{blob},{folder_on_branch(session_id)}/plan.md")
        tree = plumb("write-tree")
        made = plumb("commit-tree", tree, *(["-p", tip] if tip else []), "-m", f"records of {session_id}")
        plumb("update-ref", f"refs/heads/{RECORDS_BRANCH}", made)

    def has_branch(self, name: str) -> bool:
        import subprocess

        return subprocess.run(
            ["git", "-C", str(self.repo), "rev-parse", "--verify", "--quiet", f"refs/heads/{name}"], capture_output=True
        ).returncode == 0

    def cite(self, *args: str):
        return self.host_git("commit", "-F", str(self.message), *args)

    def sessions_of(self, commit: str = "HEAD") -> list[str]:
        return self.git("log", "-1", "--format=%(trailers:key=Session,valueonly)", commit).split()

    def test_a_commit_that_cites_no_session_is_refused_naming_the_form_it_wants(self) -> None:
        done = self.cite("mine.md")
        self.assertNotEqual(done.returncode, 0)
        for wanted in ("--session-id", "Session: ", "--no-session"):
            self.assertIn(wanted, done.stderr)
        self.assertEqual(self.git("rev-parse", "HEAD"), self.base)
        self.assertIn("M mine.md", self.git("status", "--porcelain"))

    def test_an_id_with_no_session_folder_and_no_record_is_refused(self) -> None:
        done = self.cite("--session-id", self.KNOWN, "--session-id", self.UNKNOWN, "mine.md")
        self.assertNotEqual(done.returncode, 0)
        self.assertIn(self.UNKNOWN, done.stderr)
        self.assertNotIn(f"no session {self.KNOWN}", done.stderr)
        self.assertEqual(self.git("rev-parse", "HEAD"), self.base)

    def test_a_commit_that_carries_out_no_session_is_accepted_with_the_opt_out(self) -> None:
        done = self.cite("--no-session", "mine.md")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(self.git("show", "--name-only", "--format=", "HEAD"), "mine.md")
        self.assertEqual(self.sessions_of(), [])

    def test_the_opt_out_and_a_session_together_are_refused(self) -> None:
        done = self.cite("--no-session", "--session-id", self.KNOWN, "mine.md")
        self.assertNotEqual(done.returncode, 0)
        self.assertIn("--no-session", done.stderr)
        self.assertEqual(self.git("rev-parse", "HEAD"), self.base)

    def test_each_session_is_a_trailer_git_log_reads_back_beside_the_others(self) -> None:
        self.message.write_text(
            "subject\n\nbody\n\nCo-Authored-By: Someone <someone@example.org>\n", encoding="utf-8", newline="\n"
        )
        done = self.cite("--session-id", self.KNOWN, "--session-id", self.OTHER, "--session-id", self.KNOWN, "mine.md")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(self.sessions_of(), [self.KNOWN, self.OTHER])
        self.assertEqual(
            self.git("log", "-1", "--format=%(trailers:key=Co-Authored-By,valueonly)"), "Someone <someone@example.org>"
        )
        self.assertEqual(self.git("log", "-1", "--format=%s"), "subject")

    def test_a_session_written_into_the_message_by_hand_is_refused(self) -> None:
        self.message.write_text(f"subject\n\nSession: {self.KNOWN}\n", encoding="utf-8", newline="\n")
        done = self.cite("--no-session", "mine.md")
        self.assertNotEqual(done.returncode, 0)
        self.assertIn("--session-id", done.stderr)
        self.assertEqual(self.git("rev-parse", "HEAD"), self.base)

    def test_a_fold_keeps_the_sessions_of_the_commits_it_replaces(self) -> None:
        self.assertEqual(self.cite("--session-id", self.KNOWN, "mine.md").returncode, 0)
        self.put("shared.md", "a finding\n")
        done = self.cite("--fold", "1", "--session-id", self.OTHER, "mine.md", "shared.md")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(self.git("rev-parse", "HEAD^"), self.base)
        self.assertEqual(self.sessions_of(), [self.KNOWN, self.OTHER])
        # A finding folded in carries out the sessions already cited, and needs no new one.
        self.put("shared.md", "a second finding\n")
        done = self.cite("--fold", "1", "shared.md")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(self.sessions_of(), [self.KNOWN, self.OTHER])


class RecordWritesAnotherBranch(ScratchRepository):
    """`record`: a commit on another branch, made without HEAD, the index or the working tree."""

    BRANCH = "dev-knowledge"

    def setUp(self) -> None:
        super().setUp()
        self.sources = self.repo / ".git" / "sources"
        self.sources.mkdir()
        self.manifest = self.repo / ".git" / "manifest.txt"

    def source(self, name: str, data: bytes) -> Path:
        path = self.sources / name
        path.write_bytes(data)
        return path

    def record(self, entries: dict[str, Path], *replace: str, message: str = "record\n"):
        import subprocess

        self.manifest.write_text(
            "".join(f"{target}\t{source}\n" for target, source in entries.items()), encoding="utf-8", newline="\n"
        )
        self.message.write_text(message, encoding="utf-8", newline="\n")
        arguments = [
            "record", "--repository", str(self.repo), "--branch", self.BRANCH,
            "--manifest", str(self.manifest), "-F", str(self.message),
        ]
        for each in replace:
            arguments += ["--replace", each]
        return subprocess.run(
            [sys.executable, str(HOST / "git.py"), *arguments],
            cwd=self.elsewhere, capture_output=True, text=True,
        )

    def tree(self) -> dict[str, str]:
        listed = self.git("ls-tree", "-r", "--name-only", self.BRANCH).splitlines()
        return {name: self.git("show", f"{self.BRANCH}:{name}") for name in listed}

    def test_the_first_record_makes_the_branch_with_no_parent_and_moves_nothing_else(self) -> None:
        self.put("mine.md", "edited\n")
        self.put("theirs.md", "staged\n")
        self.git("add", "theirs.md")
        head, staged, status = self.git("rev-parse", "HEAD"), self.git("diff", "--cached"), self.git("status", "--porcelain")
        done = self.record({".agents/sessions/s1/plan.md": self.source("p", b"plan\n")})
        self.assertEqual(done.returncode, 0, done.stderr)
        made = done.stdout.strip()
        self.assertEqual(self.git("rev-parse", self.BRANCH), made)
        self.assertEqual(self.git("rev-list", "--parents", "-n", "1", self.BRANCH), made)
        self.assertEqual(self.tree(), {".agents/sessions/s1/plan.md": "plan"})
        self.assertEqual(self.git("rev-parse", "HEAD"), head)
        self.assertEqual(self.git("symbolic-ref", "HEAD"), "refs/heads/main")
        self.assertEqual(self.git("diff", "--cached"), staged)
        self.assertEqual(self.git("status", "--porcelain"), status)
        self.assertEqual(self.git("log", "-1", "--format=%s", self.BRANCH), "record")

    def test_the_bytes_are_kept_as_they_are_whatever_git_would_do_to_them(self) -> None:
        import subprocess

        self.git("config", "core.autocrlf", "true")
        self.git("config", "core.safecrlf", "false")
        (self.repo / ".gitattributes").write_text("*.md text eol=lf\n", encoding="utf-8", newline="\n")
        data = b"line one\r\nline two\r\n"
        done = self.record({"a/crlf.md": self.source("c", data)})
        self.assertEqual(done.returncode, 0, done.stderr)
        blob = subprocess.run(
            ["git", "-C", str(self.repo), "cat-file", "blob", f"{self.BRANCH}:a/crlf.md"], capture_output=True
        ).stdout
        self.assertEqual(blob, data)

    def test_a_second_record_has_the_first_for_its_parent_and_replaces_only_what_it_names(self) -> None:
        first = self.record({
            "s/one/a.md": self.source("a", b"a\n"),
            "s/one/b.md": self.source("b", b"b\n"),
            "s/two/c.md": self.source("c", b"c\n"),
        })
        self.assertEqual(first.returncode, 0, first.stderr)
        first_tip = self.git("rev-parse", self.BRANCH)
        done = self.record({"s/one/a.md": self.source("a2", b"a again\n")}, "s/one")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(self.tree(), {"s/one/a.md": "a again", "s/two/c.md": "c"})
        self.assertEqual(self.git("rev-parse", f"{self.BRANCH}~1"), first_tip)

    def test_a_record_that_changes_nothing_makes_no_commit_and_says_so(self) -> None:
        entries = {"s/one/a.md": self.source("a", b"a\n")}
        first = self.record(entries).stdout.strip()
        again = self.record(entries, "s/one")
        self.assertEqual(again.returncode, 0, again.stderr)
        self.assertEqual(again.stdout.strip(), first)
        self.assertEqual(self.git("rev-parse", self.BRANCH), first)
        self.assertIn("nothing", again.stderr)

    def test_the_checked_out_branch_is_refused(self) -> None:
        import subprocess

        self.manifest.write_text(f"x.md\t{self.source('x', b'x')}\n", encoding="utf-8", newline="\n")
        done = subprocess.run(
            [sys.executable, str(HOST / "git.py"), "record", "--repository", str(self.repo), "--branch", "main",
             "--manifest", str(self.manifest), "-F", str(self.message)],
            cwd=self.elsewhere, capture_output=True, text=True,
        )
        self.assertNotEqual(done.returncode, 0)
        self.assertIn("checked out", done.stderr)
        self.assertEqual(self.git("rev-parse", "HEAD"), self.base)

    def test_a_path_that_leaves_the_branch_or_names_git_is_refused(self) -> None:
        source = self.source("x", b"x")
        for target in ("../x.md", "/x.md", "a//b.md", "a/.git/config", "a/./b.md"):
            with self.subTest(target=target):
                done = self.record({target: source})
                self.assertNotEqual(done.returncode, 0)
                self.assertFalse(self.git("branch", "--list", self.BRANCH))

    def test_a_source_that_is_no_file_is_refused_and_nothing_is_written(self) -> None:
        done = self.record({"a.md": self.sources / "missing"})
        self.assertNotEqual(done.returncode, 0)
        self.assertIn("not a file", done.stderr)
        self.assertFalse(self.git("branch", "--list", self.BRANCH))

    def test_the_repository_is_required(self) -> None:
        import subprocess

        done = subprocess.run(
            [sys.executable, str(HOST / "git.py"), "record", "--branch", self.BRANCH, "--manifest", str(self.manifest),
             "-F", str(self.message)],
            cwd=self.repo, capture_output=True, text=True,
        )
        self.assertNotEqual(done.returncode, 0)
        self.assertIn("--repository", done.stderr)

    def test_records_at_once_all_land_one_after_the_other(self) -> None:
        import subprocess
        import threading

        results = {}

        def put(name: str) -> None:
            manifest = self.sources / f"{name}.manifest"
            message = self.sources / f"{name}.message"
            manifest.write_text(f"s/{name}/f.md\t{self.source(name, name.encode())}\n", encoding="utf-8", newline="\n")
            message.write_text(f"record {name}\n", encoding="utf-8", newline="\n")
            results[name] = subprocess.run(
                [sys.executable, str(HOST / "git.py"), "record", "--repository", str(self.repo), "--branch", self.BRANCH,
                 "--manifest", str(manifest), "-F", str(message), "--replace", f"s/{name}"],
                cwd=self.elsewhere, capture_output=True, text=True,
            )

        threads = [threading.Thread(target=put, args=(name,)) for name in ("one", "two", "three")]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        for result in results.values():
            self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(sorted(self.tree()), ["s/one/f.md", "s/three/f.md", "s/two/f.md"])
        self.assertEqual(len(self.git("rev-list", self.BRANCH).split()), 3)

    def test_it_never_pushes_and_never_moves_the_checkout(self) -> None:
        record = read("git.py").partition("def cmd_record")[2].partition("\ndef ")[0]
        self.assertTrue(record)
        for forbidden in ('"push"', "checkout", '"reset"', "update-ref\", \"HEAD"):
            self.assertNotIn(forbidden, record)


def _load(name: str, file: str):
    """Load one file of the shelf, whose folder a hyphen in its path forbids importing."""
    spec = importlib.util.spec_from_loader(
        name, SourceFileLoader(name, str(HOST / file))
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


if __name__ == "__main__":
    unittest.main(verbosity=2)
