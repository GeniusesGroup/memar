#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
import re
from typing import Callable
MOST = 8
WORD = re.compile(r'[a-z0-9][a-z0-9_-]*')
COMMAND = 'get-rules-for-subject'
NONE = 'no rule has a word of the subject; search the documents with `memar content_find` and `memar content_search`'
WHY_LIMIT = 160
HEADER = 'Rules that bear on the subject, best first; open and follow the ones that govern your step:'


class RuleDelivery:

    def __init__(self, find, titles: Callable[[], tuple[str, ...]]) -> None:
        self._find = find
        self._titles = titles

    def for_subject(self, subject: str) -> list:
        if not subject.strip():
            raise ValueError('subject')
        declared = {title.lower() for title in self._titles()}
        topics: list[str] = []
        for word in WORD.findall(subject.lower()):
            if word in declared and word not in topics:
                topics.append(word)
        return self._find.do(subject, topics, MOST)


def text_of(hits) -> str:
    if not hits:
        return NONE
    return '\n'.join([HEADER] + [f'/{hit.document}#{hit.anchor} | {hit.why[:WHY_LIMIT]}' for hit in hits])


def rules_for_subject(subject: str) -> str:
    _fr = import_module('modules.process.rule.services.find_rules')
    _ref = import_module('modules.knowledge.content.services.reference')
    _dl = import_module('modules.knowledge.label.primitive.declared_label')
    delivery = RuleDelivery(_fr.FindRules(_ref.content_root()), lambda: tuple((label.title for label in _dl.DeclaredLabel.all_declared())))
    return text_of(delivery.for_subject(subject))

declare = import_module('modules.process.service.primitive.declaration').declare
DECLARATIONS = (
    declare(
        rules_for_subject,
        name=COMMAND,
        summary='print the rules that bear on the subject of the step about to be taken',
        description="Print the rules that bear on a subject, best first, one line each: the rule's link, its section and its Why. Call it with the subject of a step before taking the step, and open and follow the rules that govern it. It prints no rule's text, so what enters your context is what you open. A rule is a content that carries the label rule, here every rule document in a `rules` folder; ranking is by word similarity and a declared label named in the subject puts its rules first. Writes nothing.",
        help={'subject': 'the subject of the step, in words'},
    ),
)
