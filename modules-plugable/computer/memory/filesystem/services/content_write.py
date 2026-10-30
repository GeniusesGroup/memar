#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/computer/memory/filesystem/services/content_write.py — `memar content write`: a whole file's text put into it, undamaged.

The text arrives whole, from a file or from stdin, and is written under the
discipline `content_text` holds: UTF-8 with no BOM, the file's own line endings,
a final newline. An empty write and a write to a path that does not exist are
refused unless asked for, because both look like a mistake and neither is
reversible. The write is taken under the per-file lock, so a cooperating
task writing the same file is serialized rather than interleaved.
"""
from __future__ import annotations
from importlib import import_module
from machine.plugable_import import load as plugable_load
_m_fs_memar = plugable_load('computer.memory.filesystem.services.fs_memar')
TEMP_FOLDER = _m_fs_memar.TEMP_FOLDER
_m_fs_lock = plugable_load('computer.memory.filesystem.services.fs_lock')
edit_task = _m_fs_lock.edit_task
import argparse
import sys
from pathlib import Path
from modules.knowledge.content.services.reference import content_root
from modules.knowledge.text.services.file_text import chosen_newline, plain_path, read_utf8_strict, write_utf8, writer_id

def describe(verbs):
    parser = verbs.add_parser('write', help='write a text file as UTF-8 without a BOM, preserving its newlines', description="Put text into FILE as UTF-8 with no BOM, keeping the file's own line endings (LF for a new file) and guaranteeing a final newline. Never put text into a file through a shell's own text handling. The write is taken under the per-file lock, so a cooperating task writing the same file is serialized rather than interleaved.", formatter_class=argparse.HelpFormatter)
    parser.add_argument('file', help='path to write (any path, not only in this repo)')
    parser.add_argument('--content-file', default=None, help='read the new text from this file instead of stdin')
    parser.add_argument('--newline', choices=['lf', 'crlf'], default=None, help="line ending; default is the file's own, or LF for a new file")
    parser.add_argument('--create', action='store_true', help='required to create a file that does not exist yet')
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
    source = getattr(args, 'content_file', None)
    if source:
        refuse_kept_scratch(Path(source).expanduser())
        try:
            return Path(source).expanduser().read_bytes().decode('utf-8')
        except UnicodeDecodeError as error:
            sys.exit(f'error: --content-file is not valid UTF-8: {error}')
        except OSError as error:
            sys.exit(f'error: cannot read --content-file {source}: {error}')
    return sys.stdin.read()

def refuse_kept_scratch(source: Path) -> None:
    """Refuse a SOURCE that is scratch lying where a task's records are kept.

    A text staged only to be handed to this command, left in a task's docs/
    or beside its plan, is archived with the task and kept twice, once as
    the document written from it. Scratch goes in the task's temp/ folder,
    which is never archived.
    """
    _m_plan_file = import_module('modules-plugable.management.task.services.plan_file')
    PLAN_NAME = _m_plan_file.PLAN_NAME
    try:
        resolved = source.resolve()
    except OSError:
        return
    for folder in resolved.parents:
        if (folder / PLAN_NAME).is_file():
            relative = resolved.relative_to(folder)
            if relative.parts[0] != TEMP_FOLDER:
                sys.exit(f'error: --content-file {source} lies in task folder {folder.name} outside its {TEMP_FOLDER}/ folder, where it would be archived with the task as a second copy of what is written from it. Nothing was written. Put the scratch file in {folder / TEMP_FOLDER}/ and pass that.')
            return

def refuse_empty(path: Path, text: str, verb: str) -> None:
    """An empty write is almost never meant, and it is not reversible.

    A shell that fails to deliver a here-string, a redirect from a missing file,
    or a pipe that was never connected all look the same to this process: no
    input. Writing that over an existing document empties it, so the refusal is
    the whole point of having this command rather than a shell redirect.
    """
    if not text.strip():
        sys.exit(f'error: no text to {verb} {path.name}. Nothing was written.\n  Empty input usually means the pipe or redirect delivered nothing,\n  not that the file should be emptied. Pass the text on stdin, or\n  use --content-file PATH.')

def cmd_write(args: argparse.Namespace, root: Path) -> None:
    path = plain_path(args.file)
    if not path.is_file() and (not args.create):
        sys.exit(f'error: {path} does not exist. Nothing was written.\n  Pass --create if you mean to add a new file. A mistyped path in a\n  write would otherwise leave a stray file with no complaint.')
    text = content_from(args)
    refuse_empty(path, text, 'write')
    newline = chosen_newline(args.newline, path)
    existed = path.is_file()
    if existed:
        _, had_bom = read_utf8_strict(path)
        if had_bom:
            print(f'note: {path.name} had a BOM; the write removes it')
    with edit_task(path, task_id=writer_id(), plan_summary=f'write {len(text)} bytes to {path.name}'):
        size = write_utf8(path, text, newline)
    verb = 'rewrote' if existed else 'wrote'
    print(f'{verb} {path} ({size} bytes, utf-8, no BOM, {newline!r} newlines)')
