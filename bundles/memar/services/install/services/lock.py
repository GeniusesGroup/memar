#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""bundles/memar/services/install/services/lock.py — one install at a time.

Two tasks on one machine reach the installer at the same time when two
projects are opened at once. Whoever takes the lock records where Memar lives;
the other waits and then finds the work already done, because recording is
idempotent. A lock left by a killed process must not block every later run, so
an old one is taken over and a fresh one is waited out.

The lock is not what keeps two first runs from obtaining the same folder at
once: that act is the bootstrap's, and two clones into one folder means the
second reports a failed clone rather than waiting.

The take itself, atomic by exclusive creation with a stale takeover and a
deadline, is written once in `bundles/memar_fs/services/fs_lock.py`; this file
says only what the install lock is called, where it lies and how long it is
waited for. Releasing it is that file's `release_lock`.
"""
from __future__ import annotations
from importlib import import_module
from pathlib import Path
_m_fs_lock = import_module('bundles.memar_fs.services.fs_lock')
INSTALL_LOCK_NAME = '.memar-install.lock'
LOCK_WAIT_SECONDS = 600

def lock_path(target: Path) -> Path:
    return target.parent / INSTALL_LOCK_NAME

def take_lock(path: Path) -> int:
    _m_fs_lock.take_advisory_lock(path, wait_seconds=LOCK_WAIT_SECONDS, stale_seconds=LOCK_WAIT_SECONDS, poll_seconds=2, waiting_message=f'another Memar install is running; waiting for it (lock: {path})\n', timeout_message=f'waited {LOCK_WAIT_SECONDS}s for the Memar install lock ({path}) and it is still held; if no install is running, remove that file and run this again.')
    return 0
