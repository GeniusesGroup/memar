#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import json
import uuid
from importlib import import_module
_m_address = import_module('modules-plugable.computer.memory.store.graph.address')
_m_layout = import_module('modules-plugable.computer.memory.store.graph.codecs.layout_value')
_m_json = import_module('modules-plugable.computer.memory.store.files.codecs.json.body')
TAG_LAYOUT = _m_address.TAG_LAYOUT
TAG_COMPACT = _m_address.TAG_COMPACT
TAG_IN_COMPACT = _m_address.TAG_IN_COMPACT
LAYOUT_PREFIX = b'@'
IN_PREFIX = b'<'
_CODEC = _m_layout.Graph_Default_Layout_Value_Codec()
RECORD_ID_LENGTH = 16

def parse_graph_address(address: bytes) -> tuple[int, bytes, bytes] | None:
    return _m_address.parse_adj(address)

def is_graph_address(address: bytes) -> bool:
    return parse_graph_address(address) is not None

def part_key(tag: int, relation: bytes) -> bytes:
    if tag == TAG_LAYOUT:
        return LAYOUT_PREFIX + relation
    if tag == TAG_IN_COMPACT:
        return IN_PREFIX + relation
    return relation

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

def sides_to_json_bytes(value: bytes) -> bytes:
    sides = []
    for each in _CODEC.unpack_compact(value):
        sides.append({
            'slot': each.slot,
            'to': _uuid_text(each.to) if len(each.to) == 16 else each.to.hex(),
            'fields': _m_json.part_to_json(each.fields),
            'ended': each.ended,
            'reverse_ref': each.reverse_ref.hex(),
            'inbound_ref': each.inbound_ref.hex(),
        })
    return json.dumps(sides, ensure_ascii=False, separators=(',', ':')).encode('utf-8')

def sides_from_json_bytes(value: bytes) -> bytes:
    parsed = json.loads(value.decode('utf-8'))
    if not isinstance(parsed, list):
        raise ValueError('compact sides must be a JSON array')
    sides = []
    for each in parsed:
        sides.append(_m_layout.Stored_Side(
            int(each['slot']),
            _uuid_bytes(each['to']) if isinstance(each['to'], str) else bytes(each['to']),
            _m_json.part_from_json(each.get('fields')),
            bool(each.get('ended', False)),
            bytes.fromhex(each.get('reverse_ref') or ''),
            bytes.fromhex(each.get('inbound_ref') or ''),
        ))
    return _CODEC.pack_compact(sides)

def layout_marker_to_json_bytes(value: bytes) -> bytes:
    return json.dumps({'layout': value.hex()}, separators=(',', ':')).encode('utf-8')

def layout_marker_from_json_bytes(value: bytes) -> bytes:
    parsed = json.loads(value.decode('utf-8'))
    return bytes.fromhex(parsed['layout'])

def value_for_pack(tag: int, raw: bytes) -> bytes:
    if tag == TAG_LAYOUT:
        return layout_marker_to_json_bytes(raw)
    if tag in (TAG_COMPACT, TAG_IN_COMPACT):
        return sides_to_json_bytes(raw)
    return raw

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
    return isinstance(first, dict) and 'slot' in first and 'to' in first

def collect_node_parts(values: dict[bytes, bytes], identity: bytes, is_record_key) -> dict[bytes, bytes]:
    parts: dict[bytes, bytes] = {}
    for at, data in values.items():
        if is_record_key(at) and at[:RECORD_ID_LENGTH] == identity:
            parts[at[RECORD_ID_LENGTH:]] = data
            continue
        parsed = parse_graph_address(at)
        if parsed is None:
            continue
        tag, frm, relation = parsed
        if frm != identity or tag not in (TAG_LAYOUT, TAG_COMPACT, TAG_IN_COMPACT):
            continue
        parts[part_key(tag, relation)] = value_for_pack(tag, data)
    return parts

def restore_from_parts(identity: bytes, parts: dict[bytes, bytes]) -> dict[bytes, bytes]:
    restored: dict[bytes, bytes] = {}
    for key, data in parts.items():
        if key.startswith(LAYOUT_PREFIX):
            relation = key[len(LAYOUT_PREFIX):]
            restored[graph_store_key(TAG_LAYOUT, identity, relation)] = layout_marker_from_json_bytes(data)
            continue
        if key.startswith(IN_PREFIX):
            relation = key[len(IN_PREFIX):]
            restored[graph_store_key(TAG_IN_COMPACT, identity, relation)] = sides_from_json_bytes(data)
            continue
        if _looks_like_sides(data):
            restored[graph_store_key(TAG_COMPACT, identity, key)] = sides_from_json_bytes(data)
            continue
        restored[identity + key] = data
    return restored
