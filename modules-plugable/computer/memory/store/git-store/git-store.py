#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""`git-store`, an adapter of the store contract that keeps a store in one reference of a git object database.

What it is, what it declares and why, how it meets the suite and what it cannot do is
[Memory Git Store](git-store.md); the contract is `modules/computer/memory/store/protocol/store.py`; the groups it owes
are `cases.py`; the decisions no abstraction gave are [git-store Handoff](git-store.handoff.md#decisions).

`bind(project, class_name)` is the adapter that serves a class, read from the adapter's keys of the project's `memar:`
block; `GitStoreAdapter(...).open()` a handle on its store. The handles of one adapter in one process share one medium:
three long-lived git processes, the index, and the writer's lock. Run as a command, it prints a class's lag:

    python modules-plugable/computer/memory/store/git-store/git-store.py lag --project PATH --class NAME
"""
from __future__ import annotations
import argparse
import bisect
import enum
import hashlib
import json
import os
import shutil
import subprocess
import sys
import threading
import time
import uuid
import weakref
from dataclasses import dataclass
from importlib import import_module
from pathlib import Path
from typing import Any, Callable, Protocol, Sequence, runtime_checkable
HERE = Path(__file__).resolve().parent
TOP = next((p for p in HERE.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()))
if str(TOP) not in sys.path:
    sys.path.insert(0, str(TOP))
_m_store = import_module('modules.computer.memory.store.protocol.store')
ABSENT = _m_store.ABSENT
Absent = _m_store.Absent
Capability = _m_store.Capability
Committed = _m_store.Committed
Conflict = _m_store.Conflict
Found = _m_store.Found
Limits = _m_store.Limits
Parameters = _m_store.Parameters
Refusal = _m_store.Refusal
Refused = _m_store.Refused
Stats = _m_store.Stats
Unavailability = _m_store.Unavailability
Unavailable = _m_store.Unavailable
token = _m_store.token
TOKEN_LENGTH = len(token(b''))
MODULE = 'modules-plugable.computer.memory.store.git-store.git-store'
REFERENCE_KEY = 'git-store-reference'
SHARED_KEY = 'git-store-shared'
PUBLISH_KEY = 'git-store-publish'
NAMESPACE = 'refs/memory/'
PUBLISHED_NAMESPACE = 'refs/memory-published/'
PENDING_BRANCH = 'refs/memory-pending/batch'
WRITER_FOLDER = 'memar-git-store'
FAN_OUT = 3
STALE_LOCK_SECONDS = 2.0
SWAP_WAITS_AT_MOST = 60.0
PACKS_BEFORE_REPACK = 32
BATCHES_BETWEEN_PACK_COUNTS = 16
INDEX_SAVED_AFTER = 256
RETRY_FIRST_SECONDS = 0.5
RETRY_MOST_SECONDS = 15.0
COMMAND_BYTES = 3500
COMMITTER = b'git-store <git-store@memar.invalid>'
EMPTY_TREE = {'sha1': '4b825dc642cb6eb9a060e54bf8d69288fbee4904', 'sha256': '6ef19b41225c5369f1c104d45d8d85efa9b057b53b14b4b9b939dd74decc5321'}
EVERY_ADDRESS: tuple[tuple[bytes, bytes | None], ...] = ((b'', None),)
NOT_FAST_FORWARD = 'not a fast-forward: another writer published to the shared store first, and its batch was kept'

class Publish(enum.Enum):
    """When a batch of a class with a shared store is answered."""
    NOW = 'now'
    SOON = 'soon'

    def summary(self) -> str:
        return {Publish.NOW: 'after one push of the batch to the shared store has been tried', Publish.SOON: 'at the local commit, the push following in the background'}[self]

@dataclass(frozen=True)
class Lag:
    """How far the shared store is behind a store: the batches ahead of it, the age of the oldest in seconds, and why a push was refused."""
    batches: int
    oldest_age: float | None = None
    refused: str = ''

    def summary(self) -> str:
        if not self.batches:
            return 'the shared store holds every committed batch'
        said = f'{self.batches} batch(es) ahead of the shared store, the oldest {self.oldest_age or 0:.0f} s old'
        return f'{said}; {self.refused}' if self.refused else said

@runtime_checkable
class Fallback(Protocol):
    """What a store asks for an address outside the ranges it holds: one answer per address, and the held addresses of a range."""

    def get(self, addresses: Sequence[bytes]) -> list[Any]:
        ...

    def list(self, from_: bytes, to: bytes | None) -> Any:
        ...

class NotFound:
    """The one fallback: a shared store that answers that nothing is there."""

    def get(self, addresses: Sequence[bytes]) -> list[Any]:
        return [ABSENT for _ in addresses]

    def list(self, from_: bytes, to: bytes | None) -> tuple[bytes, ...]:
        return ()

def address_path(at: bytes) -> bytes:
    """Where an address is written in the reference's tree: its first FAN_OUT bytes as folders, then the whole address."""
    digits = at.hex()
    folders = [digits[2 * i:2 * i + 2] or '__' for i in range(FAN_OUT)]
    return '/'.join(folders + [digits or '_']).encode('ascii')

def path_address(path: bytes) -> bytes | None:
    """The address a path of the tree holds, or None for a path the rule does not make."""
    leaf = path.rsplit(b'/', 1)[-1]
    if path.count(b'/') != FAN_OUT:
        return None
    try:
        return b'' if leaf == b'_' else bytes.fromhex(leaf.decode('ascii'))
    except ValueError:
        return None

def data_area() -> Path:
    """The user's data area where `git-store` saves its index: outside every working tree."""
    if os.name == 'nt' and os.environ.get('LOCALAPPDATA'):
        return Path(os.environ['LOCALAPPDATA']) / 'Memar' / 'git-store'
    base = os.environ.get('XDG_DATA_HOME') or str(Path.home() / '.local' / 'share')
    return Path(base) / 'memar' / 'git-store'

def published_reference(reference: str) -> str:
    """The private reference that records what the shared store acknowledged of REFERENCE."""
    return PUBLISHED_NAMESPACE + (reference.removeprefix(NAMESPACE) if reference.startswith(NAMESPACE) else reference.removeprefix('refs/'))

def _page(order: Sequence[bytes], from_: bytes | None, to: bytes | None, after: bytes | None, limit: int | None, descending: bool) -> tuple[bytes, ...]:
    low = bisect.bisect_left(order, from_) if from_ is not None else 0
    high = bisect.bisect_left(order, to) if to is not None else len(order)
    if descending:
        if after is not None:
            high = min(high, bisect.bisect_left(order, after))
        start = low if limit is None else max(low, high - limit)
        return tuple(reversed(order[start:high])) if start < high else ()
    if after is not None:
        low = max(low, bisect.bisect_right(order, after))
    end = high if limit is None else min(high, low + limit)
    return tuple(order[low:end]) if low < end else ()

def _holds(held: Sequence[tuple[bytes, bytes | None]], at: bytes) -> bool:
    return any((low <= at and (high is None or at < high) for low, high in held))

def _gaps(held: Sequence[tuple[bytes, bytes | None]], from_: bytes, to: bytes | None) -> list[tuple[bytes, bytes | None]]:
    """The parts of [FROM_, TO) outside the held ranges."""
    gaps, at = ([], from_)
    for low, high in sorted(held, key=lambda each: each[0]):
        if to is not None and at >= to:
            return gaps
        if low > at:
            gaps.append((at, low if to is None else min(low, to)))
        if high is None:
            return gaps
        at = max(at, high)
    if to is None or at < to:
        gaps.append((at, to))
    return gaps

class _Lost(Exception):
    """A long-lived git process ended before it answered."""

class _FairLock:
    """A reentrant lock taken in the order it was asked for, so a reader asking again at once cannot starve a writer."""

    def __init__(self) -> None:
        self._guard = threading.Condition(threading.Lock())
        self._next = 0
        self._serving = 0
        self._owner: int | None = None
        self._depth = 0

    def __enter__(self) -> '_FairLock':
        me = threading.get_ident()
        with self._guard:
            if self._owner == me:
                self._depth += 1
                return self
            ticket = self._next
            self._next += 1
            while ticket != self._serving:
                self._guard.wait()
            self._owner, self._depth = (me, 1)
        return self

    def __exit__(self, *_: Any) -> None:
        with self._guard:
            self._depth -= 1
            if self._depth == 0:
                self._owner = None
                self._serving += 1
                self._guard.notify_all()

class _WriterLock:
    """The lock that orders a store's writers on one machine: a file in git's directory, locked by the operating system,
    which releases it when the holding process ends, however it ends."""

    def __init__(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self.fd = os.open(str(path), os.O_RDWR | os.O_CREAT, 438)
        self.threads = threading.Lock()

    def __enter__(self) -> '_WriterLock':
        self.threads.acquire()
        try:
            if os.name == 'nt':
                import msvcrt
                os.lseek(self.fd, 0, os.SEEK_SET)
                while True:
                    try:
                        msvcrt.locking(self.fd, msvcrt.LK_NBLCK, 1)
                        return self
                    except OSError:
                        time.sleep(0.005)
            import fcntl
            fcntl.flock(self.fd, fcntl.LOCK_EX)
            return self
        except BaseException:
            self.threads.release()
            raise

    def __exit__(self, *_: Any) -> None:
        try:
            if os.name == 'nt':
                import msvcrt
                os.lseek(self.fd, 0, os.SEEK_SET)
                msvcrt.locking(self.fd, msvcrt.LK_UNLCK, 1)
            else:
                import fcntl
                fcntl.flock(self.fd, fcntl.LOCK_UN)
        finally:
            self.threads.release()

    def close(self) -> None:
        try:
            os.close(self.fd)
        except OSError:
            pass

def _end(processes: dict[str, subprocess.Popen]) -> None:
    """End the long-lived processes: their input closes, and one that does not end soon is killed."""
    for name in list(processes):
        process = processes.pop(name)
        try:
            process.stdin.close()
        except (OSError, ValueError):
            pass
        try:
            process.wait(5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
        for stream in (process.stdout, process.stderr):
            if stream is not None:
                stream.close()

class _Medium:
    """What the handles of one store in one process share: the git processes, the index, the writer's lock and the publisher."""

    def __init__(self, adapter: 'GitStoreAdapter') -> None:
        self.repository = Path(adapter.repository)
        self.reference = adapter.reference
        self.published = published_reference(adapter.reference)
        self.shared = adapter.shared
        self.processes_started = 0
        self.files_opened = 0
        self.git = shutil.which('git') or 'git'
        found = self.run(['rev-parse', '--git-common-dir', '--show-object-format'], cwd=self.repository)
        if found.returncode != 0:
            raise ValueError(f'{self.repository} is not in a git repository: {found.stderr.decode("utf-8", "replace").strip()}')
        common, object_format = found.stdout.decode('utf-8').split()[:2]
        self.git_dir = (self.repository / common).resolve()
        self.object_format = object_format
        self.oid_length = hashlib.new(object_format).digest_size
        self.empty_tree = EMPTY_TREE[object_format]
        self.reading = _FairLock()
        self.processes: dict[str, subprocess.Popen] = {}
        self.writer = _WriterLock(self.git_dir / WRITER_FOLDER / (self.reference.replace('/', '_') + '.writer'))
        self.files_opened += 1
        self.lock_file = self.git_dir / (self.reference + '.lock')
        self.index_file = Path(adapter.data_area or data_area()) / (hashlib.sha256(f'{os.path.normcase(str(self.git_dir))}\n{self.reference}'.encode('utf-8')).hexdigest()[:32] + '.index')
        self.tip_indexed: str | None = None
        self.built = False
        self.blobs: dict[bytes, str] = {}
        self.order: list[bytes] = []
        self.tokens: dict[str, bytes] = {}
        self.unsaved = 0
        self.batches_since_count = 0
        self.publisher: _Publisher | None = None
        self._finalize = weakref.finalize(self, _end, self.processes)
        self._load_index()
        if self.shared:
            self.publisher = _Publisher(self, adapter.reachable)
            self.publisher.start()

    def run(self, args: list[str], cwd: Path | None=None, data: bytes | None=None, env: dict | None=None) -> subprocess.CompletedProcess[bytes]:
        self.processes_started += 1
        where = cwd or self.repository
        return subprocess.run([self.git, *(['--git-dir', str(self.git_dir)] if cwd is None else []), *args], cwd=str(where), input=data, capture_output=True, env=env, stdin=None if data is not None else subprocess.DEVNULL)

    def _long_lived(self, name: str, args: list[str], errors: Any=subprocess.DEVNULL) -> subprocess.Popen:
        process = self.processes.get(name)
        if process is None or process.poll() is not None:
            self.processes_started += 1
            process = subprocess.Popen([self.git, '--git-dir', str(self.git_dir), *args], cwd=str(self.repository), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=errors)
            self.processes[name] = process
        return process

    def end(self, *names: str) -> None:
        _end({name: self.processes.pop(name) for name in names if name in self.processes})

    def _ask(self, commands: list[bytes]) -> list[bytes | None]:
        """The answer of `cat-file --batch-command` to each command, in order: a header line, or the contents asked."""
        answers: list[bytes | None] = []
        start = 0
        while start < len(commands):
            end, size = (start, 0)
            while end < len(commands) and (end == start or size + len(commands[end]) <= COMMAND_BYTES):
                size += len(commands[end])
                end += 1
            process = self._long_lived('cat-file', ['cat-file', '--batch-command'])
            try:
                process.stdin.write(b''.join(commands[start:end]))
                process.stdin.flush()
                for command in commands[start:end]:
                    header = process.stdout.readline()
                    if not header:
                        raise _Lost('cat-file')
                    parts = header.split()
                    if len(parts) < 3:
                        answers.append(None)
                    elif command.startswith(b'contents '):
                        size_of = int(parts[2])
                        answers.append(process.stdout.read(size_of))
                        process.stdout.read(1)
                    else:
                        answers.append(header)
            except (OSError, ValueError) as lost:
                self.end('cat-file')
                raise _Lost('cat-file') from lost
            start = end
        return answers

    def object_id(self, name: str) -> str | None:
        """The id of the object NAME names, a reference or an id, or None when there is none."""
        header = self._ask([f'info {name}\n'.encode('utf-8')])[0]
        return header.split()[0].decode('ascii') if header else None

    def object_kind(self, name: str) -> str | None:
        header = self._ask([f'info {name}\n'.encode('utf-8')])[0]
        return header.split()[1].decode('ascii') if header else None

    def contents(self, names: Sequence[str]) -> list[bytes | None]:
        return self._ask([f'contents {name}\n'.encode('ascii') for name in names])

    def tip(self) -> str | None:
        return self.object_id(self.reference)

    def _load_index(self) -> None:
        try:
            saved = json.loads(self.index_file.read_text(encoding='utf-8'))
            self.files_opened += 1
            blobs = {bytes.fromhex(at): oid for at, oid in saved['blobs'].items()}
            tip = saved['tip']
        except (OSError, ValueError, KeyError, TypeError, AttributeError):
            return
        self.blobs, self.order, self.tip_indexed, self.built = (blobs, sorted(blobs), tip, True)

    def save_index(self) -> None:
        if not self.built:
            return
        try:
            self.index_file.parent.mkdir(parents=True, exist_ok=True)
            spare = self.index_file.with_name(f'{self.index_file.name}.{os.getpid()}.{uuid.uuid4().hex[:8]}')
            spare.write_text(json.dumps({'tip': self.tip_indexed, 'blobs': {at.hex(): oid for at, oid in self.blobs.items()}}), encoding='utf-8')
            self.files_opened += 1
            os.replace(spare, self.index_file)
            self.unsaved = 0
        except OSError:
            pass

    def drop_index(self) -> None:
        with self.reading:
            self.blobs, self.order, self.tip_indexed, self.built, self.tokens, self.unsaved = ({}, [], None, False, {}, 0)
            try:
                self.index_file.unlink()
            except OSError:
                pass

    def _apply(self, changed: dict[bytes, str | None]) -> None:
        added = [at for at, oid in changed.items() if oid is not None and at not in self.blobs]
        removed = {at for at, oid in changed.items() if oid is None and at in self.blobs}
        for at, oid in changed.items():
            if oid is None:
                self.blobs.pop(at, None)
            else:
                self.blobs[at] = oid
        if removed:
            self.order = [at for at in self.order if at not in removed]
        if len(added) > 64:
            self.order = sorted(set(self.order).union(added))
        else:
            for at in added:
                bisect.insort(self.order, at)
        self.unsaved += len(changed)

    def diff(self, old: str, new: str) -> list[tuple[bytes, str | None]] | None:
        """The addresses whose value differs between the trees of OLD and NEW, each with its blob in NEW (None when gone)."""
        done = self.run(['diff-tree', '-r', '-z', '--no-renames', old, new])
        if done.returncode != 0:
            return None
        fields = done.stdout.split(b'\x00')
        found = []
        for i in range(0, len(fields) - 1, 2):
            meta, path = (fields[i].split(), fields[i + 1])
            at = path_address(path)
            if at is not None and len(meta) >= 5:
                found.append((at, None if meta[4].startswith(b'D') else meta[3].decode('ascii')))
        return found

    def bring_up_to_date(self, tip: str | None) -> None:
        """Make the index reflect TIP: by `diff-tree` from the tip it reflects, or from the empty tree when it is unknown."""
        if self.built and self.tip_indexed == tip:
            return
        if tip is None:
            self.blobs, self.order, self.tip_indexed, self.built = ({}, [], None, True)
            return
        base = self.tip_indexed if self.built and self.tip_indexed else self.empty_tree
        found = self.diff(base, tip)
        if found is None and base != self.empty_tree:
            self.blobs, self.order, self.built = ({}, [], False)
            found = self.diff(self.empty_tree, tip)
        if found is None:
            raise _Lost('diff-tree')
        if not self.built:
            self.blobs, self.order = ({}, [])
        self._apply(dict(found))
        self.tip_indexed, self.built = (tip, True)
        if self.unsaved >= INDEX_SAVED_AFTER:
            self.save_index()

    def read(self, addresses: Sequence[bytes]) -> dict[bytes, Any]:
        """What the index's state holds at each of ADDRESSES: Found or Absent."""
        oids = {at: self.blobs.get(at) for at in addresses}
        wanted = sorted({oid for oid in oids.values() if oid is not None})
        values = dict(zip(wanted, self.contents(wanted)))
        answers: dict[bytes, Any] = {}
        for at, oid in oids.items():
            if oid is None:
                answers[at] = ABSENT
            elif values.get(oid) is None:
                raise _Lost('cat-file')
            else:
                data = values[oid]
                answers[at] = Found(data, self.tokens.setdefault(oid, token(data)))
        return answers

    def tokens_of(self, addresses: Sequence[bytes]) -> dict[bytes, Any]:
        """The token at each address, Absent where none: from the tokens already known, reading only the others."""
        unknown = [at for at in addresses if at in self.blobs and self.blobs[at] not in self.tokens]
        self.read(unknown)
        return {at: self.tokens[self.blobs[at]] if at in self.blobs else ABSENT for at in addresses}

    def blob_id(self, data: bytes) -> str:
        return hashlib.new(self.object_format, b'blob %d\x00' % len(data) + data).hexdigest()

    def write_objects(self, tip: str | None, write: Sequence[tuple[bytes, bytes]]) -> str:
        """Write a batch's blobs, trees and commit, its parent TIP, as one pack, and answer the commit's id; no reference is written."""
        stream = [b'commit %s\nmark :1\ncommitter %s %d +0000\ndata 6\nbatch\n' % (PENDING_BRANCH.encode('ascii'), COMMITTER, int(time.time()))]
        if tip:
            stream.append(b'from %s\n' % tip.encode('ascii'))
        for at, data in write:
            stream.append(b'M 100644 inline %s\ndata %d\n' % (address_path(at), len(data)))
            stream.append(data)
            stream.append(b'\n')
        mark = uuid.uuid4().hex.encode('ascii')
        stream.append(b'\nget-mark :1\nreset %s\ncheckpoint\nprogress %s\n' % (PENDING_BRANCH.encode('ascii'), mark))
        process = self._long_lived('fast-import', ['-c', 'fastimport.unpackLimit=0', 'fast-import', '--quiet'])
        try:
            process.stdin.write(b''.join(stream))
            process.stdin.flush()
            commit = process.stdout.readline().strip().decode('ascii')
            done = process.stdout.readline().strip()
        except (OSError, ValueError) as lost:
            self.end('fast-import')
            raise _Lost('fast-import') from lost
        if len(commit) != 2 * self.oid_length or done != b'progress ' + mark:
            self.end('fast-import')
            raise _Lost('fast-import')
        return commit

    def swap(self, new: str, old: str | None) -> str | None:
        """Move the reference from OLD to NEW in one compare-and-swap: 'ok', 'moved' when it no longer holds OLD, or None when undecided."""
        expected = old or '0' * (2 * self.oid_length)
        waited_until = time.monotonic() + SWAP_WAITS_AT_MOST
        while time.monotonic() < waited_until:
            process = self._long_lived('update-ref', ['update-ref', '--stdin'], subprocess.PIPE)
            try:
                process.stdin.write(f'start\nupdate {self.reference} {new} {expected}\ncommit\n'.encode('ascii'))
                process.stdin.flush()
                answered = (process.stdout.readline(), process.stdout.readline())
            except (OSError, ValueError):
                answered = (b'', b'')
            if answered[1] == b'commit: ok\n':
                return 'ok'
            self.end('update-ref')
            with self.reading:
                now = self.tip()
            if now == new:
                return 'ok'
            if now != old:
                return 'moved'
            try:
                age = time.time() - self.lock_file.stat().st_mtime
            except OSError:
                continue
            if age > STALE_LOCK_SECONDS:
                try:
                    self.lock_file.unlink()
                except OSError:
                    pass
            else:
                time.sleep(0.05)
        return None

    def maintain(self) -> None:
        """Keep the number of packs bounded: past PACKS_BEFORE_REPACK, `repack -d --geometric=2`, with this process's readers closed."""
        self.batches_since_count += 1
        if self.batches_since_count < BATCHES_BETWEEN_PACK_COUNTS:
            return
        self.batches_since_count = 0
        try:
            packs = sum((1 for each in os.scandir(self.git_dir / 'objects' / 'pack') if each.name.endswith('.pack')))
        except OSError:
            return
        if packs > PACKS_BEFORE_REPACK:
            with self.reading:
                self.end('cat-file', 'fast-import')
                self.run(['repack', '-d', '-q', '--geometric=2'])

    def lag(self) -> Lag:
        with self.reading:
            tip, acknowledged = (self.tip(), self.object_id(self.published))
            batches, oldest, at = (0, None, tip)
            while at is not None and at != acknowledged:
                body = self.contents([at])[0] or b''
                parent, when = (None, None)
                for line in body.split(b'\n\n', 1)[0].split(b'\n'):
                    if line.startswith(b'parent ') and parent is None:
                        parent = line.split()[1].decode('ascii')
                    elif line.startswith(b'committer '):
                        when = int(line.split()[-2])
                batches, oldest, at = (batches + 1, when, parent)
        age = time.time() - oldest if oldest is not None else None
        return Lag(batches, age, self.publisher.refused if self.publisher else '')

    def close(self) -> None:
        if self.publisher is not None:
            self.publisher.stop()
        with self.reading:
            if self.unsaved:
                self.save_index()
            _end(self.processes)
        self.writer.close()

class _Publisher(threading.Thread):
    """Pushes a store's reference to its shared store after each commit, retrying while it cannot, and records what was acknowledged."""

    def __init__(self, medium: _Medium, reachable: bool) -> None:
        super().__init__(daemon=True, name=f'git-store publisher of {medium.reference}')
        self.medium = medium
        self.reachable = reachable
        self.refused = ''
        self.wake = threading.Event()
        self.stopping = False
        self.pushing = threading.Lock()
        self.wake.set()

    def run(self) -> None:
        delay = RETRY_FIRST_SECONDS
        while not self.stopping:
            woken = self.wake.wait(None if delay is None else delay)
            self.wake.clear()
            if self.stopping:
                return
            outcome = self.push_once()
            if outcome == 'ahead':
                delay = RETRY_FIRST_SECONDS if woken else min(RETRY_MOST_SECONDS, (delay or RETRY_FIRST_SECONDS) * 2)
            else:
                delay = None

    def stop(self) -> None:
        self.stopping = True
        self.wake.set()
        self.join(30)

    def push_once(self) -> str:
        """One push of the tip: 'published', 'refused' (not a fast-forward), or 'ahead' (it could not be pushed and is retried)."""
        medium = self.medium
        with self.pushing:
            try:
                with medium.reading:
                    tip, acknowledged = (medium.tip(), medium.object_id(medium.published))
            except _Lost:
                return 'ahead'
            if tip is None or tip == acknowledged:
                return 'published'
            where = medium.shared if self.reachable else str(medium.git_dir / WRITER_FOLDER / 'unreachable.git')
            environment = {**os.environ, 'GIT_TERMINAL_PROMPT': '0'}
            pushed = medium.run(['push', '--porcelain', where, f'{tip}:{medium.reference}'], cwd=medium.repository, env=environment)
            said = (pushed.stdout + pushed.stderr).decode('utf-8', 'replace')
            if pushed.returncode == 0:
                medium.run(['update-ref', medium.published, tip])
                self.refused = ''
                return 'published'
            if '[rejected]' in said or 'non-fast-forward' in said or 'fetch first' in said:
                self.refused = NOT_FAST_FORWARD
                return 'refused'
            return 'ahead'

    def poke(self) -> None:
        self.wake.set()

class GitStore:
    """A handle on a store kept in a reference of a git object database; see the module's docstring and [Memory Git Store](git-store.md)."""
    parameters = Parameters()
    limits = Limits()

    def __init__(self, medium: _Medium, adapter: 'GitStoreAdapter') -> None:
        self._medium = medium
        self._held = tuple(adapter.held)
        self._fallback: Any = adapter.fallback or NotFound()
        self._publish = Publish(adapter.publish)
        self._hook: Callable[[], None] | None = None
        kinds = {Capability.ATOMIC_BATCH, Capability.DURABLE, Capability.SHARED_BETWEEN_PROCESSES, Capability.FALLBACK, Capability.LEAVES_WORKING_TREE_UNTOUCHED}
        self.capabilities = frozenset(kinds | ({Capability.REPLICATED} if medium.shared else set()))

    def _current(self) -> None:
        self._medium.bring_up_to_date(self._medium.tip())

    def get(self, addresses: Sequence[bytes]) -> Any:
        if not all((isinstance(at, bytes) for at in addresses)):
            return Refused(Refusal.MALFORMED, 'an address that is not bytes')
        held = [at for at in addresses if _holds(self._held, at)]
        others = [at for at in addresses if not _holds(self._held, at)]
        try:
            with self._medium.reading:
                self._current()
                found = self._medium.read(held)
        except _Lost:
            return [Unavailable(Unavailability.FAILED) for _ in addresses]
        if others:
            found.update(zip(others, self._fallback.get(others)))
        return [found[at] for at in addresses]

    def list(self, from_: bytes | None=None, to: bytes | None=None, after: bytes | None=None, limit: int | None=None, descending: bool=False) -> Any:
        if limit is not None and limit < 1:
            return Refused(Refusal.MALFORMED, 'a limit below one')
        if from_ is not None and to is not None and (from_ > to):
            return Refused(Refusal.MALFORMED, 'a from after a to')
        gaps = _gaps(self._held, from_ or b'', to)
        asked: list[bytes] = []
        for low, high in gaps:
            answer = self._fallback.list(low, high)
            if isinstance(answer, Unavailable):
                return Unavailable(Unavailability.UNREACHABLE)
            asked += answer
        try:
            with self._medium.reading:
                self._current()
                if not asked:
                    return _page(self._medium.order, from_, to, after, limit, descending)
                order = sorted(set(_page(self._medium.order, from_, to, None, None, False)).union(asked))
        except _Lost:
            return Unavailable(Unavailability.FAILED)
        return _page(order, from_, to, after, limit, descending)

    def _refusal(self, expect: Sequence, write: Sequence) -> Refused | None:
        if not write:
            return Refused(Refusal.MALFORMED, 'a batch with no write')
        written = [at for at, _ in write]
        expected = [at for at, _ in expect]
        if len(set(written)) != len(written) or len(set(expected)) != len(expected):
            return Refused(Refusal.MALFORMED, 'an address written twice or expected twice')
        if not all((isinstance(at, bytes) for at in written + expected)):
            return Refused(Refusal.MALFORMED, 'an address that is not bytes')
        if not all((isinstance(data, bytes) for _, data in write)):
            return Refused(Refusal.MALFORMED, 'a value that is not bytes')
        if not all((isinstance(e, Absent) or (isinstance(e, bytes) and len(e) == TOKEN_LENGTH) for _, e in expect)):
            return Refused(Refusal.MALFORMED, 'an expectation that is neither a token nor absent')
        return None

    def _decide(self, expect: Sequence, write: Sequence) -> Any:
        """Unavailable or Conflict, in that order, for the state the index reflects; None when every expectation holds."""
        if any((not _holds(self._held, at) for at, _ in write)) or any((not _holds(self._held, at) and (not isinstance(e, Absent)) for at, e in expect)):
            return Unavailable(Unavailability.NOT_HELD)
        outside = [at for at, _ in expect if not _holds(self._held, at)]
        current: dict[bytes, Any] = {}
        if outside:
            asked = self._fallback.get(outside)
            if any((isinstance(each, Unavailable) for each in asked)):
                return Unavailable(Unavailability.UNREACHABLE)
            current.update({at: ABSENT if isinstance(each, Absent) else each.token for at, each in zip(outside, asked)})
        current.update(self._medium.tokens_of([at for at, _ in expect if _holds(self._held, at)]))
        for index, (at, expectation) in enumerate(expect):
            if isinstance(expectation, Absent) != isinstance(current[at], Absent) or (not isinstance(expectation, Absent) and current[at] != expectation):
                return Conflict(index)
        return None

    def batch(self, expect: Sequence, write: Sequence) -> Any:
        refused = self._refusal(expect, write)
        if refused:
            return refused
        medium = self._medium
        with medium.writer:
            while True:
                try:
                    with medium.reading:
                        tip = medium.tip()
                        medium.bring_up_to_date(tip)
                        answer = self._decide(expect, write)
                except _Lost:
                    return Unavailable(Unavailability.FAILED)
                if answer is not None:
                    return answer
                if self._hook is not None:
                    try:
                        self._hook()
                    except Exception:
                        return Unavailable(Unavailability.FAILED)
                try:
                    commit = medium.write_objects(tip, write)
                except _Lost:
                    return Unavailable(Unavailability.FAILED)
                swapped = medium.swap(commit, tip)
                if swapped == 'ok':
                    break
                if swapped is None:
                    return Unavailable(Unavailability.FAILED)
            with medium.reading:
                if medium.built and medium.tip_indexed == tip:
                    changed = {}
                    for at, data in write:
                        oid = medium.blob_id(data)
                        medium.tokens[oid] = token(data)
                        changed[at] = oid
                    medium._apply(changed)
                    medium.tip_indexed = commit
                    if medium.unsaved >= INDEX_SAVED_AFTER:
                        medium.save_index()
            medium.maintain()
        if medium.publisher is not None:
            if self._publish is Publish.NOW:
                medium.publisher.push_once()
            else:
                medium.publisher.poke()
        return Committed()

    def state(self) -> bytes:
        with self._medium.reading:
            tip = self._medium.tip()
        return bytes.fromhex(tip) if tip else bytes(self._medium.oid_length)

    def changes(self, since: bytes) -> Any:
        medium = self._medium
        if not isinstance(since, bytes) or len(since) != medium.oid_length:
            return Refused(Refusal.MALFORMED, 'a state this store never answered')
        with medium.reading:
            tip = medium.tip()
            empty = since == bytes(medium.oid_length)
            if not empty and medium.object_kind(since.hex()) != 'commit':
                return Refused(Refusal.MALFORMED, 'a state this store never answered')
        if since.hex() == tip or (empty and tip is None):
            return ()
        if tip is None:
            return Refused(Refusal.MALFORMED, 'a state this store never answered')
        found = medium.diff(medium.empty_tree if empty else since.hex(), tip)
        if found is None:
            return Refused(Refusal.MALFORMED, 'a state this store never answered')
        return tuple(sorted({at for at, _ in found}))

    def stats(self) -> Stats:
        return Stats(processes_started=self._medium.processes_started, files_opened=self._medium.files_opened)

    def at_commit_point(self, hook: Callable[[], None] | None) -> None:
        self._hook = hook

    def drop_derived_structures(self) -> None:
        self._medium.drop_index()

    def lag(self) -> Lag:
        """The batches ahead of the shared store, the age of the oldest, and why a push was refused."""
        return self._medium.lag()

    def opener(self) -> tuple[str, str, dict]:
        return self._adapter_opener

    def close(self) -> None:
        """End what the store's medium runs in this process; every handle of it."""
        self._medium.close()

class GitStoreAdapter:
    """The adapter of one class: a reference of the repository at REPOSITORY. Its `store` is what names the store, so two
    classes bound to one store are told; each `open()` is a new handle on it. DATA_AREA is where the index is saved
    (the user's data area by default); SHARED the shared store, a remote's name or a URL, or None; PUBLISH `now` or `soon`."""

    def __init__(self, repository: str, reference: str, data_area: str | None=None, shared: str | None=None, publish: str=Publish.SOON.value) -> None:
        if not reference.startswith('refs/') or '..' in reference or reference.endswith(('/', '.lock')):
            raise ValueError(f'{reference!r} is not a reference git-store may keep a store in')
        self.repository = str(Path(repository).resolve())
        self.reference = reference
        self.data_area = data_area
        self.shared = shared
        self.publish = Publish(publish).value
        self.store = (os.path.normcase(self.repository), reference)
        self.held: tuple[tuple[bytes, bytes | None], ...] = EVERY_ADDRESS
        self.fallback: Any = None
        self.reachable = True
        self._medium: _Medium | None = None

    def _medium_of(self) -> _Medium:
        if self._medium is None:
            self._medium = _Medium(self)
        return self._medium

    def open(self) -> GitStore:
        handle = GitStore(self._medium_of(), self)
        handle._adapter_opener = self.opener()
        return handle

    def opener(self) -> tuple[str, str, dict]:
        """What opens the same adapter in another process: this module, the class, and its keyword arguments."""
        return (MODULE, type(self).__name__, {'repository': self.repository, 'reference': self.reference, 'data_area': self.data_area, 'shared': self.shared, 'publish': self.publish})

    def close(self) -> None:
        if self._medium is not None:
            self._medium.close()
            self._medium = None

    def fall_back(self, fallback: Any, held: Sequence[tuple[bytes, bytes | None]]) -> None:
        """The seam of the `fallback` group: handles opened after it ask FALLBACK (NotFound when None) for what lies outside HELD."""
        self.fallback = fallback
        self.held = tuple(held)

    def working_tree(self) -> Path | None:
        """The working tree of the repository, or None for a bare one."""
        return Path(self.repository) if (Path(self.repository) / '.git').exists() else None

    def shared_reachable(self, flag: bool) -> None:
        """The seam of the `replicated` group: whether the shared store can be reached from now on."""
        self.reachable = flag
        if self._medium is not None and self._medium.publisher is not None:
            self._medium.publisher.reachable = flag
            self._medium.publisher.poke()

    def shared_state(self) -> bytes | None:
        """The state of the class at the shared store, as `state()` answers it, or None when it holds none."""
        if not self.shared:
            return None
        listed = subprocess.run(['git', 'ls-remote', self.shared, self.reference], cwd=self.repository, capture_output=True, stdin=subprocess.DEVNULL)
        line = listed.stdout.split()
        return bytes.fromhex(line[0].decode('ascii')) if listed.returncode == 0 and line else None

    def sibling(self) -> 'GitStoreAdapter':
        """A new, empty adapter on another machine's store of the same class and shared store, beside this one's repository."""
        folder = Path(self.repository).parent / f'sibling-{uuid.uuid4().hex[:8]}'
        (folder / 'data').mkdir(parents=True)
        subprocess.run(['git', 'init', '-q', str(folder / 'project')], check=True, capture_output=True, stdin=subprocess.DEVNULL)
        return GitStoreAdapter(str(folder / 'project'), self.reference, data_area=str(folder / 'data'), shared=self.shared, publish=self.publish)

def bind(project: Path, class_name: str) -> GitStoreAdapter:
    """The adapter that serves CLASS_NAME in PROJECT, from the adapter's keys of its `memar:` block; it does no work on the medium."""
    preferences = import_module('modules.process.project.services.preferences')
    found: dict[str, dict[str, str]] = {}
    for key in (REFERENCE_KEY, SHARED_KEY, PUBLISH_KEY):
        values = preferences.class_values_preference(Path(project), key)
        if values is None:
            raise ValueError(f'`{key}` in {preferences.preferences_path(Path(project))} is not `class=value` pairs separated by commas, each class once')
        found[key] = values
    reference = found[REFERENCE_KEY].get(class_name, NAMESPACE + class_name)
    publish = found[PUBLISH_KEY].get(class_name, Publish.SOON.value)
    return GitStoreAdapter(str(project), reference, shared=found[SHARED_KEY].get(class_name), publish=publish)

def main(argv: Sequence[str] | None=None) -> int:
    parser = argparse.ArgumentParser(prog='git-store.py', description="Print how far a class's shared store lags behind its git-store.")
    verbs = parser.add_subparsers(dest='verb', required=True)
    lag = verbs.add_parser('lag', help='print the batches of a class ahead of its shared store, and the age of the oldest')
    lag.add_argument('--project', required=True, type=Path, help="the project whose `memar:` block binds the class")
    lag.add_argument('--class', dest='class_name', required=True, help='the class, as the `memory` key names it')
    given = parser.parse_args(argv)
    adapter = bind(given.project, given.class_name)
    try:
        store = adapter.open()
        print(store.lag().summary() if Capability.REPLICATED in store.capabilities else 'the class names no shared store')
    finally:
        adapter.close()
    return 0
if __name__ == '__main__':
    sys.exit(main())
