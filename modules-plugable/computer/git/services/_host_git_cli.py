#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/computer/git/services/_host_git_cli.py — the path-invoked face of the git verbs, which now live in `bundles/memar_git`.

Every verb but `record` forwards to the bundle (`memar git VERB`); `record` stays here with the records branch it serves
and goes with it. This script goes when the last instruction naming its path is replaced by the verb.
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path
_REPO = next(p for p in Path(__file__).resolve().parents if p.name == 'modules-plugable').parent
if __package__ in (None, ''):
    for _folder in (_REPO, _REPO / 'bundles' / 'memar', _REPO / 'bundles' / 'memar' / 'services'):
        if str(_folder) not in sys.path:
            sys.path.insert(0, str(_folder))
    __package__ = 'modules-plugable.computer.git.services'
from importlib import import_module
from . import _record as git_record
from machine.console import use_utf8_stdio
BUNDLE = 'bundles.memar_git.'
VERBS = ('rename', 'remove', 'stash', 'restore', 'undelete', 'commit', 'uncommit', 'reindex')
DESCRIPTION = '''modules-plugable/computer/git/services/_host_git_cli.py — git operations that do not lose work

Git already does all of this. Each command here does it with the constraint a
task keeps wanting to skip, and says which in its own --help.

Deleting, moving, discarding, stashing, restoring, and committing go through
this file and the path-invoked services under
modules-plugable/computer/memory/filesystem/services/ (tree, trash, link,
history_move_glob, and the fs_*.py libraries beside them). Never the host's
own command for those acts — rm, Remove-Item, git rm, git restore, git checkout
of paths, git clean, a plain git commit — and never a command a runtime rewrites.
Run each with Python by path inside the checkout; none is a memar verb.

In a working tree other tasks share, commit only this task's paths. The
records of the task's tasks are not among them: memar git archive-task-records
keeps them on the records branch. Every commit names the tasks it carries
out with --task-id for each, or says --no-task; the message itself names
none. Commits follow the whole piece of work, by area (usually the top folder
a change lies in), staged in place from git status and git diff --stat; a
sub-agent never commits. A move rides with the commit while git still sees a
rename; otherwise commit the move alone first. Run memar content check on the
files the work changed before the commit, and commit only when it reports no
problems. When a commit stops partway, do what its message says; never delete
a lock file to get past one. Every verb that acts on a repository takes
--repository PATH and never reads the folder it is run from. If these files
are not at hand or do not cover the act, stop and say so.

One thing git does that looks like a bug: a file that matches .gitignore but
is already tracked still shows up as modified. Ignoring does not untrack, and
restoring it away is not the fix.
'''

def main() -> int:
    use_utf8_stdio()
    errors = import_module(BUNDLE + 'errors.errors')
    parser = argparse.ArgumentParser(description=DESCRIPTION, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest='command', required=True)
    for verb in VERBS:
        before = set(sub.choices)
        run = import_module(BUNDLE + 'services.' + verb).describe(sub)
        for name in set(sub.choices) - before:
            sub.choices[name].set_defaults(run=run)
    git_record.add_parser(sub)
    args = parser.parse_args()
    try:
        args.run(args)
    except errors.Error as failure:
        raise SystemExit(f'error: {failure}') from None
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
