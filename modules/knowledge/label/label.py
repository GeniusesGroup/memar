#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/knowledge/label/label.py — `memar label`: add, remove, and list labels on a task plan.

Groups the label verbs that left process/task. Vocabulary helpers sit in
services/plan_labels.py. Each verb is declared by its own service.
"""
from __future__ import annotations
LABEL_COMMAND = 'label'
SUMMARY = 'add, remove, or list labels on a task plan'
DESCRIPTION = "memar label — labels on a task plan\n\nA label is a word of a kind (TaskKind, Topic), each declared once as code:\na topic by the module of the project whose it is. `add` adds or removes one;\n`list` lists those in use and the topics declared. What a plan may carry is\nservices/plan_labels.py's.\n\nEach verb below says what it does in its own --help.\n"

def describe(verbs) -> None:
    """`memar label`, which only groups its verbs."""
    verbs.add_parser(LABEL_COMMAND, help=SUMMARY, description=DESCRIPTION)
    return None
