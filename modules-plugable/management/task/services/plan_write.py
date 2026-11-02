#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
from modules.identity.thing.labels.Label_Queued import Label_Queued
from modules.identity.thing.labels.Label_Active import Label_Active
from importlib import import_module
from machine.console import fail
set_status = import_module('modules-plugable.management.task.services.plan_status').set_status
from modules.knowledge.label.services.status_words import statuses, statuses_for, status_keys, status_listing, read_status, status_definitions, STATUS_LABEL, STATUS_WORDS


def queue_plan(store, project, task, claimed: bool) -> None:
    status, _ = store.read_status(project, task)
    if status == Label_Queued.key:
        return
    if claimed:
        fail(f'task {task} is claimed by an agent; it is queued again only once that claim has lapsed')
    if status != Label_Active.key:
        fail(f"task {task} is {status or 'without a status'}; only an active task is queued")
    set_status(store, project, task, Label_Queued.key)
