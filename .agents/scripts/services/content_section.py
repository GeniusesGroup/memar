#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/content_section.py — `memar content section`: one named section of a document, and no more.

A reader who needs the part of a document that governs a step reads that part
rather than the whole. The heading is matched by its text, whatever its level,
and the section runs to the next heading at its level or above; a heading that
is not there is refused with the ones that are, so the caller corrects the name
instead of reading the whole document to find it.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from services.content_check import anchor_slug
from services.content_reference import content_root, read_text, resolve_ref


def describe(verbs):
    parser = verbs.add_parser(
        "section",
        help="print one named section",
        formatter_class=argparse.HelpFormatter,
    )
    parser.add_argument("file")
    parser.add_argument("heading")
    return run


def run(args: argparse.Namespace) -> None:
    cmd_section(args, content_root())


def headings(text: str) -> list[str]:
    pattern = re.compile(r"^(#{2,6})\s+(.*?)\s*#*\s*$", re.MULTILINE)
    return [match.group(2).strip() for match in pattern.finditer(text)]


def section(text: str, heading: str) -> str | None:
    pattern = re.compile(r"^(#{2,6})\s+(.*?)\s*#*\s*$", re.MULTILINE)
    matches = list(pattern.finditer(text))
    wanted = heading.strip().lower()
    for index, match in enumerate(matches):
        title = match.group(2).strip()
        if title.lower() != wanted:
            continue
        level = len(match.group(1))
        start = match.end()
        end = len(text)
        for later in matches[index + 1 :]:
            if len(later.group(1)) <= level:
                end = later.start()
                break
        return text[start:end].strip()
    return None


def _fenceless(text: str) -> str:
    """TEXT with the lines inside fenced blocks blanked, keeping every offset, so a `#` in a code block is no heading."""
    out, fenced = [], False
    for line in text.splitlines(keepends=True):
        if line.lstrip().startswith(("```", "~~~")):
            fenced = not fenced
            out.append(line)
        else:
            out.append(re.sub(r"[^\r\n]", " ", line) if fenced else line)
    return "".join(out)


def _extent(text: str, match: re.Match, matches: list[re.Match]) -> int:
    """Where the section opened by heading MATCH ends: at the next heading at its level or above, else at the end of TEXT."""
    level = len(match.group(1))
    for later in matches[matches.index(match) + 1 :]:
        if len(later.group(1)) <= level:
            return later.start()
    return len(text)


def by_anchor(text: str, anchor: str, through: str | None = None) -> str | None:
    """The section whose heading answers to ANCHOR, its heading line included; None when no heading does.

    With THROUGH, the text runs on to the end of the section headed THROUGH
    (compared as the heading's text, in any case), so a range of neighbouring
    sections is one read; None too when THROUGH is not a heading after it.
    """
    visible = _fenceless(text)
    matches = list(re.finditer(r"^(#{2,6})[ ]+(.*?)[ ]*#*[ ]*$", visible, re.MULTILINE))
    first = next((m for m in matches if anchor_slug(m.group(2)) == anchor.lstrip("#")), None)
    if first is None:
        return None
    end = _extent(text, first, matches)
    if through is not None:
        last = next(
            (m for m in matches if m.start() > first.start() and m.group(2).strip().lower() == through.strip().lower()),
            None,
        )
        if last is None:
            return None
        end = _extent(text, last, matches)
    return text[first.start() : end].strip()


def cmd_section(args: argparse.Namespace, root: Path) -> None:
    path = resolve_ref(args.file, root, None)
    text = read_text(path)
    found = section(text, args.heading)
    if found is None:
        available = headings(text)
        sys.exit(
            f"error: no section '{args.heading}' in {path.name}; "
            f"headings: {' | '.join(available)}"
        )
    print(found)
