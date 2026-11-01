#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.label import Label, LabelDefinition
from modules.knowledge.status.primitive.status import STATUS_LABEL
LABELS = (
    LabelDefinition(Label('deleted', '01a19853-60ef-726b-ac8d-a1ba1ecaabe4'), (STATUS_LABEL,), 'Soft-deleted; still addressable.'),
    LabelDefinition(Label('locked', '01a19853-60ef-726b-ac8d-a1bb3825a8a8'), (STATUS_LABEL,), 'Locked by its owner against further change.'),
    LabelDefinition(Label('hidden', '01a19853-60ef-726b-ac8d-a1bc3b500bf4'), (STATUS_LABEL,), 'Hidden from ordinary listing.'),
    LabelDefinition(Label('optional', '01a19853-60ef-726b-ac8d-a1bd0d8c0f78'), (STATUS_LABEL,), 'The relation or part is optional.'),
    LabelDefinition(Label('read_only', '01a19853-60ef-726b-ac8d-a1be637f1565'), (STATUS_LABEL,), 'Readers may not edit; even the owner may not remove this mark without the rule that set it.'),
    LabelDefinition(Label('block', '01a19853-60ef-726b-ac8d-a1bf52a42973'), (STATUS_LABEL,), 'Blocked from progress until a condition clears.'),
    LabelDefinition(Label('failed', '01a19853-60ef-726b-ac8d-a1c068c10945'), (STATUS_LABEL,), 'The attempt failed.'),
    LabelDefinition(Label('incompatibility', '01a19853-60ef-726b-ac8d-a1c16af7dc98'), (STATUS_LABEL,), 'Incompatible under a rule that enforces it.'),
    LabelDefinition(Label('edited', '01a19853-60ef-726b-ac8d-a1c2f4047442'), (STATUS_LABEL,), 'Edited after a prior standing; often a derived reading.'),
)
