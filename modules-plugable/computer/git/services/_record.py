#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""host/git_record.py — `record`: commit files onto a branch other than the one checked out, without touching HEAD, the shared index or the working tree.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from host.git_index import PrivateIndex, index_entries
from host.git_lock import LOCK_NOTE, lock_deadline, once, patiently, stopped
from host.git_run import plumb, repository_flag, repository_root, run_captured, stderr_of


# How many times `record` takes its work up again when the branch moved under
# it, before it says so and stops.
RECORD_ATTEMPTS = 8


def _manifest_entries(manifest: Path) -> dict[str, Path]:
    """The branch path and source file of each line of MANIFEST (`BRANCH-PATH<TAB>SOURCE-FILE`), refusing any that is not sound."""
    try:
        lines = manifest.read_bytes().decode("utf-8-sig").splitlines()
    except (OSError, UnicodeDecodeError) as error:
        sys.exit(f"error: the manifest {manifest} cannot be read ({error})")
    entries: dict[str, Path] = {}
    for line in filter(None, lines):
        target, separator, source = line.partition("\t")
        if not separator or not target or not source:
            sys.exit(f"error: a manifest line is BRANCH-PATH, a tab, SOURCE-FILE, not {line!r}")
        if not _inside_branch(target):
            sys.exit(
                f"error: {target!r} is not a path inside the branch: it must be relative, with "
                "no empty, `.` or `..` part, no backslash, and no `.git` part"
            )
        path = Path(source)
        if not path.is_file():
            sys.exit(f"error: the source of {target} is not a file: {source}")
        if "\n" in source:
            sys.exit(f"error: the source file {source!r} holds a line break in its name and cannot be recorded")
        if target in entries:
            sys.exit(f"error: the manifest names {target} twice")
        entries[target] = path
    return entries


def _inside_branch(path: str) -> bool:
    """Whether PATH is a plain relative path in a branch's tree: no empty, `.`, `..` or `.git` part, no backslash."""
    return "\\" not in path and not any(part in ("", ".", "..") or part.lower() == ".git" for part in path.split("/"))


def cmd_record(repository: Path, branch: str, manifest: Path, replace: list[str], message_file: Path) -> None:
    """Commit files onto BRANCH, a branch other than the one checked out, without moving HEAD, the shared index or the working tree.

    The tree is built in a private index from the branch's tip: the folders
    REPLACE named are emptied, then each manifest entry is written as a blob,
    byte for byte, and put at its path. The branch is moved with `update-ref`
    against the tip it read, so a writer that got there first makes this one
    start again from the new tip; the commit made never loses theirs.
    """
    root = repository_root(repository)
    ref = f"refs/heads/{branch}"
    if run_captured(["check-ref-format", ref], cwd=root).returncode != 0:
        sys.exit(f"error: {branch!r} is not a branch name git accepts")
    if run_captured(["symbolic-ref", "-q", "HEAD"], cwd=root).stdout.strip() == ref:
        sys.exit(
            f"error: {branch} is the branch checked out in {root}; moving it would leave the "
            "shared index and the working tree behind it. Nothing was written."
        )
    entries = _manifest_entries(manifest)
    folders = [name.strip("/") for name in replace]
    for folder in folders:
        if not _inside_branch(folder):
            sys.exit(f"error: --replace {folder!r} is not a folder inside the branch")
    if not entries and not folders:
        sys.exit("error: the manifest names no file and nothing is to be replaced; there is nothing to record")
    message = message_file.read_bytes().decode("utf-8").replace("\r\n", "\n").strip()
    if not message:
        sys.exit(f"error: {message_file} is empty; a commit needs a message")

    # The blobs do not depend on the tip, so they are written once.
    shas: dict[str, str] = {}
    if entries:
        listed = "".join(f"{path}\n" for path in entries.values())
        written = plumb(["hash-object", "-w", "--no-filters", "--stdin-paths"], root, data=listed.encode("utf-8"))
        shas = dict(zip(entries, written.splitlines(), strict=True))
    zero = "0" * len(plumb(["hash-object", "--stdin"], root, data=b""))
    author, committer = plumb(["var", "GIT_AUTHOR_IDENT"], root), plumb(["var", "GIT_COMMITTER_IDENT"], root)
    for _ in range(RECORD_ATTEMPTS):
        tip = run_captured(["rev-parse", "--verify", "-q", ref], cwd=root).stdout.strip()
        with PrivateIndex(root) as private:
            if tip:
                plumb(["read-tree", tip], root, env=private)
            gone = [path for folder in folders for path in index_entries([folder], root, private)]
            records = [f"0 {zero}\t{path}" for path in gone]
            records += [f"100644 {sha}\t{path}" for path, sha in shas.items()]
            if records:
                data = "".join(f"{record}\0" for record in records).encode("utf-8")
                plumb(["update-index", "-z", "--add", "--index-info"], root, env=private, data=data)
            tree = plumb(["write-tree"], root, env=private)
        if tip and tree == plumb(["rev-parse", f"{tip}^{{tree}}"], root):
            print(tip)
            print(f"nothing to record: {branch} already holds all of it at {tip[:12]}.", file=sys.stderr)
            return
        if not tip and not shas:
            sys.exit(f"error: {branch} does not exist and the manifest names no file, so there is nothing to make it of")
        parent = f"parent {tip}\n" if tip else ""
        body = f"tree {tree}\n{parent}author {author}\ncommitter {committer}\n\n{message}\n"
        made = plumb(["hash-object", "-t", "commit", "-w", "--stdin"], root, data=body.encode("utf-8"))
        moved, lock = patiently(
            ["update-ref", "-m", "host/git.py record", ref, made, tip or zero], root, lock_deadline()
        )
        if moved.returncode == 0:
            print(made)
            after = f" on {tip[:12]}" if tip else ", its first commit"
            print(
                f"recorded {made[:12]} on {branch}{after}. HEAD, the shared index and the working "
                "tree were not touched, and nothing was pushed.",
                file=sys.stderr,
            )
            return
        if lock is not None:
            stopped(
                f"the commit object {made} was written, but {branch} was not moved: a lock is held.",
                f"Nothing to undo. {once(lock).capitalize()}, rerun the same command.",
                moved,
                lock,
            )
        if run_captured(["rev-parse", "--verify", "-q", ref], cwd=root).stdout.strip() == tip:
            sys.exit(f"error: git update-ref {ref} failed: {stderr_of(moved)}")
        # The branch moved under this command: take it up again from the new tip.
    sys.exit(f"error: {branch} moved under this command {RECORD_ATTEMPTS} times, so nothing was written to it. Rerun it.")


def add_parser(sub: argparse._SubParsersAction) -> None:
    """Declare this verb on the command's subparsers."""
    p_record = sub.add_parser(
        "record",
        help="commit files onto another branch without touching HEAD, the shared index or the working tree",
        description=(
            "Write one commit on the branch BRANCH of the repository, holding the files\n"
            "the manifest lists, and leave HEAD, the shared index, the working tree and\n"
            "every other branch exactly as they are. BRANCH is made, with no parent, if it\n"
            "does not exist; it may not be the branch checked out. The manifest is a file\n"
            "of lines, each BRANCH-PATH, a tab, and SOURCE-FILE: the file's bytes are put\n"
            "at that path as they are, with no line-ending or other conversion. Each\n"
            "--replace folder is emptied first, so the commit holds that folder as the\n"
            "manifest gives it. A result the branch already holds makes no commit and\n"
            "says so. It prints the branch's tip, never pushes, and never reads the\n"
            "folder it runs from.\n\n"
            f"{LOCK_NOTE}"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    repository_flag(p_record)
    p_record.add_argument("--branch", required=True, metavar="NAME", help="the branch to commit on, made if it is missing")
    p_record.add_argument(
        "--manifest",
        required=True,
        type=Path,
        metavar="FILE",
        help="a file of BRANCH-PATH, a tab, SOURCE-FILE lines, in UTF-8; write it with a file tool",
    )
    p_record.add_argument(
        "--replace",
        action="append",
        default=[],
        metavar="FOLDER",
        help="a folder of the branch to empty before the manifest's files are put in; may be given more than once",
    )
    p_record.add_argument(
        "-F",
        "--message-file",
        required=True,
        type=Path,
        help="the commit message, read from a file (write it with a file tool)",
    )
    p_record.set_defaults(
        run=lambda a: cmd_record(a.repository, a.branch, a.manifest, a.replace, a.message_file)
    )
