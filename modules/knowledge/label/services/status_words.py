#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Memar's closed Status-kind and DocumentKind Label_* sets, queried through `taking`.

No `Status` or `DocumentKind` bag type: callers ask `taking.taking(Label_Status, among=…)`
or the helpers below. The words live under thing and documentation `labels/`.
"""
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
from modules.knowledge.label.services import taking
Label_Explanation = plugable_load('knowledge.documentation.explanation.labels.Label_Explanation').Label_Explanation
Label_Plan = plugable_load('knowledge.documentation.plan.labels.Label_Plan').Label_Plan
Label_Report = plugable_load('knowledge.documentation.report.labels.Label_Report').Label_Report
Label_Handoff = plugable_load('knowledge.documentation.handoff.labels.Label_Handoff').Label_Handoff
Label_Research = plugable_load('knowledge.documentation.research.labels.Label_Research').Label_Research
STATUS_LABEL = Label_Status.as_label
STATUS_WORDS = (
    Label_Draft, Label_Proposed, Label_Final, Label_Superseded, Label_Rejected,
    Label_Queued, Label_Active, Label_Paused, Label_Blocked, Label_Complete, Label_Withdrawn,
)
DOCUMENT_KIND_WORDS = (
    Label_Explanation, Label_Plan, Label_Report, Label_Handoff, Label_Research,
)

def statuses() -> tuple[type, ...]:
    """Every Status-kind Label_* Memar declares under thing (takes Label_Status)."""
    return taking.taking(Label_Status, among=STATUS_WORDS)

def document_kinds() -> tuple[type, ...]:
    """Every DocumentKind Label_* under documentation (takes Label_DocumentKind)."""
    Label_DocumentKind = plugable_load('knowledge.documentation.labels.Label_DocumentKind').Label_DocumentKind
    return taking.taking(Label_DocumentKind, among=DOCUMENT_KIND_WORDS)

def statuses_for(document_kind) -> tuple[type, ...]:
    """Status-kind words whose `kinds` lists DOCUMENT_KIND (a type with `.word`, or a word)."""
    word = document_kind if isinstance(document_kind, str) else document_kind.word
    return taking.whose_kinds_include(statuses(), word)

def read_status(text: str):
    return taking.read(statuses(), text)

def status_keys(document_kind) -> tuple[str, ...]:
    return taking.keys(statuses_for(document_kind))

def status_listing(document_kind) -> str:
    return taking.listing(statuses_for(document_kind))

def status_definitions():
    return taking.definitions(statuses())
