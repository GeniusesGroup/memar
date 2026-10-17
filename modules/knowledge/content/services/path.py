#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/knowledge/content/services/path.py — `memar content path`: a reference turned into the file it means.

The way into the checkout: a link copied out of a Memar document, with its
anchor, becomes the absolute path a reader opens, resolved the way
`content_reference` resolves every reference. The anchor is carried through
untouched, because the file is what is resolved and the heading is the reader's.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from modules.knowledge.content.services.reference import content_root, resolve_ref


def describe(verbs):
    parser = verbs.add_parser(
        "path",
        help="resolve references to absolute paths",
        formatter_class=argparse.HelpFormatter,
    )
    parser.add_argument("refs", nargs="+")
    parser.add_argument(
        "--from", dest="from_file", default=None,
        help="document whose directory relative refs resolve against",
    )
    return run


def run(args: argparse.Namespace) -> None:
    cmd_path(args, content_root())


def cmd_path(args: argparse.Namespace, root: Path) -> None:
    from_file = None
    if args.from_file:
        from_file = resolve_ref(args.from_file, root, None)
    for ref in args.refs:
        anchor = re.split(r"([#?])", ref, maxsplit=1)
        file_part = anchor[0].strip()
        suffix = "".join(anchor[1:]) if len(anchor) > 1 else ""
        resolved = resolve_ref(file_part, root, from_file)
        line = str(resolved)
        if suffix:
            line += suffix
        print(line)
