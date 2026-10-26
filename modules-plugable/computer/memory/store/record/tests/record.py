#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests that `record`, laid over a store, keeps the store contract and its own cases.

    python modules-plugable/computer/memory/store/record/tests/record.py

The subject is `record.py`, named for the file that holds it per
[Test Naming](../../../../../../modules/process/test/rules/test-naming/test-naming.md), in the `tests/` folder of the
module that owns it per [Test Placement](../../../../../../modules/process/test/rules/test-placement/test-placement.md).
Its expectations are the cases of [Memory Conformance](../../../../../../modules/computer/memory/conformance/conformance.md),
run through the suite's runner, and `record`'s own group below, the cases of
[Memory Record → The contract suite](../record.md#the-contract-suite): one function each, whose docstring states the case.
`CASES` is the group, so an adapter's own tests run it on `record` laid over that adapter with `group(make, CASES)`.

Nothing here reads or writes a file; the store under `record` is `volatile`, built three ways:

  Sparse         any address and value length, compare-and-write, atomic, no limits.
  Limited        the same with the three limits declared.
  NotAtomic      the same, not atomic.

The contract's suite runs on each through `Addressed`, which turns each of the suite's addresses into one key of a fixed
id, the domain key `k` and the address in hexadecimal, so that equality and the byte order are kept and every call goes
through `record` ([Memory Record Handoff](../record.handoff.md#decisions)). The group runs on each as it is.
"""
from __future__ import annotations
import random
import sys
import threading
import unittest
from importlib import import_module
from pathlib import Path
from typing import Any, Callable
TESTS = Path(__file__).resolve().parent
TOP = next((p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()))
sys.path.insert(0, str(TOP))
sys.dont_write_bytecode = True
_m_store = import_module('modules.computer.memory.store.protocol.store')
_m_volatile = import_module('modules.computer.memory.volatile.volatile')
_m_conformance = import_module('modules.computer.memory.conformance.conformance')
_m_record = import_module('modules-plugable.computer.memory.store.record.record')
ABSENT = _m_store.ABSENT
Capability = _m_store.Capability
Case = _m_conformance.Case
Committed = _m_store.Committed
Conflict = _m_store.Conflict
Found = _m_store.Found
Limits = _m_store.Limits
Parameters = _m_store.Parameters
Refusal = _m_store.Refusal
Refused = _m_store.Refused
token = _m_store.token
Volatile = _m_volatile.Volatile
OWED = _m_conformance.OWED
LABELS = _m_record.LABELS
RecordAdapter = _m_record.RecordAdapter
key = _m_record.key
labels_value = _m_record.labels_value

def ident(ms: int, n: int) -> bytes:
    """A UUID version 7 whose existence instant is `ms` and whose other bits are made from `n`."""
    b = n.to_bytes(10, 'big')
    return ms.to_bytes(6, 'big') + bytes([112 | b[0] & 15]) + b[1:2] + bytes([128 | b[2] & 63]) + b[3:10]

def node_writes(at: bytes, parts: dict[str, bytes]) -> list[tuple[bytes, bytes]]:
    return [(key(at, name), data) for name, data in sorted(parts.items())]

def commit(t: unittest.TestCase, store: Any, writes: list[tuple[bytes, bytes]], expect: list | None=None) -> None:
    t.assertEqual(store.batch(expect or [], writes), Committed())

def write_nodes(t: unittest.TestCase, store: Any, nodes: list[tuple[bytes, dict[str, bytes]]]) -> None:
    """Write nodes in batches the store takes: one write per batch when it is not atomic."""
    writes = [w for at, parts in nodes for w in node_writes(at, parts)]
    per = 100 if Capability.ATOMIC_BATCH in store.capabilities else 1
    if store.limits.writes_per_batch:
        per = min(per, store.limits.writes_per_batch)
    for start in range(0, len(writes), per):
        commit(t, store, writes[start:start + per])

def page_all(call: Callable[..., Any], limit: int, descending: bool) -> list[bytes]:
    seen: list[bytes] = []
    after = None
    while True:
        page = list(call(after=after, limit=limit, descending=descending))
        seen += page
        if len(page) < limit:
            return seen
        after = page[-1]

def atomic(store: Any) -> bool:
    return Capability.ATOMIC_BATCH in store.capabilities

def parts_are_independent(t: unittest.TestCase, make: Callable[[], Any]) -> None:
    """`parts-are-independent`: writing one domain key leaves the node's other parts and other nodes unchanged."""
    store = make().open()
    x, y = (ident(1000, 1), ident(1000, 2))
    write_nodes(t, store, [(x, {'alpha': b'1', 'beta': b'2'}), (y, {'alpha': b'3'})])
    before = store.get([key(x, 'beta'), key(y, 'alpha')])
    commit(t, store, [(key(x, 'alpha'), b'changed')])
    t.assertEqual(store.get([key(x, 'beta'), key(y, 'alpha')]), before)
    t.assertEqual(store.get([key(x, 'alpha')]), [Found(b'changed', token(b'changed'))])

def parts_lists_keys_and_tokens(t: unittest.TestCase, make: Callable[[], Any]) -> None:
    """`parts-lists-keys-and-tokens`: `parts` names every key the node holds with its token and answers Absent for a node holding none."""
    store = make().open()
    x, label = (ident(2000, 1), ident(5, 9))
    held = {'alpha': b'a', 'beta': b'', LABELS: labels_value([label])}
    write_nodes(t, store, [(x, held)])
    t.assertEqual(store.parts([x, ident(2000, 2)]), [tuple(((name, token(data)) for name, data in sorted(held.items()))), ABSENT])

def batch_malformed_refused(t: unittest.TestCase, make: Callable[[], Any]) -> None:
    """`batch-malformed-refused`, the half that stayed: an invalid domain key, and a `labels` value unsorted or with a repeated id, are each refused with nothing applied; and of `expect-holds-pass-and-conflict`, that a conflict leaves every part and label as it was."""
    store = make().open()
    x, one, two = (ident(3000, 1), ident(1, 1), ident(2, 2))
    write_nodes(t, store, [(x, {'alpha': b'a', LABELS: labels_value([one])})])
    every = [key(x, 'alpha'), key(x, LABELS)]
    before = store.get(every)
    for write in ([(x + b'Bad', b'v')], [(key(x, LABELS), two + one)], [(key(x, LABELS), one + one)], [(key(x, LABELS), one + b'\x00')]):
        t.assertEqual(store.batch([], write), Refused(Refusal.MALFORMED), write)
        t.assertEqual(store.get(every), before)
    if store.parameters.compare_and_write and atomic(store):
        stale = token(b'stale')
        t.assertEqual(store.batch([(key(x, 'alpha'), stale)], [(key(x, 'alpha'), b'b'), (key(x, LABELS), labels_value([two]))]), Conflict(0))
        t.assertEqual(store.get(every), before)
        t.assertEqual(store.scan([one]), (x,))

def batch_visible_whole(t: unittest.TestCase, make: Callable[[], Any]) -> None:
    """`batch-visible-whole`, the half that stayed: while one thread commits batches that write two parts and a label together, another reading them in one `parts` call and by `scan` on that label never finds them inconsistent, over 10,000 rounds."""
    adapter = make()
    writer, reader = (adapter.open(), adapter.open())
    if not atomic(writer):
        return
    label = ident(7, 7)
    nodes = [ident(4000, i) for i in range(64)]
    rounds, faults = (10000, [])

    def write() -> None:
        for n in range(rounds):
            at, data = (nodes[n % len(nodes)], n.to_bytes(4, 'big'))
            if writer.batch([], node_writes(at, {'alpha': data, 'beta': data, LABELS: labels_value([label])})) != Committed():
                faults.append(('batch', n))

    def whole(answer: Any) -> bool:
        if answer is ABSENT:
            return True
        tokens = dict(answer)
        return set(tokens) == {'alpha', 'beta', LABELS} and tokens['alpha'] == tokens['beta']
    thread = threading.Thread(target=write)
    thread.start()
    while thread.is_alive():
        answer, = reader.parts([random.choice(nodes)])
        if not whole(answer):
            faults.append(('parts', answer))
        for at in reader.scan([label]):
            later, = reader.parts([at])
            if later is ABSENT or not whole(later):
                faults.append(('scan', at, later))
    thread.join()
    t.assertEqual(faults, [])

def labels_set_and_scan(t: unittest.TestCase, make: Callable[[], Any]) -> None:
    """`labels-set-and-scan`: a node with labels is found by `scan` for each and for any subset of them, not for an id it lacks, and not after its label set is rewritten without it."""
    store = make().open()
    x, other = (ident(5000, 1), ident(5000, 2))
    a, b, c, lacking = (ident(1, 1), ident(1, 2), ident(1, 3), ident(1, 4))
    write_nodes(t, store, [(x, {LABELS: labels_value([a, b, c])}), (other, {LABELS: labels_value([b])})])
    for subset in ([a], [b, c], [a, b, c], [c, a]):
        t.assertIn(x, store.scan(subset), subset)
    t.assertEqual(store.scan([b]), (x, other))
    t.assertEqual(store.scan([lacking]), ())
    t.assertEqual(store.scan([a, lacking]), ())
    commit(t, store, [(key(x, LABELS), labels_value([b]))])
    t.assertEqual(store.scan([a]), ())
    t.assertEqual(store.scan([b]), (x, other))

def scan_pages_complete(t: unittest.TestCase, make: Callable[[], Any]) -> None:
    """`scan-pages-complete`: paging with a small limit visits each matching id once while other ids are written, ascending and descending, and descending paging by `scan` with `after` set to the last id returned visits every id once."""
    adapter = make()
    store, other = (adapter.open(), adapter.open())
    label, unrelated = (ident(9, 1), ident(9, 2))
    chance = random.Random(20261026)
    matching = sorted((ident(chance.randrange(1, 10 ** 6), i) for i in range(300)))
    write_nodes(t, store, [(at, {LABELS: labels_value([label])}) for at in matching])
    for descending in (False, True):
        written = [0]

        def call(**options: Any) -> Any:
            n = written[0] = written[0] + 1
            fresh = ident(chance.randrange(1, 10 ** 6), 10000 + n + (100000 if descending else 0))
            commit(t, other, [(key(fresh, LABELS), labels_value([label if n % 2 else unrelated]))])
            return store.scan([label], **options)
        seen = page_all(call, 7, descending)
        t.assertEqual(len(seen), len(set(seen)))
        t.assertTrue(set(matching) <= set(seen))
        t.assertEqual(seen, sorted(seen, reverse=descending))

def list_ignores_adapter_boundaries(t: unittest.TestCase, make: Callable[[], Any]) -> None:
    """`list-ignores-adapter-boundaries`: with ids whose instants are the Unix epoch, the instant before and after a month, a leap day, the turn of a year, the year 2100, and many ids within one second, any range of instants and paging answers as the model does (`nodes`, which the first design called `list`)."""
    store = make().open()
    month, leap_day, new_year, y2100 = (1769904000000, 1709164800000, 1767225600000, 4102444800000)
    instants = [0, 1, month - 1, month, leap_day, leap_day + 86399999, leap_day + 86400000, new_year - 1, new_year, y2100]
    instants += [1761480000000 + i * 5 for i in range(200)]
    ids = sorted((ident(ms, n) for n, ms in enumerate(instants)))
    write_nodes(t, store, [(at, {'content': b'x'}) for at in ids])
    instant = lambda at: int.from_bytes(at[:6], 'big')
    bounds = sorted({0, 1, month, leap_day, new_year, y2100, y2100 + 1, 1761480000000, 1761480000500, 2 ** 48})
    chance = random.Random(20261026)
    for _ in range(200):
        low, high = sorted(chance.sample(bounds, 2))
        model = [at for at in ids if low <= instant(at) < high]
        t.assertEqual(list(store.nodes(from_=low, to=high)), model)
        for descending in (False, True):
            limit = chance.randint(1, 9)
            t.assertEqual(page_all(lambda **o: store.nodes(from_=low, to=high, **o), limit, descending), model[::-1] if descending else model)
    t.assertEqual(list(store.nodes()), ids)

def id_form_refused(t: unittest.TestCase, make: Callable[[], Any]) -> None:
    """`id-form-refused`: 16 bytes whose version or variant bits are not those of a UUID version 7 are refused in a key, a label and an expectation."""
    store = make().open()
    good = ident(6000, 1)
    version_4 = good[:6] + bytes([64 | good[6] & 15]) + good[7:]
    variant_11 = good[:8] + bytes([192 | good[8] & 63]) + good[9:]
    variant_0 = good[:8] + bytes([good[8] & 63]) + good[9:]
    for bad in (version_4, variant_11, variant_0, bytes(16)):
        t.assertEqual(store.get([key(bad, 'alpha')]), Refused(Refusal.MALFORMED))
        t.assertEqual(store.batch([], [(key(bad, 'alpha'), b'v')]), Refused(Refusal.MALFORMED))
        t.assertEqual(store.batch([], [(key(good, LABELS), bad)]), Refused(Refusal.MALFORMED))
        if store.parameters.compare_and_write:
            t.assertEqual(store.batch([(key(bad, 'alpha'), ABSENT)], [(key(good, 'alpha'), b'v')]), Refused(Refusal.MALFORMED))
        t.assertEqual(store.parts([bad]), Refused(Refusal.MALFORMED))
        t.assertEqual(store.scan([bad]), Refused(Refusal.MALFORMED))
        t.assertEqual(store.nodes(after=bad), Refused(Refusal.MALFORMED))
    t.assertEqual(store.get([key(good, 'alpha')]), [ABSENT])

def domain_key_charset(t: unittest.TestCase, make: Callable[[], Any]) -> None:
    """`domain-key-charset`: keys at the edge of the charset are accepted, and a key that is empty, has an upper-case letter, a hyphen at an end, a slash, a dot, a control character or 65 characters is refused."""
    store = make().open()
    at = ident(7000, 1)
    for name in ('a', '0', 'a-b', 'z9-0a-b', 'a' * 64, 'a' + '-b' * 31 + 'c'):
        t.assertEqual(store.batch([], [(key(at, name), b'v')]), Committed(), name)
        t.assertEqual(store.get([key(at, name)]), [Found(b'v', token(b'v'))], name)
    for name in ('', 'A', 'aB', '-a', 'a-', 'a--b', 'a/b', 'a.b', 'a\x01', 'a b', 'a' * 65, 'é'):
        address = at + name.encode('utf-8')
        t.assertEqual(store.batch([], [(address, b'v')]), Refused(Refusal.MALFORMED), name)
        t.assertEqual(store.get([address]), Refused(Refusal.MALFORMED), name)

def read_inputs_refused(t: unittest.TestCase, make: Callable[[], Any]) -> None:
    """`read-inputs-refused`, the half that stayed: a `get`, `parts`, `nodes` or `scan` with an invalid domain key or an empty `all_of` is Refused and answers nothing; and so is `nodes` or `scan` with a `limit` below one or a `from` after a `to`."""
    store = make().open()
    at, label = (ident(8000, 1), ident(1, 1))
    t.assertIsInstance(store.get([key(at, 'alpha'), at + b'Bad']), Refused)
    t.assertIsInstance(store.parts([at, at[:15]]), Refused)
    t.assertIsInstance(store.scan([]), Refused)
    for call in (store.nodes, lambda **o: store.scan([label], **o)):
        t.assertIsInstance(call(limit=0), Refused)
        t.assertIsInstance(call(from_=2, to=1), Refused)
        t.assertIsInstance(call(from_=-1), Refused)

def many_nodes(t: unittest.TestCase, make: Callable[[], Any]) -> None:
    """`many-nodes`, the half that stayed: 10,000 nodes are found by `scan` as written."""
    store = make().open()
    label = ident(3, 3)
    ids = [ident(9000 + i // 7, i) for i in range(10000)]
    write_nodes(t, store, [(at, {'alpha': i.to_bytes(4, 'big'), LABELS: labels_value([label])}) for i, at in enumerate(ids)])
    t.assertEqual(store.scan([label]), tuple(sorted(ids)))
    t.assertEqual(store.nodes(), tuple(sorted(ids)))

def derived_structures_droppable(t: unittest.TestCase, make: Callable[[], Any]) -> None:
    """`derived-structures-droppable`, the half that stayed: dropping the label index and repeating a sequence of `scan` calls changes no answer."""
    store = make().open()
    labels = [ident(4, i) for i in range(4)]
    ids = [ident(10000 + i, i) for i in range(50)]
    write_nodes(t, store, [(at, {LABELS: labels_value([labels[i % 4], labels[i % 3]])}) for i, at in enumerate(ids)])

    def answers() -> list:
        return [store.scan([labels[0]]), store.scan([labels[1], labels[2]], limit=3, descending=True), store.scan([labels[3]], from_=10010, to=10030), store.nodes(after=ids[20], limit=5), store.parts(ids[:3])]
    before = answers()
    store.drop_derived_structures()
    t.assertEqual(answers(), before)

def one_process_sees_the_others_commit(t: unittest.TestCase, make: Callable[[], Any]) -> None:
    """`one-process-sees-the-others-commit`, the half that stayed, between two handles: a call of `parts` and `scan` that begins after another handle's batch returned sees it, including a label that batch set, whatever index the first handle held."""
    adapter = make()
    first, second = (adapter.open(), adapter.open())
    at, label = (ident(11000, 1), ident(5, 5))
    t.assertEqual(first.scan([label]), ())
    t.assertEqual(first.parts([at]), [ABSENT])
    write_nodes(t, second, [(at, {'alpha': b'a', LABELS: labels_value([label])})])
    t.assertEqual(first.scan([label]), (at,))
    t.assertEqual(first.parts([at]), [(('alpha', token(b'a')), (LABELS, token(labels_value([label]))))])

def one_process_sees_the_others_commit_across_processes(t: unittest.TestCase, make: Callable[[], Any]) -> None:
    """`one-process-sees-the-others-commit`, the half that stayed, across processes: a call of `parts` and `scan` that begins after another process's batch returned sees it, including a label that batch set."""
    adapter = make()
    store = adapter.open()
    at, label = (ident(12000, 1), ident(6, 6))
    t.assertEqual(store.scan([label]), ())
    process = _m_conformance.child_batch(adapter, [], node_writes(at, {'alpha': b'a', LABELS: labels_value([label])}))
    t.assertEqual(process.communicate(timeout=120)[0].split(), ['Committed'])
    t.assertEqual(store.scan([label]), (at,))
    t.assertNotEqual(store.parts([at]), [ABSENT])
CASES = [Case('record', lambda store: True, check) for check in (parts_are_independent, parts_lists_keys_and_tokens, batch_malformed_refused, batch_visible_whole, labels_set_and_scan, scan_pages_complete, list_ignores_adapter_boundaries, id_form_refused, domain_key_charset, read_inputs_refused, many_nodes, derived_structures_droppable, one_process_sees_the_others_commit)]
CASES.append(Case('record-shared', lambda store: Capability.SHARED_BETWEEN_PROCESSES in store.capabilities, one_process_sees_the_others_commit_across_processes))

def group(make: Callable[[], Any], cases: list[Case]) -> type[unittest.TestCase]:
    """A TestCase class with one test for each of `cases` that applies to the `record` stores `make` opens."""
    probe = make().open()
    attributes: dict[str, Any] = {}
    for each in cases:
        if each.applies(probe):

            def method(self: unittest.TestCase, check: Callable=each.check) -> None:
                check(self, make)
            method.__doc__ = each.check.__doc__
            attributes['test_' + each.check.__name__] = method
    return type('RecordGroup', (unittest.TestCase,), attributes)
FIXED = ident(1761480000000, 1)

def to_key(address: bytes | None) -> bytes | None:
    return None if address is None else key(FIXED, 'k' + address.hex())

def from_key(found: bytes) -> bytes:
    return bytes.fromhex(found[17:].decode('ascii'))

class AddressedStore:
    """A `record` handle seen by the contract's suite: each of its addresses is the key `to_key` makes of it."""

    def __init__(self, record: Any) -> None:
        self.record = record
        self.parameters, self.limits, self.capabilities = (record.parameters, record.limits, record.capabilities)

    def get(self, addresses: Any) -> Any:
        return self.record.get([to_key(at) for at in addresses])

    def list(self, from_: bytes | None=None, to: bytes | None=None, after: bytes | None=None, limit: int | None=None, descending: bool=False) -> Any:
        answer = self.record.list(to_key(from_) if from_ is not None else FIXED, to_key(to), to_key(after), limit, descending)
        return tuple((from_key(at) for at in answer)) if isinstance(answer, tuple) else answer

    def batch(self, expect: Any, write: Any) -> Any:
        return self.record.batch([(to_key(at), e) for at, e in expect], [(to_key(at), data) for at, data in write])

    def state(self) -> bytes:
        return self.record.state()

    def changes(self, since: bytes) -> Any:
        answer = self.record.changes(since)
        return tuple((from_key(at) for at in answer)) if isinstance(answer, tuple) else answer

    def stats(self) -> Any:
        return self.record.stats()

    def at_commit_point(self, hook: Any) -> None:
        self.record.at_commit_point(hook)

    def drop_derived_structures(self) -> None:
        self.record.drop_derived_structures()

class Addressed:
    """The adapter the contract's suite takes: `record` laid over `adapter`, seen through `AddressedStore`."""

    def __init__(self, adapter: Any) -> None:
        self.adapter = RecordAdapter(adapter)

    def open(self) -> AddressedStore:
        return AddressedStore(self.adapter.open())
INSTANCES = {'Sparse': (Limits(), True), 'Limited': (Limits(writes_per_batch=50, bytes_per_batch=1 << 21, bytes_per_value=1 << 20), True), 'NotAtomic': (Limits(), False)}
for _name, (_limits, _atomic) in INSTANCES.items():
    _make = lambda l=_limits, a=_atomic: Volatile(Parameters(), l, atomic_batch=a)
    globals()[_name] = type(_name, (_m_conformance.test_case(lambda m=_make: Addressed(m())),), {})
    globals()[_name + 'Record'] = type(_name + 'Record', (group(lambda m=_make: RecordAdapter(m()), CASES),), {})

class EveryCaseRuns(unittest.TestCase):

    def test_every_record_case_but_the_shared_one_runs_on_volatile(self) -> None:
        probe = RecordAdapter(Volatile()).open()
        t = [each.check.__name__ for each in CASES if not each.applies(probe)]
        self.assertEqual(t, ['one_process_sees_the_others_commit_across_processes'])
        self.assertNotIn(OWED, one_process_sees_the_others_commit_across_processes.__doc__)
if __name__ == '__main__':
    unittest.main()
