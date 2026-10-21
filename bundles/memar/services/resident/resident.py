#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""resident/resident.py — `memar resident`: the one process that answers `memar` for the calls that find it.

The command's side is `machine/resident.py` (it asks, starts and falls back); the verbs here are the process
itself and what a person does to it. Its sub-verbs are in `services/`.
"""
from __future__ import annotations
import argparse
COMMAND = 'resident'

def describe(verbs):
    verbs.add_parser(COMMAND, help='the resident process that answers `memar` calls without starting Memar again', description='The resident process: Memar loaded once, answering the `memar` command from a local socket.\nA call hands itself over to it, starting it if none runs and doing that one call in\nplace; MEMAR_SERVER=0 keeps a call in its own process. It ends after\na while without a call, and the next call starts it again.', formatter_class=argparse.RawDescriptionHelpFormatter)
    return None
