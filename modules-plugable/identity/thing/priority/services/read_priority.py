#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
from modules.knowledge.label.primitive.label_store import LabelStore

Label_Priority = import_module('modules-plugable.identity.thing.priority.labels.Priority').Label_Priority
Priority_Rank = import_module('modules-plugable.identity.thing.priority.primitive.rank').Priority_Rank
RankStore = import_module('modules-plugable.identity.thing.priority.services.rank_store').RankStore
SERVICE_UUID = '70cd58f2-61bc-5813-8ec3-4cde61e0a53b'


def read_priority(labels: LabelStore, ranks: RankStore, thing: object) -> tuple[Priority_Rank, bool]:
    held = ranks.get_rank(thing)
    if held is not None:
        return held, True
    wanted = Label_Priority.as_label
    if any(item.id == wanted.id for item in labels.get(thing)):
        return Priority_Rank.of_absent(), True
    return Priority_Rank.of_absent(), False


def rank(labels: LabelStore, ranks: RankStore, thing: object) -> int:
    value, _ = read_priority(labels, ranks, thing)
    return int(value)
