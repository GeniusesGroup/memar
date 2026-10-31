#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations


def add_content(store, text: str, kind: str) -> str:
    return store.add_content(kind, text)
