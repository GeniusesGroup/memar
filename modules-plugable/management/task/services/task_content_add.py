#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations


def add_text(store, project, task, kind: str, text: str, author: str) -> int:
    number, _, found = store.read_latest_content(project, task, kind)
    return store.add_content(project, task, kind, text, author, number if found else 0)
