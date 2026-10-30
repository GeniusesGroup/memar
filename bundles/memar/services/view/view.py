#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import argparse
COMMAND = 'view'

def describe(verbs):
    verbs.add_parser(COMMAND, help="the read-only folder that shows one class's nodes for a person's eyes", description="The view: a folder built from the committed nodes of the one class a project's `view` key\nnames, in the shape the class's presentation gives them. It is ignored by version\ncontrol, its files are read-only, and no verb reads it; a change goes through a verb.", formatter_class=argparse.RawDescriptionHelpFormatter)
    return None
