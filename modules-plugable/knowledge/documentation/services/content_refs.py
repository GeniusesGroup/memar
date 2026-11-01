#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations


def refs_of(task_id: str, content) -> set:
    found = set()
    for value in str(content.header.get('refs', '')).split():
        held, _, number = value.rpartition(':')
        if number.isascii() and number.isdigit():
            found.add((held or task_id, int(number)))
    return found
