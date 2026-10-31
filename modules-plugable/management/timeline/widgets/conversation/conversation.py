#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
from importlib import import_module
import argparse
import time
_m_check = import_module('modules.knowledge.text.services.text_bytes_check')
_m_content_add = import_module('modules.knowledge.content.services.content_add')
_m_content_read = import_module('modules.knowledge.content.services.content_read')
_m_place = import_module('modules.management.timeline.services.timeline_place')
_m_latest = import_module('modules.management.timeline.services.timeline_latest')
_m_files = import_module('modules.management.timeline.services.timeline_files')
_m_errors = import_module('modules.management.timeline.errors.placement')
_m_folder = import_module('modules-plugable.management.task.services.folder')
folder_of = _m_folder.folder_of
_m_task_files = import_module('modules-plugable.management.task.services.task_files')
has_task = _m_task_files.has_task
is_new = _m_task_files.is_new
DOMAIN = 'conversation'


class Conversation:

    def __init__(self, kind_checks: dict | None = None, clock=time.time) -> None:
        self.kind_checks = kind_checks or {}
        self.clock = clock

    def post(self, contents, placements, timeline, text: str, kind: str, placer: str, after: int) -> int:
        _m_check.check_text(text)
        _m_check.check_substance(text)
        check = self.kind_checks.get(kind)
        if check is not None:
            check(text)
        content = _m_content_add.add_content(contents, text, kind)
        return _m_place.place_content(placements, timeline, content, kind, placer, after, clock=self.clock)

    def latest(self, placements, contents, timeline, kind: str) -> tuple:
        number, content, found = _m_latest.read_latest(placements, timeline, kind)
        if not found:
            return (0, '', False)
        _, text, read = _m_content_read.read_content(contents, content)
        return (number, text, read)

    def share(self, contents, placements, content: str, timeline, placer: str, after: int) -> int:
        kind, _, found = _m_content_read.read_content(contents, content)
        if not found:
            raise _m_errors.Timeline_Error_NotFound()
        return _m_place.place_content(placements, timeline, content, kind, placer, after, clock=self.clock)


def file_timeline(timeline: str):
    folder = folder_of(timeline)
    return _m_files.FileTimeline(lambda held: folder, lambda held: is_new(held), home=folder)


def not_found_reason(timeline: str) -> str:
    if has_task(folder_of(timeline)):
        return f'timeline {timeline} is in the old shape (plan.md and report.md), which {_m_task_files.OLD_SHAPE_READER} reads; nothing was written'
    return f'no timeline {timeline}, so nothing was read or written'


def describe(verbs) -> None:
    verbs.add_parser(DOMAIN, help='say into a timeline and read what was said', description="A conversation is what is said into a timeline: a text of any kind is checked, made a content and placed\nin the timeline of a UUID, and the latest content of a kind is read back. A timeline is named by the UUID\nof the node it belongs to; the UUID of a task is the UUID of its timeline. A placement is added and never\nwritten over; a correction is a new content. The words and flags of each verb are its own help.")
