#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
import argparse
import json
import sys
from importlib import import_module
_m_memar_location = import_module('bundles.memar.services.location.memar_location')
program = _m_memar_location.program
COMMAND = 'serve'
WORKER_VERB = ('mcp', 'worker')
INITIALIZE = 'initialize'
INITIALIZED = 'notifications/initialized'
PARSE_ERROR = -32700
INVALID_REQUEST = -32600
INTERNAL_ERROR = -32603
STOP_SECONDS = 5
CALL_SECONDS = 10

def describe(verbs):
    verbs.add_parser(COMMAND, help='run the MCP server on stdin and stdout, for an agent app to start', description="Run the MCP server: read JSON-RPC from stdin and answer on stdout, one message a line,\nuntil stdin closes. An agent app starts it; a person does not type it. Each tool is one\nverb of `memar`, named by its words joined with `_`, and answers what that verb prints:\nits stdout, its stderr when it wrote any, and its exit status. Edits to documents\nare seen on the next call; Memar's own code is the code it started with until `memar update`.", formatter_class=argparse.RawDescriptionHelpFormatter)
    return run

def worker_command() -> list[str]:
    return [*program(), *WORKER_VERB]

def encode(message: dict) -> bytes:
    return json.dumps(message, ensure_ascii=False, separators=(',', ':')).encode('utf-8') + b'\n'

def failure(identity, code: int, message: str) -> bytes:
    return encode({'jsonrpc': '2.0', 'id': identity, 'error': {'code': code, 'message': message}})

class Worker:
    """One worker process, spoken to a line at a time."""

    def __init__(self) -> None:
        import queue
        import subprocess
        import threading
        self.process = subprocess.Popen(worker_command(), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        self.answers: queue.Queue = queue.Queue()
        self.timed_out = False
        self.reader = threading.Thread(target=self._read, daemon=True)
        self.reader.start()

    def _read(self) -> None:
        try:
            for line in iter(self.process.stdout.readline, b''):
                self.answers.put(line)
        except (OSError, ValueError):
            pass
        self.answers.put(None)

    def send(self, line: bytes) -> None:
        self.process.stdin.write(line if line.endswith(b'\n') else line + b'\n')
        self.process.stdin.flush()

    def ask(self, line: bytes) -> bytes | None:
        import queue
        try:
            self.send(line)
            answer = self.answers.get(timeout=CALL_SECONDS)
        except OSError:
            return None
        except queue.Empty:
            self.timed_out = True
            self.process.kill()
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
        self.reader.join(timeout=STOP_SECONDS)
        self.process.stdout.close()

class Relay:
    """The app's side of the conversation, kept so a new worker can be brought to where the old one was."""

    def __init__(self) -> None:
        self.worker: Worker | None = None
        self.initialize: bytes | None = None
        self.initialized: bytes | None = None
        self.limit_hit = False

    def current(self) -> Worker | None:
        if self.worker is not None:
            return self.worker
        self.worker = Worker()
        try:
            if self.initialize is not None:
                if self.worker.ask(self.initialize) is None:
                    raise OSError('the worker stopped while it started')
                if self.initialized is not None:
                    self.worker.send(self.initialized)
        except OSError:
            self.limit_hit = self.limit_hit or self.worker.timed_out
            self.worker.stop()
            self.worker = None
        return self.worker

    def handle(self, line: bytes) -> list[bytes]:
        try:
            message = json.loads(line)
        except ValueError:
            return [failure(None, PARSE_ERROR, 'not a JSON-RPC message')]
        if isinstance(message, list):
            return [failure(None, INVALID_REQUEST, 'a batch is not answered; send one message a line')]
        method = message.get('method') if isinstance(message, dict) else None
        if method is None:
            return []
        worker = self.current() if 'id' in message or self.worker is None else self.worker
        if method == INITIALIZE:
            self.initialize, self.initialized = (line, None)
        if method == INITIALIZED:
            self.initialized = line
        answer = None
        if worker is not None:
            if 'id' not in message:
                try:
                    worker.send(line)
                except OSError:
                    self.worker = None
                return []
            answer = worker.ask(line)
            self.limit_hit = self.limit_hit or worker.timed_out
            if answer is None:
                worker.stop()
        if answer is None:
            self.worker = None
            if 'id' not in message:
                return []
            hit, self.limit_hit = (self.limit_hit, False)
            reason = f'the call took longer than {CALL_SECONDS} second{"" if CALL_SECONDS == 1 else "s"} and its worker was killed' if hit else 'the worker stopped'
            return [failure(message['id'], INTERNAL_ERROR, f'{reason}; it is started again on the next message')]
        return [answer]

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
