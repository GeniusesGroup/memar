#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.status.primitive.status_value import StatusValue, STATUS_LABEL
from modules.knowledge.status.primitive.document_kinds.document_kind_plan import Plan
from modules.knowledge.status.primitive.document_kinds.document_kind_report import Report
from modules.knowledge.status.primitive.document_kinds.document_kind_handoff import Handoff
from modules.knowledge.status.primitive.document_kinds.document_kind_research import Research

class Active(StatusValue):
    word = 'Active'
    meaning = 'Being worked on or investigated now.'
    order = 7
    id = '01a14a04-6529-77f7-9f29-c657a634a824'
    kinds = (Plan, Report, Handoff, Research,)
    safe = 'No'
    report_ending = 'its budget ended or it made no progress: another pass is owed'

LABELS = (Active.definition(),)
