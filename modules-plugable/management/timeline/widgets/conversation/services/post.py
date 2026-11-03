#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
from importlib import import_module
import argparse
import importlib.util
import sys
from pathlib import Path
from typing import Callable
from machine.console import fail
_m_conversation = import_module('modules-plugable.management.timeline.widgets.conversation.conversation')
Conversation = _m_conversation.Conversation
_m_latest = import_module('modules.management.timeline.services.timeline_latest')
_m_errors = import_module('modules.management.timeline.errors.placement')
_m_bytes = import_module('modules.knowledge.text.errors.bytes')
_m_check = import_module('modules.knowledge.text.services.text_bytes_check')
_m_structure = import_module('modules.knowledge.text.errors.structure')
_m_task_files = import_module('modules-plugable.management.task.services.task_memory')
AUTHOR = _m_task_files.AUTHOR
read_facts = _m_task_files.read_facts
_m_plan_labels = import_module('modules-plugable.management.task.services.plan_labels')
TOPIC = _m_plan_labels.TOPIC
checked_label = _m_plan_labels.checked_label
registry_for = _m_plan_labels.registry_for
_m_task_id = import_module('modules-plugable.management.task.primitive.task_id')
TaskId = _m_task_id.TaskId
from modules.knowledge.label.primitive.label import LabelProblem
POST_COMMAND = 'post'
FIXED_KINDS = ('message',)
TEMPLATE_HOME = Path(__file__).resolve().parents[5] / 'knowledge' / 'documentation'


def template_kinds() -> tuple[str, ...]:
    found = []
    for declaration in sorted(TEMPLATE_HOME.glob('*/content_kinds.py')):
        spec = importlib.util.spec_from_file_location(f'content_kinds_{declaration.parent.name}', declaration)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if (declaration.parent / module.TEMPLATE).is_file():
            found.extend(module.KINDS)
    return tuple(found)
BYTE_REFUSALS = tuple(getattr(_m_bytes, name) for name in dir(_m_bytes) if name.startswith('Text_Error_Bytes_'))


def checked_kind(kind: str, project: Path | None) -> str:
    word = kind.strip()
    if word in FIXED_KINDS or word in template_kinds():
        return word
    registry = registry_for(project)
    for name in registry.kinds:
        try:
            label, fresh = registry.resolve(f'{name}={word}')
        except LabelProblem:
            continue
        if fresh is None:
            return label.title
    checked_label(f'{TOPIC}={word}', project, registry)
    return word


def read_text(content_file: str | None) -> str:
    if content_file:
        try:
            return _m_check.decode_text(Path(content_file).read_bytes())
        except OSError as problem:
            fail(f'{content_file} cannot be read: {problem}')
    return _m_check.decode_text(sys.stdin.buffer.read() if hasattr(sys.stdin, 'buffer') else sys.stdin.read().encode('utf-8'))


def checked_refs(values, timeline: str) -> tuple:
    found = []
    for value in values or ():
        held, separator, number = value.strip().rpartition(':')
        if (separator and not held.strip()) or not number.isascii() or not number.isdigit() or int(number) < 1:
            fail(f'the reference {value} is neither NUMBER nor TIMELINE:NUMBER with a number of one or more, so nothing was written')
        found.append(f'{held.strip() or timeline}:{int(number)}')
    return tuple(found)


def post_text(timeline: str, kind: str, content_file: str | None, author: str | None, refs=()) -> int:
    held = checked_refs(refs, timeline)
    files = _m_conversation.file_timeline(timeline, held)
    store = import_module('modules-plugable.computer.git.services.task_store')
    facts = read_facts(timeline) or {}
    project = (facts.get('project') or '').strip()
    word = checked_kind(kind, Path(project) if project else None)
    try:
        text = read_text(content_file)
        number, _, found = _m_latest.read_latest(files, timeline, word)
        placed = Conversation().post(files, files, timeline, text, word, author or AUTHOR, number if found else 0)
    except _m_structure.Text_Error_Structure_Empty as problem:
        fail(f'the text is refused, so nothing was written: {problem}')
    except BYTE_REFUSALS as problem:
        fail(f'the text is refused, so nothing was written: {problem}')
    except _m_errors.Timeline_Error_Changed:
        fail(f'another content of kind {word} was placed in timeline {timeline} meanwhile, so nothing was written; post it again')
    except _m_errors.Timeline_Error_NotFound:
        fail(_m_conversation.not_found_reason(timeline))
    del store
    print(f'{timeline}  posted content {placed} of kind {word}')
    return placed


def describe(verbs) -> Callable[[argparse.Namespace], None]:
    poster = verbs.add_parser(POST_COMMAND, help='post a text to a timeline as a content of a kind', description=f"Post a text into the timeline TIMELINE as a content of the kind KIND, and print the number of\nits placement. The text is checked for its bytes (a byte-order mark, bytes that are not UTF-8, a\nreplacement character, mojibake, mixed line endings, no final newline) and refused, with nothing\nwritten, when they are wrong. KIND is a word of the label module: plan, report, changelog, message,\na task kind, or a word the project declares (`memar label list`); any other word is refused as the\nlabel module refuses an undeclared one. The text is read from --content-file, or from standard\ninput when none is given. The placer defaults to the agent name '{AUTHOR}', never to a person. A\nplacement is added and never written over: the current plan of a task is its latest content of kind\nplan, so to change it post a new one. When another content of the kind is placed between the read\nand the write, nothing is written and the call is refused: post it again. A timeline in the old\nshape (plan.md and report.md) is refused and nothing is written to it.")
    poster.add_argument('--timeline', required=True, metavar='UUID', help='the UUID of the timeline; the UUID of a task is the UUID of its timeline')
    poster.add_argument('--kind', required=True, metavar='KIND', help='the label word of the template the text is written to: message, a kind a documentation module declares for its template (plan, report, changelog, question, decision, assumption, anticipated-work, research), or a word the project declares')
    poster.add_argument('--content-file', default=None, metavar='FILE', help='the file holding the text; standard input when not given')
    poster.add_argument('--author', default=None, metavar='USERUUID', help=f"who places the text; the agent name '{AUTHOR}' when not given")
    poster.add_argument('--refs', action='append', default=None, metavar='TIMELINE:NUMBER', help='a content this one refers to, written to its refs; TIMELINE:NUMBER, or only NUMBER for a content of this timeline; give the flag again for each reference')
    return run


def run(args: argparse.Namespace) -> None:
    post_text(args.timeline, args.kind, args.content_file, args.author, tuple(args.refs or ()))
