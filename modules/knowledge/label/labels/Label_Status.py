#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.labels.declared_label import DeclaredLabel

class Label_Status(DeclaredLabel):
    word = 'Status'
    id = '01a14a04-6522-7d19-9796-04f8a30e831f'
    meaning = (
        'A label other labels take when they name where a record stands in its life. '
        'A Status-kind label may carry a rule; when it attaches, work may start. '
        'Attachment is only Label edge on any record — including content. '
        'Status is not a separate domain vocabulary tree.'
    )
    order = 1
    labels = ('LabelKind',)
