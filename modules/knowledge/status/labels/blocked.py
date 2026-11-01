#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.status.primitive.status_value import StatusValue, STATUS_LABEL
from modules.knowledge.status.primitive.document_kinds.document_kind_plan import Plan
from modules.knowledge.status.primitive.document_kinds.document_kind_report import Report
from modules.knowledge.status.primitive.document_kinds.document_kind_handoff import Handoff

class Blocked(StatusValue):
    word = 'Blocked'
    meaning = 'Cannot continue until something outside the work arrives: an answer, an approval, a dependency; the record states what it waits for.'
    order = 9
    id = '01a14a04-652b-7a44-a88d-5f132d3b675d'
    kinds = (Plan, Report, Handoff,)
    safe = 'No'
    report_ending = 'it waits on an answer or an approval: say which'

LABELS = (Blocked.definition(),)
