#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for `memar resident`, the process that answers the `memar` command, and the command's side of it.

    python bundles/memar/services/resident/tests/resident.py

The subject is the resident process `resident/services/serve.py` starts and the client `machine/resident.py`
the router asks first, named for the file that holds the verb per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md). Its defining document is the
verbs' own help and the plan of task 20261020-T061848Z-22132; the expectations below are the plan's.

Every process here keeps its state in a folder of its own (MEMAR_SERVER_STATE), so none meets the owner's resident
process, and every child has the null device for stdin, which is what an agent's shell call has.

What is pinned:

  FallsBackAndStarts   With none running, a call is answered in place exactly as with MEMAR_SERVER=0 and starts the
                       process, which a later call finds.
  AnswersAsTheCli      A handed-over call's stdout, stderr and status are byte for byte the command's own, for a
                       verb, a refusal by the verb and a refusal by the parser.
  SwitchedOff          With MEMAR_SERVER=0 nothing is handed over and nothing is started.
  PipedStdinStaysHome  A call whose stdin is a pipe is done in place, never handed over.
  CallsOverlap         A slow call does not hold a fast one; nine calls at once each get the command's own answer;
                       a connection that sends nothing holds only itself.
  BusyIsDoneInPlace    With every worker busy, a call is done in place and the process does not run it afterwards.
  RefusesAWrongToken   A request without the process's token is refused and runs nothing.
  EndsWhenIdleOrAsked  The process ends after MEMAR_SERVER_IDLE seconds without a call, and on `resident stop`,
                       removing its state file; a second `serve` finds the first and ends at once.
  CodeIsLookedAtOnce   The pool looks at the code's fingerprint at most once in `check_every` seconds, and a change is a new generation.
"""
from __future__ import annotations
from importlib import import_module
_m_fs_test_scratch = import_module('modules-plugable.computer.filesystem.services.fs_test_scratch')
remove_tree = _m_fs_test_scratch.remove_tree
suite_scratch = _m_fs_test_scratch.suite_scratch
import json
import os
import socket
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parents[2]
TOP = SCRIPTS.parent.parent
for folder in (TOP, SCRIPTS, SCRIPTS / 'services'):
    if str(folder) not in sys.path:
        sys.path.insert(0, str(folder))
sys.dont_write_bytecode = True
ROUTER = SCRIPTS / 'memar'

def environment(state: Path | None, on: bool, idle: int=600) -> dict:
    found = {key: value for key, value in os.environ.items() if key not in ('MEMAR_SERVER', 'MEMAR_SERVER_STATE', 'MEMAR_SERVER_IDLE')}
    if state is not None:
        found['MEMAR_SERVER_STATE'] = str(state)
    if on:
        found['MEMAR_SERVER_IDLE'] = str(idle)
    else:
        found['MEMAR_SERVER'] = '0'
    return found

def cli(argv: list[str], env: dict, stdin=subprocess.DEVNULL, input: bytes | None=None) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(ROUTER), *argv], env=env, stdin=None if input is not None else stdin, input=input, capture_output=True, timeout=120)

def state_file(state: Path) -> dict | None:
    try:
        return json.loads((state / 'state.json').read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return None

def wait_for(check, seconds: float=30.0):
    end = time.monotonic() + seconds
    while time.monotonic() < end:
        found = check()
        if found:
            return found
        time.sleep(0.2)
    return None

def stop(state: Path) -> None:
    cli(['resident', 'stop'], environment(state, False))
    wait_for(lambda: state_file(state) is None, 15)

class WithState(unittest.TestCase):

    def setUp(self) -> None:
        self.state = Path(tempfile.mkdtemp(prefix='resident-', dir=suite_scratch()))
        self.addCleanup(remove_tree, self.state)
        self.addCleanup(stop, self.state)

    def start(self, idle: int=600) -> dict:
        found = cli(['content', 'hour-id'], environment(self.state, True, idle))
        self.assertEqual(found.returncode, 0, found.stderr)
        state = wait_for(lambda: state_file(self.state))
        self.assertIsNotNone(state, 'the first call did not start the process')
        return state

    def count(self) -> int:
        status = cli(['resident', 'status'], environment(self.state, False))
        self.assertEqual(status.returncode, 0, status.stderr)
        return int(status.stdout.decode().split(' calls answered')[0].split(', ')[-1])

class FallsBackAndStarts(WithState):

    def test_the_first_call_is_answered_in_place_and_starts_the_process(self) -> None:
        plain = cli(['content', 'hour-id'], environment(None, False))
        first = cli(['content', 'hour-id'], environment(self.state, True))
        self.assertEqual((first.stdout, first.stderr, first.returncode), (plain.stdout, plain.stderr, plain.returncode))
        self.assertIsNotNone(wait_for(lambda: state_file(self.state)), 'the process did not start')

    def test_a_stale_state_file_is_answered_in_place(self) -> None:
        self.state.mkdir(parents=True, exist_ok=True)
        (self.state / 'state.json').write_text(json.dumps({'port': 1, 'token': 'x', 'pid': 1}), encoding='utf-8')
        found = cli(['content', 'hour-id'], environment(self.state, True))
        self.assertEqual(found.returncode, 0)
        self.assertTrue(found.stdout.strip().isdigit())

class AnswersAsTheCli(WithState):

    def test_stdout_stderr_and_status_are_the_commands_own(self) -> None:
        self.start()
        for argv in (['commands'], ['content', 'hour-id'], ['content', 'section', 'docs/cognition.md', 'Abstract'], ['content', 'section', 'docs/cognition.md', 'No such heading anywhere'], ['task', 'nonsense'], ['--help']):
            with self.subTest(argv=argv):
                before = self.count()
                plain = cli(argv, environment(None, False))
                handed = cli(argv, environment(self.state, True))
                self.assertEqual((handed.stdout, handed.stderr, handed.returncode), (plain.stdout, plain.stderr, plain.returncode))
                self.assertEqual(self.count(), before + 1, 'the call was not answered by the process')

class SwitchedOff(WithState):

    def test_nothing_is_handed_over_or_started(self) -> None:
        found = cli(['content', 'hour-id'], environment(self.state, False))
        self.assertEqual(found.returncode, 0)
        time.sleep(2)
        self.assertIsNone(state_file(self.state))

class PipedStdinStaysHome(WithState):

    def test_a_pipe_is_done_in_place(self) -> None:
        self.start()
        before = self.count()
        found = cli(['content', 'hour-id'], environment(self.state, True), input=b'')
        self.assertEqual(found.returncode, 0)
        self.assertEqual(self.count(), before)

class CallsOverlap(WithState):

    def test_a_slow_call_does_not_hold_a_fast_one(self) -> None:
        self.start()
        results: dict = {}

        def slow() -> None:
            started = time.monotonic()
            results['slow'] = (cli(['content', 'find', 'tasks'], environment(self.state, True)), time.monotonic() - started)
        thread = threading.Thread(target=slow)
        thread.start()
        time.sleep(0.5)
        started = time.monotonic()
        fast = cli(['content', 'hour-id'], environment(self.state, True))
        fast_time = time.monotonic() - started
        thread.join(timeout=120)
        self.assertEqual(fast.returncode, 0)
        self.assertTrue(fast.stdout.strip().isdigit())
        self.assertIn('slow', results)
        self.assertLess(fast_time, results['slow'][1], 'the fast call waited for the slow one')

    def test_many_at_once_each_get_the_commands_own_answer(self) -> None:
        self.start()
        argvs = [['content', 'hour-id'], ['commands'], ['content', 'section', 'docs/cognition.md', 'Abstract']] * 3
        plain = {tuple(argv): cli(argv, environment(None, False)) for argv in argvs}
        found: list = []
        guard = threading.Lock()

        def one(argv: list[str]) -> None:
            result = cli(argv, environment(self.state, True))
            with guard:
                found.append((argv, result))
        threads = [threading.Thread(target=one, args=(argv,)) for argv in argvs]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(timeout=180)
        self.assertEqual(len(found), len(argvs))
        for argv, result in found:
            expected = plain[tuple(argv)]
            self.assertEqual((result.stdout, result.stderr, result.returncode), (expected.stdout, expected.stderr, expected.returncode), argv)

    def test_a_silent_connection_holds_only_itself(self) -> None:
        state = self.start()
        with socket.create_connection(('127.0.0.1', state['port']), timeout=10):
            before = self.count()
            found = cli(['content', 'hour-id'], environment(self.state, True))
            self.assertEqual(found.returncode, 0)
            self.assertEqual(self.count(), before + 1, 'the call was not answered by the process')

class BusyIsDoneInPlace(WithState):

    def test_with_every_worker_busy_a_call_is_done_in_place_and_not_run_twice(self) -> None:
        env = environment(self.state, True)
        env['MEMAR_SERVER_WORKERS'] = '1'
        first = cli(['content', 'hour-id'], env)
        self.assertEqual(first.returncode, 0)
        self.assertIsNotNone(wait_for(lambda: state_file(self.state)))
        wait_for(lambda: cli(['resident', 'status'], environment(self.state, False)).returncode == 0)
        holder = threading.Thread(target=lambda: cli(['content', 'find', 'tasks'], env))
        holder.start()
        time.sleep(0.5)
        before = self.count()
        started = time.monotonic()
        found = cli(['content', 'hour-id'], env)
        spent = time.monotonic() - started
        holder.join(timeout=120)
        self.assertEqual(found.returncode, 0)
        self.assertTrue(found.stdout.strip().isdigit())
        self.assertLess(spent, 30)
        self.assertLessEqual(self.count() - before, 1)

class RefusesAWrongToken(WithState):

    def test_nothing_runs(self) -> None:
        state = self.start()
        before = self.count()
        with socket.create_connection(('127.0.0.1', state['port']), timeout=10) as connection:
            connection.sendall(json.dumps({'token': 'wrong', 'argv': ['content', 'hour-id'], 'cwd': str(TOP), 'env': {}}).encode() + b'\n')
            answer = json.loads(connection.makefile('rb').readline())
        self.assertEqual(answer, {'refused': 'not allowed'})
        self.assertEqual(self.count(), before)

class EndsWhenIdleOrAsked(WithState):

    def test_idle_ends_it_and_removes_the_state(self) -> None:
        self.start(idle=3)
        self.assertTrue(wait_for(lambda: state_file(self.state) is None, 30), 'the process did not end when idle')

    def test_stop_ends_it_and_a_second_serve_ends_at_once(self) -> None:
        self.start()
        again = cli(['resident', 'serve'], environment(self.state, False))
        self.assertEqual(again.returncode, 0)
        self.assertIn(b'already running', again.stderr)
        self.assertEqual(cli(['resident', 'stop'], environment(self.state, False)).returncode, 0)
        self.assertTrue(wait_for(lambda: state_file(self.state) is None, 15))
        self.assertEqual(cli(['resident', 'status'], environment(self.state, False)).returncode, 1)

def pool_module():
    """`_pool.py` loaded by its path: this file is itself named `resident`, so the package of that name is not reachable by import."""
    import importlib.util
    spec = importlib.util.spec_from_file_location('resident_pool', SCRIPTS / 'services' / 'resident' / 'services' / '_pool.py')
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module

class CodeIsLookedAtOnce(unittest.TestCase):

    def test_the_fingerprint_is_not_taken_twice_within_check_every(self) -> None:
        _pool = pool_module()
        taken = []
        original = _pool.fingerprint
        _pool.fingerprint = lambda top: taken.append(1) or ()
        try:
            pool = _pool.Pool(TOP, SCRIPTS, 1, check_every=3600.0)
            pool.generation_now()
            pool.generation_now()
        finally:
            _pool.fingerprint = original
        self.assertEqual(len(taken), 1)

    def test_a_changed_fingerprint_is_a_new_generation(self) -> None:
        _pool = pool_module()
        original, answers = (_pool.fingerprint, [('a',), ('a',), ('b',)])
        _pool.fingerprint = lambda top: answers.pop(0)
        try:
            pool = _pool.Pool(TOP, SCRIPTS, 1, check_every=0.0)
            numbers = [pool.generation_now() for _ in range(3)]
        finally:
            _pool.fingerprint = original
        self.assertEqual(numbers, [0, 0, 1])
if __name__ == '__main__':
    unittest.main()
