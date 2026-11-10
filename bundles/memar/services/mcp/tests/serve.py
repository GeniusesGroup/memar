#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for `memar mcp serve`, the MCP server over stdio.

    python bundles/memar/services/mcp/tests/serve.py

The subject is the server `mcp/services/serve.py` starts, with the worker and its parts beside it,
named for the file that holds the verb per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md). Its defining
documents are the verb's own help and the content of a task
that records what the owner chose; the expectations below are theirs.

Each test that talks to the server starts one, as an agent app does, and speaks MCP to it over its
stdin and stdout. Every child is a test run, so the daily update's hook does nothing in it or in the
CLI it is compared with.

What is pinned:

  AnswersAsTheCli       Each tool's answer — its stdout, its stderr, its exit status — is byte for
                        byte what `memar` prints for the same arguments, for `content search`,
                        `content find`, `content section`, `task list` and `commands`, a refusal
                        by the verb and a refusal by the parser among them.
  ToolsAreTheVerbs      `tools/list` holds one tool per leaf verb `memar --help` reaches, and no
                        tool for `mcp` itself.
  SeesEditsWithoutRestart
                        A document edited, added, and deleted between two calls of one server is
                        seen by the next call, and the tools are never said to have changed; an
                        edit that leaves the file's size and modification time as they were is seen
                        too, when the file was read within two seconds of its modification.
  CodeChangeReplacesWorker
                        A change of a Python file leaves the worker as it is (same process, no
                        notice); a worker that died is answered for with an error and the next
                        request starts another without a new `initialize` and without a notice;
                        one that dies while it starts is answered for with an error and the next
                        request starts one; a batch is refused, not left waiting; a call that
                        outlasts `CALL_SECONDS` is answered with an error naming the limit, and
                        its worker is killed.
  CallsCarryNoState     A module global a call changed is as its import left it at the next call.
  ArgumentsAsTyped      A call's arguments become the words the CLI would be typed with.
"""
from __future__ import annotations
TIER = 'system'
BUDGET_SECONDS = 150
from importlib import import_module
_m_test_scratch = import_module('modules.process.test.services.test_scratch')
remove_tree = _m_test_scratch.remove_tree
suite_scratch = _m_test_scratch.suite_scratch
import json
import os
import subprocess
import sys
import time
import unittest
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = next(p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()) / 'bundles' / 'memar'
TOP = SCRIPTS.parent.parent
for folder in (TOP, SCRIPTS, SCRIPTS / 'services'):
    if str(folder) not in sys.path:
        sys.path.insert(0, str(folder))
sys.dont_write_bytecode = True
from mcp.services import _call, _tools, serve
ROUTER = SCRIPTS / 'memar'
_m_memar_location = import_module('bundles.memar.services.location.memar_location')
_m_memar_location.declare_program(_m_memar_location.entry_program(str(ROUTER)))
THIS_TASK = '20261019-T111413Z-21136'

def load_router():
    from importlib.machinery import SourceFileLoader
    from importlib.util import module_from_spec, spec_from_loader
    loader = SourceFileLoader('memar_router_probe', str(ROUTER))
    module = module_from_spec(spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = module
    loader.exec_module(module)
    return module

def cli(argv: list[str], stdin: str='') -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(ROUTER), *argv], input=stdin.encode('utf-8'), capture_output=True)

class Server:
    """One server, spoken to as an agent app speaks to it."""

    def __init__(self) -> None:
        self.process = subprocess.Popen([sys.executable, str(ROUTER), 'mcp', 'serve'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        self.number = 0
        self.notices: list[dict] = []
        self.request('initialize', {'protocolVersion': '2025-06-18', 'capabilities': {}, 'clientInfo': {'name': 'test', 'version': '0'}})
        self.notify('notifications/initialized')

    def _write(self, message: dict) -> None:
        self.process.stdin.write(json.dumps(message).encode('utf-8') + b'\n')
        self.process.stdin.flush()

    def notify(self, method: str) -> None:
        self._write({'jsonrpc': '2.0', 'method': method})

    def request(self, method: str, params: dict | None=None) -> dict:
        self.number += 1
        self._write({'jsonrpc': '2.0', 'id': self.number, 'method': method, 'params': params or {}})
        while True:
            line = self.process.stdout.readline()
            if not line:
                raise AssertionError('the server stopped')
            message = json.loads(line)
            if 'id' not in message:
                self.notices.append(message)
                continue
            assert message['id'] == self.number, message
            if 'error' in message:
                raise AssertionError(message['error'])
            return message['result']

    def call(self, name: str, arguments: dict) -> tuple[bytes, bytes, int]:
        result = self.request('tools/call', {'name': name, 'arguments': arguments})
        texts = [item['text'] for item in result['content']]
        stdout, stderr = (texts[0], texts[1] if len(texts) > 1 else '')
        status = result['_meta']['memar/status']
        assert result['isError'] == (status != 0), result
        return (stdout.encode('utf-8'), stderr.encode('utf-8'), status)

    def close(self) -> None:
        self.process.stdin.close()
        self.process.wait(timeout=30)
        self.process.stdout.close()

class WithServer(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.server = Server()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.close()

class AnswersAsTheCli(WithServer):
    CASES = (('content_search', {'patterns': ['guest adapter']}, ['content', 'search', 'guest adapter']), ('content_find', {'text': 'mcp guest adapter', 'top': 3}, ['content', 'find', 'mcp guest adapter', '--top', '3']), ('content_find', {'text': 'server stdio', 'no_links': True}, ['content', 'find', '--no-links', 'server stdio']), ('content_find', {'text': 'anything', 'top': 0}, ['content', 'find', 'anything', '--top', '0']), ('content_find', {'top': 2}, ['content', 'find', '--top', '2']), ('content_get-section', {'file': 'modules/net/srpc/srpc.md', 'heading': 'Abstract'}, ['content', 'get-section', 'modules/net/srpc/srpc.md', 'Abstract']), ('content_get-section', {'file': 'modules/net/srpc/srpc.md', 'heading': '#abstract', 'hash': True}, ['content', 'get-section', '--hash', 'modules/net/srpc/srpc.md', '#abstract']), ('content_get-section', {'file': 'modules/net/srpc/srpc.md', 'heading': 'No Such Heading'}, ['content', 'get-section', 'modules/net/srpc/srpc.md', 'No Such Heading']), ('task_list', {'text': THIS_TASK}, ['task', 'list', THIS_TASK]), ('commands', {}, ['commands']))

    def test_every_answer_is_the_clis_byte_for_byte(self):
        for name, arguments, argv in self.CASES:
            with self.subTest(tool=name, arguments=arguments):
                stdout, stderr, status = self.server.call(name, arguments)
                expected = cli(argv)
                self.assertEqual(stdout, expected.stdout)
                self.assertEqual(stderr, expected.stderr)
                self.assertEqual(status, expected.returncode)

class ToolsAreTheVerbs(WithServer):

    def test_one_tool_per_leaf_verb_and_none_for_the_server_itself(self):
        import argparse
        router = load_router()
        parser, _ = router.assemble(router.services())

        def leaves(parser, words):
            verbs = [action for action in parser._actions if isinstance(action, argparse._SubParsersAction)]
            if not verbs:
                return {' '.join(words)}
            return set().union(*(leaves(child, [*words, word]) for word, child in verbs[0].choices.items()))
        verbs = leaves(parser, [])
        self.assertIn('mcp serve', verbs)
        names = {tool['name'] for tool in self.server.request('tools/list')['tools']}
        self.assertEqual(names, {verb.replace(' ', '_') for verb in verbs if not verb.startswith('mcp ')})

    def test_each_tool_takes_what_its_verb_takes(self):
        tools = {tool['name']: tool for tool in self.server.request('tools/list')['tools']}
        find = tools['content_find']['inputSchema']
        self.assertEqual(find['required'], ['text'])
        self.assertEqual(find['properties']['top']['type'], 'integer')
        self.assertEqual(find['properties']['no_links']['type'], 'boolean')
        self.assertNotIn('stdin', find['properties'])
        self.assertIn('rank the sections', tools['content_find']['description'])

class SeesEditsWithoutRestart(unittest.TestCase):

    def setUp(self) -> None:
        self.project = suite_scratch() / f'mcp-serve-{os.getpid()}-{time.time_ns()}'
        (self.project / 'docs').mkdir(parents=True)
        self.first = self.project / 'docs' / 'first.md'
        self.first.write_text('# First\nzanzibar is the word of this document.\n', encoding='utf-8', newline='\n')
        self.server = Server()

    def tearDown(self) -> None:
        self.server.close()
        remove_tree(self.project)

    def found(self, word: str) -> str:
        stdout, _, _ = self.server.call('content_find', {'text': word, 'project_path': str(self.project), 'no_links': True})
        return stdout.decode('utf-8')

    def test_an_edit_an_addition_and_a_deletion_are_each_seen_by_the_next_call(self):
        self.assertIn('docs/first.md#first', self.found('zanzibar'))
        self.first.write_text('# First\nkilimanjaro took its place, and the text is longer now.\n', encoding='utf-8', newline='\n')
        self.assertNotIn('first.md', self.found('zanzibar'))
        self.assertIn('docs/first.md#first', self.found('kilimanjaro'))
        second = self.project / 'docs' / 'second.md'
        second.write_text('# Second\nserengeti only here.\n', encoding='utf-8', newline='\n')
        self.assertIn('docs/second.md#second', self.found('serengeti'))
        second.unlink()
        self.assertNotIn('second.md', self.found('serengeti'))
        self.assertEqual(self.server.notices, [])

    def test_an_edit_that_keeps_size_and_time_is_seen_while_the_file_is_fresh(self):
        self.assertIn('docs/first.md#first', self.found('zanzibar'))
        before = self.first.stat()
        self.first.write_text('# First\ntanzania is the word of this document.\n', encoding='utf-8', newline='\n')
        os.utime(self.first, ns=(before.st_atime_ns, before.st_mtime_ns))
        self.assertEqual(self.first.stat().st_size, before.st_size)
        self.assertIn('docs/first.md#first', self.found('tanzania'))
        self.assertNotIn('first.md', self.found('zanzibar'))

class CodeChangeReplacesWorker(unittest.TestCase):

    def test_a_changed_python_file_leaves_the_worker_and_sends_no_notice(self):
        top = suite_scratch() / f'mcp-kept-{os.getpid()}-{time.time_ns()}'
        (top / 'modules' / 'one').mkdir(parents=True)
        code = top / 'modules' / 'one' / 'one.py'
        code.write_text('A = 1\n', encoding='utf-8')
        relay = serve.Relay()
        try:
            line = lambda number, method: json.dumps({'jsonrpc': '2.0', 'id': number, 'method': method, 'params': {}}).encode() + b'\n'
            initialize = json.dumps({'jsonrpc': '2.0', 'id': 1, 'method': 'initialize', 'params': {'protocolVersion': '2025-06-18'}}).encode() + b'\n'
            self.assertEqual(len(relay.handle(initialize)), 1)
            relay.handle(b'{"jsonrpc":"2.0","method":"notifications/initialized"}\n')
            first, pid = (relay.worker, relay.worker.process.pid)
            self.assertEqual(len(relay.handle(line(2, 'ping'))), 1)
            code.write_text('A = 22\n', encoding='utf-8')
            (top / 'modules' / 'one' / 'two.py').write_text('', encoding='utf-8')
            sent = relay.handle(line(3, 'tools/list'))
            self.assertEqual(len(sent), 1)
            self.assertIn('tools', json.loads(sent[0])['result'])
            self.assertIs(relay.worker, first)
            self.assertEqual(relay.worker.process.pid, pid)
        finally:
            relay.stop()
            remove_tree(top)

    def test_a_worker_that_died_is_answered_for_and_the_next_request_starts_another_without_a_notice(self):
        relay = serve.Relay()
        try:
            line = lambda number, method: json.dumps({'jsonrpc': '2.0', 'id': number, 'method': method, 'params': {}}).encode() + b'\n'
            initialize = json.dumps({'jsonrpc': '2.0', 'id': 1, 'method': 'initialize', 'params': {'protocolVersion': '2025-06-18'}}).encode() + b'\n'
            relay.handle(initialize)
            relay.handle(b'{"jsonrpc":"2.0","method":"notifications/initialized"}\n')
            died = relay.worker.process.pid
            relay.worker.process.kill()
            relay.worker.process.wait()
            sent = relay.handle(line(2, 'ping'))
            self.assertEqual(json.loads(sent[-1])['error']['code'], serve.INTERNAL_ERROR)
            self.assertIsNone(relay.worker)
            sent = relay.handle(line(3, 'tools/list'))
            self.assertEqual(len(sent), 1)
            self.assertGreater(len(json.loads(sent[0])['result']['tools']), 0)
            self.assertNotEqual(relay.worker.process.pid, died)
        finally:
            relay.stop()

    def test_a_worker_that_cannot_start_is_an_error_answered_and_the_next_request_starts_one(self):
        relay = serve.Relay()
        command = serve.worker_command
        try:
            line = lambda number, method: json.dumps({'jsonrpc': '2.0', 'id': number, 'method': method, 'params': {}}).encode() + b'\n'
            initialize = json.dumps({'jsonrpc': '2.0', 'id': 1, 'method': 'initialize', 'params': {'protocolVersion': '2025-06-18'}}).encode() + b'\n'
            relay.handle(initialize)
            relay.handle(b'{"jsonrpc":"2.0","method":"notifications/initialized"}\n')
            relay.worker.process.kill()
            relay.worker.process.wait()
            serve.worker_command = lambda: [sys.executable, '-c', 'import sys; sys.exit(1)']
            sent = relay.handle(line(2, 'ping'))
            self.assertEqual(json.loads(sent[-1])['error']['code'], serve.INTERNAL_ERROR)
            self.assertIsNone(relay.worker)
            sent = relay.handle(line(3, 'ping'))
            self.assertEqual(json.loads(sent[-1])['error']['code'], serve.INTERNAL_ERROR)
            serve.worker_command = command
            sent = relay.handle(line(4, 'tools/list'))
            self.assertEqual(len(sent), 1)
            self.assertGreater(len(json.loads(sent[-1])['result']['tools']), 0)
        finally:
            serve.worker_command = command
            relay.stop()

    def test_a_call_that_outlasts_the_limit_is_answered_with_an_error_and_its_worker_is_killed(self):
        relay = serve.Relay()
        original, command = (serve.CALL_SECONDS, serve.worker_command)
        serve.CALL_SECONDS = 1
        serve.worker_command = lambda: [sys.executable, '-c', 'import sys, time; sys.stdin.readline(); time.sleep(120)']
        try:
            started = time.monotonic()
            sent = relay.handle(json.dumps({'jsonrpc': '2.0', 'id': 1, 'method': 'initialize', 'params': {}}).encode() + b'\n')
            self.assertLess(time.monotonic() - started, 10)
            error = json.loads(sent[-1])['error']
            self.assertEqual(error['code'], serve.INTERNAL_ERROR)
            self.assertIn('1 second', error['message'])
            self.assertIsNone(relay.worker)
        finally:
            serve.CALL_SECONDS, serve.worker_command = (original, command)
            relay.stop()

    def test_a_batch_is_refused_and_not_left_unanswered(self):
        relay = serve.Relay()
        try:
            sent = relay.handle(b'[{"jsonrpc":"2.0","id":1,"method":"ping"}]\n')
            self.assertEqual(json.loads(sent[0])['error']['code'], serve.INVALID_REQUEST)
        finally:
            relay.stop()

class WorkerIsTheProgram(unittest.TestCase):

    def test_the_command_is_the_program_with_the_worker_verb(self) -> None:
        import unittest.mock
        with unittest.mock.patch.object(serve, 'program', return_value=('the-program', 'entry')):
            self.assertEqual(serve.worker_command(), ['the-program', 'entry', 'mcp', 'worker'])

    def test_the_worker_is_started_with_exactly_that_command(self) -> None:
        import unittest.mock
        with unittest.mock.patch.object(serve, 'program', return_value=('the-program', 'entry')), unittest.mock.patch.object(subprocess, 'Popen') as popen:
            popen.return_value.stdout.readline.return_value = b''
            worker = serve.Worker()
        self.assertEqual(popen.call_args[0][0], ['the-program', 'entry', 'mcp', 'worker'])
        worker.reader.join(timeout=5)

    def test_nothing_of_the_checkout_is_named_by_the_module(self) -> None:
        for name in ('BOOT', 'SCRIPTS', 'TOP'):
            self.assertFalse(hasattr(serve, name), name)

class CallsCarryNoState(unittest.TestCase):

    def test_a_scalar_global_is_put_back_and_a_container_is_left(self):
        top = suite_scratch() / f'mcp-globals-{os.getpid()}-{time.time_ns()}'
        top.mkdir(parents=True)
        module_name = f'mcp_globals_probe_{os.getpid()}'
        (top / f'{module_name}.py').write_text('REPORTED = False\nKEPT = {}\n', encoding='utf-8')
        recorded = _call.Globals((module_name,))
        sys.path.insert(0, str(top))
        loaded = _call.SourceFileLoader.exec_module
        try:
            recorded.watch_imports()
            import importlib
            module = importlib.import_module(module_name)
            module.REPORTED = True
            module.KEPT['x'] = 1
            recorded.restore()
            self.assertIs(module.REPORTED, False)
            self.assertEqual(module.KEPT, {'x': 1})
        finally:
            _call.SourceFileLoader.exec_module = loaded
            sys.path.remove(str(top))
            sys.modules.pop(module_name, None)
            remove_tree(top)

    def test_a_module_is_recorded_when_its_name_is_declared_wherever_its_file_is(self):
        import types
        inside, outside = (f'mcp_declared_probe_{os.getpid()}', f'mcp_foreign_probe_{os.getpid()}')
        modules = {name: types.ModuleType(name) for name in (inside, outside)}
        for module in modules.values():
            module.__file__ = str(Path(sys.executable).resolve())
            module.FLAG = False
        recorded = _call.Globals((inside,))
        try:
            sys.modules.update(modules)
            for module in modules.values():
                recorded.record(module)
            self.assertEqual(set(recorded.values), {inside})
            modules[inside].FLAG = True
            modules[outside].FLAG = True
            recorded.restore()
            self.assertIs(modules[inside].FLAG, False)
            self.assertIs(modules[outside].FLAG, True)
        finally:
            for name in modules:
                sys.modules.pop(name, None)

    def test_a_declared_module_without_a_file_is_recorded_too(self):
        import types
        name = f'mcp_fileless_probe_{os.getpid()}'
        module = types.ModuleType(name)
        module.FLAG = False
        recorded = _call.Globals((name,))
        recorded.record(module)
        self.assertEqual(recorded.values, {name: {'FLAG': False}})

class ArgumentsAsTyped(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        router = load_router()
        parser, _ = router.assemble(router.services())
        cls.tools = {tool.name: tool for tool in _tools.tools(parser)}

    def test_switches_values_and_lists(self):
        self.assertEqual(_tools.argv(self.tools['content_find'], {'text': 'a b', 'top': 2, 'no_links': True})[0], ['content', 'find', '--top=2', '--no-links', 'a b'])
        self.assertEqual(_tools.argv(self.tools['content_search'], {'patterns': ['-x', 'y']})[0], ['content', 'search', '--', '-x', 'y'])

    def test_what_does_not_fit_is_refused_by_name(self):
        with self.assertRaisesRegex(_tools.Refused, 'no argument named nothing'):
            _tools.argv(self.tools['content_find'], {'text': 'a', 'nothing': 1})
        with self.assertRaisesRegex(_tools.Refused, 'true or false'):
            _tools.argv(self.tools['content_find'], {'text': 'a', 'no_links': 'yes'})

def _declared_tools():
    import argparse
    parser = argparse.ArgumentParser(prog='declared')
    verbs = parser.add_subparsers(dest='verb')
    reads = verbs.add_parser('reads', help='a verb that reads standard input')
    reads.add_argument('--file', required=True, help='where the text goes')
    reads.add_argument('--content-file', help='the content; standard input when not given')
    names = verbs.add_parser('names', help='a verb that reads nothing')
    names.add_argument('--file', required=True, help='a file')
    return {tool.name: tool for tool in _tools.tools(parser)}

class TextIsTheStandardInput(WithServer):

    def test_the_schemas_of_the_tools_carry_no_stdin(self):
        for tool in self.server.request('tools/list')['tools']:
            with self.subTest(tool=tool['name']):
                self.assertNotIn('stdin', tool['inputSchema']['properties'])

    def test_a_verb_that_reads_standard_input_carries_text_and_no_other(self):
        tools = _declared_tools()
        properties = _tools.definition(tools['reads'])['inputSchema']['properties']
        self.assertEqual(properties['text']['type'], 'string')
        self.assertNotIn('text', _tools.definition(tools['names'])['inputSchema']['properties'])

    def test_argv_hands_text_back_as_the_standard_input(self):
        tool = _declared_tools()['reads']
        words, standard_input = _tools.argv(tool, {'file': 'a.md', 'text': 'body'})
        self.assertEqual(standard_input, 'body')
        self.assertNotIn('body', words)
        with self.assertRaisesRegex(_tools.Refused, 'no argument named stdin'):
            _tools.argv(tool, {'file': 'a.md', 'stdin': 'body'})
        with self.assertRaisesRegex(_tools.Refused, 'no argument named text'):
            _tools.argv(_declared_tools()['names'], {'file': 'a.md', 'text': 'body'})
if __name__ == '__main__':
    unittest.main()
