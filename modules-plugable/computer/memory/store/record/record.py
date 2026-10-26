#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""`record`, the capsule of nodes, parts and labels laid over any store of the contract.

What it adds to the store contract (`modules/computer/memory/store/protocol/store.py`), and why, is
[Memory Record](record.md); this file is the one source of its signatures, its key, the id form and the domain key
charset. `record` is itself a store of the contract whose address is a key: the 16 bytes of an id, a UUID version 7,
then the ASCII bytes of a domain key, with no separator. A node's parts are the values under the keys that begin with
its id, and its labels the part under `labels`, the ids ascending without repetition. `get`, `list`, `batch`, `state`
and `changes` are the contract's over keys, with `record`'s refusals added; `parts`, `nodes` and `scan` are its own.

`nodes` and `scan` answer from an index of the nodes' ids and labels kept in the memory of the process, one for each
open `Record`, never in the store's medium nor on disk; it records the `state()` it reflects and applies
`changes(since)` before it answers. A read that takes more than one call of the store is repeated until `state()` is
the same before and after it, so it answers from one committed state.
"""
from __future__ import annotations
import bisect
import re
from dataclasses import dataclass, field
from importlib import import_module
from typing import Any, Sequence
_m_store = import_module('modules.computer.memory.store.protocol.store')
ABSENT = _m_store.ABSENT
Absent = _m_store.Absent
Capability = _m_store.Capability
Limits = _m_store.Limits
Parameters = _m_store.Parameters
Refusal = _m_store.Refusal
Refused = _m_store.Refused
Unavailable = _m_store.Unavailable
ID_LENGTH = 16
INSTANT_LENGTH = 6
INSTANT_END = 1 << 8 * INSTANT_LENGTH
DOMAIN_KEY_MOST = 64
DOMAIN_KEY = re.compile('[a-z0-9]+(?:-[a-z0-9]+)*')
LABELS = 'labels'
_LABELS = LABELS.encode('ascii')

def is_id(value: object) -> bool:
    """Whether `value` is 16 bytes with the version and variant bits of a UUID version 7."""
    return isinstance(value, bytes) and len(value) == ID_LENGTH and value[6] >> 4 == 7 and value[8] >> 6 == 2

def is_domain_key(name: object) -> bool:
    """Whether `name` is a domain key: lowercase letters and digits in groups joined by single hyphens, at most 64."""
    return isinstance(name, str) and len(name) <= DOMAIN_KEY_MOST and DOMAIN_KEY.fullmatch(name) is not None

def key(at: bytes, domain_key: str) -> bytes:
    """The key of a node's part: its id, then the domain key's ASCII bytes."""
    return at + domain_key.encode('ascii')

def is_key(value: object) -> bool:
    if not isinstance(value, bytes) or not ID_LENGTH < len(value) <= ID_LENGTH + DOMAIN_KEY_MOST or not is_id(value[:ID_LENGTH]):
        return False
    try:
        return is_domain_key(value[ID_LENGTH:].decode('ascii'))
    except UnicodeDecodeError:
        return False

def instant(at: bytes) -> int:
    """The existence instant of an id: the milliseconds since the Unix epoch its first six bytes carry."""
    return int.from_bytes(at[:INSTANT_LENGTH], 'big')

def labels_value(ids: Sequence[bytes]) -> bytes:
    """The `labels` part holding `ids`: their concatenation, ascending, without repetition."""
    return b''.join(sorted(set(ids)))

def labels_of(value: bytes) -> tuple[bytes, ...] | None:
    """The labels a `labels` part holds, or None when it is not in the form `labels_value` gives."""
    if len(value) % ID_LENGTH:
        return None
    ids = tuple((value[i:i + ID_LENGTH] for i in range(0, len(value), ID_LENGTH)))
    if not all((is_id(each) for each in ids)) or any((one >= two for one, two in zip(ids, ids[1:]))):
        return None
    return ids

def layable(store: Any) -> bool:
    """Whether `record` can be laid over `store`: a sparse store of any address and any value length."""
    p = store.parameters
    return p.address_length is None and (not p.dense) and (p.value_length is None)

@dataclass(frozen=True)
class Needs:
    """What a class needs of the adapter it is opened on: capabilities, and the least limits it uses (None: none)."""
    capabilities: frozenset = frozenset()
    limits: Limits = field(default_factory=Limits)

    def unmet(self, store: Any) -> list[str]:
        """What `store` declares less of than these needs, each said for a reader; empty when it meets them."""
        missing = [f'the capability `{each.value}`' for each in sorted(self.capabilities - store.capabilities, key=lambda c: c.value)]
        for name in ('writes_per_batch', 'bytes_per_batch', 'bytes_per_value'):
            needed, declared = (getattr(self.limits, name), getattr(store.limits, name))
            if needed is not None and declared is not None and (declared < needed):
                missing.append(f'{name} of {needed} (it declares {declared})')
        return missing

def _page(order: Sequence[bytes], low: int, high: int, after: bytes | None, limit: int | None, descending: bool) -> tuple[bytes, ...]:
    """The page of `order[low:high]` after `after`, ascending, or before it, descending, of at most `limit`."""
    if descending:
        if after is not None:
            high = min(high, bisect.bisect_left(order, after, low, max(low, high)))
        start = low if limit is None else max(low, high - limit)
        return tuple(reversed(order[start:high])) if start < high else ()
    if after is not None:
        low = max(low, bisect.bisect_right(order, after, low, max(low, high)))
    end = high if limit is None else min(high, low + limit)
    return tuple(order[low:end]) if low < end else ()

class _Index:
    """The ids of the nodes and the labels of each, as of the committed state `state`."""

    def __init__(self, state: bytes) -> None:
        self.state = state
        self.ids: list[bytes] = []
        self.known: set[bytes] = set()
        self.labels: dict[bytes, frozenset[bytes]] = {}
        self.carrying: dict[bytes, set[bytes]] = {}

    def apply(self, keys: Sequence[bytes], labels: dict[bytes, bytes]) -> None:
        for each in keys:
            at = each[:ID_LENGTH]
            if at not in self.known:
                self.known.add(at)
                bisect.insort(self.ids, at)
        for at, value in labels.items():
            new, old = (frozenset(labels_of(value) or ()), self.labels.get(at, frozenset()))
            for label in old - new:
                self.carrying[label].discard(at)
            for label in new - old:
                self.carrying.setdefault(label, set()).add(at)
            self.labels[at] = new

class Record:
    """`record` laid over one open handle of a store: the contract's operations over keys, and `parts`, `nodes`, `scan`."""

    def __init__(self, store: Any) -> None:
        if not layable(store):
            raise ValueError('record is laid over a sparse store of any address and value length')
        self.store = store
        self.parameters = Parameters(compare_and_write=store.parameters.compare_and_write)
        self.limits = store.limits
        self.capabilities = store.capabilities
        self._index: _Index | None = None

    def get(self, keys: Sequence[bytes]) -> Any:
        if not all((is_key(each) for each in keys)):
            return Refused(Refusal.MALFORMED, 'a key whose id or domain key is not of the form')
        return self.store.get(keys)

    def list(self, from_: bytes | None=None, to: bytes | None=None, after: bytes | None=None, limit: int | None=None, descending: bool=False) -> Any:
        return self.store.list(from_, to, after, limit, descending)

    def batch(self, expect: Sequence, write: Sequence) -> Any:
        if not all((is_key(at) for at, _ in list(expect) + list(write))):
            return Refused(Refusal.MALFORMED, 'a key whose id or domain key is not of the form')
        if any((at[ID_LENGTH:] == _LABELS and (not isinstance(data, bytes) or labels_of(data) is None) for at, data in write)):
            return Refused(Refusal.MALFORMED, 'a `labels` part that is not ids ascending without repetition')
        return self.store.batch(expect, write)

    def state(self) -> bytes:
        return self.store.state()

    def changes(self, since: bytes) -> Any:
        return self.store.changes(since)

    def stats(self) -> Any:
        return self.store.stats()

    def at_commit_point(self, hook: Any) -> None:
        self.store.at_commit_point(hook)

    def drop_derived_structures(self) -> None:
        self._index = None
        self.store.drop_derived_structures()

    def opener(self) -> Any:
        return self.store.opener()

    def parts(self, ids: Sequence[bytes]) -> Any:
        """For each id, the domain keys its node holds with the token of each, ascending, or Absent, or Unavailable."""
        if not all((is_id(at) for at in ids)):
            return Refused(Refusal.MALFORMED, 'an id that is not of the form')
        while True:
            state = self.store.state()
            held: list[Any] = []
            for at in ids:
                listed = self.store.list(from_=at, to=(int.from_bytes(at, 'big') + 1).to_bytes(ID_LENGTH, 'big'))
                held.append(listed)
            flat = [each for listed in held if isinstance(listed, tuple) for each in listed]
            found = self.store.get(flat) if flat else []
            if self.store.state() != state:
                continue
            if isinstance(found, Unavailable):
                return [found] * len(ids)
            tokens = dict(zip(flat, found))
            answers: list[Any] = []
            for listed in held:
                if not isinstance(listed, tuple):
                    answers.append(listed)
                elif any((isinstance(tokens[each], Unavailable) for each in listed)):
                    answers.append(next((tokens[each] for each in listed if isinstance(tokens[each], Unavailable))))
                else:
                    pairs = tuple(((each[ID_LENGTH:].decode('ascii'), tokens[each].token) for each in listed if not isinstance(tokens[each], Absent)))
                    answers.append(pairs or ABSENT)
            return answers

    def _current(self) -> Any:
        """The index brought up to the store's committed state, or the Unavailable that kept it from it."""
        while True:
            state = self.store.state()
            if self._index is None:
                keys = self.store.list()
                if not isinstance(keys, tuple):
                    return keys
            else:
                if self._index.state == state:
                    return self._index
                keys = self.store.changes(self._index.state)
                if isinstance(keys, Refused):
                    self._index = None
                    continue
            wanted = [each for each in keys if each[ID_LENGTH:] == _LABELS]
            values = self.store.get(wanted) if wanted else []
            if self.store.state() != state:
                continue
            if isinstance(values, Unavailable) or any((isinstance(each, Unavailable) for each in values)):
                return values if isinstance(values, Unavailable) else next((each for each in values if isinstance(each, Unavailable)))
            index = self._index or _Index(state)
            index.apply(keys, {each[:ID_LENGTH]: value.value for each, value in zip(wanted, values) if not isinstance(value, Absent)})
            index.state = state
            self._index = index
            return index

    def _refused(self, from_: Any, to: Any, after: Any, limit: Any) -> Refused | None:
        bounds = [each for each in (from_, to) if each is not None]
        if not all((isinstance(each, int) and (not isinstance(each, bool)) and (0 <= each <= INSTANT_END) for each in bounds)):
            return Refused(Refusal.MALFORMED, 'an instant that is not a whole number of milliseconds of six bytes')
        if from_ is not None and to is not None and (from_ > to):
            return Refused(Refusal.MALFORMED, 'a from after a to')
        if limit is not None and (isinstance(limit, bool) or not isinstance(limit, int) or limit < 1):
            return Refused(Refusal.MALFORMED, 'a limit below one')
        if after is not None and (not is_id(after)):
            return Refused(Refusal.MALFORMED, 'an after that is not an id')
        return None

    def _answer(self, order: Sequence[bytes], from_: int | None, to: int | None, after: bytes | None, limit: int | None, descending: bool) -> tuple[bytes, ...]:
        place = lambda ms: len(order) if ms >= INSTANT_END else bisect.bisect_left(order, ms.to_bytes(INSTANT_LENGTH, 'big'))
        low = 0 if from_ is None else place(from_)
        high = len(order) if to is None else place(to)
        return _page(order, low, max(low, high), after, limit, descending)

    def nodes(self, from_: int | None=None, to: int | None=None, after: bytes | None=None, limit: int | None=None, descending: bool=False) -> Any:
        """The ids whose existence instant lies in `[from_, to)`, paged by `after` and `limit`, ascending or descending."""
        refused = self._refused(from_, to, after, limit)
        if refused:
            return refused
        index = self._current()
        if not isinstance(index, _Index):
            return index
        return self._answer(index.ids, from_, to, after, limit, descending)

    def scan(self, all_of: Sequence[bytes], from_: int | None=None, to: int | None=None, after: bytes | None=None, limit: int | None=None, descending: bool=False) -> Any:
        """As `nodes`, only the ids of nodes whose labels include every id of `all_of`, a set of at least one."""
        if not all_of or not all((is_id(each) for each in all_of)):
            return Refused(Refusal.MALFORMED, 'an all_of that is empty or holds what is not an id')
        refused = self._refused(from_, to, after, limit)
        if refused:
            return refused
        index = self._current()
        if not isinstance(index, _Index):
            return index
        sets = sorted((index.carrying.get(each, set()) for each in set(all_of)), key=len)
        matching = sorted(set(sets[0]).intersection(*sets[1:]))
        return self._answer(matching, from_, to, after, limit, descending)

class RecordAdapter:
    """`record` laid over an adapter: each `open()` a `Record` over a new handle of the adapter's store."""

    def __init__(self, adapter: Any) -> None:
        self.adapter = adapter

    def open(self) -> Record:
        return Record(self.adapter.open())

    def opener(self) -> Any:
        return self.adapter.opener()
