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
PLAN_NAME = _m_plan_file.PLAN_NAME
front_matter = _m_plan_file.front_matter
plan_shape_problem = _m_plan_file.plan_shape_problem
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
REPORT_NAME = REPORT.file_name
OLD_SHAPE_READER = 'modules-plugable/management/task/services/plan_file.py'
AUTHOR = 'memar'
FACTS = ('title', 'status', 'priority', 'labels', 'depends_on', 'parent', 'conversation', 'project', 'participants', 'start_date')
FRONT_KEY = {'title': PlanKey.TITLE, 'status': PlanKey.STATUS, 'priority': PlanKey.PRIORITY, 'labels': PlanKey.LABELS, 'depends_on': PlanKey.DEPENDS_ON, 'parent': PlanKey.PARENT, 'conversation': PlanKey.CONVERSATION, 'project': PlanKey.PROJECT, 'start_date': PlanKey.START_DATE}
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


def rewrite(path: Path, change: Callable[[list], list]) -> None:
    def make(data: bytes) -> str:
        lines = data.decode('utf-8-sig').splitlines(keepends=True)
        problem = plan_shape_problem([line.rstrip('\r\n') for line in lines])
        if problem:
            fail(f'{path}: {problem}; nothing was written')
        return ''.join(change(lines))
    _replace_file(path, make)


def key_of(line: str) -> str:
    key, colon, _ = line.partition(':')
    return key.strip() if colon else ''


def line_end(line: str) -> str:
    return line[len(line.rstrip('\r\n')):] or '\n'


def has_task(folder: Path) -> bool:
    return (folder / TASK_FACTS_NAME).is_file() or (folder / PLAN_NAME).is_file()


def has_plan(folder: Path) -> bool:
    return has_task(folder)


def read_facts(folder: Path) -> dict | None:
    path = folder / TASK_FACTS_NAME
    if not path.is_file():
        return None
    return _header.parse(read_bytes(path).decode('utf-8-sig').splitlines())


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


def is_new(folder: Path) -> bool:
    return (folder / TASK_FACTS_NAME).is_file()


def _latest_path(folder: Path, kind: str) -> Path:
    content = latest_content(folder, kind) if is_new(folder) else None
    return folder / (_tl.content_name(content.number) if content else TASK_FACTS_NAME)


def plan_path(folder: Path) -> Path:
    return _latest_path(folder, 'plan') if is_new(folder) else folder / PLAN_NAME


def report_path(folder: Path) -> Path:
    return _latest_path(folder, 'report') if is_new(folder) else folder / REPORT_NAME


def plan_text(folder: Path) -> str:
    if is_new(folder):
        return plan_body(folder) or ''
    return read_bytes(folder / PLAN_NAME).decode('utf-8-sig')


def report_text(folder: Path) -> str:
    if is_new(folder):
        content = latest_content(folder, 'report')
        return content.body if content else ''
    return read_bytes(folder / REPORT_NAME).decode('utf-8-sig')


def has_report(folder: Path) -> bool:
    if is_new(folder):
        return latest_content(folder, 'report') is not None
    return (folder / REPORT_NAME).is_file()


def record_names(names) -> list:
    if TASK_FACTS_NAME in names:
        return [TASK_FACTS_NAME, *sorted(name for name in names if _tl.CONTENT_PATTERN.match(name))]
    return [PLAN_NAME, REPORT_NAME]


def record_of(held: dict) -> tuple | None:
    if TASK_FACTS_NAME not in held:
        return None
    front, status = _front_of(_header.parse(held[TASK_FACTS_NAME].decode('utf-8-sig').splitlines()), None)
    matches = [(_tl.CONTENT_PATTERN.match(name), data) for name, data in held.items()]
    reports = [content for content in (_tl.content_of(int(match.group(1)), data) for match, data in matches if match) if content.header.get('kind') == 'report']
    reports.sort(key=lambda content: content.number)
    return (front, status, status_word(reports[-1].header.get('status', '')) if reports else '')


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
    if is_new(folder):
        content = latest_content(folder, 'report')
        if content is None:
            return []
        front = ['---', f'{ReportKey.ID.written}: {folder.name}', f"{ReportKey.STATUS.written}: {content.header.get('status', '')}", '---']
        return [*front, *content.body.splitlines()]
    try:
        return (folder / REPORT_NAME).read_text(encoding='utf-8-sig').splitlines()
    except (OSError, UnicodeDecodeError):
        return []


def create_report_md(folder: Path, text: str) -> None:
    if (folder / TASK_FACTS_NAME).exists():
        return
    try:
        with (folder / REPORT_NAME).open('x', encoding='utf-8', newline='\n') as report:
            report.write(text)
    except FileExistsError:
        pass


def create_plan_md(folder: Path, task: str, title: str, parent, conversation, project: Path, status: str, priority, labels, depends_on) -> None:
    opened = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    text = plan_skeleton(task, title, opened, project, parent=parent, conversation=conversation, status=status, priority=priority, labels=labels, depends_on=depends_on)
    try:
        with (folder / PLAN_NAME).open('x', encoding='utf-8', newline='\n') as plan:
            plan.write(text)
    except FileExistsError:
        pass


def create_task(folder: Path, task: str, title: str, parent, conversation, project: Path, status: str, priority, labels, depends_on) -> None:
    opened = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    plan_text = '\n'.join([f'# {title}', *(line for part in PLAN.parts for line in ('', f'## {part}'))]) + '\n'
    report_text = '\n'.join([f'# {REPORT.heading}', '', *(f'## {part}' for part in REPORT.parts)]) + '\n'
    if not _tl.numbers(folder):
        write_content(folder, 'plan', plan_text, AUTHOR, placed_at=opened)
        write_content(folder, 'report', report_text, AUTHOR, placed_at=opened)
    facts = {'title': title, 'status': status_word(status), 'priority': priority, 'labels': '\n'.join(labels.lines()) if labels else '', 'depends_on': depends_on, 'parent': parent, 'conversation': conversation, 'project': project, 'start_date': opened}
    path = folder / TASK_FACTS_NAME
    temporary = folder / f'.{TASK_FACTS_NAME}.{os.getpid()}.tmp'
    with temporary.open('w', encoding='utf-8', newline='\n') as written:
        written.write(_header.render({key: facts[key] for key in FACTS if key in facts}, BLOCK_FACTS, BLOCK_FACTS))
    try:
        os.link(temporary, path)
    except FileExistsError:
        pass
    finally:
        temporary.unlink(missing_ok=True)


def _block(lines: list, start: int, key: str) -> tuple | None:
    for index in range(1, start - 1):
        if key_of(lines[index]) == key and lines[index].split(':', 1)[1].strip() == '':
            end = index + 1
            while end < start - 1 and lines[end][:1] in (' ', '\t'):
                end += 1
            return (index, end)
    return None


def _plan_read(folder: Path, fact: str) -> str:
    front, _ = front_matter(read_bytes(folder / PLAN_NAME).decode('utf-8-sig').splitlines())
    front = front or {}
    key = FRONT_KEY[fact].written
    if fact == 'labels':
        return '\n'.join(Labels.read(front.get(key, '')).lines())
    value = front.get(key, '')
    return status_word(value) if fact == 'status' else value.strip()


def _plan_write(folder: Path, fact: str, value: str, expected: str) -> str:
    path = folder / PLAN_NAME
    key = FRONT_KEY[fact].written

    def change(lines: list) -> list:
        _, start = front_matter([line.rstrip('\r\n') for line in lines])
        if not start:
            fail(f'{path} has no front matter, so its {key if fact == "depends_on" else fact} cannot be set')
        newline = line_end(lines[0])
        if fact == 'labels':
            found = _block(lines, start, key)
            was = '\n'.join(Labels.read('\n'.join(line.strip() for line in lines[found[0] + 1:found[1]])).lines()) if found else ''
            if _version(was) != expected:
                raise Task_Error_Changed()
            written = [f'{key}:{newline}', *(f'{line}{newline}' for line in value.split('\n') if line)] if value else []
            if found:
                return [*lines[:found[0]], *written, *lines[found[1]:]]
            return [*lines[:start - 1], *written, *lines[start - 1:]]
        for index in range(1, start - 1):
            if key_of(lines[index]) == key:
                current = lines[index].partition(':')[2]
                current = status_word(current) if fact == 'status' else current.strip()
                if _version(current) != expected:
                    raise Task_Error_Changed()
                text = value.capitalize() if fact == 'status' else value
                written = [f'{key}: {text}{line_end(lines[index])}'] if value else []
                return [*lines[:index], *written, *lines[index + 1:]]
        if _version('') != expected:
            raise Task_Error_Changed()
        text = value.capitalize() if fact == 'status' else value
        return [*lines[:start - 1], *([f'{key}: {text}{newline}'] if value else []), *lines[start - 1:]]
    rewrite(path, change)
    return _version(value)


def _yaml_write(folder: Path, fact: str, value: str, expected: str) -> str:
    path = folder / TASK_FACTS_NAME

    def make(data: bytes) -> str:
        pairs = _header.parse(data.decode('utf-8-sig').splitlines())
        if _version(pairs.get(fact, '')) != expected:
            raise Task_Error_Changed()
        pairs[fact] = value
        ordered = {key: pairs[key] for key in (*FACTS, *pairs) if key in pairs}
        return _header.render(ordered, BLOCK_FACTS, BLOCK_FACTS)
    _replace_file(path, make)
    return _version(value)


class FileTaskStores:

    def __init__(self, resolve: Callable) -> None:
        self.resolve = resolve

    def _folder(self, project, task) -> Path:
        folder = self.resolve(project, task)
        if not has_task(folder):
            raise Task_Error_NotFound()
        return folder

    def _read(self, project, task, fact: str) -> tuple:
        folder = self._folder(project, task)
        if (folder / TASK_FACTS_NAME).is_file():
            text = (read_facts(folder) or {}).get(fact, '')
        else:
            text = _plan_read(folder, fact)
        return (text, _version(text))

    def _replace(self, project, task, fact: str, value: str, expected: str) -> str:
        folder = self._folder(project, task)
        if (folder / TASK_FACTS_NAME).is_file():
            return _yaml_write(folder, fact, value, expected)
        return _plan_write(folder, fact, value, expected)

    def _new_folder(self, project, task) -> Path:
        folder = self._folder(project, task)
        if not is_new(folder):
            raise Task_Error_NotFound()
        return folder

    def shape_problem(self, project, task) -> str | None:
        folder = self._folder(project, task)
        path = folder / PLAN_NAME
        if (folder / TASK_FACTS_NAME).is_file() or not path.is_file():
            return None
        return _plan_shape(path)

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


def _plan_shape(path: Path) -> str | None:
    return _m_plan_file.plan_file_problem(path)


def stores_at(folder: Path) -> FileTaskStores:
    return FileTaskStores(lambda project, task: folder)


def stores() -> FileTaskStores:
    def resolve(project, task) -> Path:
        return import_module('modules-plugable.management.task.services.folder').folder_of(task)
    return FileTaskStores(resolve)
