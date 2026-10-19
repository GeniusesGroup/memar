#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for `memar mcp serve`, the MCP server over stdio.

    python .agents/scripts/mcp/tests/serve.py

The subject is the server `mcp/services/serve.py` starts, with the worker and its parts beside it,
named for the file that holds the verb per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md). Its defining
documents are the verb's own help and the entry of
[Memar Handoff](../../../../bundles/memar/memar.handoff.md#the-mcp-adapter-is-the-servers-first-face-owner-2026-10-18)
that records what the owner chose; the expectations below are theirs.

Each test that talks to the server starts one, as an agent app does, and speaks MCP to it over its
stdin and stdout. Every child is a test run, so the daily update's hook does nothing in it or in the
CLI it is compared with.

What is pinned:

  AnswersAsTheCli       Each tool's answer — its stdout, its stderr, its exit status — is byte for
                        byte what `memar` prints for the same arguments, for `content search`,
                        `content find`, `content section`, `session list` and `commands`, a refusal
                        by the verb and a refusal by the parser among them.
  ToolsAreTheVerbs      `tools/list` holds one tool per leaf verb `memar --help` reaches, and no
                        tool for `mcp` itself.
  SeesEditsWithoutRestart
                        A document edited, added, and deleted between two calls of one server is
                        seen by the next call, and the tools are never said to have changed; an
                        edit that leaves the file's size and modification time as they were is seen
                        too, when the file was read within two seconds of its modification.
  CodeChangeReplacesWorker
                        When the code fingerprint changes, the next request is answered by a new
                        worker, which the app is told of by `notifications/tools/list_changed`,
                        and the conversation goes on without a new `initialize`; a worker that
                        dies while it starts (code broken mid-edit) is answered for with an error
                        and the next request starts one; a batch is refused, not left waiting; the
                        fingerprint changes when a file of the code is added or changed.
  CallsCarryNoState     A module global a call changed is as its import left it at the next call.
  ArgumentsAsTyped      A call's arguments become the words the CLI would be typed with.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import unittest
from pathlib import Path

TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parents[1]
TOP = SCRIPTS.parent.parent
for folder in (TOP, SCRIPTS):
    if str(folder) not in sys.path:
        sys.path.insert(0, str(folder))
sys.dont_write_bytecode = True

from machine.fs_test_scratch import remove_tree, suite_scratch
from mcp.services import _call, _tools, serve

ROUTER = SCRIPTS / "memar"
THIS_SESSION = "20261019-T111413Z-21136"


def cli(argv: list[str], stdin: str = "") -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(ROUTER), *argv], input=stdin.encode("utf-8"), capture_output=True)


class Server:
    """One server, spoken to as an agent app speaks to it."""

    def __init__(self) -> None:
        self.process = subprocess.Popen([sys.executable, str(ROUTER), "mcp", "serve"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        self.number = 0
        self.notices: list[dict] = []
        self.request("initialize", {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "test", "version": "0"}})
        self.notify("notifications/initialized")

    def _write(self, message: dict) -> None:
        self.process.stdin.write(json.dumps(message).encode("utf-8") + b"\n")
        self.process.stdin.flush()

    def notify(self, method: str) -> None:
        self._write({"jsonrpc": "2.0", "method": method})

    def request(self, method: str, params: dict | None = None) -> dict:
        self.number += 1
        self._write({"jsonrpc": "2.0", "id": self.number, "method": method, "params": params or {}})
        while True:
            line = self.process.stdout.readline()
            if not line:
                raise AssertionError("the server stopped")
            message = json.loads(line)
            if "id" not in message:
                self.notices.append(message)
                continue
            assert message["id"] == self.number, message
            if "error" in message:
                raise AssertionError(message["error"])
            return message["result"]

    def call(self, name: str, arguments: dict) -> tuple[bytes, bytes, int]:
        result = self.request("tools/call", {"name": name, "arguments": arguments})
        texts = [item["text"] for item in result["content"]]
        stdout, stderr = texts[0], (texts[1] if len(texts) > 1 else "")
        status = result["_meta"]["memar/status"]
        assert result["isError"] == (status != 0), result
        return stdout.encode("utf-8"), stderr.encode("utf-8"), status

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
    CASES = (
        ("content_search", {"patterns": ["guest adapter"]}, ["content", "search", "guest adapter"]),
        ("content_find", {"text": "mcp guest adapter", "top": 3}, ["content", "find", "mcp guest adapter", "--top", "3"]),
        ("content_find", {"text": "server stdio", "no_links": True}, ["content", "find", "--no-links", "server stdio"]),
        ("content_find", {"text": "anything", "top": 0}, ["content", "find", "anything", "--top", "0"]),
        ("content_find", {"top": 2}, ["content", "find", "--top", "2"]),
        ("content_section", {"file": "modules/net/srpc/srpc.md", "heading": "Abstract"}, ["content", "section", "modules/net/srpc/srpc.md", "Abstract"]),
        ("content_section", {"file": "modules/net/srpc/srpc.md", "heading": "#abstract", "hash": True}, ["content", "section", "--hash", "modules/net/srpc/srpc.md", "#abstract"]),
        ("content_section", {"file": "modules/net/srpc/srpc.md", "heading": "No Such Heading"}, ["content", "section", "modules/net/srpc/srpc.md", "No Such Heading"]),
        ("session_list", {"text": THIS_SESSION}, ["session", "list", THIS_SESSION]),
        ("commands", {}, ["commands"]),
    )

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

        from mcp.services._worker import _load_router

        router = _load_router(SCRIPTS)
        parser, _ = router.assemble(router.services())

        def leaves(parser, words):
            verbs = [action for action in parser._actions if isinstance(action, argparse._SubParsersAction)]
            if not verbs:
                return {" ".join(words)}
            return set().union(*(leaves(child, [*words, word]) for word, child in verbs[0].choices.items()))

        verbs = leaves(parser, [])
        self.assertIn("mcp serve", verbs)
        names = {tool["name"] for tool in self.server.request("tools/list")["tools"]}
        self.assertEqual(names, {verb.replace(" ", "_") for verb in verbs if not verb.startswith("mcp ")})

    def test_each_tool_takes_what_its_verb_takes(self):
        tools = {tool["name"]: tool for tool in self.server.request("tools/list")["tools"]}
        find = tools["content_find"]["inputSchema"]
        self.assertEqual(find["required"], ["text"])
        self.assertEqual(find["properties"]["top"]["type"], "integer")
        self.assertEqual(find["properties"]["no_links"]["type"], "boolean")
        self.assertIn("stdin", find["properties"])
        self.assertIn("rank the sections", tools["content_find"]["description"])


class SeesEditsWithoutRestart(unittest.TestCase):
    def setUp(self) -> None:
        self.project = suite_scratch() / f"mcp-serve-{os.getpid()}-{time.time_ns()}"
        (self.project / "docs").mkdir(parents=True)
        self.first = self.project / "docs" / "first.md"
        self.first.write_text("# First\nzanzibar is the word of this document.\n", encoding="utf-8", newline="\n")
        self.server = Server()

    def tearDown(self) -> None:
        self.server.close()
        remove_tree(self.project)

    def found(self, word: str) -> str:
        stdout, _, _ = self.server.call("content_find", {"text": word, "project_path": str(self.project), "no_links": True})
        return stdout.decode("utf-8")

    def test_an_edit_an_addition_and_a_deletion_are_each_seen_by_the_next_call(self):
        self.assertIn("docs/first.md#first", self.found("zanzibar"))
        self.first.write_text("# First\nkilimanjaro took its place, and the text is longer now.\n", encoding="utf-8", newline="\n")
        self.assertNotIn("first.md", self.found("zanzibar"))
        self.assertIn("docs/first.md#first", self.found("kilimanjaro"))
        second = self.project / "docs" / "second.md"
        second.write_text("# Second\nserengeti only here.\n", encoding="utf-8", newline="\n")
        self.assertIn("docs/second.md#second", self.found("serengeti"))
        second.unlink()
        self.assertNotIn("second.md", self.found("serengeti"))
        self.assertEqual(self.server.notices, [])

    def test_an_edit_that_keeps_size_and_time_is_seen_while_the_file_is_fresh(self):
        self.assertIn("docs/first.md#first", self.found("zanzibar"))
        before = self.first.stat()
        self.first.write_text("# First\ntanzania is the word of this document.\n", encoding="utf-8", newline="\n")
        os.utime(self.first, ns=(before.st_atime_ns, before.st_mtime_ns))
        self.assertEqual(self.first.stat().st_size, before.st_size)
        self.assertIn("docs/first.md#first", self.found("tanzania"))
        self.assertNotIn("first.md", self.found("zanzibar"))


class CodeChangeReplacesWorker(unittest.TestCase):
    def test_a_changed_fingerprint_brings_a_new_worker_and_a_notice(self):
        relay = serve.Relay()
        codes = iter([("one",), ("one",), ("two",)])
        original = serve.fingerprint
        serve.fingerprint = lambda top=serve.TOP: next(codes)
        try:
            line = lambda number, method: json.dumps({"jsonrpc": "2.0", "id": number, "method": method, "params": {}}).encode() + b"\n"
            initialize = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18"}}).encode() + b"\n"
            self.assertEqual(len(relay.handle(initialize)), 1)
            relay.handle(b'{"jsonrpc":"2.0","method":"notifications/initialized"}\n')
            first = relay.worker
            self.assertEqual(len(relay.handle(line(2, "ping"))), 1)
            self.assertIs(relay.worker, first)
            sent = relay.handle(line(3, "tools/list"))
            self.assertIsNot(relay.worker, first)
            self.assertEqual(json.loads(sent[0]), serve.LIST_CHANGED)
            self.assertEqual(len(json.loads(sent[1])["result"]["tools"]) > 0, True)
        finally:
            serve.fingerprint = original
            relay.stop()

    def test_a_worker_that_cannot_start_is_an_error_answered_and_the_next_request_starts_one(self):
        relay = serve.Relay()
        codes = iter([("one",), ("two",), ("two",), ("three",)])
        original, boot = serve.fingerprint, serve.BOOT
        serve.fingerprint = lambda top=serve.TOP: next(codes)
        try:
            line = lambda number, method: json.dumps({"jsonrpc": "2.0", "id": number, "method": method, "params": {}}).encode() + b"\n"
            initialize = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18"}}).encode() + b"\n"
            relay.handle(initialize)
            relay.handle(b'{"jsonrpc":"2.0","method":"notifications/initialized"}\n')
            # The code as it is mid-edit: a worker made of it dies while it loads.
            serve.BOOT = "import sys; sys.exit(1)"
            sent = relay.handle(line(2, "ping"))
            self.assertEqual(json.loads(sent[-1])["error"]["code"], serve.INTERNAL_ERROR)
            self.assertIsNone(relay.worker)
            sent = relay.handle(line(3, "ping"))
            self.assertEqual(json.loads(sent[-1])["error"]["code"], serve.INTERNAL_ERROR)
            serve.BOOT = boot
            sent = relay.handle(line(4, "tools/list"))
            self.assertEqual(json.loads(sent[0]), serve.LIST_CHANGED)
            self.assertGreater(len(json.loads(sent[-1])["result"]["tools"]), 0)
        finally:
            serve.fingerprint, serve.BOOT = original, boot
            relay.stop()

    def test_a_batch_is_refused_and_not_left_unanswered(self):
        relay = serve.Relay()
        try:
            sent = relay.handle(b'[{"jsonrpc":"2.0","id":1,"method":"ping"}]\n')
            self.assertEqual(json.loads(sent[0])["error"]["code"], serve.INVALID_REQUEST)
        finally:
            relay.stop()

    def test_the_fingerprint_changes_when_code_is_added_or_changed(self):
        top = suite_scratch() / f"mcp-fingerprint-{os.getpid()}-{time.time_ns()}"
        try:
            (top / "modules" / "one").mkdir(parents=True)
            (top / "modules" / "one" / "docs").mkdir()
            code = top / "modules" / "one" / "one.py"
            code.write_text("A = 1\n", encoding="utf-8")
            first = serve.fingerprint(top)
            (top / "modules" / "one" / "docs" / "note.py").write_text("", encoding="utf-8")
            self.assertEqual(serve.fingerprint(top), first)
            (top / "modules" / "one" / "two.py").write_text("", encoding="utf-8")
            second = serve.fingerprint(top)
            self.assertNotEqual(second, first)
            code.write_text("A = 22\n", encoding="utf-8")
            self.assertNotEqual(serve.fingerprint(top), second)
        finally:
            remove_tree(top)


class CallsCarryNoState(unittest.TestCase):
    def test_a_scalar_global_is_put_back_and_a_container_is_left(self):
        top = suite_scratch() / f"mcp-globals-{os.getpid()}-{time.time_ns()}"
        top.mkdir(parents=True)
        module_name = f"mcp_globals_probe_{os.getpid()}"
        (top / f"{module_name}.py").write_text("REPORTED = False\nKEPT = {}\n", encoding="utf-8")
        recorded = _call.Globals(top)
        sys.path.insert(0, str(top))
        loaded = _call.SourceFileLoader.exec_module
        try:
            recorded.watch_imports()
            import importlib

            module = importlib.import_module(module_name)
            module.REPORTED = True
            module.KEPT["x"] = 1
            recorded.restore()
            self.assertIs(module.REPORTED, False)
            self.assertEqual(module.KEPT, {"x": 1})
        finally:
            _call.SourceFileLoader.exec_module = loaded
            sys.path.remove(str(top))
            sys.modules.pop(module_name, None)
            remove_tree(top)


class ArgumentsAsTyped(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        from mcp.services._worker import _load_router

        router = _load_router(SCRIPTS)
        parser, _ = router.assemble(router.services())
        cls.tools = {tool.name: tool for tool in _tools.tools(parser)}

    def test_switches_values_and_lists(self):
        self.assertEqual(
            _tools.argv(self.tools["content_find"], {"text": "a b", "top": 2, "no_links": True})[0],
            ["content", "find", "--top=2", "--no-links", "a b"],
        )
        self.assertEqual(
            _tools.argv(self.tools["content_search"], {"patterns": ["-x", "y"]})[0],
            ["content", "search", "--", "-x", "y"],
        )

    def test_what_does_not_fit_is_refused_by_name(self):
        with self.assertRaisesRegex(_tools.Refused, "no argument named nothing"):
            _tools.argv(self.tools["content_find"], {"text": "a", "nothing": 1})
        with self.assertRaisesRegex(_tools.Refused, "true or false"):
            _tools.argv(self.tools["content_find"], {"text": "a", "no_links": "yes"})


if __name__ == "__main__":
    unittest.main()
