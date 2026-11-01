#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.status.primitive.status_value import StatusValue, STATUS_LABEL
from modules.knowledge.status.primitive.document_kinds.document_kind_explanation import Explanation

class Draft(StatusValue):
    word = 'Draft'
    meaning = "Direction is not yet settled; real, unresolved questions remain, recorded in the document's paired handoff."
    order = 1
    id = '01a14a04-6523-7916-969a-cedf7ef62566'
    kinds = (Explanation,)
    safe = 'No'
    report_ending = None

LABELS = (Draft.definition(),)
