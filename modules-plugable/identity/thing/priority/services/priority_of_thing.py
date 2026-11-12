#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
"""priority_of_thing.py — the Priority of a thing, set through the base service; the widget of the Priority module.

The thing is named by its identity or by the name that identity derives from. A piece of work that has a Priority is
not this module's concern: any thing may carry one.
"""
from __future__ import annotations
from importlib import import_module
from typing import Any

SERVICE_SET_PRIORITY = import_module('modules-plugable.identity.thing.priority.services.set_priority').SERVICE_UUID
thing_identity = import_module('modules.identity.thing.primitive.thing_id').thing_identity
declare = import_module('modules.process.service.primitive.declaration').declare


def set_priority(thing: str, value: int, project: Any = None, services=None) -> None:
    registry = services if services is not None else import_module('modules.process.services.composition').process_services()
    registry.get_by_id(SERVICE_SET_PRIORITY).do(thing=thing_identity(thing), word=str(int(value)), project=project)


DECLARATIONS = (
    declare(
        set_priority,
        name='set',
        summary='set the Priority of a thing',
        description='Set the Priority of a thing to a rank from 1 to 10. A thing with no Priority is the lowest.',
        takes=('thing', 'value', 'project'),
        help={'thing': 'the thing, by identity or by name', 'value': 'the rank, 1 to 10'},
    ),
)
