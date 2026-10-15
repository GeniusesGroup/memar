#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/module.py — `memar module`: what Memar does to the shape of a module.

A module is Memar's unit of a domain: a folder under `modules/` in Memar's own
checkout, and the same shape in a project developed the Memar way. This file
declares the verb and nothing else of its own; each sub-verb is one service on
this shelf, `module_<capability>`, which declares it and holds why it is built
as it is. Nothing is owed before every sub-verb, so it declares no run.

What a module is, and what each of its folders holds, is the documents' answer
(`modules/README.md`), not this domain's: the verbs here make the shape those
documents describe, and say where to read what it means.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

MODULE_COMMAND = "module"

SUMMARY = "shape a module: make the role folders its kinds of work are grouped in"

DESCRIPTION = """memar module — the shape of a module, made rather than typed

A module that carries more than one kind of work groups each kind in a folder
named for its role. What each role holds is said in modules/README.md in the
Memar checkout, under "By role inside a module"."""


def describe(verbs) -> None:
    """`memar module`, which only groups its verbs: nothing is owed before every one."""
    verbs.add_parser(MODULE_COMMAND, help=SUMMARY, description=DESCRIPTION)
    return None
