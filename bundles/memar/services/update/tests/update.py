#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for `memar update` in `bundles/memar/services/update/update.py`.

    python bundles/memar/services/update/tests/update.py

The subject is the update verb, named for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes to a real agent app, editor, or checkout. Each layer the
verb asks is patched where its owner defines it, because the services import
what a run needs only when it runs, and a test is about the verb's own
decisions; the verb is run through its own `describe`, as the router runs it.
The checkout comparison runs against throwaway git repositories made under the
folder `modules-plugable/computer/memory/filesystem/services/fs_test_scratch.py` names and removed whole by its
`remove_tree`, and the one real skill-copy check is given a home that holds no
agent app.

What is pinned, and what each pin is for:

  CheckWritesNothing  With no option the tool names each stale thing on one
                      line, refreshes nothing, and exits 0: a stale copy is an
                      answer, not a failure.
  CurrentIsShort      When nothing is stale it says so in one line, and with
                      --quiet it says nothing, so it can run unattended.
  ApplyRefreshesStale --apply asks each layer to refresh only when that layer
                      named something stale, and only what it named, and never
                      touches the checkout; an extension refresh that fails
                      fails the run and says what to run.
  FailureIsNonZero    A layer that cannot answer makes the run fail; nothing
                      else does.
  CheckoutComparedOnly
                      Behind and ahead are counted against the fetched
                      upstream, the command a person would run is printed, and
                      the checkout's HEAD and working tree stay as they were; a
                      checkout tracking nothing is said to be uncompared.
  ConsumerIsFastForwarded
                      A clean checkout that tracks an upstream and is only
                      behind it is fast-forwarded to it; a current one is left.
  DevelopmentIsNeverMoved
                      A checkout behind its upstream is left exactly as it was,
                      HEAD and working tree, when it is marked as a development
                      checkout, has uncommitted or untracked changes, has
                      unpushed commits, has a detached HEAD, or tracks nothing,
                      each on its own, and the reason is named.
  BackgroundRun       The daily run leaves one line only when something moved,
                      was refused, or was refreshed, and a run that finds
                      another holding the lock does nothing; an extension
                      refresh that fails is said in that line with what to
                      run, and stops nothing else.
  RealSkillSeam       The skill copies' owner, asked with a home that holds no
                      agent app, answers with nothing.
  HelpSaysWhatIsChecked
                      `memar update --help`, asked through the launcher, names
                      what is checked, the options, that a command a person
                      runs never changes the checkout, and the daily
                      background run with its opt-out; `memar --help` carries
                      that daily run and its opt-out in the verb's summary,
                      because the top-level help has no text of its own for it.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
from importlib import import_module
_m_fs_test_scratch = import_module('modules-plugable.computer.memory.filesystem.services.fs_test_scratch')
remove_tree = _m_fs_test_scratch.remove_tree
suite_scratch = _m_fs_test_scratch.suite_scratch
import argparse
import contextlib
import io
import os
import subprocess
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = next(p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()) / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS / 'services'))
sys.path.insert(1, str(SCRIPTS))
sys.path.insert(2, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
import machine.editor_extension as editor_extension
import machine.env_location as env_location
import bundles.memar.services.update.update as update
import bundles.memar.services.update.services.check as checking
import bundles.memar.services.update.services.checkout as update_checkout
import bundles.memar.services.update.services.copies as copies
import bundles.memar.services.update.services.daily as update_daily
from bundles.memar.services.update.services.checkout import Upstream
LAUNCHER = SCRIPTS / 'memar'
SKILL_LINE = "stale: the Memar skill at /home/.cursor/skills/memar differs from the checkout's; refresh with: memar update --apply"

class Fixture(unittest.TestCase):
    """The layers patched to answer as each test says."""
    skill_lines: list[str] = []
    mcp_lines: list[str] = []
    extensions: list[Path] = []
    standing = Upstream('origin/main', 0, 0, None)
    apps_status = 0
    mcp_ok = True

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.checkout = Path(self.scratch.name)
        self.asked: list[str] = []

        def ask_apps(command: str, *, capture: bool) -> tuple[int, str, str]:
            self.asked.append(command)
            said = '\n'.join(self.skill_lines) + '\n' if command == copies.APPS_STALE else ''
            return (self.apps_status, said, 'broken' if self.apps_status else '')

        def stale_mcp() -> list[str]:
            if not self.mcp_ok:
                raise RuntimeError('mcp broken')
            return list(self.mcp_lines)

        def refresh_mcp() -> bool:
            self.asked.append('mcp_refresh')
            return self.mcp_ok
        for module, name, value in ((env_location, 'resolve_root', lambda: self.checkout), (copies, 'ask_apps', ask_apps), (copies, 'stale_mcp_lines', stale_mcp), (copies, 'refresh_mcp', refresh_mcp), (editor_extension, 'stale_extensions', lambda checkout: list(self.extensions)), (update_checkout, 'upstream_of', lambda checkout, fetch: self.standing)):
            patched = unittest.mock.patch.object(module, name, value)
            patched.start()
            self.addCleanup(patched.stop)
        installing = unittest.mock.patch.object(editor_extension, 'install_extensions')
        self.installed = installing.start()
        self.addCleanup(installing.stop)

    def run_update(self, *arguments: str) -> tuple[int, str, str]:
        parser = argparse.ArgumentParser(prog='memar')
        run = update.describe(parser.add_subparsers())
        out, err = (io.StringIO(), io.StringIO())
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = run(parser.parse_args([update.UPDATE_VERB, *arguments]))
        return (code, out.getvalue(), err.getvalue())

class CheckWritesNothing(Fixture):
    skill_lines = [SKILL_LINE]
    standing = Upstream('origin/main', 0, 3, None)

    def setUp(self) -> None:
        super().setUp()
        self.extensions = [self.checkout / 'editor' / 'memar.khayyam-1.0.0']

    def test_each_stale_thing_is_one_line_and_nothing_is_refreshed(self) -> None:
        code, out, _ = self.run_update()
        self.assertEqual(code, 0)
        lines = out.splitlines()
        self.assertEqual(len(lines), 3)
        self.assertEqual(lines[0], SKILL_LINE)
        self.assertIn('memar.khayyam-1.0.0 is not installed', lines[1])
        self.assertIn('memar update --apply', lines[1])
        self.assertIn('3 commit(s) behind origin/main', lines[2])
        self.assertEqual(self.asked, [copies.APPS_STALE])
        self.installed.assert_not_called()

class CurrentIsShort(Fixture):

    def test_nothing_stale_is_one_line(self) -> None:
        code, out, _ = self.run_update()
        self.assertEqual(code, 0)
        self.assertEqual(len(out.splitlines()), 1)
        self.assertIn('Memar is current', out)
        self.assertIn('not behind origin/main', out)

    def test_quiet_says_nothing_when_nothing_is_stale(self) -> None:
        self.assertEqual(self.run_update('--quiet'), (0, '', ''))

    def test_quiet_still_names_what_is_stale(self) -> None:
        self.skill_lines = [SKILL_LINE]
        code, out, _ = self.run_update('--quiet')
        self.assertEqual((code, out), (0, SKILL_LINE + '\n'))

class ApplyRefreshesStale(Fixture):

    def test_each_layer_is_refreshed_only_when_it_named_something(self) -> None:
        self.skill_lines = [SKILL_LINE]
        code, _, _ = self.run_update('--apply')
        self.assertEqual(code, 0)
        self.assertEqual(self.asked, [copies.APPS_STALE, copies.APPS_REFRESH])
        self.installed.assert_not_called()
        self.skill_lines, self.asked = ([], [])
        self.mcp_lines = ['stale: the MCP server in /home/.cursor/mcp.json; refresh with: memar update --apply']
        code, _, _ = self.run_update('--apply')
        self.assertEqual(code, 0)
        self.assertEqual(self.asked, [copies.APPS_STALE, 'mcp_refresh'])
        self.installed.assert_not_called()
        self.mcp_lines, self.asked = ([], [])
        self.extensions = [self.checkout / 'editor' / 'memar.khayyam-1.0.0']
        code, _, _ = self.run_update('--apply')
        self.assertEqual(code, 0)
        self.assertEqual(self.asked, [copies.APPS_STALE])
        self.installed.assert_called_once_with(self.checkout, only=self.extensions)

    def test_a_checkout_behind_is_left_as_it_is(self) -> None:
        self.standing = Upstream('origin/main', 0, 2, None)
        code, out, _ = self.run_update('--apply')
        self.assertEqual(code, 0)
        self.assertIn('left as it is', out)
        self.assertEqual(self.asked, [copies.APPS_STALE])
        self.installed.assert_not_called()

    def test_an_extension_refresh_that_fails_fails_the_run_and_says_what_to_run(self) -> None:
        self.extensions = [self.checkout / 'editor' / 'memar.khayyam-1.0.0']
        self.installed.side_effect = OSError('disk full')
        code, _, err = self.run_update('--apply')
        self.assertEqual(code, 1)
        self.assertIn('could not be refreshed (disk full)', err)
        self.assertIn('memar update --apply', err)

class FailureIsNonZero(Fixture):

    def test_a_skill_check_that_fails_fails_the_run(self) -> None:
        self.apps_status = 2
        code, _, err = self.run_update()
        self.assertEqual(code, 1)
        self.assertIn('could not be checked', err)

    def test_a_fetch_that_failed_is_an_answer_not_a_failure(self) -> None:
        self.standing = Upstream('origin/main', 0, 0, 'the fetch failed: no network')
        code, out, _ = self.run_update()
        self.assertEqual(code, 0)
        self.assertIn('counted against the last fetch', out)

class Upstreamed(unittest.TestCase):
    """A real upstream, a checkout cloned from it, and a second clone that moves it on."""

    def setUp(self) -> None:
        root = Path(tempfile.mkdtemp(dir=suite_scratch()))
        self.addCleanup(remove_tree, root)
        self.upstream = root / 'upstream.git'
        self.git(root, 'init', '-q', '--bare', '-b', 'main', str(self.upstream))
        self.checkout = root / 'checkout'
        self.git(root, 'clone', '-q', str(self.upstream), str(self.checkout))
        self.commit(self.checkout, 'base.md')
        self.git(self.checkout, 'push', '-q', 'origin', 'main')
        self.other = root / 'other'
        self.git(root, 'clone', '-q', str(self.upstream), str(self.other))
        for repository in (self.upstream, self.checkout, self.other):
            self.git(repository, 'config', 'gc.auto', '0')
            self.git(repository, 'config', 'maintenance.auto', 'false')

    def git(self, where: Path, *arguments: str) -> str:
        return subprocess.run(['git', '-C', str(where), '-c', 'user.name=Test', '-c', 'user.email=test@example.org', '-c', 'gc.auto=0', '-c', 'maintenance.auto=false', *arguments], capture_output=True, text=True, check=True).stdout.strip()

    def commit(self, where: Path, name: str) -> None:
        (where / name).write_text(f'{name}\n', encoding='utf-8', newline='\n')
        self.git(where, 'add', name)
        self.git(where, 'commit', '-q', '-m', name)

    def move_upstream_on(self) -> None:
        self.commit(self.other, 'theirs.md')
        self.git(self.other, 'push', '-q', 'origin', 'main')

    def state(self) -> tuple[str, str]:
        return (self.git(self.checkout, 'rev-parse', 'HEAD'), self.git(self.checkout, 'status', '--porcelain'))

class CheckoutComparedOnly(Upstreamed):

    def test_behind_is_counted_after_a_fetch_and_nothing_is_pulled(self) -> None:
        self.commit(self.other, 'theirs.md')
        self.git(self.other, 'push', '-q', 'origin', 'main')
        head = self.git(self.checkout, 'rev-parse', 'HEAD')
        self.assertEqual(update_checkout.upstream_of(self.checkout, fetch=False).behind, 0)
        standing = update_checkout.upstream_of(self.checkout, fetch=True)
        self.assertEqual(standing, Upstream('origin/main', 0, 1, None))
        line, _ = checking.checkout_line(self.checkout, fetch=False)
        self.assertIn(f'git -C "{self.checkout}" pull --ff-only', line)
        self.assertEqual(self.git(self.checkout, 'rev-parse', 'HEAD'), head)
        self.assertFalse((self.checkout / 'theirs.md').exists())

    def test_diverged_is_reported_with_both_counts_and_no_pull(self) -> None:
        self.commit(self.other, 'theirs.md')
        self.git(self.other, 'push', '-q', 'origin', 'main')
        self.commit(self.checkout, 'mine.md')
        line, _ = checking.checkout_line(self.checkout, fetch=True)
        self.assertIn('1 commit(s) behind origin/main, and 1 ahead', line)
        self.assertIn('reconcile', line)
        self.assertNotIn('pull', line)

    def test_ahead_only_is_not_stale(self) -> None:
        self.commit(self.checkout, 'mine.md')
        line, standing = checking.checkout_line(self.checkout, fetch=True)
        self.assertIsNone(line)
        self.assertIn('1 ahead', standing)

    def test_a_checkout_that_tracks_nothing_is_said_to_be_uncompared(self) -> None:
        self.git(self.checkout, 'checkout', '-q', '--detach')
        line, standing = checking.checkout_line(self.checkout, fetch=True)
        self.assertIsNone(line)
        self.assertIn('tracks no upstream', standing)

class ConsumerIsFastForwarded(Upstreamed):

    def test_a_clean_checkout_only_behind_is_brought_up_to_its_upstream(self) -> None:
        self.move_upstream_on()
        forwarded = update_checkout.fast_forward(self.checkout, fetch=True)
        self.assertEqual((forwarded.moved, forwarded.refused), (1, []))
        self.assertEqual(self.git(self.checkout, 'rev-parse', 'HEAD'), self.git(self.other, 'rev-parse', 'HEAD'))
        self.assertTrue((self.checkout / 'theirs.md').is_file())
        self.assertEqual(self.git(self.checkout, 'status', '--porcelain'), '')

    def test_a_checkout_that_is_current_is_left_and_nothing_is_said(self) -> None:
        before = self.state()
        forwarded = update_checkout.fast_forward(self.checkout, fetch=True)
        self.assertEqual((forwarded.moved, forwarded.refused), (0, []))
        self.assertEqual(self.state(), before)

class DevelopmentIsNeverMoved(Upstreamed):
    """Each condition alone makes a checkout behind its upstream a development one."""

    def assert_refused(self, reason: str) -> None:
        before = self.state()
        forwarded = update_checkout.fast_forward(self.checkout, fetch=True)
        self.assertEqual(forwarded.moved, 0)
        self.assertTrue(any((reason in said for said in forwarded.refused)), forwarded.refused)
        self.assertEqual(self.state(), before)
        self.assertFalse((self.checkout / 'theirs.md').exists())

    def test_a_marked_checkout(self) -> None:
        self.move_upstream_on()
        self.assertFalse(update_checkout.is_marked_development(self.checkout))
        update_checkout.mark_development(self.checkout)
        self.assertTrue(update_checkout.is_marked_development(self.checkout))
        self.assert_refused('marked as a development checkout')

    def test_uncommitted_changes(self) -> None:
        self.move_upstream_on()
        (self.checkout / 'base.md').write_text('edited\n', encoding='utf-8', newline='\n')
        self.assert_refused('uncommitted changes')

    def test_an_untracked_file(self) -> None:
        self.move_upstream_on()
        (self.checkout / 'draft.md').write_text('draft\n', encoding='utf-8', newline='\n')
        self.assert_refused('uncommitted changes')

    def test_unpushed_commits(self) -> None:
        self.move_upstream_on()
        self.commit(self.checkout, 'mine.md')
        self.assert_refused('1 unpushed commit(s)')

    def test_a_detached_head(self) -> None:
        self.move_upstream_on()
        self.git(self.checkout, 'checkout', '-q', '--detach')
        self.assert_refused('HEAD is detached')

    def test_no_upstream(self) -> None:
        self.move_upstream_on()
        self.git(self.checkout, 'branch', '--unset-upstream')
        self.assert_refused('tracks no upstream')

class BackgroundRun(Fixture):
    """The daily run: what it moves, what it refreshes, the line it leaves, and one at a time."""

    def setUp(self) -> None:
        super().setUp()
        self.forwarded = update_checkout.Forwarded(Upstream('origin/main', 0, 0, None), 0, [])
        for module, name, value in ((update_checkout, 'fast_forward', lambda checkout, fetch: self.forwarded), (update_daily, 'state_dir', lambda: self.checkout)):
            patched = unittest.mock.patch.object(module, name, value)
            patched.start()
            self.addCleanup(patched.stop)

    def run_background(self) -> tuple[int, str | None]:
        code, _, _ = self.run_update('--background')
        notice = self.checkout / update_daily.NOTICE_NAME
        return (code, notice.read_text(encoding='utf-8').strip() if notice.exists() else None)

    def test_a_current_day_leaves_no_line(self) -> None:
        self.assertEqual(self.run_background(), (0, None))
        self.assertEqual(self.asked, [copies.APPS_STALE])

    def test_a_moved_checkout_is_said_once_in_one_line(self) -> None:
        self.forwarded = update_checkout.Forwarded(Upstream('origin/main', 0, 2, None), 2, [])
        code, line = self.run_background()
        self.assertEqual(code, 0)
        self.assertIn('Memar was updated', line)
        self.assertIn('2 commit(s)', line)
        self.assertEqual(len(line.splitlines()), 1)

    def test_a_refused_checkout_is_said_with_why(self) -> None:
        self.forwarded = update_checkout.Forwarded(Upstream('origin/main', 1, 3, None), 0, ['it has uncommitted changes', 'it has 1 unpushed commit(s)'])
        _, line = self.run_background()
        self.assertIn('3 commit(s) behind origin/main and was not updated because it has uncommitted changes', line)

    def test_stale_copies_are_refreshed_and_said(self) -> None:
        self.skill_lines = [SKILL_LINE]
        self.extensions = [self.checkout / 'editor' / 'memar.khayyam-1.0.0']
        _, line = self.run_background()
        self.assertEqual(self.asked, [copies.APPS_STALE, copies.APPS_REFRESH])
        self.installed.assert_called_once_with(self.checkout, only=self.extensions)
        self.assertIn('stale copies refreshed', line)

    def test_an_extension_refresh_that_fails_leaves_a_line_saying_what_to_run(self) -> None:
        self.skill_lines = [SKILL_LINE]
        self.extensions = [self.checkout / 'editor' / 'memar.khayyam-1.0.0']
        for failure in (OSError('Access is denied'), SystemExit('error: the recycle bin refused it')):
            with self.subTest(failure=failure):
                self.installed.side_effect = failure
                code, line = self.run_background()
                self.assertEqual(code, 0)
                self.assertIn(f'the editor extensions could not be refreshed ({failure})', line)
                self.assertIn('memar update --apply', line)
                self.assertIn('1 skill copy(ies)', line)
                self.assertNotIn('editor extension(s)', line)
                (self.checkout / update_daily.NOTICE_NAME).unlink()

    def test_a_run_while_another_holds_the_lock_does_nothing(self) -> None:
        self.skill_lines = [SKILL_LINE]
        with update_daily.daily_run(self.checkout) as held:
            self.assertTrue(held)
            self.assertEqual(self.run_background(), (0, None))
        self.assertEqual(self.asked, [])
        self.installed.assert_not_called()

class RealSkillSeam(unittest.TestCase):

    def test_a_home_without_agent_apps_has_no_stale_copy(self) -> None:
        with tempfile.TemporaryDirectory(dir=suite_scratch()) as home:
            environment = dict(os.environ, HOME=home, USERPROFILE=home, PYTHONDONTWRITEBYTECODE='1')
            with unittest.mock.patch.dict(os.environ, environment):
                self.assertEqual(copies.stale_skill_lines(), [])

class HelpSaysWhatIsChecked(unittest.TestCase):
    DAILY = ('Once a day', 'in the background', 'says so if it needs you', 'MEMAR_NO_AUTO_UPDATE=1')

    def ask(self, *arguments: str) -> str:
        completed = subprocess.run([sys.executable, str(LAUNCHER), *arguments], capture_output=True, env=dict(os.environ, COLUMNS='80', PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1'))
        self.assertEqual(completed.returncode, 0, completed.stderr)
        return ' '.join(completed.stdout.decode('utf-8').split())

    def test_the_help_names_what_is_checked_and_what_is_never_changed(self) -> None:
        text = self.ask(update.UPDATE_VERB, '--help')
        self.assertIn('usage: memar update', text)
        for phrase in ('--apply', '--quiet', '--offline', '--background', 'agent apps', 'MCP server', 'editor extensions', 'A command you run never changes the checkout', *self.DAILY):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)
        for mechanism in ('memar-update', 'memar-install-apps', 'editor_extension', 'child'):
            with self.subTest(mechanism=mechanism):
                self.assertNotIn(mechanism, text)

    def test_memar_help_meets_the_daily_run_in_the_verbs_summary(self) -> None:
        text = self.ask('--help')
        summary = ' '.join(update.SUMMARY.split())
        self.assertIn(summary, text)
        for phrase in self.DAILY:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, summary)
if __name__ == '__main__':
    unittest.main(verbosity=2)
