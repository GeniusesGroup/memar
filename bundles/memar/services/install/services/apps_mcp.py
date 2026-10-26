#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""bundles/memar/services/install/services/apps_mcp.py — the agent-app layer's second half: Memar's MCP server registered at user level in the agent apps that have a setting for one.

The owner chose (2026-10-18; bundles/memar/memar.handoff.md) user-level registration only: the
server is the machine's, like the `memar` command, and a project `.mcp.json` would be one more file
in every project to keep true by hand. So this writes into each app's own user setting, for the apps
`apps.py` already knows and that have one, and only where the app is on this machine.

The server is started as the `memar` command would run it: this interpreter, the router in the
checkout the location variable names, `mcp serve`. It is not started through `memar` on the PATH,
because an app starts a server without a shell, and on Windows only a shell finds `memar.cmd`.

A setting is changed only by adding Memar's entry or replacing it, never by rewriting the rest: a
JSON setting is read, its entry set, and written back whole through a file beside it; a TOML setting,
which the standard library reads but does not write, gets the entry appended when it has none, and
when Memar's own table differs — a moved launcher, a new interpreter — only that table is replaced
in the file's text. A setting that cannot be read, or JSON with comments, is reported and left as
it is. `warn_stale` is how a registration that is not what `server_command` would now write is
noticed: `memar update` asks it through `bundles/memar/services/update/services/copies.py`.
"""
from __future__ import annotations
from importlib import import_module
import json
import os
import re
import sys
from pathlib import Path
from machine.env_location import resolve_root
_m_fs_memar = import_module('modules-plugable.computer.memory.filesystem.services.fs_memar')
SERVER_NAME = 'memar'
ROUTER = _m_fs_memar.LAUNCHER_RELATIVE / 'memar'
SERVE = ('mcp', 'serve')
REFRESH = 'memar update --apply'

def server_command() -> list[str]:
    """What an app runs to start the server."""
    return [sys.executable, str(resolve_root() / ROUTER), *SERVE]

def _claude(command):
    return (Path.home() / '.claude.json', ('mcpServers',), {'type': 'stdio', 'command': command[0], 'args': command[1:], 'env': {}})

def _cursor(command):
    return (Path.home() / '.cursor' / 'mcp.json', ('mcpServers',), {'command': command[0], 'args': command[1:]})

def _opencode(command):
    return (Path.home() / '.config' / 'opencode' / 'opencode.json', ('mcp',), {'type': 'local', 'command': command, 'enabled': True})
JSON_APPS = {'claude': (lambda: Path.home() / '.claude', _claude), 'cursor': (lambda: Path.home() / '.cursor', _cursor), 'opencode': (lambda: Path.home() / '.config' / 'opencode', _opencode)}
CODEX_SETTING = 'config.toml'
CODEX_TABLE = f'mcp_servers.{SERVER_NAME}'
_TOML_TABLE = re.compile(rf'(?m)^\[{re.escape(CODEX_TABLE)}\]\n(?:(?!^\[).*\n?)*')

def codex_dir() -> Path:
    """The folder that says Codex is installed; it keeps its setting as TOML."""
    return Path.home() / '.codex'

def _show(dry_run: bool, setting: Path, text: str) -> None:
    verb = 'dry-run: register the MCP server in' if dry_run else 'registered the MCP server in'
    print(f'{verb} {setting}:')
    for line in text.splitlines():
        print(f'    {line}')

def _toml_table(command: list[str]) -> str:
    return f'[{CODEX_TABLE}]\ncommand = {json.dumps(command[0])}\nargs = {json.dumps(command[1:])}\n'

def _replace_toml_table(text: str, table: str) -> str:
    """Replace Memar's table in TEXT with TABLE, keeping every other byte."""
    if not _TOML_TABLE.search(text):
        return text
    return _TOML_TABLE.sub(table if table.endswith('\n') else table + '\n', text, count=1)

def into_json(setting: Path, keys: tuple[str, ...], entry: dict, *, dry_run: bool) -> None:
    """Set ENTRY under KEYS and the server's name in the JSON file SETTING, leaving the rest as it was read."""
    if not setting.exists() and setting.with_suffix('.jsonc').exists():
        print(f"not registered: {setting.with_suffix('.jsonc')} is JSON with comments, which this does not rewrite; add under")
        print(f"    {'.'.join(keys)}.{SERVER_NAME}: {json.dumps(entry)}")
        return
    try:
        whole = json.loads(setting.read_text(encoding='utf-8')) if setting.exists() else {}
    except (OSError, ValueError) as unread:
        print(f'not registered: {setting} could not be read as JSON ({unread}); left as it is')
        return
    place = whole
    for key in keys:
        place = place.setdefault(key, {}) if isinstance(place, dict) else None
    if not isinstance(place, dict):
        print(f"not registered: {setting} holds no object at {'.'.join(keys)}; left as it is")
        return
    if place.get(SERVER_NAME) == entry:
        print(f'already current: {setting}')
        return
    shown = json.dumps({key: {SERVER_NAME: entry} for key in keys[-1:]}, indent=2)
    if not dry_run:
        place[SERVER_NAME] = entry
        written = setting.with_name(f'{setting.name}.new.{os.getpid()}')
        setting.parent.mkdir(parents=True, exist_ok=True)
        written.write_text(json.dumps(whole, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
        os.replace(written, setting)
    _show(dry_run, setting, shown)

def into_toml(setting: Path, command: list[str], *, dry_run: bool) -> None:
    """Append or replace the server's table in the TOML file SETTING; leave a file that cannot be read."""
    import tomllib
    try:
        text = setting.read_text(encoding='utf-8') if setting.exists() else ''
        whole = tomllib.loads(text)
    except (OSError, ValueError) as unread:
        print(f'not registered: {setting} could not be read as TOML ({unread}); left as it is')
        return
    found = whole.get('mcp_servers', {}).get(SERVER_NAME)
    wanted = {'command': command[0], 'args': command[1:]}
    table = _toml_table(command)
    if found == wanted:
        print(f'already current: {setting}')
        return
    if found is not None:
        replaced = _replace_toml_table(text, table)
        if replaced == text:
            print(f'not registered: {setting} has a [{CODEX_TABLE}] that differs and could not be rewritten; change it to')
            for line in table.splitlines():
                print(f'    {line}')
            return
        if not dry_run:
            written = setting.with_name(f'{setting.name}.new.{os.getpid()}')
            written.write_text(replaced, encoding='utf-8', newline='\n')
            os.replace(written, setting)
        _show(dry_run, setting, table)
        return
    if not dry_run:
        separator = '' if not text or text.endswith('\n\n') else '\n' if text.endswith('\n') else '\n\n'
        with setting.open('a', encoding='utf-8', newline='\n') as appended:
            appended.write(separator + table)
    _show(dry_run, setting, table)

def _json_entry(setting: Path, keys: tuple[str, ...]) -> dict | None:
    """Memar's entry in SETTING, or None when the file has none or cannot be read for a compare."""
    if not setting.exists():
        return None
    try:
        whole = json.loads(setting.read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return None
    place = whole
    for key in keys:
        if not isinstance(place, dict):
            return None
        place = place.get(key)
    if not isinstance(place, dict):
        return None
    found = place.get(SERVER_NAME)
    return found if isinstance(found, dict) else None

def _toml_entry(setting: Path) -> dict | None:
    """Memar's table in SETTING, or None when the file has none or cannot be read for a compare."""
    import tomllib
    if not setting.exists():
        return None
    try:
        whole = tomllib.loads(setting.read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return None
    found = whole.get('mcp_servers', {}).get(SERVER_NAME)
    return found if isinstance(found, dict) else None

def stale_settings() -> list[Path]:
    """Each user-level setting that holds Memar's MCP entry with a command that is not current."""
    command = server_command()
    stale: list[Path] = []
    for folder, place in JSON_APPS.values():
        if not folder().is_dir():
            continue
        setting, keys, entry = place(command)
        found = _json_entry(setting, keys)
        if found is not None and found != entry:
            stale.append(setting)
    if codex_dir().is_dir():
        setting = codex_dir() / CODEX_SETTING
        found = _toml_entry(setting)
        wanted = {'command': command[0], 'args': command[1:]}
        if found is not None and found != wanted:
            stale.append(setting)
    return stale

def warn_stale() -> None:
    """One line per stale MCP registration, naming the command that refreshes them."""
    for setting in stale_settings():
        print(f'stale: the MCP server in {setting} is not the command the checkout would register; refresh with: {REFRESH}')

def into_apps(*, dry_run: bool=False) -> None:
    """Register the server in every agent app found that has a user-level MCP setting."""
    command = server_command()
    found = False
    for folder, place in JSON_APPS.values():
        if folder().is_dir():
            found = True
            setting, keys, entry = place(command)
            into_json(setting, keys, entry, dry_run=dry_run)
    if codex_dir().is_dir():
        found = True
        into_toml(codex_dir() / CODEX_SETTING, command, dry_run=dry_run)
    if not found:
        print('no agent app with an MCP setting is on this machine; nothing registered')
