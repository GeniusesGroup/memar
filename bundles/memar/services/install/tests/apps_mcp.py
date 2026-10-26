#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the MCP server's registration in agent apps, `bundles/memar/services/install/services/apps_mcp.py`.

    python bundles/memar/services/install/tests/apps_mcp.py

The subject is the registration the agent-app layer writes, per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md); its defining
record is the owner's choice of user-level registration only, in
[Memar Handoff](../../../memar/memar.handoff.md#the-mcp-adapter-is-the-servers-first-face-owner-2026-10-18).

Nothing here writes to a real agent app: the home folder is a scratch folder, and the checkout the
command names is a stand-in.

What is pinned:

  RegistersOnce     In an app that is present, its user-level setting gets Memar's entry, which
                    starts the router with `mcp serve`; what else the setting held is kept; a
                    second run finds it current and writes nothing; an app that is absent gets
                    nothing.
  DryRunWritesNone  A dry run prints each entry it would write and writes none.
  RefreshesStale    A JSON or TOML entry that still names Memar but with a stale command is
                    rewritten to the current one; JSON with comments and an unreadable setting
                    stay byte for byte as they were.
  WarnsStale        `warn_stale` names each setting whose Memar entry is not current, and nothing
                    when every one matches.
"""
from __future__ import annotations
from importlib import import_module
_m_fs_test_scratch = import_module('modules-plugable.computer.memory.filesystem.services.fs_test_scratch')
remove_tree = _m_fs_test_scratch.remove_tree
suite_scratch = _m_fs_test_scratch.suite_scratch
import contextlib
import io
import json
import os
import sys
import time
import unittest
import unittest.mock
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = next(p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()) / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS / 'services'))
sys.path.insert(1, str(SCRIPTS))
sys.path.insert(2, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
import bundles.memar.services.install.services.apps_mcp as layer

class Home(unittest.TestCase):

    def setUp(self) -> None:
        self.home = suite_scratch() / f'apps-mcp-{os.getpid()}-{time.time_ns()}'
        self.home.mkdir(parents=True)
        self.addCleanup(remove_tree, self.home)
        for patched in (unittest.mock.patch.object(Path, 'home', return_value=self.home), unittest.mock.patch.object(layer, 'resolve_root', return_value=Path('/checkout'))):
            patched.start()
            self.addCleanup(patched.stop)

    def install(self, dry_run: bool=False) -> str:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            layer.into_apps(dry_run=dry_run)
        return out.getvalue()

class RegistersOnce(Home):

    def test_present_apps_get_the_entry_once_and_keep_the_rest(self):
        (self.home / '.claude').mkdir()
        (self.home / '.codex').mkdir()
        (self.home / '.claude.json').write_text('{"theme": "dark"}', encoding='utf-8')
        (self.home / '.codex' / 'config.toml').write_text('model = "x"\n', encoding='utf-8')
        self.install()
        claude = json.loads((self.home / '.claude.json').read_text(encoding='utf-8'))
        self.assertEqual(claude['theme'], 'dark')
        entry = claude['mcpServers']['memar']
        self.assertEqual(entry['args'][-2:], ['mcp', 'serve'])
        self.assertEqual(Path(entry['args'][0]), Path('/checkout') / 'bundles' / 'memar' / 'memar')
        toml = (self.home / '.codex' / 'config.toml').read_text(encoding='utf-8')
        self.assertTrue(toml.startswith('model = "x"\n'))
        self.assertEqual(toml.count('[mcp_servers.memar]'), 1)
        self.assertFalse((self.home / '.cursor').exists())
        again = self.install()
        self.assertEqual(again.count('already current'), 2)
        self.assertEqual((self.home / '.codex' / 'config.toml').read_text(encoding='utf-8'), toml)

class DryRunWritesNone(Home):

    def test_a_dry_run_prints_and_writes_nothing(self):
        (self.home / '.cursor').mkdir()
        out = self.install(dry_run=True)
        self.assertIn('dry-run: register the MCP server in', out)
        self.assertIn('"memar"', out)
        self.assertFalse((self.home / '.cursor' / 'mcp.json').exists())

class RefreshesStale(Home):

    def test_stale_json_and_toml_are_rewritten_unreadable_left(self):
        opencode = self.home / '.config' / 'opencode'
        opencode.mkdir(parents=True)
        (opencode / 'opencode.jsonc').write_text('// mine\n{}\n', encoding='utf-8')
        (self.home / '.cursor').mkdir()
        (self.home / '.cursor' / 'mcp.json').write_text('{not json', encoding='utf-8')
        (self.home / '.codex').mkdir()
        differing = 'model = "x"\n\n[mcp_servers.memar]\ncommand = "other"\nargs = []\n'
        (self.home / '.codex' / 'config.toml').write_text(differing, encoding='utf-8')
        (self.home / '.claude').mkdir()
        (self.home / '.claude.json').write_text(json.dumps({'mcpServers': {'memar': {'command': 'old', 'args': []}}}), encoding='utf-8')
        out = self.install()
        self.assertIn('not registered', out)
        self.assertFalse((opencode / 'opencode.json').exists())
        self.assertEqual((self.home / '.cursor' / 'mcp.json').read_text(encoding='utf-8'), '{not json')
        toml = (self.home / '.codex' / 'config.toml').read_text(encoding='utf-8')
        self.assertTrue(toml.startswith('model = "x"\n'))
        self.assertIn('bundles', toml)
        self.assertNotIn('command = "other"', toml)
        claude = json.loads((self.home / '.claude.json').read_text(encoding='utf-8'))
        self.assertEqual(claude['mcpServers']['memar']['args'][-2:], ['mcp', 'serve'])

class WarnsStale(Home):

    def test_warn_stale_names_only_settings_that_differ(self):
        (self.home / '.cursor').mkdir()
        (self.home / '.cursor' / 'mcp.json').write_text(json.dumps({'mcpServers': {'memar': {'command': 'old', 'args': ['x']}}}), encoding='utf-8')
        (self.home / '.claude').mkdir()
        command = layer.server_command()
        _, _, entry = layer._claude(command)
        (self.home / '.claude.json').write_text(json.dumps({'mcpServers': {'memar': entry}}), encoding='utf-8')
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            layer.warn_stale()
        text = out.getvalue()
        self.assertIn(str(self.home / '.cursor' / 'mcp.json'), text)
        self.assertNotIn('.claude.json', text)
        self.assertEqual(layer.stale_settings(), [self.home / '.cursor' / 'mcp.json'])

if __name__ == '__main__':
    unittest.main()
