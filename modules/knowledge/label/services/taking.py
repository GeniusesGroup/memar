#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel

def taking(kind: type) -> tuple[type, ...]:
    return DeclaredLabel.having(kind)

def read(members: tuple[type, ...], text: str):
    return DeclaredLabel.read_among(members, text)

def keys(members: tuple[type, ...]) -> tuple[str, ...]:
    return DeclaredLabel.keys_of(members)

def listing(members: tuple[type, ...]) -> str:
    return DeclaredLabel.listing_of(members)

def definitions(members: tuple[type, ...]):
    return DeclaredLabel.definitions_of(members)
