#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/content_backlinks.py — `memar content backlinks`: which documents link to a file, or to one section of it.

The question an agent changing a document has to ask first: who depends on it.
Answered by resolved path, never by prose — a mention without a link is not a
backlink, a link quoted in code is text about links, and the target's own
in-page links are navigation rather than dependence. A root-relative link
(`/docs/...`) is resolved as `memar content path` resolves it, against the
checkout, so the Memar skill's links, all of that form, are counted.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from services.content_corpus import content_files
from services.content_links import file_links, headings_by_fragment, link_target
from services.content_markdown import without_code
from services.content_reference import content_root, resolve_ref


def describe(verbs):
    parser = verbs.add_parser(
        "backlinks",
        help="list the documents linking to each file",
        description="List the documents linking to each FILE, by resolved "
                    "path: relative links, and root-relative ones (/docs/...) "
                    "resolved as `memar content path` resolves them. "
                    "FILE#anchor keeps only the links whose fragment is that "
                    "anchor.",
        formatter_class=argparse.HelpFormatter,
    )
    parser.add_argument("files", nargs="+", help="FILE or FILE#anchor")
    return run


def run(args: argparse.Namespace) -> None:
    cmd_backlinks(args, content_root())


def _outgoing_file_links(path: Path) -> list[tuple[str, str, int]]:
    """Every link to a file `path` makes, as (file part, fragment, line).

    The same walk the checker judges (`content_links.file_links`), collected
    instead of judged: external and in-page links are not links to another
    document and are left out here as they are there.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return []
    return [(file_part, fragment, line) for line, _, file_part, fragment in file_links(without_code(text))]


def find_backlinks(
    target: Path, docs: list[Path], root: Path, anchor: str | None
) -> list[tuple[Path, int, str]]:
    """Every document in `docs` linking to `target`, as (linker, line, fragment).

    Identity is the resolved path, so a document reached by two spellings is
    still one target, and a link naming a file that is no longer there stops
    matching instead of matching wrongly. Comparison is by path, never by
    prose: a mention without a link is not a backlink, and the target's own
    self-links are not incoming links. `root` is the checkout a root-relative
    link resolves under. `anchor` None keeps every link to the file; an anchor
    keeps only the links whose fragment is that anchor.
    """
    wanted = target.resolve()
    found: list[tuple[Path, int, str]] = []
    for doc in docs:
        resolved_doc = doc.resolve()
        if resolved_doc == wanted:
            continue
        for file_part, fragment, line in _outgoing_file_links(doc):
            if anchor is not None and fragment != anchor:
                continue
            try:
                if link_target(doc, file_part, root).resolve() == wanted:
                    found.append((doc, line, fragment))
            except OSError:
                continue
    return sorted(found, key=lambda hit: (str(hit[0]), hit[1]))


def _answers_to(target: Path, anchor: str) -> bool:
    """Whether a heading of `target` produces `anchor`; True when the file cannot be read, so nothing false is said."""
    try:
        text = target.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return True
    return anchor in headings_by_fragment(without_code(text), text)


def cmd_backlinks(args: argparse.Namespace, root: Path) -> None:
    for file_ref in args.files:
        _, hash_mark, fragment = file_ref.partition("#")
        anchor = fragment if hash_mark else None
        target = resolve_ref(file_ref, root, None)
        try:
            shown = target.relative_to(root)
        except ValueError:
            shown = target
        print(f"== {shown}{'#' + anchor if anchor is not None else ''} ==")
        hits = find_backlinks(target, content_files(root), root, anchor)
        if not hits:
            print("(no incoming links)")
        if anchor is not None and target.suffix.lower() == ".md" and not _answers_to(target, anchor):
            print(f"(no heading in this file answers to #{anchor})")
        for linker, line, link_fragment in hits:
            where = f"#{link_fragment}" if link_fragment else ""
            try:
                linker_shown = linker.relative_to(root)
            except ValueError:
                linker_shown = linker
            print(f"{linker_shown}:{line}{where}")
        print()
