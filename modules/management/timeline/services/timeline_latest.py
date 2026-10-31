#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations


def read_latest(store, timeline: str, kind: str) -> tuple:
    return store.read_latest_placement(timeline, kind)
