#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/knowledge/content/services/section.py — `memar content section`: one named section of a document, and no more.

A reader who needs the part of a document that governs a step reads that part
rather than the whole. A section is named by its anchor — the fragment a link
uses, `#anchor`, GitHub's `-1` suffix naming a heading's first repeat — or by
its heading's text, whatever its level, the first heading that reads so. Either
way the section is its heading line and runs to the next heading at its level or
above, so its subsections are in it; a `#` inside a fenced block is no heading.
A name no heading answers to is refused with the names that do, so the caller
corrects the name instead of reading the whole document to find it.

A section's hash is the short hash `machine/console_parts.py` names a whole
text by, taken of the section's text with its line endings made LF, so the same
section hashes alike whatever newlines a checkout gave the file; `--hash`
prints it, and a change anywhere in the section, a subsection included, changes it.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import NamedTuple

from machine.console_parts import text_id
from modules.knowledge.content.services.links import anchor_slug, fragments
from modules.knowledge.content.services.reference import content_root, read_text, resolve_ref

HEADING = re.compile(r"^(#{1,6})[ \t]+(.*?)[ \t]*#*[ \t]*$", re.MULTILINE)
ANCHOR_MARK = "#"


def describe(verbs):
    parser = verbs.add_parser(
        "section",
        help="print one named section",
        description="Print one section of FILE: its heading line and everything up to the next heading at its "
        "level or above, its subsections included. HEADING is an anchor when it opens with '#' "
        "('#scope', '#scope-1' for the first repeat of a heading), else a heading's text in any case. "
        "A '#' inside a fenced block is no heading.",
        formatter_class=argparse.HelpFormatter,
    )
    parser.add_argument("file")
    parser.add_argument("heading", help="'#anchor', or a heading's text")
    parser.add_argument(
        "--hash", action="store_true",
        help="print only the section's short hash, which any change in the section, a subsection's included, changes",
    )
    return run


def run(args: argparse.Namespace) -> None:
    cmd_section(args, content_root())


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


def _headings(text: str) -> list[re.Match]:
    """Every heading of TEXT outside a fenced block, of every level, in order."""
    return list(HEADING.finditer(_fenceless(text)))


def _anchors(matches: list[re.Match]) -> list[str]:
    """The fragment each of MATCHES answers to, repeats suffixed as the anchor check of `memar content check` counts them."""
    return fragments([anchor_slug(match.group(2)) for match in matches])


def headings(text: str) -> list[str]:
    """The text of every heading of TEXT outside a fenced block."""
    return [match.group(2).strip() for match in _headings(text)]


def anchors(text: str) -> list[str]:
    """The anchor of every heading of TEXT outside a fenced block."""
    return [anchor for anchor in _anchors(_headings(text)) if anchor]


class Outline(NamedTuple):
    """One heading of a text: where it starts, its level, its text and anchor (empty when its text gives none), and where its section stops."""

    start: int
    level: int
    heading: str
    anchor: str
    stop: int


def outline(text: str) -> list[Outline]:
    """Every heading of TEXT outside a fenced block, in order, with the anchor it answers to and where its section, subsections included, stops."""
    matches = _headings(text)
    found = []
    for number, (match, anchor) in enumerate(zip(matches, _anchors(matches))):
        level = len(match.group(1))
        stop = next((later.start() for later in matches[number + 1 :] if len(later.group(1)) <= level), len(text))
        found.append(Outline(match.start(), level, match.group(2).strip(), anchor or "", stop))
    return found


def _extent(text: str, match: re.Match, matches: list[re.Match]) -> int:
    """Where the section opened by heading MATCH ends: at the next heading at its level or above, else at the end of TEXT."""
    level = len(match.group(1))
    for later in matches[matches.index(match) + 1 :]:
        if len(later.group(1)) <= level:
            return later.start()
    return len(text)


def _span(text: str, first: re.Match | None, matches: list[re.Match], through: str | None) -> tuple[int, int] | None:
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
    return first.start(), end


def span_by_anchor(text: str, anchor: str, through: str | None = None) -> tuple[int, int] | None:
    """Where in TEXT the section `by_anchor` returns starts and ends, so whether one section lies inside another can be told."""
    matches = _headings(text)
    wanted = anchor.lstrip(ANCHOR_MARK)
    first = next((m for m, answer in zip(matches, _anchors(matches)) if answer and answer == wanted), None)
    return _span(text, first, matches, through)


def span_by_heading(text: str, heading: str, through: str | None = None) -> tuple[int, int] | None:
    """Where in TEXT the section `by_heading` returns starts and ends."""
    matches = _headings(text)
    wanted = heading.strip().lower()
    first = next((m for m in matches if m.group(2).strip().lower() == wanted), None)
    return _span(text, first, matches, through)


def by_anchor(text: str, anchor: str, through: str | None = None) -> str | None:
    """The section whose heading answers to ANCHOR, its heading line included; None when no heading does.

    With THROUGH, the text runs on to the end of the section headed THROUGH
    (compared as the heading's text, in any case), so a range of neighbouring
    sections is one read; None too when THROUGH is not a heading after it.
    """
    span = span_by_anchor(text, anchor, through)
    return None if span is None else text[span[0] : span[1]].strip()


def by_heading(text: str, heading: str) -> str | None:
    """The section of the first heading whose text is HEADING, in any case, its heading line included; None when none is."""
    span = span_by_heading(text, heading)
    return None if span is None else text[span[0] : span[1]].strip()


def named(text: str, name: str) -> str | None:
    """The section NAME names: by anchor when NAME opens with `#`, else by heading text; None when no heading answers."""
    return by_anchor(text, name) if name.startswith(ANCHOR_MARK) else by_heading(text, name)


def section_hash(section: str) -> str:
    """The short hash of SECTION's text, its line endings made LF and its outer whitespace dropped."""
    return text_id(section.replace("\r\n", "\n").strip())


def cmd_section(args: argparse.Namespace, root: Path) -> None:
    path = resolve_ref(args.file, root, None)
    text = read_text(path)
    found = named(text, args.heading)
    if found is None:
        by_anchor_name = args.heading.startswith(ANCHOR_MARK)
        available = anchors(text) if by_anchor_name else headings(text)
        sys.exit(
            f"error: no section '{args.heading}' in {path.name}; "
            f"{'anchors' if by_anchor_name else 'headings'}: {' | '.join(available)}"
        )
    print(section_hash(found) if args.hash else found)
