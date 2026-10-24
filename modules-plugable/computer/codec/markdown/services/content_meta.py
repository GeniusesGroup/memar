#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/knowledge/content/services/meta.py — `memar content meta`: what a document is, before reading it.

Its front matter, or its title where it has none, and its Abstract: enough to
decide whether the document is the one to read, without taking in its body.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from modules.knowledge.content.services.reference import content_root, read_text, resolve_ref


def describe(verbs):
    parser = verbs.add_parser(
        "meta",
        help="print front matter and Abstract",
        formatter_class=argparse.HelpFormatter,
    )
    parser.add_argument("files", nargs="+")
    return run


def run(args: argparse.Namespace) -> None:
    cmd_meta(args, content_root())


def front_matter(text: str) -> str | None:
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[: end + 4].strip()
    return None


def h1(text: str) -> str | None:
    match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    return match.group(1).strip() if match else None


def abstract(text: str) -> str | None:
    match = re.search(
        r"^##\s+Abstract\s*$(.*?)(?=^##\s+|\Z)", text, re.MULTILINE | re.DOTALL
    )
    if not match:
        return None
    return match.group(1).strip()


def cmd_meta(args: argparse.Namespace, root: Path) -> None:
    for file_ref in args.files:
        path = resolve_ref(file_ref, root, None)
        text = read_text(path)
        print(f"== {path.name} ==")
        fm = front_matter(text)
        if fm:
            print(fm)
        else:
            title = h1(text)
            if title:
                print(f"# {title}")
        abstr = abstract(text)
        if abstr:
            print(f"\n## Abstract\n{abstr}")
        print()
