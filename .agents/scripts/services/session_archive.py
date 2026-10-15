#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/session_archive.py — a session's records kept in its project, to be committed with its work.

A live session folder is scratch: it is swept once its task is done, and it
holds a claim that means nothing on another clone. Its record is not scratch:
changelogs and handoffs cite session ids, and a cited id whose folder the sweep
has sent to the trash cites nothing. So the two are two concerns with two
locations (owner, 2026-10-14): the folder stays where it is and goes as it
always went, and before it goes — when the task's changes are committed, when
`close` moves it, and when the sweep moves it — its records are copied to
`.agents/sessions/<id>/` in its project (`machine/fs_memar.RECORDS_RELATIVE`),
which the project's VCS keeps.

The records are the plan, the report, and each file inside the folder the
report links to with a relative Markdown link: the report is where a session
says what it made, and a link is how it says that a file is part of what it
made rather than scratch it mentions. The claim is not kept, and the copied
plan names its project by the project's registered name rather than by the
path it has on the computer that opened it: the path means nothing elsewhere,
and `memar project find` turns the name into this computer's path. Every other
byte of the plan, and the report and the linked files, are copied as written.

Which project is the plan's `Project`, as `session_new` wrote it: a folder.
Every project keeps its records unless its preferences say `records: off`
(`project_preferences`, a key separate from `sessions`). What cannot be kept —
a project folder not on this computer, a project with no registered name, a
`records` value it may not take, a write that fails — is refused with why, and
the caller that would move the folder leaves it where it is: a record dropped
without a word is the defect this file exists to end. A folder with no plan,
or a plan naming no project, has no project to keep anything in, and owes
nothing.

`archive` is the verb a coordinator runs before committing a task: it keeps the
records of the session named and of every session whose Parent chain leads to
it — the sessions it handed work to — and prints where each one's records are,
so they are named in the commit. The copy is idempotent: keeping again writes
what the folder holds now.
"""
from __future__ import annotations

import argparse
import re
from enum import Enum
from pathlib import Path
from typing import Callable, NamedTuple
from urllib.parse import unquote

from machine.console import fail, note
from machine.fs_memar import RECORDS_RELATIVE
from services.project_preferences import RECORDS_KEY, Records, preferences_path, read_preferences, records_preference
from services.project_registry import read_entries
from services.session_folder import Session, folder_of, read_session, session_folders
from services.session_layout import TOP_NAMES
from services.session_location import same_path
from services.session_plan import PLAN_NAME
from services.session_record import PlanKey
from services.session_report import REPORT_NAME

ARCHIVE_COMMAND = "archive"

# A Markdown link's target: `[text](target)` or `[text](target "title")`.
_LINK = re.compile(r"\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")


class Outcome(Enum):
    """How keeping one session's records ended."""

    KEPT = "kept"
    NOT_OWED = "not owed"
    REFUSED = "refused"


class Kept(NamedTuple):
    """One session's keeping: how it ended, where its records are when kept, why when not, and the files kept, relative to the folder."""

    outcome: Outcome
    folder: Path | None
    why: str = ""
    files: tuple[Path, ...] = ()


def _project_of(session: Session) -> str:
    return (session.front or {}).get(PlanKey.PROJECT.key, "").strip()


def project_name(project: Path) -> str | None:
    """PROJECT's own registered name, the first on its entry; None when it has no entry."""
    entry = next((each for each in read_entries() if same_path(each.path, project)), None)
    return entry.names[0] if entry is not None and entry.names else None


def linked_files(folder: Path) -> list[Path]:
    """The files inside FOLDER its report links to, other than the folder's top files, each once, in the order linked.

    A link with a scheme, an absolute or anchor-only target, or one that
    resolves outside FOLDER or to no file is not a record of this session.
    """
    try:
        text = (folder / REPORT_NAME).read_bytes().decode("utf-8-sig")
    except (OSError, UnicodeDecodeError):
        return []
    root = folder.resolve()
    found: list[Path] = []
    for match in _LINK.finditer(text):
        target = unquote(match.group(1).split("#", 1)[0])
        if not target or ":" in target or target.startswith(("/", "\\")):
            continue
        path = (folder / target).resolve()
        if not path.is_relative_to(root) or not path.is_file() or path == root:
            continue
        relative = path.relative_to(root)
        if len(relative.parts) == 1 and relative.name in TOP_NAMES:
            continue
        if relative not in found:
            found.append(relative)
    return found


def _named_plan(data: bytes, name: str) -> bytes:
    """The plan bytes DATA with its front matter's Project value replaced by NAME, every other byte as written."""
    lines = data.decode("utf-8-sig").splitlines(keepends=True)
    key = f"{PlanKey.PROJECT.written}:"
    if lines and lines[0].strip() == "---":
        for index in range(1, len(lines)):
            line = lines[index]
            if line.strip() == "---":
                break
            if line.startswith(key):
                ending = line[len(line.rstrip("\r\n")):]
                lines[index] = f"{key} {name}{ending}"
                break
    return "".join(lines).encode("utf-8")


def _write(path: Path, data: bytes) -> None:
    """Put DATA at PATH, making its folder; a file already holding DATA is left as it is."""
    if path.is_file() and path.read_bytes() == data:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def keep_records(folder: Path, *, write: bool = True) -> Kept:
    """Copy FOLDER's records to its project's .agents/sessions/<id>/, or say why they are not owed or cannot be kept.

    Unless WRITE, nothing is written, and what would be is returned: a dry run.
    """
    session = read_session(folder)
    if not session.has_plan:
        return Kept(Outcome.NOT_OWED, None, f"it has no {PLAN_NAME}")
    if not session.readable or session.front is None:
        return Kept(Outcome.REFUSED, None, f"its {PLAN_NAME} cannot be read, so its project is not known")
    named = _project_of(session)
    if not named:
        return Kept(Outcome.NOT_OWED, None, f"its {PLAN_NAME} names no project to keep its records in")
    project = Path(named)
    if not project.is_dir():
        return Kept(Outcome.REFUSED, None, f"its project {named} is not a folder on this computer")
    preference = records_preference(project)
    if preference is None:
        return Kept(
            Outcome.REFUSED,
            None,
            f"`{RECORDS_KEY}: {read_preferences(project).get(RECORDS_KEY, '')}` in {preferences_path(project)} "
            f"is none of {Records.listing()}, or empty",
        )
    if preference is Records.OFF:
        return Kept(Outcome.NOT_OWED, None, f"its project's preferences say `{RECORDS_KEY}: {Records.OFF.value}`")
    name = project_name(project)
    if name is None:
        return Kept(
            Outcome.REFUSED,
            None,
            f"its project {project} has no registered name to write in the kept plan; "
            "give it one with `memar project add`",
        )
    where = project / RECORDS_RELATIVE / folder.name
    files = (Path(PLAN_NAME), *((Path(REPORT_NAME),) if (folder / REPORT_NAME).is_file() else ()), *linked_files(folder))
    if not write:
        return Kept(Outcome.KEPT, where, files=files)
    try:
        for relative in files:
            data = (folder / relative).read_bytes()
            _write(where / relative, _named_plan(data, name) if relative == Path(PLAN_NAME) else data)
    except OSError as error:
        return Kept(Outcome.REFUSED, where, f"its records could not be written to {where} ({error})")
    return Kept(Outcome.KEPT, where, files=files)


def related_sessions(folder: Path) -> list[Path]:
    """FOLDER and every session folder whose Parent chain leads to it, FOLDER first, each once."""
    children: dict[str, list[Path]] = {}
    for entry in session_folders(projects=True):
        parent = read_session(entry).parent
        if parent:
            children.setdefault(parent, []).append(entry)
    found = [folder]
    for each in found:
        for child in children.get(each.name, []):
            if all(child.resolve() != known.resolve() for known in found):
                found.append(child)
    return found


def archive(session_id: str) -> None:
    """`archive`: keep the records of SESSION_ID and of the sessions it handed work to, and say where each is."""
    folder = folder_of(session_id)
    if not folder.is_dir():
        fail(f"no session folder {session_id} was found")
    refused: list[str] = []
    for each in related_sessions(folder):
        kept = keep_records(each)
        if kept.outcome is Outcome.KEPT:
            note(f"kept: {each.name}")
            note(f"records: {kept.folder}")
        elif kept.outcome is Outcome.NOT_OWED:
            note(f"not kept, {kept.why}: {each.name}")
        else:
            note(f"refused, {kept.why}: {each.name}")
            refused.append(each.name)
    if refused:
        fail(f"the records of {', '.join(refused)} could not be kept; commit none of this task until they are")


def describe(verbs) -> Callable[[argparse.Namespace], None]:
    """`memar session archive`."""
    parser = verbs.add_parser(
        ARCHIVE_COMMAND,
        help="copy a session's records into its project, to commit with the task's work",
        description=(
            f"Copy the records of the session SESSION_ID — its {PLAN_NAME}, its {REPORT_NAME}, and each\n"
            "file inside its folder the report links to with a relative link — to\n"
            f"{RECORDS_RELATIVE.as_posix()}/<id>/ in the project its plan names, and do the same for\n"
            "every session whose Parent chain leads to it. The copied plan names the\n"
            "project by its registered name, not by its path; the claim is not copied.\n"
            "Each kept session's records folder is printed: run this before committing\n"
            "a task, and name those folders in the commit. A project whose preferences\n"
            f"say `{RECORDS_KEY}: {Records.OFF.value}` keeps none. A session whose records cannot be kept\n"
            "is named with why, and the verb fails."
        ),
    )
    parser.add_argument("--session-id", required=True, help="the session whose task is being committed")
    return run


def run(args: argparse.Namespace) -> None:
    archive(args.session_id)
