#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
from importlib import import_module
import os
import re
import stat
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, NamedTuple
_m_errors = import_module('modules.management.timeline.errors.placement')
Timeline_Error_Changed = _m_errors.Timeline_Error_Changed
Timeline_Error_NotFound = _m_errors.Timeline_Error_NotFound
_m_header = import_module('modules.knowledge.text.services.header_text')

CONTENT_WIDTH = 5
CONTENT_EXTENSION = '.md'
CONTENT_PATTERN = re.compile(rf'^content\.(\d{{{CONTENT_WIDTH}}}){re.escape(CONTENT_EXTENSION)}$')
INSTANT_FORMAT = '%Y-%m-%dT%H:%M:%SZ'


class Content(NamedTuple):
    number: int
    header: dict
    body: str


def is_content_file(path: Path) -> bool:
    return CONTENT_PATTERN.match(path.name) is not None


def content_name(number: int) -> str:
    return f'content.{number:0{CONTENT_WIDTH}d}{CONTENT_EXTENSION}'


def numbers(folder: Path) -> list:
    try:
        names = [entry.name for entry in folder.iterdir()]
    except OSError:
        return []
    return sorted(int(match.group(1)) for match in map(CONTENT_PATTERN.match, names) if match)


def content_of(number: int, data: bytes) -> Content:
    text = data.decode('utf-8-sig')
    lines = text.splitlines(keepends=True)
    if lines and lines[0].strip() == '---':
        for end in range(1, len(lines)):
            if lines[end].strip() == '---':
                return Content(number, _m_header.parse([line.rstrip('\r\n') for line in lines[1:end]]), ''.join(lines[end + 1:]))
    return Content(number, {}, text)


def read_content_file(folder: Path, number: int) -> Content:
    return content_of(number, (folder / content_name(number)).read_bytes())


def read_contents(folder: Path) -> list:
    return [read_content_file(folder, number) for number in numbers(folder)]


def latest_content(folder: Path, kind: str) -> Content | None:
    found = [content for content in read_contents(folder) if content.header.get('kind') == kind]
    return found[-1] if found else None


def _newer_than(folder: Path, kind: str, follows: int, below: int | None = None) -> bool:
    return any(content.header.get('kind') == kind and content.number > follows and (below is None or content.number < below) for content in read_contents(folder))


def write_content(folder: Path, kind: str, text: str, author: str, follows: int | None = None, refs=(), fields: dict | None = None, placed_at: str | None = None) -> int:
    header = {'kind': kind, 'author': author, 'placed_at': placed_at or datetime.now(timezone.utc).strftime(INSTANT_FORMAT)}
    if follows:
        header['follows'] = str(follows)
    if refs:
        header['refs'] = '\n'.join(refs)
    header.update({key: str(value) for key, value in (fields or {}).items()})
    rendered = f'---\n{_m_header.render(header, ("refs",))}---\n{text}'
    while True:
        if follows is not None and _newer_than(folder, kind, follows):
            raise Timeline_Error_Changed()
        held = numbers(folder)
        number = (held[-1] if held else 0) + 1
        path = folder / content_name(number)
        try:
            handle = path.open('x', encoding='utf-8', newline='\n')
        except FileExistsError:
            continue
        with handle:
            handle.write(rendered)
        os.chmod(path, stat.S_IREAD)
        if follows is not None and _newer_than(folder, kind, follows, below=number):
            os.chmod(path, stat.S_IREAD | stat.S_IWRITE)
            path.unlink()
            raise Timeline_Error_Changed()
        return number


def add_text(folder: Path, kind: str, text: str, author: str, refs=(), fields: dict | None = None) -> int:
    latest = latest_content(folder, kind)
    return write_content(folder, kind, text, author, follows=latest.number if latest else None, refs=refs, fields=fields)


class FileTimeline:

    def __init__(self, resolve: Callable, exists: Callable, home: Path | None = None) -> None:
        self.resolve = resolve
        self.exists = exists
        self.home = home
        self.pending: dict = {}

    def _folder(self, timeline) -> Path:
        folder = self.resolve(timeline)
        if not self.exists(folder):
            raise Timeline_Error_NotFound()
        return folder

    def add_content(self, kind: str, text: str) -> str:
        content = str(uuid.uuid4())
        self.pending[content] = (kind, text)
        return content

    def read_content(self, content: str) -> tuple:
        if content in self.pending:
            kind, text = self.pending[content]
            return (kind, text, True)
        if self.home is not None:
            for held in reversed(read_contents(self.home)):
                if held.header.get('content') == content:
                    return (held.header.get('kind', ''), held.body, True)
        return ('', '', False)

    def read_latest_placement(self, timeline, kind: str) -> tuple:
        held = latest_content(self._folder(timeline), kind)
        return (held.number, held.header.get('content', ''), True) if held else (0, '', False)

    def add_placement(self, timeline, content: str, kind: str, placer: str, placed_at: int, after: int) -> int:
        folder = self._folder(timeline)
        _, text, found = self.read_content(content)
        if not found:
            raise Timeline_Error_NotFound()
        instant = datetime.fromtimestamp(placed_at, timezone.utc).strftime(INSTANT_FORMAT)
        number = write_content(folder, kind, text, placer, follows=after, fields={'content': content}, placed_at=instant)
        self.pending.pop(content, None)
        return number
