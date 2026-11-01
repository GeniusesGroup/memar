#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import bisect
import json
import os
import threading
import time
import uuid
import weakref
from importlib import import_module
from pathlib import Path
from typing import Any, Callable, Sequence
HERE = Path(__file__).resolve().parent
TOP = next((p for p in HERE.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()))
import sys
if str(TOP) not in sys.path:
    sys.path.insert(0, str(TOP))
_m_store = import_module('modules.computer.memory.store.protocol.store')
_m_errors = import_module('modules-plugable.computer.memory.store.files.errors.errors')
_m_storage = import_module('modules-plugable.computer.memory.filesystem.storage')
_m_codecs = import_module('modules-plugable.computer.memory.store.files.codecs.registry')
_m_graph_files = import_module('modules-plugable.computer.memory.store.files.graph_correspondence')
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
BadAddress = _m_errors.BadAddress
BadParameter = _m_errors.BadParameter
BadCodec = _m_errors.BadCodec
Lost = _m_errors.Lost
RootCollision = _m_errors.RootCollision
URI_Path = _m_storage.URI_Path
Storage_Directory = _m_storage.Storage_Directory
Storage_File = _m_storage.Storage_File
directory_at = _m_storage.directory_at
TOKEN_LENGTH = len(token(b''))
MODULE = 'modules-plugable.computer.memory.store.files.files'
MEMORY_ROOT_KEY = 'files-memory-root'
BODY_CODEC_KEY = 'files-body-codec'
SHARD_THRESHOLD_KEY = 'files-shard-threshold'
SHARD_PREFIX_KEY = 'files-shard-prefix-length'
DEFAULT_MEMORY_ROOT = '.agents/memar/memory'
DEFAULT_BODY_CODEC = 'json'
DEFAULT_SHARD_PREFIX = 4
META_FOLDER = '.files-store'
RECORD_ID_LENGTH = 16
STALE_LOCK_SECONDS = 2.0
SWAP_WAITS_AT_MOST = 60.0
_OPEN: weakref.WeakValueDictionary[str, '_Medium'] = weakref.WeakValueDictionary()
_OPEN_GUARD = threading.Lock()

def _id_segment(identity: bytes) -> str:
    try:
        return str(uuid.UUID(bytes=identity))
    except ValueError:
        return identity.hex()

def _parse_id_segment(segment: str) -> bytes | None:
    try:
        return uuid.UUID(segment).bytes
    except ValueError:
        pass
    try:
        found = bytes.fromhex(segment)
    except ValueError:
        return None
    return found if len(found) == RECORD_ID_LENGTH else None

def is_record_key(address: object) -> bool:
    if not isinstance(address, bytes) or not RECORD_ID_LENGTH < len(address) <= RECORD_ID_LENGTH + 64:
        return False
    try:
        address[RECORD_ID_LENGTH:].decode('ascii')
    except UnicodeDecodeError:
        return False
    return True

class Files_Path:

    def relative_path(self, address: bytes, shard_prefix_length: int=0, shard_enabled: bool=False) -> URI_Path:
        if not isinstance(address, bytes):
            raise BadAddress('an address that is not bytes')
        if is_record_key(address):
            identity = address[:RECORD_ID_LENGTH]
            leaf = _id_segment(identity)
            if shard_enabled and shard_prefix_length > 0:
                return URI_Path(f'{identity.hex()[:shard_prefix_length]}/{leaf}')
            return URI_Path(leaf)
        graph = _m_graph_files.parse_graph_address(address)
        if graph is not None:
            _tag, frm, _relation = graph
            leaf = _id_segment(frm)
            if shard_enabled and shard_prefix_length > 0:
                return URI_Path(f'{frm.hex()[:shard_prefix_length]}/{leaf}')
            return URI_Path(leaf)
        leaf = address.hex() if address else '_'
        return URI_Path(leaf)

    def file_identity(self, relative: str) -> tuple[bytes, bool] | None:
        parts = relative.replace('\\', '/').strip('/').split('/')
        if not parts or parts == ['']:
            return None
        if len(parts) == 1:
            leaf = parts[0]
            shard = None
        elif len(parts) == 2:
            shard, leaf = parts
        else:
            return None
        if leaf == '_':
            return (b'', False) if shard is None else None
        identity = _parse_id_segment(leaf)
        if identity is not None:
            if shard is not None and identity.hex()[:len(shard)] != shard:
                return None
            return (identity, True)
        try:
            other = bytes.fromhex(leaf)
        except ValueError:
            return None
        if shard is not None and other.hex()[:len(shard)] != shard:
            return None
        return (other, False)

class _FairLock:

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

    def __init__(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self.path = path
        self.fd = os.open(str(path), os.O_RDWR | os.O_CREAT, 438)
        self.threads = threading.Lock()

    def __enter__(self) -> '_WriterLock':
        self.threads.acquire()
        started = time.monotonic()
        try:
            while True:
                if os.name == 'nt':
                    import msvcrt
                    os.lseek(self.fd, 0, os.SEEK_SET)
                    try:
                        msvcrt.locking(self.fd, msvcrt.LK_NBLCK, 1)
                        return self
                    except OSError:
                        pass
                else:
                    import fcntl
                    try:
                        fcntl.flock(self.fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                        return self
                    except OSError:
                        pass
                try:
                    age = time.time() - self.path.stat().st_mtime
                except OSError:
                    age = 0.0
                if age > STALE_LOCK_SECONDS:
                    try:
                        os.close(self.fd)
                    except OSError:
                        pass
                    try:
                        self.path.unlink()
                    except OSError:
                        pass
                    self.fd = os.open(str(self.path), os.O_RDWR | os.O_CREAT, 438)
                if time.monotonic() - started > SWAP_WAITS_AT_MOST:
                    self.threads.release()
                    raise Lost('a writer lock could not be taken')
                time.sleep(0.005)
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

class _Medium:

    def __init__(self, adapter: 'FilesAdapter') -> None:
        self.root = adapter.memory_root
        self.root.ensure()
        self.meta = self.root.directory(META_FOLDER).ensure()
        self.path = adapter.path
        self.codec = adapter.body_codec
        self.shard_threshold = adapter.shard_threshold
        self.shard_prefix_length = adapter.shard_prefix_length
        self.writer = _WriterLock(self.meta.host_path() / 'lock')
        self.reading = _FairLock()
        self.order: list[bytes] = []
        self.values: dict[bytes, bytes] = {}
        self.commits: list[tuple[bytes, ...]] = []
        self.name = os.urandom(8)
        self.generation = 0
        self.files_opened = 0
        self._load()

    def _state_file(self) -> Storage_File:
        return self.meta.file('state')

    def _load(self) -> None:
        state = self._state_file()
        if state.exists():
            held = state.get_file_data()
            if len(held) >= 16:
                self.name = held[:8]
                self.generation = int.from_bytes(held[8:16], 'big')
        order: list[bytes] = []
        values: dict[bytes, bytes] = {}
        for relative, file in self.root.iter_files():
            text = str(relative)
            if text.startswith(META_FOLDER + '/') or '/' + META_FOLDER + '/' in f'/{text}/':
                continue
            parsed = self.path.file_identity(text)
            if parsed is None:
                continue
            identity, is_node = parsed
            body = file.get_file_data()
            self.files_opened += 1
            if is_node:
                parts = self.codec.unpack(body)
                if parts is None:
                    continue
                for at, value in _m_graph_files.restore_from_parts(identity, parts).items():
                    values[at] = value
                    bisect.insort(order, at)
            else:
                values[identity] = body
                bisect.insort(order, identity)
        self.order = order
        self.values = values
        self._recover_journal()

    def bring_up_to_date(self) -> None:
        state = self._state_file()
        if not state.exists():
            if self.generation == 0 and not self.values:
                return
            self._load()
            return
        held = state.get_file_data()
        if len(held) < 16:
            return
        name = held[:8]
        generation = int.from_bytes(held[8:16], 'big')
        if name == self.name and generation == self.generation:
            return
        self._load()

    def _save_state(self) -> None:
        self._state_file().replace_bytes(self.name + self.generation.to_bytes(8, 'big'))

    def root_file_count(self) -> int:
        count = 0
        for relative, _file in self.root.iter_files():
            text = str(relative)
            if text.startswith(META_FOLDER + '/') or '/' + META_FOLDER + '/' in f'/{text}/':
                continue
            count += 1
        return count

    def shard_for(self, address: bytes) -> tuple[int, bool]:
        if self.shard_threshold is None:
            return (self.shard_prefix_length, False)
        enabled = self.root_file_count() >= self.shard_threshold
        return (self.shard_prefix_length, enabled)

    def file_for(self, address: bytes) -> Storage_File:
        length, enabled = self.shard_for(address)
        relative = self.path.relative_path(address, length, enabled)
        found = self.root.get_file_by_path(relative)
        if found.exists() or self.shard_threshold is None:
            return found
        unsharded = self.root.get_file_by_path(self.path.relative_path(address, length, False))
        if unsharded.exists():
            return unsharded
        sharded = self.root.get_file_by_path(self.path.relative_path(address, length, True))
        return sharded if enabled else unsharded

    def read(self, addresses: Sequence[bytes]) -> list[Any]:
        answers = []
        for at in addresses:
            held = self.values.get(at)
            if held is None:
                answers.append(ABSENT)
            else:
                answers.append(Found(held, token(held)))
        return answers

    def tokens_of(self, addresses: Sequence[bytes]) -> dict[bytes, Any]:
        found = {}
        for at in addresses:
            held = self.values.get(at)
            found[at] = ABSENT if held is None else token(held)
        return found

    def _journal_file(self) -> Storage_File:
        return self.meta.file('journal')

    def _encode_journal(self, generation: int, pairs: Sequence[tuple[bytes, bytes]]) -> bytes:
        return json.dumps({'generation': generation, 'pairs': [[at.hex(), data.hex()] for at, data in pairs]}, separators=(',', ':')).encode('ascii')

    def _decode_journal(self, raw: bytes) -> tuple[int, list[tuple[bytes, bytes]]]:
        body = json.loads(raw.decode('ascii'))
        return (int(body['generation']), [(bytes.fromhex(at), bytes.fromhex(data)) for at, data in body['pairs']])

    def _set_value(self, at: bytes, data: bytes) -> None:
        if at not in self.values:
            bisect.insort(self.order, at)
        self.values[at] = bytes(data)

    def _apply_pairs(self, pairs: Sequence[tuple[bytes, bytes]]) -> None:
        by_file: dict[tuple[bytes, bool], list[tuple[bytes, bytes]]] = {}
        for at, data in pairs:
            if is_record_key(at):
                key = (at[:RECORD_ID_LENGTH], True)
            else:
                graph = _m_graph_files.parse_graph_address(at)
                if graph is not None:
                    _tag, frm, _relation = graph
                    key = (frm, True)
                else:
                    key = (at, False)
            by_file.setdefault(key, []).append((at, data))
        for (identity, is_node), group in by_file.items():
            sample = group[0][0]
            target = self.file_for(sample)
            if is_node:
                working = dict(self.values)
                for at, data in group:
                    working[at] = bytes(data)
                parts = _m_graph_files.collect_node_parts(working, identity, is_record_key)
                body, stored = self.codec.pack(parts)
                target.replace_bytes(body)
                self.files_opened += 1
                for at, raw in _m_graph_files.restore_from_parts(identity, stored).items():
                    self._set_value(at, raw)
            else:
                data = bytes(group[-1][1])
                target.replace_bytes(data)
                self.files_opened += 1
                self._set_value(identity, data)

    def _recover_journal(self) -> None:
        journal = self._journal_file()
        if not journal.exists():
            return
        generation, pairs = self._decode_journal(journal.get_file_data())
        if self.generation < generation:
            self._apply_pairs(pairs)
            self.generation = generation
            self.commits.append(tuple(sorted({at for at, _ in pairs})))
            self._save_state()
        journal.delete()

    def write(self, pairs: Sequence[tuple[bytes, bytes]]) -> None:
        generation = self.generation + 1
        journal = self._journal_file()
        journal.replace_bytes(self._encode_journal(generation, pairs))
        self._apply_pairs(pairs)
        self.generation = generation
        self.commits.append(tuple(sorted({at for at, _ in pairs})))
        self._save_state()
        journal.delete()

    def close(self) -> None:
        self.writer.close()

class Files:

    parameters = Parameters()
    limits = Limits()

    def __init__(self, medium: _Medium) -> None:
        self._medium = medium
        self.capabilities = frozenset({Capability.ATOMIC_BATCH, Capability.DURABLE})
        self._hook: Callable[[], None] | None = None

    def get(self, addresses: Sequence[bytes]) -> Any:
        if not all((isinstance(at, bytes) for at in addresses)):
            return Refused(Refusal.MALFORMED, 'an address that is not bytes')
        try:
            with self._medium.reading:
                self._medium.bring_up_to_date()
                return self._medium.read(addresses)
        except Lost:
            return [Unavailable(Unavailability.FAILED) for _ in addresses]

    def list(self, from_: bytes | None=None, to: bytes | None=None, after: bytes | None=None, limit: int | None=None, descending: bool=False) -> Any:
        if limit is not None and limit < 1:
            return Refused(Refusal.MALFORMED, 'a limit below one')
        if from_ is not None and to is not None and (from_ > to):
            return Refused(Refusal.MALFORMED, 'a from after a to')
        try:
            with self._medium.reading:
                self._medium.bring_up_to_date()
                order = self._medium.order
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
        except Lost:
            return Unavailable(Unavailability.FAILED)

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

    def batch(self, expect: Sequence, write: Sequence) -> Any:
        refused = self._refusal(expect, write)
        if refused:
            return refused
        medium = self._medium
        try:
            with medium.writer:
                with medium.reading:
                    medium.bring_up_to_date()
                    current = medium.tokens_of([at for at, _ in expect])
                    for index, (at, expectation) in enumerate(expect):
                        holds = isinstance(current[at], Absent) if isinstance(expectation, Absent) else current[at] == expectation
                        if not holds:
                            return Conflict(index)
                    if self._hook is not None:
                        try:
                            self._hook()
                        except Exception:
                            return Unavailable(Unavailability.FAILED)
                    medium.write(write)
        except Lost:
            return Unavailable(Unavailability.FAILED)
        return Committed()

    def state(self) -> bytes:
        with self._medium.reading:
            self._medium.bring_up_to_date()
            return self._medium.name + self._medium.generation.to_bytes(8, 'big')

    def changes(self, since: bytes) -> Any:
        medium = self._medium
        with medium.reading:
            medium.bring_up_to_date()
            count = int.from_bytes(since[8:], 'big') if isinstance(since, bytes) and len(since) == 16 and since[:8] == medium.name else -1
            if not 0 <= count <= medium.generation:
                return Refused(Refusal.MALFORMED, 'a state this store never answered')
            if count == medium.generation:
                return ()
            if len(medium.commits) == medium.generation:
                return tuple(sorted({at for commit in medium.commits[count:] for at in commit}))
            return tuple(medium.order)

    def stats(self) -> Stats:
        return Stats(files_opened=self._medium.files_opened)

    def at_commit_point(self, hook: Callable[[], None] | None) -> None:
        self._hook = hook

    def drop_derived_structures(self) -> None:
        pass

    def close(self) -> None:
        pass

class FilesAdapter:

    def __init__(self, project: str | Path, memory_root: str | Path | Storage_Directory | None=None, shard_threshold: int | None=None, shard_prefix_length: int=DEFAULT_SHARD_PREFIX, body_codec: Any | None=None) -> None:
        self.project = Path(project).resolve()
        if isinstance(memory_root, Storage_Directory):
            self.memory_root = memory_root
        else:
            relative = Path(memory_root) if memory_root is not None else Path(DEFAULT_MEMORY_ROOT)
            absolute = relative if relative.is_absolute() else self.project / relative
            self.memory_root = directory_at(absolute.resolve())
        self.shard_threshold = shard_threshold
        self.shard_prefix_length = shard_prefix_length
        if isinstance(body_codec, str):
            self.body_codec = _m_codecs.resolve(body_codec)
        elif body_codec is not None:
            self.body_codec = body_codec
        else:
            self.body_codec = _m_codecs.resolve(DEFAULT_BODY_CODEC)
        self.path = Files_Path()
        self.store = os.path.normcase(str(self.memory_root.host_path()))
        self._medium: _Medium | None = None

    def get_memory_root(self) -> Storage_Directory:
        return self.memory_root

    def get_path(self) -> Files_Path:
        return self.path

    def get_shard_threshold(self) -> tuple[int | None, bool]:
        return (self.shard_threshold, self.shard_threshold is not None)

    def get_shard_prefix_length(self) -> int:
        return self.shard_prefix_length

    def get_body_codec(self) -> Any:
        return self.body_codec

    def shard_for(self, address: bytes) -> tuple[int, bool]:
        return self._medium_of().shard_for(address)

    def file_at(self, address: bytes) -> Storage_File:
        return self._medium_of().file_for(address)

    def same_store(self, other: 'FilesAdapter') -> bool:
        return self.store == other.store

    def _medium_of(self) -> _Medium:
        if self._medium is None:
            key = self.store
            with _OPEN_GUARD:
                held = _OPEN.get(key)
                if held is not None:
                    self._medium = held
                else:
                    self._medium = _Medium(self)
                    _OPEN[key] = self._medium
        return self._medium

    def open(self) -> Files:
        handle = Files(self._medium_of())
        handle._adapter_opener = self.opener()
        return handle

    def opener(self) -> tuple[str, str, dict]:
        return (MODULE, type(self).__name__, {'project': str(self.project), 'memory_root': str(self.memory_root.host_path()), 'shard_threshold': self.shard_threshold, 'shard_prefix_length': self.shard_prefix_length, 'body_codec': self.body_codec.get_name()})

    def close(self) -> None:
        if self._medium is not None:
            key = self.store
            with _OPEN_GUARD:
                if _OPEN.get(key) is self._medium:
                    _OPEN.pop(key, None)
            self._medium.close()
            self._medium = None

    def working_tree(self) -> Path | None:
        return self.project if (self.project / '.git').exists() else self.project

    def sibling(self) -> 'FilesAdapter':
        folder = self.project.parent / f'sibling-{uuid.uuid4().hex[:8]}'
        folder.mkdir(parents=True)
        root = folder / DEFAULT_MEMORY_ROOT
        return FilesAdapter(folder, memory_root=root, shard_threshold=self.shard_threshold, shard_prefix_length=self.shard_prefix_length, body_codec=self.body_codec)

def _resolve_root(project: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else (project / path).resolve()

def bind(project: Path, class_name: str) -> FilesAdapter:
    preferences = import_module('modules.computer.software.edges.manifest.services.preferences')
    found: dict[str, dict[str, str]] = {}
    for key in (MEMORY_ROOT_KEY, SHARD_THRESHOLD_KEY, SHARD_PREFIX_KEY):
        values = preferences.class_values_preference(Path(project), key)
        if values is None:
            raise BadParameter(f'`{key}` in {preferences.preferences_path(Path(project))} is not `class=value` pairs separated by commas, each class once')
        found[key] = values
    codec_values = preferences.class_values_preference(Path(project), BODY_CODEC_KEY)
    if codec_values is not None and class_name in codec_values and codec_values[class_name] == '':
        raise BadParameter(f'an empty `{BODY_CODEC_KEY}` for `{class_name}`')
    codec_name = DEFAULT_BODY_CODEC if codec_values is None else codec_values.get(class_name, DEFAULT_BODY_CODEC)
    body_codec = _m_codecs.resolve(codec_name)
    root_text = found[MEMORY_ROOT_KEY].get(class_name, DEFAULT_MEMORY_ROOT)
    root = _resolve_root(Path(project), root_text)
    threshold_text = found[SHARD_THRESHOLD_KEY].get(class_name)
    threshold: int | None
    if threshold_text is None:
        threshold = None
    else:
        if not threshold_text.isdigit():
            raise BadParameter(f'{threshold_text!r} is not a whole number for `{SHARD_THRESHOLD_KEY}`')
        threshold = int(threshold_text)
    prefix_text = found[SHARD_PREFIX_KEY].get(class_name)
    if prefix_text is None:
        prefix = DEFAULT_SHARD_PREFIX
    else:
        if not prefix_text.isdigit() or int(prefix_text) < 1:
            raise BadParameter(f'{prefix_text!r} is not a positive whole number for `{SHARD_PREFIX_KEY}`')
        prefix = int(prefix_text)
    for other, bound in (preferences.memory_preference(Path(project)) or {}).items():
        if other == class_name:
            break
        if bound != HERE.name:
            continue
        theirs_text = found[MEMORY_ROOT_KEY].get(other, DEFAULT_MEMORY_ROOT)
        theirs = _resolve_root(Path(project), theirs_text)
        if root == theirs:
            continue

        def _nests(one: Path, under: Path) -> bool:
            try:
                one.relative_to(under)
            except ValueError:
                return False
            return one != under
        if _nests(root, theirs) or _nests(theirs, root):
            raise RootCollision(f'the memory root of `{class_name}`, {root}, and that of `{other}`, {theirs}, nest')
    return FilesAdapter(Path(project), memory_root=root, shard_threshold=threshold, shard_prefix_length=prefix, body_codec=body_codec)
