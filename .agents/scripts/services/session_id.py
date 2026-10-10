#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/session_id.py — one session's identity: the id its folder and notes carry.

An id, and nothing else. It is minted here rather than beside the scratch folder
because a session is a session whichever tool asks for one: the session services
name a folder with it, and a write under `memar content` names its intent note
with it, and two minting functions would produce two id formats that a reader
comparing them could not match.
"""
from __future__ import annotations

import os
import re
import time
from itertools import count

_minted = count()
# The form new_session_id mints, read back by whatever has to tell a session's
# folder from another folder beside it.
_MINTED_FORM = re.compile(r"^\d{8}T\d{6}Z-\d+-[0-9a-f]+$")
# The form minted before the clock came first: the process id, time.time_ns() in
# hex, and the counter in hex. Folders named so still exist and must still be
# reaped; once none is younger than the idle limit it can go. The clock is held
# to its sixteen digits, the width every time_ns() since 2006 has, so a person's
# folder such as 2024-01-01 is not taken for a session.
_EARLIER_FORM = re.compile(r"^\d+-[0-9a-f]{16}-[0-9a-f]+$")


def new_session_id() -> str:
    """A unique id for the calling session, for its folder and its intent notes.

    The UTC second comes first, in ISO 8601 basic form, so a plain name sort in
    any file listing is creation order and a person reads the date off the name.
    The process id separates sessions opened in the same second, and the
    per-process counter separates two mints by one process in that second.
    """
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    return f"{stamp}-{os.getpid()}-{next(_minted):x}"


def is_session_id(name: str) -> bool:
    """Whether NAME has a form new_session_id mints or has minted."""
    return bool(_MINTED_FORM.match(name) or _EARLIER_FORM.match(name))


def is_dated_session_id(name: str) -> bool:
    """Whether NAME has the form minted now, whose name sort is creation order.

    An id in the earlier form carries no clock, and was minted before any id
    that does.
    """
    return bool(_MINTED_FORM.match(name))
