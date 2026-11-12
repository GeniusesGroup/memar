#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module

Priority_Rank = import_module('modules-plugable.identity.thing.priority.primitive.rank').Priority_Rank
FACT = 'priority_rank'


class FactsRankStore:

    def __init__(self, facts, project=None) -> None:
        self.facts = facts
        self.project = project

    def get_rank(self, thing: str) -> Priority_Rank | None:
        text, _ = self.facts.read_priority_rank(self.project, thing)
        if text is None or text == '':
            return None
        return Priority_Rank.read(str(text))

    def put_rank(self, thing: str, rank: Priority_Rank) -> None:
        from machine.console import fail
        fail('priority rank belongs on the thing graph, not in task facts')
