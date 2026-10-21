#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""resident/services/stop.py — `memar resident stop`: ask the resident process to end."""
from __future__ import annotations
import argparse
import sys
from pathlib import Path
from machine.resident import ask
COMMAND = 'stop'
TOP = Path(__file__).resolve().parents[5]

def describe(verbs):
    verbs.add_parser(COMMAND, help='ask the resident process to end', description='Ask the resident process of this checkout to end; the next call started with MEMAR_SERVER=1 starts it again.')
    return run

def run(args: argparse.Namespace) -> int:
    if ask(TOP, {'stop': True}) is None:
        print('memar: no resident process is running.', file=sys.stderr)
        return 1
    print('memar: the resident process was asked to end.')
    return 0
