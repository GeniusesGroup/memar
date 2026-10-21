#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""resident/services/status.py — `memar resident status`: whether the resident process runs, and how many calls it has answered."""
from __future__ import annotations
import argparse
import sys
from pathlib import Path
from machine.resident import ask, folder, state_of
COMMAND = 'status'
TOP = Path(__file__).resolve().parents[5]

def describe(verbs):
    verbs.add_parser(COMMAND, help='say whether the resident process runs', description="Print the resident process's id, port and the number of calls it has answered; exit 1 when none runs.")
    return run

def run(args: argparse.Namespace) -> int:
    answer = ask(TOP, {'ping': True})
    if answer is None:
        print('memar: no resident process is running.', file=sys.stderr)
        return 1
    state = state_of(TOP) or {}
    print(f"running: pid {answer.get('pid')}, port {state.get('port')}, {answer.get('calls')} calls answered, {answer.get('workers')} workers, state in {folder(TOP)}")
    return 0
