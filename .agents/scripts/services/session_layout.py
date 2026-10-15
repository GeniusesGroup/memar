#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/session_layout.py — what stands at a session folder's top, and which role folder takes the rest.

A session folder's top holds its plan and its report, and the claim Memar
writes there while an agent holds the task; everything else the task makes is
filed by kind in the module role folders `session_new` makes in it
(`module_folders`), so another session reads the top as the task and finds its
material by kind. That answer is given here once: the help
`memar session --help` prints is built from it.

A kind is told by the file's suffix, and only the kinds named in KINDS are
told: a note is Markdown and goes in docs/, a script goes in services/. A file
of any other suffix, and a folder, have no kind here, so nothing guesses where
they belong; whoever made them files them.
"""
from __future__ import annotations

from typing import NamedTuple

from services.module_folders import ROLE_FOLDERS, listed
from services.session_claim import CLAIM_NAME, CLAIM_TAKEOVER_NAME
from services.session_plan import PLAN_NAME
from services.session_report import REPORT_NAME
from services.session_temp import TEMP_FOLDER

TOP_NAMES = (PLAN_NAME, REPORT_NAME, CLAIM_NAME, CLAIM_TAKEOVER_NAME)
"""The files a session folder's top holds besides its role folders: the plan, the report, and Memar's claim."""


class Kind(NamedTuple):
    """A kind of file a session makes: its name, the role folder it goes in, and the suffixes that tell it."""

    name: str
    folder: str
    suffixes: tuple[str, ...]

    def takes(self, file_name: str) -> bool:
        return file_name.lower().endswith(self.suffixes)


KINDS = (
    Kind("note", "docs", (".md",)),
    Kind("script", "services", (".py", ".mjs", ".js", ".ps1", ".sh")),
)


def belongs_at_top(name: str) -> bool:
    """Whether an entry named NAME may stand at a session folder's top: a top file or a role folder."""
    return name in TOP_NAMES or name in ROLE_FOLDERS or name == TEMP_FOLDER


def kind_of(file_name: str) -> Kind | None:
    """The kind a file named FILE_NAME is, by its suffix; None when it is of no kind named here."""
    return next((kind for kind in KINDS if kind.takes(file_name)), None)


def kinds_listing() -> str:
    """KINDS as one line for a help text, e.g. `a note (.md) in docs/`."""
    return ", ".join(f"a {kind.name} ({', '.join(kind.suffixes)}) in {listed((kind.folder,))}" for kind in KINDS)
