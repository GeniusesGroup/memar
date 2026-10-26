#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the skill pointer the agent-app layer, `bundles/memar/services/install/services/apps.py`, writes into agent apps.

    python bundles/memar/services/install/tests/apps.py

The subject is the pointer written into an agent app, per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns the installer per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes to a real agent app. The checkout, the destination, and the
home folder the apps are looked for in are scratch folders inside this one, and
the trash is a stand-in that only removes the path so the pointer can land. The
platform's trash is not this test's to call.

What is pinned, and what each pin is for:

  PointerNotCopy           An app gets one file, SKILL.md: frontmatter with
                           `name: memar` and the checkout's description, and a
                           body that sends the agent to the checkout's skill by
                           `memar content resolve-path` with the bootstrap for when
                           `memar` is not on PATH. Nothing else of the skill is
                           copied. A dry run writes nothing and prints the
                           pointer it would write.
  ReplacingTrashesIt       What is already in an app's skill folder — a full
                           copy, a local edit — is moved to the trash before
                           the pointer is written. A dry run does not touch it.
  StalePointersNamed       A skill folder that is not the pointer the checkout
                           would now write — a full copy, an old description,
                           a file beside the pointer — is named on one line
                           with the command that refreshes it, and nothing is
                           written; when every pointer matches nothing is
                           printed, since `memar update` relays these lines.
                           A refresh replaces a full copy by the pointer, and a
                           second check names nothing.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
from importlib import import_module
_m_fs_test_scratch = import_module('modules-plugable.computer.memory.filesystem.services.fs_test_scratch')
suite_scratch = _m_fs_test_scratch.suite_scratch
import contextlib
import io
import shutil
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = next(p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()) / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS / 'services'))
sys.path.insert(1, str(SCRIPTS))
sys.path.insert(2, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
import bundles.memar.services.install.services.apps as apps
from bundles.memar.services.install.services.project import POSIX_BOOTSTRAP, WINDOWS_BOOTSTRAP
DESCRIPTION = 'description: Operating practices for work the Memar way.'
SKILL = f'---\nname: memar\n{DESCRIPTION}\n---\n\n# Memar\nThe whole skill.\n'

class Checkout(unittest.TestCase):
    """A scratch home and a scratch checkout whose skill has a part folder."""

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        root = Path(self.scratch.name)
        self.home = root / 'home'
        self.home.mkdir()
        self.source = root / 'checkout' / '.agents' / 'skills' / 'memar'
        (self.source / 'part').mkdir(parents=True)
        (self.source / 'SKILL.md').write_text(SKILL, encoding='utf-8')
        (self.source / 'part' / 'more.md').write_text('more\n', encoding='utf-8')
        for patch in (unittest.mock.patch.object(Path, 'home', return_value=self.home), unittest.mock.patch.object(apps, 'resolve_root', return_value=self.source.parents[2])):
            patch.start()
            self.addCleanup(patch.stop)

    def full_copy_into(self, app_dir: str) -> Path:
        dest = self.home / app_dir / 'skills' / 'memar'
        shutil.copytree(self.source, dest)
        return dest

    def pointer_into(self, app_dir: str) -> Path:
        dest = self.home / app_dir / 'skills' / 'memar'
        dest.mkdir(parents=True)
        (dest / 'SKILL.md').write_text(apps.pointer_text(self.source), encoding='utf-8', newline='\n')
        return dest

    def run_quietly(self, call, *args, **kwargs) -> str:
        out = io.StringIO()
        with unittest.mock.patch.object(apps, 'soft_delete', side_effect=shutil.rmtree):
            with contextlib.redirect_stdout(out):
                call(*args, **kwargs)
        return out.getvalue()

class PointerNotCopy(Checkout):
    """An app gets the pointer, and only the pointer."""

    def test_the_pointer_has_the_frontmatter_and_the_content_path_line(self) -> None:
        text = apps.pointer_text(self.source)
        self.assertTrue(text.startswith(f'---\nname: memar\n{DESCRIPTION}\n---\n'))
        self.assertIn(f"Load and follow the Memar skill, the file `{(self.source / 'SKILL.md').as_posix()}`.", text)
        self.assertIn('run `memar content resolve-path .agents/skills/memar/SKILL.md` and load and follow the file it prints', text)
        self.assertIn('If `memar` is not on PATH', text)
        self.assertIn(WINDOWS_BOOTSTRAP, text)
        self.assertIn(POSIX_BOOTSTRAP, text)
        self.assertNotIn('The whole skill.', text)

    def test_a_description_over_several_lines_is_carried_whole(self) -> None:
        (self.source / 'SKILL.md').write_text('---\nname: memar\ndescription: >\n  first line\n  second line\nother: x\n---\nbody\n', encoding='utf-8')
        self.assertIn('\ndescription: >\n  first line\n  second line\n---\n', apps.pointer_text(self.source))
        self.assertNotIn('other: x', apps.pointer_text(self.source))

    def test_install_writes_only_the_pointer_into_each_app(self) -> None:
        (self.home / '.claude').mkdir()
        self.run_quietly(apps.into_apps)
        for app_dir in ('.agents', '.claude'):
            dest = self.home / app_dir / 'skills' / 'memar'
            with self.subTest(app=app_dir):
                self.assertEqual([p.name for p in dest.iterdir()], ['SKILL.md'])
                self.assertEqual((dest / 'SKILL.md').read_bytes(), apps.pointer_text(self.source).encode('utf-8'))

    def test_a_dry_run_writes_nothing_and_prints_the_pointer(self) -> None:
        (self.home / '.claude').mkdir()
        out = self.run_quietly(apps.into_apps, dry_run=True)
        self.assertFalse((self.home / '.agents').exists())
        self.assertFalse((self.home / '.claude' / 'skills').exists())
        self.assertIn(f"dry-run: write {self.home / '.agents' / 'skills' / 'memar' / 'SKILL.md'}", out)
        self.assertIn('memar content resolve-path .agents/skills/memar/SKILL.md', out)

class ReplacingTrashesIt(Checkout):
    """What is in an app's skill folder is trashed, not deleted, before the pointer lands."""

    def setUp(self) -> None:
        super().setUp()
        self.dest = self.home / '.agents' / 'skills' / 'memar'
        self.dest.mkdir(parents=True)
        (self.dest / 'local-edit.md').write_text('keep me\n', encoding='utf-8')

    def test_what_is_there_is_trashed_before_the_pointer_is_written(self) -> None:
        with unittest.mock.patch.object(apps, 'soft_delete', side_effect=shutil.rmtree) as trash:
            with contextlib.redirect_stdout(io.StringIO()):
                apps.write_pointer('pointer\n', self.dest, dry_run=False)
        trash.assert_called_once_with(self.dest)
        self.assertEqual([p.name for p in self.dest.iterdir()], ['SKILL.md'])
        source = Path(apps.__file__).read_text(encoding='utf-8')
        self.assertNotIn('rmtree', source)
        self.assertNotIn('unlink(', source)
        self.assertIn('soft_delete', source)

    def test_a_dry_run_leaves_what_is_there_where_it_is(self) -> None:
        with unittest.mock.patch.object(apps, 'soft_delete') as trash:
            with contextlib.redirect_stdout(io.StringIO()):
                apps.write_pointer('pointer\n', self.dest, dry_run=True)
        trash.assert_not_called()
        self.assertTrue((self.dest / 'local-edit.md').is_file())
        self.assertFalse((self.dest / 'SKILL.md').exists())

class StalePointersNamed(Checkout):
    """A skill folder that is not the pointer the checkout would write is named; a refresh replaces it."""

    def test_pointers_that_match_are_not_named_and_nothing_is_printed(self) -> None:
        self.pointer_into('.agents')
        self.pointer_into('.cursor')
        (self.home / '.claude').mkdir()
        self.assertEqual(apps.stale_copies(self.source), [])
        self.assertEqual(self.run_quietly(apps.warn_stale, self.source), '')

    def test_a_full_copy_an_old_description_or_an_extra_file_is_stale(self) -> None:
        full = self.full_copy_into('.agents')
        old = self.pointer_into('.cursor')
        (old / 'SKILL.md').write_text(apps.pointer_text(self.source).replace('Operating', 'Old'), encoding='utf-8', newline='\n')
        extra = self.pointer_into('.claude')
        (extra / 'local.md').write_text('mine\n', encoding='utf-8')
        self.pointer_into('.codex')
        self.assertEqual(apps.stale_copies(self.source), [full, old, extra])

    def test_each_stale_folder_gets_one_line_naming_the_refresh_and_nothing_is_written(self) -> None:
        dest = self.full_copy_into('.agents')
        with unittest.mock.patch.object(apps, 'soft_delete') as trash:
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                apps.warn_stale(apps.checkout_skill())
        trash.assert_not_called()
        lines = out.getvalue().splitlines()
        self.assertEqual(len(lines), 1)
        self.assertIn(str(dest), lines[0])
        self.assertIn('memar update --apply', lines[0])
        self.assertEqual((dest / 'SKILL.md').read_text(encoding='utf-8'), SKILL)

    def test_update_replaces_a_full_copy_and_a_second_check_names_nothing(self) -> None:
        full = self.full_copy_into('.agents')
        current = self.pointer_into('.cursor')
        with unittest.mock.patch.object(apps, 'soft_delete', side_effect=shutil.rmtree) as trash:
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                apps.into_apps(existing_only=True)
        trash.assert_called_once_with(full)
        self.assertEqual([p.name for p in full.iterdir()], ['SKILL.md'])
        self.assertIn(f'already current: {current}', out.getvalue())
        self.assertEqual(apps.stale_copies(self.source), [])
        self.assertEqual(self.run_quietly(apps.warn_stale, self.source), '')
        self.assertIn(f'already current: {full}', self.run_quietly(apps.into_apps, existing_only=True))

    def test_a_checkout_without_the_skill_names_nothing(self) -> None:
        self.full_copy_into('.agents')
        self.assertEqual(apps.stale_copies(self.home / 'nowhere'), [])
if __name__ == '__main__':
    unittest.main(verbosity=2)
