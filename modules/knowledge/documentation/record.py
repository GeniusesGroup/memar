#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""record.py — the shape of a documentation record, and the two a session writes, declared once.

A plan and a report are records: a file name, a fixed set of front-matter keys,
the parts under the front matter in order, and the Status values the file may
carry ([Status](./primitive/status.py), [Status](./documentation.md#status)).
That shape is a closed set, so it is code and is written here and nowhere else
([A Fact in Code Is Written Once](./documentation.md#a-fact-in-code-is-written-once)):
`session_plan` and `session_report` read and write by it, and `session_new`
prints it in its help by calling `Record.outline`.

The keys are the facets' own ([PlanKey](./plan/primitive/plan_key.py),
[ReportKey](./report/primitive/report_key.py)). A record is built from them and
from `Status`, so it stands here in the module's root and not in `primitive/`.
"""
from __future__ import annotations

from dataclasses import dataclass

from modules.knowledge.documentation.plan.primitive.plan_key import PlanKey
from modules.knowledge.documentation.plan.primitive.plan_part import PlanPart
from modules.knowledge.documentation.primitive.record_key import RecordKey
from modules.knowledge.documentation.primitive.status import DocumentKind, Status
from modules.knowledge.documentation.report.primitive.report_key import ReportKey
from modules.knowledge.documentation.report.primitive.report_part import HAND_BACK_MAX_LINES, ReportPart


@dataclass(frozen=True)
class Record:
    """A session file's shape: its name, its front-matter keys, its parts in order, and the DocumentKind its Status is drawn from.

    HEADING is the heading under the front matter as the help shows it: the
    task's title for a plan, the word Report for a report.

    HAND_BACK_PART is the part a session adds when it needs someone's
    decision, and HAND_BACK_MAX_LINES the most lines it may hold for the file
    to be a hand-back; a record without such a part has neither.
    """

    file_name: str
    kind: DocumentKind
    keys: tuple[RecordKey, ...]
    parts: tuple[str, ...]
    heading: str
    hand_back_part: str | None = None
    hand_back_max_lines: int | None = None

    @property
    def statuses(self) -> tuple[Status, ...]:
        """The Statuses this record's file may carry."""
        return Status.for_kind(self.kind)

    def current(self, front: dict[str, str]) -> dict[str, str]:
        """FRONT with each key an earlier name still carries read as the key: `Opened` as `Start Date`, `Session` as `ID`.

        FRONT is the record's front matter with its keys lower case. A key
        already there under its current name wins over an earlier one. The
        argument is not changed.
        """
        read = dict(front)
        for key in self.keys:
            if key.key not in read:
                earlier = next((name for name in key.earlier if name in read), None)
                if earlier is not None:
                    read[key.key] = read[earlier]
        return read

    def outline(self) -> str:
        """The record as a help text shows it: front matter with a line per key saying what it holds, the heading, the parts."""
        front = [f"{key.written}: {key.description}" for key in self.keys]
        return "\n".join(["---", *front, "---", f"# {self.heading}", "", *(f"## {part}" for part in self.parts)]) + "\n"


PLAN = Record("plan.md", DocumentKind.SESSION_PLAN, tuple(PlanKey), PlanPart.every_plan(), "TITLE")
REPORT = Record(
    "report.md",
    DocumentKind.SESSION_REPORT,
    tuple(ReportKey),
    ReportPart.every_report(),
    "Report",
    hand_back_part=ReportPart.DECISIONS_NEEDED.heading,
    hand_back_max_lines=HAND_BACK_MAX_LINES,
)
