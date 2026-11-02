#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import argparse
from typing import Callable
from ..errors.errors import Error

def guarded(call: Callable[[argparse.Namespace], None]) -> Callable[[argparse.Namespace], None]:
    def run(arguments: argparse.Namespace) -> None:
        try:
            call(arguments)
        except Error as failure:
            raise SystemExit(f'error: {failure}') from None
    return run
