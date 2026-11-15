#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""derive.py — the command line of a declared service, made from its declaration and from nothing else.

A service says what it takes (`modules/process/service/primitive/declaration.py`); this file makes the verb:

- the verb's words are the declaration's name, joined with hyphens;
- a parameter with no default is given in order, as a word; one with a default is a flag named like the parameter;
- a true-or-false parameter is a flag that sets it, a list is a flag that may be given again, a whole number is read as one;
- a parameter named `project` is the project a person names by name or by folder (the same two flags every verb
  that acts on a project has);
- the run calls the function with what was parsed, and prints what it answers.

So no service holds a verb, a flag or a print, and a service added to a module's declarations has its verb with
nothing written here.
"""
from __future__ import annotations

import argparse
import inspect
from importlib import import_module
from pathlib import Path
from typing import Callable

PROJECT = 'project'
WORD, MAYBE, WORDS, FLAG = 'word', 'maybe', 'words', 'flag'


def flag_of(name: str) -> str:
    return '--' + name.rstrip('_').replace('_', '-')


def flags_of(name: str) -> tuple[str, ...]:
    short = {'message_file': '-F', 'message': '-m', 'verbose': '-v'}.get(name)
    return (short, flag_of(name)) if short else (flag_of(name),)


def metavar_of(name: str) -> str:
    """The word a person sees for a value: the last word of its name (`task_id` is ID, `content_file` is FILE)."""
    return name.rstrip('_').split('_')[-1].upper()


def verb_of(declaration) -> str:
    return '-'.join(declaration.name.split())


TYPES = {'whole': int, 'real': float, 'path': Path, 'text': str}


def argument_of(parser, each, found) -> None:
    """The argument EACH becomes on PARSER."""
    kind = TYPES.get(each.kind, str)
    helped = each.help or None
    if each.name == PROJECT:
        found.add_project_flags(parser, 'the project it acts on', required=each.required)
    elif each.shape == WORD:
        parser.add_argument(each.name, metavar=metavar_of(each.name), type=kind, choices=each.choices, help=helped)
    elif each.shape == MAYBE:
        parser.add_argument(each.name, nargs='?', metavar=metavar_of(each.name), type=kind, choices=each.choices, default=each.default, help=helped)
    elif each.shape == WORDS:
        parser.add_argument(each.name, nargs='+' if each.required else '*', metavar=metavar_of(each.name), type=TYPES.get(each.item_kind, str), help=helped)
    elif each.kind == 'flag':
        if each.default is True:
            parser.add_argument('--no-' + each.name.replace('_', '-'), dest=each.name, action='store_false', help=helped)
        else:
            parser.add_argument(*flags_of(each.name), dest=each.name, action='store_true', help=helped)
    elif each.kind == 'many':
        repeat = 'repeat it' if each.item_kind == 'path' else 'repeat it or separate the words by commas'
        parser.add_argument(*flags_of(each.name), dest=each.name, action='append', metavar=metavar_of(each.name), default=None, required=each.required, help=(each.help + '; ' if each.help else '') + repeat)
    else:
        parser.add_argument(*flags_of(each.name), dest=each.name, metavar=metavar_of(each.name), type=kind, choices=each.choices, default=each.default, required=each.required, help=helped)


def value_of(args: argparse.Namespace, each, found):
    """What EACH was given on the command line, as the function takes it."""
    if each.name == PROJECT:
        return found.project_from_args(args)
    given = getattr(args, each.name)
    if each.kind == 'many' and each.shape == WORDS:
        return tuple(given)
    if each.kind == 'many':
        convert = TYPES.get(each.item_kind, str)
        if each.item_kind == 'path':
            return None if not given else tuple(convert(group) for group in given)
        return None if not given else tuple(convert(word.strip()) for group in given for word in group.split(',') if word.strip())
    return given


def describer(declaration) -> Callable:
    """The `describe(verbs)` of DECLARATION, which the router calls as it does for any module that declares a verb."""
    found = import_module('modules.computer.software.services.project_find')

    def describe(verbs) -> Callable[[argparse.Namespace], int | None]:
        parser = verbs.add_parser(verb_of(declaration), help=declaration.summary, description=declaration.description or declaration.summary)
        if declaration.Domain():
            parser._memar_details = declaration
        for each in declaration.fields:
            argument_of(parser, each, found)

        def run(args: argparse.Namespace) -> int | None:
            values = {each.name: value_of(args, each, found) for each in declaration.fields}
            parameters = inspect.signature(declaration.function).parameters
            positional = [values.pop(name, parameter.default) for name, parameter in parameters.items()
                          if parameter.kind is inspect.Parameter.POSITIONAL_ONLY]
            result = declaration.function(*positional, **values)
            if result is not None:
                print(result)
            return None
        return run
    return describe
