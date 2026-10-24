#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/status.py — the one vocabulary of Status, declared once.

Status names where a document, or a piece of work, stands in its life. One
vocabulary serves every kind that carries a Status; [Status](../../../../modules-plugable/knowledge/documentation/documentation.md#status)
states the rule and the reasons, and this file is the closed set itself: each
value, its meaning, the kinds that may use it, and what is safe to depend on.
It is code because a program reads it (a plan is queued, claimed, swept; a
report is checked against its plan) and because a closed set written as a
prose table is a copy ([A Fact in Code Is Written Once](../../../../modules-plugable/knowledge/documentation/documentation.md#a-fact-in-code-is-written-once)).
That document lists none of the values: they are here alone.

Every reader obtains values from here by calling the type: a script asks
`Status.for_kind(kind)` for the values a kind may take, `Status.read(text)` for
the value a written word names, `Status.listing(kind)` for them as a sentence
in a help text or a message. No other file spells a Status word.

Why the type holds all eleven values and not only the four a task plan uses:
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
from modules.knowledge.label.primitive.label import Label, LabelDefinition
STATUS_LABEL = Label('Status', '01a14a04-6522-7d19-9796-04f8a30e831f')
'The label every Status value takes: Status is a field of its own, and its values are labels of this one (owner, 2026-10-16).'
_IDS = {'Draft': '01a14a04-6523-7916-969a-cedf7ef62566', 'Proposed': '01a14a04-6524-7dda-8f7d-d0005f0d99d4', 'Final': '01a14a04-6525-7362-b4b2-3654fb2c06a6', 'Superseded': '01a14a04-6526-7818-93c4-ad6502671d9b', 'Rejected': '01a14a04-6527-7b35-8b8c-8438070c1c38', 'Queued': '01a14a04-6528-796c-8a26-e8132b15f166', 'Active': '01a14a04-6529-77f7-9f29-c657a634a824', 'Paused': '01a14a04-652a-76eb-beb2-33541b611374', 'Blocked': '01a14a04-652b-7a44-a88d-5f132d3b675d', 'Complete': '01a14a04-652c-7844-bfc5-b73cdd4f4bef', 'Withdrawn': '01a14a04-652d-7d1c-963b-a0fd21c182dd'}

class DocumentKind(Enum):
    """What carries a Status; the value is the kind's name as a reader sees it."""
    EXPLANATION = 'Explanation-facet document'
    PLAN = 'Plan'
    REPORT = 'Report'
    HANDOFF = 'Handoff'
    RESEARCH = 'Research'

class Status(Enum):
    """One value of the Status vocabulary, in the vocabulary's order.

    Each is (word, meaning, kinds that may use it, safe to depend on, how a
    task report that states it ended or None when a report may not state
    it). The word is written capitalized and compared lower case (`key`).
    """
    DRAFT = ('Draft', "Direction is not yet settled; real, unresolved questions remain, recorded in the document's paired handoff.", (DocumentKind.EXPLANATION,), 'No', None)
    PROPOSED = ('Proposed', 'Design discussion reached consensus; ready for final review before being reflected in canonical documentation.', (DocumentKind.EXPLANATION,), 'Not yet', None)
    FINAL = ('Final', 'Reflected in canonical documentation.', (DocumentKind.EXPLANATION,), 'Yes', None)
    SUPERSEDED = ('Superseded', 'Replaced by a newer document, which the cited relation names ([Citations](#citations)).', (DocumentKind.EXPLANATION,), 'No: depend on the superseding document', None)
    REJECTED = ('Rejected', 'Considered and explicitly not adopted; kept for the historical record.', (DocumentKind.EXPLANATION,), 'No', None)
    QUEUED = ('Queued', 'Waiting to be taken up; nobody has started it.', (DocumentKind.PLAN,), 'No', None)
    ACTIVE = ('Active', 'Being worked on or investigated now.', (DocumentKind.PLAN, DocumentKind.REPORT, DocumentKind.HANDOFF, DocumentKind.RESEARCH), 'No', 'its budget ended or it made no progress: another pass is owed')
    PAUSED = ('Paused', 'Stopped temporarily; resumption is expected.', (DocumentKind.HANDOFF, DocumentKind.RESEARCH), 'No', None)
    BLOCKED = ('Blocked', 'Cannot continue until something outside the work arrives: an answer, an approval, a dependency; the record states what it waits for.', (DocumentKind.PLAN, DocumentKind.REPORT, DocumentKind.HANDOFF), 'No', 'it waits on an answer or an approval: say which')
    COMPLETE = ('Complete', "Finished: a task's acceptance check passed, a handoff has nothing left open, a research's every question carries a final standing.", (DocumentKind.PLAN, DocumentKind.REPORT, DocumentKind.HANDOFF, DocumentKind.RESEARCH), 'Yes', 'the check passed, or passed because nothing needed doing')
    WITHDRAWN = ('Withdrawn', 'Abandoned without an answer; the reason is recorded in the record itself.', (DocumentKind.RESEARCH,), 'No', None)

    def __init__(self, word: str, meaning: str, kinds: tuple[DocumentKind, ...], safe: str, report_ending: str | None) -> None:
        self.word = word
        self.meaning = meaning
        self.kinds = kinds
        self.safe = safe
        self.report_ending = report_ending

    @property
    def label(self) -> Label:
        """This value as a label: its word and its identifier, defined once here and taking the label `Status`."""
        return Label(self.word, _IDS[self.word])

    @classmethod
    def definitions(cls) -> tuple[LabelDefinition, ...]:
        """Every value's definition: the label, taking `Status`."""
        return tuple((LabelDefinition(status.label, (STATUS_LABEL,)) for status in cls))

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
    def for_kind(cls, kind: DocumentKind) -> tuple[Status, ...]:
        """The values KIND may take, in the table's order."""
        return tuple((status for status in cls if kind in status.kinds))

    @classmethod
    def keys(cls, kind: DocumentKind) -> tuple[str, ...]:
        """The values KIND may take as the scripts compare them (`key`)."""
        return tuple((status.key for status in cls.for_kind(kind)))

    @classmethod
    def listing(cls, kind: DocumentKind) -> str:
        """The words KIND may take as a sentence: `Queued, Active, Blocked, or Complete`."""
        words = [status.word for status in cls.for_kind(kind)]
        return f"{', '.join(words[:-1])}, or {words[-1]}" if len(words) > 1 else words[0]
