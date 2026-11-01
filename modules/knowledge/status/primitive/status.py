#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from pathlib import Path
from modules.knowledge.content.primitive.catalog import Catalog
from modules.knowledge.status.primitive.document_kinds.document_kind_explanation import Explanation
from modules.knowledge.status.primitive.document_kinds.document_kind_handoff import Handoff
from modules.knowledge.status.primitive.document_kinds.document_kind_plan import Plan
from modules.knowledge.status.primitive.document_kinds.document_kind_report import Report
from modules.knowledge.status.primitive.document_kinds.document_kind_research import Research
from modules.knowledge.status.primitive.status_value import STATUS_LABEL
from modules.knowledge.status.labels.active import Active
from modules.knowledge.status.labels.blocked import Blocked
from modules.knowledge.status.labels.complete import Complete
from modules.knowledge.status.labels.draft import Draft
from modules.knowledge.status.labels.final import Final
from modules.knowledge.status.labels.paused import Paused
from modules.knowledge.status.labels.proposed import Proposed
from modules.knowledge.status.labels.queued import Queued
from modules.knowledge.status.labels.rejected import Rejected
from modules.knowledge.status.labels.superseded import Superseded
from modules.knowledge.status.labels.withdrawn import Withdrawn
_LABELS = Path(__file__).resolve().parents[1] / 'labels'
_KINDS = Path(__file__).resolve().parent / 'document_kinds'

class DocumentKind:
    EXPLANATION = Explanation
    PLAN = Plan
    REPORT = Report
    HANDOFF = Handoff
    RESEARCH = Research

    @classmethod
    def all(cls) -> tuple[type, ...]:
        return (cls.EXPLANATION, cls.PLAN, cls.REPORT, cls.HANDOFF, cls.RESEARCH)

class Status:
    DRAFT = Draft
    PROPOSED = Proposed
    FINAL = Final
    SUPERSEDED = Superseded
    REJECTED = Rejected
    QUEUED = Queued
    ACTIVE = Active
    PAUSED = Paused
    BLOCKED = Blocked
    COMPLETE = Complete
    WITHDRAWN = Withdrawn

    @classmethod
    def all(cls) -> tuple[type, ...]:
        return (
            cls.DRAFT, cls.PROPOSED, cls.FINAL, cls.SUPERSEDED, cls.REJECTED,
            cls.QUEUED, cls.ACTIVE, cls.PAUSED, cls.BLOCKED, cls.COMPLETE, cls.WITHDRAWN,
        )

    @classmethod
    def catalog(cls) -> Catalog:
        return Catalog(_LABELS, 'Status')

    @classmethod
    def definitions(cls):
        return tuple(member.definition() for member in cls.all())

    @classmethod
    def read(cls, text: str):
        wanted = text.strip().lower()
        return next((member for member in cls.all() if member.key == wanted), None)

    @classmethod
    def for_kind(cls, kind) -> tuple:
        return tuple(member for member in cls.all() if kind in member.kinds)

    @classmethod
    def keys(cls, kind) -> tuple[str, ...]:
        return tuple(member.key for member in cls.for_kind(kind))

    @classmethod
    def listing(cls, kind) -> str:
        words = [member.word for member in cls.for_kind(kind)]
        return f"{', '.join(words[:-1])}, or {words[-1]}" if len(words) > 1 else words[0]
