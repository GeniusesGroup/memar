#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for `memar`'s routing.

    python bundles/memar_adaptor/cli/tests/memar.py

The subject is the `memar` launcher, named for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the module that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here runs a verb's work or writes to the machine. The contract is
pinned with fake services handed to `assemble`, because a test that ran a real
tool to learn how the router composes would be testing that tool instead; what
the real services declare is reached only through `--help` and usage errors,
which do no work, and each child launcher is a test run, so the daily update's
hook does nothing in it.

What is pinned, and what each pin is for:

  ContractComposes    A domain module's verb becomes a `memar` verb and a
                      capability module's verb a sub-verb under it, each with
                      its summary in the parent's list and its overview in its
                      own --help, under a usage argparse names itself. A
                      domain's run runs before its sub-verb's, so what every
                      verb of a domain owes is said once, and a non-zero status
                      stops the chain. A module that registers nothing and
                      returns a callable runs before every verb, --help too,
                      given the arguments as typed. A module without
                      `describe` is no part of the command line. A module that
                      fails to import is named on stderr and left out, and
                      every other verb, --help included, still answers.
  DomainsFirst        The shelf is read domain modules first, then
                      capabilities, each alphabetically, `_`-prefixed files
                      skipped: a capability's verbs go under a domain verb that
                      must already exist.
  PluggableRoot       A module standing only under `modules-plugable/` is found
                      by `catalog` and `services`, and the real shelf's command
                      module answers with the hyphen in its address.
  RouterNamesNoVerb   No verb or sub-verb word the services declare appears
                      in the router as routing data. A verb named here as well
                      as in its service would be a second interface for one
                      behavior, and the two would drift.
  HelpListsTheServices
                      `memar --help` lists exactly the verbs the real services
                      declare, each with the summary it declared.
  HelpStatesItsOwnWork
                      No real verb's overview carries a command line of its
                      own sub-verbs: each help states its own work, and a
                      sub-verb's is reached through that sub-verb's --help,
                      which argparse's list of verbs leads to (owner,
                      2026-10-14).
  EveryHelpAnswers    Every real verb's and sub-verb's --help exits 0 through
                      the launcher, under its own `memar` usage, so a caller
                      can always read the interface of what they are about to
                      run.
  UsageErrorsExit2    `memar` alone, an unknown verb, and a domain verb without
                      the sub-verb it needs exit 2 with a usage line. A caller
                      who typed one word has asked for nothing, and guessing on
                      their behalf would run something.
  HelpWordIsHelp      `memar help` prints exactly what `memar --help` prints:
                      one help, two spellings a person types.
  HelpCarriesMemarNotTheRouter
                      `memar --help` says what Memar is, points at
                      `memar_commands` for the full call list, and carries none
                      of the router's mechanism, which is pinned to the
                      docstring the implementer reads; help that explains the
                      implementation is a non-answer printed confidently.
  NoShelfCmdShim       The Windows shelf `memar.cmd` is gone; PATH uses `bin/memar.cmd`.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
from importlib import import_module
import concurrent.futures
import argparse
import ast
import contextlib
import importlib.util
import io
import os
import re
import subprocess
import sys
import types
import unittest
import unittest.mock
from importlib.machinery import SourceFileLoader
from pathlib import Path
TESTS = Path(__file__).resolve().parent
FACE = TESTS.parent
TOP = FACE.parent.parent.parent
SERVER = TOP / 'bundles' / 'memar'
SCRIPTS = FACE
for folder in (TOP, FACE, SERVER, SERVER / 'services'):
    sys.path.insert(0, str(folder))
sys.dont_write_bytecode = True
LAUNCHER = FACE / 'memar'
SHIM = FACE / 'memar.cmd'  # must stay absent; PATH uses bin/memar.cmd
memar = importlib.import_module('bundles.memar_adaptor.cli.router')

def subparsers(parser: argparse.ArgumentParser) -> argparse._SubParsersAction | None:
    return next((action for action in parser._actions if isinstance(action, argparse._SubParsersAction)), None)

def declared() -> dict[tuple[str, ...], str]:
    """Every public call name the real services declare, with its one-line summary."""
    top, _ = memar.assemble(memar.services())
    found: dict[tuple[str, ...], str] = {}
    group = subparsers(top)
    assert group is not None
    summaries = {action.dest: action.help for action in group._choices_actions}
    for name, child in group.choices.items():
        if name not in summaries or summaries[name] == argparse.SUPPRESS:
            continue
        found[(name,)] = summaries.get(name, '')
        assert subparsers(child) is None, f'public call {name!r} has a group'
    return found

def launch(*arguments: str, command: list[str] | None=None) -> subprocess.CompletedProcess:
    return subprocess.run([*(command or [sys.executable, str(LAUNCHER)]), *arguments], capture_output=True, env=dict(os.environ, COLUMNS='1000', MEMAR_SERVER='0', PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1'))

def flat(text: bytes | str) -> str:
    return ' '.join((text.decode('utf-8') if isinstance(text, bytes) else text).split())

BUDGET_SECONDS = 10

class FakeShelf:
    """Services as the contract describes them, recording what runs."""
    NAMES = ['alpha', 'gamma', 'alpha_beta', 'alpha_hook', 'alpha_plain']

    def __init__(self) -> None:
        self.calls: list[tuple] = []
        self.status = {'alpha': None, 'beta': None, 'gamma': None}
        self.modules = {'alpha': types.SimpleNamespace(describe=self.describe_alpha), 'gamma': types.SimpleNamespace(describe=self.describe_gamma), 'alpha_beta': types.SimpleNamespace(describe=self.describe_beta), 'alpha_hook': types.SimpleNamespace(describe=self.describe_hook), 'alpha_plain': types.SimpleNamespace()}

    def describe_alpha(self, verbs):
        parser = verbs.add_parser('alpha', help='the alpha summary', description='the alpha overview')
        parser.add_argument('--loud', action='store_true')
        return lambda args: self.ran('alpha', args.loud)

    def describe_gamma(self, verbs):
        verbs.add_parser('gamma', help='the gamma summary', description='the gamma overview')
        return lambda args: self.ran('gamma')

    def describe_beta(self, verbs):
        parser = verbs.add_parser('beta', help='the beta summary', description='the beta overview')
        parser.add_argument('word')
        return lambda args: self.ran('beta', args.word)

    def describe_hook(self, verbs):
        return lambda argv: self.calls.append(('hook', list(argv)))

    def ran(self, name: str, *seen) -> int | None:
        self.calls.append((name, *seen))
        return self.status[name]

    def assemble(self, names=None):
        return memar._assemble_legacy(self.NAMES if names is None else names, load=self.modules.__getitem__, domain=self.domain)

    @staticmethod
    def domain(name):
        return name.partition('_')[0] if '_' in name else None

    def main(self, argv: list[str]) -> tuple[int, str, str]:
        """`memar.main` over this shelf: its status, stdout, and stderr; SystemExit's code when it exits."""
        out, err = (io.StringIO(), io.StringIO())
        with contextlib.ExitStack() as stack:
            stack.enter_context(unittest.mock.patch.object(memar, 'services', lambda: list(self.NAMES)))
            original = memar._assemble_legacy
            stack.enter_context(unittest.mock.patch.object(memar, 'assemble', lambda names: original(names, load=self.modules.__getitem__, domain=self.domain)))
            stack.enter_context(contextlib.redirect_stdout(out))
            stack.enter_context(contextlib.redirect_stderr(err))
            try:
                code = memar.main(argv)
            except SystemExit as exited:
                code = exited.code or 0
        return (code, out.getvalue(), err.getvalue())

class ContractComposes(unittest.TestCase):

    def setUp(self) -> None:
        self.shelf = FakeShelf()

    def test_a_domain_verb_and_its_sub_verb_are_declared(self) -> None:
        top, before = self.shelf.assemble()
        self.assertEqual(set(subparsers(top).choices), {'alpha', 'gamma'})
        alpha = subparsers(top).choices['alpha']
        self.assertEqual(set(subparsers(alpha).choices), {'beta'})
        self.assertEqual(len(before), 1)

    def test_summaries_list_and_overviews_answer_under_argparses_own_usage(self) -> None:
        code, out, _ = self.shelf.main(['--help'])
        self.assertEqual(code, 0)
        self.assertIn('the alpha summary', out)
        self.assertIn('the gamma summary', out)
        code, out, _ = self.shelf.main(['alpha', '--help'])
        self.assertEqual(code, 0)
        self.assertIn('usage: memar alpha', out)
        self.assertIn('the alpha overview', out)
        self.assertIn('the beta summary', out)
        code, out, _ = self.shelf.main(['alpha', 'beta', '--help'])
        self.assertEqual(code, 0)
        self.assertIn('usage: memar alpha beta', out)
        self.assertIn('the beta overview', out)

    def test_the_domains_run_runs_before_its_sub_verbs(self) -> None:
        code, _, _ = self.shelf.main(['alpha', '--loud', 'beta', 'word'])
        self.assertEqual(code, 0)
        self.assertEqual(self.shelf.calls, [('hook', ['alpha', '--loud', 'beta', 'word']), ('alpha', True), ('beta', 'word')])

    def test_a_non_zero_status_stops_the_chain(self) -> None:
        self.shelf.status['alpha'] = 3
        code, _, _ = self.shelf.main(['alpha', 'beta', 'word'])
        self.assertEqual(code, 3)
        self.assertNotIn('beta', [call[0] for call in self.shelf.calls])
        self.shelf.status.update(alpha=None, beta=5)
        self.assertEqual(self.shelf.main(['alpha', 'beta', 'word'])[0], 5)

    def test_a_domain_verb_with_no_sub_verbs_runs_itself(self) -> None:
        self.assertEqual(self.shelf.main(['gamma'])[0], 0)
        self.assertEqual(self.shelf.calls[-1], ('gamma',))

    def test_a_module_registering_nothing_runs_before_every_verb_help_too(self) -> None:
        for argv in (['--help'], ['help'], ['gamma'], ['alpha', 'beta', '--help']):
            with self.subTest(argv=argv):
                self.shelf.calls.clear()
                self.shelf.main(argv)
                self.assertEqual(self.shelf.calls[0], ('hook', argv))

    def test_a_module_without_describe_is_no_part_of_the_command_line(self) -> None:
        with_plain = self.shelf.assemble(['alpha', 'alpha_plain'])
        without = self.shelf.assemble(['alpha'])
        self.assertEqual(with_plain[1], without[1])
        self.assertEqual(with_plain[0].format_help(), without[0].format_help())

    def test_a_module_that_fails_to_import_is_named_and_the_rest_still_answer(self) -> None:
        modules = self.shelf.modules

        class Broken(dict):

            def __getitem__(self, name):
                if name == 'gamma':
                    raise SyntaxError('broken on purpose')
                return modules[name]
        self.shelf.modules = Broken()
        code, out, err = self.shelf.main(['--help'])
        self.assertEqual(code, 0)
        self.assertIn('the alpha summary', out)
        self.assertNotIn('the gamma summary', out)
        self.assertIn('memar: gamma did not load', err)
        self.assertIn('broken on purpose', err)
        code, _, _ = self.shelf.main(['alpha', 'beta', 'word'])
        self.assertEqual(code, 0)
        self.assertIn(('beta', 'word'), self.shelf.calls)

    def test_a_domain_verb_missing_its_sub_verb_is_a_usage_error(self) -> None:
        code, _, err = self.shelf.main(['alpha'])
        self.assertEqual(code, 2)
        self.assertIn('usage: memar alpha', err)
        self.assertNotIn(('alpha', False), self.shelf.calls)

class DomainsFirst(unittest.TestCase):

    def test_domains_come_before_capabilities_and_private_files_are_skipped(self) -> None:
        base = 'modules/group'
        names = ['modules.group.zeta.services.a', 'modules.group.alpha.services.beta', 'modules.group.alpha.alpha', 'modules.group.zeta.zeta', 'modules.group.alpha.services.aa', 'modules.group.alpha.services._shared', 'modules.group.alpha.tests.alpha', 'modules.group.alpha.errors.errors', 'modules.group.plain.other']
        self.assertEqual(memar.services(names), [f'{base}/alpha', f'{base}/zeta', f'{base}/alpha/services/aa', f'{base}/alpha/services/beta', f'{base}/zeta/services/a'])
        found = memar.catalog(names)
        self.assertEqual(found[f'{base}/alpha/services/beta'], 'modules.group.alpha.services.beta')
        self.assertEqual(found[f'{base}/zeta'], 'modules.group.zeta.zeta')
        self.assertNotIn(f'{base}/plain', found)
        self.assertEqual(memar.domain_of(f'{base}/alpha/services/beta', names), f'{base}/alpha')

    def test_a_capability_file_named_by_another_domain_is_that_domains(self) -> None:
        names = ['modules.alpha.alpha', 'modules.alpha.services.beta_one', 'modules.alpha.services.two', 'modules.beta.beta']
        found = memar.catalog(names)
        self.assertEqual(found['modules/alpha/services/beta_one'], 'modules.alpha.services.beta_one')
        self.assertEqual(memar.domain_of('modules/alpha/services/beta_one', names), 'modules/beta')
        self.assertEqual(memar.domain_of('modules/alpha/services/two', names), 'modules/alpha')
        self.assertEqual(len(found), 4)

    def test_the_real_shelf_is_read_the_same_way(self) -> None:
        names = memar.services()
        domains = [name for name in names if memar.domain_of(name) is None]
        self.assertEqual(names[:len(domains)], domains)
        self.assertEqual(domains, sorted(domains, key=lambda key: (Path(key).name, key)))

    def test_a_nested_module_and_its_mirror_with_one_leaf_are_two_domains(self) -> None:
        names = ['modules.computer.store.git.git', 'modules-plugable.computer.store.git.git', 'modules-plugable.other.other', 'modules-plugable.other.services.git_note', 'modules-plugable.computer.store.git.services.pull']
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            left_out = memar.catalog(names)
        self.assertIn('more than one domain', err.getvalue())
        self.assertNotIn('modules-plugable/other/services/git_note', left_out)
        kept = names[:3] + names[4:]
        found = memar.catalog(kept)
        self.assertEqual(found['modules/computer/store/git'], 'modules.computer.store.git.git')
        self.assertEqual(found['modules-plugable/computer/store/git'], 'modules-plugable.computer.store.git.git')
        self.assertEqual(memar.domain_of('modules-plugable/computer/store/git/services/pull', kept), 'modules-plugable/computer/store/git')

    def test_a_capability_beginning_with_its_own_mirrors_word_stays_in_its_folder(self) -> None:
        names = ['modules.c.disk.disk', 'modules-plugable.c.disk.disk', 'modules.c.disk.services.disk_x']
        self.assertEqual(memar.domain_of('modules/c/disk/services/disk_x', names), 'modules/c/disk')

    def test_a_verb_two_modules_declare_is_named_and_left_out(self) -> None:
        shelf = FakeShelf()
        shelf.modules['alpha_dup'] = types.SimpleNamespace(describe=lambda verbs: verbs.add_parser('beta', help='again'))
        out = io.StringIO()
        with contextlib.redirect_stderr(out):
            top, _ = shelf.assemble(['alpha', 'alpha_beta', 'alpha_dup'])
        self.assertIn('memar: alpha_dup could not declare its verb', out.getvalue())

    def test_a_name_outside_the_roots_or_inside_a_folder_that_is_no_module_is_no_entry(self) -> None:
        names = ['mcp.mcp', 'machine.resident', 'modules.a.services.services', 'modules.a.node_modules.node_modules', 'modules.a.a', 'modules.a.services.x.y']
        self.assertEqual(sorted(memar.catalog(names)), ['modules/a'])

    def test_the_shelf_spelled_short_and_long_is_one_entry(self) -> None:
        names = ['bundles.memar.services.mcp.mcp', 'mcp.mcp', 'bundles.memar.services.mcp.services.serve', 'mcp.services.serve']
        self.assertEqual(memar.catalog(names), {'bundles/memar/services/mcp': 'bundles.memar.services.mcp.mcp', 'bundles/memar/services/mcp/services/serve': 'bundles.memar.services.mcp.services.serve'})

    def test_the_entries_the_manifest_gives_are_those_the_tree_gives(self) -> None:
        top = memar.TOP
        banned = set(memar.NOT_MODULES)
        walked = set()
        for root in ('modules', 'modules-plugable', 'bundles', 'bundles/memar/services'):
            for folder, dirs, files in os.walk(top / root):
                dirs[:] = [name for name in dirs if name not in banned]
                here = Path(folder)
                package = '.'.join(here.relative_to(top).parts)
                if f'{here.name}.py' in files:
                    walked.add(f'{package}.{here.name}')
                shelf = here / 'services'
                if shelf.is_dir():
                    for path in shelf.glob('*.py'):
                        if not path.stem.startswith('_'):
                            walked.add(f'{package}.services.{path.stem}')
                    for path in shelf.glob('*/*.py'):
                        if path.stem == path.parent.name and not path.stem.startswith('_'):
                            walked.add(f'{package}.services.{path.stem}.{path.stem}')
        # Twin domain files and the services under those twins: a service whose
        # folder has no twin is still callable (provisional Domain = folder leaf)
        # but is in the release only when the manifest names it; what the tree
        # holds beyond that is not compared here.
        def domains_and_their_services(names):
            found = memar.entries(tuple(names))
            twins = {key for key, each in found.items() if each.domain is None}
            return {
                key: address
                for key, address in memar.catalog(names).items()
                if key in twins or found[key].domain in twins
            }
        walked_map = domains_and_their_services(sorted(walked))
        declared_map = domains_and_their_services(memar.DECLARED)
        # Declared twins and their services must match the tree; extra twins on
        # disk that another chat has not yet put in the manifest are not this check.
        self.assertEqual({key: walked_map[key] for key in declared_map}, declared_map)

    def test_the_entries_read_no_folder(self) -> None:
        memar.entries.cache_clear()
        with unittest.mock.patch('os.walk', side_effect=AssertionError('walked')):
            self.assertTrue(memar.services())
        memar.entries.cache_clear()

class PluggableRoot(unittest.TestCase):

    def test_a_domain_standing_only_under_modules_plugable_is_found(self) -> None:
        names = ['modules-plugable.net.mcp.mcp']
        self.assertEqual(memar.catalog(names)['modules-plugable/net/mcp'], 'modules-plugable.net.mcp.mcp')
        self.assertIn('modules-plugable/net/mcp', memar.services(names))

    def test_the_real_shelf_reads_the_pluggable_root_the_same_way(self) -> None:
        self.assertEqual(memar.catalog()['bundles/memar_adaptor/cli/services/commands'], 'bundles.memar_adaptor.cli.services.commands')
        self.assertIn('bundles/memar_adaptor/cli/services/commands', memar.services())

class RouterNamesNoVerb(unittest.TestCase):
    """The docstring may name a service as an example of the contract; that is
    the design being explained. What must not name one is a string the router
    holds, nor a name it gives a constant or function — and a sub-verb word such
    as `list` or `path` is checked in strings only, being also Python's own. A
    name an imported module gives, such as `importlib.import_module`, is that
    module's and not the router's to choose, so it is not checked.
    """

    def test_no_declared_verb_word_is_routing_data_in_the_router(self) -> None:
        paths = declared()
        verbs = {path[0] for path in paths}
        self.assertTrue({'content_search', 'memar_install', 'task_ensure', 'memar_update'} <= verbs, verbs)
        tree = ast.parse(LAUNCHER.read_text(encoding='utf-8'))
        docstring = tree.body[0].value if isinstance(tree.body[0], ast.Expr) else None
        epilog = next(
            (
                node.value
                for node in tree.body
                if isinstance(node, ast.Assign)
                for target in node.targets
                if isinstance(target, ast.Name) and target.id == 'EPILOG'
            ),
            None,
        )
        imported = {alias.asname or alias.name.split('.')[0] for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names}
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str) and (node is not docstring) and (node is not epilog):
                dotted_import_path = re.fullmatch(r'[a-z_][a-z_0-9]*(?:\.[a-z_][a-z_0-9]*)+', node.value) is not None
                if not dotted_import_path:
                    for verb in verbs & set(re.findall(r'[a-z][a-z_0-9]*', node.value)):
                        with self.subTest(text=node.value[:40], verb=verb):
                            self.fail(f"the router's text names the verb {verb!r}")
            if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and (node.value.id in imported):
                continue
            name = getattr(node, 'id', None) or getattr(node, 'attr', None) or getattr(node, 'name', None)
            if isinstance(name, str):
                if name in verbs:
                    with self.subTest(name=name):
                        self.fail(f"the router's identifier {name!r} names a verb")

class HelpListsTheServices(unittest.TestCase):

    def test_memar_help_lists_exactly_the_declared_verbs_with_their_summaries(self) -> None:
        completed = launch('--help')
        self.assertEqual(completed.returncode, 0)
        out = completed.stdout.decode('utf-8')
        rows = re.findall(r'^ {4}(\S+)(?: {2,}([^\r\n]+)|\r?\n {24}([^\r\n]+))', out, flags=re.MULTILINE)
        listed = {name: same_line or next_line for name, same_line, next_line in rows}
        verbs = {path[0]: summary for path, summary in declared().items() if len(path) == 1}
        self.assertEqual(set(listed), set(verbs))
        for verb, summary in verbs.items():
            with self.subTest(verb=verb):
                self.assertTrue(summary)
                self.assertEqual(flat(listed[verb]), flat(summary))

class HelpStatesItsOwnWork(unittest.TestCase):

    def test_no_overview_names_a_command_line_of_its_own_sub_verbs(self) -> None:
        top, _ = memar.assemble(memar.services())
        group = subparsers(top)
        self.assertIsNotNone(group)
        self.assertTrue(group.choices)
        for name, child in group.choices.items():
            with self.subTest(command=f'memar {name}'):
                self.assertIsNone(subparsers(child), 'public calls contain one token and no group')

class EveryHelpAnswers(unittest.TestCase):

    def test_every_verb_and_sub_verb_answers_its_help(self) -> None:
        paths = list(declared())
        self.assertTrue(paths)
        self.assertTrue(all(len(path) == 1 for path in paths), paths)
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            asked = list(pool.map(lambda path: launch(*path, '--help'), paths))
        for path, completed in zip(paths, asked):
            with self.subTest(verb=' '.join(path)):
                self.assertEqual(completed.returncode, 0, completed.stderr)
                self.assertIn(f"usage: memar {' '.join(path)}", flat(completed.stdout))

class UsageErrorsExit2(unittest.TestCase):

    def assert_usage_error(self, *arguments: str) -> None:
        completed = launch(*arguments)
        self.assertEqual(completed.returncode, 2, completed.stderr)
        self.assertIn('usage: memar', flat(completed.stderr))
        self.assertEqual(completed.stdout, b'')

    def test_memar_alone_is_a_usage_error(self) -> None:
        self.assert_usage_error()

    def test_an_unknown_verb_is_a_usage_error(self) -> None:
        self.assert_usage_error('no-such-verb')

    def test_old_grouped_syntax_is_a_usage_error(self) -> None:
        self.assert_usage_error('task', 'ensure')

class HelpWordIsHelp(unittest.TestCase):

    def test_memar_help_prints_what_memar_dash_help_prints(self) -> None:
        word, flag = (launch('help'), launch('--help'))
        self.assertEqual((word.returncode, flag.returncode), (0, 0))
        self.assertEqual(word.stdout, flag.stdout)
        self.assertTrue(flag.stdout)

class HelpCarriesMemarNotTheRouter(unittest.TestCase):
    """`memar --help` is addressed to a person with Memar, not to an implementer.

    The two are different documents: the first says what the thing is and does,
    the second how it is built. The mechanism is pinned to the module docstring
    instead, which is the one text addressed to whoever opens the file.
    """
    MECHANISM = ('describe', 'services/', 'subprocess', 'argparse', 'route')

    def setUp(self) -> None:
        raw = flat(launch('--help').stdout)
        self.text = raw.split('Ask any verb with')[0]

    def test_the_help_says_what_memar_is(self) -> None:
        for phrase in ('framework', 'documents', 'memar_commands', '--help'):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.text)

    def test_the_help_does_not_carry_the_routers_implementation(self) -> None:
        for phrase in self.MECHANISM:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, self.text)

    def test_the_mechanism_is_in_the_docstring_the_implementer_reads(self) -> None:
        for phrase in ('memar_adaptor', 'routes and nothing else', 'describe(verbs)'):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, memar.__doc__)

class NoShelfCmdShim(unittest.TestCase):

    def test_the_shelf_windows_cmd_shim_is_gone(self) -> None:
        self.assertTrue(LAUNCHER.is_file())
        self.assertFalse(SHIM.exists(), 'PATH must use bin/memar.cmd; shelf memar.cmd must not return')
if __name__ == '__main__':
    unittest.main()
