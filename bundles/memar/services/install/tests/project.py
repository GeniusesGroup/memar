#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for what the project layer, `bundles/memar/services/install/services/project.py`, writes into a consuming project.

    python bundles/memar/services/install/tests/project.py

The `## Memar` section it writes into AGENTS.md is pinned whole, because it is
fixed text: a wording change is an edit of two files, never a drift one of them
absorbs alone. It is the only thing written for agents: AGENTS.md is sent with
every prompt, so a file in between would cost every session a tool call. For a
machine without `memar` it names where installing is said, not the commands,
which only such a machine needs. The location is read through the module that
owns it, so a session opened before the value was written does not send this
project to the bootstrap a second time.

What an earlier install wrote is the other case: its `.agents/memar/README.md`
is removed, and a `.agents/memar/preferences.md` is named as no longer read and
left, since what it holds is the project's. No manifest is written: a project's
`memar:` block is its own.

A project under git is also given one `.gitignore` line, `temp/`, so a module's
`temp` folder at any depth is never added: added once, kept off when a line
already ignores it at every depth, the file's own lines and endings kept.

The layer is asked in this process, as `memar install` asks it, from inside a
scratch folder of its own — given a `.git` so that it is a project root wherever
it sits, and made under the folder `modules-plugable/computer/filesystem/services/fs_test_scratch.py` names. The
dry run writes nothing, and only what it printed is read: a scratch inside this repository would be installed into this
repository, whose section names its own skill file rather than the one written
for a project that has to fetch Memar first.

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
import re
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parents[2]
sys.path.insert(0, str(SCRIPTS / 'services'))
sys.path.insert(1, str(SCRIPTS))
sys.path.insert(2, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
import bundles.memar.services.install.services.project as project
import modules.process.project.services.preferences as project_preferences
_REGISTRY_SCRATCH = tempfile.TemporaryDirectory(dir=suite_scratch())
_MEMAR_ROOT = Path(_REGISTRY_SCRATCH.name)
(_MEMAR_ROOT / 'temp').mkdir()
unittest.mock.patch.object(memar_fs, 'memar_root', return_value=_MEMAR_ROOT).start()
DRY_RUN_WRITE = re.compile('^dry-run: write (.+)$')
OBSOLETE_README = Path('.agents/memar/README.md')
OBSOLETE_PREFERENCES = Path('.agents/memar/preferences.md')
AGENTS_FILE = 'AGENTS.md'
EXPECTED_SECTION = '## Memar\nBefore any other work in a session, load and follow the Memar skill: `memar content resolve-path .agents/skills/memar/SKILL.md` prints its file. Where `memar` is not on PATH, install Memar with `.agents/scripts/install.sh` or `.agents/scripts/install.ps1` (https://raw.githubusercontent.com/GeniusesGroup/memar/main/.agents/scripts/), or run `memar install --help`.'
EXPECTED_MEMAR_SECTION = '## Memar\nBefore any other work in a session, load and follow [`.agents/skills/memar/SKILL.md`](.agents/skills/memar/SKILL.md).'

class ReachedByTheCommand(unittest.TestCase):
    """What a consuming project is left holding, as the installer's own run says."""

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        (Path(self.scratch.name) / '.git').mkdir()
        self.writes = self.parse(self.into_project(dry_run=True))

    def into_project(self, **options: bool) -> str:
        """What the layer printed, asked from inside the scratch project."""
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            project.into_project(Path(self.scratch.name), **options)
        return out.getvalue()

    def parse(self, output: str) -> list[tuple[str, str]]:
        """Each announced write and the text of it, in the order printed."""
        writes: list[tuple[str, list[str]]] = []
        for line in output.splitlines():
            match = DRY_RUN_WRITE.match(line)
            if match:
                writes.append((match.group(1).replace('\\', '/'), []))
            elif writes:
                writes[-1][1].append(line)
        return [(path, '\n'.join(lines).strip('\n')) for path, lines in writes]

    def written(self, tail: str) -> str:
        """What was written to the file whose path ends with TAIL."""
        for path, text in self.writes:
            if path.endswith(tail):
                return text
        self.fail(f'nothing was written to {tail}; these were: {[path for path, _ in self.writes]}')

    def test_the_section_is_pinned_whole(self):
        self.assertEqual(self.written(AGENTS_FILE), f'{project.AGENTS_H1}\n\n{EXPECTED_SECTION}')

    def test_only_the_agent_file_is_written_for_agents(self):
        written = [path for path, _ in self.writes]
        self.assertEqual([path for path in written if not path.endswith('.gitignore')], [str(Path(self.scratch.name) / AGENTS_FILE).replace('\\', '/')])

    def test_the_section_names_no_path_into_the_scripts_folder(self):
        self.assertNotIn('.py', self.written(AGENTS_FILE))

    def test_the_location_is_read_through_the_module_that_owns_it(self):
        source = Path(project.__file__).read_text(encoding='utf-8')
        self.assertNotIn('os.environ.get', source)
        self.assertIn('recorded_value()', source)

    def test_a_machine_without_the_command_is_sent_where_installing_is_said(self):
        section = self.written(AGENTS_FILE)
        self.assertIn(project.INSTALL_BOOTSTRAP, section)
        self.assertNotIn('```', section)
        self.assertNotIn('restart', section)
        self.assertNotIn('MEMAR_ROOT', section)

class SectionUpserted(unittest.TestCase):
    """The Memar section in AGENTS.md is replaced in place; the project's own sections keep their spacing."""

    def test_a_blank_line_still_parts_the_section_from_the_projects_next_one(self):
        own = '## Source\nRead the practice first.\n'
        before = f'{project.AGENTS_H1}\n\n## Memar\nAn older pointer.\n\n{own}'
        after = project.upsert_memar_section(before)
        self.assertEqual(after, f'{project.AGENTS_H1}\n\n{project.memar_section_markdown()}\n{own}')
        self.assertEqual(project.upsert_memar_section(after), after)

    def test_the_memar_repository_names_its_own_skill_file(self):
        self.assertEqual(project.memar_section_markdown(memar=True), EXPECTED_MEMAR_SECTION + '\n')

class EarlierInstall(unittest.TestCase):
    """What an earlier install left: its README removed, a preferences file named and kept."""

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.project = Path(self.scratch.name)
        (self.project / '.git').mkdir()
        (self.project / OBSOLETE_README).parent.mkdir(parents=True)
        (self.project / OBSOLETE_README).write_text('# Memar\nRead the skill.\n', encoding='utf-8')
        trashed = unittest.mock.patch.object(project, 'soft_delete', side_effect=Path.unlink)
        trashed.start()
        self.addCleanup(trashed.stop)

    def into_project(self, **options: bool) -> tuple[str, str]:
        out, err = (io.StringIO(), io.StringIO())
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            project.into_project(self.project, **options)
        return (out.getvalue(), err.getvalue())

    def test_the_readme_and_its_empty_folder_are_removed(self):
        self.into_project()
        self.assertFalse((self.project / OBSOLETE_README).parent.exists())

    def test_a_dry_run_removes_nothing(self):
        printed, _ = self.into_project(dry_run=True)
        self.assertTrue((self.project / OBSOLETE_README).is_file())
        self.assertIn('dry-run: remove', printed)

    def test_a_preferences_file_is_named_and_left(self):
        preferences = self.project / OBSOLETE_PREFERENCES
        preferences.write_text('---\nsessions: work\n---\n', encoding='utf-8')
        _, said = self.into_project()
        self.assertTrue(preferences.is_file())
        self.assertIn('is not read any more', said)
        self.assertIn('`memar:` block', said)
        self.assertEqual(project_preferences.read_preferences(self.project), {})

    def test_no_manifest_is_written(self):
        self.into_project()
        self.assertFalse((self.project / project_preferences.PREFERENCES_RELATIVE).exists())

class TempIgnored(unittest.TestCase):
    """Every module has a `temp` folder (owner, 2026-10-15), so a project's git ignores one wherever it stands."""

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.project = Path(self.scratch.name)
        (self.project / '.git').mkdir()
        self.ignore = self.project / '.gitignore'

    def into_project(self, **options: bool) -> str:
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            project.into_project(self.project, **options)
        return out.getvalue()

    def read(self) -> str:
        with open(self.ignore, encoding='utf-8', newline='') as file:
            return file.read()

    def test_the_line_ignores_a_temp_folder_at_any_depth(self):
        self.assertEqual(project.TEMP_IGNORE_LINE, 'temp/')

    def test_a_project_without_one_gets_a_gitignore_holding_the_line(self):
        self.into_project()
        self.assertEqual(self.read(), 'temp/\n')

    def test_the_projects_own_lines_are_kept_and_the_line_added_once(self):
        self.ignore.write_text('node_modules/\n*.log', encoding='utf-8', newline='\n')
        self.into_project()
        self.assertEqual(self.read(), 'node_modules/\n*.log\ntemp/\n')
        self.into_project()
        self.assertEqual(self.read(), 'node_modules/\n*.log\ntemp/\n')

    def test_a_line_already_ignoring_temp_everywhere_is_left_as_it_is(self):
        for own in ('temp\n', '# Directories\n  temp/  \n', '**/temp/\n', '**/temp\n'):
            with self.subTest(own=own):
                self.ignore.write_text(own, encoding='utf-8', newline='\n')
                printed = self.into_project()
                self.assertEqual(self.read(), own)
                self.assertNotIn(str(self.ignore), printed)

    def test_a_top_only_line_does_not_count(self):
        self.ignore.write_text('/temp/\n', encoding='utf-8', newline='\n')
        self.into_project()
        self.assertEqual(self.read(), '/temp/\ntemp/\n')

    def test_the_files_own_line_endings_are_kept(self):
        self.ignore.write_text('a\r\nb\r\n', encoding='utf-8', newline='')
        self.into_project()
        self.assertEqual(self.read(), 'a\r\nb\r\ntemp/\r\n')

    def test_a_dry_run_writes_no_gitignore(self):
        printed = self.into_project(dry_run=True)
        self.assertFalse(self.ignore.exists())
        self.assertIn(f'dry-run: write {self.ignore}', printed)

    def test_a_project_not_under_git_gets_none(self):
        (self.project / '.git').rmdir()
        (self.project / '.hg').mkdir()
        self.into_project()
        self.assertFalse(self.ignore.exists())

class NoProjectNamed(unittest.TestCase):
    """Given no project the layer writes nothing and does not read the folder the process is in."""

    def test_none_named_writes_nothing_in_the_folder_the_process_is_in(self):
        with tempfile.TemporaryDirectory(dir=suite_scratch()) as here:
            (Path(here) / '.git').mkdir()
            err = io.StringIO()
            with contextlib.chdir(here), contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(err):
                project.into_project(dry_run=False)
            self.assertEqual(sorted((path.name for path in Path(here).iterdir())), ['.git'])
            self.assertIn('--project NAME', err.getvalue())
            self.assertIn('--project-path PATH', err.getvalue())

    def test_the_layer_never_asks_for_the_working_folder(self):
        with unittest.mock.patch.object(Path, 'cwd', side_effect=AssertionError('read the calling folder')):
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                project.into_project(dry_run=True)
if __name__ == '__main__':
    unittest.main(verbosity=2)
