#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
from modules.knowledge.label.primitive.label_store import LabelStore

Label_Priority = import_module('modules-plugable.identity.thing.priority.labels.Priority').Label_Priority
Priority_Rank = import_module('modules-plugable.identity.thing.priority.primitive.rank').Priority_Rank
RankStore = import_module('modules-plugable.identity.thing.priority.services.rank_store').RankStore
attach = import_module('modules.knowledge.label.services.attach-label.attach_label').attach
SERVICE_UUID = 'f28f2eba-6923-5e6c-814d-92ca70b4d97e'


def set_priority(labels: LabelStore, ranks: RankStore, thing: object, value: str | int) -> None:
    rank = Priority_Rank.checked(value)
    attach(labels, thing, Label_Priority.as_label)
    ranks.put_rank(thing, rank)
