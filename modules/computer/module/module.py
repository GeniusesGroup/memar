#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/computer/module/module.py — `memar module`: what Memar does to the shape of a module.

A module is Memar's unit of a domain: a folder under `modules/` in Memar's own
checkout, and the same shape in a project developed the Memar way. This file
declares the verb and nothing else of its own; each sub-verb is one service,
`module_<capability>`, which declares it and holds why it is built as it is.
Nothing is owed before every sub-verb, so it declares no run.

What a module is is the documents' answer (`modules/README.md`). Which folders
a module groups its work in is a choice an organization may make otherwise, so
no list of them is here: a pluggable module declares it and adds the sub-verb
that makes them (Memar's is `modules-plugable/knowledge/module-skeleton/`;
owner, 2026-10-20).

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
MODULE_COMMAND = 'module'
SUMMARY = 'shape a module: make the folders its kinds of work are grouped in'
DESCRIPTION = 'memar module — the shape of a module, made rather than typed\n\nA module that carries more than one kind of work groups each kind in a folder\nnamed for its role. Which folders, and what each holds, is printed by the help\nof the verb that makes them.'

def describe(verbs) -> None:
    """`memar module`, which only groups its verbs: nothing is owed before every one."""
    verbs.add_parser(MODULE_COMMAND, help=SUMMARY, description=DESCRIPTION)
    return None
