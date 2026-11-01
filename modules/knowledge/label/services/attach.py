#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import uuid
from importlib import import_module
from modules.knowledge.label.primitive.label import Label
_m_graph = import_module('modules-plugable.computer.memory.store.graph.graph')
_m_store = import_module('modules.computer.memory.store.protocol.store')
Graph_PutEdge = _m_graph.Graph_PutEdge
Graph_ListSidesQuery = _m_graph.Graph_ListSidesQuery
LAYOUT_COMPACT = _m_graph.LAYOUT_COMPACT
_NS = uuid.NAMESPACE_URL
_BASE = 'memar://modules/knowledge/label/relation/'
LABEL = uuid.uuid5(_NS, _BASE + 'label').bytes
LABEL_OF = uuid.uuid5(_NS, _BASE + 'label_of').bytes


def id_bytes(label: Label) -> bytes:
    return uuid.UUID(label.id).bytes


def put_label(graph, thing: bytes, label: Label) -> bytes:
    result = graph.put_edge(Graph_PutEdge(LAYOUT_COMPACT, thing, LABEL, id_bytes(label), LABEL_OF, b'', b''))
    if isinstance(result, (_m_store.Refused, _m_store.Unavailable, _m_store.Conflict)):
        raise RuntimeError(f'label edge refused: {result!r}')
    return result if isinstance(result, bytes) else result[0]


def list_label_ids(graph, thing: bytes) -> list[bytes]:
    listed = graph.list_sides(Graph_ListSidesQuery(thing, LABEL))
    if isinstance(listed, (_m_store.Refused, _m_store.Unavailable)):
        raise RuntimeError(listed)
    return [side.To for side in listed]
