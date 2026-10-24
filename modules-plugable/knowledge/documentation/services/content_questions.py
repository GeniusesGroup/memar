#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/knowledge/documentation/services/content_questions.py — `memar content questions`: what the handoffs still ask the owner.

Every entry under an `Open Questions` heading of a `*.handoff.md` is open by
being present ([Open Questions](../../../modules-plugable/knowledge/documentation/handoff/handoff.md#open-questions)),
so the list is the entries, one `path:line: heading` hit per line, read from
the heading's own line. An entry whose `Blocks` field (or the older `Blocks
continuation`) names something that cannot continue is marked `[blocks]`, and
those print first, oldest `Asked` date first, because they are what the person
answering many questions needs first.

The scope is one of: a handoff file, a folder (searched recursively for
`*.handoff.md`), or a project (`--project NAME`, a name `memar project
list` shows, or `--project-path PATH`, its folder), alone or with a file or folder inside it. With none,
the whole checkout is read.
"""
from __future__ import annotations
from importlib import import_module
import argparse
import os
import re
import sys
_m_handoff_section = import_module('modules-plugable.knowledge.documentation.handoff.primitive.handoff_section')
HandoffSection = _m_handoff_section.HandoffSection
from pathlib import Path
HANDOFF_SUFFIX = '.handoff.md'
SECTION = HandoffSection.OPEN_QUESTIONS.heading
BLOCKING_MARK = '[blocks]'
EMPTY = '(no open questions)'
SKIPPED_FOLDERS = {'.git', 'node_modules', 'temp', '__pycache__'}
_HEADING = re.compile('^(#{1,6})\\s+(.*?)\\s*#*\\s*$')
_FENCE = re.compile('^\\s*(```|~~~)')
_BLOCKS = re.compile('^\\s*-\\s+\\*{0,2}Blocks(?: continuation)?\\*{0,2}\\s*:\\s*(.*)$', re.I)
_ASKED = re.compile('^\\s*-\\s+\\*{0,2}Asked\\*{0,2}\\s*:\\s*(\\d{4}-\\d{2}-\\d{2})', re.I)
_NO = re.compile('^(no|none|nothing)\\b', re.I)
_YES = re.compile('\\byes\\b', re.I)
NO_DATE = '9999-99-99'

def describe(verbs):
    from modules.process.project.primitive.project_name import ProjectName
    from modules.process.project.primitive.project_path import ProjectPath
    parser = verbs.add_parser('questions', help='list open handoff questions as path:line: heading hits', description=f'List the entries under `Open Questions` in `*.handoff.md` files as one `path:line: heading` hit per line, blocking entries first (marked [blocks]), then oldest Asked date first. SCOPE is a handoff file or a folder; {ProjectName.FLAG} {ProjectName.METAVAR} names a project by a name `memar project list` shows, {ProjectPath.FLAG} {ProjectPath.METAVAR} by its folder. No arguments means the whole checkout.', formatter_class=argparse.HelpFormatter)
    parser.add_argument('scope', nargs='?', default=None, help=f'a handoff file or a folder (inside the project, with {ProjectName.FLAG} or {ProjectPath.FLAG})')
    from modules.process.project.services.find import add_project_flags
    add_project_flags(parser, 'read this project instead of the checkout')
    parser.add_argument('--blocking', action='store_true', help='list only entries that block')
    return run

def run(args: argparse.Namespace) -> None:
    from modules.knowledge.content.services.reference import content_root
    cmd_questions(args, content_root())

def is_blocking(text: str) -> bool:
    """Whether a Blocks field names something that cannot continue.

    A field that opens with no/none/nothing and has no `yes` in it blocks
    nothing; one that says `no for X; yes for Y` blocks Y, so it blocks.
    """
    text = text.strip()
    if not text:
        return False
    return not (_NO.match(text) and (not _YES.search(text)))

def open_questions(path: Path) -> list[tuple[int, str, bool, str]]:
    """(line, heading, blocking, asked) for each entry under `Open Questions` of PATH."""
    lines = path.read_text(encoding='utf-8').splitlines()
    found: list[list] = []
    section_level = 0
    entry_level = 0
    fenced = False
    current = None
    for number, line in enumerate(lines, 1):
        if _FENCE.match(line):
            fenced = not fenced
            continue
        if fenced:
            continue
        heading = _HEADING.match(line)
        if heading:
            level, title = (len(heading.group(1)), heading.group(2))
            if section_level and level <= section_level:
                section_level = 0
                current = None
            if not section_level:
                if title == SECTION:
                    section_level = level
                    entry_level = level + 1
                continue
            if level == entry_level:
                current = [number, title, False, NO_DATE]
                found.append(current)
            continue
        if current is not None:
            blocks = _BLOCKS.match(line)
            if blocks:
                current[2] = is_blocking(blocks.group(1))
                continue
            asked = _ASKED.match(line)
            if asked:
                current[3] = asked.group(1)
    return [tuple(entry) for entry in found]

def handoff_files(base: Path) -> list[Path]:
    if base.is_file():
        return [base]
    found: list[Path] = []
    for folder, names, files in os.walk(base):
        names[:] = sorted((n for n in names if n not in SKIPPED_FOLDERS))
        found.extend((Path(folder) / f for f in sorted(files) if f.endswith(HANDOFF_SUFFIX)))
    return found

def cmd_questions(args: argparse.Namespace, root: Path) -> None:
    from modules.process.project.services.find import project_from_args
    project = project_from_args(args)
    base = home = root
    if project is not None:
        base = home = project
    if args.scope:
        scoped = Path(args.scope).expanduser()
        base = scoped if scoped.is_absolute() else base / scoped
        if not base.exists():
            sys.exit(f'error: {args.scope} is not a file or folder' + (f' of the project {project}' if project else ''))
    hits = []
    for path in handoff_files(base):
        for line, heading, blocking, asked in open_questions(path):
            if args.blocking and (not blocking):
                continue
            hits.append((not blocking, asked, str(path), line, path, heading, blocking))
    hits.sort(key=lambda h: h[:4])
    if not hits:
        print(EMPTY)
        return
    for _, _, _, line, path, heading, blocking in hits:
        try:
            shown = path.relative_to(home)
        except ValueError:
            shown = path
        print(f'{shown}:{line}: {heading}' + (f' {BLOCKING_MARK}' if blocking else ''))
