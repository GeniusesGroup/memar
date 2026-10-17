#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/knowledge/content/services/edit.py — `memar content edit`: exact text in a file replaced, or nothing written.

The caller states the text it believes the file holds, and the verb refuses
unless that text occurs exactly once — or as often as `--all` accepts — so an
edit never lands somewhere the caller did not mean. The read, the match, and
the write happen under the per-file lock, so the text matched is the text
written to; the encoding and newline guarantees are `content_text`'s, the same
as `write`'s.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from modules.knowledge.content.services.reference import content_root
from modules.knowledge.content.services.text import chosen_newline, plain_path, read_utf8_strict, write_utf8, writer_id


def describe(verbs):
    parser = verbs.add_parser(
        "edit",
        help="replace exact text in a file, refusing an absent or ambiguous match",
        description="Replace exact text in FILE, refusing an absent or "
                    "ambiguous match. Same encoding and newline guarantees as "
                    "write; removes a BOM if it finds one. The read, the match, "
                    "and the write happen under the per-file lock, so the text "
                    "matched is the text written to.",
        formatter_class=argparse.HelpFormatter,
    )
    parser.add_argument("file", help="path to edit (any path, not only in this repo)")
    parser.add_argument("--old", default=None, help="text to replace")
    parser.add_argument(
        "--old-file", default=None, help="read the text to replace from this file"
    )
    parser.add_argument("--new", default=None, help="replacement text")
    parser.add_argument(
        "--new-file", default=None, help="read the replacement from this file"
    )
    parser.add_argument(
        "--all", action="store_true", help="replace every occurrence, not only a unique one"
    )
    parser.add_argument("--newline", choices=["lf", "crlf"], default=None)
    return run


def run(args: argparse.Namespace) -> None:
    root = content_root()
    if args.old is None and args.old_file is None:
        sys.exit("error: edit needs --old or --old-file")
    if args.new is None and args.new_file is None:
        sys.exit("error: edit needs --new or --new-file")
    cmd_edit(args, root)


def cmd_edit(args: argparse.Namespace, root: Path) -> None:
    from machine.fs_lock import edit_session

    path = plain_path(args.file)
    if not path.is_file():
        sys.exit(f"error: not a file: {path}")
    old = (
        Path(args.old_file).expanduser().read_bytes().decode("utf-8")
        if args.old_file
        else args.old
    )
    new = (
        Path(args.new_file).expanduser().read_bytes().decode("utf-8")
        if args.new_file
        else args.new
    )
    if old == "":
        sys.exit("error: --old must not be empty; it would match everywhere")
    # Read, match, and write all inside the lock. This is the one place the
    # plan and the base can disagree — the caller believes the file contains
    # exactly `--old`, and that belief is checked against the file as it is at
    # the moment of the write rather than against a copy read before another
    # session could have written. The refusal below is the check; the lock is
    # what keeps the copy it reads and the bytes it writes one interval.
    with edit_session(
        path,
        session_id=writer_id(),
        plan_summary=f"replace {len(old)} chars with {len(new)} in {path.name}",
    ):
        text, had_bom = read_utf8_strict(path)
        found = text.count(old)
        if found == 0:
            sys.exit(
                f"error: --old does not occur in {path.name}. Nothing was written.\n"
                "  Check the exact text, including line endings and any dash character."
            )
        if found > 1 and not args.all:
            sys.exit(
                f"error: --old occurs {found} times in {path.name}. Nothing was written.\n"
                "  Give more surrounding context to make it unique, or pass --all."
            )
        if had_bom:
            print(f"note: {path.name} had a BOM; the write removes it")
        newline = chosen_newline(args.newline, path)
        write_utf8(path, text.replace(old, new), newline)
    print(f"edited {path} ({found} replacement{'s' if found > 1 else ''})")
