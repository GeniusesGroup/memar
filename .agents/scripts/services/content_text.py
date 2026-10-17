#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/content_text.py — reading and writing a text file without damaging it.

Shared by `write` and `edit`, which put text into a file, by `changelog-append`,
which keeps a ledger's own line endings, and by `check`, which names a file the
same way the write verbs do. One discipline, so no verb writes a file another
verb would report.

**Why the write verbs exist.** Reading a file and writing it back is where a
document gets silently damaged, and the damage is invisible until someone reads
a character the round trip destroyed. The mechanism on Windows PowerShell 5.1 is
specific: `Get-Content` has no encoding argument, so it detects a file's
encoding from a byte-order mark and falls back to the console codepage when
there is none. Memar's files are UTF-8 **without** a BOM — correctly, since a
BOM becomes part of the first line for every tool that reads the file as text —
which is exactly the case that loses. Measured here: round-tripping a BOM-less
UTF-8 file through `Get-Content -Raw` and `Set-Content -Encoding UTF8` destroys
every non-ASCII character, while the same round trip over a file that had a BOM
preserves them. So the rule is not "PowerShell mangles Unicode" in general; it
is that a correctly-encoded document is the one this shell cannot read. The
verbs write UTF-8 with no BOM, keep the file's own line endings rather than
the platform's, guarantee a final newline, and refuse an empty or an ambiguous
write — and `check` reports the damage that already happened rather than letting
a later session inherit it. Mojibake is still valid UTF-8, so no checker can see
all of it; what survives is the fingerprint of the mis-decode, reported as a
hint rather than a verdict.

**What it cannot do.** It cannot repair text on its way in. On this machine a
PowerShell 5.1 pipe to a native program, a command-line argument, and `Out-File`
each lose every non-ASCII character before this process starts, and setting
`$OutputEncoding` or `[Console]::OutputEncoding` first does not recover them. For
text that is not pure ASCII, hand it a file (`--content-file`, `--old-file`,
`--new-file`) or use a file-write tool that writes it directly, and reserve stdin
for ASCII. What arrives is what gets written; that is the point of the verb and
also its limit.
"""
from __future__ import annotations

import sys
from pathlib import Path

from services.session_id import SessionId

# These functions are the whole discipline, and the write verbs are the only
# supported way to put text into a file from a shell:
#
#   * read UTF-8, strictly. Invalid input is an error, never a substitution,
#     because a substitution is how the corruption hides.
#   * write UTF-8 with no BOM. A BOM in a Markdown file is a defect: it
#     becomes part of the first line for every tool that reads the file as
#     text rather than as bytes.
#   * preserve the file's own newline convention instead of the platform's.
#     A document written on one platform and committed from another should
#     not gain or lose line endings.
#   * check the result, so a damage that already happened is reported rather
#     than inherited.


def read_utf8_strict(path: Path) -> tuple[str, bool]:
    """Return (text, had_bom). Raises SystemExit on unreadable or non-UTF-8."""
    try:
        raw = path.read_bytes()
    except OSError as error:
        sys.exit(f"error: cannot read {path}: {error}")
    had_bom = raw.startswith(b"\xef\xbb\xbf")
    if had_bom:
        raw = raw[3:]
    try:
        return raw.decode("utf-8"), had_bom
    except UnicodeDecodeError as error:
        sys.exit(
            f"error: {path} is not valid UTF-8 ({error}).\n"
            "  It is not written to, because writing a decoded-with-replacement\n"
            "  copy is how the damage spreads. Recover it from version control,\n"
            "  or convert it deliberately, before editing."
        )


def detect_newline(path: Path) -> str:
    """The file's own line ending, defaulting to LF for a new file."""
    try:
        raw = path.read_bytes()
    except OSError:
        return "\n"
    crlf = raw.count(b"\r\n")
    lf = raw.count(b"\n") - crlf
    if crlf and not lf:
        return "\r\n"
    return "\n"


NEWLINE_FLAGS = {"lf": "\n", "crlf": "\r\n"}


def chosen_newline(flag: str | None, path: Path) -> str:
    """The line ending a --newline flag names, or the file's own without one."""
    return NEWLINE_FLAGS[flag] if flag else detect_newline(path)


def write_utf8(path: Path, text: str, newline: str = "\n") -> int:
    """Write text as UTF-8, no BOM, with the given newline. Returns bytes."""
    if newline != "\n":
        text = text.replace("\r\n", "\n").replace("\r", "\n").replace("\n", newline)
    elif "\r" in text:
        text = text.replace("\r\n", "\n").replace("\r", "\n")
    if text and not text.endswith(newline):
        text += newline
    data = text.encode("utf-8")
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("wb") as handle:
            handle.write(data)
    except OSError as error:
        sys.exit(f"error: cannot write {path}: {error}")
    return len(data)


def writer_id() -> str:
    """Who this write is, for the intent note a waiter may have to read.

    One id per process. The session folder a session owns already carries its
    own id, and a write is a single act of one process, so a second option here
    would be a flag the caller must remember to pass for a note only a waiter in
    an unusual failure reads.
    """
    return SessionId.new()


def plain_path(ref: str) -> Path:
    """A path for a file operation, not for documentation navigation.

    `resolve_ref` is the right answer when a reference comes from a document and
    must stay inside the Memar repository. Writing, editing, and checking a file
    are operations on a path the caller states outright, so they are resolved
    against the current directory and are not confined to the repository — a
    round trip that mangles a file does not care which repository it is in.
    """
    return Path(ref).expanduser().resolve()
