#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""The one variable that says where Memar lives: read it, write it, resolve it.

A user-level environment variable is written to the place the platform keeps it
— the registry-backed user environment on Windows, the user's shell profile on
POSIX — and that record is where the value lives. The process environment is
the copy a program started with, and a copy can be older than what it copied.

So the record decides, and the copy only fills in what the record does not say.
When the two disagree the record is used and the disagreement is printed, never
swallowed: a session that reads nothing where a record exists concludes that
Memar was never installed, and installs again over a location that is already
recorded — overwriting the recorded value and the editor's extensions along with
it. Which is why the reading and the writing here name the same place, and why
this is the only read of the variable in this folder.
"""
from __future__ import annotations
from machine.plugable_import import load as plugable_load
_m_fs_memar_repository = plugable_load('computer.filesystem.services.fs_memar_repository')
is_memar_repository = _m_fs_memar_repository.is_memar_repository
not_a_repository = _m_fs_memar_repository.not_a_repository
import os
import re
import sys
from pathlib import Path
from machine.console import fail, note
VARIABLE = 'MEMAR_ROOT'
WINDOWS_ENVIRONMENT_KEY = 'Environment'
PROFILE_BEGIN = f'# >>> {VARIABLE} (written by Memar .agents/scripts/install.sh) >>>'
PROFILE_END = f'# <<< {VARIABLE} <<<'
PROFILE_ASSIGNMENT = re.compile(f'^\\s*(?:export\\s+)?{VARIABLE}\\s*=\\s*(.*?)\\s*$')
INSTALL_HINT = f"run install.sh (POSIX) or install.ps1 (Windows) — the bootstrap in this folder, which a consuming project's AGENTS.md also names — or set {VARIABLE} yourself for this session"
NOTICE_REPORTED = False

def shell_profile() -> Path:
    shell = Path(os.environ.get('SHELL', ''))
    name = shell.name
    if name == 'bash':
        return Path.home() / '.bashrc'
    if name == 'zsh':
        return Path.home() / '.zshrc'
    return Path.home() / '.profile'

def expand_recorded(value: str) -> str:
    """A recorded value with the variables Windows expands in it expanded.

    The value is written as REG_EXPAND_SZ, which Windows expands when it builds
    a new process's environment, so reading it back expands it too: the record
    and the copy of it agree by construction.
    """
    return os.path.expandvars(value).strip()

def profile_value() -> str:
    """What the user's shell profile records, or nothing."""
    try:
        text = shell_profile().read_text(encoding='utf-8')
    except OSError:
        return ''
    value = ''
    for line in text.splitlines():
        found = PROFILE_ASSIGNMENT.match(line)
        if found:
            value = found.group(1)
    if len(value) >= 2 and value[0] == value[-1] and (value[0] in '"\''):
        value = value[1:-1]
    return value

def user_environment_value() -> str:
    """What the registry-backed user environment records, or nothing.

    The key is opened by name and the value read from it, which is the way the
    writing does it; asking a predefined key for a value whose name contains a
    backslash is not the same thing, and reports no value rather than a wrong one.
    """
    import winreg
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, WINDOWS_ENVIRONMENT_KEY, 0, winreg.KEY_QUERY_VALUE) as key:
            value, kind = winreg.QueryValueEx(key, VARIABLE)
    except OSError:
        return ''
    text = str(value)
    return expand_recorded(text) if kind == winreg.REG_EXPAND_SZ else text.strip()

def persisted_value() -> str:
    """What the platform's own record of the variable holds, or nothing.

    This is the record: what a program started *now* would be given, whether or
    not this one was started before it was written.
    """
    if os.name == 'nt':
        return user_environment_value()
    return profile_value()

def write_profile_variable(value: str) -> Path:
    """Write the managed block, replacing it as a unit so re-running rewrites
    the value rather than appending a second export of the same name."""
    profile = shell_profile()
    line = f'export {VARIABLE}="{value}"'
    try:
        original = profile.read_text(encoding='utf-8')
    except OSError:
        original = ''
    kept: list[str] = []
    inside = False
    for existing in original.splitlines():
        if existing == PROFILE_BEGIN:
            inside = True
            continue
        if inside:
            if existing == PROFILE_END:
                inside = False
            continue
        kept.append(existing)
    while kept and (not kept[-1].strip()):
        kept.pop()
    block = [PROFILE_BEGIN, line, PROFILE_END]
    profile.parent.mkdir(parents=True, exist_ok=True)
    profile.write_text('\n'.join([*kept, '', *block, '']), encoding='utf-8')
    return profile

def write_user_variable(value: str) -> str:
    if os.name == 'nt':
        import winreg
        access = winreg.KEY_SET_VALUE | winreg.KEY_QUERY_VALUE
        with winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, WINDOWS_ENVIRONMENT_KEY, 0, access) as key:
            winreg.SetValueEx(key, VARIABLE, 0, winreg.REG_EXPAND_SZ, value)
        return "the current user's environment (HKCU\\Environment)"
    profile = write_profile_variable(value)
    return str(profile)

def report_stale_session(record: str, session: str) -> None:
    """Say that this session's copy disagrees with the record, and that the
    record is what was used. A stale copy is not a decision, and a reader who
    cannot see it cannot tell an install from a re-install."""
    global NOTICE_REPORTED
    if NOTICE_REPORTED:
        return
    NOTICE_REPORTED = True
    note(f"warning: {VARIABLE} in this session's environment disagrees with the record, so the record is used: recorded {record}, this session {session or 'unset'}")

def recorded_value() -> str:
    """What the variable says, or nothing. The only read of it in this folder.

    The record answers whenever it has an answer, including when this process
    started before it was written. It falls back to the process environment
    only where the record is silent: a value someone set for this run is a
    record for this run, and the folder README makes that equivalent to writing
    it. The two are never merged, and never averaged.
    """
    record = persisted_value()
    session = os.environ.get(VARIABLE, '').strip()
    if record and record != session:
        report_stale_session(record, session)
    return record or session

def recorded_root() -> Path | None:
    """The checkout the variable names, or None.

    None covers both ways it fails to be an answer: unset, and set to something
    that is not a Memar repository. Deciding which is which is the caller's, so
    it can say the right thing about each.
    """
    value = recorded_value()
    if not value:
        return None
    path = Path(value).expanduser()
    return path if is_memar_repository(path) else None

def resolve_root() -> Path:
    """The checkout the variable names, or stop saying what to do about it.

    Never installs and never falls back to a location of its own: a session that
    quietly puts a repository on the machine produces a location nothing else
    agrees on, which is the failure the single variable exists to prevent.
    """
    value = recorded_value()
    if not value:
        fail(f'{VARIABLE} is not set, so where Memar lives on this machine is not recorded anywhere; {INSTALL_HINT}.')
    path = Path(value).expanduser()
    if not is_memar_repository(path):
        fail(f'{VARIABLE} points at {value}, and {not_a_repository(path)}. Nothing else is tried: {INSTALL_HINT}; to keep it, point {VARIABLE} at a Memar repository you already have.')
    return path.resolve()

def refuse_bogus_value() -> None:
    """A value that is set but names no Memar repository is reported, never
    quietly overwritten: something else put it there, and only the person who put
    it there can say what it was meant to be."""
    value = recorded_value()
    if not value or recorded_root() is not None:
        return
    fail(f"{VARIABLE} is set to {value}, and {not_a_repository(Path(value).expanduser())}. It was left as it is. Clear it and run this again — on POSIX `unset {VARIABLE}` in your shell profile, on Windows [Environment]::SetEnvironmentVariable('{VARIABLE}', $null, 'User') — or point it at a Memar repository.")
