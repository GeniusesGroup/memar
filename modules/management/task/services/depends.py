#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/management/task/services/depends.py — the verb `memar task depends-on`, and the Status a session's dependencies give it.

What a dependency is, when it is met, and how it is checked is the type's
(`modules/management/task/services/dependency.py`); writing the key is `session_plan_depends`. This file
decides what the key does to a session, and says it.

The Status of a session with dependencies. An unmet `Depends_on` makes the
session Blocked, the Status word that already means "cannot continue until a
dependency arrives; the record states what it waits for" (`memar session
--help`), and the record states it: the key holds the ids, and every verb that
shows the session prints each with where it stands. No Status word is added.

How the Status is kept truthful. A stored Status is a fact that goes stale
when the session it waits for ends, and the one that ends must not write
another session's folder. So the Status is set when the key is written and
brought up to date by every verb that reads sessions to decide or to show
(`claim`, `claims`, `list`, `digest`) through `reconcile`, which does two things
and nothing else:
- a Queued session with an unmet dependency becomes Blocked;
- a Blocked session whose every dependency is now met becomes Queued again,
  but only one that Memar itself blocked for its dependencies, which the
  session log says (`BLOCKED_EVENT`, `RELEASED_EVENT`); dropping the last
  dependency leaves none unmet, so it is released the same way. A session blocked by
  hand, or a coordinator's own plan blocked on the sessions it waits for, is
  never put back in line behind its agent's back: `list` and `digest` say that
  every dependency is Complete and it can resume.
An Active session is never changed: it is running, and its agent sets Blocked
when it cannot go on. Once released, a session is an ordinary queued one:
`claim` and `claims` take it, and it goes Active on the claim.

A session whose dependency is not met cannot be claimed or started
(`refusal`), whatever its Status, and the refusal names the unmet ids and how
each stands; one that no longer resolves keeps it unclaimable until the key is
dropped, and the refusal says so.
"""
from __future__ import annotations
from machine.plugable_import import load as plugable_load
from pathlib import Path
from typing import Iterable
from modules.management.task.services.dependency import ARROW, DEPENDS_FOR, DependsOn, Reader, dependents
from modules.management.task.services.folder import Session, read_session
_m_log = plugable_load('computer.git.services.log')
log_path = _m_log.log_path
record = _m_log.record
from modules.knowledge.documentation.plan.services.plan import PLAN_NAME
from modules.knowledge.documentation.plan.services.status import set_status
from modules.knowledge.documentation.plan.primitive.plan_key import PlanKey
from modules.knowledge.documentation.primitive.status import Status
DEPENDS_COMMAND = PlanKey.DEPENDS_ON.key.replace('_', '-')
BLOCKED_EVENT = 'blocked-by-dependency'
RELEASED_EVENT = 'released-by-dependency'

def home_of(session: Session) -> Path | None:
    """The project SESSION's plan names, when it is a folder that is there; where its local references are looked for."""
    named = (session.front or {}).get(PlanKey.PROJECT.key, '').strip()
    return Path(named) if named and Path(named).is_dir() else None

def problems(session: Session, reader: Reader) -> list[str]:
    """Why SESSION's dependencies are not met, one reason each, a cycle among them; none when it has none or all are met."""
    refs = DependsOn.of(session.front)
    if not refs:
        return []
    home = home_of(session)
    reasons = reader.unmet(refs, home)
    path = reader.cycle(session.id, refs, home)
    if path:
        reasons.append(f'a dependency cycle {ARROW.join(path)}')
    return reasons

def blocked_by_memar(folder: Path) -> bool:
    """Whether the session log's last word on FOLDER's session about its dependencies is that Memar blocked it."""
    try:
        lines = log_path(folder).read_text(encoding='utf-8').splitlines()
    except (OSError, UnicodeDecodeError):
        return False
    for line in reversed(lines):
        fields = line.split('\t')
        if len(fields) >= 3 and fields[2] == folder.name and (fields[1] in (BLOCKED_EVENT, RELEASED_EVENT)):
            return fields[1] == BLOCKED_EVENT
    return False

def reconcile(session: Session, reader: Reader) -> str:
    """Bring SESSION's Status up to date with its dependencies, as the module says; the Status it has now."""
    if not (session.has_plan and session.readable):
        return session.status
    if session.status not in (Status.QUEUED.key, Status.BLOCKED.key):
        return session.status
    if not DependsOn.of(session.front) and (not (session.status == Status.BLOCKED.key and blocked_by_memar(session.path))):
        return session.status
    unmet = problems(session, reader)
    plan = session.path / PLAN_NAME
    try:
        if unmet and session.status == Status.QUEUED.key:
            set_status(plan, Status.BLOCKED.key, expected=(Status.QUEUED.key,))
            record(BLOCKED_EVENT, session.id, '; '.join(unmet), folder=session.path)
            return Status.BLOCKED.key
        if not unmet and session.status == Status.BLOCKED.key and blocked_by_memar(session.path):
            set_status(plan, Status.QUEUED.key, expected=(Status.BLOCKED.key,))
            record(RELEASED_EVENT, session.id, '', folder=session.path)
            return Status.QUEUED.key
    except SystemExit:
        return read_session(session.path).status
    return session.status

def reconcile_all(sessions: Iterable[Session]) -> None:
    """`reconcile` each of SESSIONS that has dependencies, with one reader so each cited session is read once."""
    reader = Reader(None)
    for session in sessions:
        reconcile(session, reader)

def refusal(folder: Path, act: str) -> str | None:
    """Why the session at FOLDER cannot be ACT'ed (`claim`, `start`) for its dependencies, naming each; None when it can.

    The Status is brought up to date first, so the refusal and the Status agree.
    """
    session = read_session(folder)
    if not (session.has_plan and session.readable) or not DependsOn.of(session.front):
        return None
    reader = Reader(None)
    unmet = problems(session, reader)
    reconcile(session, reader)
    if not unmet:
        return None
    return f"session {session.id} depends on {', '.join(unmet)}, so it cannot be {act}ed until each is Complete; a dependency that cannot be found stays until it is dropped with `memar task {DEPENDS_COMMAND} {session.id} --drop REF`"

def labelled(refs: DependsOn, reader: Reader, home: Path | None) -> str:
    """REFS each with where it stands, `ref (state)`, as the plan's key is shown."""
    parts = []
    for ref in refs:
        found = reader.find(ref, home)
        state = found.split(':')[0] if isinstance(found, str) else 'complete' if found.met else found.state
        parts.append(f'{ref} ({state})')
    return ', '.join(parts)

def notes_for(session: Session, reader: Reader, everyone: Iterable[Session]) -> list[str]:
    """The lines `list` shows under SESSION for its dependencies and for the sessions that depend on it; none when it has neither."""
    refs = DependsOn.of(session.front)
    lines = []
    if refs:
        lines.append(f'{PlanKey.DEPENDS_ON.written}: {labelled(refs, reader, home_of(session))}')
    cited_by = dependents(session.id, everyone)
    if cited_by:
        lines.append(f"{DEPENDS_FOR}: {', '.join(cited_by)}")
    return lines

def concerns_for(session: Session, reader: Reader) -> list[str]:
    """What SESSION's dependencies say that its reader should know: a cycle, a dependency that cannot be found, and a blocked session that can resume."""
    refs = DependsOn.of(session.front)
    if not refs or not (session.has_plan and session.readable):
        return []
    home = home_of(session)
    found = []
    for ref in refs:
        why = reader.find(ref, home)
        if isinstance(why, str):
            found.append(f'{PlanKey.DEPENDS_ON.written} {ref}: {why}; it stays unclaimable until the key is dropped')
    path = reader.cycle(session.id, refs, home)
    if path:
        found.append(f'{PlanKey.DEPENDS_ON.written} makes a cycle: {ARROW.join(path)}')
    if session.status == Status.BLOCKED.key and (not problems(session, reader)):
        found.append(f'blocked, and every {PlanKey.DEPENDS_ON.written} is Complete: it can resume')
    elif session.status == Status.BLOCKED.key:
        found.append(f'blocked by {PlanKey.DEPENDS_ON.written}: ' + '; '.join(problems(session, reader)))
    return found
