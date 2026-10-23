#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/knowledge/content/services/hour_id.py — `memar content hour-id`: the ID a new Explanation document takes.

The UTC hours since the epoch. Minting a document ID asks the clock, not the
checkout, so it resolves no root: a task on a machine that has not installed
Memar can still mint one.
"""
from __future__ import annotations
import argparse
import time

def describe(verbs):
    verbs.add_parser('hour-id', help='print UTC hour-count since epoch (Explanation document ID)', formatter_class=argparse.HelpFormatter)
    return run

def run(args: argparse.Namespace) -> None:
    print(int(time.time() // 3600))
