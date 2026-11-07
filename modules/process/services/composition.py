#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module

Process_Services = import_module('modules.process.services.services').Process_Services

_REGISTRY: Process_Services | None = None
_READY = False


def process_services() -> Process_Services:
    global _REGISTRY, _READY
    if _REGISTRY is None:
        _REGISTRY = Process_Services()
    if not _READY:
        register_defaults(_REGISTRY)
        _READY = True
    return _REGISTRY


def register_defaults(services: Process_Services) -> None:
    import_module('modules-plugable.identity.thing.priority.services.register_services').register_services(services)
    import_module('modules-plugable.knowledge.label.status.services.register_services').register_services(services)


def reset_for_tests() -> None:
    global _REGISTRY, _READY
    _REGISTRY = None
    _READY = False
