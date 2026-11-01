#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
LABEL_COMMAND = 'label'
SUMMARY = 'declare, attach, remove, or list labels on any record'
DESCRIPTION = """memar label — the Label domain

A label is a word with an identifier, defined once; its definition may take
other labels (Status, TaskKind, Topic, …). Attachment is always
(thing)-[:label]->(label); see modules/knowledge/label/edges/label/ and
services/attach.py. Status-kind values are labels too — Status does not own
a second edge.

The verbs registered under this group today that edit a *task plan's* Labels
field (TaskKind, Topic) live in modules-plugable/management/task/services/
(label_add, label_list, plan_labels). They are not the whole Label domain.
Each verb says what it does in its own --help.
"""

def describe(verbs) -> None:
    verbs.add_parser(LABEL_COMMAND, help=SUMMARY, description=DESCRIPTION)
    return None
