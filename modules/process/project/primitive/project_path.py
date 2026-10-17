#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/process/project/primitive/project_path.py — a project given by its folder, declared once.

A path is one of the two ways a verb is told which project it works for; the
other is a name (`modules/process/project/primitive/project_name.py`). They are two types because a name
is never taken for a path and a path is never looked up as a name: a caller who
said it is a path (`FLAG`) gets a folder or a refusal, and no registry is asked.

The flag, its metavar, the attribute a parser gives it, the test of what a text
written as a path looks like, and what a value must be to be a project's folder
are the type's and written nowhere else
([A Fact in Code Is Written Once](../../../modules/knowledge/documentation/documentation.md#a-fact-in-code-is-written-once)).
"""
from __future__ import annotations

from pathlib import Path
from typing import ClassVar

from machine.console import fail


class ProjectPath(str):
    """A project's folder as the caller gave it, resolved: absolute, and a folder that is there."""

    FLAG: ClassVar[str] = "--project-path"
    METAVAR: ClassVar[str] = "PATH"
    # The attribute a parser gives the flag.
    DEST: ClassVar[str] = "project_path"

    @staticmethod
    def written_like(text: str) -> bool:
        """Whether TEXT is written as a path: absolute, with a drive or a separator, or starting with . or ~."""
        return bool(text) and (
            Path(text).is_absolute()
            or bool(Path(text).drive)
            or "/" in text
            or "\\" in text
            or text[0] in ".~"
        )

    @classmethod
    def checked(cls, value: str | Path, *, hint: str = "") -> ProjectPath:
        """The folder VALUE is, resolved; refused when it is empty or not a folder, HINT ending the message of the latter."""
        text = str(value).strip()
        if not text:
            fail(f"{cls.FLAG} needs the folder of a project")
        folder = Path(text).expanduser().resolve()
        if not folder.is_dir():
            fail(f"{value} is not a folder{hint}")
        return cls(folder)

    @property
    def folder(self) -> Path:
        """The folder as a path."""
        return Path(self)
