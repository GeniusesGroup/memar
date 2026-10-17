#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/process/session/services/day.py — the day a review is asked for, and the day a session belongs to.

The owner reviews sessions by the day they were worked, because what they ask
for is "what happened today". A session belongs to the local day of the latest
change anywhere in its folder (`session_folder.last_change`), not the day it
was opened: a task opened yesterday and finished today is part of today's
review, and one opened today and left alone is not part of tomorrow's. The day
is local because the owner's day is, not UTC's. A day is named `today`,
`yesterday`, or `YYYY-MM-DD`; anything else is refused with what is accepted,
since a guessed day would review the wrong sessions.
"""
from __future__ import annotations

from datetime import date, datetime, timedelta
from pathlib import Path

from machine.console import fail
from modules.process.session.services.folder import last_change

DAY_NAMES = "today, yesterday, or a date as YYYY-MM-DD"


def parse_day(text: str, today: date | None = None) -> date:
    """The day TEXT names; refused when it is not `today`, `yesterday`, or an ISO date."""
    today = today or date.today()
    word = text.strip().lower()
    if word == "today":
        return today
    if word == "yesterday":
        return today - timedelta(days=1)
    try:
        return datetime.strptime(word, "%Y-%m-%d").date()
    except ValueError:
        fail(f"--day is {DAY_NAMES}; {text!r} is none of these")


def day_of(folder: Path) -> date | None:
    """The local day of the latest change inside FOLDER, or None when that cannot be read."""
    try:
        return date.fromtimestamp(last_change(folder))
    except OSError:
        return None
