#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/process/project/services/add.py — `memar project add NAME PATH`: a folder given a name.

The registry's rules (unique names without case, a real folder, merging into a
folder already registered) are `project_registry`'s; this file declares the
verb and says what was written. Aliases are repeatable and may be in any
language, because the owner and the agents who ask do not share one.
"""
from __future__ import annotations

import argparse
from typing import Callable

from machine.console import note
from modules.process.project.services.registry import add_project, ensure_memar_entry

ADD_COMMAND = "add"


def describe(verbs) -> Callable[[argparse.Namespace], None]:
    """`memar project add`."""
    adder = verbs.add_parser(
        ADD_COMMAND,
        help="register a folder under a name, and aliases in any language",
        description=(
            "Register the folder PATH as the project NAME. Repeat --alias for each\n"
            "other name it goes by, in any language. A name or alias must not be\n"
            "another project's, whatever its case. Adding a folder that is already\n"
            "registered adds the names to its entry."
        ),
    )
    adder.add_argument("name", metavar="NAME", help="the project's own name")
    adder.add_argument("path", metavar="PATH", help="the project's folder")
    adder.add_argument("--alias", action="append", default=[], metavar="A", help="another name for it; repeatable")
    return run


def run(args: argparse.Namespace) -> None:
    ensure_memar_entry()
    entry = add_project(args.name, args.path, args.alias)
    note(f"{entry.names[0]}  {entry.path}  names: {', '.join(entry.names)}")
