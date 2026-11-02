#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Which declared labels take a given label — in-memory, not a store walk.

Backed by `DeclaredLabel`'s registry: a Label_* is visible once its module is
imported. Prefer asking the kind itself (`Label_Status.members()`) when the
kind owns the query. This service is the store-free form of that question for
callers that already hold the kind type.
"""
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel

def taking(kind: type) -> tuple[type, ...]:
    """Every imported Label_* whose definition takes KIND."""
    return DeclaredLabel.taking(kind)

def whose_kinds_include(members: tuple[type, ...], word: str) -> tuple[type, ...]:
    wanted = word if isinstance(word, str) else getattr(word, 'word', str(word))
    return tuple(member for member in members if wanted in getattr(member, 'kinds', ()))

def read(members: tuple[type, ...], text: str):
    return DeclaredLabel.read_among(members, text)

def keys(members: tuple[type, ...]) -> tuple[str, ...]:
    return DeclaredLabel.keys_of(members)

def listing(members: tuple[type, ...]) -> str:
    return DeclaredLabel.listing_of(members)

def definitions(members: tuple[type, ...]):
    return DeclaredLabel.definitions_of(members)
