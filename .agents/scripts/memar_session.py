#!/usr/bin/env python3
"""memar_session.py — one session's identity: the id its folder and notes carry.

An id, and nothing else. It is minted here rather than beside the scratch folder
because a session is a session whichever tool asks for one: the session tool
names a folder with it, and a write under `memar content` names its intent note
with it, and two minting functions would produce two id formats that a reader
comparing them could not match.

It is a module beside `memar-session.py` rather than inside it because a hyphen
is not a legal module name and the run-only half cannot be imported. One file
here is the cost of that, and it is stated in the folder README rather than
left for a reader to find two names that differ by one character.
"""
from __future__ import annotations

import os
import time
from itertools import count

_minted = count()


def new_session_id() -> str:
    """A unique id for the calling session, for its folder and its intent notes.

    Clock plus per-process counter: the clock orders ids across runs, and the
    counter separates two mints inside one clock tick, which coarse platform
    clocks produce on back-to-back calls.
    """
    return f"{os.getpid()}-{time.time_ns():x}-{next(_minted):x}"
