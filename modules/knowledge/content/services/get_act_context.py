#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/knowledge/content/services/get_act_context.py — `memar content get-act-context`: the sections a kind of act requires, with or without a session.

`memar ai get-task-init-context` prints a session's context from its plan's Kind; this
prints the same composition (`modules/knowledge/content/services/task_context.py`), from the lists of
[Normative References](../rules/normative_references/normative_references.md),
for kinds given on the command line: for a question answered in chat, which
opens no session, or for a session whose act changes midway — from design to
implementing, or a coordinator about to queue other sessions — which reads what
the new kind adds with `--after` the kinds it already read.

**`--after` needs `--task-id`.** What a context printed is recorded in the
session's own folder, and `--after` leaves out only what that record holds as
printed with the section's hash as it reads now; with no session there is no
record, so `--after` alone is refused rather than guessed from what the earlier
kinds' lists say now. With `--task-id`, what this prints is added to the
record once its last part is printed, so every part of one text is composed
from the same record.

The kinds and when each applies are `modules/knowledge/documentation/plan/labels/task_kind.py`'s, and the help
lists them from there. A composition too long for one tool output prints in
ordered parts through `machine/console_parts.py`, each of its blocks a section
a part is cut between. The project whose preferences set the bound is named by
its flag, read in the folder as given; with none named, the default bound holds
and the first line says Memar's lists alone are read. The same project's `normative_references`
preference names the folders its own lists are read in, beside Memar's.
"""
from __future__ import annotations
import argparse
from machine.console_parts import add_part_arguments
from modules.process.project.services.find import add_project_flags
from modules.process.project.primitive.project_name import ProjectName
from modules.process.project.primitive.project_path import ProjectPath
from modules.process.project.services.preferences import MOST_CHARACTERS_KEY, PREFERENCES_RELATIVE
from modules.knowledge.documentation.plan.labels.task_kind import TaskKind
COMMAND = 'get-act-context'
SESSION_FLAG = '--task-id'
AFTER_FLAG = '--after'
AFTER_REFUSED = f"{AFTER_FLAG} needs {SESSION_FLAG}: the record of what was printed is the session's"

def _word(value: str) -> str:
    """VALUE as one word of a command a reader runs: quoted when it holds a space."""
    return f'"{value}"' if any((character.isspace() for character in value)) else value

def _kinds_listing() -> str:
    return '\n'.join((f'  {kind.word}: {kind.applies}' for kind in TaskKind))

def describe(verbs):
    parser = verbs.add_parser(COMMAND, help="print the passages of Memar's documents a kind of act requires read", description=f"""Print the sections the normative references of the given kinds name, the lists in\nmodules/knowledge/content/rules/normative_references/: the every-act list's, then each kind's in the\norder given, each section once under a line naming it and its entry's why, and a Practice's\ndescription once above its first section. The first line counts what it holds. It is what\n`memar ai get-task-init-context` prints for a plan's Kind, for an act with no session — a question\nanswered in chat — or one that changes midway.\n\nWith {SESSION_FLAG}, what is printed is recorded in that session's temp/ folder; {AFTER_FLAG} K0\nthen leaves out the sections of K0's lists that record holds as printed with the same hash,\nso a section changed since, or added since, prints. {AFTER_FLAG} without {SESSION_FLAG} is refused.\n\nA text too long for one tool output prints in ordered parts, each at most --most-characters\nlong: each part but the last ends with the exact command for the next (--part N), to run\nat once; read every part before acting. The same kinds print the same parts, and each\npart says "part N of M of text H", H a hash of the whole text: a part naming another H\nis of another version of it.\n\nThe kinds, and when each applies:\n{_kinds_listing()}""")
    add_project_flags(parser, 'the project whose preferences set the most characters a part holds')
    parser.add_argument('--kind', action='append', required=True, choices=TaskKind.words(), metavar='K', help='a kind of act whose sections to print; repeat for several')
    parser.add_argument(AFTER_FLAG, action='append', default=[], choices=TaskKind.words(), metavar='K0', help=f'a kind whose sections were already read in the session {SESSION_FLAG} names; repeat for several')
    parser.add_argument(SESSION_FLAG, dest='task_id', metavar='ID', help='the session this context is printed for: what it prints is recorded there, and --after reads that record')
    add_part_arguments(parser, f'the `{MOST_CHARACTERS_KEY}` in the {PREFERENCES_RELATIVE.as_posix()} of the project named')
    return run

def run(args: argparse.Namespace) -> None:
    from machine.console import fail
    from machine.console_parts import bound, cut, next_command, print_part
    from modules.knowledge.content.services.reference import content_root
    from modules.process.project.services.find import project_from_args
    from modules.process.project.services.preferences import most_characters_preference
    from machine.modules_import import load as modules_load
    _folder = modules_load('management', 'task', 'services', 'folder')
    folder_of, is_task_folder = (_folder.folder_of, _folder.is_task_folder)
    from modules.knowledge.content.services.task_context import context, context_places, read_record, write_record
    if args.after and args.task_id is None:
        fail(AFTER_REFUSED)
    folder = None
    if args.task_id is not None:
        folder = folder_of(args.task_id)
        if not is_task_folder(folder):
            fail(f'{SESSION_FLAG} {args.task_id}: no such session folder')
    kinds = [TaskKind.read(word) for word in args.kind]
    after = [TaskKind.read(word) for word in args.after]
    project = project_from_args(args)
    places, problems = context_places(content_root(), project)
    composed = context(places, kinds, after, read_record(folder) if folder else frozenset(), project_named=project is not None, place_problems=problems)
    blocks = composed.blocks
    if len(blocks) == 1:
        print(f"Every section {', '.join(args.kind)} requires was already printed for {', '.join(args.after)}.")
        return
    passages = [block + '\n\n' for block in blocks[:-1]] + [blocks[-1] + '\n']
    named = [ProjectName.FLAG, _word(args.project)] if args.project is not None else [ProjectPath.FLAG, _word(args.project_path)] if args.project_path is not None else []
    session = [SESSION_FLAG, args.task_id] if args.task_id is not None else []
    words = ['memar', 'content', COMMAND, *(f'--kind {word}' for word in args.kind), *(f'{AFTER_FLAG} {word}' for word in args.after), *session, *named]
    preferred = most_characters_preference(project)
    print_part(passages, args, words, preferred)
    if folder is not None and args.part == len(cut(passages, bound(args.most_characters, preferred), next_command(words, args.most_characters))):
        write_record(folder, composed.printed)
