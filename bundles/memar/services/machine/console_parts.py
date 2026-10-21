#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""machine/console_parts.py — print a text too long for one tool output whole, in ordered parts.

A command whose text an agent must hold in its context — `memar ai get-task-init-context`,
`memar content get-act-context` — can print more than an agent runtime's shell tool
returns: past its cut the runtime saves the output to a file and shows a short
preview, and a file the agent may never read is the failure those commands
exist to remove. So such a text is printed in parts, each under the cut, and the
agent runs one command per part: each part but the last ends with a line giving
the exact command for the next, to run now, and the last says it is the last. A
text that fits is printed as it is, with no closing line.

**Where a part ends.** The text is given as passages, in order. A part ends at
the end of a passage while whole passages fit; a passage longer than what is
left of a part is cut at its headings, then, where a heading does not fit, at
its paragraphs. A paragraph is never cut: one longer than a part is a part of its
own, the one case a part passes the bound. Nothing inside a fence (```` ``` ```` or
`~~~`) is a heading or a paragraph's start.

**Stateless.** The parts are a function of the passages and the bound alone,
so a run with the same inputs and `--part N` prints the same Nth part; nothing
is kept between runs.

**Which text a part is of.** Being stateless, a run prints the part of the text
as it is when it runs, and a text that changed between two runs — a document
edited, a file written into the folder a text lists — is another text whose
parts do not join to either. So each part's closing line says "part N of M of
text H", H a short hash of the whole unparted text: every part of one text
names the same H, and a part naming another is of another version, a missing
part is a missing N.

**The bound.** A command's own `--most-characters` is the bound when given;
else the project's preference, which the calling service reads and hands in
(`bound`), so a cold agent given only a fixed brief still has it; else
`MOST_CHARACTERS`. A closing line names the bound only when the flag gave it:
the next run reads the same preference.
"""
from __future__ import annotations
import argparse
import hashlib
import re
import sys
from typing import Callable, Sequence
from machine.console import fail
MOST_CHARACTERS = 24000
TEXT_ID_LENGTH = 12
CLOSING_MARK = '>>>'
PART_FLAG = '--part'
MOST_FLAG = '--most-characters'
HEADING = re.compile('#{1,6} ')
FENCE = re.compile('(```|~~~)')
PASSAGE, SECTION, PARAGRAPH = (0, 1, 2)

def text_id(text: str) -> str:
    """The short hash of TEXT every part of it names."""
    return hashlib.sha256(text.encode('utf-8')).hexdigest()[:TEXT_ID_LENGTH]

def bound(given: int | None, preferred: int | None) -> int:
    """The most characters a part holds: GIVEN by the flag, else PREFERRED by the project, else `MOST_CHARACTERS`."""
    most = given if given is not None else preferred if preferred is not None else MOST_CHARACTERS
    if most <= 0:
        fail(f'{MOST_FLAG} must be a positive number of characters, not {most}')
    return most

def _closing(number: int, count: int, identity: str, command: str | None) -> str:
    named = f'{CLOSING_MARK} part {number} of {count} of text {identity}'
    if command is None:
        return f'{named}, the last: every part has been printed; a part naming another text is of another version.\n'
    return f'{named} ends here. Run `{command}` now for part {number + 1}, and read every part before acting on any of them.\n'

def _cut_points(passages: Sequence[str]) -> dict[int, int]:
    """Where a part may begin, each with how coarse a cut it is: a passage's start, a heading's, a paragraph's."""
    points: dict[int, int] = {}
    position = 0
    for passage in passages:
        if position:
            points[position] = PASSAGE
        fenced, blank_before, offset = (False, False, position)
        for line in passage.splitlines(keepends=True):
            stripped = line.strip()
            if FENCE.match(stripped):
                if not fenced and blank_before and (offset != position):
                    points.setdefault(offset, PARAGRAPH)
                fenced = not fenced
            elif not fenced and offset != position and stripped:
                if HEADING.match(line):
                    points.setdefault(offset, SECTION)
                elif blank_before:
                    points.setdefault(offset, PARAGRAPH)
            blank_before = not stripped and (not fenced)
            offset += len(line)
        position += len(passage)
    return points

def _cut(passages: Sequence[str], room: int) -> list[str]:
    text = ''.join(passages)
    points = _cut_points(passages)
    ordered = sorted(points)
    bodies: list[str] = []
    start = 0
    while start < len(text):
        limit = start + room
        if len(text) <= limit:
            end = len(text)
        else:
            within = [point for point in ordered if start < point <= limit]
            coarsest = min((points[point] for point in within), default=None)
            if coarsest is not None:
                end = max((point for point in within if points[point] == coarsest))
            else:
                end = next((point for point in ordered if point > limit), len(text))
        bodies.append(text[start:end])
        start = end
    return bodies

def _room(passages: Sequence[str], most: int, command: Callable[[int], str]) -> int:
    """What a part's body may hold under MOST, leaving room for the longest closing line it could carry."""
    widest = 10 ** len(str(max(1, sum((len(passage) for passage in passages))))) - 1
    room = most - len(_closing(widest, widest, '0' * TEXT_ID_LENGTH, command(widest)))
    if room <= 0:
        fail(f"{MOST_FLAG} {most} cannot hold a part's closing line; give more characters")
    return room

def cut(passages: Sequence[str], most: int, command: Callable[[int], str]=lambda number: f'{PART_FLAG} {number}') -> list[str]:
    """The bodies of PASSAGES' parts under MOST, in order, without their closing lines; one body when the text fits."""
    text = ''.join(passages)
    if len(text) <= most:
        return [text]
    return _cut(passages, _room(passages, most, command))

def part_text(passages: Sequence[str], number: int, most: int, command: Callable[[int], str]) -> str:
    """Part NUMBER of PASSAGES under MOST, with its closing line, COMMAND(N) being the command that prints part N."""
    bodies = cut(passages, most, command)
    if not 1 <= number <= len(bodies):
        fail(f'there is no part {number}: the text is {len(bodies)} parts long under {most} characters')
    if len(bodies) == 1:
        return bodies[0]
    body = bodies[number - 1]
    body += '' if body.endswith('\n') else '\n'
    identity = text_id(''.join(passages))
    return body + _closing(number, len(bodies), identity, command(number + 1) if number < len(bodies) else None)

def next_command(words: Sequence[str], given: int | None) -> Callable[[int], str]:
    """The command that prints part N: WORDS, the bound when the flag GIVEN it, and the part."""
    flag = [MOST_FLAG, str(given)] if given is not None else []
    return lambda number: ' '.join([*words, *flag, PART_FLAG, str(number)])

def add_part_arguments(parser: argparse.ArgumentParser, preference: str) -> None:
    """The flags of a command that prints in parts; PREFERENCE says where the bound is read when the flag is not given."""
    parser.add_argument(PART_FLAG, type=int, default=1, metavar='N', help='print part N of a text too long for one output; each part names the command for the next')
    parser.add_argument(MOST_FLAG, type=int, default=None, metavar='N', help=f'the most characters one part holds; when not given, {preference}, else {MOST_CHARACTERS:,}, below the smallest output cut known among the runtimes in use')

def print_part(passages: Sequence[str], args: argparse.Namespace, words: Sequence[str], preferred: int | None) -> None:
    """Print the part ARGS asks for of PASSAGES, WORDS being the command that printed it, without its part flags,
    under the flag's bound, else PREFERRED, the project's."""
    most = bound(args.most_characters, preferred)
    sys.stdout.write(part_text(passages, args.part, most, next_command(words, args.most_characters)))
