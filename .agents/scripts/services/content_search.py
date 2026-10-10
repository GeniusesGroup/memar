#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/content_search.py — `memar content search`: where in the checkout's content a term occurs.

The corpus is the one `content_corpus` names — the whole checkout, less the
companions a reader is not sent into and the folders the project does not own —
so a search answers for the content and not for one folder of it. One pattern
prints every matching line; several print each file that holds all of them,
which is how a reader narrows a term too common to read line by line.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from services.content_corpus import content_files
from services.content_reference import content_root, read_text


def describe(verbs):
    parser = verbs.add_parser(
        "search",
        help="regex search the content of the checkout",
        formatter_class=argparse.HelpFormatter,
    )
    parser.add_argument("patterns", nargs="+")
    return run


def run(args: argparse.Namespace) -> None:
    cmd_search(args, content_root())


def cmd_search(args: argparse.Namespace, root: Path) -> None:
    patterns = [re.compile(pattern, re.IGNORECASE) for pattern in args.patterns]
    for path in content_files(root):
        text = read_text(path)
        if all(pattern.search(text) for pattern in patterns):
            if len(patterns) > 1:
                print(f"{path.relative_to(root)}:all-matched")
            else:
                for number, line in enumerate(text.splitlines(), start=1):
                    if patterns[0].search(line):
                        print(f"{path.relative_to(root)}:{number}:{line.strip()}")
