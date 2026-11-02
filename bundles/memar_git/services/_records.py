#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
SERVICES = 'modules-plugable.computer.git.services.'

def forward(stem: str, verbs):
    return import_module(SERVICES + stem).describe(verbs)
