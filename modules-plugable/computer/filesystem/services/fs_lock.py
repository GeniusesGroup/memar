#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""One install at a time.

Two sessions on one machine reach the installer at the same time when two
projects are opened at once. Whoever takes the lock records where Memar lives;
the other waits and then finds the work already done, because recording is
idempotent. A lock left by a killed process must not block every later run, so
an old one is taken over and a fresh one is waited out.

The lock is not what keeps two first runs from obtaining the same folder at
once: that act is the bootstrap's, and two clones into one folder means the
second reports a failed clone rather than waiting.

Who gets to do a thing is asked here whatever the span: one install at a time,
one edit of a file at a time, and — by a dated marker rather than a lock —
one run of a daily job a day. The session sweep and the daily update both ask
`claim_today`, so the guard is written once.
"""
from __future__ import annotations
from importlib import import_module
_m_fs_memar = import_module('modules-plugable.computer.filesystem.services.fs_memar')
scratch_root = _m_fs_memar.scratch_root
import contextlib
import hashlib
import json
import os
import sys
import time
from datetime import date
from pathlib import Path
from machine.console import fail
INSTALL_LOCK_NAME = '.memar-install.lock'
LOCK_WAIT_SECONDS = 600
EDIT_LOCK_DIR_NAME = 'memar-edit-locks'

def lock_path(target: Path) -> Path:
    return target.parent / INSTALL_LOCK_NAME

def _take_advisory_lock(path: Path, *, wait_seconds: float, stale_seconds: float, poll_seconds: float, waiting_message: str, timeout_message: str) -> None:
    """The one mutual-exclusion take every lock in this file shares.

    Atomic take via O_EXCL, stale takeover by mtime, wait with a deadline
    then fail. Callers differ only in timeouts and in what the two messages
    say, so both stay byte-identical by passing them in rather than by
    keeping a second copy of this loop.
    """
    deadline = time.monotonic() + wait_seconds
    announced = False
    while not try_lock(path, stale_seconds):
        if not announced:
            sys.stderr.write(waiting_message)
            announced = True
        if time.monotonic() > deadline:
            fail(timeout_message)
        time.sleep(poll_seconds)
    return None

def try_lock(path: Path, stale_seconds: float) -> bool:
    """Take the lock at PATH if nobody live holds it, and say whether it was taken.

    The one take every lock in this file makes: atomic by O_EXCL, and a lock
    older than STALE_SECONDS is a dead holder's and is taken over. A caller with
    nothing to wait for — a run that someone else is already doing — asks this
    and goes away when it answers no.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    while True:
        try:
            handle = os.open(str(path), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 384)
        except FileExistsError:
            try:
                age = time.time() - path.stat().st_mtime
            except OSError:
                age = 0.0
            if age <= stale_seconds:
                return False
            try:
                path.unlink()
            except OSError:
                return False
            continue
        os.close(handle)
        return True

def claim_today(marker: Path) -> bool:
    """Whether this call is the first today for MARKER, recording today's date if it is.

    The once-a-day guard every daily job here shares: the marker holds one date,
    so asking costs one small read however often it is asked. A marker that
    cannot be written still answers yes, and says so on stderr: a job that runs
    twice in a day is a cost, one that never runs again is a fault.
    """
    today = date.today().isoformat()
    try:
        if marker.read_text(encoding='utf-8').strip() == today:
            return False
    except OSError:
        pass
    try:
        marker.parent.mkdir(parents=True, exist_ok=True)
        marker.write_text(today + '\n', encoding='utf-8', newline='\n')
    except OSError as error:
        print(f'warning: the daily marker {marker} could not be written ({error})', file=sys.stderr)
    return True

def take_lock(path: Path) -> int:
    _take_advisory_lock(path, wait_seconds=LOCK_WAIT_SECONDS, stale_seconds=LOCK_WAIT_SECONDS, poll_seconds=2, waiting_message=f'another Memar install is running; waiting for it (lock: {path})\n', timeout_message=f'waited {LOCK_WAIT_SECONDS}s for the Memar install lock ({path}) and it is still held; if no install is running, remove that file and run this again.')
    return 0

def release_lock(path: Path) -> None:
    try:
        path.unlink()
    except OSError:
        pass
FILE_LOCK_WAIT_SECONDS = 120
FILE_LOCK_STALE_SECONDS = 120
FILE_LOCK_POLL_SECONDS = 0.5

def edit_lock_dir(lock_dir: Path | None=None) -> Path:
    """Where per-file lock and intent files live.

    Under <memar-root>/temp/ by default, so lock files and intent notes share
    the ONE session-scratch root and never enter git except through the ignored
    temp entry. An explicit directory (the tests pass a scratch folder) is
    honored instead, which is how the location is proved without writing
    to the machine's checkout.
    """
    if lock_dir is not None:
        Path(lock_dir).mkdir(parents=True, exist_ok=True)
        return Path(lock_dir)
    directory = scratch_root() / EDIT_LOCK_DIR_NAME
    directory.mkdir(parents=True, exist_ok=True)
    return directory

def edit_lock_path(target: Path, lock_dir: Path | None=None) -> Path:
    """The lock file for TARGET, one target to one lock.

    The name carries a readable stem plus the sha256 of the target's
    resolved absolute path, so spellings of one file meet at one lock
    and two files never share one.
    """
    try:
        key = str(Path(target).resolve())
    except OSError:
        key = str(Path(target).absolute())
    digest = hashlib.sha256(key.encode('utf-8')).hexdigest()[:16]
    stem = ''.join((character if character.isalnum() or character in '-_' else '-' for character in Path(target).name)).strip('-')[:32] or 'file'
    return edit_lock_dir(lock_dir) / f'memar-edit-{stem}-{digest}.lock'

def edit_intent_path(lock: Path) -> Path:
    """The intent note beside LOCK, under the same scratch root."""
    return Path(str(lock) + '.intent.json')

def file_snapshot(target: Path) -> dict:
    """The base a change plan is made against: content hash plus mtime.

    Captured at plan time and compared again at lock time by
    verify_base_unchanged. A missing file snapshots as not existing, so a
    file that appears between plan and lock also counts as changed.
    """
    path = Path(target)
    try:
        raw = path.read_bytes()
    except OSError:
        return {'exists': False, 'hash': None, 'mtime_ns': None, 'size': None}
    try:
        stat = path.stat()
    except OSError:
        return {'exists': True, 'hash': hashlib.sha256(raw).hexdigest(), 'mtime_ns': None, 'size': len(raw)}
    return {'exists': True, 'hash': hashlib.sha256(raw).hexdigest(), 'mtime_ns': stat.st_mtime_ns, 'size': stat.st_size}

def write_intent(intent: Path, *, task_id: str, target: Path, plan_summary: str, base: dict) -> None:
    """Record what this session means to change, and against which base.

    Written after the lock is taken so a waiter that takes over a stale
    lock can read what the dead session had planned. Atomic: written to a
    temporary sibling and renamed, so a reader never sees half a note.
    """
    payload = {'task_id': task_id, 'file': str(Path(target).absolute()), 'plan_summary': plan_summary, 'base_hash': base.get('hash'), 'base_mtime_ns': base.get('mtime_ns'), 'base_size': base.get('size'), 'created_at': time.time()}
    text = json.dumps(payload, indent=2, sort_keys=True) + '\n'
    intent.parent.mkdir(parents=True, exist_ok=True)
    tmp = intent.with_name(f'{intent.name}.{os.getpid()}.tmp')
    tmp.write_text(text, encoding='utf-8', newline='\n')
    os.replace(tmp, intent)

def read_intent(intent: Path) -> dict:
    """What was recorded by write_intent, as written."""
    return json.loads(Path(intent).read_text(encoding='utf-8'))

def take_file_lock(lock: Path, wait_seconds: float=FILE_LOCK_WAIT_SECONDS, stale_seconds: float=FILE_LOCK_STALE_SECONDS, poll_seconds: float=FILE_LOCK_POLL_SECONDS) -> None:
    """Take the per-file lock, waiting out a live holder, taking over a dead one.

    The install lock's pattern, generalized: atomic take via O_EXCL, stale
    takeover by mtime, wait with a deadline then fail. A lock older than
    stale_seconds is unlinked by the waiter, so a killed session blocks
    others for at most that long. Past the deadline this fails the run
    rather than applying a change blind.
    """
    _take_advisory_lock(lock, wait_seconds=wait_seconds, stale_seconds=stale_seconds, poll_seconds=poll_seconds, waiting_message=f'another session is editing; waiting for it (lock: {lock})\n', timeout_message=f'waited {wait_seconds}s for the edit lock ({lock}) and it is still held; if no session is editing, remove that file and run this again.')
    return None

def release_file_lock(lock: Path) -> None:
    """Release the per-file lock and remove its intent note. Never raises."""
    try:
        lock.unlink()
    except OSError:
        pass
    try:
        edit_intent_path(lock).unlink()
    except OSError:
        pass

class BaseChangedError(Exception):
    """The file moved under the plan: re-derive, never blind-apply."""

def verify_base_unchanged(target: Path, base: dict) -> None:
    """Re-verify the change plan against the file's state at lock time.

    Call after acquiring the lock, with the base captured at plan time by
    file_snapshot. Any move - edited content, deleted file, newly
    appeared file - raises BaseChangedError naming the file. The caller
    then re-derives the plan against the current content instead of
    applying the old one.
    """
    current = file_snapshot(target)
    if current.get('exists') != base.get('exists'):
        raise BaseChangedError(f"{target} changed since the plan was made (existed at plan time: {base.get('exists')}, exists at lock time: {current.get('exists')}); re-derive the plan against the current content.")
    if current.get('hash') != base.get('hash'):
        raise BaseChangedError(f"{target} changed since the plan was made (base {base.get('hash')}, now {current.get('hash')}); re-derive the plan against the current content.")
    if base.get('mtime_ns') is not None and current.get('mtime_ns') is not None and (current.get('mtime_ns') != base.get('mtime_ns')):
        raise BaseChangedError(f"{target} was touched since the plan was made (mtime {base.get('mtime_ns')}, now {current.get('mtime_ns')}); re-derive the plan against the current content.")

@contextlib.contextmanager
def edit_session(target: Path, task_id: str, plan_summary: str, lock_dir: Path | None=None, wait_seconds: float=FILE_LOCK_WAIT_SECONDS, stale_seconds: float=FILE_LOCK_STALE_SECONDS, poll_seconds: float=FILE_LOCK_POLL_SECONDS):
    """Hold the per-file lock for one edit, releasing however it ends.

    Snapshots the base, takes the lock, writes the intent note, then
    re-verifies the base before yielding: if the file moved between plan
    and lock, this raises BaseChangedError without yielding, and the lock
    is still released. The release runs in a finally, which is the
    try/finally discipline callers that take the lock by hand must keep.
    """
    base = file_snapshot(target)
    lock = edit_lock_path(target, lock_dir)
    take_file_lock(lock, wait_seconds, stale_seconds, poll_seconds)
    try:
        write_intent(edit_intent_path(lock), task_id=task_id, target=target, plan_summary=plan_summary, base=base)
        verify_base_unchanged(target, base)
        yield {'lock': lock, 'base': base}
    finally:
        release_file_lock(lock)
