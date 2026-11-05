#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import argparse
import sys
from importlib import import_module
from pathlib import Path
from ..errors.errors import ContentOfTask, NotNamed, ScratchInTaskFolder
from ._edge import guarded
_m_edit = import_module('modules.knowledge.text.errors.edit')
_m_text_edit = import_module('modules.knowledge.text.services.text_edit')
_m_rule = import_module('modules.knowledge.text.services.text_line_ending_rule')
_m_file_text = import_module('modules.knowledge.text.services.file_text')
_m_codec = import_module('modules-plugable.computer.codec.string.utf8.services.utf8_codec')
_m_store = import_module('bundles.memar_fs.services.text_edit_store')
_m_lock = import_module('bundles.memar_fs.services.text_edit_lock')
_m_memar_location = import_module('bundles.memar.services.location.memar_location')
_m_timeline_files = import_module('modules.management.timeline.services.timeline_files')
TEMP_FOLDER = _m_memar_location.TEMP_FOLDER
is_content_file = _m_timeline_files.is_content_file
LINE_ENDINGS = {'lf': _m_rule.Text_LineEnding(_m_rule.LF), 'crlf': _m_rule.Text_LineEnding(_m_rule.CRLF)}


class Choice:

    def __init__(self, flag: str | None) -> None:
        self.line_ending = LINE_ENDINGS[flag] if flag else None

    def is_given(self) -> bool:
        return self.line_ending is not None

    def get_line_ending(self):
        return self.line_ending


class Limits:

    def get_wait_seconds(self) -> float:
        return 120

    def get_stale_seconds(self) -> float:
        return 120

    def get_poll_seconds(self) -> float:
        return 0.5


def plain(ref: str) -> Path:
    return _m_file_text.plain_path(ref)


def stored(path: Path):
    return _m_store.Text_Edit_Store_Held(path)


def named_text(source: str) -> str:
    return _m_codec.UTF8_Codec().decode_named(stored(Path(source).expanduser()).get_bytes())


def refuse_kept_scratch(source: Path) -> None:
    _m_task_memory = import_module('modules-plugable.management.task.services.task_memory')
    try:
        resolved = source.resolve()
    except OSError:
        return
    for folder in resolved.parents:
        if _m_task_memory.has_task(folder):
            relative = resolved.relative_to(folder)
            if relative.parts[0] != TEMP_FOLDER:
                raise ScratchInTaskFolder(f'the source {source} lies in task folder {folder.name} outside its {TEMP_FOLDER}/ folder, where it would be archived with the task as a second copy of what is written from it. Nothing was written. Put the scratch file in {folder / TEMP_FOLDER}/ and pass that.')
            return


def said(failure: Exception, subject: str) -> str:
    if isinstance(failure, _m_edit.Text_Error_Edit_OldEmpty):
        return 'the text to replace must not be empty; it would match everywhere'
    if isinstance(failure, _m_edit.Text_Error_Edit_MatchAbsent):
        return f'the text to replace does not occur in {subject}. Nothing was written. Check the exact text, including line endings and any dash character.'
    if isinstance(failure, _m_edit.Text_Error_Edit_MatchAmbiguous):
        return f'the text to replace occurs {failure.args[0]} times in {subject}. Nothing was written. Give more surrounding context to make it unique, or ask for every occurrence.'
    if isinstance(failure, _m_edit.Text_Error_Edit_EmptyText):
        return f'no text to write {subject}. Nothing was written. Empty input usually means nothing was delivered, not that the file should be emptied.'
    if isinstance(failure, _m_edit.Text_Error_Edit_CreateNotAsked):
        return f'{subject} is not an existing file. Nothing was written. Ask for creating if a new file is meant; a mistyped path would otherwise leave a stray file with no complaint.'
    if isinstance(failure, _m_edit.Text_Error_Edit_TextAbsent):
        return f'not a file: {subject}'
    if isinstance(failure, _m_edit.Text_Error_Edit_NotUtf8):
        return f'{subject} is not valid UTF-8 ({failure}). Nothing was written, because writing a decoded-with-replacement copy is how the damage spreads.'
    if isinstance(failure, _m_edit.Text_Error_Edit_NamedTextNotUtf8):
        return f'a named file is not valid UTF-8: {failure}'
    return str(failure)


def translated(call, subject: str):
    try:
        return call()
    except _m_edit.Text_Error_Edit_Error as failure:
        raise SystemExit(f'error: {said(failure, subject)}') from None


def replace_text(file: str, old: str | None=None, new: str | None=None, old_file: str | None=None, new_file: str | None=None, every: bool=False, newline: str | None=None) -> int:
    if old is None and old_file is None:
        raise NotNamed('edit needs the text to replace')
    if new is None and new_file is None:
        raise NotNamed('edit needs the replacement')
    path = plain(file)
    if is_content_file(path):
        raise ContentOfTask(f'{path.name} is a content of a task: a text of a task is added as a new content, never written over. Nothing was written.')

    def act():
        old_text = named_text(old_file) if old_file else old
        new_text = named_text(new_file) if new_file else new
        return _m_text_edit.Text_Edit().replace(stored(path), old_text, new_text, every, Choice(newline), _m_rule.Text_LineEnding_Rule(), _m_codec.UTF8_Codec(), _m_lock.Text_Edit_Lock_Held(), Limits(), _m_file_text.writer_id())
    found, had_mark = translated(act, path.name)
    if had_mark:
        print(f'note: {path.name} had a BOM; the write removes it')
    return found


def describe_edit(verbs):
    parser = verbs.add_parser('edit', help='replace exact text in a file, refusing an absent or ambiguous match', description='Replace exact text in FILE, refusing an absent or ambiguous match. Same encoding and newline guarantees as write; removes a BOM if it finds one. The read, the match, and the write happen under the per-file lock, so the text matched is the text written to.', formatter_class=argparse.HelpFormatter)
    parser.add_argument('file', help='path to edit (any path, not only in this repo)')
    parser.add_argument('--old', default=None, help='text to replace')
    parser.add_argument('--old-file', default=None, help='read the text to replace from this file')
    parser.add_argument('--new', default=None, help='replacement text')
    parser.add_argument('--new-file', default=None, help='read the replacement from this file')
    parser.add_argument('--all', action='store_true', help='replace every occurrence, not only a unique one')
    parser.add_argument('--newline', choices=['lf', 'crlf'], default=None)
    return guarded(run_edit)


def run_edit(args: argparse.Namespace) -> None:
    found = replace_text(args.file, old=args.old, new=args.new, old_file=args.old_file, new_file=args.new_file, every=args.all, newline=args.newline)
    print(f"edited {plain(args.file)} ({found} replacement{('s' if found > 1 else '')})")


def write_text(file: str, text: str | None=None, source: str | None=None, newline: str | None=None, create: bool=False) -> int:
    path = plain(file)
    if is_content_file(path):
        raise ContentOfTask(f'{path.name} is a content of a task: a text of a task is added as a new content, never written over. Nothing was written.')
    if source is not None:
        refuse_kept_scratch(Path(source).expanduser())
    elif text is None:
        raise NotNamed('write needs a text or a source file')
    existed = path.is_file()
    target = stored(path)
    service = _m_text_edit.Text_Edit()
    rule = _m_rule.Text_LineEnding_Rule()
    codec = _m_codec.UTF8_Codec()

    def act():
        if source is not None:
            return service.write_from(target, stored(Path(source).expanduser()), Choice(newline), create, rule, codec, _m_lock.Text_Edit_Lock_Held(), Limits(), _m_file_text.writer_id())
        return service.write(target, text, Choice(newline), create, rule, codec, _m_lock.Text_Edit_Lock_Held(), Limits(), _m_file_text.writer_id())
    size, had_mark = translated(act, path.name if source is None else f'{source} or {path.name}')
    if had_mark:
        print(f'note: {path.name} had a BOM; the write removes it')
    chosen = rule.detect(codec.decode_bare(target.get_bytes())).get_sequence()
    print(f"{('rewrote' if existed else 'wrote')} {path} ({size} bytes, utf-8, no BOM, {chosen!r} newlines)")
    return size


def describe_write(verbs):
    parser = verbs.add_parser('write', help='write a text file as UTF-8 without a BOM, preserving its newlines', description="Put text into FILE as UTF-8 with no BOM, keeping the file's own line endings (LF for a new file) and guaranteeing a final newline. Never put text into a file through a shell's own text handling. The write is taken under the per-file lock, so a cooperating task writing the same file is serialized rather than interleaved.", formatter_class=argparse.HelpFormatter)
    parser.add_argument('file', help='path to write (any path, not only in this repo)')
    parser.add_argument('--content-file', default=None, help='read the new text from this file instead of stdin')
    parser.add_argument('--newline', choices=['lf', 'crlf'], default=None, help="line ending; default is the file's own, or LF for a new file")
    parser.add_argument('--create', action='store_true', help='required to create a file that does not exist yet')
    return guarded(run_write)


def run_write(args: argparse.Namespace) -> None:
    text = None if args.content_file else sys.stdin.read()
    write_text(args.file, text=text, source=args.content_file, newline=args.newline, create=args.create)
