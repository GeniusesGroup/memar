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
import os
import re
import shlex
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Callable, NoReturn, TypeVar

DESCRIPTION = """host/git.py — git operations that do not lose work

Git already does all of this. Each command here does it with the constraint a
session keeps wanting to skip, and says which in its own --help.

One thing git does that looks like a bug: a file that matches `.gitignore` but
is already tracked still shows up as modified. Ignoring does not untrack, and
restoring it away is not the fix.
"""

LOCK_NOTE = """When another git process — often your editor, refreshing its status — holds a
lock this command needs, it says so and how long it will wait for it. If it
still cannot finish, it stops and says what stage it reached, what git said, how
old the lock is, and the exact command that finishes or undoes what was done. Do
what that message says; never delete a lock file to get past one."""
"""What `commit` and `uncommit` both say about a lock another git process holds, said once."""

SCRIPTS = Path(__file__).resolve().parent.parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from machine.console import use_utf8_stdio

GIT_MISSING = (
    "error: `git` is not on PATH. Run the Memar bootstrap for this machine "
    "(install.sh on POSIX, install.ps1 on Windows) — it installs git — then "
    "run this again."
)


def _git() -> str:
    """The git executable, or the one command that provides it."""
    found = shutil.which("git")
    if found is None:
        sys.exit(GIT_MISSING)
    return found


def run_git(args: list[str]) -> None:
    completed = subprocess.run([_git(), *args], check=False)
    if completed.returncode != 0:
        sys.exit(completed.returncode)


def run_captured(
    args: list[str], cwd: Path | None = None
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [_git(), *args],
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def cmd_rename(source: Path, destination: Path) -> None:
    if not source.exists():
        sys.exit(f"error: source does not exist: {source}")
    run_git(["mv", str(source), str(destination)])
    print(
        f"renamed (index): {source} -> {destination}\n"
        "The rename rides with the task's commit while git still detects it\n"
        "as a rename; an edit that breaks detection needs the rename committed first.",
        file=sys.stderr,
    )


def cmd_remove(paths: list[Path]) -> None:
    fs_py = Path(__file__).resolve().parent / "fs.py"
    for path in paths:
        if not path.exists() and not _tracked(path):
            sys.exit(f"error: path does not exist and is not tracked: {path}")
        if path.exists():
            completed = subprocess.run(
                [sys.executable, str(fs_py), "trash", str(path)],
                check=False,
            )
            if completed.returncode != 0:
                sys.exit(completed.returncode)
        # Stage the working-tree deletion without git rm.
        run_git(["add", "-u", "--", str(path)])
        print(
            f"removed (trashed + staged): {path}\n"
            "Do not use git rm — recovery from it is hard.",
            file=sys.stderr,
        )


def _tracked(path: Path) -> bool:
    return run_captured(["ls-files", "--error-unmatch", str(path)]).returncode == 0


DISCARD_CONFIRM = "DISCARD-UNCOMMITTED"


def _working_tree_dirty() -> bool:
    """True when tracked or untracked-non-ignored paths differ from HEAD/index."""
    porcelain = run_captured(["status", "--porcelain", "--untracked-files=normal"])
    return bool(porcelain.stdout.strip())


def cmd_stash(message: str | None) -> None:
    """Park WIP recoverably. Does not include ignored files (use commit for those)."""
    if not _working_tree_dirty():
        print("nothing to stash", file=sys.stderr)
        return
    args = ["stash", "push", "--include-untracked"]
    if message:
        args.extend(["-m", message])
    run_git(args)
    print(
        "stashed tracked + untracked (not ignored).\n"
        "Recover with `git stash pop` / `git stash apply` when ready.\n"
        "Ignored paths were not included — commit those if they must survive.",
        file=sys.stderr,
    )


def cmd_restore(paths: list[Path], confirm: str | None) -> None:
    """Discard working-tree changes only with an explicit irreversible token."""
    if confirm != DISCARD_CONFIRM:
        sys.exit(
            "error: refusing to discard uncommitted work.\n"
            "To tidy status without losing WIP: commit, or run "
            "`git.py stash`.\n"
            "gitignore does not hide tracked modifications.\n"
            f"Irreversible discard requires --confirm {DISCARD_CONFIRM} "
            "(do not pass that casually)."
        )
    if not paths:
        sys.exit("error: restore requires one or more paths")
    # Match host `git restore --worktree --source=HEAD` for the named paths only.
    run_git(["restore", "--source=HEAD", "--worktree", "--"] + [str(p) for p in paths])
    print(
        "discarded working-tree changes for the named paths "
        f"(confirmed {DISCARD_CONFIRM}).",
        file=sys.stderr,
    )


def cmd_undelete(paths: list[Path], source: str) -> None:
    """Bring paths back from `source` (HEAD by default) into index and tree.

    Both stages, always: a path staged as deleted is still absent from the
    index, so restoring only the working tree would leave a file on disk that
    git still believes is gone — the state that makes the next commit silently
    re-delete it.
    """
    for path in paths:
        listed = run_captured(["ls-tree", source, "--", str(path)])
        if listed.returncode != 0 or not listed.stdout.strip():
            sys.exit(
                f"error: {path} is not in {source}, so there is nothing to bring back"
            )
        state = run_captured(["ls-files", "--stage", "--", str(path)]).stdout.strip()
        before = state if state else "absent from index"
        print(f"recovering {path} from {source} (index was: {before})", file=sys.stderr)
        run_git(
            [
                "restore",
                f"--source={source}",
                "--staged",
                "--worktree",
                "--",
                str(path),
            ]
        )
        after = run_captured(["ls-files", "--stage", "--", str(path)]).stdout.strip()
        if not after:
            sys.exit(f"error: {path} did not come back into the index")
        print(f"recovered: {after}", file=sys.stderr)
    print(
        "Recovered into the index and the working tree. Nothing was committed, and\n"
        "nothing else in the index or the tree was touched.",
        file=sys.stderr,
    )


def _attempt(
    args: list[str], root: Path, env: dict | None = None, data: bytes | None = None
) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        [_git(), "-C", str(root), *args], input=data, capture_output=True, env=env
    )


def _said(completed: subprocess.CompletedProcess[bytes]) -> str:
    return completed.stderr.decode("utf-8", "replace").strip()


def _plumb(
    args: list[str], root: Path, env: dict | None = None, data: bytes | None = None
) -> str:
    completed = _attempt(args, root, env, data)
    if completed.returncode != 0:
        sys.exit(f"error: git {' '.join(args)} failed: {_said(completed)}")
    return completed.stdout.decode("utf-8").strip()


# Another git process holding a lock — most often an editor refreshing its
# status in the background — lets go within moments; one still holding it after
# this long is reported, with what was found, rather than waited out.
LOCK_WAIT_SECONDS = 20
LOCK_FIRST_PAUSE_SECONDS = 0.1
LOCK_LONGEST_PAUSE_SECONDS = 2.0
# Older than this with no git process running, a lock was most likely left by
# one that crashed; younger, it most likely belongs to one still running.
LOCK_STALE_SECONDS = 60
# How git says the lock it needed is held, whichever file it was taking.
LOCK_HELD = re.compile(r"Unable to create '([^']+?\.lock)': File exists")

Waited = TypeVar("Waited")


def _lock_deadline() -> float:
    """When a command stops waiting for locks: one deadline for all its stages, so the wait is LOCK_WAIT_SECONDS in all."""
    return time.monotonic() + LOCK_WAIT_SECONDS


def _waited(
    attempt: Callable[[], tuple[Waited, Path | None]], before: str, deadline: float
) -> tuple[Waited, Path | None]:
    """Repeat ATTEMPT while it finds a lock held, until DEADLINE: its last result, and the lock still held."""
    pause, named = LOCK_FIRST_PAUSE_SECONDS, set()
    while True:
        result, held = attempt()
        left = deadline - time.monotonic()
        if held is None or left <= 0:
            return result, held
        if held not in named:
            named.add(held)
            print(
                f"waiting up to {max(1, round(left))} s more before {before}: "
                f"{held} is held by another git process",
                file=sys.stderr,
            )
        time.sleep(min(pause, left))
        pause = min(pause * 2, LOCK_LONGEST_PAUSE_SECONDS)


def _locks_free(locks: list[Path], before: str, deadline: float) -> Path | None:
    """Wait for every one of LOCKS to be free before BEFORE: the one still held at DEADLINE, else None."""
    _, held = _waited(lambda: (None, next((lock for lock in locks if lock.exists()), None)), before, deadline)
    return held


def _patiently(
    args: list[str], root: Path, deadline: float, data: bytes | None = None
) -> tuple[subprocess.CompletedProcess[bytes], Path | None]:
    """Run git on the shared index or a ref, waiting out a lock another git process holds, until DEADLINE.

    Only a held lock is waited out: any other failure comes back at once, with
    no lock, for the caller to report.
    """
    def attempt() -> tuple[subprocess.CompletedProcess[bytes], Path | None]:
        completed = _attempt(args, root, data=data)
        found = LOCK_HELD.search(_said(completed)) if completed.returncode else None
        return completed, Path(found.group(1)) if found else None

    return _waited(attempt, f"git {args[0]}", deadline)


def _shared_locks(root: Path) -> list[Path]:
    """The lock files moving HEAD and writing the shared index take: the index's, HEAD's, and its branch's."""
    names = ["index", "HEAD"]
    branch = run_captured(["symbolic-ref", "-q", "HEAD"], cwd=root).stdout.strip()
    if branch:
        names.append(branch)
    listed = _plumb(["rev-parse", *(word for name in names for word in ("--git-path", name))], root)
    return [root / f"{line}.lock" for line in listed.splitlines()]


# tasklist reads no command lines, so on Windows the count takes in git's
# launcher shims beside the git each starts, and background daemons such as
# fsmonitor: an upper bound, which errs toward a lock still being someone's.
COUNT_INCLUDES = (
    "counting launcher shims and background daemons such as fsmonitor, so it may never reach 0"
    if os.name == "nt"
    else "not counting fsmonitor daemons"
)


def _git_processes() -> int | None:
    """How many git processes are running on this machine, or None when that cannot be asked."""
    if os.name == "nt":
        command = ["tasklist", "/FI", "IMAGENAME eq git.exe", "/FO", "CSV", "/NH"]
        counts = lambda line: line.lower().startswith('"git.exe"')
    else:
        command = ["ps", "-A", "-o", "args="]
        counts = lambda line: (
            Path((line.split() or [""])[0]).name == "git" and "fsmonitor--daemon" not in line
        )
    try:
        listed = subprocess.run(command, capture_output=True, text=True, errors="replace", timeout=10)
    except (OSError, subprocess.SubprocessError):
        return None
    if listed.returncode != 0:
        return None
    return sum(1 for line in listed.stdout.splitlines() if counts(line))


def _lock_account(lock: Path) -> str:
    """What a lock still held says about its holder: its age, and whether a git process is there to hold it."""
    try:
        age = time.time() - lock.stat().st_mtime
    except OSError:
        return f"The lock {lock} is gone now: its holder let go after the wait ran out."
    running = _git_processes()
    if running is None:
        seen = "whether a git process is running could not be asked"
    else:
        seen = f"{running} git process(es) are running on this machine ({COUNT_INCLUDES})"
    if age < LOCK_STALE_SECONDS:
        verdict = (
            "a lock this young most likely belongs to a live git process — an editor "
            "refreshing its status, or another session — which lets go on its own"
        )
    elif running == 0:
        verdict = (
            "a lock this old with no git process running was most likely left by one "
            "that crashed; a person may delete it once sure of that — this script never does"
        )
    else:
        verdict = (
            "a lock this old is either a long git operation or one left by a crash; only "
            "once no git process is working on this repository may a person delete it — "
            "this script never does"
        )
    return f"The lock {lock} was last written {age:.0f} s ago and {seen}: {verdict}."


def _stopped(
    stage: str,
    then: str,
    completed: subprocess.CompletedProcess[bytes] | None = None,
    lock: Path | None = None,
) -> NoReturn:
    """Stop, saying what stage was reached, what git said, what the lock still held means, and what to do next."""
    said = [f"error: {stage}"]
    if completed is not None:
        command = " ".join(str(word) for word in completed.args[3:])
        said.append(f"`git {command}` exited {completed.returncode}; git said:")
        said.extend(f"    {line}" for line in (_said(completed) or "(nothing)").splitlines())
    if lock is not None:
        said.append(_lock_account(lock))
    said.append(then)
    sys.exit("\n".join(said))


def _once(lock: Path | None) -> str:
    """When the stopped command can be taken up again: when the lock is free, or when git's reason is dealt with."""
    return "once the lock is free" if lock is not None else "once what git said above is dealt with"


def _this_command(*arguments: str) -> str:
    """This file run with ARGUMENTS, to print: on Windows `python` first, as `memar.cmd` runs it, so only arguments are ever quoted."""
    words = [str(Path(__file__).resolve()), *arguments]
    if os.name == "nt":
        return "python " + subprocess.list2cmdline(words)
    return shlex.join([sys.executable, *words])


def _in_repo(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root).as_posix()
    except ValueError:
        sys.exit(f"error: {path} is not inside the repository at {root}")


def _tree_entry(rev: str, path: str, root: Path) -> str:
    """`mode sha` of path in rev, or empty when rev does not hold it."""
    listed = _plumb(["ls-tree", rev, "--", path], root)
    return listed.split("\t")[0].replace(" blob ", " ") if listed else ""


def _upstream_holding(commit: str, root: Path) -> str:
    """The upstream's commit when COMMIT is already on it, else empty: the published-history check."""
    upstream = run_captured(["rev-parse", "--verify", "--quiet", "@{upstream}"], cwd=root)
    if upstream.returncode != 0:
        return ""
    held = run_captured(
        ["merge-base", "--is-ancestor", commit, upstream.stdout.strip()], cwd=root
    ).returncode == 0
    return upstream.stdout.strip() if held else ""


def _repository_root() -> Path:
    toplevel = run_captured(["rev-parse", "--show-toplevel"])
    if toplevel.returncode != 0:
        sys.exit("error: not inside a git repository")
    return Path(toplevel.stdout.strip()).resolve()


def _tree_entries(rev: str, paths: list[str], root: Path) -> dict[str, str]:
    """`mode sha` of each file under PATHS in REV, by path."""
    if not paths:
        return {}
    listed = _plumb(["--literal-pathspecs", "ls-tree", "-r", "-z", rev, "--", *paths], root)
    entries = {}
    for record in filter(None, listed.split("\0")):
        meta, _, path = record.partition("\t")
        mode, _, sha = meta.split(" ")
        entries[path] = f"{mode} {sha}"
    return entries


def _index_entries(paths: list[str], root: Path, env: dict | None = None) -> dict[str, str]:
    """`mode sha` of each entry under PATHS in the index ENV names, the shared one by default, by path."""
    if not paths:
        return {}
    listed = _plumb(["--literal-pathspecs", "ls-files", "-s", "-z", "--", *paths], root, env=env)
    entries = {}
    for record in filter(None, listed.split("\0")):
        meta, _, path = record.partition("\t")
        mode, sha, _ = meta.split(" ")
        entries[path] = f"{mode} {sha}"
    return entries


def _index_input(rev: str, paths: list[str], root: Path, env: dict | None = None) -> bytes:
    """`update-index -z --index-info` input giving PATHS REV's entries, and taking out each entry REV lacks."""
    want = _tree_entries(rev, paths, root)
    zero = "0" * len(_plumb(["rev-parse", rev], root))
    records = [f"{entry}\t{path}" for path, entry in want.items()]
    records += [f"0 {zero}\t{path}" for path in _index_entries(paths, root, env) if path not in want]
    return "".join(f"{record}\0" for record in records).encode("utf-8")


def _index_from(rev: str, was: str, paths: list[str], root: Path, reached: str, deadline: float) -> None:
    """Give PATHS in the shared index REV's entries, in one write; stop saying how to finish or undo when it cannot.

    One write, so the shared index holds either every path as it did before or
    every path as REV has them, never a mix. REACHED says where HEAD stands,
    for the message that stops; WAS is the commit HEAD was moved from.
    """
    if not paths:
        return
    done, lock = _patiently(["update-index", "-z", "--index-info"], root, deadline, _index_input(rev, paths, root))
    if done.returncode == 0:
        return
    named = ["--from", rev, "--was", was, "--", *paths]
    _stopped(
        f"{reached}, but the shared index was not updated for the commit's {len(paths)} "
        f"path(s): {', '.join(paths)}. It holds them as it held them before this command, "
        "and the working tree is as it should be; until this is finished `git status` "
        "shows a staged difference for them.",
        f"To finish, {_once(lock)}, run in {root}:\n    {_this_command('reindex', *named)}\n"
        f"To undo instead, moving HEAD back to {was[:12]} so it matches the shared index again:\n"
        f"    {_this_command('reindex', '--undo', *named)}",
        done,
        lock,
    )


def _staged_moves(
    paths: list[str], root: Path, against: str = "HEAD", prepared: dict[str, Path] | None = None
) -> set[str]:
    """Both ends of each move, and each removal, staged for PATHS against AGAINST as `rename` and `remove` stage them.

    `rename` stages a `git mv` and asks for it to be committed. A staged move
    whose source and destination the caller both names is claimed by that
    naming, and so is an edit staged into its destination — any edit that
    keeps the file above git's rename threshold, which folds into the task's
    commit with the move even when another session staged it — so it is not the someone-else's staging
    `_refuse_staged` guards against. What still makes it a move is git's own
    rename detection at its default threshold, here and, through
    `_renames_lost`, in the tree the commit writes. Nor is a staged removal of
    a named path the working tree no longer has, which is what `remove`
    leaves: the commit records the absence either way.

    A destination PREPARED gives a file for counts only when that file is the
    very blob the move staged: it is how the move is committed alone once the
    destination has been edited in the working tree. A source or a removal
    given a file is never a move.
    """
    if not paths:
        return set()
    prepared = prepared or {}
    listed = run_captured(
        ["diff", "--cached", "-M", "--name-status", "-z", against, "--", *paths], cwd=root
    ).stdout.split("\0")
    wanted, moved, at = set(paths), set(), 0
    while at < len(listed) and listed[at]:
        status = listed[at]
        if status.startswith(("R", "C")):
            source, destination = listed[at + 1], listed[at + 2]
            if (
                status.startswith("R")
                and source in wanted
                and source not in prepared
                and destination in wanted
                and (destination not in prepared or _is_staged_blob(prepared[destination], destination, root))
            ):
                moved.update((source, destination))
            at += 3
        else:
            path = listed[at + 1]
            if status == "D" and path in wanted and path not in prepared and not (root / path).exists():
                moved.add(path)
            at += 2
    return moved


def _renames(args: list[str], root: Path) -> set[tuple[str, str]]:
    """The (source, destination) pairs a `--name-status -z` listing from git ARGS reports as renamed."""
    listed = run_captured([*args[:1], "--name-status", "-z", *args[1:]], cwd=root).stdout.split("\0")
    pairs, at = set(), 0
    while at < len(listed) and listed[at]:
        if listed[at].startswith(("R", "C")):
            if listed[at].startswith("R"):
                pairs.add((listed[at + 1], listed[at + 2]))
            at += 3
        else:
            at += 2
    return pairs


def _renames_lost(moved: set[str], parent: str, tree: str, root: Path) -> list[str]:
    """Each staged move among MOVED that TREE, against PARENT, no longer shows as a rename.

    The commit takes a named file as the working tree has it, so an edit made
    after the move was staged rides with it too; the move survives only if git
    still pairs the two ends once that edit is in.
    """
    if not moved:
        return []
    staged = _renames(["diff", "--cached", "-M", "HEAD", "--", *sorted(moved)], root)
    written = _renames(["diff-tree", "-r", "-M", parent, tree, "--", *sorted(moved)], root)
    return [f"{source} -> {destination}" for source, destination in sorted(staged - written)]


def _is_staged_blob(file: Path, path: str, root: Path) -> bool:
    """Whether FILE, cleaned as PATH would be, is the blob the shared index holds for PATH."""
    staged = _index_entries([path], root).get(path, "")
    return _plumb(["hash-object", "--path", path, str(file)], root) == staged.partition(" ")[2]


def _refuse_staged(paths: list[str], root: Path, outcome: str) -> None:
    """Stop when any of PATHS holds a staged change HEAD does not: it is someone's, not this verb's."""
    for path in paths:
        if run_captured(["diff", "--cached", "--quiet", "HEAD", "--", path], cwd=root).returncode:
            sys.exit(
                f"error: {path} has a staged change that HEAD does not hold — another "
                f"session's, or yours from host git. {outcome} Commit "
                "or unstage it first; this verb will not decide whose it is."
            )


def cmd_commit(
    paths: list[Path],
    prepared: list[str],
    leave_out: list[Path],
    fold: int,
    message_file: Path,
) -> None:
    """Commit the named paths alone, without the shared index and without porcelain."""
    root = _repository_root()
    if fold < 0:
        sys.exit("error: --fold counts commits and cannot be negative")
    if not paths and not prepared and not fold:
        sys.exit("error: name a path, an --as, or a --fold; there is nothing to commit")
    if leave_out and not fold:
        sys.exit("error: --leave-out only means something inside a --fold")

    head = _plumb(["rev-parse", "HEAD"], root)
    parent = _plumb(["rev-parse", f"HEAD~{fold}"], root) if fold else head
    if fold:
        if _plumb(["rev-list", "--min-parents=2", f"{parent}..{head}"], root):
            sys.exit(f"error: the last {fold} commits include a merge; this does not fold merges")
        oldest = _plumb(["rev-parse", f"HEAD~{fold - 1}"], root)
        upstream = _upstream_holding(oldest, root)
        if upstream:
            sys.exit(
                f"error: {oldest[:12]} is already on {upstream[:12]} upstream; "
                "folding it would rewrite published history"
            )

    named: dict[str, Path | None] = {_in_repo(p, root): None for p in paths}
    for pair in prepared:
        target, separator, source = pair.partition("=")
        if not separator or not target or not source:
            sys.exit(f"error: --as takes PATH=FILE, not {pair!r}")
        source_path = Path(source).expanduser().resolve()
        if not source_path.is_file():
            sys.exit(f"error: --as source is not a file: {source}")
        named[_in_repo(Path(target), root)] = source_path
    left = [_in_repo(p, root) for p in leave_out]
    prepared_for = {path: source for path, source in named.items() if source is not None}
    moved = _staged_moves(list(named), root, prepared=prepared_for)
    _refuse_staged([path for path in [*named, *left] if path not in moved], root, "Nothing was committed.")

    git_dir = _plumb(["rev-parse", "--absolute-git-dir"], root)
    private = dict(os.environ, GIT_INDEX_FILE=f"{git_dir}/memar-host-commit.index")
    _plumb(["read-tree", head], root, env=private)
    if left:
        _plumb(["update-index", "-z", "--index-info"], root, env=private, data=_index_input(parent, left, root, private))
    for path, source in named.items():
        if source is not None:
            sha = _plumb(["hash-object", "-w", "--path", path, str(source)], root)
            entry = _index_entries([path], root)[path] if path in moved else _tree_entry(head, path, root)
            mode = entry.split()[0] if entry else "100644"
            _plumb(["update-index", "--add", "--cacheinfo", f"{mode},{sha},{path}"], root, env=private)
        elif (root / path).exists():
            _plumb(["add", "--", path], root, env=private)
        else:
            _plumb(["update-index", "--force-remove", "--", path], root, env=private)
    tree = _plumb(["write-tree"], root, env=private)
    if tree == _plumb(["rev-parse", f"{parent}^{{tree}}"], root):
        sys.exit("error: the result is the tree the parent already has; nothing to commit")
    lost = _renames_lost(moved, parent, tree, root)
    if lost:
        sys.exit(
            "error: with the working tree's edit in it, git no longer sees "
            + ", ".join(lost)
            + " as a rename, so its history would not follow. An edit rides with a move only "
            "while the file stays above git's rename threshold; this one pushes it below, so "
            "the move keeps a commit of its own: commit the move alone with "
            "--as DESTINATION=FILE holding the blob the move staged, and fold the edit into "
            "the task's commit after it. Nothing was committed."
        )

    message = message_file.read_bytes().decode("utf-8").replace("\r\n", "\n").strip()
    if not message:
        sys.exit(f"error: {message_file} is empty; a commit needs a message")
    body = (
        f"tree {tree}\nparent {parent}\n"
        f"author {_plumb(['var', 'GIT_AUTHOR_IDENT'], root)}\n"
        f"committer {_plumb(['var', 'GIT_COMMITTER_IDENT'], root)}\n\n{message}\n"
    )
    made = _plumb(["hash-object", "-t", "commit", "-w", "--stdin"], root, data=body.encode("utf-8"))
    unmoved = (
        f"the commit object {made} was written, but HEAD was not moved: it is still "
        f"{head}, and the shared index and the working tree are as they were (git gc "
        "drops the unreferenced object)."
    )
    deadline = _lock_deadline()
    lock = _locks_free(_shared_locks(root), "moving HEAD", deadline)
    if lock is not None:
        _stopped(unmoved, f"Nothing to undo. {_once(lock).capitalize()}, rerun the same command.", lock=lock)
    moved, lock = _patiently(["update-ref", "-m", f"host/git.py commit (fold {fold})", "HEAD", made, head], root, deadline)
    if moved.returncode != 0:
        _stopped(unmoved, f"Nothing to undo. {_once(lock).capitalize()}, rerun the same command.", moved, lock)
    _index_from(made, head, [*named, *left], root, f"HEAD moved from {head} to the commit {made}", deadline)

    print(made)
    print(_plumb(["diff", "--stat", parent, made], root), file=sys.stderr)
    replaced = f"; it replaces {fold} commit(s), recoverable from git reflog as {head[:12]}" if fold else ""
    print(
        f"committed {made[:12]} on {parent[:12]}{replaced}.\n"
        "The shared index was updated for the committed paths only; whatever "
        "else was staged is still staged.",
        file=sys.stderr,
    )


# A commit id as `git log` prints it, whole or abbreviated: `--expect` is the
# caller saying which commit it means, and a name like HEAD would say nothing.
COMMIT_ID = re.compile(r"[0-9a-f]{7,40}")


def cmd_uncommit(expect: str) -> None:
    """Move HEAD back to its parent, the commit's work kept in the tree and others' staging in the index."""
    root = _repository_root()
    expected = expect.lower()
    if not COMMIT_ID.fullmatch(expected):
        sys.exit(f"error: --expect takes the commit's id as `git log` prints it, not {expect!r}")
    head = _plumb(["rev-parse", "HEAD"], root)
    if not head.startswith(expected):
        sys.exit(f"error: HEAD is {head[:12]}, not {expect}; nothing was changed")
    parents = _plumb(["rev-list", "--parents", "-n", "1", head], root).split()[1:]
    if len(parents) != 1:
        sys.exit(
            f"error: {head[:12]} has {len(parents)} parents; this takes back only a commit "
            "with exactly one"
        )
    parent = parents[0]
    upstream = _upstream_holding(head, root)
    if upstream:
        sys.exit(
            f"error: {head[:12]} is already on {upstream[:12]} upstream; "
            "taking it back would rewrite published history"
        )
    listed = _plumb(["diff-tree", "-r", "--no-renames", "--name-only", "-z", parent, head], root)
    changed = [path for path in listed.split("\0") if path]
    _refuse_staged(changed, root, "Nothing was changed.")

    unchanged = f"nothing was changed: HEAD is still {head}, and the shared index and the working tree are as they were."
    deadline = _lock_deadline()
    lock = _locks_free(_shared_locks(root), "moving HEAD", deadline)
    if lock is not None:
        _stopped(unchanged, f"{_once(lock).capitalize()}, rerun the same command.", lock=lock)
    moved, lock = _patiently(["update-ref", "-m", "host/git.py uncommit", "HEAD", parent, head], root, deadline)
    if moved.returncode != 0:
        _stopped(unchanged, f"{_once(lock).capitalize()}, rerun the same command.", moved, lock)
    _index_from(parent, head, changed, root, f"HEAD moved from {head} back to its parent {parent}", deadline)

    print(parent)
    print(_plumb(["diff", "--stat", parent, head], root), file=sys.stderr)
    print(
        f"took back {head[:12]}; HEAD is {parent[:12]}. Its changes are in the working "
        f"tree, unstaged; the shared index was reset for its {len(changed)} path(s) "
        "only, and whatever else was staged is still staged.\n"
        f"It is recoverable from git reflog as {head}: `git update-ref HEAD {head} "
        f"{parent}` puts it back, and `git reset -q {head} -- PATH...` its paths' index entries.",
        file=sys.stderr,
    )


def cmd_reindex(paths: list[Path], source: str, was: str, undo: bool) -> None:
    """Finish a commit or uncommit that moved HEAD but stopped before the shared index, or with UNDO take its move back.

    Finishing gives PATHS SOURCE's entries, and only while HEAD holds them as
    SOURCE does; undoing moves HEAD from SOURCE back to WAS, and only while HEAD
    is SOURCE and the shared index still holds them as before the command. That
    is WAS's entries, except where a commit took a move or removal staged
    against WAS, which the index still holds as staged. Either way a path
    staged otherwise is refused, so nothing someone staged since is overwritten
    or left against the wrong HEAD.
    """
    root = _repository_root()
    deadline = _lock_deadline()
    rev = _plumb(["rev-parse", "--verify", f"{source}^{{commit}}"], root)
    old = _plumb(["rev-parse", "--verify", f"{was}^{{commit}}"], root)
    named = [_in_repo(path, root) for path in paths]
    have, want, then = _index_entries(named, root), _tree_entries(rev, named, root), _tree_entries(old, named, root)
    uncommitted = rev in _plumb(["rev-list", "--parents", "-n", "1", old], root).split()[1:]
    staged = set() if uncommitted else _staged_moves(named, root, old)
    for path in sorted({*have, *want, *then} - staged):
        if have.get(path) not in (want.get(path), then.get(path)):
            sys.exit(
                f"error: {path} is staged as neither {rev[:12]} nor {old[:12]} has it — "
                "another session's, or yours from host git. Nothing was changed. Commit "
                "or unstage it first; this verb will not decide whose it is."
            )
    head = _plumb(["rev-parse", "HEAD"], root)
    if undo:
        if head != rev:
            sys.exit(
                f"error: HEAD is {head[:12]}, not {rev[:12]}: it has moved since, so it is "
                f"not moved back to {old[:12]}. Nothing was changed."
            )
        if any(have.get(path) != then.get(path) for path in named if path not in staged):
            sys.exit(
                f"error: the shared index no longer holds these paths as {old[:12]} has "
                f"them — it was finished, or they were staged since — so HEAD is not moved "
                f"back to {old[:12]}. Nothing was changed."
            )
        moved, lock = _patiently(["update-ref", "-m", "host/git.py reindex --undo", "HEAD", old, rev], root, deadline)
        if moved.returncode != 0:
            _stopped(
                f"nothing was changed: HEAD is still {rev}.",
                f"{_once(lock).capitalize()}, rerun the same command.",
                moved,
                lock,
            )
        print(
            f"moved HEAD from {rev[:12]} back to {old[:12]}; the shared index was not touched, "
            f"and holds the {len(named)} named path(s) as it did before {rev[:12]} was made "
            f"HEAD. {rev[:12]} stays in git reflog.",
            file=sys.stderr,
        )
        return
    if _tree_entries("HEAD", named, root) != want:
        sys.exit(
            f"error: HEAD is {head[:12]}, which does not hold these paths as {rev[:12]} "
            "does: it has moved since, so the shared index is not given them. Nothing "
            "was changed."
        )
    _index_from(rev, old, named, root, f"HEAD is {head}", deadline)
    print(
        f"the shared index holds the {len(named)} named path(s) as {rev[:12]} has them; "
        "nothing else in it was touched.",
        file=sys.stderr,
    )


def main() -> int:
    use_utf8_stdio()
    parser = argparse.ArgumentParser(
        description=DESCRIPTION,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_rename = sub.add_parser(
        "rename",
        help="git mv for a tracked path; the rename rides with the task's commit",
        description="Move a tracked file or folder with `git mv`, so history follows it.",
    )
    p_rename.add_argument("source", type=Path)
    p_rename.add_argument("destination", type=Path)

    p_remove = sub.add_parser(
        "remove",
        help="trash working-tree path then git add -u (never git rm)",
        description=(
            "Stop tracking each PATH without deleting it: the file goes to the recycle\n"
            "bin, so it is still there if it turns out to be needed, and its\n"
            "disappearance is staged."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p_remove.add_argument("paths", nargs="+", type=Path)

    p_stash = sub.add_parser(
        "stash",
        help="stash tracked+untracked WIP (not ignored); prefer over discard",
        description="Set uncommitted work aside where a later session can get it back.",
    )
    p_stash.add_argument(
        "-m",
        "--message",
        default=None,
        help="optional stash message",
    )

    p_restore = sub.add_parser(
        "restore",
        help="refuse discard by default; needs --confirm DISCARD-UNCOMMITTED",
        description=(
            "Discard uncommitted changes to each PATH, and refuse unless --confirm is\n"
            "given: \"tidy the status\" is how uncommitted work is most often lost. If\n"
            "you want the work set aside, `stash` is the command for that."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p_restore.add_argument("paths", nargs="+", type=Path)
    p_restore.add_argument(
        "--confirm",
        default=None,
        help=f"must be exactly {DISCARD_CONFIRM} to discard",
    )

    p_undelete = sub.add_parser(
        "undelete",
        help="bring a deleted path back from a commit, into index and worktree",
        description="Bring each deleted or untracked-back PATH back from a commit; it says what it recovered.",
    )
    p_undelete.add_argument("paths", nargs="+", type=Path)
    p_undelete.add_argument(
        "--from",
        dest="source",
        default="HEAD",
        metavar="REV",
        help="the commit to bring the path back from (default: HEAD)",
    )

    p_commit = sub.add_parser(
        "commit",
        help="commit only the named paths; the shared index keeps others' staging",
        description=(
            "Commit only the paths you name, as they are in the working tree, for a\n"
            "working tree other sessions share: plain `git commit` takes everything\n"
            "staged, theirs included, and so does any rewrite of it your runtime makes.\n"
            "The commits a --fold replaces stay reachable through `git reflog`.\n\n"
            f"{LOCK_NOTE}"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p_commit.add_argument(
        "paths", nargs="*", type=Path, help="paths to commit as they are in the working tree"
    )
    p_commit.add_argument(
        "-F",
        "--message-file",
        required=True,
        type=Path,
        help="the commit message, read from a file (write it with a file tool)",
    )
    p_commit.add_argument(
        "--as",
        dest="prepared",
        action="append",
        default=[],
        metavar="PATH=FILE",
        help=(
            "commit FILE's content as PATH: your hunk in a file others also edit, or a staged "
            "move's destination as the move staged it once the file has been edited"
        ),
    )
    p_commit.add_argument(
        "--fold",
        type=int,
        default=0,
        metavar="N",
        help="replace the last N unpushed commits with this one",
    )
    p_commit.add_argument(
        "--leave-out",
        action="append",
        default=[],
        type=Path,
        metavar="PATH",
        help="inside a --fold, keep PATH as the new parent has it; its change stays unstaged",
    )

    p_uncommit = sub.add_parser(
        "uncommit",
        help="take back the last unpushed commit; its changes stay in the tree, others' staging stays staged",
        description=(
            "Move HEAD back to the parent of the commit you name, which must be HEAD,\n"
            "have one parent, and not be upstream yet. The working tree is left as it\n"
            "is, so the commit's changes show as unstaged edits; in the shared index\n"
            "only that commit's paths go back to the parent, and anything else staged\n"
            "stays staged. A path of the commit holding a staged change of its own is\n"
            "refused. The commit stays recoverable from git reflog, and the command\n"
            "prints how to put it back. It asks for the commit's id, so it never takes\n"
            "back one you did not mean.\n\n"
            f"{LOCK_NOTE}"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p_uncommit.add_argument(
        "--expect",
        required=True,
        metavar="SHA",
        help="the id of the commit to take back, as git log prints it; refused unless it is HEAD",
    )

    p_reindex = sub.add_parser(
        "reindex",
        help="finish, or undo, a commit or uncommit that moved HEAD but could not update the shared index",
        description=(
            "Give the named paths, in the shared index, the entries the commit --from has,\n"
            "in one write, and touch nothing else in it. This is the last step of `commit`\n"
            "and `uncommit`; when another git process holds the index lock past the wait,\n"
            "they stop after moving HEAD and print this command, and its --undo, with their\n"
            "arguments filled in. Finishing is refused once HEAD no longer holds the paths\n"
            "as --from does; --undo moves HEAD from --from back to --was instead, and is\n"
            "refused once HEAD is not --from or the index no longer holds the paths as it\n"
            "did before the command. A path staged as neither --from nor --was has it, and\n"
            "not as a move or removal the commit took, is refused either way: someone\n"
            "staged it since."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p_reindex.add_argument("paths", nargs="+", type=Path, help="the commit's paths, as the stopped command printed them")
    p_reindex.add_argument(
        "--from",
        dest="source",
        required=True,
        metavar="REV",
        help="the commit HEAD was moved to",
    )
    p_reindex.add_argument(
        "--was",
        required=True,
        metavar="REV",
        help="the commit HEAD was moved from",
    )
    p_reindex.add_argument(
        "--undo",
        action="store_true",
        help="move HEAD from --from back to --was, leaving the shared index as it is",
    )

    args = parser.parse_args()
    if args.command == "rename":
        cmd_rename(args.source, args.destination)
    elif args.command == "remove":
        cmd_remove(args.paths)
    elif args.command == "stash":
        cmd_stash(args.message)
    elif args.command == "restore":
        cmd_restore(args.paths, args.confirm)
    elif args.command == "undelete":
        cmd_undelete(args.paths, args.source)
    elif args.command == "commit":
        cmd_commit(args.paths, args.prepared, args.leave_out, args.fold, args.message_file)
    elif args.command == "uncommit":
        cmd_uncommit(args.expect)
    elif args.command == "reindex":
        cmd_reindex(args.paths, args.source, args.was, args.undo)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
