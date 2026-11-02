#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.identity.thing.labels.Label_Queued import Label_Queued
from modules.identity.thing.labels.Label_Complete import Label_Complete
from modules.identity.thing.labels.Label_Blocked import Label_Blocked
from modules.identity.thing.labels.Label_Active import Label_Active
from importlib import import_module
import uuid
from pathlib import Path
_m_store = import_module('modules.computer.memory.store.protocol.store')
_m_record = import_module('modules-plugable.computer.memory.store.record.record')
_m_graph = import_module('modules-plugable.computer.memory.store.graph.graph')
_generation = import_module('modules-plugable.management.task.services.task_generation')
_predecessor = import_module('modules-plugable.management.task.services.task_predecessor_adapter')
_task_files = import_module('modules-plugable.management.task.services.task_files')
_tl = import_module('modules.management.timeline.services.timeline_files')
_encode = import_module('modules-plugable.management.task.services.task_g2_encode')
_types = import_module('modules-plugable.management.task.services.task_graph_types')
_place = import_module('modules.management.timeline.services.timeline_place')
_timeline_graph = import_module('modules.management.timeline.services.timeline_graph')
_attach = import_module('modules.knowledge.label.services.attach')
_status = import_module('modules.knowledge.label.services.status_words')
ABSENT = _m_store.ABSENT
Committed = _m_store.Committed
Found = _m_store.Found
record_key = _m_record.key
Graph_Store = _m_graph.Graph_Store
Graph_PutEdge = _m_graph.Graph_PutEdge
Graph_ListSidesQuery = _m_graph.Graph_ListSidesQuery
LAYOUT_COMPACT = _m_graph.LAYOUT_COMPACT
TASK_STATUSES = (_status.Label_Queued, _status.Label_Active, _status.Label_Blocked, _status.Label_Complete)


class RecordContents:

    def __init__(self, memory, graph) -> None:
        self.memory = memory
        self.graph = graph
        self._kinds: dict[bytes, str] = {}
        self._bodies: dict[bytes, bytes] = {}

    def add_content(self, kind: str, text: str) -> bytes:
        content_id = uuid.uuid7().bytes
        text_id = uuid.uuid7().bytes
        body = text.encode('utf-8')
        writes = [(record_key(text_id, _encode.TEXT), body)]
        expect = [(at, ABSENT) for at, _ in writes]
        result = self.memory.batch(expect, writes)
        if not isinstance(result, Committed):
            raise RuntimeError(f'content batch refused: {result!r}')
        put = self.graph.put_edge(Graph_PutEdge(
            LAYOUT_COMPACT, content_id, _types.HAS_BODY, text_id, _types.HAS_BODY_OF, _types.fields_kind(kind), b'', b'',
        ))
        if isinstance(put, (_m_store.Refused, _m_store.Unavailable, _m_store.Conflict)):
            raise RuntimeError(f'has_body edge refused: {put!r}')
        self._kinds[content_id] = kind
        self._bodies[content_id] = text_id
        return content_id

    def read_content(self, content) -> tuple:
        at = content if isinstance(content, bytes) else uuid.UUID(str(content)).bytes
        if at in self._kinds:
            return (self._kinds[at], '', True)
        listed = self.graph.list_sides(Graph_ListSidesQuery(at, _types.HAS_BODY))
        if isinstance(listed, tuple) and listed:
            fields = _types.read_fields(listed[0].Fields)
            kind = fields.get(_types.FIELD_KIND) or ''
            self._kinds[at] = kind
            return (kind, '', True)
        return ('', '', False)

    def body_id(self, content_id: bytes) -> bytes | None:
        if content_id in self._bodies:
            return self._bodies[content_id]
        listed = self.graph.list_sides(Graph_ListSidesQuery(content_id, _types.HAS_BODY))
        if isinstance(listed, tuple) and listed:
            return listed[0].To
        return None


def _facts(folder: Path) -> dict:
    if (folder / _task_files.TASK_FACTS_NAME).is_file():
        held = _task_files.read_facts(folder) or {}
    else:
        held = _predecessor.read_facts(folder)
    return held


def _legacy_list(value: str) -> list:
    text = (value or '').strip()
    if not text:
        return []
    return text.splitlines() if '\n' in text else [text]


def _placed_at_unix(header: dict) -> int:
    text = (header.get('placed_at') or '').strip()
    if not text:
        return 0
    from datetime import datetime, timezone
    try:
        return int(datetime.strptime(text, _tl.INSTANT_FORMAT).replace(tzinfo=timezone.utc).timestamp())
    except ValueError:
        return 0


def _put(graph, frm: bytes, relation: bytes, to: bytes, reverse: bytes, fields: bytes = b'') -> None:
    result = graph.put_edge(Graph_PutEdge(LAYOUT_COMPACT, frm, relation, to, reverse, fields, b'', b''))
    if isinstance(result, (_m_store.Refused, _m_store.Unavailable, _m_store.Conflict)):
        raise RuntimeError(f'edge refused: {result!r}')


def _set_status_label(graph, task_id: bytes, status: str) -> None:
    word = _task_files.status_word(status) or 'queued'
    value = _status.read_status(word) or _status.Label_Queued
    _attach.put_label(graph, task_id, value.label)


def _attach_plan_labels(graph, facts: dict, task_id: bytes) -> None:
    from modules.knowledge.label.primitive.label import Labels
    raw = facts.get('labels') or ''
    for label in Labels.read(raw):
        _attach.put_label(graph, task_id, label)


def _write_task_edges(graph, store, folder: Path, facts: dict, task_id: bytes) -> None:
    project = (facts.get('project') or '').strip()
    priority = int((facts.get('priority') or '5').strip() or '5')
    start = (facts.get('start_date') or '').strip()
    _put(graph, _types.project_id(project), _types.HAS_TASK, task_id, _types.HAS_TASK_OF, _types.fields_priority_start(priority, start))
    title = facts.get('title') or ''
    if title:
        text_id = uuid.uuid7().bytes
        result = store.batch([(record_key(text_id, _encode.TEXT), ABSENT)], [(record_key(text_id, _encode.TEXT), title.encode('utf-8'))])
        if not isinstance(result, Committed):
            raise RuntimeError(f'title text refused: {result!r}')
        _put(graph, task_id, _types.TITLE, text_id, _types.TITLE_OF, b'')
    type_id = uuid.UUID(_generation.G2_TYPE_UUID).bytes
    _put(graph, task_id, _types.TYPE_IS, type_id, _types.TYPE_OF, b'')
    _put(graph, task_id, _types.LEGACY, task_id, _types.LEGACY_OF, _types.fields_legacy_id(folder.name))
    parent = (facts.get('parent') or '').strip()
    if parent:
        _put(graph, task_id, _types.PARENT, _types.legacy_ref_id(parent), _types.PARENT_OF, _types.fields_legacy_ref(parent))
    conversation = (facts.get('conversation') or '').strip()
    if conversation:
        _put(graph, task_id, _types.CONVERSATION, _types.legacy_ref_id(conversation), _types.CONVERSATION_OF, _types.fields_legacy_ref(conversation))
    for dep in _legacy_list(facts.get('depends_on') or ''):
        _put(graph, task_id, _types.DEPENDS_ON, _types.legacy_ref_id(dep), _types.DEPENDS_FOR, _types.fields_legacy_ref(dep))


def read_status_label(store, task_id: bytes) -> str:
    graph = Graph_Store(store, LAYOUT_COMPACT)
    held = set(_attach.list_label_ids(graph, task_id))
    for value in TASK_STATUSES:
        if _attach.id_bytes(value.label) in held:
            return value.key
    return ''


def list_event_is(store, task_id: bytes) -> list[dict]:
    graph = Graph_Store(store, LAYOUT_COMPACT)
    listed = graph.list_sides(Graph_ListSidesQuery(task_id, _timeline_graph.EVENT_IS))
    if isinstance(listed, (_m_store.Refused, _m_store.Unavailable)):
        raise RuntimeError(listed)
    rows = []
    for side in listed:
        fields = _timeline_graph.fields_of(side.Fields)
        kind = ''
        bodies = graph.list_sides(Graph_ListSidesQuery(side.To, _types.HAS_BODY))
        if isinstance(bodies, tuple) and bodies:
            kind = _types.read_fields(bodies[0].Fields).get(_types.FIELD_KIND) or ''
        rows.append({
            'to': _encode.uuid_text(side.To),
            'number': int(fields['number']),
            'placer': fields['placer'],
            'placed_at': int(fields['placed_at']),
            'kind': kind,
        })
    rows.sort(key=lambda row: row['number'])
    return rows


def convert_g1_folder(folder: Path, store) -> bytes:
    facts = _facts(folder)
    task_id = uuid.uuid7().bytes
    graph = Graph_Store(store, LAYOUT_COMPACT)
    contents = RecordContents(store, graph)
    timeline = _timeline_graph.GraphTimeline(graph, store, contents)
    _set_status_label(graph, task_id, facts.get('status') or 'queued')
    _attach_plan_labels(graph, facts, task_id)
    _write_task_edges(graph, store, folder, facts, task_id)
    after_by_kind: dict[str, int] = {}
    for content in _tl.read_contents(folder):
        kind = (content.header.get('kind') or '').strip() or 'message'
        placer = (content.header.get('author') or '').strip() or 'memar'
        content_id = contents.add_content(kind, content.body)
        after = after_by_kind.get(kind, 0)
        instant = _placed_at_unix(content.header) or 1
        number = _place.place_content(
            timeline,
            task_id,
            content_id,
            kind,
            placer,
            after,
            clock=lambda instant=instant: instant,
        )
        after_by_kind[kind] = number
    return task_id


def dump_task_part(store, task_id: bytes) -> dict:
    """Inspectable projection from edges — not a stored domain blob."""
    graph = Graph_Store(store, LAYOUT_COMPACT)
    part: dict = {}
    legacy = graph.list_sides(Graph_ListSidesQuery(task_id, _types.LEGACY))
    if isinstance(legacy, tuple) and legacy:
        fields = _types.read_fields(legacy[0].Fields)
        if _types.FIELD_LEGACY_ID in fields:
            part['legacy_id'] = fields[_types.FIELD_LEGACY_ID]
    titles = graph.list_sides(Graph_ListSidesQuery(task_id, _types.TITLE))
    if isinstance(titles, tuple) and titles:
        text = store.get([record_key(titles[0].To, _encode.TEXT)])[0]
        if isinstance(text, Found):
            part['title'] = text.value.decode('utf-8')
    types = graph.list_sides(Graph_ListSidesQuery(task_id, _types.TYPE_IS))
    if isinstance(types, tuple) and types:
        part['type_uuid'] = _encode.uuid_text(types[0].To)
    parents = graph.list_sides(Graph_ListSidesQuery(task_id, _types.PARENT))
    if isinstance(parents, tuple) and parents:
        refs = []
        for side in parents:
            fields = _types.read_fields(side.Fields)
            refs.append(fields.get(_types.FIELD_LEGACY_REF) or _encode.uuid_text(side.To))
        part['parents'] = refs
    conversations = graph.list_sides(Graph_ListSidesQuery(task_id, _types.CONVERSATION))
    if isinstance(conversations, tuple) and conversations:
        fields = _types.read_fields(conversations[0].Fields)
        part['conversation'] = fields.get(_types.FIELD_LEGACY_REF) or _encode.uuid_text(conversations[0].To)
    depends = graph.list_sides(Graph_ListSidesQuery(task_id, _types.DEPENDS_ON))
    if isinstance(depends, tuple) and depends:
        part['depends_on'] = sorted(
            (_types.read_fields(side.Fields).get(_types.FIELD_LEGACY_REF) or _encode.uuid_text(side.To))
            for side in depends
        )
    for project_probe in graph.list_sides(Graph_ListSidesQuery(task_id, _types.HAS_TASK_OF)):
        # inbound rebuilt: has_task_of points to project; priority is on project's has_task side
        break
    # priority lives on project → task has_task; find by scanning reverse
    # Graph list from task via HAS_TASK_OF to project, then project's HAS_TASK sides
    projects = graph.list_sides(Graph_ListSidesQuery(task_id, _types.HAS_TASK_OF))
    if isinstance(projects, tuple):
        for project_side in projects:
            sides = graph.list_sides(Graph_ListSidesQuery(project_side.To, _types.HAS_TASK))
            if not isinstance(sides, tuple):
                continue
            for side in sides:
                if side.To == task_id:
                    fields = _types.read_fields(side.Fields)
                    if _types.FIELD_PRIORITY in fields:
                        part['priority'] = int(fields[_types.FIELD_PRIORITY])
                    if _types.FIELD_START in fields:
                        part['start'] = fields[_types.FIELD_START]
    return part
