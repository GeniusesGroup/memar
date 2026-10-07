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

import contextlib
import hashlib
import json
import os
import sys
import time
from pathlib import Path


from memar_console import fail
from machine.fs_memar import scratch_root

# Both lock families name themselves here rather than deriving a name from
# whatever folder they guard. The install lock was `.Memar-install.lock`,
# built from the installer's own `INSTALL_DIRNAME`, which made this module ask
# the module that decides a destination folder for one string literal: the
# address of a lock is this module's business, and borrowing another module's
# name to spell it is how a rename in one place silently orphans every lock
# the other place had written.
INSTALL_LOCK_NAME = ".memar-install.lock"
LOCK_WAIT_SECONDS = 600

# Where the per-file locks and their intent notes live, under the one scratch
# root, so they never enter git except through the ignored `temp` entry. Named
# here because this is the module that writes them: a reader looking for where
# a lock goes finds the lock, not the location module that owns `temp` itself.
EDIT_LOCK_DIR_NAME = "memar-edit-locks"


def lock_path(target: Path) -> Path:
    # Beside the destination, not inside it: the directory may not exist yet.
    return target.parent / INSTALL_LOCK_NAME


def _take_advisory_lock(
    path: Path,
    *,
    wait_seconds: float,
    stale_seconds: float,
    poll_seconds: float,
    waiting_message: str,
    timeout_message: str,
) -> None:
    """The one mutual-exclusion take every lock in this file shares.

    Atomic take via O_EXCL, stale takeover by mtime, wait with a deadline
    then fail. Callers differ only in timeouts and in what the two messages
    say, so both stay byte-identical by passing them in rather than by
    keeping a second copy of this loop.
    """
    deadline = time.monotonic() + wait_seconds
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
            if age > stale_seconds:
                try:
                    path.unlink()
                except OSError:
                    pass
                continue
            if not announced:
                sys.stderr.write(waiting_message)
                announced = True
            if time.monotonic() > deadline:
                fail(timeout_message)
            time.sleep(poll_seconds)
            continue
        os.close(handle)
        return None


def take_lock(path: Path) -> int:
    _take_advisory_lock(
        path,
        wait_seconds=LOCK_WAIT_SECONDS,
        stale_seconds=LOCK_WAIT_SECONDS,
        poll_seconds=2,
        waiting_message=(
            f"another Memar install is running; waiting for it (lock: {path})\n"
        ),
        timeout_message=(
            f"waited {LOCK_WAIT_SECONDS}s for the Memar install lock "
            f"({path}) and it is still held; if no install is running, "
            f"remove that file and run this again."
        ),
    )
    return 0


def release_lock(path: Path) -> None:
    try:
        path.unlink()
    except OSError:
        pass


# Per-file advisory locks for editing sessions.
#
# Advisory only - enforced by skill rule (agents honor it), not by the
# filesystem; file-write tools bypass it; a central server would enforce
# it, a lock file cannot.
#
# Parallel agent sessions edit one shared working tree with no
# coordination, and concurrent writes to one file collide silently. The
# install lock above is the pattern: atomic take via O_EXCL, stale
# takeover by mtime, wait with a deadline then fail. The locks below
# generalize that pattern to one lock per edited file.
#
# Lock and intent files live under the ONE agent-scratch root,
# <memar-root>/temp/, so they never enter git except through the ignored
# temp entry the root .gitignore already carries: no ignore rule is owed
# because the only repo path they can occupy is an ignored one. The lock
# name carries a readable stem
# plus the sha256 of the target's resolved absolute path, so two
# checkouts holding the same relative path never share a lock.
#
# Release discipline is the caller's: prefer edit_session (which releases
# in a finally) or pair take_file_lock with release_file_lock in
# try/finally. A dead session never blocks others forever: a lock older
# than FILE_LOCK_STALE_SECONDS is unlinked by the next waiter.

FILE_LOCK_WAIT_SECONDS = 120
FILE_LOCK_STALE_SECONDS = 120
FILE_LOCK_POLL_SECONDS = 0.5


def edit_lock_dir(lock_dir: Path | None = None) -> Path:
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


def edit_lock_path(target: Path, lock_dir: Path | None = None) -> Path:
    """The lock file for TARGET, one target to one lock.

    The name carries a readable stem plus the sha256 of the target's
    resolved absolute path, so spellings of one file meet at one lock
    and two files never share one.
    """
    try:
        key = str(Path(target).resolve())
    except OSError:
        key = str(Path(target).absolute())
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]
    stem = "".join(
        character if character.isalnum() or character in "-_" else "-"
        for character in Path(target).name
    ).strip("-")[:32] or "file"
    return edit_lock_dir(lock_dir) / f"memar-edit-{stem}-{digest}.lock"


def edit_intent_path(lock: Path) -> Path:
    """The intent note beside LOCK, under the same scratch root."""
    return Path(str(lock) + ".intent.json")


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
        return {"exists": False, "hash": None, "mtime_ns": None, "size": None}
    try:
        stat = path.stat()
    except OSError:
        return {
            "exists": True,
            "hash": hashlib.sha256(raw).hexdigest(),
            "mtime_ns": None,
            "size": len(raw),
        }
    return {
        "exists": True,
        "hash": hashlib.sha256(raw).hexdigest(),
        "mtime_ns": stat.st_mtime_ns,
        "size": stat.st_size,
    }


def write_intent(
    intent: Path,
    *,
    session_id: str,
    target: Path,
    plan_summary: str,
    base: dict,
) -> None:
    """Record what this session means to change, and against which base.

    Written after the lock is taken so a waiter that takes over a stale
    lock can read what the dead session had planned. Atomic: written to a
    temporary sibling and renamed, so a reader never sees half a note.
    """
    payload = {
        "session_id": session_id,
        "file": str(Path(target).absolute()),
        "plan_summary": plan_summary,
        "base_hash": base.get("hash"),
        "base_mtime_ns": base.get("mtime_ns"),
        "base_size": base.get("size"),
        "created_at": time.time(),
    }
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    intent.parent.mkdir(parents=True, exist_ok=True)
    tmp = intent.with_name(f"{intent.name}.{os.getpid()}.tmp")
    tmp.write_text(text, encoding="utf-8", newline="\n")
    os.replace(tmp, intent)


def read_intent(intent: Path) -> dict:
    """What was recorded by write_intent, as written."""
    return json.loads(Path(intent).read_text(encoding="utf-8"))


def take_file_lock(
    lock: Path,
    wait_seconds: float = FILE_LOCK_WAIT_SECONDS,
    stale_seconds: float = FILE_LOCK_STALE_SECONDS,
    poll_seconds: float = FILE_LOCK_POLL_SECONDS,
) -> None:
    """Take the per-file lock, waiting out a live holder, taking over a dead one.

    The install lock's pattern, generalized: atomic take via O_EXCL, stale
    takeover by mtime, wait with a deadline then fail. A lock older than
    stale_seconds is unlinked by the waiter, so a killed session blocks
    others for at most that long. Past the deadline this fails the run
    rather than applying a change blind.
    """
    _take_advisory_lock(
        lock,
        wait_seconds=wait_seconds,
        stale_seconds=stale_seconds,
        poll_seconds=poll_seconds,
        waiting_message=f"another session is editing; waiting for it (lock: {lock})\n",
        timeout_message=(
            f"waited {wait_seconds}s for the edit lock "
            f"({lock}) and it is still held; if no session is editing, "
            f"remove that file and run this again."
        ),
    )
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
    if current.get("exists") != base.get("exists"):
        raise BaseChangedError(
            f"{target} changed since the plan was made "
            f"(existed at plan time: {base.get('exists')}, "
            f"exists at lock time: {current.get('exists')}); "
            f"re-derive the plan against the current content."
        )
    if current.get("hash") != base.get("hash"):
        raise BaseChangedError(
            f"{target} changed since the plan was made "
            f"(base {base.get('hash')}, now {current.get('hash')}); "
            f"re-derive the plan against the current content."
        )
    if (
        base.get("mtime_ns") is not None
        and current.get("mtime_ns") is not None
        and current.get("mtime_ns") != base.get("mtime_ns")
    ):
        raise BaseChangedError(
            f"{target} was touched since the plan was made "
            f"(mtime {base.get('mtime_ns')}, now {current.get('mtime_ns')}); "
            f"re-derive the plan against the current content."
        )


@contextlib.contextmanager
def edit_session(
    target: Path,
    session_id: str,
    plan_summary: str,
    lock_dir: Path | None = None,
    wait_seconds: float = FILE_LOCK_WAIT_SECONDS,
    stale_seconds: float = FILE_LOCK_STALE_SECONDS,
    poll_seconds: float = FILE_LOCK_POLL_SECONDS,
):
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
        write_intent(
            edit_intent_path(lock),
            session_id=session_id,
            target=target,
            plan_summary=plan_summary,
            base=base,
        )
        verify_base_unchanged(target, base)
        yield {"lock": lock, "base": base}
    finally:
        release_file_lock(lock)
