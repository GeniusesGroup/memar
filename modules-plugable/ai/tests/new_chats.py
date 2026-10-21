#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the prompt that asks the owner to run sessions each in a new chat, in `modules-plugable/ai/services/new_chats.py`.

    python modules/management/task/tests/new_chats.py

Named for the file that holds the subject per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes outside its scratch folder: the Memar root is patched onto
one made under the folder `modules-plugable/computer/filesystem/services/fs_test_scratch.py` names.

What is pinned, and what each pin is for:

  Message   For each session the message holds its title, its priority, the
            first sentence of its Why and the very text
            `plan_brief.brief_text` gives; a session named by
            `--blocking` is marked blocks and the others independent.
  Refusals  An id with no folder or plan, and a `--blocking` id that is not
            among the sessions, are refused and print nothing.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
from importlib import import_module
_m_fs_test_scratch = import_module('modules-plugable.computer.filesystem.services.fs_test_scratch')
suite_scratch = _m_fs_test_scratch.suite_scratch
_m_fs_memar = import_module('modules-plugable.computer.filesystem.services.fs_memar')
memar_fs = _m_fs_memar
import contextlib
import io
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parents[2] / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
new_chats = import_module('modules-plugable.ai.services.get_new_chats_ask')
brief_text = import_module('modules-plugable.ai.services.get_task_plan_carry_out_brief').brief_text
FIRST, SECOND = ('20261016-T000000Z-1', '20261016-T000000Z-2')

class Fixture(unittest.TestCase):

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        patched = unittest.mock.patch.object(memar_fs, 'memar_root', return_value=Path(self.scratch.name))
        patched.start()
        self.addCleanup(patched.stop)

    def session(self, sid: str, title: str, priority: int, why: str) -> None:
        folder = memar_fs.task_dir(sid, create=True)
        (folder / 'plan.md').write_bytes(f'---\nTitle: {title}\nStatus: Queued\nPriority: {priority}\n---\n# {title}\n\n## Request\nR.\n\n## Why\n{why}\n\n## Steps\n1. x\n'.encode())

    def printed(self, ids: list[str], blocking: list[str]) -> str:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            new_chats.get_new_chats_ask(ids, blocking)
        return out.getvalue()

class Message(Fixture):

    def test_each_session_is_described_marked_and_handed_over_by_the_one_brief(self) -> None:
        self.session(FIRST, 'First task', 9, 'Because one. And more words.')
        self.session(SECOND, 'Second task', 3, 'Because two.')
        text = self.printed([FIRST, SECOND], [FIRST])
        self.assertIn('First task — priority 9 — blocks\nWhy: Because one.\n' + brief_text(FIRST), text)
        self.assertNotIn('And more words', text)
        self.assertIn('Second task — priority 3 — independent\nWhy: Because two.\n' + brief_text(SECOND), text)
        self.assertLess(text.index('First task'), text.index('Second task'))

class Refusals(Fixture):

    def test_an_unknown_session_or_a_blocking_id_outside_the_list_prints_nothing(self) -> None:
        self.session(FIRST, 'First task', 9, 'Because one.')
        for ids, blocking in (([SECOND], []), ([FIRST], [SECOND])):
            with self.subTest(ids=ids, blocking=blocking):
                with contextlib.redirect_stdout(io.StringIO()) as out, self.assertRaises(SystemExit):
                    new_chats.get_new_chats_ask(ids, blocking)
                self.assertEqual(out.getvalue(), '')
if __name__ == '__main__':
    unittest.main(verbosity=2)
