#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/session_id.py — one session's identity: the id its folder and notes carry.

An id, and nothing else. It is minted here rather than beside the scratch folder
because a session is a session whichever tool asks for one: the session services
name a folder with it, and a write under `memar content` names its intent note
with it, and two minting functions would produce two id formats that a reader
comparing them could not match.

The form is the UTC date, a dash, the time, and the process id, e.g.
`20261013-T190845Z-23368`: the dash between date and time
is for the reader. Ids were once minted with a per-process counter after the
process id; it told apart two mints of one process in one second, and every
folder ever made carried `-0`, since a command mints at most one session id.
The counter is gone, and the case it covered is kept unique another way: a
process that would mint the same second twice waits for the next second.
Nothing here reads a form minted before; a folder still named in one is a
session by its plan (`session_folder`), and renaming such folders is a
one-time migration, which lives in the session that does it, not here.
"""
from __future__ import annotations

import os
import re
import time
from typing import ClassVar


class SessionId(str):
    """One session's id, the name of its folder and the key of its notes.

    The form is the UTC date, a dash, the time, a `Z`, a dash and the process
    id; `new` mints one and `is_form` says whether a name has it. The form, the
    clock's format and the rule that one process never mints the same second
    twice are written here and nowhere else.
    """

    FORM: ClassVar[re.Pattern[str]] = re.compile(r"^\d{8}-T\d{6}Z-\d+$")
    STAMP_FORMAT: ClassVar[str] = "%Y%m%d-T%H%M%SZ"
    # The second this process last minted in, so a second mint in it waits rather than repeats.
    _last: ClassVar[str | None] = None

    @classmethod
    def new(cls) -> SessionId:
        """A unique id for the calling session, for its folder and its intent notes.

        The UTC second comes first, in ISO 8601 basic form with a dash before the
        time, so a plain name sort in any file listing is creation order and a
        person reads the date off the name. The process id separates sessions
        opened in the same second; a second mint by one process in the second it
        last minted in waits for the next second.
        """
        stamp = time.strftime(cls.STAMP_FORMAT, time.gmtime())
        while stamp == cls._last:
            time.sleep(1.0 - time.time() % 1.0)
            stamp = time.strftime(cls.STAMP_FORMAT, time.gmtime())
        cls._last = stamp
        return cls(f"{stamp}-{os.getpid()}")

    @classmethod
    def is_form(cls, name: str) -> bool:
        """Whether NAME has the form `new` mints."""
        return bool(cls.FORM.match(name))
