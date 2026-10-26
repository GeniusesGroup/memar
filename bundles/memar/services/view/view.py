#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""view/view.py — `memar view`: the read-only folder a project's `view` key names, built from one class's nodes.

What a view is, and why no verb reads it, is Memory View (`modules-plugable/computer/memory/store/view/view.md`); the
builder is that module's. The verb is kept in `bundles/memar` because it opens a class through `open`, which is this
bundle's, and a pluggable module does not reach a bundle. Its sub-verb is in `services/`.
"""
from __future__ import annotations
import argparse
COMMAND = 'view'

def describe(verbs):
    verbs.add_parser(COMMAND, help="the read-only folder that shows one class's nodes for a person's eyes", description="The view: a folder built from the committed nodes of the one class a project's `view` key\nnames, in the shape the class's presentation gives them. It is ignored by version\ncontrol, its files are read-only, and no verb reads it; a change goes through a verb.", formatter_class=argparse.RawDescriptionHelpFormatter)
    return None
