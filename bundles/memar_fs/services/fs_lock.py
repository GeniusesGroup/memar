#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import os
import sys
import time
from datetime import date
from pathlib import Path
from machine.console import fail

def take_advisory_lock(path: Path, *, wait_seconds: float, stale_seconds: float, poll_seconds: float, waiting_message: str, timeout_message: str) -> None:
    deadline = time.monotonic() + wait_seconds
    announced = False
    while not try_lock(path, stale_seconds):
        if not announced:
            sys.stderr.write(waiting_message)
            announced = True
        if time.monotonic() > deadline:
            fail(timeout_message)
        time.sleep(poll_seconds)
    return None

def try_lock(path: Path, stale_seconds: float) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    while True:
        try:
            handle = os.open(str(path), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 384)
        except FileExistsError:
            try:
                age = time.time() - path.stat().st_mtime
            except OSError:
                age = 0.0
            if age <= stale_seconds:
                return False
            try:
                path.unlink()
            except OSError:
                return False
            continue
        os.close(handle)
        return True

def claim_today(marker: Path) -> bool:
    today = date.today().isoformat()
    try:
        if marker.read_text(encoding='utf-8').strip() == today:
            return False
    except OSError:
        pass
    try:
        marker.parent.mkdir(parents=True, exist_ok=True)
        marker.write_text(today + '\n', encoding='utf-8', newline='\n')
    except OSError as error:
        print(f'warning: the daily marker {marker} could not be written ({error})', file=sys.stderr)
    return True

def release_lock(path: Path) -> None:
    try:
        path.unlink()
    except OSError:
        pass
