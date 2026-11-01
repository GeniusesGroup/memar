#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import struct
from dataclasses import dataclass
from importlib import import_module
from typing import Any, Sequence
_m_store = import_module('modules.computer.memory.store.protocol.store')
_m_errors = import_module('modules-plugable.computer.memory.store.graph.errors.errors')
_m_layout_value = import_module('modules-plugable.computer.memory.store.graph.codecs.layout_value')
_m_address = import_module('modules-plugable.computer.memory.store.graph.address')
_m_side = import_module('modules-plugable.computer.memory.store.graph.side_structural')
ABSENT = _m_store.ABSENT
Absent = _m_store.Absent
Committed = _m_store.Committed
Conflict = _m_store.Conflict
Found = _m_store.Found
Parameters = _m_store.Parameters
Refusal = _m_store.Refusal
Refused = _m_store.Refused
Unavailable = _m_store.Unavailable
token = _m_store.token
Bad = _m_errors.Bad
NotLayable = _m_errors.NotLayable
Graph_Default_Layout_Value_Codec = _m_layout_value.Graph_Default_Layout_Value_Codec
Stored_Side = _m_layout_value.Stored_Side
Stored_Edge_Value = _m_layout_value.Stored_Edge_Value
LAYOUT_COMPACT = 1
LAYOUT_PER_EDGE = 2
DIRECTION_OUT = 1
DIRECTION_IN = 2
DIRECTION_EITHER = 3
PATH_TRAIL = 1
PATH_ACYCLIC = 2
_TAG_LAYOUT = _m_address.TAG_LAYOUT
_TAG_COMPACT = _m_address.TAG_COMPACT
_TAG_PER_EDGE = _m_address.TAG_PER_EDGE
_TAG_IN_COMPACT = _m_address.TAG_IN_COMPACT
_TAG_IN_PER_EDGE = _m_address.TAG_IN_PER_EDGE
_U64 = struct.Struct('>Q')
_LAYOUT_VALUES = Graph_Default_Layout_Value_Codec()
_pack = _m_address.pack
_take = _m_address.take

def layable(store: Any) -> bool:
    p = store.parameters
    return p.address_length is None and (not p.dense) and (p.value_length is None)

@dataclass(frozen=True)
class Graph_PutEdge:
    Layout: int
    From: bytes
    Relation: bytes
    To: bytes
    ReverseRelation: bytes = b''
    Fields: bytes = b''
    ExpectFrom: bytes = b''
    ExpectTo: bytes = b''

@dataclass(frozen=True)
class Graph_ListSidesQuery:
    From: bytes
    Relation: bytes
    After: bytes = b''
    Limit: int = 0
    Descending: bool = False

@dataclass(frozen=True)
class Graph_Side:
    Ref: bytes
    To: bytes
    Fields: bytes
    Token: bytes

@dataclass(frozen=True)
class Graph_GetSideQuery:
    From: bytes
    Relation: bytes
    To: bytes

@dataclass(frozen=True)
class Graph_GetSideAnswer:
    Found: bool
    Ref: bytes = b''
    Fields: bytes = b''
    Token: bytes = b''
    Err: Any = None

@dataclass(frozen=True)
class Graph_Pattern_Step:
    Direction: int
    Relation: bytes
    FromSlot: int
    ToSlot: int
    FieldPrefix: bytes = b''
    RequireFieldPrefix: bool = False

@dataclass(frozen=True)
class Graph_Pattern:
    SlotCount: int
    Steps: list
    BoundSlot: int = 0
    BoundVertex: bytes = b''
    HasBound: bool = False
    Limit: int = 0

@dataclass(frozen=True)
class Graph_Path_Query:
    From: bytes
    Relation: bytes
    Direction: int
    MinHops: int
    MaxHops: int
    Mode: int
    Limit: int = 0

@dataclass(frozen=True)
class Graph_Binding:
    Slot: int
    Vertex: bytes
    Side: bytes = b''
    HasSide: bool = False

class Graph_Store:

    def __init__(self, store: Any, layout: int) -> None:
        if not layable(store):
            raise NotLayable(NotLayable().summary())
        if layout not in (LAYOUT_COMPACT, LAYOUT_PER_EDGE):
            raise NotLayable(Bad.LAYOUT.summary())
        self.store = store
        self.layout = layout
        self.parameters = Parameters(compare_and_write=store.parameters.compare_and_write)
        self.limits = store.limits
        self.capabilities = store.capabilities

    def get(self, addresses: Sequence[bytes]) -> Any:
        return self.store.get(addresses)

    def list(self, from_: bytes | None=None, to: bytes | None=None, after: bytes | None=None, limit: int | None=None, descending: bool=False) -> Any:
        return self.store.list(from_, to, after, limit, descending)

    def batch(self, expect: Sequence, write: Sequence) -> Any:
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
        self.store.drop_derived_structures()

    def opener(self) -> Any:
        return self.store.opener()

    def close(self) -> None:
        close = getattr(self.store, 'close', None)
        if callable(close):
            close()

    def _layout_key(self, frm: bytes, relation: bytes) -> bytes:
        return bytes([_TAG_LAYOUT]) + _pack([frm, relation])

    def _adj_key(self, tag: int, frm: bytes, relation: bytes) -> bytes:
        return bytes([tag]) + _pack([frm, relation])

    def _per_edge_prefix(self, tag: int, frm: bytes, relation: bytes) -> bytes:
        return bytes([tag]) + _pack([frm, relation])

    def _per_edge_key(self, tag: int, frm: bytes, relation: bytes, slot: int) -> bytes:
        return self._per_edge_prefix(tag, frm, relation) + _U64.pack(slot)

    def _side_ref(self, tag: int, frm: bytes, relation: bytes, slot: int) -> bytes:
        return self._adj_key(tag, frm, relation) + _U64.pack(slot) if tag in (_TAG_COMPACT, _TAG_IN_COMPACT) else self._per_edge_key(tag, frm, relation, slot)

    def _parse_side_ref(self, ref: bytes) -> tuple[int, bytes, bytes, int] | None:
        if not ref or ref[0] not in (_TAG_COMPACT, _TAG_PER_EDGE, _TAG_IN_COMPACT, _TAG_IN_PER_EDGE):
            return None
        try:
            frm, at = _take(ref, 1)
            relation, at = _take(ref, at)
            if at + 8 != len(ref):
                return None
            slot = _U64.unpack_from(ref, at)[0]
            return (ref[0], frm, relation, slot)
        except (struct.error, IndexError):
            return None

    def _read(self, key: bytes) -> Any:
        answer = self.store.get([key])
        if isinstance(answer, Refused):
            return answer
        return answer[0]

    def _check_layout(self, frm: bytes, relation: bytes, layout: int, markers: dict[bytes, bytes]) -> Any:
        key = self._layout_key(frm, relation)
        if key in markers:
            return None if markers[key] == bytes([layout]) else Refused(Refusal.MALFORMED, Bad.LAYOUT.summary())
        held = self._read(key)
        if isinstance(held, (Refused, Unavailable)):
            return held
        if isinstance(held, Absent):
            markers[key] = bytes([layout])
            return None
        if held.value[:1] != bytes([layout]):
            return Refused(Refusal.MALFORMED, Bad.LAYOUT.summary())
        markers[key] = held.value
        return None

    def _next_slot_compact(self, sides: Sequence[Stored_Side]) -> int:
        return max((each.slot for each in sides), default=0) + 1

    def _next_slot_per_edge(self, tag: int, frm: bytes, relation: bytes) -> int | Any:
        prefix = self._per_edge_prefix(tag, frm, relation)
        keys = self.store.list(from_=prefix, to=prefix + b'\xff' * 8)
        if isinstance(keys, (Refused, Unavailable)):
            return keys
        if not keys:
            return 1
        return _U64.unpack_from(keys[-1], len(prefix))[0] + 1

    def _load_compact(self, tag: int, frm: bytes, relation: bytes, planned: dict, tokens: dict, expect_token: bytes) -> Any:
        key = self._adj_key(tag, frm, relation)
        if key in planned:
            return key
        held = self._read(key)
        if isinstance(held, (Refused, Unavailable)):
            return held
        if isinstance(held, Absent):
            planned[key] = []
            tokens[key] = expect_token if expect_token else ABSENT
        else:
            planned[key] = _LAYOUT_VALUES.unpack_compact(held.value)
            tokens[key] = expect_token if expect_token else held.token
        return key

    def put_edge(self, edge: Graph_PutEdge) -> Any:
        refs = self.put_edges([edge])
        if isinstance(refs, list):
            return refs[0]
        return refs

    def put_edges(self, edges: Sequence[Graph_PutEdge]) -> Any:
        if not edges:
            return Refused(Refusal.MALFORMED, Bad.EDGE.summary())
        for each in edges:
            if each.Layout != self.layout:
                return Refused(Refusal.MALFORMED, Bad.LAYOUT.summary())
            if not isinstance(each.From, bytes) or not isinstance(each.Relation, bytes) or not isinstance(each.To, bytes):
                return Refused(Refusal.MALFORMED, Bad.EDGE.summary())
            if not _m_side.is_relation_type_uuid(each.Relation):
                return Refused(Refusal.MALFORMED, Bad.RELATION.summary())
            if each.ReverseRelation and not _m_side.is_relation_type_uuid(each.ReverseRelation):
                return Refused(Refusal.MALFORMED, Bad.RELATION.summary())
            if _m_side.fields_map_or_refuse(each.Fields if isinstance(each.Fields, bytes) else b'') is None:
                return Refused(Refusal.MALFORMED, Bad.FIELDS.summary())
        if self.layout == LAYOUT_COMPACT:
            return self._put_edges_compact(edges)
        return self._put_edges_per_edge(edges)

    def _put_edges_compact(self, edges: Sequence[Graph_PutEdge]) -> Any:
        markers: dict[bytes, bytes] = {}
        planned: dict[bytes, list[Stored_Side]] = {}
        tokens: dict[bytes, Any] = {}
        refs: list[bytes] = []
        for each in edges:
            pairs = [(each.From, each.Relation), (each.To, each.Relation)]
            if each.ReverseRelation:
                pairs.append((each.To, each.ReverseRelation))
            for frm, relation in pairs:
                err = self._check_layout(frm, relation, LAYOUT_COMPACT, markers)
                if err is not None:
                    return err
            out_key = self._load_compact(_TAG_COMPACT, each.From, each.Relation, planned, tokens, each.ExpectFrom)
            if not isinstance(out_key, bytes):
                return out_key
            in_key = self._load_compact(_TAG_IN_COMPACT, each.To, each.Relation, planned, tokens, b'')
            if not isinstance(in_key, bytes):
                return in_key
            out_slot = self._next_slot_compact(planned[out_key])
            in_slot = self._next_slot_compact(planned[in_key])
            out_ref = self._side_ref(_TAG_COMPACT, each.From, each.Relation, out_slot)
            in_ref = self._side_ref(_TAG_IN_COMPACT, each.To, each.Relation, in_slot)
            reverse_ref = b''
            if each.ReverseRelation:
                rev_key = self._load_compact(_TAG_COMPACT, each.To, each.ReverseRelation, planned, tokens, each.ExpectTo)
                if not isinstance(rev_key, bytes):
                    return rev_key
                rev_slot = self._next_slot_compact(planned[rev_key])
                reverse_ref = self._side_ref(_TAG_COMPACT, each.To, each.ReverseRelation, rev_slot)
                planned[rev_key].append(Stored_Side(rev_slot, each.From, each.Fields, False, out_ref, b''))
            planned[out_key].append(Stored_Side(out_slot, each.To, each.Fields, False, reverse_ref, in_ref))
            planned[in_key].append(Stored_Side(in_slot, each.From, each.Fields, False, out_ref, b''))
            refs.append(out_ref)
        expect: list = []
        write: list = []
        for key, value in markers.items():
            held = self._read(key)
            if isinstance(held, Absent):
                expect.append((key, ABSENT))
                write.append((key, value))
        for key, sides in planned.items():
            expect.append((key, tokens[key]))
            write.append((key, _LAYOUT_VALUES.pack_compact(sides)))
        answer = self.store.batch(expect, write)
        if answer != Committed():
            return answer
        return refs

    def _put_edges_per_edge(self, edges: Sequence[Graph_PutEdge]) -> Any:
        markers: dict[bytes, bytes] = {}
        expect: list = []
        write: list = []
        refs: list[bytes] = []
        used: dict[tuple[int, bytes, bytes], int] = {}
        for each in edges:
            pairs = [(each.From, each.Relation), (each.To, each.Relation)]
            if each.ReverseRelation:
                pairs.append((each.To, each.ReverseRelation))
            for frm, relation in pairs:
                err = self._check_layout(frm, relation, LAYOUT_PER_EDGE, markers)
                if err is not None:
                    return err

            def take(tag: int, frm: bytes, relation: bytes) -> int | Any:
                pair = (tag, frm, relation)
                if pair not in used:
                    nxt = self._next_slot_per_edge(tag, frm, relation)
                    if not isinstance(nxt, int):
                        return nxt
                    used[pair] = nxt
                else:
                    used[pair] += 1
                return used[pair]
            out_slot = take(_TAG_PER_EDGE, each.From, each.Relation)
            if not isinstance(out_slot, int):
                return out_slot
            in_slot = take(_TAG_IN_PER_EDGE, each.To, each.Relation)
            if not isinstance(in_slot, int):
                return in_slot
            out_ref = self._per_edge_key(_TAG_PER_EDGE, each.From, each.Relation, out_slot)
            in_ref = self._per_edge_key(_TAG_IN_PER_EDGE, each.To, each.Relation, in_slot)
            reverse_ref = b''
            if each.ReverseRelation:
                rev_slot = take(_TAG_PER_EDGE, each.To, each.ReverseRelation)
                if not isinstance(rev_slot, int):
                    return rev_slot
                reverse_ref = self._per_edge_key(_TAG_PER_EDGE, each.To, each.ReverseRelation, rev_slot)
                expect.append((reverse_ref, each.ExpectTo if each.ExpectTo else ABSENT))
                write.append((reverse_ref, _LAYOUT_VALUES.pack_per_edge(Stored_Edge_Value(each.From, each.Fields, False, out_ref, b''))))
            expect.append((out_ref, each.ExpectFrom if each.ExpectFrom else ABSENT))
            write.append((out_ref, _LAYOUT_VALUES.pack_per_edge(Stored_Edge_Value(each.To, each.Fields, False, reverse_ref, in_ref))))
            expect.append((in_ref, ABSENT))
            write.append((in_ref, _LAYOUT_VALUES.pack_per_edge(Stored_Edge_Value(each.From, each.Fields, False, out_ref, b''))))
            refs.append(out_ref)
        for key, value in markers.items():
            held = self._read(key)
            if isinstance(held, Absent):
                expect.append((key, ABSENT))
                write.append((key, value))
        answer = self.store.batch(expect, write)
        if answer != Committed():
            return answer
        return refs

    def list_sides(self, query: Graph_ListSidesQuery) -> Any:
        return self._list_direction(query.From, query.Relation, DIRECTION_OUT, query.After, query.Limit, query.Descending)

    def _list_direction(self, frm: bytes, relation: bytes, direction: int, after: bytes, limit: int, descending: bool) -> Any:
        if limit < 0:
            return Refused(Refusal.MALFORMED, Bad.LIMIT.summary())
        page_limit = limit if limit else None
        held = self._read(self._layout_key(frm, relation))
        if isinstance(held, (Refused, Unavailable)):
            return held
        if isinstance(held, Absent):
            return ()
        layout = held.value[0]
        tags = []
        if direction in (DIRECTION_OUT, DIRECTION_EITHER):
            tags.append(_TAG_COMPACT if layout == LAYOUT_COMPACT else _TAG_PER_EDGE)
        if direction in (DIRECTION_IN, DIRECTION_EITHER):
            tags.append(_TAG_IN_COMPACT if layout == LAYOUT_COMPACT else _TAG_IN_PER_EDGE)
        items: list[Graph_Side] = []
        for tag in tags:
            if tag in (_TAG_COMPACT, _TAG_IN_COMPACT):
                part = self._list_compact(tag, frm, relation, after, None, descending)
            else:
                part = self._list_per_edge(tag, frm, relation, after, None, descending)
            if isinstance(part, (Refused, Unavailable)):
                return part
            items.extend(part)
        items.sort(key=lambda s: s.Ref, reverse=descending)
        if after:
            if descending:
                items = [each for each in items if each.Ref < after]
            else:
                items = [each for each in items if each.Ref > after]
        if page_limit is not None:
            items = items[:page_limit]
        return tuple(items)

    def _list_compact(self, tag: int, frm: bytes, relation: bytes, after: bytes, limit: int | None, descending: bool) -> Any:
        key = self._adj_key(tag, frm, relation)
        held = self._read(key)
        if isinstance(held, (Refused, Unavailable)):
            return held
        if isinstance(held, Absent):
            return ()
        sides = [each for each in _LAYOUT_VALUES.unpack_compact(held.value) if not each.ended]
        sides.sort(key=lambda s: s.slot, reverse=descending)
        items = [Graph_Side(self._side_ref(tag, frm, relation, each.slot), each.to, each.fields, held.token) for each in sides]
        if after:
            if descending:
                items = [each for each in items if each.Ref < after]
            else:
                items = [each for each in items if each.Ref > after]
        if limit is not None:
            items = items[:limit]
        return tuple(items)

    def _list_per_edge(self, tag: int, frm: bytes, relation: bytes, after: bytes, limit: int | None, descending: bool) -> Any:
        prefix = self._per_edge_prefix(tag, frm, relation)
        keys = self.store.list(from_=prefix, to=prefix + b'\xff' * 8, after=after or None, limit=None, descending=descending)
        if isinstance(keys, (Refused, Unavailable)):
            return keys
        if not keys:
            return ()
        found = self.store.get(keys)
        if isinstance(found, Refused):
            return found
        items: list[Graph_Side] = []
        for key, held in zip(keys, found):
            if isinstance(held, Unavailable):
                return held
            if isinstance(held, Absent):
                continue
            edge = _LAYOUT_VALUES.unpack_per_edge(held.value)
            if edge.ended:
                continue
            items.append(Graph_Side(key, edge.to, edge.fields, held.token))
            if limit is not None and len(items) >= limit:
                break
        return tuple(items)

    def count_sides(self, frm: bytes, relation: bytes) -> Any:
        listed = self.list_sides(Graph_ListSidesQuery(frm, relation, b'', 0, False))
        if isinstance(listed, (Refused, Unavailable)):
            return listed
        return len(listed)

    def get_side(self, query: Graph_GetSideQuery) -> Graph_GetSideAnswer:
        listed = self.list_sides(Graph_ListSidesQuery(query.From, query.Relation, b'', 0, False))
        if isinstance(listed, Refused):
            return Graph_GetSideAnswer(False, Err=listed)
        if isinstance(listed, Unavailable):
            return Graph_GetSideAnswer(False, Err=listed)
        for each in listed:
            if each.To == query.To:
                return Graph_GetSideAnswer(True, each.Ref, each.Fields, each.Token)
        return Graph_GetSideAnswer(False)

    def set_side_fields(self, ref: bytes, fields: bytes, expect: bytes) -> Any:
        return self._mutate_side(ref, fields, expect, end=False)

    def end_edge(self, ref: bytes, expect: bytes) -> Any:
        return self._mutate_side(ref, b'', expect, end=True)

    def _mutate_side(self, ref: bytes, fields: bytes, expect: bytes, end: bool) -> Any:
        parsed = self._parse_side_ref(ref)
        if parsed is None:
            return Refused(Refusal.MALFORMED, Bad.REF.summary())
        if not end and _m_side.fields_map_or_refuse(fields if isinstance(fields, bytes) else b'') is None:
            return Refused(Refusal.MALFORMED, Bad.FIELDS.summary())
        tag = parsed[0]
        if tag in (_TAG_COMPACT, _TAG_IN_COMPACT):
            return self._mutate_compact(ref, fields, expect, end)
        return self._mutate_per_edge(ref, fields, expect, end)

    def _mutate_compact(self, ref: bytes, fields: bytes, expect: bytes, end: bool) -> Any:
        parsed = self._parse_side_ref(ref)
        assert parsed is not None
        tag, frm, relation, slot = parsed
        key = self._adj_key(tag, frm, relation)
        held = self._read(key)
        if isinstance(held, (Refused, Unavailable)):
            return held
        if isinstance(held, Absent):
            return Refused(Refusal.MALFORMED, Bad.REF.summary())
        sides = _LAYOUT_VALUES.unpack_compact(held.value)
        target = next((each for each in sides if each.slot == slot and not each.ended), None)
        if target is None:
            return Refused(Refusal.MALFORMED, Bad.REF.summary())
        if end:
            target.ended = True
        else:
            target.fields = fields
        expects = [(key, expect if expect else held.token)]
        writes = [(key, _LAYOUT_VALUES.pack_compact(sides))]
        for linked in (target.reverse_ref, target.inbound_ref):
            if not linked:
                continue
            err = self._append_compact_link(linked, fields, end, expects, writes)
            if err is not None:
                return err
        return self.store.batch(expects, writes)

    def _append_compact_link(self, ref: bytes, fields: bytes, end: bool, expects: list, writes: list) -> Any:
        parsed = self._parse_side_ref(ref)
        if parsed is None:
            return Refused(Refusal.MALFORMED, Bad.REF.summary())
        tag, frm, relation, slot = parsed
        key = self._adj_key(tag, frm, relation)
        for i, (at, data) in enumerate(writes):
            if at != key:
                continue
            sides = _LAYOUT_VALUES.unpack_compact(data)
            target = next((each for each in sides if each.slot == slot), None)
            if target is None:
                return Refused(Refusal.MALFORMED, Bad.REF.summary())
            if end:
                target.ended = True
            else:
                target.fields = fields
            writes[i] = (key, _LAYOUT_VALUES.pack_compact(sides))
            return None
        held = self._read(key)
        if isinstance(held, (Refused, Unavailable)):
            return held
        if isinstance(held, Absent):
            return Refused(Refusal.MALFORMED, Bad.REF.summary())
        sides = _LAYOUT_VALUES.unpack_compact(held.value)
        target = next((each for each in sides if each.slot == slot and not each.ended), None)
        if target is None:
            return Refused(Refusal.MALFORMED, Bad.REF.summary())
        if end:
            target.ended = True
        else:
            target.fields = fields
        expects.append((key, held.token))
        writes.append((key, _LAYOUT_VALUES.pack_compact(sides)))
        return None

    def _mutate_per_edge(self, ref: bytes, fields: bytes, expect: bytes, end: bool) -> Any:
        held = self._read(ref)
        if isinstance(held, (Refused, Unavailable)):
            return held
        if isinstance(held, Absent):
            return Refused(Refusal.MALFORMED, Bad.REF.summary())
        edge = _LAYOUT_VALUES.unpack_per_edge(held.value)
        if edge.ended:
            return Refused(Refusal.MALFORMED, Bad.REF.summary())
        new_fields = edge.fields if end else fields
        expects = [(ref, expect if expect else held.token)]
        writes = [(ref, _LAYOUT_VALUES.pack_per_edge(Stored_Edge_Value(edge.to, new_fields, end, edge.reverse_ref, edge.inbound_ref)))]
        for linked in (edge.reverse_ref, edge.inbound_ref):
            if not linked:
                continue
            rheld = self._read(linked)
            if isinstance(rheld, (Refused, Unavailable)):
                return rheld
            if isinstance(rheld, Absent):
                return Refused(Refusal.MALFORMED, Bad.REF.summary())
            redge = _LAYOUT_VALUES.unpack_per_edge(rheld.value)
            if redge.ended:
                return Refused(Refusal.MALFORMED, Bad.REF.summary())
            expects.append((linked, rheld.token))
            writes.append((linked, _LAYOUT_VALUES.pack_per_edge(Stored_Edge_Value(redge.to, new_fields if not end else redge.fields, end, redge.reverse_ref, redge.inbound_ref))))
        return self.store.batch(expects, writes)

    def match(self, pattern: Graph_Pattern) -> Any:
        if pattern.SlotCount < 1 or not pattern.Steps or not pattern.HasBound:
            return Refused(Refusal.MALFORMED, Bad.PATTERN.summary())
        if pattern.Limit < 0:
            return Refused(Refusal.MALFORMED, Bad.PATTERN.summary())
        limit = pattern.Limit if pattern.Limit else None
        seed = {pattern.BoundSlot: Graph_Binding(pattern.BoundSlot, pattern.BoundVertex)}
        rows: list[list[Graph_Binding]] = []
        err = self._match_steps(pattern.Steps, 0, seed, rows, limit)
        if err is not None:
            return err
        return rows

    def _match_steps(self, steps: Sequence[Graph_Pattern_Step], index: int, bound: dict[int, Graph_Binding], rows: list, limit: int | None) -> Any:
        if limit is not None and len(rows) >= limit:
            return None
        if index >= len(steps):
            rows.append([bound[i] for i in sorted(bound)])
            return None
        step = steps[index]
        if step.FromSlot not in bound:
            return Refused(Refusal.MALFORMED, Bad.PATTERN.summary())
        sides = self._expand_sides(bound[step.FromSlot].Vertex, step.Relation, step.Direction)
        if isinstance(sides, (Refused, Unavailable)):
            return sides
        for each in sides:
            if step.RequireFieldPrefix and not each.Fields.startswith(step.FieldPrefix):
                continue
            nxt = dict(bound)
            nxt[step.ToSlot] = Graph_Binding(step.ToSlot, each.To, each.Ref, True)
            err = self._match_steps(steps, index + 1, nxt, rows, limit)
            if err is not None:
                return err
            if limit is not None and len(rows) >= limit:
                return None
        return None

    def _expand_sides(self, frm: bytes, relation: bytes, direction: int) -> Any:
        if direction not in (DIRECTION_OUT, DIRECTION_IN, DIRECTION_EITHER):
            return Refused(Refusal.MALFORMED, Bad.PATTERN.summary())
        return self._list_direction(frm, relation, direction, b'', 0, False)

    def path(self, query: Graph_Path_Query) -> Any:
        if query.MaxHops < query.MinHops or query.MinHops < 1:
            return Refused(Refusal.MALFORMED, Bad.PATTERN.summary())
        limit = query.Limit if query.Limit else None
        rows: list[list[Graph_Binding]] = []
        stack: list[tuple[bytes, list[Graph_Binding], set[bytes]]] = [(query.From, [Graph_Binding(0, query.From)], set())]
        while stack:
            if limit is not None and len(rows) >= limit:
                break
            vertex, trail, used_edges = stack.pop()
            hops = len([b for b in trail if b.HasSide])
            if hops >= query.MinHops:
                rows.append(list(trail))
                if limit is not None and len(rows) >= limit:
                    break
            if hops >= query.MaxHops:
                continue
            sides = self._expand_sides(vertex, query.Relation, query.Direction)
            if isinstance(sides, (Refused, Unavailable)):
                return sides
            seen_vertices = {b.Vertex for b in trail}
            for each in sides:
                if query.Mode == PATH_TRAIL and each.Ref in used_edges:
                    continue
                if query.Mode == PATH_ACYCLIC and each.To in seen_vertices:
                    continue
                nxt_edges = set(used_edges)
                nxt_edges.add(each.Ref)
                nxt_trail = list(trail) + [Graph_Binding(hops + 1, each.To, each.Ref, True)]
                stack.append((each.To, nxt_trail, nxt_edges))
        return rows

    def exists(self, pattern: Graph_Pattern) -> Any:
        limited = Graph_Pattern(pattern.SlotCount, pattern.Steps, pattern.BoundSlot, pattern.BoundVertex, pattern.HasBound, 1)
        rows = self.match(limited)
        if isinstance(rows, (Refused, Unavailable)):
            return rows
        return bool(rows)

    def expand(self, frm: bytes, relation: bytes, direction: int, limit: int) -> Any:
        sides = self._expand_sides(frm, relation, direction)
        if isinstance(sides, (Refused, Unavailable)):
            return sides
        rows = []
        for each in sides:
            rows.append([Graph_Binding(0, frm), Graph_Binding(1, each.To, each.Ref, True)])
            if limit and len(rows) >= limit:
                break
        return rows
