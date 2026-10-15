#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/project_remove.py — `memar project remove WORD`: a project forgotten, its folder untouched.

WORD is an exact name or alias in any case, or the folder: a removal is never
decided by similarity, because forgetting the wrong project is not undone by
asking again.
"""
from __future__ import annotations

import argparse
from typing import Callable

from machine.console import note
from services.project_registry import remove_project

REMOVE_COMMAND = "remove"


def describe(verbs) -> Callable[[argparse.Namespace], None]:
    """`memar project remove`."""
    remover = verbs.add_parser(
        REMOVE_COMMAND,
        help="unregister a project by an exact name, alias, or folder",
        description=(
            "Unregister the project WORD names: an exact name or alias in any case, or\n"
            "its folder. The folder itself is not touched, and similarity is not used."
        ),
    )
    remover.add_argument("word", metavar="WORD", help="a name, an alias, or the folder")
    return run


def run(args: argparse.Namespace) -> None:
    entry = remove_project(args.word)
    note(f"removed {entry.names[0]}  {entry.path}")
