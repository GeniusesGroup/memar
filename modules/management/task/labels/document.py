#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.management.task.labels.task_kind_value import TaskKindValue

class Document(TaskKindValue):
    word = 'document'
    meaning = 'The task writes or revises a document whose content is already settled.'
    order = 6
    carried = True
    id = '01a14a04-6534-78ea-b510-9d2abcdcba79'
