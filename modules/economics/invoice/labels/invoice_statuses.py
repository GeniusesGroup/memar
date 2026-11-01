#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.label import Label, LabelDefinition
from modules.knowledge.status.primitive.status import STATUS_LABEL
PAID = Label('paid', '01a19853-60ef-726b-ac8d-a1b44b006589')
PAID_PARTIALLY = Label('paid-partially', '01a19853-60ef-726b-ac8d-a1b5d81f078d')
VOIDED = Label('voided', '01a19853-60ef-726b-ac8d-a1b6ffdba8a4')
EXPIRED = Label('expired', '01a19853-60ef-726b-ac8d-a1b7be557fe3')
LABELS = (
    LabelDefinition(PAID, (STATUS_LABEL,), 'The customer has fully paid the invoice amount.'),
    LabelDefinition(PAID_PARTIALLY, (STATUS_LABEL,), 'The customer has paid only part of the invoice amount.'),
    LabelDefinition(VOIDED, (STATUS_LABEL,), 'The invoice is void; it is not collectable.'),
    LabelDefinition(EXPIRED, (STATUS_LABEL,), 'The invoice passed its due window without settlement.'),
)
