#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import hashlib
from importlib import import_module
from pathlib import Path
_m_edit = import_module('modules.knowledge.text.errors.edit')


def snapshot(path: Path) -> dict:
    try:
        raw = path.read_bytes()
    except OSError:
        return {'exists': False, 'hash': None, 'mtime_ns': None, 'size': None}
    digest = hashlib.sha256(raw).hexdigest()
    try:
        stat = path.stat()
    except OSError:
        return {'exists': True, 'hash': digest, 'mtime_ns': None, 'size': len(raw)}
    return {'exists': True, 'hash': digest, 'mtime_ns': stat.st_mtime_ns, 'size': stat.st_size}


class Text_Edit_Stamp_Held:

    def __init__(self, state: dict) -> None:
        self.state = state

    def is_same(self, other) -> bool:
        return self.state == other.state


class Text_Edit_Store_Held:

    def __init__(self, path):
        self.path = Path(path)

    def exists(self):
        return self.path.is_file()

    def get_bytes(self):
        try:
            return self.path.read_bytes()
        except OSError as error:
            raise _m_edit.Text_Error_Edit_ReadFailed(f'cannot read {self.path}: {error}') from None

    def replace_bytes(self, data):
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open('wb') as handle:
                handle.write(data)
        except OSError as error:
            raise _m_edit.Text_Error_Edit_WriteFailed(f'cannot write {self.path}: {error}') from None

    def get_stamp(self):
        return Text_Edit_Stamp_Held(snapshot(self.path))

    def get_key(self):
        try:
            return str(self.path.resolve())
        except OSError:
            return str(self.path.absolute())
