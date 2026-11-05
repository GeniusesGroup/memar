#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import hashlib
import json
import os
import sys
import time
from importlib import import_module
from pathlib import Path
_m_edit = import_module('modules.knowledge.text.errors.edit')
_m_fs_lock = import_module('bundles.memar_fs.services.fs_lock')
_m_memar_location = import_module('bundles.memar.services.location.memar_location')
EDIT_LOCK_DIR_NAME = 'memar-edit-locks'


def lock_path(key: str, folder: Path | None) -> Path:
    directory = Path(folder) if folder is not None else _m_memar_location.scratch_root() / EDIT_LOCK_DIR_NAME
    directory.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256(key.encode('utf-8')).hexdigest()[:16]
    name = Path(key).name
    stem = ''.join((character if character.isalnum() or character in '-_' else '-' for character in name)).strip('-')[:32] or 'file'
    return directory / f'memar-edit-{stem}-{digest}.lock'


def intent_path(lock: Path) -> Path:
    return Path(str(lock) + '.intent.json')


def write_intent(lock: Path, writer: str, key: str, summary: str, base: dict) -> None:
    payload = {'task_id': writer, 'file': key, 'plan_summary': summary, 'base_hash': base.get('hash'), 'base_mtime_ns': base.get('mtime_ns'), 'base_size': base.get('size'), 'created_at': time.time()}
    intent = intent_path(lock)
    temporary = intent.with_name(f'{intent.name}.{os.getpid()}.tmp')
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + '\n', encoding='utf-8', newline='\n')
    os.replace(temporary, intent)


class Text_Edit_Held_Held:

    def __init__(self, lock: Path) -> None:
        self.lock = lock

    def release(self):
        for leftover in (self.lock, intent_path(self.lock)):
            try:
                leftover.unlink()
            except OSError:
                pass


class Text_Edit_Lock_Held:

    def __init__(self, lock_folder=None):
        self.lock_folder = lock_folder

    def take(self, store, writer, summary, limits):
        base = store.get_stamp()
        key = store.get_key()
        wait = limits.get_wait_seconds()
        stale = limits.get_stale_seconds()
        poll = limits.get_poll_seconds()
        try:
            lock = lock_path(key, self.lock_folder)
            deadline = time.monotonic() + wait
            announced = False
            while not _m_fs_lock.try_lock(lock, stale):
                if not announced:
                    sys.stderr.write(f'another task is editing; waiting for it (lock: {lock})\n')
                    announced = True
                if time.monotonic() > deadline:
                    raise _m_edit.Text_Error_Edit_Locked(f'waited {wait}s for the edit lock ({lock}) and it is still held; if no task is editing, remove that file and run this again.')
                time.sleep(poll)
        except OSError as error:
            raise _m_edit.Text_Error_Edit_LockUnwritable(f'cannot make the edit lock: {error}') from None
        held = Text_Edit_Held_Held(lock)
        try:
            write_intent(lock, writer, key, summary, base.state)
            if not base.is_same(store.get_stamp()):
                raise _m_edit.Text_Error_Edit_ChangedWhileWaiting(f'{key} changed since the plan was made; re-derive the plan against the current content.')
        except OSError as error:
            held.release()
            raise _m_edit.Text_Error_Edit_LockUnwritable(f'cannot write the intent note: {error}') from None
        except BaseException:
            held.release()
            raise
        return held
