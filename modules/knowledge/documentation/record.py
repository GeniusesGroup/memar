#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/session_record.py — the shape of a session's plan.md and report.md, declared once.

A plan and a report are records: a file name, a fixed set of front-matter keys,
the parts under the front matter in order, and the Status values the file may
carry ([Status](../status.py), [Status](../../../modules/content/documentation/documentation.md#status)).
That shape is a closed set, so it is code and is written here and nowhere else
([A Fact in Code Is Written Once](../../../modules/content/documentation/documentation.md#a-fact-in-code-is-written-once)):
`session_plan` and `session_report` read and write by it, and `session_new`
prints it in its help by calling `Record.outline`.

A report has no key of its own for how the run ended: that is its Status
with the Result part, so `ReportKey` holds the session's id, the Title and
the Status. The earlier shapes (an `Outcome` key, a `Stop:` line) are not part of today's
record; the services that name them, so that a reader is told why such a
file is not read, keep them.

A key is stored lower case, which is how callers ask for it, and written in
PascalCase, which for the one-word keys of both records is a capital.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from services.project_name import ProjectName
from services.project_path import ProjectPath
from services.status import Kind, Status


class RecordKey(Enum):
    """A front-matter key: the (lower-case) key callers ask for, and what it holds."""

    def __init__(self, key: str, description: str) -> None:
        self.key = key
        self.description = description

    @property
    def written(self) -> str:
        """The key as the front matter writes it: PascalCase."""
        return self.key.capitalize()


# Both records name the session they belong to, one declaration for both kinds
# ([Documentation — Plan](../../../modules/content/documentation/plan/plan.md)):
# the record must not presume it is a file, since a folder may be moved,
# renamed or swept, so the identifier is found inside the document.
SESSION_FIELD = ("session", "the id of the session this record belongs to")


class PlanKey(RecordKey):
    SESSION = SESSION_FIELD
    TITLE = ("title", "TITLE")
    STATUS = ("status", "where the task stands, one of the Status words `memar session --help` gives")
    OPENED = ("opened", "the UTC time it was written, e.g. 2026-10-08T13:20:34Z")
    PROJECT = ("project", f"the git top-level of the folder {ProjectName.FLAG} or {ProjectPath.FLAG} names, else that folder")
    PARENT = ("parent", "ID of the session this one came from, with --parent")
    CONVERSATION = ("conversation", "the id of the first session of the conversation, with --parent")
    PRIORITY = ("priority", "N, with --priority")
    TOPIC = ("topic", "T, with --topic")
    KIND = ("kind", "K, with --kind: what the task is, which says how strong a model it needs")
    DEPENDS_ON = (
        "depends_on",
        "ID, ID, ...: the sessions that must be Complete before this one can start, each an id or project/id; "
        "while one is not, this session is Blocked",
    )


class ReportKey(RecordKey):
    SESSION = SESSION_FIELD
    TITLE = ("title", "TITLE, when known")
    STATUS = ("status", "empty until the session ends, then one of the Statuses a report may state")


@dataclass(frozen=True)
class Record:
    """A session file's shape: its name, its front-matter keys, its parts in order, and the Kind its Status is drawn from.

    HEADING is the heading under the front matter as the help shows it: the
    task's title for a plan, the word Report for a report.

    HAND_BACK_PART is the part a session adds when it needs someone's
    decision, and HAND_BACK_MAX_LINES the most lines it may hold for the file
    to be a hand-back; a record without such a part has neither.
    """

    file_name: str
    kind: Kind
    keys: tuple[RecordKey, ...]
    parts: tuple[str, ...]
    heading: str
    hand_back_part: str | None = None
    hand_back_max_lines: int | None = None

    @property
    def statuses(self) -> tuple[Status, ...]:
        """The Statuses this record's file may carry."""
        return Status.for_kind(self.kind)

    def outline(self) -> str:
        """The record as a help text shows it: front matter with a line per key saying what it holds, the heading, the parts."""
        front = [f"{key.written}: {key.description}" for key in self.keys]
        return "\n".join(["---", *front, "---", f"# {self.heading}", "", *(f"## {part}" for part in self.parts)]) + "\n"


PLAN = Record("plan.md", Kind.SESSION_PLAN, tuple(PlanKey), ("Request", "Why", "Steps", "Next"), "TITLE")
REPORT = Record(
    "report.md",
    Kind.SESSION_REPORT,
    tuple(ReportKey),
    ("What ran", "Check", "Result", "Left open"),
    "Report",
    hand_back_part="Decisions needed",
    hand_back_max_lines=10,
)
