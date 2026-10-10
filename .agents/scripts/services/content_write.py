#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/content_write.py — `memar content write`: a whole file's text put into it, undamaged.

The text arrives whole, from a file or from stdin, and is written under the
discipline `content_text` holds: UTF-8 with no BOM, the file's own line endings,
a final newline. An empty write and a write to a path that does not exist are
refused unless asked for, because both look like a mistake and neither is
reversible. The write is taken under the per-file lock, so a cooperating
session writing the same file is serialized rather than interleaved.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from services.content_reference import content_root
from services.content_text import chosen_newline, plain_path, read_utf8_strict, write_utf8, writer_id


def describe(verbs):
    parser = verbs.add_parser(
        "write",
        help="write a text file as UTF-8 without a BOM, preserving its newlines",
        description="Put text into FILE as UTF-8 with no BOM, keeping the "
                    "file's own line endings (LF for a new file) and "
                    "guaranteeing a final newline. Never put text into a file "
                    "through a shell's own text handling. The write is taken "
                    "under the per-file lock, so a cooperating session writing "
                    "the same file is serialized rather than interleaved.",
        formatter_class=argparse.HelpFormatter,
    )
    parser.add_argument("file", help="path to write (any path, not only in this repo)")
    parser.add_argument(
        "--content-file",
        default=None,
        help="read the new text from this file instead of stdin",
    )
    parser.add_argument(
        "--newline",
        choices=["lf", "crlf"],
        default=None,
        help="line ending; default is the file's own, or LF for a new file",
    )
    parser.add_argument(
        "--create",
        action="store_true",
        help="required to create a file that does not exist yet",
    )
    return run


def run(args: argparse.Namespace) -> None:
    cmd_write(args, content_root())


def content_from(args: argparse.Namespace) -> str:
    """The new text, from a file if asked for, else from stdin.

    A file is the only transport that survives non-ASCII text. On Windows
    PowerShell 5.1, a pipe to a native program, a command-line argument, and
    `Out-File` all cross the console codepage on the way out, and a character
    that codepage cannot represent is replaced by `?` or dropped *before* this
    script ever sees it. The document is then written with the loss already
    baked in, and no check on the written file can find it, because the file is
    perfectly valid UTF-8 — it is simply the wrong text. Measured on this
    machine: a here-string piped to this script loses every non-ASCII
    character, and so does one passed as an argument; setting `$OutputEncoding`
    or `[Console]::OutputEncoding` first does not recover it.

    So the order of preference is: a tool that writes the file directly (an
    agent's own file-write, which is not a shell), then `--content-file` when
    the content is already safely on disk, then stdin for ASCII only. stdin is
    read only when the transports above it are absent: a caller whose text is
    on disk must never wait on a pipe nobody is going to close.
    """
    source = getattr(args, "content_file", None)
    if source:
        try:
            return Path(source).expanduser().read_bytes().decode("utf-8")
        except UnicodeDecodeError as error:
            sys.exit(f"error: --content-file is not valid UTF-8: {error}")
        except OSError as error:
            sys.exit(f"error: cannot read --content-file {source}: {error}")
    return sys.stdin.read()


def refuse_empty(path: Path, text: str, verb: str) -> None:
    """An empty write is almost never meant, and it is not reversible.

    A shell that fails to deliver a here-string, a redirect from a missing file,
    or a pipe that was never connected all look the same to this process: no
    input. Writing that over an existing document empties it, so the refusal is
    the whole point of having this command rather than a shell redirect.
    """
    if not text.strip():
        sys.exit(
            f"error: no text to {verb} {path.name}. Nothing was written.\n"
            "  Empty input usually means the pipe or redirect delivered nothing,\n"
            "  not that the file should be emptied. Pass the text on stdin, or\n"
            "  use --content-file PATH."
        )


def cmd_write(args: argparse.Namespace, root: Path) -> None:
    from machine.fs_lock import edit_session

    path = plain_path(args.file)
    if not path.is_file() and not args.create:
        sys.exit(
            f"error: {path} does not exist. Nothing was written.\n"
            "  Pass --create if you mean to add a new file. A mistyped path in a\n"
            "  write would otherwise leave a stray file with no complaint."
        )
    text = content_from(args)
    refuse_empty(path, text, "write")
    newline = chosen_newline(args.newline, path)
    existed = path.is_file()
    if existed:
        _, had_bom = read_utf8_strict(path)
        if had_bom:
            print(f"note: {path.name} had a BOM; the write removes it")
    # Held across the write, and released however this ends. The whole text
    # arrives at once, so there is nothing to re-derive: the lock is here to
    # keep another cooperating session from writing the same file between this
    # session's decision to write it and the bytes reaching disk. It is
    # advisory — a file-write tool does not take it — and the intent note is
    # what a waiter that takes over a stale lock reads to learn what this
    # session meant to do to this file and against which base.
    with edit_session(
        path,
        session_id=writer_id(),
        plan_summary=f"write {len(text)} bytes to {path.name}",
    ):
        size = write_utf8(path, text, newline)
    verb = "rewrote" if existed else "wrote"
    print(f"{verb} {path} ({size} bytes, utf-8, no BOM, {newline!r} newlines)")
