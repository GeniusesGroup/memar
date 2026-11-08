#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
import argparse
from typing import Callable
COMMAND = 'get-rules-for-subject'
NONE = 'no rule has a word of the subject; search the documents with `memar content find` and `memar content search`'
WHY_LIMIT = 160
HEADER = 'Rules that bear on the subject, best first; open and follow the ones that govern your step:'

def text_of(hits) -> str:
    if not hits:
        return NONE
    return '\n'.join([HEADER] + [f'/{hit.document}#{hit.anchor} | {hit.why[:WHY_LIMIT]}' for hit in hits])

def describe(verbs) -> Callable[[argparse.Namespace], None]:
    rules = verbs.add_parser(COMMAND, help='print the rules that bear on the subject of the step about to be taken', description="Print the rules that bear on a subject, best first, one line each: the rule's link, its section and its Why. Call it with the subject of a step before taking the step, and open and follow the rules that govern it. It prints no rule's text, so what enters your context is what you open. A rule is a content that carries the label rule, here every rule document in a `rules` folder; ranking is by word similarity and a declared label named in the subject puts its rules first. Writes nothing.\n\nComposition is owned by agency (`Rule_Delivery`); this verb is the stable command face.")
    rules.add_argument('subject', help='the subject of the step, in words')
    return run

def run(args: argparse.Namespace) -> None:
    _fr = import_module('modules.process.rule.services.find_rules')
    _rd = import_module('modules-plugable.management.agency.widgets.rule_delivery.rule_delivery')
    _ref = import_module('modules.knowledge.content.services.reference')
    _dl = import_module('modules.knowledge.label.primitive.declared_label')
    delivery = _rd.RuleDelivery(_fr.FindRules(_ref.content_root()), lambda: tuple((label.title for label in _dl.DeclaredLabel.all_declared())))
    print(text_of(delivery.for_subject(args.subject)))
