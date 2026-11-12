#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import json
import uuid
from importlib import import_module
_m_graph = import_module('modules-plugable.computer.memory.store.graph.graph')
_m_store = import_module('modules.computer.memory.store.protocol.store')
_m_rank = import_module('modules-plugable.identity.thing.priority.primitive.rank')
_m_priority_label = import_module('modules-plugable.identity.thing.priority.labels.Priority')
_m_errors = import_module('modules-plugable.identity.thing.priority.errors.errors')
Graph_PutEdge = _m_graph.Graph_PutEdge
Graph_ListSidesQuery = _m_graph.Graph_ListSidesQuery
Priority_Rank = _m_rank.Priority_Rank
GraphRank_Error_Changed = _m_errors.GraphRank_Error_Changed
GraphRank_Error_Refused = _m_errors.GraphRank_Error_Refused
Conflict = _m_store.Conflict
_NS = uuid.NAMESPACE_URL
_BASE = 'memar://modules-plugable/identity/thing/priority/relation/'
PRIORITY = uuid.uuid5(_NS, _BASE + 'priority').bytes
PRIORITY_OF = uuid.uuid5(_NS, _BASE + 'priority_of').bytes
VERTEX = uuid.UUID(_m_priority_label.Label_Priority.id).bytes
ATTEMPTS = 5


class _PriorityOnGraph:

    def __init__(self, graph) -> None:
        self.graph = graph

    def get_rank(self, thing: bytes) -> Priority_Rank | None:
        return self._rank_of(self._held(self._sides(thing)))

    def put_rank(self, thing: bytes, rank: Priority_Rank) -> None:
        wanted = Priority_Rank(int(rank))
        fields = json.dumps({Priority_Rank.TYPE_UUID: int(wanted)}).encode('utf-8')
        for _ in range(ATTEMPTS):
            sides = self._sides(thing)
            held = self._held(sides)
            if held is not None and self._rank_of(held) == wanted:
                return
            token = sides[0].Token if sides else b''
            if held is not None:
                answer = self.graph.set_side_fields(held.Ref, fields, token)
            else:
                answer = self.graph.put_edge(Graph_PutEdge(self.graph.layout, thing, PRIORITY, VERTEX, PRIORITY_OF, fields, token))
            if isinstance(answer, Conflict):
                continue
            if isinstance(answer, (_m_store.Refused, _m_store.Unavailable)):
                raise GraphRank_Error_Refused(answer)
            return
        raise GraphRank_Error_Changed()

    def _sides(self, thing: bytes) -> tuple:
        listed = self.graph.list_sides(Graph_ListSidesQuery(thing, PRIORITY))
        if isinstance(listed, (_m_store.Refused, _m_store.Unavailable)):
            raise GraphRank_Error_Refused(listed)
        return tuple(listed)

    def _held(self, sides: tuple):
        return next((side for side in sides if side.To == VERTEX), None)

    def _rank_of(self, side) -> Priority_Rank | None:
        if side is None:
            return None
        try:
            return Priority_Rank(int(json.loads(side.Fields)[Priority_Rank.TYPE_UUID]))
        except (ValueError, KeyError, TypeError):
            return None


def priority_on_graph(graph) -> _PriorityOnGraph:
    return _PriorityOnGraph(graph)
