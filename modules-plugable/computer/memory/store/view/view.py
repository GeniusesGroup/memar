#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""The builder of a memory view: a read-only folder of one class's committed nodes, as a domain presents them.

What a view is, and why it is never committed, never edited and read by no verb, is [Memory View](view.md); this file is
the one source of the key `view`, of a node as a presentation is handed it, of the list the builder keeps in the folder,
and of what a build answers. The builder reaches the store through `record` alone (`nodes`, `parts`, `get`, `state`),
handed to it already opened, so it imports no adapter; `memar view refresh` opens the class and calls `build`.

A presentation is a function from a `Node` to the files it shows: relative paths, written with forward slashes, and
their bytes. A domain registers its own for the class its services use (`register`), when the entry point of Memar's
tooling starts. Importing this file does no work: every `memar` call imports it while assembling the command line.
"""
from __future__ import annotations
import enum
import hashlib
import os
import stat
import subprocess
from dataclasses import dataclass, field
from importlib import import_module
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Mapping
VIEW_KEY = 'view'
LIST_NAME = '.memar-view'
LIST_HEADER = b'# The files `memar view refresh` wrote here, each with the SHA-256 of its bytes. Never edit this folder.\n'

@dataclass(frozen=True)
class Node:
    """A node as a presentation is handed it: its id, and the bytes of each part by its domain key."""
    id: bytes
    parts: Mapping[str, bytes]
Presentation = Callable[[Node], Mapping[str, bytes]]
_PRESENTATIONS: dict[str, Presentation] = {}

def register(class_name: str, presentation: Presentation) -> None:
    """Make PRESENTATION the one that shows the nodes of CLASS_NAME; a second registration replaces the first."""
    _PRESENTATIONS[class_name] = presentation

def presentation(class_name: str) -> Presentation | None:
    """The presentation registered for CLASS_NAME, or None."""
    return _PRESENTATIONS.get(class_name)

def view_preference(project: Path) -> dict[str, str] | None:
    """The class PROJECT's `view` key shows and the folder it is built in, relative to the project's top folder: empty
    when the key is unset, None when its form is broken or it names more than one class."""
    preferences = import_module('modules.process.project.services.preferences')
    values = preferences.class_values_preference(Path(project), VIEW_KEY)
    return None if values is None or len(values) > 1 else values

class ViewRefusal(enum.Enum):
    """Why a build is refused; nothing is written or removed."""
    UNIGNORED_FOLDER = 'UnignoredFolder'
    FOREIGN_FILES = 'ForeignFiles'
    MALFORMED_PATH = 'MalformedPath'
    UNAVAILABLE = 'Unavailable'

    def summary(self) -> str:
        return {ViewRefusal.UNIGNORED_FOLDER: 'the folder is in a working tree under version control, which does not ignore it', ViewRefusal.FOREIGN_FILES: 'the folder holds a file the builder did not write', ViewRefusal.MALFORMED_PATH: 'the presentation gave a path that leaves the folder, names the list, or shows two things', ViewRefusal.UNAVAILABLE: 'the store did not answer every read'}[self]

@dataclass(frozen=True)
class ViewRefused:
    """The build is refused and the folder is as it was; `detail` names what, for a reader."""
    reason: ViewRefusal
    detail: str = field(default='', compare=False)

    def summary(self) -> str:
        return f'{self.reason.summary()}: {self.detail}' if self.detail else self.reason.summary()

@dataclass(frozen=True)
class Built:
    """A build that finished: files written, removed, left as they were, and found changed by hand (rewritten)."""
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
    """Why FOLDER may not hold a view, when it lies in a working tree that does not ignore it; None when it may."""
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
    """The files the list in FOLDER names, with their tokens; empty when there is no list, None when it is not one."""
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
    """Every node of RECORD, with the bytes of its parts, read from one committed state."""
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
    """Build the view of RECORD's committed nodes, as PRESENTATION shows them, in FOLDER; every refusal is decided first."""
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
