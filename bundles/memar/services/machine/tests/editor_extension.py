#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for where an editor's extensions land, in `machine/editor_extension.py`.

    python bundles/memar/services/machine/tests/editor_extension.py

The subject is the placement of an extension, per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes to the machine. The editor's extensions folder is patched
onto a scratch folder inside this one, and the checkout the extensions are read
from is a second scratch folder holding manifests written by the test; both are
removed with the temporary directories that hold them. No editor is started and
nothing under the real `~/.vscode` is read or written.

What is pinned, and what each pin is for:

  FolderNameFromManifest  The folder name is `<publisher>.<name>-<version>`
                          read from the extension's own manifest, so nothing
                          here names an extension or a version and a new
                          extension needs no edit to this module.
  RefusesAnUnnamedOne     A manifest with no publisher, name, or version names
                          no installable extension, and is refused by name
                          rather than skipped past into a silent no-op.
  SecondRunWritesOver     An installed folder is replaced, because a change in
                          the checkout that does not reach the editor is a
                          change that is not installed. The folder already
                          there is moved to the trash first, so a local edit
                          can be taken back.
  DryRunTouchesNothing    A dry run prints what it would install or refresh and
                          neither moves the installed folder to the trash nor
                          writes the checkout's copy.
  NoEditorIsSkipped       An editor folder that is not there is reported and
                          left alone, rather than created: writing into a folder
                          no editor reads leaves litter, not an extension.
  NoExtensionIsNotAFault  A checkout that ships no extension is reported, not
                          an error, because installing Memar does not require
                          an editor.
  OnlyManifestsAreTaken   Not every folder under the extensions folder is an
                          extension, so one with no manifest is passed over.
  StaleExtensionsNamed    An installed folder that is missing, or is not what
                          copying the checkout's extension would write, is
                          named and nothing is written; what a copy never
                          carries is left out, and no editor means nothing is.
                          A refresh of only what was named moves nothing that
                          is current.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
from machine.plugable_import import load as plugable_load
_m_fs_test_scratch = plugable_load('computer.memory.filesystem.services.fs_test_scratch')
suite_scratch = _m_fs_test_scratch.suite_scratch
import contextlib
import io
import json
import os
import shutil
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parent.parent
CHECKOUT = SCRIPTS.parent.parent
sys.path.insert(0, str(SCRIPTS))
sys.dont_write_bytecode = True
import machine.editor_extension as extension

class Fixture(unittest.TestCase):
    """A checkout that ships one extension, and an editor folder to copy it into."""

    def setUp(self) -> None:
        self.notes = io.StringIO()
        self.checkout = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.checkout.cleanup)
        self.checkout_root = Path(self.checkout.name)
        self.editor = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.editor.cleanup)
        self.editor_root = Path(self.editor.name)
        self.sources = self.checkout_root / extension.EXTENSIONS_RELATIVE
        self.sources.mkdir(parents=True)
        patch = unittest.mock.patch.object(extension, 'editor_extensions_dir', lambda: self.editor_root)
        self.addCleanup(patch.stop)
        patch.start()
        printer = unittest.mock.patch('builtins.print', self.notes.write)
        self.addCleanup(printer.stop)
        printer.start()

        def _aside(path: Path) -> None:
            shutil.rmtree(path)
        trash = unittest.mock.patch.object(extension, 'soft_delete', side_effect=_aside)
        self.addCleanup(trash.stop)
        trash.start()

    def add_extension(self, folder: str, **fields: object) -> Path:
        """Write one extension manifest into the checkout and return its folder."""
        source = self.sources / folder
        source.mkdir(parents=True, exist_ok=True)
        manifest = {'publisher': fields.get('publisher', 'Memar'), 'name': fields.get('name', folder), 'version': fields.get('version', '1.0.0'), 'main': './extension.js'}
        for absent in (key for key, value in fields.items() if value is None):
            del manifest[absent]
        (source / extension.MANIFEST_NAME).write_text(json.dumps(manifest), encoding='utf-8')
        return source

    def said(self, fragment: str) -> bool:
        return fragment in self.notes.getvalue()

class FolderNameFromManifest(unittest.TestCase):
    """The editor's own name for the folder, read rather than written here."""

    def test_the_publisher_name_and_version_make_the_folder_name(self) -> None:
        with tempfile.TemporaryDirectory(dir=suite_scratch()) as scratch:
            manifest = Path(scratch) / extension.MANIFEST_NAME
            manifest.write_text(json.dumps({'publisher': 'Memar', 'name': 'khayyam', 'version': '2.1.0'}), encoding='utf-8')
            self.assertEqual(extension.extension_folder_name(manifest), 'memar.khayyam-2.1.0')

    def test_a_publisher_with_dots_loses_them(self) -> None:
        with tempfile.TemporaryDirectory(dir=suite_scratch()) as scratch:
            manifest = Path(scratch) / extension.MANIFEST_NAME
            manifest.write_text(json.dumps({'publisher': 'Memar.Foundation', 'name': 'khayyam', 'version': '1.0.0'}), encoding='utf-8')
            self.assertEqual(extension.extension_folder_name(manifest), 'memarfoundation.khayyam-1.0.0')

class RefusesAnUnnamedOne(Fixture):
    """A manifest that names no installable extension is said so, by field."""

    def test_each_missing_field_is_refused_by_its_own_name(self) -> None:
        with tempfile.TemporaryDirectory(dir=suite_scratch()) as scratch:
            manifest = Path(scratch) / extension.MANIFEST_NAME
            for absent in ('publisher', 'name', 'version'):
                fields = {'publisher': 'Memar', 'name': 'khayyam', 'version': '1.0.0'}
                del fields[absent]
                manifest.write_text(json.dumps(fields), encoding='utf-8')
                with self.subTest(absent=absent):
                    with self.assertRaises(SystemExit) as raised:
                        extension.extension_folder_name(manifest)
                    self.assertIn(absent, str(raised.exception))

    def test_a_manifest_that_is_not_json_is_refused_with_the_reason(self) -> None:
        with tempfile.TemporaryDirectory(dir=suite_scratch()) as scratch:
            manifest = Path(scratch) / extension.MANIFEST_NAME
            manifest.write_text('{not json', encoding='utf-8')
            with self.assertRaises(SystemExit) as raised:
                extension.extension_folder_name(manifest)
            self.assertIn(str(manifest), str(raised.exception))

class SecondRunWritesOver(Fixture):
    """The installed folder is the installer's own copy, so it is refreshed."""

    def test_the_installed_file_becomes_the_checkouts(self) -> None:
        self.add_extension('khayyam')
        (self.sources / 'khayyam' / 'rules.txt').write_text('first', encoding='utf-8')
        extension.install_extensions(self.checkout_root)
        installed = self.editor_root / 'memar.khayyam-1.0.0'
        self.assertEqual((installed / 'rules.txt').read_text(encoding='utf-8'), 'first')
        (self.sources / 'khayyam' / 'rules.txt').write_text('second', encoding='utf-8')
        extension.install_extensions(self.checkout_root)
        self.assertEqual((installed / 'rules.txt').read_text(encoding='utf-8'), 'second')
        self.assertTrue(self.said('memar.khayyam-1.0.0 refreshed'))

    def test_the_first_run_says_installed_and_the_second_says_refreshed(self) -> None:
        self.add_extension('khayyam')
        extension.install_extensions(self.checkout_root)
        self.assertTrue(self.said('memar.khayyam-1.0.0 installed'))
        self.assertFalse(self.said('refreshed'))
        extension.install_extensions(self.checkout_root)
        self.assertTrue(self.said('refreshed'))

    def test_a_second_run_moves_the_installed_folder_to_the_trash(self) -> None:
        self.add_extension('khayyam')
        extension.install_extensions(self.checkout_root)
        installed = self.editor_root / 'memar.khayyam-1.0.0'
        with unittest.mock.patch.object(extension, 'soft_delete', side_effect=shutil.rmtree) as trash:
            extension.install_extensions(self.checkout_root)
        trash.assert_called_once_with(installed)
        source = Path(extension.__file__).read_text(encoding='utf-8')
        self.assertNotIn('rmtree', source)
        self.assertNotIn('unlink(', source)
        self.assertIn('soft_delete', source)

class DryRunTouchesNothing(Fixture):
    """A dry run says what it would do to the editor and does neither the trash nor the copy."""

    def test_a_dry_run_over_an_installed_folder_trashes_and_writes_nothing(self) -> None:
        self.add_extension('khayyam')
        extension.install_extensions(self.checkout_root)
        installed = self.editor_root / 'memar.khayyam-1.0.0'
        (self.sources / 'khayyam' / 'rules.txt').write_text('new', encoding='utf-8')
        with unittest.mock.patch.object(extension, 'soft_delete') as trash:
            extension.install_extensions(self.checkout_root, dry_run=True)
        trash.assert_not_called()
        self.assertFalse((installed / 'rules.txt').exists())
        self.assertTrue(self.said('dry-run: refresh'))
        self.assertFalse(self.said('refreshed'))

    def test_a_dry_run_with_nothing_installed_creates_nothing(self) -> None:
        self.add_extension('khayyam')
        extension.install_extensions(self.checkout_root, dry_run=True)
        self.assertEqual(list(self.editor_root.iterdir()), [])
        self.assertTrue(self.said('dry-run: install'))

class NoEditorIsSkipped(Fixture):
    """An editor that is not installed leaves no folder behind."""

    def test_the_editor_folder_is_not_created(self) -> None:
        self.add_extension('khayyam')
        missing = self.editor_root / 'no-editor-here'
        with unittest.mock.patch.object(extension, 'editor_extensions_dir', lambda: missing):
            extension.install_extensions(self.checkout_root)
        self.assertFalse(missing.exists())
        self.assertTrue(self.said('no editor on this machine'))

class NoExtensionIsNotAFault(Fixture):
    """Installing Memar does not require shipping an editor extension."""

    def test_a_checkout_without_the_folder_is_reported_not_raised(self) -> None:
        without = self.checkout_root / 'elsewhere'
        without.mkdir()
        extension.install_extensions(without)
        self.assertTrue(self.said('no editor extension to install'))

    def test_an_empty_extensions_folder_installs_nothing(self) -> None:
        extension.install_extensions(self.checkout_root)
        self.assertEqual(list(self.editor_root.iterdir()), [])

class OnlyManifestsAreTaken(Fixture):
    """Not every folder under the extensions folder is an extension."""

    def test_a_folder_with_no_manifest_is_passed_over(self) -> None:
        self.add_extension('khayyam')
        (self.sources / 'notes').mkdir()
        extension.install_extensions(self.checkout_root)
        self.assertEqual(sorted((path.name for path in self.editor_root.iterdir())), ['memar.khayyam-1.0.0'])

class StaleExtensionsNamed(Fixture):
    """An installed extension that is missing or no longer what copying would write is named; nothing is written."""

    def test_a_fresh_install_is_current(self) -> None:
        self.add_extension('khayyam')
        extension.install_extensions(self.checkout_root)
        self.assertEqual(extension.stale_extensions(self.checkout_root), [])

    def test_a_change_in_the_checkout_makes_the_installed_folder_stale(self) -> None:
        source = self.add_extension('khayyam')
        extension.install_extensions(self.checkout_root)
        (source / 'extension.js').write_text('moved on\n', encoding='utf-8')
        installed = self.editor_root / 'memar.khayyam-1.0.0'
        self.assertEqual(extension.stale_extensions(self.checkout_root), [installed])
        self.assertFalse((installed / 'extension.js').exists())

    def test_a_version_not_installed_yet_is_stale(self) -> None:
        self.add_extension('khayyam')
        extension.install_extensions(self.checkout_root)
        self.add_extension('khayyam', version='1.0.1')
        self.assertEqual(extension.stale_extensions(self.checkout_root), [self.editor_root / 'memar.khayyam-1.0.1'])

    def test_what_a_copy_never_carries_is_left_out(self) -> None:
        source = self.add_extension('khayyam')
        extension.install_extensions(self.checkout_root)
        (source / 'node_modules').mkdir()
        (source / 'node_modules' / 'dep.js').write_text('dev only\n', encoding='utf-8')
        self.assertEqual(extension.stale_extensions(self.checkout_root), [])

    def test_no_editor_means_nothing_is_stale(self) -> None:
        self.add_extension('khayyam')
        with unittest.mock.patch.object(extension, 'editor_extensions_dir', lambda: self.editor_root / 'absent'):
            self.assertEqual(extension.stale_extensions(self.checkout_root), [])

    def test_a_refresh_of_what_is_stale_moves_nothing_that_is_current(self) -> None:
        self.add_extension('khayyam')
        changed = self.add_extension('display')
        extension.install_extensions(self.checkout_root)
        (changed / 'extension.js').write_text('moved on\n', encoding='utf-8')
        stale = extension.stale_extensions(self.checkout_root)
        self.assertEqual(stale, [self.editor_root / 'memar.display-1.0.0'])
        with unittest.mock.patch.object(extension, 'soft_delete', side_effect=shutil.rmtree) as trash:
            extension.install_extensions(self.checkout_root, only=stale)
        trash.assert_called_once_with(stale[0])
        self.assertEqual(extension.stale_extensions(self.checkout_root), [])
if __name__ == '__main__':
    unittest.main(verbosity=2)
