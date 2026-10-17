#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/depends_on.py — a plan's dependencies, declared once: the sessions that must be Complete before it can start.

A plan's `Depends_on` is the sessions it cannot start without, as
[Documentation → Citations](../../../modules/content/documentation/documentation.md#citations)
uses the word for documents ("cannot be implemented or understood without the
cited work"), stronger in time for a session: it cannot start until each cited
session is Complete. The key is declared once, as `PlanKey.DEPENDS_ON`
(`session_record`); its inverse, `Depends_for`, is declared here once and is
derived from the plans that cite a session, never written. Renaming either is
one edit.

What the type holds. The value is ids, comma-separated, on one line, each `ID`
for a session of the plan's own project or `project/ID` for one of another
project the owner works on beside it. A project is resolved the way
`memar project find` resolves a name and never guessed from a path; one that
does not resolve is refused, with why. Why a session waits goes in the plan's
Next, as before: the key holds ids alone.

When a dependency is met. The cited session's plan and its report both state
Complete ([Status](../../../modules/content/documentation/documentation.md#status):
only Complete is safe to depend on, and a plan and its report must agree). A
session that no longer resolves (deleted, or archived and gone from the
project's records branch) is not met, and says so: it stays unmet until the key
is dropped. A closed session is read from its project's records branch, where
`archive` kept it (`session_branch`).

Cycles. A plan is refused a dependency that would let it be reached from
itself, at any length, and the refusal names the path. A cycle written by hand
is met when read: each session in it is unmet and the path is named.

This file only reads and checks. Writing the key is `session_plan_depends`,
the Status a dependency gives a session is `session_depends`.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import ClassVar, Iterable, NamedTuple

from machine.console import fail
from services.project_find import project_by_name
from services.project_path import ProjectPath
from services.session_branch import read as read_from_branch
from services.session_folder import folder_of
from services.session_plan import PLAN_NAME, front_key, front_matter, read_plan, status_word
from services.session_record import PlanKey, ReportKey
from services.session_report import REPORT_NAME, read_report_status
from services.status import Status

# The inverse of the key: the sessions that cite a session. Derived, never written.
DEPENDS_FOR = "Depends_for"
SEPARATOR = ","
PROJECT_SEPARATOR = "/"
ARROW = " → "
_ID = re.compile(r"^[\w.-]+$")


class Ref(NamedTuple):
    """One cited session: its id, and the name of its project when it is not the citing plan's own."""

    id: str
    project: str = ""

    def __str__(self) -> str:
        return f"{self.project}{PROJECT_SEPARATOR}{self.id}" if self.project else self.id

    @classmethod
    def read(cls, text: str) -> Ref | None:
        """TEXT as a reference, `ID` or `project/ID`; None when it is neither (a project is a name, never written as a path)."""
        word = text.strip()
        project, slash, session_id = word.rpartition(PROJECT_SEPARATOR)
        project = project.strip()
        if not _ID.match(session_id) or (slash and (not project or ProjectPath.written_like(project))):
            return None
        return cls(session_id, project)

    @classmethod
    def parse(cls, text: str) -> Ref:
        """TEXT as a reference; refused when it is none."""
        found = cls.read(text)
        if found is None:
            fail(f"{text!r} is not a session to depend on: write an id, or project{PROJECT_SEPARATOR}id for a session of another project")
        return found


class DependsOn(tuple):
    """A plan's dependencies: its `Depends_on` read as references, in the order written, none twice; empty when it has none."""

    KEY: ClassVar[PlanKey] = PlanKey.DEPENDS_ON

    @classmethod
    def normalized(cls, refs: Iterable[Ref]) -> DependsOn:
        """REFS, the first of each kept."""
        return cls(dict.fromkeys(refs))

    @classmethod
    def checked(cls, text: str) -> DependsOn:
        """TEXT as dependencies; refused when it holds a line break or a word that is not a reference. Empty is none."""
        if "\n" in text or "\r" in text:
            fail(f"{cls.KEY.written} is one line; this one holds a line break")
        words = [word for word in text.split(SEPARATOR) if word.strip()]
        return cls.normalized(Ref.parse(word) for word in words)

    @classmethod
    def of(cls, front: dict[str, str] | None) -> DependsOn:
        """The dependencies FRONT matter gives its plan; a word that is no reference is left out, since reading never refuses."""
        refs = [ref for word in (front or {}).get(cls.KEY.key, "").split(SEPARATOR) if (ref := Ref.read(word))]
        return cls.normalized(refs)

    def text(self) -> str:
        """The dependencies as the plan writes them: the references joined, one line."""
        return f"{SEPARATOR} ".join(str(ref) for ref in self)

    def ids(self) -> list[str]:
        return [ref.id for ref in self]


class Found(NamedTuple):
    """A cited session that resolved: what its plan and report say."""

    id: str
    front: dict[str, str] | None
    plan_status: str
    report_status: str
    # The project its plan names, None when it names none.
    project: Path | None

    @property
    def met(self) -> bool:
        """Whether it is safe to depend on: its plan and its report both state Complete."""
        return self.plan_status == Status.COMPLETE.key and self.report_status == Status.COMPLETE.key

    @property
    def state(self) -> str:
        """How it stands, for the reason an unmet dependency prints."""
        if self.plan_status == Status.COMPLETE.key:
            return f"plan complete, report {self.report_status or 'without a status'}"
        return self.plan_status or "without a status"


def _front_status(data: bytes, key: PlanKey | ReportKey) -> tuple[dict[str, str] | None, str]:
    """The front matter of the record DATA, keys lowercased as `read_plan` does, and its status."""
    lines = data.decode("utf-8-sig", "replace").splitlines()
    front, _ = front_matter(lines)
    if front is not None:
        front = {name.lower(): value for name, value in front.items() if name == front_key(name)}
    return front, status_word((front or {}).get(key.STATUS.key, ""))


class Reader:
    """Resolves references and reads what the cited sessions say; remembers what it read, so one run reads each only once.

    HOME is the project of the plan being checked, where a reference without a
    project is looked for on the records branch once its folder is gone.
    """

    def __init__(self, home: Path | None) -> None:
        self.home = home
        self._projects: dict[str, Path | str] = {}
        self._found: dict[tuple[str, Path | None], Found | str] = {}

    def project(self, name: str) -> Path | str:
        """The folder of the project NAME names, else why it does not resolve."""
        if name not in self._projects:
            try:
                self._projects[name] = project_by_name(name)
            except SystemExit as refused:
                self._projects[name] = str(refused.code).removeprefix("error: ")
        return self._projects[name]

    def find(self, ref: Ref, home: Path | None = None) -> Found | str:
        """The session REF cites, else why it cannot be found; a local reference is looked for from HOME, else from the reader's."""
        home = home or self.home
        where: Path | str | None = self.project(ref.project) if ref.project else home
        key = (str(ref), where if isinstance(where, Path) else None)
        if key not in self._found:
            self._found[key] = self._resolve(ref, where)
        return self._found[key]

    def _resolve(self, ref: Ref, where: Path | str | None) -> Found | str:
        if isinstance(where, str):
            return f"project {ref.project} does not resolve: {where}"
        try:
            folder = folder_of(ref.id)
        except SystemExit as refused:
            return str(refused.code).removeprefix("error: ")
        if folder.is_dir() and (folder / PLAN_NAME).is_file():
            plan = read_plan(folder / PLAN_NAME)
            named = (plan.front or {}).get(PlanKey.PROJECT.key, "").strip()
            return Found(ref.id, plan.front, plan.status, read_report_status(folder), Path(named) if named else where)
        if where is not None:
            kept = read_from_branch(where, ref.id, PLAN_NAME)
            if kept is not None:
                front, status = _front_status(kept, PlanKey)
                report = read_from_branch(where, ref.id, REPORT_NAME)
                report_status = _front_status(report, ReportKey)[1] if report is not None else ""
                return Found(ref.id, front, status, report_status, where)
        return "cannot be found: it has no session folder, and the project's records branch holds nothing for it"

    def unmet(self, refs: Iterable[Ref], home: Path | None = None) -> list[str]:
        """Each of REFS that is not met, as `ref (how it stands)`; none when every one is."""
        reasons = []
        for ref in refs:
            found = self.find(ref, home)
            if isinstance(found, str):
                reasons.append(f"{ref} ({found})")
            elif not found.met:
                reasons.append(f"{ref} ({found.state})")
        return reasons

    def cycle(self, start: str, refs: Iterable[Ref], home: Path | None = None) -> list[str] | None:
        """The path from START back to START through REFS and what they depend on, e.g. [A, B, A]; None when there is none."""
        seen: set[str] = set()

        def walk(path: list[str], refs: Iterable[Ref], home: Path | None) -> list[str] | None:
            for ref in refs:
                if ref.id == start:
                    return [*path, start]
                if ref.id in seen:
                    continue
                seen.add(ref.id)
                found = self.find(ref, home)
                if isinstance(found, str):
                    continue
                inner = walk([*path, ref.id], DependsOn.of(found.front), found.project or home)
                if inner:
                    return inner
            return None

        return walk([start], refs, home)


def refused_for_writing(session_id: str, refs: DependsOn, reader: Reader, added: DependsOn | None = None) -> None:
    """Refuse REFS as the dependencies of SESSION_ID unless each of ADDED (all of REFS when not given) resolves and none makes a cycle.

    Written once, when the key is written: a session that depends on itself,
    one that cannot be found, a project that does not resolve, and a cycle of
    any length through all of REFS. A dependency already in the key that no
    longer resolves is not refused again when another is added: it is dropped.
    """
    for ref in refs if added is None else added:
        if ref.id == session_id:
            fail(f"session {session_id} cannot depend on itself")
        found = reader.find(ref)
        if isinstance(found, str):
            fail(f"{DependsOn.KEY.written} {ref}: {found}; a dependency is written only for a session that is there")
    path = reader.cycle(session_id, refs)
    if path:
        fail(f"{DependsOn.KEY.written} would make a cycle: {ARROW.join(path)}")


def dependents(session_id: str, sessions: Iterable) -> list[str]:
    """The ids of SESSIONS whose plan cites SESSION_ID: the `Depends_for` of that session, derived and never written."""
    return [session.id for session in sessions if session_id in DependsOn.of(session.front).ids()]
