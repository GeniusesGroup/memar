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

`remove` does not delete: the file goes to the recycle bin, so it is still there
if it turns out to be needed. `restore` will not discard anything unless you
pass an explicit confirmation, because "tidy the status" is how uncommitted work
is most often lost — if you want it set aside, `stash` is the command for that.

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

    args = parser.parse_args()
    if args.command == "rename":
        cmd_rename(args.source, args.destination)
    elif args.command == "remove":
        cmd_remove(args.paths)
    elif args.command == "stash":
        cmd_stash(args.message)
    elif args.command == "restore":
        cmd_restore(args.paths, args.confirm)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
