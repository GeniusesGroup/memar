#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/knowledge/documentation/services/content_obligations.py — `memar content obligations`: what a change has not yet been carried to.

The work-list `check` prints apart, asked for on its own: every `Propagates to`
entry still `Pending`, one `path:line: entry` hit per line, read by
`content_propagation`. With no files it reads every ledger of the checkout,
because a propagation owed under `modules/` is as open as one owed under
`docs/`.
"""
from __future__ import annotations
from importlib import import_module

import argparse
from pathlib import Path

from modules.knowledge.text.services.corpus import ledger_files
_m_propagation = import_module('modules-plugable.knowledge.documentation.services.propagation')
undischarged_propagations = _m_propagation.undischarged_propagations
from modules.knowledge.content.services.reference import content_root, resolve_ref


def describe(verbs):
    parser = verbs.add_parser(
        "obligations",
        help="list undischarged Propagates-to entries as path:line hits",
        description="List undischarged `Propagates to: Pending` entries — the "
                    "work-list `check` prints apart — as one `path:line: "
                    "entry` hit per line. No arguments means every ledger of "
                    "the checkout, not only the ones under `docs/`.",
        formatter_class=argparse.HelpFormatter,
    )
    parser.add_argument(
        "files", nargs="*", help="files to read (default: every ledger)"
    )
    return run


def run(args: argparse.Namespace) -> None:
    cmd_obligations(args, content_root())


def cmd_obligations(args: argparse.Namespace, root: Path) -> None:
    if args.files:
        paths = [resolve_ref(ref, root, None) for ref in args.files]
    else:
        # `content_files` excludes ledgers from the search corpus by design, so
        # the ledgers are collected separately.
        paths = ledger_files(root)
    found = undischarged_propagations(paths)
    if not found:
        print("(no undischarged obligations)")
        return
    for path, line, report in found:
        try:
            shown = path.relative_to(root)
        except ValueError:
            shown = path
        _, _, entry = report.partition(": ")
        print(f"{shown}:{line}: {entry}")
