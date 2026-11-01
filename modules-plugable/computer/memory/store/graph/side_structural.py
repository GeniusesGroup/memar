#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import json
import uuid
from typing import Any
_NS = uuid.NAMESPACE_URL
_BASE = 'memar://modules-plugable/computer/memory/store/graph/side/'
SLOT_TYPE_UUID = uuid.uuid5(_NS, _BASE + 'slot')
TO_TYPE_UUID = uuid.uuid5(_NS, _BASE + 'to')
FIELDS_TYPE_UUID = uuid.uuid5(_NS, _BASE + 'fields')
ENDED_TYPE_UUID = uuid.uuid5(_NS, _BASE + 'ended')
SLOT_KEY = str(SLOT_TYPE_UUID)
TO_KEY = str(TO_TYPE_UUID)
FIELDS_KEY = str(FIELDS_TYPE_UUID)
ENDED_KEY = str(ENDED_TYPE_UUID)
SIDE_KEYS = frozenset({SLOT_KEY, TO_KEY, FIELDS_KEY, ENDED_KEY})
SLOT_BYTES = SLOT_TYPE_UUID.bytes
TO_BYTES = TO_TYPE_UUID.bytes
FIELDS_BYTES = FIELDS_TYPE_UUID.bytes
ENDED_BYTES = ENDED_TYPE_UUID.bytes

def is_type_uuid_text(text: str) -> bool:
    try:
        uuid.UUID(text)
    except ValueError:
        return False
    return True

def is_relation_type_uuid(relation: bytes) -> bool:
    if not isinstance(relation, bytes):
        return False
    if len(relation) == 16:
        try:
            uuid.UUID(bytes=relation)
        except ValueError:
            return False
        return True
    try:
        text = relation.decode('ascii')
    except UnicodeDecodeError:
        return False
    return is_type_uuid_text(text)

def relation_as_part_key(relation: bytes) -> bytes:
    if len(relation) == 16:
        return str(uuid.UUID(bytes=relation)).encode('ascii')
    return relation

def relation_from_part_key(key: bytes) -> bytes:
    text = key.decode('ascii')
    return uuid.UUID(text).bytes

def fields_map_or_refuse(fields: bytes) -> dict[str, Any] | None:
    if not fields:
        return {}
    try:
        text = fields.decode('utf-8')
    except UnicodeDecodeError:
        return None
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        return None
    if not isinstance(parsed, dict):
        return None
    for key in parsed:
        if not isinstance(key, str) or not is_type_uuid_text(key):
            return None
    return parsed

def encode_fields_map(fields: dict[str, Any]) -> bytes:
    if not fields:
        return b''
    return json.dumps(fields, ensure_ascii=False, separators=(',', ':'), sort_keys=True).encode('utf-8')
