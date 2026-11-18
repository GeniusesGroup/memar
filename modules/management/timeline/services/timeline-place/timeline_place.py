#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
import time


def place_content(store, timeline: str, content: str, kind: str, placer: str, after: int, clock=time.time, provenance=None) -> int:
    if provenance is None:
        return store.add_placement(timeline, content, kind, placer, int(clock()), after)
    return store.add_placement(timeline, content, kind, placer, int(clock()), after, provenance=provenance)
