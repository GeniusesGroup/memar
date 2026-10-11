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
"""

from __future__ import annotations

import ast
import importlib.util
import sys
import unittest
from importlib.machinery import SourceFileLoader
from pathlib import Path

TESTS = Path(__file__).resolve().parent
HOST = TESTS.parent
SCRIPTS = HOST.parent
sys.path.insert(0, str(SCRIPTS))
sys.dont_write_bytecode = True

from machine.fs_test_scratch import suite_scratch


def read(name: str) -> str:
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

        module = _load("host_git", "git.py")
        with self.assertRaises(SystemExit) as raised:
            module.cmd_restore([TESTS], None)
        message = str(raised.exception)
        self.assertIn("refusing to discard", message)
        self.assertIn("stash", message)
        self.assertIn(self.TOKEN, message)

    def test_discarding_needs_a_path_too(self) -> None:
        module = _load("host_git", "git.py")
        with self.assertRaises(SystemExit) as raised:
            module.cmd_restore([], self.TOKEN)
        self.assertIn("requires one or more paths", str(raised.exception))


class RenameIsHistoryKeeping(unittest.TestCase):
    def test_a_move_goes_through_git_mv_not_a_plain_move(self) -> None:
        source = read("git.py")
        self.assertIn('run_git(["mv",', source)
        for plain in ("shutil.move(", "os.rename(", "os.replace("):
            self.assertNotIn(plain, source)

    def test_a_rename_is_staged_on_its_own_before_the_content_changes(self) -> None:
        # A mixed rename+edit commit defeats rename detection, which is the
        # history this command exists to preserve; only an edit that keeps it
        # may ride along.
        self.assertIn("Commit this rename by itself", read("git.py"))
        self.assertIn("keeps it detected as a rename", read("git.py"))


class StashIsNotDiscard(unittest.TestCase):
    def test_stashing_carries_untracked_work_and_says_ignored_is_left_alone(self) -> None:
        source = read("git.py")
        self.assertIn("--include-untracked", source)
        self.assertIn("Ignored paths were not included", source)

    def test_a_clean_tree_is_not_stashed_at_all(self) -> None:
        # Parking work is for work there is; a stash of nothing is a stash entry
        # a later session will have to read to learn that nothing happened.
        module = _load("host_git", "git.py")
        module._working_tree_dirty = lambda: False
        import io
        import contextlib

        with contextlib.redirect_stderr(io.StringIO()) as said:
            module.cmd_stash(None)
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
                self.assertFalse((SCRIPTS / router.SHELF / name).exists())

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

    def git(self, *args: str) -> str:
        import subprocess

        return subprocess.run(
            ["git", "-C", str(self.repo), *args],
            capture_output=True, text=True, check=True,
        ).stdout.strip()

    def put(self, name: str, text: str) -> None:
        (self.repo / name).write_text(text, encoding="utf-8", newline="\n")

    def host_git(self, *args: str):
        import subprocess

        return subprocess.run(
            [sys.executable, str(HOST / "git.py"), *args],
            cwd=self.repo, capture_output=True, text=True,
        )

    def commit(self, *args: str):
        return self.host_git("commit", "-F", str(self.message), *args)

    def a_file_long_enough_to_keep_a_rename(self) -> str:
        """Commit mine.md long enough that a license header added to it leaves git pairing a move of it."""
        body = "".join(f"line {number}\n" for number in range(20))
        self.put("mine.md", body)
        self.git("commit", "-q", "-am", "body")
        self.base = self.git("rev-parse", "HEAD")
        return body


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
        self.module = _load("host_git_locks", "git.py")
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
            stack.enter_context(unittest.mock.patch.object(self.module, "LOCK_WAIT_SECONDS", 0.5))
            stack.enter_context(unittest.mock.patch.object(self.module, "LOCK_FIRST_PAUSE_SECONDS", 0.05))
            for patch in patches:
                stack.enter_context(patch)
            try:
                verb()
            except SystemExit as stopped:
                return str(stopped.code), said.getvalue()
        return None, said.getvalue()

    def commit_here(self, *patches) -> tuple[str | None, str]:
        return self.here(lambda: self.module.cmd_commit([Path("mine.md")], [], [], 0, self.message), *patches)

    def uncommit_here(self, expect: str, *patches) -> tuple[str | None, str]:
        return self.here(lambda: self.module.cmd_uncommit(expect), *patches)

    def grabbed_after_update_ref(self):
        """Another git process taking the index lock the moment HEAD has moved."""
        import unittest.mock

        real = self.module._attempt

        def grabbed(args, root, env=None, data=None):
            done = real(args, root, env, data)
            if args[0] == "update-ref":
                self.lock.write_text("", encoding="utf-8")
            return done

        return unittest.mock.patch.object(self.module, "_attempt", grabbed)

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
            self.module.time, "sleep", side_effect=lambda seconds: self.lock.unlink(missing_ok=True)
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
        self.assertIn(f"reindex --from {made} --was {self.base} -- mine.md", stopped)
        self.assertIn(f"reindex --undo --from {made} --was {self.base} -- mine.md", stopped)
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
            lambda: self.module.cmd_commit([Path("mine.md"), Path("moved.md")], [], [], 0, self.message),
            self.grabbed_after_update_ref(),
        )
        self.assertIsNotNone(stopped)
        made = self.git("rev-parse", "HEAD")
        self.assertIn(f"reindex --undo --from {made} --was {self.base} -- mine.md moved.md", stopped)
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
        self.assertIn(f"reindex --from {self.base} --was {second} -- mine.md", stopped)
        self.assertIn(f"reindex --undo --from {self.base} --was {second} -- mine.md", stopped)
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

        real, calls = self.module._attempt, []

        def refused(args, root, env=None, data=None):
            if args[0] != "update-ref":
                return real(args, root, env, data)
            calls.append(args)
            return subprocess.CompletedProcess(
                ["git", "-C", str(root), *args], 128, b"",
                b"fatal: update_ref failed for ref 'HEAD': cannot lock ref 'HEAD': is at 1234 but expected 5678\n",
            )

        stopped, said = self.commit_here(unittest.mock.patch.object(self.module, "_attempt", refused))
        self.assertIsNotNone(stopped)
        self.assertEqual(len(calls), 1)
        self.assertNotIn("waiting", said)
        self.assertIn("is at 1234 but expected 5678", stopped)
        self.assertIn("HEAD was not moved", stopped)
        self.assertIn("Once what git said above is dealt with, rerun", stopped)
        self.assertNotIn("once the lock is free", stopped)
        self.assertEqual(self.git("rev-parse", "HEAD"), self.base)


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
