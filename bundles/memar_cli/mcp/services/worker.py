#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""mcp/services/worker.py — `memar mcp worker`: the worker process of `memar mcp serve` and of the resident process, the program itself.

It is not typed by a person. The relay (`serve.py`) and the pool (`resident/services/_pool.py`) start the program with this verb,
and speak to it a JSON-RPC line at a time on its stdin and stdout; `_worker.py` holds what it does.
"""
from __future__ import annotations
import argparse
import sys
COMMAND = 'worker'

def describe(verbs):
    verbs.add_parser(COMMAND, help=argparse.SUPPRESS, description="Run a worker: read JSON-RPC from stdin and answer on stdout until stdin closes.\nThe relay of `memar mcp serve` and the resident process start it; a person does not type it.", formatter_class=argparse.RawDescriptionHelpFormatter)
    return run

def run(args: argparse.Namespace) -> int:
    from mcp.services import _worker
    _worker.main(sys.modules['__main__'])
    return 0
