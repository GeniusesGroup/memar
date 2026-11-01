#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.management.task.labels.task_kind_value import TaskKindValue

class PlanKind(TaskKindValue):
    word = 'plan'
    meaning = 'A task coordinates other tasks — writes, queues or hands over their plans, or asks for a review of their work — and adds this to the kind of its own task, so no plan carries it.'
    order = 2
    carried = False
    id = ''
