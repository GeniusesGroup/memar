#!/usr/bin/env python3
"""host/git.py — a git operation with the constraint a session keeps violating.

**Two audiences, two texts, and this file is where each lives.** `DESCRIPTION`
below is what `--help` prints, and the per-verb `help=` strings beside each
argument are what `git.py <verb> --help` prints. Both are addressed to whoever is
about to run one of these — usually an agent holding uncommitted work. Everything
from here down is addressed to whoever opens this file.

The host tool already speaks git. This file is the constraint, not the
capability:

  rename   Move/rename a *tracked* path with `git mv`, never plain mv.
           Commit that rename by itself before editing content — a mixed
           rename+edit commit defeats rename detection and orphans history.

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
           shared index for the committed paths alone. `--fold` replaces the
           last unpushed commits with the one it writes; `--leave-out` keeps a
           path's change out of that fold; `--as` commits a prepared file as
           a path, which is how one session's hunk is committed out of a file
           another session is also editing. Hooks do not run.

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
import shutil
import subprocess
import sys
from pathlib import Path

DESCRIPTION = """host/git.py — git operations that do not lose work

Git already does all of this. These do it with the constraint a session keeps
wanting to skip:

  rename    move a tracked file or folder, with history following it
  remove    stop tracking a path, sending it to the recycle bin first
  stash     set uncommitted work aside where a later session can get it
  restore   give uncommitted work back, and refuse to throw it away unasked
  undelete  bring a deleted or untracked-back path back from a commit
  commit    commit only the paths you name, leaving what others staged alone

`remove` does not delete: the file goes to the recycle bin, so it is still there
if it turns out to be needed. `restore` will not discard anything unless you
pass an explicit confirmation, because "tidy the status" is how uncommitted work
is most often lost — if you want it set aside, `stash` is the command for that.
`undelete` is neither of those: it recovers, and it says what it recovered.
`commit` is for a working tree other sessions share: plain `git commit` takes
everything staged, theirs included, and so does any rewrite of it your runtime
makes. The commits a `--fold` replaces stay reachable through `git reflog`.

One thing git does that looks like a bug: a file that matches `.gitignore` but
is already tracked still shows up as modified. Ignoring does not untrack, and
restoring it away is not the fix.
"""

SCRIPTS = Path(__file__).resolve().parent.parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from memar_console import use_utf8_stdio

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
        "Commit this rename by itself before editing content.",
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


def _plumb(
    args: list[str], root: Path, env: dict | None = None, data: bytes | None = None
) -> str:
    completed = subprocess.run(
        [_git(), "-C", str(root), *args], input=data, capture_output=True, env=env
    )
    if completed.returncode != 0:
        said = completed.stderr.decode("utf-8", "replace").strip()
        sys.exit(f"error: git {' '.join(args)} failed: {said}")
    return completed.stdout.decode("utf-8").strip()


def _in_repo(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root).as_posix()
    except ValueError:
        sys.exit(f"error: {path} is not inside the repository at {root}")


def _tree_entry(rev: str, path: str, root: Path) -> str:
    """`mode sha` of path in rev, or empty when rev does not hold it."""
    listed = _plumb(["ls-tree", rev, "--", path], root)
    return listed.split("\t")[0].replace(" blob ", " ") if listed else ""


def cmd_commit(
    paths: list[Path],
    prepared: list[str],
    leave_out: list[Path],
    fold: int,
    message_file: Path,
) -> None:
    """Commit the named paths alone, without the shared index and without porcelain."""
    toplevel = run_captured(["rev-parse", "--show-toplevel"])
    if toplevel.returncode != 0:
        sys.exit("error: not inside a git repository")
    root = Path(toplevel.stdout.strip()).resolve()
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
        upstream = run_captured(["rev-parse", "--verify", "--quiet", "@{upstream}"], cwd=root)
        oldest = _plumb(["rev-parse", f"HEAD~{fold - 1}"], root)
        if upstream.returncode == 0 and run_captured(
            ["merge-base", "--is-ancestor", oldest, upstream.stdout.strip()], cwd=root
        ).returncode == 0:
            sys.exit(
                f"error: {oldest[:12]} is already on {upstream.stdout.strip()[:12]} upstream; "
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
    for path in [*named, *left]:
        if run_captured(["diff", "--cached", "--quiet", "HEAD", "--", path], cwd=root).returncode:
            sys.exit(
                f"error: {path} has a staged change that HEAD does not hold — another "
                "session's, or yours from host git. Nothing was committed. Commit "
                "or unstage it first; this verb will not decide whose it is."
            )

    git_dir = _plumb(["rev-parse", "--absolute-git-dir"], root)
    private = dict(os.environ, GIT_INDEX_FILE=f"{git_dir}/memar-host-commit.index")
    _plumb(["read-tree", head], root, env=private)
    for path in left:
        entry = _tree_entry(parent, path, root)
        if entry:
            mode, sha = entry.split()
            _plumb(["update-index", "--add", "--cacheinfo", f"{mode},{sha},{path}"], root, env=private)
        else:
            _plumb(["update-index", "--force-remove", "--", path], root, env=private)
    for path, source in named.items():
        if source is not None:
            sha = _plumb(["hash-object", "-w", "--path", path, str(source)], root)
            entry = _tree_entry(head, path, root)
            mode = entry.split()[0] if entry else "100644"
            _plumb(["update-index", "--add", "--cacheinfo", f"{mode},{sha},{path}"], root, env=private)
        elif (root / path).exists():
            _plumb(["add", "--", path], root, env=private)
        else:
            _plumb(["update-index", "--force-remove", "--", path], root, env=private)
    tree = _plumb(["write-tree"], root, env=private)
    if tree == _plumb(["rev-parse", f"{parent}^{{tree}}"], root):
        sys.exit("error: the result is the tree the parent already has; nothing to commit")

    message = message_file.read_bytes().decode("utf-8").replace("\r\n", "\n").strip()
    if not message:
        sys.exit(f"error: {message_file} is empty; a commit needs a message")
    body = (
        f"tree {tree}\nparent {parent}\n"
        f"author {_plumb(['var', 'GIT_AUTHOR_IDENT'], root)}\n"
        f"committer {_plumb(['var', 'GIT_COMMITTER_IDENT'], root)}\n\n{message}\n"
    )
    made = _plumb(["hash-object", "-t", "commit", "-w", "--stdin"], root, data=body.encode("utf-8"))
    _plumb(["update-ref", "-m", f"host/git.py commit (fold {fold})", "HEAD", made, head], root)

    for path in [*named, *left]:
        entry = _tree_entry(made, path, root)
        if entry:
            mode, sha = entry.split()
            _plumb(["update-index", "--add", "--cacheinfo", f"{mode},{sha},{path}"], root)
        else:
            _plumb(["update-index", "--force-remove", "--", path], root)

    print(made)
    print(_plumb(["diff", "--stat", parent, made], root), file=sys.stderr)
    replaced = f"; it replaces {fold} commit(s), recoverable from git reflog as {head[:12]}" if fold else ""
    print(
        f"committed {made[:12]} on {parent[:12]}{replaced}.\n"
        "The shared index was updated for the committed paths only; whatever "
        "else was staged is still staged.",
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
        help="git mv for a tracked path; commit the rename alone afterwards",
    )
    p_rename.add_argument("source", type=Path)
    p_rename.add_argument("destination", type=Path)

    p_remove = sub.add_parser(
        "remove",
        help="trash working-tree path then git add -u (never git rm)",
    )
    p_remove.add_argument("paths", nargs="+", type=Path)

    p_stash = sub.add_parser(
        "stash",
        help="stash tracked+untracked WIP (not ignored); prefer over discard",
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
        help="commit FILE's content as PATH: your hunk in a file others also edit",
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
