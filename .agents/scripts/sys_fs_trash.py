#!/usr/bin/env python3
"""Recoverable deletion: move a path to whatever this platform calls its trash.

Never a permanent delete. Agents that "deep delete" then need the file again
burn tokens reconstructing it; the trash keeps recovery cheap.

Each platform's trash is a different mechanism under one act, so the three
implementations live here and `fs.py` keeps the `trash` command that calls them.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import time
from pathlib import Path


def _trash_windows(path: Path) -> None:
    # SHFileOperationW with FOF_ALLOWUNDO sends to Recycle Bin.
    import ctypes
    from ctypes import wintypes

    FO_DELETE = 3
    FOF_ALLOWUNDO = 0x40
    FOF_NOCONFIRMATION = 0x10
    FOF_NOERRORUI = 0x400
    FOF_SILENT = 0x04

    class SHFILEOPSTRUCTW(ctypes.Structure):
        _fields_ = [
            ("hwnd", wintypes.HWND),
            ("wFunc", ctypes.c_uint),
            ("pFrom", wintypes.LPCWSTR),
            ("pTo", wintypes.LPCWSTR),
            ("fFlags", ctypes.c_ushort),
            ("fAnyOperationsAborted", wintypes.BOOL),
            ("hNameMappings", wintypes.LPVOID),
            ("lpszProgressTitle", wintypes.LPCWSTR),
        ]

    # Double-null-terminated path list required by SHFileOperation.
    # Do not resolve symlinks/junctions: the caller may be deleting a link
    # at the canonical temp path, not the checkout it points at.
    from_path = os.path.abspath(str(path)) + "\0\0"
    op = SHFILEOPSTRUCTW()
    op.hwnd = None
    op.wFunc = FO_DELETE
    op.pFrom = from_path
    op.pTo = None
    op.fFlags = FOF_ALLOWUNDO | FOF_NOCONFIRMATION | FOF_NOERRORUI | FOF_SILENT
    op.fAnyOperationsAborted = False
    op.hNameMappings = None
    op.lpszProgressTitle = None
    result = ctypes.windll.shell32.SHFileOperationW(ctypes.byref(op))
    if result != 0 or op.fAnyOperationsAborted:
        sys.exit(f"error: Recycle Bin move failed (code {result}): {path}")


def _trash_darwin(path: Path) -> None:
    posix = os.path.abspath(str(path)).replace("\\", "/")
    script = f'tell application "Finder" to delete POSIX file "{posix}"'
    completed = subprocess.run(
        ["osascript", "-e", script],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        sys.exit(
            f"error: Trash move failed: {path}\n{completed.stderr.strip()}"
        )


def _trash_xdg(path: Path) -> None:
    # Prefer desktop tools that register in Trash correctly.
    for cmd in (
        ["gio", "trash", str(path)],
        ["trash-put", str(path)],
    ):
        if shutil.which(cmd[0]):
            completed = subprocess.run(cmd, check=False)
            if completed.returncode == 0:
                return
            sys.exit(f"error: {' '.join(cmd)} failed for {path}")

    # Minimal FreeDesktop Trash fallback.
    home = Path.home()
    trash = home / ".local" / "share" / "Trash"
    files_dir = trash / "files"
    info_dir = trash / "info"
    files_dir.mkdir(parents=True, exist_ok=True)
    info_dir.mkdir(parents=True, exist_ok=True)
    original = os.path.abspath(str(path))
    dest_name = Path(original).name
    dest = files_dir / dest_name
    if dest.exists() or dest.is_symlink():
        dest = files_dir / f"{Path(original).stem}-{int(time.time())}{Path(original).suffix}"
    shutil.move(original, str(dest))
    info = info_dir / (dest.name + ".trashinfo")
    deletion_date = time.strftime("%Y-%m-%dT%H:%M:%S")
    info.write_text(
        "[Trash Info]\n"
        f"Path={original}\n"
        f"DeletionDate={deletion_date}\n",
        encoding="utf-8",
    )


def soft_delete(path: Path) -> None:
    path = Path(os.path.abspath(str(path)))
    if not path.is_symlink() and not path.exists():
        sys.exit(f"error: path does not exist: {path}")
    if os.name == "nt":
        _trash_windows(path)
    elif sys.platform == "darwin":
        _trash_darwin(path)
    else:
        _trash_xdg(path)
    print(f"trashed (recoverable): {path}", file=sys.stderr)
