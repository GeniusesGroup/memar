#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import calendar
import contextlib
import os
import shutil
import subprocess
import sys
import time
from importlib import import_module
from pathlib import Path
from typing import Callable
_m_errors = import_module('bundles.memar.targets.python.errors.errors')
_m_bundle_modules = import_module('modules.computer.software.edges.manifest.services.bundle_modules')
FOLDER = ('bin',)
POINTER = 'current'
EXECUTABLE = 'memar.exe' if os.name == 'nt' else 'memar'
SERVER_DIR = 'server'
SERVER_EXECUTABLE = 'memar_server.exe' if os.name == 'nt' else 'memar_server'
PROGRAM_NAME = 'memar'
SERVER_PROGRAM_NAME = 'memar_server'
ENTRY = 'memar_entry.py'
SERVER_ENTRY = 'memar_server_entry.py'
BUNDLE = ('bundles', 'memar')
FACE = ('bundles', 'memar_cli')
SHELVES = ((), BUNDLE, (*BUNDLE, 'services'), FACE)
STAMP = '%Y%m%dT%H%M%SZ'
CMD_SHIM = 'memar.cmd'
SERVER_CMD_SHIM = 'memar_server.cmd'
RUNTIME_VENDOR = 'Memar'
RUNTIME_RELEASES = 'releases'
RUNTIME_SCRATCH = 'scratch'
CMD_TEXT = '@echo off\nsetlocal\nset /p MEMAR_RELEASE=<"%~dp0current"\nset "EXE=%LOCALAPPDATA%\\Memar\\releases\\%MEMAR_RELEASE%\\memar.exe"\nif not exist "%EXE%" set "EXE=%~dp0%MEMAR_RELEASE%\\memar.exe"\n"%EXE%" %*\nexit /b %ERRORLEVEL%\n'
SERVER_CMD_TEXT = '@echo off\nsetlocal\nset /p MEMAR_RELEASE=<"%~dp0current"\nset "EXE=%LOCALAPPDATA%\\Memar\\releases\\%MEMAR_RELEASE%\\server\\memar_server.exe"\nif not exist "%EXE%" set "EXE=%~dp0%MEMAR_RELEASE%\\server\\memar_server.exe"\n"%EXE%" %*\nexit /b %ERRORLEVEL%\n'
SH_TEXT = '#!/bin/sh\nhere=$(dirname "$0")\nread -r release < "$here/current"\nruntime="${XDG_DATA_HOME:-$HOME/.local/share}/memar/releases/$release/memar"\nif [ -x "$runtime" ]; then exec "$runtime" "$@"; fi\nexec "$here/$release/memar" "$@"\n'
SERVER_SH_TEXT = '#!/bin/sh\nhere=$(dirname "$0")\nread -r release < "$here/current"\nruntime="${XDG_DATA_HOME:-$HOME/.local/share}/memar/releases/$release/server/memar_server"\nif [ -x "$runtime" ]; then exec "$runtime" "$@"; fi\nexec "$here/$release/server/memar_server" "$@"\n'
START_SECONDS = 120
BUILD_SECONDS = 540

def releases_of(project: Path) -> Path:
    return Path(project).joinpath(*FOLDER)

def runtime_home() -> Path:
    if os.name == 'nt':
        base = Path(os.environ.get('LOCALAPPDATA') or Path.home() / 'AppData' / 'Local')
        return base / RUNTIME_VENDOR
    base = Path(os.environ.get('XDG_DATA_HOME') or Path.home() / '.local' / 'share')
    return base / 'memar'

def runtime_releases() -> Path:
    return runtime_home() / RUNTIME_RELEASES

def runtime_scratch(project: Path) -> Path:
    """Per-project scratch under the machine runtime home, when the checkout temp is not writable."""
    import hashlib
    key = hashlib.sha256(str(Path(project).resolve()).encode('utf-8')).hexdigest()[:16]
    return runtime_home() / RUNTIME_SCRATCH / key

def mirror_release(made: Path) -> Path:
    destination = runtime_releases() / made.name
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(made, destination)
    return destination

def executable_of(project: Path) -> Path | None:
    try:
        name = current(project)
    except _m_errors.NoneInstalled:
        return None
    for path in (runtime_releases() / name / EXECUTABLE, releases_of(project) / name / EXECUTABLE):
        if path.is_file():
            return path
    return None

def server_executable_of(project: Path) -> Path | None:
    try:
        name = current(project)
    except _m_errors.NoneInstalled:
        return None
    for path in (
        runtime_releases() / name / SERVER_DIR / SERVER_EXECUTABLE,
        releases_of(project) / name / SERVER_DIR / SERVER_EXECUTABLE,
    ):
        if path.is_file():
            return path
    return None

def program_of(project: Path) -> tuple[str, ...] | None:
    path = executable_of(project)
    return (str(path),) if path is not None else None

def server_program_of(project: Path) -> tuple[str, ...] | None:
    path = server_executable_of(project)
    return (str(path),) if path is not None else None

def release_name() -> str:
    return time.strftime(STAMP, time.gmtime())

def point(project: Path, name: str) -> None:
    folder = releases_of(project)
    folder.mkdir(parents=True, exist_ok=True)
    scratch = folder / f'{POINTER}.{os.getpid()}.tmp'
    scratch.write_text(name + '\n', encoding='utf-8')
    os.replace(scratch, folder / POINTER)

def current(project: Path) -> str:
    try:
        name = (releases_of(project) / POINTER).read_text(encoding='utf-8').strip()
    except OSError:
        raise _m_errors.NoneInstalled(f'no release is installed under {releases_of(project)}') from None
    if not name or not (releases_of(project) / name).is_dir():
        raise _m_errors.NoneInstalled(f'the pointer names {name!r}, which is not a release under {releases_of(project)}')
    return name

def child_environment() -> dict[str, str]:
    environment = dict(os.environ)
    if getattr(sys, 'frozen', False):
        for key in [key for key in environment if key.startswith('_PYI_') or key == '_MEIPASS2']:
            del environment[key]
        original = environment.pop('LD_LIBRARY_PATH_ORIG', None)
        environment.pop('LD_LIBRARY_PATH', None)
        if original is not None:
            environment['LD_LIBRARY_PATH'] = original
    return environment

def builder() -> str:
    candidates = [shutil.which('python'), shutil.which('python3')] if getattr(sys, 'frozen', False) else [sys.executable]
    for python in candidates:
        if python and subprocess.run([python, '-c', 'import PyInstaller'], capture_output=True, env=child_environment()).returncode == 0:
            return python
    raise _m_errors.NoBuilder('no Python with the packaging tool (PyInstaller) is on the path')

def build(source: Path, releases: Path) -> Path:
    python = builder()
    source, releases = (Path(source).resolve(), Path(releases).resolve())
    name = release_name()
    for left in releases.glob('.build-*'):
        shutil.rmtree(left, ignore_errors=True)
    work = releases / f'.build-{name}'
    work.mkdir(parents=True)
    shutil.copyfile(source.joinpath(*FACE, 'memar'), work / ENTRY)
    shutil.copyfile(source.joinpath(*BUNDLE, 'memar_server'), work / SERVER_ENTRY)
    names = _m_bundle_modules.modules_of(source.joinpath(*BUNDLE))
    def _pyinstaller(entry: Path, program: str) -> None:
        command = [python, '-m', 'PyInstaller', '--noconfirm', '--onedir', '--name', program, '--distpath', str(work / 'dist'), '--workpath', str(work / f'work-{program}'), '--specpath', str(work)]
        for shelf in SHELVES:
            command += ['--paths', str(source.joinpath(*shelf))]
        command += ['--add-data', f'{source.joinpath(*BUNDLE, "manifest.yaml")}{os.pathsep}.']
        for each in names:
            command += ['--hidden-import', each]
        command.append(str(entry))
        log = work / f'build-{program}.log'
        try:
            with log.open('wb') as output:
                done = subprocess.run(command, stdout=output, stderr=subprocess.STDOUT, timeout=BUILD_SECONDS, env=child_environment())
        except subprocess.TimeoutExpired:
            shutil.rmtree(work, ignore_errors=True)
            raise _m_errors.BuildFailed(f'the {program} build took longer than {BUILD_SECONDS} seconds and was stopped') from None
        if done.returncode != 0:
            kept = releases / f'build-failed-{name}-{program}.log'
            os.replace(log, kept)
            shutil.rmtree(work, ignore_errors=True)
            raise _m_errors.BuildFailed(f'the {program} build ended with status {done.returncode}; its log is {kept}')
    _pyinstaller(work / ENTRY, PROGRAM_NAME)
    _pyinstaller(work / SERVER_ENTRY, SERVER_PROGRAM_NAME)
    made = releases / name
    os.replace(work / 'dist' / PROGRAM_NAME, made)
    os.replace(work / 'dist' / SERVER_PROGRAM_NAME, made / SERVER_DIR)
    shutil.rmtree(work, ignore_errors=True)
    return made

def starts(made: Path) -> None:
    environment = {**os.environ, 'MEMAR_SERVER': '0'}
    try:
        done = subprocess.run([str(Path(made) / EXECUTABLE), '--help'], capture_output=True, text=True, encoding='utf-8', errors='replace', env=environment, timeout=START_SECONDS)
    except subprocess.TimeoutExpired:
        raise _m_errors.DoesNotStart(f'{made} did not answer --help within {START_SECONDS} seconds') from None
    if done.returncode != 0 or 'usage:' not in done.stdout or '<verb>' not in done.stdout or 'did not load' in done.stderr:
        raise _m_errors.DoesNotStart(f'{made} does not start and list its verbs: status {done.returncode}; {done.stderr.strip()[-300:]}')
    if not (Path(made) / SERVER_DIR / SERVER_EXECUTABLE).is_file():
        raise _m_errors.DoesNotStart(f'{made} has no {SERVER_DIR}/{SERVER_EXECUTABLE}')

def module_file(source: Path, name: str) -> Path | None:
    base = Path(source).joinpath(*name.split('.'))
    for candidate in (base.with_name(base.name + '.py'), base / '__init__.py'):
        if candidate.is_file():
            return candidate
    return None

def built_at(folder: Path) -> float:
    try:
        return float(calendar.timegm(time.strptime(folder.name, STAMP)))
    except ValueError:
        return folder.stat().st_mtime

def stale_why(source: Path, project: Path) -> str:
    try:
        name = current(project)
    except _m_errors.NoneInstalled:
        return 'none installed'
    built = built_at(releases_of(project) / name)
    face = Path(source) / 'bundles' / 'memar_cli' / 'memar'
    if face.is_file() and face.stat().st_mtime > built:
        return f'{face.relative_to(source).as_posix()} is newer than release {name}'
    for each in _m_bundle_modules.modules_of(Path(source).joinpath(*BUNDLE)):
        file = module_file(source, each)
        if file is not None and file.stat().st_mtime > built:
            return f'{file.relative_to(source).as_posix()} is newer than release {name}'
    return ''

def stale(source: Path, project: Path) -> bool:
    return bool(stale_why(source, project))

def write_shims(project: Path) -> None:
    folder = releases_of(project)
    for name, text, newline, mode in (
        (CMD_SHIM, CMD_TEXT, CRLF, 0o644),
        (PROGRAM_NAME, SH_TEXT, LF, 0o755),
        (SERVER_CMD_SHIM, SERVER_CMD_TEXT, CRLF, 0o644),
        (SERVER_PROGRAM_NAME, SERVER_SH_TEXT, LF, 0o755),
    ):
        wanted = text.replace(LF, newline)
        try:
            if (folder / name).read_bytes() == wanted.encode('utf-8'):
                continue
        except OSError:
            pass
        scratch = folder / f'{name}.{os.getpid()}.tmp'
        with scratch.open('w', encoding='utf-8', newline=newline) as output:
            output.write(text)
        os.chmod(scratch, mode)
        os.replace(scratch, folder / name)

CRLF = chr(13) + chr(10)
LF = chr(10)
LOCK = '.apply'
LOCK_SECONDS = BUILD_SECONDS + START_SECONDS + 60

@contextlib.contextmanager
def locked(project: Path):
    folder = releases_of(project)
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / LOCK
    try:
        if time.time() - path.stat().st_mtime > LOCK_SECONDS:
            path.unlink()
    except OSError:
        pass
    try:
        descriptor = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        raise _m_errors.ReleaseRefused(f'another update is building a release ({path})') from None
    try:
        os.write(descriptor, str(os.getpid()).encode('utf-8'))
        os.close(descriptor)
        yield
    finally:
        with contextlib.suppress(OSError):
            path.unlink()

def install(source: Path, project: Path, build: Callable[[Path, Path], Path]=build, starts: Callable[[Path], None]=starts) -> str:
    folder = releases_of(project)
    with locked(project):
        made = build(source, folder)
        try:
            starts(made)
        except _m_errors.DoesNotStart:
            os.replace(made, folder / f'.failed-{made.name}')
            raise
        try:
            mirror_release(made)
            write_shims(project)
            point(project, made.name)
        except OSError as error:
            raise _m_errors.ReleaseRefused(f'the release {made.name} was built and could not be made current: {error}') from None
    return made.name
