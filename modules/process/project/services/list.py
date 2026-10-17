#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/process/project/services/list.py — `memar project list`: every registered project, one a line.

Memar's own checkout is always among them (`project_registry.ensure_memar_entry`).
"""
from __future__ import annotations

import argparse
from typing import Callable

from modules.process.project.services.registry import ensure_memar_entry, read_entries

LIST_COMMAND = "list"


def describe(verbs) -> Callable[[argparse.Namespace], None]:
    """`memar project list`."""
    verbs.add_parser(
        LIST_COMMAND,
        help="show every registered project, its names and its folder",
        description="Show every registered project, one a line: its names, the first its own, then its folder.",
    )
    return run


def run(args: argparse.Namespace) -> None:
    ensure_memar_entry()
    for entry in read_entries():
        print(f"{', '.join(entry.names)}  {entry.path}")
