#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.status.primitive.status_value import StatusValue, STATUS_LABEL
from modules.knowledge.status.primitive.document_kinds.document_kind_plan import Plan
from modules.knowledge.status.primitive.document_kinds.document_kind_report import Report
from modules.knowledge.status.primitive.document_kinds.document_kind_handoff import Handoff
from modules.knowledge.status.primitive.document_kinds.document_kind_research import Research

class Complete(StatusValue):
    word = 'Complete'
    meaning = "Finished: a task's acceptance check passed, a handoff has nothing left open, a research's every question carries a final standing."
    order = 10
    id = '01a14a04-652c-7844-bfc5-b73cdd4f4bef'
    kinds = (Plan, Report, Handoff, Research,)
    safe = 'Yes'
    report_ending = 'the check passed, or passed because nothing needed doing'

LABELS = (Complete.definition(),)
