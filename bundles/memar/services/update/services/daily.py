#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""bundles/memar/services/update/services/daily.py — `memar update` once a day in the background, and the one line it leaves.

Most people with Memar never develop it, and nothing reminds them to update it:
`memar update` answers when asked, and nobody asks. So this file asks the
router to run it before every verb — its `describe` registers no verb and
returns `before` — and the first verb of the day starts `memar update
--background`, through the launcher, as a process of its own — detached, its
output in a log beside the day's marker — and goes on with what it was asked
without waiting for it. The foreground command's output and exit status are
what they would have been: nothing here writes to stdout, and nothing here
raises. The background run itself comes through the router too, and is asked
nothing here: it is the day's run, and a notice is for a person.

What the background run found is left as one line, and the next `memar`
command prints it on stderr and removes it, so it is printed once. A line is
left only when something needs a person or changed under them: the checkout
was brought up to date, it is behind and was not, a copy was refreshed, or the
run could not check. A day on which everything was current leaves nothing.

That once-shown line is the one way Memar tells a person of something a
command they did not run did to them, so another service leaves its own here
too, on a subject of its own. Each subject keeps a
notice file of its own, so one never replaces another's; a newer line on the
update replaces one not yet printed, since only the latest state of the
checkout matters, and a service that reports separate events adds its line
after the last instead.

Three things stop the run before it starts, and each is checked first, so a
stopped run costs nothing: `memar update` itself, which is already the
question; a test run, which must never reach the machine it runs on; and
MEMAR_NO_AUTO_UPDATE set to anything but empty or 0. A notice left is still
printed under that opt-out, because the opt-out stops the update and a notice
may be about something else; a test run prints none. The once-a-day guard is
`s_lock.claim_today`, the one the task sweep asks too, and two runs
at once are kept apart by a lock from the same module: a run that finds it held
goes away rather than waiting, because the run holding it is doing the same
work.

The day's marker, the lock, the notices, and the log live in `temp/update/` of
the Memar root, which the checkout's `.gitignore` already covers, so a run
leaves nothing git sees.

Every `memar` invocation imports this file, so what only a run needs — the
lock, the Memar root, the test-run check, a child process — is imported
where it is used.
"""
from __future__ import annotations
from importlib import import_module
_m_fs_memar = import_module('modules-plugable.computer.memory.filesystem.services.fs_memar')
scratch_root = _m_fs_memar.scratch_root
_m_fs_lock = import_module('modules-plugable.computer.memory.filesystem.services.fs_lock')
claim_today = _m_fs_lock.claim_today
release_lock = _m_fs_lock.release_lock
try_lock = _m_fs_lock.try_lock
scratch_root = _m_fs_memar.scratch_root
_m_fs_test_scratch = import_module('modules-plugable.computer.memory.filesystem.services.fs_test_scratch')
in_test_run = _m_fs_test_scratch.in_test_run
import contextlib
import io
import os
import sys
from collections.abc import Iterator, Mapping
from pathlib import Path
from typing import TYPE_CHECKING, Callable
if TYPE_CHECKING:
    import subprocess
OPT_OUT_VARIABLE = 'MEMAR_NO_AUTO_UPDATE'
UPDATE_VERB = 'update'
BACKGROUND_FLAG = '--background'
LAUNCHER = _m_fs_memar.checkout_root() / 'bundles' / 'memar' / 'memar'
UPDATE_DIRNAME = 'update'
DAILY_MARKER_NAME = 'update.daily'
LOCK_NAME = 'update.lock'
NOTICE_SUFFIX = '.notice'
UPDATE_SUBJECT = 'update'
NOTICE_NAME = f'{UPDATE_SUBJECT}{NOTICE_SUFFIX}'
LOG_NAME = 'update.log'
LOCK_STALE_SECONDS = 15 * 60

def state_dir() -> Path:
    """Where the day's marker, the lock, the notice, and the log live: temp/update/."""
    directory = scratch_root() / UPDATE_DIRNAME
    directory.mkdir(exist_ok=True)
    return directory

def suppressed(environ: Mapping[str, str], *, testing: bool) -> str | None:
    """Why no daily run may start here, or None."""
    if testing:
        return 'this is a test run'
    if environ.get(OPT_OUT_VARIABLE, '').strip() not in ('', '0'):
        return f'{OPT_OUT_VARIABLE} is set'
    return None

def detach(command: list[str], log: Path) -> subprocess.Popen:
    """Start COMMAND as a process that outlives this one, its output into LOG.

    On Windows the child gets a console of its own with no window, so the
    console programs it starts open none either, and it leaves the caller's
    job where the job allows it; elsewhere it gets a task of its own.
    """
    import subprocess
    options: dict = {'stdin': subprocess.DEVNULL, 'stderr': subprocess.STDOUT, 'close_fds': True}
    with log.open('w', encoding='utf-8') as output:
        if os.name != 'nt':
            return subprocess.Popen(command, stdout=output, start_new_task=True, **options)
        flags = subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP
        try:
            return subprocess.Popen(command, stdout=output, creationflags=flags | subprocess.CREATE_BREAKAWAY_FROM_JOB, **options)
        except OSError:
            return subprocess.Popen(command, stdout=output, creationflags=flags, **options)

def start_daily(directory: Path) -> bool:
    """Start today's background run if this is the first ask today; whether it was started."""
    if not claim_today(directory / DAILY_MARKER_NAME):
        return False
    detach([sys.executable, str(LAUNCHER), UPDATE_VERB, BACKGROUND_FLAG], directory / LOG_NAME)
    return True

def take_notice(directory: Path) -> str | None:
    """The lines left for the next command, each subject's removed as it is read, so each is printed once."""
    said = []
    try:
        notices = sorted(directory.glob(f'*{NOTICE_SUFFIX}'))
    except OSError:
        return None
    for notice in notices:
        taken = notice.with_name(f'{notice.name}.{os.getpid()}')
        try:
            os.replace(notice, taken)
        except OSError:
            continue
        try:
            said.append(taken.read_text(encoding='utf-8').strip())
        except OSError:
            pass
        finally:
            taken.unlink(missing_ok=True)
    return '\n'.join((line for line in said if line)) or None

def leave_notice(directory: Path, line: str) -> None:
    """Leave LINE for the next `memar` command to print, replacing the one not yet printed."""
    notice = directory / f'{UPDATE_SUBJECT}{NOTICE_SUFFIX}'
    written = notice.with_name(f'{notice.name}.new.{os.getpid()}')
    written.write_text(line.strip() + '\n', encoding='utf-8', newline='\n')
    os.replace(written, notice)

@contextlib.contextmanager
def daily_run(directory: Path) -> Iterator[bool]:
    """Hold the run's lock for its length; yields False when another run holds it."""
    lock = directory / LOCK_NAME
    held = try_lock(lock, LOCK_STALE_SECONDS)
    try:
        yield held
    finally:
        if held:
            release_lock(lock)

def before_verb(verb: str | None, *, environ: Mapping[str, str]=os.environ, testing: bool | None=None) -> None:
    """What runs before VERB: print the notices left for it, then start today's run.

    Never raises and never writes to stdout: whatever fails here is the daily
    run's, and the command the person asked for goes on exactly as it would have.
    """
    notice = None
    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            if in_test_run() if testing is None else testing:
                return
            if suppressed(environ, testing=False):
                notice = take_notice(scratch_root() / UPDATE_DIRNAME)
            else:
                directory = state_dir()
                notice = take_notice(directory)
                if verb != UPDATE_VERB:
                    start_daily(directory)
    except (Exception, SystemExit):
        pass
    if notice:
        sys.stderr.write(''.join((f'memar: {line}\n' for line in notice.splitlines())))

def before(argv: list[str]) -> None:
    """What the router runs before every verb, given ARGV as typed: `before_verb` on its first word.

    The background run is the day's run itself, so it takes no notice meant
    for the next command a person types.
    """
    if argv[:1] == [UPDATE_VERB] and BACKGROUND_FLAG in argv:
        return
    before_verb(argv[0] if argv else None)

def describe(verbs) -> Callable[[list[str]], None]:
    return before
