#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/process/session/services/show.py — a session's plan and report, or the files an agent asks for, wherever they are.

A session's folder is scratch and goes once its task is done; its records stay
on its project's records branch (`session_archive`). A reader who has a session
id from a changelog, a handoff or a report wants what the session said, not to
know which of the two places holds it today, so one command returns it (owner,
2026-10-15): the folder in the main repository's temp first, because while the
folder exists it is the session's latest state, then the branch. Each file is
looked for in that order on its own, and each is printed under a line naming
where it came from, so a reader of a folder that has moved on past what was
archived sees which is which.

A file is named by its path from the session's folder, never by one that
leaves it; the branch is read with git's read-only commands, in the project
told by `--project` or `--project-path`, never the folder this runs in.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path, PurePosixPath
from typing import Callable

from machine.console import fail
from machine.fs_memar import RECORDS_BRANCH
from modules.process.session.services import branch as session_branch
from modules.process.project.services.find import add_project_flags, project_from_args
from modules.process.session.services.branch import folder_on_branch, reference
from modules.process.session.services.dependency import Reader
from modules.process.session.services.depends import concerns_for, home_of, notes_for
from modules.process.session.services.find import find_sessions
from modules.process.session.services.folder import folder_of, read_session
from modules.knowledge.documentation.plan.services.plan import PLAN_NAME, read_plan
from modules.knowledge.documentation.report.services.report import REPORT_NAME, decisions_needed, handback_problem, read_report_status
from modules.process.project.primitive.project_name import ProjectName

SHOW_COMMAND = "show"
PROJECT_REQUIRED = f"name the project the session belongs to with {ProjectName.either_words()}: the branch is the project's"


def _relative(path: str) -> str:
    """PATH as a plain relative path from the session's folder, refused when it could leave it."""
    posix = path.replace("\\", "/")
    parts = PurePosixPath(posix).parts
    if not path or posix.startswith("/") or ":" in posix or any(part in ("..", ".") for part in parts):
        fail(f"{path!r} is not a path inside the session's folder; name it from the folder, like docs/note.md")
    return PurePosixPath(posix).as_posix()


def listing(session_id: str, project_path: Path) -> list[str]:
    """The files the session has: those in its folder when it is in temp, else those the branch holds for it."""
    folder = folder_of(session_id)
    if folder.is_dir():
        return sorted(
            each.relative_to(folder).as_posix() for each in folder.rglob("*") if each.is_file() and not each.is_symlink()
        )
    found = sorted(session_branch.held(project_path, session_id))
    if not found:
        fail(f"no session {session_id}: not in temp, and {RECORDS_BRANCH} of {project_path} holds nothing for it")
    return found


def show(session_id: str, project_path: Path, files: list[str]) -> None:
    """Print each of FILES (the plan and the report when none) of SESSION_ID, its folder first and then the branch."""
    folder = folder_of(session_id)
    names = [_relative(each) for each in files] or [PLAN_NAME, REPORT_NAME]
    printed = 0
    for name in names:
        local = folder / name
        if folder.is_dir() and local.is_file():
            source, data = str(local), local.read_bytes()
        else:
            data = session_branch.read(project_path, session_id, name)
            source = f"{reference(session_id)}{name}"
        if data is None:
            where = f"in {folder}, and " if folder.is_dir() else ""
            fail(
                f"{name} of session {session_id} is not {where}on the branch {RECORDS_BRANCH} of {project_path} "
                f"({folder_on_branch(session_id)}/{name}); `show --list` names the files it has"
            )
        try:
            text = data.decode("utf-8-sig")
        except UnicodeDecodeError:
            fail(f"{name} of session {session_id} is not text, so it is not printed")
        sys.stdout.write(f"=== {name} ({source})\n{text}")
        if not text.endswith("\n"):
            sys.stdout.write("\n")
        sys.stdout.write("\n")
        printed += 1
    if not files and (folder / PLAN_NAME).is_file():
        dependency_lines(read_session(folder), project_path)


def dependency_lines(session, project_path: Path) -> None:
    """Print, under the plan, where each of SESSION's dependencies stands and which sessions depend on it (derived, from Memar's sessions and the project's); nothing when neither."""
    reader = Reader(home_of(session) or project_path)
    everyone = {each.id: each for each in [*find_sessions(), *find_sessions(project=project_path)]}
    lines = [*notes_for(session, reader, everyone.values()), *(f"concerns: {each}" for each in concerns_for(session, reader))]
    if lines:
        sys.stdout.write("=== dependencies\n" + "\n".join(lines) + "\n\n")


def hand_back(session_id: str) -> None:
    """Print SESSION_ID's hand-back alone: its Status, its report's path, and its `Decisions needed` lines; none of the rest of the report.

    Read from the session's folder, where a session that has just ended is; a
    report that is not a hand-back is named, with why, after what it does hold.
    """
    folder = folder_of(session_id)
    if not folder.is_dir():
        fail(f"session {session_id} has no folder in temp, so there is no hand-back to read; `show --file {REPORT_NAME}` reads it from the branch")
    plan_status = read_plan(folder / PLAN_NAME).status
    lines = [f"Status: {read_report_status(folder) or '(none)'}", f"Report: {folder / REPORT_NAME}", *decisions_needed(folder)]
    problem = handback_problem(folder, plan_status)
    if problem:
        lines.append(f"Not a hand-back: {problem}")
    sys.stdout.write("\n".join(lines) + "\n")


def describe(verbs) -> Callable[[argparse.Namespace], None]:
    """`memar session show`."""
    shower = verbs.add_parser(
        SHOW_COMMAND,
        help="print a session's plan and report, or files of it, from its folder or the records branch",
        description=(
            f"Print the {PLAN_NAME} and the {REPORT_NAME} of the session SESSION_ID, or the files named with\n"
            "--file, each under a line saying where it came from. A file is read from the\n"
            "session's folder in the main repository's temp when it is there, and then from\n"
            f"the branch {RECORDS_BRANCH} of the project, where `archive` kept it. Use it for a session\n"
            "id a changelog, a handoff or a report cites: it needs no knowledge of which\n"
            "place holds the session today. A file is named by its path from the\n"
            "session's folder, like docs/note.md; --list prints the files the session has\n"
            "instead. The project's branch is read, never the folder this runs in."
        ),
    )
    shower.add_argument("--session-id", required=True, help="the session whose records to print")
    shower.add_argument(
        "--file",
        action="append",
        default=[],
        metavar="PATH",
        help=f"a file of the session, by its path from the session's folder; may be repeated; without it, {PLAN_NAME} and {REPORT_NAME}",
    )
    shower.add_argument("--list", action="store_true", help="print the names of the files the session has, one a line, instead of their text")
    shower.add_argument(
        "--hand-back",
        action="store_true",
        help="print only the session's hand-back: the report's Status, its path and its Decisions needed lines, and why it is not one when it is not",
    )
    add_project_flags(shower, "the project the session belongs to", required=True)
    return run


def run(args: argparse.Namespace) -> None:
    project = project_from_args(args)
    if project is None:
        fail(PROJECT_REQUIRED)
    if args.hand_back:
        hand_back(args.session_id)
        return
    if args.list:
        for name in listing(args.session_id, project):
            sys.stdout.write(f"{name}\n")
        return
    show(args.session_id, project, args.file)
