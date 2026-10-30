#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
TIER = 'unit'
BUDGET_SECONDS = 60
import ast
import enum
import io
import tokenize
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
LABELS = _m_record.LABELS
RecordAdapter = _m_record.RecordAdapter
key = _m_record.key
labels_value = _m_record.labels_value

def ident(ms: int, n: int) -> bytes:
    b = n.to_bytes(10, 'big')
    return ms.to_bytes(6, 'big') + bytes([112 | b[0] & 15]) + b[1:2] + bytes([128 | b[2] & 63]) + b[3:10]

def node_writes(at: bytes, parts: dict[str, bytes]) -> list[tuple[bytes, bytes]]:
    return [(key(at, name), data) for name, data in sorted(parts.items())]

def commit(t: unittest.TestCase, store: Any, writes: list[tuple[bytes, bytes]], expect: list | None=None) -> None:
    t.assertEqual(store.batch(expect or [], writes), Committed())

def write_nodes(t: unittest.TestCase, store: Any, nodes: list[tuple[bytes, dict[str, bytes]]]) -> None:
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
    store = make().open()
    x, y = (ident(1000, 1), ident(1000, 2))
    write_nodes(t, store, [(x, {'alpha': b'1', 'beta': b'2'}), (y, {'alpha': b'3'})])
    before = store.get([key(x, 'beta'), key(y, 'alpha')])
    commit(t, store, [(key(x, 'alpha'), b'changed')])
    t.assertEqual(store.get([key(x, 'beta'), key(y, 'alpha')]), before)
    t.assertEqual(store.get([key(x, 'alpha')]), [Found(b'changed', token(b'changed'))])

def parts_lists_keys_and_tokens(t: unittest.TestCase, make: Callable[[], Any]) -> None:
    store = make().open()
    x, label = (ident(2000, 1), ident(5, 9))
    held = {'alpha': b'a', 'beta': b'', LABELS: labels_value([label])}
    write_nodes(t, store, [(x, held)])
    t.assertEqual(store.parts([x, ident(2000, 2)]), [tuple(((name, token(data)) for name, data in sorted(held.items()))), ABSENT])

def batch_malformed_refused(t: unittest.TestCase, make: Callable[[], Any]) -> None:
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
    store = make().open()
    label = ident(3, 3)
    ids = [ident(9000 + i // 7, i) for i in range(10000)]
    write_nodes(t, store, [(at, {'alpha': i.to_bytes(4, 'big'), LABELS: labels_value([label])}) for i, at in enumerate(ids)])
    t.assertEqual(store.scan([label]), tuple(sorted(ids)))
    t.assertEqual(store.nodes(), tuple(sorted(ids)))

def derived_structures_droppable(t: unittest.TestCase, make: Callable[[], Any]) -> None:
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
    adapter = make()
    first, second = (adapter.open(), adapter.open())
    at, label = (ident(11000, 1), ident(5, 5))
    t.assertEqual(first.scan([label]), ())
    t.assertEqual(first.parts([at]), [ABSENT])
    write_nodes(t, second, [(at, {'alpha': b'a', LABELS: labels_value([label])})])
    t.assertEqual(first.scan([label]), (at,))
    t.assertEqual(first.parts([at]), [(('alpha', token(b'a')), (LABELS, token(labels_value([label]))))])

def one_process_sees_the_others_commit_across_processes(t: unittest.TestCase, make: Callable[[], Any]) -> None:
    adapter = make()
    store = adapter.open()
    at, label = (ident(12000, 1), ident(6, 6))
    t.assertEqual(store.scan([label]), ())
    process = _m_conformance.child_batch(adapter, [], node_writes(at, {'alpha': b'a', LABELS: labels_value([label])}))
    t.assertEqual(process.communicate(timeout=120)[0].split(), ['Committed'])
    t.assertEqual(store.scan([label]), (at,))
    t.assertNotEqual(store.parts([at]), [ABSENT])
CASES = [Case('record', lambda store: True, check) for check in (parts_are_independent, parts_lists_keys_and_tokens, batch_malformed_refused, batch_visible_whole, labels_set_and_scan, scan_pages_complete, list_ignores_adapter_boundaries, id_form_refused, domain_key_charset, read_inputs_refused, many_nodes, derived_structures_droppable, one_process_sees_the_others_commit)]
CASES.append(Case('record-shared', lambda store: Capability.SHARED_BETWEEN_PROCESSES in store.capabilities, one_process_sees_the_others_commit_across_processes, budget=120, cost=_m_conformance.Cost(subprocesses=1)))

def group(make: Callable[[], Any], cases: list[Case]) -> type[unittest.TestCase]:
    probe = make().open()
    attributes: dict[str, Any] = {}
    for each in cases:
        if each.applies(probe):

            def method(self: unittest.TestCase, check: Callable=each.check) -> None:
                check(self, make)
            attributes['test_' + each.check.__name__] = method
    return type('RecordGroup', (unittest.TestCase,), attributes)
FIXED = ident(1761480000000, 1)

def to_key(address: bytes | None) -> bytes | None:
    return None if address is None else key(FIXED, 'k' + address.hex())

def from_key(found: bytes) -> bytes:
    return bytes.fromhex(found[17:].decode('ascii'))

class AddressedStore:

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
def bare(path):
    source = Path(path).read_text(encoding='utf-8')
    comments = [t.start[0] for t in tokenize.generate_tokens(io.StringIO(source).readline) if t.type == tokenize.COMMENT and t.start[0] > 2]
    documented = [getattr(n, 'lineno', 0) for n in ast.walk(ast.parse(source)) if isinstance(n, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) and ast.get_docstring(n, clean=False) is not None]
    return (comments, documented)

def own_error_types(module):
    return sorted((name for name, each in vars(module).items() if isinstance(each, type) and each.__module__ == module.__name__ and (issubclass(each, (BaseException, enum.Enum)) or 'Refus' in name)))

_m_store_errors = import_module('modules.computer.memory.store.errors.errors')

def errors_module():
    return import_module('modules-plugable.computer.memory.store.record.errors.errors')

class Closing(Volatile):
    closed = 0

    def close(self) -> None:
        self.closed += 1

class ClosingAdapter:

    def __init__(self) -> None:
        self.opened = []

    def open(self) -> Closing:
        self.opened.append(Closing())
        return self.opened[-1]

    def opener(self):
        return None

class ErrorsFolder(unittest.TestCase):

    def test_the_errors_are_declared_in_the_errors_folder(self) -> None:
        errors = errors_module()
        self.assertEqual([each.name for each in errors.Bad], ['KEY', 'ID', 'LABELS', 'INSTANT', 'BOUNDS', 'LIMIT', 'ALL_OF'])
        self.assertTrue(all((each.summary() for each in errors.Bad)))
        self.assertTrue(issubclass(errors.NotLayable, ValueError))
        self.assertTrue(issubclass(errors.NotLayable, _m_store_errors.Raised))

    def test_record_defines_no_error_type_of_its_own(self) -> None:
        self.assertEqual(own_error_types(_m_record), [])

    def test_each_refusal_of_record_is_malformed_with_the_declared_error_as_its_detail(self) -> None:
        errors = errors_module()
        record = RecordAdapter(Volatile()).open()
        at = ident(1, 1)
        said = [(record.get([b'not a key']), errors.Bad.KEY), (record.batch([], [(b'not a key', b'x')]), errors.Bad.KEY), (record.batch([], [(key(at, LABELS), b'x')]), errors.Bad.LABELS), (record.parts([b'x']), errors.Bad.ID), (record.nodes(after=b'x'), errors.Bad.ID), (record.nodes(from_=-1), errors.Bad.INSTANT), (record.nodes(from_=5, to=2), errors.Bad.BOUNDS), (record.nodes(limit=0), errors.Bad.LIMIT), (record.scan([]), errors.Bad.ALL_OF)]
        for answer, why in said:
            with self.subTest(why=why):
                self.assertEqual(answer, Refused(Refusal.MALFORMED))
                self.assertEqual(answer.detail, why.summary())

    def test_a_store_record_cannot_be_laid_over_raises_the_declared_error(self) -> None:
        errors = errors_module()
        with self.assertRaises(errors.NotLayable) as raised:
            _m_record.Record(Volatile(Parameters(address_length=4)))
        self.assertIsInstance(raised.exception, ValueError)
        self.assertEqual(raised.exception.reason, Refusal.MALFORMED)

class Closes(unittest.TestCase):

    def test_closing_a_record_closes_the_store_it_is_laid_over(self) -> None:
        store = Closing()
        _m_record.Record(store).close()
        self.assertEqual(store.closed, 1)

    def test_closing_a_record_over_a_store_with_nothing_to_close_is_quiet(self) -> None:
        _m_record.Record(Volatile()).close()

    def test_a_record_the_adapter_opens_is_closable(self) -> None:
        adapter = ClosingAdapter()
        RecordAdapter(adapter).open().close()
        self.assertEqual([each.closed for each in adapter.opened], [1])

class NoComments(unittest.TestCase):

    def test_the_files_carry_no_comment_and_no_docstring(self) -> None:
        for path in (_m_record.__file__, errors_module().__file__, __file__):
            with self.subTest(path=Path(path).name):
                self.assertEqual(bare(path), ([], []))
if __name__ == '__main__':
    unittest.main()
