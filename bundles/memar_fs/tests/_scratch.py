#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import subprocess
import sys
import tempfile
import threading
import unittest
import unittest.mock
from importlib import import_module
from pathlib import Path
TESTS = Path(__file__).resolve().parent
BUNDLE = TESTS.parent
TOP = BUNDLE.parent.parent
for _folder in (TOP, TOP / 'bundles' / 'memar', TOP / 'bundles' / 'memar' / 'services'):
    if str(_folder) not in sys.path:
        sys.path.insert(0, str(_folder))
sys.dont_write_bytecode = True
suite_scratch = import_module('modules.process.test.services.test_scratch').suite_scratch
text_edit_lock = import_module('bundles.memar_fs.services.text_edit_lock')
text_edit_store = import_module('bundles.memar_fs.services.text_edit_store')
memar_location = import_module('bundles.memar.services.location.memar_location')
PROCESS_SECONDS = 60
HOLD_SECONDS = 1.5

class HoldLimits:

    def get_wait_seconds(self) -> float:
        return 120

    def get_stale_seconds(self) -> float:
        return 120

    def get_poll_seconds(self) -> float:
        return 0.5

def bundle(dotted: str):
    return import_module(f'bundles.memar_fs.{dotted}')

def errors():
    return bundle('errors.errors')

def git_in(folder: Path, *args: str) -> str:
    return subprocess.run(['git', '-C', str(folder), *args], capture_output=True, text=True, check=True, timeout=PROCESS_SECONDS).stdout.strip()

class ScratchFolder(unittest.TestCase):

    def setUp(self) -> None:
        scratch = tempfile.TemporaryDirectory(dir=suite_scratch(), prefix='tmp-fs-', ignore_cleanup_errors=True)
        self.addCleanup(scratch.cleanup)
        self.root = Path(scratch.name)
        self.memar_root = self.root / 'memar'
        self.memar_root.mkdir()
        patched = unittest.mock.patch.object(memar_location, 'memar_root', return_value=self.memar_root)
        patched.start()
        self.addCleanup(patched.stop)

    def held_locks(self) -> list[Path]:
        return list((self.memar_root / 'temp').rglob('*.lock'))

    def blocked_while_locked(self, target: Path, act) -> None:
        outcome: dict = {}

        def run() -> None:
            try:
                outcome['value'] = act()
            except BaseException as error:
                outcome['error'] = error
        held = text_edit_lock.Text_Edit_Lock_Held().take(text_edit_store.Text_Edit_Store_Held(target), 'test-holder', 'hold', HoldLimits())
        try:
            worker = threading.Thread(target=run)
            worker.start()
            worker.join(HOLD_SECONDS)
            if 'error' in outcome:
                raise outcome['error']
            self.assertTrue(worker.is_alive(), 'the act finished while another holder had the lock of the file')
        finally:
            held.release()
        worker.join(PROCESS_SECONDS)
        if 'error' in outcome:
            raise outcome['error']
        self.assertFalse(worker.is_alive())

def junction_or_symlink(link: Path, target: Path) -> bool:
    try:
        link.symlink_to(target, target_is_directory=True)
        return True
    except (OSError, NotImplementedError):
        pass
    done = subprocess.run(['cmd', '/c', 'mklink', '/J', str(link), str(target)], capture_output=True, text=True)
    return done.returncode == 0
