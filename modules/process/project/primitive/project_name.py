#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/process/project/primitive/project_name.py — a project given by its name, declared once.

A name is one of the two ways a verb is told which project it works for; the
other is a folder (`modules/process/project/primitive/project_path.py`). They are two types because a
name is never taken for a path: a value written as a path is refused with the
flag that takes a path, and is not looked up. Turning a name into a folder is
the registry's (`project_find`), which needs a name this type has checked.

The flag, its metavar, the attribute a parser gives it, what a value must be to
be a name, and the words that say both flags together are the type's and
written nowhere else
([A Fact in Code Is Written Once](../../../modules/knowledge/documentation/documentation.md#a-fact-in-code-is-written-once)).
"""
from __future__ import annotations
from typing import ClassVar
from machine.console import fail
from modules.process.project.primitive.project_path import ProjectPath

class ProjectName(str):
    """A project's name or alias as the caller gave it: one word, not written as a path."""
    FLAG: ClassVar[str] = '--project'
    METAVAR: ClassVar[str] = 'NAME'
    DEST: ClassVar[str] = 'project'

    @classmethod
    def checked(cls, value: str) -> ProjectName:
        """VALUE stripped, as a name; refused when it is empty or written as a path, with the flag that takes a path."""
        if not value or not value.strip():
            fail(f'{cls.FLAG} needs the name of a project, one `memar project list` shows')
        text = value.strip()
        if ProjectPath.written_like(text):
            fail(f"{cls.FLAG} takes a project's name, and {value} looks like a path; for a folder use {ProjectPath.FLAG} {ProjectPath.METAVAR}")
        return cls(text)

    @classmethod
    def either_words(cls) -> str:
        """The two flags together as a help or an error says them: `--project NAME or --project-path PATH`."""
        return f'{cls.FLAG} {cls.METAVAR} or {ProjectPath.FLAG} {ProjectPath.METAVAR}'
