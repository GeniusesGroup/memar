#!/usr/bin/env python3
"""memar-session.py — one session's scratch folder under temp/, opened and closed.

**Two audiences, two texts, and this file is where each lives.** `DESCRIPTION`
below is what `memar session --help` prints: it is addressed to whoever is about
to open a session and says what to run and when its starter may close it.
Everything from here down is addressed to whoever opens this file. A person
opening a scratch folder does not need to know which module resolves the temp
root, and help output that told them would be a second, worse copy of this.

Why one folder per session, under ONE root. Parallel agent sessions edit one
shared working tree with no coordination, and concurrent writes to one file
collide silently — shared-tree collisions. The per-file advisory locks in
`machine/fs_lock.py` answer that, and the write verbs of `memar-content.py` take one,
but advisory locks are honored by skill rule and not by the filesystem:
file-write tools bypass them, and only intent notes saying who plans what
against which base let a waiter that takes over a stale lock read what the dead
session meant. Intent notes and locks are scratch, and scratch needs a home that
survives the session: session folders give every session its own folder, and
every session works inside its own folder so nothing lands in git by accident.
That home is <memar-root>/temp/, the ONE root the root .gitignore already
ignores — OS temp dirs are forbidden, because they are wiped by other apps
while sessions last days (the OS-temp wiped risk). The temp root resolves as the
recorded location else the checkout the tool runs inside; when neither resolves
this fails closed and guesses nothing.

Lifecycle. A session moves its folder to the OS trash when its starter declares
it finished. A folder left behind stays visible under its named id until then;
orphans are reaped by owner decision, never silently. One folder is never shared
across sessions: --session-id reuses an id only to continue the same logical
session. Sharing one folder between distinct sessions reintroduces the
unattributed mixing this tool exists to remove.

TODO(owner): the fate of the orphans — whether a session age reaps them, whether
`memar content` lists them as an obligation, or whether they are left for a
person to judge — is a decision about what a scratch folder owes its owner, and
no rule states it yet. Nothing reaps one until it does; that silence is the
safe direction, since an automatic reaper that guessed would delete the state a
session died before it could write down.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import argparse
from pathlib import Path


from memar_console import note, use_utf8_stdio
from machine.fs_memar import session_dir
from machine.fs_trash import soft_delete
from memar_session import new_session_id

NEW_COMMAND = "new"
CLOSE_COMMAND = "close"


def ensure_session(session_id: str | None = None) -> tuple[str, Path]:
    """Ensure <temp>/<session-id>/ exists and return its id and path.

    A rerun with the same id is idempotent: the folder is kept as is and the
    same id and path are reported again.
    """
    sid = new_session_id() if session_id is None else session_id
    path = session_dir(sid, create=True)
    return sid, path


def close_session(session_id: str) -> tuple[str, Path, bool]:
    """Trash one session's folder. Idempotent: a missing folder is already closed.

    Returns the id, its path, and whether anything was moved to recoverable
    storage. The target is confined to the session folder by construction:
    session_dir refuses anything shaped like a path.
    """
    path = session_dir(session_id)
    if not path.exists() and not path.is_symlink():
        return session_id, path, False
    soft_delete(path)
    return session_id, path, True


DESCRIPTION = """memar session — one folder for the work you are about to do

Work inside this folder, not in the checkout: the files you write while working
belong to your session, not to the repository.

    memar session new      open a folder and print its id and path
    memar session close    move it to the OS recycle bin / Trash

`new` prints an id and a path; pass that id back as `--session-id` to continue
the same session later. Close only when the person who started the session
declares the work finished, never after just one reply or task. Until then the
folder stays; `close` moves it to recoverable storage.
"""


def main(argv: list[str] | None = None) -> int:
    use_utf8_stdio()
    parser = argparse.ArgumentParser(
        description=DESCRIPTION,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    verbs = parser.add_subparsers(dest="verb", required=True)
    opener = verbs.add_parser(NEW_COMMAND, help="ensure one session folder and print its id and path")
    opener.add_argument(
        "--session-id",
        default=None,
        help="reuse this session id instead of minting one (rerun is idempotent)",
    )
    closer = verbs.add_parser(CLOSE_COMMAND, help="move a finished session folder to the OS recycle bin / Trash")
    closer.add_argument("--session-id", required=True, help="the session id to close")
    args = parser.parse_args(argv)
    if args.verb == NEW_COMMAND:
        sid, path = ensure_session(args.session_id)
        note(f"session_id: {sid}")
        note(f"path: {path}")
    else:
        sid, path, removed = close_session(args.session_id)
        note(f"{'closed' if removed else 'already closed'}: {sid}")
        note(f"path: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
