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
