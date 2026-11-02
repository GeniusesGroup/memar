#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from machine.plugable_import import load as plugable_load
from modules.identity.thing.labels.Label_Active import Label_Active
from modules.identity.thing.labels.Label_Blocked import Label_Blocked
from modules.identity.thing.labels.Label_Complete import Label_Complete
from modules.identity.thing.labels.Label_Draft import Label_Draft
from modules.identity.thing.labels.Label_Final import Label_Final
from modules.identity.thing.labels.Label_Paused import Label_Paused
from modules.identity.thing.labels.Label_Proposed import Label_Proposed
from modules.identity.thing.labels.Label_Queued import Label_Queued
from modules.identity.thing.labels.Label_Rejected import Label_Rejected
from modules.identity.thing.labels.Label_Superseded import Label_Superseded
from modules.identity.thing.labels.Label_Withdrawn import Label_Withdrawn
from modules.knowledge.label.labels.Label_Status import Label_Status
Label_Explanation = plugable_load('knowledge.documentation.explanation.labels.Label_Explanation').Label_Explanation
Label_Plan = plugable_load('knowledge.documentation.plan.labels.Label_Plan').Label_Plan
Label_Report = plugable_load('knowledge.documentation.report.labels.Label_Report').Label_Report
Label_Handoff = plugable_load('knowledge.documentation.handoff.labels.Label_Handoff').Label_Handoff
Label_Research = plugable_load('knowledge.documentation.research.labels.Label_Research').Label_Research
STATUS_LABEL = Label_Status.as_label

class _Members(type):
    def __iter__(cls):
        return iter(cls.all())

class DocumentKind(metaclass=_Members):
    EXPLANATION = Label_Explanation
    PLAN = Label_Plan
    REPORT = Label_Report
    HANDOFF = Label_Handoff
    RESEARCH = Label_Research

    @classmethod
    def all(cls) -> tuple[type, ...]:
        return (cls.EXPLANATION, cls.PLAN, cls.REPORT, cls.HANDOFF, cls.RESEARCH)

class Status(metaclass=_Members):
    DRAFT = Label_Draft
    PROPOSED = Label_Proposed
    FINAL = Label_Final
    SUPERSEDED = Label_Superseded
    REJECTED = Label_Rejected
    QUEUED = Label_Queued
    ACTIVE = Label_Active
    PAUSED = Label_Paused
    BLOCKED = Label_Blocked
    COMPLETE = Label_Complete
    WITHDRAWN = Label_Withdrawn

    @classmethod
    def all(cls) -> tuple[type, ...]:
        return (
            cls.DRAFT, cls.PROPOSED, cls.FINAL, cls.SUPERSEDED, cls.REJECTED,
            cls.QUEUED, cls.ACTIVE, cls.PAUSED, cls.BLOCKED, cls.COMPLETE, cls.WITHDRAWN,
        )

    @classmethod
    def definitions(cls):
        return tuple(member.definition() for member in cls.all())

    @classmethod
    def read(cls, text: str):
        wanted = text.strip().lower()
        return next((member for member in cls.all() if member.key == wanted), None)

    @classmethod
    def for_kind(cls, kind) -> tuple:
        wanted = kind.word if hasattr(kind, 'word') else str(kind)
        return tuple(member for member in cls.all() if wanted in member.kinds)

    @classmethod
    def keys(cls, kind) -> tuple[str, ...]:
        return tuple(member.key for member in cls.for_kind(kind))

    @classmethod
    def listing(cls, kind) -> str:
        words = [member.word for member in cls.for_kind(kind)]
        return f"{', '.join(words[:-1])}, or {words[-1]}" if len(words) > 1 else words[0]
