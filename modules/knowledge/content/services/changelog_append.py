#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/knowledge/content/services/changelog_append.py — `memar content changelog-append`: one entry added to the end of a ledger.

A changelog is oldest-first, so a new entry goes at its end, and only the tail
is read to decide the separator: an append never loads a ledger it has no need
to read. The entry takes the ledger's own line endings, because the practice
tells every contributor to append through this verb and `check` reports mixed
line endings — an append in the host's convention would make the verb the
cause of the defect it is the authority for detecting.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from modules.knowledge.content.services.reference import content_root, resolve_ref
from modules.knowledge.content.services.text import detect_newline


def describe(verbs):
    parser = verbs.add_parser(
        "changelog-append",
        help="append one oldest-first Changelog entry at end-of-file",
        formatter_class=argparse.HelpFormatter,
    )
    parser.add_argument("file", help="path to a *.changelog.md")
    parser.add_argument(
        "--entry-file",
        default=None,
        help="read entry Markdown from this file instead of stdin",
    )
    return run


def run(args: argparse.Namespace) -> None:
    cmd_changelog_append(args, content_root())


def changelog_append(path: Path, entry: str) -> None:
    """Append one Changelog entry at EOF (oldest-first). Peeks only the tail."""
    if path.suffixes[-2:] != [".changelog", ".md"] and not path.name.endswith(
        ".changelog.md"
    ):
        # Accept both Path("x.changelog.md") forms across platforms.
        if not path.name.endswith(".changelog.md"):
            sys.exit(
                f"error: changelog-append expects a *.changelog.md path, got {path.name}"
            )
    entry = entry.strip()
    if not entry.startswith("### "):
        sys.exit("error: changelog entry must begin with '### ' (an entry title)")

    if not path.is_file():
        sys.exit(f"error: not a file: {path}")

    # Peek at most the last 512 bytes for separator hygiene — never load the
    # whole changelog into memory for an append.
    size = path.stat().st_size
    with path.open("rb") as handle:
        handle.seek(max(0, size - 512))
        tail = handle.read().decode("utf-8", errors="replace")
    tail_stripped = tail.rstrip()
    needs_rule = not tail_stripped.endswith("---")

    parts: list[str] = []
    if size > 0 and not tail.endswith("\n"):
        parts.append("\n")
    if needs_rule:
        if size > 0 and not tail_stripped.endswith("\n\n"):
            if not tail.endswith("\n"):
                parts.append("\n")
            parts.append("\n")
        parts.append("---\n\n")
    elif size > 0 and not tail.endswith("\n\n"):
        if tail.endswith("\n"):
            parts.append("\n")
        else:
            parts.append("\n\n")
    parts.append(entry)
    parts.append("\n")

    # The file's own convention, not this machine's. Appending with a fixed one
    # is how a changelog that held CRLF for a year gains an LF tail from the
    # first append made on a host whose default differs. The entry is
    # normalized first so that a contributor's CRLF does not survive as a stray
    # CR inside an LF file.
    entry_text = "".join(parts).replace("\r\n", "\n").replace("\r", "\n")
    newline = detect_newline(path) if size else "\n"
    if newline != "\n":
        entry_text = entry_text.replace("\n", newline)
    with path.open("a", encoding="utf-8", newline="") as handle:
        handle.write(entry_text)


def cmd_changelog_append(args: argparse.Namespace, root: Path) -> None:
    path = resolve_ref(args.file, root, None)
    if args.entry_file:
        entry = Path(args.entry_file).expanduser().read_text(encoding="utf-8")
    else:
        entry = sys.stdin.read()
    changelog_append(path, entry)
    print(f"appended to {path}")
