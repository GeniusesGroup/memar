#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for making a module's role folders in `modules-plugable/knowledge/module-skeleton/services/module_ensure_folders.py`.

    MEMAR_SERVER=0 PYTHONPATH="<checkout>/bundles/memar/services;<checkout>" python modules-plugable/knowledge/module-skeleton/tests/module_ensure_folders.py

The subject is `memar module ensure-folders` and the role list it makes, named
for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the module that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).
The domain verb, `modules/computer/module/module.py`, only groups it, so its help is pinned
here too. The module is pluggable, and nothing under `modules/` imports it
(`bundles/memar/tests/module_graph.py` fails if one does).

Nothing here writes outside its scratch folder: each folder the roles are made
in is made under the folder `modules-plugable/computer/memory/filesystem/services/fs_test_scratch.py` names, and removed
again. `modules/README.md` is read, never written. The subprocesses run ask
for `--help` only, which writes nothing.

What is pinned, and what each pin is for:

  RolesMatchTheReadme  The role names are the ones `modules/README.md` lists in
                       its bullet "By role inside a module", which points at
                       `module_ensure_folders.py` for what each role holds;
                       a role added there and not here, or here and not there,
                       fails. Only the bare `name/` paths of the sentence that
                       lists the roles are read, so `services/<name>/`, the
                       padded and singular names the bullet warns against, and
                       modules such as `process/test/` are not taken for roles.
                       Every role carries what it holds and what it does not,
                       and the README retypes neither: a description is in the
                       code once.
  MakesOnlyWhatIsMissing
                       Each missing role folder is made, one already there is
                       left with what is in it, nothing is deleted or renamed,
                       and a file standing in a role's place is reported and
                       left.
  CommandSaysWhatItDid `memar module ensure-folders PATH` makes them in PATH,
                       prints what it made and what was already there, and
                       refuses a PATH that is not a folder, and no PATH: the
                       current folder is never read.
  TempIsTheMachines    The `temp` role takes its name from `modules-plugable/computer/memory/filesystem/services/fs_memar.py`,
                       which spells it once, and the task's sentence on
                       temporary files takes it from there too.
  ToolsReadTheProfile  `fs_memar.role_folders()`, which the router and
                       the module-graph test skip by, gives this enum's names,
                       and `fs_memar.MODULE_SKELETON` names this service.
  HelpDeclaresIt       `memar module --help` says where what each role folder
                       holds is printed, and carries no command line of
                       `ensure-folders`; `memar module ensure-folders --help`
                       names the role folders it makes and prints, by calling
                       the enum, what each holds and what it does not.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
from importlib import import_module
_m_fs_test_scratch = import_module('modules-plugable.computer.memory.filesystem.services.fs_test_scratch')
suite_scratch = _m_fs_test_scratch.suite_scratch
_m_fs_memar = import_module('modules-plugable.computer.memory.filesystem.services.fs_memar')
memar_fs = _m_fs_memar
import contextlib
import importlib.util
import io
import os
import re
import subprocess
import sys
import tempfile
import unittest
import unittest.mock
from importlib.machinery import SourceFileLoader
from pathlib import Path
TESTS = Path(__file__).resolve().parent
TOP = next(p for p in TESTS.parents if p.name == 'modules-plugable').parent
SCRIPTS = TOP / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS / 'services'))
sys.path.insert(1, str(SCRIPTS))
sys.path.insert(2, str(TOP))
sys.dont_write_bytecode = True
ensure_folders = import_module(memar_fs.MODULE_SKELETON)
LAUNCHER = SCRIPTS / 'memar'
MODULES_README = TOP / 'modules' / 'README.md'
SPELLED_TEMP = re.compile('TEMP_FOLDER\\s*=\\s*[\'"]')
ROLE_BULLET = '- **By role inside a module**'
ROLES_START = 'The roles in use are'
ROLES_END = 'The list is not closed'
BARE_ROLE = re.compile('^[a-z][a-z0-9-]*/$')
_spec = importlib.util.spec_from_loader('memar_launcher', SourceFileLoader('memar_launcher', str(LAUNCHER)))
launcher = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(launcher)
MODULE_SERVICES = launcher.services_of('module')

def readme_roles() -> list[str]:
    """The bare role names the roles sentence of the README's bullet lists, in order."""
    lines = [line for line in MODULES_README.read_text(encoding='utf-8').splitlines() if line.startswith(ROLE_BULLET)]
    assert len(lines) == 1, f'{MODULES_README} has {len(lines)} bullets starting {ROLE_BULLET!r}'
    sentence = lines[0].partition(ROLES_START)[2].partition(ROLES_END)[0]
    assert sentence, f'the bullet no longer says {ROLES_START!r} ... {ROLES_END!r}'
    return [path[:-1] for path in re.findall('`([^`]+)`', sentence) if BARE_ROLE.match(path)]

def command(*arguments: str) -> tuple[int, str]:
    """`memar module ARGUMENTS`, assembled from the module services alone, and what it printed."""
    out = io.StringIO()
    with unittest.mock.patch.object(launcher, 'services', return_value=MODULE_SERVICES), contextlib.redirect_stdout(out):
        code = launcher.main(['module', *arguments])
    return (code, out.getvalue())

def run_help(*arguments: str) -> str:
    environment = dict(os.environ, COLUMNS='80', PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1')
    completed = subprocess.run([sys.executable, str(LAUNCHER), 'module', *arguments, '--help'], capture_output=True, env=environment)
    assert completed.returncode == 0, completed.stderr
    return ' '.join(completed.stdout.decode('utf-8').split())

class Fixture(unittest.TestCase):

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.folder = Path(self.scratch.name)

class RolesMatchTheReadme(unittest.TestCase):

    def test_the_roles_are_the_ones_the_readme_lists(self) -> None:
        self.assertEqual(readme_roles(), list(ensure_folders.ROLE_FOLDERS))
        self.assertEqual(list(ensure_folders.ROLE_FOLDERS), [role.folder for role in ensure_folders.Role])

    def test_primitive_is_a_role_singular_like_protocol(self) -> None:
        self.assertIn('primitive', ensure_folders.ROLE_FOLDERS)
        self.assertNotIn('primitives', ensure_folders.ROLE_FOLDERS)
        self.assertNotIn('capsules', ensure_folders.ROLE_FOLDERS)

    def test_every_role_says_what_it_holds_and_what_it_does_not(self) -> None:
        for role in ensure_folders.Role:
            with self.subTest(role=role.folder):
                self.assertGreater(len(role.holds.split()), 5)
                self.assertGreater(len(role.holds_not.split()), 2)

    def test_the_readme_points_at_the_code_and_retypes_no_description(self) -> None:
        bullet = next((line for line in MODULES_README.read_text(encoding='utf-8').splitlines() if line.startswith(ROLE_BULLET)))
        self.assertIn('module-skeleton/services/module_ensure_folders.py', bullet)
        flat = ' '.join(bullet.split())
        for role in ensure_folders.Role:
            with self.subTest(role=role.folder):
                self.assertNotIn(' '.join(role.holds.split()), flat)
                self.assertNotIn(' '.join(role.holds_not.split()), flat)

    def test_the_enum_says_it_owns_the_descriptions(self) -> None:
        said = ensure_folders.Role.__doc__ or ''
        self.assertIn('modules/README.md', said)
        self.assertIn('the list is open', said)

class TempIsTheMachines(unittest.TestCase):

    def test_temp_is_a_role_and_its_name_is_defined_once(self) -> None:
        self.assertEqual(memar_fs.TEMP_FOLDER, 'temp')
        self.assertIs(ensure_folders.Role.TEMP.folder, memar_fs.TEMP_FOLDER)
        self.assertNotRegex(Path(ensure_folders.__file__).read_text(encoding='utf-8'), SPELLED_TEMP)
        import modules.management.task.services.temp as task_temp
        self.assertIs(task_temp.TEMP_FOLDER, memar_fs.TEMP_FOLDER)
        source = Path(task_temp.__file__).read_text(encoding='utf-8')
        self.assertNotRegex(source, SPELLED_TEMP)
        self.assertNotIn('"temp"', source)

class ToolsReadTheProfile(unittest.TestCase):

    def test_the_tools_skip_by_the_names_this_enum_declares(self) -> None:
        self.assertEqual(memar_fs.role_folders(), ensure_folders.ROLE_FOLDERS)
        self.assertTrue(set(ensure_folders.ROLE_FOLDERS) <= launcher.NOT_MODULES)

    def test_the_filesystem_service_names_this_service(self) -> None:
        self.assertEqual(Path(ensure_folders.__file__).resolve(), (TESTS.parent / 'services' / 'module_ensure_folders.py').resolve())

class MakesOnlyWhatIsMissing(Fixture):

    def test_each_missing_role_folder_is_made_and_one_there_is_left_with_its_contents(self) -> None:
        (self.folder / 'rules').mkdir()
        (self.folder / 'rules' / 'kept.md').write_text('# Kept\n', encoding='utf-8', newline='\n')
        (self.folder / 'test').mkdir()
        done = ensure_folders.ensure_role_folders(self.folder)
        self.assertEqual(done.present, ['rules'])
        self.assertEqual(done.made, [role for role in ensure_folders.ROLE_FOLDERS if role != 'rules'])
        self.assertEqual(done.blocked, [])
        self.assertTrue((self.folder / 'rules' / 'kept.md').is_file())
        self.assertTrue((self.folder / 'test').is_dir())
        again = ensure_folders.ensure_role_folders(self.folder)
        self.assertEqual((again.made, again.present), ([], list(ensure_folders.ROLE_FOLDERS)))

    def test_a_file_in_a_roles_place_is_reported_and_left(self) -> None:
        (self.folder / 'docs').write_text('not a folder\n', encoding='utf-8', newline='\n')
        done = ensure_folders.ensure_role_folders(self.folder)
        self.assertEqual(done.blocked, ['docs'])
        self.assertEqual((self.folder / 'docs').read_text(encoding='utf-8'), 'not a folder\n')

class CommandSaysWhatItDid(Fixture):

    def test_path_given_makes_them_there_and_says_what_was_made_and_there(self) -> None:
        (self.folder / 'tests').mkdir()
        code, printed = command(ensure_folders.FOLDERS_COMMAND, str(self.folder))
        self.assertEqual(code, 0)
        self.assertIn('made: protocol/, primitive/, rules/, errors/, services/, docs/, temp/', printed)
        self.assertIn('already there: tests/', printed)
        _, printed = command(ensure_folders.FOLDERS_COMMAND, str(self.folder))
        self.assertNotIn('made:', printed)
        self.assertIn('already there: protocol/, primitive/, rules/, errors/, tests/, services/, docs/, temp/', printed)

    def test_no_path_is_refused_and_the_current_folder_is_never_read(self) -> None:
        with contextlib.chdir(self.folder), contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                command(ensure_folders.FOLDERS_COMMAND)
        self.assertEqual(list(self.folder.iterdir()), [])

    def test_a_path_that_is_not_a_folder_is_refused(self) -> None:
        with self.assertRaises(SystemExit):
            command(ensure_folders.FOLDERS_COMMAND, str(self.folder / 'absent'))
        self.assertFalse((self.folder / 'absent').exists())

    def test_a_file_in_the_way_is_a_non_zero_status(self) -> None:
        (self.folder / 'errors').write_text('', encoding='utf-8')
        code, printed = command(ensure_folders.FOLDERS_COMMAND, str(self.folder))
        self.assertEqual(code, 1)
        self.assertIn('not made, a file of that name is there: errors/', printed)

class HelpDeclaresIt(unittest.TestCase):

    def test_the_domain_and_its_verb_say_what_they_make_and_where_the_roles_are_said(self) -> None:
        domain = run_help()
        self.assertNotIn(f'memar module {ensure_folders.FOLDERS_COMMAND}', domain)
        self.assertIn('help of the verb that makes them', domain)
        verb = run_help(ensure_folders.FOLDERS_COMMAND)
        self.assertNotIn('current folder', verb)
        self.assertIn('protocol/, primitive/, rules/, errors/, tests/, services/, docs/, temp/', verb)
        self.assertIn('nothing is deleted or renamed', verb)
        self.assertIn('modules/README.md', verb)
        for role in ensure_folders.Role:
            with self.subTest(role=role.folder):
                self.assertIn(' '.join(role.holds.split()), verb)
                self.assertIn(' '.join(role.holds_not.split()), verb)
if __name__ == '__main__':
    unittest.main(verbosity=2)
