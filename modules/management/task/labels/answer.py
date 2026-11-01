#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.management.task.labels.task_kind_value import TaskKindValue

class Answer(TaskKindValue):
    word = 'answer'
    meaning = 'A question is answered in the conversation itself, which opens no task and so writes no plan.'
    order = 1
    carried = False
    id = ''
