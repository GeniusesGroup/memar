#!/usr/bin/env python3
"""The Desktop shortcut that points at the checkout.

One of the two things a machine gets beside the checkout; the editor extensions
are the other. The shortcut is a convenience and its failure is a warning rather
than a failed install: a machine with no Desktop folder is still a machine Memar
is installed on.
"""
from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

from console import note

SHORTCUT_NAME = "Memar"


def desktop_dir() -> Path:
    """Where this platform puts the user's desktop. POSIX only: the Windows
    branch asks PowerShell for it in the same call that makes the shortcut."""
    finder = shutil.which("xdg-user-dir")
    if finder:
        found = subprocess.run(
            [finder, "DESKTOP"], capture_output=True, text=True, check=False
        ).stdout.strip()
        if found and Path(found).is_dir():
            return Path(found)
    if (Path.home() / "Desktop").is_dir():
        return Path.home() / "Desktop"
    return Path.home()


def create_shortcut(target: Path) -> str:
    if os.name == "nt":
        # The platform's own way to make a .lnk is COM, which Python cannot reach
        # without a package this script refuses to depend on — and the same call
        # resolves the Desktop folder, which is .NET's job for the same reason.
        # The paths travel as environment variables, so nothing has to survive
        # quoting. Exit 2 means this user has no Desktop folder.
        script = (
            "$desktop = [System.Environment]::GetFolderPath('Desktop'); "
            "if (-not $desktop) { exit 2 }; "
            "$link = [System.IO.Path]::Combine($desktop, 'Memar.lnk'); "
            "$shell = New-Object -ComObject WScript.Shell; "
            "$shortcut = $shell.CreateShortcut($link); "
            "$shortcut.TargetPath = $env:MEMAR_SHORTCUT_TARGET; "
            "$shortcut.WorkingDirectory = $env:MEMAR_SHORTCUT_TARGET; "
            "$shortcut.Description = 'Memar'; $shortcut.Save(); "
            "Write-Output $link"
        )
        environment = dict(
            os.environ,
            MEMAR_SHORTCUT_TARGET=str(target),
        )
        completed = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", script],
            env=environment,
            check=False,
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0:
            reason = (
                "no Desktop folder for this user"
                if completed.returncode == 2
                else (completed.stderr.strip() or "the shortcut could not be created")
            )
            note(f"warning: {reason}")
            return ""
        return completed.stdout.strip()

    link = desktop_dir() / SHORTCUT_NAME
    if link.is_symlink():
        if Path(os.readlink(str(link))) != target:
            link.unlink()
            link.symlink_to(target, target_is_directory=True)
    elif link.exists():
        note(f"warning: {link} already exists and is not a symlink; left as it is")
        return str(link)
    else:
        try:
            link.symlink_to(target, target_is_directory=True)
        except OSError as error:
            note(f"warning: this platform refused the symlink at {link} ({error})")
            return ""
        if not link.is_symlink():
            note(f"warning: this platform made a copy at {link} instead of a link")
    return str(link)
