#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""resident/services/serve.py — `memar resident serve`: the resident process, which answers the command's calls over a local socket.

**What it is.** Workers of `memar mcp serve` (`mcp/services/_worker.py`) behind a socket on 127.0.0.1 instead of an agent
app's stdio: each worker holds Memar loaded and runs a call through the router's own `main` as the command would. The
process itself loads none of that, so it is small. The command's side, `machine/resident.py`, says when a call is handed
to it and when it is not; `_pool.py` says how calls overlap, in workers of their own.

**One process a checkout.** It writes `temp/resident/state.json` (port, token, process id) once it listens, and
removes it when it ends; one that finds a live process behind an existing state file ends at once. The token is
made at start and is sent back by every client; a request without it is refused and nothing runs.

**Every connection has a thread**, so a slow call, a silent connection or a stuck worker holds only its own. A call that
finds no worker free within a few seconds is refused as busy, and the command does it in its own process. **It ends**
after `IDLE_SECONDS` without a call (`MEMAR_SERVER_IDLE` sets another, in seconds), when asked to by `memar resident
stop`, or when its state file is gone or names another process. `MEMAR_SERVER_WORKERS` sets the most workers (4).
"""
from __future__ import annotations

import argparse
import hmac
import json
import os
import secrets
import socket
import sys
import threading
import time
from pathlib import Path

from machine.resident import STATE, ask, folder, read_line, state_of
from resident.services._pool import Pool

COMMAND = "serve"
SCRIPTS = Path(__file__).resolve().parents[2]
TOP = SCRIPTS.parent.parent
IDLE_SECONDS = 30 * 60
IDLE_ENV = "MEMAR_SERVER_IDLE"
WORKERS = 4
WORKERS_ENV = "MEMAR_SERVER_WORKERS"
# How often a waiting process looks at its state file, its idle workers and the clock.
TICK_SECONDS = 2.0
RUN = "memar/run"
SLOW_LOG = "slow.log"
SLOW_SECONDS = 5.0
# How long a connection may take to send its request.
REQUEST_SECONDS = 30
# How long the process waits for calls in progress when it ends.
FINISH_SECONDS = 10


def describe(verbs):
    verbs.add_parser(
        COMMAND,
        help="run the resident process in this terminal until it ends",
        description=(
            "Run the resident process: listen on 127.0.0.1, answer the `memar` command's calls, end after\n"
            "a while without one (MEMAR_SERVER_IDLE seconds, 1800 by default) or on `memar resident stop`.\n"
            "A call starts it by itself, detached, unless MEMAR_SERVER=0; a person runs this to watch it."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    return run


def write_state(top: Path, port: int, token: str) -> Path:
    path = folder(top) / STATE
    path.parent.mkdir(parents=True, exist_ok=True)
    scratch = path.with_suffix(f".{os.getpid()}.tmp")
    scratch.write_text(json.dumps({"pid": os.getpid(), "port": port, "token": token, "started": time.time()}), encoding="utf-8")
    os.replace(scratch, path)
    return path


def gone(connection) -> bool:
    """Whether the other side has closed CONNECTION, as a call that gave up waiting has: nothing more to read, end of stream."""
    import select

    readable, _, _ = select.select([connection], [], [], 0)
    if not readable:
        return False
    try:
        return connection.recv(1, socket.MSG_PEEK) == b""
    except OSError:
        return True


def ours(top: Path, token: str) -> bool:
    state = state_of(top)
    return state is not None and state.get("token") == token


def sent(connection, message: dict) -> None:
    connection.sendall(json.dumps(message, ensure_ascii=False).encode("utf-8") + b"\n")


class Resident:
    def __init__(self, top: Path = TOP, scripts: Path = SCRIPTS, workers: int = WORKERS) -> None:
        self.top = top
        self.pool = Pool(top, scripts, workers)
        self.token = secrets.token_hex(16)
        self.stopping = False
        self.answered = 0
        self.active = 0
        self.last = time.monotonic()
        self.guard = threading.Lock()

    def run(self, worker, call: dict) -> dict:
        """The answer to one call's fields (argv, cwd, env, stdin) run by WORKER."""
        with self.guard:
            self.answered += 1
            identity = self.answered
        params = {key: call[key] for key in ("argv", "cwd", "env", "stdin") if key in call}
        request = {"jsonrpc": "2.0", "id": identity, "method": RUN, "params": params}
        line = self.pool.ask(worker, json.dumps(request, ensure_ascii=False).encode("utf-8"))
        if line is None:
            return {"failed": "the worker stopped before it answered"}
        answer = json.loads(line)
        if "result" in answer:
            return answer["result"]
        return {"failed": answer.get("error", {}).get("message", "the worker failed")}

    def handle(self, connection) -> None:
        """One connection: a request line, then its answer; each call with a worker to itself."""
        with self.guard:
            self.active += 1
        try:
            with connection:
                connection.settimeout(REQUEST_SECONDS)
                try:
                    self.converse(connection)
                except OSError:
                    pass
        finally:
            with self.guard:
                self.active -= 1
                self.last = time.monotonic()

    def converse(self, connection) -> None:
        line = read_line(connection)
        try:
            call = json.loads(line)
        except ValueError:
            call = None
        if not isinstance(call, dict) or not hmac.compare_digest(str(call.get("token", "")), self.token):
            sent(connection, {"refused": "not allowed"})
            return
        if call.get("ping"):
            sent(connection, {"pid": os.getpid(), "calls": self.answered, "workers": self.pool.live})
            return
        if call.get("stop"):
            self.stopping = True
            sent(connection, {"stopped": True})
            return
        if not isinstance(call.get("argv"), list):
            sent(connection, {"refused": "argv is a list"})
            return
        if gone(connection):
            return
        taken = self.pool.acquire()
        if taken is None:
            sent(connection, {"refused": "busy"})
            return
        worker, generation = taken
        healthy = False
        try:
            if gone(connection):
                healthy = True
                return
            connection.settimeout(None)
            sent(connection, {"taken": True})
            started = time.monotonic()
            answer = self.run(worker, call)
            healthy = "failed" not in answer
            sent(connection, answer)
            spent = time.monotonic() - started
            if spent > SLOW_SECONDS:
                self.note(f"{spent:.1f}s for {call.get('argv')!r}")
        finally:
            self.pool.release(worker, generation, healthy)

    def note(self, message: str) -> None:
        """A line in `slow.log` beside the state file, for the next person who wonders why a call took long."""
        try:
            with self.guard, (folder(self.top) / SLOW_LOG).open("a", encoding="utf-8") as log:
                log.write(f"{time.strftime('%Y-%m-%dT%H:%M:%S')} {message}\n")
        except OSError:
            pass

    def serve(self, idle: float) -> None:
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.bind(("127.0.0.1", 0))
        listener.listen(64)
        listener.settimeout(TICK_SECONDS)
        write_state(self.top, listener.getsockname()[1], self.token)
        threading.Thread(target=self.pool.warm, daemon=True).start()
        try:
            while not self.stopping:
                try:
                    connection, _ = listener.accept()
                except socket.timeout:
                    self.pool.reap()
                    with self.guard:
                        quiet = self.active == 0 and time.monotonic() - self.last > idle
                    if quiet or not ours(self.top, self.token):
                        return
                    continue
                threading.Thread(target=self.handle, args=(connection,), daemon=True).start()
        finally:
            listener.close()
            end = time.monotonic() + FINISH_SECONDS
            while self.active and time.monotonic() < end:
                time.sleep(0.05)
            self.pool.close()
            if ours(self.top, self.token):
                try:
                    (folder(self.top) / STATE).unlink()
                except OSError:
                    pass


def serve_forever() -> int:
    """The process: what `memar resident serve` runs, and what the command starts without the router."""
    if ask(TOP, {"ping": True}) is not None:
        print("memar: a resident process is already running.", file=sys.stderr)
        return 0
    try:
        idle = float(os.environ.get(IDLE_ENV, IDLE_SECONDS))
    except ValueError:
        idle = IDLE_SECONDS
    try:
        workers = int(os.environ.get(WORKERS_ENV, WORKERS))
    except ValueError:
        workers = WORKERS
    Resident(workers=workers).serve(idle)
    return 0


def run(args: argparse.Namespace) -> int:
    return serve_forever()
