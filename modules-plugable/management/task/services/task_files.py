#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
from importlib import import_module
import hashlib
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable
from machine.console import fail
_m_errors = import_module('modules-plugable.management.task.errors.errors')
Task_Error_Changed = _m_errors.Task_Error_Changed
Task_Error_NotFound = _m_errors.Task_Error_NotFound
_tl = import_module('modules.management.timeline.services.timeline_files')
_header = import_module('modules.knowledge.text.services.header_text')
read_contents = _tl.read_contents
latest_content = _tl.latest_content
write_content = _tl.write_content
_m_plan_file = import_module('modules-plugable.management.task.services.plan_file')
_generation = import_module('modules-plugable.management.task.services.task_generation')
plan_skeleton = _m_plan_file.plan_skeleton
read_bytes = _m_plan_file.read_bytes
status_word = _m_plan_file.status_word
REWRITE_ATTEMPTS = _m_plan_file.REWRITE_ATTEMPTS
REWRITE_PAUSE_SECONDS = _m_plan_file.REWRITE_PAUSE_SECONDS
_m_record = import_module('modules-plugable.knowledge.documentation.primitive.record')
PLAN = _m_record.PLAN
REPORT = _m_record.REPORT
_m_plan_key = import_module('modules-plugable.knowledge.documentation.plan.primitive.plan_key')
PlanKey = _m_plan_key.PlanKey
_m_report_key = import_module('modules-plugable.knowledge.documentation.report.primitive.report_key')
ReportKey = _m_report_key.ReportKey
_m_priority = import_module('modules-plugable.knowledge.documentation.plan.primitive.priority')
Priority = _m_priority.Priority
from modules.knowledge.label.primitive.label import Labels

TASK_FACTS_NAME = 'task.yaml'
AUTHOR = 'memar'
FACTS = ('title', 'status', 'priority', 'labels', 'depends_on', 'parent', 'conversation', 'project', 'participants', 'start_date', 'writer', 'converted_from')
FRONT_KEY = {'title': PlanKey.TITLE, 'priority': PlanKey.PRIORITY, 'labels': PlanKey.LABELS, 'depends_on': PlanKey.DEPENDS_ON, 'parent': PlanKey.PARENT, 'conversation': PlanKey.CONVERSATION, 'project': PlanKey.PROJECT, 'start_date': PlanKey.START_DATE}
BLOCK_FACTS = ('labels', 'participants')
PLAIN_START = '"\'[]{}&*!|>%@`-?#,'


def _version(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()[:16]


def _replace_file(path: Path, make: Callable[[bytes], str]) -> None:
    for _ in range(REWRITE_ATTEMPTS):
        data = read_bytes(path)
        text = make(data)
        temporary = path.with_name(f'.{path.name}.{os.getpid()}.tmp')
        try:
            with temporary.open('w', encoding='utf-8', newline='') as written:
                written.write(text)
            if read_bytes(path) == data:
                os.replace(temporary, path)
                return
        except PermissionError:
            time.sleep(REWRITE_PAUSE_SECONDS)
        finally:
            temporary.unlink(missing_ok=True)
    fail(f'{path} kept changing while it was being rewritten, so nothing was written; try again')


def line_end(line: str) -> str:
    return line[len(line.rstrip('\r\n')):] or '\n'


def _task_id(task) -> str:
    return task if isinstance(task, str) else Path(task).name


def has_task(folder) -> bool:
    if isinstance(folder, Path) and folder.is_dir():
        return (folder / TASK_FACTS_NAME).is_file()
    store = import_module('modules-plugable.computer.git.services.task_store')
    return TASK_FACTS_NAME in store.tree(_task_id(folder))


def has_plan(folder) -> bool:
    return has_task(folder)


def read_facts(folder) -> dict | None:
    if isinstance(folder, Path) and folder.is_dir():
        path = folder / TASK_FACTS_NAME
        if not path.is_file():
            return None
        return _header.parse(read_bytes(path).decode('utf-8-sig').splitlines())
    store = import_module('modules-plugable.computer.git.services.task_store')
    data = store.tree(_task_id(folder)).get(TASK_FACTS_NAME)
    if data is None:
        return None
    return _header.parse(data.decode('utf-8-sig').splitlines())


def _front_of(facts: dict, task: str | None) -> tuple:
    front = {PlanKey.ID.key: task} if task else {}
    for key, value in facts.items():
        if key in FRONT_KEY:
            front[FRONT_KEY[key].key] = value
    return (front, status_word(facts.get('status', '')))


def plan_front(folder: Path) -> tuple | None:
    facts = read_facts(folder)
    if facts is None:
        return None
    return _front_of(facts, folder.name)


def _latest_path(folder: Path, kind: str) -> Path:
    content = latest_content(folder, kind)
    return folder / (_tl.content_name(content.number) if content else TASK_FACTS_NAME)


def plan_path(folder: Path) -> Path:
    return _latest_path(folder, 'plan')


def report_path(folder: Path) -> Path:
    return _latest_path(folder, 'report')


def plan_text(folder: Path) -> str:
    return plan_body(folder) or ''


def report_text(folder: Path) -> str:
    content = latest_content(folder, 'report')
    return content.body if content else ''


def has_report(folder: Path) -> bool:
    return latest_content(folder, 'report') is not None


def record_names(names) -> list:
    if TASK_FACTS_NAME in names:
        return [TASK_FACTS_NAME, *sorted(name for name in names if _tl.CONTENT_PATTERN.match(name))]
    return []


def record_of(held: dict) -> tuple | None:
    if TASK_FACTS_NAME not in held:
        return None
    return _front_of(_header.parse(held[TASK_FACTS_NAME].decode('utf-8-sig').splitlines()), None)


def facts_named_project(data: bytes, name: str) -> bytes:
    lines = data.decode('utf-8-sig').splitlines(keepends=True)
    for index, line in enumerate(lines):
        if line.startswith('project:'):
            lines[index] = f'project: {_header.scalar(name)}{line_end(line)}'
            break
    return ''.join(lines).encode('utf-8')


def plan_body(folder: Path) -> str | None:
    if read_facts(folder) is None:
        return None
    content = latest_content(folder, 'plan')
    return content.body if content else ''


def report_lines(folder: Path) -> list:
    content = latest_content(folder, 'report')
    if content is None:
        return []
    front = ['---', f'{ReportKey.ID.written}: {folder.name}', '---']
    return [*front, *content.body.splitlines()]


def facts_bytes(facts: dict) -> bytes:
    return _header.render({key: facts[key] for key in FACTS if key in facts}, BLOCK_FACTS, BLOCK_FACTS).encode('utf-8')


def write_facts(folder, facts: dict) -> None:
    """Write facts onto the records branch for the task id (folder Path or id string)."""
    store = import_module('modules-plugable.computer.git.services.task_store')
    refused = import_module('modules-plugable.computer.git.services.branch').RecordRefused
    task = _task_id(folder)
    project = facts.get('project')
    try:
        store.put_files(task, {TASK_FACTS_NAME: facts_bytes(facts)}, Path(project) if project else None, message=f'Record task {task}\n')
    except refused as error:
        fail(f'task {task} could not be recorded on the records branch ({error})')


def create_task(folder, task: str, title: str, parent, conversation, project: Path, status: str, priority, labels, depends_on) -> None:
    opened = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    write_facts(task, {'title': title, 'status': status_word(status), 'priority': priority, 'labels': '\n'.join(labels.lines()) if labels else '', 'depends_on': depends_on, 'parent': parent, 'conversation': conversation, 'project': project, 'start_date': opened, 'writer': _generation.TASK_TYPE_UUID})


def _yaml_write(task_id: str, fact: str, value: str, expected: str, project=None) -> str:
    store = import_module('modules-plugable.computer.git.services.task_store')
    refused = import_module('modules-plugable.computer.git.services.branch').RecordRefused
    data = store.tree(task_id).get(TASK_FACTS_NAME)
    if data is None:
        raise Task_Error_NotFound()
    pairs = _header.parse(data.decode('utf-8-sig').splitlines())
    if _version(pairs.get(fact, '')) != expected:
        raise Task_Error_Changed()
    pairs[fact] = value
    ordered = {key: pairs[key] for key in (*FACTS, *pairs) if key in pairs}
    rendered = _header.render(ordered, BLOCK_FACTS, BLOCK_FACTS).encode('utf-8')
    try:
        store.put_files(task_id, {TASK_FACTS_NAME: rendered}, Path(project) if project is not None else None, message=f'Record task {task_id}\n')
    except refused as error:
        fail(f'task {task_id} could not be recorded on the records branch ({error})')
    return _version(value)


class FileTaskStores:

    def __init__(self, resolve: Callable) -> None:
        self.resolve = resolve

    def _task(self, project, task) -> str:
        resolved = self.resolve(project, task)
        task_id = _task_id(resolved)
        if not has_task(task_id):
            raise Task_Error_NotFound()
        return task_id

    def _read(self, project, task, fact: str) -> tuple:
        text = (read_facts(self._task(project, task)) or {}).get(fact, '')
        return (text, _version(text))

    def _replace(self, project, task, fact: str, value: str, expected: str) -> str:
        return _yaml_write(self._task(project, task), fact, value, expected, project)

    def read_priority(self, project, task) -> tuple:
        text, version = self._read(project, task, 'priority')
        return (Priority.of({PlanKey.PRIORITY.key: text}), version)

    def replace_priority(self, project, task, priority, expected: str) -> str:
        return self._replace(project, task, 'priority', str(priority), expected)

    def read_status(self, project, task) -> tuple:
        return self._read(project, task, 'status')

    def replace_status(self, project, task, status: str, expected: str) -> str:
        return self._replace(project, task, 'status', status_word(status), expected)

    def read_labels(self, project, task) -> tuple:
        text, version = self._read(project, task, 'labels')
        return (Labels.read(text), version)

    def replace_labels(self, project, task, labels, expected: str) -> str:
        return self._replace(project, task, 'labels', '\n'.join(labels.lines()), expected)

    def read_depends_on(self, project, task) -> tuple:
        dependency = import_module('modules-plugable.management.task.services.dependency')
        text, version = self._read(project, task, 'depends_on')
        return (dependency.DependsOn.of({PlanKey.DEPENDS_ON.key: text}), version)

    def replace_depends_on(self, project, task, cited, expected: str) -> str:
        return self._replace(project, task, 'depends_on', cited.text() if cited else '', expected)


def stores_at(folder) -> FileTaskStores:
    task_id = _task_id(folder)
    return FileTaskStores(lambda project, task: task_id)


def stores() -> FileTaskStores:
    return FileTaskStores(lambda project, task: task)
