#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/knowledge/content/services/search.py — `memar content search`: where in the checkout's content a term occurs.

The corpus is the one `content_corpus` names — the whole checkout, less the
companions a reader is not sent into and the folders the project does not own —
so a search answers for the content and not for one folder of it. One pattern
prints every matching line; several print each file that holds all of them,
which is how a reader narrows a term too common to read line by line.

`--from` says which sources the corpus is made of (`CorpusSource`): the
documents and the code when it is not given, as before it existed; the sessions
only when named, read by `session_records.py`, each hit naming the session and
the file it came from. Whatever of the sessions could not be read is said on
standard error, so an empty answer is not taken for an absence.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from modules.knowledge.content.services.corpus import content_files
from modules.knowledge.content.services.reference import content_root, read_text


def describe(verbs):
    from modules.knowledge.content.primitive.corpus_source import CorpusSource
    from modules.process.project.services.find import add_project_flags

    parser = verbs.add_parser(
        "search",
        help="regex search the content of the checkout",
        description=(
            "Print where in the content each PATTERN, a regular expression matched in any case, occurs.\n"
            "One pattern prints each matching line as path:line:text; several print each file that\n"
            "holds all of them as path:all-matched. A path that begins with the records branch, or that\n"
            "lies in a session folder, is a session's record: what that session wrote, never a ruling.\n"
            "What is read is chosen with --from; what of the sessions could not be read is said on\n"
            "standard error. To rank sections by how alike they are to a text, use `memar content find`."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("patterns", nargs="+")
    CorpusSource.add_flag(parser)
    add_project_flags(parser, "the project whose content is searched; without either, Memar's checkout")
    return run


def run(args: argparse.Namespace) -> None:
    from modules.knowledge.content.primitive.corpus_source import CorpusSource
    from modules.process.project.services.find import project_from_args

    project = project_from_args(args)
    root = project if project is not None else content_root()
    cmd_search(args, root, CorpusSource.chosen(args))


def cmd_search(args: argparse.Namespace, root: Path, sources=None) -> None:
    from modules.knowledge.content.primitive.corpus_source import CorpusSource

    chosen = CorpusSource.default() if sources is None else tuple(sources)
    patterns = [re.compile(pattern, re.IGNORECASE) for pattern in args.patterns]
    for path in content_files(root, chosen):
        _print_matches(str(path.relative_to(root)), read_text(path), patterns)
    if CorpusSource.SESSIONS not in chosen:
        return
    from modules.knowledge.content.services.session_records import read_all, session_records

    records, notes = session_records(root)
    texts = read_all(root, records)
    for record in records:
        if record.path in texts:
            _print_matches(record.path, texts[record.path], patterns)
    for note in notes:
        print(note, file=sys.stderr)


def _print_matches(where: str, text: str, patterns: list[re.Pattern]) -> None:
    if not all(pattern.search(text) for pattern in patterns):
        return
    if len(patterns) > 1:
        print(f"{where}:all-matched")
        return
    for number, line in enumerate(text.splitlines(), start=1):
        if patterns[0].search(line):
            print(f"{where}:{number}:{line.strip()}")
