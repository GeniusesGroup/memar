#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""resident/services/_pool.py — the workers the resident process runs calls in, one call to a worker, several workers at once.

**Why processes.** A worker (`mcp/services/_worker.py`) runs a verb as the command would: it captures the verb's output at the
process's file descriptors and takes the caller's folder and environment for the call. Those are the process's own and one
at a time, so two calls in one worker would write into each other's output, folder and environment. A call therefore has
a worker to itself for its length, and calls that overlap have workers of their own, each its own process: no memory is
shared between calls, so no call can corrupt another's. What overlapping calls share is the files, which they share when the
command is typed in two terminals as well, and the verbs that write take their per-file locks as they always did.

**How many.** At most `most` workers, started when a call finds none idle and ended when they have been idle
`WORKER_IDLE_SECONDS`, except one. A call that finds all busy waits `wait` seconds and is then refused as busy, which
sends the command to do it in its own process: a wait is never longer than that, so a slow call delays no one by more than it.

**When the code changes.** The fingerprint of the Python under the checkout is looked at at most once in `check_every` seconds. When it
differs, the generation number goes up: idle workers end, busy ones end when their call does, and the next call gets
a worker made of the code as it is.
"""
from __future__ import annotations

import threading
import time
from pathlib import Path

from mcp.services.serve import Worker, fingerprint

WORKER_IDLE_SECONDS = 300.0


class Pool:
    def __init__(self, top: Path, scripts: Path, most: int, check_every: float = 1.0, wait: float = 4.0) -> None:
        self.top = top
        self.scripts = scripts
        self.most = max(1, most)
        self.check_every = check_every
        self.wait = wait
        self.condition = threading.Condition()
        self.looking = threading.Lock()
        self.idle: list[tuple[Worker, float]] = []
        self.live = 0
        self.generation = 0
        self.code: tuple | None = None
        self.checked = 0.0
        self.closed = False
        self.asked = 0

    def generation_now(self) -> int:
        """The generation of the code as it is, looking at the fingerprint at most once in `check_every` seconds."""
        with self.looking:
            if self.code is None or time.monotonic() - self.checked >= self.check_every:
                code = fingerprint(self.top)
                self.checked = time.monotonic()
                if self.code is not None and code != self.code:
                    with self.condition:
                        self.generation += 1
                        stale, self.idle = self.idle, []
                    for worker, _ in stale:
                        self._end(worker)
                self.code = code
            return self.generation

    def acquire(self) -> tuple[Worker, int] | None:
        """A worker for one call, and the generation it was taken in; None when all are busy for longer than `wait`."""
        generation = self.generation_now()
        deadline = time.monotonic() + self.wait
        with self.condition:
            while True:
                if self.closed:
                    return None
                if self.idle:
                    return self.idle.pop()[0], generation
                if self.live < self.most:
                    self.live += 1
                    break
                left = deadline - time.monotonic()
                if left <= 0:
                    return None
                self.condition.wait(left)
        try:
            return Worker(self.top, self.scripts), generation
        except OSError:
            with self.condition:
                self.live -= 1
                self.condition.notify()
            return None

    def release(self, worker: Worker, generation: int, healthy: bool) -> None:
        """Give WORKER back after its call: kept idle if it is sound and of the code as it is now, else ended."""
        with self.condition:
            if healthy and not self.closed and generation == self.generation:
                self.idle.append((worker, time.monotonic()))
                self.condition.notify()
                return
        self._end(worker)

    def ask(self, worker: Worker, line: bytes) -> bytes | None:
        with self.condition:
            self.asked += 1
        return worker.ask(line)

    def reap(self) -> None:
        """End the workers idle too long, except one."""
        stale = []
        with self.condition:
            now = time.monotonic()
            self.idle.sort(key=lambda entry: entry[1])
            while len(self.idle) > 1 and now - self.idle[0][1] > WORKER_IDLE_SECONDS:
                stale.append(self.idle.pop(0)[0])
        for worker in stale:
            self._end(worker)

    def warm(self) -> None:
        """Start one worker before the first call asks for one, so that call does not wait for Memar to load."""
        with self.condition:
            if self.live or self.closed:
                return
            self.live += 1
        try:
            worker = Worker(self.top, self.scripts)
        except OSError:
            with self.condition:
                self.live -= 1
            return
        self.release(worker, self.generation_now(), True)

    def close(self) -> None:
        with self.condition:
            self.closed = True
            stale, self.idle = self.idle, []
            self.condition.notify_all()
        for worker, _ in stale:
            self._end(worker)

    def _end(self, worker: Worker) -> None:
        worker.stop()
        with self.condition:
            self.live -= 1
            self.condition.notify()
