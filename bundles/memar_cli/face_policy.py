#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations

from typing import Callable

NOT_HANDED_OVER = frozenset({'mcp', 'resident', 'install', 'update'})


def run_ref(run: Callable) -> str:
    return f'{run.__module__}:{run.__name__}'
