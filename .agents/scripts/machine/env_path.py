# For license and copyright information please see the LEGAL file in the code repository

"""The user's PATH, read from the record and written to deliberately.

Split out of the installer because the concern is not Memar's: what a
machine's PATH says, and how a program asks to be added to it, is the same
question for anything installed on that machine, and the day a second thing
wants to be on it is the day the answer must not be written again.
`services/install_machine.py` is the one place that decides *about Memar*;
this is the one place that decides *about the machine's environment*, and the
installer asks it the same way it asks `machine/fs_memar_repository.py`
whether a folder qualifies.

Two facts about PATH drive everything here. It is **per-process**: a shell
opened before a change does not see it, which is why the installer says so
rather than letting a person discover it. And it is **written down separately
from the copy a process inherited**, so a re-run that reads only its own copy
would add the same entry again on every run — the check below reads both, and
the written one is what decides.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

WINDOWS_ENVIRONMENT_KEY = "Environment"


def persisted_user_path() -> str:
    """The user's PATH as it is written down, not as this process inherited it.

    The written one is what makes a second installer run a no-op. A shell that
    opened before the install holds a copy without the entry and would otherwise
    report the directory missing every time.
    """
    if sys.platform == "win32":
        try:
            import winreg

            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                WINDOWS_ENVIRONMENT_KEY,
                0,
                winreg.KEY_QUERY_VALUE,
            ) as key:
                value, _ = winreg.QueryValueEx(key, "PATH")
                return str(value)
        except OSError:
            return ""
    for name in (".profile", ".bashrc", ".zshrc"):
        try:
            text = (Path.home() / name).read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for line in text.splitlines():
            if line.startswith("export PATH="):
                return line[len("export PATH=") :].strip().strip('"').strip("'")
    return ""


def holds(directory: Path) -> bool:
    """Whether a directory is already reachable by a bare name.

    Both sources are consulted and either one answers, because a directory can be
    in the written PATH and absent from this process's copy, or the reverse.
    Windows compares case-insensitively, where two spellings of one directory are
    one directory and a duplicate entry is noise a person notices and asks about.
    """
    target = directory.resolve()
    for source in (persisted_user_path(), os.environ.get("PATH", "")):
        for part in source.split(os.pathsep):
            cleaned = part.strip().strip('"')
            if not cleaned:
                continue
            try:
                if Path(cleaned).resolve() == target:
                    return True
            except OSError:
                continue
    return False


def _broadcast_environment_change() -> None:
    """Tell already-running programs that the user environment changed.

    Writing the registry key is only half of it. Explorer holds a cached copy of
    the user environment and hands that copy to every process it starts, so a
    value written without a broadcast is invisible to every terminal, editor, and
    tool launched from the desktop — forever, until Explorer itself restarts. The
    broadcast is what `setx` does and what a direct `SetValueEx` does not, which
    is why a registry write here is correct for what `setx` truncates and still
    has to make up for what `setx` would have done.

    Best effort by design: a shell that misses the broadcast still reads the new
    value when it is started with a fresh environment, so failing to broadcast is
    a delay, not a wrong answer, and must not fail the install.
    """
    if sys.platform != "win32":
        return
    try:
        import ctypes

        HWND_BROADCAST = 0xFFFF
        WM_SETTINGCHANGE = 0x001A
        SMTO_ABORTIFHUNG = 0x0002
        result = ctypes.windll.user32.SendMessageTimeoutW(
            HWND_BROADCAST,
            WM_SETTINGCHANGE,
            0,
            ctypes.c_wchar_p("Environment"),
            SMTO_ABORTIFHUNG,
            5000,
            None,
        )
        del result
    except Exception:  # noqa: BLE001 - a missed broadcast must not fail an install
        return


def prepend(directory: Path) -> str:
    """Add a directory at the front of the user's PATH; return what was written.

    Front, not end, because the thing being added is the framework a person is
    about to use and an older copy of the same name earlier in the PATH would be
    found first — a wrong answer that looks like a right one.
    """
    if sys.platform == "win32":
        import winreg

        # Read and write together: a key opened for writing alone cannot be
        # queried, and the existing value is what has to be preserved.
        access = winreg.KEY_SET_VALUE | winreg.KEY_QUERY_VALUE
        with winreg.CreateKeyEx(
            winreg.HKEY_CURRENT_USER, WINDOWS_ENVIRONMENT_KEY, 0, access
        ) as key:
            existing, _ = winreg.QueryValueEx(key, "PATH")
            updated = f"{directory}{os.pathsep}{existing}" if existing else str(directory)
            winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, updated)
        _broadcast_environment_change()
        return "the user environment (HKCU\\Environment\\PATH)"
    shell_file = ".zshrc" if (Path.home() / ".zshrc").is_file() else ".profile"
    subprocess.run(
        [
            "sh",
            "-c",
            f'printf \'export PATH="{directory}:$PATH"\\n\' >> ~/{shell_file}',
        ],
        check=False,
    )
    return f"~/{shell_file}"


def ensure_on_path(directory: Path, exists: callable) -> list[str]:
    """Put a directory on the user's PATH if it holds what the caller expects.

    `exists` is asked about one named file inside the directory, so a directory
    that does not hold the thing being installed is left alone rather than
    advertised. Returns what to report; every step is idempotent.
    """
    if not exists(directory):
        return [f"{directory} holds nothing to install; PATH left alone"]
    if holds(directory):
        return [f"{directory} is already on PATH"]
    try:
        where = prepend(directory)
    except OSError as error:
        # Not fatal, and deliberately so. Everything else the installer does has
        # already happened; aborting here would leave a machine in a state its
        # owner has to reason about, over a step whose remedy is one line they
        # can read.
        return [
            f"could not add {directory} to PATH ({error}); add it yourself: "
            f'export PATH="{directory}:$PATH"'
        ]
    return [f"added {directory} to {where}", "a new shell sees it; open ones do not"]
