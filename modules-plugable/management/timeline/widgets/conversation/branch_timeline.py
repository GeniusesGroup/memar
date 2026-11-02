#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""A timeline backed by the records branch — no task folder on disk."""
from __future__ import annotations
from importlib import import_module
import re
import uuid
from datetime import datetime, timezone
_m_errors = import_module('modules.management.timeline.errors.placement')
Timeline_Error_Changed = _m_errors.Timeline_Error_Changed
Timeline_Error_NotFound = _m_errors.Timeline_Error_NotFound
_m_header = import_module('modules.knowledge.text.services.header_text')
_m_files = import_module('modules.management.timeline.services.timeline_files')
CONTENT_PATTERN = _m_files.CONTENT_PATTERN
content_name = _m_files.content_name
content_of = _m_files.content_of
INSTANT_FORMAT = _m_files.INSTANT_FORMAT
_m_task_store = import_module('modules-plugable.computer.git.services.task_store')

class BranchTimeline:

    def __init__(self, timeline: str, refs=(), project=None) -> None:
        self.timeline = timeline
        self.refs = tuple(refs)
        self.project = project
        self.pending: dict = {}

    def _tree(self) -> dict[str, bytes]:
        return _m_task_store.tree(self.timeline, self.project)

    def _exists(self) -> bool:
        files = self._tree()
        return 'task.yaml' in files or any(CONTENT_PATTERN.match(name) for name in files)

    def _contents(self) -> list:
        files = self._tree()
        numbers = sorted(int(match.group(1)) for name, match in ((n, CONTENT_PATTERN.match(n)) for n in files) if match)
        return [content_of(number, files[content_name(number)]) for number in numbers]

    def _latest(self, kind: str):
        found = [content for content in self._contents() if content.header.get('kind') == kind]
        return found[-1] if found else None

    def add_content(self, kind: str, text: str) -> str:
        content = str(uuid.uuid4())
        self.pending[content] = (kind, text)
        return content

    def read_content(self, content: str) -> tuple:
        if content in self.pending:
            kind, text = self.pending[content]
            return (kind, text, True)
        for held in reversed(self._contents()):
            if held.header.get('content') == content:
                return (held.header.get('kind', ''), held.body, True)
        return ('', '', False)

    def read_latest_placement(self, timeline, kind: str) -> tuple:
        del timeline
        held = self._latest(kind)
        return (held.number, held.header.get('content', ''), True) if held else (0, '', False)

    def add_placement(self, timeline, content: str, kind: str, placer: str, placed_at: int, after: int) -> int:
        del timeline
        if not self._exists():
            raise Timeline_Error_NotFound()
        _, text, found = self.read_content(content)
        if not found:
            raise Timeline_Error_NotFound()
        files = self._tree()
        if after and any(c.header.get('kind') == kind and c.number > after for c in self._contents()):
            raise Timeline_Error_Changed()
        numbers = sorted(int(match.group(1)) for name, match in ((n, CONTENT_PATTERN.match(n)) for n in files) if match)
        number = (numbers[-1] if numbers else 0) + 1
        header = {'kind': kind, 'author': placer, 'placed_at': datetime.fromtimestamp(placed_at, timezone.utc).strftime(INSTANT_FORMAT), 'content': content}
        if after:
            header['follows'] = str(after)
        if self.refs:
            header['refs'] = '\n'.join(self.refs)
        rendered = f'---\n{_m_header.render(header, ("refs",))}---\n{text}'.encode('utf-8')
        name = content_name(number)
        if name in files:
            raise Timeline_Error_Changed()
        _m_task_store.put_files(self.timeline, {name: rendered}, self.project, message=f'Record task {self.timeline} content {number}\n')
        self.pending.pop(content, None)
        return number
