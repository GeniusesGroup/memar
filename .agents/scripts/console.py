#!/usr/bin/env python3
"""How a script in this folder reports and stops.

One place, so that every step line looks like every other step line, and so
that a failure is reported as a message rather than as a traceback a person
has to read bottom-up. Nothing here decides anything.
"""
from __future__ import annotations

import sys
from typing import NoReturn


def use_utf8_stdio() -> None:
    """Print non-ASCII without crashing a console that is not UTF-8."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8", errors="replace")


def step(message: str) -> None:
    print(f"==> {message}")


def note(message: str) -> None:
    print(f"    {message}")


def fail(message: str) -> NoReturn:
    sys.exit(f"error: {message}")
