#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
from importlib import import_module
import argparse
from typing import Callable
from machine.console import fail
_m_conversation = import_module('modules-plugable.management.timeline.widgets.conversation.conversation')
_m_errors = import_module('modules.management.timeline.errors.placement')
LATEST_COMMAND = 'latest'


def latest_text(timeline: str, kind: str) -> str:
    files = _m_conversation.file_timeline(timeline)
    try:
        _, text, found = _m_conversation.Conversation().latest(files, files, timeline, kind)
    except _m_errors.Timeline_Error_NotFound:
        fail(_m_conversation.not_found_reason(timeline))
    if not found:
        fail(f'timeline {timeline} holds no content of kind {kind}')
    print(text, end='')
    return text


def describe(verbs) -> Callable[[argparse.Namespace], None]:
    reader = verbs.add_parser(LATEST_COMMAND, help='print the latest content of a kind in a timeline', description='Print the text of the latest content of the kind KIND placed in the timeline TIMELINE, exactly as it\nwas placed. Refused when the timeline holds none of that kind or is no timeline.')
    reader.add_argument('--timeline', required=True, metavar='UUID', help='the UUID of the timeline; the UUID of a task is the UUID of its timeline')
    reader.add_argument('--kind', required=True, metavar='KIND', help='the label word of the template of the content to read')
    return run


def run(args: argparse.Namespace) -> None:
    latest_text(args.timeline, args.kind)
