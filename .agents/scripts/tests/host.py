#!/usr/bin/env python3
"""Tests for the constraints `host/fs.py` and `host/git.py` hold a session to.

    python .agents/scripts/tests/host.py

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
                         rewrites what is already upstream.
"""

from __future__ import annotations

import ast
import importlib.util
import sys
import unittest
from importlib.machinery import SourceFileLoader
from pathlib import Path

TESTS = Path(__file__).resolve().parent
HOST = TESTS.parent / "host"
SCRIPTS = HOST.parent
sys.path.insert(0, str(SCRIPTS))
sys.dont_write_bytecode = True


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
        # history this command exists to preserve.
        self.assertIn("Commit this rename by itself", read("git.py"))


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
        # is the routing being explained. What it must not do is route there: no
        # constant may name a file of this shelf.
        launcher = (SCRIPTS / "memar").read_text(encoding="utf-8")
        for name in ("fs.py", "git.py", '"host"', "'host'"):
            with self.subTest(name=name):
                self.assertNotIn(name, launcher)
        for name in ("fs.py", "git.py"):
            with self.subTest(name=name):
                self.assertNotIn(name, launcher.split("USAGE")[1])

    def test_the_shelf_states_why_it_is_not_under_memar(self) -> None:
        readme = (HOST / "README.md").read_text(encoding="utf-8")
        self.assertIn("not under `memar`", readme)
        self.assertIn("host tool", readme.lower())


class CommitTakesOnlyWhatItNames(unittest.TestCase):
    def setUp(self) -> None:
        import tempfile

        scratch = tempfile.TemporaryDirectory(
            dir=TESTS, prefix="tmp-host-commit-", ignore_cleanup_errors=True
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

    def commit(self, *args: str):
        import subprocess

        return subprocess.run(
            [sys.executable, str(HOST / "git.py"), "commit", "-F", str(self.message), *args],
            cwd=self.repo, capture_output=True, text=True,
        )

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
