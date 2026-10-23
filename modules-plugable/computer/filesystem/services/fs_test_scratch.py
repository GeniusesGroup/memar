#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/computer/filesystem/services/fs_test_scratch.py — where a test suite in this folder writes: the one owner of MEMAR_TEST_SCRATCH.

Every suite here, on whichever shelf it sits, makes its throwaway folders under
the folder `suite_scratch()` returns, so the name of the variable and what it
resolves to are decided in this file and nowhere else. A suite that spelled the
name itself, or fell back on its own, would be one more place to disagree about
where a run leaves its files.

MEMAR_TEST_SCRATCH, when set, names that folder: an agent with a task points
it into its own task folder, so what its test runs leave lands with the rest
of its scratch. The folder has to exist already; a value naming nothing is
refused rather than created, because a mistyped value would otherwise leave a
folder where nobody looks.

Unset, the folder is `temp/test-scratch/` in the checkout this file sits in, and
never the OS temporary directory: a task's scratch is not kept there, and
neither is a suite's. `temp/` is the checkout's one scratch root, named by
`modules-plugable/computer/filesystem/services/fs_memar.py` and ignored by the checkout's `.gitignore`, so a run
leaves nothing git sees and whatever a failed run leaves is found where a person
looks for scratch. The folder is not named the way a task is, so the task
sweep never takes it.

What a suite makes there it removes whole with `remove_tree`, never by
ignoring the errors: on Windows git writes its objects read-only and a process
it leaves behind may hold a file for a moment, so a removal that gives up
silently leaves half a repository where the next run looks. Read-only bits are
cleared, a held file is waited for briefly, and what still cannot go fails the
test that made it, naming it.

It also answers whether this process is a test run, because a test run is what
reaches the machine by accident: the daily update must never start from one.
A suite has `unittest` loaded, and importing this file from a suite writes
MEMAR_TEST_RUN into its environment, so a launcher or tool the suite starts as
a child is a test run too. Imported by anything else, it marks nothing.
"""
from __future__ import annotations
from importlib import import_module
_m_fs_memar = import_module('modules-plugable.computer.filesystem.services.fs_memar')
TEMP_DIRNAME = _m_fs_memar.TEMP_DIRNAME
checkout_root = _m_fs_memar.checkout_root
import os
import shutil
import stat
import sys
import time
from pathlib import Path
from machine.console import fail
VARIABLE = 'MEMAR_TEST_SCRATCH'
FALLBACK_NAME = 'test-scratch'
TEST_RUN_VARIABLE = 'MEMAR_TEST_RUN'
TEST_RUNNERS = ('unittest', 'pytest')
REMOVE_ATTEMPTS = 5
REMOVE_PAUSE_SECONDS = 0.2

def in_test_run() -> bool:
    """Whether this process is a suite, or was started by one."""
    return bool(os.environ.get(TEST_RUN_VARIABLE)) or any((runner in sys.modules for runner in TEST_RUNNERS))
if any((runner in sys.modules for runner in TEST_RUNNERS)):
    os.environ[TEST_RUN_VARIABLE] = '1'

def suite_scratch() -> Path:
    """The folder a suite makes its throwaway folders under: the variable's, else temp/test-scratch/."""
    named = os.environ.get(VARIABLE)
    if named:
        folder = Path(named)
        if not folder.is_dir():
            fail(f'{VARIABLE} names {folder}, which is not a folder; create it or unset {VARIABLE}')
        return folder
    folder = checkout_root() / TEMP_DIRNAME / FALLBACK_NAME
    folder.mkdir(parents=True, exist_ok=True)
    return folder

def _writable_then_again(function, path, error) -> None:
    if isinstance(error[1] if isinstance(error, tuple) else error, FileNotFoundError):
        return
    os.chmod(path, stat.S_IWRITE | stat.S_IREAD | (stat.S_IEXEC if os.path.isdir(path) else 0))
    function(path)

def remove_tree(folder: Path) -> None:
    """Remove FOLDER, which a suite made, whole; raise naming it when it cannot be."""
    for attempt in range(1, REMOVE_ATTEMPTS + 1):
        try:
            if sys.version_info >= (3, 12):
                shutil.rmtree(folder, onexc=_writable_then_again)
            else:
                shutil.rmtree(folder, onerror=_writable_then_again)
            return
        except FileNotFoundError:
            return
        except OSError:
            if attempt == REMOVE_ATTEMPTS:
                raise
            time.sleep(REMOVE_PAUSE_SECONDS * attempt)
