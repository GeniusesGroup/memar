#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/knowledge/content/services/find.py — `memar content find`: the sections of the checkout's content most like a text, ranked.

For what no normative-references list reaches: a subject that enters the work midway, or a
question the lists do not answer. `search` answers where a term occurs; this answers which
sections are about a text, best first, so a reader opens the few that matter instead of grepping.
It is informative and nothing more: it ranks by word similarity, binds nobody, and does not find
what an act must read — that is what `memar content context` prints from the lists of
[Normative References](../rules/normative_references/normative_references.md).

The ranking and its corpus are `modules/knowledge/content/services/index.py`'s, with the support its constants have.
**A hit** is one line: the checkout's name, the document's path and the section's anchor, the
heading, the section's first sentence cut at `SENTENCE_LIMIT` characters with links reduced to
their text, and the section's hash, the one `memar content section FILE '#anchor' --hash` prints
and an entry of a list records. **Link expansion**, on by default: under each hit, the sections it
links by anchor, one level, each once, indented and marked; a linked section is one an author tied
to the hit, which carries the author's judgment and not a similarity. `--no-links` turns it off.
A reader opens a hit with `memar content section FILE '#anchor'`.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

COMMAND = "find"
# The first line of the output: what it is, and where what an act must read is printed.
INFORMATIVE = (
    "informative: ranked by word similarity; the normative references of an act are printed by `memar content context`"
)
TOP = 10
SENTENCE_LIMIT = 160
LINKED = "    linked from above: "
MARKDOWN_LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")
# A full stop ends a sentence unless it ends a list number (" 1.").
SENTENCE_END = re.compile(r"(?<=[.!?])(?<!\s\d\.)\s")
FRONT_MATTER = re.compile(r"\A---\r?\n.*?\r?\n---\r?\n", re.DOTALL)
NO_HEADING = "(before the first heading)"


def describe(verbs):
    from modules.process.project.services.find import add_project_flags

    parser = verbs.add_parser(
        COMMAND,
        help="rank the sections of the checkout's content by word similarity to a text",
        description=(
            f"{INFORMATIVE}.\n"
            "\n"
            "Print the sections of the checkout's content most like TEXT, best first, one line each:\n"
            "root:path#anchor | heading | first sentence | hash. The hash is the one\n"
            "`memar content section FILE '#anchor' --hash` prints. Under each hit are the sections it\n"
            "links by anchor, one level, each once, marked; --no-links leaves them out. Open a hit with\n"
            "`memar content section FILE '#anchor'`. The words are compared as they are written, with no\n"
            "stemming, and a section whose heading holds them ranks above one that mentions them. It\n"
            "does not find what an act must read: that is printed by `memar content context`. To see\n"
            "where a term occurs, use `memar content search`."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("text", help="the words to look for: a subject, a question, a sentence")
    parser.add_argument("--top", type=int, default=TOP, metavar="N", help=f"how many hits to print (default {TOP})")
    parser.add_argument("--no-links", dest="links", action="store_false", help="leave out the sections each hit links")
    add_project_flags(parser, "the project whose files are the corpus; without either, Memar's checkout")
    return run


def _sentence(text: str, heading: bool) -> str:
    """The first sentence of TEXT, a unit's text, past its heading line and front matter, cut at `SENTENCE_LIMIT`."""
    body = FRONT_MATTER.sub("", text, count=1)
    lines = body.splitlines()
    if heading and lines and lines[0].lstrip().startswith("#"):
        lines = lines[1:]
    paragraph = []
    for line in lines:
        if line.strip():
            paragraph.append(line.strip())
        elif paragraph:
            break
    flat = MARKDOWN_LINK.sub(r"\1", " ".join(paragraph))
    first = SENTENCE_END.split(flat, maxsplit=1)[0] if flat else ""
    return first if len(first) <= SENTENCE_LIMIT else first[: SENTENCE_LIMIT - 1].rstrip() + "…"


def _line(index, unit, label: str) -> str:
    where = f"{label}:{unit.path}" + (" (kh)" if unit.kh else (f"#{unit.anchor}" if unit.anchor else ""))
    heading = unit.heading or NO_HEADING
    sentence = _sentence(index.text_of(unit), heading=bool(unit.heading) and not unit.kh)
    return f"{where} | {heading} | {sentence} | {unit.hash}"


def find_lines(root: Path, query: str, top: int = TOP, links: bool = True, label: str | None = None) -> list[str]:
    """The output for QUERY over the checkout at ROOT: the informative line, then the TOP best hits, each followed by the sections it links when LINKS.

    LABEL names ROOT in a hit; the folder's name when not given.
    """
    from modules.knowledge.content.services.index import build

    name = label or root.name
    index = build(root)
    ranked = index.rank(query)[: max(top, 0)]
    where = {(unit.path, unit.anchor): number for number, unit in enumerate(index.units) if unit.anchor}
    shown = set(ranked)
    lines = [INFORMATIVE]
    for number in ranked:
        lines.append(_line(index, index.units[number], name))
        if not links:
            continue
        for target in index.units[number].links:
            linked = where.get(target)
            if linked is not None and linked not in shown:
                shown.add(linked)
                lines.append(LINKED + _line(index, index.units[linked], name))
    return lines


def run(args: argparse.Namespace) -> None:
    import sys

    from machine.console import fail
    from modules.knowledge.content.services.reference import content_root
    from modules.process.project.services.find import project_from_args

    if args.top < 1:
        fail("--top must be a positive whole number")
    project = project_from_args(args)
    root = content_root()
    label = "memar"
    if project is not None:
        root, label = project, project.name
    lines = find_lines(root, args.text, args.top, args.links, label)
    print("\n".join(lines))
    if len(lines) == 1:
        print("no section holds a word of the text", file=sys.stderr)
