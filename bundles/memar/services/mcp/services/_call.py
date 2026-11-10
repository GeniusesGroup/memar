#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
import io
import os
import sys
import traceback
from importlib.machinery import SourceFileLoader
from pathlib import Path
from typing import Iterable
from machine.console import CALLER_ENV, MCP_CALLER
from typing import NamedTuple
SCALARS = (bool, int, float, str, bytes, type(None))
CAPTURE_FOLDER = 'mcp'

class Output(NamedTuple):
    stdout: str
    stderr: str
    status: int

class Globals:

    def __init__(self, declared: Iterable[str]) -> None:
        self.declared = frozenset(declared)
        self.values: dict[str, dict[str, object]] = {}

    def watch_imports(self) -> None:
        loaded = SourceFileLoader.exec_module
        record = self.record

        def exec_module(loader, module):
            loaded(loader, module)
            record(module)
        SourceFileLoader.exec_module = exec_module

    def record(self, module) -> None:
        if module.__name__ not in self.declared:
            return
        self.values[module.__name__] = {key: value for key, value in vars(module).items() if not key.startswith('__') and isinstance(value, SCALARS)}

    def restore(self) -> None:
        for name, values in self.values.items():
            module = sys.modules.get(name)
            if module is None:
                continue
            space = vars(module)
            for key, value in values.items():
                if space.get(key) is not value:
                    space[key] = value

    def clear_caches(self) -> None:
        for name in self.values:
            module = sys.modules.get(name)
            for value in list(vars(module).values()) if module is not None else ():
                if callable(getattr(value, 'cache_clear', None)) and hasattr(value, 'cache_info'):
                    value.cache_clear()

def _stream(descriptor: int, errors: str) -> io.TextIOWrapper:
    """A text stream over DESCRIPTOR as the interpreter opens stdout and stderr: the locale's encoding, the platform's line ending."""
    return open(descriptor, 'w', encoding=None, errors=errors, closefd=False)

def align_windows_std_handles() -> None:
    """Point the Win32 standard handles at CRT fds 0/1/2.

    `os.dup2` updates the CRT table and does not call `SetStdHandle`. A later
    `subprocess` that inherits stdin then duplicates an invalid Win32 handle
    (`WinError 6`). Call this after every `dup2` of a standard fd on Windows.
    """
    if sys.platform != 'win32':
        return
    import ctypes
    import msvcrt
    for fd, which in ((0, -10), (1, -11), (2, -12)):
        try:
            handle = msvcrt.get_osfhandle(fd)
        except OSError:
            continue
        ctypes.windll.kernel32.SetStdHandle(which, handle)

class Runner:
    """Runs verbs through the router's `main`, one at a time, each captured whole."""

    def __init__(self, router, recorded: Globals, scratch: Path) -> None:
        self.router = router
        self.globals = recorded
        folder = scratch / CAPTURE_FOLDER
        folder.mkdir(parents=True, exist_ok=True)
        import tempfile
        self.captures = (
            tempfile.TemporaryFile(dir=folder),
            tempfile.TemporaryFile(dir=folder),
            tempfile.TemporaryFile(dir=folder),
        )

    def run(self, argv: list[str], stdin: str='') -> Output:
        self.globals.restore()
        environment, folder = (dict(os.environ), os.getcwd())
        saved = (sys.stdin, sys.stdout, sys.stderr, sys.argv)
        kept = (os.dup(0), os.dup(1), os.dup(2))
        for capture in self.captures:
            capture.seek(0)
            capture.truncate()
        self.captures[0].write(stdin.encode('utf-8'))
        self.captures[0].seek(0)
        os.dup2(self.captures[0].fileno(), 0)
        os.dup2(self.captures[1].fileno(), 1)
        os.dup2(self.captures[2].fileno(), 2)
        align_windows_std_handles()
        sys.stdin = open(0, 'r', encoding='utf-8', closefd=False)
        sys.stdout, sys.stderr = (_stream(1, 'strict'), _stream(2, 'backslashreplace'))
        sys.argv = [str(self.router.__file__), *argv]
        os.environ[CALLER_ENV] = MCP_CALLER
        try:
            status = self._main(argv)
        finally:
            for stream in (sys.stdout, sys.stderr, sys.stdin):
                try:
                    stream.flush()
                except (OSError, ValueError):
                    pass
            os.dup2(kept[0], 0)
            os.dup2(kept[1], 1)
            os.dup2(kept[2], 2)
            align_windows_std_handles()
            for descriptor in kept:
                os.close(descriptor)
            sys.stdin, sys.stdout, sys.stderr, sys.argv = saved
            if dict(os.environ) != environment:
                os.environ.clear()
                os.environ.update(environment)
            if os.getcwd() != folder:
                os.chdir(folder)
            self.globals.clear_caches()
        return Output(self._read(1), self._read(2), status)

    def _main(self, argv: list[str]) -> int:
        try:
            status = self.router.main(list(argv))
        except SystemExit as stop:
            if stop.code is None:
                status = 0
            elif isinstance(stop.code, int):
                status = stop.code
            else:
                print(stop.code, file=sys.stderr)
                status = 1
        except Exception:
            traceback.print_exc()
            status = 1
        return status or 0

    def _read(self, number: int) -> str:
        capture = self.captures[number]
        capture.seek(0)
        return capture.read().decode('utf-8', errors='replace')
