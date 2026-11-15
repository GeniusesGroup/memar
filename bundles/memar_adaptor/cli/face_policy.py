#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations

import sys
from typing import Callable

NOT_HANDED_OVER = frozenset({'mcp_serve', 'mcp_worker', 'resident_serve', 'resident_status', 'resident_stop', 'memar_install', 'memar_update'})

# The few calls the small program `memar` does itself instead of sending as words, keyed by the words as typed.
# This is data about calls and holds no verb's behavior: what a verb does is declared by its own module.
RELAYS = ('mcp_serve',)
RUNS_THE_SERVER = ('resident_serve',)
WITHOUT_STARTING = ('resident_status', 'resident_stop')


def kind_of(words: list[str]) -> str:
    """What the program does with the call WORDS: 'relay', 'server', 'only-if-running', or 'send'."""
    if '--help' in words or '-h' in words:
        return 'send'
    head = words[0] if words else ''
    if head in RELAYS:
        return 'relay'
    if head in RUNS_THE_SERVER:
        return 'server'
    if head in WITHOUT_STARTING:
        return 'only-if-running'
    return 'send'


def run_ref(run: Callable) -> str | None:
    """The `module:name` the server can load this run by, or None when the run is a closure or a lambda: only the process that built it can call it, so a call that uses one is run by the face itself."""
    module = sys.modules.get(run.__module__)
    if getattr(module, run.__name__, None) is not run:
        return None
    return f'{run.__module__}:{run.__name__}'
