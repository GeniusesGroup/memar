#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
import os
import shutil
import stat
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path
TESTS = Path(__file__).resolve().parent
TOP = next(p for p in TESTS.parents if p.name == 'bundles').parent
sys.path.insert(0, str(TOP / 'bundles' / 'memar' / 'services')); sys.path.insert(1, str(TOP))
sys.dont_write_bytecode = True
BUDGET_SECONDS = 200
release = import_module('bundles.memar.targets.python.release')
errors = import_module('bundles.memar.targets.python.errors.errors')

def project_with(*names: str) -> Path:
    project = Path(tempfile.mkdtemp())
    for name in names:
        (project / 'bin' / name).mkdir(parents=True)
    return project

class Pointer(unittest.TestCase):

    def test_none_installed_is_refused(self) -> None:
        with self.assertRaises(errors.NoneInstalled):
            release.current(project_with())

    def test_the_pointer_names_the_release_and_no_listing_is_read(self) -> None:
        project = project_with('20260101T000000Z', '20260202T000000Z')
        release.point(project, '20260101T000000Z')
        self.assertEqual(release.current(project), '20260101T000000Z')

    def test_a_pointer_to_a_release_that_is_not_there_is_refused(self) -> None:
        project = project_with()
        (project / 'bin').mkdir(parents=True)
        (project / 'bin' / release.POINTER).write_text('gone\n', encoding='utf-8')
        with self.assertRaises(errors.NoneInstalled):
            release.current(project)

class Install(unittest.TestCase):

    def test_the_pointer_moves_only_after_the_release_starts(self) -> None:
        project = project_with('old')
        release.point(project, 'old')
        order: list[str] = []

        def build(source: Path, releases: Path) -> Path:
            order.append('build')
            made = releases / 'new'
            made.mkdir()
            return made

        def starts(made: Path) -> None:
            order.append(f'starts:{release.current(project)}')

        name = release.install(TOP, project, build=build, starts=starts)
        self.assertEqual((name, release.current(project), order), ('new', 'new', ['build', 'starts:old']))

    def test_a_release_that_does_not_start_leaves_the_pointer_and_the_previous_release(self) -> None:
        project = project_with('old')
        release.point(project, 'old')

        def build(source: Path, releases: Path) -> Path:
            made = releases / 'new'
            made.mkdir()
            return made

        def starts(made: Path) -> None:
            raise errors.DoesNotStart(str(made))

        with self.assertRaises(errors.DoesNotStart):
            release.install(TOP, project, build=build, starts=starts)
        self.assertEqual(release.current(project), 'old')
        self.assertTrue((project / 'bin' / 'old').is_dir())

    def test_a_failed_build_leaves_the_pointer(self) -> None:
        project = project_with('old')
        release.point(project, 'old')

        def build(source: Path, releases: Path) -> Path:
            raise errors.BuildFailed('x')

        with self.assertRaises(errors.BuildFailed):
            release.install(TOP, project, build=build, starts=lambda made: None)
        self.assertEqual(release.current(project), 'old')

class StaleRelease(unittest.TestCase):

    def setUp(self) -> None:
        self.source = Path(tempfile.mkdtemp())
        (self.source / 'bundles' / 'memar').mkdir(parents=True)
        (self.source / 'bundles' / 'memar' / 'manifest.yaml').write_text('modules:\n  - alpha.beta\n  - modules-plugable.a.b\n  - pkg.sub\n  - absent.one\n', encoding='utf-8', newline='\n')
        self.files = {'alpha.beta': self.source / 'alpha' / 'beta.py', 'modules-plugable.a.b': self.source / 'modules-plugable' / 'a' / 'b.py', 'pkg.sub': self.source / 'pkg' / 'sub' / '__init__.py'}
        for each in self.files.values():
            each.parent.mkdir(parents=True, exist_ok=True)
            each.write_text('x = 1\n', encoding='utf-8')
        self.project = project_with('rel')
        release.point(self.project, 'rel')
        self.touch(self.project / 'bin' / 'rel', 2000)
        for each in self.files.values():
            self.touch(each, 1000)

    def touch(self, path: Path, seconds: int) -> None:
        os.utime(path, (seconds, seconds))

    def test_none_installed_is_stale(self) -> None:
        empty = project_with()
        self.assertTrue(release.stale(self.source, empty))
        self.assertEqual(release.stale_why(self.source, empty), 'none installed')

    def test_a_release_newer_than_every_module_file_is_not_stale(self) -> None:
        self.assertFalse(release.stale(self.source, self.project))
        self.assertEqual(release.stale_why(self.source, self.project), '')

    def test_a_newer_module_file_makes_it_stale_and_is_named(self) -> None:
        self.touch(self.files['alpha.beta'], 3000)
        self.assertTrue(release.stale(self.source, self.project))
        why = release.stale_why(self.source, self.project)
        self.assertIn('beta.py', why)
        self.assertIn('rel', why)

    def test_a_hyphenated_module_name_maps_to_its_folder(self) -> None:
        self.touch(self.files['modules-plugable.a.b'], 3000)
        self.assertIn('b.py', release.stale_why(self.source, self.project))

    def test_a_package_module_is_its_init_file(self) -> None:
        self.touch(self.files['pkg.sub'], 3000)
        self.assertIn('__init__.py', release.stale_why(self.source, self.project))

    def test_a_declared_module_with_no_file_is_ignored(self) -> None:
        self.assertEqual(release.module_file(self.source, 'absent.one'), None)
        self.assertFalse(release.stale(self.source, self.project))

    def test_a_file_no_module_declares_does_not_matter(self) -> None:
        other = self.source / 'other.py'
        other.write_text('y = 1\n', encoding='utf-8')
        self.touch(other, 9000)
        self.assertFalse(release.stale(self.source, self.project))

class Shims(unittest.TestCase):

    def install(self, project: Path, name: str) -> None:
        def build(source: Path, releases: Path) -> Path:
            made = releases / name
            made.mkdir()
            return made

        release.install(TOP, project, build=build, starts=lambda made: None)

    def test_install_writes_both_shims_beside_the_pointer(self) -> None:
        project = project_with()
        self.install(project, 'one')
        folder = project / 'bin'
        cmd = (folder / 'memar.cmd').read_bytes().decode('utf-8')
        sh = (folder / 'memar').read_bytes().decode('utf-8')
        self.assertIn('%~dp0current', cmd)
        self.assertIn('LOCALAPPDATA', cmd)
        self.assertIn('Memar\\releases', cmd)
        self.assertIn('memar.exe', cmd)
        self.assertIn('%*', cmd)
        self.assertTrue(sh.startswith('#!/bin/sh\n'))
        self.assertIn('/current', sh)
        self.assertIn('exec ', sh)
        self.assertIn('"$@"', sh)
        self.assertIn('XDG_DATA_HOME', sh)
        self.assertNotIn('\r', sh)

    def test_a_pointer_move_changes_what_new_calls_start_and_the_shims_stay_the_same(self) -> None:
        project = project_with()
        self.install(project, 'one')
        folder = project / 'bin'
        before = ((folder / 'memar.cmd').read_bytes(), (folder / 'memar').read_bytes())
        self.assertNotIn(b'one', before[0] + before[1])
        self.assertEqual((folder / release.POINTER).read_text(encoding='utf-8').strip(), 'one')
        self.install(project, 'two')
        self.assertEqual((folder / release.POINTER).read_text(encoding='utf-8').strip(), 'two')
        self.assertEqual(((folder / 'memar.cmd').read_bytes(), (folder / 'memar').read_bytes()), before)

    def test_shims_are_rewritten_on_every_install_and_leave_no_scratch(self) -> None:
        project = project_with()
        self.install(project, 'one')
        folder = project / 'bin'
        (folder / 'memar.cmd').write_text('stale', encoding='utf-8')
        (folder / 'memar').write_text('stale', encoding='utf-8')
        self.install(project, 'two')
        self.assertIn('%*', (folder / 'memar.cmd').read_text(encoding='utf-8'))
        self.assertIn('"$@"', (folder / 'memar').read_text(encoding='utf-8'))
        self.assertEqual(sorted(each.name for each in folder.iterdir() if each.is_file()), ['current', 'memar', 'memar.cmd'])

    @unittest.skipIf(os.name == 'nt', 'the executable bit is not kept on Windows')
    def test_the_posix_shim_is_executable(self) -> None:
        project = project_with()
        self.install(project, 'one')
        self.assertTrue((project / 'bin' / 'memar').stat().st_mode & stat.S_IXUSR)

    def test_a_refused_install_writes_no_shim(self) -> None:
        project = project_with()

        def build(source: Path, releases: Path) -> Path:
            raise errors.BuildFailed('x')

        with self.assertRaises(errors.BuildFailed):
            release.install(TOP, project, build=build, starts=lambda made: None)
        self.assertFalse((project / 'bin' / 'memar.cmd').exists())

class Names(unittest.TestCase):

    def test_a_release_name_is_a_sortable_utc_stamp(self) -> None:
        name = release.release_name()
        self.assertRegex(name, r'^\d{8}T\d{6}Z$')

class ProgramOf(unittest.TestCase):

    def test_none_without_a_current_release(self) -> None:
        self.assertIsNone(release.program_of(project_with()))

    def test_names_the_release_executable_when_present(self) -> None:
        project = project_with('20260101T000000Z')
        release.point(project, '20260101T000000Z')
        exe = project / 'bin' / '20260101T000000Z' / release.EXECUTABLE
        exe.write_text('x', encoding='utf-8')
        self.assertEqual(release.program_of(project), (str(exe),))

    def test_a_runtime_mirror_is_preferred_over_the_checkout_copy(self) -> None:
        project = project_with('20260101T000000Z')
        release.point(project, '20260101T000000Z')
        checkout = project / 'bin' / '20260101T000000Z' / release.EXECUTABLE
        checkout.write_text('checkout', encoding='utf-8')
        runtime = release.runtime_releases() / '20260101T000000Z'
        runtime.mkdir(parents=True)
        mirrored = runtime / release.EXECUTABLE
        mirrored.write_text('runtime', encoding='utf-8')
        self.addCleanup(shutil.rmtree, runtime, True)
        self.assertEqual(release.program_of(project), (str(mirrored),))

class Hardening(unittest.TestCase):

    def test_a_release_that_does_not_start_is_set_aside_under_a_failed_name(self) -> None:
        project = project_with('old')
        release.point(project, 'old')

        def build(source: Path, releases: Path) -> Path:
            made = releases / '20260101T000000Z'
            made.mkdir()
            return made

        def starts(made: Path) -> None:
            raise errors.DoesNotStart(str(made))

        with self.assertRaises(errors.DoesNotStart):
            release.install(TOP, project, build=build, starts=starts)
        folder = project / 'bin'
        self.assertFalse((folder / '20260101T000000Z').exists())
        self.assertTrue((folder / '.failed-20260101T000000Z').is_dir())

    def test_a_second_install_while_one_runs_is_refused(self) -> None:
        project = project_with()
        with release.locked(project):
            with self.assertRaises(errors.ReleaseRefused):
                with release.locked(project):
                    pass
        with release.locked(project):
            pass

    def test_a_build_that_fails_leaves_no_work_folder_and_keeps_its_log(self) -> None:
        project = Path(tempfile.mkdtemp())
        releases = project / 'bin'
        releases.mkdir(parents=True)
        (releases / '.build-old').mkdir()
        with unittest.mock.patch.object(release, 'builder', return_value=sys.executable), unittest.mock.patch.object(release.subprocess, 'run', side_effect=release.subprocess.TimeoutExpired('x', 1)):
            with self.assertRaises(errors.BuildFailed):
                release.build(TOP, releases)
        self.assertEqual([path.name for path in releases.iterdir() if path.name.startswith('.build-')], [])

    def test_a_start_that_takes_too_long_is_a_refusal(self) -> None:
        with unittest.mock.patch.object(release.subprocess, 'run', side_effect=release.subprocess.TimeoutExpired('x', 1)):
            with self.assertRaises(errors.DoesNotStart):
                release.starts(Path('anywhere'))

    def test_staleness_is_judged_from_the_build_start_in_the_name(self) -> None:
        import os
        import time
        source = Path(tempfile.mkdtemp())
        bundle = source / 'bundles' / 'memar'
        bundle.mkdir(parents=True)
        (bundle / 'manifest.yaml').write_text('modules:\n  - alpha\n', encoding='utf-8')
        (source / 'alpha.py').write_text('x = 1\n', encoding='utf-8')
        started = time.time() - 100
        os.utime(source / 'alpha.py', (started + 50, started + 50))
        name = time.strftime(release.STAMP, time.gmtime(started))
        project = project_with(name)
        release.point(project, name)
        self.assertIn('alpha.py', release.stale_why(source, project))


class RealBuild(unittest.TestCase):

    def test_the_built_release_starts_lists_its_verbs_and_answers_from_another_folder(self) -> None:
        project = Path(tempfile.mkdtemp())
        name = release.install(TOP, project)
        folder = project / 'bin' / name
        self.assertTrue((folder / release.EXECUTABLE).is_file())
        self.assertEqual(release.current(project), name)

if __name__ == '__main__':
    unittest.main()
