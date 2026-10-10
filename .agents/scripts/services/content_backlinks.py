#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/content_backlinks.py — `memar content backlinks`: which documents link to a file.

The question an agent changing a document has to ask first: who depends on it.
Answered by resolved path, never by prose — a mention without a link is not a
backlink, a link quoted in code is text about links, and the target's own
in-page links are navigation rather than dependence.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from services.content_corpus import content_files
from services.content_markdown import EXTERNAL_LINK, without_code
from services.content_reference import content_root, resolve_ref

_LINK_TARGET = re.compile(r"\]\(([^)\s]+)\)")


def describe(verbs):
    parser = verbs.add_parser(
        "backlinks",
        help="list the documents linking to each file",
        formatter_class=argparse.HelpFormatter,
    )
    parser.add_argument("files", nargs="+")
    return run


def run(args: argparse.Namespace) -> None:
    cmd_backlinks(args, content_root())


def _outgoing_file_links(path: Path) -> list[tuple[str, str, int]]:
    """Every relative file link `path` makes, as (file part, fragment, line).

    The same walk the checker judges, collected instead of judged: external,
    site-root, and in-page links are not links to another document and are
    left out here as they are there.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return []
    visible = without_code(text)
    found: list[tuple[str, str, int]] = []
    for match in _LINK_TARGET.finditer(visible):
        link = match.group(1)
        if EXTERNAL_LINK.match(link):
            continue
        file_part, _, fragment = link.partition("#")
        if not file_part or file_part.startswith("/"):
            continue
        line = visible[: match.start()].count("\n") + 1
        found.append((file_part, fragment, line))
    return found


def find_backlinks(target: Path, docs: list[Path]) -> list[tuple[Path, int, str]]:
    """Every document in `docs` linking to `target`, as (linker, line, fragment).

    Identity is the resolved path, so a document reached by two spellings is
    still one target, and a link naming a file that is no longer there stops
    matching instead of matching wrongly. Comparison is by path, never by
    prose: a mention without a link is not a backlink, and the target's own
    self-links are not incoming links.
    """
    wanted = target.resolve()
    found: list[tuple[Path, int, str]] = []
    for doc in docs:
        resolved_doc = doc.resolve()
        if resolved_doc == wanted:
            continue
        for file_part, fragment, line in _outgoing_file_links(doc):
            try:
                if (doc.parent / file_part).resolve() == wanted:
                    found.append((doc, line, fragment))
            except OSError:
                continue
    return sorted(found, key=lambda hit: (str(hit[0]), hit[1]))


def cmd_backlinks(args: argparse.Namespace, root: Path) -> None:
    for file_ref in args.files:
        target = resolve_ref(file_ref, root, None)
        try:
            shown = target.relative_to(root)
        except ValueError:
            shown = target
        print(f"== {shown} ==")
        hits = find_backlinks(target, content_files(root))
        if not hits:
            print("(no incoming links)")
        for linker, line, fragment in hits:
            where = f"#{fragment}" if fragment else ""
            try:
                linker_shown = linker.relative_to(root)
            except ValueError:
                linker_shown = linker
            print(f"{linker_shown}:{line}{where}")
        print()
