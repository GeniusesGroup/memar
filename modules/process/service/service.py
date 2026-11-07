#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import argparse
from importlib import import_module
from typing import Callable
from machine.console import fail

Priority_Rank = import_module('modules-plugable.identity.thing.priority.primitive.rank').Priority_Rank
add_project_flags = import_module('modules.computer.software.services.project_find').add_project_flags
project_from_args = import_module('modules.computer.software.services.project_find').project_from_args
process_services = import_module('modules.process.services.composition').process_services

VERB = 'service'
SUMMARY = 'call a service by its Service_UUID (transitional; remove when verbs are gone)'


def _only_from(args: argparse.Namespace) -> tuple[str, ...] | None:
    if not args.only_from:
        return None
    return tuple(word.strip() for group in args.only_from for word in group.split(',') if word.strip())


def _summary(service: object) -> str:
    if hasattr(service, 'summary'):
        value = service.summary
        return str(value() if callable(value) else value)
    return ''


def _help_lines(registry) -> str:
    lines = []
    for service in registry.services():
        operation_id = service.operation_id() if callable(getattr(service, 'operation_id', None)) else getattr(service, 'operation_id', '')
        summary = _summary(service)
        if summary:
            lines.append(f'{summary}: {operation_id}')
        else:
            lines.append(str(operation_id))
    return '; '.join(lines)


def run(args: argparse.Namespace) -> None:
    registry = process_services()
    service = registry.get_by_id(args.service_id)
    if service is None:
        known = ', '.join(
            item.operation_id() if callable(getattr(item, 'operation_id', None)) else str(getattr(item, 'operation_id', ''))
            for item in registry.services()
        )
        fail(f'no service {args.service_id}; known: {known}')
    do = getattr(service, 'do', None)
    if do is None:
        fail(f'service {args.service_id} has no domain entry')
    result = do(
        thing=args.thing,
        word=args.word,
        project=project_from_args(args),
        only_from=_only_from(args),
    )
    if result is not None:
        print(result)


def describe(verbs) -> Callable[[argparse.Namespace], None]:
    registry = process_services()
    parser = verbs.add_parser(
        VERB,
        help=SUMMARY,
        description=(
            'Invoke a service by Service_UUID. Transitional face until callers use ids directly; '
            'remove this verb when other CLI verbs are gone. '
            f'{_help_lines(registry)}.'
        ),
    )
    parser.add_argument('service_id', help='the Service_UUID of the service to call')
    parser.add_argument('--thing', help='the thing the service acts on')
    parser.add_argument('--word', help=f'a Priority_Rank when setting: {Priority_Rank.listing()}')
    parser.add_argument('--only-from', action='append', help='a status word the thing must hold now for Set Status to apply; repeat it or separate words by commas')
    add_project_flags(parser, 'the project the thing belongs to')
    return run
