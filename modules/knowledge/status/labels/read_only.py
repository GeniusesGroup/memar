#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.label import Label, LabelDefinition
from modules.knowledge.status.primitive.status_value import STATUS_LABEL
LABELS = (LabelDefinition(Label('read_only', '01a19853-60ef-726b-ac8d-a1be637f1565'), (STATUS_LABEL,), 'Readers may not edit; even the owner may not remove this mark without the rule that set it.'),)
