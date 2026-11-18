#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
_m_graph = import_module('modules-plugable.computer.memory.store.graph.graph')
_m_store = import_module('modules.computer.memory.store.protocol.store')
_m_record = import_module('modules-plugable.computer.memory.store.record.record')
_m_errors = import_module('modules.management.timeline.errors.placement')
_m_types = import_module('modules.management.timeline.services.timeline_types')
_m_label_relation = import_module('modules.knowledge.label.edges.label.relation')
Graph_PutEdge = _m_graph.Graph_PutEdge
Graph_ListSidesQuery = _m_graph.Graph_ListSidesQuery
LAYOUT_COMPACT = _m_graph.LAYOUT_COMPACT
Found = _m_store.Found
EVENT_IS = _m_types.EVENT_IS
EVENT_OF = _m_types.EVENT_OF
TASK = 'task'
fields_bytes = _m_types.fields_bytes
fields_of = _m_types.fields_of


def _as_id(value) -> bytes:
    if isinstance(value, bytes):
        return value
    import uuid
    return uuid.UUID(str(value)).bytes


class GraphTimeline:

    def __init__(self, graph, memory, contents) -> None:
        self.graph = graph
        self.memory = memory
        self.contents = contents

    def _exists(self, timeline: bytes) -> bool:
        answer = self.memory.get([_m_record.key(timeline, TASK)])[0]
        if isinstance(answer, Found):
            return True
        for relation in (EVENT_IS, _m_label_relation.LABEL):
            listed = self.graph.list_sides(Graph_ListSidesQuery(timeline, relation))
            if isinstance(listed, (_m_store.Refused, _m_store.Unavailable)):
                return False
            if listed:
                return True
        return False

    def _sides(self, timeline: bytes) -> tuple:
        listed = self.graph.list_sides(Graph_ListSidesQuery(timeline, EVENT_IS))
        if isinstance(listed, (_m_store.Refused, _m_store.Unavailable)):
            raise RuntimeError(listed)
        return listed

    def _kind_of(self, content: bytes) -> str:
        kind, _, found = self.contents.read_content(content)
        return kind if found else ''

    def read_latest_placement(self, timeline, kind: str) -> tuple:
        at = _as_id(timeline)
        if not self._exists(at):
            raise _m_errors.Timeline_Error_NotFound()
        latest = (0, b'', False)
        for side in self._sides(at):
            if self._kind_of(side.To) != kind:
                continue
            held = fields_of(side.Fields)
            number = int(held['number'])
            if number >= latest[0]:
                latest = (number, side.To, True)
        return latest

    def add_placement(self, timeline, content, kind: str, placer: str, placed_at: int, after: int) -> int:
        at = _as_id(timeline)
        target = _as_id(content)
        if not self._exists(at):
            raise _m_errors.Timeline_Error_NotFound()
        number, _, found = self.read_latest_placement(at, kind)
        if found and number != after:
            raise _m_errors.Timeline_Error_Changed()
        if not found and after != 0:
            raise _m_errors.Timeline_Error_Changed()
        next_number = 1
        for side in self._sides(at):
            held = fields_of(side.Fields)
            next_number = max(next_number, int(held['number']) + 1)
        edge = Graph_PutEdge(LAYOUT_COMPACT, at, EVENT_IS, target, EVENT_OF, fields_bytes(next_number, placer, int(placed_at)))
        result = self.graph.put_edge(edge)
        if isinstance(result, (_m_store.Refused, _m_store.Unavailable, _m_store.Conflict)):
            raise RuntimeError(result)
        return next_number

    def list_placements(self, timeline) -> list[dict]:
        at = _as_id(timeline)
        if not self._exists(at):
            raise _m_errors.Timeline_Error_NotFound()
        found = []
        for side in self._sides(at):
            held = fields_of(side.Fields)
            found.append({
                'content': side.To,
                'kind': self._kind_of(side.To),
                'number': int(held['number']),
                'placed_at': int(held['placed_at']),
                'placer': held['placer'],
            })
        found.sort(key=lambda part: part['number'])
        return found
