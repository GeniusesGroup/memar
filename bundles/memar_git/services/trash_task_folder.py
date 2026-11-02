#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations

def describe(verbs):
    from ._records import forward
    return forward('trash_task_folder', verbs)
