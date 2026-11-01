#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import json
import struct
import uuid
from importlib import import_module
_m_address = import_module('modules-plugable.computer.memory.store.graph.address')
_m_layout = import_module('modules-plugable.computer.memory.store.graph.codecs.layout_value')
_m_json = import_module('modules-plugable.computer.memory.store.files.codecs.json.body')
_m_side = import_module('modules-plugable.computer.memory.store.graph.side_structural')
_m_errors = import_module('modules-plugable.computer.memory.store.files.errors.errors')
TAG_LAYOUT = _m_address.TAG_LAYOUT
TAG_COMPACT = _m_address.TAG_COMPACT
TAG_IN_COMPACT = _m_address.TAG_IN_COMPACT
_CODEC = _m_layout.Graph_Default_Layout_Value_Codec()
RECORD_ID_LENGTH = 16
LAYOUT_COMPACT_VALUE = bytes([1])
_U64 = struct.Struct('>Q')
BadBody = _m_errors.BadBody

def parse_graph_address(address: bytes) -> tuple[int, bytes, bytes] | None:
    return _m_address.parse_adj(address)

def is_graph_address(address: bytes) -> bool:
    return parse_graph_address(address) is not None

def graph_store_key(tag: int, frm: bytes, relation: bytes) -> bytes:
    return _m_address.adj_key(tag, frm, relation)

def _uuid_text(identity: bytes) -> str:
    try:
        return str(uuid.UUID(bytes=identity))
    except ValueError:
        return identity.hex()

def _uuid_bytes(text: str) -> bytes:
    try:
        return uuid.UUID(text).bytes
    except ValueError:
        return bytes.fromhex(text)

def _side_ref(tag: int, frm: bytes, relation: bytes, slot: int) -> bytes:
    return graph_store_key(tag, frm, relation) + _U64.pack(slot)

def sides_to_json_bytes(value: bytes) -> bytes:
    sides = []
    for each in _CODEC.unpack_compact(value):
        if not each.fields:
            fields_map: object = {}
        else:
            fields_map = _m_json.part_to_json(each.fields)
            if isinstance(fields_map, dict):
                for key in fields_map:
                    if not isinstance(key, str) or not _m_side.is_type_uuid_text(key):
                        raise BadBody('edge fields that are not a TypeUUID map')
            else:
                raise BadBody('edge fields that are not a TypeUUID map')
        item = {
            _m_side.SLOT_KEY: each.slot,
            _m_side.TO_KEY: _uuid_text(each.to) if len(each.to) == 16 else each.to.hex(),
            _m_side.FIELDS_KEY: fields_map,
            _m_side.ENDED_KEY: each.ended,
        }
        sides.append(item)
    return json.dumps(sides, ensure_ascii=False, separators=(',', ':')).encode('utf-8')

def _fields_from_side(each: dict) -> bytes:
    raw = each.get(_m_side.FIELDS_KEY)
    if raw is None:
        raise BadBody('a side without the fields TypeUUID')
    if isinstance(raw, dict):
        for key in raw:
            if not isinstance(key, str) or not _m_side.is_type_uuid_text(key):
                raise BadBody('edge fields that are not a TypeUUID map')
    return _m_json.part_from_json(raw)

def sides_from_json_bytes(value: bytes) -> bytes:
    parsed = json.loads(value.decode('utf-8'))
    if not isinstance(parsed, list):
        raise BadBody('compact sides must be a JSON array')
    sides = []
    for each in parsed:
        if not isinstance(each, dict):
            raise BadBody('a side that is not an object')
        keys = set(each.keys())
        if keys != _m_side.SIDE_KEYS:
            raise BadBody('a side that is not the TypeUUID envelope')
        to_value = each[_m_side.TO_KEY]
        sides.append(_m_layout.Stored_Side(
            int(each[_m_side.SLOT_KEY]),
            _uuid_bytes(to_value) if isinstance(to_value, str) else bytes(to_value),
            _fields_from_side(each),
            bool(each[_m_side.ENDED_KEY]),
            b'',
            b'',
        ))
    return _CODEC.pack_compact(sides)

def _looks_like_sides(data: bytes) -> bool:
    try:
        parsed = json.loads(data.decode('utf-8'))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return False
    if not isinstance(parsed, list):
        return False
    if not parsed:
        return True
    first = parsed[0]
    return isinstance(first, dict) and (_m_side.SLOT_KEY in first or 'slot' in first)

def validate_node_parts(parts: dict[bytes, bytes]) -> None:
    for key, data in parts.items():
        try:
            text_key = key.decode('ascii')
        except UnicodeDecodeError as exc:
            raise BadBody('a part key that is not ASCII') from exc
        try:
            parsed = json.loads(data.decode('utf-8'))
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
        if isinstance(parsed, list):
            if not _m_side.is_type_uuid_text(text_key):
                raise BadBody('a relation that is not a TypeUUID')
            sides_from_json_bytes(data)
            continue
        if isinstance(parsed, dict):
            raise BadBody('a free-form domain object at top level')

def collect_node_parts(values: dict[bytes, bytes], identity: bytes, is_record_key) -> dict[bytes, bytes]:
    parts: dict[bytes, bytes] = {}
    for at, data in values.items():
        parsed = parse_graph_address(at)
        if parsed is not None:
            tag, frm, relation = parsed
            if frm == identity and tag == TAG_COMPACT:
                parts[_m_side.relation_as_part_key(relation)] = sides_to_json_bytes(data)
            continue
        if is_record_key(at) and at[:RECORD_ID_LENGTH] == identity:
            parts[at[RECORD_ID_LENGTH:]] = data
    validate_node_parts(parts)
    return parts

def restore_from_parts(identity: bytes, parts: dict[bytes, bytes]) -> dict[bytes, bytes]:
    validate_node_parts(parts)
    restored: dict[bytes, bytes] = {}
    for key, data in parts.items():
        if key[:1] in (b'@', b'<'):
            continue
        if _looks_like_sides(data):
            relation = _m_side.relation_from_part_key(key) if _m_side.is_type_uuid_text(key.decode('ascii')) else key
            restored[graph_store_key(TAG_COMPACT, identity, relation)] = sides_from_json_bytes(data)
            continue
        restored[identity + key] = data
    return restored

def _outbound_entries(values: dict[bytes, bytes]) -> list[tuple[bytes, bytes, list]]:
    entries = []
    for at, data in values.items():
        parsed = parse_graph_address(at)
        if parsed is None or parsed[0] != TAG_COMPACT:
            continue
        _tag, frm, relation = parsed
        entries.append((frm, relation, list(_CODEC.unpack_compact(data))))
    return entries

def _pair_reverse_refs(entries: list[tuple[bytes, bytes, list]]) -> None:
    by_vertex: dict[bytes, list[tuple[bytes, object]]] = {}
    for frm, relation, sides in entries:
        for side in sides:
            by_vertex.setdefault(frm, []).append((relation, side))
    used: set[tuple[bytes, bytes, int, bytes, bytes, int]] = set()
    for frm, relation, sides in entries:
        for side in sides:
            if side.reverse_ref:
                continue
            candidates = []
            for far_rel, far_side in by_vertex.get(side.to, []):
                if far_side.to != frm or far_side.ended:
                    continue
                key = (frm, relation, side.slot, side.to, far_rel, far_side.slot)
                rev_key = (side.to, far_rel, far_side.slot, frm, relation, side.slot)
                if key in used or rev_key in used:
                    continue
                if far_side.fields != side.fields:
                    continue
                candidates.append((far_rel, far_side))
            if len(candidates) != 1:
                continue
            far_rel, far_side = candidates[0]
            side.reverse_ref = _side_ref(TAG_COMPACT, side.to, far_rel, far_side.slot)
            far_side.reverse_ref = _side_ref(TAG_COMPACT, frm, relation, side.slot)
            used.add((frm, relation, side.slot, side.to, far_rel, far_side.slot))

def apply_derived_graph(values: dict[bytes, bytes]) -> None:
    drop = [at for at in values if (parsed := parse_graph_address(at)) is not None and parsed[0] in (TAG_LAYOUT, TAG_IN_COMPACT)]
    for at in drop:
        del values[at]
    entries = _outbound_entries(values)
    _pair_reverse_refs(entries)
    inbound: dict[bytes, list] = {}
    inbound_slots: dict[bytes, int] = {}
    for frm, relation, sides in entries:
        values[graph_store_key(TAG_LAYOUT, frm, relation)] = LAYOUT_COMPACT_VALUE
        rebuilt = []
        for side in sides:
            in_key = graph_store_key(TAG_IN_COMPACT, side.to, relation)
            values[graph_store_key(TAG_LAYOUT, side.to, relation)] = LAYOUT_COMPACT_VALUE
            in_slot = inbound_slots.get(in_key, 0) + 1
            inbound_slots[in_key] = in_slot
            out_ref = _side_ref(TAG_COMPACT, frm, relation, side.slot)
            inbound.setdefault(in_key, []).append(_m_layout.Stored_Side(in_slot, frm, side.fields, side.ended, out_ref, b''))
            rebuilt.append(_m_layout.Stored_Side(side.slot, side.to, side.fields, side.ended, side.reverse_ref, _side_ref(TAG_IN_COMPACT, side.to, relation, in_slot)))
        values[graph_store_key(TAG_COMPACT, frm, relation)] = _CODEC.pack_compact(rebuilt)
    for in_key, sides in inbound.items():
        values[in_key] = _CODEC.pack_compact(sides)
