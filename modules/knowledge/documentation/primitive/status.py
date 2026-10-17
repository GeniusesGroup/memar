#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/status.py — the one vocabulary of Status, declared once.

Status names where a document, or a piece of work, stands in its life. One
vocabulary serves every kind that carries a Status; [Status](../../../modules/content/documentation/documentation.md#status)
states the rule and the reasons, and this file is the closed set itself: each
value, its meaning, the kinds that may use it, and what is safe to depend on.
It is code because a program reads it (a plan is queued, claimed, swept; a
report is checked against its plan) and because a closed set written as a
prose table is a copy ([A Fact in Code Is Written Once](../../../modules/content/documentation/documentation.md#a-fact-in-code-is-written-once)).
That document lists none of the values: they are here alone.

Every reader obtains values from here by calling the type: a script asks
`Status.for_kind(kind)` for the values a kind may take, `Status.read(text)` for
the value a written word names, `Status.listing(kind)` for them as a sentence
in a help text or a message. No other file spells a Status word.

Why the type holds all eleven values and not only the four a session plan uses:
the vocabulary is one, a kind never adds a value of its own, and a value a
document, a handoff or a research uses is the same fact as one a plan uses
(Active, Blocked, Complete are shared). Splitting the set by the scripts' own
need would leave the other seven values with no declaration at all.

The meanings are English; a description in another
human language is the type's own detail in a file of its own, a rule beyond
this file.
"""
from __future__ import annotations

from enum import Enum


class Kind(Enum):
    """What carries a Status; the value is the kind's name as a reader sees it."""

    EXPLANATION = "Explanation-facet document"
    SESSION_PLAN = "Session plan"
    SESSION_REPORT = "Session report"
    HANDOFF = "Handoff"
    RESEARCH = "Research"


class Status(Enum):
    """One value of the Status vocabulary, in the vocabulary's order.

    Each is (word, meaning, kinds that may use it, safe to depend on, how a
    session report that states it ended or None when a report may not state
    it). The word is written capitalized and compared lower case (`key`).
    """

    DRAFT = (
        "Draft",
        "Direction is not yet settled; real, unresolved questions remain, recorded in the document's paired handoff.",
        (Kind.EXPLANATION,),
        "No",
        None,
    )
    PROPOSED = (
        "Proposed",
        "Design discussion reached consensus; ready for final review before being reflected in canonical documentation.",
        (Kind.EXPLANATION,),
        "Not yet",
        None,
    )
    FINAL = (
        "Final",
        "Reflected in canonical documentation.",
        (Kind.EXPLANATION,),
        "Yes",
        None,
    )
    SUPERSEDED = (
        "Superseded",
        "Replaced by a newer document, which the cited relation names ([Citations](#citations)).",
        (Kind.EXPLANATION,),
        "No: depend on the superseding document",
        None,
    )
    REJECTED = (
        "Rejected",
        "Considered and explicitly not adopted; kept for the historical record.",
        (Kind.EXPLANATION,),
        "No",
        None,
    )
    QUEUED = (
        "Queued",
        "Waiting to be taken up; nobody has started it.",
        (Kind.SESSION_PLAN,),
        "No",
        None,
    )
    ACTIVE = (
        "Active",
        "Being worked on or investigated now.",
        (Kind.SESSION_PLAN, Kind.SESSION_REPORT, Kind.HANDOFF, Kind.RESEARCH),
        "No",
        "its budget ended or it made no progress: another pass is owed",
    )
    PAUSED = (
        "Paused",
        "Stopped temporarily; resumption is expected.",
        (Kind.HANDOFF, Kind.RESEARCH),
        "No",
        None,
    )
    BLOCKED = (
        "Blocked",
        "Cannot continue until something outside the work arrives: an answer, an approval, a dependency; the record states what it waits for.",
        (Kind.SESSION_PLAN, Kind.SESSION_REPORT, Kind.HANDOFF),
        "No",
        "it waits on an answer or an approval: say which",
    )
    COMPLETE = (
        "Complete",
        "Finished: a session's acceptance check passed, a handoff has nothing left open, a research's every question carries a final standing.",
        (Kind.SESSION_PLAN, Kind.SESSION_REPORT, Kind.HANDOFF, Kind.RESEARCH),
        "Yes",
        "the check passed, or passed because nothing needed doing",
    )
    WITHDRAWN = (
        "Withdrawn",
        "Abandoned without an answer; the reason is recorded in the record itself.",
        (Kind.RESEARCH,),
        "No",
        None,
    )

    def __init__(
        self,
        word: str,
        meaning: str,
        kinds: tuple[Kind, ...],
        safe: str,
        report_ending: str | None,
    ) -> None:
        self.word = word
        self.meaning = meaning
        self.kinds = kinds
        self.safe = safe
        self.report_ending = report_ending

    @property
    def key(self) -> str:
        """The word as the scripts compare it: lower case."""
        return self.word.lower()

    @classmethod
    def read(cls, text: str) -> Status | None:
        """The value TEXT names, stripped and in any case; None for any other word, the old words `open` and `done` too."""
        wanted = text.strip().lower()
        return next((status for status in cls if status.key == wanted), None)

    @classmethod
    def for_kind(cls, kind: Kind) -> tuple[Status, ...]:
        """The values KIND may take, in the table's order."""
        return tuple(status for status in cls if kind in status.kinds)

    @classmethod
    def keys(cls, kind: Kind) -> tuple[str, ...]:
        """The values KIND may take as the scripts compare them (`key`)."""
        return tuple(status.key for status in cls.for_kind(kind))

    @classmethod
    def listing(cls, kind: Kind) -> str:
        """The words KIND may take as a sentence: `Queued, Active, Blocked, or Complete`."""
        words = [status.word for status in cls.for_kind(kind)]
        return f"{', '.join(words[:-1])}, or {words[-1]}" if len(words) > 1 else words[0]
