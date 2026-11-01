#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.management.task.labels.task_kind_value import TaskKindValue

class Implement(TaskKindValue):
    word = 'implement'
    meaning = 'The task builds or changes code, a test or a tool whose design is already settled, one checked step at a time.'
    order = 5
    carried = True
    id = '01a14a04-6533-7efe-98ac-0e9e47dc1376'
