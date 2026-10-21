#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/computer/filesystem/services/fs_target.py — the folder a run would use, and the one place that refuses a temporary one.

A refusal is only useful if it names the directory it was decided against, so
the directory is asked once here and the same answer decides and reports. There
is no second opinion to drift from the first.

`INSTALL_DIRNAME` is what a default install is called, and it lives here because
this is the module that answers "which folder would a run use" — the install
folder's name is that answer, not a string another module should reach for when
it needs a word to put in a file name.
"""
from __future__ import annotations
import os
import sys
from pathlib import Path
from machine.console import fail
INSTALL_DIRNAME = 'Memar'

def full_path(value: str) -> Path:
    return Path(os.path.expandvars(value)).expanduser().absolute()

def default_target() -> Path:
    """Memar in this user's home directory."""
    return Path.home() / INSTALL_DIRNAME

def temporary_directory() -> Path:
    """The directory this platform calls temporary, asked once per refusal."""
    return Path(os.environ.get('TEMP') or os.environ.get('TMPDIR') or '/tmp')

def is_temporary(path: Path, directory: Path) -> bool:
    """True when PATH is under DIRECTORY, which the caller has already asked for."""
    try:
        path.resolve().relative_to(directory.resolve())
    except (ValueError, OSError):
        return False
    return True

def refuse_temporary(path: Path, consequence: str) -> None:
    """Refuse a folder under the temporary directory, naming that directory.

    The consequence of putting Memar there is the same for every caller; what
    the caller was about to do with the folder is not, so the caller supplies
    that sentence. The directory in the message is the one the decision was made
    against, because it is read once, here, for both.
    """
    directory = temporary_directory()
    if not is_temporary(path, directory):
        return
    fail(f'{path} is under the temporary directory ({directory}). {consequence}')
