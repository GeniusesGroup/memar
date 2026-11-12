#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
from typing import Protocol

Priority_Rank = import_module('modules-plugable.identity.thing.priority.primitive.rank').Priority_Rank


class RankStore(Protocol):
    def get_rank(self, thing: object) -> Priority_Rank | None: ...

    def put_rank(self, thing: object, rank: Priority_Rank) -> None: ...


class MemoryRankStore:

    def __init__(self) -> None:
        self.held: dict[object, Priority_Rank] = {}

    def get_rank(self, thing: object) -> Priority_Rank | None:
        return self.held.get(thing)

    def put_rank(self, thing: object, rank: Priority_Rank) -> None:
        self.held[thing] = Priority_Rank(int(rank))
