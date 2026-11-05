#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
FS_COMMAND = 'fs'
SUMMARY = 'make directory links, list a tree and put paths in the recycle bin'
DESCRIPTION = '''memar fs: acts on files and folders that keep a text or a path from being lost

Each verb below says what it does in its own --help. Writing and editing text is under memar content.
'''

def describe(verbs) -> None:
    verbs.add_parser(FS_COMMAND, help=SUMMARY, description=DESCRIPTION)
    return None
