#!/usr/bin/env python3
"""One install at a time.

Two sessions on one machine reach the installer at the same time when two
projects are opened at once. Whoever takes the lock records where Memar lives;
the other waits and then finds the work already done, because recording is
idempotent. A lock left by a killed process must not block every later run, so
an old one is taken over and a fresh one is waited out.

The lock is not what keeps two first runs from obtaining the same folder at
once: that act is the bootstrap's, and two clones into one folder means the
second reports a failed clone rather than waiting.
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path

from console import fail
from sys_fs_target import INSTALL_DIRNAME

LOCK_NAME = f".{INSTALL_DIRNAME}-install.lock"
LOCK_WAIT_SECONDS = 600


def lock_path(target: Path) -> Path:
    # Beside the destination, not inside it: the directory may not exist yet.
    return target.parent / LOCK_NAME


def take_lock(path: Path) -> int:
    deadline = time.monotonic() + LOCK_WAIT_SECONDS
    path.parent.mkdir(parents=True, exist_ok=True)
    announced = False
    while True:
        try:
            handle = os.open(str(path), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError:
            try:
                age = time.time() - path.stat().st_mtime
            except OSError:
                age = 0.0
            if age > LOCK_WAIT_SECONDS:
                try:
                    path.unlink()
                except OSError:
                    pass
                continue
            if not announced:
                sys.stderr.write(
                    f"another Memar install is running; waiting for it (lock: {path})\n"
                )
                announced = True
            if time.monotonic() > deadline:
                fail(
                    f"waited {LOCK_WAIT_SECONDS}s for the Memar install lock "
                    f"({path}) and it is still held; if no install is running, "
                    f"remove that file and run this again."
                )
            time.sleep(2)
            continue
        os.close(handle)
        return 0


def release_lock(path: Path) -> None:
    try:
        path.unlink()
    except OSError:
        pass
