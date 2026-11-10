#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
import threading
import time
from mcp.services.serve import Worker
WORKER_IDLE_SECONDS = 300.0

class Pool:

    def __init__(self, most: int, wait: float=4.0) -> None:
        self.most = max(1, most)
        self.wait = wait
        self.condition = threading.Condition()
        self.idle: list[tuple[Worker, float]] = []
        self.live = 0
        self.closed = False
        self.asked = 0

    def acquire(self) -> Worker | None:
        deadline = time.monotonic() + self.wait
        with self.condition:
            while True:
                if self.closed:
                    return None
                if self.idle:
                    return self.idle.pop()[0]
                if self.live < self.most:
                    self.live += 1
                    break
                left = deadline - time.monotonic()
                if left <= 0:
                    return None
                self.condition.wait(left)
        try:
            return Worker()
        except OSError:
            with self.condition:
                self.live -= 1
                self.condition.notify()
            return None

    def release(self, worker: Worker, healthy: bool) -> None:
        with self.condition:
            if healthy and (not self.closed):
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
            worker = Worker()
        except OSError:
            with self.condition:
                self.live -= 1
            return
        self.release(worker, True)

    def close(self) -> None:
        with self.condition:
            self.closed = True
            stale, self.idle = (self.idle, [])
            self.condition.notify_all()
        for worker, _ in stale:
            self._end(worker)

    def _end(self, worker: Worker) -> None:
        worker.stop()
        with self.condition:
            self.live -= 1
            self.condition.notify()
