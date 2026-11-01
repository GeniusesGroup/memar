#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
import json
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
_place = import_module('modules.management.timeline.services.timeline_place')
_timeline_graph = import_module('modules.management.timeline.services.timeline_graph')
_attach = import_module('modules.knowledge.label.services.attach')
_status = import_module('modules.knowledge.status.primitive.status')
ABSENT = _m_store.ABSENT
Committed = _m_store.Committed
Found = _m_store.Found
record_key = _m_record.key
Graph_Store = _m_graph.Graph_Store
Graph_ListSidesQuery = _m_graph.Graph_ListSidesQuery
LAYOUT_COMPACT = _m_graph.LAYOUT_COMPACT
TASK_STATUSES = (_status.Status.QUEUED, _status.Status.ACTIVE, _status.Status.BLOCKED, _status.Status.COMPLETE)


class RecordContents:

    def __init__(self, memory) -> None:
        self.memory = memory
        self._kinds: dict[bytes, str] = {}

    def add_content(self, kind: str, text: str) -> bytes:
        content_id = uuid.uuid7().bytes
        text_id = uuid.uuid7().bytes
        content_part = {
            'kind': kind,
            'media_type': _encode.MEDIA_MARKDOWN,
            'text': _encode.uuid_text(text_id),
        }
        writes = [
            (record_key(content_id, _encode.CONTENT), _encode.json_bytes(content_part)),
            (record_key(text_id, _encode.TEXT), text.encode('utf-8')),
        ]
        expect = [(at, ABSENT) for at, _ in writes]
        result = self.memory.batch(expect, writes)
        if not isinstance(result, Committed):
            raise RuntimeError(f'content batch refused: {result!r}')
        self._kinds[content_id] = kind
        return content_id

    def read_content(self, content) -> tuple:
        at = content if isinstance(content, bytes) else uuid.UUID(str(content)).bytes
        if at in self._kinds:
            return (self._kinds[at], '', True)
        answer = self.memory.get([record_key(at, _encode.CONTENT)])[0]
        if not isinstance(answer, Found):
            return ('', '', False)
        part = json.loads(answer.value.decode('utf-8'))
        kind = part.get('kind') or ''
        self._kinds[at] = kind
        return (kind, '', True)


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


def _task_part(folder: Path, facts: dict) -> dict:
    parent = (facts.get('parent') or '').strip()
    part = {
        'legacy_id': folder.name,
        'priority': int((facts.get('priority') or '5').strip() or '5'),
        'title': facts.get('title') or '',
        'type_uuid': _generation.G2_TYPE_UUID,
    }
    conversation = (facts.get('conversation') or '').strip()
    if conversation:
        part['conversation'] = conversation
    start = (facts.get('start_date') or '').strip()
    if start:
        part['start'] = start
    depends = _legacy_list(facts.get('depends_on') or '')
    if depends:
        part['depends_on'] = sorted(depends)
    if parent:
        part['parents'] = [parent]
    return part


def _placed_at_unix(header: dict) -> int:
    text = (header.get('placed_at') or '').strip()
    if not text:
        return 0
    from datetime import datetime, timezone
    try:
        return int(datetime.strptime(text, _tl.INSTANT_FORMAT).replace(tzinfo=timezone.utc).timestamp())
    except ValueError:
        return 0


def _set_status_label(graph, task_id: bytes, status: str) -> None:
    word = _task_files.status_word(status) or 'queued'
    value = _status.Status.read(word) or _status.Status.QUEUED
    _attach.put_label(graph, task_id, value.label)


def _attach_plan_labels(graph, facts: dict, task_id: bytes) -> None:
    from modules.knowledge.label.primitive.label import Labels
    raw = facts.get('labels') or ''
    for label in Labels.read(raw):
        _attach.put_label(graph, task_id, label)


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
        rows.append({
            'to': _encode.uuid_text(side.To),
            'number': int(fields['number']),
            'placer': fields['placer'],
            'placed_at': int(fields['placed_at']),
        })
    rows.sort(key=lambda row: row['number'])
    return rows


def convert_g1_folder(folder: Path, store) -> bytes:
    facts = _facts(folder)
    task_id = uuid.uuid7().bytes
    contents = RecordContents(store)
    graph = Graph_Store(store, LAYOUT_COMPACT)
    timeline = _timeline_graph.GraphTimeline(graph, store, contents)
    task_writes = [
        (record_key(task_id, _encode.TASK), _encode.json_bytes(_task_part(folder, facts))),
    ]
    expect = [(at, ABSENT) for at, _ in task_writes]
    result = store.batch(expect, task_writes)
    if not isinstance(result, Committed):
        raise RuntimeError(f'task batch refused: {result!r}')
    _set_status_label(graph, task_id, facts.get('status') or 'queued')
    _attach_plan_labels(graph, facts, task_id)
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
    answer = store.get([record_key(task_id, _encode.TASK)])[0]
    if not isinstance(answer, Found):
        raise RuntimeError(f'task part absent: {answer!r}')
    return json.loads(answer.value.decode('utf-8'))
