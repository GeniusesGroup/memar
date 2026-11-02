#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import uuid
from importlib import import_module
_m_side = import_module('modules-plugable.computer.memory.store.graph.side_structural')
_NS = uuid.NAMESPACE_URL
_REL = 'memar://modules-plugable/management/task/relation/'
_FIELD = 'memar://modules-plugable/management/task/field/'
HAS_TASK = uuid.uuid5(_NS, _REL + 'has_task').bytes
HAS_TASK_OF = uuid.uuid5(_NS, _REL + 'has_task_of').bytes
PARENT = uuid.uuid5(_NS, _REL + 'parent').bytes
PARENT_OF = uuid.uuid5(_NS, _REL + 'parent_of').bytes
CONVERSATION = uuid.uuid5(_NS, _REL + 'conversation').bytes
CONVERSATION_OF = uuid.uuid5(_NS, _REL + 'conversation_of').bytes
DEPENDS_ON = uuid.uuid5(_NS, _REL + 'depends_on').bytes
DEPENDS_FOR = uuid.uuid5(_NS, _REL + 'depends_for').bytes
TITLE = uuid.uuid5(_NS, _REL + 'title').bytes
TITLE_OF = uuid.uuid5(_NS, _REL + 'title_of').bytes
TYPE_IS = uuid.uuid5(_NS, _REL + 'type_is').bytes
TYPE_OF = uuid.uuid5(_NS, _REL + 'type_of').bytes
HAS_BODY = uuid.uuid5(_NS, _REL + 'has_body').bytes
HAS_BODY_OF = uuid.uuid5(_NS, _REL + 'has_body_of').bytes
LEGACY = uuid.uuid5(_NS, _REL + 'legacy').bytes
LEGACY_OF = uuid.uuid5(_NS, _REL + 'legacy_of').bytes
FIELD_PRIORITY = str(uuid.uuid5(_NS, _FIELD + 'priority'))
FIELD_START = str(uuid.uuid5(_NS, _FIELD + 'start'))
FIELD_LEGACY_ID = str(uuid.uuid5(_NS, _FIELD + 'legacy_id'))
FIELD_LEGACY_REF = str(uuid.uuid5(_NS, _FIELD + 'legacy_ref'))
FIELD_KIND = str(uuid.uuid5(_NS, _FIELD + 'kind'))


def project_id(project: str) -> bytes:
    text = (project or '').strip() or '/'
    return uuid.uuid5(_NS, 'memar://modules-plugable/management/task/project/' + text).bytes


def legacy_ref_id(ref: str) -> bytes:
    return uuid.uuid5(_NS, 'memar://modules-plugable/management/task/legacy-ref/' + ref).bytes


def fields_priority_start(priority: int, start: str = '') -> bytes:
    held = {FIELD_PRIORITY: int(priority)}
    if start:
        held[FIELD_START] = start
    return _m_side.encode_fields_map(held)


def fields_legacy_id(legacy_id: str) -> bytes:
    return _m_side.encode_fields_map({FIELD_LEGACY_ID: legacy_id})


def fields_legacy_ref(ref: str) -> bytes:
    return _m_side.encode_fields_map({FIELD_LEGACY_REF: ref})


def fields_kind(kind: str) -> bytes:
    return _m_side.encode_fields_map({FIELD_KIND: kind})


def read_fields(value: bytes) -> dict:
    return _m_side.fields_map_or_refuse(value if isinstance(value, bytes) else b'') or {}
