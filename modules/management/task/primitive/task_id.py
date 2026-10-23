#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/management/task/primitive/task_id.py — one task's identity: the id its folder and notes carry.

An id, and nothing else. It is minted here rather than beside the scratch folder
because a task is a task whichever tool asks for one: the task services
name a folder with it, and a write under `memar content` names its intent note
with it, and two minting functions would produce two id formats that a reader
comparing them could not match.

The flag that carries an id (`FLAG`), its metavar, the attribute a parser gives it
and the way a verb declares it (`add_flag`, `add_positional`) are the type's too:
no verb writes `--task-id` or its help by hand
([A Fact in Code Is Written Once](../../../knowledge/documentation/documentation.md#a-fact-in-code-is-written-once)).

The form is the UTC date, a dash, the time, and the process id, e.g.
`20261013-T190845Z-23368`: the dash between date and time
is for the reader. Ids were once minted with a per-process counter after the
process id; it told apart two mints of one process in one second, and every
folder ever made carried `-0`, since a command mints at most one task id.
The counter is gone, and the case it covered is kept unique another way: a
process that would mint the same second twice waits for the next second.
Nothing here reads a form minted before; a folder still named in one is a
task by its plan (`task_folder`), and renaming such folders is a
one-time migration, which lives in the task that does it, not here.
"""
from __future__ import annotations
import argparse
import os
import re
import time
from typing import ClassVar

class TaskId(str):
    """One task's id, the name of its folder and the key of its notes.

    The form is the UTC date, a dash, the time, a `Z`, a dash and the process
    id; `new` mints one and `is_form` says whether a name has it. The form, the
    clock's format and the rule that one process never mints the same second
    twice are written here and nowhere else.
    """
    FORM: ClassVar[re.Pattern[str]] = re.compile('^\\d{8}-T\\d{6}Z-\\d+$')
    STAMP_FORMAT: ClassVar[str] = '%Y%m%d-T%H%M%SZ'
    FLAG: ClassVar[str] = '--task-id'
    METAVAR: ClassVar[str] = 'ID'
    DEST: ClassVar[str] = 'task_id'
    _last: ClassVar[str | None] = None

    @classmethod
    def new(cls) -> TaskId:
        """A unique id for the calling task, for its folder and its intent notes.

        The UTC second comes first, in ISO 8601 basic form with a dash before the
        time, so a plain name sort in any file listing is creation order and a
        person reads the date off the name. The process id separates tasks
        opened in the same second; a second mint by one process in the second it
        last minted in waits for the next second.
        """
        stamp = time.strftime(cls.STAMP_FORMAT, time.gmtime())
        while stamp == cls._last:
            time.sleep(1.0 - time.time() % 1.0)
            stamp = time.strftime(cls.STAMP_FORMAT, time.gmtime())
        cls._last = stamp
        return cls(f'{stamp}-{os.getpid()}')

    @classmethod
    def is_form(cls, name: str) -> bool:
        """Whether NAME has the form `new` mints."""
        return bool(cls.FORM.match(name))

    @classmethod
    def add_flag(cls, parser: argparse.ArgumentParser, what: str, *, required: bool=False) -> None:
        """Give PARSER the flag that names a task; WHAT says, in the help, which task the verb means."""
        parser.add_argument(cls.FLAG, dest=cls.DEST, metavar=cls.METAVAR, required=required, default=None, help=what)

    @classmethod
    def add_positional(cls, parser: argparse.ArgumentParser, what: str) -> None:
        """Give PARSER the positional that names a task; WHAT says, in the help, which task the verb means."""
        parser.add_argument(cls.DEST, metavar=cls.METAVAR, help=what)
