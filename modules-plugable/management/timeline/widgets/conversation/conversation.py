#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
from importlib import import_module
import argparse
import time
_m_check = import_module('modules.knowledge.text.services.text_bytes_check')
_m_content_add = import_module('modules.knowledge.content.services.content_add')
_m_content_read = import_module('modules.knowledge.content.services.content_read')
_m_place = import_module('modules.management.timeline.services.timeline-place.timeline_place')
_m_latest = import_module('modules-plugable.management.timeline.widgets.conversation.get-latest.timeline_latest')
_m_files = import_module('modules.management.timeline.services.timeline_files')
_m_errors = import_module('modules.management.timeline.errors.placement')
_m_folder = import_module('modules-plugable.management.task.services.folder')
folder_of = _m_folder.folder_of
_m_task_files = import_module('modules-plugable.management.task.services.task_memory')
has_task = _m_task_files.has_task
accepts_contents = _m_task_files.accepts_contents
_m_branch_timeline = import_module('modules-plugable.management.timeline.widgets.conversation.branch_timeline')
BranchTimeline = _m_branch_timeline.BranchTimeline
_m_task_store = import_module('bundles.memar_adaptor.git.services.task_store')
DOMAIN = 'conversation'


class Conversation:

    def __init__(self, kind_checks: dict | None = None, clock=time.time) -> None:
        self.kind_checks = kind_checks or {}
        self.clock = clock

    def post(self, contents, placements, timeline, text: str, kind: str, placer: str, after: int, provenance=None) -> int:
        _m_check.check_text(text)
        _m_check.check_substance(text)
        check = self.kind_checks.get(kind)
        if check is not None:
            check(text)
        _, latest_text, found = self.latest(placements, contents, timeline, kind)
        if found and latest_text == text:
            raise _m_errors.Timeline_Error_SameContent()
        content = _m_content_add.add_content(contents, text, kind)
        return _m_place.place_content(placements, timeline, content, kind, placer, after, clock=self.clock, provenance=provenance)

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


def file_timeline(timeline: str, refs=()):
    return BranchTimeline(timeline, refs=refs)


def not_found_reason(timeline: str) -> str:
    """Describe an absent timeline without interpreting predecessor files."""
    return f'no timeline {timeline}, so nothing was read or written'

# No `describe`: public calls are flat (`conversation_post`, …). List them with `memar memar_commands`.
