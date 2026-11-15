#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""handler.py — the command line's handler of requests, which the server loads and knows nothing of.

A request of kind `words` carries what a person typed: the words, the folder, the environment and the standard
input. Reading the words into a verb, finding its run and running it are done here, so the server only receives a
request, finds the handler of its kind, and sends back the answer. The program `memar` sends the request and prints
the answer; it holds none of this.
"""
from __future__ import annotations

from importlib import import_module
from typing import Any

KIND = 'words'
ARGV = 'argv'


def answer(call: dict) -> dict[str, Any]:
    """The status, standard output and standard error of the command line CALL names, as a person would have had them."""
    dispatch = import_module('bundles.memar.services.dispatch.dispatch')
    router = import_module('bundles.memar_adaptor.cli.router')
    words = call.get(ARGV)
    if not (isinstance(words, list) and all(isinstance(word, str) for word in words)):
        raise dispatch.Refused('argv is a list of words')
    for key, kind in (('cwd', str), ('env', dict)):
        if not isinstance(call.get(key, kind()), kind):
            raise dispatch.Refused(f'{key} is a {kind.__name__}')
    if not (isinstance(call.get('stdin', ''), str) or callable(call['stdin'])):
        raise dispatch.Refused('stdin is text, or a function that returns it')
    argv = list(words)
    return dispatch.captured(call.get('cwd') or '.', call.get('env') or {}, call.get('stdin', ''), lambda: router.apply(router.parsed_of(argv)))


def elsewhere(call: dict) -> dict | None:
    """Where else the call can be run when the process that answers is busy: the program given the words, in a process of its own; None when it cannot (it reads standard input, which only the client holds)."""
    if call.get('stdin_lazy') or not isinstance(call.get(ARGV), list):
        return None
    location = import_module('bundles.memar.services.location.memar_location')
    return {'command': [*location.program(), *call[ARGV]], 'cwd': call.get('cwd') or '.', 'env': call.get('env') or {}}
