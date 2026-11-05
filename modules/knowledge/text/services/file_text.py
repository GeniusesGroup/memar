#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import os
import time
from pathlib import Path

def writer_id() -> str:
    return f'{os.getpid()}-{time.time_ns()}'

def plain_path(ref: str) -> Path:
    return Path(ref).expanduser().resolve()
