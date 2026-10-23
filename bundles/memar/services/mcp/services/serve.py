#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""mcp/services/serve.py — `memar mcp serve`: the MCP server on stdio, a relay to a worker that is replaced when Memar's code changes.

**Why two processes.** An agent app starts this once per conversation and keeps it, so it lives
across edits to the services it runs: a pull, a checkout or a task's own change to a script.
A process that imported those services cannot unimport them, so the services live in a worker
(`_worker.py` beside this file), and this file holds nothing a verb is made of. Before it hands a
message on, it compares a fingerprint of the Python the router reads; when it differs, the worker is
stopped and a new one started, which is given the app's `initialize` again, and the app is told the
tools changed, since a changed service may declare different ones. This file is in the fingerprint
too, but a change to it reaches the app only when the app starts the server again.

**What passes through.** MCP's stdio transport: one JSON-RPC message per line, each way. Every
request is answered by the worker before the next is read, in order; a notification is handed on and
not answered. A worker that stops mid-call is answered for with an error and started again on the
next message.

Content edits need no restart: the worker checks the files it keeps on every call (`index.py`'s
`keep`), and every other verb reads its files as the CLI does.
"""
from __future__ import annotations
import argparse
import json
import os
import sys
from pathlib import Path
COMMAND = 'serve'
SCRIPTS = Path(__file__).resolve().parents[3]
TOP = SCRIPTS.parent.parent
CODE_ROOTS = ('modules', 'modules-plugable', 'bundles')
ROUTER = 'memar'
NOT_CODE = {'node_modules', '__pycache__', 'temp', 'tests', 'docs', 'rules', 'protocol', 'errors'}
BOOT = 'import sys; from pathlib import Path; s, t = Path(sys.argv[1]), Path(sys.argv[2]); sys.path[0:0] = [str(t), str(s), str(s / "services")]; from mcp.services._worker import main; main(str(s), str(t))'
INITIALIZE = 'initialize'
INITIALIZED = 'notifications/initialized'
LIST_CHANGED = {'jsonrpc': '2.0', 'method': 'notifications/tools/list_changed'}
PARSE_ERROR = -32700
INVALID_REQUEST = -32600
INTERNAL_ERROR = -32603
STOP_SECONDS = 5

def describe(verbs):
    verbs.add_parser(COMMAND, help='run the MCP server on stdin and stdout, for an agent app to start', description="Run the MCP server: read JSON-RPC from stdin and answer on stdout, one message a line,\nuntil stdin closes. An agent app starts it; a person does not type it. Each tool is one\nverb of `memar`, named by its words joined with `_`, and answers what that verb prints:\nits stdout, its stderr when it wrote any, and its exit status. Edits to documents and\nto Memar's own code are seen on the next call, without starting it again.", formatter_class=argparse.RawDescriptionHelpFormatter)
    return run

def fingerprint(top: Path=TOP) -> tuple[tuple[str, int, int], ...]:
    """Every file of the worker's code with its size and modification time, in a fixed order."""
    found = []
    for root in CODE_ROOTS:
        for folder, dirs, files in os.walk(top / root):
            dirs[:] = [name for name in dirs if name not in NOT_CODE]
            for name in files:
                if not (name.endswith('.py') or name == ROUTER):
                    continue
                path = os.path.join(folder, name)
                try:
                    status = os.stat(path)
                except OSError:
                    continue
                found.append((path, status.st_size, status.st_mtime_ns))
    return tuple(sorted(found))

def encode(message: dict) -> bytes:
    return json.dumps(message, ensure_ascii=False, separators=(',', ':')).encode('utf-8') + b'\n'

def failure(identity, code: int, message: str) -> bytes:
    return encode({'jsonrpc': '2.0', 'id': identity, 'error': {'code': code, 'message': message}})

class Worker:
    """One worker process, spoken to a line at a time."""

    def __init__(self, top: Path, scripts: Path) -> None:
        import subprocess
        self.process = subprocess.Popen([sys.executable, '-c', BOOT, str(scripts), str(top)], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    def send(self, line: bytes) -> None:
        self.process.stdin.write(line if line.endswith(b'\n') else line + b'\n')
        self.process.stdin.flush()

    def ask(self, line: bytes) -> bytes | None:
        """LINE's answer, or None when the worker stopped before giving one."""
        try:
            self.send(line)
            answer = self.process.stdout.readline()
        except OSError:
            return None
        return answer or None

    def stop(self) -> None:
        import subprocess
        try:
            self.process.stdin.close()
            self.process.wait(timeout=STOP_SECONDS)
        except (OSError, subprocess.TimeoutExpired):
            self.process.kill()
            self.process.wait()
        self.process.stdout.close()

class Relay:
    """The app's side of the conversation, kept so a new worker can be brought to where the old one was."""

    def __init__(self, top: Path=TOP, scripts: Path=SCRIPTS) -> None:
        self.top = top
        self.scripts = scripts
        self.worker: Worker | None = None
        self.code: tuple = ()
        self.initialize: bytes | None = None
        self.initialized: bytes | None = None

    def current(self) -> tuple[Worker | None, bool]:
        """The worker for the code as it is now, and whether it replaced one; None when a new one could not be started.

        Code being edited is often broken for a moment, and a worker made of it dies while it loads. That is the
        worker's failure and not the relay's: the request is answered with an error, and the next one starts a
        worker again, whether or not the code changed meanwhile.
        """
        code = fingerprint(self.top)
        if self.worker is not None and code == self.code:
            return (self.worker, False)
        replaced = self.worker is not None or bool(self.code)
        if self.worker is not None:
            self.worker.stop()
        self.worker, self.code = (Worker(self.top, self.scripts), code)
        try:
            if self.initialize is not None:
                if self.worker.ask(self.initialize) is None:
                    raise OSError('the worker stopped while it started')
                if self.initialized is not None:
                    self.worker.send(self.initialized)
        except OSError:
            self.worker.stop()
            self.worker = None
        return (self.worker, replaced)

    def handle(self, line: bytes) -> list[bytes]:
        """What the app is sent for LINE: a notice that the tools changed, when they may have, then the answer, if any."""
        try:
            message = json.loads(line)
        except ValueError:
            return [failure(None, PARSE_ERROR, 'not a JSON-RPC message')]
        if isinstance(message, list):
            return [failure(None, INVALID_REQUEST, 'a batch is not answered; send one message a line')]
        method = message.get('method') if isinstance(message, dict) else None
        if method is None:
            return []
        sent: list[bytes] = []
        worker, replaced = self.current() if 'id' in message or self.worker is None else (self.worker, False)
        if method == INITIALIZE:
            self.initialize, self.initialized = (line, None)
        elif replaced and self.initialized is not None and (worker is not None):
            sent.append(encode(LIST_CHANGED))
        if method == INITIALIZED:
            self.initialized = line
        answer = None
        if worker is not None:
            if 'id' not in message:
                try:
                    worker.send(line)
                except OSError:
                    self.worker = None
                return sent
            answer = worker.ask(line)
        if answer is None:
            self.worker = None
            if 'id' not in message:
                return sent
            return sent + [failure(message['id'], INTERNAL_ERROR, 'the worker stopped; it is started again on the next message')]
        return sent + [answer]

    def stop(self) -> None:
        if self.worker is not None:
            self.worker.stop()

def run(args: argparse.Namespace) -> int:
    incoming, outgoing = (sys.stdin.buffer, sys.stdout.buffer)
    relay = Relay()
    try:
        for line in iter(incoming.readline, b''):
            if not line.strip():
                continue
            for answer in relay.handle(line):
                outgoing.write(answer)
                outgoing.flush()
    finally:
        relay.stop()
    return 0
