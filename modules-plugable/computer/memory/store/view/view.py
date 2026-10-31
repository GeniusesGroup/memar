#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import hashlib
import os
import stat
import subprocess
from dataclasses import dataclass, field
from importlib import import_module
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Mapping
_m_errors = import_module('modules-plugable.computer.memory.store.view.errors.errors')
ViewRefusal = _m_errors.ViewRefusal
ViewRefused = _m_errors.ViewRefused
VIEW_KEY = 'view'
LIST_NAME = '.memar-view'
LIST_HEADER = b'# The files `memar view refresh` wrote here, each with the SHA-256 of its bytes. Never edit this folder.\n'

@dataclass(frozen=True)
class Node:
    id: bytes
    parts: Mapping[str, bytes]
Presentation = Callable[[Node], Mapping[str, bytes]]
_PRESENTATIONS: dict[str, Presentation] = {}

def register(class_name: str, presentation: Presentation) -> None:
    _PRESENTATIONS[class_name] = presentation

def presentation(class_name: str) -> Presentation | None:
    return _PRESENTATIONS.get(class_name)

def view_preference(project: Path) -> dict[str, str] | None:
    preferences = import_module('modules.computer.software.edges.manifest.services.preferences')
    values = preferences.class_values_preference(Path(project), VIEW_KEY)
    return None if values is None or len(values) > 1 else values

@dataclass(frozen=True)
class Built:
    written: int
    removed: int
    unchanged: int
    drift: int

    def summary(self) -> str:
        said = f'{self.written} file(s) written, {self.removed} removed, {self.unchanged} unchanged'
        return f'{said}; {self.drift} changed by hand and restored from the store' if self.drift else said

def _token(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def _unignored(folder: Path) -> str | None:
    probe = folder
    while not probe.exists():
        probe = probe.parent
    top = subprocess.run(['git', '-C', str(probe), 'rev-parse', '--show-toplevel'], capture_output=True, text=True)
    if top.returncode != 0:
        return None
    relative = os.path.relpath(folder, Path(top.stdout.strip()))
    if relative == '.' or relative.startswith('..'):
        return f'{folder} is the top of a working tree' if relative == '.' else None
    ignored = subprocess.run(['git', '-C', top.stdout.strip(), 'check-ignore', '-q', Path(relative).as_posix() + '/'], capture_output=True)
    return None if ignored.returncode == 0 else f'{folder} is in the working tree {top.stdout.strip()}, which does not ignore it; add it to the ignore list first'

def _listed(folder: Path) -> dict[str, str] | None:
    try:
        lines = (folder / LIST_NAME).read_bytes().decode('utf-8').splitlines()
    except FileNotFoundError:
        return {}
    except (OSError, UnicodeDecodeError):
        return None
    listed: dict[str, str] = {}
    for line in lines:
        if line.startswith('#') or not line:
            continue
        token, separator, path = line.partition(' ')
        if not separator or len(token) != 64:
            return None
        listed[path] = token
    return listed

def _list_bytes(written: Mapping[str, str]) -> bytes:
    return LIST_HEADER + b''.join((f'{token} {path}\n'.encode('utf-8') for path, token in sorted(written.items())))

def _well_formed(path: str) -> bool:
    if not isinstance(path, str) or not path or '\\' in path or ':' in path or path.startswith('/'):
        return False
    parts = path.split('/')
    return all((part and part not in ('.', '..') for part in parts)) and parts[0] != LIST_NAME

def _committed_nodes(record: Any) -> list[Node] | ViewRefused:
    key = import_module('modules-plugable.computer.memory.store.record.record').key
    while True:
        state = record.state()
        ids = record.nodes()
        if not isinstance(ids, tuple):
            return ViewRefused(ViewRefusal.UNAVAILABLE, f'`nodes` answered {ids}')
        held = record.parts(list(ids)) if ids else []
        if not isinstance(held, list) or any((not isinstance(each, tuple) for each in held)):
            return ViewRefused(ViewRefusal.UNAVAILABLE, '`parts` did not answer every node')
        keys = [key(at, name) for at, pairs in zip(ids, held) for name, _ in pairs]
        values = record.get(keys) if keys else []
        if record.state() != state:
            continue
        if not isinstance(values, list) or any((not hasattr(each, 'value') for each in values)):
            return ViewRefused(ViewRefusal.UNAVAILABLE, '`get` did not answer every part')
        found = iter(values)
        return [Node(at, {name: next(found).value for name, _ in pairs}) for at, pairs in zip(ids, held)]

def _writable(path: Path) -> None:
    os.chmod(path, stat.S_IWRITE | stat.S_IREAD)

def _write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        _writable(path)
    path.write_bytes(data)
    os.chmod(path, stat.S_IREAD)

def build(record: Any, presentation: Presentation, folder: Path) -> Built | ViewRefused:
    folder = Path(folder).resolve()
    why = _unignored(folder)
    if why:
        return ViewRefused(ViewRefusal.UNIGNORED_FOLDER, why)
    listed = _listed(folder) if folder.is_dir() else {}
    if listed is None:
        return ViewRefused(ViewRefusal.FOREIGN_FILES, f'{folder / LIST_NAME} is not a list the builder wrote')
    present = sorted((each.relative_to(folder).as_posix() for each in folder.rglob('*') if each.is_file())) if folder.is_dir() else []
    foreign = [each for each in present if each != LIST_NAME and each not in listed]
    if foreign:
        return ViewRefused(ViewRefusal.FOREIGN_FILES, ', '.join(foreign[:5]) + (' and more' if len(foreign) > 5 else ''))
    nodes = _committed_nodes(record)
    if isinstance(nodes, ViewRefused):
        return nodes
    wanted: dict[str, bytes] = {}
    for node in nodes:
        for path, data in presentation(node).items():
            if not _well_formed(path) or path in wanted or not isinstance(data, bytes):
                return ViewRefused(ViewRefusal.MALFORMED_PATH, f'{path!r} of the node {node.id.hex()}')
            wanted[path] = data
    folders = {str(PurePosixPath(path).parent) for path in wanted}
    clash = sorted((path for path in wanted if path in folders))
    if clash:
        return ViewRefused(ViewRefusal.MALFORMED_PATH, f'{clash[0]!r} is both a file and a folder')
    written = removed = unchanged = drift = 0
    for path, data in sorted(wanted.items()):
        target = folder / path
        current = target.read_bytes() if target.is_file() else None
        if current == data:
            unchanged += 1
            if target.stat().st_mode & stat.S_IWRITE:
                os.chmod(target, stat.S_IREAD)
            continue
        if path in listed and (current is None or _token(current) != listed[path]):
            drift += 1
        _write(target, data)
        written += 1
    for path in sorted(set(listed) - set(wanted)):
        target = folder / path
        if target.is_file():
            _writable(target)
            target.unlink()
        removed += 1
        for parent in target.parents:
            if parent == folder or not parent.is_dir() or any(parent.iterdir()):
                break
            parent.rmdir()
    tokens = {path: _token(data) for path, data in wanted.items()}
    if tokens != listed or not (folder / LIST_NAME).is_file():
        _write(folder / LIST_NAME, _list_bytes(tokens))
    return Built(written, removed, unchanged, drift)
