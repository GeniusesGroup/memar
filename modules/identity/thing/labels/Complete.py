#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.knowledge.label.labels.Status import Label_Status

class Label_Complete(DeclaredLabel):
    word = 'Complete'
    id = '01a14a04-652c-7844-bfc5-b73cdd4f4bef'
    meaning = "Finished: a task's acceptance check passed, a handoff has nothing left open, a research's every question carries a final standing."
    order = 10
    labels = (Label_Status,)
    safe = 'Yes'
    report_ending = 'the check passed, or passed because nothing needed doing'
