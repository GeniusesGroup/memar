#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.label import Label, LabelDefinition
from modules.knowledge.status.primitive.status_value import STATUS_LABEL
LABELS = (LabelDefinition(Label('voided', '01a19853-60ef-726b-ac8d-a1b6ffdba8a4'), (STATUS_LABEL,), 'The invoice is void; it is not collectable.'),)
