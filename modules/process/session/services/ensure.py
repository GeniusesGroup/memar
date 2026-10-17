#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/process/session/services/ensure.py — one session's folder, plan and report ensured, wherever the project keeps its sessions.

What `new` and `start` both ask: the folder is found or made in the location the project names, its
plan is written or kept (`session_plan_write`), its report and role folders are made, and the id and
path come back. The verb's own help and what it prints are in `session_new`.

A session writes only inside its own folder: --session-id reuses an id only to continue the same
session, and two sessions writing one folder reintroduce the unattributed mixing session folders
exist to remove. The parent a new session names must be a session folder that is there, because its
conversation is read from it. Where exactly a folder is made is asked of the project the plan
names (`session_location`), and the day's sweep runs when one is opened (`session_gc`), never
touching the session being opened or continued.
"""
from __future__ import annotations

from pathlib import Path

from machine.console import fail
from machine.fs_memar import session_dir
from modules.process.session.services.dependency import DependsOn, Reader, Ref, refused_for_writing
from modules.computer.module.services.folders import ensure_role_folders
from modules.knowledge.documentation.plan.primitive.priority import Priority
from modules.process.project.services.find import project_by_path
from modules.process.project.services.preferences import SESSIONS_KEY, preferences_path
from modules.process.session.services.folder import folder_of, project_folder_of, read_session
from modules.process.session.services.gc import reap_once_a_day
from modules.process.session.primitive.session_id import SessionId
from modules.process.session.services.location import in_project_location, project_location, project_root, register
from modules.process.session.services.log import record
from modules.knowledge.documentation.plan.services.plan import PLAN_NAME, checked_title
from modules.process.session.services.depends import BLOCKED_EVENT, reconcile
from modules.process.session.services.plan_depends import set_depends_on
from modules.process.session.services.plan_labels import TOPIC, add_label, checked_label, keep_definition, registry_for
from modules.process.session.services.plan_priority import set_priority
from modules.process.session.services.plan_write import queue_plan, write_plan
from modules.knowledge.documentation.report.services.report import write_report
from modules.process.session.services.label import warn_near
from modules.knowledge.documentation.primitive.label import Labels
from modules.knowledge.documentation.primitive.status import Status
from modules.process.project.primitive.project_name import ProjectName
from modules.knowledge.documentation.plan.primitive.plan_key import PlanKey


NEW_COMMAND = "new"
PROJECT_REQUIRED = (
    f"{NEW_COMMAND} needs {ProjectName.either_words()} to make a session: the project is always named, "
    "by a name `memar project find` resolves or by a folder, and the folder this runs in is never read; "
    "a session that is already there is continued without it"
)


def named_project(project: str | None) -> Path | None:
    """The project whose folder is PROJECT, its git top-level, or None when none was named.

    The flags (`add_project_flags`) have already turned a name into a folder;
    `project_by_path` refuses an empty value or one that is not a folder;
    nothing here reads the folder the process runs in.
    """
    if project is None:
        return None
    return project_root(project_by_path(project))


def recorded_project(folder: Path) -> Path | None:
    """The project FOLDER's plan records, when it names a folder that is there, else None."""
    named = ((read_session(folder).front or {}).get(PlanKey.PROJECT.key) or "").strip()
    if not named:
        return None
    where = Path(named)
    return where if where.is_dir() else None


def linked_conversation(session_id: str, parent: str) -> str:
    """The conversation a session opened from PARENT belongs to; PARENT must be a session folder."""
    if parent == session_id:
        fail("--parent names this session itself; name the session this task came from")
    folder = folder_of(parent)
    if not folder.is_dir():
        fail(f"no session folder {parent}: --parent names a session that is there, the one this task came from")
    return read_session(folder).conversation


def ensure_session(
    session_id: str | None = None,
    title: str | None = None,
    parent: str | None = None,
    queued: bool = False,
    priority: int | str | None = None,
    labels: list[str] | None = None,
    project: str | None = None,
    depends_on: list[str] | None = None,
) -> tuple[str, Path]:
    """Ensure the session's folder, its plan.md and report.md, and its role folders exist; return its id and path.

    TITLE is required when the folder has no plan.md yet, and unused when it
    has one. PARENT links a new plan to the session it came from; a plan that
    is there keeps the link it was written with, and a different one is
    refused rather than ignored. A rerun with the same id is idempotent: the
    folder, its plan, and its report are kept as they are and the same id and
    path are reported again. A session an earlier Memar left in temp/ is
    continued where it is; no second folder is made for it. A session in a project's
    own location is continued there. A folder that is nowhere yet is made in
    the location the project's preferences set, else temp/sessions/ inside the project (the Memar checkout's own is under Memar's root); a
    name already taken there by anything that is not a session folder is
    refused, and a location that cannot be made fails with a message. The
    first call of a day also reaps the session folders that have been idle past
    the limit, other than this one. QUEUED leaves a new plan queued, or queues
    an active one; PRIORITY, checked before anything is made, is written into a
    new plan or set on the one that is there; so are LABELS, each `KIND=WORD`
    checked against its kind before anything is made and added to the plan
    (several of one kind are kept, none is twice), and a topic near one the
    project uses is warned about, not refused.

    PROJECT, a name or a folder, is required to make a folder, and an empty
    one is refused: the project is always named, and the folder the process
    runs in is never read. A folder that is there is continued without it, its
    project the one its plan records.

    DEPENDS_ON, references to sessions, are checked before anything is made
    (`depends_on.refused_for_writing`) and added to the plan's key; a new
    session with an unmet one is written Blocked, and an existing queued one
    becomes Blocked (`session_depends`).
    """
    priority = None if priority is None else Priority.checked(priority)
    cited = DependsOn.normalized(Ref.parse(word) for word in depends_on or [])
    sid = SessionId.new() if session_id is None else session_id
    folder = session_dir(sid)
    project = named_project(project)
    location = project_location(project) if project is not None else None
    if session_id is not None and not folder.is_dir():
        folder = project_folder_of(sid, also=location) or folder
    if project is None and folder.is_dir():
        project = recorded_project(folder)
        location = project_location(project) if project is not None else None
    if project is None and not (folder.is_dir() and (folder / PLAN_NAME).is_file()):
        fail(PROJECT_REQUIRED)
    if not folder.is_dir() and location is not None:
        folder = location / sid
        if folder.exists() or folder.is_symlink():
            fail(
                f"{folder} is there and is not a session folder; `new` never writes into it. "
                "Pass --session-id a name not used in that location, or none to mint one"
            )
    given, kept = None, []
    if labels is not None:
        given, registry = Labels(), registry_for(project)
        for text in labels:
            label, fresh = checked_label(text, project, registry)
            if fresh is not None:
                registry.add(fresh)
                kept.append(fresh)
            given = given.with_label(label)
    existed = folder.is_dir()
    has_plan = (folder / PLAN_NAME).is_file()
    title = checked_title(title, required=not has_plan)
    parent = (parent or "").strip() or None
    conversation = None
    if parent is not None:
        if has_plan:
            recorded = read_session(folder).parent
            if recorded != parent:
                fail(
                    f"session {sid} was opened with parent {recorded or '(none)'}; "
                    "a session's link is written once, with its plan"
                )
        else:
            conversation = linked_conversation(sid, parent)
    reader = Reader(project)
    now = DependsOn.normalized([*(DependsOn.of(read_session(folder).front) if has_plan else ()), *cited])
    if cited:
        refused_for_writing(sid, now, reader, cited)
    for fresh in kept:
        if project is not None:
            keep_definition(project, fresh)
    path = folder
    if not existed:
        try:
            path.mkdir(parents=True, exist_ok=True)
        except OSError as error:
            where = f"; check `{SESSIONS_KEY}` in {preferences_path(project)}" if location is not None and project is not None else ""
            fail(f"the session folder {path} could not be made ({error.strerror or error}){where}")
        record("opened", sid, f"parent {parent}" if parent else "", folder=path)
    if in_project_location(path):
        register(path.parent, project)
    if not has_plan:
        waits = bool(cited) and bool(reader.unmet(cited))
        status = Status.BLOCKED.key if waits else Status.QUEUED.key if queued else Status.ACTIVE.key
        write_plan(path, sid, title, parent, conversation, project, status, priority, given, now.text() or None)
        if waits:
            record(BLOCKED_EVENT, sid, "; ".join(reader.unmet(cited)), folder=path)
    else:
        if queued:
            queue_plan(path)
        if priority is not None:
            set_priority(path / PLAN_NAME, priority)
        for label in given or ():
            add_label(path / PLAN_NAME, label)
        if cited:
            set_depends_on(path / PLAN_NAME, now)
            reconcile(read_session(path), reader)
    if project is not None:
        for label in given or ():
            if any(taken.word == TOPIC for taken in registry_for(project).kinds_of(label)):
                warn_near(label.word, project, sid)
    write_report(path, sid, (read_session(path).front or {}).get(PlanKey.TITLE.key))
    ensure_role_folders(path)
    reap_once_a_day(keep=sid)
    return sid, path
