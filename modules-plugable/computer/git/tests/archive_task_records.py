#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for keeping a session's records in `modules-plugable/computer/git/services/archive_task_records.py`.

    python modules/management/task/tests/archive.py

The subject is keeping a session's records on a branch of its project's own
repository — the owner's rulings of 2026-10-14 and 2026-10-15 that
`session_archive`'s docstring states — named for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes outside its scratch folder: the Memar root is patched onto
a scratch folder, and the project, its repository and its registry entry are
made inside it. The branch is written through `_host_git_cli.py record`, which the
module runs by its path; the project's HEAD, index and working tree are
checked unmoved.

What is pinned, and what each pin is for:

  WhatIsKept      A session's whole folder is on the branch dev-knowledge at
                  .agents/tasks/<id>/ except the claim, caches, a path
                  with a .git part, binary files, a non-document file over
                  256 KB, and the session's own temp folder. The kept plan
                  names its project by its registered name and is otherwise as
                  written, bytes and line endings; the commit message lists
                  each leave-out with its size and reason. Keeping again
                  writes what the folder holds now, drops what it no longer
                  holds, and makes no commit when nothing changed; a dry run
                  writes nothing and says what would be kept.
  Standing        Whether a session is archived is whether the branch holds
                  what archiving would write now: a change after archiving, in
                  a file that is kept, makes it not archived; in temp, not.
  WhenNotOwed     A project whose preferences say `records: off`, a plan that
                  names no project, and a folder with no plan owe no records,
                  and nothing is written.
  WhenRefused     A `records` value it may not take, a project folder that is
                  not on this computer, a project with no registered name, a
                  project that is not a git repository, and a project whose
                  checked-out branch is the records branch are refused, with
                  why, and nothing is written: a record that cannot be kept
                  is not silently dropped.
  BranchNameIsOneConstant
                  The branch name is spelled in one line of the scripts,
                  `fs_memar.RECORDS_BRANCH`.
  RelatedSessions `archive` keeps the session named and every session whose
                  Parent chain leads to it in one commit, and prints the
                  branch reference of each and the commit.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
from importlib import import_module
_m_fs_test_scratch = import_module('modules-plugable.computer.filesystem.services.fs_test_scratch')
suite_scratch = _m_fs_test_scratch.suite_scratch
_m_fs_memar = import_module('modules-plugable.computer.filesystem.services.fs_memar')
memar_fs = _m_fs_memar
import argparse
import contextlib
import io
import subprocess
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parents[3] / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
session_archive = import_module('modules-plugable.computer.git.services.archive_task_records')
from modules.process.project.services.registry import add_project
Outcome = import_module('modules-plugable.computer.git.services.archive_task_records').Outcome
State = import_module('modules-plugable.computer.git.services.archive_task_records').State
NAME = 'example'
BRANCH = 'dev-knowledge'

class Fixture(unittest.TestCase):

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.fake_root = Path(self.scratch.name)
        patched = unittest.mock.patch.object(memar_fs, 'memar_root', return_value=self.fake_root)
        patched.start()
        self.addCleanup(patched.stop)
        self.project = self.fake_root / 'work' / NAME
        (self.project / '.agents' / 'memar').mkdir(parents=True)
        add_project(NAME, self.project)
        self.git('init', '-q', '-b', 'main')
        self.git('config', 'user.name', 'Test')
        self.git('config', 'user.email', 'test@example.org')
        (self.project / 'readme.md').write_text('project\n', encoding='utf-8', newline='\n')
        self.git('add', 'readme.md')
        self.git('commit', '-q', '-m', 'base')

    def git(self, *args: str, folder: Path | None=None) -> str:
        return subprocess.run(['git', '-C', str(folder or self.project), *args], capture_output=True, text=True, check=True).stdout.strip()

    def prefer(self, text: str) -> None:
        (self.project / 'manifest.yaml').write_text(f'memar:\n  {text}\n', encoding='utf-8', newline='\n')

    def session(self, sid: str, *, project: str | None=None, parent: str='', report: str='') -> Path:
        folder = memar_fs.task_dir(sid, create=True)
        named = str(self.project) if project is None else project
        front = ['---', f'Title: Task {sid}', 'Status: Complete', 'Opened: 2026-10-14T00:00:00Z']
        if named:
            front.append(f'Project: {named}')
        if parent:
            front.append(f'Parent: {parent}')
        front.append('---')
        (folder / 'plan.md').write_bytes('\r\n'.join([*front, f'# Task {sid}', '', '## Request', 'Do it.', '']).encode('utf-8'))
        (folder / 'report.md').write_text(report or '---\nTitle: T\nStatus: Complete\n---\n# Report\n\n## Result\nDone.\n', encoding='utf-8', newline='\n')
        (folder / 'claim').write_text('host: here\npid: 1\n', encoding='utf-8', newline='\n')
        return folder

    def put(self, folder: Path, relative: str, data: bytes=b'text\n') -> Path:
        path = folder / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def branch_files(self, sid: str) -> list[str]:
        if not self.git('branch', '--list', BRANCH):
            return []
        prefix = f'.agents/tasks/{sid}/'
        listed = self.git('ls-tree', '-r', '--name-only', BRANCH, '--', prefix).splitlines()
        return sorted((name.removeprefix(prefix) for name in listed))

    def blob(self, sid: str, relative: str) -> bytes:
        return subprocess.run(['git', '-C', str(self.project), 'cat-file', 'blob', f'{BRANCH}:.agents/tasks/{sid}/{relative}'], capture_output=True, check=True).stdout

    def commits(self) -> int:
        return len(self.git('rev-list', BRANCH).split()) if self.git('branch', '--list', BRANCH) else 0

    def keep(self, folder: Path, **named) -> session_archive.Kept:
        return session_archive.keep_records([folder], **named)[0]

class WhatIsKept(Fixture):
    REPORT = '---\nTitle: T\nStatus: Complete\n---\n# Report\n\n## Result\nThe entry is [drafted](docs/entry.md#first), the script [here](services/fix.py).\n'

    def make(self) -> Path:
        folder = self.session('20261014-T100000Z-1', report=self.REPORT)
        self.put(folder, 'docs/entry.md', b'# Entry\n')
        self.put(folder, 'docs/scratch.txt', b'not linked, kept\n')
        self.put(folder, 'services/fix.py', b"print('fix')\n")
        self.put(folder, 'services/__pycache__/fix.cpython-311.pyc', b'\x00\x00\x00')
        self.put(folder, 'temp/draft.md', b'draft\n')
        self.put(folder, 'lab/.git/config', b'[core]\n')
        self.put(folder, 'docs/pack.tar', b'a\x00b' * 100)
        self.put(folder, 'services/huge.py', b'x = 1\n' * 60000)
        self.put(folder, 'docs/long.md', b'line\n' * 100000)
        return folder

    def test_the_whole_folder_is_on_the_branch_minus_the_leave_outs(self) -> None:
        folder = self.make()
        kept = self.keep(folder)
        self.assertIs(kept.outcome, Outcome.KEPT, kept.why)
        self.assertEqual(self.branch_files(folder.name), ['docs/entry.md', 'docs/long.md', 'docs/scratch.txt', 'plan.md', 'report.md', 'services/fix.py'])
        self.assertEqual(kept.reference, f'{BRANCH}:.agents/tasks/{folder.name}/')
        self.assertEqual(kept.commit, self.git('rev-parse', BRANCH))

    def test_the_commit_message_lists_each_leave_out_with_its_size_and_reason(self) -> None:
        folder = self.make()
        self.keep(folder)
        message = self.git('log', '-1', '--format=%B', BRANCH)
        self.assertIn(folder.name, message.splitlines()[0])
        for path, words in (('claim', 'claim'), ('temp', 'never archived'), ('services/__pycache__', 'cache'), ('lab/.git', '.git'), ('docs/pack.tar', 'binary'), ('services/huge.py', '256 KB')):
            line = next((line for line in message.splitlines() if path in line), '')
            self.assertIn(words, line, f'{path}: {message}')
        self.assertIn('360000', next((line for line in message.splitlines() if 'huge.py' in line)))

    def test_the_project_is_untouched(self) -> None:
        folder = self.make()
        head, status = (self.git('rev-parse', 'HEAD'), self.git('status', '--porcelain'))
        self.keep(folder)
        self.assertEqual(self.git('rev-parse', 'HEAD'), head)
        self.assertEqual(self.git('symbolic-ref', 'HEAD'), 'refs/heads/main')
        self.assertEqual(self.git('status', '--porcelain'), status)
        self.assertFalse((self.project / '.agents' / 'sessions').exists())

    def test_the_kept_plan_names_its_project_by_name_and_is_otherwise_as_written(self) -> None:
        folder = self.make()
        self.keep(folder)
        original = (folder / 'plan.md').read_bytes().decode('utf-8')
        kept = self.blob(folder.name, 'plan.md').decode('utf-8')
        self.assertIn(f'Project: {NAME}\r\n', kept)
        self.assertNotIn(str(self.project), kept)
        self.assertEqual(kept, original.replace(f'Project: {self.project}', f'Project: {NAME}'))

    def test_every_other_file_is_kept_byte_for_byte(self) -> None:
        folder = self.make()
        self.put(folder, 'docs/crlf.md', b'one\r\ntwo\r\n')
        self.keep(folder)
        for relative in ('report.md', 'docs/crlf.md', 'docs/entry.md', 'services/fix.py'):
            self.assertEqual(self.blob(folder.name, relative), (folder / relative).read_bytes(), relative)

    def test_a_dry_run_says_what_would_be_kept_and_writes_nothing(self) -> None:
        folder = self.make()
        kept = self.keep(folder, write=False)
        self.assertIs(kept.outcome, Outcome.KEPT)
        self.assertEqual(kept.reference, f'{BRANCH}:.agents/tasks/{folder.name}/')
        self.assertIn('docs/entry.md', kept.files)
        self.assertNotIn('temp/draft.md', kept.files)
        self.assertIsNone(kept.commit)
        self.assertFalse(self.git('branch', '--list', BRANCH))

    def test_keeping_again_writes_what_the_folder_holds_now_and_drops_what_it_no_longer_holds(self) -> None:
        folder = self.make()
        self.keep(folder)
        (folder / 'report.md').write_text('---\nTitle: T\nStatus: Complete\n---\n# Report\nLater.\n', encoding='utf-8', newline='\n')
        (folder / 'docs' / 'scratch.txt').unlink()
        self.put(folder, 'docs/new.md', b'new\n')
        first = self.git('rev-parse', BRANCH)
        self.keep(folder)
        self.assertIn(b'Later.', self.blob(folder.name, 'report.md'))
        files = self.branch_files(folder.name)
        self.assertIn('docs/new.md', files)
        self.assertNotIn('docs/scratch.txt', files)
        self.assertEqual(self.git('rev-parse', f'{BRANCH}~1'), first)

    def test_keeping_what_is_already_kept_makes_no_commit(self) -> None:
        folder = self.make()
        first = self.keep(folder)
        again = self.keep(folder)
        self.assertIs(again.outcome, Outcome.KEPT)
        self.assertEqual(again.commit, first.commit)
        self.assertEqual(self.commits(), 1)

    def test_another_sessions_records_stay_when_this_one_is_kept_again(self) -> None:
        one, two = (self.session('20261014-T100001Z-2'), self.session('20261014-T100002Z-3'))
        self.keep(one)
        self.keep(two)
        self.put(one, 'docs/more.md')
        self.keep(one)
        self.assertIn('plan.md', self.branch_files(two.name))
        self.assertIn('docs/more.md', self.branch_files(one.name))

    def test_a_change_in_temp_is_no_change_to_the_records(self) -> None:
        folder = self.make()
        self.keep(folder)
        self.put(folder, 'temp/more.md', b'more\n')
        self.assertEqual(self.keep(folder).commit, self.git('rev-parse', BRANCH))
        self.assertEqual(self.commits(), 1)

class Standing(Fixture):

    def test_a_session_is_archived_once_the_branch_holds_what_archiving_would_write(self) -> None:
        folder = self.session('20261014-T101000Z-1')
        before = session_archive.standing(folder)
        self.assertIs(before.state, State.WAITING)
        self.keep(folder)
        self.assertIs(session_archive.standing(folder).state, State.ARCHIVED)

    def test_a_change_after_archiving_in_a_kept_file_makes_it_not_archived_again(self) -> None:
        folder = self.session('20261014-T101001Z-2')
        self.keep(folder)
        self.put(folder, 'docs/late.md')
        self.assertIs(session_archive.standing(folder).state, State.WAITING)
        self.keep(folder)
        self.assertIs(session_archive.standing(folder).state, State.ARCHIVED)

    def test_a_change_in_temp_or_the_claim_leaves_it_archived(self) -> None:
        folder = self.session('20261014-T101002Z-3')
        self.keep(folder)
        self.put(folder, 'temp/x.md')
        self.put(folder, 'claim', b'changed\n')
        self.assertIs(session_archive.standing(folder).state, State.ARCHIVED)

    def test_standing_writes_nothing(self) -> None:
        folder = self.session('20261014-T101003Z-4')
        session_archive.standing(folder)
        self.assertFalse(self.git('branch', '--list', BRANCH))

    def test_standing_says_not_owed_and_refused_as_keeping_would(self) -> None:
        self.prefer('records: off')
        off = self.session('20261014-T101004Z-5')
        self.assertIs(session_archive.standing(off).state, State.NOT_OWED)
        self.prefer('records: maybe')
        self.assertIs(session_archive.standing(off).state, State.REFUSED)

    def test_the_reference_is_the_branch_and_the_sessions_folder_on_it(self) -> None:
        self.assertEqual(session_archive.reference('20261014-T101005Z-6'), f'{BRANCH}:.agents/tasks/20261014-T101005Z-6/')

class WhenNotOwed(Fixture):

    def test_a_project_that_says_off_keeps_none(self) -> None:
        self.prefer('records: off')
        folder = self.session('20261014-T100001Z-2')
        kept = self.keep(folder)
        self.assertIs(kept.outcome, Outcome.NOT_OWED)
        self.assertIn('records: off', kept.why)
        self.assertFalse(self.git('branch', '--list', BRANCH))

    def test_an_empty_key_and_on_keep_them(self) -> None:
        for text in ('records:', 'records: on', 'sessions:'):
            with self.subTest(text=text):
                self.prefer(text)
                folder = self.session(f'20261014-T10000{len(text) % 10}Z-3')
                self.assertIs(self.keep(folder).outcome, Outcome.KEPT)

    def test_a_plan_that_names_no_project_owes_none(self) -> None:
        folder = self.session('20261014-T100002Z-4', project='')
        self.assertIs(self.keep(folder).outcome, Outcome.NOT_OWED)
        self.assertFalse(self.git('branch', '--list', BRANCH))

    def test_a_folder_with_no_plan_owes_none(self) -> None:
        folder = memar_fs.task_dir('20261014-T100003Z-5', create=True)
        self.assertIs(self.keep(folder).outcome, Outcome.NOT_OWED)

class WhenRefused(Fixture):

    def assertRefused(self, folder: Path, words: str) -> None:
        kept = self.keep(folder)
        self.assertIs(kept.outcome, Outcome.REFUSED)
        self.assertIn(words, kept.why)
        self.assertFalse(self.git('branch', '--list', BRANCH))

    def test_a_value_records_may_not_take_is_refused(self) -> None:
        self.prefer('records: maybe')
        self.assertRefused(self.session('20261014-T100004Z-6'), 'maybe')

    def test_a_project_not_on_this_computer_is_refused(self) -> None:
        folder = self.session('20261014-T100005Z-7', project=str(self.fake_root / 'elsewhere'))
        kept = self.keep(folder)
        self.assertIs(kept.outcome, Outcome.REFUSED)
        self.assertIn('not a folder', kept.why)

    def test_a_project_with_no_registered_name_is_refused(self) -> None:
        other = self.fake_root / 'work' / 'unnamed'
        other.mkdir(parents=True)
        self.git('init', '-q', '-b', 'main', folder=other)
        folder = self.session('20261014-T100006Z-8', project=str(other))
        kept = self.keep(folder)
        self.assertIs(kept.outcome, Outcome.REFUSED)
        self.assertIn('memar project add', kept.why)
        self.assertFalse(self.git('branch', '--list', BRANCH, folder=other))

    def test_a_project_that_is_not_a_git_repository_is_refused(self) -> None:
        plain = self.fake_root / 'work' / 'plain'
        plain.mkdir(parents=True)
        add_project('plain', plain)
        folder = self.session('20261014-T100007Z-9', project=str(plain))
        kept = self.keep(folder)
        self.assertIs(kept.outcome, Outcome.REFUSED)
        self.assertIn('not the top folder of a git repository', kept.why)
        self.assertFalse((plain / '.git').exists())

    def test_a_project_whose_checked_out_branch_is_the_records_branch_is_refused(self) -> None:
        self.git('checkout', '-q', '-b', BRANCH)
        folder = self.session('20261014-T100008Z-10')
        kept = self.keep(folder)
        self.assertIs(kept.outcome, Outcome.REFUSED)
        self.assertIn('checked out', kept.why)

class BranchNameIsOneConstant(unittest.TestCase):

    def test_no_script_spells_the_branch_name_but_the_one_line_that_defines_it(self) -> None:
        spelled = [path.relative_to(SCRIPTS).as_posix() for path in SCRIPTS.rglob('*.py') if 'tests' not in path.relative_to(SCRIPTS).parts and BRANCH in path.read_text(encoding='utf-8')]
        self.assertEqual(spelled, ['modules-plugable/computer/filesystem/services/fs_memar.py'])
        self.assertEqual(memar_fs.RECORDS_BRANCH, BRANCH)

class RelatedSessions(Fixture):

    def run_archive(self, sid: str) -> str:
        parser = argparse.ArgumentParser()
        verbs = parser.add_subparsers()
        run = session_archive.describe(verbs)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            run(parser.parse_args([session_archive.ARCHIVE_COMMAND, '--task-id', sid]))
        return out.getvalue()

    def test_the_session_and_those_its_parent_chain_leads_to_are_kept_in_one_commit_and_named(self) -> None:
        top = self.session('20261014-T110000Z-10')
        child = self.session('20261014-T110001Z-11', parent=top.name)
        grandchild = self.session('20261014-T110002Z-12', parent=child.name)
        other = self.session('20261014-T110003Z-13')
        said = self.run_archive(top.name)
        for each in (top, child, grandchild):
            self.assertIn('plan.md', self.branch_files(each.name), each.name)
            self.assertIn(session_archive.reference(each.name), said)
        self.assertEqual(self.branch_files(other.name), [])
        self.assertEqual(self.commits(), 1)
        self.assertIn(self.git('rev-parse', BRANCH), said)

    def test_a_refused_session_is_named_with_why_and_fails_the_verb(self) -> None:
        top = self.session('20261014-T110004Z-14', project=str(self.fake_root / 'elsewhere'))
        with self.assertRaises(SystemExit):
            self.run_archive(top.name)

    def test_a_refused_session_stops_the_others_of_the_task_too(self) -> None:
        top = self.session('20261014-T110006Z-16')
        self.session('20261014-T110007Z-17', parent=top.name, project=str(self.fake_root / 'elsewhere'))
        with self.assertRaises(SystemExit):
            self.run_archive(top.name)
        self.assertEqual(self.branch_files(top.name), [])

    def test_an_unknown_session_is_refused(self) -> None:
        with self.assertRaises(SystemExit):
            self.run_archive('20261014-T110005Z-15')

    def test_the_help_names_the_branch_and_what_is_left_out(self) -> None:
        parser = argparse.ArgumentParser()
        session_archive.describe(parser.add_subparsers())
        helper = io.StringIO()
        with contextlib.redirect_stdout(helper), self.assertRaises(SystemExit):
            parser.parse_args([session_archive.ARCHIVE_COMMAND, '--help'])
        said = helper.getvalue()
        for words in (BRANCH, '.agents/tasks/', 'temp', 'claim', '256 KB', 'binary', 'never pushes'):
            self.assertIn(words, said)
if __name__ == '__main__':
    unittest.main(verbosity=2)
