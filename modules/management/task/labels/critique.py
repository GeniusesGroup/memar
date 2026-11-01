#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.management.task.labels.task_kind_value import TaskKindValue

class Critique(TaskKindValue):
    word = 'critique'
    meaning = 'The task judges work it did not make against the documents that govern that work, and returns a verdict on each part.'
    order = 4
    carried = True
    id = '01a14a04-6532-76bf-b48e-4b7cc539bf44'
