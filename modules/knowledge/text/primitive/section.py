#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations

class Section:
    heading: str = ''
    purpose: str = ''
    use: str = ''
    distinct_from: str = ''
    reason: str = ''
    order: int = 0
    labels: tuple[str, ...] = ()
