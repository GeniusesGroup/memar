#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""bundles/memar/services/install/services/machine.py — the machine layer of `memar install`: where Memar lives, recorded, and the machine settled around it.

One mechanism decides where Memar lives: the MEMAR_ROOT environment variable.
This layer writes it, for the current user, persistently, and reads it back for
everything that needs to know where Memar is. Nothing else decides it, and
nothing keeps a second copy of the repository. What the variable says is what
the platform's record of it says, not merely what this process was started with:
a task that opened before the value was written still finds it.

Obtaining the repository is not here, and the reason is where it belongs: the
bootstrap is what puts a checkout on a machine, and this layer is only ever run
from one. So what is left is the recording, the three questions asked on their
own — would a folder be refused, where is Memar, is this checkout one somebody
develops — and the machine around a recorded checkout:

  - writes MEMAR_ROOT for the current user, into that user's shell profile on
    POSIX and into the registry-backed user environment on Windows, so it
    survives the task;
  - puts the `memar` command on the user's PATH;
  - installs the editor extensions that checkout ships, under the names their
    own manifests give, writing the checkout's copy over any it installed before;
  - prints the value it wrote and where it wrote it.

What each of those is is asked rather than repeated here:
`modules-plugable/computer/filesystem/services/fs_memar_repository.py` what a Memar repository is,
`bundles/memar/services/update/services/checkout.py` what marks a checkout as a developer's,
`machine/env_location.py` what the location variable
says and where that variable lives, `machine/env_path.py` the user's PATH,
`modules-plugable/computer/filesystem/services/fs_target.py` the folder a run would use, `modules-plugable/computer/filesystem/services/fs_lock.py` two
tasks at once, `modules-plugable/computer/filesystem/services/fs_memar.py` where the checkout and its scratch live,
`machine/editor_extension.py` the editor extensions, and `machine/console.py`
how a step is printed.

A folder that is not a Memar repository is refused, so the variable is never
pointed at an arbitrary directory. A destination under a temporary directory is
refused for the same reason: a copy there is machine-local and does not survive,
which is the failure this layer exists to prevent. `check` prints the folder,
the temporary directory the refusal is decided against, and the refusal a
record would print — or that there would be none. It writes nothing, clones
nothing, and touches neither the variable nor the editor, so the refusal can be
proved on a machine that is already installed.

Two tasks arriving at once never record one folder at once: the recording is
taken under a lock file, and it is idempotent, so the second waits and then
finds the work already done.

MEMAR_ROOT takes effect for programs started *after* it is written. Other
programs — your editor, your shell, this task's parent — must be restarted
before they see it: a running program does not read a new value. This process
sets it for itself, so the layers `bundles/memar/services/install/install.py` asks after this one, in
this same process, see it. When this process's own copy disagrees with the
record, the record is used and the disagreement is printed.
"""
from __future__ import annotations
from importlib import import_module
_m_fs_lock = import_module('modules-plugable.computer.filesystem.services.fs_lock')
lock_path = _m_fs_lock.lock_path
release_lock = _m_fs_lock.release_lock
take_lock = _m_fs_lock.take_lock
_m_fs_memar = import_module('modules-plugable.computer.filesystem.services.fs_memar')
checkout_root = _m_fs_memar.checkout_root
memar_root = _m_fs_memar.memar_root
_m_fs_memar_repository = import_module('modules-plugable.computer.filesystem.services.fs_memar_repository')
is_memar_repository = _m_fs_memar_repository.is_memar_repository
not_a_repository = _m_fs_memar_repository.not_a_repository
_m_fs_target = import_module('modules-plugable.computer.filesystem.services.fs_target')
default_target = _m_fs_target.default_target
full_path = _m_fs_target.full_path
refuse_temporary = _m_fs_target.refuse_temporary
temporary_directory = _m_fs_target.temporary_directory
import os
from pathlib import Path
from machine.console import fail, note, step
from machine.editor_extension import install_extensions
from machine.env_location import VARIABLE, recorded_root, refuse_bogus_value, write_user_variable
from machine.env_path import ensure_on_path
from bundles.memar.services.install.services.development import DEVELOPMENT_KEY, mark_development
LAUNCHER = 'memar'

def temporary_consequence() -> str:
    """What refusing an install's target under the temporary directory says."""
    return f'Memar installed there would be machine-local and would not survive. Name a folder that persists, such as {default_target()}.'

def report_installed(path: Path, *, dry_run: bool=False) -> None:
    """Say where Memar is already, and bring the machine up to that checkout.

    The bootstrap scripts used to make this decision in their own dialect, before
    the installer existed as the one that answers for every entry point alike.
    They do not decide anything now: they make sure git and Python are here,
    obtain the checkout, and then hand the run to `memar install`. So the
    question whether Memar is already on this machine is asked here, against the
    record, and not by a shell reading a copy of the variable that a task
    opened earlier may not hold.

    A re-run costs nothing, so it also puts the launcher on PATH when a move
    left the old folder there, and writes this checkout's editor extension over
    the installed one: re-running is how an agent updates the editor after a
    change, and a run that only reported would leave the editor on the code it
    was first given. A dry run only says what it would do to the editor; PATH is
    never dry, for the same reason a record is not.
    """
    step(f'Memar is already installed at {path}')
    note(f'{VARIABLE} = {path}')
    for line in ensure_on_path(path / 'bundles' / 'memar', lambda d: (d / LAUNCHER).is_file()):
        note(line)
    install_extensions(path, dry_run=dry_run)

def record(target: Path) -> None:
    if not is_memar_repository(target):
        fail(f'{not_a_repository(target)}, so {VARIABLE} was not written. Nothing was deleted.')
    step('Recorded the location')
    where = write_user_variable(str(target))
    os.environ[VARIABLE] = str(target)
    note(f'{VARIABLE} = {target}')
    note(f'written to {where}')
    note('other programs must be restarted before they see it')
    step('The memar command')
    for line in ensure_on_path(target / 'bundles' / 'memar', lambda d: (d / LAUNCHER).is_file()):
        note(line)
    step('Editor extensions')
    install_extensions(target)
    step(f'Memar is registered at {target}')

def register(path: str) -> None:
    """Record PATH as where Memar lives, and settle the machine around it.

    Nothing is moved, copied, cloned, or deleted here: the bootstrap has already
    obtained the checkout — a clone, a pull, or the one the user pointed at — so
    what is left is to write down where it is, and everything the machine needs
    beside it. Whether PATH is a Memar repository is asked here, through the
    module that holds the test, and a folder that is not one is refused.
    """
    target = full_path(path)
    refuse_temporary(target, "Memar registered from there would not survive the machine's housekeeping.")
    refuse_bogus_value()
    step('Memar location')
    note(f'target: {target}')
    note('mode: register (the bootstrap obtained this checkout)')
    lock = lock_path(target)
    take_lock(lock)
    try:
        record(target)
    finally:
        release_lock(lock)

def check(path: str) -> None:
    """Ask the temporary-directory check a question, and stop.

    The refusal printed here is the refusal a record would print, because it is
    the refusal, and nothing after it runs: no clone, no write to the variable,
    nothing written to the editor. That is what makes the refusal provable on a
    machine that already has Memar on it.
    """
    target = full_path(path)
    step('Checking a target')
    note(f'target: {target}')
    note(f'temporary directory: {temporary_directory()}')
    refuse_temporary(target, temporary_consequence())
    note('not refused: that folder is not under the temporary directory')

def print_root() -> None:
    """Print where Memar is, and nothing else.

    A program that needs to find Memar has three ways to learn where it is, and
    this is the one that survives all of them. A recorded environment variable
    answers only when the program was started after the install and after the
    shell read it; a path typed into a configuration answers only while that
    configuration is intact. Asking the installed command answers by definition,
    because the command is the thing installed — the same reason `go env GOROOT`
    is how a program asks a Go toolchain where it lives rather than reading a
    variable the toolchain also writes.

    It lives here rather than among the content verbs because it is not about
    content: where Memar lives is what the installer decides, so this is the
    installer's own question. One line on stdout and nothing else, so it can be
    captured by substitution without parsing.
    """
    print(memar_root())

def mark_developer() -> None:
    """Mark the recorded checkout, else this one, as where Memar is developed, and stop.

    Its own mode rather than a flag on a bare run, because a bare run puts Memar
    into the project it is run from, and a developer runs this from inside the
    checkout, which is not a project to install into. What the mark is, and where
    it is kept, is `bundles/memar/services/install/services/development.py`'s.
    """
    checkout = recorded_root() or checkout_root()
    if not is_memar_repository(checkout):
        fail(f'{not_a_repository(checkout)}, so nothing was marked')
    try:
        mark_development(checkout)
    except (OSError, RuntimeError) as error:
        fail(f'{checkout} could not be marked as a development checkout: {error}')
    step(f'{checkout} is marked as a development checkout')
    note('the daily update checks and reports it, and never moves it')
    note(f'to undo: git -C "{checkout}" config --unset {DEVELOPMENT_KEY}')
