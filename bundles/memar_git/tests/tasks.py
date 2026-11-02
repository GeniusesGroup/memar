#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
TIER = 'system'
BUDGET_SECONDS = 120
import ast
import contextlib
import io
import subprocess
import sys
import unittest
import unittest.mock
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _scratch import BUNDLE, ScratchRepository, bundle, errors

class ServerDouble:

    def __init__(self, known=(), unreachable=None) -> None:
        self.known = set(known)
        self.unreachable = unreachable
        self.calls: list[list[str]] = []

    def __call__(self, arguments, *rest, **named):
        self.calls.append([str(word) for word in arguments])
        if self.unreachable is not None:
            raise self.unreachable
        asked = [word for word in self.calls[-1] if word in self.known or word.startswith('2000')]
        found = bool(asked) and asked[0] in self.known
        return subprocess.CompletedProcess(arguments, 0 if found else 1, '' if found else '', '' if found else f'no task {asked[0] if asked else ""}')

class CommitCitesItsTasks(ScratchRepository):
    KNOWN = '20000101-T000000Z-1'
    OTHER = '20000101-T000000Z-2'
    UNKNOWN = '20000101-T000000Z-9'

    def setUp(self) -> None:
        super().setUp()
        self.module = bundle('services.commit')
        self.tasks = bundle('services._tasks')
        self.errors = errors()
        self.put('mine.md', 'mine\n')

    def commit_here(self, server, *given, no_task=False, paths=('mine.md',), fold=0):
        with contextlib.redirect_stderr(io.StringIO()), contextlib.redirect_stdout(io.StringIO()):
            with unittest.mock.patch.object(self.tasks, 'server', server):
                return self.module.cmd_commit(self.repo, [Path(p) for p in paths], [], [], fold, self.message, tasks=list(given), no_task=no_task)

    def tasks_of(self, commit: str = 'HEAD') -> list[str]:
        return self.git('log', '-1', '--format=%(trailers:key=Task,valueonly)', commit).split()

    def test_a_commit_that_cites_no_task_is_refused_naming_the_form_it_wants(self) -> None:
        with self.assertRaises(self.errors.TaskNotCited) as raised:
            self.commit_here(ServerDouble())
        for wanted in ('--task-id', 'Task: ', '--no-task'):
            self.assertIn(wanted, str(raised.exception))
        self.assertEqual(self.git('rev-parse', 'HEAD'), self.base)

    def test_the_opt_out_and_a_task_together_are_refused(self) -> None:
        with self.assertRaises(self.errors.TaskNotCited):
            self.commit_here(ServerDouble([self.KNOWN]), self.KNOWN, no_task=True)
        self.assertEqual(self.git('rev-parse', 'HEAD'), self.base)

    def test_a_commit_that_carries_out_no_task_asks_the_server_nothing(self) -> None:
        server = ServerDouble()
        self.commit_here(server, no_task=True)
        self.assertEqual(server.calls, [])
        self.assertEqual(self.tasks_of(), [])

    def test_a_task_the_server_does_not_know_is_refused_naming_it_and_not_the_known_one(self) -> None:
        server = ServerDouble([self.KNOWN])
        with self.assertRaises(self.errors.TaskUnknown) as raised:
            self.commit_here(server, self.KNOWN, self.UNKNOWN)
        self.assertIn(self.UNKNOWN, str(raised.exception))
        self.assertNotIn(f'no task {self.KNOWN}', str(raised.exception))
        self.assertEqual(self.git('rev-parse', 'HEAD'), self.base)

    def test_each_cited_task_is_asked_of_the_server_with_the_repository_as_the_project(self) -> None:
        server = ServerDouble([self.KNOWN, self.OTHER])
        self.commit_here(server, self.KNOWN, self.OTHER, self.KNOWN)
        asked = [word for call in server.calls for word in call]
        for each in (self.KNOWN, self.OTHER):
            self.assertIn(each, asked)
        self.assertTrue(any(str(self.repo) in call for call in server.calls), server.calls)

    def test_each_task_is_a_trailer_git_log_reads_back_beside_the_others(self) -> None:
        self.message.write_text('subject\n\nbody\n\nCo-Authored-By: Someone <someone@example.org>\n', encoding='utf-8', newline='\n')
        self.commit_here(ServerDouble([self.KNOWN, self.OTHER]), self.KNOWN, self.OTHER, self.KNOWN)
        self.assertEqual(self.tasks_of(), [self.KNOWN, self.OTHER])
        self.assertEqual(self.git('log', '-1', '--format=%(trailers:key=Co-Authored-By,valueonly)'), 'Someone <someone@example.org>')
        self.assertEqual(self.git('log', '-1', '--format=%s'), 'subject')

    def test_a_task_written_into_the_message_by_hand_is_refused(self) -> None:
        self.message.write_text(f'subject\n\nTask: {self.KNOWN}\n', encoding='utf-8', newline='\n')
        with self.assertRaises(self.errors.TaskByHand):
            self.commit_here(ServerDouble([self.KNOWN]), no_task=True)
        self.assertEqual(self.git('rev-parse', 'HEAD'), self.base)

    def test_a_fold_keeps_the_tasks_of_the_commits_it_replaces(self) -> None:
        server = ServerDouble([self.KNOWN, self.OTHER])
        self.commit_here(server, self.KNOWN)
        self.put('shared.md', 'a finding\n')
        self.commit_here(server, self.OTHER, paths=('mine.md', 'shared.md'), fold=1)
        self.assertEqual(self.git('rev-parse', 'HEAD^'), self.base)
        self.assertEqual(self.tasks_of(), [self.KNOWN, self.OTHER])

class TheTasksReachGoesThroughTheServer(ScratchRepository):
    TASK = '20000101-T000000Z-1'

    def setUp(self) -> None:
        super().setUp()
        self.tasks = bundle('services._tasks')
        self.errors = errors()

    def asked(self, server):
        with unittest.mock.patch.object(self.tasks, 'server', server):
            return self.tasks.not_found([self.TASK], self.repo)

    def test_a_known_task_is_not_in_the_answer(self) -> None:
        self.assertEqual(self.asked(ServerDouble([self.TASK])), [])

    def test_an_unknown_task_is_in_the_answer_with_what_the_server_said(self) -> None:
        said = self.asked(ServerDouble())
        self.assertEqual(len(said), 1)
        self.assertIn('no task', said[0])

    def test_a_server_that_cannot_be_started_is_unreachable_and_not_a_task_unknown(self) -> None:
        with self.assertRaises(self.errors.ServerUnreachable) as raised:
            self.asked(ServerDouble(unreachable=FileNotFoundError('memar')))
        self.assertNotIsInstance(raised.exception, self.errors.TaskUnknown)

    def test_a_server_that_does_not_answer_in_time_is_unreachable(self) -> None:
        with self.assertRaises(self.errors.ServerUnreachable):
            self.asked(ServerDouble(unreachable=subprocess.TimeoutExpired('memar', 1)))

    def test_a_server_unreachable_never_lets_a_commit_through(self) -> None:
        self.put('mine.md', 'mine\n')
        commit = bundle('services.commit')
        with contextlib.redirect_stderr(io.StringIO()), contextlib.redirect_stdout(io.StringIO()):
            with unittest.mock.patch.object(self.tasks, 'server', ServerDouble(unreachable=OSError('down'))):
                with self.assertRaises(self.errors.ServerUnreachable):
                    commit.cmd_commit(self.repo, [Path('mine.md')], [], [], 0, self.message, tasks=[self.TASK], no_task=False)
        self.assertEqual(self.git('rev-parse', 'HEAD'), self.base)

    def test_the_bundle_imports_no_module_of_the_task_domain_and_reads_no_task_store(self) -> None:
        for file in sorted(BUNDLE.rglob('*.py')):
            if 'tests' in file.parts:
                continue
            with self.subTest(file=file.name):
                for node in ast.walk(ast.parse(file.read_text(encoding='utf-8'))):
                    named = []
                    if isinstance(node, ast.Import):
                        named = [alias.name for alias in node.names]
                    elif isinstance(node, ast.ImportFrom) and node.module:
                        named = [node.module]
                    elif isinstance(node, ast.Call) and node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
                        named = [node.args[0].value]
                    for each in named:
                        self.assertNotIn('management.task', each)
                        self.assertNotIn('management/task', each)
                        self.assertNotIn('computer.git', each)

if __name__ == '__main__':
    unittest.main()
