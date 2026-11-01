#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.management.task.labels.task_kind_value import TaskKindValue

class Mechanical(TaskKindValue):
    word = 'mechanical'
    meaning = 'The task searches, counts, moves or rewrites by a rule given to it in full, and no step of it decides anything.'
    order = 7
    carried = True
    id = '01a14a04-6535-780b-bfa4-4a451f6e5d70'
