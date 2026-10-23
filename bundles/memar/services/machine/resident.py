#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""machine/resident.py — the `memar` command's side of the resident process: ask it, or start it, or do the work in place.

**Why it is here.** Every call of the command is a new process that finds the verbs (a walk of the checkout), imports
them all and only then does its work; a process that stays does that once. The router asks this file first, before
it imports anything of Memar's, so the whole cost of a call that the resident process answers is this interpreter's
start and a local round trip.

**It is on unless `MEMAR_SERVER=0`** (owner, 2026-10-20): the router is the one command every chat and agent calls, so
the off switch is one variable, and nothing here may make a call worse than the call in place:

- Any failure before a call is handed over — no state file, a refused connection, a refused token — leaves the call to
  the router, which does it in its own process as it always did. A state file that is missing, or a connection
  that is refused, also starts the resident process (detached, at most once in `START_BACKOFF` seconds), so the next
  call finds it; this call is not made to wait for it.
- A call is handed over only when its answer does not depend on this process's standard input: stdin is a console or the
  null device, not a pipe or a file. The verbs of `mcp`, `resident`, `install` and `update` are never handed over
  (the first two are the process itself; the others change what the process is made of).
- A call the process does not take up within `TAKEN_SECONDS` (it is busy with another, or stuck) is done in place, and the
  process, finding the connection closed when it gets to it, does not run it.
- Once a call is taken up it is not run again in place: a verb may have changed files, and running it twice
  is worse than saying that the answer was lost.

**What is sent**: the arguments, this process's folder and environment, and a token from the state file. **What comes
back**: the verb's stdout and stderr, whole, and its status, which are written as the command would have written them.
The state file, `temp/resident/state.json` of the checkout, holds the port (on 127.0.0.1 only), the token made when the
process started, and its id; it is the whole of the way to find the process, and whoever can read the file as the
person can reach the process as the person does, which is the protection a local socket has.
"""
from __future__ import annotations
import json
import os
import stat
import subprocess
import sys
import time
from pathlib import Path
ENABLE = 'MEMAR_SERVER'
OFF = '0'
STATE_ENV = 'MEMAR_SERVER_STATE'
NOT_HANDED_OVER = frozenset({'mcp', 'resident', 'install', 'update'})
FOLDER = ('temp', 'resident')
STATE = 'state.json'
STARTING = 'starting'
START_BACKOFF = 15
CONNECT_SECONDS = 0.5
TAKEN_SECONDS = 5.0
MOST_BYTES = 64 * 1024 * 1024
BOOT = '# memar resident process\nimport sys; from pathlib import Path; s, t = Path(sys.argv[1]), Path(sys.argv[2]); sys.path[0:0] = [str(t), str(s), str(s / "services")]; from resident.services.serve import serve_forever; raise SystemExit(serve_forever())'
ROUTER = Path(__file__).resolve().parents[2] / 'memar'
CREATION_FLAGS = 512 | 134217728

def folder(top: Path) -> Path:
    """Where the state file is: the checkout's scratch, or the folder MEMAR_SERVER_STATE names (a test's own, so it never meets the owner's process)."""
    named = os.environ.get(STATE_ENV)
    return Path(named) if named else top.joinpath(*FOLDER)

def read_line(connection) -> bytes:
    """One line from CONNECTION, without its end; b"" when the other side closed before sending one."""
    chunks, size = ([], 0)
    while True:
        chunk = connection.recv(65536)
        if not chunk:
            break
        chunks.append(chunk)
        size += len(chunk)
        if chunk.endswith(b'\n') or size > MOST_BYTES:
            break
    return b''.join(chunks).rstrip(b'\r\n')

def state_of(top: Path) -> dict | None:
    try:
        state = json.loads((folder(top) / STATE).read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return None
    return state if isinstance(state, dict) and {'port', 'token'} <= state.keys() else None

def stdin_allows() -> bool:
    """Whether the answer cannot depend on what is on stdin: it is a console or the null device."""
    try:
        return stat.S_ISCHR(os.fstat(0).st_mode)
    except OSError:
        return False

def ask(top: Path, request: dict, timeout: float | None=None) -> dict | None:
    """The resident process's answer to REQUEST; None when nothing was handed over (no state, no connection, a refusal)."""
    import socket
    state = state_of(top)
    if state is None:
        return None
    try:
        connection = socket.create_connection(('127.0.0.1', int(state['port'])), timeout=CONNECT_SECONDS)
    except (OSError, ValueError):
        return None
    with connection:
        connection.settimeout(TAKEN_SECONDS)
        try:
            connection.sendall(json.dumps({'token': state['token'], **request}, ensure_ascii=False).encode('utf-8') + b'\n')
            reader = connection.makefile('rb')
            first = reader.readline()
        except OSError:
            return None
        answer = _decoded(first)
        if answer is None or 'refused' in answer:
            return None
        if 'taken' in answer:
            connection.settimeout(timeout)
            try:
                answer = _decoded(reader.readline())
            except OSError:
                return {'lost': True}
    return answer if answer is not None else {'lost': True}

def _decoded(line: bytes) -> dict | None:
    try:
        answer = json.loads(line)
    except ValueError:
        return None
    return answer if isinstance(answer, dict) else None

def start(top: Path) -> None:
    """Start the resident process, detached, unless a call started one a moment ago."""
    marker = folder(top) / STARTING
    try:
        if time.time() - marker.stat().st_mtime < START_BACKOFF:
            return
    except OSError:
        pass
    try:
        marker.parent.mkdir(parents=True, exist_ok=True)
        marker.write_text(str(os.getpid()), encoding='utf-8')
        options = {'creationflags': CREATION_FLAGS} if os.name == 'nt' else {'start_new_task': True}
        subprocess.Popen([sys.executable, '-c', BOOT, str(ROUTER.parent), str(ROUTER.parents[2])], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, close_fds=True, **options)
    except OSError:
        pass

def served(argv: list[str], top: Path) -> int | None:
    """The status of ARGV when the resident process answered it, writing its output; None when the router is to do it."""
    if os.environ.get(ENABLE) == OFF or not argv or argv[0] in NOT_HANDED_OVER or (not stdin_allows()):
        return None
    answer = ask(top, {'argv': argv, 'cwd': os.getcwd(), 'env': dict(os.environ)})
    if answer is None:
        start(top)
        return None
    if 'stdout' not in answer:
        sys.stderr.write('memar: the resident process stopped before it answered; the call may or may not have run.\n')
        return 1
    for stream, text in ((sys.stdout, answer['stdout']), (sys.stderr, answer.get('stderr', ''))):
        if text:
            stream.flush()
            stream.buffer.write(text.encode('utf-8'))
            stream.buffer.flush()
    return int(answer.get('status', 0))
