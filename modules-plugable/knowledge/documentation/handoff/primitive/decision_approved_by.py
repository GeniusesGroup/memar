#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.content.primitive.section import Section

class DecisionApprovedBy(Section):
    heading = 'Approved by'
    purpose = 'optional reference to the content that approved the decision, such as the comment of a user with the CTO role'
    use = 'when an approval exists, so the decision cites it and does not restate the status of the task'
    order = 5
    labels = ('decision-field',)
