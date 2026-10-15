#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""host/git.py — a git operation with the constraint a session keeps violating.

**Two audiences, two texts, and this file is where each lives.** `DESCRIPTION`
below is what `--help` prints, and each verb's `description=` and the `help=`
strings beside its arguments are what `git.py <verb> --help` prints: each help
states its own work, never another verb's. Both are addressed to whoever is
about to run one of these — usually an agent holding uncommitted work. Everything
from here down is addressed to whoever opens this file.

The host tool already speaks git. This file is the constraint, not the
capability:

  rename   Move/rename a *tracked* path with `git mv`, never plain mv.
           The rename rides with the task's one commit, and history follows
           it while each moved file stays above git's rename threshold. An
           edit that would push a file below the threshold is what makes a
           separate commit of the rename first necessary; `commit` refuses
           a result git no longer sees as a rename.
           `commit` takes the staged move when both of its paths are named;
           once the destination has been edited, name it with `--as` and a
           file holding the blob the move staged, and the move is committed
           alone while the edit stays in the working tree.

  remove   Stop tracking a path without `git rm`. `git rm` deletes in a way
           that is hard to recover from. This command sends the working-tree
           path to the OS Recycle Bin / Trash via `fs.py trash`, then stages
           the disappearance with `git add -u` so the index matches.

  stash    Park uncommitted work (tracked + untracked, not ignored) so a
           later session can recover it. Prefer this — or an ordinary
           commit — over discarding the working tree to tidy status.

  restore  Refuse to discard uncommitted work by default. Host `git restore`
           / checkout-of-paths / clean are what sessions use to "tidy"
           status and lose WIP. This command exits non-zero unless the
           caller passes an explicit irreversible confirmation token.
           Presence of the subcommand is not permission to call it casually.

  undelete Bring a path back from a commit, into the index and the working
           tree both. `restore` is the opposite operation and does not do this:
           it gives committed work back to HEAD by *discarding* what is
           uncommitted. A session that deletes a tracked path and then needs
           it again has neither `remove` (which goes forward) nor `restore`
           (which goes to HEAD by throwing work away), and falls back to
           hand-written `git restore --source --staged --worktree`, which is
           the same class of un-verbbed git the other verbs exist to replace.

  commit   Commit named paths, and only them, in a tree other sessions share.
           Host `git commit` commits the shared index, which holds whatever
           another session staged, and an agent runtime may rewrite any
           command spelled `git commit…` into exactly that — one rewrote
           `git commit-tree` and committed another session's staged renames.
           This builds the tree in a private index under `.git/`, writes the
           commit object with `hash-object`, moves the branch with
           `update-ref` against the commit it expects, and then updates the
           shared index for the committed paths alone, in one write so it
           never holds some of them updated and some not. `--fold` replaces the
           last unpushed commits with the one it writes; `--leave-out` keeps a
           path's change out of that fold; `--as` commits a prepared file as
           a path, which is how one session's hunk is committed out of a file
           another session is also editing. Hooks do not run.

  uncommit Take back the last commit, unpushed, keeping its work. Host
           `git reset --soft HEAD~1` leaves the commit's changes staged in
           the shared index, where `commit` then refuses them as another
           session's, and `reset --hard` or a mixed reset throws away or
           unstages what others hold. This moves HEAD to the parent with
           `update-ref` against the commit the caller names, resets the
           shared index to the parent for that commit's paths alone, and
           leaves the working tree as it is. The commit must be the one the
           caller expects, have one parent, and not be upstream — the same
           check `--fold` makes — and a path of it that holds a staged change
           of its own is refused rather than unstaged.

  reindex  Finish, or with `--undo` take back, a `commit` or `uncommit` that
           moved HEAD and then could not write the shared index. Both share
           that index with every other git process on the tree — an editor
           refreshing its status takes its lock many times a minute — so both
           wait for the index, HEAD and branch locks to be free before moving
           HEAD, and retry a write git refuses for a held lock, until one
           deadline LOCK_WAIT_SECONDS after the first of those stages begins,
           so that is the whole wait however many stages wait; any other failure
           stops at once. A lock still held after that is reported, never
           deleted: the message names the git command and all git said, the
           stage reached — nothing changed, the commit object written but HEAD
           not moved, or HEAD moved but the shared index not — the lock's path
           and age and how many git processes are running, and the two
           commands that finish or undo it. Both are this verb, so a session
           reaches for neither internals nor a host `git update-ref` or
           `git reset`. Finishing is refused once HEAD no longer holds the
           paths as the commit does, undoing once HEAD is not that commit, and
           both refuse a path staged since, as `commit` does.

           A known limit: a reftable repository keeps its refs in tables, not
           in files, so the ref lock files checked here never exist there, and
           git words a contended ref write differently. Such a write is then
           reported at once rather than waited out — the stop is the same,
           only sooner, so the limit costs a rerun and never a commit.

  record   Commit files onto a branch other than the one checked out, without
           touching HEAD, the shared index or the working tree: a branch that
           keeps a record out of the history of the work (the session records
           `memar session archive` keeps). It is the plumbing of `commit`
           pointed at another branch — a private index read from that
           branch's tip, blobs written byte for byte, a commit object, and
           `update-ref` against the tip it read, so a writer that got there
           first makes it start again from the new tip. It takes the
           repository from `--repository`, never the folder it runs from, and
           it never pushes: publishing a branch is a person's act.

           Every verb that acts on a repository takes `--repository` the same
           way, none reads the folder it runs from, and a relative path is
           relative to the repository. Each command has its own private index file, in a folder of
           its own under the repository's git folder that goes when it ends,
           so two commands at once never read or write one file.

This file needs git, and says so plainly if it is missing. It does not install
git: the Memar bootstrap (`install.sh` / `install.ps1` in the folder above this
one) is the one place that puts git and Python on a machine, and a second
implementation of that here is a second answer to a question with one answer.
Document-ID minting is not here either — it is a content verb, under `memar
content`.

`gitignore` only hides untracked paths; tracked files that match an ignore
pattern still show as modifications — do not "fix" that by restoring them
away.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from host import (
    git_commit,
    git_record,
    git_reindex,
    git_remove,
    git_rename,
    git_restore,
    git_stash,
    git_uncommit,
    git_undelete,
)
from machine.console import use_utf8_stdio

DESCRIPTION = """host/git.py — git operations that do not lose work

Git already does all of this. Each command here does it with the constraint a
session keeps wanting to skip, and says which in its own --help.

One thing git does that looks like a bug: a file that matches `.gitignore` but
is already tracked still shows up as modified. Ignoring does not untrack, and
restoring it away is not the fix.
"""


def main() -> int:
    use_utf8_stdio()
    parser = argparse.ArgumentParser(
        description=DESCRIPTION,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)
    for verb in (
        git_rename,
        git_remove,
        git_stash,
        git_restore,
        git_undelete,
        git_commit,
        git_uncommit,
        git_reindex,
        git_record,
    ):
        verb.add_parser(sub)
    args = parser.parse_args()
    args.run(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
